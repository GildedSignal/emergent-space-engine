#!/usr/bin/env python3
"""Verify the compiled encounters page against the raw runs (P1-P5 of predictions.md).

Re-derives: the 65-run partition (encounters / routed-by-topic / no-record),
every run's grade from its own check.md, the page's Runs list, the coorbital-cert
disjointness, and five sampled in-text claims against their cited sources.
Exit 0 iff everything matches. No network; reads git refs and the working tree.
"""
import re, subprocess, sys

RUN = "lab/results/20261012-1827-q-wiki-encounters-e8e3"
PAGE = f"{RUN}/wiki/encounters.md"

ALL = """20261006-0030-library-39a2
20261006-0220-scout-4ea2
20261006-0346-inversion-8cee
20261006-0437-components-2222
20261006-0437-dynamics-43d5
20261006-0519-rung-r8-encounters-v4-0e5d
20261006-0521-rung-r8-encounters-v4-6cd5
20261006-0737-components-4643
20261006-1029-dynamics-6875
20261006-1135-spacex-317c
20261006-1249-library-8f99
20261006-1436-autoresearch-cdf8
20261006-1436-scout-eab7
20261006-1545-second-20261006-1436-scout-eab7-73f0
20261006-2240-b-encounter-skin-8bfa
20261007-0341-second-20261006-2240-b-encounter-skin-8bfa-57c1
20261007-0621-autoresearch-f521
20261007-0711-taleb-2e81
20261007-0933-system-0510
20261007-1032-quant-7578
20261007-1234-dynamics-da90
20261007-1550-dynamics-71a5
20261007-1801-dynamics-532c
20261007-1843-dynamics-1b1f
20261007-2002-library-b2d5
20261007-2002-second-20261007-1918-scout-3da3-3fb7
20261007-2246-system-969a
20261007-2344-second-20261007-2246-system-969a-5d90
20261008-0338-redteam-4e7c
20261008-0615-library-83f9
20261008-0945-taleb-48e5
20261008-1058-second-20261008-0945-taleb-48e5-abd7
20261008-1419-dynamics-5cbd
20261008-1521-second-20261008-1419-system-2f89-75aa
20261008-1859-autoresearch-b62c
20261008-2031-dynamics-87da
20261008-2113-scout-6652
20261009-0401-second-20261009-0208-fermi-fe6b-90fb
20261009-0521-library-189e
20261009-0621-second-20261009-0521-redteam-93a4-e93c
20261009-0819-library-5959
20261009-1345-second-20261009-1259-fermi-c7eb-46a6
20261009-1345-system-136a
20261009-1504-second-20261009-1345-system-136a-ca96
20261009-1649-system-aa29
20261009-1858-library-c716
20261009-1936-system-8716
20261009-2043-second-20261009-1936-system-8716-88ee
20261009-2120-library-30a7
20261009-2212-dynamics-79ef
20261009-2212-second-20261009-2120-taleb-8ea0-bd6a
20261010-0541-dynamics-6565
20261010-1029-taleb-5c01
20261010-1920-autoresearch-ccc6
20261010-1947-second-20261010-1920-spacex-cb3f-f79a
20261011-0517-quant-d7bd
20261011-0736-dynamics-ec74
20261011-0924-library-9834
20261011-1102-second-20261011-0924-library-9834-5c16
20261011-1234-taleb-62f7
20261011-2132-autoresearch-a85a
20261011-2132-second-20261011-2028-system-3b42-214f
20261011-2306-constraint-9e62
20261012-1227-system-8685
20261012-1340-quant-e49d""".split()

ROUTED = {  # id -> (topic, reason) ; graded records that belong to another page
 "20261006-0030-library-39a2": "kick-cadence",
 "20261007-0933-system-0510": "kick-cadence",
 "20261008-0615-library-83f9": "kick-cadence",
 "20261008-1419-dynamics-5cbd": "kick-cadence",
 "20261012-1227-system-8685": "kick-cadence",
 "20261007-2002-second-20261007-1918-scout-3da3-3fb7": "gravity-news",
 "20261008-1521-second-20261008-1419-system-2f89-75aa": "b12-statistic",
 "20261009-2212-second-20261009-2120-taleb-8ea0-bd6a": "memory-h-live",
 "20261011-2306-constraint-9e62": "frame-cost",
}
NO_RECORD = [  # no graded record on the branch
 "20261006-0519-rung-r8-encounters-v4-0e5d",   # VOID rung; topic coorbital-cert
 "20261006-0521-rung-r8-encounters-v4-6cd5",   # VOID rung; topic coorbital-cert
 "20261008-1859-autoresearch-b62c",
 "20261009-0621-second-20261009-0521-redteam-93a4-e93c",
 "20261009-0819-library-5959",
]

def show(rid, path):
    r = subprocess.run(["git", "show", f"origin/claude/lab-{rid}:{path}"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None

def grade_of(rid):
    check = show(rid, f"lab/results/{rid}/check.md")
    if check is None:
        return None
    m = re.search(r"Grade:\s*(gold|silver|lead)", check)
    return m.group(1) if m else None

fail = []

# --- P1/P2: partition and grades -------------------------------------------------
encounters = [i for i in ALL if i not in ROUTED and i not in NO_RECORD]
assert len(encounters) + len(ROUTED) + len(NO_RECORD) == len(ALL) == 65
grades = {}
for rid in ALL:
    grades[rid] = grade_of(rid)
for rid in NO_RECORD:
    if rid.endswith(("0e5d", "6cd5")):  # rungs: verdict.txt must say VOID
        v = show(rid, f"lab/results/{rid}/verdict.txt") or ""
        if "VOID" not in v:
            fail.append(f"P2 {rid}: rung verdict not VOID: {v.strip()!r}")
    elif grades[rid] is not None:
        fail.append(f"P2 {rid}: expected no graded record, found grade {grades[rid]}")

page = open(PAGE).read()
runs_section = page.split("## Runs", 1)[1]
page_runs = re.findall(r"^- (\S+) \((gold|silver|lead)\):", runs_section, re.M)
page_ids = {i for i, g in page_runs}

if page_ids != set(encounters):
    fail.append(f"P1 page/run-set mismatch: only-page={sorted(page_ids-set(encounters))} "
                f"only-partition={sorted(set(encounters)-page_ids)}")
for rid, g in page_runs:
    if grades[rid] != g:
        fail.append(f"P2 {rid}: page says {g}, check.md says {grades[rid]}")

from collections import Counter
tally = Counter(g for _, g in page_runs)
expect = {"gold": 18, "silver": 29, "lead": 4}
if dict(tally) != expect:
    fail.append(f"P1 grade tally {dict(tally)} != {expect}")
print(f"P1/P2: {len(page_runs)} runs on page, tally {dict(tally)}; "
      f"routed {len(ROUTED)}, no-record {len(NO_RECORD)}")

# --- P4: disjoint from the coorbital-cert page ------------------------------------
coorb = open("lab/wiki/coorbital-cert.md").read()
coorb_ids = set(re.findall(r"^- (\S+) \(", coorb.split("## Runs", 1)[1], re.M))
overlap = page_ids & coorb_ids
if overlap:
    fail.append(f"P4 overlap with coorbital-cert: {sorted(overlap)}")
print(f"P4: coorbital-cert lists {len(coorb_ids)} runs; overlap {sorted(overlap) or 'none'}")

# --- P3: five sampled in-text claims against their cited sources ------------------
SAMPLES = [  # (claim on page, run id, list of substrings expected in check.md/dossier.md)
 ("horizon edge 20.2% / 284/1407", "20261010-1029-taleb-5c01",
  ["20.2", "284/1407"]),
 ("engagement store 144 TB, tier sound", "20261007-0711-taleb-2e81",
  ["144 TB", "0 missed"]),
 ("cascade law 0.0346", "20261009-0401-second-20261009-0208-fermi-fe6b-90fb",
  ["0.0346"]),
 ("key sound domain e≈0.969, 206/289", "20261007-2344-second-20261007-2246-system-969a-5d90",
  ["0.969", "206/289"]),
 ("skin build setups 142.3→17.1", "20261006-2240-b-encounter-skin-8bfa",
  ["142.3", "17.1"]),
 ("m_crit 1.3e-17 Msun", "20261009-1345-second-20261009-1259-fermi-c7eb-46a6",
  ["10⁻¹⁷"]),
]
for label, rid, needles in SAMPLES:
    blobs = [b for b in (show(rid, f"lab/results/{rid}/check.md"),
                         show(rid, f"lab/results/{rid}/dossier.md")) if b]
    missing = [n for n in needles if not any(n in b for b in blobs)]
    status = "OK " if not missing else "FAIL"
    if missing:
        fail.append(f"P3 {label} ({rid}): substrings not found: {missing}")
    print(f"P3: {status} {label} [{rid}]")

print()
if fail:
    print("FAILURES:")
    for f in fail:
        print(" -", f)
    sys.exit(1)
print("ALL CHECKS PASS: page is regenerable and faithful to the refs.")
