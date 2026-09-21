# Restore Drill — north star

> **This document is an illustration.** Restore Drill is not a real system. It
> exists to show what these documents look like when they are done properly, and
> it is the only worked example this skill ships. Copy the shape, not the
> content.

**Status:** ratified 2026-08-11. **Supersedes nothing.** Read before `architecture.md`.
**Author:** the architect · **Gate:** the owner · **Builder:** a separate build session.

---

## 1. The one sentence

**Restore Drill proves that a backup can actually be restored, by restoring it —
on a schedule, without a human, and loudly enough that a failure cannot be
mistaken for silence.**

Note what the sentence does: it names the capability, then the two constraints
that shape every decision downstream (unattended, and loud on failure). It names
no language, no database, no cloud. Test yours the same way — if replacing the
entire stack would change the sentence, it belongs in the architecture.

## 2. The problem, stated precisely

Backups are verified today by checking that the backup job exited zero and that
the archive is the size we expected. Both checks pass for an archive that cannot
be restored.

The scar: a nightly backup set reported green for fourteen months. When it was
finally needed, the restore failed — the schema had drifted, and the dump had
been written with a flag that silently excluded one table. Every check that
existed had passed, every night, for fourteen months. **The checks were measuring
the backup job, not the backup.**

A problem statement with a specific failure in it is worth ten that are reasoned.
Where the project has a real incident, cite it. Where it does not, say so rather
than inventing one.

### Why the existing tooling did not already solve this

The backup tool ships a `--verify` flag. It reads the archive back and confirms
it is internally consistent — which proves the file is not corrupt, and proves
nothing about whether the data in it reconstitutes a working system. The
capability gap was never "can we read the file." It was that **nobody had ever
run the last step**, because the last step needs somewhere to restore *to*.

## 3. End state

Someone who has not thought about backups in a month can answer "is our data
recoverable?" in one look, and the answer is grounded in a restore that actually
happened.

Concretely: at 02:00 the drill picks one backup from the last seven days at
random, restores it into a scratch database, runs the declared checks against it
— row counts within tolerance of the source, every declared table present, three
canary records byte-identical — destroys the scratch database, and writes a
verdict. If it passes, a dashboard tile stays green. If it fails, or if no drill
has completed in 48 hours, someone is paged.

## 4. Invariants — true regardless of what any work order asks

Numbered, because work orders cite them by number and an uncitable invariant
erodes. Each carries the observation that would disprove it: an invariant nobody
can test is a wish, and writing the falsification column is what collapses the
ones that were only aspirations.

| # | Invariant | How to falsify |
|---|---|---|
| 1 | A backup is proven only by a completed restore and a passed check against it. Archive-integrity checks are evidence, never a verdict. *This invariant is the project.* | Find any backup reported "verified" for which no restore ran end to end |
| 2 | The drill holds no credential that can write to production. Read-only to the backup store, read-write to scratch, nothing else. | Attempt a production write using the drill's credentials; success falsifies |
| 3 | Failure to run is reported as failure, never as silence. No completed drill inside the staleness window turns the verdict red. | Stop the scheduler; if the verdict is still green past the window, this fails |
| 4 | The verdict compares restored data against the source of truth, not against the archive it came from. | Corrupt a row in the source after backup; a drill that still passes falsifies |
| 5 | Scratch is destroyed after every drill, pass or fail. | List scratch resources after a run; anything surviving falsifies |
| 6 | A drill never mutates the artifact it is testing. The backup store is mounted read-only. | Check the mount flags and the store's audit log for writes from the drill |
| 7 | Every verdict names the exact artifact it restored. "Backups are fine" is not a verdict. | Read any verdict; one lacking a resolvable artifact id falsifies |

Seven is inside the working range of six to eight. Twenty would be a design
document wearing an invariant costume; three usually means the hard ones were
not found.

## 5. Non-goals — deliberately not built

Each carries the reason it is excluded, because the reason is what stops it being
relitigated every third work order.

- **Taking backups.** A system that both takes and verifies backups can hide a
  shared assumption in both halves — the fourteen-month failure above was exactly
  that. The verifier has to be able to fail the backup system, which it cannot do
  if it is the backup system.
- **Restoring into production.** Recovery is a different job with a different
  blast radius, run by a human under pressure. Sharing code between a drill and a
  real recovery means the drill's conveniences become the recovery's hazards.
- **Retention and lifecycle management.** Deciding what to keep is a policy
  question; this answers an evidence question.
- **Verifying application behaviour on restored data.** The drill proves the data
  came back. Whether the app is happy with it is a larger question and a
  different test suite.

The strongest non-goals name a tempting-but-wrong solution — the first two do.
"Retention — out of scope" would prevent nothing; someone proposes it in six
weeks and no one remembers why not.

## 6. What would make this a failure

- It reports green while a restore has not succeeded in weeks.
- It is so slow or expensive that the schedule gets widened until it means
  nothing.
- Its failures are noisy enough that people learn to close the page unread.
- It becomes a path from the backup store into production.

## 7. Amendments

| Date | Section | Change | Rationale |
|---|---|---|---|
| 2026-08-11 | — | Initial version | Seed |

## 8. Provenance

Written as the illustrative example shipped with this skill, 2026-08-11. Rests on
nothing outside this document set; every figure in it is invented for teaching.
