# The Front End: What Runs on Your Screen

This chapter looks at the side of the app you can see: who draws the screen, the three languages every web page is made of, what a front-end framework adds, and why a phone app is a front end too.

*The problem.* The same app looks right on my laptop and my phone, but who draws it?

*The question.* How does an app become the picture on my screen, and how does that picture fit every size of screen?

## The Server Sends Instructions, Not a Picture

When you open a website, the server does not send a finished picture of the page. It sends *instructions*, and your device draws the page itself.

Think of flat-pack furniture. The shop doesn't deliver a built bookcase. It sends the parts and an instruction sheet, and you assemble it at home. A good sheet even says: "If your wall is narrow, stack the shelves in one column."

The program that does the assembling is the **browser**: Chrome, Safari, Firefox, or Edge. It downloads the instructions, follows them, and draws the result. That is why the same app looks right on a laptop and a phone: each device builds the page to fit its own screen.

## Three Languages, Three Jobs

The instructions come in three languages:

| Language | Its job | In the furniture picture |
|---|---|---|
| **HTML** | What is on the page: text, buttons, images | The list of parts |
| **CSS** | How it looks: colours, fonts, layout | The paint and arrangement |
| **JavaScript** | What happens when you touch it | The drawers that slide |

Here is a tiny but complete page that uses all three:

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    h1 { font-family: sans-serif; }
    button { background: royalblue; color: white; }
  </style>
</head>
<body>
  <h1>My Notes</h1>
  <button id="save">Save</button>
  <p id="status"></p>
  <script>
    const button = document.getElementById("save");
    button.onclick = function () {
      document.getElementById("status").textContent = "Saved!";
    };
  </script>
</body>
</html>
```

The CSS inside `<style>` makes the heading plain and the button blue. The HTML inside `<body>` lists a heading, a button, and an empty paragraph. The JavaScript inside `<script>` says: when someone clicks the button, put *Saved!* in the empty paragraph. Open this file in a browser and click *Save*, and *Saved!* appears under the button.

> **Note:** This button is a fake. It changed the page, but nothing left your computer, so nothing was saved. A real Save button must send a request to a back end. Chapter 4 shows this same button doing exactly that.

## One Page, Every Screen

A phone screen is narrow; a laptop screen is wide. Designers don't build two websites. They write CSS rules that change the layout to fit the space: "on a wide screen, show the menu on the left; on a narrow one, hide it behind a button." This is **responsive design**: the "stack the shelves if the wall is narrow" line of the instruction sheet.

## Front-End Frameworks

The example page has one button. An online shop has thousands, and changing one number can mean five places on the screen must change with it. Doing that by hand in JavaScript is slow and error-prone.

A **front-end framework** is ready-made code that does this bookkeeping. React, Vue, Angular, and Svelte are well-known ones. The developer describes what the screen should look like for the current data ("the cart shows these three items"), and the framework updates the page whenever the data changes.

Frameworks build screens from **components**: small, reusable pieces such as a product card or a like button. Like building bricks, one component can appear hundreds of times on a page.

> **Note:** A framework helps the developer; it is not a new language for the browser. A React app still reaches your browser as HTML, CSS, and JavaScript, the only three languages a browser draws.

## Mobile Apps Are Front Ends Too

Apps you install from an app store are usually **native apps**: programs written for one kind of phone, in languages like Swift (iPhone) or Kotlin (Android). They draw their own screens without a browser.

The tools differ, but the role is the same. A native app shows screens, reacts to taps, and asks a back end for anything it doesn't have. Often one back end serves the website, the iPhone app, and the Android app together.

## What the Front End Can't Do

Everything in the front end travels to the user's device, where the user can read it and change it. So the front end can't keep secrets, and it can't make final decisions. It can say "this coupon looks valid", but only the back end can accept it.

> **Warning:** Never put a password, a secret key, or a price the customer must not change in front-end code. The back end must check everything the front end sends.

## Try It

See the instructions behind a real page, and change them.

1. Open any website on a computer. Right-click a heading and choose *Inspect*. The *Elements* tab shows the page's HTML, with your heading highlighted.
2. Double-click the heading's text in that panel, type something new, and press Enter. Then reload the page.
3. Click the phone-and-tablet icon at the top of the developer tools (the device toolbar) and pick a phone.

*Expected result:* In step 2 the heading changes to your text, then goes back when you reload. You changed only your own copy of the instructions; the server never knew. In step 3 the page rearranges itself for a narrow screen: responsive design at work.

## Summary, Key Terms, and Review Questions

### Summary

- The server sends instructions; the browser follows them and draws the page.
- HTML says what is on the page, CSS says how it looks, and JavaScript says what it does.
- Responsive design lets one page fit any screen.
- Front-end frameworks keep large screens up to date, built from reusable components.
- Native apps are front ends too, often sharing one back end with the website.
- The front end can't keep secrets or make final decisions.

### Key Terms

| Term | Meaning |
|---|---|
| Browser | The program that downloads and draws web pages |
| HTML | The language for what is on a page |
| CSS | The language for how a page looks |
| JavaScript | The language for what a page does |
| Responsive design | One layout that adapts to any screen size |
| Front-end framework | Ready-made code that keeps a screen in step with its data |
| Component | A small, reusable piece of a screen |
| Native app | An app written for one kind of phone |

### Review Questions

1. Why can the same website look right on a laptop and a phone?
2. For a *Like* button, what does the HTML do, what does the CSS do, and what does the JavaScript do?
3. What problem does a front-end framework solve?
4. In what way is an iPhone app the same thing as a website?
5. Why can't a shop let the front end decide the final price?

> **You understand this when** you can look at any screen in any app and say what the front end drew by itself and what it must have asked the back end for.
