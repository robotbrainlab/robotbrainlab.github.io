# Docker in Practice

This chapter turns Chapter 2's ideas into skills: write a Dockerfile for a small Python web app, build and run it, reach it through a port, keep its data in a volume, pass it configuration, make the image smaller and safer, and run it next to a database with Docker Compose.

*The problem.* I understand containers, but I've never built one.

*The question.* How do I describe my app to Docker, build it into an image, and run it the way a server would?

## Meet tinyapp

The labs from here on use one very small web app, called tinyapp. It is written with FastAPI and has two addresses: `/health` says the app is alive and which version it is, and `/visits` counts visitors. It stores the count in a file, or in PostgreSQL when it is given a database address. Here is `main.py`:

```python
"""tinyapp: a very small web app for the labs in this book."""
import os
from pathlib import Path

from fastapi import FastAPI

VERSION = os.environ.get("APP_VERSION", "dev")
DATABASE_URL = os.environ.get("DATABASE_URL", "")
DATA_FILE = Path(os.environ.get("DATA_DIR", "/tmp")) / "visits.txt"

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok", "version": VERSION}


@app.get("/visits")
def visits():
    return {"visits": count_visit()}


def count_visit() -> int:
    if DATABASE_URL:
        return count_visit_in_postgres()
    count = int(DATA_FILE.read_text()) if DATA_FILE.exists() else 0
    DATA_FILE.write_text(str(count + 1))
    return count + 1
```

The file ends with `count_visit_in_postgres()`, a few lines that do the same count in a database table. Notice that every setting comes from an **environment variable**: a named value that the operating system hands to a process when it starts. `os.environ.get("APP_VERSION", "dev")` reads one, with a default. That is how one image can get a different configuration in each environment.

The app's libraries are listed in `requirements.txt`:

```text
fastapi==0.141.1
uvicorn==0.54.0
psycopg[binary]==3.3.6
```

Uvicorn is the web server that runs a FastAPI app. Make a fresh folder, `~/infra-labs/ch05`, and copy into it `main.py`, `test_main.py`, and both requirements files from the book's `labs/tinyapp/` folder. The tests are for Chapter 6.

## The Dockerfile

A **Dockerfile** is the recipe for an image: a text file of instructions that Docker follows from top to bottom, each one adding a layer. Create `Dockerfile` in the `ch05` folder:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

RUN useradd --create-home appuser && mkdir /data && chown appuser /data
USER appuser
ENV DATA_DIR=/data

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

| Instruction | What it does here |
|---|---|
| `FROM` | Starts from the base image `python:3.12-slim`: Debian plus Python |
| `WORKDIR` | Makes `/app` the current folder for the following steps |
| `COPY` | Copies files from your folder into the image |
| `RUN` | Runs a command at build time, here `pip install` and creating a user |
| `USER` | Runs the app as `appuser` instead of the all-powerful root user |
| `ENV` | Sets an environment variable baked into the image |
| `EXPOSE` | Documents that the app listens on port 8000 |
| `CMD` | The command that runs when a container starts |

Two details matter. `requirements.txt` is copied and installed *before* `main.py`, which makes rebuilds fast (see below). And `--host 0.0.0.0` makes Uvicorn listen on all of the container's network interfaces. The default, `127.0.0.1`, means `localhost` only, and inside a container `localhost` is the container itself, so nothing outside could reach the app.

Next to it, create `.dockerignore`, the list of files never to send to Docker:

```text
.git
.venv
__pycache__
.pytest_cache
.env
*.tar
```

## Building and the Cache

`docker build -t tinyapp:1.0 .` builds the image and names it `tinyapp:1.0`. The final `.` is the build context: the folder whose files `COPY` can see. Docker runs each instruction and saves a layer. When you rebuild, it reuses a layer from its build cache if the instruction and its input files haven't changed, and it rebuilds everything after the first change.

That is why the order matters. Your code changes all the time; your requirements rarely do. With requirements first, editing `main.py` rebuilds only the last few cheap layers, and the slow `pip install` step says `CACHED`. Put `COPY . .` first and every one-line change reinstalls every library.

## Running, Ports, and Logs

`docker run -d --name tinyapp -p 8080:8000 tinyapp:1.0` starts a container. `-d` runs it detached, in the background. `--name` gives it a name to use in other commands. `-p 8080:8000` is a port mapping: connections to port 8080 on your machine are forwarded to port 8000 inside the container.

```text
   your machine                    container "tinyapp"
  ┌──────────────────────┐        ┌─────────────────────────┐
  │ curl localhost:8080  │──────► │ port 8000: uvicorn      │
  └──────────────────────┘        └─────────────────────────┘
           -p 8080:8000 forwards 8080 to 8000
```

A few commands you will use every day: `docker ps` lists running containers, `docker logs tinyapp` shows what the app printed, `docker exec tinyapp whoami` runs a command inside it, and `docker rm -f tinyapp` stops and removes it.

## Volumes: Data That Survives

A container's own files vanish when it is removed, and the visit count lives in a file. A **volume** is storage that Docker manages outside any container, which you attach to a folder inside one. Replace the container, attach the same volume, and the data is still there. It's like parking the food truck but keeping the pantry in a warehouse.

`docker volume create tinyapp-data` creates one, and `-v tinyapp-data:/data` attaches it at `/data`, where the app writes its file. A bind mount is the other kind: `-v "$PWD":/work` attaches a folder from your own machine, which is handy in development, as in Chapter 1.

## Configuration and Secrets

Pass configuration when the container starts, never when the image is built. `-e APP_VERSION=1.0` sets one environment variable; `--env-file .env` reads many from a file. The same image then runs in every environment with different settings.

A **secret** is configuration that must stay private: passwords, API keys, tokens. Secrets need extra care.

> **Warning:** Never put a secret in a Dockerfile, with `ENV` or by copying a file. Anyone who can pull the image can read every layer, and `docker history` prints `ENV` values in plain text. Pass secrets at run time, keep `.env` files out of git and out of the image (that is why `.env` is in `.dockerignore`), and in production use your platform's secret store.

## Smaller and Safer Images

Every megabyte is downloaded on every deploy, and every extra program is something an attacker might use. Some habits give you most of the benefit:

- *Start slim.* The full `python:3.12` image uses 1.62 GB of disk; `python:3.12-slim` uses 205 MB. Slim leaves out compilers and tools most apps never need.
- *Don't keep caches.* `pip install --no-cache-dir` stops pip saving downloads inside the image.
- *Ignore what you don't need.* `.dockerignore` keeps `.git`, virtual environments, and secrets out.
- *Don't run as root.* If an attacker breaks into your app, they get only what `appuser` can do.
- *Pin versions.* `python:3.12-slim` and `fastapi==0.141.1` rebuild the same way next month.

Larger projects also use multi-stage builds, where one stage compiles things and a second, clean stage receives only the results. tinyapp doesn't need one.

## Compose: Several Containers Together

Real apps rarely run alone. tinyapp can use PostgreSQL, which would mean a network, a volume, a database container with the right settings, and the app container, started in the right order. Docker Compose lets you describe all of that in one file, `compose.yaml`, and start it with one command:

```yaml
name: tinyapp

services:
  app:
    build: .
    ports:
      - "8080:8000"
    environment:
      APP_VERSION: "1.0"
      DATABASE_URL: postgresql://tinyapp:${DB_PASSWORD}@db:5432/tinyapp
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: tinyapp
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: tinyapp
    volumes:
      - db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "tinyapp"]
      interval: 2s
      retries: 10

volumes:
  db-data:
```

`name` is the project's name, which Compose puts in front of everything it creates. Each entry under `services` becomes a container. Compose puts them on a private network where each one can reach the others by service name, which is why the app connects to host `db`. `depends_on` with `service_healthy` waits until PostgreSQL answers before starting the app. `${DB_PASSWORD}` is filled in from a file called `.env` in the same folder, so the password is not written in `compose.yaml`.

## Lab: Build, Run, and Compose

1. In `~/infra-labs/ch05`, with `Dockerfile` and `.dockerignore` created as above, build the image. Docker draws a live progress display in the terminal; the steps are the same as these lines:

   ```bash
   docker build -t tinyapp:1.0 .
   ```

   ```text
   #4 [1/6] FROM docker.io/library/python:3.12-slim@sha256:f77ac9e4…
   …
   #7 [3/6] COPY requirements.txt .
   #8 [4/6] RUN pip install --no-cache-dir -r requirements.txt
   #8 DONE 4.7s
   #9 [5/6] COPY main.py .
   #10 [6/6] RUN useradd --create-home appuser && mkdir /data && chown…
   …
   #11 naming to docker.io/library/tinyapp:1.0 done
   ```

2. Add a comment line to the end of `main.py` and build again as `tinyapp:1.1`. The install step is now `#8 CACHED`, and only steps 5 and 6 run. Remove the comment afterwards.

3. Run the app and call it:

   ```bash
   docker run -d --name tinyapp -p 8080:8000 tinyapp:1.0
   curl localhost:8080/health
   curl localhost:8080/visits
   curl localhost:8080/visits
   docker exec tinyapp whoami
   ```

   ```text
   {"status":"ok","version":"dev"}
   {"visits":1}
   {"visits":2}
   appuser
   ```

   `docker run` also prints the container's long ID; from here on such lines are left out. `curl` doesn't end with a new line, so your prompt may appear right after the JSON.

4. Replace the container and call `/visits` again:

   ```bash
   docker rm -f tinyapp
   docker run -d --name tinyapp -p 8080:8000 tinyapp:1.0
   curl localhost:8080/visits
   ```

   ```text
   {"visits":1}
   ```

   The count was lost with the old container.

5. Now use a volume. Call `/visits` three times, replace the container, and call it once more:

   ```bash
   docker rm -f tinyapp
   docker volume create tinyapp-data
   docker run -d --name tinyapp -p 8080:8000 -v tinyapp-data:/data tinyapp:1.0
   curl localhost:8080/visits
   curl localhost:8080/visits
   curl localhost:8080/visits
   docker rm -f tinyapp
   docker run -d --name tinyapp -p 8080:8000 -v tinyapp-data:/data tinyapp:1.0
   curl localhost:8080/visits
   ```

   ```text
   {"visits":1}
   {"visits":2}
   {"visits":3}
   {"visits":4}
   ```

6. Pass configuration at run time:

   ```bash
   docker rm -f tinyapp
   docker run -d --name tinyapp -p 8080:8000 -e APP_VERSION=1.0 tinyapp:1.0
   curl localhost:8080/health
   ```

   ```text
   {"status":"ok","version":"1.0"}
   ```

7. Remove it, then start the app with PostgreSQL. Create `.env` containing `DB_PASSWORD=change-me-locally`, save `compose.yaml` as shown, and run:

   ```bash
   docker rm -f tinyapp
   docker compose up -d
   ```

   ```text
   …
    Network tinyapp_default Created
   …
    Volume tinyapp_db-data Created
   …
    Container tinyapp-db-1 Started
    Container tinyapp-db-1 Healthy
    Container tinyapp-app-1 Started
   ```

   (Before these lines, Compose builds the image.) Wait two seconds for the app to start, then call `/visits` twice: you get 1, then 2.

8. Stop everything and start it again. The containers and network are removed, but the database volume stays:

   ```bash
   docker compose down
   docker compose up -d
   curl localhost:8080/visits
   ```

   ```text
   {"visits":3}
   ```

9. Clean up. `-v` also deletes the database volume:

   ```bash
   docker compose down -v
   docker volume rm tinyapp-data
   ```

**Expected results:** the second build reuses the cached install layer; the app runs as `appuser`; the count resets when the container is replaced without a volume and survives with one; `APP_VERSION` changes without rebuilding; and with Compose the count lives in PostgreSQL and survives `down` and `up`.

## Summary, Key Terms, and Review Questions

### Summary

- A Dockerfile is an image's recipe. Each instruction adds a layer; copy requirements before code so rebuilds are fast.
- `docker run -d -p 8080:8000` runs a container in the background and forwards a port. Apps in containers must listen on `0.0.0.0`.
- Volumes keep data when containers are replaced.
- Configuration arrives as environment variables at run time. Secrets never go into images.
- Slim bases, no caches, `.dockerignore`, a non-root user, and pinned versions make images smaller and safer.
- Docker Compose describes several containers, their network, and their volumes in one file.

### Key Terms

| Term | Meaning |
|---|---|
| Environment variable | A named value given to a process when it starts |
| Dockerfile | The text recipe Docker follows to build an image |
| Volume | Docker-managed storage that outlives containers |
| Secret | Private configuration such as a password or key |

### Review Questions

1. Why does the Dockerfile copy `requirements.txt` before `main.py`?
2. What does `-p 8080:8000` do, and why must the app listen on `0.0.0.0`?
3. Why should a password never be set with `ENV` in a Dockerfile?
4. Name four habits that make an image smaller or safer.
5. How does the app container find the database in the Compose file?

> **You understand this when** you can write a Dockerfile for a small Python app from memory, run it with a port and a volume, and explain what survives when the container is replaced.
