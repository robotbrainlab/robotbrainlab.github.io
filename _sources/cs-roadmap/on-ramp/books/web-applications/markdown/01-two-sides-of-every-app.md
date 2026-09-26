# Two Sides of Every App

This chapter gives you the one picture the rest of the book hangs on. Every app you use has two sides: one in your hand, and one far away. The two sides talk by passing messages. By the end of the chapter you will know what each side is called and how their conversation works.

*The problem.* I tap a button, and something happens far away.

*The question.* What is on the other end of my tap, and how do the two ends talk?

## One App, Two Places

You open a food delivery app, pick a pizza, and tap *Order*. A few seconds later the screen says "Order placed." In between, the restaurant received your order, a driver was found, and your card was charged. None of that happened on your phone. Your phone doesn't know which drivers are free, and it can't charge a card by itself.

So the app you "use" is really two programs. One runs on your phone. The other runs on the delivery company's computers, often hundreds of kilometres away. Together they make one **web application**: a program split between your device and a computer on the internet, with the two halves talking over the network. Email, maps, banking, social media, and online shopping all work this way.

## The Restaurant Picture

A restaurant has two areas. The *front of house* is the dining room: tables, menus, waiters. Everything there is designed for you. The *back of house* is the kitchen. You never go there, but that is where the food, the recipes, and the cooks are.

Apps are built the same way, and developers even use the same words:

- The **front end** is the part you see and touch: screens, buttons, text boxes. It runs on your device.
- The **back end** is the part you never see: the program that keeps the data, applies the rules, and does the real work. It runs on the company's computers.

A waiter carries orders to the kitchen and plates back to the table. In an app, messages sent over the internet do the carrying.

> **Note:** You will also see "frontend", "client side", "backend", and "server side". They mean the same two things.

## Client and Server

Two more words describe the *roles* in the conversation:

- The **client** is the program that asks. Your phone app is a client. So is a web browser.
- The **server** is the program that answers. It waits for questions, day and night, from many clients at once. People also say "server" for the computer it runs on.

One kitchen feeds every table, and one back end serves millions of phones. That is why shared data lives on the server: it is the one place every client can reach. Your friend sees your new photo because the photo is stored on the server, not on your phone.

## The Request and Response Loop

Client and server talk in a strict pattern. The client sends a **request**: a message saying what it wants. The server sends back a **response**: a message with the answer. One request plus its response is a **round trip**.

```text
  ┌──────────────┐     request      ┌──────────────┐
  │    Client    │ ───────────────► │    Server    │
  │ (front end)  │                  │  (back end)  │
  │ your device  │ ◄─────────────── │  far away    │
  └──────────────┘     response     └──────────────┘
```

Three rules hold for almost every round trip:

1. *The client speaks first.* The server answers questions; it doesn't start conversations.
2. *Every request gets one response*, even if the answer is "no" or "something broke".
3. *Each round trip stands alone.* The server treats every request as a fresh message. (Chapter 3 shows how it still remembers who you are.)

Here is the pizza order as a round trip:

- Request: "Place an order: one margherita, to 12 Park Road, paid with the saved card."
- Response: "Done. Order number 5531. The driver arrives in 25 minutes."

Then the app shows the result on your screen. That is the whole shape of a web application: *tap, request, work, response, show.* The rest of this book fills in each step.

## Why Split an App at All?

Why not put everything on the phone? Four reasons:

- *Sharing.* Data that many people need must live in one place everyone can reach.
- *Trust.* You control what runs on your own phone. A rule like "charge the card only after the restaurant accepts" must run where customers can't tamper with it.
- *Power.* A server can search millions of restaurants in a blink. A phone has a small battery.
- *Updates.* Fix a bug on the server once, and every user gets the fix at the same moment.

The price of the split: the two sides must be able to reach each other. No network, no app. You have seen this price as "No internet connection."

## Try It

You can watch round trips happen. Your browser has **developer tools**: a built-in panel that shows what a web page is doing behind the scenes.

1. Open any news website in Chrome, Edge, or Firefox on a computer.
2. Open the developer tools: press F12 (Windows, Linux) or Cmd+Option+I (Mac), or right-click the page and choose *Inspect*.
3. Click the *Network* tab, then reload the page.

*Expected result:* The panel fills with a long list, often over a hundred lines. Each line is one round trip. The *Status* column shows numbers such as `200`, which means "OK", and the bar at the bottom counts the requests. One page, loaded by one click, needed all of them.

## Summary, Key Terms, and Review Questions

### Summary

- A web application is split in two: a front end on your device and a back end on the company's computers.
- The client asks and the server answers. One server answers many clients.
- Client and server talk in round trips: one request, one response.
- Apps are split for sharing, trust, power, and easy updates. The cost is that both sides need the network.

### Key Terms

| Term | Meaning |
|---|---|
| Web application | A program split between your device and a server |
| Front end | The part you see and touch |
| Back end | The hidden part that keeps data and does the work |
| Client | The program that asks |
| Server | The program that answers |
| Request | The message the client sends |
| Response | The message the server sends back |
| Round trip | One request plus its response |
| Developer tools | The browser panel that shows what a page is doing |

### Review Questions

1. Using the restaurant picture, explain the front end and the back end.
2. Why does your friend's phone show a photo you uploaded from your phone?
3. Walk through "tap, request, work, response, show" for sending a chat message.
4. Give two reasons a rule like "charge the card" runs on the server, not the phone.

> **You understand this when** you can pick any app on your phone and say which of its jobs happen on your device and which happen far away.
