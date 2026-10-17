# Predictions (written before the decisive long flights and the bench)

Instrument calibration (not predictions): the same flights must reproduce the published
record first — OFF 5,400 gs: max/p99 334/136, events 22,219, kicks 9,217 (1a46); the
deleted set 477 (274 belt, 200 in-situ, 3 doll-3); max |Δangle| of the deleted in-situ
2.6e-4° at 5,400 and 1.2e-3° at 11,000 (1a46 + its 1637 check). These hold already in
work/flights (bit-identical ledgers; thread-4 states identical).

The decisive experiment (the checker's named one, cheapest decisive part): fly OFF and
ES_SECULAR to as far past 11,000 gs as the window allows (target 8e6 game-s; the checker
asked 2e7 — see dossier for what the reached horizon still decides), tracing the deleted
set's position angles at log-spaced horizons, and price the re-kick on shipped code.

## Held-out predictions

1. **The two-point exponent 2.15 does not survive; the debt bends toward linear.**
   Mechanism: the debt is the unapplied secular precession (the arm's pure tube never
   precesses; OFF's sigma-delta applies it in velocity quanta, error bounded), so
   asymptotically |Δangle| ~ ω·t with ω ≈ 1.1e-7 deg/gs (the 11,000-gs slope), not t^2.15.
   Falsifier: max |Δangle| ≥ 10° by 1e6 gs, or ≥ 1,000° by the last horizon (the power
   law's numbers) — that would confirm t^2.15 and put the debt at 2,750° by 1e7 gs.

2. **Under the linear law, every sane fence quantum q gives k* well under 2^10 at the belt
   cadence** (k* = log2(T*·3.55e-5), T* = horizon where max debt = q): k* ≈ 8.4 at q = 1°,
   5.7 at 0.1°, ~2.5 at 1e-2°. The page's 2^10–2^12 band then needs q ∈ [30°, 4,000°] —
   absurd. Falsifier: the measured quantum (from the shipped words: 2^length_exponent /
   radius for the readout, 2^velocity_exponent / speed for the kick grid) comes out at or
   above ~30°, or the debt saturates below every candidate quantum (then no re-kick is
   ever needed — the stronger kill of the page's band, and of mine).

3. **The re-kick costs less than 36× one fired kick** (the budget test's ceiling at
   k = 8.5; 6× at k = 6). Mechanism: one re-kick = the secular rate sum over the doll's
   sources (the same O(#sources) walk `secular` already does per plan) + one rebind; a
   fired kick = readout + force field + quantize + apply + rebind. Predicted ratio 1–5×.
   Falsifier: the bench measures ≥ 36×.

4. **The 3×-horizon sensitivity does not flip the verdict.** With the law fitted over
   3+ decades (5,400 → the reached horizon), k*(3× the horizon) moves by log2(3) ≈ 1.6
   kicks; the band 2^10–2^12 stays out of reach unless the fitted law is the power law
   (prediction 1's falsifier). Falsifier: the fit is ambiguous at the last octave.

5. **The spared set stays bit-identical** at every traced horizon (structural: an event's
   ctx is read-only in others). Falsifier: any spared body's angle differs between arms
   at any horizon — then the delete leaks and the whole add-back question is moot.
