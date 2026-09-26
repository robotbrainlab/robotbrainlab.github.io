# Networking from Zero

**The problem you hit:** It works on `localhost`, but nobody else can reach it.
**The question it answers:** How does a request from someone's browser find my program and get an answer back?
**Target:** 80–95 pages

## Front matter

Title page · Copyright · Contents · Preface (Who This Book Is For, How This Book Is Organized, How to Use This Book, What You Need Installed, Conventions Used in This Book)

## Part I · Understand

*What to ignore for now:* the OSI model's seven layers in detail, radio and cabling, and routing protocols' internals.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 1 | What Happens When You Type a URL | I type an address, press Enter, and a page appears a moment later. | The whole trip in one picture, clients and servers, packets | 7 |
| 2 | Layers: How the Internet Is Organised | The internet carries video, email, and games on the same wires. How? | Layering and encapsulation, the four layers that matter | 6 |
| 3 | Addresses, Routing, and Ports | My laptop and a server across the world find each other among billions of machines. | IP addresses, private and public addresses, NAT, routing, ports, `localhost` vs `0.0.0.0` | 7 |
| 4 | Names: DNS | Computers use numbers, but I type names. | How DNS works, record types, caching and TTL, `dig` | 6 |

## Part II · Use

*What to ignore for now:* HTTP/3 internals and certificate authority operations.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 5 | TCP and UDP: Reliable or Fast | The network loses and reorders packets, yet my file arrives perfect, while video calls just stutter. | Connections, the handshake, acknowledgements and retries, flow and congestion control, UDP and when to choose it | 10 |
| 6 | HTTP: The Language of the Web | My browser and a server agree on a language. What does it look like? | Requests and responses, methods, status codes, headers, HTTP versions, `curl` | 8 |
| 7 | TLS and HTTPS | Anyone between me and the server could read what I send. | Encryption, certificates, the TLS handshake, HTTPS | 7 |
| 8 | Proxies, Load Balancers, and Firewalls | One server isn't enough, and my app shouldn't face the internet directly. | Reverse proxies, load balancing, TLS termination, firewalls | 6 |

## Part III · Apply

*What to ignore for now:* building production load balancers and tuning TCP.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 9 | Lab: Write a Tiny Server | I want to see a connection from the inside. | Sockets in Python, a tiny TCP server and client, a tiny HTTP server | 7 |
| 10 | Lab: Put a Proxy in Front | My app should sit safely behind one public front door. | Running a reverse proxy in front of two copies of the tiny server, spreading requests between them | 7 |
| 11 | Lab: The Connection That Won't Connect | "Connection refused." "Timed out." Which one, and why? | Debugging by layer: DNS, reachability, ports, firewalls, TLS | 8 |

## Part IV · What Next

| Ch | Chapter | Covers | Pages |
|---|---|---|---|
| 12 | Security, Speed, Failure, and Cost | Exposed ports and eavesdropping, latency and bandwidth, network failures, data transfer costs | 5 |
| 13 | Where to Go from Here | What to learn next, what to skip for now | 3 |

## Appendices

A. Network Tools Cheat Sheet · B. HTTP Status Codes · C. Glossary · Index (4 pages)

**Total:** about 91 pages
