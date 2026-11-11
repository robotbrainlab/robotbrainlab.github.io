# Installing Software and Working Remotely

This chapter covers two everyday jobs: getting the software you need, safely and in the right version, and working on a machine that isn't in front of you, with SSH keys, file copies, and sessions that survive a dropped connection.

*The problem.* I need a tool on a machine I can only reach over the internet.

*The question.* How do I install tools safely, and work on a machine that isn't in front of me?

## Package Managers

On a phone you use the app store, not random websites. The terminal's app store is a **package manager**. It downloads software from a trusted source, installs it, and can update or remove it later. Each piece of software is a package, and most need other packages, their dependencies, which the package manager installs for you.

| System | Package manager | Install | Update everything |
|---|---|---|---|
| Ubuntu, Debian, WSL | `apt` | `sudo apt install jq` | `sudo apt update && sudo apt upgrade` |
| Fedora, Red Hat | `dnf` | `sudo dnf install jq` | `sudo dnf upgrade` |
| macOS | Homebrew | `brew install jq` | `brew update && brew upgrade` |

On Debian and Ubuntu, `apt update` only refreshes the list of what's available; `apt upgrade` installs newer versions. Run `update` before installing. Homebrew, installed from brew.sh, keeps everything in your own folders, so it needs no `sudo`.

> **Warning:** Some guides say to paste `curl ... | sudo bash`, which runs a downloaded script as root, unread. Prefer your package manager, or download the script and read it first.

## Virtual Environments for Python

Project A needs version 1 of a library and project B needs version 2, but your system has one Python. A **virtual environment** solves this: a folder with its own Python and its own packages, one per project. Create one in the project folder, then activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
which python
```

```text
/home/ada/sandbox/.venv/bin/python
```

Activating puts `.venv/bin` at the front of your PATH, so `python` and `pip` mean the project's copies, and your prompt shows `(.venv)`. Now `pip install requests` installs into this project only. `deactivate` goes back. A version manager, such as `pyenv` or `uv` for Python, goes further and installs whole language versions side by side.

> **Tip:** Keep `.venv` out of Git (Chapter 8 shows how). Record what the project needs with `pip freeze > requirements.txt` instead, so anyone can rebuild the environment.

## SSH: A Terminal on Another Machine

**SSH** (Secure Shell) lets you open a shell on another computer over the network. Everything you type and see travels encrypted.

```bash
ssh ada@203.0.113.10
```

That means "log in as `ada` on the machine at that address". The first time, SSH shows the server's fingerprint and asks whether to trust it; it remembers your answer in `~/.ssh/known_hosts` and warns loudly if the fingerprint ever changes.

You could log in with a password, but passwords can be guessed. The better way is a **key pair**: two linked files. Think of a padlock and its key. The **public key** is the padlock: you can hand out copies freely and fit one to every server you use. The **private key** is the only key that opens those padlocks, and it never leaves your laptop.

```bash
ssh-keygen -t ed25519 -C "ada@laptop" -f ~/.ssh/id_ed25519
```

It asks for a passphrase twice. Choose one: it protects the private key if your laptop is stolen. Then:

```text
Your identification has been saved in /home/ada/.ssh/id_ed25519
Your public key has been saved in /home/ada/.ssh/id_ed25519.pub
…
```

The `.pub` file is the padlock:

```bash
cat ~/.ssh/id_ed25519.pub
```

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDIpXo4KbS5P4qftLjgXDY393xIkLDJdG/ggTPq9Dqyk ada@laptop
```

`ssh-copy-id ada@203.0.113.10` installs it on a server; GitHub and cloud providers have a page where you paste it. From then on, `ssh` logs you in with the key.

> **Warning:** Never share or copy `~/.ssh/id_ed25519` (the file without `.pub`). Anyone who has it can log in as you everywhere you've installed the padlock. `ssh-keygen` makes it `600` for you; keep it that way.

To save typing, name your servers in `~/.ssh/config`:

```text
Host web
    HostName 203.0.113.10
    User ada
```

Now `ssh web` is enough.

## Copying Files Between Machines

`scp` copies files over SSH, like `cp` with a remote path written `host:path`: `scp report.csv web:/home/ada/`. For folders you copy again and again, use rsync, which sends only what changed. It works between local folders too:

```bash
rsync -av notes/ backup/notes/
```

It lists each file it copies. Add a file to `notes` and run the same command again, and only the new file is sent. The trailing `/` on `notes/` means "the contents of notes".

## Keeping Work Alive with tmux

If your connection drops, the shell on the server ends, and so does anything running in its foreground. `tmux` runs sessions on the server that keep going while you're away. Start one with `tmux new -s work`, run your long job, then press Ctrl-B followed by D to detach. Later, from a new login, `tmux attach -t work` puts you back exactly where you were. Install it with `apt install tmux` or `brew install tmux`.

## Lab: Your Toolbox

Work in `~/sandbox`. None of these steps needs a server.

1. Install jq and shellcheck with your package manager if you haven't: `sudo apt install jq shellcheck` or `brew install jq shellcheck`. **Expected:** `jq --version` prints a version such as `jq-1.8.2`.
2. Create and activate a virtual environment: `python3 -m venv .venv` then `source .venv/bin/activate`. **Expected:** your prompt starts with `(.venv)`, and `which python` points inside `~/sandbox/.venv`.
3. Run `pip list`, then `deactivate`. **Expected:** only `pip` is listed, then `(.venv)` disappears.
4. Make a practice key pair: `ssh-keygen -t ed25519 -C "practice" -f ~/sandbox/practice_key`. **Expected:** two files, `practice_key` (mode `-rw-------`) and `practice_key.pub`. Check with `ls -l practice_key*`.
5. Read the public half: `cat practice_key.pub`. **Expected:** one line starting with `ssh-ed25519`. Delete both files when you're done.
6. Sync a folder twice: `mkdir -p notes`, `echo a > notes/monday.txt`, `rsync -av notes/ backup/notes/`; then `echo c > notes/wednesday.txt` and run the same `rsync` again. **Expected:** the second run copies only `wednesday.txt` (it may also list `./`, the folder itself).

## Summary, Key Terms, and Review Questions

### Summary

- Package managers install software and its dependencies from trusted sources: `apt`, `dnf`, Homebrew.
- A virtual environment gives each Python project its own packages; version managers install whole language versions.
- SSH opens an encrypted shell on another machine. Key pairs beat passwords: share the public key, guard the private key.
- `scp` copies files over SSH; `rsync` copies only what changed.
- `tmux` keeps sessions alive when your connection drops.

### Key Terms

| Term | Meaning |
|---|---|
| Package manager | A tool that installs, updates, and removes software |
| Virtual environment | A per-project folder with its own Python and packages |
| SSH | Secure Shell: an encrypted way to use another machine's shell |
| Key pair | A linked public and private key used to prove who you are |
| Public key | The half you share, installed on servers like a padlock |
| Private key | The secret half that stays on your machine |

### Review Questions

1. What's the difference between `apt update` and `apt upgrade`?
2. Why does each Python project deserve its own virtual environment?
3. In the padlock picture, which file do you give to a server, and which do you never share?
4. When would you choose `rsync` over `scp`?
5. You start a two-hour job over SSH and your Wi-Fi drops. How could `tmux` have saved it?

> **You understand this when** you can set up a project's Python environment, and explain how an SSH key lets you in without a password.
