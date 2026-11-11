# Lab: Ship a Small Python App in a Container

This whole chapter is a lab. You take tinyapp from source code to a versioned image that knows how to report its own health, watch a healthy and an unhealthy container side by side, publish the image to a registry, and run it from there on a machine that doesn't have it yet.

*The problem.* I have a working app and want it to run anywhere.

*The question.* What does it take to turn my app into one tested image that any machine can pull and run?

## What You'll Build

```text
 source ──► tests ──► docker build ──► tinyapp:1.0.0
                                           │
                                   docker run: healthy?
                                           │
                     docker push ──► localhost:5001 registry
                                           │
         "another machine" ◄── docker pull + docker run
```

Start in a fresh folder, `~/infra-labs/ch09`, holding the app's four files and Chapter 5's `Dockerfile` and `.dockerignore`, copied from the book's `labs/` folder. You also need the registry from Chapter 6: if it is stopped, `docker start registry` starts it again, and if you removed it, run `docker run -d --name registry -p 5001:5000 registry:2`. If a container called `tinyapp` is still running from an earlier chapter, remove it with `docker rm -f tinyapp`.

## Step 1: Test the App Before You Package It

An image is only as good as the code inside it, so run the tests first. In `~/infra-labs/ch09`:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
```

```text
..                                                                       [100%]
2 passed in 0.29s
```

`.venv` is listed in `.dockerignore`, so the virtual environment never ends up in the image.

## Step 2: Teach the Image to Report Its Health

A running process is not the same as a working app. The process can be alive while the app is stuck, misconfigured, or listening on the wrong port. A health check asks the app itself.

Docker supports this with the `HEALTHCHECK` instruction: a command that Docker runs inside the container every few seconds. If it succeeds (exit code 0), the container is healthy; after a few failures in a row, it is unhealthy. Add two lines to the Dockerfile, just before `CMD`:

```dockerfile
HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=2)"
```

| Option | Meaning |
|---|---|
| `--interval=5s` | Check every 5 seconds |
| `--timeout=3s` | A check that takes longer than 3 seconds counts as failed |
| `--start-period=5s` | Failures in the first 5 seconds don't count; the app is starting |
| `--retries=3` | Three failures in a row mark the container unhealthy |

The check uses Python's own `urllib`, because the slim image doesn't include `curl`. `urlopen` raises an error on a failed connection or an error status, which makes Python exit with code 1. Real services use longer intervals, such as 30 seconds; 5 seconds keeps the lab quick.

## Step 3: Build a Versioned Image

Give each release a version. A common scheme is **semantic versioning**. A version has three numbers, `MAJOR.MINOR.PATCH`: raise PATCH for bug fixes, MINOR for new features, and MAJOR for changes that break something for users. This is version `1.0.0`:

```bash
docker build -t tinyapp:1.0.0 .
```

```text
…
#7 [4/6] RUN pip install --no-cache-dir -r requirements.txt
…
#10 [6/6] RUN useradd --create-home appuser && mkdir /data && chown…
#11 naming to docker.io/library/tinyapp:1.0.0 done
```

## Step 4: Run It and Watch It Become Healthy

```bash
docker run -d --name tinyapp -p 8080:8000 -e APP_VERSION=1.0.0 tinyapp:1.0.0
docker ps --format 'table {{.Names}}\t{{.Status}}'
```

```text
NAMES     STATUS
tinyapp   Up Less than a second (health: starting)
```

Wait about seven seconds and ask again:

```bash
docker ps --format 'table {{.Names}}\t{{.Status}}'
docker inspect --format '{{.State.Health.Status}}' tinyapp
curl localhost:8080/health
```

```text
NAMES     STATUS
tinyapp   Up 7 seconds (healthy)
healthy
{"status":"ok","version":"1.0.0"}
```

`docker inspect` prints everything Docker knows about a container as JSON; `--format` picks out one field. Scripts use exactly this command to wait for a new version to become healthy, as you'll see in Chapter 10.

## Step 5: See What Unhealthy Looks Like

Start a second container from the same image, but override its command so the app listens on port 9999 instead of 8000. The process runs perfectly well. It just isn't where the health check (or any user) expects it:

```bash
docker run -d --name tinyapp-broken tinyapp:1.0.0 uvicorn main:app --port 9999
```

Wait about 20 seconds, then look:

```bash
docker ps --filter name=tinyapp-broken --format 'table {{.Names}}\t{{.Status}}'
docker inspect --format '{{(index .State.Health.Log 0).Output}}' tinyapp-broken | grep URLError
```

```text
NAMES            STATUS
tinyapp-broken   Up 22 seconds (unhealthy)
    raise URLError(err)
urllib.error.URLError: <urlopen error [Errno 111] Connection refused>
```

Docker keeps the output of the last few checks, and here it says exactly what went wrong: nothing answered on port 8000. Without a health check, this container would look fine in `docker ps`. Remove it:

```bash
docker rm -f tinyapp-broken
```

> **Note:** On its own, Docker only *reports* an unhealthy container; it doesn't restart it. Platforms built on containers, such as cloud container services and Kubernetes, act on health checks: they stop sending traffic to unhealthy copies and replace them. Chapter 12 returns to this.

## Step 6: Push the Image to the Registry

To push, the image's name must start with the registry's address. `docker tag` adds a second name to the same image; nothing is copied:

```bash
docker tag tinyapp:1.0.0 localhost:5001/tinyapp:1.0.0
docker push localhost:5001/tinyapp:1.0.0
```

```text
The push refers to repository [localhost:5001/tinyapp]
…
b59ec4124c64: Layer already exists
e91e57f70610: Layer already exists
…
826b96dc18b7: Pushed
d122ce05d523: Layer already exists
1.0.0: digest: sha256:8615741e44becf529f9830f67909fedec585c424cc931db80f5df3e74a65d2ae size: 856
```

Only one layer was uploaded. The others were already in the registry from Chapter 6, because both images share the same base and libraries. That is layer sharing saving you time and space.

Ask the registry which tags it holds:

```bash
curl localhost:5001/v2/tinyapp/tags/list
```

```text
{"name":"tinyapp","tags":["53ba61aa33f5…","1.0.0","10ff8b9d01b5…"]}
```

The long tags are the commit hashes from Chapter 6's pipeline. Yours will differ.

## Step 7: Run It "Somewhere Else"

A real second machine would log in to a registry it can reach over the network and pull from it. You can get the same effect on your machine by deleting every local copy of the image first, so Docker has to fetch it:

```bash
docker rm -f tinyapp
docker rmi tinyapp:1.0.0 localhost:5001/tinyapp:1.0.0
docker run -d --name tinyapp -p 8080:8000 -e APP_VERSION=1.0.0 localhost:5001/tinyapp:1.0.0
```

```text
…
Untagged: tinyapp:1.0.0
Untagged: localhost:5001/tinyapp:1.0.0
Deleted: sha256:8615741e44becf529f9830f67909fedec585c424cc931db80f5df3e74a65d2ae
Unable to find image 'localhost:5001/tinyapp:1.0.0' locally
1.0.0: Pulling from tinyapp
826b96dc18b7: Download complete
Digest: sha256:8615741e44becf529f9830f67909fedec585c424cc931db80f5df3e74a65d2ae
Status: Downloaded newer image for localhost:5001/tinyapp:1.0.0
5b5efbbac133aa3edcade642bf004fc9edf08de1cdde20c7708813c16ad8433c
```

The digest after the pull is the same as the digest printed by the push: the bytes you run are exactly the bytes you built. After a few seconds:

```bash
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'
curl localhost:8080/health
```

```text
NAMES     IMAGE                          STATUS
tinyapp   localhost:5001/tinyapp:1.0.0   Up 7 seconds (healthy)
{"status":"ok","version":"1.0.0"}
```

Leave it running if you're going straight on to Chapter 10, which replaces it.

## When Something Goes Wrong

| You see | It usually means |
|---|---|
| `Bind for 0.0.0.0:8080 failed: port is already allocated` | Another container already uses port 8080. Remove it, or pick another host port |
| `curl` fails to connect to port 8080 | The container isn't running (check `docker ps -a` and `docker logs`), or `-p` is missing |
| `(unhealthy)` in `docker ps` | The app doesn't answer on port 8000; read the health log as in step 5 |
| `…tinyapp:9.9.9: not found` when pulling | That tag was never pushed; list the tags with `curl` |
| `pull access denied for tinyap, repository does not exist` | A typo in the image name, so Docker looked for it on Docker Hub |

## Summary, Key Terms, and Review Questions

### Summary

- Test first, then package. The image should contain only code that has passed its tests.
- A `HEALTHCHECK` lets Docker tell a running container from a working one.
- Tag images with a version, and with the registry's address so they can be pushed.
- Pushing uploads only missing layers; pulling by tag gives the same digest, so the same image.

### Key Terms

| Term | Meaning |
|---|---|
| Semantic versioning | Version numbers in the form MAJOR.MINOR.PATCH |

### Review Questions

1. Why is "the process is running" not enough to know the app works?
2. What do the four `HEALTHCHECK` options control?
3. Why did the push upload only one layer?
4. How can you be sure that the image you pulled is the one you built?

> **You understand this when** you can ship a small web app, with a health check, through a registry.
