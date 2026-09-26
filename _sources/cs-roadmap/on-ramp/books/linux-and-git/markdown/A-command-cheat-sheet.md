# Command Cheat Sheet

The commands from this book, grouped by job. Where Linux and macOS differ, both are shown.

## Files, Folders, and Text

| Command | What it does |
|---|---|
| `pwd`, `ls -la`, `cd dir` | Where am I; list everything; go into `dir` (`cd ..` up, `cd` home) |
| `mkdir -p a/b`, `touch f` | Make folders with parents; create an empty file |
| `cp a b`, `mv a b`, `rm f` | Copy, move or rename, remove (`-r` for folders; no undo) |
| `cat f`, `less f`, `head`/`tail -n 5 f` | Print, page through, first or last lines (`tail -f` follows) |
| `du -sh d`, `df -h` | Size of a folder; free space on each disk |
| `find . -name '*.py'` | Find files by name (also `-type`, `-mtime`, `-size`) |
| `grep -rn word .` | Search inside files, with line numbers (`-c`, `-i`, `-v`, `-E`) |
| `sed 's/a/b/g' f` | Print a changed copy; `-i` edits in place (macOS: `-i ''`) |
| `cut -d' ' -f5 \| sort \| uniq -c \| sort -rn` | Keep a column, then count and rank its values |
| `jq '.key' f.json` | Pull fields out of JSON; `jq .` pretty-prints |

## The Shell, Permissions, and Settings

| Command | What it does |
|---|---|
| `cmd > f`, `>> f`, `2> f`, `a \| b` | Output to a file; append; errors; feed `a` into `b` |
| `echo $PATH`, `which cmd` | Where commands are looked up; which one runs |
| `export NAME=value` | Pass a setting to programs (keep it in `~/.bashrc`) |
| `id`, `ls -l f` | Who you are; a file's owner and permissions |
| `chmod u+x f`, `chmod 600 f` | Let the owner run it; make it private (`644`, `755`) |
| `sudo cmd` | Run one command as root |

## Processes, Software, and Remote Work

| Command | What it does |
|---|---|
| `ps aux`, `pgrep -af name` | List processes; find one by name (macOS: `-fl`) |
| `cmd &`, `nohup cmd > log 2>&1 &` | Run in the background; outlive the terminal |
| `kill PID`, `kill -9 PID` | Ask to stop (SIGTERM); force stop (SIGKILL) |
| `crontab -e` | Schedule a job |
| `sudo apt install x`, `brew install x` | Install software (Debian/Ubuntu; macOS) |
| `python3 -m venv .venv` | Create a virtual environment |
| `ssh-keygen -t ed25519`, `ssh user@host` | Make a key pair; open a shell on another machine |
| `rsync -av src/ dst/`, `tmux new -s x` | Copy only what changed; a lasting session |

## Scripts

| Syntax | What it does |
|---|---|
| `#!/usr/bin/env bash`, `set -euo pipefail` | Run with bash; stop at the first error |
| `"$name"`, `$(cmd)`, `${1:-default}` | A quoted variable; a command's output; an argument |
| `if [[ -f "$f" ]]`, `for f in *.md` | Test and branch; repeat for each item |
| `exit 1`, `>&2`, `shellcheck s.sh` | Fail with a code; write to stderr; check for bugs |
