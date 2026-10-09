# Check 2 (blind, independent)

Grade: silver

**Abstract for the integrator.** Claim: the frame's constraint is the unbudgeted synchronous view gather, not the engine. Reproduced from a clean tree with `work/patch.diff`: digests bit-for-bit (`06b78c67…` m400, `4366e41e…` m4, unpatched identical — the patch is pure instrumentation); gather p50 3.33/3.27 ms at 405 bodies, atom 10.4–10.9 µs/readout across seeds 7/3/42, gather the largest part everywhere at rtf ≤ 100. My clamp bypass (`--members 1600`, a one-character CLI edit) turns the extrapolated break-even into a measurement: 1,502 bodies → gather p50 14.35 ms, p99 17.0, frame p50 23.5 ms, rtf median 0.03. Cost to adopt: board text only. Gain: naming, not yet a moved bottleneck — the fix (cull/incremental gather) is designed, not built.

## Reproduction

Clean tree, `git apply work/patch.diff`, `CARGO_TARGET_DIR=~/lab-target-2 cargo build --release -p xtask`, then the dossier's commands (load 2.5–3.3, i.e. the author's "under load" condition):

| case | dossier | mine | verdict |
|---|---|---|---|
| m400 rtf100 gather p50 | 3.18 ms | 3.33 / 3.27 ms (two runs) | ✓ shared-runner noise |
| m400 engine p50 | 0.88 ms | 1.07 / 1.00 ms | ✓ |
| µs/readout | 10.4 | 10.74 (272 readouts) | ✓ |
| readouts/body | 0.67 | 0.67 | ✓ |
| digest m400 | `06b78c67…` | identical, paced and unpaced | ✓ |
| kick-bench median/p99 | 43 / 77 µs | 48 / 67 µs | ✓ |
| unpatched m4 digest | `4366e41e…` | identical; no `gather_profile_last` key unpatched | ✓ patch is instrumentation only |

Every table row in the dossier matches its stored JSON (I re-derived µs/readout = `bodies_ns/readouts` and readouts/body for all six rows). The 4× idle-vs-loaded swing is present in the stored artifacts themselves: first run of the session, paced, idle: gather 3.31 ms at 70 bodies; later same-digest (`89417b00…`) runs: 0.71–0.81 ms. My paced-vs-unpaced pair under load: 3.27 vs 3.25 ms, same digest — the swing is idle-specific, as claimed.

## Predictions

`predictions.md` mtime 22:23:15; both held-out runs started after it (finishing 22:23:34 and 22:23:46, each 12 s — started ≥ 22:23:22). Order holds. Outcomes: atom 11.2/9.6 µs in the 9–13 band ✓; idle-observer gather share 0.711 > 0.5 ✓; overflow 94/720 = 13 % ≥ 10 % with zero hitches ✓; readouts/body 0.54 vs the 0.8–1.3 band — the one miss, reported as a miss in the dossier. Honest.

## Adversarial cases (mine)

1. **Fresh seed 42, m400 rtf100:** atom 10.77 µs, readouts/body 0.63, gather share 57 %, engine p50 0.30 ms. Holds on an unseen seed.
2. **rtf 500, m400:** the engine saturates its 5 ms budget (p50 5.01 ms, share 46.7 % > gather 44.8 %) yet still throws zero hitches above 16.7 ms, while the gather has no valve at all. The structural claim (budgeted engine vs unbudgeted view) survives; the flat claim "the engine is not the frame's constraint" is only true in the measured rtf ≤ 100 band — the dossier scopes this but never probes beyond it.
3. **Clamp bypassed (`clamp(4,400)` → `clamp(4,4000)`, scratch edit, reverted): 1,502 bodies:** gather p50 14.35 ms, p99 16.96, max 20.3; atom 10.92 µs, readouts/body 0.76 (both inside the measured bands — the linear law holds to 3.7× the largest run); frame p50 23.5 ms; hitches above 16.7 ms ≈ 1.4×10⁵/hour; rtf median collapses to 0.029. The "~1,600 live bodies eats the frame" headline is confirmed by run, not just extrapolation.

## Novelty

Partially anticipated. H0210's limitations already say "the view gather is 83% of a light frame", and its Next was the gather cache, built in H0211 and made relativistic in H0212 (both cited by the author only as working). representation.md already plans r6 ("Newton iterations and samples per frame for the gather") and the scale answer ("aggregates are one sample each, and the screen caps the work at about one sample per pixel"). What is genuinely new: the post-cache residual quantified (the cache already wins the search — ~1 readout per live emitter — so the atom is the readout itself, ~10.5 µs, seed- and scale-stable), the scaling law with break-even, the per-part decomposition (bodies loop is the gather; player 23–50 µs; fleets 4–50 µs), the foundation-7 violation framing, and the idle-DVFS timing trap.

## Goal fit

Strong. PRINCIPLES 3: "Nothing is evolved that can be derived when looked at (clocks, redshift, views)" — the view currently re-derives every emitter every frame. plane.md foundation 7: "Nothing takes an unbounded synchronous claim on the frame" — measured violated at ≥ 1,500 bodies. The board's focus list indeed names no view item.

## Why silver, not gold

Reproduced, honest, and my adversarial cases strengthened it — but nothing moved yet: no lever built, no component deleted, no 10× delivered. The dominance fact was already in H0210 and had already cost two merges (the cache); the design already contains the intended fix. Gold bar asks for a bottleneck moved, a deletion, or a premise killed *adoptable in one step*; this run measures and names.

**The one experiment:** build the smallest lever — doll-level culling or incremental re-derivation of emitters whose crossing/image cannot have changed — and show the gather share collapse at m400/m1600 on this same bench, with the emitted view provably unchanged where physics requires it (the 5 October memo lesson applied to the view). That is a one-step, gate-able run.

## What the author missed

- **H0210 uncited.** The novelty section positions against the board but not against the HISTORY entry that already recorded gather dominance and commissioned the cache; a checker reading only the dossier would think the dominance itself is the discovery.
- **The headline was runnable.** The `--members` clamp is a one-character CLI edit (`mod.rs:32`); the 1,600-body break-even took me ~50 s of build+run to measure. An extrapolation was left where a run was cheap.
- **Band edges flatter the claim.** Measured gather share spans 53–76 % (stated 56–78 %; no artifact shows 78); engine share is tail-weighted, reaching 32–33 % at m400 (stated 4–22 %, a p50-flavoured number). Substance survives — gather > engine everywhere at rtf ≤ 100 — but the stated bands are wrong at both edges.
- **The rtf > 100 regime is unprobed** (see case 2): the engine's valve is what makes the asymmetry structural; showing the saturation boundary would have made the argument tighter.
- **The DVFS mechanism is inferred,** not isolated: the inflated run was also the session's first run (cold caches confound). The swing's magnitude is measured; its cause is a label.
- The gather's *correctness* (aberration, shift, retardation) is taken as given — self-flagged under "The lens", and it is the exact risk the gold experiment above must gate.
