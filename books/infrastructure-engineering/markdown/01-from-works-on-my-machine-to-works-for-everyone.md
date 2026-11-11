# From "Works on My Machine" to "Works for Everyone"

This chapter explains why code that runs fine on your laptop can fail somewhere else, and names the ideas the rest of the book is built on: infrastructure, environments, DevOps, and the cloud. By the end you will have watched the same file work on one machine and crash on another.

*The problem.* It runs perfectly on my laptop and crashes on the server.

*The question.* What is different about the server, and how do teams make every machine behave the same way?

## Why "Works on My Machine" Happens

Think of a recipe. It works perfectly in your kitchen. You send it to a friend, and their cake sinks. Nothing was wrong with the recipe. Their oven runs hotter, they had a different flour, and they skipped an ingredient you never wrote down because you always have it in the cupboard.

Code is a recipe, and the machine it runs on is the kitchen. When you run a Python program, it silently depends on many things that are not in your `.py` file:

| Hidden ingredient | Example of what differs |
|---|---|
| The Python version | 3.12 on your laptop, 3.9 on the server |
| Installed libraries | FastAPI 0.141 locally, an older one there, or none |
| The operating system | macOS or Windows locally, Linux on almost every server |
| Settings | A password or a URL you set once on your laptop and forgot |
| Files and data | A folder or a database that only exists on your machine |
| The network | Your laptop can reach a service that the server cannot |

Every one of these is a way for "it works on my machine" to become "it crashes on the server". The fix is never "be more careful". People forget. The fix is to make the hidden ingredients visible, write them down, and let machines set them up the same way every time. That is what this book teaches.

## What Infrastructure Is

A city runs on things nobody looks at: roads, water pipes, power lines. Without them, nothing works.

**Infrastructure** is the same thing for software: everything your code needs in order to run for other people, apart from the code itself. That includes the machines, their operating systems, the network between them, where data is stored, and the steps that put your code onto those machines.

A server is simply a computer whose job is to run programs for others, usually without a screen or keyboard, in a building full of other servers called a data centre. There is nothing magic about it. Your laptop could be a server if it were always on and reachable.

Infrastructure engineering is the work of making all of this reliable and repeatable: the same result every time, on any machine, without a person clicking through steps from memory.

## Environments

An **environment** is one complete place where your app runs, with its own machines, settings, and data. Most teams have several:

| Environment | Who uses it | What it's for |
|---|---|---|
| Development | You | Writing code, usually on your laptop |
| Test | Automated tests | Checking each change |
| Staging | The team | A dress rehearsal that looks like production |
| **Production** | Real users | The real thing |

A theatre company rehearses on the real stage, in costume, before opening night. **Staging** is that dress rehearsal: it should look as much like production as possible, so that surprises happen there instead of in front of the audience.

The values that change from one environment to the next (a database address, a password, a feature switch) are called **configuration**. Configuration belongs outside your code, so the same code can run unchanged in every environment. You will pass configuration into containers in Chapter 5.

> **Tip:** The more your environments differ, the more bugs hide in the differences. A good rule is "same code, same packaging, different configuration".

## The DevOps Idea

In many older companies, developers "threw code over the wall" to an operations team, who installed it on servers. Each side blamed the other when things broke, and painful releases happened a few times a year.

**DevOps** is the idea that building software and running it are one job, shared by one team, with as much of the work automated as possible. Its heart is the feedback loop: the time between making a change and learning whether it worked.

```text
        make a small change
               │
               ▼
     test it automatically ◄──────┐
               │                  │
               ▼                  │
      release it the same         │
          way every time          │
               │                  │
               ▼                  │
      watch how it behaves ───────┘
```

Short loops are safe loops. If you change ten lines and something breaks ten minutes later, you know where to look. If you change ten thousand lines and release them once a quarter, you don't.

This book gives you three tools that make the loop fast and safe:

1. *Package* the app with everything it needs, so it runs the same everywhere (containers, Chapters 2 and 5).
2. *Automate* the steps from a commit to a running app (pipelines, Chapters 4 and 6).
3. *Describe* the machines themselves in files, so you can rebuild them at will (infrastructure as code, Chapter 8).

## The Cloud Idea

You don't need to own a server any more than you need to own a power station. The **cloud** means renting computers, storage, and ready-made services from a provider over the internet, and paying only for what you use, often by the second. Amazon Web Services (AWS), Microsoft Azure, and Google Cloud are the big three. Chapter 3 explains what they sell.

For now, one idea matters: in the cloud, machines are created by software in seconds, and they can disappear just as fast. So you can't rely on careful manual setup. You need everything to be repeatable.

## Lab: Two Machines, Two Answers

You'll run one Python file on two "servers" and watch it work on one and crash on the other. The servers are containers, which Chapter 2 explains. For now, treat `docker run python:3.9-slim` as "borrow a clean Linux machine that has Python 3.9".

1. Make a folder for the book's labs and a file called `hello.py`:

   ```bash
   mkdir -p ~/infra-labs/ch01 && cd ~/infra-labs/ch01
   ```

   ```python
   import platform


   def describe(count):
       match count:
           case 0:
               return "no visitors yet"
           case 1:
               return "one visitor"
           case _:
               return f"{count} visitors"


   print(describe(3), "on Python", platform.python_version(), platform.system())
   ```

2. Run it on your own machine:

   ```bash
   python3 hello.py
   ```

   ```text
   3 visitors on Python 3.14.4 Darwin
   ```

   Your version may differ; `Darwin` means macOS.

3. Run the same file on a machine with Python 3.9. The `-v` part lends your folder to that machine (Chapter 5 explains it). The first run downloads Python 3.9, which takes a minute.

   ```bash
   docker run --rm -v "$PWD":/work -w /work python:3.9-slim python hello.py
   ```

   ```text
     File "/work/hello.py", line 5
       match count:
             ^
   SyntaxError: invalid syntax
   ```

4. Run it once more with Python 3.12:

   ```bash
   docker run --rm -v "$PWD":/work -w /work python:3.12-slim python hello.py
   ```

   ```text
   3 visitors on Python 3.12.14 Linux
   ```

**Expected results:** the same file works on your laptop and on Python 3.12, and fails with a `SyntaxError` on Python 3.9, because `match` only exists from Python 3.10. Notice also that the containers report `Linux`, not your laptop's operating system. The code never changed. Only the kitchen did.

## Summary, Key Terms, and Review Questions

### Summary

- Code silently depends on things outside the file: the Python version, libraries, the operating system, settings, data, and the network.
- Infrastructure is everything your code needs to run for others. Infrastructure engineering makes it reliable and repeatable.
- Apps run in several environments. Staging should look like production; configuration is what differs between them.
- DevOps joins building and running software, and aims for short, safe, automated feedback loops.
- The cloud rents machines and services by use. Machines come and go, so setup must be repeatable.

### Key Terms

| Term | Meaning |
|---|---|
| Infrastructure | Everything code needs to run for others, apart from the code |
| Environment | One complete place where an app runs, with its own settings and data |
| Production | The environment real users use |
| Staging | A production-like rehearsal environment |
| Configuration | Settings that differ between environments, kept outside the code |
| DevOps | Building and running software as one automated job |
| Cloud | Computers and services rented over the internet, paid for by use |

### Review Questions

1. List four hidden ingredients a Python program depends on that are not in its `.py` file.
2. What is the difference between staging and production, and why should they be alike?
3. Why should configuration live outside the code?
4. What is a feedback loop, and why is a short one safer?
5. In the lab, why did the same file fail on one machine and work on another?

> **You understand this when** you can look at a "works on my machine" bug and name which hidden ingredient differed between the two machines.
