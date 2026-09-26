# Infrastructure as Code

Your app is packaged and your pipeline automated. The last manual part is the infrastructure itself. This chapter describes it in files that Terraform reads and builds: providers, resources, `plan`, `apply`, and state. In the lab, Terraform creates, changes, repairs, and deletes a container.

*The problem.* I clicked 40 buttons to build this, and I can't do it again.

*The question.* How do I write my infrastructure down so that a tool can build it the same way every time?

## Clicks Don't Repeat

Clicking through a console is fine for exploring and bad for anything you need to keep. Nobody remembers the 40 clicks or can review them, and when you need a second copy for staging, you start from zero.

Builders don't construct a house from memory. They work from a blueprint that anyone can read, check, copy, and correct. **Infrastructure as code** (IaC) is the blueprint approach: you describe your servers, networks, databases, and permissions in text files, keep those files in git next to your app, and let a tool create exactly what they describe. You get:

- *Repeatability.* Staging and production are built from the same files.
- *Review.* A change to the infrastructure is a change to a file, so a colleague can read it before it happens.
- *History.* Git shows who changed what, when, and why.
- *Disposability.* If you can rebuild it in minutes, you can also delete it without fear.

## Declarative: Say What, Not How

You can tell a taxi driver "take me to the station", or you can give every turn yourself. The first is **declarative**: you describe the destination and let the expert find the route. The second is imperative: you list the steps.

Terraform is declarative: you write "there should be a container like this", and it compares that with what exists and makes only the changes needed. Run it twice and the second run does nothing, because nothing differs.

## Terraform

Terraform is the most widely used IaC tool. You write its files in HCL (HashiCorp Configuration Language), a simple language of blocks and `name = value` settings, in files ending in `.tf`.

Terraform itself knows nothing about clouds. A **provider** is a plugin that knows how to talk to one system's API: AWS, Azure, Google Cloud, GitHub, or, for this book's labs, your local Docker. A **resource** is one thing a provider manages, such as a VM, a bucket, or a container.

Here is a complete configuration that runs the nginx web server in a container:

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

resource "docker_image" "web" {
  name         = "nginx:alpine"
  keep_locally = true
}

resource "docker_container" "web" {
  name  = "tf-web"
  image = docker_image.web.image_id

  ports {
    internal = 80
    external = 8081
  }
}
```

The `terraform` block says which provider to download: `kreuzwerker/docker`, any 4.x version from 4.6. The `provider` block configures it; empty means "use the local Docker". Each `resource` block has a type (`docker_container`) and a name you choose (`web`).

The line `image = docker_image.web.image_id` is a reference: the container uses an attribute of the image resource. References tell Terraform the order: the image must exist before the container. You never write the order yourself.

`keep_locally = true` stops Terraform deleting the image from your machine on destroy.

## The Workflow: init, plan, apply, destroy

| Command | What it does |
|---|---|
| `terraform init` | Downloads the providers and prepares the folder. Run once, and after changing providers |
| `terraform plan` | Compares the files with reality and shows what would change. Changes nothing |
| `terraform apply` | Shows the plan again, asks for `yes`, then makes the changes |
| `terraform destroy` | Deletes everything this configuration manages, after asking |

A **plan** marks each resource with a symbol: `+` create, `~` update in place, `-` destroy, and `-/+` destroy and re-create, which Terraform does when a setting can't be changed on a live resource. Read the plan every time. It is your last chance to catch "1 to destroy" before it happens.

## State

After `apply`, Terraform writes a file called `terraform.tfstate`. This **state** is Terraform's notebook: which real object belongs to which resource block, with its ID and attributes. On the next run, Terraform reads the notebook, asks the provider what really exists, and compares both with your files.

If someone changes or deletes something by hand, reality no longer matches the files. That difference is called **drift**, and the next `plan` shows it and offers to put things back.

> **Warning:** State can contain secrets, such as database passwords, in plain text. Never commit `terraform.tfstate` to git, and never edit it by hand. Teams keep it in remote state: a shared, access-controlled location, such as a storage bucket, with a lock so two people can't apply at once.

## Lab: Your First Terraform

1. Create `~/infra-labs/ch08/main.tf` with the configuration above, then initialise the folder:

   ```bash
   cd ~/infra-labs/ch08
   terraform init
   ```

   ```text
   Initializing the backend...

   Initializing provider plugins...
   - Finding kreuzwerker/docker versions matching "~> 4.6"...
   - Installing kreuzwerker/docker v4.6.0...
   - Installed kreuzwerker/docker v4.6.0 (self-signed, key ID 0DCE698927DAF8EC)
   …
   Terraform has been successfully initialized!
   ```

   `init` also writes `.terraform.lock.hcl`, which pins the exact provider version. Commit it.

2. Check the file and preview the changes:

   ```bash
   terraform validate
   terraform plan
   ```

   ```text
   Success! The configuration is valid.

   …
     # docker_container.web will be created
     + resource "docker_container" "web" {
         + name                                        = "tf-web"
   …
     # docker_image.web will be created
     + resource "docker_image" "web" {
   …
   Plan: 2 to add, 0 to change, 0 to destroy.
   ```

3. Apply it. Terraform shows the plan again and asks for confirmation; type `yes`. The first time, it also downloads the nginx image:

   ```bash
   terraform apply
   ```

   ```text
   …
     Enter a value: yes

   docker_image.web: Creating...
   docker_image.web: Creation complete after 0s [id=sha256:1ed1b0e1d765…nginx:alpine]
   docker_container.web: Creating...
   docker_container.web: Creation complete after 1s [id=c5c48da6fc2e…]

   Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
   ```

4. Check the result and the state:

   ```bash
   curl -s localhost:8081 | grep title
   terraform state list
   ```

   ```text
   <title>Welcome to nginx!</title>
   docker_container.web
   docker_image.web
   ```

5. Run `terraform plan` again. Nothing differs, so nothing would change:

   ```text
   No changes. Your infrastructure matches the configuration.
   …
   ```

6. Change `external = 8081` to `8082` in `main.tf`, and plan:

   ```text
     # docker_container.web must be replaced
   -/+ resource "docker_container" "web" {
   …
             ~ external = 8081 -> 8082 # forces replacement
   …
   Plan: 1 to add, 0 to change, 1 to destroy.
   ```

   A running container's ports can't be changed, so Terraform will replace it. Run `terraform apply` and type `yes`.

7. Cause drift by deleting the container behind Terraform's back, then plan and apply:

   ```bash
   docker rm -f tf-web
   terraform plan
   ```

   ```text
     # docker_container.web will be created
   …
   Plan: 1 to add, 0 to change, 0 to destroy.
   ```

   After `terraform apply`, `curl localhost:8082` answers again.

8. Delete everything, typing `yes` when asked:

   ```bash
   terraform destroy
   ```

   ```text
   Plan: 0 to add, 0 to change, 2 to destroy.
   …
   docker_container.web: Destruction complete after 0s
   docker_image.web: Destroying... [id=sha256:1ed1b0e1d765…nginx:alpine]
   docker_image.web: Destruction complete after 0s

   Destroy complete! Resources: 2 destroyed.
   ```

**Expected results:** `plan` previews without changing anything; `apply` creates the image and container; a second plan finds no changes; changing the port forces a replacement; a container deleted by hand is detected and re-created; and `destroy` removes it all (the nginx image stays on disk because of `keep_locally`).

## Summary, Key Terms, and Review Questions

### Summary

- Infrastructure as code describes infrastructure in files kept in git, so it can be rebuilt, reviewed, and versioned.
- Terraform is declarative: you describe the result, and it works out the changes.
- Providers talk to systems; resources are the things they manage; references set the order.
- `init`, `plan`, `apply`, and `destroy` are the whole workflow. Always read the plan.
- State records what Terraform built. Drift is reality differing from the files. State can hold secrets, so keep it out of git.

### Key Terms

| Term | Meaning |
|---|---|
| Infrastructure as code (IaC) | Describing infrastructure in files that a tool builds from |
| Declarative | Describing the result you want, not the steps to get there |
| Provider | A Terraform plugin that manages one system through its API |
| Resource | One thing a provider manages |
| Plan | Terraform's preview of the changes it would make |
| State | Terraform's record of what it built |
| Drift | Differences between reality and the configuration |

### Review Questions

1. Name three problems with building infrastructure by clicking in a console.
2. What does "declarative" mean, and why does running `terraform apply` twice change nothing the second time?
3. How does Terraform know to create the image before the container?
4. What do `+`, `~`, and `-/+` mean in a plan?
5. Why must `terraform.tfstate` stay out of git?

> **You understand this when** you can read a Terraform plan and predict exactly what will be created, replaced, or destroyed before you type `yes`.
