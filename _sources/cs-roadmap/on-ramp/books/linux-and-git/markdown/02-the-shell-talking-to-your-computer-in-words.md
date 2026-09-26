# The Shell: Talking to Your Computer in Words

This chapter turns the shell from a mystery into a tool. You'll learn to read any command, move around, see how the shell finds programs, and join small commands into bigger ones. By the end, you'll predict what a command does before you press Enter.

*The problem.* I type a command and something happens, but I couldn't tell you what.

*The question.* What exactly happens between pressing Enter and seeing the result?

## The Shell's Loop

The shell does the same four things, forever:

1. It shows a prompt, the text before your cursor (often your name, the folder you're in, and a `$` or `%`).
2. It reads the line you type when you press Enter.
3. It finds the program you named and runs it, passing along the rest of the line.
4. It shows the program's output, then goes back to step 1.

The two shells you'll meet are bash, the default on most Linux systems, and zsh, the default on macOS. For everything in this book they behave the same way.

## The Parts of a Command

Every command line has the same shape: a command, then options, then arguments.

```text
  ls   -l   -a   /home/ada/sandbox
  │    └──┬──┘   └──────┬────────┘
  │       │             └─ argument: what to act on
  │       └─ options: how to do it
  └─ command: which program to run
```

- The command is the program to run. Here it's `ls`, which lists files.
- An **option** (also called a flag) changes how the command behaves. Short options are one letter after a dash (`-l`), and can be combined (`-la` means `-l -a`). Long options are words after two dashes (`--all`).
- An **argument** is the thing the command acts on, usually a file or folder. Most commands have a sensible default when you leave it out.

Spaces separate the parts. That's why file names with spaces cause trouble: `my notes.txt` looks like two arguments. Wrap such names in quotes: `"my notes.txt"`.

## Where You Are: Paths and the Working Directory

The shell always has a current folder, called the **working directory**. Commands act there unless you say otherwise. When you open a terminal, you start in your **home directory**, your personal folder: `/home/ada` on Linux, `/Users/ada` on macOS. The shell lets you write it as `~`.

A **path** is the address of a file or folder. An absolute path starts at the very top of the file system, `/`, and works from anywhere: `/home/ada/sandbox/todo.txt`. A relative path starts from where you are now: if you're in `/home/ada`, then `sandbox/todo.txt` means the same file. Two special names help: `.` means "this folder" and `..` means "the folder above".

Three commands do most of the moving around. `pwd` prints the working directory. `ls` lists what's in it. `cd` changes it.

```bash
pwd
mkdir -p sandbox/notes
cd sandbox
touch todo.txt ideas.txt
ls
```

```text
/home/ada
ideas.txt  notes  todo.txt
```

`mkdir -p` made the folder `sandbox` and, inside it, `notes` (the `-p` means "make parent folders too, and don't complain if they exist"). `touch` created two empty files. Now the long listing:

```bash
ls -l
```

```text
total 4
-rw-r--r-- 1 ada ada    0 Sep 26 14:27 ideas.txt
drwxr-xr-x 2 ada ada 4096 Sep 26 14:27 notes
-rw-r--r-- 1 ada ada    0 Sep 26 14:27 todo.txt
```

Each line shows permissions, owner, size in bytes, date, and name. A `d` at the start marks a directory. Chapter 3 reads the rest.

To move around, `cd notes` goes into a folder, `cd ..` climbs one level, and `cd` on its own always takes you home.

## Making, Copying, and Removing

A few more commands handle everyday file work:

| Command | What it does |
|---|---|
| `mkdir -p a/b` | Make folders, including parents |
| `touch f` | Create an empty file (or update its time) |
| `cp src dst` | Copy a file; `cp -r` copies a folder |
| `mv old new` | Move or rename |
| `rm f` | Remove a file; `rm -r` removes a folder |
| `cat f` | Print a whole file |

> **Warning:** `rm` does not use the bin or the Trash. The file is gone the moment you press Enter. Be especially careful with `rm -r`, and read the whole line before you press Enter.

## How the Shell Finds a Command

When you type `ls`, how does the shell know which program you mean? It looks in a list of folders stored in a setting called **PATH**. It checks them from left to right and runs the first program with that name.

```bash
echo $PATH
```

```text
/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
```

The folders are separated by colons. `which` tells you where a command was found:

```bash
which ls python3
```

```text
/usr/bin/ls
/usr/local/bin/python3
```

A few commands, like `cd`, aren't programs at all. They're a builtin, part of the shell itself:

```bash
type cd
```

```text
cd is a shell builtin
```

This explains the most common error in the terminal:

```text
bash: nosuchcmd: command not found
```

No folder on your PATH holds a program with that name. It's misspelled, not installed, or installed in a folder that isn't on your PATH.

## Streams, Redirection, and Pipes

Every program starts with three streams, like three hoses attached to it. **Standard input** (stdin) is where it reads from, usually your keyboard. **Standard output** (stdout) is where it writes results, usually your screen. **Standard error** (stderr) is a second output just for error messages, also your screen.

[**Redirection**]{idx="redirection"} points those hoses somewhere else. `>` sends stdout into a file, replacing what was there. `>>` adds to the end instead. `2>` sends stderr into a file.

```bash
cd ~/sandbox
echo "buy milk" > todo.txt
echo "call Sam" >> todo.txt
cat todo.txt
```

```text
buy milk
call Sam
```

Errors travel on their own hose, so you can separate them:

```bash
ls /nope
ls /nope 2> errors.txt
cat errors.txt
```

```text
ls: cannot access '/nope': No such file or directory
ls: cannot access '/nope': No such file or directory
```

The first `ls` printed its complaint on the screen. The second printed nothing, because its error went into `errors.txt`. On macOS the message reads `ls: /nope: No such file or directory`; the idea is the same.

A **pipe**, written `|`, connects one program's stdout to the next program's stdin. This is how small tools join forces. How many entries are in `/etc`? `ls` lists them, `wc -l` counts lines:

```bash
ls /etc | wc -l
```

```text
75
```

Read a pipeline left to right, like a sentence: "list `/etc`, then count the lines". Chapter 5 builds longer ones.

## Getting Help

You never need to memorise options. Every standard command has a manual page, or **man page**. Run `man ls` to read it; use the arrow keys or space to scroll, `/word` to search, and `q` to quit. Most GNU tools on Linux also print a short summary with `--help`:

```bash
ls --help | head -1
```

```text
Usage: ls [OPTION]... [FILE]...
```

macOS's `ls` doesn't understand `--help`; use `man ls` there.

> **Tip:** Press Tab while typing a name, and the shell completes it for you; press it twice to see the choices. It saves typing and, more importantly, typos.

A few more keys make life easier. The Up arrow brings back earlier commands. Ctrl-R searches your history as you type. Ctrl-C cancels whatever is running. Ctrl-L clears the screen.

## Lab: A Sandbox Tour

Work in a new terminal window. Each step says what you should see.

1. Make a fresh folder for this lab: `mkdir -p ~/sandbox/ch2/notes`, then `cd ~/sandbox/ch2`. **Expected:** `pwd` prints your home folder followed by `/sandbox/ch2`.
2. Create a file with two lines: `echo "first" > log.txt`, then `echo "second" >> log.txt`, then `cat log.txt`. **Expected:** `first` and `second` on two lines.
3. Replace instead of adding: `echo "only" > log.txt` and `cat log.txt`. **Expected:** just `only`. That's the difference between `>` and `>>`.
4. Copy and move: `cp log.txt notes/copy.txt`, then `mv notes/copy.txt notes/moved.txt`, then `ls notes`. **Expected:** `moved.txt`.
5. Separate an error: `ls /nope 2> err.txt`, then `cat err.txt`. **Expected:** nothing on screen from the first command; the error message from the second.
6. Count with a pipe: `ls ~/sandbox/ch2 | wc -l`. **Expected:** `3` (`err.txt`, `log.txt`, `notes`).
7. Find where Python lives: `which python3`. **Expected:** a path such as `/usr/bin/python3`.
8. Look up an option: run `man wc` and find what `-w` does. **Expected:** it counts words. Press `q` to leave.

## Summary, Key Terms, and Review Questions

### Summary

- The shell loops: prompt, read, run, show. bash and zsh work the same way for everyday use.
- A command line is a command, then options, then arguments, separated by spaces.
- The working directory is where commands act. Absolute paths start at `/`; relative paths start where you are.
- The shell finds programs by searching the folders on your PATH, left to right.
- Every program has stdin, stdout, and stderr. Redirection points them at files; pipes connect programs.
- `man` and `--help` explain any command.

### Key Terms

| Term | Meaning |
|---|---|
| Option | A setting that changes how a command behaves, like `-l` |
| Argument | What a command acts on, usually a file or folder |
| Working directory | The folder the shell is currently in |
| Home directory | Your personal folder, written `~` |
| Path | The address of a file or folder |
| PATH | The list of folders the shell searches for commands |
| Standard input, output, error | The three streams every program starts with |
| Redirection | Sending a stream to or from a file (`>`, `>>`, `2>`) |
| Pipe | The `|` symbol, which feeds one program's output into another |
| Man page | The built-in manual for a command |

### Review Questions

1. In `cp -r photos /home/ada/backup`, which part is the command, which the option, and which the arguments?
2. You're in `/home/ada/sandbox`. Write the absolute and relative paths to `notes/ideas.txt`.
3. What's the difference between `>` and `>>`? Which one can destroy data?
4. What does "command not found" tell you, and what are three possible causes?
5. What does `ls /etc | wc -l` do, step by step?

> **You understand this when** you can read a command like `ls -l ~/sandbox 2> err.txt | wc -l` aloud and say what each part does.
