# The Cloud: Renting Computers by the Minute

This chapter explains what "the cloud" actually sells: three ways to rent computing power, regions and zones, the building blocks every app uses (compute, storage, and networking), and how the bill is calculated. The lab is a small Python cost model, because in the cloud every design decision is also a pricing decision.

*The problem.* I don't own a server, and buying one feels wrong.

*The question.* How do I get a computer on the internet without buying one, and what exactly am I paying for?

## Renting Instead of Buying

You could buy a car to get to the airport twice a year, or take a taxi. The taxi costs more per kilometre, but you pay only when you ride and someone else fixes the engine. Owning servers is owning the car: you pay up front, you buy enough for your busiest day so the machine is mostly idle, and a disk failing at 3 a.m. is your problem.

The cloud is the taxi. You rent on-demand: ask for a machine and get it in about a minute, then give it back and stop paying. You can also grow and shrink as traffic changes, which is called elasticity. The price per hour is higher than owning, but you never pay for the idle years.

Renting also splits the work. Under the **shared responsibility model**, the provider secures the buildings, the hardware, and its own services. You secure what you put on top: your code, your data, your settings, and who gets access. Most cloud security incidents happen on the customer's side of that line, usually through a setting left open.

## Three Ways to Rent: IaaS, PaaS, and Serverless

Think of pizza: make it at home, rent an equipped kitchen and cook it yourself, have a bakery bake your recipe, or buy one slice only when you're hungry.

| | You manage | The provider manages | Examples |
|---|---|---|---|
| Your own servers | Everything, including the building | Nothing | A server in your office |
| IaaS | OS, runtime, app, data | Hardware, network, buildings | AWS EC2, Google Compute Engine |
| PaaS | App and data | Also the OS, runtime, scaling | Render, Heroku, Google Cloud Run |
| Serverless | Just your functions | Also servers, scaling to zero | AWS Lambda, Azure Functions |

**Infrastructure as a Service (IaaS)** rents you virtual machines, disks, and networks. You get a bare Linux machine and do everything else: updates, containers, security. It is the most flexible option and the most work.

**Platform as a Service (PaaS)** runs your code or container image for you: "run this image with 512 MB of memory and send it traffic". The platform handles the machines, restarts crashes, and adds copies when traffic grows.

**Serverless** goes further: the provider runs your code only when a request or event arrives. The best-known form is function as a service (FaaS), where each request runs one function. When nothing happens, nothing runs, and you pay nothing. The catch is the cold start: if your function hasn't run for a while, the first request waits while it starts, from a fraction of a second to several seconds.

> **Note:** Containers fit all three. You can run them yourself on an IaaS machine, hand them to a PaaS, and several serverless services accept container images too. That is one reason this book starts with containers.

## Regions and Zones

A **region** is a geographic area, such as Frankfurt or Mumbai, containing several data centres. Pick one close to your users, because distance adds delay, and one where the law allows your data to live.

Inside each region are several **availability zones**. A zone is one or more data centres with their own power, cooling, and network, a few kilometres from the others. A fire or power cut in one zone should not affect the others.

```text
  Region: eu-central (Frankfurt)
  ┌──────────────────────────────────────────────────┐
  │ ┌────────────┐   ┌────────────┐   ┌────────────┐ │
  │ │   Zone a   │   │   Zone b   │   │   Zone c   │ │
  │ │ app copy 1 │   │ app copy 2 │   │  (spare)   │ │
  │ └────────────┘   └────────────┘   └────────────┘ │
  │   each zone: own power, cooling, and network     │
  └──────────────────────────────────────────────────┘
```

To survive a zone failing, run copies of your app in at least two zones. Surviving a whole region failing, which is rare, needs two regions and is well beyond this book.

## Compute: Where Code Runs

Compute is the cloud's word for processing power, in the three shapes you just met:

- An instance is a virtual machine you rent (IaaS). You choose an instance type, a fixed size such as "2 virtual CPUs and 4 GB of memory", and a starting disk image with an operating system on it.
- A container service (PaaS) runs your images and adds or removes copies as needed.
- A function service (serverless) runs your code per request.

## Storage: Where Data Lives

Apps store three kinds of thing, and the cloud has a different service for each:

| Kind | What it is | Good for |
|---|---|---|
| Block storage | A virtual disk attached to one machine | The operating system, a database's files |
| **Object storage** | Files ("objects") stored by name in buckets, read and written over HTTP | Uploads, images, backups, logs |
| Managed database | A database the provider runs and backs up for you | Your app's records |

Object storage is the least like your laptop: no folders, no disk to mount. You send "store these bytes as `photos/cat.jpg` in bucket `uploads`" and later "give me `photos/cat.jpg`". In return it is cheap, practically endless, and very durable. Amazon's version, S3, is so common that other products copy its interface, which is how you'll try it locally in Chapter 7.

## Networking: How Traffic Reaches It

Just enough networking first. Every machine on a network has an IP address, such as `10.0.1.5`, which works like a street address. One machine runs many programs, so each program that accepts connections listens on a numbered **port**, like a flat number in a building. A web app might listen on port 8000; a PostgreSQL database uses port 5432.

A cloud network is built from a few pieces:

- A **virtual private cloud** (VPC) is your own private network inside the provider, split into subnets. A public subnet can be reached from the internet; a private one cannot, which is where databases belong.
- A **firewall** decides which traffic may pass: for example, "allow port 443 from anyone, and allow port 5432 only from the app's machines". Many clouds call these rules security groups.
- A **load balancer** is the front door. It receives all incoming requests and spreads them across healthy copies of your app, skipping any that stop answering.

Picture a gated community: the VPC is the wall, the firewall is the guard with a list of who may enter, and the load balancer is the receptionist sending each visitor to a free desk.

## Paying for What You Use

Every cloud service has a meter. The common units are:

| Unit | Example |
|---|---|
| Time running | $0.02 per hour for a small instance, billed by the second |
| Storage held | $0.023 per GB per month in object storage |
| Requests | $0.20 per million function calls |
| Data sent out | Egress, around $0.09 per GB leaving the provider |

(These are round example figures. Real prices vary by provider, region, and year.)

Two things surprise every beginner. The meter runs whether or not anyone uses the thing, so a forgotten test machine costs the same as a busy one. And small prices multiply: a tiny per-request price can become the biggest line on the bill at high traffic.

> **Warning:** Cloud bills have no upper limit by default. Before you create anything in a real account, set a budget alert (Chapter 7) and learn how to delete what you create (Chapter 8).

## Lab: Pay-per-Use on Paper (and in Python)

You'll compare two ways to pay for the same small app: one small instance running all month, or serverless functions billed per request. The prices are round example numbers, not any provider's real price list.

1. Create `~/infra-labs/ch03/cost.py`:

   ```python
   """Compare two ways to pay for the same small app.

   The prices are round example numbers, close to what big clouds
   charge, but not any provider's real price list.
   """

   HOURS_PER_MONTH = 730

   # Option 1: a small virtual machine that runs all month.
   VM_PRICE_PER_HOUR = 0.02

   # Option 2: serverless, billed per request and per unit of work.
   PRICE_PER_MILLION_REQUESTS = 0.20
   PRICE_PER_GB_SECOND = 0.0000167
   MEMORY_GB = 0.5          # memory given to each run
   SECONDS_PER_REQUEST = 0.1


   def vm_cost(requests):
       return VM_PRICE_PER_HOUR * HOURS_PER_MONTH  # same price at any traffic


   def serverless_cost(requests):
       per_request = requests / 1_000_000 * PRICE_PER_MILLION_REQUESTS
       work = requests * SECONDS_PER_REQUEST * MEMORY_GB * PRICE_PER_GB_SECOND
       return per_request + work


   print(f"{'requests/month':>15} {'VM':>9} {'serverless':>11}")
   for requests in [10_000, 1_000_000, 10_000_000, 50_000_000]:
       print(f"{requests:>15,} {vm_cost(requests):>9.2f} "
             f"{serverless_cost(requests):>11.2f}")
   ```

   A GB-second is one gigabyte of memory held for one second, the usual way serverless work is measured.

2. Run it:

   ```bash
   cd ~/infra-labs/ch03 && python3 cost.py
   ```

   ```text
    requests/month        VM  serverless
            10,000     14.60        0.01
         1,000,000     14.60        1.03
        10,000,000     14.60       10.35
        50,000,000     14.60       51.75
   ```

3. Find the break-even point. Change the list of request counts to `[14_000_000, 15_000_000]` and run it again:

   ```text
    requests/month        VM  serverless
        14,000,000     14.60       14.49
        15,000,000     14.60       15.53
   ```

4. Put the list back, change `MEMORY_GB` to `1.0`, and run it once more. The 10-million row now shows `18.70` for serverless, above the instance's `14.60`.

**Expected results:** serverless is almost free at low traffic and grows in a straight line with use; the instance costs the same at any traffic. With these prices they cross at about 14 million requests a month, and giving each function twice the memory makes serverless roughly twice as expensive per request. The lesson isn't which option wins. It's that you can, and should, work the numbers out before you build.

## Summary, Key Terms, and Review Questions

### Summary

- The cloud rents computing on demand. You pay more per hour than owning, but never for idle capacity, and you can grow and shrink quickly.
- The provider secures the platform; you secure what you put on it.
- IaaS rents machines, PaaS runs your app or container, and serverless runs your functions per request, with cold starts as the trade-off.
- Regions are places; availability zones are separate data centres within a region. Spread copies across zones to survive one failing.
- Apps use compute, storage (block, object, database), and networking (VPCs, subnets, firewalls, load balancers).
- Everything has a meter, including data sent out. Small prices multiply.

### Key Terms

| Term | Meaning |
|---|---|
| Shared responsibility model | The provider secures the platform; you secure what you put on it |
| Infrastructure as a Service (IaaS) | Renting virtual machines, disks, and networks |
| Platform as a Service (PaaS) | A service that runs your code or container for you |
| Serverless | Running code only when events arrive, without managing servers |
| Region | A geographic area containing a provider's data centres |
| Availability zone | An independent data centre (or group) within a region |
| Object storage | Files stored by name in buckets and used over HTTP |
| Port | A number that picks which program on a machine receives traffic |
| Virtual private cloud (VPC) | Your private network inside a cloud |
| Firewall | Rules that decide which network traffic may pass |
| Load balancer | The front door that spreads requests across healthy copies |

### Review Questions

1. Why is renting from the cloud usually cheaper than owning for a small app, even though the hourly price is higher?
2. Explain IaaS, PaaS, and serverless using the pizza picture.
3. What is a cold start, and which kind of service has it?
4. Why run copies of an app in two availability zones?
5. When would you use object storage instead of block storage?
6. In the lab, at roughly what traffic did the instance become cheaper than serverless?

> **You understand this when** you can look at a new cloud service and say whether it is compute, storage, or networking, and what its meter counts.
