# Git Every Day

This chapter turns the ideas from Chapter 4 into commands. You'll start a repository, learn where your changes live before and after a commit, read history and differences, keep unwanted files out, work on branches, share with a remote, and undo the most common mistakes. These are the Git commands you'll use every working day.

*The problem.* I want to save my work properly, not as `final_v2_really_final.py`.

*The question.* What are the daily Git commands, and what does each one do to my project?

The examples build a tiny project, `recipes`, that scales ingredient amounts. You need the name and email you set in the Chapter 4 lab.

## Starting a Repository

Any folder becomes a Git repository with `git init`:

```bash
mkdir -p ~/projects/recipes
cd ~/projects/recipes
git init
```

```text
Initialized empty Git repository in /home/ada/projects/recipes/.git/
```

Git created one hidden folder, `.git`. That's the repository: every commit and branch lives inside it. Your files stay where they are. Delete `.git` and the folder is an ordinary folder again, with all its history gone.

`git status` is the command you'll run most. It tells you where you are and what has changed:

```bash
git status
```

```text
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

## Three Places Your Work Lives

Git keeps your work in three places, and every command moves changes between them. Think of posting a parcel. Your desk is where you make things. The box is where you put exactly what you want to send. The post office stamps the box and keeps a record forever.

- The **working tree** is your desk: the normal files you edit.
- The **staging area** is the box: the changes you've chosen for the next commit. (Git also calls it the index.)
- The repository is the post office: the commits, stored safely in `.git`.

```text
  working tree      staging area       repository
  (your files)      (next commit)      (history)
       │                 │                 │
       │ ── git add ───► │                 │
       │                 │ ─ git commit ─► │
       │ ◄──────── git restore ─────────── │
```

Why the box? Because you often change several things at once, and they belong in separate commits. Staging lets you choose.

## The Everyday Loop: Add and Commit

Create `scale.py` in your editor:

```python
def scale(amount, factor):
    return amount * factor

print(scale(200, 2))
```

Git notices the new file but doesn't track it yet: `git status` now lists `scale.py` under "Untracked files". `git add` puts it in the box; `git commit` records the snapshot. The `-m` gives the message:

```bash
git add scale.py
git commit -m "Add function to scale a recipe"
```

```text
[main (root-commit) 4978b71] Add function to scale a recipe
 1 file changed, 4 insertions(+)
 create mode 100644 scale.py
```

`4978b71` is the start of the new commit's ID. `git log` shows the history: each commit's full ID, author, date, and message.

That's the loop you'll repeat all day: edit, `git status`, `git add`, `git commit`.

> **Tip:** `git add .` stages every change in the current folder. It's handy, but run `git status` first so you don't commit something you didn't mean to.

## Seeing What Changed

Now change `scale.py` so it rounds results, and add a second example:

```python
def scale(amount, factor):
    return round(amount * factor, 1)

print(scale(200, 2))
print(scale(150, 0.333))
```

`git diff` shows changes in the working tree that aren't staged yet. Lines starting with `-` were removed; lines starting with `+` were added:

```bash
git diff
```

```text
diff --git a/scale.py b/scale.py
…
@@ -1,4 +1,5 @@
 def scale(amount, factor):
-    return amount * factor
+    return round(amount * factor, 1)
 
 print(scale(200, 2))
+print(scale(150, 0.333))
```

Once you `git add` the file, plain `git diff` shows nothing, because nothing is left unstaged. `git diff --staged` shows what's in the box instead. Always look before you commit:

```bash
git add scale.py
git commit -m "Round scaled amounts to one decimal place"
git log --oneline
```

```text
[main 450c3a8] Round scaled amounts to one decimal place
 1 file changed, 2 insertions(+), 1 deletion(-)
450c3a8 Round scaled amounts to one decimal place
4978b71 Add function to scale a recipe
```

`git log --oneline` gives one line per commit, newest first. `git show 450c3a8` shows a single commit and its changes.

## Keeping Files Out with .gitignore

Some files must never be committed: secrets such as `.env`, and files your tools generate, such as Python's `__pycache__` folder or a `.venv`. Git lists them as untracked, which is noise at best and a leak at worst:

```bash
git status --short
```

```text
?? .env
?? __pycache__/
```

List the patterns to ignore in a file called **.gitignore** at the top of the project, one per line:

```text
.env
__pycache__/
.venv/
```

Now `git status --short` shows only `?? .gitignore`. Commit the `.gitignore` itself, so everyone who clones the project ignores the same things.

> **Warning:** `.gitignore` only stops files from being added. If a secret was already committed, ignoring it now doesn't remove it from history. Chapter 12 explains what to do.

## Writing Good Commit Messages

A commit message is a note to the person reading the history later, usually you. Write the first line as a short command that completes the sentence "If applied, this commit will…". Keep it under about 50 characters. If more explanation helps, leave a blank line and write why you made the change.

| Weak | Better |
|---|---|
| `fix` | `Fix crash when amount is zero` |
| `changes` | `Round scaled amounts to one decimal place` |
| `stuff for Sam` | `Add ounces-to-grams conversion` |

One commit should hold one logical change. If your message needs "and", consider two commits.

## Branches and Merging

To try something without touching `main`, create a branch and switch to it in one step with `git switch -c`. `git branch` lists branches; the `*` marks where HEAD is:

```bash
git switch -c metric
git branch
```

```text
Switched to a new branch 'metric'
  main
* metric
```

Add a `to_grams` function to `scale.py` and commit it on the branch. (`git commit -am` stages every changed tracked file and commits in one step.) Then switch back: `main` doesn't have the new function yet, because the commit lives only on `metric`:

```bash
git commit -am "Add ounces-to-grams conversion"
git switch main
git merge metric
```

```text
[metric 015db0b] Add ounces-to-grams conversion
 1 file changed, 4 insertions(+)
Switched to branch 'main'
Updating f88f44f..015db0b
Fast-forward
 scale.py | 4 ++++
 1 file changed, 4 insertions(+)
```

This was a **fast-forward** merge. `main` hadn't moved since the branch split, so Git simply slid the `main` bookmark forward to the branch's commit. No new commit was needed. Delete the finished branch with `git branch -d metric`.

When both branches have new commits, Git makes a merge commit with two parents. Git opens your editor with a ready-made message; save and close it to finish. `git log --graph` draws the result:

```text
*   0ea3aaa Merge branch 'readme'
|\  
| * 97e1215 Add a README
* | 8ea3115 Print a conversion example
|/  
* 015db0b Add ounces-to-grams conversion
```

> **Tip:** If Git opens an editor you don't know how to leave, you're probably in Vim: type `:wq` and press Enter. To use a friendlier editor, run `git config --global core.editor "nano"` (or `"code --wait"` for VS Code).

## Push and Pull

A remote can be any Git repository you can reach, including a folder on your own disk. A **bare repository** has history but no working tree: nobody edits files in it, it only receives and hands out commits. That's what hosting services like GitHub keep on their servers, and you can make one yourself:

```bash
git init --bare ~/remotes/recipes.git
git remote add origin ~/remotes/recipes.git
git push -u origin main
```

```text
Initialized empty Git repository in /home/ada/remotes/recipes.git/
To /home/ada/remotes/recipes.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

`git remote add` gives the remote a short name; origin is the usual name for the main one. `git push -u origin main` sends your `main` branch there, and `-u` remembers the pairing, so later you can type just `git push` and `git pull`.

Anyone (including you, on another machine) can now `git clone ~/remotes/recipes.git`, commit, and `git push`. To bring their commits into your copy, pull:

```bash
git pull
```

```text
From /home/ada/remotes/recipes
   0ea3aaa..1d39f76  main       -> origin/main
Updating 0ea3aaa..1d39f76
Fast-forward
 README.md | 1 +
 1 file changed, 1 insertion(+)
```

Chapter 11 covers what happens when two people push at once.

## Undoing Mistakes

Git can undo almost anything, as long as you pick the right tool for where the mistake lives:

| Situation | Command |
|---|---|
| Throw away edits to a file (not yet staged) | `git restore scale.py` |
| Take a file out of the box, keeping the edits | `git restore --staged notes.txt` |
| Fix the last commit's message, or add a forgotten file | `git commit --amend` |
| Undo a commit that's already pushed | `git revert <id>` |
| Undo the last commit, keeping its changes staged | `git reset --soft HEAD~1` |
| Throw away the last commit and its changes | `git reset --hard HEAD~1` |

`HEAD~1` means "one commit before where I am". A typo'd message is fixed like this:

```bash
git commit -am "Add serving sise"
git commit --amend -m "Add serving size"
```

`git revert` is the safe undo for shared history. Instead of deleting a commit, it adds a new commit that does the opposite, so nobody who already pulled is confused:

```bash
git revert --no-edit HEAD
git log --oneline -3
```

```text
[main 2f795a7] Revert "Add serving size"
…
2f795a7 Revert "Add serving size"
ebebf8c Add serving size
1d39f76 Describe the project
```

`git reset` moves the branch bookmark backwards, as if later commits never happened. Use it only on commits you haven't pushed.

> **Warning:** `git restore <file>` and `git reset --hard` discard uncommitted work for good. Git never saw those edits, so it can't give them back. Commit often.

And if you reset too far? Suppose you ran `git reset --hard HEAD~1` twice, throwing away both the revert and "Add serving size". Git keeps a diary of everywhere HEAD has been, the **reflog**, and even "lost" commits appear there for weeks:

```bash
git reflog -4
```

```text
1d39f76 HEAD@{0}: reset: moving to HEAD~1
ebebf8c HEAD@{1}: reset: moving to HEAD~1
2f795a7 HEAD@{2}: revert: Revert "Add serving size"
ebebf8c HEAD@{3}: commit (amend): Add serving size
```

`git reset --hard ebebf8c` would bring that commit back. Chapter 10 practises exactly this rescue.

## Lab: Save Your Work Properly

Make a new folder and go into it: `mkdir -p ~/projects/lab8`, then `cd ~/projects/lab8`.

1. `git init`, then `git status`. **Expected:** `On branch main` and `No commits yet`.
2. Create `hello.py` containing `print("hello")`. Run `git status --short`. **Expected:** `?? hello.py`.
3. `git add hello.py`, then `git status --short`. **Expected:** `A  hello.py`.
4. `git commit -m "Add greeting script"`. **Expected:** a line starting `[main (root-commit)` and `1 file changed`.
5. Change the text to `"hello, world"` and run `git diff`. **Expected:** one `-` line and one `+` line.
6. `git commit -am "Greet the world"`, then `git log --oneline`. **Expected:** two commits, newest first.
7. Create `.env` and a `.gitignore` containing `.env`. Run `git status --short`. **Expected:** only `?? .gitignore`. Commit it with `git add .gitignore` and `git commit -m "Ignore .env"`.
8. `git switch -c shout`, change the text to `"HELLO, WORLD"`, commit, `git switch main`, `git merge shout`. **Expected:** `Fast-forward`, and `python3 hello.py` prints `HELLO, WORLD`.
9. Make a bare remote with `git init --bare ~/remotes/lab8.git`, then `git remote add origin ~/remotes/lab8.git` and `git push -u origin main`. **Expected:** `* [new branch]      main -> main`.
10. Edit `hello.py` badly, then `git restore hello.py`. **Expected:** `git status` says `nothing to commit, working tree clean`.

## Summary, Key Terms, and Review Questions

### Summary

- `git init` creates the repository (`.git`). `git status` is your compass.
- Work moves from the working tree, to the staging area (`git add`), to the repository (`git commit`).
- `git diff`, `git diff --staged`, `git log`, and `git show` let you see changes and history.
- `.gitignore` keeps secrets and generated files out. Good messages say what the commit does, in a short command.
- `git switch -c` creates a branch; `git merge` joins it back, by fast-forward or with a merge commit.
- `git push` and `git pull` sync with a remote such as `origin`.
- Undo with `restore`, `--amend`, `revert` (safe for shared history), or `reset` (local only). The reflog remembers where you've been.

### Key Terms

| Term | Meaning |
|---|---|
| Working tree | The project files you see and edit |
| Staging area | The changes chosen for the next commit (also called the index) |
| .gitignore | A file listing patterns Git should not track |
| Fast-forward | A merge that just moves the branch pointer forward |
| Bare repository | A repository with history but no working tree, used as a remote |
| Reflog | Git's record of everywhere HEAD has pointed |

### Review Questions

1. Name the three places your work lives, and the commands that move it.
2. What's the difference between `git diff` and `git diff --staged`?
3. Why ignore `.env`, and why isn't that enough once it's committed?
4. When does a merge fast-forward, and when does it create a merge commit?
5. You pushed a bad commit an hour ago. Should you use `reset` or `revert`? Why?

> **You understand this when** you can make a change, review it with `git diff`, commit it with a clear message, and undo it the safe way.
