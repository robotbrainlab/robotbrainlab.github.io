/* Mermaid rendering — vendored, offline, theme-aware.
   The canonical diagram source stays in the page: if rendering fails or
   JavaScript is unavailable, the text form remains visible. */
(function () {
  "use strict";

  var script = document.currentScript;
  var mermaidSrc = script ? script.getAttribute("data-mermaid-src") : null;
  var figures = Array.prototype.slice.call(document.querySelectorAll("[data-diagram]"));
  if (!figures.length || !mermaidSrc) return;

  var loading = null;
  var counter = 0;

  function readTokens() {
    var styles = getComputedStyle(document.documentElement);
    function token(name, fallback) {
      var value = styles.getPropertyValue(name);
      return (value && value.trim()) || fallback;
    }
    var line = token("--rule-strong", "#888");
    return {
      background: token("--surface", "#fff"),
      primaryColor: token("--panel", "#f4f1eb"),
      primaryTextColor: token("--head", "#15181d"),
      primaryBorderColor: line,
      secondaryColor: token("--panel-strong", "#ece7de"),
      secondaryTextColor: token("--head", "#15181d"),
      secondaryBorderColor: line,
      tertiaryColor: token("--bg", "#fbfaf7"),
      tertiaryTextColor: token("--text", "#24272c"),
      tertiaryBorderColor: line,
      lineColor: token("--muted", "#5c636d"),
      textColor: token("--text", "#24272c"),
      mainBkg: token("--panel", "#f4f1eb"),
      nodeBorder: line,
      nodeTextColor: token("--head", "#15181d"),
      clusterBkg: token("--bg", "#fbfaf7"),
      clusterBorder: token("--rule-mid", "#d6d0c5"),
      titleColor: token("--head", "#15181d"),
      edgeLabelBackground: token("--bg", "#fbfaf7"),
      fontFamily: token("--font-sans", "system-ui, sans-serif"),
      fontSize: "14px"
    };
  }

  function configure() {
    window.mermaid.initialize({
      startOnLoad: false,
      securityLevel: "strict",
      theme: "base",
      themeVariables: readTokens(),
      flowchart: { useMaxWidth: true, htmlLabels: true, curve: "basis" }
    });
  }

  function loadMermaid() {
    if (loading) return loading;
    loading = new Promise(function (resolve, reject) {
      if (window.mermaid) { resolve(window.mermaid); return; }
      var tag = document.createElement("script");
      tag.src = mermaidSrc;
      tag.onload = function () { resolve(window.mermaid); };
      tag.onerror = function () { reject(new Error("Mermaid could not be loaded")); };
      document.head.appendChild(tag);
    });
    return loading;
  }

  function sourceOf(figure) {
    var pre = figure.querySelector(".diagram-source");
    return pre ? pre.textContent : "";
  }

  function showError(figure, message) {
    if (figure.querySelector(".diagram-error")) return;
    var note = document.createElement("p");
    note.className = "diagram-error";
    note.setAttribute("data-chrome", "");
    note.textContent = message;
    figure.insertBefore(note, figure.firstChild);
  }

  function renderFigure(figure) {
    if (figure.dataset.state === "done" || figure.dataset.state === "busy") return Promise.resolve();
    figure.dataset.state = "busy";
    var source = sourceOf(figure);
    counter += 1;
    var id = "mermaid-" + counter;
    return window.mermaid.render(id, source).then(function (result) {
      var host = figure.querySelector(".diagram-svg");
      if (!host) {
        host = document.createElement("div");
        host.className = "diagram-svg";
        // The figure scrolls sideways on a narrow screen: make that scroll reachable
        // from the keyboard, as the wide tables already are.
        host.setAttribute("role", "group");
        host.setAttribute("tabindex", "0");
        var figureLabel = figure.getAttribute("aria-label");
        if (figureLabel) host.setAttribute("aria-label", figureLabel);
        figure.insertBefore(host, figure.firstChild);
      }
      host.innerHTML = result.svg;
      var svg = host.querySelector("svg");
      if (svg) {
        svg.setAttribute("role", "img");
        var label = figure.getAttribute("aria-label");
        if (label) svg.setAttribute("aria-label", label);
        var box = svg.viewBox && svg.viewBox.baseVal ? svg.viewBox.baseVal.width : 0;
        if (box > figure.clientWidth) figure.classList.add("breakout");
      }
      var pre = figure.querySelector(":scope > .diagram-source");
      if (pre) {
        var details = document.createElement("details");
        details.className = "diagram-text";
        details.setAttribute("data-chrome", "");
        var summary = document.createElement("summary");
        summary.textContent = "Diagram as text";
        details.appendChild(summary);
        details.appendChild(pre);
        figure.appendChild(details);
      }
      figure.classList.add("is-rendered");
      figure.dataset.state = "done";
    }, function () {
      figure.dataset.state = "error";
      showError(figure, "This diagram could not be rendered. Its source is shown below.");
    });
  }

  function rerender() {
    if (!window.mermaid) return;
    configure();
    figures.forEach(function (figure) {
      if (figure.dataset.state !== "done") return;
      var details = figure.querySelector(".diagram-text");
      var pre = figure.querySelector(".diagram-source");
      if (details && pre) {
        figure.insertBefore(pre, figure.firstChild);
        details.remove();
      }
      figure.dataset.state = "";
      figure.classList.remove("is-rendered");
      renderFigure(figure);
    });
  }

  function start(figure) {
    loadMermaid().then(function (mermaid) {
      if (!mermaid) return;
      if (!start.configured) { configure(); start.configured = true; }
      renderFigure(figure);
    }, function () {
      showError(figure, "Diagram rendering is unavailable. The source is shown below.");
    });
  }

  if ("IntersectionObserver" in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        observer.unobserve(entry.target);
        start(entry.target);
      });
    }, { rootMargin: "400px 0px" });
    figures.forEach(function (figure) { observer.observe(figure); });
  } else {
    figures.forEach(start);
  }

  document.addEventListener("themechange", rerender);
})();
