# The Machine Behind the Terminal

Before you type a single command, you need a picture of what you're talking to. This chapter gives you that picture: what the terminal window is, what sits behind it, what Linux really is, and the two simple ideas that explain why the command line works the way it does.

*The problem.* Every tutorial starts with "open a terminal", but I don't know what that window actually is.

*The question.* What is that window, and what is on the other side of it?

## The Terminal Is a Window, Not the Computer

The **terminal** is just a window that shows text and sends your keystrokes somewhere. On its own it does nothing. It's like a phone: useful only because someone answers at the other end.

The one who answers is the **shell**: a program that reads the line you type, runs the right program, shows you the result, and waits for the next line. Chapter 2 is all about the shell. The programs it runs, in turn, ask the operating system for everything they need.

## What an Operating System Does

An **operating system** is the software that shares one computer among many programs. Your laptop may be running a browser, an editor, and fifty background helpers at once. Something has to decide who runs next, whose memory is whose, and who may open which file.

The heart of the operating system is the **kernel**. Think of a block of flats. The tenants are your programs. The kernel is the building manager. Tenants can't walk into the boiler room or another tenant's flat. When they need something, they ask the manager, and the manager decides whether to allow it.

That "asking" has a name. A **system call** is a request from a program to the kernel: "open this file", "start this program", "send these bytes". Programs never touch the disk or the network directly. They make system calls, and the kernel does the work, after checking that they're allowed.

Everything outside the kernel is called userspace. Your shell, `ls`, Python, your editor, and your own scripts all live there.

```text
  ┌──────────────────────────────────────────────┐
  │ USERSPACE: shell, ls, python, your programs  │
  ├──────────────────────────────────────────────┤
  │ system calls: the only door into the kernel  │
  ├──────────────────────────────────────────────┤
  │ KERNEL: files, processes, memory, devices    │
  ├──────────────────────────────────────────────┤
  │ HARDWARE: disk, memory, CPU, network card    │
  └──────────────────────────────────────────────┘
```

You only need to know the door is there. When a command says "Permission denied", it is the kernel saying no at that door.

## Linux: A Kernel Plus Everything Around It

Strictly speaking, **Linux** is just a kernel. On its own it gives you no shell, no `ls`, and no way to install software. To get a working system, people bundle the kernel with a shell, hundreds of small tools, a way to install more software, and sometimes a desktop.

That bundle is a **distribution**, or "distro". The distributions you're most likely to meet:

| Distribution | Where you'll see it |
|---|---|
| Ubuntu | Laptops, cloud servers, and WSL on Windows |
| Debian | Servers; Ubuntu is built on it |
| Fedora, Red Hat Enterprise Linux | Company servers |

They share the same kernel and core ideas; mostly, they differ in how you install software (Chapter 7). What you learn on one works on all of them. And Linux runs most of the world's servers, so the machine your code ends up on is probably Linux.

## macOS and Windows: Cousins and Guests

**Unix** is the older operating system that Linux was modelled on. Linux copied its ideas and commands, but not its code. macOS is a direct descendant: underneath the Mac's desktop is a real Unix system. So the terminal on a Mac speaks almost the same language as Linux. The commands are the same; a few options differ.

The differences come from two families of tools: Linux ships the GNU versions of `ls`, `sed`, `grep`, and friends, and macOS ships the BSD versions. When it matters, this book shows both.

Windows is not Unix, and its own command line, PowerShell, uses different commands. But Windows can run a real Linux inside it with **WSL**, the Windows Subsystem for Linux. For this book, a WSL terminal is a Linux terminal.

## The Unix Idea: Small Tools

Unix was built on a few simple ideas that still explain almost everything you'll see. The first is: do one thing well. `ls` lists files. `sort` sorts lines. `wc` counts lines and words. None tries to do everything.

The power comes from connecting them. The output of one tool can flow straight into the next, like water through pipes. There is no "count files" command; you join the tool that lists to the tool that counts. Chapter 2 shows you how.

A second idea surprises beginners: silence means success. A command that works often prints nothing at all. If you see output, read it; it may be an error.

## Everything Is a File

The other big Unix idea is that almost everything is shown to you as a file. Your documents are files, of course. But so are folders (a folder is a file that lists other files). So are devices: on Linux, your disk appears as a file under `/dev`, and so does the terminal itself.

Here is a strange but useful one. `/dev/null` is a file that throws away whatever you write into it and is always empty when you read it:

```bash
echo "into the void" > /dev/null
cat /dev/null
```

Both commands print nothing. The first wrote a line into `/dev/null`, which discarded it. The second read `/dev/null` and found it empty. It's the command line's rubbish bin, and you'll use it to hide output you don't care about.

On Linux, the kernel even shows its own live state as files under `/proc`. You can read how much memory the machine has with the same tool you'd use to read a text file:

```bash
head -1 /proc/meminfo
```

```text
MemTotal:        8024788 kB
```

So a handful of tools that read files can inspect almost anything on the system. Learn to handle files, and you can handle the whole machine.

## Lab: First Look Around

Open your terminal (on Windows, the Ubuntu app from WSL). Type each command and press Enter.

1. Ask who you are: `whoami`. **Expected:** your user name, such as `ada`.
2. Ask which kernel is running: `uname -s`. **Expected:** `Linux` on Linux and WSL, `Darwin` on macOS (Darwin is the name of macOS's Unix core).
3. Find out which distribution you have with `head -2 /etc/os-release`, or on macOS, `sw_vers`. **Expected:** your system's name and version, such as:

   ```text
   PRETTY_NAME="Debian GNU/Linux 13 (trixie)"
   NAME="Debian GNU/Linux"
   ```

4. Find out which shell answers you: `echo $SHELL`. **Expected:** `/bin/bash` on most Linux systems, `/bin/zsh` on macOS.
5. Look at `/dev/null` itself: `ls -l /dev/null`.

   ```text
   crw-rw-rw- 1 root root 1, 3 Sep 26 14:25 /dev/null
   ```

   **Expected:** a line starting with `c`. That letter means "character device": a file that is really a device. You'll learn to read the rest of this line in Chapter 3.

## Summary, Key Terms, and Review Questions

### Summary

- The terminal is only a window. The shell behind it reads your commands and runs programs.
- The kernel is the core of the operating system. Programs ask it for everything through system calls, and it can say no.
- Linux is a kernel. A distribution bundles it with a shell, tools, and a way to install software.
- macOS is a Unix system with slightly different (BSD) tools; WSL runs real Linux inside Windows.
- Unix tools are small and are combined to do big jobs. Silence usually means success.
- Almost everything, including devices, is presented as a file.

### Key Terms

| Term | Meaning |
|---|---|
| Terminal | The window that shows text and passes your typing to the shell |
| Shell | The program that reads your commands and runs them |
| Operating system | Software that shares one computer among many programs |
| Kernel | The core of the operating system; controls hardware and access |
| System call | A program's request to the kernel |
| Linux | A Unix-like kernel, and by extension the systems built on it |
| Distribution | The Linux kernel bundled with tools and a package manager |
| Unix | The older operating system whose design Linux and macOS follow |
| WSL | Windows Subsystem for Linux: real Linux running inside Windows |

### Review Questions

1. What is the difference between the terminal and the shell?
2. What does the kernel do, and why can't a program read the disk directly?
3. Why is "Linux" not, strictly, a complete operating system? What turns it into one?
4. Why do most commands you learn on Linux also work on macOS?
5. What does "silence means success" mean, and why does it matter when you read output?

> **You understand this when** you can explain, in your own words, what happens between typing in the terminal window and the kernel doing the work.
