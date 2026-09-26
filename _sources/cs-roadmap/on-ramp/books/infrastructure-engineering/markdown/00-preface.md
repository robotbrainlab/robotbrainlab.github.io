# Preface

*It works on my machine but breaks on the server, and I don't even own a server.*

Almost every developer says this at some point. The code is fine and the tests pass, but when it has to run somewhere else, for other people, everything that was quietly true on your laptop stops being true. This book answers one question:

*How does my code get from my laptop to machines that serve everyone, the same way every time?*

The answer has three parts. You package the program together with everything it needs (containers). You let a machine do the boring, error-prone steps for you on every change (pipelines). And you describe the machines themselves in files, so you can rebuild them whenever you like (infrastructure as code). The cloud is where all of this usually runs, so you will learn what it is and what it charges for.

## Who This Book Is For

You know Python basics: variables, functions, `if`, loops, and how to run a `.py` file. You have never used Docker, never written a pipeline, and never rented a server. That is fine. Every idea starts from zero, and the few operating-system and networking ideas you need (processes, ports, `localhost`) are explained when they first appear.

## How This Book Is Organized

- Part I, *Understand* (Chapters 1–4) builds the mental model: what infrastructure is, what containers are, what the cloud sells, and how a pipeline moves a change to production. There is very little code.
- Part II, *Use* (Chapters 5–8) makes you a confident user of the four tools: Docker, GitHub Actions, the cloud's basic building blocks, and Terraform.
- Part III, *Apply* (Chapters 9–11) is three longer labs. You ship a small app in a container, deploy it on every push (including a failed deploy and a rollback), and rebuild the whole setup from code.
- Part IV, *What Next* (Chapters 12–13) looks at security, speed, failure, and cost, and tells you what to learn next and what to skip.

## How to Use This Book

Read Part I in order, then do every lab. Infrastructure is learned with your hands: the moment a pipeline goes red, or Terraform rebuilds something you deleted, the idea sticks.

Everything runs on your own computer: no cloud account, GitHub account, login, or credit card. Steps that only exist in a real cloud (a web console, cloud permissions, a billing alert) are described in words.

A tested copy of every lab file is in the book's lab files: download *Infrastructure Engineering from Zero Lab Files.zip* from this book's entry on the Towards Intelligence CS & Engineering on-ramp ([robotbrainlab.github.io/cse/on-ramp.html](https://robotbrainlab.github.io/cse/on-ramp.html)) and unzip it. It unpacks to a folder called `labs/`: `labs/tinyapp/` holds the small web app used from Chapter 5 onward, and `labs/chNN/` holds each chapter's own files. Every lab starts in its own fresh folder under `~/infra-labs/`, so none depends on files left by another. Use the copies to check your work, not to skip the typing.

When you meet a term you don't know, look in Appendix C (Glossary).

## What You Need Installed

- Docker Desktop (macOS or Windows) or Docker Engine (Linux). The book was tested with Docker 29. On Windows, use it with WSL 2.
- act 0.2.89 or newer, which runs GitHub Actions workflows locally (`brew install act` on macOS; see the act documentation for other systems).
- Terraform 1.16 or newer.
- Python 3.12 or newer, git, and curl.
- About 5 GB of free disk space. Most of it is Docker images; act's runner image alone is over 2 GB.

Check them with:

```bash
docker version --format '{{.Server.Version}}'
act --version
terraform version
python3 --version
```

## Conventions Used in This Book

- **Bold** marks a new term the first time it is explained. Every such term is also in Appendix C.
- `Constant width` marks commands, file names, code, and anything you would type exactly.
- Shell commands are shown without a prompt, so you can paste them as they are. Output follows in a separate block. A line containing only `…` means output was trimmed.
- Container IDs, commit hashes, timings, and dates in your output will differ from the book's.
- Three kinds of callout appear in the text:

> **Tip:** A suggestion that saves time or trouble.

> **Note:** Something to be aware of.

> **Warning:** A mistake that can cost you data, money, or security. Read these twice.

- Chapters 1–8 end with a Lab, then a Summary, Key Terms, and Review Questions. Chapters 9–11 are labs from start to finish.
