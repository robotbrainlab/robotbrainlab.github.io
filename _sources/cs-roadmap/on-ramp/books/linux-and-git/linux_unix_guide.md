<div style="text-align: justify;">

# The Linux & Unix Guide for Developers

> A complete, project-independent path to becoming genuinely comfortable on Linux and Unix systems — from "what is a shell?" to running and securing production services. It is a standalone guide, but it is also the companion to [The OpenClaw Guide](openclaw/README.md): wherever a Unix concept powers something in OpenClaw, a **🦞 OpenClaw in practice** callout shows you the concrete payoff. Learn the two together and operating an AI agent becomes the project that teaches you Linux.

---

## How to use this guide

Read top to bottom the first time — each section builds on the last, in roughly the order a developer needs them. After that it's a reference; every section stands alone.

Conventions, mirroring the OpenClaw guide so the two feel like one resource:

- **Difficulty tags**: 🟢 **Beginner** (no prior systems knowledge), 🟡 **Intermediate**, 🔴 **Advanced** (production, scale, security).
- **🦞 OpenClaw in practice** callouts connect a Linux skill to the exact place it's used in OpenClaw, linking to the relevant part of the [OpenClaw Guide](openclaw/README.md). These are the mirror image of that guide's **🐧 Linux deep-dive** callouts — together they stitch the two documents into one learning path.
- **🧪 Try it** boxes turn reading into muscle memory. Everything here works on a normal Linux box, a Mac (most of it), or WSL on Windows.
- **You understand this when…** lines give you a completeness check for each major section.

Where commands differ between Linux and macOS, both are shown. The mental models are identical across all Unix-like systems; the flags occasionally differ.

---

## Table of contents

1. [Fundamentals & the Unix Philosophy](#fundamentals--the-unix-philosophy) 🟢
2. [Shells & the Command Line](#shells--the-command-line) 🟢
3. [The Filesystem & FHS](#the-filesystem--fhs) 🟢
4. [Files, Permissions & Ownership](#files-permissions--ownership) 🟢🟡
5. [Users, Groups & sudo](#users-groups--sudo) 🟡
6. [Processes & Signals](#processes--signals) 🟡
7. [Services & Init Systems](#services--init-systems) 🟡🔴
8. [Shells & Scripting](#shells--scripting) 🟡
9. [Text Processing](#text-processing) 🟡
10. [Environment & Configuration](#environment--configuration) 🟢🟡
11. [Package Management & Runtimes](#package-management--runtimes) 🟢🟡
12. [Networking](#networking) 🟡🔴
13. [SSH & Remote Access](#ssh--remote-access) 🟡
14. [Logs & Debugging](#logs--debugging) 🟡🔴
15. [Automation: cron & systemd timers](#automation-cron--systemd-timers) 🟡
16. [Containers & Sandboxing](#containers--sandboxing) 🔴
17. [Servers & Infrastructure](#servers--infrastructure) 🔴
18. [Production Operations & Infrastructure](#production-operations--infrastructure) 🔴
19. [Security Hardening](#security-hardening) 🔴

---

## Fundamentals & the Unix Philosophy

🟢 **Beginner.** Before any commands, the worldview. Unix is not just an operating system; it's a *design philosophy* that, once you internalize it, makes everything else predictable.

### What Linux and Unix actually are

**Unix** is an operating-system design from Bell Labs (1970s). It spawned a family: the BSDs, macOS (which is Unix under the hood), and — most importantly for you — **Linux**, a Unix-*like* kernel written by Linus Torvalds in 1991, now running the overwhelming majority of servers, cloud instances, containers, and Android phones on Earth.

A crucial distinction:

- **The kernel** is the core program that talks to hardware, manages memory, schedules processes, and controls access. "Linux" is, strictly, just the kernel.
- **Userspace** is everything else — the shell, the utilities (`ls`, `grep`, `cat`), the libraries, the desktop. A **distribution** ("distro" — Ubuntu, Debian, Fedora, Arch, Alpine) is the kernel plus a curated userspace plus a package manager.

```
   ┌─────────────────────────────────────────────┐
   │ USERSPACE: your shell, programs, services,   │  ← you live here
   │ libraries, package manager, OpenClaw, …       │
   ├─────────────────────────────────────────────┤
   │            SYSTEM CALL INTERFACE             │  ← the boundary
   ├─────────────────────────────────────────────┤
   │ KERNEL: processes, memory, files, devices,   │  ← privileged
   │ networking, permissions                      │
   ├─────────────────────────────────────────────┤
   │                  HARDWARE                    │
   └─────────────────────────────────────────────┘
```

Programs request privileged operations (open a file, send a packet, start a process) by making **system calls** across that boundary. That boundary is also where *security* lives — the kernel decides whether your process is *allowed* to do what it asked.

### The Unix philosophy

A handful of principles explain almost every design choice you'll meet:

1. **Do one thing well.** Each tool is small and focused (`ls` lists, `grep` searches, `sort` sorts). Power comes from *combining* them.
2. **Everything is a file.** Regular files, directories, devices, sockets, even running-kernel state (`/proc`) are presented as files you can read and write with the same tools. This is why your file skills generalize so far.
3. **Compose with text streams.** Programs read **stdin** and write **stdout**; you connect them with **pipes** (`|`). Text is the universal interface.
4. **Make it scriptable.** Anything you can do interactively, you can automate. The command line *is* a programming language.
5. **Silence is golden.** A command that succeeds usually says nothing. No news is good news; output means something happened (often an error).

> 🦞 **OpenClaw in practice — "everything is a file" is why OpenClaw is transparent.** OpenClaw stores an agent's entire mind — identity, memory, config — as plain Markdown and YAML files you can read, `grep`, diff, and back up. That's the Unix "everything is a file / text is the universal interface" philosophy applied to AI. The skills in this guide (navigating, searching, and editing files) *are* the skills for inspecting an agent. See [OpenClaw Guide → Part 7: Memory](openclaw/07-memory.md) and [Part 4: The Agent's Mind](openclaw/04-agent-mind.md).

### Standards: POSIX

**POSIX** is the standard that keeps Unix-like systems compatible — it specifies the shell, core utilities, and system-call API so a script written on Linux mostly works on macOS or BSD. When someone says a tool is "POSIX-compliant," they mean it follows that portable baseline. It's why the mental models here transfer across every Unix-like system you'll touch.

**You understand this when…** you can explain the difference between the kernel and a distribution, and why "do one thing well + pipes + everything is a file" lets a handful of small tools solve enormous problems.

---

## Shells & the Command Line

🟢 **Beginner.** The shell is the program that reads your typed commands and runs them. It's the single most important tool you'll learn — your primary interface to every Unix system, and a full programming language in its own right.

### What the shell is

When you open a terminal, a **shell** starts. It prints a **prompt**, waits for a line, interprets it, runs the corresponding program(s), shows output, and loops. Common shells: **bash** (the long-time default), **zsh** (default on modern macOS), **fish**, **dash** (minimal, fast, used for scripts). They share the same core grammar; differences are mostly interactive niceties.

The anatomy of a command:

```bash
command  -f  --flag  value  argument
# │        │     │      │       └ what to act on (e.g. a filename)
# │        │     └──────┴──────── options that modify behavior
# └ the program to run
```

### The commands you'll use every hour

```bash
pwd                 # print working directory — where am I?
ls -la              # list files, long format, including hidden (dotfiles)
cd /path/to/dir     # change directory; `cd` alone → home; `cd -` → previous
cd ..               # up one level
mkdir -p a/b/c      # make directories, parents too (-p)
cp src dst          # copy;  cp -r for directories
mv old new          # move/rename
rm file             # remove;  rm -r dir (recursive);  rm -i (confirm each)
cat file            # dump a file;  less file to page through it
head -n 20 file     # first 20 lines;  tail -n 20 file;  tail -f to follow
touch file          # create empty file / update timestamp
find . -name '*.md' # search the tree by name (and much more)
man ls              # the manual — your built-in documentation
ls --help           # quick usage for most commands
```

### Paths: absolute vs relative

- **Absolute** paths start at the root `/`: `/home/you/notes.txt`. Unambiguous from anywhere.
- **Relative** paths start from your current directory: `notes.txt`, `../sibling/file`.
- Shorthands: `~` = your home directory, `.` = here, `..` = parent, `-` (with `cd`) = previous directory.

### Pipes and redirection — the superpower

This is where the Unix philosophy becomes power. Every program has three streams: **stdin** (input, fd 0), **stdout** (output, fd 1), **stderr** (errors, fd 2).

```bash
command > file        # redirect stdout to a file (overwrite)
command >> file       # append stdout to a file
command 2> errors.log # redirect stderr
command < input.txt   # feed a file as stdin
cmd1 | cmd2           # PIPE: cmd1's stdout becomes cmd2's stdin
cmd1 | cmd2 | cmd3    # chain as long as you like
command &> all.log    # both stdout and stderr to one file
```

A real pipeline reads left to right like a sentence:

```bash
# "list processes, find the openclaw one, ignore the grep itself, count them"
ps aux | grep openclaw | grep -v grep | wc -l
```

Internalizing pipes is the moment the command line stops being a list of commands and becomes a *language*.

### Interactive efficiency

- **Tab completion** — start typing, press Tab; the shell completes filenames and commands. Use it constantly.
- **History** — Up/Down to recall commands; `Ctrl-R` to search history; `!!` repeats the last command (`sudo !!` re-runs it with sudo).
- **Line editing** — `Ctrl-A` start of line, `Ctrl-E` end, `Ctrl-U` clear to start, `Ctrl-W` delete a word, `Ctrl-C` cancel the current command, `Ctrl-D` end of input / logout.
- **`Ctrl-L`** clears the screen.

> 🦞 **OpenClaw in practice — the shell is how you operate the Gateway.** Installing OpenClaw, checking it's alive, reading its config, and watching it work are all shell commands: `npm install -g openclaw@latest`, `openclaw dashboard`, `cat ~/.openclaw/openclaw.json`, `journalctl --user -u openclaw -f`. The fluency you build here is exactly the fluency [OpenClaw Guide → Part 2: Installation](openclaw/02-installation.md) assumes.

### 🧪 Try it

1. Navigate to your home dir, `mkdir -p sandbox/a/b`, `cd` into it, and `pwd`. Get back with one `cd`.
2. Create three files and list them with `ls -la`. Then `ls -la | wc -l` and reason about the count.
3. Run `ls /nonexistent > out.txt 2> err.txt` and inspect each file — you've just separated stdout from stderr.
4. Build a pipeline: `history | grep cd | tail -5`.

**You understand this when…** you can chain three commands with pipes to answer a question, and you reach for Tab and `Ctrl-R` without thinking.

---

## The Filesystem & FHS

🟢 **Beginner.** Unix arranges everything into a single tree starting at `/`. Knowing the map means you can find anything and you understand where programs put their files.

### One tree, rooted at `/`

There are no drive letters. Everything — every disk, device, and network mount — hangs off the single root `/`. Additional disks are **mounted** onto directories within that tree (e.g. a backup drive at `/mnt/backup`).

### The Filesystem Hierarchy Standard (FHS)

The **FHS** standardizes what lives where. The directories worth knowing:

| Path | What's there |
|------|--------------|
| `/` | The root of everything. |
| `/home/<user>` | Users' home directories (`~`). Your files and dotfiles live here. (`/Users` on macOS.) |
| `/root` | The root user's home. |
| `/etc` | System-wide **configuration** files (text). "Et cetera," but think "editable text config." |
| `/bin`, `/usr/bin` | **Executables** (programs/commands). |
| `/usr/local/bin` | Locally-installed programs (often where global tools land). |
| `/var` | **Variable** data that changes at runtime: `/var/log` (logs!), spool, caches, databases. |
| `/tmp` | Temporary files, often cleared on reboot. |
| `/opt` | Optional/third-party software packages. |
| `/dev` | **Device** files (disks, terminals) — "everything is a file" made literal. |
| `/proc`, `/sys` | Virtual filesystems exposing live kernel/process state as files. |
| `/mnt`, `/media` | Mount points for extra/removable filesystems. |

### Hidden files and dotfiles

Any file whose name starts with `.` is **hidden** from a normal `ls` (use `ls -a`). This convention is how per-user configuration stays out of the way: `~/.bashrc`, `~/.ssh/`, `~/.gitconfig`, and — for OpenClaw — `~/.openclaw/`. "Dotfiles" are a culture unto themselves; people version-control and share theirs.

### Moving around and finding things

```bash
tree -L 2 ~/.openclaw        # visualize a directory tree (install `tree`)
find /etc -name '*.conf'     # find by name
find . -type f -mtime -1     # files modified in the last day
find . -type d               # only directories
du -sh ~/.openclaw           # total size of a directory
du -sh * | sort -h           # size of each item here, smallest→largest
df -h                        # free space per mounted filesystem
stat file                    # detailed metadata: size, times, permissions, inode
```

### Links

- A **symbolic link** (`ln -s target linkname`) is a pointer to another path — like a shortcut. Ubiquitous for "current version" pointers.
- A **hard link** points to the same underlying data (inode). Less common day-to-day.

> 🦞 **OpenClaw in practice — an agent's mind is a directory tree.** Everything OpenClaw knows lives under `~/.openclaw/` (a hidden dotfile dir in your home): `openclaw.json` for config, `agents/<id>/` per agent, `memory/YYYY-MM-DD.md` for daily logs. Auditing an agent is filesystem work — `du -sh ~/.openclaw/agents/*/` to see which agent's memory is bloating, `find ~/.openclaw -path '*/memory/*.md' -mtime +30` to find old logs to prune. See [OpenClaw Guide → Part 7: Memory](openclaw/07-memory.md).

**You understand this when…** you can predict where a program's config (`/etc` or `~/.something`) and logs (`/var/log`) live before looking, and you can find any file by name, age, or size.

---

## Files, Permissions & Ownership

🟢🟡 **Beginner → Intermediate.** Permissions are how Unix decides who can read, write, and run each file. This is the foundation of *all* Unix security — including, very directly, the security of an autonomous agent.

### Every file has an owner, a group, and a mode

Run `ls -l` and decode the first column:

```
-rw-r--r--  1  deepak  staff  1240  Jun  8 21:00  notes.txt
│└┬┘└┬┘└┬┘     │       │
│ │  │  │      │       └ group that owns it
│ │  │  │      └ user that owns it
│ │  │  └ others' permissions (r--)   → read only
│ │  └ group's permissions   (r--)    → read only
│ └ owner's permissions      (rw-)    → read + write
└ file type: - regular, d directory, l symlink
```

Three permission bits, for three classes of user:

| Bit | On a file | On a directory |
|-----|-----------|----------------|
| **r** (read, 4) | read contents | list entries |
| **w** (write, 2) | modify contents | create/delete/rename entries inside |
| **x** (execute, 1) | run it as a program | **enter/traverse** it (`cd` into it) |

Three classes: **u**ser (owner), **g**roup, **o**thers. So `rwxr-x---` = owner full, group read+enter, others nothing.

### Changing permissions: `chmod`

Two notations — symbolic and numeric (octal):

```bash
chmod u+x script.sh        # add execute for the owner
chmod g-w file             # remove write from group
chmod o= file              # remove all "others" permissions
chmod 600 secret.env       # rw------- : owner read/write, nobody else
chmod 644 notes.txt        # rw-r--r-- : owner rw, everyone read
chmod 755 script.sh        # rwxr-xr-x : owner all, others read+run
chmod -R 750 dir/          # recursive
```

The octal trick: add the values — read 4 + write 2 + execute 1. So `7 = rwx`, `6 = rw-`, `5 = r-x`, `4 = r--`, `0 = ---`. `chmod 600` is the canonical "secret file — only I can read it."

### Changing ownership: `chown` / `chgrp`

```bash
sudo chown deepak file            # change owning user
sudo chown deepak:staff file      # change user and group
sudo chown -R appuser:appuser dir # recursive — common when deploying a service
```

### The execute bit and the shebang

A script needs the `x` bit to run as `./script.sh`. Its first line, the **shebang**, tells the kernel which interpreter to use:

```bash
#!/usr/bin/env bash      # run with bash found on PATH
#!/usr/bin/env node      # run with node
```

### Special bits (briefly)

- **setuid/setgid** — run a program as its *owner's* identity (how `passwd` lets you edit a root-owned file). Powerful and security-sensitive.
- **The sticky bit** on `/tmp` — anyone can create files, but only the owner can delete their own.
- **umask** — the default permissions mask for newly created files (commonly `022`, yielding `644` files / `755` dirs).

### Atomic writes (why it matters)

To change a file safely, well-behaved programs write to a temp file and then `mv` (rename) it over the original. Rename is **atomic** on Unix — a reader sees either the old file or the new one, never a half-written mess. This is how state files survive a crash mid-write.

> 🦞 **OpenClaw in practice — permissions are an agent's security perimeter.** OpenClaw's local execution runs with the permissions of the Unix user the Gateway runs as. "What can a compromised agent do?" reduces to "what can its user read and write?" Channel tokens and API keys belong in `chmod 600` files owned only by that user — a leaked, world-readable token is a stranger driving your bot. And the atomic-write pattern is exactly how an agent's memory files avoid corruption when a heartbeat is interrupted. See [OpenClaw Guide → Part 10: Security](openclaw/10-security.md) and [Part 5: Channels](openclaw/05-channels-control-plane.md).

### 🧪 Try it

1. `touch secret.env`, `chmod 600 secret.env`, then `ls -l` and read the mode aloud.
2. Create a script with a shebang, `chmod +x` it, and run it with `./`. Remove the `x` bit and watch it fail.
3. `umask` to see your default, create a file, and confirm its resulting permissions.

**You understand this when…** you can look at `-rw-r-----`, say who can do what, and produce the same with both `chmod` symbolic and octal forms.

---

## Users, Groups & sudo

🟡 **Intermediate.** Unix is multi-user at its core. Understanding users, groups, and privilege escalation is what lets you run services safely under *least privilege* — the single most important operational security idea.

### Users and groups

Every process runs **as a user**, identified by a numeric **UID**; every user belongs to one or more **groups** (numeric **GIDs**). Permissions ([previous section](#files-permissions--ownership)) are evaluated against the running process's user and groups.

```bash
whoami            # current username
id                # your UID, GID, and all group memberships
groups            # just the groups you're in
who / w           # who's logged in right now
```

Key files (readable text, the Unix way):

- `/etc/passwd` — the user list (username, UID, home dir, login shell). Not passwords despite the name.
- `/etc/group` — groups and their members.
- `/etc/shadow` — the actual (hashed) passwords, readable only by root.

### Types of users

- **root** (UID 0) — the superuser. Can do *anything*; ignores permission checks. Powerful and dangerous.
- **Regular users** — you. Limited to what permissions allow.
- **System/service users** — non-login accounts that own and run services (e.g. `www-data`, `postgres`). Crucial idea: **services should run as their own dedicated, unprivileged user**, not as root and not as you.

### Managing users

```bash
sudo adduser appuser                 # create a user (interactive, Debian/Ubuntu)
sudo useradd -m -s /bin/bash appuser # lower-level equivalent
sudo usermod -aG docker deepak       # ADD user to a group (the -a is vital!)
sudo passwd appuser                  # set/change a password
sudo deluser appuser                 # remove
```

> ⚠️ `usermod -G` *without* `-a` **replaces** all of a user's supplementary groups. Always `-aG` to append. Forgetting the `-a` is a classic way to lock yourself out of `sudo`.

### sudo: borrowing root, briefly

You rarely log in as root. Instead, **`sudo`** runs a single command with elevated privilege, asks for *your* password, and logs it.

```bash
sudo apt update           # run one command as root
sudo -i                   # start an interactive root shell (use sparingly)
sudo -u postgres psql     # run as a different user (not just root)
sudo !!                   # re-run the previous command with sudo
```

Who may use `sudo` is configured in `/etc/sudoers` (edit it **only** with `sudo visudo`, which validates syntax — a broken sudoers file can lock everyone out). Membership in the `sudo` (Debian/Ubuntu) or `wheel` (RHEL/Arch) group typically grants it.

### Least privilege — the principle that runs through everything

Give every user, process, and service **exactly the permissions it needs and no more.** A web app doesn't need root; it needs to read its code and write its data dir. Running things as root "to avoid permission errors" is how a small bug becomes a full system compromise. The disciplined alternative: a dedicated service user with a tightly-scoped home and data directory.

> 🦞 **OpenClaw in practice — run agents as their own least-privileged user.** Because an OpenClaw agent executes with its Unix user's powers, the safest deployment runs the Gateway as a dedicated, unprivileged service user — not your personal account (which can read your SSH keys and delete your files), and never root. In multi-agent setups, isolating sensitive agents as separate users (or containers) is what makes the "isolated by default" guarantee real. See [OpenClaw Guide → Part 10: Security](openclaw/10-security.md) and [Part 9: Multi-Agent Systems](openclaw/09-multi-agent.md).

### 🧪 Try it

1. Run `id` and `groups`; find yourself in `/etc/passwd` with `grep "^$(whoami):" /etc/passwd`.
2. (On a test box) create a `svc` user, make a directory owned by it, and confirm *you* can't write there while `sudo -u svc` can.
3. Inspect who can sudo: `getent group sudo` (or `wheel`).

**You understand this when…** you can explain why a service should run as a dedicated unprivileged user, and you instinctively distrust any instruction to "just run it as root."

---

## Processes & Signals

🟡 **Intermediate.** A process is a running program. Understanding how processes are created, inspected, controlled, and signaled is the core of operating *any* long-running service — and an AI agent's Gateway is exactly that.

### What a process is

When you run a program, the kernel creates a **process**: an instance with its own memory, a numeric **PID** (process ID), an owning user, open **file descriptors** (every open file, socket, and pipe is an fd), and a parent process (**PPID**). Processes form a tree — every process is started by another, all the way up to PID 1 (the init system).

```
   PID 1 (init/systemd)
     └─ sshd
         └─ bash (your shell)
             └─ node  ← e.g. the OpenClaw Gateway
```

### Inspecting processes

```bash
ps aux                  # snapshot of ALL processes (user, PID, CPU%, MEM%, command)
ps aux | grep node      # find a specific one
top                     # live, refreshing process view
htop                    # nicer interactive top (install it) — sort, search, kill
pgrep -fl openclaw      # find PIDs by name pattern
pstree -p               # the process tree with PIDs
lsof -p <PID>           # every file/socket that process has open
```

Reading `ps aux` columns: `%CPU`, `%MEM`, `VSZ`/`RSS` (virtual / resident memory), `STAT` (R running, S sleeping, Z zombie, D uninterruptible), `START`, `TIME` (CPU time used), `COMMAND`.

### Foreground, background, and jobs

```bash
long-command            # runs in the FOREGROUND, ties up your shell
long-command &          # run in the BACKGROUND (returns the prompt)
Ctrl-Z                  # SUSPEND the foreground job
bg                      # resume it in the background
fg                      # bring it back to the foreground
jobs                    # list this shell's jobs
nohup long-command &    # keep running after you log out
```

For anything that must outlive your session, prefer a **terminal multiplexer** (`tmux` or `screen`) or — better for services — an init system (next section).

### Signals — how you talk to a process

A **signal** is an asynchronous message to a process. You send them with `kill` (which, despite the name, just sends signals):

| Signal | Number | Meaning | Default behavior |
|--------|--------|---------|------------------|
| `SIGTERM` | 15 | "Please terminate." | Graceful stop — the **polite default**. |
| `SIGINT` | 2 | Interrupt (`Ctrl-C`). | Stop. |
| `SIGKILL` | 9 | "Die now." | Forced kill — **cannot be caught**; last resort. |
| `SIGHUP` | 1 | Hangup / "reload config." | Many daemons reload on this. |
| `SIGSTOP`/`SIGCONT` | 19/18 | Pause / resume. | — |

```bash
kill <PID>              # sends SIGTERM (graceful) by default
kill -9 <PID>           # SIGKILL — only when SIGTERM won't work
kill -HUP <PID>         # ask a daemon to reload
pkill -f openclaw       # kill by name pattern
```

**Graceful shutdown** is the key concept: a well-written program catches `SIGTERM`, finishes in-flight work, flushes data to disk, and exits cleanly. `SIGKILL` gives it no such chance — which can corrupt files. Reach for `-9` only when graceful stop has failed.

### Resource limits and the OOM killer

The kernel can't conjure infinite memory. When RAM is exhausted, the **OOM (out-of-memory) killer** terminates a process to save the system — and logs it (`dmesg`, `journalctl -k`). `ulimit -a` shows per-process limits (max open files, etc.). "Too many open files" and "killed (OOM)" are two of the most common production failures; both are process-resource issues.

> 🦞 **OpenClaw in practice — the Gateway is one process you supervise with signals.** OpenClaw's Gateway is a single Node process with a PID you can see in `htop`. Stopping it cleanly matters: a `SIGTERM` lets it flush an agent's memory to disk before exiting, while a `SIGKILL` mid-write can corrupt memory files. "Gateway using 100% CPU," "too many open files," and "killed by OOM" are all diagnosed with the tools here. See [OpenClaw Guide → Part 3: Architecture](openclaw/03-architecture.md) and [Part 11: Deployment & Operations](openclaw/11-deployment-operations.md).

### 🧪 Try it

1. Start `sleep 300 &`, find it with `pgrep -fl sleep`, inspect it in `htop`, then `kill` it gracefully.
2. Run `sleep 300` in the foreground; `Ctrl-Z` to suspend, `bg` to background it, `fg` to return, `Ctrl-C` to stop.
3. `lsof -p $$` to see what *your own shell* has open. Notice fds 0/1/2 are your terminal.

**You understand this when…** you can find any process, read its resource use, and explain why you'd send `SIGTERM` before `SIGKILL`.

---

## Services & Init Systems

🟡🔴 **Intermediate → Advanced.** A **service** (a.k.a. **daemon**) is a process meant to run continuously in the background, detached from any terminal. An **init system** is the supervisor that starts services at boot, restarts them on failure, captures their logs, and limits their resources. This is *the* highest-leverage operational topic — master it and you can run any service, including an AI agent.

### What makes a process a daemon

A daemon detaches from the controlling terminal, runs in the background, and typically logs to files or the journal rather than your screen. You don't want to manage one by hand (a closed laptop or dropped SSH session would kill it). You want a supervisor.

### systemd — the modern Linux standard

**systemd** is PID 1 on most Linux distributions. You describe a service in a **unit file** and manage it with `systemctl`.

A minimal service unit (`/etc/systemd/system/myapp.service`, or `~/.config/systemd/user/myapp.service` for a *user* service):

```ini
[Unit]
Description=My App
After=network.target

[Service]
ExecStart=/usr/bin/node /opt/myapp/server.js
WorkingDirectory=/opt/myapp
EnvironmentFile=/opt/myapp/.env       # inject secrets/config as env vars
Restart=on-failure                    # auto-restart if it crashes
RestartSec=5                          # wait 5s between restarts
User=appuser                          # run as a dedicated unprivileged user
MemoryMax=1G                          # cgroup resource cap
CPUQuota=50%

[Install]
WantedBy=multi-user.target            # start at boot
```

Managing it:

```bash
sudo systemctl daemon-reload          # after editing a unit file
sudo systemctl enable myapp           # start at boot
sudo systemctl start myapp            # start now
sudo systemctl status myapp           # running? since when? recent logs?
sudo systemctl restart myapp
sudo systemctl stop myapp             # sends SIGTERM (graceful)
systemctl --user ...                  # for per-user services (no sudo)
```

The big wins encoded in that unit file: **start on boot**, **restart on failure**, **run as a specific user** (least privilege), **resource caps** (cgroups), **environment injection** (secrets without hard-coding), and **graceful `SIGTERM` stop**.

### Logs: journald

systemd captures each service's stdout/stderr into the **journal**:

```bash
journalctl -u myapp                   # all logs for the service
journalctl -u myapp -f                # follow live (like tail -f)
journalctl -u myapp --since "1 hour ago"
journalctl -u myapp -e                # jump to the end
journalctl -u myapp -p err            # only error-priority and worse
journalctl --user -u myapp            # user-service logs
```

### macOS: launchd

macOS uses **launchd** instead of systemd. Services are `.plist` files under `~/Library/LaunchAgents/` (per-user) or `/Library/LaunchDaemons/` (system), managed with `launchctl`:

```bash
launchctl list | grep myapp
launchctl load   ~/Library/LaunchAgents/com.me.myapp.plist
launchctl kickstart -k gui/$(id -u)/com.me.myapp   # restart
```

`KeepAlive` in the plist is launchd's equivalent of `Restart=on-failure`.

### The mental model

```
   boot ──► init system (systemd/launchd, PID 1)
              │ starts, supervises, restarts, logs, limits
              ├─ service A  (running as user A, capped)
              ├─ service B
              └─ service C
```

A *script* runs once and stops. A *service* is a script the init system keeps alive forever. That difference is the whole job of operations.

> 🦞 **OpenClaw in practice — `openclaw onboard --install-daemon` writes one of these units.** That single flag registers the OpenClaw Gateway as a systemd (Linux) or launchd (macOS) service — which is why you then operate it with `systemctl --user status openclaw`, `restart`, and `journalctl --user -u openclaw -f`. Every production concern from [OpenClaw Guide → Part 11](openclaw/11-deployment-operations.md) (restart-on-failure, run-as-dedicated-user, resource caps, graceful shutdown, log capture) is just this unit file, configured well. If you learn one thing here for OpenClaw, learn systemd. See also [Part 2: Installation](openclaw/02-installation.md).

### 🧪 Try it

1. Write a tiny `~/.config/systemd/user/hello.service` that runs a script printing the date every 10s in a loop. `daemon-reload`, `enable --now`, and watch it with `journalctl --user -u hello -f`.
2. Make the script `exit 1` and confirm `Restart=on-failure` brings it back; watch the restart in `status`.
3. Add `MemoryMax=50M` and confirm it shows in `systemctl --user show hello | grep Memory`.

**You understand this when…** you can write a unit file from scratch that runs a program as a dedicated user, restarts on failure, and starts at boot — and read its logs with `journalctl`.

---

## Shells & Scripting

🟡 **Intermediate.** Anything you can type, you can script. Shell scripting is how you turn a sequence of commands into a reusable, automatable tool — the basis of deployment, backups, health checks, and skills.

### A script is just commands in a file

```bash
#!/usr/bin/env bash
set -euo pipefail            # the safety preamble — explained below

echo "Backing up OpenClaw state…"
dest="$HOME/backups/openclaw-$(date +%F).tar.gz"
tar czf "$dest" "$HOME/.openclaw"
echo "Wrote $dest"
```

Make it runnable and run it:

```bash
chmod +x backup.sh
./backup.sh
```

### The safety preamble (use it every time)

```bash
set -e        # exit immediately if any command fails
set -u        # error on use of an unset variable (catches typos)
set -o pipefail  # a pipeline fails if ANY stage fails, not just the last
# combined:
set -euo pipefail
```

Without these, a failing command is silently ignored and your script charges ahead doing damage. This one line prevents a huge class of bugs.

### Variables, quoting, and substitution

```bash
name="Deepak"            # NO spaces around =
echo "Hello, $name"      # double quotes: variables expand
echo 'Hello, $name'      # single quotes: literal, no expansion
today="$(date +%F)"      # command substitution: capture output
count=$(( 3 + 4 ))       # arithmetic
```

> ⚠️ **Always double-quote your variables**: `"$file"`, not `$file`. An unquoted variable containing spaces (or being empty) breaks word-splitting and is the #1 source of shell bugs. `rm -rf "$dir/"` is safe; `rm -rf $dir/` with an empty `$dir` is a catastrophe.

### Conditionals

```bash
if [[ -f "$file" ]]; then
  echo "file exists"
elif [[ -d "$file" ]]; then
  echo "it's a directory"
else
  echo "not found"
fi
```

Common test operators: `-f` file exists, `-d` directory, `-z` empty string, `-n` non-empty, `==`/`!=` string compare, `-eq`/`-lt`/`-gt` numeric, `&&`/`||` and/or.

### Loops

```bash
for f in *.md; do
  echo "processing $f"; wc -w "$f"
done

while read -r line; do
  echo "got: $line"
done < input.txt
```

### Functions, arguments, exit codes

```bash
log() { echo "[$(date +%T)] $*"; }   # $* = all arguments
log "starting"

# script arguments: $1 $2 …, $# = count, "$@" = all (quoted, preferred)
greet() { echo "Hello, ${1:-stranger}"; }   # default if $1 unset

# Every command returns an exit code: 0 = success, non-zero = failure
some_command && echo "ok" || echo "failed"
exit 0
```

The exit code (`$?`) is how scripts and tools chain decisions; it's why `set -e` works and why init systems can detect failure.

### Debugging scripts

```bash
bash -x script.sh        # trace every command as it runs
set -x ... set +x        # trace just a section
shellcheck script.sh     # LINT it — catches quoting bugs and more (install it)
```

`shellcheck` is mandatory: it finds the subtle mistakes (unquoted vars, useless `cat`, wrong test syntax) before they bite.

> 🦞 **OpenClaw in practice — skills and ops are shell scripts.** Many OpenClaw skills bundle a script the agent runs, and your operational glue (backups of `~/.openclaw`, health checks, log triage) is shell scripting. Two lessons transfer directly: (1) auditing a skill means *reading its script* before you let an agent run it with your permissions — the safety preamble and `shellcheck` habits are how you judge it; (2) your backup/restore and monitoring runbooks are scripts you'll write. See [OpenClaw Guide → Part 6: Skills](openclaw/06-skills-plugins.md) and [Part 11: Operations](openclaw/11-deployment-operations.md).

### 🧪 Try it

1. Write the backup script above (with `set -euo pipefail`), run it, and verify the archive with `tar tzf`.
2. Deliberately leave a variable unquoted, give it a value with a space, and watch it break. Quote it and confirm the fix.
3. Run `shellcheck` on a script and fix what it flags.

**You understand this when…** you can write a defensive script (safety preamble, quoted vars, exit codes) that loops over files and does real work, and you `shellcheck` it by reflex.

---

## Text Processing

🟡 **Intermediate.** Unix is built to slice, filter, and transform text streams. These tools — `grep`, `sed`, `awk`, `cut`, `sort`, `jq` — are the power tools of the command line, and since so much of computing is text (logs, config, data, an agent's memory), they pay off constantly.

### grep — search

```bash
grep "error" app.log            # lines containing "error"
grep -i "error" app.log         # case-insensitive
grep -r "TODO" src/             # recursive through a directory
grep -n "error" app.log         # show line numbers
grep -c "error" app.log         # COUNT matching lines
grep -v "debug" app.log         # INVERT: lines NOT matching
grep -E "error|warn" app.log    # extended regex (alternation)
grep -l "needle" *.md           # just the filenames that match
grep -A2 -B2 "error" app.log    # 2 lines of context after/before
```

### Regular expressions (the universal pattern language)

Regex appears in `grep`, `sed`, editors, and most programming languages. The essentials:

| Pattern | Matches |
|---------|---------|
| `.` | any single character |
| `*` | zero or more of the previous |
| `^` / `$` | start / end of line |
| `[abc]` / `[^abc]` | one of / none of |
| `\d` `\w` `\s` | digit / word char / whitespace (in many engines) |
| `+` `?` | one-or-more / optional (extended regex `-E`) |
| `(a|b)` | a or b |

### sed — stream edit (find & replace)

```bash
sed 's/old/new/' file           # replace first match per line
sed 's/old/new/g' file          # replace ALL matches per line
sed -i 's/old/new/g' file       # edit the file IN PLACE
sed -n '10,20p' file            # print only lines 10–20
sed '/^#/d' file                # delete comment lines
```

### awk — field-aware processing

`awk` splits each line into fields (`$1`, `$2`, … ; `$0` is the whole line) — perfect for columns:

```bash
awk '{print $1}' access.log              # first field of each line
awk -F: '{print $1}' /etc/passwd         # custom delimiter (colon)
awk '$3 > 100 {print $1, $3}' data       # filter by a column value
awk '{sum+=$1} END {print sum}' nums     # sum a column
ps aux | awk '{print $2, $11}'           # PID and command
```

### cut, sort, uniq, tr, wc — the supporting cast

```bash
cut -d',' -f2 data.csv          # field 2, comma-delimited
sort file                       # sort lines;  sort -n numeric;  sort -r reverse
sort -h                         # human-readable sizes (2K, 5M…)
uniq -c                         # count adjacent duplicates (sort first!)
tr 'a-z' 'A-Z'                  # translate/transform characters
wc -l / -w / -c                 # count lines / words / bytes
```

The classic "top 10 most frequent" idiom composes them:

```bash
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head
```

### jq — JSON on the command line

Config and APIs are JSON; `jq` is the `grep`/`awk` for it:

```bash
jq . config.json                       # pretty-print
jq '.channels' ~/.openclaw/openclaw.json   # extract a field
jq '.items[] | .name' data.json        # iterate an array, pull a field
curl -s api/url | jq '.results | length'   # query an API response
```

(`yq` does the same for YAML.)

> 🦞 **OpenClaw in practice — these tools are how you read an agent's mind.** OpenClaw's config is JSON (`jq '.channels' ~/.openclaw/openclaw.json`) and its memory is Markdown (`grep -rl "deploy server" ~/.openclaw/*/memory/` to find which day the agent learned something; `wc -w MEMORY.md` to check memory isn't bloating; `grep -ri "token" ~/.openclaw` to audit for leaked secrets). Because the agent is plain text, text-processing fluency *is* agent-introspection fluency. See [OpenClaw Guide → Part 7: Memory](openclaw/07-memory.md) and [Part 2: Installation](openclaw/02-installation.md).

### 🧪 Try it

1. Find the 5 most common words in any text file with a `tr | sort | uniq -c | sort -rn | head` pipeline.
2. `jq` a field out of any JSON file on your system (try `~/.openclaw/openclaw.json` if present).
3. Use `sed -i` to rename a term across a copy of a file, and `grep -c` to confirm the count changed.

**You understand this when…** you can answer a question about a log or data file by composing `grep`/`awk`/`sort`/`uniq`/`jq` into one pipeline, without writing a program.

---

## Environment & Configuration

🟢🟡 **Beginner → Intermediate.** The environment is the set of named values every process inherits. It's how configuration and secrets reach programs without hard-coding them — a concept you'll use constantly for services and deployments.

### Environment variables

Each process has a set of **environment variables** — `KEY=value` pairs it inherits from its parent. They configure behavior without changing code.

```bash
printenv               # show all environment variables
echo "$HOME"           # one variable
echo "$PATH"           # the command search path
export API_KEY="abc"   # set a variable AND export it to child processes
API_KEY="abc" ./run.sh # set just for this one command
unset API_KEY          # remove it
```

A variable set without `export` exists only in the current shell; **`export`** makes it available to programs the shell launches. This parent→child inheritance is the whole model: your shell exports vars, and the `node`/`python`/service it starts sees them.

### PATH — how commands are found

`PATH` is a colon-separated list of directories. When you type `node`, the shell searches them **left to right** and runs the first match:

```bash
echo "$PATH"           # e.g. /home/you/.nvm/.../bin:/usr/local/bin:/usr/bin:/bin
which node             # which one wins
type -a node           # ALL matches, in order
```

"Command not found" almost always means the program's directory isn't on `PATH`. Tools like `nvm`, `pyenv`, and virtualenvs work precisely by *prepending* their directory to `PATH` so their version wins.

### Where environment is configured

- **Interactive shells** read startup files: `~/.bashrc` / `~/.bash_profile` (bash), `~/.zshrc` (zsh). Put your `export`s and aliases here.
- **Login shells** vs **non-login**, **interactive** vs **non-interactive** read different files — a frequent source of "why isn't my variable set in cron/systemd?" The fix is usually to set it explicitly in the service/cron environment, not rely on `~/.bashrc`.
- **Services** get environment from their unit (`Environment=`, `EnvironmentFile=` in systemd), **not** from your shell rc files.

### The `.env` file pattern

The community convention for app config and secrets:

```bash
# .env  (chmod 600, and add to .gitignore!)
API_KEY=sk-...
DATABASE_URL=postgres://...
PORT=8080
```

Loaded by the app, by `EnvironmentFile=/path/.env` in a systemd unit, or with `set -a; source .env; set +a` in a script. The golden rules: **never commit `.env` to git**, and **`chmod 600`** it.

> 🦞 **OpenClaw in practice — env vars carry OpenClaw's location and secrets.** OpenClaw reads `OPENCLAW_HOME`, `OPENCLAW_STATE_DIR`, and `OPENCLAW_CONFIG_PATH` from the environment to find its files, and its config references channel tokens via `${VAR}` interpolation so secrets live in the environment, not in `openclaw.json`. When you run the Gateway as a systemd service, those vars come from an `EnvironmentFile=`, not your shell — exactly the parent→child inheritance and "services don't read .bashrc" lessons above. And `PATH` is why `which openclaw` and a correctly-selected `node` matter at install time. See [OpenClaw Guide → Part 2: Installation](openclaw/02-installation.md) and [Part 5: Channels](openclaw/05-channels-control-plane.md).

### 🧪 Try it

1. `export GREETING=hi`, then run `bash -c 'echo $GREETING'` (child sees it). Set it without `export` and confirm the child does *not*.
2. `echo "$PATH"`, then `which` three commands you use and confirm which directory each comes from.
3. Make a `.env`, `chmod 600` it, `source` it with `set -a`, and confirm the vars are present.

**You understand this when…** you can explain why a variable in `~/.bashrc` isn't visible to a systemd service, and you keep secrets in a `chmod 600` `.env` that's git-ignored.

---

## Package Management & Runtimes

🟢🟡 **Beginner → Intermediate.** Package managers install, update, and remove software and its dependencies. Knowing your system's package manager — and how language runtimes are versioned — is how you set up and maintain any machine.

### System package managers

Each distro family has one:

| Family | Manager | Install | Update index | Upgrade all |
|--------|---------|---------|--------------|-------------|
| Debian/Ubuntu | **apt** | `sudo apt install pkg` | `sudo apt update` | `sudo apt upgrade` |
| RHEL/Fedora | **dnf** (yum) | `sudo dnf install pkg` | (automatic) | `sudo dnf upgrade` |
| Arch | **pacman** | `sudo pacman -S pkg` | `sudo pacman -Sy` | `sudo pacman -Syu` |
| Alpine | **apk** | `sudo apk add pkg` | `sudo apk update` | `sudo apk upgrade` |
| macOS | **Homebrew** | `brew install pkg` | `brew update` | `brew upgrade` |

The two-step pattern on Debian/Ubuntu trips up newcomers: `apt update` refreshes the *list of available* packages; `apt upgrade` actually *installs* newer versions. Run `update` before installing so you get current versions.

```bash
apt list --installed | grep node    # is it installed?
apt show nginx                      # package details
sudo apt remove pkg                 # remove;  apt purge also deletes config
```

### Keeping a system patched

Security updates ship through these managers. **Applying them promptly is a core security duty** — an unpatched package is a known vulnerability you've chosen to keep. On servers, `unattended-upgrades` (Debian/Ubuntu) can apply security patches automatically.

### Language runtimes and version managers

You usually want a *specific* version of a runtime per project, not whatever the OS ships. Use a **version manager**:

- **Node:** `nvm` (or `fnm`, `volta`) — `nvm install 24 && nvm use 24`.
- **Python:** `pyenv` + virtual environments (`python -m venv .venv && source .venv/bin/activate`).
- **Ruby/Java/etc.:** `rbenv`, `sdkman`, or the universal `asdf`/`mise`.

Version managers work by manipulating `PATH` ([previous section](#environment--configuration)) so the chosen version's binary is found first. They also let you avoid `sudo` for global installs by keeping everything in your home directory.

### npm — Node's package manager (you'll use this for OpenClaw)

```bash
npm install -g pkg        # install a global CLI tool
npm install pkg           # install into the current project (./node_modules)
npm update                # update packages
npm list -g --depth=0     # list global packages
npx pkg                   # run a package without installing it globally
```

> ⚠️ Avoid `sudo npm install -g` on a system-managed Node — it scatters root-owned files into your home and causes `EACCES` headaches. The clean fix is a version manager (`nvm`) so the global directory lives in *your* home and needs no `sudo`. This is really a permissions/ownership lesson ([Files & Permissions](#files-permissions--ownership)).

> 🦞 **OpenClaw in practice — OpenClaw is an npm package on a managed Node.** You install it with `npm install -g openclaw@latest` on **Node 24 (or 22.19+)**, ideally provisioned via `nvm` so no `sudo` is needed and you can pin the version. Keeping OpenClaw **updated** through npm is a direct security control — its CVE fixes ship as new versions (e.g. the control-plane RCE patched in `2026.1.29`). The "patch promptly" and "use a version manager" habits here are exactly what [OpenClaw Guide → Part 2](openclaw/02-installation.md) and [Part 10: Security](openclaw/10-security.md) rely on.

### 🧪 Try it

1. Identify your package manager and run its "update index" + "list installed" commands.
2. Install `nvm`, then `nvm install 24` and `nvm use 24`; confirm with `which node` that the nvm version wins on `PATH`.
3. `npm install -g` a small CLI (e.g. `cowsay`) without `sudo` and run it — proving the version-manager approach avoids permission pain.

**You understand this when…** you can set up a specific runtime version cleanly (no `sudo`), explain how the version manager hijacks `PATH`, and know that patching is security work.

---

## Networking

🟡🔴 **Intermediate → Advanced.** Almost every service talks over the network. Understanding addresses, ports, sockets, DNS, and the tools to inspect them is essential for connecting things, debugging "it won't connect," and securing what's exposed.

### The layers, briefly

You don't need the full OSI model, but the working mental stack is:

```
   Application   HTTP, WebSocket, SSH, DNS      ← what your program speaks
   Transport     TCP (reliable), UDP (fast)     ← ports live here
   Internet      IP (addresses, routing)        ← IP addresses
   Link          Ethernet, Wi-Fi                ← the physical-ish layer
```

### IP addresses, ports, and sockets

- An **IP address** identifies a machine (`192.168.1.10`, or IPv6 `::1`).
- A **port** (0–65535) identifies a *service* on that machine. Web = 80/443, SSH = 22, DNS = 53.
- A **socket** is the combination `IP:port` — one endpoint of a connection.
- **`127.0.0.1` / `localhost`** is the loopback — *this machine only*. **`0.0.0.0`** means "all interfaces" — reachable from the network. **This distinction is a security decision:** binding a service to `127.0.0.1` keeps it private; binding to `0.0.0.0` exposes it.

### Inspecting connections

```bash
ss -tlnp                 # listening TCP sockets + the process (the modern netstat)
ss -tunap                # all TCP/UDP sockets
lsof -iTCP:18789 -sTCP:LISTEN   # what's listening on a specific port
ip addr                  # this machine's IP addresses (modern `ifconfig`)
ip route                 # routing table — how packets leave
```

"Is anything actually listening on that port?" (`ss -tlnp | grep <port>`) is the first question when a connection fails.

### DNS — names to addresses

DNS translates `example.com` → an IP. Tools:

```bash
dig example.com          # full DNS query/answer
dig +short example.com   # just the IP
nslookup example.com     # simpler query
getent hosts example.com # resolve via the system resolver
cat /etc/hosts           # static local overrides (checked before DNS)
cat /etc/resolv.conf     # which DNS servers the system uses
```

DNS issues masquerade as everything else; when a hostname won't connect but the IP will, suspect DNS.

### Talking to services: curl

```bash
curl https://api.example.com           # GET
curl -i https://example.com            # include response headers
curl -sf https://example.com >/dev/null && echo UP   # health check idiom
curl -X POST -H 'Content-Type: application/json' \
     -d '{"k":"v"}' https://api/endpoint
curl -s https://api/data | jq .         # pipe JSON into jq
```

`curl` is your universal "does this endpoint respond, and with what?" tool.

### Firewalls

A firewall controls which ports are reachable from where. Default-deny inbound, allow only what you need:

```bash
sudo ufw allow 22/tcp     # allow SSH (Ubuntu's simple firewall)
sudo ufw enable
sudo ufw status
```

(`nftables`/`iptables` are the lower-level mechanism; cloud providers add **security groups** at the network edge.)

> 🦞 **OpenClaw in practice — the control plane lives on `127.0.0.1:18789`.** OpenClaw's Gateway exposes a WebSocket control plane on **port 18789, bound to localhost by default** — a deliberate "private, not network-exposed" choice. When something won't connect, you check it with `ss -tlnp | grep 18789` and `curl -i http://127.0.0.1:18789/`. The localhost-vs-`0.0.0.0` distinction is the crux of a real OpenClaw vulnerability (a malicious web page reaching the control plane → RCE), so *never* expose that port to the network. See [OpenClaw Guide → Part 3: Architecture](openclaw/03-architecture.md) and [Part 10: Security](openclaw/10-security.md).

### 🧪 Try it

1. `ss -tlnp` and identify three services listening on your machine and their ports.
2. `dig +short` a domain, then `curl -i` it and read the status line and headers.
3. Build a one-line health check for any local service with the `curl -sf … && echo UP` idiom.

**You understand this when…** you can answer "is it listening, on which interface, and can I reach it?" with `ss`, `curl`, and `dig`, and you can explain why `127.0.0.1` vs `0.0.0.0` is a security choice.

---

## SSH & Remote Access

🟡 **Intermediate.** **SSH** (Secure Shell) is how you securely log into and operate remote machines. For anyone running a server — including an always-on AI agent — SSH is the daily front door. It's also a Swiss-army knife for tunneling and file transfer.

### Logging in

```bash
ssh user@host                 # log into a remote machine
ssh -p 2222 user@host         # non-default port
```

The first connection asks you to verify the host's fingerprint (trust-on-first-use), then records it in `~/.ssh/known_hosts`.

### Key-based authentication (do this, disable passwords)

Passwords are weak and brute-forceable. **SSH keys** are a public/private keypair: the public key goes on the server, the private key stays secret on your laptop.

```bash
ssh-keygen -t ed25519 -C "you@laptop"     # generate a modern keypair
ssh-copy-id user@host                     # install your public key on the server
ssh user@host                             # now logs in with no password
```

The private key (`~/.ssh/id_ed25519`) must be `chmod 600` and never leave your machine. `ssh-agent` holds it unlocked for a session so you don't retype the passphrase.

### The SSH config file — quality of life

`~/.ssh/config` turns long commands into short aliases:

```
Host myserver
    HostName 203.0.113.5
    User deepak
    Port 22
    IdentityFile ~/.ssh/id_ed25519
```

Now `ssh myserver` just works. You can also define jump hosts, keep-alives, and per-host keys here.

### Moving files

```bash
scp file.txt user@host:/path/        # copy a file to the server
scp -r dir user@host:/path/          # recursively
rsync -avz dir/ user@host:/path/     # efficient sync (only changed bytes); ideal for backups
rsync -avz --delete src/ dst/        # mirror, deleting extras (careful!)
```

`rsync` is the workhorse for backups and deployments because it transfers only differences and can resume.

### Tunneling — SSH's superpower

**Local port forwarding** lets you reach a private service on a remote machine through the encrypted SSH connection, without exposing it publicly:

```bash
ssh -L 18789:127.0.0.1:18789 user@host
# now http://127.0.0.1:18789 on YOUR laptop reaches the server's localhost:18789
```

This is the canonical secure way to use a localhost-only service remotely. (Reverse forwarding `-R` and dynamic SOCKS `-D` exist too.)

### Keeping remote work alive

A dropped SSH session kills foreground programs. Run long tasks under **`tmux`** (or `screen`): start `tmux`, do your work, detach with `Ctrl-B d`, reconnect later with `tmux attach`. Your session survives disconnects.

> 🦞 **OpenClaw in practice — you operate a remote agent over SSH.** Running OpenClaw on an always-on box means SSH is how you reach it: key-based login, a `~/.ssh/config` alias, `rsync` to back up `~/.openclaw` off-box, and — crucially — **`ssh -L 18789:127.0.0.1:18789`** to open the dashboard of a remote Gateway *without ever exposing its control plane to the internet*. That localhost-binding + SSH-tunnel pattern is the secure-by-default way to manage any sensitive local service remotely. See [OpenClaw Guide → Part 5: Channels & Control Plane](openclaw/05-channels-control-plane.md) and [Part 11: Operations](openclaw/11-deployment-operations.md).

### 🧪 Try it

1. Generate an `ed25519` key, `ssh-copy-id` it to a box you control (or a free-tier VM), and confirm passwordless login.
2. Add a `~/.ssh/config` alias and log in with just `ssh <alias>`.
3. Set up an `ssh -L` tunnel to some service on the remote box and reach it locally. Reflect on why nothing was exposed publicly.
4. Start a `tmux` session, run something, detach, reconnect.

**You understand this when…** you log into a server with keys (no password), reach a private remote service through an `ssh -L` tunnel, and keep long jobs alive with `tmux`.

---

## Logs & Debugging

🟡🔴 **Intermediate → Advanced.** When something breaks, logs are where the truth is. Debugging on Unix is a disciplined skill: know where logs live, read them effectively, and diagnose layer by layer until you find the failure.

### Where logs live

- **systemd journal** — most modern services log here: `journalctl` ([Services section](#services--init-systems)).
- **`/var/log/`** — traditional log files: `/var/log/syslog`, `/var/log/auth.log` (logins/sudo), `/var/log/nginx/`, app-specific dirs.
- **App-specific locations** — many apps log to their own data dir.
- **`dmesg` / `journalctl -k`** — kernel messages (hardware, OOM killer).

### Reading logs effectively

```bash
journalctl -u myapp -f                  # follow a service's logs live
journalctl -u myapp --since "10 min ago" --no-pager
journalctl -p err -b                    # errors since this boot
tail -f /var/log/syslog                 # follow a file
grep -i error /var/log/app.log | tail   # filter then look at recent
zcat /var/log/app.log.1.gz | grep error # search rotated (compressed) logs
```

For structured (JSON) logs, pipe through `jq`. Correlate related lines with a **request/trace ID** — searching one ID across logs reconstructs a single request's journey, the most powerful debugging move in a busy system.

### Log rotation

Logs grow forever and will fill a disk if unmanaged. **`logrotate`** rotates, compresses, and deletes old logs on a schedule (config in `/etc/logrotate.d/`). journald has its own size limits (`journalctl --vacuum-size=500M`). "Disk full because of unrotated logs" is one of the most common production outages — and entirely preventable.

### The four golden signals

When watching a service's health, track: **latency** (how long requests take), **traffic** (how many), **errors** (how many fail), **saturation** (how full the resources are — CPU, memory, disk, fds). A change in any one is your early warning.

### Debugging by layer

The fastest debugging picks the right layer first, then drills:

```
   1. Is the MACHINE ok?   df -h (disk full?), free -h (OOM?), uptime (load?)
   2. Is the NETWORK ok?   ss -tlnp (listening?), curl (responds?), dig (DNS?)
   3. Is the APP ok?       journalctl/logs (errors? stack traces? restarts?)
   4. Is the STATE ok?     bad config? corrupt data? a recent change? (git diff)
```

The two most common "why did it die" causes are gloriously mundane: **disk full** (find the hog with `du -sh * | sort -h`) and **out-of-memory** (the OOM killer, in `dmesg`/`journalctl -k`). Check those before exotic theories.

### Deeper tools (when you need them)

```bash
strace -p <PID>          # trace the system calls a process makes (what is it doing?)
lsof -p <PID>            # what files/sockets it has open
ltrace, gdb              # library-call tracing, interactive debugging
vmstat 1 / iostat / pidstat   # live system/IO/per-process stats
```

`strace` answering "what is this stuck process actually trying to do?" feels like magic the first time.

### Reproduce, isolate, fix, verify

A reliable method: **reproduce** the failure (ideally minimally), **isolate** the layer/component, **fix** the root cause (not just the symptom), **verify** the fix actually resolves it, and write a **blameless post-mortem** so the next person (or you, in six months) benefits.

> 🦞 **OpenClaw in practice — diagnosing a down agent is layer-by-layer debugging.** When the Gateway misbehaves: `systemctl --user status openclaw` (running? crash-looping?), `journalctl --user -u openclaw -e` (the error), `df -h` (disk full — often from unbounded agent memory/daily logs, exactly the log-rotation problem above), `free -h` (OOM?), `ss -tlnp | grep 18789` (listening?), and `jq . openclaw.json` + `git diff` the workspace (bad config/state?). The recovery runbook in [OpenClaw Guide → Part 11](openclaw/11-deployment-operations.md) *is* this method. An agent's memory directory is also a log directory — rotate and age it out or it fills the disk ([Part 7](openclaw/07-memory.md)).

### 🧪 Try it

1. `journalctl -p err -b --no-pager | tail` and read your machine's recent errors.
2. `du -sh /var/log/* | sort -h` to see which logs are largest; reason about rotation.
3. Practice the layer drill on any service: machine → network → app → state, one command each.
4. `strace -f -e trace=openat ls` and watch `ls` open files. Demystifying, isn't it?

**You understand this when…** when something breaks you can name the failing layer within a couple of minutes and have the right diagnostic command ready — and you check disk and memory before anything exotic.

---

## Automation: cron & systemd timers

🟡 **Intermediate.** Recurring work — backups, cleanups, health checks, scheduled jobs — should run automatically, not from memory. Unix has two main schedulers: classic **cron** and modern **systemd timers**.

### cron

`cron` runs commands on a schedule defined in a **crontab**:

```bash
crontab -e        # edit your crontab
crontab -l        # list it
```

A crontab line is five time fields plus a command:

```
# ┌ minute (0–59)
# │ ┌ hour (0–23)
# │ │ ┌ day of month (1–31)
# │ │ │ ┌ month (1–12)
# │ │ │ │ ┌ day of week (0–6, Sun=0)
# │ │ │ │ │
  0 2 * * *   /home/me/backup.sh         # every day at 02:00
  */15 * * * * /home/me/healthcheck.sh    # every 15 minutes
  0 9 * * 1   /home/me/weekly-report.sh   # Mondays at 09:00
```

### The classic cron gotchas

- **Timezone trap.** cron uses the *system* timezone (often UTC on servers). "Runs at 9am" may not be *your* 9am. Be explicit; on servers, think in UTC.
- **Minimal environment.** cron jobs run with a bare environment — your `PATH` and shell vars from `~/.bashrc` are **not** loaded. Use absolute paths and set needed vars inside the job/script.
- **Silent failure.** If a job fails, you may never know. Capture output (`>> /var/log/myjob.log 2>&1`) and/or alert on failure. cron mails output to the local user by default — usually unread.
- **Overlap.** If a job runs longer than its interval, the next one starts anyway, and now two run at once. Guard with a **lockfile** (`flock`):
  ```bash
  */5 * * * * /usr/bin/flock -n /tmp/job.lock /home/me/job.sh
  ```

### systemd timers (the modern alternative)

A timer unit triggers a service unit. More verbose than cron, but with real advantages: logs in the journal, dependency ordering, `Persistent=true` to catch up missed runs (e.g. machine was asleep), randomized delays, and resource limits.

```ini
# backup.timer
[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true
[Install]
WantedBy=timers.target
```

```bash
systemctl --user enable --now backup.timer
systemctl --user list-timers           # see all timers and next run times
```

`list-timers` answering "what's scheduled and when does it next fire?" is something cron can't do cleanly.

### Idempotency — the rule for all scheduled work

A scheduled job may run more than you expect (retries, overlaps, catch-up runs). **Make it idempotent**: safe to run repeatedly without duplicating or corrupting. Patterns: check-before-acting, a marker/state file recording what's done, atomic writes, and lockfiles to prevent concurrent runs. Monitor **missed** runs, not just failed ones — a job that silently stopped firing is the scariest kind.

> 🦞 **OpenClaw in practice — the heartbeat is a smart cron.** OpenClaw's autonomy comes from a **heartbeat** (~every 30 min) that, like a cron job, fires on a schedule and decides whether to act — except it asks an LLM "is anything due?" Everything that makes cron jobs fail (timezone confusion, silent failure, overlap, non-idempotency) applies to the heartbeat: each `HEARTBEAT.md` item must be **idempotent** (check → act-if-needed → record, guarded by a marker/lock) or restarts and extra ticks cause duplicates. You'll also use real cron/timers for OpenClaw ops — nightly `~/.openclaw` backups, log pruning. See [OpenClaw Guide → Part 8: Autonomy](openclaw/08-autonomy.md).

### 🧪 Try it

1. Add a cron job that appends the date to a log every minute (`* * * * * date >> ~/cron.log`). Confirm it runs, then remove it.
2. Reproduce the environment gotcha: a cron job that calls a command by bare name and fails because `PATH` is minimal; fix it with an absolute path.
3. Wrap a job in `flock` and prove two can't run at once.
4. Write a `systemd` timer + service pair and inspect it with `list-timers`.

**You understand this when…** you can schedule a recurring job two ways (cron and a timer), make it idempotent and lock-guarded, and explain why you monitor missed runs.

---

## Containers & Sandboxing

🔴 **Advanced.** A **container** packages an application with its dependencies and runs it in an isolated environment — its own filesystem, network, and process view — while sharing the host kernel. Containers are how modern software is shipped, and **sandboxing** is how you safely run code you don't fully trust.

### What a container actually is

A container is *not* a virtual machine. It's a normal Linux process that the kernel has **isolated** using two features:

- **Namespaces** — give the process its own view of the system: its own process tree (it sees itself as PID 1), its own filesystem mount, its own network stack, its own hostname. It can't see the host's other processes or files.
- **cgroups (control groups)** — limit and account for resources: this container gets at most 512MB RAM and 1 CPU.

So a container is "a process in a box," far lighter than a VM (no second kernel, near-instant start), but sharing — and therefore trusting — the host kernel.

### Docker / Podman basics

```bash
docker run -it ubuntu bash          # run a container interactively
docker run -d --name web -p 8080:80 nginx   # detached, map host:container port
docker ps                           # running containers
docker logs web                     # its logs
docker exec -it web bash            # shell into a running container
docker stop web && docker rm web    # stop and remove
docker images                       # local images
```

(`podman` is a daemonless, rootless-friendly drop-in with the same commands.)

### Dockerfiles — building an image

```dockerfile
FROM node:24-slim
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
USER node                 # don't run as root inside the container!
CMD ["node", "server.js"]
```

`docker build -t myapp .` produces a reproducible image you can run anywhere. **Volumes** (`-v host:container`) persist data outside the container's ephemeral filesystem; **networks** connect containers; **docker compose** declares multi-container stacks in one YAML file.

### Containers for isolation and sandboxing

Containers shine for running untrusted or risky code with limited blast radius:

- **Read-only filesystem** (`--read-only`) so the code can't modify anything unexpected.
- **Drop capabilities** (`--cap-drop=ALL`), **no new privileges** (`--security-opt=no-new-privileges`).
- **Resource caps** (`--memory`, `--cpus`) so it can't exhaust the host.
- **Restricted network** (`--network none`, or an egress-limited network) so it can't phone home or exfiltrate.
- **Run as non-root inside** (`USER`), and ideally **rootless** on the host.

For stronger isolation than containers (which share the kernel), step up to a **VM** or kernel-level sandboxes (`gVisor`, `firecracker`, `seccomp` profiles, `bubblewrap`).

> 🦞 **OpenClaw in practice — sandbox untrusted agents and skills.** OpenClaw supports **per-agent sandbox modes**: an untrusted agent can run in a containerized environment with limited tools (read-only, no exec) while a trusted one runs on the host. Because skills can carry arbitrary code (~26% of audited community skills had vulnerabilities), running risky agents/skills in a container — non-root, read-only FS, dropped caps, restricted egress — is how you cap the damage a malicious skill or a prompt-injection attack can do. Official guidance is to run OpenClaw "in an isolated environment — a dedicated VM or container, not your daily driver." See [OpenClaw Guide → Part 9: Multi-Agent](openclaw/09-multi-agent.md), [Part 10: Security](openclaw/10-security.md), and [Part 6: Skills](openclaw/06-skills-plugins.md).

### 🧪 Try it

1. `docker run -it --rm alpine sh`; inside, run `ps aux` (you're PID 1, you can't see the host) and `ls /` (a fresh filesystem). Exit; it's gone.
2. Run something with `--memory=64m --read-only --network none` and observe the limits bite.
3. Write a tiny Dockerfile for a hello-world server, build it, run it with a port mapping, and `curl` it.

**You understand this when…** you can containerize an app, run untrusted code with read-only FS / no network / non-root / capped resources, and explain why a container shares the kernel (and a VM doesn't).

---

## Servers & Infrastructure

🔴 **Advanced.** Bringing it together: provisioning a server from scratch and turning it into a place that reliably runs services. This is the end-to-end "I have a cloud VM, now what?" workflow.

### Provisioning a fresh server

The standard first-hour checklist on a new cloud VM (a "VPS"):

1. **Log in** as the provided user (often `root`) over SSH.
2. **Create a non-root user** with sudo, and stop using root directly:
   ```bash
   adduser deepak && usermod -aG sudo deepak
   ```
3. **Set up SSH keys** for that user; **disable password and root login** ([Security Hardening](#security-hardening)).
4. **Update everything**: `apt update && apt upgrade -y`.
5. **Firewall**: default-deny inbound, allow SSH (and only the ports you need):
   ```bash
   ufw allow OpenSSH && ufw enable
   ```
6. **Install runtimes** (Node via `nvm`, etc.) and your app.
7. **Run the app as a service** under systemd, as a dedicated user.
8. **Set up backups and monitoring** ([next section](#production-operations--infrastructure)).

### Reverse proxies and TLS

A **reverse proxy** (nginx, Caddy, Traefik) sits in front of your app and handles TLS termination (HTTPS), routing, load balancing, and rate limiting. Caddy even gets certificates automatically:

```
# Caddyfile — automatic HTTPS via Let's Encrypt
app.example.com {
    reverse_proxy 127.0.0.1:8080
}
```

The pattern: your app listens on **localhost only**; the proxy is the single public-facing, TLS-terminating, authenticated front door. This keeps the app private and centralizes security.

### Infrastructure as Code

Beyond hand-provisioning, real infrastructure is **declared in code** so it's reproducible: **Terraform/OpenTofu** to create cloud resources, **Ansible** to configure servers, **Docker Compose / Kubernetes** to run containers. The principle — *describe the desired state, let the tool converge to it* — beats clicking in a console because it's versionable, reviewable, and repeatable.

### The "cattle, not pets" idea

Treat servers as **disposable and reproducible** (cattle), not hand-tuned irreplaceable snowflakes (pets). If a box dies, you should be able to recreate it from code + backups, not from memory. This mindset is what makes scaling and recovery sane.

> 🦞 **OpenClaw in practice — deploying an agent is this exact workflow.** Standing up an always-on OpenClaw agent means: provision a small VM, create a non-root user, harden SSH, firewall everything but SSH, install Node via nvm, install OpenClaw, run the Gateway as a systemd service under a dedicated user, and reach it over an SSH tunnel (its control plane stays localhost-only — no public reverse proxy needed unless you deliberately expose it). "Deploy my OpenClaw agent to a VPS and harden it" is one of the best hands-on projects for learning everything in this section. See [OpenClaw Guide → Part 11: Deployment & Operations](openclaw/11-deployment-operations.md).

### 🧪 Try it

1. On a free-tier or cheap VM, run the provisioning checklist end to end: non-root sudo user, SSH keys, disable password login, firewall, updates.
2. Deploy any small app as a systemd service running as a dedicated user.
3. (Optional) Put Caddy in front of it for automatic HTTPS on a domain you own.

**You understand this when…** you can take a blank cloud VM to "hardened box running my service as a supervised, non-root systemd unit behind a firewall" without looking up each step.

---

## Production Operations & Infrastructure

🔴 **Advanced.** Running a service in production is an ongoing discipline, not a one-time deploy. This section covers the operational pillars: monitoring, backups, recovery, and the practices that keep a system trustworthy over time.

### Observability: the three pillars

- **Logs** — discrete events ([Logs & Debugging](#logs--debugging)). Centralize them off-box so a dead/compromised machine doesn't take its logs with it.
- **Metrics** — numbers over time (CPU, memory, request rate, error rate, cost). Tools: Prometheus + Grafana, or your cloud's monitoring. Track the **four golden signals**.
- **Traces** — the path of a single request through a system. Invaluable in distributed systems.

A practical minimum: a health-check endpoint, alerting on **symptoms** (error rate up, latency up, disk filling) rather than every cause, and a dashboard you actually look at. Beware **alert fatigue** — too many alerts and people ignore the real one.

### Health checks

- **Shallow** — "the process is up / the port answers."
- **Deep** — "the app can reach its database and dependencies and is actually functional."

A trustworthy one-line health check is gold: `systemctl is-active myapp && curl -sf localhost:8080/health >/dev/null && echo OK`.

### Backups and disaster recovery

The rules that matter:

- **3-2-1**: three copies, two media, one off-site.
- **Automate** backups (cron/timer) — `tar`/`rsync` for simple cases, **`restic`/`borg`** for deduplicated, encrypted, incremental backups.
- **Define RPO and RTO**: how much data you can afford to lose (Recovery Point Objective) and how fast you must be back (Recovery Time Objective). Size backup frequency to your RPO.
- **Test restores.** *An untested backup is a hope, not a backup.* Periodically restore into a scratch environment and verify.

```bash
# simple, effective nightly backup of a state dir, off-box
restic -r sftp:backup@host:/backups backup ~/.openclaw
restic -r sftp:backup@host:/backups snapshots     # verify they exist
restic -r ... restore latest --target /tmp/restore-test   # DRILL it
```

### Capacity and resource management

Watch **saturation**: disk filling (`df -h` + alerts), memory pressure (OOM risk), CPU, and file-descriptor limits. The most common slow-motion outage is a disk filling from unrotated logs or unbounded data growth — prevent it with rotation and monitoring, not heroics.

### Change management and post-mortems

- **Deploy safely**: small changes, the ability to **roll back**, and ideally staged rollouts (canary/blue-green) so a bad release doesn't hit everyone.
- **Version your config and infra** in git so you can diff and revert.
- **Blameless post-mortems**: after every incident, write what happened, why, and what will prevent recurrence — focused on systems and process, not blame. Each one should produce a concrete improvement (a new alert, a guardrail, a doc).

> 🦞 **OpenClaw in practice — operate an agent like any production service.** An OpenClaw deployment needs all of this: monitor liveness/cost/disk-growth of `~/.openclaw`, a trustworthy health check, **nightly off-box backups of the whole `~/.openclaw` tree** (the agent's entire mind) with tested restores, capacity watching (memory bloat = higher cost and OOM risk), and append-only audit logs for trust. Cost is a first-class metric here — a misconfigured heartbeat can quietly run up a bill, so cap spend at the provider and alert on anomalies. See [OpenClaw Guide → Part 11: Operations](openclaw/11-deployment-operations.md) and [Part 12: Advanced Patterns](openclaw/12-advanced-patterns.md).

### 🧪 Try it

1. Set up `restic` (or a `tar`+`rsync` script on a timer) to back up a directory off-box nightly. Then **do a restore drill** into a scratch dir.
2. Build a deep health check for a service and wire it to alert (even just an email/Telegram) when it fails.
3. Write a one-page post-mortem template you'd actually use, and fill it in for any small failure you cause on purpose.

**You understand this when…** for any service you run, you can answer "is it healthy, how is it backed up, how fast could I restore it, and how would I notice it degrading?" with specifics.

---

## Security Hardening

🔴 **Advanced.** Security is not a feature you add at the end; it's a posture you maintain throughout. This closing section consolidates the defensive practices that run through every prior section into a checklist you can apply to any system — especially one running an autonomous agent.

### Defense in depth

No single control is enough; layer them so a failure in one doesn't mean compromise. The layers, each drawn from an earlier section:

- **Least privilege** ([Users & sudo](#users-groups--sudo)) — every user/service/process gets only what it needs. Dedicated unprivileged service users; no casual root.
- **File permissions** ([Permissions](#files-permissions--ownership)) — secrets `chmod 600`, data dirs scoped to their owner, nothing world-writable that shouldn't be.
- **Network minimization** ([Networking](#networking)) — default-deny firewall; services bound to localhost unless they must be public; only required ports open.
- **Strong remote access** ([SSH](#ssh--remote-access)) — key-only SSH, no password auth, no root login, ideally a non-default port and `fail2ban` to throttle brute force.
- **Isolation** ([Containers](#containers--sandboxing)) — run untrusted or risky workloads in containers/VMs with read-only FS, dropped capabilities, restricted egress.
- **Patching** ([Package Management](#package-management--runtimes)) — apply security updates promptly; an unpatched CVE is an open door.
- **Secrets hygiene** ([Environment](#environment--configuration)) — secrets in env/secret-manager, never in git or logs; rotate on suspicion of compromise; scope keys minimally.
- **Auditing & monitoring** ([Logs](#logs--debugging), [Production Ops](#production-operations--infrastructure)) — append-only logs shipped off-box, alert on anomalies, review `auth.log`.

### SSH hardening specifics

In `/etc/ssh/sshd_config` (then `sudo systemctl restart sshd`):

```
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
```

Add `fail2ban` to ban IPs after repeated failures. These three lines eliminate the most common server-compromise vector — brute-forced SSH.

### The principle of least privilege, restated

If you remember one idea from this whole guide, make it this: **grant the minimum access necessary, and no more — to every user, process, service, key, and network path.** Most catastrophic breaches are a least-privilege failure somewhere: a service running as root, a world-readable secret, an over-scoped key, a port open to the world. Least privilege is the single highest-return security habit.

### Threat modeling

Before deploying anything, ask: *What could go wrong? Who might attack this? What's the worst case, and what limits the blast radius?* You don't need a formal process — just the habit of identifying the top few risks and ensuring each has a control. For an internet-facing or autonomous system, this habit is the difference between "secure by design" and "breached by surprise."

> 🦞 **OpenClaw in practice — an autonomous agent concentrates every risk here.** OpenClaw executes code, acts autonomously, and reads untrusted input — so its security *is* applied Linux hardening: run it as a least-privileged user (ideally containerized/VM-isolated, not your daily driver); keep its control plane localhost-only behind SSH; keep the software patched (CVE-2026-25253 was a real control-plane RCE); store secrets in env, `chmod 600`, out of logs/git; firewall the box; audit and sandbox skills; and gate irreversible actions behind human approval. **Prompt injection** adds one agent-specific twist — untrusted text can become instructions — but the defense is the same Unix instinct: *constrain capability* (least privilege, tool policies, sandboxing) rather than trusting good behavior. Every control in [OpenClaw Guide → Part 10: Security](openclaw/10-security.md) is one of the layers above.

### 🧪 Try it

1. Harden SSH on a test box: key-only, no root login, install `fail2ban`. Confirm password login is refused.
2. Audit a machine for least-privilege violations: anything running as root that needn't, any `chmod 777` files, any service on `0.0.0.0` that should be localhost.
3. Threat-model a service you run in three bullets: top risk, who'd exploit it, what limits the damage. Add a control for the top risk.

**You understand this when…** you can take any service and apply defense-in-depth — least privilege, minimal network exposure, hardened SSH, patched software, isolated risky parts, protected secrets, monitoring — and explain why least privilege is the foundation under all of it.

---

## Where to go from here

You've covered the path from "what is a shell?" to provisioning, securing, and operating production services. The way to make it stick is to **operate something real**:

- **Stand up a service on a VM you own** and run it as a hardened, supervised systemd unit. Break it on purpose and recover it.
- **Work the [OpenClaw Guide](openclaw/README.md) in parallel.** Its 🐧 *Linux deep-dive* callouts point back into the exact sections here, and deploying/securing/operating an OpenClaw agent exercises nearly every topic in this guide — the shell, files, permissions, users, processes, systemd, networking, SSH, logs, cron, containers, and hardening — in one coherent project. That was the whole idea: **learn Linux by running an agent, and learn the agent by knowing Linux.**
- **Keep the man pages close** (`man <command>`) and reach for `--help`. The depth here is enormous; you now have the map and the mental models to explore it confidently.

The single thread through all nineteen sections: **Unix is small tools, composed, over text, with least privilege.** Once that worldview is yours, every new tool and every new system fits a pattern you already understand.

---

[↑ Top](#the-linux--unix-guide-for-developers) · [OpenClaw Guide →](openclaw/README.md)

</div>








