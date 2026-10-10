# Dossier — 20261010-1544-system-97ce (lens: the whole system)

## Claim

On the engine's own belt path the cycle memo hits **0 of 203,017 kicks** (every kick rebinds and rekeys: 1.000/kick measured), so the "shared compiled cycle" delivers zero sharing exactly where sharing should be easiest — a smooth belt — and one Darwin compile per kick (~24 µs/event on this box) is the belt's whole engine cost; the same scalar stream is the allocator's H_live input, so the compute bottleneck (kicks) and the unmeasured memory risk (H_live, HANDOFF) are one measurement, not two.

## Bottleneck

Board line 1 ("fewer kicks per orbit; kicks dominate the engine's cost") and HANDOFF risk "H_live … not measured yet". What actually dominates is not the kick (an integer add plus carry, nanoseconds) but the **rebind each kick forces**: a fresh fit and compile because the quantized (E, L) key flips on every kick — including kicks whose impulse is physically tiny (a 2⁻¹⁰ planet's tide at ≥ 2 AU). Expected gain of the already-designed fix (the re-anchor: keep the compiled cycle until the accumulated offset reaches √(floor/C), law.md "Not adopted … re-anchored, ≈ 0.05 compiles per kick"): measured 1.00 compiles/kick on the belt against the design's 0.05 — **~20× the design's own target, and on the weak-field population where the billions live**. It deletes the compile, not the event; the secular-kick build (0.3 kicks/orbit, H0190) then deletes the events. What it lets us delete: the memo's per-body recompile path and the fear that 10⁹ needs a new memory mechanism.

## Evidence (commands ≤ 60 s, this box: 8 vCPU x86 cloud runner, shared)

Instrumented `crates/universe/src/universe.rs` (`Stats`: `kicks_dv`, `rekeys`, `rebinds`, `dv_class`; counted in `apply`) and wrote `crates/universe/tests/hlive.rs` (a 384-ship smooth belt: banded p 2.1–3.3 AU, Rayleigh e σ=0.1, uniform angles — B18's generator shape, a fixed LCG; one Jupiter-analog planet 5.2 AU, mass 2⁻¹⁰; two cadences).

```
cargo test -p emergent-universe --release --test hlive -- --nocapture
```

- step_log2 7 (2 planet periods ≈ 24 game-years): events 406,220 (kicks 203,017, boundaries 202,818), **rebinds 203,017, rekeys 203,017 (100%)**, wall 9.4–10.0 s ≈ 23–25 µs/event; 196.7 events/body/ship-orbit (4.4 yr orbit).
- step_log2 4: events 50,939, rekeys 25,401 (100%), 24.7 events/body/orbit, 23.7 µs/event. **Work ∝ cadence (8.0× for 8×); cost per event flat** (same machinery).
- Control (`control_coorbital_kicks_are_quantum_large`, 8 ships at sep ± 1.5–3 Hill radii): kicks 397, rekeys 397 — the probe is alive; co-orbital kicks are quantum-large as expected.
- Sizes: `Binding` 176 B, `Segment` 192 B, `BodyRec` 448 B per body today (the plane's live record); design floor 16 B tube.
- Extrapolation, 10⁹-body belt at 2⁷: 1.42e-6 events/s/body ⇒ ~1.4e3 events/s ⇒ ~35 ms CPU/s ≈ **3.5% of one core** on this box (4.4-yr orbits; the board's "~190 cores at 10⁹" was low orbits — belt-scale compute was never the emergency). H_live from this stream: the tube is *replaced* per kick, not appended (history pruned at the light cone), so live RAM per body is bounded by the record format — **16 B tubes alone = 16 GB > 8 GB at 10⁹**: the memory question is the record format and program materialization (shipmem), not the kick stream.

## Predictions (`predictions.md`, written before the decisive read)

Failed honestly, and the failures are the result:
1. Predicted dv≠0 fraction 1–30% and a dv histogram concentrated at ±1 quantum. **First run showed 0/203,017 — my control then failed too, proving `kick.dv` is never populated on the ext (root-doll ship) path: the first probe was blind, an instrument artifact.** The control did its job (lab rule: controls on both sides).
2. Re-issued with the memo-key probe (retired vs new `Cycle::key()`): rekeys 100% at both cadences. Prediction 1's structure (distinction rate ≠ proportional to cadence) failed in the limit: the key distinction stream *saturates* the event stream.
3. Prediction 5's memory half held: the kick stream is not the 8 GB threat; the record format is.

## What would make it wrong

- If `cat.insert` dedups by content and the compile is *not* the per-kick cost: the 23–25 µs/event is then in the fit/readout, and the re-anchor buys less. Distinguishing test: time `bind()` alone per kick (one more counter).
- If the plane is *already* meant to carry the re-anchor and this belt path predates it (motion-law v2 steps 1–2 only): then this is a known-open item measured, not a new finding — but the 1.00 vs 0.05 gap is now a number the build must hit, on the belt scene.
- If B18's belt (2²⁰–2²³ bodies as a program, zero per-body events until a real encounter) is the *shipped* belt path and this per-body belt is only the debug plane: the 0% memo hit still stands for every kicked body — programs delay the first kick, they do not change the kick's cost.
- Co-orbital/fleet concentrations rekey per kick *legitimately* (the physics is quantum-large there): the re-anchor must fall back to per-kick compiles exactly where encounters live — the hard special case (see lens).

## Cost of adoption, fit with PRINCIPLES

The fix is already in the design (law.md, "Not adopted: a quantized (E, L) memo for kicks … re-anchored"); this run prices it: 20× compile cut on the belt, and it converts HANDOFF's unmeasured H_live risk into "measure the record format, not the stream". PRINCIPLES: "The cheapest compute is compute not done. Delete before optimizing" (1); "Compute only surprises … cost follows change and entropy" (3) — a rekey below the certificate's floor is a surprise nobody can observe; "A fix signals the wrong representation" (19) — the memo key quantized at the exact state's scale instead of the behaviour's scale is the wrong water for this fish. No gate touched; the belt scene can seed a cadence/compile-count row for B9's "zero work per orbit until an event" promise (a compile per kick is work per orbit).

## The lens (what it may have missed)

The whole-system lens sees the scheduler, the memo and the allocator as one stream — and it may have missed that the *encounter* tier feeds the same stream: near a secondary the rekeys are real (control: 397/397) and the re-anchor must not defer them, or close-approach certificates go stale. A unified "surprise = one quantum of the behaviour's own certificate" rule needs its strong-field case tested before adoption (B12–B13's scene, where the last three runs found the plane's failures). Also one rung of ladder only: 24 game-years, one planet, one belt; the 5-hour-window scale-up (2³ᵉ bodies, resonances) is untested here.
