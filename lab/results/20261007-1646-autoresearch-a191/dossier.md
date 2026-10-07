# Dossier — 20261007-1646-autoresearch-a191 (lens: autoresearch on something that works)

## Claim

The plane's kick resolver pays two redundant exact tube decodes per kick for clock bookkeeping; removing them (bit-identically, digests unchanged) makes the median ship kick 16–21 % cheaper and the leaver kick 6–11.5 % cheaper, and the measurement shows the remaining cost is 60–66 % certified quadrature inside `Orbit::compile`, which cannot shrink without changing the law's bits.

## Bottleneck

Board focus line 1, "cheaper events" (kicks dominate the engine's cost; correctors and splits are dead, so per-event cost is what is left). Expected gain: the deletion of two exact trajectory solves per kick, i.e. one small component on the hot path, not a new one. The phase profile that justifies it (diagnostic scopes, `EMERGENT_PROF=1`): per kick, `compile` 60–66 %, rebind bookkeeping (`u_tau2`) two full solves, forces (secondaries+tide) ~7 %, everything else < 5 %.

## Evidence

Commands (each ≤ 60 s; medians of the pure resolver, interleaved A/B on the same loaded machine — this box swung 2.2× in load during the run, so only ratios count):

```
cargo build --release -p xtask
# A/B (tuned case; identical replay_digest and digest required on both sides):
./target/release/xtask universe --kick-bench --rtf 100 --seconds 20
# held out (not tuned on):
./target/release/xtask universe --kick-bench --members 24 --rtf 100 --seconds 20
./target/release/xtask universe --kick-bench --members 96 --rtf 100 --seconds 20
./target/release/xtask universe --kick-bench --members 48 --rtf 60 --seconds 20
# phase profile of either binary:
EMERGENT_PROF=1 ./target/release/xtask universe --kick-bench --rtf 100 --seconds 10
# behaviour gate:
cargo test --release -p emergent-universe -p emergent-space
```

Tuned (members 48, rtf 100, 3 interleaved pairs): made 70.6→59.4 µs (−16 %), leavers 173.1→162.5 µs (−6 %). Held out: m24 leavers 166.9→147.7 (−11.5 %), made 71.4→56.7 (−20.6 %); m96 153.9→140.1 (−9.0 %), 72.2→58.7 (−18.7 %); rtf60 173.5→155.2 (−10.5 %), 69.6→55.7 (−20.0 %). `replay_digest` and the canonical `digest` are bit-identical to the pre-change binary in every case (`eaef383e…`/`c8ab26da…` at the tuned case; the held-out cases keep theirs), `refused` 0 everywhere. Test suites: all green. Re-profile after: `u_tau2` collapsed from ~2 % of total to 0.0 % (0.21 µs/x, one Scalar subtract), `compile`'s share rose as predicted.

The change: `Binding::readout_state` hands the kick the `OrbitState` its own decode already produced; the kick passes it into `rebind_at`; `Binding.proper0: Option<Scalar>` caches the fit's decode at the binding event (`Bound.orbit.proper_time`, already computed — zero added solves), `None` falling back to the old solve so even the error paths are identical. `Debug` for `Binding` is hand-written to omit the cache so record hashing (the bench's replay digest) reads as before.

## Predictions

`predictions.md`, written before the decisive A/B. Leaver medians −8–15 %: held (−6 % tuned — below range there, in range on all three held-out cases); made −5–12 %: exceeded (−16 to −21 %, conservative guess); digests bit-identical: held everywhere; p99 within 10 %: held (−1.5 to −7 %); `u_tau2` collapse with `compile` share rising: held. One miss to report: seeds do not vary the scene (identical digests at seeds 1–3), so the held-out axes were changed to population and cadence before the run.

## What would make it wrong

The gain is bounded by the two deleted solves; at higher real-time factors or on the M1 the mix shifts (more compiles per readout), shrinking it. If `Bound.orbit.proper_time` ever diverged from `orbit_state(event_time).proper_time` for a passage whose decode is edge-legal, `proper0` would carry a wrong clock — the digest equality across four scenes and the whole suite is the evidence against it, and the `None` fallback keeps the failure mode the old error, not silent bits. Adoption cost: one `Option<Scalar>` per binding and one method; nothing else moves. Fit with PRINCIPLES: "The cheapest compute is compute not done. Delete before optimizing" (§1) and "Nothing is evolved that can be derived when looked at" (§3) — the proper time at the binding event is derived-once information that was being re-derived every kick.

## The lens (blind spot)

A local search tuned one case and measured three; it cannot see past the compile wall. The structural change that would beat this best configuration: the per-kick recompile itself (60–66 %) — either the memo at a quantized key (a law change, already adjudicated: it changes orbits) or a cadence change (fewer rebinds per orbit, the integrator's queue). Both are one-way doors outside this lens. Also: this run's absolute µs are from a shared, heavily loaded Linux box (2.2× load swing observed); the integrator re-measures on the M1 — only the ratios and the digest equality are load-bearing here.
