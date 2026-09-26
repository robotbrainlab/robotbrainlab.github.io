# Preface

Every tutorial says "open the terminal", and I don't know what I'm typing. When my code breaks, I can't get the old version back.

If that sounds like you, this book is for you. It answers one question: *how do I use the tools every developer uses every day, and never lose my work?*

The tools are the command line (the shell, on Linux, macOS, or Windows with WSL) and Git. They are not glamorous. But nearly every other skill in software sits on top of them, and once they stop feeling like magic spells, everything else gets easier.

## Who This Book Is For

You know basic Python: variables, functions, loops, lists, and dictionaries, and you have run a `.py` file. You do not need to know anything about Linux, the terminal, or Git. If you have copied commands from tutorials without knowing what they do, this book is written for you. Everything is explained when it's needed, in the order you need it.

## How This Book Is Organized

- *Part I, Understand*, gives you the mental model. What the terminal is, what the shell does with the words you type, how files and permissions work, and why code needs a history. There is very little to type yet.
- *Part II, Use*, makes you a confident everyday user: finding and searching files, keeping programs running, installing software, working on remote machines, and the Git commands you'll use every single day.
- *Part III, Apply*, is three guided labs. You automate a chore with a script, try a risky idea on a Git branch, and work on a shared project with a second person.
- *Part IV, What Next*, looks at security, speed, failure, and cost for these tools, then tells you what to learn next and what to skip for now.
- *The appendices* hold a command cheat sheet, a Git cheat sheet, and a glossary.

## How to Use This Book

Read Part I in order. It is short, and the rest of the book leans on it. After that, keep a terminal open next to the book and type the commands yourself. Typing is slower than pasting, and that is the point: your fingers learn what your eyes skim.

Every chapter in Parts I and II ends with a lab, and the chapters of Part III are labs. Each lab step says what you should see, so you can check your work. Do the labs in a throwaway folder such as `~/sandbox`, never inside a project you care about. The sample files the labs use are in the book's lab files: download *Linux and Git from Zero Lab Files.zip* from this book's entry on the Towards Intelligence CS & Engineering on-ramp ([robotbrainlab.github.io/cse/on-ramp.html](https://robotbrainlab.github.io/cse/on-ramp.html)) and unzip it. It unpacks to a folder called `labs/`.

When you meet a word you don't know, look it up in Appendix C (Glossary). Every bold term in the book is defined there in a line.

## What You Need Installed

- *A terminal.* Linux and macOS have one built in. On Windows, install WSL (Windows Subsystem for Linux) with `wsl --install` in PowerShell, then use the Ubuntu terminal it gives you. Chapter 1 explains what WSL is.
- *Git 2.28 or newer* (check with `git --version`). On macOS, running `git` the first time offers to install it. On Ubuntu or WSL, run `sudo apt install git`.
- *Python 3.10 or newer* (check with `python3 --version`).
- *jq* and *shellcheck*, two small tools used in Chapters 5 and 9. Install them with `sudo apt install jq shellcheck` on Ubuntu or WSL, or `brew install jq shellcheck` on macOS.
- *A text editor.* VS Code is the usual choice, but any editor that saves plain text will do.

You do not need a GitHub account or a server. The labs use a shared folder on your own computer to stand in for GitHub.

The examples were tested with Git 2.52, bash 5.2 on Debian 13, zsh on macOS 26, Python 3.14, jq 1.8, and ShellCheck 0.11.

## Conventions Used in This Book

- Bold type marks a new term the first time it is explained. Every bold term is also in Appendix C.
- `Constant width` marks commands, file names, and anything else you would type exactly.
- Code blocks show commands, output, or Python. Commands are shown without a prompt, so you can paste them as they are. When a block mixes commands and their results, the result follows in its own block.
- Output was copied from real runs. Your user name, dates, sizes, and Git commit IDs will differ. The example user is `ada`, with a home folder of `/home/ada`. On macOS your home folder is `/Users/<you>` instead.
- A line containing only `…` means some output was left out.
- Where Linux and macOS behave differently, the text shows both.
- Three kinds of callout appear in the text:

> **Tip:** A suggestion that saves you time or trouble.

> **Note:** Something to be aware of, or a detail that explains what you're seeing.

> **Warning:** A mistake that can cost you data, money, or security. Read these twice.
