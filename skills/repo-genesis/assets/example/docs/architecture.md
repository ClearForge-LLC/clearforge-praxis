# Restore Drill — architecture

> **This document is an illustration.** Restore Drill is not a real system, and
> every measurement below is invented to show the shape of a real one. Copy the
> structure and the habits, not the numbers.

**Status:** 2026-08-11. **Supersedes nothing.** Read `northstar.md` first.
**Author:** the architect · **Gate:** the owner.

---

## 1. How to use this document

This is the source of truth for what is being built and why each choice was made.
Implementation detail belongs in work orders; this document constrains them. The
roadmap tracks sequence; this tracks shape.

**The divergence rule:** any deviation from this document is recorded as a dated
amendment in §10 with its rationale. Undocumented drift is a defect, not a
shortcut.

Invariants are **not** defined here. They live in `northstar.md` and are cited
below by number.

## 2. Ground truth — measured, not assumed

Measured before anything was designed. The commands are cited so a reader can
re-run them rather than trust the number.

- Backup store holds 34 archive sets, 08:12 GB largest, 41 GB total
  (`aws s3 ls --summarize --human-readable s3://backups/pg/`).
- Largest archive restores into a scratch instance in 6m 12s, measured three
  times, spread 5m 58s – 6m 31s (`time pg_restore -d scratch …`).
- The scheduler host has 240 GB free (`df -h /var`).
- The backup store's IAM policy currently grants `s3:PutObject` to the role the
  drill was going to reuse (`aws iam get-role-policy …`).

### 2.1 Corrections to earlier assumptions

The wrong belief is the instructive half — it shows where the reasoning was weak,
so record both rather than quietly replacing one with the other.

| Assumed | Measured |
|---|---|
| Restores take "about an hour", so the drill must run weekly | 6m 12s for the largest set — a nightly drill is affordable, which changed the whole cadence design |
| The backup store is already read-only to automation | The intended role can write to it, violating northstar invariant 2 before a line was written |
| Scratch can reuse the staging database | Staging has a modified schema; a restore there would compare against the wrong source of truth and pass falsely |
| Archives are all one format | Three of 34 are from the pre-migration tool and need a different restore path |

The staging-database correction is the load-bearing one: reusing staging was the
obvious cheap choice, and it would have produced a drill that passed while
proving nothing.

**Blocked, not faked.** Restore time for the three legacy-format archives is
unmeasured — the old tool is not installed on the scheduler host. Reported as
blocked; `RDRL-WO-0103` installs it and produces the number. No estimate is
recorded in its place, because a plumbing measurement dressed as a quality
measurement is worse than none.

## 3. Shape — three parts and two seams

```
  scheduler ──> drill runner ──> scratch instance
                     │
                     └──> verdict store ──> dashboard / pager
```

- **Scheduler** decides when a drill runs and nothing else.
- **Drill runner** selects an artifact, restores it, runs the checks, destroys
  scratch, writes one verdict.
- **Verdict store** is append-only. A verdict is never edited; a re-run writes a
  new one.

**Seams that are security boundaries**, named as such because a seam that is only
a module boundary and a seam that is a trust boundary get maintained differently:

- **Drill runner → backup store** is a trust boundary. Read-only, enforced by the
  store's own policy, not by the runner's good behaviour (northstar invariant 2).
- **Drill runner → scratch** is a blast-radius boundary. Scratch is disposable
  and network-isolated from production (invariants 5 and 6).

The scheduler → runner seam is neither; it is an ordinary internal call.

## 4. Ratified rulings

Each carries its reason, because a table of bare verdicts is a list of things
nobody can defend six weeks on.

| Question | Ruling | Reason |
|---|---|---|
| Scratch environment | A container started per drill and destroyed after | Reuse invites state from the previous drill to mask a failure in this one |
| Where read-only is enforced | At the store's IAM policy, not in runner code | Invariant 2 must survive a bug in the runner; a check the runner performs on itself is not a boundary |
| Comparison target | The live source of truth, sampled at drill start | Comparing against the archive's own manifest proves only that the archive agrees with itself |
| Verdict storage | Append-only, one row per drill | A mutable verdict cannot answer "was this green last Tuesday", which is the question asked after an incident |
| Legacy-format archives | Do not decide yet — spike it (`RDRL-WO-0103`) | Prior: a second restore path is cheaper than a migration. Held loosely; the spike may show the three archives are past retention and the question is moot |
| Alert transport | **Departure from the house default of email** — use the paging service | Email fails silently into a filter, and invariant 3 requires failure to be loud. Recorded as a departure so it is not later mistaken for drift |

## 5. Runtime and deployment

Runs as a scheduled unit on the scheduler host. One drill at a time, enforced by
a lock file — two concurrent drills would contend for the scratch name and the
second would fail in a way that looks like a restore failure.

Operational gotcha worth writing down: the restore emits to stderr on success as
well as failure, so exit status is the only reliable signal. Anything parsing its
output for the word "error" will report false failures nightly.

## 6. Security posture

The drill's value comes from touching real backup data, which is also its risk.
The posture that follows: it holds no production write credential (invariant 2),
scratch is network-isolated, and the verdict records artifact ids rather than
restored content, so the verdict store never becomes a second copy of the data.

## 7. Traceability

None — this project has no governing standard. Recorded explicitly rather than
omitted, so a reader knows the question was asked and answered rather than
skipped.

## 8. Open questions

Each names a decider and what it blocks. None of these is written as
`(PLACEHOLDER)`, because a placeholder says nothing and ages invisibly, while an
open question is a debt with a name.

- **How many canary records, and chosen how?** Decider: the owner. Blocks the
  check definition in `RDRL-WO-0201`; does not block P0 or P1.
- **Do the three legacy archives still need to be restorable?** Decider: the
  owner, informed by the `RDRL-WO-0103` spike. Blocks P1's exit gate.
- **Staleness window — 48 hours or 24?** Decider: the owner. Blocks nothing;
  48 is in place and cheap to change.

## 9. What this document does not cover

Work-order-level implementation detail, and sequence. Sequence lives in
`roadmap.md`; this document constrains the order without setting it.

## 10. Amendments

| Date | Section | Change | Rationale |
|---|---|---|---|
| 2026-08-11 | — | Initial version | Seed |

New sections continue the sequence and never reuse a number, even when an
amendment logically belongs beside an existing section. Numbers get cited from
commits, work orders, and sometimes code comments; reusing one silently
invalidates every citation, with nothing to catch it.

## 11. Provenance

Written as the illustrative example shipped with this skill, 2026-08-11. Rests on
`northstar.md`. Every measurement in §2 is invented for teaching.
