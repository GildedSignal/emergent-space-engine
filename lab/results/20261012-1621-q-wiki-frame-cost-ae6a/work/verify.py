#!/usr/bin/env python3
"""Verify the compiled frame-cost page against the raw run branches.

Regenerates, from `git show origin/claude/lab-<id>:lab/results/<id>/check.md`:
the grade of every run, then checks the page (wiki/frame-cost.md) for
faithfulness: every Runs-line run is classified frame-cost, every cited id
exists in the cluster, grades match, claim lines fit 20 words, and the
per-topic classification counts match the dossier. Exit 0 = all checks pass.
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs.txt"
PAGE = HERE.parent / "wiki" / "frame-cost.md"

# classification of the 68 clustered runs, decided by this compile (see dossier)
TOPICS = {
    "frame-cost": [
        "20261006-1135-autoresearch-eb29", "20261006-1354-constraint-df79",
        "20261007-1234-system-2517", "20261007-1646-autoresearch-a191",
        "20261007-1801-second-20261007-1646-autoresearch-a191-18df",
        "20261007-2246-components-4955", "20261007-2344-quant-4211",
        "20261008-0234-quant-2300", "20261008-0615-taleb-40c0",
        "20261008-0743-second-20261008-0615-taleb-40c0-a342",
        "20261008-1252-quant-291f", "20261009-0709-quant-6766",
        "20261009-2043-autoresearch-d4f1", "20261009-2043-quant-3cfc",
        "20261010-0656-quant-d540", "20261010-0656-spacex-2439",
        "20261010-1302-spacex-6785", "20261010-1544-system-97ce",
        "20261010-1920-spacex-cb3f", "20261010-1947-autoresearch-2833",
        "20261010-2141-constraint-ae40", "20261011-0736-components-825f",
        "20261011-0836-autoresearch-469c", "20261011-1102-quant-ba35",
        "20261011-1729-components-b063",
        "20261011-1917-second-20261011-1814-taleb-762d-119f",
        "20261011-2306-system-3367", "20261012-0036-quant-115e",
        "20261012-0616-system-1537", "20261012-1019-quant-b29b",
    ],
    "view": [
        "20261007-0528-constraint-6094", "20261007-0800-constraint-7a39",
        "20261007-0842-constraint-0411", "20261007-1550-constraint-578e",
        "20261007-1801-constraint-3126", "20261007-1843-constraint-2658",
        "20261007-2155-constraint-b952", "20261008-0743-constraint-4588",
        "20261008-1058-constraint-caa2", "20261008-1719-constraint-1fe2",
        "20261008-2031-constraint-4b27", "20261009-1210-constraint-c10d",
        "20261009-1210-second-20261009-0621-constraint-51bf-97bc",
        "20261009-1259-constraint-2666", "20261009-1504-redteam-2320",
        "20261009-1556-redteam-18fc",
        "20261009-1556-second-20261009-1504-redteam-2320-56bc",
        "20261009-1936-constraint-8af7", "20261009-2212-constraint-2380",
        "20261009-2257-constraint-842c", "20261010-0100-constraint-c97d",
        "20261010-0352-quant-3435",
        "20261010-0448-second-20261010-0352-taleb-cb7c-c2f8",
        "20261010-0814-constraint-f3f1", "20261010-1029-redteam-435b",
        "20261010-1152-constraint-c575", "20261010-1407-constraint-775f",
        "20261010-1920-quant-9464", "20261011-0324-constraint-986f",
        "20261011-1600-constraint-2094",
        "20261011-1729-second-20261011-1600-constraint-2094-07b8",
        "20261011-1814-quant-f8f9", "20261012-1019-spacex-3463",
        "20261012-1227-constraint-cf31",
    ],
    "memory-h-live": [
        "20261007-1843-fermi-1feb", "20261010-1706-fermi-2914",
        "20261010-1816-components-6273",
    ],
    "kick-cadence": ["20261006-0220-redteam-fermi2-v2-b7a4"],
}
# one grade drift between the cluster list and the branch's check.md,
# disclosed in the dossier (a kick-cadence run; no frame-cost page impact)
KNOWN_DRIFT = {"20261006-0220-redteam-fermi2-v2-b7a4": "gold"}
MY_RUN = "20261012-1621-q-wiki-frame-cost-ae6a"
# grades as given in the cluster prompt; regenerated from branches below
GIVEN_GRADES = {
    "20261006-0220-redteam-fermi2-v2-b7a4": "silver",
    "20261006-1135-autoresearch-eb29": "silver",
    "20261006-1354-constraint-df79": "silver",
    "20261007-0528-constraint-6094": "silver",
    "20261007-0800-constraint-7a39": "silver",
    "20261007-0842-constraint-0411": "silver",
    "20261007-1234-system-2517": "gold",
    "20261007-1550-constraint-578e": "silver",
    "20261007-1646-autoresearch-a191": "silver",
    "20261007-1801-constraint-3126": "silver",
    "20261007-1801-second-20261007-1646-autoresearch-a191-18df": "silver",
    "20261007-1843-constraint-2658": "silver",
    "20261007-1843-fermi-1feb": "silver",
    "20261007-2155-constraint-b952": "silver",
    "20261007-2246-components-4955": "silver",
    "20261007-2344-quant-4211": "silver",
    "20261008-0234-quant-2300": "silver",
    "20261008-0615-taleb-40c0": "gold",
    "20261008-0743-constraint-4588": "silver",
    "20261008-0743-second-20261008-0615-taleb-40c0-a342": "missing",
    "20261008-1058-constraint-caa2": "silver",
    "20261008-1252-quant-291f": "silver",
    "20261008-1719-constraint-1fe2": "silver",
    "20261008-2031-constraint-4b27": "silver",
    "20261009-0709-quant-6766": "silver",
    "20261009-1210-constraint-c10d": "silver",
    "20261009-1210-second-20261009-0621-constraint-51bf-97bc": "gold",
    "20261009-1259-constraint-2666": "gold",
    "20261009-1504-redteam-2320": "silver",
    "20261009-1556-redteam-18fc": "silver",
    "20261009-1556-second-20261009-1504-redteam-2320-56bc": "gold",
    "20261009-1936-constraint-8af7": "silver",
    "20261009-2043-autoresearch-d4f1": "silver",
    "20261009-2043-quant-3cfc": "silver",
    "20261009-2212-constraint-2380": "gold",
    "20261009-2257-constraint-842c": "lead",
    "20261010-0100-constraint-c97d": "silver",
    "20261010-0352-quant-3435": "silver",
    "20261010-0448-second-20261010-0352-taleb-cb7c-c2f8": "gold",
    "20261010-0656-quant-d540": "gold",
    "20261010-0656-spacex-2439": "gold",
    "20261010-0814-constraint-f3f1": "silver",
    "20261010-1029-redteam-435b": "gold",
    "20261010-1152-constraint-c575": "silver",
    "20261010-1302-spacex-6785": "silver",
    "20261010-1407-constraint-775f": "silver",
    "20261010-1544-system-97ce": "silver",
    "20261010-1706-fermi-2914": "silver",
    "20261010-1816-components-6273": "silver",
    "20261010-1920-quant-9464": "silver",
    "20261010-1920-spacex-cb3f": "silver",
    "20261010-1947-autoresearch-2833": "silver",
    "20261010-2141-constraint-ae40": "silver",
    "20261011-0324-constraint-986f": "silver",
    "20261011-0736-components-825f": "silver",
    "20261011-0836-autoresearch-469c": "lead",
    "20261011-1102-quant-ba35": "silver",
    "20261011-1600-constraint-2094": "silver",
    "20261011-1729-components-b063": "gold",
    "20261011-1729-second-20261011-1600-constraint-2094-07b8": "silver",
    "20261011-1814-quant-f8f9": "silver",
    "20261011-1917-second-20261011-1814-taleb-762d-119f": "gold",
    "20261011-2306-system-3367": "silver",
    "20261012-0036-quant-115e": "gold",
    "20261012-0616-system-1537": "silver",
    "20261012-1019-quant-b29b": "gold",
    "20261012-1019-spacex-3463": "silver",
    "20261012-1227-constraint-cf31": "silver",
}


def grade_from_branch(run: str) -> str:
    p = subprocess.run(
        ["git", "show", f"origin/claude/lab-{run}:lab/results/{run}/check.md"],
        capture_output=True, text=True)
    if p.returncode != 0:
        return "missing"
    m = re.search(r"^Grade:\s*(\w+)", p.stdout, re.M)
    return m.group(1).lower() if m else "unreadable"


def main() -> int:
    ids = [l.strip() for l in RUNS.read_text().splitlines() if l.strip()]
    assert len(ids) == 68, f"expected 68 runs, got {len(ids)}"
    classified = [r for ts in TOPICS.values() for r in ts]
    assert sorted(classified) == sorted(ids), "classification is not a partition of the 68"

    fail = []
    print("== grades regenerated from branches vs the cluster list")
    regen = {}
    for r in ids:
        regen[r] = grade_from_branch(r)
        if regen[r] != GIVEN_GRADES[r] and KNOWN_DRIFT.get(r) != regen[r]:
             fail.append(f"grade drift {r}: branch={regen[r]} prompt={GIVEN_GRADES[r]}")
        if KNOWN_DRIFT.get(r) == regen[r]:
            print(f"  disclosed drift {r}: branch says {regen[r]}, "
                  f"cluster list says {GIVEN_GRADES[r]} (kept in dossier)")
    by_g = {}
    for g in regen.values():
        by_g[g] = by_g.get(g, 0) + 1
    print("  tally:", dict(sorted(by_g.items())))
    fc_gold = [r for r in TOPICS["frame-cost"] if regen[r] == "gold"]
    print(f"  frame-cost runs: {len(TOPICS['frame-cost'])} "
          f"({len(fc_gold)} gold); view: {len(TOPICS['view'])}; "
          f"memory-h-live: {len(TOPICS['memory-h-live'])}; "
          f"kick-cadence: {len(TOPICS['kick-cadence'])}")

    page = PAGE.read_text()
    print("== page checks")
    runs_section = page.split("## Runs", 1)[1]
    lines = [l for l in runs_section.splitlines() if l.startswith("- ")]
    print(f"  runs listed: {len(lines)}")
    if len(lines) != len(TOPICS["frame-cost"]):
        fail.append(f"Runs section has {len(lines)} lines, classification says "
                    f"{len(TOPICS['frame-cost'])}")
    for l in lines:
        m = re.match(r"- (\S+) \((\w+)\): (.*)$", l)
        if not m:
            fail.append(f"malformed runs line: {l[:60]}")
            continue
        rid, grade, claim = m.groups()
        if rid not in TOPICS["frame-cost"]:
            fail.append(f"{rid} listed on the page but classified elsewhere")
        if grade != regen.get(rid):
            fail.append(f"{rid} grade on page ({grade}) != branch ({regen.get(rid)})")
        words = len(claim.split())
        if words > 20:
            fail.append(f"{rid} claim is {words} words (> 20)")

    body = page.split("## Runs", 1)[0]
    for rid in set(re.findall(r"20\d{6}-\d{4}-[0-9a-z-]+", body)):
        if rid != MY_RUN and rid not in ids and not any(
                rid.startswith(r + "-") or r.startswith(rid) for r in ids):
            fail.append(f"cited id not in the cluster: {rid}")
    for rid in set(re.findall(r"20\d{6}-\d{4}-[0-9a-z-]+", body)):
        if rid in ids and regen[rid] == "missing" and "(missing)" not in page:
            fail.append(f"{rid} is ungraded but not marked missing on the page")
    for sect in ("## Current best", "## Refuted", "## Open directions",
                 "## Contradictions", "## Runs"):
        if sect not in page:
            fail.append(f"missing section {sect}")
    if f"updated: 20261012-1621-q-wiki-frame-cost-ae6a" not in page:
        fail.append("header updated: is not this run id")
    if "status: open" not in page:
        fail.append("status is not open")

    print("== result:", "FAIL" if fail else "PASS")
    for f in fail:
        print("  !", f)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
