topic: cell-rebind
status: open
closed-by:
valid-while: crates/space@9ce84b67 + 20261018-2312-system-9eeb's patch (orbit.rs served/from_shared, binding.rs:422)
updated: 20261018-2312-system-9eeb

# The rebind served from the law's quantized cell, exact key carried

## Current best

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

## Open directions

1. **Adoption shape (the biggest change):** efd4's intern + refcount + evict keyed by cell
   (memory-h-live's "the mint must consult the key before fitting", now flown in reading form),
   the belt's cell census at this width (unmeasured; the view page's "peaks at 37" was a coarser
   2⁻³ grouping), and the plane gates B12/B13/B17 re-judged with the served rebind.
2. **The width ladder:** 12+12 → 13+13 fraction bits if any plane gate fails (P2 held with only
   1.5× margin); one more bit halves the error, doubles the cells.
3. **Compose with Carlson wiring** (kick-jet open 1) for the ~3–10 % cold builds; the levers
   multiply.
4. **The resonance guard:** a population straddling a mean-motion boundary sees a 2⁻¹¹ period
   shift as a regime change, not an instrument error; the strong-branch exact serve as a guard
   is designed, unmeasured.

## Contradictions

- law.md's "Not adopted: a quantized (E, L) memo for kicks" (the write-back reading) vs this
  page's carried form — resolved by construction and measurement (exact recurrence 0.000, hashes
  stable), but the law text is its owner's to re-word.

## Runs

- 20261018-2312-system-9eeb (awaiting grade): the carried cell serves 96.7 % of rebinds (58
  builds / 1,764; 10.2 % never-seen cells per distinct kick), FIT −64 %, 85 cells standing, all
  gate bands held, state channel exact.
