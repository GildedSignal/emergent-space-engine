topic: cell-rebind
status: open
closed-by:
valid-while: crates/space@9ce84b67 + 20261018-2312-system-9eeb's patch (orbit.rs served/from_shared, binding.rs:422); census arm: main@f7c3's patch (print-only rebind hook, beltcensus example)
updated: 20261019-1316-system-f7c3

# The rebind served from the law's quantized cell, exact key carried

## Current best

**The belt's census is flown and the cells saturate: the standing set is O(1) in N, so the
served rebind survives to 10⁹ as ~2–3 MB, and the kick's compile bill, the promotion bill and
the belt's live shape memory are one aggregate — the cell is the generator (20261019-1316-system-f7c3;
print-only hook at `step.rs::rebind`, shipped exact compile throughout, `memo.rs` control passes
hook OFF and ON).** Belt birth cells at 11+11: 1,095 (2,699 bodies) → 1,425 (9,699; seed 2
1,420) → 1,610 (29,699) → 1,731 (99,699) → 1,831 (299,699) — ∝ N^0.11, per-decade increments
185→121→100 shrinking (missing-mass of the Rayleigh e-draw on the 2,048-fraction gap grid);
**weak branch 100% at every arm, so the standing set is grid-bounded: 2,048 cells per gap
octave (the code's 11 fraction bits), times the octaves the draw spans — 2 here (a ∈ [2,3) AU
with p > 1.2 AU ⇒ ≤ 2 binades), a property of the draw, not of the code; at these N only one
octave is occupied (every belt key sits in gap octave 1, checker-verified; the second opens at
~3×10⁶ bodies), so the draw-bounded ceiling is 4,096 cells ≈ 3.4 MB, not a fit**
~840 B a shape (knots p50 7–8; 948 B at the 10⁷ cells the checker flew); belt B/body 334→5.6 over
the range, against the live build's 2,460–5,100. The fired stream stays in its birth cell:
belt stream cells = birth cells exactly at 10⁴ (both seeds) and 10⁵ over 2–3.2 intervals
(68–89k game-s), fires p50 2–3, cells per body p50 1, new cells beyond birth 29–61 a window
(nearly all the locals'), belt recurrence 0.95–0.99, whole-plane 0.991–0.994 (the 301
non-belt bodies: 237 birth cells, 103–160k rebinds (seed 2's locals fired 160,388), recurrence
0.996 — their own aggregate).
Composition to 10⁹ on cited constants: 36–43k rebinds/game-s (0659's p = 1.0) × 0.40–0.85 µs
serve = **0.016–0.037 cores + turnover**, against the 104 µs compile ceiling's 3.7–4.5 cores;
turnover ≈ 0 per 3 fires measured (no belt–belt channel, 0659). Domains not flown: the burn (a
thrusting body walks its cell every fire), stirring/resonance (turnover, not standing, is the
exposed side), horizons past ~3 intervals, e-draws wider than σ 0.07 (asymptote rises toward the
4,096 ceiling; the ceiling does not move).

[Checker, 20261019 (grade: silver): every number reproduced — the 3×10⁵ and 10⁴ birth arms
bit-for-bit, the 10⁵ stream arm (cells 1,760, recurrence 0.9943, new-beyond-birth 29), memo.rs
both arms. Four attacks, two beyond the flown range: (i) a key-space census from `ladder_ship`
validated exact against the universe census at 10⁵ (96,358 keys / 1,731 cells / 1,401,000 B)
then run to 3×10⁶ (2,035 cells) and 10⁷ bodies (2,141 cells, 2.03 MB, 0.20 B/body, β = 0.083
to 10⁷; seed 2: 2,136, seed 7 at 10⁵: 1,728) — saturation holds 33× beyond the top arm; (ii)
the horizon pushed to 250,282 game-s (~8.4 intervals, past the 8ffc shearing horizon the
author named): the belt stream is still exactly its 1,425 birth cells, recurrence 0.9837,
fires p50 9, all 144 new-beyond-birth cells the locals'. Two corrections: the ceiling is
draw-bounded, not code-bounded (folded in above: one gap octave occupied at the run's N, the
second opens at ~3×10⁶; per-decade increments stabilise near 200 while it fills), and the
locals' rebinds reach 160k (fixed above). Silver, not gold: the 10⁹ CPU row (0.016–0.037 vs
3.7–4.5 cores) is composed from cited constants — 0659's fire rate and 0355's serve cost,
itself awaiting grade — and adoption (9eeb's wiring, B12/B13/B17 re-judged, the memo.rs guard
recalibration, the unflown turnover arm) is the one experiment that would make it gold.]

**The kick's compile bill and the per-body standing-shape bill are one mechanism — the exact
(E, L) key in the rebind — and the carried form of the law's cell deletes both walls at once
(20261018-2312-system-9eeb; the `memo.rs` harness verbatim, plane seed 1, 48 bodies, 900 frames,
distinct kicks only).** With the shape served from the 11+11-bit cell
(`QuantizedMemo::get_carried` → `Orbit::from_shared(exact_key, cell_shape)`, env `ES_QMEMO=1`;
unset = shipped verbatim, measured bit-identical, every rebind compiled) and the exact integers
plus the residual channel untouched: **FIT −64 %** (129→46–47 ms per 796-kick stream,
162→58–59 µs/rebind; the compile term, ~104 µs of FIT, is ~99.7 % deleted — 58 cold builds
serve 1,764 rebinds: 3.3 % builds per rebind, 10.2 % never-seen cells per distinct kick; the
served stream explores ~2× the cells of the shipped stream, 81 vs 42, so the standing
`memo.rs` test's 0.9 recurrence guard reads 0.898 and trips under ES_QMEMO=1 — disclosed, it is
calibrated on the shipped stream), standing shapes bounded by **85 cells** (≈27 birth + 58
stream; ~1.8 per body on this scene — the win is amortization, one cell serving ~21 rebinds),
period error vs the exact compile max 6.786e-4 (inside B2's 1e-3 band), advance max 1.322e-4
(B1's band 1e-2, 75× margin), knot counts identical (B9), exact-key recurrence 0.000 over all
796 distinct kicks (the state channel never snapped — this is not law.md's killed write-back
form), and rerun outcome hashes identical. Domain: the plane's weak-field cycles, Linux/x86
orders of magnitude; NOT the belt, not resonant populations, not strong circles (guarded
exact), not Kerr dolls, and the plane gates B12/B13/B17 were not re-judged (a law-level digest
change, exactly as memo.rs's header owes: "behind B1, B2 and B9 re-judged on memo keys" — this
run re-judges B1/B2/B9-class statistics against the exact compile, not yet the plane gates).

[Checker, 20261019 (grade: silver): every number reproduced (patch re-applied, clean rebuild,
regen commands); the disclosed memo.rs on-arm trip verified at 0.898 (regen.sh's "both arms"
echo never actually runs that arm). Adversarial arms all hold: seed 3 (build 2.67 %, 71 cells,
period 5.381e-4, knot delta 1); 3× horizon, outside the tested range (cells 85→90→92 —
saturating, not linear; build 2.09 %); 4× bodies (162 cells < 192 bodies — sublinear). Two
corrections. (1) "Deletes both walls" overstates the memory half: on the flown scene 85 cells
> 48 bodies, so the win is amortization, not a standing-memory reduction — it appears at
scale (my 192-body arm) and the belt census stays the open measurement. (2) The lineage is
uncited and required: the direction is kick-jet gold 6c47's named prize ("the realizable
prize is the QuantizedMemo, ~70×, a law change"), a765/12db measured the compile share
(84–87 %) and the 12+12-bit hit domain from the census side, and read-stream 0355 (18 Oct,
awaiting grade) benched the carried form (`from_shape(exact key, class shape)`, ~85 % of the
compile deletable at 0.40 µs/hit, error p50 1.9e-6 via the finer shape-class — 61× smaller
than this 11+11 cell, hit 0.992). New here: the live wiring, the feedback (served stream
explores 2× cells, live recurrence 0.898 vs census 0.947), FIT/wall measured, off-arm
inertness, saturation. Silver because the kick moves 2.8× (FIT), not 10×, and adoption is a
law decision (B12/B13/B17 un-re-judged, eviction, the memo.rs guard recalibration) — the
gold rung is the gates + belt census, and it should price this 11+11 cell against 0355's
class memo.]

## Refuted

- The write-back form (the orbit's key snapped to the cell): law.md "re-rounds at every kick, a
  random walk (principle 13)" — the shipped `QuantizedMemo::get` returns `from_shape(decode())`;
  the carried form is the one measured above (lineage: r2's exact increments, the 5 October
  correction that an exact memo never hits on distinct kicks).
- **"The belt census is the open measurement / the amortization win's memory half is unproven
  at scale" (the checker's correction (1) above, and open direction 1's belt half): measured —
  cells saturate at O(1) (1,831 at 3×10⁵ bodies, β = 0.11, grid ceiling 4,096 ≈ 3.4 MB), the
  stream adds ~nothing to the birth set over 2–3.2 intervals, and the aggregate reading holds
  (20261019-1316-system-f7c3).** The FIT half of the checker's correction stands (2.8× on the
  plane scene); the memory half is closed.

## Open directions

1. **Adoption shape (the wiring half stays):** efd4's intern + refcount keyed by cell
   (eviction now optional — the 4,096 ceiling ≈ 3.4 MB fits any budget), and the plane gates
   B12/B13/B17 re-judged with the served rebind. ~~The belt's cell census at this width
   (unmeasured; the view page's "peaks at 37" was a coarser 2⁻³ grouping)~~ **closed at 11+11:
   1,831 cells at 3×10⁵, ceiling 4,096 by construction (20261019-1316-system-f7c3).**
2. **The width ladder:** 12+12 → 13+13 fraction bits if any plane gate fails (P2 held with only
   1.5× margin); one more bit halves the error, doubles the cells. [f7c3: on the belt the
   ladder inverts — cells are NOT the binding side at any width up to 11 (the e-draw occupies
   ~90% of one gap octave), so width is set by the error gates alone, and coarsening buys
   little memory: w=9 → 467 cells, w=7 → 122.]
3. **Compose with Carlson wiring** (kick-jet open 1) for the ~3–10 % cold builds; the levers
   multiply. [f7c3: on the belt the cold-build share is ≤ 1.1 % (1,425/165k rebinds at 10⁴),
   so Carlson matters only for the locals.]
4. **The resonance guard:** a population straddling a mean-motion boundary sees a 2⁻¹¹ period
   shift as a regime change, not an instrument error; the strong-branch exact serve as a guard
   is designed, unmeasured.
5. **Turnover, the successor experiment (f7c3):** the standing set is grid-bounded, but a
   stirred or burning belt's cold-build turnover is unmeasured past 3 fires (≈0 measured); if
   turnover approaches the fire rate, CPU returns to the compile ceiling. Fly a stirred belt
   (needs wiring, 0659's note) and a burn arm with the census hook.

## Contradictions

- law.md's "Not adopted: a quantized (E, L) memo for kicks" (the write-back reading) vs this
  page's carried form — resolved by construction and measurement (exact recurrence 0.000, hashes
  stable), but the law text is its owner's to re-word.

## Runs

- 20261018-2312-system-9eeb (awaiting grade): the carried cell serves 96.7 % of rebinds (58
  builds / 1,764; 10.2 % never-seen cells per distinct kick), FIT −64 %, 85 cells standing, all
  gate bands held, state channel exact.
- 20261019-1316-system-f7c3 (this run): the belt census — cells saturate (1,095→1,831 over
  111× bodies, β 0.11, grid ceiling 4,096 ≈ 3.4 MB, weak 100%), the stream stays in its birth
  cell (recurrence 0.95–0.99), and the 10⁹ rebind stream prices at ~0.02–0.04 cores served
  against ~4 cores compiled.
