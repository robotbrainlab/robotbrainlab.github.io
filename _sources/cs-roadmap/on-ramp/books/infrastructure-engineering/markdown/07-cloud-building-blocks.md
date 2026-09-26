# Cloud Building Blocks

A cloud provider's menu is enormous, but a small app uses only a handful of dishes: accounts and access control, virtual machines, object storage, managed databases, firewalls, serverless functions, and cost alerts. In the lab you run an S3-compatible object store locally and give an app a key that can do only what it needs.

*The problem.* The cloud console has 200 services, and I need three.

*The question.* Which few building blocks does a small app actually need, and how do I use them safely?

## The Few You Actually Need

A console is the provider's website for managing things by clicking, and it lists hundreds of services. For a small web app, this short list covers nearly everything:

| Need | Building block |
|---|---|
| Who may do what | Accounts and IAM |
| Somewhere to run code | A virtual machine, a container service, or functions |
| Somewhere to keep files | Object storage |
| Somewhere to keep records | A managed database |
| Control over who can connect | Firewalls |
| No surprises on the bill | Budgets and cost alerts |

## Accounts and IAM

When you sign up, you get an account: the container for everything you create and pay for. The login you signed up with is the **root user**, and it can do anything, including closing the account. Protect it with multi-factor authentication (MFA), a second proof such as a code from your phone, and don't use it for daily work.

**Identity and access management** (IAM) decides who may do what. Picture a hotel key card that opens your room and the gym, but not other rooms or the safe. IAM hands out key cards:

- An IAM user is a person or program with long-term credentials.
- A **role** is a set of permissions that a machine or service takes on, receiving short-lived credentials automatically. An app on a cloud VM should use a role, not a stored password.
- A **policy** is a document listing what is allowed: which actions, on which resources.

Here is a policy that allows reading and writing objects in one bucket, called `uploads`, and nothing else:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": ["arn:aws:s3:::uploads/*"]
    }
  ]
}
```

Anything not explicitly allowed is denied. `arn:aws:s3:::uploads/*` is how AWS names "every object in the bucket `uploads`".

The rule behind good IAM is **least privilege**: give each person and program only the permissions it needs. If the app's key leaks, the thief can touch only the app's own bucket.

Programs that can't use a role sign their requests with an **access key**: a pair of a key ID (like a username) and a secret key (like a password).

> **Warning:** Leaked access keys are the most common way cloud accounts get abused. Never commit them to git, never put them in an image, and prefer roles, whose credentials expire on their own.

## Virtual Machines

Launching a VM means choosing a region, a disk image (such as Ubuntu Linux), an instance type, firewall rules, and an SSH key, which proves it's you when you open a terminal on it. A minute later you can log in, install Docker, and run your container as on your laptop. A *stopped* VM still pays for its disk; only a *terminated* (deleted) one costs nothing.

## Object Storage

New buckets are private: only identities with permission can read them. Keep it that way; a bucket accidentally made public is one of the most common causes of data leaks.

Many products speak S3's interface, including MinIO, a storage server you can run yourself. In the lab, MinIO plays the cloud's object storage, and `boto3`, the official AWS library for Python, talks to it exactly as it would to S3.

> **Note:** MinIO no longer publishes ready-made images for its free edition, so the lab uses free builds of its open-source code from Chainguard: `cgr.dev/chainguard/minio` and `cgr.dev/chainguard/minio-client`.

## Managed Databases

A **managed database** is a database, such as PostgreSQL, that the provider installs, updates, backs up, and can copy to a second availability zone. You connect with a host name, port, user, and password as usual. It costs more than running PostgreSQL yourself, and for almost every small team it's worth it. Keep it in a private subnet, reachable only by the app.

## Firewalls

In the cloud, firewall rules are usually called security groups: lists of what may come in, attached to machines or databases. Everything not listed is blocked.

| Rule | Why |
|---|---|
| Allow port 443 from anywhere to the load balancer | Users reach the app over HTTPS |
| Allow port 8000 from the load balancer to the app | Only the front door talks to the app |
| Allow port 5432 from the app to the database | Only the app talks to the database |
| Allow port 22 (SSH) from your own IP address only | Nobody else can even try to log in |

> **Warning:** "Allow 0.0.0.0/0" means "allow the whole internet". Automated scanners find open database and SSH ports within minutes of them appearing.

## Serverless Functions

A function service runs your code whenever an event happens: an HTTP request, a file landing in a bucket, a nightly timer. There is nothing to patch and nothing to pay while it's idle, but functions have a maximum run time (often 15 minutes) and cold starts. They shine for glue work, such as resizing each uploaded image.

## Cost Alerts

Before you create anything in a real account, create a budget alert: in the billing section, set a monthly amount, say $10, and ask for an email at 50%, 80%, and 100% of it, or when the forecast says you'll pass it. An alert doesn't stop spending; it tells you in time to stop it yourself. Label what you create, so the bill shows what each thing costs, and delete experiments when you're done.

## Lab: Least Privilege with Local Object Storage

You'll run MinIO, create two buckets, and give an "app" an access key that can read and write one bucket only. Then you'll prove what it can and cannot do.

1. Create a folder and a private network, and start MinIO with a volume for its data:

   ```bash
   mkdir -p ~/infra-labs/ch07 && cd ~/infra-labs/ch07
   docker network create cloudlab
   docker run -d --name minio --network cloudlab -p 9000:9000 \
     -v minio-data:/data \
     -e MINIO_ROOT_USER=admin -e MINIO_ROOT_PASSWORD=change-me-please \
     cgr.dev/chainguard/minio server /data
   ```

   `admin` is MinIO's root user, like the cloud account's owner.

2. The MinIO client, `mc`, is the admin tool. It runs in a container on the same network, so define a small shell function that runs it for you. `MC_HOST_local` tells it where the server is and how to log in, and `"$@"` passes along whatever you type after `mc`:

   ```bash
   mc() {
     docker run --rm --network cloudlab -v "$PWD":/work -w /work \
       -e MC_HOST_local=http://admin:change-me-please@minio:9000 \
       cgr.dev/chainguard/minio-client "$@"
   }
   ```

3. Create two buckets, and put a "private" file in one of them:

   ```bash
   printf 'name,amount\nAsha,1200\n' > report.csv
   mc mb local/uploads
   mc mb local/billing
   mc cp report.csv local/billing/
   mc ls local
   ```

   ```text
   Bucket created successfully `local/uploads`.
   Bucket created successfully `local/billing`.
   `/work/report.csv` -> `local/billing/report.csv`
   …
   [2026-09-26 14:38:42 UTC]     0B billing/
   [2026-09-26 14:38:42 UTC]     0B uploads/
   ```

4. Save the policy from "Accounts and IAM" as `uploads-only.json`. Create it in MinIO, create a user for the app, and attach the policy:

   ```bash
   mc admin policy create local uploads-only uploads-only.json
   mc admin user add local app-uploader uploader-secret-123
   mc admin policy attach local uploads-only --user app-uploader
   ```

   ```text
   Created policy `uploads-only` successfully.
   Added user `app-uploader` successfully.
   Attached Policies: [uploads-only]
   To User: app-uploader
   ```

   In MinIO, the user name and password serve as the access key ID and secret key.

5. Create a virtual environment, install `boto3`, and save this as `s3_demo.py`:

   ```bash
   python3 -m venv .venv && . .venv/bin/activate && pip install boto3==1.43.103
   ```

   ```python
   """Use object storage the way an app would: with a limited access key."""
   import os

   import boto3
   from botocore.exceptions import ClientError

   s3 = boto3.client(
       "s3",
       endpoint_url="http://localhost:9000",
       aws_access_key_id=os.environ["S3_ACCESS_KEY"],
       aws_secret_access_key=os.environ["S3_SECRET_KEY"],
       region_name="us-east-1",
   )


   def read(bucket, key):
       return s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode()


   def attempt(label, action):
       try:
           result = action()
       except ClientError as error:
           print(f"DENIED  {label}: {error.response['Error']['Code']}")
           return
       print(f"OK      {label}", result if isinstance(result, (str, list)) else "")


   attempt("upload uploads/hello.txt",
           lambda: s3.put_object(Bucket="uploads", Key="hello.txt", Body=b"hi!"))
   attempt("read uploads/hello.txt", lambda: read("uploads", "hello.txt"))
   attempt("read billing/report.csv", lambda: read("billing", "report.csv"))
   attempt("delete uploads/hello.txt",
           lambda: s3.delete_object(Bucket="uploads", Key="hello.txt"))
   attempt("list all buckets",
           lambda: [bucket["Name"] for bucket in s3.list_buckets()["Buckets"]])
   ```

6. Run it with the app's limited key:

   ```bash
   S3_ACCESS_KEY=app-uploader S3_SECRET_KEY=uploader-secret-123 python3 s3_demo.py
   ```

   ```text
   OK      upload uploads/hello.txt
   OK      read uploads/hello.txt hi!
   DENIED  read billing/report.csv: AccessDenied
   DENIED  delete uploads/hello.txt: AccessDenied
   DENIED  list all buckets: AccessDenied
   ```

7. Run it again with the root credentials (`S3_ACCESS_KEY=admin S3_SECRET_KEY=change-me-please`). Every line now says `OK`: the root user reads the report, deletes the upload, and lists `['billing', 'uploads']`.

8. Try reading the private file with no credentials at all:

   ```bash
   curl -s -o /dev/null -w '%{http_code}\n' http://localhost:9000/billing/report.csv
   ```

   ```text
   403
   ```

9. Clean up:

   ```bash
   docker rm -f minio && docker volume rm minio-data && docker network rm cloudlab
   ```

**Expected results:** the app's key can put and get objects in `uploads`, and nothing else, not even deleting its own upload or listing buckets; the root user can do everything; and an anonymous request gets `403 Forbidden`, because buckets are private by default.

## Summary, Key Terms, and Review Questions

### Summary

- A small app needs identity, compute, storage, a database, firewalls, and a budget.
- Lock the root user away with MFA. Policies decide who may do what; prefer roles to stored keys, and grant least privilege.
- A VM costs money until it is terminated; buckets are private by default; managed databases buy you tested backups.
- Firewalls block everything not listed. Never open databases or SSH to the whole internet. Budget alerts warn you before the bill does.

### Key Terms

| Term | Meaning |
|---|---|
| Root user | An account's all-powerful owner login |
| Identity and access management (IAM) | The service that decides who may do what |
| Role | Permissions taken on with short-lived credentials |
| Policy | A document listing allowed actions on resources |
| Least privilege | Giving each identity only the permissions it needs |
| Access key | A key ID and secret a program signs requests with |
| Managed database | A database the provider runs and backs up |

### Review Questions

1. Why should you not use the root user for everyday work?
2. How do an IAM user and a role differ, and which should an app on a VM use?
3. Write the firewall rules for an app behind a load balancer, with a database.
4. Does a budget alert stop spending? What should you do when one arrives?

> **You understand this when** you can write a policy that gives a program exactly one bucket.
