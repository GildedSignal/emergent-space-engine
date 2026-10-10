Grade: gold

Abstract: The shipped plane's presented frame is Ω(N) in bodies at zero events (~0.7–0.8 µs/body/frame of pure deadline bookkeeping), breaking 16.67 ms at ≈3×10⁴ live tubes (0.72–0.84 s at 10⁶, events 0 everywhere), and the exact player-neighbourhood scan (1.7 µs/body, linear, the shipped default finder) breaks one player item at ≈10⁴. Reproduced from the patch in a clean tree: digest control bit-identical (1674 events, EQUAL), fresh layout to 1.03×, far end 1.00–1.16×, peak RSS 1 930 140 KB vs 1 930 272 (1.9 KB/tube). Code attribution verified line-by-line. Gain: the two digest-invariant when-changes (gate rekey on observer movement; horizon from peeked deadlines) delete the frame's sweep and rekey as work classes; ≥700× is projected, the wall itself is measured. Adopt: one step in crates/universe, before b-belt-wire runs.

## Reasons

**Reproduction (clean tree, `git apply work/patch.diff`, build 10 s).**
- Control: `events settled 1674`, digests `4c390dfb…c70a` EQUAL — identical to the author.
- Main sweep (load 1.6–2.7): 10³ 199 µs, 10⁴ 5 264 µs, 10⁵ 64 453 µs, events 0; sched-only 200/4 436/63 996 (100%, 84%, 99% of frame). My 10⁴ point ran 2.3× the author's isolated value — transient shared-box load; the fresh-layout rerun (2 244 µs vs author 2 236) and 10⁵ (53 585 vs 55 019) match to 1.2×. Constants wobble ±2× on this box; the structure is solid.
- Far end: 3×10⁵ 194 246 µs (author 193 578, +0.4%); 10⁶ 839 041 µs (author 721 515, +16% at load 2.69); peak RSS 1 930 140 KB (author 1 930 272). 1.9 KB/tube confirmed.
- rtf 1 ≈ rtf 100 (2 632 vs 2 251/5 264 µs at 10⁴): per-frame cost, not per-game-second.
- Attribution verified in source: `advance` calls `rekey` unconditionally (universe.rs:792); `rekey` requeues every entity (499–505) — one `Calendar::set` each; the advance loop sets aside every far entity (805–809, `set(e, None)` = remove) and requeues all at the end (827–832); `Calendar::set_unchecked` (crates/space/src/events/calendar.rs:75–97) has no same-key fast path — every touch sifts or removes. Three real heap ops per body per frame, always. `PlayerNeighbourhood::find` is a linear `binding_at`+`cartesian` per body (encounter.rs:53–82) and is the shipped default (universe.rs:207).
- Predictions: all five held (P1 323× growth 10³→10⁵ in my run; P2 ≥84%; P3 crossing ≈3×10⁴, the disclosed low edge; P4 1.7 µs/body, crossing ≈10⁴; P5 EQUAL non-vacuous, fresh layout within 1.2×). File times: predictions.md 07:11:42, results.md 07:19:53 — frozen before the decisive runs.

**Adversarial cases (mine).**
1. rtf 1000 at 10⁵: frame 51 988 µs, events 0 — the wall is per-frame, not per-sim-time; robust.
2. Co-orbital pile-up (stride 0, 10⁴–10⁵): wall unchanged, and it exposed a defect below.
3. Scene has no player body, so the frame numbers exclude the player's own `find` and `take_due` — optimistic against a real plane; the wall stands a fortiori.

**Novelty.** No HISTORY entry measures the plane's (crates/universe) presented-frame cost against N; the frame-cost and scheduler work of H0157–H0173 (ladder v6/v7, allocator rounds) belongs to the pre-pivot engine. docs/plane.md foundation 7 asserts "Bounded work per presented frame" with a 16.67 ms deadline: measured false in the shipped code — the frame itself is Ω(N) scheduling before any physics runs. `b-belt-wire` and `b-readout-cost` are both in lab/queue.txt; this lands exactly before the belt bet is placed, and its warning (B18b would grade the scheduler, not the belt) is decision-changing.

**Goal fit.** Board item 4 (smoothness and the allocator: "least-slack scheduling fed by surprise rates" cannot be fed by a sweep that touches every body to learn nothing is due). PRINCIPLES #14: "No work for no reason… 'we only care about changes'" — the frame re-touches every body three times to learn that nothing is due; #12: "i care about the p95/99 results i want the game to be smooth" — at zero events the whole frame is the tail; #1: the cheapest compute is compute not done. The digest control (budget invariance) respects #2: exact means deterministic, and the fix changes *when*, never *what*.

**Dings (recorded, none fatal).**
- "sched-only = frame within ±5% at every N ≥ 10³" is overstated by the author's own S4: 795 481/721 515 = +10.3% at 10⁶ (mine +2.8%). The ~100%-scheduling conclusion stands.
- The ≥700× gain is projected (the fix is not built); the measured facts are the wall (43× over budget per frame at 10⁶, 180× for one `find`) and its code attribution. The dossier labels it "expected gain" — honest, but the integrator should read it as a projection.
- Small-N constants move ±2× with load on this shared box; the integrator re-measures on the M1 anyway.

## What the author missed

- **The stationary-overlap miss in `hit` (a correctness lead, found by the stride-0 adversarial case).** `law::hit` (crates/lattice/src/law.rs:332–348) requires approach: for a pair already within reach it returns `dw < 0`, and the far branch short-circuits on `ww == 0`. Two bodies with zero relative velocity that are permanently within reach — exact formation flight, identical orbits — are never encounters: measured 0 hits for body 2 with 512 ships two-per-identical-orbit (scan still costs 1.17 ms). A player flying in formation sees an empty neighbourhood; a wingman inside the radius is invisible. The bench's zero hits at stride 0 are this defect, not empty space. For the lattice law "approaching" is deliberate (settled pairs must not re-fire); the encounter finder inherited it. Whichever lens picks it up should decide whether `encounter.rs` needs the stationary case before the Binet cone replaces it.
- The 10⁶ sched-only sample ran on a universe already advanced 18 frames; the +10% gap vs the frame p50 is disclosed nowhere.
- Per-event resolution cost under cache pressure at N (records at DRAM distance) and the `threads > 1` wave path remain unmeasured — the author says so in the lens section; the zero-event wall makes them second-order for this claim, but they will bound the fixed scheduler's floor.
