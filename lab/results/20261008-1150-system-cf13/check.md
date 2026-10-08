Grade: silver

**Abstract.** Claim: the encounter finder needs one certificate — in-band phase-rank + cross-band cone, band width from the drift bound, no trigger. I reproduced every number in the run folder bit-identically (all 16 lines: pairs/evals/checks/hits/missed; F1 59.7× evals, 0 missed; BANDS=1 self-destruction margin 712; k-boundary 12→4→0). But one adversarial scene inside the claimed regime breaks it: a convoy (F1's exact a/e, longitudes clustered in 0.1 rad — a fleet on one orbit, the taleb-09b5 motivating case) silently misses 11,736 of 15,497 truth encounters (76%) while the crate's cone misses 0. The rank-count k derives from mean spacing TAU/m and assumes uniform longitude density; clustered populations (convoys, Trojan clouds) violate it by orders of magnitude. Adoptable after the scale is fixed: one named experiment away.

## Reproduction (clean tree, `work/patch.diff` is empty — exp is self-contained)

- Built `exp` with `CARGO_TARGET_DIR=/home/glmlab/lab-target-1`, ran F1/F2/X/B. All counters (pairs, scanned, evals, checks, hits, sections, missed, false, matched) match `f1/f2/x/b.jsonl` exactly; only ms differ (shared machine). Cone misses 0 on all scenes; unified misses 0 on all four declared scenes.
- `BANDS=1 F2` = 4,957 pairs / 439,206 evals / 0 missed — the dossier's "maximal band" row is regenerable (identical to `globalrank`, as one-band-over-everything must be). `BANDS=1 B` = margin 712, self-destructs to all 499,500 in-band pairs, 0 missed, ~3.3 s — the "tier chosen by the drift bound, not a trigger" claim reproduces.
- `K_OVERRIDE=0/1/2` on F1: 98/12/4 missed; adaptive k=4: 0. The boundary is real. (Dossier's "k=1/k=2" labels are the override values; actual rank width is override+1.)
- Truth independence confirmed in `crates/encounters/src/truth.rs`: conservative advancement with Lipschitz/Gronwall step bounds, Halley states vs the method's Newton — no shared solver.

## Predictions

`predictions.md` predates the run (file times and log order consistent). P1–P4, P6 held as reported; P5 honestly falsified in direction (no-band swells in cost rather than missing) — the correction is real, I reproduced the swelling on B (499,500 pairs) and its absence on F2. **Hygiene flaw:** the declared scenes were resized before the run without disclosure — predictions say F1 N=800 σ_e=3e-4, F2 N=1000, X 2×400; the code runs 500/600/2×250, σ_e=1e-3. The direction does not favor the headline (smaller N shrinks the quadratic win; larger σ_e is harder), so this is not tuning, but a pre-registered protocol that silently drifted.

## Attack (my three cases)

1. **CONVOY** (N=500, a∈[1,1+3e-5], e Rayleigh 1e-3, M0 and ω both uniform in [0,0.1], ρ=1e-4, 30 orbits — F1 with clustered phase): truth 15,497 encounters; cone misses 0; **band/globalrank miss 11,736 (76%), with 0 false positives — silent**. Cause: `k_enc = ceil(2.5·2·e_hi/spacing)` uses mean spacing `TAU/m`; the encounter window |Δλ| ≲ 2(e_i+e_j) spans ranks proportional to *local* density, ~63× finer in a convoy. This is inside the claimed regime ("exact on formations, co-orbital swarms"): a convoy is a formation, and real co-orbital populations (Trojan clouds) are clustered and stay clustered.
2. **F1HOT** (σ_e=3e-2): 0 missed, still ~5× cheaper — the eccentric degradation behaves exactly as the author disclosed.
3. **TROJAN** (a-spread 1e-6, uniform longitudes, ρ=3e-4): 0 missed, 38× evals cut — the degenerate-regime win is real where phase is spread.

## Novelty and goal fit

Not in HISTORY.md or docs: taleb-09b5 (board, 6 Oct) established the O(n·k) phase tier with a dimensionless trigger; this run's contributions — the tier as the in-band readout of the crate's own cone, the band width from the certificate horizon, the trigger deleted in favour of the drift bound's self-destruction (measured on B), and the P1 correction that the *crate* misses 0 on formations — are new and measured on the crate's unchanged `pair_events`. It targets the board's top scaling risk (candidate work must track real encounters; components-4643's 92% setup dominance). Fit: PRINCIPLES 19 ("a fix signals the wrong representation") and 32 are served by the unification; but PRINCIPLES 2/"exact means deterministic and reproducible" and r8's frozen contract ("every candidate finds every encounter") are violated by the convoy case as shipped.

## The one experiment to gold

Replace the rank-count scale with a sound one — an **angular** window (|Δλ| ≤ c·2·e_hi + drift margin, materialized by range search over the sorted longitudes, cost = window × local density; equivalently bound k by max local spacing) — then re-run all four scenes plus CONVOY and a clustered Trojan cloud (0 missed required), and judge under kicks with r8 v4's case (d) as the author already proposes. The unification's shape, the drift-bound tier selection and the cost numbers all survive; only the in-band scale is wrong.

## What the author missed

- Phase clustering. All four samplers draw mean longitude uniform over TAU; the derivation then quietly assumes it. The lens section lists eccentric swarms, kicks, resonance, GR — everything except the density of the phase distribution itself, in the regime (formations) the certificate exists for. The miss is silent (0 false positives), the worst failure mode for a candidate tier.
- The undisclosed scene resizing between predictions.md and the run.
- Small gaps: the negative control's "k=138 of 500" (X) is not regenerable from the shipped binary (globalrank prints no k/margin); hits exceed matched by 1/7 on F2/X (duplicate conjunction events) — benign but unexplained.
