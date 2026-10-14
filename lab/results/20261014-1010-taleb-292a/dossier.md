# Dossier — 20261014-1010-taleb-292a (Taleb lens)

## Claim

The compact↔live crossing that the adopted ephemeral-promotion design will multiply never
finds a fixed point (128/128 chains, no key repeat to depth 64) and its walk lives in the
**w column** (periapsis angle): the decoded state drifts a median 6.4×10⁻³ of the radius
in 64 crossings (worst 3.4× — the orbit scrambles), **invariant to the doll's word scale**,
because near-circular and strong-field members re-lottery their periapsis angle by up to
0.31 turns **per crossing** — so demote-at-commit cannot land on today's columns; the
residual (or a phase-anchored angle column) must be carried first.

## Bottleneck

`nladder` open direction 0 / `frame-cost`'s ephemeral promotion: b29a's composed path
(13× CPU, ≥200× bytes) is the adopted direction and it multiplies crossings. The page's
own gap: "an end-to-end `resolve_handout` scene with doll units" and direction 3
(canonicality). This run measures what one crossing does to the compact row's columns and
what 64 of them do to the orbit. Expected gain: none claimed — this is a pre-adoption
hazard measurement (the lens's job): it deletes the assumption "the crossing is
error-free, only its CPU matters".

## Evidence

Composed probe on shipped pub APIs only (`Orbit::compile`, `Orbit::state`, `binding::cartesian`,
`Rebinding::from_state`, `Residual::reconstruct`, `Trajectory::key`; the shipped
`decode`'s `to_doll` radius conversion, bind.rs:127-131; `in_tube_units`, bind.rs:252-258),
crates/universe/examples/seam_cycle.rs (in work/patch.diff). Cycle: columns → compile →
state at fixed phase φ (t = φ·P(keyₙ), as the compact t column demands) → cartesian at the
doll word → [×1/μ rounding] → `from_state` → columns′. 432 chains: 6 periapsis scales
(16·2^{-1…30} M) × 6 e (0…0.99) × 2 φ × 3 word coarsenings (0/+4/+8) × 2 dolls (unity, μ≈1.28),
depth 64. All numbers: `sh lab/results/20261014-1010-taleb-292a/regen.sh` (~70 s incl. build).

- **No fixed point**: 128 completed chains, 128 never repeat a key (unique ≥ 60); only 3
  one-step repeats. 8398's key-level transit result confirmed at column level.
- **The walk is the w column**: per-crossing |Δw| median 1.4×10⁻⁵ turns, max **3.1×10⁻¹
  turns** (near-circles e ≤ 0.001 and strong-field/high-e arms p = 8–4096 M). k is stable
  by comparison: median |Δk| ≤ 1 Q48 ulp per crossing (max 1.4×10⁵ ulp on outliers; 6–14
  directed k-walks, worst −2.3×10⁶ ulps over 64, an e = 0 circle at p = 8 M).
- **State drift over 64 crossings** (decoded at equal phase, integer quanta, position ≈
  2^60 quanta by construction): median 6.4×10⁻³ of the radius, min 3.9×10⁻⁷ (best-conditioned:
  p = 16·2³⁰, moderate e), max 3.36 (orbit scrambled). **Identical to 3 digits at word
  shifts +0/+4/+8** — the leak is not the position word; it is the fit's angle
  conditioning (Q32 periapsis angle, Q61/Q62 trig), which coarsening the doll cannot touch.
- **Refusals**: of 432 attempted, 195 `cartesian:Range` (all the μ≈1.28 arm: the fixed
  doll word overflows once the radius leaves tube units — the shipped `word_for` keeps a
  factor-2 margin, my fixed word does not; the μ arm is therefore **unmeasured here, not
  safe**), 99 `state:Range` (extreme apoapsis arms at e ≥ 0.9), 10 fit refusals. The
  completed set is all-unity-doll arms; the μ conversion adds one more rounding per
  crossing, unmeasured.
- **Controls**: P1 `reconstruct()` is an exact left inverse on 128/128 (within-order
  identity holds; the residual carries what the fit discards — the leak appears exactly
  when it is dropped, as the compact row does). P2 a real kick (|v|/1024) moves k by
  1.3×10⁷–9.7×10¹¹ ulps — the instrument sees physics. Determinism: one chain rerun,
  every step bit-identical (the seam is a pure function of the integer state; direction 3
  answered: **no schedule dependence exists at the seam — the hazard is information
  loss, not nondeterminism**).
- **Cost**: full crossing 22.8–32 µs (`from_state` alone 13–19 µs) — b29a's 21 µs refit
  arm class; the CPU is not the question.
- **Lower bound**: real crossings also re-quantize each column to the belt Spec's
  p_bits/e_bits/w_bits/t_bits and re-anchor t; none of that is modeled here, so the real
  per-crossing error is worse, not better.

## Predictions

predictions.md was written before the decisive run. What happened: P1 held (128/128), P2
held, P3 held (key moves on ~100%; residual one-shot ≤ 2 quanta not separately tabulated —
subsumed by the drift table), **P4 half-refuted** (the walk is real and directed in w, but
coarse words do NOT bound it — the drift is word-invariant, the predicted drowning
mechanism is wrong), P5 untested (μ arm overflowed the word; honest gap), P6 held
(22.8–32 µs), P7 held (294/432 refused somewhere; all counted, none dropped).

## What would make it wrong, adoption cost, PRINCIPLES fit

- **Wrong if**: the wired demote keeps w+t jointly anchored so the *observed* angle
  (w + phase, observable even for circles) is what survives — then the w lottery I
  measure never reaches the store; or if the engine's real crossings are rare enough
  (battle-only) that 10⁻⁵–10⁻¹ turn errors per crossing stay under a player floor at
  shipping event rates. Both are checkable when the wiring lands; neither is true of the
  columns as they stand (`shipmem::Body` = p,e,w,t, and b29a's checker measured naive
  wiring forcing Wide at 53%/47%).
- **Cost of adopting the finding**: zero for the measurement; the fix direction is b29a's
  own open question made load-bearing — anchor w and t as one observed-angle column (or
  carry the 4×65-bit residual on scars), decided before demote-at-commit merges. Cost of
  ignoring it: every ephemeral cycle re-lotteries near-circular members' orientation up to
  0.31 turns — for a belt (mostly near-circular bodies) that is a contact-discoverer's
  random noise source, and "errors never compound" (PRINCIPLES #13) fails at the seam.
- **PRINCIPLES**: #13 "basically we don't want errors that can compound that's the goal" —
  measured compounding at the seam the adopted design multiplies; #19 "if you find
  yourself fixing things that's oftentimes a signal that it is the wrong representation" —
  the w column is the wrong representation for near-circles (the angle is unobservable
  there); #34/#2 the oracles guard, and this is a guard's measurement, not a new law.
- **The lens (Taleb)**: what it may have missed — I priced the error tail, not the
  allocator's; the one place the doll conversion (μ) was testable my instrument broke
  (word overflow), so the Extremistan question "what does the worst doll do" stays open;
  and I did not measure whether the w lottery changes contact outcomes (that needs the
  encounter tier, off-plan until wired).
