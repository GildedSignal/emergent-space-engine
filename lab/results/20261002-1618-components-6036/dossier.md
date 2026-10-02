# Dossier — 20261002-1618-components-6036 (lens: first principles, one component)

## Claim

The kick's rebind compiles a fresh exact-key orbit every kick (64 distinct keys per orbit,
measured), where the law's own shared cycle memo (`docs/law.md`: "the memo key's index
(quantized E and L, 32 bits) … It is shared by every tube with the same key") would amortize
compiles to ~1 per 100+ kicks at the plane's tide strengths — a measured ~2× cheaper rebind on
the way — but the naive quantized-bucket rebind I built is killed as built: exact at events,
wrong between them, so adoption needs law.md's derivative-corrected memo (∂/∂E, ∂/∂L), which
is the named next experiment.

## Bottleneck

Board live question 1 ("fewer kicks per orbit … kicks dominate the engine's cost") and the
plane's measured kick cost (29 µs on the M1, 15 µs in "rebinding fit and compile"). The
component is the rebind: `crates/universe step.rs::kick` → `bind` → `Rebinding::from_state`
(fit_key + `Orbit::compile`), and the universe's `Catalogue` (`bind.rs`) never dedupes by key.

- **Floor:** a kick = readout + Δv + fit + (key lookup) + remainder. The compile is a pure
  function of the quantized key, so it amortizes over bucket lifetime; the per-kick floor after
  that is `fit_key` (~9 µs here — the next question, a cubic root search).
- **Idiot index (rebind):** ~2–3× today (compile is 53–71% of `from_state` on realistic cases;
  the 29 µs M1 kick carries the same share).

## Evidence (cloud box: 2 vCPU EPYC 7763, load ~1.3, orders of magnitude only)

Reproduce: `git apply lab/results/20261002-1618-components-6036/memo_probe.patch` then
`cargo test --release -p emergent-space memo_probe -- --nocapture` (≈55 s build, <1 s run).
Patch = a `#[cfg(test)] mod memo_probe` appended to `crates/space/src/binding.rs`; no library
API or behaviour touched. Log: `memo-probe.log`.

- **Today, every kick compiles:** `exact_distinct_keys_1orbit = 64` in every case. `from_state`
  median 19–31 µs (case-dependent; near-circular 11), `Orbit::compile` alone 10–22 µs.
- **The exact key moves smoothly and slowly:** the KEYS trace (tuned tide, 128 kicks): gap
  = (1−e)/(1+e) drifts 3.6×10⁻⁴ total, crossing ~1 bucket boundary at width (10,10) per 128
  kicks → memo hit rate ~99%/kick at the tuned tide; ~90%/kick at 10× weaker bucket-relative
  motion fails only for the 100× strong tide (crossings every kick, as the memo arm's collapse
  35/128 → 3/128 → 0/128 from (8,8) to (12,12) shows — graceful, width-driven).
- **Cost when the hit lands:** memo arm ratio 0.52 (tuned), 0.32 (eccentric: compile is 71% of
  the rebind there). `Trajectory` deep-clone cost 0.08 µs — sharing by value is already cheap;
  Arc is not needed for cost.
- **Exactness control (held, 100%):** every rebind, bucketed or not, satisfies
  `reconstruct() == input state` bit for bit — sharing a compiled trajectory cannot drift the
  *event* state; the remainder absorbs the whole bucket offset exactly.
- **KILLED as built:** bucketed drift + refit diverges — `r_memo ≈ 1.5` apoapsis radii after one
  orbit, at *every* width including (20,20) (bucket 5×10⁻⁷ in e, where coarsening cannot explain
  1.5 apo), so the failure is my phase/branch construction on the bucketed trajectory, not the
  coarsening size. For comparison `r_split` (exact key, 64 vs 512 kicks) is 10⁻⁵–10⁻³.
- Two held-out refusals, reported as found: `far` (p = 1000) panics inside fit/quantize
  (`NoBoundOrbit`), and near-circular e = 10⁻³ at (8,8) falls back on 128/128 kicks (the
  bucketed orbit cannot reach r: naive (k, p) buckets are the wrong grid near circles).

## Predictions (predictions.md, pre-registered)

- Held: exactness control 100%; smooth key motion ⇒ hit rate ≥98% at (10,10) tuned (clean trace:
  1–2 changes/128); graceful width-driven degradation under the strong tide; reuse ratio ≤0.5
  tuned (0.52), and 0.32 eccentric.
- Failed: idiot index ≥5 (measured 2–3× — `fit_key` is the bigger half of the floor than I
  predicted); compile ≥50% of `from_state` holds for tuned/eccentric but not near-circular (30%);
  the behaviour gate `r_memo < r_split` failed at all widths — because the construction is wrong,
  and (20,20) proves it is not the coarsening. The formation measurement (cross-ship amortization)
  never ran (the `far` panic precedes it).

## What would make it wrong, adoption cost, PRINCIPLES fit

- Wrong if the M1's kick-bench 15 µs fit+compile share is unlike this box's (compile 50–70%) —
  the integrator re-measures; or if real tides (not my toy diag(+w,−w)·x) move keys 100× faster
  than the tuned case (the strong-tide arm suggests the memo then buys nothing at any width).
- Adoption: not this code. The correct form is law.md's memo — compiled tables keyed by
  quantized (E, L) **plus ∂/∂E, ∂/∂L readout corrections**, so the drift keeps the exact orbit's
  rates while tables are shared; `crates/space` QUADRATURE.md already names this ("a
  Hessian/remainder bound for authoritative kick reuse is future work"). A second, cheaper
  adoption path: dedupe `crates/universe`'s Catalogue by exact key (populations from programs
  share orbits — the shipmem convoys), which the exactness result already licenses.
- PRINCIPLES: "It is shared by every tube with the same key" is the law already saying it
  (principle 6: "Store the generator, not the generated"); "The cheapest compute is compute not
  done"; and the kill respects "A failed experiment kills that configuration, never the method".

## The lens

The lens' blind spot bit exactly as warned: optimizing the rebind component in isolation found
the compile, and the *neighbour* (`fit_key`, ~9 µs) is now the dominant term once compiles
amortize; and my toy tide isolates the rebind from the real force layer, so the hit-rate numbers
are lower bounds on key motion only for tide-like perturbations. The checker should attack the
(20,20) r_memo result (construction bug vs real instability) and re-run the formation arm.
