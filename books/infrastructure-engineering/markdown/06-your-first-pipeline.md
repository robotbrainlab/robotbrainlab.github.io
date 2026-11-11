# Your First Pipeline

In this chapter you write a real CI pipeline with GitHub Actions: it runs the tests on every push, builds the image, and publishes it to a registry, using a secret on the way. You will run it on your own machine with act, so you need no GitHub account.

*The problem.* I keep forgetting to run the tests before I push.

*The question.* How do I make a machine run my checks on every push, so that forgetting is no longer possible?

## GitHub Actions in One Picture

GitHub Actions is the pipeline service built into GitHub. You describe a pipeline in a YAML file inside your repository, and GitHub runs it for you whenever something happens. Think of it as a robot assistant that watches the repository: "whenever someone pushes to `main`, do these things, in this order, and tell me if anything fails."

Five words cover almost everything:

| Word | Meaning | In the file |
|---|---|---|
| **Workflow** | One pipeline, in one YAML file under `.github/workflows/` | the whole file |
| Event | What starts the workflow, such as a push | `on:` |
| Job | A group of steps that runs on one fresh runner | `jobs:` |
| Step | One command, or one action | `steps:` |
| Action | A reusable, ready-made step someone else wrote | `uses:` |

```text
 workflow  (.github/workflows/ci.yml, started by a push)
 ├── job: test      (runner 1)
 │    ├── step: check out the code
 │    ├── step: set up Python
 │    ├── step: pip install
 │    └── step: pytest
 └── job: publish   (runner 2, only after "test" passes)
      ├── step: build the image
      └── step: push the image
```

Jobs run at the same time unless one says `needs:` another. Steps inside a job run in order, and the first failing step fails the job.

YAML is the file format. It is Python-like in one important way: indentation matters. `key: value` sets a value, an indented block belongs to the line above it, and lines starting with `-` form a list.

## Running Workflows Locally with act

On GitHub, each job runs on a fresh virtual machine. act imitates that on your computer: it reads your workflow files and runs each job in a Docker container that looks like GitHub's runner. The image it uses, `catthehacker/ubuntu:act-latest`, is over 2 GB, so the first run takes a while to download it.

Put a file called `.actrc` in your repository. act reads its options from there, so you don't have to type them each time:

```text
-P ubuntu-latest=catthehacker/ubuntu:act-latest
--pull=false
```

The first line picks the image for `ubuntu-latest` jobs; the second stops act checking for a newer one on every run.

To build and push images, a job needs Docker. act shares yours with each job by attaching the Docker socket, the file through which the `docker` command talks to the Docker daemon. So a `docker build` inside a job builds on your own Docker, and the image appears in your own `docker images`.

> **Note:** If act can't reach your Docker, point it at the socket with `--container-daemon-socket unix:///path/to/docker.sock`.

## A Workflow That Runs the Tests

tinyapp has two small tests in `test_main.py`. They call the app in memory, without a server:

```python
from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_visits_count_up(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DATA_FILE", tmp_path / "visits.txt")
    assert client.get("/visits").json() == {"visits": 1}
    assert client.get("/visits").json() == {"visits": 2}
```

The first half of the workflow runs them on every push to `main`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

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
```

`on:` lists the events: pushes to `main`, and pull requests. `runs-on:` picks the runner. `actions/checkout` copies the repository into the runner, and `actions/setup-python` installs the Python version you ask for. `requirements-dev.txt` adds the test tools to the app's own requirements:

```text
-r requirements.txt
pytest==9.1.1
httpx2==2.13.1
```

The first line pulls in `requirements.txt`; `httpx2` is the HTTP client FastAPI's test client needs. The `env:` block sets a variable every job can use.

## Building and Publishing the Image

Once the tests pass, the second job builds the image and pushes it to a registry. You'll run your own registry: Docker's `registry:2` image is a complete registry in one container.

```yaml
  publish:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check the registry token
        env:
          REGISTRY_TOKEN: ${{ secrets.REGISTRY_TOKEN }}
        run: |
          test -n "$REGISTRY_TOKEN" || { echo "REGISTRY_TOKEN is missing"; exit 1; }
          echo "Using token $REGISTRY_TOKEN"
      - name: Build the image
        run: docker build -t $IMAGE:${{ github.sha }} .
      - name: Push the image
        run: docker push $IMAGE:${{ github.sha }}
```

`needs: test` means "only if the test job passed". `${{ github.sha }}` is filled in with the commit hash, so every image is tagged with the exact commit it was built from. That is the build-once artifact from Chapter 4.

> **Note:** The registry listens on port 5001, not the usual 5000, because on macOS port 5000 is taken by the AirPlay Receiver. Docker trusts registries on `localhost` without HTTPS, which is fine for a lab and never for anything real.

## Secrets in CI

Pipelines need secrets, such as a registry password. They never go in the workflow file, which is in git for everyone to read.

On GitHub, you store secrets in the repository's settings (Settings, then Secrets and variables, then Actions). A workflow reads one as `${{ secrets.REGISTRY_TOKEN }}`, and GitHub replaces the value with `***` anywhere it would appear in the logs. act reads secrets from a file called `.secrets` in the same `NAME=value` format, and masks them the same way.

Our "Check the registry token" step stands in for `docker login`: it fails if the secret is missing, and prints it only so you can watch the masking. Never print a secret in a real workflow.

> **Warning:** Add `.secrets` and `.env` to `.gitignore` before your first commit. Masking protects the logs, not the repository, and it can't stop a step from sending the secret somewhere else. Only use actions you trust in workflows that can see secrets.

## Lab: Tests on Every Push

1. Start the local registry and check that it is empty:

   ```bash
   docker run -d --name registry -p 5001:5000 registry:2
   curl localhost:5001/v2/_catalog
   ```

   ```text
   {"repositories":[]}
   ```

2. Make a fresh folder, `~/infra-labs/ch06`, and copy in the app's four files (from `labs/tinyapp/`) and Chapter 5's `Dockerfile` and `.dockerignore` (from `labs/ch05/` and `labs/tinyapp/`). Then create `.gitignore` (with `.env`, `.secrets`, `__pycache__/`, `.pytest_cache/`, and `.venv/`), `.actrc` as above, `.secrets` containing `REGISTRY_TOKEN=not-a-real-token-123`, and `.github/workflows/ci.yml` with both jobs. Then make it a git repository and commit:

   ```bash
   git init -b main
   git add -A
   git commit -m "tinyapp with CI"
   ```

   If git asks who you are, set `user.name` and `user.email` with `git config` inside the folder, then commit again.

3. List the jobs act found:

   ```bash
   act -l
   ```

   ```text
   Stage  Job ID   Job name  Workflow name  Workflow file  Events
   0      test     test      CI             ci.yml         push,pull_request
   1      publish  publish   CI             ci.yml         push,pull_request
   ```

4. Run the workflow as if you had pushed. The first run downloads the runner image and the actions:

   ```bash
   act push
   ```

   ```text
   [CI/test]   | 2 passed in 0.13s
   …
   [CI/test] 🏁  Job succeeded
   …
   [CI/publish]   | Using token ***
   …
   [CI/publish]   | 53ba61aa33f5…: digest: sha256:cdc5d934… size: 856
   [CI/publish]   ✅  Success - Main Push the image [736.652791ms]
   …
   [CI/publish] 🏁  Job succeeded
   ```

5. Break a test on purpose: in `main.py`, change `"status": "ok"` to `"status": "OK"`, commit, and run act again:

   ```bash
   git commit -am "Shout the status"
   act push
   ```

   ```text
   …
   [CI/test]   | FAILED test_main.py::test_health - AssertionError: assert 'OK' == 'ok'
   [CI/test]   | 1 failed, 1 passed in 0.13s
   [CI/test]   ❌  Failure - Main pytest -q [334.395125ms]
   [CI/test] 🏁  Job failed
   Error: Job 'test' failed
   ```

   The publish job never ran, so no broken image reached the registry.

6. Undo the change with a new commit, then run once without the secrets file to see the check fail:

   ```bash
   git revert --no-edit HEAD
   mv .secrets ../secrets.bak
   act push
   mv ../secrets.bak .secrets
   ```

   ```text
   …
   [CI/publish]   | REGISTRY_TOKEN is missing
   [CI/publish] 🏁  Job failed
   Error: Job 'publish' failed
   ```

7. Run `act push` once more. Both jobs succeed. Ask the registry what it holds:

   ```bash
   curl localhost:5001/v2/tinyapp/tags/list
   ```

   ```text
   {"name":"tinyapp","tags":["53ba61aa33f5…","10ff8b9d…"]}
   ```

**Expected results:** a clean push runs the tests and publishes an image tagged with the commit hash; a failing test stops the workflow before anything is built; a missing secret stops the publish job; and the secret shows as `***` in logs. Leave the registry running for the next chapters. Your commit hashes will differ.

## Summary, Key Terms, and Review Questions

### Summary

- A GitHub Actions workflow is a YAML file of jobs and steps, started by an event.
- Jobs run on fresh runners; `needs:` orders them; a failing step stops the line.
- Tag images with the commit hash. Secrets live in the CI system and are masked in logs.

### Key Terms

| Term | Meaning |
|---|---|
| Workflow | One pipeline, defined in a YAML file in `.github/workflows/` |

### Review Questions

1. What is the difference between a job and a step?
2. What does `needs: test` do, and what would happen without it?
3. Why tag the image with `${{ github.sha }}` rather than `latest`?
4. Where should a CI secret live, and what does masking protect against?

> **You understand this when** you can read a workflow and say what runs, when, and what a failing test stops.
