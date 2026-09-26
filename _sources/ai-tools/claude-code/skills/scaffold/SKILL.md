---
name: scaffold
description: >-
  Generate a new module, component, endpoint, service, or class that matches the
  codebase's existing structure. Use whenever the user wants to create a new unit
  of a kind that already exists in the repo — "scaffold a new module for X",
  "create another endpoint like the others", "add a new component", "set up a new
  service". Produces boilerplate that looks like it belongs: same layout, naming,
  imports, wiring, and a stub test.
---

# Scaffold

Create the skeleton of a new thing so it's indistinguishable in shape from its siblings — then the
user (or you) fills in the real logic.

## Workflow

1. **Find a sibling** — an existing module/component/endpoint of the same kind. It is your template.
2. **Mirror its shape:** file location and name, internal structure, imports, the public
   interface, how errors/logging are handled, and how it gets **wired in** (route registration,
   module export, dependency injection, config entry).
3. **Generate the new unit** with the specifics swapped in and clear `TODO` markers where real
   logic goes.
4. **Wire it up** the same way its siblings are wired — a scaffold that isn't registered is dead code.
5. **Add a stub test** matching the repo's test convention, so the loop is closed from the start.

Don't introduce a new framework, folder convention, or style. The value of a scaffold is that it
*matches* — a new file that follows local convention is immediately reviewable and obviously correct.
