# Lab: Work on a Project with Someone Else

In this lab you play two people, Ada and Ben, sharing one project through a remote. You'll see how Git refuses to let one person's push wipe out another's work, how `fetch` and `pull` bring changes together, and how teams use feature branches and pull requests to review work before it lands. You'll finish with forks, the open-source workflow, and licences.

*The problem.* Two of us edited the same file, and someone's work vanished.

*The question.* How do several people change one project at the same time without losing anyone's work?

You need no accounts. A bare repository on your own disk plays the part of GitHub, and two folders play Ada's and Ben's laptops. Paths in the output show `/home/ada` because one person runs the whole lab.

## Step 1: Set Up the Shared Remote

Create the shared repository, then Ada's copy:

```bash
mkdir -p ~/collab && cd ~/collab
git init --bare ~/remotes/team.git
git clone ~/remotes/team.git ada
cd ada
git config user.name "Ada"
git config user.email "ada@example.com"
```

`git config` without `--global` sets the name for this repository only. That's how one computer can pretend to be two people. Git warns `You appear to have cloned an empty repository`, which is true and harmless.

Ada writes `shop.py`:

```python
PRICES = {"apple": 0.5, "bread": 2.0}


def total(items):
    return sum(PRICES[item] for item in items)


print(total(["apple", "bread"]))
```

She commits and pushes:

```bash
git add shop.py
git commit -m "Add shop total"
git push
```

**Expected:** `* [new branch]      main -> main`.

Now make Ben's copy the same way: from `~/collab`, run `git clone ~/remotes/team.git ben`, then set `user.name` to `Ben` and `user.email` to `ben@example.com` inside it. **Expected:** `git log --oneline` in `ben` shows Ada's commit.

## Step 2: Both Work at Once

Ada adds milk to the prices in `shop.py`, commits, and pushes. It goes through. Meanwhile Ben, who hasn't seen Ada's change, adds a `README.md`, commits, and pushes:

```bash
git push
```

```text
To /home/ada/remotes/team.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to '/home/ada/remotes/team.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. …
```

This is the answer to the chapter's problem. When files are shared by email or a synced folder, the last person to save wins, and the other's work silently vanishes. Git refuses instead. Ben's push would have replaced Ada's commit, so the remote rejects it until Ben has Ada's work too.

## Step 3: Fetch, Look, Then Pull

`git fetch` downloads new commits from the remote without touching your files or your branches. They land in a **remote-tracking branch**, `origin/main`: Git's record of where `main` was on the remote when you last checked.

```bash
git fetch
git status
git log --oneline --graph --all
```

```text
On branch main
Your branch and 'origin/main' have diverged,
and have 1 and 1 different commits each, respectively.
…
* 193c83f Add README
| * b2f7c97 Add milk to prices
|/  
* 04da6ba Add shop total
```

History has forked, just like two branches. `git pull` is simply `git fetch` followed by a merge of `origin/main` into your branch. When the histories have diverged, Git wants you to choose once how pulls should combine them. Pick merging, which you already know:

```bash
git config --global pull.rebase false
git pull
```

```text
Merge made by the 'ort' strategy.
 shop.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

Git opens your editor with a merge message; save and close it. Now Ben has both changes, and `git push` succeeds. Back in `ada`, a `git pull` fast-forwards and brings in Ben's README.

**Expected:** both folders contain `README.md` and the milk price, and `git log --oneline` shows the same commit at the top in both.

If Ada and Ben had changed the same line, `git pull` would have stopped with a conflict. You'd resolve it exactly as in Chapter 10: edit, `git add`, commit, then push.

> **Tip:** Pull before you start work and before you push. The less time your copy spends out of date, the smaller any conflict will be.

## Step 4: A Feature Branch

Pushing straight to `main` works for two people. Teams usually protect `main` and make every change on a **feature branch** first, so someone can review it before it lands. Ben wants to add discounts:

```bash
git switch -c add-discount
```

He appends a function to `shop.py`:

```python
def with_discount(amount, percent):
    return round(amount * (1 - percent / 100), 2)
```

He commits it as "Add percentage discount" and pushes the branch, not `main`:

```bash
git push -u origin add-discount
```

```text
To /home/ada/remotes/team.git
 * [new branch]      add-discount -> add-discount
branch 'add-discount' set up to track 'origin/add-discount'.
```

## Step 5: The Pull Request and the Review

On GitHub, this is where Ben opens a **pull request**: a web page that proposes "please merge `add-discount` into `main`", with a place to discuss it. Pull requests are a feature of hosting sites, not of Git. Here's what Ben would see:

1. A yellow banner on the repository page says his branch had recent pushes, with a *Compare & pull request* button.
2. He picks the target (`main`) and his branch, writes a title and a description of what changed and why, and clicks *Create pull request*.
3. The pull request page has tabs. *Conversation* holds the discussion. *Commits* lists his commits. *Files changed* shows the diff.

Ada does a code review: she reads the change and leaves comments on specific lines. She can then choose *Comment*, *Approve*, or *Request changes*. You can do the same review from the terminal:

```bash
cd ~/collab/ada
git fetch
git diff main...origin/add-discount
```

```text
…
 print(total(["apple", "bread"]))
+
+
+def with_discount(amount, percent):
+    return round(amount * (1 - percent / 100), 2)
```

The three dots mean "what the branch changed since it split from `main`". Ada asks for an example of the function in use. Ben adds `print(with_discount(10, 15))`, commits "Show a discount example", and runs `git push` again. On GitHub, the new commit simply appears in the same pull request. There's no need to open a new one.

## Step 6: Merge and Clean Up

Satisfied, Ada merges. On GitHub she'd click *Merge pull request*, then *Delete branch*. Locally, the same thing is:

```bash
git merge --no-ff --no-edit origin/add-discount
git push
git push origin --delete add-discount
```

`--no-ff` makes a merge commit even though a fast-forward was possible, as GitHub's button does, so the history records that a reviewed branch came in. Ben then updates and tidies his copy:

```bash
cd ~/collab/ben
git switch main
git pull
git branch -d add-discount
```

**Expected:** `python3 shop.py` prints `2.5` and `8.5` in both folders.

## Step 7: Forks

You can't push to a stranger's project. So on GitHub you click **Fork**, which makes your own full copy of their repository under your account. You push to your fork, then open a pull request from your fork to theirs. The original project is called **upstream**.

Simulate it with a third person, Cy. A fork is just a bare clone:

```bash
cd ~/collab
git clone --bare ~/remotes/team.git ~/remotes/cy-fork.git
git clone ~/remotes/cy-fork.git cy
cd cy
git remote add upstream ~/remotes/team.git
git remote -v
```

```text
origin	/home/ada/remotes/cy-fork.git (fetch)
origin	/home/ada/remotes/cy-fork.git (push)
upstream	/home/ada/remotes/team.git (fetch)
upstream	/home/ada/remotes/team.git (push)
```

Cy's `origin` is her fork, which she can push to. `upstream` is the original. When the original moves on, she keeps her fork current like this:

```bash
git fetch upstream
git merge upstream/main
git push origin main
```

**Expected:** after Ada pushes a new commit to `team.git`, these three commands bring it into Cy's copy and her fork.

## The Open-Source Workflow

**Open source** means the code is public and anyone may use, study, change, and share it, under the terms of its licence. Contributing to a project usually goes like this:

1. Read the `README` and any `CONTRIBUTING` file. They explain how the project wants to work.
2. Find or open an issue, the project's to-do and bug list on GitHub. Say what you plan to do before writing code, so nobody's effort is wasted.
3. Fork, clone, create a feature branch, commit, and push to your fork.
4. Open a pull request to upstream, respond to review, and push fixes to the same branch.

A **licence** is the file, usually `LICENSE`, that says what others may do with the code. Three are common:

| Licence | In short |
|---|---|
| MIT | Do almost anything; keep the copyright notice |
| Apache 2.0 | Like MIT, plus explicit patent terms |
| GPL 3.0 | You may share changes, but shared versions must stay GPL |

> **Warning:** Public code with no licence is not free to use. By default, copyright means all rights are reserved. Check the licence before you copy code into your project, and add one to anything you publish.

## Summary, Key Terms, and Review Questions

### Summary

- A shared remote is the meeting point. Git rejects a push that would overwrite someone else's commits.
- `git fetch` downloads commits into remote-tracking branches like `origin/main`; `git pull` fetches and merges.
- Teams make changes on feature branches, push them, and open pull requests for code review before merging.
- More commits pushed to the branch update the same pull request. After merging, delete the branch.
- A fork is your own copy of someone else's repository; `upstream` points at the original.
- Open-source work flows through issues, forks, and pull requests. The licence decides what you may do with the code.

### Key Terms

| Term | Meaning |
|---|---|
| Remote-tracking branch | Git's record of a remote branch, such as `origin/main` |
| Feature branch | A branch holding one change, to be reviewed and merged |
| Pull request | A hosting site's proposal and discussion page for merging a branch |
| Fork | Your own copy of someone else's repository on a hosting site |
| Upstream | The original repository a fork was copied from |
| Open source | Code anyone may use, change, and share under its licence |
| Licence | The terms that say what others may do with the code |

### Review Questions

1. Why did Git reject Ben's push, and what would have happened to Ada's work if it hadn't?
2. What's the difference between `git fetch` and `git pull`?
3. Why do teams use feature branches and pull requests instead of pushing to `main`?
4. How do you update an open pull request after a reviewer asks for changes?
5. In a fork, what do `origin` and `upstream` point to?
6. You find useful code on GitHub with no licence. May you copy it into your project?

> **You understand this when** you can take a change from a feature branch, through review, into a shared `main`, without anyone's work being lost.
