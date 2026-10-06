Working...
Check complete. `check.md` written to the run folder; nothing else touched.

**Grade: silver.**

What I did and found:

**Reproduction — exact.** Every table number recomputed from `data/*.json` matches (all six rows, including each µs/item derived from `cost_ns`/`items`). Fresh runs: m400 bench digest `24208b…` and cut_tick **identical**; kick-bench digest `a6792e…` **identical** with memo hit-rates exactly 0%/95.47%/1125 shapes. Timing numbers land within shared-box noise (overflow 301 vs 389; player 2336 µs vs 3405 — same 28× dominance over ships). Source claims verified in code: the O(N) scan at `encounter.rs:53`, the forced fleet pull at `universe.rs:564–586`, the horizon clamp at `819–830`, the 400-member clamp, ships-only wave path.

**Held-out breach — the record's flaw.** File times show `predictions.md` (13:59:31) was written after the m200 (13:58:30) and m400 (13:59:00) runs finished, contradicting its own header and the dossier. Predictions 1–3 were not held out; only 4–5 were. The measurements are genuine; the hold-out claim is not.

**Attacks (all survived).** m100 confirms the transition band (worst-1% rtf 81.4, between 9.9 and 0.03); threads-4 independently reproduces the worsening (301→507, author 389→505) with the player item still serial; seed 2 same regime (overflow 313, player 23× ship). Bonus finding: paced/unpaced/t4 share one digest at one cut — schedule independence stronger than the author claimed, sitting unclaimed in their own data.

**Why silver, not gold:** builds nothing (no gate moved, no 10×), and the central predictions weren't actually held out. The one experiment: swap the O(N) player scan for constant work and re-measure the m400 tail — predictions written before the run this time.
