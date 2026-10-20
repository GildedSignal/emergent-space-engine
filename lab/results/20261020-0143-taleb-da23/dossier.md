# Dossier — the stride gate: finality stops publishing past live stride starts

**Claim.** A 3-part gate in `alone_at`/`final_through` (`Config::stride_gate`, off by default)
cuts the allocator's finality-assert fires on the fleet-battle fire protocol from **7/8 draws
(shipped) to 1/10 (gated)** in one hot window, at a present-rate cost of ~15-40%, with the
equality law intact on every clean draw — but **one fire topology survives**, so the gate is a
risk reduction, not a closure: the fix direction is confirmed, the last hole is named.

**Bottleneck.** The allocator-ratchet page's direction 1 (the engine's one reachable crash,
`alloc.rs` "would revise its published tick", exit 101), measured state-decided at certify by
c749 (D > 0 ⟺ fire). Not a 10× compute gain: this is the ruin side (PRINCIPLES #25, Taleb lens
item 3) — the crash deletes the whole process, so no nanosecond elsewhere counts until it is
closed.

**The gate** (all inside the finality coalesce, so before/after share one build):
1. every reach box grown by one stride's light travel, `v·(stride_max+1)·window`: a stride's
   certificate hull (what clashes are decided on, and rollbacks restore to its start) lies
   inside it, so no region turns final through `t` while a neighbour's live-or-next stride
   started below `t`;
2. no region is skipped for `fin ≥ t`: a restored/merged giant carries final parts above its
   `verified` (c749's violated region, every fire) — it now projects its current stride hull;
   its current `rmax` also enters its group radius;
3. every certified truth with `start < t` enters the coalesce as an ids-empty pseudo-member:
   a truth is a committed restore point, and finality had never consulted the truths table.

**Evidence** (this window, Linux x86, load-coupled incidence; commands in `regen.sh`, ~3 min):
- Shipped arm (`gate 0`): 8 draws of `battle s∈{11..31} 2400 32 8192 0.5 24 8704 4.5` →
  **7 fire** (exit 101, FIRE line, PRE D>0 immediately before; e.g. `PRE id=51 s=960 e=976
  D=(32,44,944)` → `FIRE id=52 s0=944 fin_hi=976`), 1 clean (present 2128).
- Gate v1 (parts 1-2): 8 draws → **1 fire** (s19: same D=32 topology; led to part 3).
- Gate v2 (parts 1-3): 10 draws (8 seeds + s19 ×3) → **1 fire** (s19 try 3; try 1-2 same seed
  clean), 9 clean, present 1280-1536, regions collapse 22-25→1, `final lead max` 64-96 (>0,
  P5: no publication livelock), and **every RB line on clean draws at m ≤ 0** (equality law
  holds under the gate; the only m>0 RB is the fire's own).
- Cost: present 1280-1536 vs 1792-2128 shipped-clean (~15-40% down); deadline misses
  914→~1100-1200 (bounded, within the 2× of P2). Rollbacks 2-11 both arms.
- Shipped lib tests pass with the switch in (`cargo test -p emergent-allocator` in regen).

**Predictions** (`predictions.md`, written before the decisive run): P1 fires die — **held
with the named exception** (the gate itself fired once per version, each naming the next
hole: v1's fire exposed the `fin ≥ t` skip — exactly c749's giant signature; v2's survivor is
the remaining open hole). P2 no starvation — held (all clean gate draws complete, present
within 40%, misses < 2×). P3 state law — held on clean draws (A lines only as armed
possibilities, all realized RB m ≤ 0). P4/P5 — P5 held (lead 64-96 > 0); P4 (gas churn
min_region 1) **not flown: out of time** — named next experiment, not a result.

**What would make it wrong.** The surviving fire (s19-class, D=32, a certified truth from 944
against fin_hi 976, box c≈[266,166] s≈[2040,2316]): either the truth-hull radius (`truth.r`
vs the coalesce radius), base staleness across the 8 finalize rounds, or a merge path that
raises `fin_hi` without an `alone_at` decision. Until it is pinned and closed, the gate must
not ship as the fix — it is a 7-8× risk cut on the worst class. Incidence is a wall-clock
race: a quiet machine under-fires the shipped arm (bf83: 0/8 quiet); only the paired
same-window comparison regenerates. Cost of adopting: the switch + 3 gated blocks in two
functions (~30 lines), one extra `truths` scan per finalize pass (the present cost above);
fits the crate's one-build convention (`Config::round2` untouched, default off).

**PRINCIPLES.** #13 "errors never compound / divergence is not a joke": the assert is exactly
an error that cannot be allowed to exist, so it crashes instead — the gate moves the guard
before the publication instead of after. #9: the v1 gate firing killed that configuration
(skip-on-fin), not the method. #12/#27: the ~15-40% present cost is the price of the crash's
absence and must be re-measured on the M1 as the player runs it.

**Lens.** Taleb: ruin first — I bought down the worst tail before any throughput argument,
and the two gate-fires were treated as information, not noise. What the lens missed: the
survivor's mechanism needs a builder's read of the merge/finality code, not more draws; and I
did not fly the churn class (P4), so "the gate does not starve the 01e7 family" is untested —
the starvation warning (e517's cost note) stands.
