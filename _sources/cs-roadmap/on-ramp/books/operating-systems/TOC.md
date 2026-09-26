# Operating Systems from Zero

**The problem you hit:** I start my program and it "just runs", but when it crashes, hangs, or runs out of memory, I don't know where to look.
**The question it answers:** What is the computer actually doing when my code runs?
**Target:** 80–95 pages

## Front matter

Title page · Copyright · Contents · Preface (Who This Book Is For, How This Book Is Organized, How to Use This Book, What You Need Installed, Conventions Used in This Book)

## Part I · Understand

*What to ignore for now:* writing a kernel, assembly language, and hardware details.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 1 | What an Operating System Does | Dozens of programs share one computer, and none of them crash into each other. How? | The operating system's jobs, the kernel and user space, protection | 6 |
| 2 | The Kernel and System Calls | My program says `open("notes.txt")`. Who actually opens it? | System calls, the boundary between program and kernel, watching calls with `strace` | 7 |
| 3 | Processes: Programs in Motion | I ran the same script twice, and now there are two of it. | What a process is, starting processes (`fork` and `exec`), process IDs, parents and children, exit codes | 7 |
| 4 | Threads and Concurrency | My program does one thing at a time, and I want it to do several. | Threads, sharing memory, race conditions, locks, deadlocks, Python's threads and the GIL in brief | 7 |

## Part II · Use

*What to ignore for now:* scheduler internals and file system on-disk formats.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 5 | Scheduling: Sharing the CPU | My computer has 8 cores and runs 300 programs. | Time slices, context switches, priorities, what "load" means | 6 |
| 6 | Memory and Virtual Memory | My program uses 2 GB, but the system says it's using 200 MB. | Address spaces, virtual memory and pages, the stack and the heap, swapping, the OOM killer | 8 |
| 7 | Files and File Systems | I deleted a 5 GB file, and the disk is still full. | Files, directories, inodes, links, file descriptors, mounting, caching and `fsync` | 7 |
| 8 | Input, Output, and Interrupts | My program is "waiting", but for what? | Devices, interrupts, blocking and non-blocking I/O, why disk and network are slow | 6 |

## Part III · Apply

*What to ignore for now:* kernel debugging and performance tuning.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 9 | Lab: Why Is My Program Hanging? | My program isn't crashing. It's just stuck. | Inspecting a stuck process, `ps`, `strace`, finding a deadlock | 7 |
| 10 | Lab: Out of Memory | My program was killed, and there's no error message. | Watching memory grow, finding the OOM killer's message, fixing a leak | 7 |
| 11 | Lab: Too Many Open Files and Other Limits | "Too many open files", but I only opened a few. | File-descriptor leaks, `ulimit`, `lsof`, resource limits | 8 |

## Part IV · What Next

| Ch | Chapter | Covers | Pages |
|---|---|---|---|
| 12 | Security, Speed, Failure, and Cost | Isolation and privileges, what makes programs slow, how programs die, paying for CPU and memory | 5 |
| 13 | Where to Go from Here | What to learn next, what to skip for now | 3 |

## Appendices

A. Process and Memory Tools Cheat Sheet · B. Glossary · Index (4 pages)

**Total:** about 88 pages
