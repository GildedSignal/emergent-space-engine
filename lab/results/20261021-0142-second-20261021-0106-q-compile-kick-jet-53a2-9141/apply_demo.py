#!/usr/bin/env python3
"""Adoption through the real tool (2nd author run ...-9141): drives lab/wiki.py's own
`apply()` (no re-implementation) in sandboxes, three scenarios.

  A. CONTROL (unpatched HEAD wiki.py, the exact historical inputs): ours = the 444-line
     page, base = the 1st run's base commit, theirs = the 1st run's compiled 107-line
     page -> must reproduce BYTE-FOR-BYTE the page now on main (the 135-line landing the
     checker measured: 85 raw run lines, 28 duplicate excess).
  B. Same inputs, PATCHED wiki.py (id-aware fold_runs) -> the page the run actually
     wrote lands: 107 lines, 57 run lines, 0 duplicates.
  C. FORWARD (patched wiki.py): ours = main's current page, base = this run's base,
     theirs = this run's corrected page -> lands byte-for-byte; sandbox `index` shows
     kick-jet open, no conflict, no over-budget flag.
Exit 0 iff all three hold.
"""
import os, re, shutil, subprocess, sys, tempfile

MY = "lab/results/20261021-0142-second-20261021-0106-q-compile-kick-jet-53a2-9141"
ORIG = "20261021-0106-q-compile-kick-jet-53a2"
TOPIC = "kick-jet.md"


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout


def census(text):
    ids = re.findall(r"^- (\d{8}-\d{4}-\S+)", text, re.M)
    return len(text.splitlines()), len(ids), len(set(ids)), len(ids) - len(set(ids))


def scenario(label, wiki_py_text, ours_text, base_commit, theirs_text, theirs_run):
    """Run the given lab/wiki.py text's `apply` in a sandbox; return the landed page."""
    sbx = os.path.join(MY, "work", f"sbx-{label}")  # inside the repo: sandboxed git works
    shutil.rmtree(sbx, ignore_errors=True)
    os.makedirs(f"{sbx}/lab/wiki"); os.makedirs(f"{sbx}/results/{theirs_run}/wiki")
    for name in os.listdir("lab/wiki"):
        shutil.copy(f"lab/wiki/{name}", f"{sbx}/lab/wiki/{name}")   # all pages, as on main
    open(f"{sbx}/lab/wiki/{TOPIC}", "w", encoding="utf-8").write(ours_text)  # ...ours swapped in
    open(f"{sbx}/lab/wiki.py", "w", encoding="utf-8").write(wiki_py_text)
    open(f"{sbx}/results/{theirs_run}/DONE", "w").write("Grade: silver\n")
    open(f"{sbx}/results/{theirs_run}/base", "w").write(base_commit + "\n")
    open(f"{sbx}/results/{theirs_run}/wiki/{TOPIC}", "w", encoding="utf-8").write(theirs_text)
    r = subprocess.run([sys.executable, "lab/wiki.py", "apply", "results", base_commit],
                       cwd=sbx, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    landed = open(f"{sbx}/lab/wiki/{TOPIC}", encoding="utf-8").read()
    index = open(f"{sbx}/lab/wiki/index.md", encoding="utf-8").read()
    shutil.rmtree(sbx)
    return landed, index, r.stdout

def fold_check(patched_py):
    """fold_runs on toy inputs: collision -> run's variant; main-only id -> kept."""
    ns = {}
    exec(compile(re.search(r"def fold_runs.*?\n    return out\n", patched_py, re.S).group(0),
                 "<fold>", "exec"), {"re": re}, ns)
    got = ns["fold_runs"](["- run2-2222 (gold): new"], ["- run1-1111 (silver): old", "- run2-2222 (silver): old"])
    return got == ["- run2-2222 (gold): new", "- run1-1111 (silver): old"]


def main():
    ok = True
    head_py = git("show", "HEAD:lab/wiki.py")
    patched_py = open("lab/wiki.py", encoding="utf-8").read()
    # fold_runs semantics, both directions (scenarios B/C exercise only equal id sets):
    # the run's variant wins a collision; a run graded after the proposal (main-only) survives.
    demo = fold_check(patched_py)
    print(f"[fold|unit] run variant wins + main-only kept: {demo}")
    if not demo:
        ok = False; print("[fold] FAIL: append-only semantics broken")
    assert "fold_runs" in patched_py and "fold_runs" not in head_py, "patch not in place?"

    old_base = git("show", f"origin/claude/lab-{ORIG}:lab/results/{ORIG}/base").strip()
    old444 = git("show", f"{old_base}:lab/wiki/{TOPIC}")
    orig107 = git("show", f"origin/claude/lab-{ORIG}:lab/results/{ORIG}/wiki/{TOPIC}")
    main_now = git("show", f"HEAD:lab/wiki/{TOPIC}")
    mine = open(f"{MY}/wiki/{TOPIC}", encoding="utf-8").read()
    my_base = open(f"{MY}/base").read().strip()

    # A. control: HEAD's own apply() on the historical inputs
    landed, _, out = scenario("A", head_py, old444, old_base, orig107, ORIG)
    lines, raw, dist, dup = census(landed)
    same = landed == main_now
    print(f"[A|HEAD apply, historical] lands {lines} lines, {raw} raw run lines, "
          f"{dist} distinct, {dup} duplicate excess; byte-identical to main's page: {same}")
    if not same:
        ok = False
        print("[A] FAIL: control does not reproduce main's landed page")
        open(f"{MY}/work/A-landed.md", "w", encoding="utf-8").write(landed)
        open(f"{MY}/work/A-main.md", "w", encoding="utf-8").write(main_now)

    # B. patched apply, same historical inputs
    landed, _, _ = scenario("B", patched_py, old444, old_base, orig107, ORIG)
    lines, raw, dist, dup = census(landed)
    same = landed == orig107
    print(f"[B|patched apply, historical] lands {lines} lines, {raw} raw run lines, "
          f"{dist} distinct, {dup} duplicate excess; byte-identical to the run's page: {same}")
    if not (lines == 107 and raw == 57 and dup == 0):
        ok = False; print("[B] FAIL: budget/id invariants broken")
    if not same:
        print("[B] NOTE: landed text differs from the run's page (see work/B-landed.md)")
        open(f"{MY}/work/B-landed.md", "w", encoding="utf-8").write(landed)

    # C. forward: patched apply lands THIS run's corrected page on main's current one
    landed, index, _ = scenario("C", patched_py, main_now, my_base, mine,
                                "20261021-0142-second-20261021-0106-q-compile-kick-jet-53a2-9141")
    lines, raw, dist, dup = census(landed)
    same = landed == mine
    row = next(l for l in index.splitlines() if TOPIC[:-3] in l)
    clean = "conflict" not in row and "over budget" not in row
    print(f"[C|patched apply, forward] lands {lines} lines, {raw} raw run lines, "
          f"{dist} distinct, {dup} duplicate excess; byte-identical to proposal: {same}")
    print(f"[C|sandbox index row] {row}")
    print(f"[C|index] open, no conflict, no over-budget flag: {clean}")
    if not (same and dup == 0 and dist == 57 and clean):
        ok = False; print("[C] FAIL")
        open(f"{MY}/work/C-landed.md", "w", encoding="utf-8").write(landed)

    print("VERDICT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
