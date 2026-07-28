# The Triad Dev System (PLACEHOLDER — theoretical)

> **STATUS: PLACEHOLDER / THEORETICAL.** This lays out a possible three-device
> development system and the force-multiplication we might predict from it. It is a
> design thesis, not a shipped, measured system. Treat the multiplier claims as
> hypotheses to test, not facts.

## The three roles
A ClearForge build loop distributed across three devices, each with a distinct role:

- **S25 Ultra — the COCKPIT.** Control surface. Mobile SSH, direction, ratification,
  minting the write path, kicking off and steering sessions from anywhere. The
  operator's seat: where intent enters the system.
- **PRECISION777 — the FORGE.** Compute + code host. Where clones live, builds run,
  MCP servers serve, the code mirror refreshes, and the heavy work happens. The
  anvil where raw material becomes form.
- **Surface — the LENS.** Visual eyes. Via the Claude Code browser (sandboxed
  headless Chromium), a way to *see* rendered web output and visual state — closing
  a loop that a pure-terminal workflow leaves open. (Still-image vision — operator
  screenshots read by Claude's native vision — already works today; the browser
  extends this to live-navigated web surfaces.)

## The loop
Cockpit directs -> Forge builds and hosts -> Lens shows the result -> Cockpit
evaluates and re-directs. Intent, compute, and sight as three separable stations
handing off around a single build.

## Force-multiplication thesis (hypothesis)
The claim: separating **control** (cockpit), **compute** (forge), and **sight**
(lens) lets each run at its strength without bottlenecking the others — the operator
steers from anywhere, the forge does unattended heavy work, and the lens gives
feedback the terminal can't. The predicted multiplier comes from parallel stations +
tight feedback, not from any one device being faster.

**This is theory.** Real force-multiplication must be measured against a
single-device baseline before any multiplier is claimed. Recorded here so the idea
is durable — not so it's assumed true.

## Open questions
- What is the actual measured delta vs. working from the Precision alone?
- Where does the lens genuinely close a loop vs. just add a hop?
- Which handoffs are friction (device-switch cost) vs. real leverage?

## Provenance
Articulated collaboratively (Scotty + Claude Opus 4.8), 2026-07-28. Related infra:
ClearMirror (substrate) and CartographerMCP (code intelligence), both under
ClearForge-LLC.
