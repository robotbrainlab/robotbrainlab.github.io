# Files, Folders, and Who May Touch Them

This chapter gives you a map and a set of keys. The map is the single tree that every file on a Unix system hangs from, so you know where things live. The keys are users, groups, and permissions, so you know who may read, change, or run each file, and how to fix "Permission denied" without making things worse.

*The problem.* It says "Permission denied", and I don't know whose permission I need.

*The question.* Who decides what I'm allowed to do with a file, and how do I get permission the right way?

## One Tree from `/`

Windows gives each drive a letter: `C:`, `D:`. Unix doesn't. Everything hangs from one tree, and the top of that tree is the root directory, written `/`. Every disk, every USB stick, every device appears somewhere under it.

Programs follow a shared convention about where things go, so once you know the map, you can guess where to look:

| Path | What lives there |
|---|---|
| `/home/ada` | Your home folder (on macOS, `/Users/ada`) |
| `/root` | The home folder of the administrator account |
| `/etc` | System-wide settings, as plain text files |
| `/bin`, `/usr/bin` | Programs: `ls`, `cat`, `python3` |
| `/usr/local/bin`, `/opt` | Programs you installed yourself |
| `/var/log` | Log files that programs write as they run |
| `/tmp` | Temporary files, often wiped at restart |
| `/dev` | Devices, shown as files |
| `/proc` | Live information from the kernel (Linux only) |

macOS adds its own folders (`/Applications`, `/Users`, `/Library`), and Homebrew installs programs under `/opt/homebrew` on Apple silicon Macs. The idea is the same.

## Hidden Files

A file whose name starts with a dot is a **hidden file**, often called a dotfile. Plain `ls` skips them. `ls -a` shows everything:

```bash
ls -a
```

```text
.  ..  .bash_logout  .bashrc  .profile  sandbox
```

Dotfiles are mostly settings. `.bashrc` configures bash each time it starts; `.zshrc` does the same for zsh. Later you'll meet `.ssh` (your keys), `.gitconfig`, and `.gitignore`. They're hidden to keep them out of your way, not to keep them secret.

## Users and Groups

Unix was built for many people sharing one machine, so every file and every running program belongs to someone. A user is an account: a name, a numeric UID (user ID), and a home folder. A group is a named set of users, handy for sharing files with a team.

```bash
whoami
id
```

```text
ada
uid=1000(ada) gid=1000(ada) groups=1000(ada)
```

Users are listed in the text file `/etc/passwd` (it holds no passwords, despite the name):

```bash
grep ada /etc/passwd
```

```text
ada:x:1000:1000::/home/ada:/bin/bash
```

The fields are separated by colons: name, a placeholder for the password, UID, group ID, a comment, home folder, and login shell.

One user is special. **root**, UID 0, is the superuser. The kernel skips permission checks for root, so root can read, change, or delete anything. That's exactly why you don't use it for everyday work.

## Reading Permissions

Every file has an owner (a user), a group, and a set of **permissions** saying who may do what. `ls -l` shows all three:

```text
-rwxr--r--  1  ada  ada  27  Sep 26 14:31  hello.sh
│└┬┘└┬┘└┬┘      │    │
│ │  │  │       │    └ group
│ │  │  │       └ owner
│ │  │  └ others: r-- (read only)
│ │  └ group:  r-- (read only)
│ └ owner:  rwx (read, write, run)
└ type: - file, d directory, l link
```

There are three permissions, given separately to three classes of people: the owner, members of the file's group, and everyone else. A dash means "not allowed".

| Letter | On a file | On a directory |
|---|---|---|
| `r` read | Read its contents | List what's inside |
| `w` write | Change its contents | Add, delete, or rename files inside |
| `x` execute | Run it as a program | Enter it with `cd` or reach files inside |

So `rwxr--r--` means: the owner can do everything; group members and others can only read.

## Changing Permissions with chmod

`chmod` (change mode) changes permissions. The readable form names who (`u` user/owner, `g` group, `o` others, `a` all), then `+` to add or `-` to remove, then the letters:

```bash
chmod u+x hello.sh
chmod go-r secret.txt
```

The first lets you run `hello.sh`. The second stops group members and others from reading `secret.txt`.

The short form uses numbers. Each permission has a value (read 4, write 2, execute 1), and you add them up for each class, in the order owner, group, others:

| Number | Letters | Common use |
|---|---|---|
| `600` | `rw-------` | Secrets: only you can read or write |
| `644` | `rw-r--r--` | Normal files: you write, everyone reads |
| `700` | `rwx------` | Private folders and personal scripts |
| `755` | `rwxr-xr-x` | Programs and shared folders |

```bash
chmod 600 secret.txt
ls -l secret.txt
```

```text
-rw------- 1 ada ada 15 Sep 26 14:31 secret.txt
```

To change who owns a file, use `chown`, as in `sudo chown ada:ada report.txt`. Giving files away is an administrator's job, so it needs `sudo`, which is explained below.

## Three Reasons for "Permission Denied"

Almost every "Permission denied" you'll meet has one of three causes.

*It isn't yours.* Files under `/etc` belong to root. You may read most of them, but not change them, and a few you may not even read:

```bash
ls -l /etc/shadow
cat /etc/shadow
```

```text
-rw-r----- 1 root shadow 524 Sep 26 14:31 /etc/shadow
cat: /etc/shadow: Permission denied
```

*It isn't executable.* A new file never has the `x` permission. To run a script as a program, you must add it:

```bash
./hello.sh
chmod u+x hello.sh
./hello.sh
```

```text
bash: ./hello.sh: Permission denied
Hello from a script
```

*You can't get through the folder.* To reach a file, you need `x` on every folder along its path. Here, a second user, `ben`, tries to look into Ada's home folder, which is `drwx------`:

```text
ls: cannot open directory '/home/ada': Permission denied
```

Each time, `ls -l` on the file and its folders shows you which rule said no.

## sudo: Borrowing Root for One Command

Sometimes you really do need to change a system file or install software for the whole machine. For that, you use **sudo** ("superuser do"). It runs one command as root, after asking for *your* password, and records that you did it.

```bash
sudo apt install tree
```

```text
[sudo] password for ada:
```

Type your password (nothing appears as you type) and press Enter. On macOS the prompt is just `Password:`. Only users an administrator has allowed may use `sudo`; on your own laptop, that's you.

> **Warning:** `sudo` switches off every safety check. Use it only when a command must change the system. Never use it to fix "Permission denied" on files in your own home folder; that usually means something was created with `sudo` earlier and now belongs to root. And never "fix" errors with `chmod 777`, which lets every user and every program change the file.

## Least Privilege

The rule behind all of this is **least privilege**: give each person and each program exactly the access it needs, and no more. Your notes don't need to be readable by others, so make them `600`. A script needs `x` only for you, so use `u+x`, not `777`. A web app needs to read its code and write its data folder; it doesn't need root.

Least privilege limits the damage when something goes wrong. A buggy script running as you can hurt your files. The same script running as root can wreck the whole machine.

## Lab: Lock It Down

Make a fresh folder for this lab and work there: `mkdir -p ~/sandbox/ch3`, then `cd ~/sandbox/ch3`.

1. List your home folder with hidden files: `ls -a ~`. **Expected:** entries starting with a dot, such as `.bashrc` (Linux) or `.zshrc` (macOS).
2. Check who you are: `id`. **Expected:** your name, your UID, and your groups. On macOS your UID is usually `501` and your groups include `staff` and `admin`.
3. Create a secret: `echo "API_KEY=abc123" > secret.txt`, then `ls -l secret.txt`. **Expected:** `-rw-r--r--`, readable by everyone.
4. Lock it: `chmod 600 secret.txt`, then `ls -l secret.txt`. **Expected:** `-rw-------`.
5. Make a script: `echo 'echo "Hello from a script"' > hello.sh`, then run `./hello.sh`. **Expected:** `Permission denied`.
6. Make it runnable: `chmod u+x hello.sh`, then `./hello.sh`. **Expected:** `Hello from a script`, and `ls -l hello.sh` shows `-rwxr--r--`.
7. Block a folder: `mkdir box`, `chmod u-x box`, then `cd box`. **Expected:** a "Permission denied" error (bash and zsh word it slightly differently). Restore it with `chmod u+x box`.
8. Try a system file: `touch /etc/myapp.conf`. **Expected:** `Permission denied`. Don't fix it; it's supposed to fail.

## Summary, Key Terms, and Review Questions

### Summary

- Everything hangs from one tree rooted at `/`; settings live in `/etc`, programs in `/usr/bin`, logs in `/var/log`, your files in your home folder.
- Names starting with a dot are hidden; `ls -a` shows them.
- Every file has an owner, a group, and `rwx` permissions for owner, group, and others. On folders, `x` means "may enter".
- `chmod` changes permissions, in letters (`u+x`) or numbers (`600`, `644`, `755`).
- "Permission denied" means it isn't yours, it isn't executable, or a folder on the way is closed.
- `sudo` runs one command as root. Use it rarely, and follow least privilege.

### Key Terms

| Term | Meaning |
|---|---|
| Hidden file (dotfile) | A file whose name starts with `.`, usually settings |
| root | The superuser (UID 0), who bypasses permission checks |
| Permissions | The `rwx` rules for owner, group, and others |
| sudo | Runs one command as root after checking your password |
| Least privilege | Give each user or program only the access it needs |

### Review Questions

1. Where would you look for a program's system-wide settings? For its log files?
2. Read `-rw-r-----` aloud: who can do what?
3. What number would you give `chmod` for a file only you may read and write? For a script everyone may run?
4. Why do you need `x` on a folder to open a file inside it?
5. Why is "just use `sudo`" a poor fix for a permission error in your own home folder?

> **You understand this when** you can look at any "Permission denied", run `ls -l` on the file and its folders, and say which rule refused you.
