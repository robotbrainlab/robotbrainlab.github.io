/* AI Engineer Roadmap — progressive enhancements.
   Everything here is optional: the page is complete without JavaScript.
   Classic script, no modules, no network requests. */
(function () {
  "use strict";

  var root = document.documentElement;
  var live = document.getElementById("live-region");

  function announce(message) {
    if (!live) return;
    live.textContent = "";
    window.setTimeout(function () { live.textContent = message; }, 30);
  }

  /* ---------------------------------------------------------- theme */

  var THEMES = ["system", "light", "dark"];
  var LABELS = { system: "System", light: "Light", dark: "Dark" };

  function storedTheme() {
    try {
      var value = localStorage.getItem("air-theme");
      return THEMES.indexOf(value) > -1 ? value : "system";
    } catch (e) { return "system"; }
  }

  function applyTheme(theme) {
    if (theme === "system") root.removeAttribute("data-theme");
    else root.setAttribute("data-theme", theme);
    var button = document.querySelector("[data-theme-toggle]");
    if (button) {
      var label = button.querySelector(".theme-label");
      if (label) label.textContent = LABELS[theme];
      button.setAttribute("aria-label", "Theme: " + LABELS[theme] + ". Activate to change.");
    }
    document.dispatchEvent(new CustomEvent("themechange", { detail: { theme: theme } }));
  }

  var theme = storedTheme();
  applyTheme(theme);

  var themeButton = document.querySelector("[data-theme-toggle]");
  if (themeButton) {
    themeButton.addEventListener("click", function () {
      theme = THEMES[(THEMES.indexOf(theme) + 1) % THEMES.length];
      try { localStorage.setItem("air-theme", theme); } catch (e) {}
      applyTheme(theme);
      announce("Theme: " + LABELS[theme]);
    });
  }

  if (window.matchMedia) {
    var query = window.matchMedia("(prefers-color-scheme: dark)");
    var onSystemChange = function () { if (theme === "system") applyTheme("system"); };
    if (query.addEventListener) query.addEventListener("change", onSystemChange);
    else if (query.addListener) query.addListener(onSystemChange);
  }

  /* --------------------------------------------------------- drawers */

  var scrim = document.querySelector("[data-scrim]");
  var openDrawer = null;
  var lastTrigger = null;

  function closeDrawer() {
    if (!openDrawer) return;
    openDrawer.classList.remove("is-open");
    var toggles = document.querySelectorAll('[data-drawer-toggle="' + openDrawer.id + '"]');
    for (var i = 0; i < toggles.length; i++) toggles[i].setAttribute("aria-expanded", "false");
    if (scrim) scrim.hidden = true;
    var main = document.getElementById("main");
    if (main) main.removeAttribute("inert");
    openDrawer = null;
    if (lastTrigger) { lastTrigger.focus(); lastTrigger = null; }
  }

  function showDrawer(panel, trigger) {
    if (!panel) return;
    if (openDrawer && openDrawer !== panel) closeDrawer();
    openDrawer = panel;
    lastTrigger = trigger || null;
    panel.classList.add("is-open");
    if (trigger) trigger.setAttribute("aria-expanded", "true");
    if (scrim) scrim.hidden = false;
    var focusable = panel.querySelector("a, button");
    if (focusable) focusable.focus();
  }

  document.addEventListener("click", function (event) {
    var toggle = event.target.closest ? event.target.closest("[data-drawer-toggle]") : null;
    if (toggle) {
      var panel = document.getElementById(toggle.getAttribute("data-drawer-toggle"));
      if (panel === openDrawer) closeDrawer();
      else showDrawer(panel, toggle);
      return;
    }
    if (event.target.closest && event.target.closest("[data-drawer-close]")) {
      closeDrawer();
      return;
    }
    if (openDrawer && event.target === scrim) closeDrawer();
    if (openDrawer && event.target.closest && event.target.closest("a") && openDrawer.contains(event.target)) {
      closeDrawer();
    }
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && openDrawer) closeDrawer();
  });

  window.addEventListener("resize", function () {
    if (openDrawer && window.innerWidth >= 1280) closeDrawer();
  });

  /* ------------------------------------------------- on this page rail */

  /* Highlights the entry for the section being read. Used by the right rail
     and by the Roadmap's outline in the left rail. */
  function scrollSpy(links, railSelector, itemSelector, minWidth) {
    var targets = [];
    links.forEach(function (link) {
      var href = link.getAttribute("href");
      var hash = href.indexOf("#");
      if (hash < 0) return;
      var heading = document.getElementById(decodeURIComponent(href.slice(hash + 1)));
      if (heading) targets.push({ link: link, heading: heading });
    });
    if (!targets.length) return;
    targets.sort(function (a, b) {
      return a.heading.compareDocumentPosition(b.heading) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1;
    });

    var rail = document.querySelector(railSelector);
    var current = null;

    function setActive(entry) {
      if (entry === current) return;
      if (current) {
        current.link.classList.remove("is-active");
        current.link.removeAttribute("aria-current");
        var openItem = itemSelector && current.link.closest(itemSelector);
        if (openItem) openItem.classList.remove("is-open");
      }
      current = entry;
      if (!entry) return;
      entry.link.classList.add("is-active");
      entry.link.setAttribute("aria-current", "location");
      var item = itemSelector && entry.link.closest(itemSelector);
      if (item) item.classList.add("is-open");
      if (rail && rail.scrollHeight > rail.clientHeight && window.innerWidth >= minWidth) {
        var linkTop = entry.link.offsetTop;
        if (linkTop < rail.scrollTop || linkTop > rail.scrollTop + rail.clientHeight - 80) {
          rail.scrollTop = Math.max(0, linkTop - rail.clientHeight / 2);
        }
      }
    }

    var ticking = false;
    function updateActive() {
      ticking = false;
      var line = window.innerHeight * 0.28;
      var found = null;
      for (var i = 0; i < targets.length; i++) {
        if (targets[i].heading.getBoundingClientRect().top <= line) found = targets[i];
        else break;
      }
      setActive(found || (itemSelector ? targets[0] : null));
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(updateActive); }
    }, { passive: true });
    updateActive();
  }

  scrollSpy(Array.prototype.slice.call(document.querySelectorAll(".page-toc [data-toc-link]")),
            ".toc-rail", ".toc-item", 1024);
  scrollSpy(Array.prototype.slice.call(document.querySelectorAll(".area-nav [data-toc-link]")),
            ".sidebar", null, 1280);

  /* ------------------------------------------------- heading anchors */

  document.addEventListener("click", function (event) {
    var anchor = event.target.closest ? event.target.closest(".heading-anchor") : null;
    if (!anchor || !navigator.clipboard) return;
    var url = anchor.href;
    navigator.clipboard.writeText(url).then(function () {
      announce("Link copied");
    }, function () {});
  });

  /* ------------------------------------------------------ code copy */

  Array.prototype.forEach.call(document.querySelectorAll(".code-block"), function (block) {
    var meta = block.querySelector(".code-meta");
    var code = block.querySelector("pre.code");
    if (!meta || !code || !navigator.clipboard) return;
    var button = document.createElement("button");
    button.type = "button";
    button.className = "code-copy";
    button.textContent = "Copy";
    button.addEventListener("click", function () {
      navigator.clipboard.writeText(code.innerText).then(function () {
        button.textContent = "Copied";
        announce("Code copied");
        window.setTimeout(function () { button.textContent = "Copy"; }, 1600);
      }, function () {});
    });
    meta.appendChild(button);
  });

  /* ------------------------------------------------------- back to top */

  var toTop = document.querySelector("[data-to-top]");
  if (toTop) {
    var toggleTop = function () {
      if (window.scrollY > window.innerHeight * 0.75) toTop.classList.add("is-visible");
      else toTop.classList.remove("is-visible");
    };
    window.addEventListener("scroll", toggleTop, { passive: true });
    toggleTop();
  }

  /* ------------------------------------- scrollable regions and print */

  function markScrollables() {
    Array.prototype.forEach.call(document.querySelectorAll(".table-wrap"), function (wrap) {
      if (wrap.scrollWidth > wrap.clientWidth + 2) wrap.setAttribute("tabindex", "0");
      else wrap.removeAttribute("tabindex");
    });
  }
  markScrollables();
  window.addEventListener("resize", markScrollables);

  var reopen = [];
  window.addEventListener("beforeprint", function () {
    reopen = [];
    Array.prototype.forEach.call(document.querySelectorAll("details:not([open])"), function (details) {
      details.open = true;
      reopen.push(details);
    });
  });
  window.addEventListener("afterprint", function () {
    reopen.forEach(function (details) { details.open = false; });
    reopen = [];
  });
})();
