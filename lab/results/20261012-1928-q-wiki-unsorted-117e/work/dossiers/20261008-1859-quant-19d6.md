# Dossier — 20261008-1859-quant-19d6

**Claim.** On the plane's own bench (Linux/x86, shared box, load 1.3–2.9 — orders of magnitude only),
the frame budget holds everywhere we have flown it, but the engine's capacity knee sits only ~20×
above the flying point, the readout (not the engine) is two-thirds of the frame at that point, and
the player's max burn leaves every frame metric nearly untouched while collapsing the real-time
factor's tail 100× — impact lands on presentation time, not on the frame, and the deferral is
canonical (bit-identical digests across engine budgets).

**Bottleneck.** Board #4 (smoothness and the allocator: worst frame and p99) and the readout's cost
(b-readout-cost, queued). Numbers the integrator had no record of: the capacity knee, the burn's
tail impact, the per-kind event price list, and the pure-resolver-versus-scheduled overhead. No
10× lever delivered; this is the instrument reading the integrator needs before spending the
encounter-skin budget (it prices the event the skin would cheapen, and shows the readout competing
with it).

## Evidence

All runs: `cargo run --release -p xtask -- universe --bench --seed 1 --rtf R --level L --seconds 30`
(paced 60 Hz, engine budget 5 ms/frame, deterministic canonical-tick burn script, digest at a
canonical cut, machine state recorded); JSONs and driver scripts in `work/`. Table: `python3
work/table.py`. 71 bodies (28 + 48 fleet members).

**The latency budget at the flying point (rtf 100, level 0).** Frame CPU p50 1.33 ms = engine 0.11
(8%) + view gather 0.92 (69%) + JSON 0.22 + wire 0.08; frame-CPU p99 3.26 ms, p99.9 5.98, hitches
>16.7 ms: 0, RTF median 100, lowest-1% 100, overflow 3. **The readout is the stage over its
share**, at every rtf ≤ 10³ (view p50 0.92–1.44 ms, engine p50 0.10–0.31 ms).

**The capacity knee (level 0).** Engine p50 grows ∝ rtf: 0.10 / 0.11 / 0.31 / 1.09 / 3.43 ms at
rtf 10 / 10² / 10³ / 4·10³ / 1.6·10⁴. The RTF tail holds at 10³ (lowest-1% = 1000, overflow 10)
and breaks at 4·10³ (lowest-1% 1239 = 31% of target, overflow 109); the median holds even at
1.6·10⁴ (deferral then catch-up). **Knee ≈ 2·10³, ~20× above Julien's 100×**. Unpaced at
1.6·10⁴: same 3.8·10³ events/s as paced — the 5 ms budget binds, not the pacing; blended ~79
µs/event (63 events/frame).

**The event price list (in-universe, per item).** Fleet slice 20–35 µs; ship kick 84–95 µs; player
item 280–590 µs (3–7× a ship, 10–20× a slice). Pure resolver on distinct pending kicks
(`--kick-bench`, 949 samples): made ships median 39 µs (p99 57), leavers median 102 µs (p99 423) —
the leaver is the kick distribution's heavy tail, and scheduling+apply roughly doubles the cheap
path. Memo on distinct kicks: exact hit 0.0%, quantized 94.5% — both reproduce the 5 October
record exactly (harness sanity).

**The burn's market impact (rtf 100, level 0 → 15, same seed/script/cut).** Frame CPU p99.9
5.98 → 6.85 ms (1.15×), hitches stay 0. But: overflow frames 3 → 90, RTF lowest-1% 100 → 1
(presentation stalls ~1.5 s at worst), engine p99 1.74 → 5.39 ms (over budget in the tail). Player
items 297 → 2213 (7.5×). The wake is physical, not an artifact: at level 5 (overflow 3, same as
level 0 — no deferral) ship-class items still grow +38% (1552 → 2144) and encounters 169 → 269;
the player's doll-wide `PlayerNeighbourhood::find` (encounter.rs: every co-doll body tested per
player item, O(doll population) — the one linear-per-event path in the plane) couples the burn into
other bodies' schedules.

**The budget is canonical (control).** Same L15 log, engine budget 1 ms vs 5 ms: overflow 576 vs
90, RTF tail 0.1 vs 1, yet **digest bit-identical** (`a6afde3d…`). The burst is moved in time,
never changed — plane foundation 7, measured.

**Predictions** ([predictions.md](predictions.md)): P1 held (p99 3.26 ≤ 4 ms, RTF on target); P2
held (knee in [10³, 10⁴], engine p50 ∝ rtf); P4 held on frames (p99.9 within 2×, hitches 0) but
missed the metric where impact actually lands — the RTF tail, which I had not forecast; P3
**falsified**: planet/moon items equal, but ship +30–38% and fleet +59% under burns (I predicted
≤10%), and the player reached 18% of items (I predicted <5%) — the wake spreads beyond the
player's stream. P5 held: all digests differ across levels; rtf 10 negative control clean;
overflow > 0 appears by 4·10³.

**What would make it wrong.** x86/shared-box numbers, not M1: orders of magnitude only, the
integrator re-measures (the record's M1 p99 2.45–2.72 ms vs my 3.26 suggests ~1.3×, well inside
one order). 71 bodies: this prices the presentation path, not billion-body scaling. The ship-item
coupling is pinned to the encounter seam by elimination (present at L5 without deferral; nothing
else reads the player) and by the finder's code, not by per-body attribution. The unpaced ceiling
still contains the 5 ms budget — the raw unlimited-budget throughput is unmeasured. Cost of
adoption: zero (instrument + numbers; no code changed). PRINCIPLES: "i care about the p95/99
results i want the game to be smooth" — the tail is where the burn lands, and hitches/hour alone
would have missed it; "the budget changes *when* work is done, never *what*" — now evidenced
bit-identically; "Compute only surprises" — a 0.9 ms/frame gather over a mostly-static 71-body sky
is the next thing that rule should eat.

**The lens.** Quant sees orders, tails and per-event prices; it may have under-weighted *what the
player sees*: an RTF tail of 1× is a frozen game clock, which no ns accounting prices. And the
capacity knee at 71 bodies says little about 10⁹ — the true capacity question (candidate degree
at scale) stays with the encounter lenses.
