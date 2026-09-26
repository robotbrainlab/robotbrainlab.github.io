---
name: api-design
description: >-
  Design (or review) an API contract between systems. Use whenever the user is
  defining an interface others will call — "design the API for X", "what endpoints
  should this have", "design the REST interface", "how should we version/paginate
  this API", "what should the error responses look like". Designs along the five
  contract dimensions and produces concrete endpoints plus an OpenAPI sketch, with
  the decisions that are hard to change made deliberately.
---

# API Design

An API is a contract, and a contract is harder to change than code because it breaks everyone on
the other side. Design the things that age badly — URLs, versioning, error shape — on purpose.

## The five dimensions to pin down

1. **Shape** — REST/JSON by default (simple, cacheable, universal); GraphQL/gRPC/events only with
   a concrete reason.
2. **Versioning** — how it changes without breaking callers (additive = safe; removals/renames =
   a new version, e.g. `/v2`). Plan graceful deprecation.
3. **Identity** — how callers authenticate (API key, OAuth, mTLS).
4. **Authorization** — what each identity may do.
5. **Failure** — consistent error shape, correct status codes (4xx caller, 5xx server), no leaked
   internals.

## Design checklist

- **Resources as nouns**, not actions (`/notes/41`, not `/getNote`). Plural collections, hierarchy
  for relationships.
- **Methods + idempotency:** GET safe; PUT/DELETE idempotent; POST is not — use an **idempotency
  key** for safe-retry creates.
- **Pagination** on every collection — prefer **cursor/keyset** over offset for scale. Decide it
  before anyone depends on the endpoint (adding it later is a breaking change).
- **One error shape** everywhere (`{"error": "...", "code": ...}`).
- **Write it down** as an **OpenAPI** sketch — the single source of truth both sides agree to.

## Output

A list of endpoints (method · path · purpose · request/response shape), the versioning + pagination
+ error conventions, and an OpenAPI fragment. Show good vs bad where a choice is non-obvious.
