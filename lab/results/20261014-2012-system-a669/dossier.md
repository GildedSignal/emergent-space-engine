# Dossier — 20261014-2012-system-a669 (lens: the whole system)

## Claim

The ladder's breaks 1 (the wave's CPU), 2 (memory doubling per first kick) and 4 (the birth
build) are one mechanism: the tube key's own quantum — L's Q32 above all — is 10²–10⁶×
finer than the belt's per-kick ΔL, so the key flips on ~100% of kicks and
`Rebinding::from_state` (which compiles unconditionally, `crates/space/src/binding.rs:421-422`)
mints a fresh compiled orbit per kick; the binding's residual already carries sub-quantum
exactness legally, so a per-population coarser key with a flip-gated rebind divides all three
breaks by the flip run length (measured: exactly linear in the coarsening, 3.3 kicks at Q48
→ 107 at 2⁵·Q48 → 857 at 2⁸·Q48 on E; L needs ~2¹²–2¹³ to reach the same run).

## Bottleneck

The board's "one kick: 75-160 µs against a ~50 ns floor" (10^3.3) and "memory per body,
~5,100 B after the first kick" (10^2.6), at the cadence the N ladder just made binding
(bodies × kick rate × kick cost). The kick's expensive term IS the compile (b29a:
`from_state` 21 µs of the 38 µs composed promotion; the wave at ~30 µs a kick), and the
memory's growth IS the minted+retired compiled orbit (0e37: 74.3% of standing bytes are
derived knots; ladder break 2). Deleting the per-kick compile deletes the wave's CPU, the
retired-table churn and most of the birth build at once: ~10²× at 2⁵/2¹³, ~10³× at 2⁸/2¹⁴.

## Evidence

Code facts (shipped tree, read):
- `crates/universe/src/step.rs:424-429` — the kick quantizes Δv at the **velocity word's**
  exponent and carries the sub-quantum part (`if dvq == [0,0] { return Ok(()) }`): the
  remainder rule exists at this quantum only.
- `step.rs:433` → `rebind` → `crates/space/src/binding.rs:419-448` — `from_state` fits the
  key then calls **`Orbit::compile(key)?` unconditionally** (line 422); no memo lookup, no
  key-equality gate; the universe's `Catalogue` (`crates/universe/src/bind.rs:44`) reuses
  slots but never dedups by key.
- `bind.rs:1-16` — the binding keeps `residual` + `turn`: "what the fit discards… the
  remainder is carried and never dropped" (`fit.residual = Residual::between(state,
  fit.decoded_event()?)`). Sub-quantum (E,L) drift is carried exactly today; the key's
  fineness is a representation choice, not a physics requirement.

Measurement (SI replica of the shipped kick path on the shipped roster —
`work/key_quantum.py`, 64 ladder-belt bodies [2,3) AU, Rayleigh e 0.07, re-fit after every
kick as `from_state` does, 120,000 kicks ≈ 107 yr, h = 2.814e4 s, perturbers Cinder 2⁻²¹ /
Home 2⁻¹⁸ / Giant 2⁻¹⁰ at their shipped elements):
- per-kick |ΔL|/L p50 = **2.10×10⁻⁷** (p01 3.0×10⁻⁹). Against the key's own documented L
  range (1/4 ≤ L ≤ 4096, Q32): the coar**est** legal quantum is 2⁻³²/0.25 = 9.31×10⁻¹⁰
  relative → **226 L-quanta per kick**; the finest (2⁻³²/4096) → 3.7×10⁶. **The key flips
  on 100% of kicks at every legal scaling** (P1 held).
- per-kick |ΔE| p50 = **0.23 Q48 quanta** (p99 0.91); E-word flip fraction **0.300** (P2
  held: predicted 0.25-0.60).
- the velocity-carry gate never blocks: p01 |Δv| = 2,363 quanta of 2⁻⁴⁸c → early-return
  fraction **0.0%** (P5 held) — consistent with the record's "the plane recompiles ~99% of
  kicks".
- the coarsening dial is diffusion-limited, exactly linear: E-flip fraction 0.300 → 0.0094
  at 2⁵ → 0.0012 at 2⁸ (run length 3.3 → 107 → 857 kicks). No oscillation-absorption bonus:
  P3 partially failed — the synodic cancellation ratio is 0.168 (predicted ≤ 0.05) and the
  E word drifts a median −51 quanta over 107 yr (tail 1,616).
- P4 failed as stated: inner-belt kicks are 1.19× *larger* (ΔE = v·Δv; the velocity factor
  beats the pull factor even though Giant dominates the acceleration everywhere).

Reproduce: `cd lab/results/20261014-2012-system-a669 && ./regen.sh` (≈ 55 s; regenerates
`work/key_quantum.out`). Constants are read from shipped code paths cited above; the
script names every one.

Composed onto the ladder's own numbers (orders of magnitude, Linux replica): at 2⁵(E)/2¹³(L)
coarsening the belt's compile stream falls ~100×: the first wave at 10⁶ bodies ~30 s of
compile → ~0.3 s; steady-state belt kicks (8.2 cores at 231 µs, cf45) → the compile term
~0.08 cores + a ~50 ns carry-arithmetic stream; the 2.6→5.1 KB first-kick doubling and the
retired-segment churn per kick appear only per flip; the birth build's compile term
(28 µs/body, exponent 1.0 — ladder break 4) amortizes across a coarse cell (5–180
bodies/cell at 10⁹ at this grain — sharing is a bonus, not the headline).

## Predictions

`predictions.md` was written before the run (see file). P1, P2, P5 held; P3 partially
failed (cancellation 0.168 not ≤ 0.05 — reported as held-not: the dial's gain is linear,
not super-linear); P4 failed with the mechanism named (v·Δv). The load-bearing prediction
(P1) is the one that survived.

## What would make it wrong

- The engine's doll-0 key path for 2-3 AU tubes: the naive root-doll reading puts the
  belt's L at 1.6×10⁴ doll units, **outside the documented [1/4, 4096]** — either doll 0
  rescales (my bracket covers every scaling in the range; the claim is invariant) or belt
  tubes are keyed by another structure entirely, in which case only the E axis (f0a2's
  shipped-code anchor, 319.3 m²/s²) stands, and the E-only dial gives 3.3→107× at 2⁵.
- B5/B12-type instruments could reject the coarser walk: the between-events readout drift
  grows by the coarsening factor (today ≤ ~0.3 m/step at the belt; ~2 km/step at 2¹³ on L,
  ~6×10⁻⁹ relative), re-anchored at each flip — same error type as today (principle 13's
  bar is the type), but the Jacobi/energy gates over 10⁴ periods are the adoption check,
  not this replica.
- Hot scenes are untouched: near Home the per-kick ΔL is far larger and keys flip at any
  grain — this is a cold-belt dial, per population (a global coarsening buys nothing where
  kicks are big and could break the gates).
- The replica is Newtonian-Kepler with the secondaries as impulses; the GR doll, kick
  churn and the resonance tail (one body drifted 1,616 quanta) are unmodeled.

Cost of adopting: a per-population scale on the key's words (a byte per population, the
fit rounds through it), a flip-gated rebind (~20 lines: compare the fitted key to the
binding's; if equal, Arc-reuse the entry and refresh only the residual and the kick word),
catalogue insert on flip only. No law change: the residual already carries exactness
(bind.rs); principle 6 is the law's own sentence.

Fit with PRINCIPLES: #6, verbatim — "Store the generator, not the generated. Aggregates
matter: influences below one quantum accumulate": the sub-quantum per-kick drift below one
coarse quantum accumulates in the residual until the flip, instead of being billed a
compiled orbit per kick. And #1 (the cheapest compute is compute not done): the compile is
compute done for a key that has not changed meaningfully.

## The lens

What the whole-system lens may have missed: the unification is drawn on a replica, not on
the engine's own doll-0 key path (the cap discrepancy above is a real hole — resolving it
is part of the next run); the elegant single dial could hide the hot-regime special case
(fleets, burns, plunges) where coarse keys are wrong or useless; and the sharing bonus at
birth is asserted from occupancy arithmetic, not measured.

Grade suggestion: **silver** — real, reproduced-by-script, one named experiment from gold:
wire the flip-gated rebind with a per-population 2⁵/2¹³ key on the ladder rung and hold
`frame_digest` where the key does not flip, F1 through the wave, and B5/B12 on the coarser
walk. That experiment is a build; this window could not carry one.
