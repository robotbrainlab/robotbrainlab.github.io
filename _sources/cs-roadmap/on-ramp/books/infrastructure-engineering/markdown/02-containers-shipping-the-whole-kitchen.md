# Containers: Shipping the Whole Kitchen

Containers are the most important idea in this book. This chapter explains what they are, how they relate to images, why images have layers, how containers compare with virtual machines, and where images are stored. Then you run your first containers.

*The problem.* The server has a different Python, different libraries, and a different operating system.

*The question.* Can I send my program together with everything it needs, so the server's differences stop mattering?

## Ship the Kitchen, Not the Recipe

In Chapter 1, your recipe failed in a friend's kitchen. You could send a longer recipe with every detail. Or you could do something bolder: send the whole kitchen. A food truck arrives with its own oven, its own flour, and its own spices. It parks anywhere there is a road and electricity, and it cooks the same dish every time.

A **container** is a food truck for software. It is your program running together with its own private copy of everything it needs: the right Python, the right libraries, and the Linux files they expect. The server only has to provide the road and the electricity, which means a machine that can run containers.

## Just Enough Operating System

To see what a container really is, you need three words.

The operating system (OS) is the software that manages a computer for all the programs on it: Linux, macOS, Windows. At its centre is the kernel, the part that talks to the hardware. The kernel decides which program uses the processor, hands out memory, reads and writes files, and sends network traffic.

A process is one running program. Every process gets a number from the kernel, its process ID (PID). When you run `python3 hello.py`, the kernel starts a process, gives it a PID, and cleans up when it ends.

A container is not a small computer. It is an ordinary process that the Linux kernel fences off. Inside the fence, the process sees its own files, its own list of processes (in which it is often PID 1, the first and only one), and its own network. Outside the fence, it is just one more process on the machine.

> **Note:** The fencing is a Linux kernel feature, so containers are Linux programs. On macOS and Windows, Docker Desktop quietly runs a small Linux virtual machine and runs your containers inside it. That is why the containers in Chapter 1 reported `Linux`.

## Images and Containers

A container starts from an **image**: a read-only package holding all the files the program needs, plus a note saying which command to run at start-up.

If you know Python classes, this picture helps: an image is like a class, and a container is like an object made from it. You write the class once. You can create many objects from it, each with its own state, and deleting an object doesn't touch the class.

| | Image | Container |
|---|---|---|
| What it is | A package of files and a start command | A running (or stopped) process made from an image |
| Changes? | Never; you build a new one instead | Yes, it can write files while it runs |
| How many | One per version of your app | As many as you start |
| Lifetime | Kept until you delete it | Often seconds to days, then replaced |

Containers are disposable. Anything a container writes into its own files disappears when the container is removed. That sounds alarming, but it's a feature: every container starts from the same clean image, so there is no slow build-up of manual changes. Data that must survive goes somewhere else, which Chapter 5 covers.

Docker is the most popular tool for building images and running containers. The `docker` command you type is a client. It sends your requests to the Docker daemon, a background service that does the real work of pulling images and starting containers.

## Layers

An image is built in steps: start from a small Linux, add Python, install your libraries, copy in your code. Each step saves its changes to the files as a **layer**. The image is the stack of layers, like transparent sheets laid on top of each other: look down through them and you see one complete set of files.

```text
 ┌────────────────────────────────────┐
 │ writable layer (this container)    │  ◄ gone when removed
 ├────────────────────────────────────┤
 │ your code: main.py          12 kB  │  ┐
 ├────────────────────────────────────┤  │
 │ pip install: libraries     54 MB   │  │ read-only
 ├────────────────────────────────────┤  │ image layers,
 │ Python 3.12                 45 MB  │  │ shared
 ├────────────────────────────────────┤  │
 │ Debian Linux files         110 MB  │  ┘
 └────────────────────────────────────┘
```

Layers matter for two practical reasons:

1. *Sharing.* Ten images built on the same Python base share its layers. Your disk stores them once, and a download skips layers you already have.
2. *Speed.* When you rebuild an image, Docker reuses every layer whose inputs didn't change. Change one line of code, and only the top layer is rebuilt. Chapter 5 shows how to order the steps so this works in your favour.

A running container adds one thin writable layer on top. That is where its own changes go, and why they vanish with it.

## Containers Compared with Virtual Machines

Before containers, the usual way to isolate programs was a **virtual machine** (VM): software that pretends to be a whole computer, with its own virtual processor, memory, and disk, running its own complete operating system, kernel included. A program called a hypervisor runs many VMs on one physical machine.

Picture houses and flats. Each VM is a separate house with its own foundations, plumbing, and wiring. Containers are flats in one building: each has its own locked door and furniture, but they share the foundations and the plumbing, which is the host's kernel.

| | Virtual machine | Container |
|---|---|---|
| Contains | A whole OS, including a kernel | An app and its files; uses the host's kernel |
| Typical size | Gigabytes | Tens to hundreds of megabytes |
| Start time | Tens of seconds to minutes | Usually under a second |
| Isolation | Very strong | Good, but all share one kernel |
| Can run | Any OS | Linux programs on a Linux kernel |

They are not rivals: in the cloud, your containers usually run inside VMs, which keep customers apart.

## Registries

You build an image on your laptop. How does the server get it? Through a **registry**: a server that stores images and hands them out, like a library that lends out books. You push an image to a registry to upload it, and pull it to download it. Docker Hub is the default public registry; cloud providers each run their own, and in Chapter 6 you will run one on your own machine.

An image's full name tells Docker where to find it:

```text
   localhost:5001/tinyapp:1.0.0
   └─────┬──────┘ └──┬──┘ └─┬─┘
      registry   repository  tag
```

A **tag** is a human-friendly label for one version, such as `1.0.0` or `3.12-slim`. When the registry part is missing, Docker assumes Docker Hub, so `python:3.12-slim` really means `docker.io/library/python:3.12-slim`.

Tags can be moved to point at a different image later. For an exact, unchangeable reference, every image also has a **digest**: a long fingerprint like `sha256:f77ac9e4…` calculated from its contents. The same digest always means exactly the same bytes.

> **Warning:** A tag like `latest` can point at a different image tomorrow. For anything that must be repeatable, use a specific version tag, and for the strictest cases, the digest.

## Lab: Your First Containers

You'll run containers, look inside them, see their layers, and prove that they are disposable.

1. Download (pull) an image. If you did the Chapter 1 lab, it is already there:

   ```bash
   docker pull python:3.12-slim
   ```

   ```text
   3.12-slim: Pulling from library/python
   Digest: sha256:f77ac9e44ae96ef2c90b8053ea08c31f8be030f824196b0ae4db6d462c84e51f
   Status: Image is up to date for python:3.12-slim
   docker.io/library/python:3.12-slim
   ```

2. Run a one-off container. `--rm` removes it when it finishes:

   ```bash
   docker run --rm python:3.12-slim python -c "print('hello from inside a container')"
   ```

   ```text
   hello from inside a container
   ```

3. Look at the operating system inside it:

   ```bash
   docker run --rm python:3.12-slim cat /etc/os-release | head -3
   ```

   ```text
   PRETTY_NAME="Debian GNU/Linux 13 (trixie)"
   NAME="Debian GNU/Linux"
   VERSION_ID="13"
   ```

   Your laptop runs something else, but the container carries its own Debian files.

4. Ask the process for its PID:

   ```bash
   docker run --rm python:3.12-slim python -c "import os; print('my process id is', os.getpid())"
   ```

   ```text
   my process id is 1
   ```

   Inside its fence, your program is the first and only process.

5. Look at the image's layers, newest first:

   ```bash
   docker history --format 'table {{.CreatedBy}}\t{{.Size}}' python:3.12-slim
   ```

   ```text
   CREATED BY                                      SIZE
   CMD ["python3"]                                 0B
   RUN /bin/sh -c set -eux;  for src in idle3 p…   16.4kB
   RUN /bin/sh -c set -eux;   savedAptMark="$(a…   44.6MB
   ENV PYTHON_SHA256=5c8462af5790baf43a321a1559…   0B
   ENV PYTHON_VERSION=3.12.14                      0B
   …
   # debian.sh --arch 'arm64' out/ 'trixie' '@1…   110MB
   ```

   The `--format` option picks just two columns so the table fits. The bottom row is the Debian base. The 44.6 MB step installed Python. Rows of `0B` only record settings.

6. Prove that containers are disposable. Give a container a name, and have it write a file:

   ```bash
   docker run --name scratchpad python:3.12-slim sh -c "echo 'I was here' > /note.txt && cat /note.txt"
   ```

   ```text
   I was here
   ```

   Now look for the file from a new container made from the same image:

   ```bash
   docker run --rm python:3.12-slim cat /note.txt
   ```

   ```text
   cat: /note.txt: No such file or directory
   ```

7. The first container stopped but still exists. List all containers, including stopped ones, then remove it:

   ```bash
   docker ps -a --filter name=scratchpad --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'
   docker rm scratchpad
   ```

   ```text
   NAMES        IMAGE              STATUS
   scratchpad   python:3.12-slim   Exited (0) Less than a second ago
   scratchpad
   ```

**Expected results:** every container reports Debian Linux and PID 1, `docker history` shows the base layer at the bottom, and no other container can see `scratchpad`'s file, because it lived only in that container's writable layer.

## Summary, Key Terms, and Review Questions

### Summary

- A container is a normal Linux process fenced off by the kernel, with its own files, process list, and network.
- An image is a read-only package of files plus a start command. A container is a running instance of it, like an object made from a class.
- Images are stacks of layers. Layers are shared between images and reused when rebuilding.
- Virtual machines carry a whole OS; containers share the host's kernel, so they are smaller and start faster. In the cloud, containers usually run inside VMs.
- Registries store images. You push and pull them by name and tag; a digest names one exact image.

### Key Terms

| Term | Meaning |
|---|---|
| Container | A program running with its own private files, isolated by the kernel |
| Image | A read-only package of files and a start command, used to create containers |
| Layer | One step's worth of file changes in an image |
| Virtual machine (VM) | Software that imitates a whole computer, with its own OS |
| Registry | A server that stores and serves images |
| Tag | A movable, human-friendly version label on an image |
| Digest | A fingerprint that names one exact image |

### Review Questions

1. In your own words, why does a container stop "works on my machine" problems?
2. Using the class and object picture, how do an image and a container differ?
3. Why do images use layers? Give two benefits.
4. Name two differences between a virtual machine and a container.
5. What does `docker.io/library/python:3.12-slim` tell Docker, part by part?

> **You understand this when** you can explain why a file written in a container vanishes with it.
