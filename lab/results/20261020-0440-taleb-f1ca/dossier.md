# Dossier — v4: the disarm channel built as an exactly-safe publish floor; fires 3/8→0/8, quiet present at 71-94% of shipped, and the remaining starvation is min-coupled to the deepest live truth

**Claim.** 541d's named next experiment is built and flown: the disarm channel exists as a
five-line change (publish up to `floor0 = min(oldest kept snapshot, oldest kept truth
start)` instead of removing the frontier advance), it is exact (no rollback can restore
below floor0, so publication there cannot fire the assert), and on the battle protocol it
takes shipped's **3 fires in 8 quiet draws to 0 in 8** at **71-94% of shipped present
(median 93% on clean pairs)** — while under 4- and 12-way crush the gate still starves,
and the instrument shows why: the channel is **min-coupled** — one region that stops
accepting pins `frontier = 0` and `floor0 = 0` for everyone (its truths at start 0 stay
live and readable by itself), and shipped "survives" the same laggard only through the
coalesce, which is precisely the publisher that fires.

**Bottleneck.** allocator-ratchet direction 1 (the engine's one reachable crash, exit 101).
Ruin-side: no compute multiple matters until the crash closes (PRINCIPLES #25), and 541d
showed the naive close starves, so the channel was the prerequisite of any close.

**Evidence** (battle protocol: galaxy 8704/24 fleets, rate 2400, margin 0.5, 4.5 s, one
process per draw; harness `crates/allocator/examples/exposure.rs` (541d's, verbatim);
`ESE_V3=1` recovers the v3 arm from the same binary; `work/patch.diff` = 541d's patch +
v4 in `finalize()`. All raw stderr in `work/draws/`; `bash regen.sh` regenerates ~5 min).

- **Fires, quiet paired protocol, 8 seeds × both arms** (`work/draws/quiet_*.err`):
  shipped FIRE 3/8 — s11, s21, s23, exit 101, all with the same signature
  `fin_hi > s0 = front` (id=51: s0=1024 fin_hi=1072 front=1024; id=34: 512/544/512;
  id=39: 512/672/512) — a **second unsafe publisher besides 541d's frontier pin**: the
  shipped light-cone coalesce publishing `fin_hi` above `front` while a truth at the
  frontier's start is live. v4: **0/8**, same seeds, same window.
- **Present, same protocol** (clean pairs): 1440/1536, 1280/1472, 1440/1536, 1280/1792,
  1440/1536 = **86.9-93.8%** (s19 71.4%; the fired seeds have no shipped present — the
  process died). Rollbacks, merges and region collapse (→1) are the same class in both
  arms; deadline misses within ~10% (915-1352). E1 reproducer s19, sequential:
  shipped 1984 / v4 1792 (90%) / v3 1696 — in a quiet window even v3 does not starve on
  s19 (541d's own 43-1732 span), so the window, not the arm, owned their 43-141.
- **The equality law under v4**: 136 RB lines across all gated draws, **every m ≤ 0**
  (max m=0, minimum −512), `out=[]` on 136/136 — containment and the boundary attractor
  hold under the floor publisher exactly as under v3/da23.
- **The load axis** (`work/draws/mid_*.err`, `crush_*.err`): 4-way block — v4 present
  730/730, 717/748, 311/647 and **43/529 on s11**; 12-way — v4 341/730, 435/545, 119/270,
  **43/362 on s11**; v3 identically starved wherever v4 did (43, 341, 119) and worse
  elsewhere (153 vs 435 on s21). HAZ lines in the pinned draws show the mechanism:
  `f=0 F=0 S=0` for the whole draw under v4 vs `f=0 F=368→512` under shipped — a region
  never accepts (frontier pinned at 0), its truths at start 0 pin `floor0`, and shipped
  presents only through the coalesce above them — the exact publications that fire when
  the clash lands.

**Predictions** (`predictions.md`, registered before the paired/crush blocks; only E1-s19
had been flown): P2-fires **held with the full contrast** (v4 0/8; shipped 3/8, inside the
predicted 0-4 race band). P2-present **held** (every clean pair ≥ 0.5×, median 0.93 ≥ 0.7).
P2-equality **held** (all m ≤ 0). P1-v3-starves **failed in a quiet window** (1696, not
≤ 250) — 541d's starvation was their window's load, which sharpened the design: the load
axis, not the seed axis, discriminates. P3-crush **held on 6/8 paired draws, failed on s11
twice** (0.08-0.12× shipped) — the honest boundary below. Kill criteria: **not triggered**
(no v4 fire, no pinned-final-lead-with-shipped-advancing beyond the s11 laggard class,
which is the same pin as the kill criterion's letter — reported as the finding).

**What would make it wrong.** The exactness argument (restores read kept snapshots and
kept truth starts, both ≥ floor0; floor0 monotone) is argued, not proven — a v4 fire with
`fin_hi ≤ floor0` at publish time would break it; none landed in 30 gated draws (E1 2 + quiet 8 + mid 4 + crush 8 + 541d's 8 v3 draws on the same gate). The three shipped fires
are wall-clock draws; a checker's window may see fewer (bf83 pooled 4/62) — the
deterministic content is the fire *signature* (fin_hi > s0 = front through the coalesce)
and v4's zero. The laggard under load was measured at 4- and 12-way only; between quiet
and 4-way the boundary is unmapped, and the laggard's own cause (parked? blocked? starved
by oversubscription) is not opened — the HAZ `b=3` line says busy regions exist while one
never accepts.

**Cost of adopting.** Five lines in `finalize()` behind the existing `stride_gate` flag
(one build, both arms). Cost in flight: the floor lags the shipped advance by
O(sync + window) ≈ ≤ 144 chronons (final lead 0 everywhere, by design), and present
within 10% of shipped when every region accepts. Not adoptable as the whole fix: under
load the channel is min-coupled and starves (s11: 43 vs 529). What is adoptable is the
shape: the close is no longer blocked on a channel that must beat the coalesce — it needs
a floor that is **per-region, not global** (publish up to the deepest restorable tick
among truths that can still touch *this* lineage, with merge-capping so a merge cannot
union fin parts past a member's bound), or the scheduler refusing to let one region pin
the whole engine's finality (the laggard is also a scheduling failure: shipped hides it
behind the unsafe publisher).

**PRINCIPLES.** #13 "we don't want errors that can compound": the floor publisher cannot
fire because it never publishes above what a rollback can reach — safety by construction,
not by margin. #19 "if you find yourself fixing things that's oftentimes a signal that it
is the wrong representation": the shipped design has two publishers above live truths;
v4 makes finality's invariant explicit (publish only below the deepest restorable tick)
instead of patching each publisher. #9: the crush starvation kills this configuration of
the channel, not the method. #22: "the simulation tells us what's next" — the HAZ f=0/F=0
lines named the laggard, not a hypothesis.

**Lens (Taleb).** The barbell held: the exact, paranoid floor (integers, monotone bound)
at one end; the disposables (v3 arm, load blocks) at the other. What the lens gave: the
crush axis found the convexity violation — the gate converts one region's stall into
everyone's ruin (min-coupling), which a mean-load test (the quiet protocol alone) would
have hidden. What it may have missed: the per-region bound is one experiment away and I
did not fly it — the window closed on measuring the boundary rather than closing it; and
I did not check whether the laggard pin also exists in *shipped* as a silent deadline-miss
path (it does — shipped's present 529 vs 1984 across windows is the same laggard, hidden
by the coalesce).
