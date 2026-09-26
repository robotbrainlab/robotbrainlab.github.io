# Linux and Git from Zero

**The problem you hit:** Every tutorial says "open the terminal", and I don't know what I'm typing. When my code breaks, I can't get the old version back.
**The question it answers:** How do I use the tools every developer uses every day, and never lose my work?
**Target:** 85–95 pages

The labs need no accounts. A local "bare" repository stands in for GitHub, and GitHub's own screens (forks, pull requests) are described in words.

## Front matter

Title page · Copyright · Contents · Preface (Who This Book Is For, How This Book Is Organized, How to Use This Book, What You Need Installed, Conventions Used in This Book)

## Part I · Understand

*What to ignore for now:* how the kernel manages memory, the history of Unix, and Git's internal file formats.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 1 | The Machine Behind the Terminal | Every tutorial starts with "open a terminal", but I don't know what that window actually is. | What Linux is, the kernel and everything around it, distributions, macOS and WSL, the Unix idea: small tools, and everything is a file | 6 |
| 2 | The Shell: Talking to Your Computer in Words | I type a command and something happens, but I couldn't tell you what. | What a shell is, the parts of a command, where you are and paths, how commands are found (`PATH`), pipes and redirection, getting help | 7 |
| 3 | Files, Folders, and Who May Touch Them | It says "Permission denied", and I don't know whose permission I need. | One tree from `/` and where things live, hidden files, users and groups, permissions, `sudo`, least privilege | 7 |
| 4 | Why Code Needs a History | My code worked yesterday. I changed something, and now I can't get yesterday back. | Version control as a series of snapshots, commits, branches as bookmarks, merging, remotes as copies of a project, what Git is, and why GitHub is not Git | 7 |

## Part II · Use

*What to ignore for now:* every flag of every command, advanced `awk`, and Git plumbing commands.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 5 | The Everyday Command Line | I can move around, but finding a file or reading a log still feels like guessing. | Finding files, viewing files, `grep`, `sed`, `sort`, `uniq`, `jq`, building pipelines, environment variables | 7 |
| 6 | Programs That Keep Running | My program stops the moment I close the terminal. | Processes, signals, foreground and background jobs, services, logs, scheduled jobs | 6 |
| 7 | Installing Software and Working Remotely | I need a tool on a machine I can only reach over the internet. | Package managers, version managers and virtual environments, SSH and keys, copying files, `tmux` | 5 |
| 8 | Git Every Day | I want to save my work properly, not as `final_v2_really_final.py`. | Starting a repository, the working tree, staging, and commits, `status`, `diff`, `log`, `.gitignore`, good commit messages, branches and merging, `push` and `pull`, undoing mistakes (`restore`, `reset`, `revert`, `reflog`) | 10 |

## Part III · Apply

*What to ignore for now:* Git hooks, submodules, and complex branching strategies.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 9 | Lab: Automate a Daily Chore | I type the same five commands every morning. | Turning commands into a script: the shebang, `set -euo pipefail`, variables and quoting, conditions and loops, exit codes, checking with `shellcheck`, scheduling it | 8 |
| 10 | Lab: Try an Idea Without Breaking Anything | I want to try an idea without risking the version that works. | A branch for the idea, a merge conflict and how to resolve it, rebasing in brief, recovering a "lost" commit with `reflog` | 6 |
| 11 | Lab: Work on a Project with Someone Else | Two of us edited the same file, and someone's work vanished. | A shared remote, `fetch` and `pull`, a feature branch, a pull request and a code review, forks, open-source workflow and licences | 8 |

## Part IV · What Next

| Ch | Chapter | Covers | Pages |
|---|---|---|---|
| 12 | Security, Speed, Failure, and Cost | Secrets in the terminal and in Git, permissions, large repositories, recovering lost work, what these tools cost | 5 |
| 13 | Where to Go from Here | What to learn next, what to skip for now | 3 |

## Appendices

A. Command Cheat Sheet · B. Git Cheat Sheet · C. Glossary · Index (5 pages)

**Total:** about 90 pages
