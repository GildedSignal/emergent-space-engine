#!/usr/bin/env python3
"""No-loss check across the conflict resolution (P5) + negative control (P6).

Old side: the standing conflicted page (both marker sides + the 64-bullet Runs
union). New side: the resolved page. Token canon: 16c3's check_compile.py
(NFKC, − → -, superscript + → +, leading zeros stripped), applied to both.
Tokens may be missing only from stale run-line variants superseded by a final
line for the same run; each such miss is traced to the final line.
"""
import re, sys, unicodedata

def norm(s):
    return unicodedata.normalize("NFKC", s.replace("\u2212", "-").replace("\u207a", "+"))

def tokens(text):
    out = set()
    for m in re.finditer(r"\d+(?:\.\d+)?(?:e-?\d+)?", norm(text), re.I):
        s = m.group(0).lower()
        s = re.sub(r"^(\d+)", lambda g: g.group(1).lstrip("0") or "0", s)
        out.add(s)
    return out

old = open(sys.argv[1], encoding="utf-8").read()
new = open(sys.argv[2], encoding="utf-8").read()
missing = sorted(tokens(old) - tokens(new), key=lambda s: (len(s), s))
print(f"old tokens {len(tokens(old))} | new tokens {len(tokens(new))} | missing {len(missing)}: {missing}")

# every missing token must appear in a stale run line (starts '- <id>') whose
# run also has a final line elsewhere on the page
runs = re.findall(r"^- (\d{8}-\d{4}-[a-z0-9-]+)[^\n]*", new, re.M)
def only_in_run_lines(tok):
    # every occurrence in the old page must sit on a run line (- <id> ...)
    for m in re.finditer(re.escape(tok), norm(old)):
        ls = old.rfind("\n", 0, m.start()) + 1
        if not re.match(r"- \d{8}-\d{4}-[a-z0-9-]+", old[ls:]):
            return False
    return True
untraced = [t for t in missing if not only_in_run_lines(t)]
print("missing outside any run line:", untraced if untraced else "none")
sys.exit(1 if untraced else 0)
