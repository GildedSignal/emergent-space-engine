#!/usr/bin/env python3
"""4a71: rebuild wiki/nladder.md's body from the standing (conflicted) page. Provenance only —
the checked-in nladder.md was built by exactly these line ranges, which resolve BOTH standing
conflicts additively (all three prior NEW entries kept, in run order). Line numbers refer to
lab/wiki/nladder.md AS THIS RUN FOUND IT (718 lines, two conflict blocks). The run's own
extensions (Refuted / Open directions / Runs) were then applied on top by hand.
"""
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
W = "lab/wiki/nladder.md"
OUT = HERE / "nladder.body.md"

cmds = [
    f"sed -n '1,4p' {W}",
    "echo 'updated: 20261019-0141-inversion-4a71'",
    f"sed -n '8,9p' {W}",
    "echo ''",
    "echo '## Current best'",
    "echo ''",
    f"cat '{HERE}/entry.md'",               # my NEW entry
    f"sed -n '497,543p' {W}",               # d839's NEW (newest of the three)
    "echo ''",
    "echo '*[Prior best retained below.]*'",
    "echo ''",
    f"sed -n '11,48p' {W}",                 # dcf1's NEW (its dangling 2403 opener at 49 dropped:
                                            # 99da retells 2403 corrected, completing at line 88)
    f"sed -n '54,86p' {W}",                 # 99da's NEW (minus its updated/blank/title, 51-53)
    f"sed -n '88,489p' {W}",                # the shared standing record (2403 completion onwards)
    f"sed -n '546,718p' {W}",               # Refuted / Open directions / Runs
]
subprocess.run(["sh", "-c", "cd '%s' && { %s ; } > '%s'" % (ROOT, "; ".join(cmds), OUT)], check=True)
print(f"wrote {OUT}: {OUT.stat().st_size} bytes")
