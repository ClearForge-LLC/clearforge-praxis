# Writing `docs/northstar.md`

**Read `SKILL.md` first** — shared rules (§5) and numbering (§6) apply and are not
repeated. **Worked example: `assets/example/docs/northstar.md`**; every
illustration below comes from it.

**Trust this file less than the other two.** Of nine repositories surveyed,
exactly one had a northstar, days old and unproven by use; a second had a document
*called* a north star that was half architecture. The rest is back-derived from
northstar-shaped content stranded inside architecture docs. Where the human's
judgement conflicts with this file, prefer theirs.

---

## 1. Purpose

Answers **why this exists and what must stay true**, in terms surviving a total
stack change. Shortest of the three, and the only one whose contents require
re-ratification to change. Written once at inception, before any architecture —
its job is to make the architecture's decisions *constrained* rather than free.

**The hardest part is getting it written at all.** Eight of nine surveyed projects
never had one. Make the first pass cheap and explicitly permit a short one: a good
one sentence plus six real invariants beats a thorough document that never gets
written. Offer the short version rather than negotiating scope.

## 2. Required sections

1. Status line — date, author, gate, builder, what to read next
2. The one sentence
3. The problem, stated precisely
4. End state, with at least one concrete walkthrough
5. **Invariants** — the section the document exists for
6. Non-goals, each with its reason
7. What would make this a failure
8. Amendments
9. Provenance

8 and 9 are the most-omitted and the cheapest. They are what make the document
maintainable rather than disposable.

## 3. The one sentence

Stack-independent. If it cannot be written, the project is not understood well
enough to design.

> **Restore Drill proves that a backup can actually be restored, by restoring it —
> on a schedule, without a human, and loudly enough that a failure cannot be
> mistaken for silence.**

It names the capability, then the two constraints shaping every downstream
decision (unattended, loud on failure). No language, no database, no vendor. Test
yours by imagining the stack replaced entirely — if the sentence changes, it is an
architecture summary wearing a northstar's clothes.

## 4. The problem

Not "X is hard" — what specifically fails today, with evidence. **Cite real
incidents where they exist.** The example cites a backup set green for fourteen
months that failed when finally needed, and lands it: *"The checks were measuring
the backup job, not the backup."*

**A problem statement with a scar in it is worth ten that are reasoned.** Hunt the
scar — past work orders, issue history, incident records — before settling for a
general argument. Where there is no real incident, say so; a fabricated scar is
worse than an honest abstraction, because it gets repeated as fact.

Where the real insight is *why existing tooling didn't already solve this*, give it
a subsection. The example's: the backup tool's `--verify` proves the archive is
internally consistent and nothing about whether the data reconstitutes — *"the
capability gap was never 'can we read the file'"*. Most projects have such a
paragraph; most documents omit it.

## 5. Invariants

Not a preference or a best practice. **A thing that, if violated, means the system
is wrong regardless of whether it works.**

- **Number them.** Work orders cite by number; unnumbered invariants cannot be
  cited and therefore erode. One surveyed project stated five as unnumbered
  bullets while its architecture numbered nine — the unnumbered set was cited by
  nothing.
- **State the failure, not the rule.** *"Fail closed"* is a slogan. *"Failure to
  run is reported as failure, never silence; no completed drill inside the
  staleness window turns the verdict red"* is checkable.
- **Mark the one that is the project.** Usually one invariant is the reason the
  project exists. The example's invariant 1 carries *"This invariant is the
  project."*
- **Six to eight.** Twenty is a design document in costume; three means the hard
  ones were not found.

## 6. Falsifiability — the claim table

The strongest pattern in the corpus: a numbered table with a falsification column.

| # | Invariant | How to falsify |
|---|---|---|
| 1 | A backup is proven only by a completed restore and a passed check against it. *This invariant is the project.* | Find any backup reported "verified" for which no restore ran end to end |
| 2 | The drill holds no credential that can write to production. | Attempt a production write with the drill's credentials; success falsifies |
| 4 | The verdict compares restored data against the source of truth, not the archive it came from. | Corrupt a row in the source after backup; a drill that still passes falsifies |

**An invariant no one can test is a wish.** The column's real job is collapsing the
vague ones: if you cannot write it, you found an aspiration. It also pays off
downstream — several of the example's falsifications become literal exit gates in
its roadmap, so an invariant written this way arrives at the build already knowing
how it will be proven.

Where falsification is not yet runnable, say what harness would make it so. Never
write a column entry you know to be untestable.

## 7. Non-goals

Each carries its reason, because **the reason is what stops it being relitigated
every third work order.**

**The strongest name a tempting-but-wrong solution:**

> **Taking backups.** A system that both takes and verifies backups can hide a
> shared assumption in both halves. The verifier has to be able to fail the backup
> system, which it cannot do if it is the backup system.

That prevents a whole class of future argument. "Retention — out of scope"
prevents nothing; someone proposes it in six weeks and nobody remembers why not.

## 8. What would make this a failure

Inverted success criteria — catches the case where every box is ticked and the
project still missed. The example's work because each is plausible rather than
catastrophic: it reports green while no restore has succeeded in weeks; it becomes
so slow the schedule widens until it means nothing; its failures are noisy enough
that people close the page unread.

## 9. Anti-patterns

- **Aspiration instead of constraint.** "Fast, reliable, secure" constrains
  nothing. If its negation is absurd, it is not an invariant.
- **Stack decisions leaking in.** Naming a library, vendor, or protocol means it
  belongs in the architecture.
- **Growth.** A northstar at architecture length has become a second architecture.
  It must stay short enough to re-read whole before every work order — that is its
  delivery mechanism. The corpus had one at 349 lines and one at 100; the long one
  is the one nobody re-read.
- **Skipping it because the project is small.** The default failure. The short
  version is always available.

## 10. Acceptance

- One sentence exists and is stack-independent.
- Invariants numbered, each falsifiable, one marked as the project's reason for
  existing; six to eight, or a stated reason otherwise.
- Every non-goal has a reason; at least one names a tempting-but-wrong solution.
- Problem section cites specific evidence, or says plainly it has none.
- Nothing would change if the stack changed.
- Amendments and Provenance present.
