# Databases from Zero

**The problem you hit:** My app forgets everything when it stops. A list in memory can't be shared between users, searched well, or trusted after a crash.
**The question it answers:** Where should my app keep information so that it survives restarts, many users can share it, and I can find exactly what I need?
**Target:** 95–99 pages

## Front matter

Title page · Copyright · Contents · Preface (Who This Book Is For, How This Book Is Organized, How to Use This Book, What You Need Installed, Conventions Used in This Book)

## Part I · Understand

*What to ignore for now:* relational algebra, normal forms beyond the third, and database administration.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 1 | Why Not Just Use Files? | I saved my data in a JSON file, and two users just overwrote each other. | What a database is, what it guarantees that a file doesn't, the database server | 5 |
| 2 | Kinds of Databases | Everyone says "just use Postgres", but also Redis, MongoDB, and a vector database. | Relational, key-value, document, search, vector, graph, time-series, and analytical databases; how to choose | 7 |
| 3 | Tables, Rows, and Relationships | My app has users, notes, and tags. How do they fit into tables? | The relational model, keys, one-to-many and many-to-many, constraints, designing a schema | 8 |
| 4 | Inside the Database: Storage, the Log, and Copies | My data is "in the database". Where, physically, and what if the machine dies? | Pages and the buffer pool, rows on disk, the write-ahead log, replicas and backups built from the log | 7 |

## Part II · Use

*What to ignore for now:* storage engine source code and query optimiser internals.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 5 | Talking to a Database: SQL | I know what I want from the data, but not how to ask for it. | `SELECT`, filtering and sorting, joins, grouping and counting, inserting, updating, deleting | 9 |
| 6 | Indexes and How a Query Runs | One query takes 4 seconds, and the same query on another column takes 4 milliseconds. | What an index is, B-tree indexes, what indexes cost, the query planner, reading `EXPLAIN` | 9 |
| 7 | Transactions and Concurrency | Two people bought the last ticket at the same moment. | ACID, transactions, isolation levels, locking, MVCC, deadlocks | 7 |
| 8 | Beyond Tables: Caches, Documents, Search, and Vectors | My app needs instant repeat reads, full-text search, and "find similar". | Caches (Redis), document stores, full-text search, vector search, object storage | 6 |

## Part III · Apply

*What to ignore for now:* running your own database cluster.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 9 | Lab: Fix a Slow Query | One page of my app takes eight seconds to load. | Finding the slow query, reading its plan, adding the right index, measuring again | 8 |
| 10 | Lab: Two Buyers, One Ticket | My app sometimes sells the same ticket twice. | Reproducing a race, fixing it with a transaction and a lock, checking the fix | 8 |
| 11 | Lab: The Server Died Last Night | The database is gone. Can I get the data back? | Taking a backup, restoring it, a read replica, testing a restore | 8 |

## Part IV · What Next

| Ch | Chapter | Covers | Pages |
|---|---|---|---|
| 12 | Security, Speed, Failure, and Cost | SQL injection and access control, slow queries, crashes and corruption, what storage and queries cost | 6 |
| 13 | Where to Go from Here | What to learn next, what to skip for now | 3 |

## Appendices

A. SQL Cheat Sheet · B. Glossary · Index (4 pages)

**Total:** about 95 pages
