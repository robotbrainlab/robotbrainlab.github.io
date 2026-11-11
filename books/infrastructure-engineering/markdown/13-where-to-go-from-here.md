# Where to Go from Here

You can now package an app so it runs the same everywhere, ship it through a pipeline that tests, publishes, deploys, and rolls back on its own, and describe the infrastructure in code that rebuilds it in seconds. You have also seen what the cloud sells, how it charges, and how to keep access tight. This short chapter points to what comes next, and what can wait.

## Kubernetes and What It's For

In this book, one machine ran your containers, and a shell script replaced them. That works for one app on one server. With twenty services on fifty machines, someone has to decide which container runs where, restart the ones that fail their health checks, replace them one at a time during a deploy, add copies when traffic grows, and route requests to whichever copies are healthy.

Kubernetes is the system that does this. Like Terraform, it is declarative: you write files saying "run three copies of `tinyapp:1.1.0`, each with 512 MB of memory, healthy when `/health` answers", and Kubernetes keeps reality matching them, forever, across many machines. Every major cloud offers a managed version.

It is powerful, and it is a lot to learn and to run. You need it when you have many services, many machines, and a team to look after them. For one small app, a PaaS or a VM running Docker Compose is simpler, cheaper, and just as reliable. Everything you learned here, from images and health checks to declarative files and rolling deploys, is what Kubernetes is built on, so you'll find it much easier when the time comes.

## Platform Engineering

As companies grow, every product team ends up needing the same things: a Dockerfile, a pipeline, a registry, Terraform for a database, alerts, and secrets. Platform engineering is the practice of building those once, well, as a product for the company's own developers. The result is often called an internal developer platform: ready-made templates, pipelines, and infrastructure modules, so that a developer can go from a new service to production by following a paved path instead of becoming an infrastructure expert first.

The skills in this book are exactly the ones platform engineers use every day.

## What to Learn Next, in This Order

1. *A real cloud, carefully.* Create a free-tier account on one provider, set a budget alert first, and deploy tinyapp to its container service (a PaaS). Then delete it.
2. *Terraform for that cloud.* Recreate the same deployment with Terraform, and keep the state in remote storage.
3. *Observability.* Observability is being able to see inside a running system from the outside, through logs, metrics, and alerts, and it's the missing piece in this book's setup. Learn to answer "is it working, and how do I know?" without logging into a machine.
4. *Networking.* DNS, HTTPS certificates, and load balancers are where many deploys get stuck. *Networking from Zero* covers them.
5. *Linux.* Servers are Linux machines. *Linux and Git from Zero* and *Operating Systems from Zero* go deeper into processes, files, and permissions.
6. *Kubernetes basics,* once you have several services to run.

## What to Skip for Now

- Service meshes, which manage traffic between hundreds of services.
- Multi-cloud and multi-region designs. One cloud, one region, two zones will serve you for a long time.
- Writing your own CI runners, Kubernetes operators, or Terraform providers.
- Chasing every new tool. The ideas in this book (images, pipelines, declarative infrastructure, least privilege, health checks) outlast any single product.

## Cleaning Up the Labs

Chapters 5, 7, 8, and 11 cleaned up after themselves. What is left is the app, the registry, the images you built, and Trivy's cache. `-v` also deletes the registry's storage:

```bash
docker rm -f -v tinyapp registry
docker image ls --format '{{.Repository}}:{{.Tag}}' | grep tinyapp | xargs docker rmi
docker volume rm trivy-cache
```

```text
tinyapp
registry
Untagged: localhost:5001/tinyapp:58fc4c9
Deleted: sha256:32936c85afb2b26ec116bdbd9c6eb2268cad469b4303b5a719cfa61d39444f7d
…
trivy-cache
```

The images you downloaded (Python, PostgreSQL, nginx, MinIO, Trivy, and act's runner) stay; remove any of them with `docker rmi` if you need the disk space.

## A Last Word

The problem at the start of this book was "it works on my machine but breaks on the server, and I don't even own a server". You now know why it breaks, how to make it not break, and how to rent, build, and rebuild the servers with a few commands. The next time something works on your machine, you'll know how to make it work for everyone.
