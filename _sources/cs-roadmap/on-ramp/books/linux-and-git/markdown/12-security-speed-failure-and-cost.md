# Security, Speed, Failure, and Cost

This chapter looks back at the terminal and Git through four questions that every tool raises sooner or later: what can go wrong, what makes it slow, how it breaks, and what it costs. Each section is short and practical: the few habits that protect your work, your time, and your money.

*The problem.* The tools work for me now, but I don't know what could go badly wrong, or what it would cost me.

*The question.* What are the real risks of the terminal and Git, and which habits keep me safe?

## Security: What Can Go Wrong, and What Limits the Damage

*Secrets in your shell history.* Your shell saves the commands you type, in `~/.bash_history` or `~/.zsh_history`. Type `export API_KEY=...` at the prompt and the key sits in that file for years. In bash, setting `HISTCONTROL=ignorespace` makes the shell skip any command that starts with a space:

```bash
export HISTCONTROL=ignorespace
 export API_KEY=sk-live-4f9a2c
export COLOUR=blue
history 3
```

```text
    1  export HISTCONTROL=ignorespace
    2  export COLOUR=blue
    3  history 3
```

The line with the key never reached the history. (In zsh, the setting is `setopt HIST_IGNORE_SPACE`.) Better still, keep secrets in a `.env` file with `chmod 600` and never type them at all.

*Secrets in Git.* This is the big one. Once a secret is committed, deleting the file doesn't delete it from history. Here a project committed `.env`, then removed it and added it to `.gitignore`:

```bash
ls -a
git show HEAD~1:.env
```

```text
.  ..  .git  .gitignore  app.py
API_KEY=sk-live-4f9a2c
```

The file is gone from the folder, but one command pulls it straight out of the previous commit. Anyone who clones the repository can do the same, and bots scan public repositories for keys within minutes of a push.

> **Warning:** If you ever commit a secret, treat it as stolen. Revoke or rotate it at the provider first (create a new key, disable the old one), then clean up the repository. Rewriting history with a tool such as `git filter-repo` doesn't help if someone has already copied the key.

The prevention is cheap: create `.gitignore` before your first commit, and always read `git status` and `git diff --staged` before you commit.

*Permissions and privilege.* The habits from Chapter 3 limit the damage when something does go wrong. Keep private files at `600`, including SSH keys. Protect your private key with a passphrase. Don't work as root, and use `sudo` for single commands only. Read scripts before running them, especially anything piped from `curl` into a shell.

## Speed: What Makes This Slow

*Searching too much.* Most slow commands are searching far more than you need. `grep -r` or `find` started at `/` or your home folder crawls through every file, including huge folders like `.venv`, `node_modules`, and `.git`. Start as close to the target as you can, and skip the heavy folders: `grep -r --exclude-dir=.venv TODO .`.

*Large repositories.* Git keeps every version of every file forever. That's wonderful for code and costly for big binary files, such as videos, datasets, and build outputs. Watch what happens when a 20 MB file is committed and then deleted:

```bash
du -sh .git
```

```text
 19M	.git
```

The file is gone from the project, but it's still in history, so every clone downloads it, for good. Before the video, `.git` was 128 KB. Three habits keep repositories fast:

- Put build outputs, virtual environments, and data files in `.gitignore`.
- Store large assets somewhere else, or use Git LFS (Large File Storage), a Git add-on that keeps big files outside the history.
- When you only need the latest version of someone's huge project, clone just that: `git clone --depth 1 <url>`.

*Waiting on the network.* `git status`, `diff`, `log`, `commit`, and `branch` are fast because they never leave your machine. Only `clone`, `fetch`, `pull`, and `push` talk to the remote. If Git feels slow, check which kind of command you're running.

## Failure: How It Breaks, and How to Diagnose It

Most failures in this book announce themselves with a clear message. Read the message first, then run the one command that checks it:

| You see | Likely cause | Check with |
|---|---|---|
| `command not found` | Typo, not installed, or not on PATH | `which name`, `echo $PATH` |
| `Permission denied` | Not yours, not executable, or a closed folder | `ls -l` on the file and its folders |
| `No space left on device` | Disk full, often from logs or backups | `df -h`, then `du -sh *` in suspect folders |
| A background program vanished | It crashed or was killed | Its log, or `journalctl -u name` |
| A script "succeeded" but did damage | Errors were ignored | Add `set -euo pipefail` |
| `! [rejected] … (fetch first)` | Someone pushed before you | `git pull`, then push |
| `CONFLICT` | Both sides changed the same lines | `git status`, then resolve |
| `HEAD detached at …` | You checked out a commit, not a branch | `git switch main` |
| A commit seems lost | Branch deleted or reset | `git reflog` |

Two failures can't be fixed afterwards, so prevent them. First, uncommitted work that you discard with `git restore` or `git reset --hard` is gone, because Git never saw it; commit small and often. Second, a laptop is a single point of failure; push to a remote regularly, because a repository that exists in one place isn't backed up.

> **Tip:** When you're stuck, run `git status`. It almost always says what state you're in and prints the exact command to get out of it.

## Cost: What This Costs You

The tools themselves are free. Linux, bash, zsh, the command-line tools, and Git are all open source, and they run on the laptop you already have. The real costs are elsewhere:

- *Time.* The first weeks in the terminal are slower than clicking. That cost is paid once, and the time it saves comes back every day after.
- *Hosting.* GitHub, GitLab, and Bitbucket all have free plans that cover public and private repositories for individuals and small teams. Paid plans add things like more automation minutes, more storage for large files, and organisation controls. Check current prices before you rely on a limit.
- *Disk and bandwidth.* Big files in history cost every person who clones the project, on every clone.
- *Mistakes.* The most expensive items in this chapter are the silent ones. A cloud key leaked in a public repository can be used to run up a large bill before you notice. A week of work that was never pushed dies with a stolen laptop. Both are prevented by habits that cost nothing: ignore secrets, commit often, push daily.
