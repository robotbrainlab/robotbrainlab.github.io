# Security, Speed, Failure, and Cost

Every web application, from a to-do list to a bank, faces the same four questions: what can go wrong, what makes it slow, how it breaks, and what it costs. This chapter answers each one using the picture you now have of the two sides and the trip between them.

*The problem.* My app works on my screen. But could someone break in, could it feel slow, could it fall over, and who pays for it?

*The question.* What can go wrong with a web application, and what keeps each kind of trouble small?

## Security: What Can Go Wrong

The front end lives on the user's device, so the user controls it. Anyone can skip your page and send requests with a tool like `curl`. So the back end must treat every request as a stranger at the door and check three things: *who are you* (the session), *are you allowed* (the rules), and *does this make sense* (a negative price? a 10 MB name?).

The other dangers follow the trip:

- *On the device:* secrets in front-end code are not hidden. Keep them on the back end.
- *On the way:* a stolen cookie is a stolen login. HTTPS seals every request, and sessions that expire limit how long a stolen ticket works.
- *In the database:* a leak exposes everything stored. Keep only what you need, and never store passwords as plain text. Store them **hashed**: scrambled one way, so that even a leak doesn't reveal them.

What limits the damage: give each part only the access it needs, so one mistake can't open every door.

## Speed: What Makes an App Feel Slow

Time goes to three places on the trip:

- *Distance.* Every round trip takes time; twenty trips take twenty times as long.
- *Size.* Big images and heavy JavaScript download slowly, especially on a phone.
- *Work.* A back end that searches a huge database carelessly can take seconds.

The fixes match. A **cache** keeps a copy of an answer close by, so the next request travels less far, or not at all. A **CDN** (content delivery network) keeps copies of files on servers near the users. Shrink images and code. And *feel* faster: show the new note at once, while the request is still travelling.

## Failure: What Breaks, and How to Tell Where

When something goes wrong, first find which step of the trip failed. The developer tools tell you most of it:

| What you see | Where it likely failed | Where to look |
|---|---|---|
| A button does nothing | Front end: a JavaScript error | The *Console* tab |
| "Can't reach this site" | The network or DNS | Try another site |
| An endless spinner | Back end slow or down | *Network* tab |
| A status starting with 4 | Your request (401, 404) | *Network* tab |
| A status starting with 5 | The back end broke | The server's logs |

A client gives up after a **timeout**, a set time such as thirty seconds. On the back end, developers read **logs**: lines the server writes about every request, such as `"POST /notes HTTP/1.1" 200 OK` from Chapter 3's back end.

## Cost: What It Costs to Run

The two sides cost very different amounts:

- *The front end* is cheap to serve: its files are sent once and cached, and the drawing happens on the user's device.
- *The back end* runs day and night, and that is where the bills are: servers, the database (often the biggest item), data sent to users, and paid services such as email.

Costs grow with users, though free tiers let a small app run almost free. The largest cost is usually people, who build, update, and protect both sides.
