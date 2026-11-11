# Why Code Needs a History

This chapter explains version control before you type a single Git command. You'll learn to see a project as a series of snapshots, what commits, branches, merges, and remotes are, and how Git differs from GitHub. With this picture in your head, the commands in Chapter 8 will make sense instead of feeling like spells.

*The problem.* My code worked yesterday. I changed something, and now I can't get yesterday back.

*The question.* How can I keep every working version of my project, and move between them safely?

## Version Control: A Photo Album for Your Project

**Version control** is a system that records the state of your project at moments you choose, so you can look back at any of them, compare them, and return to them. Think of a photo album. Every time the project reaches a state worth keeping, you take a photo of the whole thing and put it in the album with a caption. Later you can flip back to any page.

Each photo is a snapshot: the full contents of every file in the project at that moment. You don't photograph just the part you changed; the snapshot is the whole project. (Behind the scenes Git stores unchanged files only once, so this costs very little space.)

The album itself, with all its snapshots, is the **repository**, or repo. It lives in a hidden folder inside your project, so the project carries its own history with it.

## Commits: Snapshots with a Caption

A **commit** is one snapshot plus a few facts about it:

- *Who* made it (a name and email).
- *When* it was made.
- *Why*: a short message you write, like "Add login form".
- *What came before*: a link to the previous commit, called its parent.

Those parent links chain the commits together into a history. Each commit points back to the one before it:

```text
  A ◄── B ◄── C ◄── D
                    ▲
                  (now)
```

Every commit gets a unique ID, a long string of letters and digits computed from its contents, such as `b7e4f09c1d…`. People usually use just the first seven characters. The ID is how you name a commit when you want to look at it or go back to it.

A commit is deliberate. You decide when your work is in a state worth saving, and you describe it. That's different from autosave: the history records meaningful steps, not every keystroke. A good rule is to commit whenever something small works: a function is written, a bug is fixed, a test passes.

## Branches: Bookmarks in the Album

What if you want to try a risky idea without disturbing the version that works? You start a new line of commits that splits off from the main one. That separate line is a **branch**.

Here's the surprise: a branch isn't a copy of your files. It's a bookmark. A branch is just a name that points at one commit. When you make a new commit on a branch, the bookmark moves forward to it.

```text
                E ◄── F      idea
               /
  A ◄── B ◄── C ◄── D        main
```

Here `main` is the usual name for the main line, and `idea` is a branch that split off at `C`. Commits `E` and `F` exist only on `idea`; `main` doesn't see them. You can switch between branches at any time, and Git swaps the files in your folder to match.

How does Git know which branch you're on? It keeps one more marker, **HEAD**, which means "you are here". HEAD normally points at a branch, and the branch points at a commit.

Because branches are just bookmarks, they're cheap. Making one is instant, so developers make them for every feature, every fix, and every experiment.

## Merging: Bringing Work Back Together

If the idea works, you want it in `main`. A **merge** combines the work of two branches. Git finds the commit where they split (`C`), works out what each side changed since then, and applies both sets of changes. The result is a new commit with two parents:

```text
                E ◄── F
               /       \
  A ◄── B ◄── C ◄── D ◄── M    main
```

Most merges are automatic. If one side changed `login.py` and the other changed `README.md`, there's nothing to decide. But if both sides changed the same lines of the same file in different ways, Git can't know which one you want. That's a **merge conflict**: Git stops, marks the disputed lines in the file, and asks you to choose. It sounds scary, and it's routine. Chapter 10 walks you through one.

If the idea fails, you simply switch back to `main` and delete the branch. `main` never knew about it.

## Remotes: Copies of the Project Elsewhere

So far the album sits on your laptop. If your laptop dies, the history dies with it. And a colleague can't add their own photos.

The fix is to keep another copy of the repository somewhere else, usually on a server. That other copy is a **remote**. Unlike older systems, Git doesn't treat the server as special. Every copy is a complete repository with the full history. Making your own full copy of an existing repository is called cloning, and the copy is a **clone**.

Copies are kept in step with two actions:

- **Push** sends your new commits from your repository to the remote.
- **Pull** brings new commits from the remote into your repository.

```text
   Ada's laptop                        Ben's laptop
   ┌──────────┐    push     ┌───────┐    pull   ┌──────────┐
   │   repo   │ ──────────► │remote │ ────────► │   repo   │
   └──────────┘             └───────┘           └──────────┘
```

Ada commits on her laptop and pushes. Ben pulls and gets Ada's commits. Then it's Ben's turn. The remote is the meeting point, and also a backup.

## What Git Is, and Why GitHub Is Not Git

**Git** is the version control program you'll use in this book. It's free, it runs on your own computer, and it works entirely offline. Commits, branches, merges, and history all happen on your machine.

**GitHub** is a website owned by a company. It stores Git repositories on its servers, so they can serve as remotes, and it adds features around them: web pages to browse code, pull requests for reviewing changes, issue trackers, and automated checks. GitLab and Bitbucket are similar services.

The difference matters. You don't need GitHub to use Git: a folder on a shared drive can be a remote, and that's what this book's labs use. And the pull request, GitHub's best-known feature, is not part of Git at all; Chapter 11 explains it. When a tutorial says "Git", it means the program. When it says "GitHub", it means the website.

> **Note:** Git has many commands, but the ideas are few: snapshots, a chain of history, bookmarks called branches, merges that join them, and copies called remotes. Every command in Chapter 8 is one of these ideas in action.

## Lab: Meet Git

Git needs to know who you are before it can record who made each commit. These settings live in a small file in your home folder and apply to every repository you create.

1. Check that Git is installed: `git --version`. **Expected:** a line like `git version 2.52.0`. Any version from 2.28 onward works with this book.
2. Tell Git your name and email (use your own):

   ```bash
   git config --global user.name "Ada Lovelace"
   git config --global user.email "ada@example.com"
   ```

   **Expected:** no output. Silence means success.

3. Make new repositories start on a branch called `main`:

   ```bash
   git config --global init.defaultBranch main
   ```

   **Expected:** no output.

4. Check your settings: `git config --global --list`. **Expected:**

   ```text
   user.name=Ada Lovelace
   user.email=ada@example.com
   init.defaultbranch=main
   ```

   You may see extra lines if you've used Git before.

5. On paper, draw the history for this story: you commit `A` and `B` on `main`; you make a branch `fix` from `B` and commit `C` on it; you commit `D` on `main`; then you merge `fix` into `main`, creating `M`. **Expected:** `A ◄── B ◄── D ◄── M` along `main`, with `C` branching off `B` and joining at `M`. `M` has two parents: `D` and `C`.

> **Tip:** The email becomes part of every commit and is visible to anyone who sees the repository. If you'll publish code, GitHub gives you a private "noreply" address you can use here instead.

## Summary, Key Terms, and Review Questions

### Summary

- Version control keeps snapshots of your whole project so you can compare and return to any of them.
- A commit is a snapshot plus author, time, message, and a link to its parent. The links form the history.
- A branch is a movable bookmark pointing at a commit. HEAD marks where you are.
- A merge combines two branches; when both changed the same lines, you resolve a conflict.
- A remote is another full copy of the repository. You push to it and pull from it.
- Git is the program on your computer. GitHub is a website that hosts Git repositories and adds features like pull requests.

### Key Terms

| Term | Meaning |
|---|---|
| Version control | A system that records a project's states so you can return to them |
| Repository | The project's collected history, stored with the project |
| Commit | A snapshot with an author, time, message, and parent |
| Branch | A movable name that points at a commit |
| HEAD | Git's marker for "you are here" |
| Merge | Combining the work of two branches |
| Merge conflict | Both branches changed the same lines; you must choose |
| Remote | Another copy of the repository, usually on a server |
| Clone | A full copy of an existing repository |
| Push | Send your commits to a remote |
| Pull | Bring a remote's commits into your repository |
| Git | The free version control program that runs on your computer |
| GitHub | A website that hosts Git repositories and adds collaboration tools |

### Review Questions

1. Why is `app_final_v2.py` a poor way to keep old versions?
2. What four things does a commit record besides your files?
3. A branch "isn't a copy of your files". What is it, then, and why does that make branches cheap?
4. When does a merge need your help?
5. If GitHub disappeared tomorrow, what would happen to the repository on your laptop?

> **You understand this when** you can draw a history with a branch and a merge, and explain every arrow and label in it.
