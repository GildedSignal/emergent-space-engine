# Dossier — 20261011-1102 (autoresearch lens)

**Claim.** On the shipped per-kick path (`readout -> parent tide -> handoff::bind`), deleting the redundant state reconstruction inside `TubeEvent::bind` (plus word-width divisions in `fast_quad`) cuts ns/kick by 6–19% across eight scenes with bit-identical tube streams — and the same measurement shows the kernel sits within ~1.2× of its per-node arithmetic floor, so no ≥2× remains at bit-identity: the lever for ns/event is nodes per kick, not the kernel's arithmetic.

**Bottleneck.** Board #1: "kicks dominate the engine's cost" — the plane rebinds (compiles a tube) on ~99% of kicks, so ns/kick is ns/event for the dominant event. Expected gain: the measured one (fractions of the event, not orders); what it deletes: one full phase-solve + cartesian per kick, and four 128-bit divisions per quadrature node. It also prices the rest: any "make the kernel cheaper" run now knows the ceiling.

**Evidence** (Linux/x86 cloud, 8 vCPU shared, load 0.9–1.5; orders of magnitude only):

    cargo build --release -p emergent-space --example kickbench
    $CARGO_TARGET_DIR/release/examples/kickbench           # tuned scenes
    $CARGO_TARGET_DIR/release/examples/kickbench heldout   # held-out scenes
    cargo test --release -p emergent-space                 # 50 passed, 0 failed

Tuned scenes (µs/kick, best of 5×64; baseline → final; digests identical):

| scene | baseline | final | Δ |
|---|---|---|---|
| weak-circle-p1e8 | 18.6 | 15.7–17.1 | −8…−15% |
| weak-ecc-p1e8-e0.5 | 36.1 | 32.8–33.4 | −8% |
| strong-ecc-p1e5-e0.5 | 49.8 | 42.3–45.4 | −9…−15% |
| deep-ecc-p40-e0.5 | 49.4 | 42.0–42.6 | −14% |

Held-out (run once, final state): 20.3→17.7, 23.6→19.5, 23.5→21.3, 47.3→42.3 µs/kick (−9…−17%),
digests identical to the pre-change baseline on every scene.

Where the kick goes (why): bind is 86–94% of the kick; within bind, compile is 40–65%
(~28 quads at 0.4–1.0 µs each, 27 cut() at ~0.2 µs); within a fast_quad node,
cos = 44 ns, shape/isqrt = 44 ns, three div_words = 51 ns (micro-bench, `example micro`).
Round 1 (div_word for the four u128/u128 divisions) was bit-identical but moved ≤6%:
128-bit division was already cheap, refuting my prior cost model. Round 2 was the win.

**Predictions** (predictions.md, written before the loop): digest identity held everywhere (as predicted);
H2's predicted −5–10% on bind measured −8…−19% (under-predicted); H1's predicted −15–25% did NOT hold
(≤6% — divisions were not the cost); no scene got slower beyond load noise (one 25 µs weak-circle reading
traced to shared-box load; reruns 15.7–17.1 µs).

**What would make it wrong.** `fit.reconstruct()` ≡ the caller's `exact` relies on residuals being
exact i128 differences added back to a deterministic re-decode (`decoded_event` is a pure function of
the fit); if any future change makes the decode path stateful or lossy, the passed-in `exact` diverges.
The gain size is x86-shared-box timing; the integrator re-measures on the M1. The floor argument
(~1.2×) covers the kernel only — a law-level change (fewer nodes, shape reuse) sits outside it.

**Cost of adoption.** One signature change (`TubeEvent::bind(fit, exact, …)`) with two call sites
(`events/handoff.rs`, one test); `num::div_word`/`mod num` made `pub` for the bench; `blake3` added to
`crates/space` dev usage. Patch: `work/patch.diff` (this run's edits). Fits PRINCIPLES #1 ("the cheapest
compute is compute not done. Delete before optimizing") and #2 ("'Exact' means deterministic and
reproducible": every tube bit unchanged).

**Grade suggested:** silver. Real, reproduced, bit-identical, adoptable in one step — but it moves the
bottleneck by a fraction, not 10×, and the floor measurement is the larger half of the result.

**The lens's blind spot.** A local search finds local optima: it cannot take the structural door —
reusing the previous kick's shape table (the table depends on `k` and the weak-field class alone, and
consecutive kicks change `k` by quanta; a law-level k-quantization policy would make the catalogue hit
and delete ~all compile work per kick). That decision belongs to the motion law's owner, not this kernel
run; the cadence lever (q-cadence) multiplies whatever ns/kick remains.
