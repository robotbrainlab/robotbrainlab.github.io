# CI and Terraform Cheat Sheet

## GitHub Actions and act

| Key or command | Meaning |
|---|---|
| `on:` | Events that start the workflow |
| `jobs.<id>.runs-on:` | The runner a job uses |
| `needs:` | Run this job only after the named jobs succeed |
| `uses:` / `with:` | Run a ready-made action / give it inputs |
| `run:` | Run shell commands (`run: \|` starts a block of several lines) |
| `env:` | Environment variables for the workflow, a job, or a step |
| `${{ secrets.NAME }}` | A secret, masked as `***` in logs |
| `${{ github.sha }}`, `$GITHUB_SHA` | The commit hash being built |
| `concurrency: NAME` | Never run two workflows in the same group at once |
| `act -l`, `act push` | List the jobs; run the workflows as if you had pushed (`-v` for detail) |
| `.actrc`, `.secrets` | act's default options; its secrets, one `NAME=value` per line (keep out of git) |

## Terraform Commands

| Command | What it does |
|---|---|
| `terraform init` | Download providers and prepare the folder |
| `terraform validate` | Check the files for mistakes |
| `terraform plan` | Show what would change: `+` create, `~` update, `-` destroy, `-/+` replace |
| `terraform apply` | Show the plan, ask for `yes`, and make the changes |
| `terraform destroy` | Delete everything the configuration manages, after asking |
| `terraform state list`, `terraform output` | List what's in the state; print the outputs again |

## Terraform Language

| To do this | Write this |
|---|---|
| Choose a provider | `required_providers` in the `terraform` block, with `source` and `version` |
| Declare a resource | `resource "TYPE" "NAME" { … }` |
| Refer to another resource | `docker_image.app.image_id` (type, name, attribute) |
| Use a variable | `var.app_version`, or `"APP_VERSION=${var.app_version}"` |
| Set a variable from the shell | `export TF_VAR_db_password=…` |
| Hide a variable's value | `sensitive = true` in its `variable` block |
| Print a value after apply | an `output` block with a `value` |
| Refuse to destroy a resource | `lifecycle { prevent_destroy = true }` |
