# Lab: Try an Idea Without Breaking Anything

In this lab you use a branch as a safe place to experiment. You'll hit a real merge conflict and resolve it, see what rebasing does to history, and rescue a commit you thought you'd deleted. After this, branches stop being scary and become the first thing you reach for.

*The problem.* I want to try an idea without risking the version that works.

*The question.* How do I experiment on a copy of my code and bring back only what works?

## Step 1: A Project That Works

Make a new repository with one working file:

```bash
mkdir -p ~/projects/greeter
cd ~/projects/greeter
git init
```

Create `greet.py`:

```python
def greet(name):
    return "Hello, " + name + "!"


print(greet("Ada"))
```

Check it runs, then commit:

```bash
python3 greet.py
git add greet.py
git commit -m "Add greeting"
```

**Expected:** `Hello, Ada!`, then a `root-commit` line.

## Step 2: Try the Idea on a Branch

The idea: a friendlier greeting. Create a branch for it, so `main` stays exactly as it is:

```bash
git switch -c friendly
```

On this branch, change the `return` line to `return "Hi there, " + name + "!"`, run the script, and commit:

```bash
python3 greet.py
git commit -am "Use a friendlier greeting"
```

**Expected:** `Hi there, Ada!`. Now switch back with `git switch main` and run `python3 greet.py` again. **Expected:** `Hello, Ada!`. The working version is untouched; Git swapped the file back when you switched.

## Step 3: Meanwhile, main Moves On

Real projects don't stand still while you experiment. On `main`, tidy the same line into an f-string, `return f"Hello, {name}!"`, and commit:

```bash
git commit -am "Use an f-string for the greeting"
git log --oneline --graph --all
```

```text
* 165c65b Use a friendlier greeting
| * c2ed7e4 Use an f-string for the greeting
|/  
* 180f173 Add greeting
```

`--all` shows every branch. The history has forked: both branches changed the same line in different ways.

## Step 4: Merge, and Meet a Conflict

The idea worked, so bring it into `main`:

```bash
git merge friendly
```

```text
Auto-merging greet.py
CONFLICT (content): Merge conflict in greet.py
Automatic merge failed; fix conflicts and then commit the result.
```

Nothing is broken. Git has paused the merge because it can't guess which version of that line you want. `git status` says so, and lists the file under `both modified`. Open `greet.py`:

```text
def greet(name):
<<<<<<< HEAD
    return f"Hello, {name}!"
=======
    return "Hi there, " + name + "!"
>>>>>>> friendly


print(greet("Ada"))
```

Git wrote both versions into the file between conflict markers. Everything between `<<<<<<< HEAD` and `=======` is your current branch's version. Everything between `=======` and `>>>>>>> friendly` is the incoming branch's version.

## Step 5: Resolve It

Resolving means editing the file into what it should be, and deleting all three marker lines. You can keep one side, the other, or combine them. Here the best answer combines both ideas: the f-string and the friendlier words.

```python
def greet(name):
    return f"Hi there, {name}!"


print(greet("Ada"))
```

Run it to make sure it works, then tell Git the conflict is resolved by staging the file, and finish the merge:

```bash
python3 greet.py
git add greet.py
git commit --no-edit
git log --oneline --graph
```

```text
Hi there, Ada!
[main beb0c29] Merge branch 'friendly'
*   beb0c29 Merge branch 'friendly'
|\  
| * 165c65b Use a friendlier greeting
* | c2ed7e4 Use an f-string for the greeting
|/  
* 180f173 Add greeting
```

`--no-edit` accepts Git's ready-made message. The idea is now in `main`, so delete its branch with `git branch -d friendly`.

> **Tip:** If a conflict gets confusing, `git merge --abort` puts everything back to how it was before the merge. Nothing is lost, and you can try again.

## Step 6: Rebasing, in Brief

A merge keeps history exactly as it happened, forks and all. There's a second way to bring a branch up to date: **rebase**. It lifts your branch's commits off and replays them on top of the latest `main`, as if you'd started the branch just now.

Make a branch, commit on it, then let `main` move on:

```bash
git switch -c shout
echo 'print(greet("Ben").upper())' >> greet.py
git commit -am "Shout at Ben"
git switch main
```

On `main`, add the line `"""A tiny greeter."""` at the top of `greet.py` and commit it as "Add a docstring". The history has forked again:

```text
* 2ebbb10 Add a docstring
| * eeb1248 Shout at Ben
|/  
*   beb0c29 Merge branch 'friendly'
```

Now rebase `shout` onto `main`:

```bash
git switch shout
git rebase main
git log --oneline --graph --all -3
```

```text
Successfully rebased and updated refs/heads/shout.
* 88709a8 Shout at Ben
* 2ebbb10 Add a docstring
*   beb0c29 Merge branch 'friendly'
```

The fork is gone. "Shout at Ben" now sits on top of the docstring commit, with a new ID (`88709a8` instead of `eeb1248`), because it's technically a new commit. Merging it into `main` is now a simple fast-forward: `git switch main`, then `git merge shout`. `python3 greet.py` prints `Hi there, Ada!` and `HI THERE, BEN!`.

> **Warning:** Rebase only commits that nobody else has. Rebasing rewrites commits into new ones, so if you rebase commits you've already pushed, everyone who pulled the old ones ends up with two conflicting histories. Rebase your own local work; merge shared work.

## Step 7: Lose a Commit, Then Find It

Last, the rescue. Make an experiment and commit it:

```bash
git switch -c experiment
echo 'print(greet("World"))' >> greet.py
git commit -am "Greet the whole world"
git switch main
```

Now delete the branch. Git refuses with `-d`, because the commit isn't merged anywhere, which is a good warning. Force it with `-D`:

```bash
git branch -D experiment
```

```text
Deleted branch experiment (was 207ad9c).
```

`git log --all` no longer shows "Greet the whole world". It looks gone. But the reflog remembers every place HEAD has been:

```bash
git reflog -3
```

```text
88709a8 HEAD@{0}: checkout: moving from experiment to main
207ad9c HEAD@{1}: commit: Greet the whole world
88709a8 HEAD@{2}: checkout: moving from main to experiment
```

There it is: `207ad9c`, one step back, at `HEAD@{1}`. A branch is just a bookmark, so put a new bookmark on it:

```bash
git branch experiment 207ad9c
git log --oneline -1 experiment
```

```text
207ad9c Greet the whole world
```

The commit is back. The same trick undoes an unwanted `git reset --hard HEAD~1`: find the old position in `git reflog`, then `git reset --hard HEAD@{1}`.

> **Note:** Git only keeps unreachable commits for a while (normally at least 30 days) before cleaning them up. The reflog is a safety net, not an archive. And it only knows about commits: uncommitted edits you throw away are gone for good.

## Summary, Key Terms, and Review Questions

### Summary

- A branch is a safe place to try an idea. Switching back to `main` restores the working version instantly.
- A merge conflict happens when both branches changed the same lines. Git pauses and writes both versions into the file between conflict markers.
- To resolve, edit the file into its final form, remove the markers, `git add` it, and commit. `git merge --abort` backs out.
- Rebase replays your commits on top of another branch, giving a straight history. Only rebase commits you haven't shared.
- Deleted branches and reset commits can be found in `git reflog` and brought back with a new branch or a reset.

### Key Terms

| Term | Meaning |
|---|---|
| Rebase | Replay a branch's commits on top of another commit, creating new commits |

### Review Questions

1. Why is the working version safe while you experiment on a branch?
2. In a conflict, which side sits between `<<<<<<< HEAD` and `=======`?
3. What three things must you do to finish resolving a conflict?
4. How does history look after a rebase compared with a merge? Why do the rebased commits get new IDs?
5. You deleted a branch with `git branch -D` and regret it. Describe how to get it back.

> **You understand this when** you can resolve a merge conflict without panic, and bring back a commit you thought was lost.
