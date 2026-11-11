"""Print a heartbeat every two seconds until asked to stop."""
import signal
import time
from datetime import datetime

running = True


def stop(signum, frame):
    global running
    print(f"got signal {signum}, finishing up", flush=True)
    running = False


signal.signal(signal.SIGTERM, stop)

beat = 0
while running:
    beat += 1
    print(f"{datetime.now():%H:%M:%S} beat {beat}", flush=True)
    time.sleep(2)
print("saved my work, bye", flush=True)
