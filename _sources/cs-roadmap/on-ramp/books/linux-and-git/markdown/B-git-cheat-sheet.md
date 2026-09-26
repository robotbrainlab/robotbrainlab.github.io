# Git Cheat Sheet

The Git commands from this book, in the order you'll usually need them.

## Set Up Once

| Command | What it does |
|---|---|
| `git config --global user.name "Ada Lovelace"` | Name recorded in your commits (and `user.email`) |
| `git config --global init.defaultBranch main` | New repositories start on `main` |
| `git config --global pull.rebase false` | Pulls combine diverged work by merging |

## Every Day

| Command | What it does |
|---|---|
| `git init`, `git clone <url-or-path>` | Start a repository; copy an existing one |
| `git status` | What changed, and what's staged |
| `git diff`, `git diff --staged` | Unstaged changes; what the next commit will hold |
| `git add file`, `git commit -m "Message"` | Stage a change; record the snapshot (`-am` does both) |
| `git log --oneline --graph --all` | History of every branch, drawn as a graph |
| `git switch -c name`, `git switch name` | Create and switch to a branch; switch to one |
| `git merge name`, `git merge --abort` | Merge `name` into this branch; back out of a conflict |
| `git rebase main` | Replay this branch on top of `main` (unshared commits only) |
| `git branch -d name` | Delete a merged branch (`-D` forces it) |

## Sharing

| Command | What it does |
|---|---|
| `git init --bare name.git` | Make a repository to use as a shared remote |
| `git remote add origin <url-or-path>` | Name a remote (`git remote -v` lists them) |
| `git push -u origin main` | First push of a branch, remembering the pairing |
| `git push`, `git pull`, `git fetch` | Send; fetch and merge; fetch only |
| `git diff main...origin/branch` | What a branch changed since it split from `main` |
| `git push origin --delete name` | Delete a branch on the remote |

## Undo

| Situation | Command |
|---|---|
| Discard unstaged edits to a file | `git restore file` |
| Unstage a file, keeping the edits | `git restore --staged file` |
| Fix the last commit (message or files) | `git commit --amend` |
| Undo a pushed commit safely | `git revert <id>` |
| Undo the last local commit | `git reset --soft HEAD~1` (keep changes) or `--hard` (discard) |
| Find a "lost" commit and bring it back | `git reflog`, then `git branch name <id>` |

## Resolving a Conflict

1. `git status` lists files marked `both modified`.
2. Edit each file to its final form and delete the `<<<<<<<`, `=======`, and `>>>>>>>` lines.
3. Run the code to check it works, then `git add` each file and `git commit`.
