#!/usr/bin/env python3
"""Audit the compiled belt page (run 20261021-0213-q-compile-belt-49ad).

Read-only. Recomputes the budgets exactly as lab/wiki.py index does, then checks:
  1. budget: current best <= 15 non-blank lines, page <= 300 lines;
  2. token survival: every digit-bearing token of the old page (lab/wiki/belt.md)
     appears somewhere in the new page (run's wiki/belt.md) — no supported number
     lost, stronger than the checker's ten-sample. Abbreviated citations (with …)
     survive iff every piece does; the old `updated:` header value is metadata the
     compile must replace, and is excluded;
  3. Runs: the run lines are byte-identical between old and new;
  4. citations: every 2026MMDD-HHMM prefix in the new page resolves to a Runs id;
  5. sections: the five sections appear, line-anchored, in the schema's order.
Exit code 0 iff all pass; misses are listed token by token.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OLD = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "lab/wiki/belt.md"
NEW = ROOT / "lab/results/20261021-0213-q-compile-belt-49ad/wiki/belt.md"

old, new = OLD.read_text(encoding="utf-8"), NEW.read_text(encoding="utf-8")
fail = []

# --- 1. budgets (lab/wiki.py index, verbatim logic) --------------------------
def budget(text):
    best = [l for l in text.split("## Current best", 1)[-1]
            .split("\n## ", 1)[0].splitlines() if l.strip()]
    return len(best), len(text.splitlines())

ob, ol = budget(old)
nb, nl = budget(new)
print(f"old: {ol} lines, current best {ob}")
print(f"new: {nl} lines, current best {nb}")
if nb > 15:
    fail.append(f"current best over budget: {nb} > 15")
if nl > 300:
    fail.append(f"page over budget: {nl} > 300")

# --- 2. token survival --------------------------------------------------------
EDGE = "()[]{}<>\"'“”‘’.,;:!?"
def tokens(text):
    out = []
    for w in text.split():
        t = w.strip(EDGE)
        if len(t) >= 2 and any(c.isdigit() for c in t):
            out.append(t)
    return out

def survives(t):
    if t in new:
        return True
    if "…" in t:  # abbreviated citation: survives iff every piece appears
        return all(p in new for p in t.split("…") if p)
    return False

old_updated = re.search(r"^updated:\s*(\S+)", old, re.M).group(1)
old_tokens = [t for t in tokens(old) if t != old_updated]
missing = [t for t in old_tokens if not survives(t)]
print(f"digit-bearing tokens in old page: {len(old_tokens)} (unique {len(set(old_tokens))})")
print(f"missing from new page: {len(missing)}")
for t in sorted(set(missing)):
    fail.append(f"token lost: {t}")

# checker-style sample: the 10 longest unique tokens, plus a fixed probe list
sample = sorted((t for t in set(old_tokens) if "…" not in t), key=len, reverse=True)[:10]
probes = ["16,456", "0.126", "1.3×10⁻⁴", "157.4", "19.7 GB", "108.71", "108.77",
          "0.55", "20.7–22.1", "9.54×10⁻⁴", "1.7×10⁻¹⁸", "23.7 kyr", "Λ(10⁻⁴) = 0.525",
          "ρ = 0.74", "ρ = −0.05", "2²⁰", "2²³", "e₀ > 0.2", "N^1.07", "m^1.13"]
sample_hits = {s: (s in new) for s in sample}
probe_hits = {p: (p in new) for p in probes}
for k, v in {**sample_hits, **probe_hits}.items():
    if not v:
        fail.append(f"sample/probe lost: {k}")
print("checker-style sample (10 longest): " + ", ".join(f"{k}={'ok' if v else 'LOST'}" for k, v in sample_hits.items()))
print(f"fixed probes: {sum(probe_hits.values())}/{len(probe_hits)} present")

# --- 3. Runs identity ----------------------------------------------------------
def runs(text):
    m = re.search(r"^## Runs\s*$", text, re.M)
    return [l for l in text[m.end():].splitlines() if l.strip()]
old_runs, new_runs = runs(old), runs(new)
print(f"runs old={len(old_runs)} new={len(new_runs)} identical={old_runs == new_runs}")
if old_runs != new_runs:
    fail.append("Runs section changed")
    for l in old_runs:
        if l not in new_runs:
            fail.append(f"  run line lost: {l[:60]}")

# --- 4. citation resolution -----------------------------------------------------
run_ids = [re.match(r"^- (\S+)", l).group(1) for l in old_runs]
THIS = "20261021-0213"  # the compiling run, named in the header/provenance
cites = set(re.findall(r"\b(2026\d{4}-\d{4})", new))
# a prefix resolves if it starts a run id, is embedded in one (second-author ids
# carry their parent's date-time), or is this run's own id
unresolved = [c for c in cites
              if not (any(r.startswith(c) or c in r for r in run_ids) or c == THIS)]
print(f"citation prefixes in new page: {len(cites)}, unresolved: {len(unresolved)}")
for c in unresolved:
    fail.append(f"citation does not resolve to a run: {c}")

# --- 5. section order ------------------------------------------------------------
order = ["## Current best", "## Refuted", "## Open directions", "## Contradictions", "## Runs"]
pos = []
for s in order:
    m = re.search(rf"^{re.escape(s)}\s*$", new, re.M)
    pos.append(m.start() if m else -1)
if pos != sorted(pos) or -1 in pos:
    fail.append(f"sections out of order or missing: {list(zip(order, pos))}")
print(f"sections in schema order: {pos == sorted(pos) and -1 not in pos}")
# header keys
head = new.split("\n\n", 1)[0]
for key in ("topic:", "status:", "updated:"):
    if key not in head:
        fail.append(f"header key missing: {key}")

print()
if fail:
    print("FAIL")
    for f in fail:
        print(" -", f)
    sys.exit(1)
print(f"PASS: new page {nl} lines (<=300), current best {nb} (<=15), "
      f"{len(old_tokens)} old tokens all present, {len(old_runs)} run lines identical, "
      f"{len(cites)} citations resolve, sections ordered.")
