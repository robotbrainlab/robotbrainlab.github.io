# Security, Speed, Failure, and Cost

Every book in this series ends by asking four questions about its topic. For infrastructure, the answers pull together everything you've built: secrets and access, slow builds and cold starts, health checks and restarts, and the bill.

*The problem.* My app is live, and now I worry about what will leak, slow down, break, or cost too much.

*The question.* For the infrastructure around my app, what goes wrong in security, speed, failure, and cost, and what limits the damage?

## Security: What Can Go Wrong, and What Limits the Damage

*Leaked secrets.* Passwords and keys escape through git commits, image layers, CI logs, and Terraform state. Keep them in a secret store (the CI system's secrets, the cloud's secret manager), pass them at run time, keep `.env`, `.secrets`, and `*.tfstate` out of git, and prefer roles, whose credentials expire by themselves. If a secret leaks, change it at once: deleting the commit doesn't help, because copies already exist.

*Too much access.* One key that can do everything turns a small leak into a disaster. Apply least privilege as in Chapter 7: one identity per app and per environment, each with only the permissions it needs, and MFA on every human login.

*Vulnerable images.* Your image contains hundreds of packages you didn't write, and security flaws are found in them every week. **Image scanning** compares every package in an image with public lists of known vulnerabilities. Trivy is a free scanner that runs in a container:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  -v trivy-cache:/root/.cache aquasec/trivy image --quiet \
  --severity HIGH,CRITICAL --scanners vuln localhost:5001/tinyapp:1.0.0 | grep Total
```

```text
Total: 44 (HIGH: 44, CRITICAL: 0)
```

The first run downloads Trivy's vulnerability database into the `trivy-cache` volume (delete it with `docker volume rm trivy-cache` when you're done). The same scan of the full `python:3.12` image found `Total: 343 (HIGH: 324, CRITICAL: 19)`, which is one more reason to start slim. Adding `--ignore-unfixed` shows only problems that already have a fix; for tinyapp on the day of writing, that was zero. The numbers change daily, so scan in the pipeline on every build, and rebuild images regularly even when your code hasn't changed, to pick up fixed base images.

*Open doors.* Databases and admin ports open to the whole internet are found by scanners within minutes. Keep databases in private subnets, allow only the traffic each part needs, and put a load balancer in front of the app.

*The supply chain.* Every base image, library, and CI action is code from someone else running with your permissions. Pin versions (`python:3.12-slim`, `fastapi==0.141.1`, `kreuzwerker/docker ~> 4.6`), commit lock files, prefer official and widely used actions, and remember that a job with the Docker socket controls the machine.

## Speed: What Makes This Slow

*Slow builds.* The biggest win is layer order: dependencies first, code last, so that the slow install step is `CACHED` on most builds (Chapter 5). Keep the build context small with `.dockerignore`. In CI, where each runner starts empty, use the cache options your CI offers: `actions/setup-python` can cache pip downloads, and Docker builds can reuse layers stored in the registry.

*Slow pipelines.* Run independent jobs in parallel, run the fastest checks first so failures show up early, and keep the test suite quick. A pipeline that takes an hour gets ignored; one that takes five minutes gets trusted.

*Slow deploys.* Every server pulls the image before it can start it. A 205 MB image arrives much sooner than a 1.62 GB one, and layers the server already has are skipped.

*Cold starts.* A new copy of an app can't answer until it has started. On a laptop, tinyapp answered about 0.4 seconds after `docker run`, but serverless platforms and freshly created instances add their own start-up time, from a fraction of a second to many seconds for large images. Keep images small, do less work at start-up, and on serverless platforms keep a minimum number of copies warm if the delay hurts.

*Distance.* Every request crosses the network. Pick a region close to your users, and keep the app and its database in the same region.

## Failure: How It Breaks, and How to Diagnose It

*Crashes.* A process can die: a bug, running out of memory, a restart of the machine. A restart policy tells Docker what to do then. Start a container with one:

```bash
docker run -d --name crashy --restart unless-stopped localhost:5001/tinyapp:1.0.0
```

Give the app a few seconds to start, then stop its process from inside, as if it had crashed. Signal 15 asks a process to stop:

```bash
docker exec crashy python -c "import os; os.kill(1, 15)"
```

Wait a few more seconds, then ask Docker what happened, and clean up:

```bash
docker inspect --format '{{.RestartCount}} restart(s), running: {{.State.Running}}' crashy
docker rm -f crashy
```

```text
1 restart(s), running: true
crashy
```

`unless-stopped` restarts the container whenever it exits, until you stop it yourself. Use it (or `always`) for anything that should keep running.

*Running but broken.* A restart policy only notices a process that has exited. A stuck or misconfigured app needs a health check, and something that acts on it. Plain Docker only reports `unhealthy`; container platforms stop sending it traffic and replace it.

*Bad releases.* The pipeline is your safety net: tests before build, health-gated deploys, automatic rollback, and every old image kept in the registry (Chapter 10).

*Lost machines and zones.* Infrastructure as code rebuilds machines in minutes (Chapter 11); backups bring back data; copies in two availability zones keep you running while that happens.

When something is wrong, find the failing layer before changing anything:

| Symptom | First thing to run |
|---|---|
| The app doesn't answer | `docker ps -a` (is it running?), then `docker logs <name>` |
| It runs but misbehaves | `docker inspect --format '{{json .State.Health}}' <name>` |
| "Connection refused" | Check the `-p` mapping and that the app listens on `0.0.0.0` |
| A pipeline fails | Read the first red step's log; rerun it with `act -v` for detail |
| Something changed by itself | `terraform plan` to find drift |

## Cost: What Does This Cost Me?

*Forgotten resources.* The most common surprise bill is something nobody uses any more: a test VM, a disk left behind by a deleted VM, an old database snapshot, a load balancer for a finished experiment. Create experiments with Terraform and remove them with `terraform destroy`; label everything so the bill shows who owns it.

*Always-on services.* VMs, managed databases, and load balancers charge every hour whether or not traffic arrives. Turn development environments off at night, and choose serverless or scale-to-zero services for spiky or tiny workloads (Chapter 3's lab showed where the lines cross).

*Growth you don't see.* Every push in Chapter 10 added an image to the registry, and every log line is stored somewhere. Set retention rules: keep, say, the last 20 images and 30 days of logs.

*Data leaving the cloud.* Egress is charged per gigabyte. Serving large files to users, or copying data between regions or providers, can cost more than the servers.

*Oversized machines.* Start small, measure, then grow. A small app on an instance four times too big pays four times too much, forever.

And before any of this: set a budget alert (Chapter 7), and read it when it arrives.

## Summary, Key Terms, and Review Questions

### Summary

- Security: keep secrets out of git, images, and logs; give least privilege; scan images and rebuild them regularly; close unneeded ports; pin what you depend on.
- Speed: order layers for caching, keep images and contexts small, parallelise pipelines, and plan for cold starts and distance.
- Failure: restart policies handle crashes, health checks handle stuck apps, pipelines and rollback handle bad releases, and IaC plus backups handle lost machines. Diagnose layer by layer.
- Cost: delete what you don't use, switch off what you don't need, set retention and budgets, and watch egress.

### Key Terms

| Term | Meaning |
|---|---|
| Image scanning | Checking an image's packages against lists of known vulnerabilities |

### Review Questions

1. Name four places a secret can leak from in the setup you built, and how each is prevented.
2. Why can an image with no changes to your code still need rebuilding?
3. What makes a Docker build slow, and what is the single biggest fix?
4. What is the difference between what a restart policy catches and what a health check catches?
5. List three ways a cloud bill grows without anyone noticing.

> **You understand this when** you can look at any part of your setup, from the Dockerfile to the Terraform state, and say what could leak, slow down, break, or cost money there, and what you would do about it.
