# Writing `docs/architecture.md`

**Read `SKILL.md` first** — shared rules (§5) and numbering (§6) apply and are not
repeated. **Worked example: `assets/example/docs/architecture.md`**; every
illustration below comes from it.

**Evidence base:** seven architecture documents, 73–1431 lines. Best-evidenced of
the three, and the widest quality spread — two were placeholders, one was 1431
lines with duplicate section numbers.

---

## 1. Purpose

Answers **what this is and how it is shaped** — the decisions, their reasons, and
the structure that follows. The boundary statement worth adopting near-verbatim,
from the strongest document in the corpus:

> *"This is the source of truth for what we are building and why each choice was
> made. Implementation detail belongs in work orders; this document constrains
> them. The roadmap tracks sequence; this tracks shape."*

**Required sections:** status line · how to use it (incl. the divergence rule) ·
ground truth (§2) · shape and seams (§4) · ratified rulings (§3) · runtime and
deployment · security posture · traceability (§6) · open questions with deciders ·
Amendments · Provenance. Scale them to the project; do not drop them. A section
reading *"None — this project has no governing standard"* is worth more than a
missing one, because it records that the question was asked.

## 2. Ground truth — measure before you design

**The highest-value practice found, and the one no surveyed document had a section
for.** Before designing anything, read the running system and record what is there.

One project's phase-0 pass overturned four beliefs held in written docs: a box
believed headless was running a display server; a runtime believed to be on one
major version was two ahead; services believed to depend on it did not; a cadence
believed broken worked by design. **One wrong belief came from an official project
file and had already produced a wrong recommendation that reached the human.**

- **A corrections table** — *assumed* vs *measured* — wherever measurement
  contradicts belief:

  | Assumed | Measured |
  |---|---|
  | Restores take "about an hour", so the drill must run weekly | 6m 12s for the largest set — a nightly drill is affordable, which changed the whole cadence design |
  | Scratch can reuse the staging database | Staging has a modified schema; a restore there would compare against the wrong source of truth and pass falsely |

  **The wrong belief is more instructive than the right fact** — it shows where
  the reasoning was weak. Record both; do not silently replace one with the other.
  The example calls the staging correction load-bearing precisely because reusing
  staging was the obvious cheap choice and would have produced a drill that passed
  while proving nothing.
- **Cite the command.** A claim from running something says what was run.
- **Correct the upstream source too**, or the stale belief keeps being re-read.
- **Never fake a number.** Report blocked measurements as blocked with the harness
  that will produce them — the example does this for its legacy-format archives
  and records no estimate in its place.

With no running system yet, this records the environment the build lands in: what
is on the box, what ports and services are taken, what the deploy path is. Still
measurement.

## 3. Rulings carry reasons

A bare verdict column is a list of things nobody can defend six weeks on. Use
three columns:

| Question | Ruling | Reason |
|---|---|---|
| Where read-only is enforced | At the store's IAM policy, not in runner code | Invariant 2 must survive a bug in the runner; a check the runner performs on itself is not a boundary |

- **Label departures as departures.** The example marks its alerting choice a
  *"departure from the house default of email"* with the reason. An unlabelled
  departure is indistinguishable from an accident.
- **"Do not decide yet — spike it" is a legitimate ruling**, recorded as one, with
  the architect's prior stated so the spike has something to test rather than a
  blank page. The example does this and marks the prior as held loosely.

## 4. Seams, and which are boundaries

Describe the parts and where the seams fall — then **name which are security or
blast-radius boundaries**, because a module boundary and a trust boundary get
maintained differently. The example names two of three as boundaries and says
explicitly that the third is neither, which is the part most documents leave to
inference.

## 5. The divergence rule

**Any deviation from this document is recorded as a dated amendment with its
rationale. Undocumented drift is a defect, not a shortcut.**

The strongest artifact in the corpus was an amendments table with fourteen
entries, several recording that the original ruling was *wrong* and why. That kind
is the most valuable thing a steering document can contain: the only evidence the
process is working rather than being performed.

- **Never reuse a section number.** That same document has two §15s and two §16s
  because appended content took spent numbers. See `SKILL.md` §5 for why this
  matters more than it looks when code cites the document.
- **A change to an invariant is not an amendment here.** It goes to the northstar
  and is re-ratified; the architecture records the consequence, not the decision.

## 6. Traceability

Where a governing standard exists, close with a table mapping **every control to
the clause it satisfies**. This makes an audit possible rather than aspirational,
and surfaces the controls pointing at nothing — where the gaps are. Pin the
standard's **version and commit** in the status line; "per the standard" without a
revision is unverifiable a month later. Where none governs, say so explicitly.

## 7. Anti-patterns

- **`(PLACEHOLDER)` as a decision.** Two repos carried it for a fortnight at
  73–80 lines. Both *did* have a provenance footer, and it was the only useful
  content in them — which tells you how cheap the required sections are relative
  to their value.
- **Absorbing the roadmap.** Two projects had a build backlog inside the
  architecture; in one, the commit says so outright. Sequence belongs in the
  roadmap; extracting it is a repair with its own rules (`SKILL.md` §8).
- **Defining invariants here** instead of citing northstar numbers. Exception and
  repair path: `SKILL.md` §8.
- **Unbounded growth.** Past ~600 lines, split by domain and keep this as the
  index.
- **Assumption stated as fact.** If it was not measured, mark it unverified.

## 8. Acceptance

- Ground truth measured, commands cited, contradictions in a corrections table.
- Every ruling has a reason; every departure is labelled one.
- Seams that are security boundaries identified as such.
- Open questions name a decider and what they block.
- Traceability table present, or an explicit "no governing standard".
- No section number used twice; Amendments and Provenance present.
- No invariant *defined* here — only referenced by northstar number, unless the
  documented deviation in `SKILL.md` §8 applies and is recorded in the header.
