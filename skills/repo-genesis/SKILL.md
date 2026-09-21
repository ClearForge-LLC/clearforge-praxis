---
name: repo-genesis
description: Give a repository its documentary backbone - README (the front door), docs/northstar.md (why it exists and what must stay true), docs/architecture.md (what it is and how it is shaped), docs/roadmap.md (in what order, and how a phase is known to be done). USE THIS AGGRESSIVELY the moment a project moves from being talked about to being built, even when the request sounds like ordinary writing or planning and names no document at all. Trigger on "fire the genesis docs", "let's fire genesis", "run genesis on this", "genesis this repo", "lay out the repo", "stand up the repo", "set up the new project", "we just finished hashing this out, make it real", "turn this plan into a repo", "flesh this out into something buildable", "scope this so a coding agent can pick it up", "get this on track to be built", "write the architecture", "we need a roadmap", "figure out what order to build this in", "how will we know when a phase is actually done", "what has to stay true here", "what are the invariants", "write the non-goals down", "I want a north star". Fire it immediately after a planning conversation when the human says the idea is ready - do not go hunting for more context first, the conversation is the input. If the deliverable is a repo's foundational planning documents, this skill applies; do not hand-roll them. Also use it to audit or repair existing planning docs: an architecture stuck at (PLACEHOLDER), a roadmap buried inside an architecture, invariants restated divergently in two documents, duplicate section numbers after amendments, a README describing a version that no longer exists, or a repo inherited from someone else that needs to become plannable. Do NOT use for authoring an individual work order, the builder kickoff, or reviewing a parked PR - that is co-architect-work-order. Do NOT use for copyediting an existing README, generating API reference docs, writing a single ADR in an existing set, sprint tickets, a customer-facing product roadmap, or explaining what these documents are.
---

# A repository's documentary backbone

Four documents carry a project from plan to buildable. Written in order, each
constraining the next:

> **README: what this is, and where to go.
> Northstar: why, and what must stay true.
> Architecture: what it is, and how it is shaped.
> Roadmap: in what order, and how we know a phase is done.**

**Write for an agent with no memory of this conversation, months from now.** That
single constraint drives everything here. These are not a record of thinking; they
are durable instructions to someone who was not there.

**Worked example: `assets/example/`** — an invented system, labelled as such,
compliant with every rule below. Read it for the shape of a section rather than a
description of one. Every illustration in this skill and its references comes from
it, so nothing depends on a repo you cannot open.

## 1. The normal case: the plan is the conversation you are in

Usually nothing is written down. You and the human just worked an idea out, and
now it becomes real. **The plan lives in the context window, and the context
window is about to end.** Everything decided either lands in these four documents
or is lost, with no artifact to check against afterwards.

### 1.1 Is there enough to build on

Firing early produces confident documents full of guesses — worse than none,
because they get believed. Three things must hold:

- **The one sentence can be written**, stack-independently. If not, the project
  is not understood well enough to design. Say so and keep talking.
- **A few things that must stay true are known**, and are real constraints rather
  than hopes (§3, `references/northstar.md` §5).
- **The first phase's end state is describable** — not the whole roadmap, just
  what "working and more capable" looks like once.

If one is missing, name it and what would settle it. Genesis is cheap later,
expensive to unwind.

### 1.2 The trap: you were there

**You are the worst-placed author to notice what you left implicit.** Having sat
through the reasoning, a document that merely gestures at a decision reads as
complete to you and as a non-sequitur to whoever picks it up in October. It does
not announce itself — the documents will feel finished.

- **Replay the decisions before writing.** List back what you understood to be
  settled, one line each, and have the human confirm. A conversation has no single
  version of a ruling — it may have been revised three times in an hour, and what
  you remember is usually the version you argued for.
- **Hunt the questions that only *feel* answered.** In a written plan, gaps appear
  as missing sections. In a conversation, a question discussed at length feels
  resolved whether or not it was. **Discussion volume is not resolution.** List
  what is open, name a decider for each, check that list too.

### 1.3 Then

1. **Route each decision through the boundary tests (§3).** This determines
   whether the documents are worth anything.
2. **Measure ground truth before writing the architecture** — read the running
   system, run the commands, record what is there (`references/architecture.md`
   §2). The conversation ran on belief; the corrections are the most valuable
   content you will produce.
3. **Write northstar → architecture → roadmap → README.** Each constrains the
   next: an architecture written without a northstar is a set of free choices, and
   free choices get relitigated.
4. **Write reasons down even when obvious** — they are obvious only to people who
   were in the room. Afterwards these documents are the entire surviving record.

Cite the session and date in Provenance. Where the conversation produced something
worth keeping — a rejected alternative and why, an argument that settled a ruling
— put it in the document. It will not survive elsewhere.

### 1.4 Variants

**A half-formed idea parked as a durable doc**: treat as above, with one addition
— **the doc is an input, not one of the four.** The shortcut is renaming it
`architecture.md` and adding sections, which is precisely how you get a northstar
that is half architecture and a roadmap with no gates: the original had no reason
to separate them. Extract from it, cite it in Provenance, leave it where it is.

**Thin material**: say so rather than padding. A northstar with a good one sentence
and six real invariants, plus an architecture naming what is open and who decides,
beats four complete-looking documents built on guesses.

## 2. Why this exists

Nine repositories were surveyed. These are not carelessness — they are what
happens when each document is invented fresh under time pressure:

| what went wrong | what it looked like |
|---|---|
| Architecture stalled at `(PLACEHOLDER)`, mistaken for a decision | two repos, 73 and 80 lines, unchanged for a fortnight |
| Roadmap written *inside* the architecture | two projects; one's commit message reads "durable roadmap in ARCHITECTURE.md" — deliberate |
| Stack rulings in the northstar | one titled "North-Star *Architecture*", ruling on an SDK and rejecting a named alternative |
| Invariants defined twice, divergently, neither citing the other | nine numbered in the architecture, five unnumbered in the northstar under another heading |
| Amendments reused section numbers | a 1431-line architecture with two §15s and two §16s; its roadmap has two P4s |
| Work-order numbering ran out | ten slots per phase; one phase consumed all ten plus an ad-hoc `011A` |
| README advertising a design that shipped | three of three; one read "pre-build" for a system running in production |
| Every shared section omitted | a triad written by a capable agent in one sitting: no Amendments, no Provenance, no exit gates |

**That last row is the lesson.** The per-document craft was good; what it missed
was the *shared* rules. **Craft is not where compliance fails; boilerplate is.**
Run §10 before calling anything done, even when the prose feels finished.

## 3. Which document does this belong in

Apply in order. Most drift is content sitting one document from home.

1. **True regardless of stack?** Yes → northstar. No → architecture.
2. **Constrains a decision, or records one?** Constrains → northstar (invariant).
   Records → architecture (ruling).
3. **A property of the system, or a step toward it?** Property → architecture.
   Step → roadmap.
4. **Changing it needs re-ratification, or re-planning?** Re-ratification →
   northstar. Re-planning → roadmap.
5. **Needed in a stranger's first thirty seconds?** Yes → README, *as a pointer*
   (§4), never as a definition.

**The canonical confusion is the invariant.** Established in the northstar,
referenced by number in the architecture, restated in slices by each work order —
defined in exactly one place. A roadmap introducing an invariant is a defect; the
one legitimate exception is in §8.

## 4. Placement, naming, the front door

```
README.md
docs/northstar.md
docs/architecture.md
docs/roadmap.md
docs/work-orders/<PREFIX>-WO-PSNN[a].md
```

Lowercase because mixed casing breaks case-sensitive cross-references; `docs/`
because a root holding four planning documents buries the README — the file every
stranger opens first.

**Never rename existing files retroactively.** A rename breaks every link in
commits, PRs, code comments, and external indexes. Where a project deviates, note
it in the document header and move on.

**The README points; it does not define.** What this is, whether it works yet,
where to go next — see `assets/example/README.md`, which closes by naming its own
restraint. Anything more is a fourth copy of a fact another document owns, and
copies drift: a README listing invariants will list them slightly wrong within two
months, and it is the version a stranger reads first. It is also the most reliably
stale file in any repo, because nobody re-reads it. **When you touch any other
document, check the README's status line is still true** — nothing else in the
process performs that check.

## 5. Rules all four inherit

- **Status line**: what this is, date, author, gate (who ratifies), what it
  supersedes, what to read first.
- **Amendments table**, dated, with rationale: *"Undocumented drift is a defect,
  not a shortcut."*
- **Never renumber or reuse a section number.** New sections continue the
  sequence. Not tidiness: in one surveyed project, forty-two source files and
  nineteen test files cite the architecture by invariant and section number, so
  renumbering silently invalidates code comments with nothing to catch it.
  **Assume every number is cited from somewhere you cannot see.**
- **Never `(PLACEHOLDER)` in place of a decision.** Write the open question, who
  answers it, what it blocks. A placeholder says nothing and ages invisibly; an
  open question is a debt with a name.
- **Reasons travel with rulings.** A bare directive does not survive a context
  boundary; the reason does.
- **Measured evidence over assertion.** Say what was run; where nothing was,
  mark it unverified. **Never fake a number** — report a blocked measurement as
  blocked, with the harness that would produce it. A plumbing measurement dressed
  as a quality measurement is worse than none, because it gets believed.
- **Provenance footer**: who, when, what session, what it rests on, including the
  planning conversation. In two otherwise-empty documents in the corpus, this was
  the only useful content.

README is exempt from Amendments and Provenance; git history is its changelog.

## 6. Work-order numbering — defined here

Defined in this skill and nowhere else; `co-architect-work-order` owns work-order
*structure* and cites this for ids. Two definitions guarantee drift.

```
<PREFIX>-WO-PSNN[a]
  PREFIX  project tag, per repo   P  phase 0-9      S  subsection 0-9
  NN      order within subsection 00-99             a  inserted refinement
```

- **Why a prefix.** Ids are unique per repo, not per organisation, and
  cross-project references happen. Without one they collide the moment two
  projects reach the same number.
- **Why a letter suffix, not a leading digit.** An iteration marker in the
  most-significant position sorts a revision away from what it revises:
  `WO-1121` lands after `WO-0999`, nowhere near `WO-0121`. Ids appear in branch
  names, PR titles, and directory listings — all sorted lexically.
- **Why two digits for NN — empirical.** An earlier scheme gave each phase ten
  slots and ran out: *"P3 consumed `030`–`039` plus a `011A`, and iterative work
  has no room in a scheme with ten slots per phase. Iteration is the norm here,
  not the exception — six of P3's work orders came from the maker using the tool,
  and none were predicted."* That ad-hoc `011A` is this suffix invented under
  pressure.

**A phase needing more than ten subsections is mis-decomposed, not
under-numbered** — treat the ceiling as a decomposition check.

**Legacy ids are never renumbered.** Renumbering shreds every reference in
commits, PRs, code, and external indexes. Existing projects adopt the scheme going
forward and record the changeover in the roadmap. **State this explicitly in such
a roadmap, or a future instance will "helpfully" migrate history.**

## 7. Per-document craft

Shared rules above apply to all four; the craft specific to each lives in a
reference file. **Read only the one you are writing.** Each ends with that
document's acceptance checklist.

- **`references/northstar.md`** — the one sentence, falsifiable invariants,
  non-goals that stop relitigation.
- **`references/architecture.md`** — ground truth and the corrections table,
  rulings with reasons, seams that are security boundaries, traceability.
- **`references/roadmap.md`** — phases, dependency ordering, exit gates, critical
  path, reconciliation.

## 8. When the repo already has documents

Less common than genesis, and the rules differ — placement, numbering, and history
are load-bearing here in a way they are not on a blank page.

**Run the mechanical checks first** — duplicate section numbers, placeholders,
missing shared sections, unnumbered invariants, roadmaps with dates, uncheckable
gates, phase dependencies pointing forward or in a cycle, a README pointing
nowhere:

```bash
python3 scripts/check_docs.py <repo-path>
```

It proves what it can and stays quiet otherwise. Its findings are real; **a clean
run is not proof the documents are good.** Judgement stays yours.

**Then read for the three defects a script cannot see:** *role collapse* (content
doing another document's job — apply §3), *invariant scatter* (one constraint
stated divergently in two places), *aspiration in invariant costume* ("fast,
reliable, secure" — if the negation is absurd, it is not an invariant).

**Repair rules:**

- **Fix forward; never renumber history.** Add missing sections with the next free
  number. Where numbering is already broken, add a reconciliation note mapping the
  collision rather than resequencing.
- **Migrating an invariant to the northstar is a decision, not a cleanup.** Where
  an architecture already owns numbered invariants that code or work orders cite,
  **do not move them.** Leave them, have the northstar cite those numbers, record
  the deviation in both headers. The case motivating this rule had sixty-one such
  citations; consolidating would have bought consistency at the cost of the whole
  reference graph. Raise it for the gate; never perform it silently.
- **Growing a placeholder is genesis.** Return to §1 and measure ground truth.

## 9. The seam with `co-architect-work-order`

That skill owns the handoff to a builder; this one owns the documents. The
contract runs both ways, and **the upward half decays if nobody names it.**

**Downward.** A WO is one buildable unit inside a roadmap phase. It cites
northstar invariants *by number* for the slice it touches, the architecture
sections it rests on, and its phase — inheriting that phase's exit gate as the
boundary its acceptance rolls up into. That is why invariants must be numbered and
gates checkable: both are consumed by a session that cannot see this conversation.

**Upward.** A build discovers what the plan could not. Those findings land in the
builder's `FEEDBACK.md` and then, unless carried, stop. They belong here:

- a changed or superseded ruling → an **Amendments** row, dated, with reasoning,
  including when the original was wrong;
- a change to something that must stay true → the **northstar**, re-ratified,
  never folded into a feature work order;
- built diverging from planned → the roadmap's **reconciliation** table, history
  left as written;
- a gate that could not be checked → fix the **gate** by amendment;
- anything changing what the project *is* → check the **README**.

**This is the failure the corpus documents most expensively.** An audit of one
mature project found four months of ratified change that reached the code, tests,
and a running ledger but never the steering documents — including a northstar
decision false in the built system for three weeks, and resume instructions citing
two work-order files that did not exist. Nothing was careless; there was no step
saying *write it down where the next context-less reader will look*. Prompt the
wider audit at every phase boundary, where it is cheap.

**One place, always.** Sequencing lives in the roadmap. "What do I build next" is
answered *from* it — the first work order in the earliest phase whose dependencies
are green and whose gate has not passed — never from a parallel task list,
tracker, or state file. A second store of the same fact is the defect this whole
set exists to prevent; convenience does not change that.

## 10. Before calling anything done

- Status line, Amendments, Provenance present — even if Amendments holds one seed
  row. (README: status line only.)
- No section number appears twice.
- No `(PLACEHOLDER)`; open questions name a decider and what they block.
- Every ruling and non-goal carries its reason.
- Invariants defined in exactly one document, numbered, referenced elsewhere by
  number only.
- Nothing measured-in-name-only; unverified claims say so.
- README describes the project that now exists and points at documents that exist.
- Then the checklist in the relevant reference file.

**Report what you did not do.** Where a section is thin because the information
does not exist, say so in the document and in your reply. A document that hides
its gaps is worse than a short one, because the gaps are what the next work order
walks into.
