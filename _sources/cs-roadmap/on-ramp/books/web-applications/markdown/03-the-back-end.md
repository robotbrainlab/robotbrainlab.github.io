# The Back End: What Runs Where You Can't See

This chapter walks into the kitchen: what the back end does with each request, where your data ends up, how the server remembers you, and how the two sides agree on what they may ask each other.

*The problem.* Where does my data go when I press Save?

*The question.* What happens on the far side of the app, and how does it keep my data and remember me?

## A Computer That Never Sleeps

A back end runs on a server: usually a computer with no screen in a *data centre*, a warehouse full of such computers. Most companies rent these machines from a cloud company.

The back-end program *listens*: it waits for a request, answers it, and waits again. For each request it does three jobs, like a kitchen handling an order slip:

1. *Routing:* send the order to the right station. Which piece of code handles "save a note"?
2. *Business logic:* follow the recipe and the house rules. Is this allowed? Does it make sense?
3. *Storing and fetching:* get ingredients from the store room. Read or write the database.

Then it builds a response and sends it back.

## Back-End Frameworks

Every back end needs the same plumbing: receive requests, find the right code, send responses. A **back-end framework** provides it, so developers write only what is special to their app. Here is a complete, tiny back end written with FastAPI, a Python framework:

```python
from fastapi import FastAPI

app = FastAPI()
notes = []  # the app's memory, for now

@app.post("/notes")
def save_note(note: dict):
    notes.append(note["text"])
    return {"saved": True, "count": len(notes)}

@app.get("/notes")
def list_notes():
    return {"notes": notes}
```

The two functions are ordinary Python. The line above each, starting with `@`, is a **route**: it tells the framework, "when a request to save a note (`POST /notes`) arrives, run this function." A function that answers a request is a **handler**. Whatever it returns becomes the response.

You don't need to run this; it is here to show how small a handler can be. Saved as `app.py` and started with `uvicorn app:app` (a program that runs FastAPI apps), it listens on your own computer, called `localhost`. `curl`, a terminal program that sends one request and prints the response, can then play the client:

```bash
curl -X POST http://localhost:8000/notes \
  -H "Content-Type: application/json" \
  -d '{"text": "Buy milk"}'
```

```text
{"saved":true,"count":1}
```

## Business Logic: The House Rules

The **business logic** is the set of rules that makes an app *this* app:

- A cinema can't sell the same seat twice.
- A bank can't let you send more money than you have.
- Only the person who wrote a post can edit it.
- The shop, not your browser, adds up the price of your cart.

These rules live on the back end because it is the one place the company fully controls.

## The Database: Where Your Data Lives

Our tiny back end keeps notes in a Python list. Stop the server, start it again, and ask for the list:

```bash
curl http://localhost:8000/notes
```

```text
{"notes":[]}
```

The milk is gone: a list in memory vanishes when the program stops. Real apps use a **database**: a program built to keep data safely on disk, find any piece of it quickly, and let many users read and write at once. Picture a huge filing room with a fast, careful clerk. PostgreSQL, MySQL, and MongoDB are well-known ones.

So here is the answer to this chapter's problem. When you press Save, your data travels to the back end, which checks it against the rules and hands it to the database. Your phone may keep a copy for speed, but the real copy lives there.

## How the Server Remembers You

The server greets every request like a stranger. So how does it know this request comes from *you*, who logged in ten minutes ago?

Think of a cloakroom. You hand over your coat and get a numbered ticket. Later you show the ticket, not your face, and get your coat back.

When you log in, the back end checks your password and writes down a **session**: a record saying "ticket 7f3a9c belongs to Priya, logged in at 9:14." It gives the ticket to your browser as a **cookie**: a small piece of text the browser stores and sends back with every later request to that site. Mobile apps use a similar ticket, usually called a token.

> **Warning:** Whoever holds your ticket *is* you, as far as the server knows. Never paste cookie values anywhere, and log out on shared computers: that tears up the ticket.

## APIs: The Contract Between the Two Sides

The front end and the back end are often built by different people. They need an agreement: which requests the back end accepts, what each must contain, and what comes back. That agreement is the **API** (Application Programming Interface). Each thing it offers, such as "save a note" at `POST /notes`, is an **endpoint**. The data usually travels as **JSON**: plain text that looks almost exactly like a Python dictionary, such as `{"text": "Buy milk"}`.

The API is the restaurant's menu. As long as the menu stays the same, the kitchen can buy new stoves and the dining room can be repainted without breaking each other. And a website, an iPhone app, and an Android app can share one back end: they all order from the same menu.

## Try It

Look at the cloakroom tickets your browser holds for a site.

1. Open a private (incognito) window and log in to a site you use, such as web email.
2. Open the developer tools. In Chrome or Edge, go to *Application*, then *Cookies*; in Firefox, *Storage*, then *Cookies*. Click the site's name.
3. Right-click the site's name, choose *Clear* (Chrome, Edge) or *Delete All* (Firefox), and reload the page.

*Expected result:* In step 2 you see several cookies, each a name and a value; the login one usually has a long, random value. In step 3 you are suddenly logged out: you threw away your tickets, so the server no longer knows you.

## Summary, Key Terms, and Review Questions

### Summary

- A back end listens for requests on a server. For each one it routes, applies business logic, and reads or writes the database.
- Back-end frameworks provide the plumbing; developers write handlers.
- Data in memory vanishes; a database keeps it safe and shared.
- A session and a cookie let the server know who you are on every request.
- The API is the contract between the two sides, usually spoken in JSON.

### Key Terms

| Term | Meaning |
|---|---|
| Back-end framework | Ready-made plumbing for answering requests |
| Route | A rule linking a kind of request to its handler |
| Handler | A function that answers one kind of request |
| Business logic | The app's own rules |
| Database | A program that stores data safely and shares it |
| Session | The server's record of who is logged in |
| Cookie | A small piece of text the browser keeps and sends back |
| API | The agreement on what the front end may ask the back end |
| Endpoint | One thing an API offers, such as `POST /notes` |
| JSON | A plain-text data format, like a Python dictionary |

### Review Questions

1. What three jobs does a back end do for every request?
2. In the tiny FastAPI app, what is the route and what is the handler for saving a note?
3. Why did the note disappear when the server restarted, and what fixes that?
4. Explain sessions and cookies using the cloakroom picture.
5. How can a company rebuild its back end without breaking the apps that use it?

> **You understand this when** you can answer "where does my data go when I press Save?" for any app, naming the handler, the rules it checks, and the database, and explain how the server knows it was you.
