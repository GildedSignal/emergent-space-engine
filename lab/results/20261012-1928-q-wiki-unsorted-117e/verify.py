#!/usr/bin/env python3
"""Verify the sorting of the 81 unsorted runs against the lab branches.

Checks (predictions P1-P5 in predictions.md): two-checker grades vs the
assignment sheet, dossier presence, already-placed runs on today's wiki
pages, second-author parent branches, and topic counts. Run from the repo
root: `python3 lab/results/20261012-1928-q-wiki-unsorted-117e/verify.py`.
Writes work/verify-out.txt.
"""
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
WIKI = HERE.parent.parent / "wiki"

PLACEMENTS = {
    "20261005-2231-m-micro-numbers-13dd": "changeover",
    "20261006-0030-q-kerr-compile-0528": "handoff",
    "20261006-0220-autoresearch-c3a5": "kick-jet",
    "20261006-0220-quant-9e04": "smoothness",
    "20261006-0346-library-563d": "smoothness",
    "20261006-0437-constraint-ec9d": "kick-jet",
    "20261006-0737-scout-b73e": "smoothness",
    "20261006-1101-autoresearch-52e5": "contacts",
    "20261006-1101-quant-5457": "smoothness",
    "20261006-1101-spacex-ef61": "kick-jet",
    "20261006-1135-scout-7a46": "plunge-tubes",
    "20261006-1436-components-ed09": "frame-cost",
    "20261006-1738-second-20261006-1436-quant-18e5-55ca": "smoothness",
    "20261006-2240-second-20261006-1738-b-kerr-compiler-fa4b-6586": "handoff",
    "20261007-0341-autoresearch-9dc2": "kick-jet",
    "20261007-0711-library-9ab7": "smoothness",
    "20261007-0800-second-20261007-0711-library-9ab7-480e": "smoothness",
    "20261007-1032-spacex-3d04": "smoothness",
    "20261007-1334-autoresearch-a235": "kick-jet",
    "20261007-1334-second-20261007-1234-components-97bf-98e6": "frame-cost",
    "20261007-1420-redteam-9fbd": "binet-cells",
    "20261007-1646-second-20261007-1550-dynamics-71a5-f282": "encounters",
    "20261007-1918-autoresearch-db5f": "kick-jet",
    "20261008-0148-second-20261008-0041-redteam-ecfd-90ec": "handoff",
    "20261008-0234-second-20261008-0148-system-098e-bd06": "gravity-news",
    "20261008-0234-spacex-0083": "kick-jet",
    "20261008-0338-library-f045": "kick-cadence",
    "20261008-0458-dynamics-7166": "contacts",
    "20261008-0615-redteam-cc34": "resonance-gate",
    "20261008-1252-second-20261008-1150-system-cf13-3565": "encounters",
    "20261008-1252-taleb-2570": "smoothness",
    "20261008-1337-second-20261008-1252-taleb-2570-9420": "smoothness",
    "20261008-1419-components-620e": "kick-jet",
    "20261008-1419-system-2f89": "b12-statistic",
    "20261008-1521-autoresearch-a48d": "kick-jet",
    "20261008-1757-constraint-1c2e": "kick-jet",
    "20261008-1757-dynamics-2a25": "smoothness",
    "20261008-1859-quant-19d6": "smoothness",
    "20261008-2113-autoresearch-687b": "view",
    "20261008-2206-second-20261008-2113-scout-6652-3eee": "encounters",
    "20261009-0401-autoresearch-e044": "kick-jet",
    "20261009-0621-dynamics-0a0b": "memory-h-live",
    "20261009-0709-autoresearch-b2a0": "kick-jet",
    "20261009-0709-second-20261009-0621-system-7f97-1eca": "kick-cadence",
    "20261009-1754-second-20261009-1649-system-aa29-0ee9": "resonance-gate",
    "20261009-2120-second-20261009-2043-scout-a1a4-a194": "plunge-tubes",
    "20261009-2257-second-20261009-2212-fermi-a11b-ba64": "memory-h-live",
    "20261009-2348-autoresearch-19f8": "kick-jet",
    "20261010-0100-second-20261009-2348-scout-3851-0d8c": "handoff",
    "20261010-0448-redteam-f771": "binet-cells",
    "20261010-0541-second-20261010-0448-redteam-f771-9999": "binet-cells",
    "20261010-0656-autoresearch-cc88": "kick-jet",
    "20261010-0920-autoresearch-1411": "contacts",
    "20261010-1029-second-20261010-0920-scout-e5f5-0c3b": "gravity-news",
    "20261010-1302-second-20261010-1152-fermi-e9a5-a9c4": "memory-h-live",
    "20261010-1706-redteam-e07f": "binet-cells",
    "20261010-1816-second-20261010-1706-redteam-e07f-311d": "binet-cells",
    "20261010-1920-second-20261010-1816-system-67f2-3ea5": "kick-cadence",
    "20261010-2052-second-20261010-1947-spacex-19bc-d205": "memory-h-live",
    "20261010-2220-autoresearch-2fe1": "kick-jet",
    "20261011-0134-autoresearch-2d92": "contacts",
    "20261011-0614-second-20261011-0517-taleb-3ebf-b04d": "coorbital-cert",
    "20261011-0736-system-785d": "resonance-gate",
    "20261011-0836-second-20261011-0736-system-785d-07b5": "resonance-gate",
    "20261011-1234-second-20261011-1102-scout-4c5b-dde0": "gravity-news",
    "20261011-1456-autoresearch-bb4d": "kick-jet",
    "20261011-1456-scout-126c": "plunge-tubes",
    "20261011-1600-second-20261011-1456-scout-126c-640f": "plunge-tubes",
    "20261011-1814-taleb-762d": "smoothness",
    "20261011-2028-components-6a0e": "memory-h-live",
    "20261011-2028-dynamics-7807": "encounters",
    "20261011-2028-second-20261011-1917-redteam-fb64-7521": "view",
    "20261011-2132-quant-fca2": "smoothness",
    "20261012-0036-autoresearch-e3ca": "kick-jet",
    "20261012-0138-second-20261012-0036-scout-aac1-2da8": "handoff",
    "20261012-0311-autoresearch-3d4e": "kick-jet",
    "20261012-0358-autoresearch-ff43": "kick-jet",
    "20261012-0753-quant-dafc": "smoothness",
    "20261012-1019-autoresearch-c549": "kick-jet",
    "20261012-1019-second-20261012-0753-quant-dafc-9a07": "smoothness",
    "20261012-1117-second-20261012-1019-spacex-3463-c304": "memory-h-live",
}

MISSING = {"20261009-0621-dynamics-0a0b", "20261010-2220-autoresearch-2fe1"}

EXPECT_PLACED = {  # P4: already on a wiki page updated today (12 October)
    "20261006-0220-autoresearch-c3a5", "20261006-0437-constraint-ec9d",
    "20261008-0234-spacex-0083", "20261008-1419-components-620e",
    "20261008-1521-autoresearch-a48d", "20261009-2257-second-20261009-2212-fermi-a11b-ba64",
    "20261010-1302-second-20261010-1152-fermi-e9a5-a9c4",
    "20261010-2052-second-20261010-1947-spacex-19bc-d205",
    "20261011-2028-components-6a0e", "20261012-1117-second-20261012-1019-spacex-3463-c304",
    "20261006-2240-second-20261006-1738-b-kerr-compiler-fa4b-6586",
    "20261010-0100-second-20261009-2348-scout-3851-0d8c",
    "20261012-0138-second-20261012-0036-scout-aac1-2da8",
}

SLUG_PAGES = ["kick-jet", "frame-cost", "memory-h-live", "handoff", "encounters",
              "kick-cadence", "gravity-news", "view", "b12-statistic",
              "coorbital-cert", "belt", "high-gamma-clock"]


def sh(*args):
    return subprocess.run(args, capture_output=True, text=True).stdout


def first_grade(rid, which):
    txt = sh("git", "show", f"origin/claude/lab-{rid}:lab/results/{rid}/{which}")
    m = re.findall(r"grade[^\n]{0,40}?(\b(?:gold|silver|lead|void)\b)", txt, re.I)
    return m[0].lower() if m else None


def sheet_grades():
    grades = {}
    for line in (WORK / "sheet_grades.txt").read_text().splitlines():
        rid, grade = line.split()
        grades[rid] = grade
    return grades


def main():
    out = []
    ids = sorted(PLACEMENTS)
    sheet = sheet_grades()
    assert len(ids) == 81, f"expected 81 runs, got {len(ids)}"
    assert set(ids) == set(sheet), "placement ids != sheet ids"

    # P3: counts
    counts = Counter(PLACEMENTS.values())
    out.append("P3 topic counts: " + ", ".join(f"{k}={v}" for k, v in counts.most_common()))

    # P5/P1: dossiers present; sheet grade equals the two-checker rule
    grade_mismatch, missing_dossier = [], []
    for rid in ids:
        dos = WORK / "dossiers" / f"{rid}.md"
        if not dos.exists() or len(dos.read_text().strip()) < 200:
            missing_dossier.append(rid)
            continue
        if rid in MISSING:
            continue
        g1 = first_grade(rid, "check.md")
        g2 = first_grade(rid, "check2.md")
        if g1 == "gold" and g2 == "gold":
            derived = "gold"
        elif g1 is None and g2 is None:
            derived = "unrecorded"
        elif "lead" in (g1, g2) and "gold" not in (g1, g2):
            derived = "lead"
        else:
            derived = "silver"
        if derived not in (sheet[rid], "unrecorded"):
            grade_mismatch.append((rid, sheet[rid], g1, g2, derived))
    out.append(f"P5 missing/short dossiers: {missing_dossier or 'none'}")
    out.append(f"P1 sheet-vs-two-checker mismatches: {grade_mismatch or 'none'}")

    # P4: already on a wiki page. Match run ids only as Runs-list entries or
    # parenthesised citations — a second author's id embeds its parent's id.
    already = set()
    for page in SLUG_PAGES:
        txt = (WIKI / f"{page}.md").read_text()
        for rid in ids:
            if (re.search(rf"^- {re.escape(rid)} ?\(", txt, re.M)
                    or re.search(rf"[-–—( ]{re.escape(rid)}[,;) ]", txt)):
                already.add(rid)
    extra = already - EXPECT_PLACED
    out.append(f"P4 already-placed found: {len(already)}; "
               f"predicted-but-not-found: {sorted(EXPECT_PLACED - already) or 'none'}; "
               f"found-but-unpredicted: {sorted(extra) or 'none'}")

    # P2: second-author runs; the parent id strips this run's own 4-hex suffix.
    parent_missing = []
    for rid in ids:
        m = re.match(r"\d{8}-\d{4}-second-(.+)-[0-9a-f]{4}$", rid)
        if not m:
            continue
        parent = m.group(1)
        if not sh("git", "show",
                  f"origin/claude/lab-{parent}:lab/results/{parent}/dossier.md"):
            parent_missing.append((rid, parent))
    out.append(f"P2 second-author runs with missing parent branches: "
               f"{parent_missing or 'none'}")

    (WORK / "verify-out.txt").write_text("\n".join(out) + "\n")
    print("\n".join(out))
    return 1 if (grade_mismatch or missing_dossier or parent_missing
                 or extra or (EXPECT_PLACED - already)) else 0


if __name__ == "__main__":
    sys.exit(main())
