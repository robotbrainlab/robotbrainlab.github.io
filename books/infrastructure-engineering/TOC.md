# Infrastructure Engineering from Zero

**The problem you hit:** It works on my machine but breaks on the server, and I don't even own a server.
**The question it answers:** How does my code get from my laptop to machines that serve everyone, the same way every time?
**Target:** 95–99 pages

The labs run on the reader's own machine, so no cloud account or bill is needed: Docker, GitHub Actions run locally with `act`, a local registry, MinIO standing in for cloud object storage, and Terraform with its Docker provider. Steps that need a real cloud account are described in words, not as commands.

## Front matter

Title page · Copyright · Contents · Preface (Who This Book Is For, How This Book Is Organized, How to Use This Book, What You Need Installed, Conventions Used in This Book)

## Part I · Understand

*What to ignore for now:* Kubernetes, service meshes, and comparing every cloud provider's products.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 1 | From "Works on My Machine" to "Works for Everyone" | It runs perfectly on my laptop and crashes on the server. | What infrastructure is, environments, the DevOps idea (fast, safe feedback loops), the cloud idea | 6 |
| 2 | Containers: Shipping the Whole Kitchen | The server has a different Python, different libraries, and a different operating system. | What a container is, images and containers, layers, containers compared with virtual machines, registries | 8 |
| 3 | The Cloud: Renting Computers by the Minute | I don't own a server, and buying one feels wrong. | IaaS, PaaS, and serverless, regions and zones, compute, storage, cloud networking, paying for what you use | 8 |
| 4 | Pipelines: From a Commit to Production | Every release is a nervous afternoon of manual steps. | Continuous integration, continuous delivery, stages and artifacts, environments, deployment strategies, rollback | 7 |

## Part II · Use

*What to ignore for now:* orchestration at scale, multi-cloud, and writing your own CI runners.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 5 | Docker in Practice | I understand containers, but I've never built one. | Dockerfiles, building and running, ports, volumes, configuration and secrets, smaller and safer images, Compose | 9 |
| 6 | Your First Pipeline | I keep forgetting to run the tests before I push. | GitHub Actions, running tests on every push, building and publishing an image, secrets in CI | 7 |
| 7 | Cloud Building Blocks | The cloud console has 200 services, and I need three. | Accounts and IAM, virtual machines, object storage (tried locally with MinIO), managed databases, firewalls, serverless, cost alerts | 7 |
| 8 | Infrastructure as Code | I clicked 40 buttons to build this, and I can't do it again. | Describing infrastructure in files, Terraform: providers, resources, `plan`, `apply`, state | 6 |

## Part III · Apply

*What to ignore for now:* tuning, autoscaling policies, and production-grade monitoring.

| Ch | Chapter | Opens with | Covers | Pages |
|---|---|---|---|---|
| 9 | Lab: Ship a Small Python App in a Container | I have a working app and want it to run anywhere. | Containerise an app, run it, check its health, push the image | 8 |
| 10 | Lab: Deploy on Every Push | I want every change on `main` to go live on its own, safely. | A pipeline that tests, builds, pushes to a registry, and deploys; a failed deploy; rolling back to the previous image | 8 |
| 11 | Lab: Rebuild Everything from Code | My server died. Can I get it all back in five minutes? | Terraform with the Docker provider: create the app, its database, and their network; change, destroy, and recreate the whole setup | 8 |

## Part IV · What Next

| Ch | Chapter | Covers | Pages |
|---|---|---|---|
| 12 | Security, Speed, Failure, and Cost | Secrets and least-privilege access, image scanning, slow builds and cold starts, health checks and restarts, surprise bills | 6 |
| 13 | Where to Go from Here | Kubernetes and what it's for, platform engineering, what to skip for now | 3 |

## Appendices

A. Docker Cheat Sheet · B. CI and Terraform Cheat Sheet · C. Glossary · Index (5 pages)

**Total:** about 96 pages
