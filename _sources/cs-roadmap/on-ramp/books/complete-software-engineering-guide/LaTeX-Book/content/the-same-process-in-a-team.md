# The Same Process in a Real Team

### What you did alone, as a team does it — and the same map laid over any kind of software

You have now been around the loop from [How Software Gets Built](how-software-gets-built.md) once, from start to finish, entirely on your own. Every job was yours. You decided what to build and wrote the plan. You wrote the code and its tests, packaged it, rented a machine, deployed to it and gave it a name. Then you watched it, secured it, scaled it, and saw how it would grow into many services. That was deliberate: doing every job once is the only way to see how the jobs connect.

Real software is rarely built by one person. This chapter replays the same journey with a team. It shows who does each step, what they hand to each other, and where things go wrong between them. Then it lays the same map over other kinds of software, to show what stays the same when the technology changes. You will not meet many new techniques here. You will see the techniques you already know from a new angle: as the way a group of people builds one thing together.

## The Team

Imagine a small company that has grown the Notes API into a product. People use it through a website and a phone app, and both talk to the API. The people who build it:

| Role | How many | What they own |
|---|---|---|
| Product manager | 1 | what gets built, and why; what comes first |
| Designer | 1 | what users see and do, on the website and the app |
| Tech lead | 1 | the design of the whole system; also writes backend code |
| Backend engineers | 2 | the Notes API, its database and its background workers |
| Frontend engineer | 1 | the website |
| Mobile engineer | 1 | the phone app |
| Platform engineer | shared | the road to production: automatic checks, packaging, servers, deployment |
| Site reliability engineer | shared | reliability; leading the response when something breaks |
| Security engineer | shared | reviews of anything that touches access, data or secrets |
| Engineering manager | 1 | the people, their priorities, and how the team works |

Eight people, five of whom write code for this product, plus three specialists shared with the rest of the company. It is a very ordinary team. Every job you did alone in this book belongs to at least one of them.

## The First Version, as a Team

Here is the first trip around the loop, as this team would make it.

**Discover.** The product manager spends two weeks with people who take notes for their work. The aim is to learn what they do today, what annoys them, and what they would pay for. The designer sketches screens on paper and tries them with five of those people. The tech lead joins a few of the conversations to spot, early, the ideas that would be very expensive to build. The result is a one-page **problem statement**. It says who has the problem, what "solved" means in measurable terms, and what is out of scope for the first version (no sharing, no attachments). The whole team reads it and questions it before anyone plans anything. This is [Part I](product-discovery.md), done by several people instead of one.

**Plan.** The tech lead writes the **design document** ([Part II](project-planning-guide.md)). It names the pieces: the API, its database, the website and the app. It describes the data and how the service will be run. Most importantly, it defines the **API contract** early: the exact requests the API accepts and the answers it gives. Three groups will build against that contract at the same time — backend, web and mobile — so it has to be settled first. [Chapter 34](34-response-handling.md) (section 34.10) explains why a contract is so hard to change once others depend on it. Big decisions go into **decision records** ([Chapter 39](39-local-vs-production.md)), such as which database to use and why.

Before any code is written, others review the design. The platform engineer asks whether the service can be run on the company's usual setup. The security engineer asks what could go wrong: who might attack it, and what they would want ([Chapter 38](38-security.md)). Finally, the work is cut into small pieces, often called **tickets**. Each takes a few days and has a clear definition of "done".

**Code.** Each backend engineer takes a ticket. They work on a separate copy of the code (a **branch**) and open a **pull request**, a proposed change that others can see. The automatic checks run the tests and code-quality tools on it ([Chapter 17](17-build-process.md)). Another engineer reads the change and approves it or asks for changes. Only then is it merged into the main code. The shared conventions and review habits of [Part III](writing-good-code.md) are what let several people change one codebase without stepping on each other.

Meanwhile, the frontend and mobile engineers build their screens against the agreed contract. Until the real API exists, they use a stand-in that returns realistic answers. Because the contract was settled first, nobody waits for anybody.

**Ship.** In a company this size, nobody builds the road to production from scratch for each service. The platform engineer built it once, and every team uses it: the automatic pipeline, the container image, the package store and the deployment scripts. These are the things you built yourself in Stages 4 to 6.

The backend team's job is to keep its service *shippable*: dependencies pinned, configuration outside the code, a health check that tells the truth. Each change goes first to **staging**, a copy of production with no real users, and then to production. The public name, the certificates and the front door (Stage 7) are usually shared, and the platform team runs them for everyone.

The website ships the moment it is ready. The phone app ships differently. It goes through the app store's review, which can take days, and reaches users only as they update.

**Launch.** The first version goes to a small group of users first. The team measures it against the success criteria in the problem statement. It is not "done" when the code is merged. It is done when users have the problem solved.

**Run.** Each team runs what it builds. The backend team owns the dashboards and alerts for the API ([Chapter 35](35-observability.md)). One backend engineer at a time is **on call** for a week and is woken if an alert fires. When something breaks, the on-call engineer's first job is to stop the harm, not to find the perfect fix. For a serious incident, the SRE joins and coordinates. The team keeps a **runbook** for each alert: step-by-step instructions written in daylight for the person reading them at 3 a.m. After every serious incident comes a blameless **postmortem**. Both are in [Chapter 37](37-reliability.md).

**Learn.** The product manager reads the usage numbers and the support messages. Follow-up work from the postmortems becomes tickets. Requests from users go into the next round of discovery, and the loop begins again.

## Where Hand-offs Break

Most problems in a team come from the gaps *between* steps and *between* people, not from inside them. One person can do each step well and the team can still fail. The problem statement said one thing and the design assumed another, or the code worked on the author's laptop and nowhere else.

The table below lists the seams you have seen in this book. For each one it gives the failure that happens there and the practice that protects it.

| Seam | What goes wrong there | The practice that protects it | Where in this book |
|---|---|---|---|
| Discover → Plan | a well-built answer to the wrong question | a written problem statement with success criteria and scope | Part I; Part II, Section 1 |
| Plan → Code | engineers build different ideas; the pieces do not fit | a design document; the API contract agreed before building | Part II; section 34.10 |
| Engineer → engineer | code only its author understands | code review, shared conventions, tests | Part III; Chapter 17 |
| Laptop → server | "it works on my machine" | pinned dependencies, configuration outside the code, containers | Stages 2–4 |
| Build → release | what runs in production is not what was tested | one versioned package, promoted unchanged | Chapters 18, 19 and 23 |
| Ship → Run | the system is handed to people who cannot see inside it | health checks, logs, metrics, runbooks | Chapters 25, 35 and 37 |
| Backend ↔ clients | a change breaks the website, or old copies of the app | a versioned contract; changes that only add | section 34.10 |
| Today → next year | nobody remembers why it was built this way | decision records and a changelog | Chapter 39 |
| Run → Learn | the same failure happens again | blameless postmortems, with follow-up work that gets done | Chapter 37 |

This table is the real reason the book is full of *practices*. Each one exists because some hand-off failed often enough, at enough companies, that people found a way to protect it. When a practice feels like bureaucracy, find the hand-off it protects. Then decide whether your team actually has that hand-off. A practice without a hand-off to protect usually *is* bureaucracy.

## A Change to a Live System

After launch, almost all of a team's work is changing the live system. Here is one change, followed through the loop: **letting a user share a note with a colleague.**

**Day 1 — Learn → Discover.** Many users have asked for sharing, and the support messages show it. The product manager writes a short problem statement: who needs it, why, and what "done" looks like. Editing a shared note is out of scope, and so is sharing with people outside the company.

**Day 2 — Plan.** The designer sketches the "share" flow. The tech lead writes a one-page design with three parts:

- a new database table recording which notes are shared with whom;
- two new API requests, one to share a note and one to list what has been shared with you;
- a change to the rule for who may read a note.

The security engineer reviews it within the hour, because a shared note must never be visible to anyone it was not shared with ([Chapter 38](38-security.md)). The web and mobile engineers agree the additions to the contract.

**Days 3–6 — Code and Ship, in small steps.** The backend engineer does the work in stages:

1. First, a database change that only *adds* a table, so the code already running is not affected ([Chapter 33](33-logic-execution.md)).
2. Then the new requests, with their tests. One test checks that a user who was not given access gets "not found", exactly as if the note did not exist.
3. Each step goes in as its own small pull request, which is reviewed, checked, merged and released on its own.

The new feature reaches production switched off. It is hidden behind a setting called a **feature flag**, so code can be released before users see it.

**Days 4–8 — the clients.** The web and mobile engineers build the screens against the agreed contract. The website change goes live the day it is finished. The app update goes to store review and reaches users over the next few weeks. Meanwhile, older copies of the app know nothing about sharing, and they must keep working. That is why the contract only gained new requests, and nothing existing changed.

**Day 9 — Run.** The flag is turned on for one user in twenty. The team watches the dashboards for errors and slow requests. Two days later, it is turned on for everyone.

**The weeks after — Learn.** The product manager sees how many people share notes. Support notices a new request: people want colleagues to be able to *edit* shared notes. That becomes the next trip around the loop.

Look at what happened. The change went through every step of the loop and involved seven people, yet no single step was big. That is what a healthy change loop looks like. The steps are small and safe, the hand-offs are clear, and the system is never broken in between.

## The Rituals, and What They Are For

Teams have regular meetings and habits. From outside they can look like overhead. Each one, though, serves a hand-off or the Learn arrow:

| Ritual | How often | What it is for on the map |
|---|---|---|
| Planning | every week or two | choosing which pieces of work come next (Plan → Code) |
| Stand-up | daily, a few minutes | finding out who is stuck (engineer ↔ engineer) |
| Design review | before any large change | checking a design before code exists (Plan → Code) |
| Code review | every change | a second pair of eyes on everything (engineer → engineer) |
| Release | many times a day, ideally | a change reaching users (Code → Ship) |
| On-call hand-over | weekly | telling the next person what is fragile (Run → Run) |
| Postmortem | after every serious incident | turning a failure into lessons (Run → Learn) |
| Retrospective | every few weeks | looking at how the team works, not what it built (Learn, applied to the team itself) |

This book does not teach how to run these meetings well; that belongs to books about teams and process. You do now know where each one sits on the map, and what goes wrong when it is skipped.

## The Same Map, for Any Application

The Notes API is a backend service. Here is the same loop for four other common kinds of software:

| Step | Website | Phone app | Data pipeline | Library or installed software |
|---|---|---|---|---|
| Discover | users and their problem | the same, plus where and when people use their phones | the "users" are the people who need the numbers | the users are other developers |
| Plan | screens and flows, as well as the API | also: working offline, small screens, slow networks | where the data comes from, how often, how it is checked | the public interface, the hardest part to change later |
| Code | code for the browser and the backend | code for the phone and the backend | the steps that clean and combine data, and checks on the data itself | the library itself, its tests and examples |
| Ship | every user gets the new version at once | store review; users update slowly | each scheduled run is, in effect, a release | publish a numbered release |
| Run | everything in this book, plus errors in users' browsers | crash reports from devices you cannot reach | "is the data fresh and correct?" | you do not run it; bug reports and support |
| Learn | how people use the pages | store reviews and crash rates | are the numbers used, and trusted? | issues, questions, downloads |

What never changes is even more useful than what does:

- **The loop.** Every kind of software is discovered, planned, coded, shipped, run and learned from.
- **The workshop.** A code repository, automatic checks, versioned releases, monitoring and written decisions appear everywhere, under different names.
- **Contracts between pieces.** Wherever two teams or two programs meet, there is an agreement about what one gives the other, and changing it safely follows the same rules.
- **Observing what is real.** Every team needs to see what its software is actually doing in the hands of real users.

That is why what you learned from one small API carries over to software you have never seen.

## Where Specialists Sit

Every specialty in software is a close-up of one region of the map:

| Specialty | Its region of the map |
|---|---|
| Frontend and mobile | the client, in depth |
| Backend | the program, the data and the helpers, plus the contract every client depends on |
| Platform and DevOps | the workshop, and Ship |
| Site reliability | Run |
| Data | the data, and Learn |
| Security | a thread through every step and every piece |
| Product and design | Discover and Plan |

Specialists go deep, and they should. The map is what lets them talk to one another. The people who end up leading technical work are usually those who carry the whole map, and who can talk with each role about its own region. Leading technical work is mostly a matter of managing the seams.

Backend is an especially good place to stand while you learn the whole map. The program sits in the middle of all the pieces. Its contract is where the clients, the data and the platform meet, and its failures show up in every other role's work.

## Using the Map from Now On

The map is not only for reading this book. Use it at work, in four situations:

- **Joining a team.** First place the team on the map. Which regions does it own? What does it receive, and from whom? What does it hand over, and to whom? Then use the questions in [Appendix E](44-appendices.md#appendix-e--walking-into-an-unfamiliar-system) to learn the system itself.
- **Meeting a new tool or practice.** Ask the four questions from the opening chapter: when, where, who and why. A tool you cannot place is a tool you do not yet understand.
- **In a meeting that goes nowhere.** Ask which step of the loop the discussion belongs to. Many unproductive meetings are two people in different steps talking past each other. For example, one is still deciding *whether* to build something (Discover) while the other is arguing about *how* (Plan).
- **Learning something new.** Go deep on one region at a time, and keep the map in view while you do. Depth attached to the map becomes understanding. Depth without it becomes another pile of disconnected facts, and that pile is where this book began.

## Where to Go Next

This book went deep on one region of the map, the backend, and walked the whole loop around it. Here is where to go from here. The directions are ordered by how directly they build on what you now have. Each one comes with a first project built on the Notes API, because extending a system you understand teaches faster than starting from nothing.

**Go deeper where you stand.** Most backend work is data work. Learn how PostgreSQL stores, indexes and plans (*Use The Index, Luke*, then *Designing Data-Intensive Applications*, both in [Appendix D](44-appendices.md#appendix-d--further-reading)). *First project:* load a million notes, find the three slowest queries with `pg_stat_statements`, and make each one ten times faster, measuring before and after (section 36.2).

**Own the client.** Every API exists for its clients, and building one shows you your API from the other side: the error you thought was clear, the pagination that is awkward to use. Learn enough HTML, CSS and JavaScript to write a small web page that calls an API (the MDN Web Docs are the reference). *First project:* a one-page client for the Notes API, with login, a list, and search. You will meet CORS, where to keep a token in a browser, and why `openapi.yaml` matters to the people on the other side.

**Hand over the workshop.** You ran everything yourself on one server. The next step is to let a platform run parts of it. Chapter 43 introduced both halves. **Kubernetes** runs containers across a fleet from a declaration of what you want, and **Terraform** declares the machines, networks and databases themselves. *First project:* run the Notes API and its worker in a local Kubernetes cluster (kind or minikube), with the migration as a Job that runs before the Deployment. Then write the Terraform for the server and firewall of Chapters 20 to 22, and destroy and recreate them.

**Use a cloud provider's managed pieces.** Replace one piece you ran by hand with a managed service: a managed PostgreSQL, with backups and failover you no longer have to operate; object storage for files; a managed queue. Each one trades control and money for time. *First project:* move the database to a managed PostgreSQL, and write down exactly what you no longer have to do, and what you can no longer do.

**Split a service, only when there is a reason.** Microservices solve problems of *teams* and of scale, and they add every problem of Chapter 40. Learn them by doing one split for a real reason. *First project:* make the email sender a separate service with its own small API and its own deployment, and list everything that got harder: tracing a request, deploying the two together, testing across the boundary.

**Strengthen the foundations under all of it.** The book touched algorithms, operating systems and networks wherever the Notes API needed them. Depth there pays off everywhere, and especially in interviews and in the hardest production problems. For algorithms and data structures, *Grokking Algorithms* (Bhargava) is a gentle start and *The Algorithm Design Manual* (Skiena) goes much further. For operating systems and networks, see *The Linux Programming Interface* and *Computer Networking: A Top-Down Approach*, also in Appendix D.

Whichever direction you choose, keep going around the loop: decide what to build and why, plan it, build it in small steps with tests, ship it, run it and watch it, and learn from what you see. The tools will change many times during your career. The loop will not.
