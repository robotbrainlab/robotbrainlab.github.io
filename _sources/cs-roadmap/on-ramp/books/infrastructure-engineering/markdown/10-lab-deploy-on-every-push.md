# Lab: Deploy on Every Push

In this lab you build continuous deployment. Every push to `main` runs the tests, builds and publishes an image, and replaces the running app with it. Then you break a release on purpose and watch the pipeline notice and put the previous version back on its own. Finally, you roll back by hand and fix forward.

*The problem.* I want every change on `main` to go live on its own, safely.

*The question.* How do I build a pipeline that deploys every push, notices a bad release, and puts the good one back?

## The Plan

"Production" in this lab is the container named `tinyapp` on port 8080 of your machine. The pipeline has three jobs:

```text
 git commit + act push
        │
        ▼
 ┌────────┐    ┌──────────────────┐    ┌───────────────────┐
 │ test   │ ─► │ publish          │ ─► │ deploy            │
 │ pytest │    │ build + push     │    │ remember current  │
 └────────┘    │ localhost:5001/  │    │ start new, wait   │
               │ tinyapp:<commit> │    │ for healthy, else │
               └──────────────────┘    │ put old one back  │
                                       │ and fail          │
                                       └───────────────────┘
```

The deploy job uses the recreate strategy from Chapter 4, with an **automatic rollback**: if the new container isn't healthy in time, the old image goes back and the pipeline turns red.

Start in a fresh folder, `~/infra-labs/ch10`, with the app's four files, Chapter 9's `Dockerfile` (the one with the `HEALTHCHECK`), `.dockerignore`, and `.gitignore`, all from the book's `labs/tinyapp/` folder, plus Chapter 6's `.actrc` from `labs/ch06/`. Make it a repository with `git init -b main`. The registry on port 5001 must be running, as in Chapter 9.

## Step 1: The Deploy Script

Deploying is several commands with decisions between them, so it lives in a script, `deploy.sh`, in the repository. The workflow calls it, and so can you.

```bash
#!/usr/bin/env bash
# Replace the running tinyapp container with a new image.
# If the new one is not healthy in time, put the old one back.
set -euo pipefail

NEW_IMAGE="$1"
NAME="tinyapp"

start() {
  docker rm -f "$NAME" >/dev/null 2>&1 || true
  docker run -d --name "$NAME" -p 8080:8000 \
    -e APP_VERSION="${1##*:}" "$1" >/dev/null
}

wait_until_healthy() {
  for _ in $(seq 1 30); do
    status="$(docker inspect --format '{{.State.Health.Status}}' "$NAME")"
    echo "  health: $status"
    case "$status" in
      healthy) return 0 ;;
      unhealthy) return 1 ;;
    esac
    sleep 2
  done
  return 1
}

OLD_IMAGE="$(docker inspect --format '{{.Config.Image}}' "$NAME" 2>/dev/null || true)"
echo "Running now: ${OLD_IMAGE:-nothing}"
echo "Deploying:   $NEW_IMAGE"
start "$NEW_IMAGE"

if wait_until_healthy; then
  echo "Deploy succeeded: $NEW_IMAGE is healthy"
  exit 0
fi

echo "Deploy FAILED: $NEW_IMAGE is not healthy"
if [ -n "$OLD_IMAGE" ]; then
  echo "Rolling back to $OLD_IMAGE"
  start "$OLD_IMAGE"
  wait_until_healthy && echo "Rollback succeeded"
fi
exit 1
```

Reading it from the bottom half up:

- Before touching anything, it asks Docker which image the current `tinyapp` container runs, and remembers it as `OLD_IMAGE`. If there is no container yet, that's empty.
- `start` removes the old container and runs a new one. `${1##*:}` is the part of the image name after the last colon, the tag, which becomes `APP_VERSION`.
- `wait_until_healthy` asks for the health status every 2 seconds, for up to a minute, and stops as soon as it's `healthy` or `unhealthy`.
- On failure, it starts `OLD_IMAGE` again and exits with 1, which makes the pipeline step fail. A rollback that works still leaves the pipeline red, because the release didn't go out.

Make it executable with `chmod +x deploy.sh`.

## Step 2: The Workflow

The workflow does everything Chapter 6's `ci.yml` did (apart from the secret check) and adds the deploy job. Save it as `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

concurrency: deploy

env:
  IMAGE: localhost:5001/tinyapp

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements-dev.txt
      - run: pytest -q

  publish:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and push the image
        run: |
          TAG="${GITHUB_SHA::7}"
          docker build -t "$IMAGE:$TAG" .
          docker push "$IMAGE:$TAG"

  deploy:
    needs: publish
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Replace the running container
        run: ./deploy.sh "$IMAGE:${GITHUB_SHA::7}"
```

`GITHUB_SHA` is the commit hash, and `${GITHUB_SHA::7}` keeps its first seven characters, the short form git itself shows. `concurrency: deploy` tells GitHub never to run two of these workflows at once, so two quick pushes can't deploy over each other.

## Step 3: The First Deploy

Remove any `tinyapp` container left over from Chapter 9, so the pipeline starts from nothing, then commit and push:

```bash
docker rm -f tinyapp
git add -A
git commit -m "Deploy on every push"
act push
```

The interesting lines of act's output:

```text
[Deploy/test]   | 2 passed in 0.12s
[Deploy/test] 🏁  Job succeeded
[Deploy/publish]   | 11e42a4: digest: sha256:03d58610… size: 856
[Deploy/publish] 🏁  Job succeeded
[Deploy/deploy ]   | Running now: nothing
[Deploy/deploy ]   | Deploying:   localhost:5001/tinyapp:11e42a4
[Deploy/deploy ]   |   health: starting
[Deploy/deploy ]   |   health: starting
[Deploy/deploy ]   |   health: starting
[Deploy/deploy ]   |   health: healthy
[Deploy/deploy ]   | Deploy succeeded: localhost:5001/tinyapp:11e42a4 is healthy
[Deploy/deploy ] 🏁  Job succeeded
```

Production is live:

```bash
curl localhost:8080/health
```

```text
{"status":"ok","version":"11e42a4"}
```

## Step 4: A Good Change Goes Live

In `main.py`, make `/health` name the app:

```python
    return {"status": "ok", "version": VERSION, "app": "tinyapp"}
```

```bash
git commit -am "Name the app in /health"
act push
```

In act's output:

```text
[Deploy/deploy ]   | Running now: localhost:5001/tinyapp:11e42a4
[Deploy/deploy ]   | Deploying:   localhost:5001/tinyapp:6c357a4
…
[Deploy/deploy ]   | Deploy succeeded: localhost:5001/tinyapp:6c357a4 is healthy
```

`curl localhost:8080/health` now returns `{"status":"ok","version":"6c357a4","app":"tinyapp"}`. You changed code and committed; the machine did the rest.

## Step 5: A Bad Deploy, Caught and Rolled Back

Now a change that passes every test but breaks production. Someone edits the Dockerfile's last line to serve on port 8001, forgetting that the health check (and the `-p` mapping) expect 8000:

```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

```bash
git commit -am "Serve on port 8001"
act push
```

In act's output:

```text
[Deploy/test]   | 2 passed in 0.12s
[Deploy/test] 🏁  Job succeeded
[Deploy/publish] 🏁  Job succeeded
[Deploy/deploy ]   | Running now: localhost:5001/tinyapp:6c357a4
[Deploy/deploy ]   | Deploying:   localhost:5001/tinyapp:17541b3
[Deploy/deploy ]   |   health: starting
…
[Deploy/deploy ]   |   health: unhealthy
[Deploy/deploy ]   | Deploy FAILED: localhost:5001/tinyapp:17541b3 is not healthy
[Deploy/deploy ]   | Rolling back to localhost:5001/tinyapp:6c357a4
[Deploy/deploy ]   |   health: starting
[Deploy/deploy ]   |   health: starting
[Deploy/deploy ]   |   health: starting
[Deploy/deploy ]   |   health: healthy
[Deploy/deploy ]   | Rollback succeeded
[Deploy/deploy ]   ❌  Failure - Main Replace the running container [23.091493666s]
[Deploy/deploy ] 🏁  Job failed
Error: Job 'deploy' failed
```

The tests passed because they never look at the Dockerfile. The image built and was published. Only the health check, in the real environment, caught the problem. Users saw a few seconds of downtime while the broken version was tried, and then the previous version was back:

```bash
docker ps --filter name=tinyapp --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'
curl localhost:8080/health
```

```text
NAMES     IMAGE                            STATUS
tinyapp   localhost:5001/tinyapp:6c357a4   Up 6 seconds (healthy)
{"status":"ok","version":"6c357a4","app":"tinyapp"}
```

> **Tip:** A blue-green or rolling deployment would avoid even those few seconds: the new version starts next to the old one, and traffic moves only when it is healthy. The idea is the same; the platform does more of the work.

## Step 6: Roll Back by Hand

Sometimes a release is healthy but wrong, and you decide to go back. Every version the pipeline ever built is still in the registry:

```bash
curl localhost:5001/v2/tinyapp/tags/list
```

```text
{"name":"tinyapp","tags":["6c357a4","53ba61aa33f5…","11e42a4","1.0.0","10ff8b9d01b5…","17541b3"]}
```

Rolling back is just deploying an older tag. The same script works from your terminal:

```bash
./deploy.sh localhost:5001/tinyapp:11e42a4
```

```text
Running now: localhost:5001/tinyapp:6c357a4
Deploying:   localhost:5001/tinyapp:11e42a4
  health: starting
  health: starting
  health: starting
  health: healthy
Deploy succeeded: localhost:5001/tinyapp:11e42a4 is healthy
```

## Step 7: Fix Forward

The real fix belongs in git, so that `main` describes what should run. `git revert` makes a new commit that undoes the bad one, and the pipeline deploys it like any other change:

```bash
git revert --no-edit HEAD
act push
```

The deploy job replaces the hand-picked image with one built from the revert commit, and ends with `Deploy succeeded`. The history in `git log --oneline` now tells the whole story: the good change, the bad one, and its revert.

## How act Reaches Your Docker

The deploy job runs inside act's runner, yet `tinyapp` appears on your own port 8080. Through the Docker socket (Chapter 6), the job's `docker run` asks *your* Docker daemon to start the container, beside the runner rather than inside it.

> **Warning:** Access to the Docker socket is access to the whole machine: anything that can talk to it can start containers with any files mounted. That is fine on your laptop. On shared CI, deploy jobs instead call the target platform with a narrowly scoped credential, for example a cloud deploy command, or SSH to a server that runs `docker compose up -d`.

## Summary, Key Terms, and Review Questions

### Summary

- Continuous deployment chains test, publish, and deploy; every passing push to `main` goes live.
- The deploy script remembers the running image, starts the new one, and waits for it to become healthy.
- Tests can pass while a release is broken. A health check in the real environment is the last line of defence, and it triggers the automatic rollback.
- Kept images make a manual rollback one command; `git revert` fixes forward and keeps `main` truthful.

### Key Terms

| Term | Meaning |
|---|---|
| Automatic rollback | Restoring the previous version when the new one fails its health check |

### Review Questions

1. What does `deploy.sh` remember before it changes anything, and why?
2. Why did the bad release pass the test and publish jobs?
3. The rollback in step 5 succeeded. Why is the pipeline still red?
4. What is the difference between rolling back (step 6) and fixing forward (step 7)?
5. How does a job inside act start a container on your machine, and why is that risky?

> **You understand this when** you can push a change and predict, before act finishes, which image will be running on port 8080 and what the pipeline's final colour will be.
