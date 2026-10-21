#!/usr/bin/env python3
"""Honest verifier for the compiled kick-jet page (2nd author run 20261021-0142-...-9141).

Fixes the 1st-author instrument the checker broke open (check.md, adversarial 1):
the sweep's unit is now EVERY non-blank line of the old `## Current best` + `## Refuted`
(prose paragraphs included), not only `- ` bullets — the old page's Current best is
eight `**…` paragraphs and contributed 0 bullets to the original 109-token tally.

Checks, against lab/wiki.py's own rules:
  1. budget: current best <= 15 non-blank lines, page <= 300 lines;
  2. run ids: set equality old->new (nothing lost, nothing invented), none twice;
  3. grades: no `## Runs` token understates the run's branch grade
     (branch = last commit of origin/claude/lab-<id>, wiki.py's own `grade()` source);
  4. numbers: every multi-digit token of the old Current best + Refuted is in the new
     page verbatim, or its old line cites a run the new page carries ("behind a run").
Old page = lab/wiki/kick-jet.md at the 1st run's recorded base commit (its `base` file).
Exit 0 iff: under budget, id sets equal, no dup, no understating grade, zero LOST.
"""
import re, subprocess, sys
from collections import Counter

NEW = "lab/results/20261021-0142-second-20261021-0106-q-compile-kick-jet-53a2-9141/wiki/kick-jet.md"
ORIG_RUN = "20261021-0106-q-compile-kick-jet-53a2"
FULL_ID = re.compile(r"\d{8}-\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*")
RUN_LINE = re.compile(r"^- (\d{8}-\d{4}-\S+) \(([^)]*)\):", re.M)
NUM = re.compile(r"\d[\d.,:]*\d|\d")
HEX4 = re.compile(r"(?<![0-9a-z])([0-9a-f]{4})(?![0-9a-z])")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout


def sections(text):
    parts = re.split(r"^## (.+?)\s*$", text, flags=re.M)
    return parts[0], {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}


def split_runs(text):  # mirror of lab/wiki.py
    m = re.search(r"^## Runs\s*$", text, re.M)
    if not m:
        return text, []
    rest = text[m.end():]
    end = re.search(r"^## ", rest, re.M)
    lines = [l for l in (rest[:end.start()] if end else rest).splitlines() if l.startswith("- ")]
    return text[:m.start()] + (rest[end.start():] if end else ""), lines


def budget(text):  # mirror of lab/wiki.py index()
    best = len([l for l in split_runs(text)[0].split("## Current best", 1)[-1]
                .split("\n## ", 1)[0].splitlines() if l.strip()])
    return len(text.splitlines()), best


def units(sec):
    """THE FIX: every logical line of a section — `**…` paragraphs and `- ` bullets
    alike, each with its continuation lines folded in. The 1st author's `bullets()`
    kept only `- ` lines, so prose paragraphs were never swept."""
    out, cur = [], None
    for line in sec.splitlines():
        if line.strip() and cur is not None and not line.startswith("- "):
            cur += " " + line.strip()
        elif line.strip():
            if cur:
                out.append(cur)
            cur = line
        else:
            if cur:
                out.append(cur)
            cur = None
    if cur:
        out.append(cur)
    return out


def branch_grade(rid):
    m = re.search(r"Grade: (\w+)", git("log", "-1", "--format=%s", f"origin/claude/lab-{rid}"))
    return m.group(1) if m else None


def main():
    base = git("show", f"origin/claude/lab-{ORIG_RUN}:lab/results/{ORIG_RUN}/base").strip()
    old = git("show", f"{base}:lab/wiki/kick-jet.md")
    new = open(NEW, encoding="utf-8").read()
    ok = True

    # -- 1. budget ------------------------------------------------------------
    for name, text in ((f"old@{base[:9]}", old), ("new", new)):
        total, best = budget(text)
        print(f"[budget] {name}: {total} lines total, current best {best} non-blank lines")
    nt, nb = budget(new)
    if nb > 15 or nt > 300:
        print("[budget] FAIL: new page over budget"); ok = False

    _, sn = sections(new)
    want = ["Current best", "Refuted", "Open directions", "Contradictions", "Runs"]
    print(f"[schema] new sections: {list(sn)}")
    if list(sn) != want:
        print("[schema] FAIL: section order"); ok = False

    # -- 2. run ids -----------------------------------------------------------
    old_ids = [m.group(1) for m in RUN_LINE.finditer(old)]
    new_ids = [m.group(1) for m in RUN_LINE.finditer(new)]
    print(f"[runs] old raw run lines: {len(old_ids)}, distinct {len(set(old_ids))}; "
          f"dupes removed {len(old_ids) - len(set(old_ids))}")
    print(f"[runs] new run lines: {len(new_ids)}, distinct {len(set(new_ids))}")
    dups = [i for i, c in Counter(new_ids).items() if c > 1]
    lost, invented = set(old_ids) - set(new_ids), set(new_ids) - set(old_ids)
    if dups:
        print(f"[runs] FAIL: duplicated ids in new page: {dups}"); ok = False
    if lost:
        print(f"[runs] FAIL: run ids lost: {sorted(lost)}"); ok = False
    if invented:
        print(f"[runs] FAIL: run ids invented: {sorted(invented)}"); ok = False
    if not (dups or lost or invented):
        print(f"[runs] OK: id sets equal ({len(set(old_ids))} = {len(set(new_ids))}), none duplicated")

    # -- 3. grades vs branches (the named refresh, verified) -------------------
    stale = []
    for m in RUN_LINE.finditer(new):
        rid, tok = m.group(1), m.group(2)
        g = branch_grade(rid)
        if g == "gold" and "gold" not in tok:
            stale.append((rid, tok, g))
        elif g == "silver" and "gold" not in tok and "silver" not in tok:
            stale.append((rid, tok, g))
    n_branch = sum(1 for m in RUN_LINE.finditer(new) if branch_grade(m.group(1)))
    print(f"[grades] run lines with a local branch: {n_branch}/{len(new_ids)}")
    if stale:
        for rid, tok, g in stale:
            print(f"[grades] FAIL: {rid} page '({tok})' understates branch {g}")
        ok = False
    else:
        print("[grades] OK: no token understates its branch grade")

    # -- 4. number faithfulness, honest unit of sweep ---------------------------
    _, os_ = sections(old)
    target = units(os_.get("Current best", "")) + units(os_.get("Refuted", ""))
    in_page = behind = lost_nums = 0
    lost_list = []
    for u in target:
        cited = set(FULL_ID.findall(u)) | {h for h in HEX4.findall(u) if any(c.isdigit() for c in h)}
        cited_new = {c for c in cited if c in new}
        for tok in set(NUM.findall(u)):
            tok = tok.strip(".,:")
            if not tok or (tok.isdigit() and int(tok) < 10):
                continue  # single digits carry no claim
            if tok in new:
                in_page += 1
            elif cited_new:
                behind += 1
            else:
                lost_nums += 1
                lost_list.append((tok, u[:90]))
    total = in_page + behind + lost_nums
    print(f"[numbers] units swept (paragraphs + bullets) from old Current best + Refuted: {len(target)}")
    print(f"[numbers] tokens swept: {total}")
    print(f"[numbers] in new page verbatim: {in_page} ({100*in_page//max(total,1)}%), "
          f"behind a cited run: {behind} ({100*behind//max(total,1)}%), LOST: {lost_nums}")
    for tok, ctx in lost_list:
        print(f"[numbers] LOST '{tok}' in: {ctx}")
    if lost_nums:
        ok = False

    print("VERDICT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
