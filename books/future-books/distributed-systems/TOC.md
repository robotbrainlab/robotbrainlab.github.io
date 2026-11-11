# Distributed Systems from Zero

**The problem you hit:** One machine can't handle the load, and any machine can die at any time.
**The question it answers:** What changes when my app runs on many machines at once?
**Target:** 65–80 pages

## Front matter

Title page · Copyright · Contents · Preface (Who This Book Is For, How This Book Is Organized, How to Use This Book, What You Need Installed, Conventions Used in This Book)

## Part I · Understand

*What to ignore for now:* formal proofs, Byzantine fault tolerance, and blockchain.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 1 | Why Use More Than One Machine? | My one server is full, and when it restarts, everyone is locked out. | Scaling out, redundancy, what distribution costs | 6 |
| 2 | What Can Go Wrong | I sent a message and got no reply. Did it arrive? | Lost and delayed messages, crashed machines, network partitions, partial failure, timeouts | 8 |
| 3 | Time and Order | Two servers disagree about which event happened first. | Clocks that drift, why "now" is unreliable, ordering events, logical clocks | 9 |

## Part II · Use

*What to ignore for now:* implementing Paxos and tuning replication.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 4 | Replication | I keep copies of my data on three machines. Which one is right? | Leaders and followers, synchronous and asynchronous copies, quorums | 7 |
| 5 | Consistency | I saved my profile, refreshed, and saw the old one. | Strong and eventual consistency, read-your-writes, the CAP trade-off | 7 |
| 6 | Consensus and Leaders | Three machines must agree on one leader, even while some of them fail. | Leader election, consensus, Raft in plain words, two-phase commit | 7 |
| 7 | Retries and Idempotency | My request timed out. Should I send it again? | Retries with backoff, idempotency keys, at-least-once and exactly-once delivery, graceful degradation | 5 |

## Part III · Apply

*What to ignore for now:* building production consensus systems.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 8 | Lab: Watch Replicas Disagree | I want to see eventual consistency happen. | A small simulation in Python: replicas, delays, and stale reads | 6 |
| 9 | Lab: Elect a Leader | What happens when the leader dies? | A small leader-election simulation, failures and recovery | 6 |
| 10 | Lab: The Retry That Charged Twice | My retry charged the customer twice. | Reproducing a double charge, fixing it with an idempotency key | 6 |

## Part IV · What Next

| Ch | Chapter | Covers | Pages |
|---|---|---|---|
| 11 | Security, Speed, Failure, and Cost | Trust between machines, latency across regions, cascading failures, the cost of copies | 5 |
| 12 | Where to Go from Here | What to learn next, what to skip for now | 3 |

## Appendices

A. Patterns Cheat Sheet · B. Glossary · Index (4 pages)

**Total:** about 79 pages
