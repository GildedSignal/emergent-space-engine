import re, io, sys

src = open("lab/wiki/nladder.md").read().splitlines(keepends=True)
out = []
i = 0
n = len(src)

def mk(l, p): return l.rstrip("\n") == p

# --- conflict 1: header (updated:) ---
# <<<<<<< main / updated: bf21 / updated: 6138 / ======= / updated: second... / >>>>>>> ...
assert mk(src[4], "<<<<<<< main"), src[4]
assert mk(src[7], "======="), src[7]
assert src[9].startswith(">>>>>>> "), src[8]
out.append("updated: 20261014-2012-components-38bf\n")
i = 10

skip_conflict = False
while i < n:
    l = src[i]
    if mk(l, "<<<<<<< main"):
        # peek: nested open (16,17) -> drop both markers, keep content; empty inner pair (89,90) -> drop both
        if i + 1 < n and mk(src[i+1], "<<<<<<< main"):
            i += 2; continue
        if i + 1 < n and src[i+1].startswith(">>>>>>> "):
            i += 2; continue
        # full conflict open (open-directions): drop marker, keep ours until =======
        i += 1; continue
    if mk(l, "======="):
        # separator inside a conflict: drop marker, keep both sides
        i += 1; continue
    if l.startswith(">>>>>>> "):
        i += 1; continue
    # fix the glued direction line
    if "open.0. **The break-#2 build" in l:
        l = l.replace("stays unnamed and open.0. **The break-#2 build", "stays unnamed and open.\n1. **The break-#2 build")
    out.append(l)
    i += 1

txt = "".join(out)
# renumber the open-directions block after ours' item 0 got a neighbour (ours had 0..9 with a glued 0)
# drop the truncated duplicate Runs lines from theirs' tail
dupes = [
 "- 20261014-1631-taleb-6138 (silver): the wave's ruin basin measured — 315/1,213 ms single frames at\n",
 "- 20261014-1631-library-7f99 (gold): the deletion program's method — 26 kills, the 10% add-back\n",
 "- 20261014-1511-components-a2c1 (silver): break 3's scan half decomposed — the cap's monotone walk\n",
 "- 20261014-1221-components-0e37 (silver): break 2's lever — the compiled orbit is write-only memory,\n",
 "- 20261014-0450-scout-b29a (silver): the smallest promotion is no promotion.\n",
 "- 20261014-0059-fermi-effb (silver): the 10⁹ ledger composed; the cadence law code-verified.\n",
 "- 20261014-0000-fermi-3071 (silver): rule 2 dead by decomposition; the tail manufactured.\n",
]
for d in dupes:
    txt = txt.replace(d, "")
# complete the truncated 4487 Runs line
txt = txt.replace(
 "- 20261014-1719-second-20261014-1631-taleb-6138-4487 (awaiting grade): the checker's named gold\n",
 "- 20261014-1719-second-20261014-1631-taleb-6138-4487 (awaiting grade): the wave's freeze deleted — pull held at 64, a budgeted drain, Waiting scans; 315→37.7 ms at 10⁵, 1,213→90.3 at 2×10⁵, 1,280→123.8 at 3×10⁵; bit-exact at every canonical cut past the drain; the mid-drain cut and the belt digest's wall-schedule instability named.\n",
)

mine_cb = """**The input seam inside a wave is measured and bounded: with the pull capped, a player decision
mid-wave costs O(1) — 0.168 ms once, ≤ 0.229 ms at 60 Hz through the whole wave — and a no-op
decision moves no kick but can move the log (20261014-2012-components-38bf).** On shipped main plus
this run's re-derivation of bf21's cap (`ES_PULL_CAP`, default-unset; bench `wave_input`), the wave
scene (2×10⁵, seed 1, L8 burn, rtf 100, 12 ms, cut 16,000 game-s settled): uncapped worst frame
1,486.9 ms / 9 over; capped 12.487 ms with the digest bit-identical (`c2b834bb…`, kicks 225,949
equal — bf21's certificate reproduced independently); then one no-op decision at the wave's p50
costs 0.168 ms (≤ 2 events), and 657 of them (every frame of p01–p99, an adversarial bound: the
shipped page calls `input` on key change only, `session.rs:118`) cost ≤ 0.229 ms each — max frame
12.5 ms, 1 over, lag +0.21 game-s. The checker-2-bf21 exposure (`input` resolving the player's
items over an overdue backlog outside the queue) is real as a mechanism and **bounded by the same
cap**: O(1), not O(backlog); the input path needs no deferral machinery. Margin: kicks bit-equal
everywhere, but the 657 no-op decisions add exactly one encounter to the log (1,625 vs 1,624: the
decision's requeue carries scans at ticks the scheduled items never scan) — "same keys" is not "no
event". Unmeasured: a key-**changing** decision mid-wave (a turn re-plans the player), the player
inside the belt band, 4×10⁵, a busy box (4487's 1-event second seam is load-conditional; it did not
appear here — the worst frames are the budgeted drain itself, and P1 vs P2 digests equal under
settle-at-cut on one pair, which does not retire 4487's instability finding).

"""
txt = txt.replace("## Current best\n\n", "## Current best\n\n" + mine_cb, 1)

mine_ref = """- "A player decision inside a same-doll wave is an unbudgeted backlog drain" (the checker-2-bf21
  exposure, read as a cost): the mechanism is real (`input` resolves outside the budget) but its cost
  is the capped pull's constant — ≤ 0.229 ms a call at 2×10⁵ mid-wave, every frame through the wave,
  max frame 12.5 ms; what a no-op decision can still move is the log, not the kicks (+1 encounter per
  657 decisions) (20261014-2012-components-38bf).
"""
# insert into Refuted: after the section's first existing entry block (before the effb cadence refutation at the tail)
anchor = '- "effb\'s cadence law `rate = 2⁷/P'
txt = txt.replace(anchor, mine_ref + anchor, 1)

mine_dir = """0. **The key-changing decision mid-wave** (38bf's untested arm): a turn under burn re-plans the
   player (the no-op arm never re-derived the plan); one flight with `word(5,8)` at the wave's p50
   against the no-op control, judged on the frame profile and the counters. With it, the wave seam's
   player-facing story is closed and the cap can be adopted without an input caveat.
"""
txt = txt.replace("## Open directions\n\n", "## Open directions\n\n" + mine_dir, 1)

mine_run = "- 20261014-2012-components-38bf (awaiting grade): the input seam bounded — 0.17–0.23 ms a decision mid-wave under the cap, monsters 1,487→12.5 ms, digest bit-identical, +1 encounter per 657 no-op decisions.\n"
txt = txt.rstrip("\n") + "\n" + mine_run

open("lab/results/20261014-2012-components-38bf/wiki/nladder.md", "w").write(txt)
print("markers left:", txt.count("<<<<<<<"), txt.count(">>>>>>>"), "=======", txt.count("\n======="))
