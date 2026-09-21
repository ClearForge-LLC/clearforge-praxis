# Restore Drill — roadmap

> **This document is an illustration.** Restore Drill is not a real system. Copy
> the phase shape, the exit gates, and the numbering discipline; the work itself
> is invented.

**Status:** 2026-08-11. **Supersedes nothing.** Read `architecture.md` first.
**Author:** the architect · **Gate:** the owner.

---

## 1. How this document works

Phases are **dependency-ordered, not calendar-ordered.** No dates are assigned,
because a build done in whatever hours are available should be measured by gate
completion, not by a schedule that will be wrong.

Every phase carries four things: a **goal** in one sentence, its **dependencies**,
its **work orders**, and an **exit gate** that is objectively verifiable. A phase
is done when its gate passes, not when the code is written.

This document introduces no invariants. Those live in `northstar.md` and are
cited by number. A roadmap that asserts a new constraint is a defect.

**The divergence rule:** deviations are recorded as dated amendments in §8, and
reconciled in §7 once plan and build diverge. Undocumented drift is a defect, not
a shortcut.

## 2. Work-order numbering

Scheme is `RDRL-WO-PSNN[a]` — project prefix, phase, subsection, number within
subsection, optional letter for an inserted refinement pass. **The scheme itself
is defined in this skill's `SKILL.md`; it is cited here, not redefined**, because
two definitions of an id scheme drift apart.

Project prefix is `RDRL`. Ids are unique per repository, and the prefix is what
keeps a cross-project reference unambiguous once two projects reach the same
number.

Legacy ids are never renumbered. This project has none, being new; a project
adopting the scheme partway through keeps its old ids as written and applies the
scheme going forward, recording the changeover here.

## 3. Critical path at a glance

```
P0 ──> P1 ──> P2 ──> P3
              │
              └──> P4 (parallel from P2)
```

- **Risk concentrates in P2**, the comparison logic. Everything before it is
  plumbing that fails loudly; P2 is where a bug produces a *confident wrong
  answer*, which is the failure mode the whole project exists to prevent. It gets
  the most review and the adversarial pass.
- **P4 runs in parallel with P2 and P3** — the dashboard depends only on the
  verdict schema fixed at the end of P1.
- **Human-track, not code:** the backup store's IAM policy has to be narrowed by
  whoever owns that account, and the paging rota needs an owner before P3's gate
  can pass. Both are the most likely things to block delivery while everyone
  stares at code, so they are named here rather than discovered late.

## 4. Phase map

| Phase | Name | Ends when |
|---|---|---|
| P0 | Scratch and safety | A restore runs into disposable scratch with read-only credentials |
| P1 | One honest drill | One artifact restores and produces one durable verdict |
| P2 | The comparison | Verdicts distinguish a good restore from a subtly bad one |
| P3 | Unattended and loud | Failure and staleness both page a human |
| P4 | The one-look answer | Someone uninvolved can answer "is our data recoverable" |

## 5. Sequenced work orders

### P0 — Scratch and safety

**Goal:** make it possible to restore something without endangering anything.
**Depends on:** nothing.

**Work orders**

- `RDRL-WO-0001` — spike, then STOP: scratch container lifecycle, and confirm the
  narrowed IAM policy actually blocks writes.
- `RDRL-WO-0002` — scratch provisioning and teardown.
- `RDRL-WO-0003` — read-only credential path.

**Exit gate**

- `aws s3api put-object` with the drill's credentials returns `AccessDenied`.
- A drill run leaves zero scratch containers behind: `docker ps -a --filter
  name=drill-scratch` prints no rows.

### P1 — One honest drill

**Goal:** one artifact, restored end to end, with a verdict that survives a
reboot.
**Depends on:** P0.

**Work orders**

- `RDRL-WO-0101` — artifact selection.
- `RDRL-WO-0102` — restore execution and exit-status handling.
- `RDRL-WO-0102a` — refinement: treat stderr-on-success correctly (see
  `architecture.md` §5). Inserted after `WO-0102` and sorting beside it, which is
  why the refinement marker is a suffix rather than a leading digit.
- `RDRL-WO-0103` — spike: legacy-format archives.
- `RDRL-WO-0104` — append-only verdict store.

**Exit gate**

- A drill against the largest artifact writes exactly one verdict row naming a
  resolvable artifact id, and the row survives a service restart.
- Re-running the same drill writes a second row and edits no existing row.

### P2 — The comparison ⚠ highest risk

**Goal:** a verdict that can tell a good restore from a subtly bad one.
**Depends on:** P1.

**Work orders**

- `RDRL-WO-0201` — declared checks: table presence, row counts within tolerance,
  canary records.
- `RDRL-WO-0202` — comparison against the live source of truth, not the archive.

**Exit gate**

- With a row corrupted in the source after backup, the drill returns FAIL
  (northstar invariant 4's falsification, run as a test).
- With an intact archive, the drill returns PASS on three consecutive runs.

### P3 — Unattended and loud

**Goal:** nobody has to remember to look.
**Depends on:** P2. Human-track: paging rota owner.

**Work orders**

- `RDRL-WO-0301` — scheduling and the concurrency lock.
- `RDRL-WO-0302` — failure paging.
- `RDRL-WO-0303` — staleness detection.

**Exit gate**

- With the scheduler stopped, the verdict goes red inside the staleness window
  and a page arrives (northstar invariant 3's falsification, run as a test).
- Two drills started simultaneously result in one run and one skip, not two runs.

### P4 — The one-look answer

**Goal:** the answer is available without reading logs.
**Depends on:** P1 (verdict schema only). Runs in parallel with P2 and P3.

**Work orders**

- `RDRL-WO-0401` — verdict dashboard.

**Exit gate**

- Someone who has not worked on this can state the current verdict and the
  artifact it came from, without assistance, in under a minute.

## 6. Standing cadence

Every work order inherits: spike first on anything novel, then stop for review;
one pull request per work order, left unmerged; an adversarial pass before the
feedback document; and no number faked — a blocked measurement is reported as
blocked with the harness that would produce it later.

## 7. Reconciliation — plan versus built

Empty at inception. Once what was built diverges from what was planned, it gains
rows of **number as built → what it actually was → what was planned**, and
history is left as written. The table explains the divergence; it does not erase
it.

| number as built | what it actually was | what the roadmap had planned |
|---|---|---|
| — | — | — |

Run a reconciliation audit at every phase boundary: count what was planned, what
merged, and what did not, and confirm the gap is deliberate. It is cheap at a
boundary and expensive at the end.

## 8. Amendments

| Date | Section | Change | Rationale |
|---|---|---|---|
| 2026-08-11 | — | Initial version | Seed |

## 9. Provenance

Written as the illustrative example shipped with this skill, 2026-08-11. Rests on
`northstar.md` and `architecture.md`.
