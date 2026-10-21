#!/usr/bin/env python3
"""The gold bar, applied to every number: each numeric token of the old page must appear
in the compiled page or behind a cited run (its branch artifacts). Also checks the wiki.py
budgets (old and new) and run-line conservation. Usage: python3 compile_check.py (repo root)."""
import re, subprocess, sys, collections

RUN = "20261021-0142-q-compile-cell-rebind-4c5b"
NEW = f"lab/results/{RUN}/wiki/cell-rebind.md"
CITED = ["20261018-2312-system-9eeb", "20261019-1316-components-ef8c",
         "20261019-1316-system-f7c3", "20261019-1452-second-20261019-1316-system-f7c3-6e91"]
ART = ["dossier.md", "predictions.md", "regen.txt", "regen.log", "author-final.md",
       "checker-final.md", "checker2-final.md", "check.md", "check2.md", "wiki/cell-rebind.md"]

SUP = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7",
       "⁸": "8", "⁹": "9", "⁻": "-"}

def norm(t):
    out = []
    for c in t:
        if c in SUP:
            out.append("^" + SUP[c] if out and out[-1].isdigit() and c != "⁻" else
                       ("^-" if c == "⁻" and out and out[-1].isdigit() else SUP[c]))
        else:
            out.append(c)
    return re.sub(r"(\d),(\d{3})\b", r"\1\2", "".join(out))

def toks(t):
    return set(re.findall(r"\d+(?:\.\d+)?(?:\^-?\d+)?(?:[eE][+-]?\d+)?", norm(t)))

def show(ref):
    r = subprocess.run(["git", "show", ref], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None

def budget(text):
    body = text.split("## Runs", 1)[0]
    best = [l for l in body.split("## Current best", 1)[-1].split("\n## ", 1)[0].splitlines() if l.strip()]
    return len(best), len(text.splitlines())

old = show("HEAD:lab/wiki/cell-rebind.md")  # the pre-compile page (patch not applied yet here)
if old is None:
    old = subprocess.run(["git", "show", "origin/main:lab/wiki/cell-rebind.md"],
                         capture_output=True, text=True).stdout
new = open(NEW).read()
fail = 0

# --- budgets, exactly wiki.py's rule ---
ob, ot = budget(old)
nb, nt = budget(new)
print(f"old page (HEAD): current best {ob} non-blank lines, {ot} lines -> "
      f"{'over budget (as the index flagged)' if ob > 15 or ot > 300 else 'within budget'}")
print(f"new page: current best {nb} non-blank lines (limit 15), {nt} lines (limit 300)")
if nb > 15 or nt > 300:
    print("FAIL: new page over budget"); fail += 1

# --- run-line conservation: ids, grades, claim heads ---
old_ids = re.findall(r"^- (\d{8}-\d{4}-\S+) \(([^)]+)\): (.*)$", old, re.M)
new_ids = re.findall(r"^- (\d{8}-\d{4}-\S+) \(([^)]+)\): (.*)$", new, re.M)
old_by_id = collections.defaultdict(list)
for i, g, c in old_ids:
    old_by_id[i].append((g, c))
new_by_id = {i: (g, c) for i, g, c in new_ids}
print(f"runs: old {len(old_ids)} lines ({len(old_by_id)} ids), new {len(new_ids)} lines (one per id)")
for i, lines in old_by_id.items():
    if i not in new_by_id:
        print(f"FAIL: run id lost: {i}"); fail += 1; continue
    for g, c in lines:
        head = " ".join(c.split()[:5])
        if head not in new_by_id[i][1] and head.replace(" ", "") not in new_by_id[i][1].replace(" ", ""):
            print(f"FAIL: claim head changed for {i}: {head!r} -> {new_by_id[i][1][:80]}"); fail += 1
for i, (g, c) in new_by_id.items():
    r = subprocess.run(["git", "log", "-1", "--format=%s", f"origin/claude/lab-{i}"],
                       capture_output=True, text=True)
    m = re.search(r"Grade: (\w+)", r.stdout)
    grade = m.group(1) if m else "unknown"
    if grade != g:
        print(f"FAIL: grade mismatch {i}: page says {g}, branch says {grade}"); fail += 1

# --- number conservation ---
corpus = {}
for rid in CITED:
    for f in ART:
        t = show(f"origin/claude/lab-{rid}:lab/results/{rid}/{f}")
        if t:
            corpus[(rid, f)] = toks(t)
old_t, new_t = toks(old), toks(new)
behind = {t: src for t in (old_t - new_t)
          for src in [next((k for k, s in corpus.items() if t in s), None)] if src}
missing = sorted(t for t in (old_t - new_t) if t not in behind)
print(f"numbers: {len(old_t)} distinct old-page tokens; {len(old_t & new_t)} in the new page; "
      f"{len(behind)} behind a cited run; {len(missing)} LOST")
for t in sorted(behind, key=lambda x: (len(x), x)):
    print(f"  behind {behind[t][0]}/{behind[t][1].split('/')[-1]}: {t}")
for t in missing:
    print(f"  LOST: {t}")
if missing:
    fail += 1

print("VERDICT:", "FAIL" if fail else "PASS — budget clear, runs kept, every number conserved")
sys.exit(1 if fail else 0)
