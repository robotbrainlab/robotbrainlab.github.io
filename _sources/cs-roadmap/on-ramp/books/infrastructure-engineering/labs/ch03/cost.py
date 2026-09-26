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
