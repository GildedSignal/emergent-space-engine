#!/usr/bin/env python3
"""verify.py — the compile check for the `promotion` wiki page.

Compares the compiled page (this run's wiki/promotion.md) against the old page
(lab/wiki/promotion.md) under the wiki's own rules (lab/wiki/README.md, and
lab/wiki.py's budget rule at line 88):

  1. budgets   — Current best <= 15 non-blank lines, page <= 300 lines total;
  2. structure — the five sections in README order, header keys intact;
  3. runs      — every distinct run id of the old ## Runs appears in the new
                 ## Runs (dup lines collapse; one line per run);
  4. numbers   — census: every DISTINCTIVE numeric token of the old page
                 (>= 3 chars, so not bare 0-99) is either verbatim in the new
                 page, or sits in a block whose run id (4-hex) the new page
                 cites — "no supported number lost".

Exit 0 = all pass. Prints the numbers the dossier quotes.
"""
import re
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
OLD = RUN.parents[1] / "wiki" / "promotion.md"
NEW = RUN / "wiki" / "promotion.md"

SECTIONS = ["## Current best", "## Refuted", "## Open directions",
            "## Contradictions", "## Runs"]

# 4-hex run keys that mean "a run" anywhere on the page (ids end in them, or
# they are the page's shorthand citations like (4f59), [396d, ...]).
HEX = r"[0-9a-f]{4}"


def sections(text):
    """{name: [lines]} for the five body sections."""
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^## ", line)
        if m:
            cur = line.strip()
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return out


def budget(lines_best, text):
    best = [l for l in lines_best if l.strip()]
    return len(best), len(text.splitlines())


def main():
    old, new = OLD.read_text(), NEW.read_text()
    so, sn = sections(old), sections(new)
    ok = True

    # 1. budgets (wiki.py line 88 rule)
    b_old = budget(so["## Current best"], old)
    b_new = budget(sn["## Current best"], new)
    print(f"old page: {b_old[1]} lines total, current best {b_old[0]} non-blank")
    print(f"new page: {b_new[1]} lines total, current best {b_new[0]} non-blank")
    for name, val, lim in (("current best lines", b_new[0], 15),
                           ("total lines", b_new[1], 300)):
        stat = "PASS" if val <= lim else "FAIL"
        ok &= val <= lim
        print(f"budget {name}: {val} <= {lim}  {stat}")

    # 2. structure
    order = [l for l in new.splitlines() if l.startswith("## ")]
    head = new.split("\n\n", 1)[0]
    keys = [k for k in ("topic:", "status:", "updated:") if k in head]
    stat = "PASS" if order == SECTIONS and len(keys) == 3 else "FAIL"
    ok &= stat == "PASS"
    print(f"structure: sections in order={order == SECTIONS}, header keys={keys}  {stat}")

    # 3. runs
    def run_ids(runs_lines):
        ids = []
        for l in runs_lines:
            for m in re.finditer(r"20\d{6}-\d{4}-[a-z]+(?:-[a-z0-9]+)*", l):
                ids.append(m.group(0))
        return ids

    old_ids, new_ids = run_ids(so["## Runs"]), run_ids(sn["## Runs"])
    old_lines = [l for l in so["## Runs"] if l.strip().startswith("-")]
    new_lines = [l for l in sn["## Runs"] if l.strip().startswith("-")]
    missing = [i for i in set(old_ids) if i not in set(new_ids)]
    stat = "PASS" if not missing else "FAIL"
    ok &= not missing
    print(f"runs: old {len(old_lines)} lines / {len(set(old_ids))} distinct ids "
          f"-> new {len(new_lines)} lines / {len(set(new_ids))} distinct; "
          f"missing={missing}  {stat}")

    # 4. number census
    known = set(re.findall(rf"(?<![\w.-])({HEX})(?![\w.-])",
                           old)) & set(re.findall(HEX, old))
    new_hex = set(re.findall(rf"(?<![\w.-])({HEX})(?![\w.-])", new))
    tok_re = re.compile(r"\d+(?:,\d{3})+(?:\.\d+)?|\d+\.\d+(?:e-?\d+)?|"
                        r"\d+e-?\d+|\d*[⁰¹²³⁴⁵⁶⁷⁸⁻]+\d*|\d{3,}|\d+")
    block_re = re.compile(r"(\d+(?:,\d{3})*(?:\.\d+)?(?:e-?\d+)?|\d[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)")

    def paras(text):
        return [p for p in re.split(r"\n\s*\n", text) if p.strip()]

    hits = {"verbatim": [], "run": [], "lost": []}
    body = "\n\n".join("\n".join(so[s]) for s in SECTIONS if s in so)
    for p in paras(body):
        pids = set(re.findall(rf"(?<![\w.-])({HEX})(?![\w.-])", p)) & known
        for m in block_re.finditer(p):
            t = m.group(1)
            if len(t.strip("⁰¹²³⁴⁵⁶⁷⁸⁹⁻")) < 3 and not t.startswith("0."):
                continue  # trivial token (bare 0-99 / single superscript)
            if t in new:
                hits["verbatim"].append(t)
            elif pids & new_hex:
                hits["run"].append((t, sorted(pids & new_hex)))
            else:
                hits["lost"].append((t, p[:70]))
    n_v, n_r, n_l = (len(hits["verbatim"]), len(hits["run"]), len(hits["lost"]))
    tot = n_v + n_r + n_l
    stat = "PASS" if n_l == 0 else "FAIL"
    ok &= n_l == 0
    print(f"numbers: {tot} distinctive tokens -> {n_v} verbatim "
          f"({100*n_v/tot:.0f}%), {n_r} behind a cited run, {n_l} LOST  {stat}")
    for t, p in hits["lost"][:20]:
        print(f"  LOST {t!r} in: {p}…")
    if n_l == 0:
        print("sample of tokens held only behind their run (first 12):")
        for t, ids in hits["run"][:12]:
            print(f"  {t!r} -> {ids}")

    # 5. section census (the dossier's counts) + headline numbers
    for s in SECTIONS[1:]:
        body = "\n".join(sn[s])
        nb = len([l for l in body.splitlines() if l.strip()])
        bl = len([l for l in body.splitlines()
                  if l.strip().startswith(("-", "1.", "2.", "3.", "4.", "5.",
                                           "6.", "7.", "8."))])
        print(f"section {s[3:]}: {nb} non-blank lines ({bl} entries)")
    heads = ["21–24×", "0.11%", "167–214 ns", "91.7–99.7%", "~3×10³×"]
    print("headline numbers verbatim:",
          ", ".join(f"{h}={'Y' if h in new else 'N'}" for h in heads))

    print("VERDICT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
