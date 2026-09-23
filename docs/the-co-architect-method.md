# The Co-Architect Method

**How one person, with no computer-science degree and no intention of learning to write code fluently, runs production infrastructure built by AI agents — and why the discipline, not the model, is what makes it hold.**

*Scotty · ClearForge LLC · September 2026*

---

## The short version

I am a kitchen manager. I started building software in February 2026. I don't write the code — AI agents do. What I do is decide what gets built and why, hand that decision to an agent in a form it cannot misread, and verify what comes back before anything ships.

Seven months in, that has produced a fleet of self-hosted infrastructure: eight of my own MCP servers wired into the assistant I work with, the tools behind a real restaurant's inventory and costing, a client storefront, and a published security standard for this class of system. None of it rests on my ability to type code. All of it rests on a method.

The method is short to state:

> **Humans and a conversational model decide *what* and *why*. A coding agent owns *how*. Subagents do the work. Every handoff crosses a durable written boundary, and nothing merges unreviewed.**

The rest of this document is why each piece exists — every one of them was paid for by a failure — and where to see the method running.

---

## Why a method at all

The common story about building with AI is that the model is the bottleneck: get a better model, get better software. My experience is the opposite. Current models are more than capable of writing the code. What fails is everything *around* the code:

- The agent confidently builds the wrong thing, because the request was ambiguous and it filled the gap reasonably — but not my way.
- Scope creeps past anything anyone reviewed, because nothing said where to stop.
- A design quietly breaks a constraint nobody restated, because the constraint lived in a conversation that ended.
- The agent discovers something important mid-build, and it evaporates when the session closes.
- A check reports success while measuring the wrong thing, and everyone believes it.

These are not model failures. They are the failures of any team where the people who decide and the people who build are separated by a handoff — which is to say, they are management failures. I happen to manage a kitchen for a living, and a kitchen is a system built entirely around surviving that handoff under pressure.

---

## The roles

| Role | Who | Owns |
|---|---|---|
| **Co-architects** | Me + a conversational model (Claude, in chat) | *What* gets built and *why*. Rulings, trade-offs, review, the merge decision. |
| **Project manager** | A coding agent (Claude Code) | *How* it gets built. Breaks the work down, delegates, integrates, reports. |
| **Workers** | Subagents spawned by the coding agent | Individual pieces of the build — and, deliberately, attacks on the finished work. |

The separation is the point. The conversational model is a thinking partner with standing to argue, not a code vending machine — it pushes back when an idea is bad, and I expect it to. The coding agent owns the build and is encouraged to delegate: it keeps its own context clear for integration while subagents do focused work. Nobody self-merges.

In a kitchen this is the brigade. The chef decides the menu and tastes every plate at the pass. The sous chef runs the line. The cooks execute their stations. No plate leaves without passing the chef — and the chef does not need to be the fastest cook in the building to run it well.

---

## 1. Steering documents before code

A new project starts with four documents, written before any work order: a **README** (what this is, where to go), a **northstar** (why it exists, and the numbered invariants that must stay true), an **architecture** (what it is, how it is shaped, and the reason behind each ruling), and a **roadmap** (in what order, and a checkable exit gate for each phase).

**Why:** the plan for a new project usually lives in a conversation — and the conversation is about to end. Everything decided either lands in a durable document or is gone. And the author who was in the room is the worst-placed person to notice what was left implicit: a document that merely gestures at a decision reads as complete to the person who made it, and as a non-sequitur to the agent who picks it up a month later.

Two rules carry most of the weight. **Invariants are defined in exactly one place and cited everywhere else by number** — because a constraint restated in three documents is three slightly different constraints within two months. And **section numbers are never reused or renumbered** — because code comments, commits and work orders cite them, and renumbering silently breaks every one of those references with nothing to catch it.

In the kitchen this is *mise en place*: nothing gets cooked until everything is prepped, labelled and where it belongs.

→ The full discipline: [`skills/repo-genesis/`](../skills/repo-genesis/SKILL.md)

---

## 2. Work orders, not requests

Work reaches the coding agent as a **work order**: a durable file in the repository, not a chat message. The message that starts the session — the *kickoff* — stays deliberately thin and just points at the file.

**Why a file:** long pasted instructions collapse, fail to submit, or scroll out of reach. A file the agent can reopen is a specification it can re-read at the moment it needs it. The kickoff carries orientation; the work order carries the weight.

Every work order has the same sections, and two of them are the ones most often skipped:

- **The scope fence** — what is *not* in this work order. Name the adjacent things a capable agent would reasonably fold in, and say they are out. This is what stops a build from quietly growing.
- **"Verify live HEAD"** — a stale checkout is the most common opening failure, and a build on a stale base silently omits work that already merged.

Work orders separate two kinds of line that are easy to collapse into one:

- An **invariant** is something that should stay true. If a work order contradicts itself — forbidding the very thing it demands — the agent crosses the invariant rather than stalling, and **leads its report with what it crossed and why**. An invariant that had to be crossed almost always means the work order was wrong, so that section is read first.
- A **flag-and-stop** is something that must *never* happen — the crossings that cost money, data, or a safety property. If one blocks the work, the agent parks the branch and says so. That is a work order needing a rewrite, not a decision for the build to make.

In the kitchen, this is the ticket. The line does not cook from a shouted description; it cooks from the ticket, and the ticket says what is *not* on the plate as clearly as what is.

---

## 3. A goal must end where the agent's authority ends

Every work order also sets a persistent goal — the observable end state the agent checks before it is allowed to stop. That goal has one rule I learned the expensive way:

> **The goal must terminate at the agent's authority boundary.** Where finishing requires a human — a merge, a privileged command, spending money, publishing — the goal ends at "parked for the gate," never at "merged."

**Why:** a goal only reachable through an action the agent is forbidden to take can never be met. A completion loop that checks the goal will keep re-invoking the agent indefinitely, chasing a state it is not allowed to produce.

→ The incident: [A Goal Must End Where the Agent's Authority Ends](https://github.com/ClearForge-LLC/ClearProof/blob/main/notes/a-goal-it-was-forbidden-to-reach.md)

---

## 4. Attack the work, then report upward

A build closes in two stages, in order.

**First, an adversarial pass.** Before anything reaches review, the work is deliberately attacked — preferably by a fresh subagent with no investment in it being sound. Violate each invariant directly. Interrupt between steps that must be atomic. Feed hostile input, including anything treated as "just data." Remove a dependency and confirm the system refuses rather than silently degrading.

**Why a separate stage:** the builder has just spent hours in "it works" mode, where every test it wrote is one it expected to pass. Hunting for its own failures is a real change of mode, and it will not happen unless the work order names it as a step.

**Then, upward feedback.** The builder writes a `FEEDBACK.md` parked with the work: what it found, what it questioned, what it deliberately did not build, what did *not* work and why, and every finding from the attack — each marked with whether it needs my ruling before the next step.

**Why:** the builder knows things I cannot see from outside — wrong assumptions in my specification, risks it routed around, adjacent problems. Without a required channel, that knowledge evaporates when the session ends. The "deliberately not built" section alone prevents the most expensive misunderstanding in this whole mode of working: believing something shipped that never did.

---

## 5. Review is verification, not reading

The feedback file is a claim. Review is where the claim is checked:

- Diff against the **live** base — but judge what the builder touched against the branch's **merge-base**. Mixing the two refs fails a builder for the reviewer's own commits.
- Re-run the proof suites myself when anything adjacent moved. Never accept green on faith.
- Verify security-critical claims **at the source** — if the report says a component holds no credential, read those lines.
- Rule on every decision-needed item, with reasons — including the ones I agree with, so the record shows they were weighed.

And when the builder's design beats the one I specified, adopt it and say so. A review process that cannot absorb a better idea teaches the builder to stop offering them.

I call the stance underneath this **informed reliance with verification**. I rely on the agents heavily — that is the whole point — but reliance is earned by checking, and every check is recorded.

→ The pattern behind most of the failures I have caught: [Make the Instrument Disagree With Itself](https://github.com/ClearForge-LLC/ClearProof/blob/main/notes/make-the-instrument-disagree.md)

---

## 6. Close the loop upward

Reviewing the branch is not the end of a work order. **What the build learned has to reach the steering documents, or it reaches nothing.** A ruling the build changed gets a dated amendment. A change to something that must stay true goes back to the northstar and is re-ratified there. A divergence from the roadmap gets a reconciliation row. And the README gets re-read, because it is the first thing a stranger opens and the most reliably stale file in any repository.

**Why:** in one mature project, an audit found four months of ratified change that had reached the code, the tests and a running ledger — but never the steering documents. Including a northstar decision that had been false in the built system for three weeks. Every one of those changes passed through a review. Nothing was careless. There was simply no step that said *write it down where the next reader will look*. Now there is.

→ The full discipline, including review and the upward loop: [`skills/co-architect-work-order/`](../skills/co-architect-work-order/SKILL.md)

---

## 7. Context is a budget

A coding agent's working memory is finite, and how it is spent matters as much as what it is spent on.

- **Compact, don't clear.** An agent that keeps its model of the codebase doesn't have to rediscover the architecture, the conventions and its own recent work on every task. Clearing the window before each work order looked disciplined and was quietly expensive: switching to compact-only-when-full raised both completion and thoroughness.
- **Delegate to subagents.** Focused workers get clean context for their piece; the coordinating agent keeps its own context for integration. Better work *and* a healthier budget.
- **One writer per tree.** The architect writes the work order in its own clone and lands it through a pull request; the builder's worktree is never written into concurrently.

---

## What this method has produced

The method is meant to be judged by its output, so here is the public part of it:

- **[ClearSeal](https://github.com/ClearForge-LLC/ClearSeal-public)** — an integrity and authenticity standard for MCP servers and other LLM-access nodes. It was hardened by building against it: most of what is in its last three versions was found by a builder agent implementing the standard and fed back upstream — including one mechanism invented at the reference implementation that reached the standard a week late, which is now a rule in the standard itself.
- **[The two methodology skills](../skills/)** — this method written as executable instructions for an agent. They are versioned and reviewed like code, because they are the thing that makes the method repeatable rather than something I have to remember.
- **[ClearProof](https://github.com/ClearForge-LLC/ClearProof)** — the failure record. Real incidents, each reduced to one rule, added as the work turns up new ones. The failure that keeps recurring in the private record is one bug in different clothes: *a check that reported success while measuring the wrong thing.*

---

## What it doesn't do

Honesty about the limits is part of the method.

- **It is not faster for small things.** For a one-line fix, a work order is overhead. The discipline pays off where a mistake is expensive or the work spans more than one session.
- **It does not replace judgment.** It concentrates it. Every decision point that matters still routes to a human, and the quality of the whole system is capped by the quality of those rulings.
- **It does not make the agents remember.** The continuity is engineered — steering documents, work orders, feedback files, a vault of session records — not assumed. The partnership is real; the memory is written down.
- **It does not prevent every failure.** It makes failures visible, recorded, and less likely to happen twice. ClearProof exists because the method did not prevent those — it caught them.

---

## Why I'm publishing this

I built this because I had to: I needed real systems to support my family, and I was never going to become a fluent programmer on nights and weekends. What I found is that the skill that mattered was the one I already had — running a system of people under pressure, where the person who decides and the person who executes are different, and the handoff between them is where things break.

If you can do that, you can build with AI agents. The method is how.

---

## Provenance

Drafted by Claude (Anthropic) at Scotty's direction on 2026-09-21, from the two methodology skills in this repository, the ClearSeal standard, the ClearProof record, and the working rules of the collaboration itself; approved for publication by Scotty. That is the method describing itself: the architect decided what this document needed to say and why, the model drafted it, and nothing was published without the architect's approval.
