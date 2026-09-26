# Following One Tap from Start to Finish

This chapter puts the two sides together. You will follow one tap on a Save button to the server and back, then meet the common combinations of tools real apps are built from.

*The problem.* I know the two sides now, but not how one tap travels between them.

*The question.* What happens, in order, between tapping Save and seeing "Saved!"?

## The Button, Now for Real

In Chapter 2, the Save button only changed the page. Here is the same button's JavaScript, now talking to the back end from Chapter 3:

```javascript
button.onclick = async function () {
  const response = await fetch("/notes", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({text: "Buy milk"}),
  });
  const data = await response.json();
  document.getElementById("status").textContent =
    "Saved! Notes so far: " + data.count;
};
```

`fetch` sends a request; `await` means "wait here for the response." The last lines put the result on the page: *Saved! Notes so far: 1*. Everything in this chapter happens inside that one `await`.

## The Whole Trip

```text
 FRONT END              BACK END              DATABASE
 (your browser)         (a server)            (the memory)
 ──────────────         ──────────            ────────────
 1 You tap Save
 2 JavaScript builds
   the request
 3 Look up the address
 4 POST /notes ───────► 5 Route to handler,
   + JSON + cookie        check cookie + rules
                        6 Store the note ◄──► saved
 8 Draw "Saved!" ◄───── 7 200 OK + JSON
```

1. *The tap.* The browser notices the click and runs the button's JavaScript.
2. *The request.* JavaScript builds a request: an action (`POST`, meaning "create"), an address, and a JSON body. The browser attaches the site's cookie by itself.
3. *The address.* Every request goes to a **URL**, such as `https://notes.example.com/notes`. The middle part, `notes.example.com`, is a **domain name**: a human-friendly name for the server. Computers really find each other by numbers called **IP addresses**, so the browser asks **DNS**, the internet's phone book, to turn the name into a number. The `https` at the front means **HTTPS**: the request travels sealed, so nobody on the way can read it.
4. *The journey.* The sealed request hops across the internet to the server.
5. *The back end.* The framework matches `POST /notes` to its route and runs the handler, which looks up the cookie to learn who you are and applies the rules.
6. *The database.* The handler asks the database to store the note and waits for "OK".
7. *The response.* The back end sends back a **status code**, a number that says how it went, plus JSON. Here is that response exactly as it arrives, shown by `curl -i` (the `-i` means "include the headers"):

   ```bash
   curl -i -X POST http://localhost:8000/notes \
     -H "Content-Type: application/json" \
     -d '{"text": "Buy milk"}'
   ```

   ```text
   HTTP/1.1 200 OK
   date: Sat, 26 Sep 2026 14:31:05 GMT
   server: uvicorn
   content-length: 24
   content-type: application/json

   {"saved":true,"count":1}
   ```

   The first line is the status. Then come headers, notes about the message. After the blank line comes the body: the handler's JSON.
8. *The drawing.* JavaScript reads the JSON and changes one paragraph. The browser redraws only that part; the page doesn't reload.

The whole trip usually takes a tenth to a third of a second. You feel it as "instant".

> **Tip:** Status codes come in families. Numbers starting with 2 mean success, with 4 mean "your request was wrong" (404 is "not found"), and with 5 mean "the server broke". The first digit tells you which side to blame.

## Common Stacks

Every app picks a front end, a back end, and a database. That combination is its **stack**. The pieces mix freely, because they only talk through requests and responses:

| Stack | Front end | Back end | Database |
|---|---|---|---|
| Python | React or plain HTML | FastAPI or Django | PostgreSQL |
| JavaScript everywhere | React | Node.js with Express | MongoDB |
| Classic "LAMP" | HTML made by PHP | PHP on Linux | MySQL |
| Ruby on Rails | Rails pages | Ruby on Rails | PostgreSQL |
| Mobile | Swift or Kotlin app | Any of the above | Any |

A developer who works on both sides is called a **full-stack developer**. The tools change every few years; the trip you just followed does not.

## Try It

Catch a real request in the act.

1. Open a site with a search box that suggests results as you type, such as an online shop.
2. Open the developer tools, click *Network*, and choose the *Fetch/XHR* filter. This hides images and files and shows only requests made by JavaScript. Clear the list with the clear button.
3. Type one letter into the search box. Click the new request that appears.

*Expected result:* A request appears as you type, with status `200`. *Headers* shows its URL and method, *Response* (or *Preview*) shows JSON holding the suggestions, and *Timing* shows how long the server took. Match each piece to the eight steps above.

## Summary, Key Terms, and Review Questions

### Summary

- A tap runs JavaScript, which builds a request and sends it to a URL.
- DNS turns the domain name into an IP address; HTTPS seals the request for the journey.
- The back end routes the request, checks who you are and the rules, and uses the database.
- The response carries a status code and JSON; JavaScript redraws part of the page.
- A stack is one app's choice of front end, back end, and database.

### Key Terms

| Term | Meaning |
|---|---|
| URL | The full address a request is sent to |
| Domain name | A human-friendly name for a server |
| IP address | The number computers use to find each other |
| DNS | The internet's phone book, from names to numbers |
| HTTPS | The sealed, encrypted way requests travel |
| Status code | A number saying how a request went |
| Stack | An app's front end, back end, and database |
| Full-stack developer | Someone who works on both sides |

### Review Questions

1. List the eight steps between tapping Save and seeing "Saved!".
2. What does DNS do, and why is it needed?
3. What are the three parts of the response shown by `curl -i`?
4. What would a status code of 500 tell you, and what would 404 tell you?
5. Why can a React front end work with a Django back end?

> **You understand this when** you can draw the whole trip from memory for any button in any app, and point to the step where each piece of this book fits.
