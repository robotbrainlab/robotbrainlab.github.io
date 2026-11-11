# Where to Go from Here

You can now open a terminal and know what you're typing. You can find, read, and change files, keep programs running, write a script you trust, and use Git to save your work, try ideas safely, and share a project with other people. This last chapter suggests what to learn next, and just as usefully, what you can safely ignore for a while.

## Make It a Habit First

The fastest way to get good at these tools is to use them for everything, starting today:

- Put every project in a Git repository from its first file, and push it to a remote.
- Do small jobs in the terminal even when a mouse would be quicker at first: moving files, searching logs, renaming things.
- When you type the same commands twice, make them a script, with `set -euo pipefail` and a pass through shellcheck.
- When a command surprises you, read its `man` page instead of searching for a fix to paste.

A month of this does more than any course.

## What to Learn Next

*More Git, as you need it.* A few commands earn their place once the basics feel natural. `git stash` puts half-finished work aside so you can switch branches. `git tag` marks releases. `git rebase -i` (interactive rebase) lets you tidy your own commits before you open a pull request. `git bisect` finds the commit that introduced a bug by testing halfway points. Learn each one when a real problem calls for it.

*Automated checks.* Hosting sites can run your tests on every push and every pull request, and block merging when they fail. On GitHub this is GitHub Actions. It's the natural next step after pull requests, and it's covered in *Infrastructure Engineering from Zero*.

*A terminal editor.* Sooner or later you'll edit a file on a server with no graphical editor. Learn enough `nano` to edit and save, or enough Vim to edit, save, and quit (`:wq`).

*What's under the shell.* This book explained only as much about the kernel, processes, and memory as the terminal needs. *Operating Systems from Zero* goes underneath: system calls, how processes and threads really run, virtual memory, and file systems.

*The network.* SSH, `git push`, and `curl` all cross a network you've treated as a pipe. *Networking from Zero* explains what happens on the way: addresses, ports, DNS, TCP, and HTTP. It's the book to read when "it works on my machine" but nobody else can reach it.

*Building with these tools.* *Web Applications from Zero* and *APIs to FastAPI* put the terminal and Git to work on real programs, and *The Complete Software Engineering Guide* takes one project from an idea all the way to production, using everything here along the way.

## What to Skip for Now

Plenty of material online is correct but not yet useful to you. It's safe to skip:

- *Git's internals.* How objects, trees, and packfiles are stored is fascinating, and you don't need it to use Git well. The same goes for "plumbing" commands like `git cat-file` and `git update-ref`.
- *Complex branching strategies.* Models with many long-lived branches (develop, release, hotfix) solve problems of large teams shipping versioned software. A `main` branch plus short feature branches serves almost everyone else.
- *Submodules and hooks.* Useful in specific situations; you'll know when you reach one.
- *Every option of every command.* Learn the handful you use, and look the rest up when you need them.
- *Advanced `awk` and `sed` programs.* Past a few lines, write the job in Python instead. It's easier to read and test.
- *Shell customisation rabbit holes.* Fancy prompts, plugin frameworks, and elaborate dotfiles are fun, but they don't make you more capable. A plain shell you understand is better than a clever one you don't.

## One Last Thing

Every developer you admire once typed `ls` and wondered what it would do. The difference between them and a beginner isn't talent; it's hours in the terminal and a history of commits. Open a terminal, start a repository, and make your first commit today. Then make another one tomorrow.
