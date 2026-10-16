#!/usr/bin/env python3
"""H6: adversarial defuse shapes, crafted before running (see predictions.md).
Calls defuse() from the v2 module (necessarily), but every assertion goes through
the independent instrument (inst.py's regexes), never wiki.py's own marked().
Usage: probes.py <v2-wiki.py>
"""
import importlib.util as u
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import inst  # the independent instrument

spec = u.spec_from_file_location("wv2", sys.argv[1])
w = u.module_from_spec(spec)
spec.loader.exec_module(w)

CASES = {
    "well-formed depth-1": """text
<<<<<<< main
ours line
=======
theirs line
>>>>>>> run1
tail""",
    "opener inside ours side (interleaved nesting)": """text
<<<<<<< main
outer ours
<<<<<<< run1
inner ours
=======
inner theirs
>>>>>>> run1
outer ours 2
=======
outer theirs
>>>>>>> run2
tail""",
    "orphan separator then orphan closer (empty stack)": """text
=======
still text
>>>>>>> gone
more""",
    "well-formed then orphan closer (empty stack)": """text
<<<<<<< main
a
=======
b
>>>>>>> run1
tail
>>>>>>> ghost""",
    "truncated at end of page": """text
<<<<<<< main
ours only
=======
theirs only""",
    "heading resync (never swallows a section)": """## Current best
<<<<<<< main
standing
=======
new
## Runs
- 20261016-0000-a (gold): first""",
    "double separator (orphan mid)": """<<<<<<< main
a
=======
b
=======
c
>>>>>>> run1""",
    "empty theirs": """x
<<<<<<< main
a
=======
>>>>>>> run1
y""",
}

fails = 0
for name, text in CASES.items():
    out = w.defuse(text)
    c = inst.counts(out)
    ok_markers = (c["starts"], c["mids"], c["ends"]) == (0, 0, 0)
    ok_seq, miss = inst.subseq_text(text, out)
    status = "OK" if (ok_markers and ok_seq) else "FAIL"
    print(f"  {name}: markers=({c['starts']},{c['mids']},{c['ends']}) content={ok_seq} -> {status}")
    if status == "FAIL":
        fails += 1
        print("    output:")
        for l in out.splitlines():
            print(f"      {l!r}")
        if miss is not None:
            print(f"    first missing content line: {miss!r}")
print("ALL_OK" if fails == 0 else f"FAILURES={fails}")
sys.exit(1 if fails else 0)
