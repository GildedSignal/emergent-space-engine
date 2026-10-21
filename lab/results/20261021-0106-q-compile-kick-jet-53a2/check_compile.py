#!/usr/bin/env python3
"""Faithfulness verifier for the compiled kick-jet page (run 20261021-0106-q-compile-kick-jet-53a2).

Checks, against lab/wiki.py's own rules:
  1. budget: `## Current best` non-blank lines <= 15, total page lines <= 300, for old and new;
  2. run ids: set equality old->new (nothing lost, nothing invented), no id twice in new `## Runs`;
  3. numbers: every number token of the old `## Current best` + `## Refuted` is either in the
     new page verbatim, or its old line cites a run id that the new page carries ("behind a
     cited run"). Prints the tally and any LOST tokens.
Exit code 0 iff: new page under budget, run sets equal, no dup ids, zero LOST tokens.
"""
import re, sys

OLD = "lab/wiki/kick-jet.md"
NEW = "lab/results/20261021-0106-q-compile-kick-jet-53a2/wiki/kick-jet.md"
FULL_ID = re.compile(r"\d{8}-\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*")
RUN_LINE = re.compile(r"^- (\d{8}-\d{4}-\S+) \(([^)]*)\):", re.M)
NUM = re.compile(r"\d[\d.,:]*\d|\d")
HEX4 = re.compile(r"(?<![0-9a-z])([0-9a-f]{4})(?![0-9a-z])")

def sections(text):
    """Ordered dict of section heading -> content (heading excluded)."""
    parts = re.split(r"^## (.+?)\s*$", text, flags=re.M)
    head, out = parts[0], {}
    for i in range(1, len(parts), 2):
        out[parts[i]] = parts[i + 1]
    return head, out

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

def bullets(sec):
    """Logical bullets: a bullet line plus its continuation lines."""
    out, cur = [], None
    for line in sec.splitlines():
        if line.startswith("- "):
            if cur: out.append(cur)
            cur = line
        elif cur is not None:
            cur += " " + line.strip()
    if cur: out.append(cur)
    return out

def ids_in(text):
    return set(FULL_ID.findall(text))

def main():
    old = open(OLD, encoding="utf-8").read()
    new = open(NEW, encoding="utf-8").read()
    ok = True

    # -- 1. budget ------------------------------------------------------------
    for name, text in (("old", old), ("new", new)):
        total, best = budget(text)
        print(f"[budget] {name}: {total} lines total, current best {best} non-blank lines")
    nt, nb = budget(new)
    if nb > 15 or nt > 300:
        print(f"[budget] FAIL: new page over budget"); ok = False

    # header sanity + section order (README schema)
    head = old and new
    keys = [l.split(":")[0] for l in new.splitlines()[:6] if l.strip() and ":" in l]
    assert keys[:1] == ["topic"], keys
    _, so = sections(old); _, sn = sections(new)
    want = ["Current best", "Refuted", "Open directions", "Contradictions", "Runs"]
    print(f"[schema] new sections: {list(sn)} (old: {list(so)})")
    if list(sn) != want:
        print("[schema] FAIL: section order"); ok = False
    nopen = len([l for l in sn["Open directions"].splitlines() if l.strip()])
    print(f"[schema] open directions: {nopen} entries (limit 8)")
    if nopen > 8:
        print("[schema] FAIL: too many open directions"); ok = False

    # -- 2. run ids -----------------------------------------------------------
    old_ids = [m.group(1) for m in RUN_LINE.finditer(old)]
    new_ids = [m.group(1) for m in RUN_LINE.finditer(new)]
    from collections import Counter
    print(f"[runs] old raw run lines: {len(old_ids)}, distinct {len(set(old_ids))}; "
          f"dupes removed {len(old_ids) - len(set(old_ids))}")
    print(f"[runs] new run lines: {len(new_ids)}, distinct {len(set(new_ids))}")
    dups = [i for i, c in Counter(new_ids).items() if c > 1]
    lost = set(old_ids) - set(new_ids)
    invented = set(new_ids) - set(old_ids)
    if dups: print(f"[runs] FAIL: duplicated ids in new page: {dups}"); ok = False
    if lost: print(f"[runs] FAIL: run ids lost: {sorted(lost)}"); ok = False
    if invented: print(f"[runs] FAIL: run ids invented: {sorted(invented)}"); ok = False
    if not (dups or lost or invented):
        print(f"[runs] OK: id sets equal ({len(set(old_ids))} = {len(set(new_ids))}), none duplicated")
    # grades recorded on kept lines must not regress a recorded final grade
    def grade_of(line_id, text):
        m = re.search(r"^- " + re.escape(line_id) + r" \(([^)]*)\):", text, re.M)
        return m.group(1) if m else ""
    for rid in set(old_ids) & set(new_ids):
        g_old, g_new = grade_of(rid, old), grade_of(rid, new)
        if "silver" in g_old and "silver" not in g_new and "gold" not in g_new:
            print(f"[runs] WARN: {rid} old grade '{g_old}' -> new '{g_new}'"); ok = False

    # -- 3. number faithfulness ----------------------------------------------
    _, os_ = sections(old)
    target_bullets = bullets(os_.get("Current best", "")) + bullets(os_.get("Refuted", ""))
    new_all_ids = ids_in(new)
    in_page = behind = lost_nums = 0
    lost_list = []
    for b in target_bullets:
        cited = set(FULL_ID.findall(b)) | {h for h in HEX4.findall(b) if any(c.isdigit() for c in h)}
        cited_new = {c for c in cited if c in new}
        for tok in set(NUM.findall(b)):
            tok = tok.strip(".,:")
            if not tok or tok.isdigit() and int(tok) < 10:
                continue  # single digits carry no claim
            if tok in new:
                in_page += 1
            elif cited_new:
                behind += 1
            else:
                lost_nums += 1
                lost_list.append((tok, b[:90]))
    total = in_page + behind + lost_nums
    print(f"[numbers] tokens swept from old Current best + Refuted: {total}")
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
