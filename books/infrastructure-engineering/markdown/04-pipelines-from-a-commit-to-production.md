# Pipelines: From a Commit to Production

A pipeline turns "I changed some code" into "the change is running for users", with checks at every step. This chapter covers continuous integration and delivery, stages and artifacts, environments, deployment strategies, and rollback. In the lab you build a tiny pipeline from a shell script.

*The problem.* Every release is a nervous afternoon of manual steps.

*The question.* How can a machine take my change from a commit to production the same safe way every time?

## The Nervous Afternoon

A manual release means pulling the code, running the tests (if you remember), building, copying to the server, and restarting, all from memory. One forgotten step means a broken site on a Friday evening, so releases become rare, and each one bigger and scarier.

Factories solved this with the assembly line: every car passes the same stations in the same order, and an inspection station can stop the line when it finds a fault. A pipeline is an assembly line for code.

## Just Enough Git

Pipelines start from git, the tool almost every team uses to track changes to code. A commit is one saved snapshot of a project, with a message such as "Fix the greeting" and an ID like `53ba61a…`. The main line of history is usually called `main`. Pushing sends your commits to a shared copy of the project, on a service such as GitHub, and that push is the moment a pipeline wakes up.

## The Pipeline

A **pipeline** is an automated sequence of stages that every change passes through. Each stage must succeed before the next one starts. If any stage fails, the line stops, and nobody gets the broken change.

```text
 git push
    │
    ▼
 ┌───────┐  ┌──────┐  ┌─────────┐  ┌─────────┐  ┌────────────┐
 │ build │─►│ test │─►│ package │─►│ staging │─►│ production │
 └───────┘  └──────┘  └─────────┘  └─────────┘  └────────────┘
   a red stage stops the line and tells you why
```

A pipeline runs on a runner: a fresh container or VM that follows the pipeline's instructions and is thrown away afterwards. Starting clean each time, it catches the "works on my machine" problems your laptop hides.

## Continuous Integration

**Continuous integration** (CI) means that everyone merges their work into the shared branch often, at least daily, and that every change is built and tested automatically. The result is a simple signal: green (it passed) or red (it didn't, and here is the log).

Good CI is fast: aim for minutes, or people start ignoring it.

## Continuous Delivery and Continuous Deployment

After CI, the change has passed its tests. What happens next has two names that sound almost the same:

| | Continuous delivery | Continuous deployment |
|---|---|---|
| After tests pass | Ready to release; a person presses a button | Released to production automatically |
| Good for | Teams that want a human decision | Teams with strong tests and quick rollback |

Both are called CD, so people say CI/CD. With **continuous delivery**, every passing change *could* go live at any moment. With **continuous deployment**, it *does*. You will build continuous deployment in Chapter 10.

## Artifacts: Build Once, Deploy Many

The package stage produces an **artifact**: the built, ready-to-run output, stored and labelled with a version. For container apps it is an image in a registry, tagged with the commit hash.

The rule is build once, deploy many: build the artifact one time and send that exact artifact to staging, then to production. A rebuild for production could pick up a newer library, and then staging tested something other than what production runs.

Keep old artifacts, too. They are what makes going back possible.

## Environments in a Pipeline

The same artifact moves through the environments from Chapter 1, with a different configuration in each. Many teams move it to staging automatically, and to production only after a check: automatic tests on staging, or a person clicking "approve".

## Deployment Strategies

Deploying means swapping the running old version for the new one. There are four common ways, and each is a **deployment strategy**:

| Strategy | How it works | Downtime | Extra cost | Risk |
|---|---|---|---|---|
| Recreate | Stop the old version, start the new one | A few seconds | None | Everyone gets a bad release at once |
| Rolling | Replace copies one at a time | None | Little | A bad release spreads gradually |
| Blue-green | Run the new version beside the old, then switch all traffic | None | Double, briefly | Switching back is instant |
| Canary | Send a small share of users to the new version first | None | Little | Only a few users meet a bad release |

The canary is named after the birds miners carried underground as an early warning of bad air. A canary release lets a few per cent of users try the new version while you watch the error rate.

A **health check** is what makes all of these safe: a quick automatic test, such as calling the app's `/health` address, that says whether a copy is working. A deployment should wait for the new version to report healthy before treating it as live. Chapter 9 adds one to a container.

## Rollback

A **rollback** means going back to the previous good version. Because the old artifact is still in the registry, rolling back is just a deployment of an older version, and it should take seconds. The alternative is to roll forward: fix the bug and push a new version through the pipeline. Rolling back first and fixing calmly afterwards is usually the kinder option for your users.

> **Warning:** Code rolls back easily; data doesn't. If the new version changed the database's structure, the old version may not understand it any more. Make database changes in small steps that both the old and new code can live with.

## Lab: A Pipeline in Twenty Lines

You'll build a three-stage pipeline (test, build, deploy) as a shell script, watch a failing test stop the line, and roll back to an older artifact. The "server" is just a folder called `staging`.

1. Create a folder with a tiny module and its test:

   ```bash
   mkdir -p ~/infra-labs/ch04 && cd ~/infra-labs/ch04
   ```

   `greet.py`:

   ```python
   def greet(name):
       return f"Hello, {name}!"
   ```

   `test_greet.py`:

   ```python
   import unittest

   from greet import greet


   class GreetTest(unittest.TestCase):
       def test_greet(self):
           self.assertEqual(greet("Asha"), "Hello, Asha!")


   if __name__ == "__main__":
       unittest.main()
   ```

2. Create `deploy.sh`, which installs one artifact on the "server":

   ```bash
   #!/usr/bin/env bash
   # Deploy one built artifact (a version) to the staging folder.
   set -euo pipefail
   VERSION="$1"

   rm -rf staging && mkdir staging
   tar -xzf "artifacts/greet-$VERSION.tar.gz" -C staging
   echo "$VERSION" > staging/VERSION
   echo "staging now runs version $VERSION"
   ```

   And `pipeline.sh`, which runs the stages in order:

   ```bash
   #!/usr/bin/env bash
   # A tiny pipeline: test, build, deploy. Any failure stops the line.
   set -euo pipefail
   VERSION="$1"

   echo "== Stage 1: test"
   python3 -m unittest -q

   echo "== Stage 2: build"
   mkdir -p artifacts
   tar -czf "artifacts/greet-$VERSION.tar.gz" greet.py
   echo "built artifacts/greet-$VERSION.tar.gz"

   echo "== Stage 3: deploy to staging"
   ./deploy.sh "$VERSION"
   ```

   `set -euo pipefail` is the "stop the line" switch: the script exits at the first command that fails. `$1` is the first argument, the version.

3. Make both scripts executable and run the pipeline:

   ```bash
   chmod +x pipeline.sh deploy.sh
   ./pipeline.sh 1.0.0
   ```

   ```text
   == Stage 1: test
   ----------------------------------------------------------------------
   Ran 1 test in 0.000s

   OK
   == Stage 2: build
   built artifacts/greet-1.0.0.tar.gz
   == Stage 3: deploy to staging
   staging now runs version 1.0.0
   ```

4. Break the code: in `greet.py`, change `Hello` to `Hi`. Run the pipeline for a new version, then check what staging runs:

   ```bash
   ./pipeline.sh 1.1.0
   cat staging/VERSION
   ```

   ```text
   == Stage 1: test
   ======================================================================
   FAIL: test_greet (test_greet.GreetTest.test_greet)
   …
   AssertionError: 'Hi, Asha!' != 'Hello, Asha!'
   …
   FAILED (failures=1)
   1.0.0
   ```

   The line stopped at stage 1. No `1.1.0` artifact was built, and staging still runs `1.0.0`.

5. Change `Hi` back to `Hello` and run `./pipeline.sh 1.1.0` again. This time all three stages pass and the last line is `staging now runs version 1.1.0`.

6. Suppose users dislike 1.1.0. Roll back by deploying the older artifact, which is still on the shelf:

   ```bash
   ./deploy.sh 1.0.0
   ls artifacts
   ```

   ```text
   staging now runs version 1.0.0
   greet-1.0.0.tar.gz
   greet-1.1.0.tar.gz
   ```

**Expected results:** a passing run goes through all three stages; a failing test stops the line before anything is built or deployed; and rollback is just `deploy.sh` with an older version, taking well under a second, because the old artifact was kept.

## Summary, Key Terms, and Review Questions

### Summary

- Manual releases are slow and risky because people forget steps. A pipeline runs the same stages, in the same order, for every change.
- CI builds and tests every change automatically. Continuous delivery makes every passing change ready to release; continuous deployment releases it.
- Build an artifact once, version it, and promote the same artifact through every environment.
- Recreate, rolling, blue-green, and canary deployments trade downtime, cost, and risk. Health checks make them safe.
- Rollback redeploys an older artifact. Database changes need extra care.

### Key Terms

| Term | Meaning |
|---|---|
| Pipeline | An automated sequence of stages every change passes through |
| Continuous integration (CI) | Building and testing every change automatically |
| Continuous delivery | Every passing change is ready to release at the press of a button |
| Continuous deployment | Every passing change is released automatically |
| Artifact | The built, versioned output of a pipeline |
| Deployment strategy | Recreate, rolling, blue-green, or canary: how the new version replaces the old |
| Health check | A quick automatic test of whether an app copy is working |
| Rollback | Returning to the previous good version |

### Review Questions

1. Why do manual releases tend to become rarer and riskier over time?
2. What is the difference between continuous delivery and continuous deployment?
3. Why should the artifact that reached staging be the one deployed to production, rather than a fresh build?
4. Compare blue-green and canary deployments. What does each protect you from?
5. Why is rolling back code easier than rolling back a database change?

> **You understand this when** you can draw the pipeline for a small app, name what each stage produces, and explain how you would roll back if production broke after the last stage.
