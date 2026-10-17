# Dossier — 20261017-1829-spacex-d399 (spacex lens)

## Claim

One of the three trajectory evaluations inside every belt kick's fit is dead work — `Rebinding::from_state`'s `decoded_event()` computes a residual the flown path (`bind_in`) throws away — and deleting it is **bit-identical on every digest** (all 5 `N=3000` ladder_digest cases) while cutting the fit by **18.6% in ns/call** and the flight's engine p50 by **18.3%**; the same measurement refutes the page's direction-2 hypothesis (`at_radius` is 1.1 µs, 4% of the fit) and corrects the compile share upward (12.3 µs, **49%** of the fit on flown keys, not ~26%).

## Bottleneck

The board's #3: one kick at 75–160 µs against a ~50 ns floor (gap ~10^3.3); the fit (`bind_surface`) is its largest measured term (45–59% of the kick clock item, this page). SpaceX order: question, then **delete**. The fit evaluates the *same* trajectory three times per bind — `at_radius` (closed-form radius cut), `decoded_event` (a time→psi Newton solve), and `bind_in`'s `decode` (another time→psi Newton solve). This run prices each and deletes one.

## Evidence (Linux/x86, 8 vCPU shared; orders of magnitude only)

Instrument: env-gated stage timers + counters (`crates/space/src/fitprof.rs`), input capture (`crates/universe/src/fitcap.rs`), replay bench `--example fitbench`; all arithmetic untouched, digest-neutral (the bench's own flight reproduces pristine `4995f384…` with kicks 40,106, bit for bit).

**Decomposition** (24,576 `bind_surface` inputs captured from the flown `N=3000 belt crossing`, replayed 3×; per call, means; p50 total 17.2 µs, mean 26.2):

| stage | µs/call | share of stage-sum |
|---|---|---|
| `fit_key` (cubic inverse) | 4.03 | 16% |
| `compile` (shape quadrature) | **12.33** | **49%** |
| `at_radius` (cut + 1 quad + read) | 1.16 | 4.6% |
| `decoded_event` (Newton + read + cartesian) | 3.67 | 15% |
| `residual_between` | 0.02 | 0.1% |
| `bind_in: decode` (Newton + read + cartesian) | 3.66 | 15% |
| `bind_in: turn + residual` | 0.34 | 1.3% |

Newton solves: 2.755 µs each, 2 per bind, ~2.98 iterations/solve; quads 18.6/bind (15.6 without `decoded_event`), `node()` evals 13.3/bind.

**The delete** (skip `fit.residual = Residual::between(state, fit.decoded_event()?)`, `binding.rs:447`, env `FIT_NODECODED`): replay mean 26.16 → 22.52 µs/call (−13.9%), p50 17.19 → 13.63 (−20.7%). On the wave flight (`nladder 3000 coast 20 1000`, prof build): `bind_surface` 617.1 → 502.6 µs/frame (**−18.5%**), ns/call 21,892 → 17,813 (**−18.6%**), engine ms p50 3.530 → 2.883 (**−18.3%**), p99 10.043 → 9.799, `process` 1720.6 → 1578.8 µs/frame (−8.2%), zero frames over budget both arms. (nladder's ±0.1% kick-rate jitter is tool noise — two pristine reruns vary 5.650/5.652e-4; the authority is ladder_digest.)

**Identity**: `FIT_NODECODED=1 ladder_digest N=3000` vs the inert-patch baseline — all five cases (coast, forward L8, key mashing, coast through the wave, belt crossing L10) identical in digest, kicks, encounters, contacts (`ddd5b1cc…`, `69d7abbb…`, `253d8aed…`, `d2632de9…`, `4995f384…`), four schedules agree in both arms. Structural proof: `bind_in` builds its own residual from its own `decode` (bind.rs:276–291) and the universe never reads `fit.residual` (`grep`: universe's only `Rebinding` consumers are `trajectory`, `periapsis_angle`, `periapsis_time`, `clockwise`); the residual's real consumer, `TubeEvent::bind` → `fit.reconstruct()`, lives in the space crate's handoff path, which the plane does not fly.

Commands (each ≤ 80 s): `cargo run --release -p emergent-universe --example fitbench`; `cargo run --release -p emergent-universe --example ladder_digest -- N=3000` with and without `FIT_NODECODED=1`; `nladder 3000 coast 20 1000` both arms. Full set: `regen.sh` (~7 min).

## Predictions

`predictions.md` written before the held-out runs. **P1 held** (bit-identity on all five cases, including `key mashing`'s hand-out/burn callers — P3's risk case). **P2 held with margin** (predicted 3–8% engine-ms drop, measured 8.2% on `process`, 18.3% on p50). P4 held (spikes reproduce per-input; not claimed as engine costs).

## What would make it wrong

- A future caller that reads `Rebinding::residual` on the plane's path (today none does; the API split must make the residual opt-in, e.g. a separate constructor, so the dead value is never silently wanted).
- A state where `decoded_event()` errors while the rest of the fit succeeds: with the skip, `from_state` binds slightly *more* often (no corpus case did; the five digests cannot prove the nonexistent case — a probe would).
- The replay's tail (p99 345 µs, max 1.6 ms) is first-touch/FIT2-rebind in replay; the flight's own stage table is the honest wall source (used above).

## Cost of adoption, and fit with PRINCIPLES

One-line semantic change plus an API split (~10 lines: a residual-free constructor for the plane's `bind_in`; space's `TubeEvent::bind` keeps `from_state`). No new state, no law change — the certificate is bit-identity itself. This **is** the principle: "The cheapest compute is compute not done. Delete before optimizing" (§1); "the best part is no part" (§17). It also sharpens the page's map for the remaining 81%: the compile (49%) is the next term, and `from_state` compiles with no `ShapeMemo` — the belt's quantized keys (`MemoCode`, 44 bits) make a shape-key memo the next candidate delete-class lever, unmeasured here.

## The lens

SpaceX's delete-first found a pure delete, but the same lens biases against the subtler lever it exposed and did not take: `bind_in`'s `decode` (3.66 µs) also re-inverts information `at_radius` already produced — but its output *defines* the residual the tube's later readouts are measured against, so deleting it is a representation change (the residual's reference frame), not a delete. A checker should ask whether the two Newton solves can share a warm start (same target, ± the periapsis tick rounding) without touching the residual's definition.

## Files

`predictions.md`; `fitbench_stages.txt`; `ladder_digest_pristine_n3000.txt` + `ladder_digest_delete_n3000.txt` (identity; regen re-derives the inert-patch baseline itself); `nladder_wave_{shipped,delete}.txt` (wall A/B); `work/patch.diff` (fitprof, fitcap, fitbench, instrumentation, the env-gated delete arm, and the `proc_pid_rusage` Linux fallback so `nladder` links off the Mac); `wiki/read-stream.md` (page update, conflicts folded).
