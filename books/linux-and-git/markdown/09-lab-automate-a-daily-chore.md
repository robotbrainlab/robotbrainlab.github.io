# Lab: Automate a Daily Chore

In this lab you turn five commands you'd type every morning into a shell script you can trust to run on its own. Along the way you meet everything a beginner needs for scripting: the shebang, a safety line that stops a script at the first error, variables and quoting, conditions, loops, arguments, exit codes, a checker that finds bugs for you, and a schedule.

*The problem.* I type the same five commands every morning.

*The question.* How do I turn commands I type into a script I can trust to run by itself?

The finished script is in `labs/ch09/morning.sh`. Type it yourself as you go, and use the copy only to check your work.

## Step 1: Do the Chore by Hand

Ada keeps plain-text notes in a `notes` folder, one file per day. Every morning she creates today's note, backs up the folder to a `backups` folder, deletes backups older than a week, and checks how much she has written. Set up the same folders inside your sandbox, so nothing touches your real files:

```bash
mkdir -p ~/sandbox/notes ~/sandbox/backups
printf '# Ideas\nLearn Git branches.\nTry tmux.\n' > ~/sandbox/notes/ideas.md
```

Now the five commands. `$(date +%F)` is replaced by today's date, such as `2026-09-26`; this is called command substitution:

```bash
cd ~/sandbox/notes
echo "# Notes for $(date +%F)" > "$(date +%F).md"
tar -czf ~/sandbox/backups/notes-$(date +%F).tar.gz .
find ~/sandbox/backups -name 'notes-*.tar.gz' -mtime +7 -delete
wc -w *.md
```

```text
 4 2026-09-26.md
 7 ideas.md
11 total
```

`tar -czf` packs the folder into one compressed file, and `find ... -mtime +7 -delete` removes backups more than seven days old.

**Expected:** a new note named after today's date, and a backup in `~/sandbox/backups`. Check with `ls ~/sandbox/backups`.

## Step 2: Put the Commands in a File

A **script** is just commands saved in a file. Create `~/sandbox/morning.sh` in your editor with the same five lines, plus one line at the top:

```bash
#!/usr/bin/env bash
cd ~/sandbox/notes
echo "# Notes for $(date +%F)" > "$(date +%F).md"
tar -czf ~/sandbox/backups/notes-$(date +%F).tar.gz .
find ~/sandbox/backups -name 'notes-*.tar.gz' -mtime +7 -delete
wc -w *.md
```

The first line is the **shebang**. `#!` tells the kernel which program should run this file; `/usr/bin/env bash` means "whichever bash is first on my PATH". Now make it executable and run it, as in Chapter 3:

```bash
cd ~/sandbox
chmod +x morning.sh
./morning.sh
```

**Expected:** the same word counts as Step 1. The `./` matters: your sandbox isn't on your PATH, so you must say where the script is.

## Step 3: Watch It Fail Badly

Scripts run without you watching, so ask: what if something goes wrong? Rename the notes folder, then run the script from an empty folder so the damage stays small:

```bash
mv ~/sandbox/notes ~/sandbox/notes-old
mkdir -p ~/sandbox/empty
cd ~/sandbox/empty
~/sandbox/morning.sh
echo $?
```

```text
/home/ada/sandbox/morning.sh: line 2: cd: /home/ada/sandbox/notes: No such file or directory
4 2026-09-26.md
0
```

The `cd` failed, and the script carried on regardless. It created a stray note in the empty folder, backed up that folder instead of your notes, and then reported success. Run from your home folder, it would have backed up your entire home folder. `$?` holds the **exit code** of the last command: `0` means success, anything else means failure. Every command sets one, and so does every script.

Clean up the damage: `rm ~/sandbox/empty/*.md ~/sandbox/backups/notes-$(date +%F).tar.gz`. Leave the notes folder renamed for Step 4.

## Step 4: Add the Safety Line

Add this as the second line of the script, right after the shebang:

```bash
set -euo pipefail
```

This is often called **strict mode**. `-e` stops the script at the first failing command. `-u` treats a misspelled or unset variable as an error instead of silently using an empty string. `-o pipefail` makes a pipeline fail if any stage fails, not just the last one. Repeat Step 3's experiment:

```text
/home/ada/sandbox/morning.sh: line 3: cd: /home/ada/sandbox/notes: No such file or directory
1
```

**Expected:** the script stops at `cd`, touches nothing, and returns `1`. Put the notes folder back before continuing: `cd ~/sandbox`, then `mv notes-old notes`.

> **Tip:** Start every bash script with `set -euo pipefail`. It turns silent disasters into loud, early stops.

## Step 5: Use Variables, and Quote Them

Repeating `~/sandbox/notes` and `$(date +%F)` is fragile. Store them in a **variable** instead: a name that holds a value. Write it with no spaces around `=`, and read it back with `$`:

```bash
notes_dir="$HOME/sandbox/notes"
today="$(date +%F)"
note="$notes_dir/$today.md"
```

Now quoting. Always put double quotes around a variable when you use it. Here's why. Suppose the folder were called `my notes`:

```bash
notes_dir="$HOME/sandbox/my notes"
ls $notes_dir
```

```text
ls: cannot access '/home/ada/sandbox/my': No such file or directory
notes:
2026-09-26.md  ideas.md
```

Without quotes, the shell split the value at the space into two arguments, `/home/ada/sandbox/my` and `notes`. The first didn't exist. The second happened to match a different folder (you ran this from `~/sandbox`), which `ls` listed as if nothing were wrong. With `rm` instead of `ls`, that's how scripts delete the wrong files. Written as `ls "$notes_dir"`, the value stays one argument.

Double quotes still expand variables; single quotes don't. `echo "$HOME"` prints your home folder; `echo '$HOME'` prints `$HOME`. And `-u` catches typos. Here a tiny script, run with `bash -c`, misspells `notes_dir`:

```bash
bash -c 'set -u; notes_dir=~/sandbox/notes; ls "$note_dir"'
```

```text
bash: line 1: note_dir: unbound variable
```

## Step 6: Make Decisions with if

Running the script twice would overwrite today's note. A script that's safe to run again and again, leaving the same result, is **idempotent**, and scheduled scripts should always be. An `if` statement makes it so:

```bash
if [[ -f "$note" ]]; then
  echo "Today's note already exists"
else
  echo "# Notes for $today" > "$note"
  echo "Created $note"
fi
```

`[[ ... ]]` is a test. Common ones:

| Test | True when |
|---|---|
| `-f "$x"` | `$x` is an existing file |
| `-d "$x"` | `$x` is an existing folder |
| `-z "$x"` | `$x` is empty |
| `"$a" == "$b"` | The two strings are equal |
| `! ...` | The test after it is false |

Spaces inside the brackets are required: `[[-f "$note"]]` is an error.

## Step 7: Repeat with a Loop

Replace `wc -w *.md` with a `for` loop that reports each note on its own line. The loop runs its body once per matching file, with `file` holding each name in turn:

```bash
for file in "$notes_dir"/*.md; do
  echo "$(wc -w < "$file") words in $(basename "$file")"
done
```

`basename` strips the folder from a path, leaving just the file name.

## Step 8: Accept an Argument and Fail Clearly

A script can take [**arguments**]{idx="argument"} just like a command. Inside, the first is `$1`, the second `$2`. `${1:-$HOME/sandbox/notes}` means "the first argument, or `~/sandbox/notes` if none was given". If the folder is missing, the script should say so on stderr (`>&2`) and exit with a non-zero code, so whatever runs it knows it failed. Here is the finished script:

```bash
#!/usr/bin/env bash
# morning.sh: start the day. Make today's note, back up all notes,
# and delete backups older than a week.
set -euo pipefail

notes_dir="${1:-$HOME/sandbox/notes}"
backup_dir="$HOME/sandbox/backups"
today="$(date +%F)"
note="$notes_dir/$today.md"

if [[ ! -d "$notes_dir" ]]; then
  echo "morning: no notes folder at $notes_dir" >&2
  exit 1
fi

if [[ -f "$note" ]]; then
  echo "Today's note already exists"
else
  echo "# Notes for $today" > "$note"
  echo "Created $note"
fi

mkdir -p "$backup_dir"
archive="$backup_dir/notes-$today.tar.gz"
tar -czf "$archive" -C "$notes_dir" .
echo "Backed up to $archive"

find "$backup_dir" -name 'notes-*.tar.gz' -mtime +7 -print -delete

for file in "$notes_dir"/*.md; do
  echo "$(wc -w < "$file") words in $(basename "$file")"
done
```

`tar -C "$notes_dir"` means "change into that folder first", so the script no longer needs `cd` at all. `-print` makes `find` name each backup it deletes. Run it twice:

```text
Created /home/ada/sandbox/notes/2026-09-26.md
Backed up to /home/ada/sandbox/backups/notes-2026-09-26.tar.gz
4 words in 2026-09-26.md
7 words in ideas.md
Today's note already exists
Backed up to /home/ada/sandbox/backups/notes-2026-09-26.tar.gz
4 words in 2026-09-26.md
7 words in ideas.md
```

The first run created the note; the second changed nothing it shouldn't. Once you have backups more than a week old, their paths appear after the "Backed up" line as they're deleted. (On macOS, `wc` pads the numbers with spaces.) Now give it a folder that doesn't exist:

```bash
./morning.sh /nope
echo $?
```

```text
morning: no notes folder at /nope
1
```

Exit codes let you chain commands: `a && b` runs `b` only if `a` succeeded, and `a || b` runs `b` only if `a` failed. So `./morning.sh || echo "morning failed"` prints a warning when something goes wrong.

## Step 9: Let shellcheck Review It

`shellcheck` reads a script and points out common bugs, especially missing quotes. Run it on the first version from Step 2:

```bash
shellcheck morning.sh
```

```text
In morning.sh line 2:
cd ~/sandbox/notes
^----------------^ SC2164 (warning): Use 'cd ... || exit' or 'cd ... || return' in case cd fails.
…
In morning.sh line 4:
tar -czf ~/sandbox/backups/notes-$(date +%F).tar.gz .
                                 ^---------^ SC2046 (warning): Quote this to prevent word splitting.
```

It found exactly the two problems you fixed by hand: the unchecked `cd` and the unquoted substitution. On the finished script it prints nothing, which, as always, means success. Run shellcheck on every script you write. To see each command as it runs, use `bash -x morning.sh`.

## Step 10: Schedule It

Finally, let the computer remember. Open your crontab with `crontab -e` and add one line (Chapter 6 explains the five time fields):

```text
0 7 * * 1-5 /home/ada/sandbox/morning.sh >> /home/ada/sandbox/morning.log 2>&1
```

At 07:00 every weekday, cron runs the script and appends everything it prints, including errors, to `morning.log`. Use full paths: cron doesn't read your shell's startup files. Check the log the next morning.

> **Note:** On macOS, cron works but may need permission to reach your files (System Settings, Privacy & Security, Full Disk Access). macOS's own scheduler is launchd. On WSL, cron runs only while WSL itself is running. Remove the line with `crontab -e` when you're done with this lab.

## Summary, Key Terms, and Review Questions

### Summary

- A script is commands in a file. The shebang picks the interpreter; `chmod +x` makes it runnable.
- `set -euo pipefail` stops a script at the first error, unset variable, or failed pipeline stage.
- Store values in variables, and always double-quote them when you use them.
- `if [[ ... ]]` makes decisions; `for` repeats work; `$1` reads arguments.
- Every command returns an exit code: `0` for success. `exit 1` and `>&2` report failure properly.
- Scheduled scripts should be idempotent. shellcheck catches bugs before they bite, and cron runs the script on time.

### Key Terms

| Term | Meaning |
|---|---|
| Script | A file of commands the shell runs in order |
| Shebang | The `#!` first line naming the program that runs a script |
| Exit code | A number every command returns: `0` success, non-zero failure |
| Strict mode | `set -euo pipefail`: stop on errors, unset variables, and failed pipes |
| Variable | A name that holds a value, read with `$name` |
| Idempotent | Safe to run many times with the same result |
| Argument | A value passed to a script, read as `$1`, `$2`, … |

### Review Questions

1. What does the shebang line do, and why `/usr/bin/env bash` rather than a fixed path?
2. In Step 3, the script "succeeded" while doing damage. Which part of strict mode prevents that?
3. Why does `ls $dir` misbehave when `dir` contains a space, and what's the fix?
4. What makes a script idempotent, and why does that matter for scheduled jobs?
5. What does `./morning.sh || echo "failed"` print when the script succeeds? When it fails?

> **You understand this when** you can take any sequence of commands you type often and turn it into a strict, quoted, idempotent script that shellcheck approves of.
