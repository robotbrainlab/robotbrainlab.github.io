# How Software Gets Built

### A map of the whole process, before any of its parts

If you have worked on software for a while, you have probably met its pieces one at a time: a ticket here, a deployment there, a meeting about "the API contract," an alert in the middle of the night, a design review. Each one arrives on its own, with its own vocabulary, and nobody explains where it fits. The result is a pile of disconnected facts. You can follow the instructions for each one, but you cannot see the whole.

This chapter gives you the whole first. It is a map of how any piece of software goes from an idea to a working system that people use — and what happens after that. It uses almost no technical vocabulary, because you are not expected to know any yet. Everything in the rest of the book is a closer look at one region of this map, and every part and stage of the book opens by showing you where on the map you are.

The map has three layers:

1. **The loop** — the steps software goes through, in *time*.
2. **The pieces** — what a running application is made of, in *space*.
3. **The people** — who does which part, and what they hand to each other.

Learn these three, and every topic you meet later — in this book or at work — has a place to go.

## The One-Sentence Version

Software is built in a loop: someone decides what is worth building, plans how to build it, builds it, puts it in front of real users, and keeps it working — and what they learn from real use decides what to build next.

That is the whole process. Everything else is detail about one of those steps. A company with a thousand engineers and a student with a weekend project are going around the same loop. The difference is how many people work on each step, and how carefully they hand work from one step to the next.

## Layer 1: The Loop

```text
  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
  │ 1 DISCOVER  │─────▶│   2 PLAN    │─────▶│   3 CODE    │
  │ is this     │      │ how will we │      │ build it,   │
  │ worth doing?│      │ build it?   │      │ test it     │
  └─────────────┘      └─────────────┘      └──────┬──────┘
         ▲                                         │
         │                                         ▼
         │        ┌───────────────────────────────────────────┐
         │        │               4 PRODUCTION                │
         │        │   SHIP  ────────▶  RUN  ────────▶  GROW   │
         │        │   put it in        keep it         when   │
         │        │   front of         working         one is │
         │        │   users                            not    │
         │        │                                    enough │
         │        └─────────────────────┬─────────────────────┘
         │                              │
         └─────────────  LEARN  ◀───────┘
               what real use teaches you
```

The loop has four phases. The first three happen before anyone uses the software; the fourth is where it meets the real world. For each step below you will find the question it answers, what comes into it, what comes out, what goes wrong when it is skipped, and where this book covers it.

### Step 1 — Discover: is this worth building?

Every piece of software starts as someone's idea or request: "customers keep asking for this," "our team wastes hours every week on that." Discovery is the work of checking the idea *before* anyone builds it: who actually has this problem, how badly, what they do about it today, and whether a solution would really be used. It is mostly talking to people, watching them work, and testing cheap sketches — not writing code.

- **Comes in:** an idea, a request, a complaint, a number that looks wrong.
- **Goes out:** a clearly described problem, who has it, and what "solved" will look like.
- **When it is skipped:** the team builds the wrong thing, and builds it well. This is the most expensive mistake in software, because every later step multiplies it.
- **In this book:** Part I, [Product Discovery](product-discovery.md).

### Step 2 — Plan: how will we build it?

Now the question changes from *what* to *how*. Planning turns the problem into things engineers can act on: what the system must do (the **requirements**), what it deliberately will not do (the **scope**), how it will be shaped (the **design**: which pieces, how they talk to each other, where the information lives), how it will be operated once it is live, and in what order the work will happen. The main output is written down — usually as a **design document** — because a plan that lives in one person's head is re-argued every week and lost when that person leaves.

- **Comes in:** the problem, and what "solved" means.
- **Goes out:** a plan — requirements, a design, a list of pieces of work, and the important decisions with their reasons.
- **When it is skipped:** every engineer builds a slightly different idea, the pieces do not fit, and the big decisions get made by accident.
- **In this book:** Part II, [Project Planning](project-planning-guide.md).

### Step 3 — Code: build it

Engineers turn the plan into working code. This is the step most people picture when they think of software engineering — but notice that it is only one of the six steps: discover, plan, code, ship, run and grow. Good teams write code in small pieces. Each piece is checked by automated **tests** (small programs that check the real program behaves as intended) and read by another engineer before it is accepted. Accepted code is kept in one shared place, the **code repository**, which holds every version of the code and is the single truth of what the software is.

- **Comes in:** the plan, broken into small pieces of work.
- **Goes out:** working, tested, reviewed code in the shared repository.
- **When it is done badly:** code that works today but that nobody can safely change tomorrow.
- **In this book:** Part III, [Writing Good Code](writing-good-code.md), for the craft of writing code; and Stages 1 and 9 of Part IV for what the code actually does when it runs.

### Step 4 — Production: make it real

**Production** is the name engineers give to the real world: the place where the software runs for real users, with real data, and where mistakes cost something. Code sitting in a repository helps nobody. Production has three parts.

**Ship — put it in front of users.** The code has to leave the engineer's laptop and run on a computer that is always on and reachable from anywhere. That means packaging it so that it runs the same way everywhere, getting a machine to run it on, putting it there, keeping it running, and connecting it to the internet under a name people can find. Done well, shipping is automatic and boring: a change is approved, and minutes later it is live.

**Run — keep it working.** Once people depend on the software, it has to keep working when nobody is watching. And it will be tested by things you never saw on your laptop: machines fail, traffic suddenly doubles, someone tries to break in, a disk fills up. Running a system means being able to *see* what it is doing, being told when something goes wrong, recovering quickly, protecting it from attackers, and coping with more users.

**Grow — when one is not enough.** Some systems eventually outgrow a single program on a single machine: too many users, too much data, too many engineers changing one codebase. Then the work is split across many programs and many machines that must cooperate. This is powerful and expensive, and the most common mistake is doing it too early.

- **Comes in:** reviewed code.
- **Goes out:** a system real people use — and a steady stream of evidence about how it behaves.
- **When it is done badly:** "it worked on my machine"; failures nobody notices until users complain; the same failure happening again and again.
- **In this book:** Part IV — Stages 2 to 7 for Ship, Stages 8 and 10 for Run, Stage 11 for Grow.

### The arrow back: Learn

Learning is what turns the line into a loop. Production produces evidence: how people really use the software, what they ignore, what breaks, what is slow, what they ask for next. That evidence goes back to Discover, and the loop starts again — for a new feature, a fix, or an improvement.

This is the most important thing to understand about real engineering work: **the loop never finishes.** The first trip around produces a first version. Every trip after that changes a system that already exists and already has users. That is where most engineers spend almost all of their working lives — not building new systems, but changing live ones without breaking them.

### Three sizes of the same loop

The loop is not only a months-long cycle. The same shape repeats at three sizes, one inside the other:

| Size | How long one trip takes | Example |
|---|---|---|
| The big loop | weeks to months | a new product or a major feature: discover, plan, build, launch, learn |
| The change loop | hours to days | one small change: a piece of work, the code, a review, automatic checks, release, watch it |
| The inner loop | seconds to minutes | one engineer at a keyboard: change the code, run it, look at the result, change it again |

Healthy teams make the two smaller loops fast and safe, so that they can go around the big loop often. A large part of this book is about exactly that: making the change loop fast and safe enough that shipping stops being frightening.

## Layer 2: The Pieces

The loop is about *time*. The second layer is about *space*: what a working application is actually made of once it is running. When you use almost any app — send a message, book a ticket, save a note — the same handful of pieces is involved.

```text
  WHAT USERS TOUCH
  ┌──────────┐    ┌──────────────┐    ┌───────────────────────────────┐
  │  CLIENT  │───▶│     PATH     │───▶│            MACHINE            │
  │ browser, │    │ the internet,│    │  ┌─────────┐    ┌──────────┐  │
  │ phone app│◀───│ a name, the  │◀───│  │ PROGRAM │───▶│   DATA   │  │
  │ or other │    │ front door   │    │  └────┬────┘    └──────────┘  │
  │ program  │    └──────────────┘    │       ▼                       │
  └──────────┘                        │  ┌─────────┐                  │
                                      │  │ HELPERS │  background work,│
                                      │  └─────────┘  other services  │
                                      └───────────────────────────────┘
  THE WORKSHOP BEHIND IT
  code repository · automatic checks · package store · monitoring · documents
```

- **The client** is whatever the user holds: a web browser, a phone app, or another program. It shows things and sends requests. It keeps as little as possible, because it lives on a device you do not control.
- **The path** is everything between the client and your machine: the internet, the name users type (which has to be turned into a numeric address), and a **front door** on your side that receives every visitor first, checks them, and passes them in.
- **The machine** is a computer that is always on — usually rented from a cloud provider — with an operating system that runs your program and connects it to the network.
- **The program** is your code, running. It receives a request ("save this note"), checks it, applies the rules of your application, and sends back an answer. A program that does this for other programs, out of sight on a server, is called a **backend**, and the set of requests it accepts is its **API** (application programming interface).
- **The data** lives in a **database**, so that it survives when the program restarts or the machine is replaced. Almost every hard problem in real systems eventually turns out to be a problem about data.
- **The helpers** do work the program should not do itself. Slow jobs that should not make the user wait — sending an email, building a report — go to **background workers**. Work that another company does better — taking payments, delivering email — goes to **other services**, which your program calls over the internet.

The second group is **the workshop**. Users never see it, but it is what makes the loop work:

- the **code repository**, where all the code lives with its full history;
- the **automatic checks**, which test every change before it is accepted;
- the **package store**, which keeps the finished, runnable package of every version;
- **monitoring**, the numbers and records that show what the running system is doing, and the alarms that go off when something is wrong;
- the **documents**: the plan, the decisions and their reasons, and step-by-step instructions for handling failures.

### One request, end to end

To see how the pieces fit together, follow one action. You tap *Save* on a note in an app:

1. **Client.** The app packages "save this note" as a request and sends it toward the name of the service.
2. **Path.** The name is turned into a numeric address; the request crosses the internet and reaches the front door, which checks it and passes it to the program.
3. **Program.** The program checks that the request is valid and that you are allowed to make it, applies the application's rules, and asks the database to store the note.
4. **Data.** The database stores the note permanently and confirms.
5. **Back.** The program builds an answer — "saved; here is its number" — and it travels back along the same path to the app, which shows it to you.
6. **Workshop.** Meanwhile, monitoring records one more successful request, and how long it took.

The whole trip usually takes a fraction of a second. Stages 8 and 9 of Part IV follow exactly this trip, in full detail.

### Two coordinates for everything

Put the first two layers together and you get a grid. Any topic, tool, or task in software has two coordinates: **when** it happens (a step of the loop) and **where** it lives (a piece of the system, or the workshop).

| What you hear | When (step) | Where (piece) |
|---|---|---|
| "Write the design document first." | Plan | the workshop: documents |
| "The checks failed on my change." | Code, in the change loop | the workshop: automatic checks |
| "We're releasing the new version." | Ship | from the package store to the machine |
| "Users can't reach the site." | Run | the path, the machine, or the program |
| "Saving is slow since yesterday." | Run | the program or the data |
| "We need to split this into several services." | Grow | the program and the machines |

Notice how often the "where" for a problem in Run is *several* pieces. That is normal. The first job when something goes wrong is always to find *which* piece is failing — and you can only do that if you know what the pieces are.

## Layer 3: The People

On a small project one person can do everything. That is how this book works: you do every step yourself, so that you see all of them. In a company, the steps and the pieces are divided between people with different jobs. Titles vary from company to company, but the division is remarkably consistent:

| Role | Works mostly on (steps) | Works mostly on (pieces) | Hands to others |
|---|---|---|---|
| Product manager | Discover, Learn; priorities in Plan | — | the problem, why it matters, what comes first |
| Designer | Discover, Plan | the client: what users see and do | screens and flows |
| Tech lead or architect | Plan, and the whole loop | how all the pieces connect | the design and the key decisions |
| Frontend engineer | Code | the client, in the browser | the website |
| Mobile engineer | Code, Ship | the client, on phones | the phone apps |
| Backend engineer | Code, Ship, Run | the program, the data, the helpers | the API: what the program accepts and answers |
| QA or test engineer | Code, Ship | the automatic checks | confidence that it works |
| Platform or DevOps engineer | Ship | the workshop, the machines, the path | a safe, automatic way to ship |
| Site reliability engineer (SRE) | Run | monitoring, and the whole running system | reliability; leading the response when things break |
| Data engineer | Code, Learn | the data, and copies of it for analysis | reports and numbers people trust |
| Security engineer | every step | every piece | reviews, rules, protection |
| Engineering manager | the loop as a way of working | — | the people, and a team that works well |

Two things are worth noticing.

First, the rows do not disappear when a team is small. In a startup, three engineers cover all of them; in a large company, each row is a whole team. Someone is always doing each job — often without the title.

Second, **people coordinate mostly through artifacts, not conversation.** Each step hands the next one something concrete: a written problem, a design, a reviewed change, a versioned package, a dashboard, a **postmortem** (a written account of a failure: what happened, why, and what will change). When those things are clear, dozens of people can work in parallel without constantly talking to each other. When they are vague, everything turns into a meeting.

| From → to | What is handed over |
|---|---|
| Discover → Plan | the problem statement: who has what problem, and what "solved" means |
| Plan → Code | the design, broken into small pieces of work, and the agreed API |
| Engineer → engineer | a proposed change, reviewed before it is accepted |
| Code → Ship | reviewed code that has passed every check, turned into a versioned package |
| Ship → Run | a running system, plus written instructions for when it fails |
| Run → Learn → Discover | measurements, failure reports, user feedback |
| Frontend ↔ backend | the API contract: exactly which requests the program accepts and what it answers |

A great deal of engineering practice exists purely to make one of these hand-offs safe. When you meet a practice and wonder why anyone bothers, ask which hand-off it protects. The closing chapter of this book, [The Same Process in a Real Team](the-same-process-in-a-team.md), returns to this with a whole team.

## The Same Map, for Any Application

This book builds one kind of software: a backend service — a program that other programs talk to over the internet. But the map is not specific to it. The loop is the same for every kind of software; what changes is which pieces exist, and what Ship and Run look like.

| Kind of software | What changes on the map |
|---|---|
| A website | The client is code your server sends to each browser, so you can update every user at once. |
| A phone app | The client lives on users' phones and ships through app stores. Old versions stay in use for months, so the backend must keep answering them. |
| A data pipeline | Nobody sends it requests; it runs on a schedule. "Working" means the data it produces is fresh and correct. |
| Installed software, or a library | Ship means publishing a release. You do not run it — your users do — so Run becomes bug reports and support. |
| A large system of many services | Grow has happened: many programs, and many teams, each going around its own loop. |

Every one of them has a Discover, a Plan, Code, a way to Ship, something to keep running, and a way to Learn. The closing chapter lays them side by side.

## How to Use the Map

Whenever you meet something new — in this book, at work, in a meeting, in a job description — ask four questions:

1. **When?** Which step of the loop does it belong to?
2. **Where?** Which piece of the system, or which part of the workshop?
3. **Who?** Which role owns it, and what do they hand to whom?
4. **Why?** What goes wrong without it?

If you can answer all four, the thing has a place in your head and is no longer an isolated fact. If you cannot, the question you could not answer is exactly what to find out next.

## How This Book Walks the Map

The book goes around the loop once, from start to finish, for one small application — a service that stores notes, called the **Notes API** — and you do every step yourself. That is deliberate. Specialists usually see only their own region of the map, and the fastest way to see all of it is to walk all of it once.

| Part or stage | Step | Piece | The question it answers |
|---|---|---|---|
| Part I — Product Discovery | Discover | — | Should we build this, and what exactly? |
| Part II — Project Planning | Plan | documents | How will we build it and run it? |
| Part III — Writing Good Code | Code | the program | How do we write code others can safely change? |
| Stage 1 — Creating a Running Program | Code | the program, on your laptop | What is a program, really, when it runs? |
| Stage 2 — Breaking the Local Illusion | Code → Ship | the gap between laptop and server | Why is "it works on my machine" not enough? |
| Stage 3 — Making the Program Portable | Ship | the program | How is it made to run anywhere? |
| Stage 4 — Build and Packaging | Ship | the workshop | How is it checked and packaged? |
| Stage 5 — Infrastructure and Environment | Ship | the machine | What will it run on? |
| Stage 6 — Deployment | Ship | the program, on the machine | How does it get there, and stay running? |
| Stage 7 — Making It Reachable | Ship | the path | How do users reach it? |
| Stage 8 — Request Flow | Run | the path, end to end | What happens to one request on its way in? |
| Stage 9 — Inside the Running Program | Code, seen again | the program and its data | What does the program do with the request? |
| Stage 10 — Production Reality | Run | the whole system | How does it keep working in the real world? |
| Stage 11 — Beyond a Single Service | Grow | many programs and machines | What changes when one is not enough? |
| Chapter 44 — the project | the whole loop, five times | the whole system | Can you do all of this yourself? |
| The Same Process in a Real Team | the whole loop | the whole system | How does a team do all of this, for any application? |

Most of the book's pages are spent in the backend engineer's region of the map — the program, its data, and everything between it and its users — because that is where Code, Ship and Run meet. The book does not teach frontend or mobile code, or the day-to-day mechanics of running a team; they have their places on the map, and the closing chapter shows where, but they belong to other books.

Every part of the book opens with the loop, marked with where you are, and every stage of Part IV opens with its place on the loop and the piece it works on. When you feel lost in detail, come back to this chapter. The detail always belongs somewhere on the map.
