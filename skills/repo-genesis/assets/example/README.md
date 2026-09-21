# Restore Drill

> **This README is an illustration**, shipped with this skill to show the front
> door's shape. Restore Drill is not a real system.

Proves that a backup can actually be restored, by restoring it — on a schedule,
without a human, and loudly enough that a failure cannot be mistaken for silence.

**Status:** in build, phase P1 of 5. Not yet running unattended.

## Where to go

| I want to know | Read |
|---|---|
| Why this exists and what must stay true | [`docs/northstar.md`](docs/northstar.md) |
| What it is and how it is shaped | [`docs/architecture.md`](docs/architecture.md) |
| What order it gets built in, and what "done" means | [`docs/roadmap.md`](docs/roadmap.md) |

## Running it

```bash
drill run --artifact latest    # one drill, prints the verdict
drill status                   # current verdict and its age
```

---

Note what this README does **not** do: it does not list the invariants, restate
the architecture, or describe the phases. Every one of those facts has exactly one
home, and a copy here would be a fourth place for the same thing to drift. The
front door points; it does not define. What lives here is what a stranger needs in
the first thirty seconds — what this is, whether it works yet, and where to go
next.
