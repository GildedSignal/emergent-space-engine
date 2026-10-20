Working...
Check complete. Diff confirms exactly the intended corrections; the Refuted section repair restored the original byte-for-byte.

## Verdict: `Grade: lead` (written to `check.md`)

**Reproduced.** regen.sh exit 0 in the clean tree: tests 14/0, chase fire caught (try 3), arm table matches (arm1 2/3 fires, arm2 1/3, arm3 0/3 · 42 DEFERs · merges 0 · present 538), gas 1024 identical across arms, 5/5 quotes byte-identical on a fresh 4,590-highlight fetch. predictions.md (04:49:13) precedes every decisive draw (04:53+). Author's kept matrix matches the dossier (3/10, 0/10, 0/10).

**Why lead — the headline is contradicted by the author's own log.** The dossier pins the survivor on the regroup mint; that rests on **one** fire (`why=["merge@864"]`). The other three author fires and all four checker-window fires show `why=[""]`, single donor part, each immediately preceded by `RB lid=<donor> s0=<mint tick>` restoring that donor at exactly the fired region's `verified`. Proof these are the **rollback restore's** `make_region` (alloc.rs:1480 — the one mint site the instrument doesn't label): the `merge` note at regroup is unconditional for fresh ids and can't have drained (newest entry, fire follows within lines); single-member regroups reuse ids; `make_region(Some(fin))` has exactly two callers. 7/8 pooled fires are restore-mints; a regroup-only cap would not close the class.

**Further adversarial findings.**
- "0 DECIDED, every arm" is false: the author's own `s19.a0` (shipped) holds 91 (self-truth only); my `quiet` run shows 514 (instrument valid).
- Outside the author's range (galaxy 12288/36, gate 1): 14 clean draws — but **8 DECIDED/draw, two publishing past foreign truths starting 512** — the author's predicted hole (d) is live at the next scale, so arm 2 is inert only at 8704, not by construction.
- DEFER regenerates as a flat 42/draw (13/13), not "42–168"; arm 3's 0 fires is doubly confounded (it deferred all regroups, collapsed present to 538, and never touched the actual fatal mints).

**What stands:** the fatal `fin_hi` is never a finality decision — it's inherited publication at an unchecked mint; the NED/END inversion (arm 2 ≈ arm 1 under load) is reproduced; the starvation price is real. The corrected pin and the next experiment (instrument + cap **both** mint sites, inherit live truths, re-fly the paired interleave at 8704 and 12288) are recorded in the corrected wiki page — NEW block, open direction 1, and the Runs line, all marked checker-corrected.
