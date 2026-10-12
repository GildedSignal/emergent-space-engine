#!/usr/bin/env python3
"""Regenerate the kick-cadence page's verification record.

Every number quoted in wiki/kick-cadence.md and dossier.md is re-found in its
run's check.md or dossier.md on the published branch; every grade in the page's
## Runs list is re-read from the branch's check.md. Output: regen-out.json.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
REPO = RUN.parents[2]  # lab/results/<run>/ -> repo root

# (full run id, expected grade as listed on the page; None = never graded)
PAGE_RUNS = [
    ("20261005-2231-q-cadence-7d0d", "silver"),
    ("20261006-1029-system-06a8", "silver"),
    ("20261006-1135-quant-a4ed", "gold"),
    ("20261007-0128-b-b17-parallel-cee8", None),
    ("20261007-0341-scout-9abe", "silver"),
    ("20261007-0528-second-20261007-0341-scout-9abe-67be", "gold"),
    ("20261007-1550-system-9205", "lead"),
    ("20261007-1646-scout-0713", "gold"),
    ("20261007-2246-scout-1db4", "silver"),
    ("20261008-0458-second-20261008-0338-library-f045-0102", "silver"),
    ("20261008-0945-library-51bf", "lead"),
    ("20261009-0621-system-7f97", "silver"),
    ("20261009-1936-dynamics-5030", "silver"),
    ("20261010-1152-dynamics-ad35", "silver"),
    ("20261010-1302-library-a2ec", "silver"),
    ("20261010-1816-dynamics-3a4c", "silver"),
    ("20261010-2052-library-2d94", "silver"),
    ("20261010-2141-dynamics-cd52", "silver"),
    ("20261010-2314-library-e5a2", "lead"),
    ("20261010-2314-second-20261010-2141-dynamics-cd52-f2e3", "gold"),
    ("20261011-0224-library-213e", "silver"),
    ("20261011-0836-spacex-0c44", "silver"),
    ("20261011-0924-second-20261011-0836-spacex-0c44-c01c", "gold"),
    ("20261011-2235-library-54d9", "gold"),
    ("20261012-1340-second-20261012-1227-system-8685-2eb1", "gold"),
    # routed to other topics' pages (dossier routing); branch-verified, not listed here
    ("20261009-1754-autoresearch-b727", "lead"),
    ("20261012-0358-second-20261012-0311-scout-6759-0ae6", "gold"),
    ("20261012-1340-autoresearch-887d", "silver"),
]
ROUTED = {"20261009-1754-autoresearch-b727", "20261012-0358-second-20261012-0311-scout-6759-0ae6",
          "20261012-1340-autoresearch-887d"}
MISSING = "20261007-0128-b-b17-parallel-cee8"  # branch exists, checker died at a 429, never graded

# (run id, needle regex) — every number the page and dossier quote.
NEEDLES = [
    ("20261006-1135-quant-a4ed", r"213"), ("20261006-1135-quant-a4ed", r"29 µs"),
    ("20261006-1135-quant-a4ed", r"1\.4e10"), ("20261006-1135-quant-a4ed", r"2\.7"),
    ("20261007-0528-second-20261007-0341-scout-9abe-67be", r"29/30"),
    ("20261007-0528-second-20261007-0341-scout-9abe-67be", r"1\.14"),
    ("20261007-0528-second-20261007-0341-scout-9abe-67be", r"1\.24"),
    ("20261007-0528-second-20261007-0341-scout-9abe-67be", r"operator-precedence"),
    ("20261011-2235-library-54d9", r"1,548"), ("20261011-2235-library-54d9", r"0\.49"),
    ("20261011-2235-library-54d9", r"21,668"),
    ("20261012-1340-second-20261012-1227-system-8685-2eb1", r"84-134"),
    ("20261012-1340-second-20261012-1227-system-8685-2eb1", r"48-175"),
    ("20261012-1340-second-20261012-1227-system-8685-2eb1", r"\+0\.5% at K ?= ?32"),
    ("20261012-1340-second-20261012-1227-system-8685-2eb1", r"\+2\.5% at K ?= ?16"),
    ("20261011-0924-second-20261011-0836-spacex-0c44-c01c", r"60/64"),
    ("20261011-0924-second-20261011-0836-spacex-0c44-c01c", r"1292\.4"),
    ("20261011-0924-second-20261011-0836-spacex-0c44-c01c", r"2,578"),
    ("20261011-0924-second-20261011-0836-spacex-0c44-c01c", r"4-6"),
    ("20261011-0924-second-20261011-0836-spacex-0c44-c01c", r"12\.9"),
    ("20261009-1936-dynamics-5030", r"4-10 kicks per secular"),
    ("20261009-1936-dynamics-5030", r"T_sec/20"), ("20261009-1936-dynamics-5030", r"1613"),
    ("20261009-1936-dynamics-5030", r"15-60"),
    ("20261010-1152-dynamics-ad35", r"n\^?-2\.1"), ("20261010-1152-dynamics-ad35", r"693"),
    ("20261005-2231-q-cadence-7d0d", r"4/8/16"), ("20261005-2231-q-cadence-7d0d", r"0\.2/0\.3/0\.45"),
    ("20261005-2231-q-cadence-7d0d", r"4\.4%"), ("20261005-2231-q-cadence-7d0d", r"9\.7%"),
    ("20261006-1029-system-06a8", r"8/orbit"), ("20261006-1029-system-06a8", r"8\.1 evals/orbit"),
    ("20261007-1646-scout-0713", r"1\.4-30"), ("20261007-1646-scout-0713", r"1\.03"),
    ("20261008-0945-library-51bf", r"1\.92"),
    ("20261010-1302-library-a2ec", r"1\.65"), ("20261010-1302-library-a2ec", r"11\.6"),
    ("20261010-1302-library-a2ec", r"3\.5"),
    ("20261010-2052-library-2d94", r"2\.8-6\.7"), ("20261010-2052-library-2d94", r"14-18"),
    ("20261010-2141-dynamics-cd52", r"2\.303e-2"), ("20261010-2141-dynamics-cd52", r"512/orbit"),
    ("20261010-2314-second-20261010-2141-dynamics-cd52-f2e3", r"2\.2e6"),
    ("20261010-2314-second-20261010-2141-dynamics-cd52-f2e3", r"1\.11"),
    ("20261010-2314-second-20261010-2141-dynamics-cd52-f2e3", r"1\.56"),
    ("20261010-2314-second-20261010-2141-dynamics-cd52-f2e3", r"0\.15"),
    ("20261010-2314-second-20261010-2141-dynamics-cd52-f2e3", r"2\.0e6"),
    ("20261011-0224-library-213e", r"33/132/704"), ("20261011-0224-library-213e", r"20-130"),
    ("20261011-0224-library-213e", r"1\.5-2\.4"),
    ("20261007-2246-scout-1db4", r"2 kicks per orbit"), ("20261007-2246-scout-1db4", r"16-32"),
    ("20261009-0621-system-7f97", r"16 kicks per"), ("20261009-0621-system-7f97", r"60/64"),
    ("20261009-0621-system-7f97", r"62/64"), ("20261009-0621-system-7f97", r"41/64"),
    ("20261009-0621-system-7f97", r"3/64"), ("20261009-0621-system-7f97", r"5x of"),
    ("20261008-0458-second-20261008-0338-library-f045-0102", r"71\.6"),
    ("20261008-0458-second-20261008-0338-library-f045-0102", r"75\.2"),
    ("20261007-1550-system-9205", r"cosν"),
    ("20261010-2314-library-e5a2", r"2\.5e-3"),
    ("20261010-1816-dynamics-3a4c", r"\+0\.948"),
    ("20261011-0836-spacex-0c44", r"43 µs"), ("20261011-0836-spacex-0c44", r"44\.2"),
    ("20261011-0836-spacex-0c44", r"NoBoundOrbit"),
    # routed runs (quoted in the dossier's routing table)
    ("20261009-1754-autoresearch-b727", r"≤ ?3%|<= ?3%"),
    ("20261009-1754-autoresearch-b727", r"1932f6c"),
    ("20261012-1340-autoresearch-887d", r"19\.7"), ("20261012-1340-autoresearch-887d", r"20\.8"),
    ("20261012-0358-second-20261012-0311-scout-6759-0ae6", r"45-80"),
    ("20261012-0358-second-20261012-0311-scout-6759-0ae6", r"34\.4"),
]


def show(ref: str):
    p = subprocess.run(["git", "show", ref], capture_output=True, text=True, cwd=REPO)
    return p.stdout if p.returncode == 0 else None


def norm(s: str) -> str:
    return (s.replace("–", "-").replace("—", "-").replace("−", "-")
             .replace("×", "x").replace("\u2009", "").replace("\u00a0", " "))


def main() -> int:
    docs, grades = {}, {}
    for rid, _ in PAGE_RUNS:
        entry = {}
        for doc in ("check", "dossier"):
            t = show(f"origin/claude/lab-{rid}:lab/results/{rid}/{doc}.md")
            if t is not None:
                entry[doc] = norm(t)
        docs[rid] = entry
        m = re.search(r"^Grade:\s*(\w+)", entry.get("check", ""), re.M) if entry.get("check") else None
        grades[rid] = m.group(1).lower() if m else None

    failures = []
    page = norm((RUN / "wiki" / "kick-cadence.md").read_text())
    listed = dict(re.findall(r"^- (\S+) \((\w+)\):", page, re.M))

    # 1. grades: page == branch == expectation; routed runs verified on branch only
    for rid, expected in PAGE_RUNS:
        got = grades[rid] or ("no-grade" if docs[rid] else "missing")
        if expected is None:  # the never-graded entry
            finals = show(f"origin/claude/lab-{rid}:lab/results/{rid}/author-final.md")
            if got != "no-grade" or not (finals and finals.strip()):
                failures.append(f"{rid}: expected never-graded author-final-only, got {got}")
            elif listed.get(rid) != "missing":
                failures.append(f"{rid}: page lists {listed.get(rid)}, expected 'missing'")
        elif rid in ROUTED:
            if got != expected:
                failures.append(f"routed {rid}: branch={got} expected={expected}")
        else:
            if listed.get(rid) != expected or got != expected:
                failures.append(f"{rid}: page={listed.get(rid)} branch={got} expected={expected}")
    expected_ids = {r for r, e in PAGE_RUNS if e and r not in ROUTED} | {MISSING}
    if set(listed) != expected_ids:
        failures.append(f"page Runs ids != verified ids: extra={set(listed) - expected_ids} "
                        f"absent={expected_ids - set(listed)}")

    # 2. every quoted number is found in its run's branch docs
    for rid, needle in NEEDLES:
        blob = docs.get(rid, {})
        hay = blob.get("check", "") + "\n" + blob.get("dossier", "")
        if not re.search(norm(needle), hay, re.I):
            failures.append(f"needle /{needle}/ not found in {rid}")

    # 3. short ids cited in the page body resolve to a Runs entry
    shorts = {r.split("-")[-1]: r for r, e in PAGE_RUNS if e}
    body = page.split("## Runs")[0]
    for sid in re.findall(r"\(([0-9a-f]{4}(?:;[0-9a-f]{4})*)\)", body):
        for s in sid.split(";"):
            if s not in shorts:
                failures.append(f"page cites unknown short id {s}")

    out = {
        "page_runs_listed": len(listed),
        "graded_gold_on_page": sum(1 for r, e in PAGE_RUNS if e == "gold" and r in listed),
        "needles_checked": len(NEEDLES),
        "failures": failures,
        "ok": not failures,
    }
    (RUN / "regen-out.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
