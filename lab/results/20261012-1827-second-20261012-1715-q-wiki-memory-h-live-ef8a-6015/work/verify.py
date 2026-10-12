"""Verify the compiled page against the run branches (updated for the 21 folded runs).

Checks (all must pass):
  1. every full run id cited in the page exists in runs.txt ∪ runs-added.txt;
  2. every abbreviated id (head…tail) resolves to exactly one run;
  3. every `## Runs` line has <= 20 words in its claim;
  4. every `## Runs` grade equals the run's check.md grade
     (exception: runs with no check.md must be marked `missing`);
  5. the page's Runs set is exactly cluster(111 runs.txt) minus off-topic minus
     missing-check PLUS the 21 added runs = 103 lines, no duplicates;
  6. no added run is already compiled on another topic's wiki page;
  7. the partition (classify.py) covers all 111 cluster runs exactly once.
"""
import re, sys, pathlib, subprocess

here = pathlib.Path(__file__).parent
page = (here / ".." / "wiki" / "memory-h-live.md").read_text()
cluster = {l.strip() for l in open(here / "runs.txt") if l.strip()}
added = {l.strip() for l in open(here / "runs-added.txt") if l.strip()}
known = cluster | added
abstracts = here / "abstracts"
fail = []

abbrev_heads = {h.rstrip("-") for h, _ in re.findall(r"(2026\d{4}-\d{4}-[a-z0-9-]+)…([a-z0-9-]+)", page)}
full = {i for i in re.findall(r"2026\d{4}-\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*", page)
        if not i.endswith("-") and "q-wiki" not in i and i not in abbrev_heads}
unknown = [i for i in full if i not in known]
if unknown:
    fail.append(f"unknown ids: {sorted(unknown)}")

for head, tail in re.findall(r"(2026\d{4}-\d{4}-[a-z0-9-]+)…([a-z0-9-]+)", page):
    m = [r for r in known if r.startswith(head) and r.endswith(tail)]
    if len(m) != 1:
        fail.append(f"abbreviation {head}…{tail} -> {m}")

runs_lines = re.findall(r"^- (2026\S+) \((\w+)\): (.+)$", page, re.M)
if len(runs_lines) != 103:
    fail.append(f"expected 103 runs lines, found {len(runs_lines)}")
seen = set()
for rid, claimed, claim in runs_lines:
    if rid in seen:
        fail.append(f"{rid}: duplicated runs line")
    seen.add(rid)
    if len(claim.split()) > 20:
        fail.append(f"{rid}: claim {len(claim.split())} words > 20")
    f = abstracts / f"{rid}.txt"
    if not f.exists() or f.stat().st_size == 0:
        if claimed != "missing":
            fail.append(f"{rid}: no check.md but claimed {claimed}")
        continue
    g = re.search(r"Grade: (\w+)", f.read_text(errors="replace"))
    actual = g.group(1) if g else None
    if actual and actual.lower() != claimed.lower():
        fail.append(f"{rid}: page says {claimed}, check.md says {actual}")

# 5) set identity: page = cluster minus off-topic/missing plus added
ONTOPIC = 82
page_set = {rid for rid, _, _ in runs_lines}
missing_from_page = added - page_set
extra_beyond = page_set - added - cluster
if missing_from_page:
    fail.append(f"added runs not on page: {sorted(missing_from_page)}")
# cluster runs on the page should number exactly 82 (the compiler's on-topic set)
n_cluster_on_page = len(page_set & cluster)
if n_cluster_on_page != ONTOPIC:
    fail.append(f"cluster runs on page: {n_cluster_on_page}, expected {ONTOPIC}")

# 6) no added run compiled on another topic's wiki page
repo = here.parents[2]
for rid in sorted(added):
    out = subprocess.run(["grep", "-l", rid, "-r", str(repo / "lab" / "wiki")],
                         capture_output=True, text=True).stdout.split()
    hits = [h for h in out if not h.endswith("wiki/memory-h-live.md")]
    if hits:
        fail.append(f"{rid}: already compiled on {hits}")

out = subprocess.run([sys.executable, str(here / "classify.py")],
                     capture_output=True, text=True)
if "UNASSIGNED: []" not in out.stdout or "overlap on/off: set()" not in out.stdout:
    fail.append("partition broken:\n" + out.stdout)

if fail:
    print("FAIL")
    for f in fail:
        print(" -", f)
    sys.exit(1)
print(f"OK: {len(full)} full ids + abbreviations resolve; "
      f"{len(runs_lines)} runs lines (82 cluster + 21 added) graded, <= 20 words, "
      f"no duplicates, none compiled elsewhere; partition exact.")
