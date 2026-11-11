# Data Structures and Algorithms from Zero

**The problem you hit:** My code gives the right answer, but it gets painfully slow as the data grows.
**The question it answers:** Why is one way of organising data a thousand times faster than another, and how do I choose?
**Target:** 80–95 pages

## Front matter

Title page · Copyright · Contents · Preface (Who This Book Is For, How This Book Is Organized, How to Use This Book, What You Need Installed, Conventions Used in This Book)

## Part I · Understand

*What to ignore for now:* formal proofs, the maths of recurrences, and competitive-programming tricks.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 1 | Why Some Code Is Slow | My script took one second on 1,000 rows and an hour on a million. | What an algorithm is, counting steps, why growth matters more than speed | 6 |
| 2 | Big-O Without the Fear | People say "that's O(n²)", and I nod without knowing what it means. | Big-O, the common growth rates, best, worst, and average case, time and memory | 7 |
| 3 | Lists in Memory | Adding to the front of my list is slow, but adding to the end is fast. Why? | Arrays and Python lists, linked lists, what each operation costs | 7 |
| 4 | Recursion and Divide and Conquer | A function that calls itself sounds like a bug. | Recursion, the call stack, splitting a problem in half, binary search, remembering answers you've already worked out (memoization) | 7 |

## Part II · Use

*What to ignore for now:* self-balancing tree rotations in detail and exotic structures.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 5 | Hash Tables: Finding Anything Instantly | Looking up one user in a list of a million takes forever. | Hashing, dictionaries and sets, collisions, when hashing fails | 6 |
| 6 | Stacks, Queues, and Heaps | I need to always handle the most urgent task first. | Stacks, queues, priority queues and heaps, `heapq` | 6 |
| 7 | Trees: Sorted and Searchable | I need my data sorted and searchable at the same time. | Binary search trees, balance, B-trees and why databases use them | 6 |
| 8 | Graphs: Data About Connections | My data is about connections: friends, roads, dependencies. | Nodes and edges, representing graphs, breadth-first and depth-first search, weighted edges and what a shortest path is | 6 |
| 9 | Sorting and Searching | Sorting a million rows froze my program. | Simple sorts, merge sort, quicksort, Python's sort, searching sorted data with `bisect` | 6 |

## Part III · Apply

*What to ignore for now:* NP-completeness proofs and advanced graph algorithms.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 10 | Lab: Speed Up a Slow Script | My report script takes ten minutes, and I don't know why. | Timing and profiling, replacing a list with a set or a dictionary, sorting once instead of many times | 7 |
| 11 | Lab: Find the Fastest Route | How does a map app find the fastest route? | Modelling roads as a graph, breadth-first search, Dijkstra's algorithm with a heap | 7 |
| 12 | Lab: Stop Solving the Same Problem Twice | My recursive solution is correct, but it takes forever. | Overlapping subproblems, memoization, building a table (dynamic programming) | 8 |

## Part IV · What Next

| Ch | Chapter | Covers | Pages |
|---|---|---|---|
| 13 | Security, Speed, Failure, and Cost | Slow inputs chosen by attackers, choosing a structure, what breaks at scale, memory cost | 4 |
| 14 | Where to Go from Here | What to learn next, what to skip for now | 3 |

## Appendices

A. Big-O Cheat Sheet · B. Python Data Structures Cheat Sheet · C. Glossary · Index (4 pages)

**Total:** about 90 pages
