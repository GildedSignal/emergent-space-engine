#!/usr/bin/env python3
"""audit.py — the compile's verifier (run id 20261021-0142-q-compile-budget-1e9-8179).

Compares the page as shipped in the tree (OLD) with the compiled page (NEW):
  P1 budgets (wiki.py's own counting), P2 runs, P3 exhaustive number coverage
  (literal, or behind a cited run), P4 headline constants, P5 decided disagreements.
Exit 0 iff nothing fails; writes audit-out.txt-compatible report to stdout.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]          # repo root
OLD = ROOT / "lab/wiki/budget-1e9.md"
NEW = Path(__file__).resolve().parent / "wiki/budget-1e9.md"

old, new = OLD.read_text(encoding="utf-8"), NEW.read_text(encoding="utf-8")
fails, notes = [], []

def check(cond, msg):
    (notes if cond else fails).append(("PASS" if cond else "FAIL") + " " + msg)

# ---------- P1 budgets ----------
def cb_lines(text):
    body = re.split(r"^## Runs\s*$", text, flags=re.M)[0]
    seg = body.split("## Current best", 1)[-1].split("\n## ", 1)[0]
    return [l for l in seg.splitlines() if l.strip()]

def section(text, name):
    m = re.search(rf"^## {name}\s*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else ""

old_cb, new_cb = cb_lines(old), cb_lines(new)
check(len(old.splitlines()) == 411, f"P0 old page is the 411-line flagged page (got {len(old.splitlines())})")
check(len(new.splitlines()) <= 300, f"P1 new total lines {len(new.splitlines())} <= 300")
check(len(new_cb) <= 15, f"P1 current best {len(new_cb)} non-blank lines <= 15 (old {len(old_cb)})")
od = [l for l in section(new, "Open directions").splitlines() if re.match(r"^\d+\.", l)]
check(len(od) <= 8, f"P1 open directions {len(od)} <= 8")
ref = [l for l in section(new, "Refuted").splitlines() if l.startswith("- ")]
known = set("097e 0659 73b5 3aec d4ff f876 f623 8994 5f76 6e76 cd3b e3a4 a765 262f cd6e 07b4 fc48 0820 f80a cc9d 9edc 08d0 7b6f a9d7 1738 277d c749".split())
check(all(known & set(re.findall(r"\b[0-9a-f]{3,4}\b", l)) for l in ref) and len(ref) == len(set(ref)), f"P1 refuted one line each, each citing a run ({len(ref)} entries)")
hdr = [l.split(":")[0] for l in new.splitlines()[:6] if l.strip()]
check(hdr == ["topic", "status", "closed-by", "valid-while", "updated"], f"P1 header keys {hdr}")
order = re.findall(r"^## (.+)$", new, re.M)
check(order == ["Current best", "Refuted", "Open directions", "Contradictions", "Runs"], f"P1 section order {order}")

# ---------- P2 runs ----------
run_re = re.compile(r"^- (\d{8}-\d{4}-[a-z0-9-]+) \(", re.M)
old_ids, new_ids = run_re.findall(old), run_re.findall(new)
check(len(old_ids) == 16 and len(set(old_ids)) == 10, f"P2 old: {len(old_ids)} lines, {len(set(old_ids))} distinct ids")
check(set(old_ids) == set(new_ids), f"P2 all old ids kept (lost: {set(old_ids)-set(new_ids)}, added: {set(new_ids)-set(old_ids)})")
check(len(new_ids) == len(set(new_ids)) == 10, f"P2 new: one line each ({len(new_ids)} lines, {len(set(new_ids))} distinct)")

# ---------- P3 number coverage ----------
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
DASH = str.maketrans("–−", "--")
def norm(t):  # strip commas; fold superscripts, dashes and × so tokens compare cleanly
    t = t.replace("⁻", "^-").replace("×", "x")
    return t.translate(SUP).translate(DASH).replace(",", "")

num_re = re.compile(r"\d[\d,]*(?:\.\d+)?")
sci_re = re.compile(r"\d+(?:\.\d+)?x10\^?-?\d+")
oldN, newN = norm(old), norm(new)
ID_RE = r"\b(097e|0659|73b5|3aec|d4ff|f876|f623|8994|5f76|6e76|cd3b|e3a4|a765|262f|cd6e|07b4|fc48|0820|f80a|cc9d|9edc|08d0|7b6f|a9d7|1738|277d|c749)\b"

# short ids of the runs the NEW page cites (its Runs ids + inline shorthands)
cited = set(re.findall(ID_RE, new))

# The old page is hard-wrapped: a number's owning run is named at its PARAGRAPH's
# head ("NEW (5f76, fermi - ..." or an inline [id]), not on every wrapped line.
# Attribution is therefore paragraph-local (blocks separated by blank lines).
para_ids, para_of_line, raw_lines = [], [], old.splitlines()
for raw in raw_lines:
    if not raw.strip():
        para_ids.append(set())  # blank: starts a new paragraph marker
        para_of_line.append(None)
        continue
    if para_of_line and para_of_line[-1] is None:
        para_ids.append(set())
    ids = set(re.findall(ID_RE, raw))
    if not para_ids:
        para_ids.append(set())
    para_ids[-1] |= ids
    para_of_line.append(len(para_ids) - 1)

def covering_ids(line_nos):
    out = set()
    for i in line_nos:
        p = para_of_line[i - 1]
        if p is not None:
            out |= para_ids[p]
    return out

old_lines = norm(old).splitlines()
tokens = {}  # token -> list of old line numbers
for i, ln in enumerate(old_lines, 1):
    for m in num_re.finditer(ln):
        tok = m.group(0)
        if len(tok.replace(".", "")) >= 2:  # skip 1-digit trivial tokens
            tokens.setdefault(tok, []).append(i)

literal, behind, dropped = [], {}, []
for tok, line_nos in tokens.items():
    if tok in newN:
        literal.append(tok)
        continue
    covers = covering_ids(line_nos) & cited
    if covers:
        behind[tok] = sorted(covers)
    else:
        dropped.append((tok, line_nos))

check(not dropped, f"P3 zero dropped tokens (literal {len(literal)}, behind-cited-run {len(behind)}, dropped {len(dropped)})")
cov = len(literal) / len(tokens) * 100 if tokens else 100
check(cov >= 80, f"P3 literal coverage {cov:.1f}% >= 80% ({len(literal)}/{len(tokens)} distinct tokens)")
check(len(behind) < 80, f"P3 residual (behind cited runs) {len(behind)} < 80 distinct tokens")

# compound scientific tokens: verbatim in NEW, or behind a cited run (same rule)
sci_miss2 = []
for s in set(sci_re.findall(oldN)):
    if s in newN:
        continue
    line_nos = [i for i, ln in enumerate(old_lines, 1) if s in ln]
    if not (covering_ids(line_nos) & cited):
        sci_miss2.append(s)
check(not sci_miss2, f"P3 scientific-notation tokens all present or behind a cited run (missing: {sci_miss2})")

# ---------- P4 headline constants (verbatim, superscripts included) ----------
head = ["6.21", "422", "82.5", "44.7", "29.3", "193.4", "57,344", "11.35", "12.42",
        "0.35–1.4", "43.6", "2,348–2,464", "978×", "294×", "5.4–7.0", "−7.1%", "179.7",
        "311", "3,670,016", "7,340,032", "10–42%", "95.7%"]
miss = [h for h in head if h not in new]
check(not miss, f"P4 headline constants all present (missing: {miss})")

# ---------- P5 decided disagreements ----------
refText = section(new, "Refuted")
for pair, a, b in [("θ-mixing", "84.09", "6.21"), ("reserve-exact", "5f76", "6e76"),
                   ("K-rising", "1.45", "2.99"), ("OLS", "f623", "8994")]:
    check(a in refText and b in refText, f"P5 disagreement {a} vs {b} both in Refuted")

# ---------- report ----------
print(f"old page: {len(old.splitlines())} lines, current best {len(old_cb)}")
print(f"new page: {len(new.splitlines())} lines, current best {len(new_cb)}, refuted {len(ref)}, open directions {len(od)}, runs {len(new_ids)}")
print(f"tokens: {len(tokens)} distinct; literal {len(literal)} ({cov:.1f}%); behind cited runs {len(behind)}; dropped {len(dropped)}")
if dropped:
    print("DROPPED (token: old line numbers):")
    for tok, line_nos in dropped[:60]:
        print(f"  {tok}: lines {line_nos}")
if behind:
    print(f"BEHIND-CITED-RUN tokens ({len(behind)}):")
    for tok in sorted(behind):
        print(f"  {tok} <- {','.join(behind[tok])}")
print()
for line in notes:
    print(line)
for line in fails:
    print(line)
print(f"\nAUDIT: {'PASS' if not fails else 'FAIL'} ({len(notes)} passed, {len(fails)} failed)")
sys.exit(1 if fails else 0)
