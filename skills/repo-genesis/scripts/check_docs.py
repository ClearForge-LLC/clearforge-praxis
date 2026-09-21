#!/usr/bin/env python3
"""Mechanical checks for the steering document triad.

Reports only what it can prove from the text: duplicate section numbers,
placeholders, missing shared sections, unnumbered invariants, roadmaps with
dates, invariants defined in more than one document.

A clean run is not proof the documents are good -- it means nothing mechanical
is wrong. Whether an invariant is really an invariant, or an exit gate really
checkable, is a judgement call the reader still has to make.

    python3 check_docs.py <repo-path> [--json]

Exit codes: 0 = no findings, 1 = findings, 2 = no triad documents found.
"""

import argparse
import json
import pathlib
import re
import sys

ROLES = ("northstar", "architecture", "roadmap")

CANONICAL = {r: f"docs/{r}.md" for r in ROLES}

# Filenames that are plainly one of the three, including the deviations found in
# real repositories: uppercase (ARCHITECTURE.md), project-prefixed
# (MYPROJECT_NORTHSTAR.md), and files sitting at the repo root instead of docs/.
PATTERNS = {
    "northstar": re.compile(r"(^|[_-])north[_-]?star\b", re.I),
    "architecture": re.compile(r"(^|[_-])architecture\b", re.I),
    "roadmap": re.compile(r"(^|[_-])roadmap\b", re.I),
}

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}

H2 = re.compile(r"^##\s+(?:§\s*)?(\d+(?:\.\d+)?)\s*[.．:—–\-\s]", re.M)
# Phases appear at h2 or h3, as "## P0", "### P0 - name", or "### Phase 0 (P0)".
# Matching only h2 misses well-formed roadmaps, and matching h3 too is what
# catches the real defect where a "### P3 - remaining" section is bolted on
# beside an existing "## P3".
H2_PHASE = re.compile(r"^#{2,3}\s+(?:Phase\s*\d+\s*\()?(P\d+)\b", re.M)
INLINE_CODE = re.compile(r"`[^`\n]*`")
# Matches "1. ", "1) " and the table row "| 1 | ...". The table form matters:
# the claim table with a How-to-falsify column is the recommended shape, so a
# pattern that only understands list items rejects the format the skill asks for.
NUMBERED_ITEM = re.compile(r"^\s*(?:\d+[.)]\s|\|\s*(?:\*\*)?\d+(?:\*\*)?\s*\|)", re.M)
DATE = re.compile(r"\b(20\d{2}-\d{2}-\d{2}|Q[1-4]\s*20\d{2}|"
                  r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+20\d{2})\b")

VAGUE_GATE = re.compile(r"\b(solid|robust|works|working well|good|complete enough|"
                        r"stable|polished|clean|done)\b", re.I)


class Finding:
    __slots__ = ("path", "line", "level", "code", "message")

    def __init__(self, path, line, level, code, message):
        self.path, self.line, self.level = path, line, level
        self.code, self.message = code, message

    def as_dict(self):
        return {"file": self.path, "line": self.line, "level": self.level,
                "check": self.code, "message": self.message}


def discover(root: pathlib.Path):
    """Map role -> path. Prefers docs/<role>.md; falls back to any clear match."""
    found = {r: [] for r in ROLES}
    for p in root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        stem = p.stem
        for role, pat in PATTERNS.items():
            if pat.search(stem):
                found[role].append(p)
    chosen = {}
    for role, paths in found.items():
        if not paths:
            continue
        canonical = [p for p in paths
                     if p.relative_to(root).as_posix().lower() == CANONICAL[role]]
        # Prefer the canonical path, then the shallowest, then the longest file.
        chosen[role] = (canonical or sorted(
            paths, key=lambda p: (len(p.parts), -p.stat().st_size)))[0]
    return chosen


def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def find_line(text: str, needle_re, default=1) -> int:
    m = needle_re.search(text)
    return line_of(text, m.start()) if m else default


def check_shared(rel, text, out):
    head = "\n".join(text.splitlines()[:12])
    if not re.search(r"\*\*(status|what this is)\b|^>\s*\*\*", head, re.I | re.M) \
            or not DATE.search(head):
        out.append(Finding(rel, 1, "error", "status-line",
                           "no status line in the first 12 lines: expected what this "
                           "is, a date, the author, and what to read first"))
    if not re.search(r"^#{1,3}.*\bamendments?\b", text, re.I | re.M):
        out.append(Finding(rel, 1, "error", "amendments",
                           "no Amendments section; add one with a seed row even at "
                           "inception -- undocumented drift is a defect"))
    if not re.search(r"\bprovenance\b", text, re.I):
        out.append(Finding(rel, 1, "error", "provenance",
                           "no Provenance footer: who designed it, when, in what "
                           "session, and what it rests on"))

    # Two deliberate narrowings, both to stop the check crying wolf -- a guard
    # people learn to ignore is worse than no guard.
    #   Uppercase only: one surveyed roadmap discusses gray "placeholder" images
    #   in prose, and a case-insensitive match flags that legitimate usage.
    #   Skip inline code spans: a document saying "never write `(PLACEHOLDER)` in
    #   place of a decision" is following the rule, not breaking it.
    spans = [(m.start(), m.end()) for m in INLINE_CODE.finditer(text)]
    for m in re.finditer(r"\(?\bPLACEHOLDER\b\)?|\bTBD\b|\bTODO\b", text):
        if any(lo <= m.start() < hi for lo, hi in spans):
            continue
        out.append(Finding(rel, line_of(text, m.start()), "error", "placeholder",
                           f"'{m.group(0)}' stands in for a decision; write the open "
                           "question, who answers it, and what it blocks"))

    for pat, label in ((H2, "section"), (H2_PHASE, "phase")):
        seen = {}
        for m in pat.finditer(text):
            key = m.group(1)
            if key in seen:
                out.append(Finding(
                    rel, line_of(text, m.start()), "error", "duplicate-number",
                    f"{label} {key} already used at line {seen[key]}; amendments "
                    "continue the sequence, they never reuse a number"))
            else:
                seen[key] = line_of(text, m.start())


def section_body(text, heading_re):
    m = heading_re.search(text)
    if not m:
        return None, None
    start = m.end()
    nxt = re.compile(r"^##\s", re.M).search(text, start)
    return text[start:nxt.start() if nxt else len(text)], line_of(text, m.start())


def check_northstar(rel, text, out):
    body, ln = section_body(text, re.compile(r"^##\s.*\binvariant", re.I | re.M))
    if body is None:
        out.append(Finding(rel, 1, "error", "invariants",
                           "no Invariants section -- this is the section the "
                           "northstar exists for"))
    else:
        items = NUMBERED_ITEM.findall(body)
        if not items:
            out.append(Finding(rel, ln, "error", "invariants-unnumbered",
                               "invariants are not numbered; work orders cite them "
                               "by number, and an uncitable invariant erodes"))
        elif not 6 <= len(items) <= 8:
            out.append(Finding(rel, ln, "warn", "invariant-count",
                               f"{len(items)} invariants; 6-8 is the working range "
                               "(too many is a design doc, too few means the hard "
                               "ones were not found) -- state a reason if deliberate"))
        if not re.search(r"falsif", body, re.I):
            out.append(Finding(rel, ln, "warn", "falsifiability",
                               "no falsification column or line; an invariant no one "
                               "can test is a wish"))
        if not re.search(r"this invariant is the project|is the project\b", body, re.I):
            out.append(Finding(rel, ln, "warn", "the-one",
                               "no invariant is marked as the project's reason for "
                               "existing; usually exactly one is"))

    nb, nl = section_body(text, re.compile(r"^##\s.*\bnon[- ]?goals?\b", re.I | re.M))
    if nb is None:
        out.append(Finding(rel, 1, "error", "non-goals",
                           "no Non-goals section; without it, excluded work is "
                           "relitigated every third work order"))
    else:
        # Flag the individual bare non-goal rather than judging the section.
        # Scanning prose for the word "because" marks good sections as bad --
        # the best example in the corpus states its reasons without ever using the word.
        for m in re.finditer(r"^\s*[-*]\s+(?:\*\*(?P<lead>[^*]+)\*\*)?(?P<rest>.*"
                             r"(?:\n(?!\s*[-*]\s|\s*$).*)*)", nb, re.M):
            rest = " ".join(m.group("rest").split())
            if len(rest) < 45:
                label = (m.group("lead") or rest)[:40]
                out.append(Finding(
                    rel, nl + nb.count("\n", 0, m.start()), "warn",
                    "non-goal-reasons",
                    f"non-goal '{label}' states no reason for exclusion; the reason "
                    "is what stops it being relitigated every third work order"))

    if len(text.splitlines()) > 200:
        out.append(Finding(rel, 1, "warn", "length",
                           f"{len(text.splitlines())} lines; a northstar should stay "
                           "short enough to re-read whole before every work order "
                           "(the one existing example is 100)"))


def check_architecture(rel, text, out):
    if not re.search(r"^##\s.*\b(ground truth|measured)\b", text, re.I | re.M):
        out.append(Finding(rel, 1, "error", "ground-truth",
                           "no Ground truth section; measure the running system and "
                           "record what the measurement overturned before designing"))
    elif not re.search(r"assum", text, re.I):
        out.append(Finding(rel, 1, "warn", "corrections-table",
                           "ground truth present but no assumed-vs-measured "
                           "corrections table; the wrong belief is the instructive "
                           "half"))
    if not re.search(r"^##\s.*\b(ruling|decision)", text, re.I | re.M):
        out.append(Finding(rel, 1, "warn", "rulings",
                           "no Ratified rulings section (question / ruling / reason)"))
    if not re.search(r"^##\s.*\bopen question", text, re.I | re.M):
        out.append(Finding(rel, 1, "warn", "open-questions",
                           "no Open questions section; name what is undecided, who "
                           "decides, and what it blocks"))
    if not re.search(r"^##\s.*\b(security|threat)\b", text, re.I | re.M):
        out.append(Finding(rel, 1, "warn", "security-posture",
                           "no Security posture section"))
    if re.search(r"^##\s.*\b(roadmap|build sequenc|phases?)\b", text, re.I | re.M):
        out.append(Finding(rel, find_line(text, re.compile(
            r"^##\s.*\b(roadmap|build sequenc|phases?)\b", re.I | re.M)),
            "error", "absorbed-roadmap",
            "sequencing inside the architecture; sequence belongs in the roadmap "
            "(extracting it is a repair with its own rules -- see SKILL.md 7)"))
    if len(text.splitlines()) > 600:
        out.append(Finding(rel, 1, "warn", "length",
                           f"{len(text.splitlines())} lines; past ~600, split by "
                           "domain and keep this as the index"))


def check_roadmap(rel, text, out):
    phases = H2_PHASE.findall(text) or re.findall(r"^###?\s+Phase\s+\d+", text, re.M)
    if not phases:
        out.append(Finding(rel, 1, "error", "no-phases",
                           "no phases found; a list of intentions without phases, "
                           "dependencies, and gates is a backlog, not a roadmap"))
    gates = len(re.findall(r"exit gate", text, re.I))
    if gates == 0:
        out.append(Finding(rel, 1, "error", "exit-gates",
                           "no exit gates; the gate is what converts 'we think we "
                           "finished' into a checkable fact"))
    elif phases and gates < len(phases):
        out.append(Finding(rel, 1, "warn", "exit-gates",
                           f"{len(phases)} phases but {gates} exit gates; every phase "
                           "ends on an objectively verifiable gate"))
    if not re.search(r"depends on", text, re.I):
        out.append(Finding(rel, 1, "warn", "dependencies",
                           "no 'Depends on' lines; phases are dependency-ordered"))
    if not re.search(r"critical path", text, re.I):
        out.append(Finding(rel, 1, "warn", "critical-path",
                           "no critical path; it should name where risk concentrates, "
                           "what runs in parallel, and what is human-track not code"))
    check_phase_graph(rel, text, out)

    # Dates are legitimate in the status line and in Amendments, so work on the
    # original text and skip those spans -- stripping them first and re-finding
    # the match reports the status line's own date, which is allowed.
    allowed = []
    first_h2 = re.compile(r"^##\s", re.M).search(text)
    allowed.append((0, first_h2.start() if first_h2 else len(text)))
    # [^\n]* on the heading line, not .* -- under re.S a greedy .* runs past the
    # heading to the last match in the file and swallows the document whole,
    # which silently suppresses every real finding after it.
    for m in re.finditer(r"^#{1,3}\s[^\n]*\b(amendments?|provenance)\b[^\n]*\n"
                         r".*?(?=^##\s|\Z)", text, re.S | re.M | re.I):
        allowed.append((m.start(), m.end()))
    for m in DATE.finditer(text):
        if any(lo <= m.start() < hi for lo, hi in allowed):
            continue
        out.append(Finding(rel, line_of(text, m.start()), "warn", "dates",
                           f"'{m.group(0)}' reads as a schedule; phases are "
                           "dependency-ordered, not calendar-ordered (dates in the "
                           "status line and amendments are fine)"))
        break
    # Scan only real gates. The section that *defines* the phase schema says
    # things like "a phase is done when the gate passes" -- correct prose that a
    # naive scan reports as a vague gate.
    scan = re.sub(r"^##\s[^\n]*\b(how this document works|phase schema|how to use)"
                  r"\b[^\n]*\n.*?(?=^##\s|\Z)", "", text, flags=re.S | re.M | re.I)
    for m in VAGUE_GATE.finditer(scan):
        seg = scan[max(0, m.start() - 120):m.start()]
        if re.search(r"exit gate", seg, re.I):
            out.append(Finding(rel, line_of(text, text.find(m.group(0), max(
                0, m.start() - 200))), "warn", "vague-gate",
                f"gate wording '{m.group(0)}' needs the author's judgement to "
                "check; could someone who was not in the room get an unambiguous "
                "yes or no?"))


def check_readme(root, chosen, out):
    """The front door. It points; it does not define.

    README rot is the most common documentation defect there is: the file every
    stranger reads first is the one nobody updates. The checks here are
    deliberately few, because most of what makes a README good is not mechanical.
    """
    path = next((root / n for n in ("README.md", "readme.md", "README.MD")
                 if (root / n).exists()), None)
    if path is None:
        out.append(Finding("README.md", 0, "warn", "readme-missing",
                           "no README. It is the front door -- what this is, whether "
                           "it works yet, and where to go next"))
        return
    rel, text = path.name, path.read_text(encoding="utf-8", errors="replace")

    spans = [(m.start(), m.end()) for m in INLINE_CODE.finditer(text)]
    for m in re.finditer(r"\(?\bPLACEHOLDER\b\)?|\bTBD\b|\bTODO\b", text):
        if not any(lo <= m.start() < hi for lo, hi in spans):
            out.append(Finding(rel, line_of(text, m.start()), "error", "readme-stale",
                               f"'{m.group(0)}' in the front door. Whatever it "
                               "describes has either been decided or is an open "
                               "question with a name"))
            break

    pointed = [r for r in ROLES if r in chosen
               and re.search(re.escape(chosen[r].name), text, re.I)]
    if chosen and not pointed:
        out.append(Finding(rel, 1, "warn", "readme-points-nowhere",
                           "the README links to none of the steering documents; a "
                           "reader has no way to find them from the front door"))

    n = len(text.splitlines())
    if n > 150:
        out.append(Finding(rel, 1, "info", "readme-length",
                           f"{n} lines. A long front door is usually one that has "
                           "started defining things the steering documents own -- "
                           "check for facts here that live somewhere else too"))


def check_phase_graph(rel, text, out):
    """Validate the phase dependency graph the roadmap declares in prose.

    A roadmap states "Depends on: P1, P2" and nothing ever checks it. The two
    failures worth catching are mechanical: a phase that depends on itself or on
    a later phase (which makes the ordering unbuildable), and a cycle. Both are
    invisible on a read-through once there are more than about five phases.
    """
    phases, order = {}, []
    for m in re.finditer(r"^#{2,3}\s*(?:Phase\s*)?(P\d)\b[^\n]*\n(.*?)(?=^#{2,3}\s|\Z)",
                         text, re.S | re.M):
        pid, body = m.group(1), m.group(2)
        if pid not in phases:
            phases[pid] = set()
            order.append((pid, line_of(text, m.start())))
        dep = re.search(r"\*\*Depends on:?\*\*\s*([^\n]*)", body, re.I)
        if dep and not re.search(r"\bnothing\b|\bnone\b|^\s*[-—]\s*$", dep.group(1), re.I):
            phases[pid] |= set(re.findall(r"\bP(\d)\b", dep.group(1)))

    for pid, ln in order:
        deps = phases[pid]
        if pid[1] in deps:
            out.append(Finding(rel, ln, "error", "phase-self-dependency",
                               f"{pid} lists itself as a prerequisite"))
        later = sorted(d for d in deps if d > pid[1])
        if later:
            out.append(Finding(
                rel, ln, "error", "phase-forward-dependency",
                f"{pid} depends on {', '.join('P'+d for d in later)}, which comes "
                "later. Phases are dependency-ordered, so either the ordering is "
                "wrong or the dependency is"))

    # Cycles among the declared edges.
    state = {}

    def visit(node, stack):
        if state.get(node) == 2:
            return None
        if state.get(node) == 1:
            return stack[stack.index(node):] + [node]
        state[node] = 1
        for dep in sorted(phases.get(node, set())):
            found = visit("P" + dep, stack + [node])
            if found:
                return found
        state[node] = 2
        return None

    for pid, ln in order:
        cyc = visit(pid, [])
        if cyc:
            out.append(Finding(rel, ln, "error", "phase-cycle",
                               "dependency cycle: " + " -> ".join(cyc)))
            break


def check_cross(chosen, texts, out):
    definers = []
    for role, text in texts.items():
        body, _ = section_body(text, re.compile(r"^##\s.*\binvariant", re.I | re.M))
        if body and NUMBERED_ITEM.findall(body):
            definers.append(role)
    # The observed case: an architecture numbering nine invariants while the
    # northstar stated five as unnumbered bullets under another name, so the
    # pair never trips the scatter check below. Surface the half we can prove.
    if definers == ["architecture"]:
        out.append(Finding(chosen["architecture"].name, 0, "info", "invariant-owner",
                           "the architecture defines numbered invariants. They belong "
                           "to the northstar, cited here by number -- unless code or "
                           "work orders already cite these numbers, in which case "
                           "leave them and record the deviation (SKILL.md 7). Check "
                           "the northstar for a second, divergent set under another "
                           "name"))
    if len(definers) > 1:
        where = ", ".join(f"{r} ({chosen[r].name})" for r in definers)
        out.append(Finding("<cross-document>", 0, "error", "invariant-scatter",
                           f"numbered invariants defined in more than one document: "
                           f"{where}. They are defined in exactly one place and cited "
                           "by number elsewhere -- but if code or work orders already "
                           "cite these numbers, do NOT move them: record the deviation "
                           "and raise the migration (SKILL.md 7)"))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo", type=pathlib.Path)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    root = args.repo.expanduser().resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    chosen = discover(root)
    if not chosen:
        msg = (f"no northstar, architecture, or roadmap found under {root}. "
               "If this project is about to be built, that is the finding.")
        print(json.dumps({"findings": [], "note": msg}) if args.json else msg)
        return 2

    findings, texts = [], {}
    for role, path in chosen.items():
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        texts[role] = text
        if rel.lower() != CANONICAL[role]:
            findings.append(Finding(
                rel, 1, "info", "placement",
                f"not at {CANONICAL[role]}. Do not rename retroactively -- a rename "
                "breaks every link in commits, PRs, code, and the vault. Note the "
                "deviation in the document's header instead"))
        check_shared(rel, text, findings)
        {"northstar": check_northstar, "architecture": check_architecture,
         "roadmap": check_roadmap}[role](rel, text, findings)

    for role in ROLES:
        if role not in chosen:
            findings.append(Finding(CANONICAL[role], 0, "error", "missing-document",
                                    f"no {role} found"))
    check_readme(root, chosen, findings)
    check_cross(chosen, texts, findings)

    if args.json:
        print(json.dumps({"root": str(root),
                          "documents": {r: p.relative_to(root).as_posix()
                                        for r, p in chosen.items()},
                          "findings": [f.as_dict() for f in findings]}, indent=2))
    else:
        for role in ROLES:
            print(f"{role:13} {chosen[role].relative_to(root).as_posix() if role in chosen else '-- not found --'}")
        print()
        order = {"error": 0, "warn": 1, "info": 2}
        for f in sorted(findings, key=lambda f: (order[f.level], f.path, f.line)):
            loc = f"{f.path}:{f.line}" if f.line else f.path
            print(f"[{f.level:5}] {loc}  ({f.code})\n         {f.message}\n")
        errs = sum(1 for f in findings if f.level == "error")
        warns = sum(1 for f in findings if f.level == "warn")
        print(f"{errs} error(s), {warns} warning(s), "
              f"{len(findings) - errs - warns} note(s).")
        if findings:
            print("\nMechanical checks only. A clean run is not proof the documents "
                  "are good.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
