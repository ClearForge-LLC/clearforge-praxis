# Writing `docs/roadmap.md`

**Read `SKILL.md` first** — shared rules (§5) and work-order numbering (§6) apply
and are not repeated. The numbering scheme is defined there; cite it, do not
restate it. **Worked example: `assets/example/docs/roadmap.md`**; every
illustration below comes from it.

**Evidence base:** one mature example of 756 lines, one build backlog embedded in
an architecture, and one document called a roadmap that was really a backlog — six
deferred intentions, no phases, no dependencies, no gates. That last one matters:
because it was *called* a roadmap, nothing surfaced that the project had no
sequencing artifact at all.

---

## 1. Purpose

Answers **in what order, and how we know a phase is done.** It sequences against
the northstar's invariants and the architecture's shape, and introduces neither.

The failure it prevents is subtle: without exit gates, "done" is decided by
whoever is tired. Everything below serves the gate.

**Required sections:** status line · how this document works · work-order
numbering (cite `SKILL.md` §6; state the `PREFIX` and, for existing projects, the
legacy-id rule) · critical path (§3) · phase map · sequenced work orders ·
standing cadence · reconciliation (§4) · Amendments.

## 2. Phases are dependency-ordered, not calendar-ordered

Take this verbatim, including the reason: **no dates are assigned, because a build
done in whatever hours are available should be measured by gate completion, not by
a schedule that will be wrong.**

Every phase carries a **goal** (one sentence), **depends on** (hard
prerequisites), **work orders**, and an **exit gate**.

**The exit gate is the highest-value element in the entire set.** It converts "we
think we finished" into a checkable fact:

| Not a gate | A gate |
|---|---|
| Core is solid | A drill run leaves zero scratch containers: `docker ps -a --filter name=drill-scratch` prints no rows |
| Auth works | `aws s3api put-object` with the drill's credentials returns `AccessDenied` |
| The comparison is reliable | With a row corrupted in the source after backup, the drill returns FAIL |

The test: **could someone who was not in the room run this and get an unambiguous
yes or no?** If checking needs the author's judgement, it is not a gate.

Note where the example's gates come from — several are the *falsification column*
of a northstar invariant, run as a test. An invariant written falsifiably arrives
here already knowing how it will be proven; that is the cheapest route to a real
gate.

**Every phase should end at a working, more-capable system.** If it cannot, it is
two phases or the wrong cut.

## 3. The critical path

A diagram — ASCII is fine — plus three annotations only the strongest document in
the corpus had:

- **Where risk concentrates.** The example names P2, the comparison logic, because
  everything before is plumbing that fails loudly while P2 is where a bug produces
  a *confident wrong answer* — the failure the project exists to prevent. Naming
  it early is how it gets the review it needs.
- **What runs in parallel.** The example notes P4 depends only on the verdict
  schema.
- **What is human-track, not code.** Filings, policy changes, account access,
  rotas, purchases, copy. These are **the most likely things to block delivery
  while everyone stares at code.** Ask explicitly what non-code work the project
  depends on — the answer is never "none" and is rarely volunteered.

## 4. Scoping later phases, and reconciliation

**Only phases whose shape is known get scoped to work-order level.** Later ones
are stated as intent with the spike that will shape them named. Pre-writing
distant phases in work-order detail feels productive and is the most common way a
roadmap goes stale on the day it is written.

Once reality diverges, add a table mapping **number as built → what it actually
was → what was planned**:

| number as built | what it actually was | what the roadmap had planned |
|---|---|---|
| `WO-011A` | form affordances added from use | — (P1 addition, unplanned) |
| `WO-035` | auth enforced at the database | — (arose from WO-030's finding) |

**History is left as written.** The table explains the divergence; it does not
erase it.

One project audited its own numbering after its owner asked whether anything had
fallen through — *"78 numbers planned, 49 merged, 41 unmerged, and most of the 41
are not missing"* — finding one genuinely dropped item and three more while
looking. **Prompt this at every phase boundary:** cheap there, expensive at launch.

## 5. Anti-patterns

- **Dates.** They will be wrong and they convert a planning tool into a debt.
- **A backlog wearing a roadmap's name.** A queue of deferred intentions with no
  phases, dependencies, or gates is a useful document but not a roadmap — and
  calling it one means the project has no sequencing artifact and nobody notices.
- **Exit gates that are not checkable.**
- **Reusing a phase number on amendment.** The corpus has a roadmap with two P4
  sections and a scattered P5, from later work appended under spent numbers.
- **Introducing invariants.** They belong to the northstar; a roadmap asserting a
  new constraint is a defect. Raise it there and cite the number.
- **Omitting human-track work.**
- **Renumbering legacy ids.** See `SKILL.md` §6; state the rule in the document
  itself for existing projects.

## 6. Acceptance

- Every phase has a goal, dependencies, work orders, and an objectively verifiable
  exit gate.
- No dates.
- Critical path names risk concentration, parallelism, and human-track work.
- Numbering section states the `PREFIX`, cites `SKILL.md` §6 rather than redefining
  the scheme, and states the legacy rule for existing projects.
- No phase number appears twice; Amendments present.
- Only phases whose shape is known are scoped to work-order level; the rest name
  the spike that will shape them.
