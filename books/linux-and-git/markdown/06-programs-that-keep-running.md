# Programs That Keep Running

This chapter shows you running programs from the outside: how to list them, run them in the background, stop them politely or by force, and hand them to the system so they keep running after you leave. You'll also see where their logs go and how to run a job on a schedule.

*The problem.* My program stops the moment I close the terminal.

*The question.* How do I keep a program running, see what's running, and stop it cleanly?

## Processes: Programs in Motion

A program is a file on disk, like a recipe in a book. A **process** is that program running, like someone cooking the recipe. The same recipe can be cooked twice at once.

The kernel gives every process a number, its **PID** (process ID), and remembers who started it, its parent. Programs you run from the shell are the shell's children. That's why closing the terminal can end your program: when the terminal goes, the shell and its children are told to hang up.

The examples use a small Python program, `labs/ch06/heartbeat.py`, which prints a line such as `14:36:53 beat 2` every two seconds until it's asked to stop.

## Foreground and Background

Normally a program runs in the foreground, holding the terminal until it finishes. With `&` at the end, it runs in the background: the shell prints a job number and the PID, and gives you the prompt back:

```bash
python3 heartbeat.py > heartbeat.log &
jobs
```

```text
[1] 25
[1]+  Running                 python3 heartbeat.py > heartbeat.log &
```

Each background program started from this shell is a job. `jobs` lists them and `fg` brings one back to the foreground. `ps` lists your processes, and `pgrep` finds one by name (on macOS, use `pgrep -fl`):

```bash
ps
pgrep -af heartbeat
```

```text
  PID TTY          TIME CMD
   21 pts/0    00:00:00 bash
   25 pts/0    00:00:00 python3
   27 pts/0    00:00:00 ps
25 python3 heartbeat.py
```

`ps aux` lists every process on the machine, and `top` shows a live view (press `q` to quit).

Jobs still belong to your terminal. To let a program survive the terminal closing, start it with `nohup` ("no hang-up"):

```bash
nohup python3 heartbeat.py > heartbeat.log 2>&1 &
```

`2>&1` sends errors into the same file, since no screen will show them. The log's first line, `nohup: ignoring input`, is harmless.

## Signals: Asking a Process to Stop

You talk to a running process by sending it a **signal**, a small numbered message from the kernel. The ones you'll use:

| Signal | Number | Meaning |
|---|---|---|
| SIGINT | 2 | "Interrupt." Sent when you press Ctrl-C |
| SIGTERM | 15 | "Please finish up and stop." The polite default |
| SIGKILL | 9 | "Stop now." Cannot be caught or ignored |

Signals are sent with `kill`, a gloomy name for something usually polite. `kill 25` sends SIGTERM to PID 25; `kill %1` sends it to job 1. A well-written program catches SIGTERM, finishes what it was doing, saves its work, and exits. That's a graceful shutdown. `heartbeat.py` does it by registering a Python function to run when SIGTERM arrives:

```python
def stop(signum, frame):
    global running
    print(f"got signal {signum}, finishing up", flush=True)
    running = False

signal.signal(signal.SIGTERM, stop)
```

The main loop checks `running`, so it stops after the current beat. Send SIGTERM with `kill %1`, and a couple of seconds later the shell reports `[1]+ Done`, and the log ends with a goodbye:

```bash
tail -n 3 heartbeat.log
```

```text
14:36:55 beat 3
got signal 15, finishing up
saved my work, bye
```

`kill -9` sends SIGKILL instead. The kernel ends the process on the spot, the shell reports `Killed`, and the program gets no chance to save anything.

> **Warning:** Use `kill -9` only when a polite `kill` hasn't worked after a few seconds. A program killed mid-write can leave a half-written, corrupted file.

## Services: Programs the System Looks After

With `nohup`, nobody restarts a crashed program, and a reboot ends it. For programs that should always run, the system takes charge.

A **service** (or daemon) is a background program with no terminal, supervised by the **init system**: the first process the kernel starts at boot, PID 1. It starts services, restarts them if they crash, and collects their output. On most Linux systems it's systemd; on macOS it's launchd, controlled with `launchctl`.

With systemd, you describe a service in a small text file called a unit file. For a personal service, it goes in `~/.config/systemd/user/heartbeat.service`:

```ini
[Unit]
Description=Heartbeat demo

[Service]
ExecStart=/usr/bin/python3 /home/ada/sandbox/heartbeat.py
Restart=on-failure

[Install]
WantedBy=default.target
```

`ExecStart` is the command, `Restart=on-failure` restarts it after a crash, and `WantedBy` starts it automatically. You control it with `systemctl`:

```bash
systemctl --user daemon-reload
systemctl --user enable --now heartbeat
systemctl --user status heartbeat
```

```text
● heartbeat.service - Heartbeat demo
     Active: active (running) since Fri 2026-09-25 10:02:11 UTC
   Main PID: 2143 (python3)
…
```

`stop` sends SIGTERM, `restart` stops and starts it, and `disable` stops it starting automatically. System-wide services use `sudo` instead of `--user`.

> **Note:** systemd runs only on Linux, and not inside every WSL setup or container. On macOS, use `nohup` for this chapter's lab, and read this section for the idea.

## Logs: Where the Output Goes

A service has no screen, so its output goes into a **log**: a record of timestamped messages. systemd keeps every service's output in its journal, and `journalctl -f` follows it like `tail -f`:

```bash
journalctl --user -u heartbeat -f
```

Many programs write their own log files, traditionally under `/var/log`; read them with the tools from Chapter 5. On macOS, use the Console app.

## Scheduled Jobs with cron

Some work should run only at set times, like a nightly backup. **cron** is the classic scheduler on Linux and macOS. Each user has a crontab, a table of jobs, edited with `crontab -e` and listed with `crontab -l`. Each line has five time fields, then the command:

```text
  ┌──────── minute (0-59)
  │ ┌────── hour (0-23)
  │ │ ┌──── day of month (1-31)
  │ │ │ ┌── month (1-12)
  │ │ │ │ ┌ day of week (0-6, Sunday is 0)
  │ │ │ │ │
  0 7 * * 1-5  /home/ada/bin/morning.sh
```

A `*` means "every". This line runs `morning.sh` at 07:00, Monday to Friday.

cron runs jobs with a bare environment, without your PATH or `~/.bashrc`. Use full paths, and send output to a file (`>> /home/ada/morning.log 2>&1`), or you'll never see the errors. Chapter 9 schedules a real script.

## Lab: A Program That Outlives the Terminal

Copy `labs/ch06/heartbeat.py` into `~/sandbox` and `cd` there.

1. Run it in the foreground: `python3 heartbeat.py`. After a few beats, press Ctrl-C. **Expected:** beats every two seconds, then a traceback ending in `KeyboardInterrupt`. Ctrl-C sent SIGINT, which this program doesn't handle gracefully.
2. Start it in the background: `nohup python3 heartbeat.py > heartbeat.log 2>&1 &`. **Expected:** a job number and PID, such as `[1] 25`, and your prompt back.
3. Find it: `pgrep -af heartbeat` (macOS: `pgrep -fl heartbeat`). **Expected:** the same PID and the command.
4. Watch it with `tail -f heartbeat.log`, then press Ctrl-C. **Expected:** new beats appear; stopping `tail` doesn't stop the program.
5. Close the terminal window, open a new one, and run `pgrep -af heartbeat` again. **Expected:** it's still running, under the same PID.
6. Stop it gracefully: `kill <PID>`, wait a few seconds, then `tail -n 2 ~/sandbox/heartbeat.log`. **Expected:** `got signal 15, finishing up` and `saved my work, bye`.

## Summary, Key Terms, and Review Questions

### Summary

- A process is a running program with a PID and a parent. `ps`, `pgrep`, and `top` show them.
- `&` runs a command in the background; `jobs` and `fg` manage it. `nohup` lets it survive the terminal closing.
- Signals ask processes to act. SIGTERM asks politely; SIGKILL forces. Prefer graceful shutdown.
- Services are supervised by the init system (systemd on Linux, launchd on macOS), which starts, restarts, and logs them.
- Logs hold what background programs say. `journalctl` reads systemd's; `tail -f` follows a file.
- cron runs commands on a schedule, with a bare environment.

### Key Terms

| Term | Meaning |
|---|---|
| Process | A running instance of a program |
| PID | The number the kernel gives each process |
| Signal | A small numbered message sent to a process |
| Service | A background program supervised by the system |
| Init system | The first process (PID 1), which starts and supervises services |
| Log | A record of timestamped messages written by a program |
| cron | The classic scheduler for running commands at set times |

### Review Questions

1. What's the difference between a program and a process?
2. Why does a program started normally stop when you close its terminal? Name two ways to prevent that.
3. Why should you try `kill` before `kill -9`?
4. What does a service manager give you that `nohup` doesn't?
5. A cron job works when you run it by hand but fails from cron. What's the likely cause?

> **You understand this when** you can start a program in the background, find its PID, read its output, and stop it gracefully.
