Grade: gold

The shipped plane's frame loop is a hidden tick: `Universe::advance` peeks, defers and requeues every body every frame (deadline-ordered queue, tick-based deferral), costing 0.43 µs × N per frame at constant event rate. Reproduced from `work/patch.diff` in a clean tree: slope 0.429 µs/body/frame; walked/frame = N minus the due few at every size; events/s 453–454 flat in N; engine p99 flat (kick bursts, not the N-term); digests bit-identical with/without the rekey walk at three (N, seed) pairs including my own seed 7; and my fresh build reproduces the author's stored N=6203 digest exactly. The 5 ms budget is exhausted by the scan at ≈1.2×10⁴ quiet bodies; at 10⁹ the scan alone is ≈430 s/frame. Adoption: queue restructure (key-tick order, calendar wheel, or defer-by-deadline) with the digest-equality method as regression; nothing in the law changes.

## Reproduction (mine, shared 8-vCPU box, orders of magnitude)

Built `cargo build --release -p xtask` after `git apply work/patch.diff` (28 s). Runs: `xtask universe --bench --seconds 6 --rtf 100 --unpaced --haulers {71,800,3200,6144}` plus `--no-rekey-walk` and `--seed 7` pairs.

| N | engine p50 (mine / author) | walked/frame | ev/s | digest rekey = norekey |
|---|---|---|---|---|
| 130 | 0.127 / 0.065 ms | 115.3 | 453.0 | — |
| 859 | 0.353 / 0.21–0.23 | 834.2 | 453.0 | — |
| 3,259 | 1.05–1.52 / 1.02–1.12 | 3,218.9 | 453–454 | yes (`d1b192f3…`) |
| 6,203 | 2.73–2.80 / 2.45–2.67 | 6,138.3 | 453–454 | yes (`3ea75405…`) |

- Slope (130→6203, rekey): **0.429 µs/body/frame** vs the author's 0.43. Absolute p50s sit above the author's (loaded box); the slope — the claim — matches to 1%.
- My N=6203 seed-1 digest `3ea754054a98055e…` equals the author's stored artifact bit-for-bit: the shipped code regenerates the numbers, and the run is deterministic across builds and machines.
- Mechanism verified in source: the `advance` loop only breaks when the queue is empty; every entity is peeked, and non-due ones are `set(None)` → `deferred.push` → `requeue`. `walked` counts exactly that, and it equals N at every size. The queue is ordered by light-delayed deadline while deferral compares the canonical tick, so the frame must pop past everything to find the due few — as the dossier says.
- The author's rtf-30 artifacts: engine p50 1.02–1.47 ms at N=3,259 with identical digests across the flag — the term is per frame, not per game-second.
- Patch hygiene: `baseline-default.json` and `patched-default.json` share digest `a7d089f9…`; the probing knob does not perturb the shipped scene, and `--haulers 12` is the default.

## Predictions

`predictions.md` (07:08) precedes the held-out matrix (07:09–07:17); the two smoke points it was fit on (71, 6203) are disclosed inside it. Held: linearity and magnitude (their intervals missed low at the mid points — disclosed), events constancy, rtf independence, digest neutrality at every pair. Failed: the ≥16× drop from deleting the rekey walk. That failure was pre-registered as prediction 5's kill criterion ("rekey is acquitted and I report the residual term's magnitude instead"), and that branch held: the counter attributes the slope to the defer scan. Honest failure reporting per H0183, not a defect of the claim.

## Adversarial cases (mine)

1. **Seed 7** (fresh draws, higher event rate 541/s): digest identical across the flag (`bf440750…`), no 16× drop (1.52 vs 1.50 ms), walked/frame still ≈ N. The claim survives a different universe.
2. **Held-out mid point fit on my own endpoints**: affine fit on 130/6203 predicts 0.44 ms at N=859, measured 0.35 — sublinear middle (cache), same direction and disclosure as the author's own miss.
3. **Cross-artifact determinism**: fresh build from the patch reproduces the stored digest exactly (above).
4. **p99 flat in N** (3–5.5 ms everywhere): the N-term is not event work.

## Novelty and goal fit

No HISTORY entry or doc measures the plane's per-frame scan; the H0012–H0030 scan kills are the old `emergent-engine` SAP/knowledge scans, a different crate. plane.md §7 promises "bounded work per presented frame" — this shows the promise broken at ≈10⁴ quiet bodies, correcting the focus line's premise ("kicks dominate the engine's cost" only below ~10⁴ bodies). PRINCIPLES P14: "No work for no reason, so no ticks" — the loop asking "who is due" is a tick over all bodies; P22: "the simulation decides, heuristics schedule." Board bottleneck 4 (worst frame, smoothness). Diagnosis-with-nothing-to-build is gold precedent (`components-4643`); here the premise killed is the frame loop's cost following events, the instrument (`walked`, digest equality) ships with it, and the fix directions are concrete. Adoptable within one step by the queue's owner.

## What the author missed

- **Ordering of fixes**: view_gather measured 146 ms p50 at 6,203 bodies in my run (88% of frame, ≈53× the engine scan). The queue fix alone moves nothing player-visible until the gather's identical every-emitter-every-frame structure is also fixed; the dossier flags it as owned elsewhere but does not weigh the ordering.
- The sublinear middle (both their runs and mine sit below the two-point fit) is disclosed but not diagnosed; likely heap/cache effects.
- Digest neutrality is proven at the canonical cut; mid-run presented ticks (the horizon) may differ between schedules — schedule-only by design, but the queue owner should have that sentence.
- `--haulers` caps at 200,000 (≈86 ms/frame scan alone by the measured constant): a natural larger rung was available and not run, though unnecessary for the claim.
