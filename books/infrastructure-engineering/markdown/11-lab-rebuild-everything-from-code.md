# Lab: Rebuild Everything from Code

In this lab Terraform builds a complete small system: tinyapp, a PostgreSQL database, a private network between them, and a volume for the data. Then you change it, "lose the server", get it all back with one command, and finally destroy and recreate everything, learning on the way what code can rebuild and what it can't.

*The problem.* My server died. Can I get it all back in five minutes?

*The question.* If everything is described in code, can I delete it all and rebuild it with one command?

## What You'll Build

```text
            your machine, port 8090
                     │
 ┌───────────────────┼─ network: tinyapp-net ──────────────┐
 │                   ▼                                     │
 │  ┌──────────────────────┐      ┌─────────────────────┐  │
 │  │ tinyapp-web          │ ───► │ tinyapp-db          │  │
 │  │ localhost:5001/      │ 5432 │ postgres:16-alpine  │  │
 │  │   tinyapp:1.0.0      │      └──────────┬──────────┘  │
 │  └──────────────────────┘                 │             │
 └───────────────────────────────────────────┼─────────────┘
                                             ▼
                                volume: tinyapp-db-data
```

Six resources: two images, two containers, one network, one volume. The app image is the `1.0.0` you pushed in Chapter 9, so the registry must be running. If `curl localhost:5001/v2/tinyapp/tags/list` doesn't list `1.0.0`, build and push it from the book's `labs/tinyapp/` folder with `docker build -t localhost:5001/tinyapp:1.0.0 .` and `docker push localhost:5001/tinyapp:1.0.0`. This system uses port 8090 and its own names, so it doesn't disturb Chapter 10's `tinyapp` on port 8080.

## Step 1: Describe the System

Create `~/infra-labs/ch11/main.tf`. It starts like Chapter 8's file, then declares two inputs:

```hcl
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 4.6"
    }
  }
}

provider "docker" {}

variable "app_version" {
  type    = string
  default = "1.0.0"
}

variable "db_password" {
  type      = string
  sensitive = true
}
```

A **variable** is an input to a configuration. `app_version` has a default. `db_password` has none, so Terraform must be given it, and `sensitive = true` stops Terraform printing it. Terraform reads any environment variable called `TF_VAR_<name>`, so the password never has to be written in a file.

Next, the network, the volume, and the two images:

```hcl
resource "docker_network" "lab" {
  name = "tinyapp-net"
}

resource "docker_volume" "db_data" {
  name = "tinyapp-db-data"
}

resource "docker_image" "postgres" {
  name         = "postgres:16-alpine"
  keep_locally = true
}

resource "docker_image" "app" {
  name         = "localhost:5001/tinyapp:1.0.0"
  keep_locally = true
}
```

The database container joins the network, keeps its files in the volume, and has a health check. `wait = true` makes Terraform wait until the container is healthy before moving on:

```hcl
resource "docker_container" "db" {
  name  = "tinyapp-db"
  image = docker_image.postgres.image_id
  env = [
    "POSTGRES_USER=tinyapp",
    "POSTGRES_PASSWORD=${var.db_password}",
    "POSTGRES_DB=tinyapp",
  ]

  networks_advanced {
    name = docker_network.lab.name
  }

  volumes {
    volume_name    = docker_volume.db_data.name
    container_path = "/var/lib/postgresql/data"
  }

  healthcheck {
    test     = ["CMD", "pg_isready", "-U", "tinyapp"]
    interval = "2s"
    retries  = 10
  }
  wait = true
}
```

Finally, the app and an output:

```hcl
resource "docker_container" "app" {
  name  = "tinyapp-web"
  image = docker_image.app.image_id
  env = [
    "APP_VERSION=${var.app_version}",
    "DATABASE_URL=postgresql://tinyapp:${var.db_password}@${docker_container.db.name}:5432/tinyapp",
  ]

  networks_advanced {
    name = docker_network.lab.name
  }

  ports {
    internal = 8000
    external = 8090
  }
  wait = true
}

output "url" {
  value = "http://localhost:8090"
}
```

`${docker_container.db.name}` is a reference inside the database address. It gives the app the database's name on the network, and it tells Terraform to create the database first. `wait = true` here waits for the image's own `HEALTHCHECK` from Chapter 9. An **output** is a value Terraform prints after `apply` and shows again with `terraform output`.

## Step 2: Build It

```bash
cd ~/infra-labs/ch11
export TF_VAR_db_password=change-me-locally
terraform init
terraform plan
```

```text
…
  # docker_container.app will be created
  # docker_container.db will be created
  # docker_image.app will be created
  # docker_image.postgres will be created
  # docker_network.lab will be created
  # docker_volume.db_data will be created
…
Plan: 6 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + url = "http://localhost:8090"
```

(These lines are picked out of a longer plan.) Apply it, answering `yes`. Putting `time` in front measures how long it takes:

```bash
time terraform apply
```

```text
…
docker_network.lab: Creation complete after 2s [id=309f6b4865e3…]
docker_container.db: Creating...
docker_container.db: Creation complete after 4s [id=0506b66e5fb6…]
docker_container.app: Creating...
docker_container.app: Creation complete after 6s [id=19b358f8dfa7…]

Apply complete! Resources: 6 added, 0 changed, 0 destroyed.

Outputs:

url = "http://localhost:8090"
```

It took about 12 seconds; `time` adds its own lines, which differ between shells. Notice the order: Terraform created the network, volume, and images together, then the database, and only when the database was healthy, the app. Try it:

```bash
curl localhost:8090/health
curl localhost:8090/visits
curl localhost:8090/visits
```

```text
{"status":"ok","version":"1.0.0"}
{"visits":1}
{"visits":2}
```

The count is now stored in PostgreSQL.

## Step 3: Change Something

In `main.tf`, change the default of `app_version` from `"1.0.0"` to `"1.1.0"`, and plan:

```text
  # docker_container.app must be replaced
…
      ~ env                                         = (sensitive value) # forces replacement
…
Plan: 1 to add, 0 to change, 1 to destroy.
```

Only the app container changes. Its environment is shown as `(sensitive value)` because it contains the password. Apply it, and Terraform destroys and re-creates just that container.

```bash
curl localhost:8090/health
curl localhost:8090/visits
```

```text
{"status":"ok","version":"1.1.0"}
{"visits":3}
```

A new app container, and the count carried on, because it lives in the database, not in the app.

## Step 4: The Server Dies

Simulate losing the machine's containers and network all at once:

```bash
docker rm -f tinyapp-web tinyapp-db
docker network rm tinyapp-net
```

`curl localhost:8090/health` now fails with a connection error: nothing is listening any more.

Ask Terraform what it thinks:

```bash
terraform plan
```

```text
Note: Objects have changed outside of Terraform
…
  # docker_container.db has been deleted
…
  # docker_network.lab has been deleted
…
  # docker_container.app will be created
  # docker_container.db will be created
  # docker_network.lab will be created
…
Plan: 3 to add, 0 to change, 0 to destroy.
```

Terraform compared its state with reality, found what was missing, and plans to put back exactly that. Apply it:

```bash
time terraform apply
```

```text
…
Apply complete! Resources: 3 added, 0 changed, 0 destroyed.
```

About 14 seconds later:

```bash
curl localhost:8090/visits
```

```text
{"visits":4}
```

Everything is back, and so is the data, because the volume was never deleted. That is the answer to the chapter's question: yes, in seconds, provided the data survives.

## Step 5: Destroy and Recreate from Nothing

Now remove everything Terraform manages, volume included, answering `yes`:

```bash
terraform destroy
```

```text
Plan: 0 to add, 0 to change, 6 to destroy.
…
docker_volume.db_data: Destruction complete after 2s
docker_network.lab: Destruction complete after 2s
Destroy complete! Resources: 6 destroyed.
```

Build it again from nothing:

```bash
terraform apply
curl localhost:8090/visits
```

```text
…
Apply complete! Resources: 6 added, 0 changed, 0 destroyed.
…
{"visits":1}
```

The whole system is back in about 12 seconds, but the count starts again at 1. The code described an empty database, and that is what you got.

> **Warning:** Infrastructure as code rebuilds infrastructure, not data. Data needs backups, stored somewhere else, and restores that you have actually tested. In a real cloud, managed databases take the backups for you; your job is to switch them on and try a restore.

## Step 6: Protect the Data from Yourself

Terraform can refuse to destroy a resource. Add a `lifecycle` block to the volume:

```hcl
resource "docker_volume" "db_data" {
  name = "tinyapp-db-data"

  lifecycle {
    prevent_destroy = true
  }
}
```

and try `terraform destroy` again:

```text
Error: Instance cannot be destroyed
…
Resource docker_volume.db_data has lifecycle.prevent_destroy set, but the
plan calls for this resource to be destroyed.
…
```

Nothing was destroyed. Use this for anything whose loss would hurt: databases, buckets, volumes.

## Step 7: See Where the Password Went

The password never appeared in `main.tf` or on screen. But look in the state file:

```bash
grep -c change-me-locally terraform.tfstate
```

```text
2
```

It is stored there twice, in plain text. This is why state must never go into git, and why teams keep it in encrypted, access-controlled remote state.

To finish, remove the `lifecycle` block, then run `terraform destroy` and answer `yes`.

## Summary, Key Terms, and Review Questions

### Summary

- One Terraform configuration can describe a whole system: images, containers, a network, and a volume, with references deciding the order.
- Variables take inputs such as passwords from `TF_VAR_` environment variables; outputs print useful values.
- A change replaces only what it must. Data kept in a volume or database survives app replacements.
- When things vanish, `plan` detects it and `apply` rebuilds exactly what is missing, in seconds.
- Code rebuilds infrastructure, not data. Back data up, and use `prevent_destroy` for anything precious.
- State stores secrets in plain text; keep it private.

### Key Terms

| Term | Meaning |
|---|---|
| Variable (Terraform) | An input to a Terraform configuration |
| Output (Terraform) | A value Terraform prints after applying |

### Review Questions

1. How does Terraform know to create the database before the app?
2. After the "server died", how did Terraform decide what to create, and why was the data still there?
3. What does `prevent_destroy` protect against, and what doesn't it protect against?
4. Where did the database password end up, even though it was never in a file?

> **You understand this when** you can delete every container and network of a system without worrying, because you know exactly what one `terraform apply` will bring back, and what it won't.
