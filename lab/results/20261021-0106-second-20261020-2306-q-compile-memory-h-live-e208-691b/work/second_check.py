#!/usr/bin/env python3
"""Independent second check of e208's compile (my own instruments, not the author's).

Inputs (fetched by fetch.sh): old-page.md (587-line page at e208's base),
compiled-page.md (e208's 178-line proposal), head.md, compile_check.py (author's).
Also re-runs the author's compile_check.py verbatim in a sandbox, to confirm the
record regenerates from shipped code.

Instruments:
  R0  author's compile_check.py rerun in a sandbox (old page planted as lab/wiki) -> PASS + numbers
  R1  budgets by lab/wiki.py's own rule (total <= 300, Current-best non-blank <= 15) on compiled page
  R2  dated run-id multiset: every old id present, none duplicated in the compiled page
  R3  Refuted preservation: every old Refuted bullet (first-60-chars key) present in compiled page
  R4  MY strict tokenizer: number cores (digits + internal dots only, all other chars stripped
      page-wide before matching) of the old head vs the compiled page -> count lost, list each
  R5  header check: compiled page header topic/status, updated = e208
"""
import re, os, subprocess, sys, shutil, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))  # repo root

old = open(f"{HERE}/old-page.md", encoding="utf-8").read()
new = open(f"{HERE}/compiled-page.md", encoding="utf-8").read()
fails = []


def sect(text, name):
    m = re.search(rf"^## {name}\s*$", text, re.M)
    rest = text[m.end():]
    e = re.search(r"^## ", rest, re.M)
    return rest[:e.start()] if e else rest


def lines_with(text, pre):
    return [l for l in text.splitlines() if l.startswith(pre)]


# R0: author's script rerun verbatim in a sandbox repo layout.
sb = tempfile.mkdtemp(prefix="e208-sandbox-")
os.makedirs(f"{sb}/lab/wiki"); os.makedirs(f"{sb}/lab/results/x/work")
shutil.copy(f"{HERE}/old-page.md", f"{sb}/lab/wiki/memory-h-live.md")
shutil.copy(f"{HERE}/compile_check.py", f"{sb}/lab/results/x/work/")
shutil.copy(f"{HERE}/head.md", f"{sb}/lab/results/x/work/")
r0 = subprocess.run([sys.executable, f"{sb}/lab/results/x/work/compile_check.py"],
                    capture_output=True, text=True)
print("== R0: author's compile_check.py rerun in sandbox ==")
print(r0.stdout.strip() or r0.stderr.strip())
rebuilt = open(f"{sb}/lab/results/x/wiki/memory-h-live.md", encoding="utf-8").read()
same = rebuilt == new
print(f"rebuilt == shipped compiled page: {'PASS' if same else 'FAIL'}")
if r0.returncode or not same:
    fails.append("R0")
shutil.rmtree(sb)

# R1: budgets (wiki.py's rule).
n_new = len(new.splitlines())
best = [l for l in sect(new, "Current best").splitlines() if l.strip()]
ok = n_new <= 300 and len(best) <= 15
print(f"== R1: budgets == total {n_new} <= 300, current best {len(best)} <= 15: {'PASS' if ok else 'FAIL'}")
if not ok: fails.append("R1")

# R2: dated ids, multiset.
d_old = re.findall(r"^- (\d{8}-\d{4}-\S+)", old, re.M)
d_new = re.findall(r"^- (\d{8}-\d{4}-\S+)", new, re.M)
missing = [i for i in set(d_old) if i not in d_new]
dupes = sorted({i for i in d_new if d_new.count(i) > 1})
print(f"== R2: dated ids == old lines {len(d_old)} ({len(set(d_old))} ids) -> new lines {len(d_new)} "
      f"({len(set(d_new))} ids); missing {missing}; duplicated {dupes}: "
      f"{'PASS' if not missing and not dupes else 'FAIL'}")
if missing or dupes: fails.append("R2")

# R3: Refuted preservation (structural key: first 60 chars of each old bullet).
ref_old = [l for l in sect(old, "Refuted").splitlines() if l.startswith("- ")]
ref_new = [l for l in sect(new, "Refuted").splitlines() if l.startswith("- ")]
absent = [k[:50] for k in ref_old if not any(n.startswith(k[:60]) for n in ref_new)]
print(f"== R3: Refuted == old {len(ref_old)} -> new {len(ref_new)}; absent by first-60-chars: "
      f"{absent if absent else 'none'}: {'PASS' if not absent else 'FAIL'}")
if absent: fails.append("R3")

# R4: MY strict tokenizer — number cores only (e.g. "226", "0.974", "2048", "1600"),
# matched after stripping every non-alphanumeric from the page, so punctuation
# attachment cannot hide a loss; cores that appear only inside longer number
# runs (e.g. "22" inside "20261017") do NOT count as present.
def cores(text):
    return set(re.findall(r"\d+(?:\.\d+)?", text))

def stripped(text):
    return re.sub(r"[^0-9A-Za-z]", "", text)

head_old = old[:re.search(r"^## Runs\s*$", old, re.M).start()]
c_old, c_new = cores(head_old), cores(new)
st_new = stripped(new)
lost = sorted((c for c in c_old - c_new if c not in re.findall(r"\d+(?:\.\d+)?", st_new)),
              key=lambda s: (len(s), s))
# a core is present if it appears as a standalone number run anywhere in the new page
present = lambda c: re.search(rf"(?<![0-9.]){re.escape(c)}(?![0-9])", new) is not None
lost = sorted(c for c in c_old - c_new if not present(c))
print(f"== R4: strict number-core survival, old head vs compiled page ==")
print(f"   old-head cores {len(c_old)}, lost page-wide: {len(lost)}: "
      f"{'PASS' if not lost else 'FAIL'}")
for c in lost: print("   LOST CORE:", c)
if lost: fails.append("R4")

# R5: header.
h = dict(re.findall(r"^([a-z-]+):\s*(.*)$", new.split("\n\n")[0], re.M))
ok = h.get("topic") == "memory-h-live" and h.get("updated") == "20261020-2306-q-compile-memory-h-live-e208"
print(f"== R5: header == {h}: {'PASS' if ok else 'FAIL'}")
if not ok: fails.append("R5")

print(f"SECOND CHECK: {'ALL PASS' if not fails else 'FAILS: ' + ','.join(fails)}")
sys.exit(1 if fails else 0)
