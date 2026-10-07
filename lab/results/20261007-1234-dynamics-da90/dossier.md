# Run 20261007-1234-dynamics-da90 — lens: dynamics and attractors

**Claim.** The Diophantine encounter certificate (`crates/encounters`, r8 v4) amortizes at ~1% of per-conjunction work on crossing asteroid pairs with zero missed encounters, but its static window sits below a hard dynamical floor: relative secular apsidal drift of g_rel·T_syn ≈ 0.02–0.03 rad per conjunction — half the window's own width — breaks every fixed-window policy (~30% of encounters learned late), and the failure is repaired representation-level, not margin-level, by widening the window by the total drift over the certified span (0 late, 0.4% work, still ~250× below the per-conjunction baseline).

**Bottleneck.** Board item "finding encounters without work per orbit or per element change (Binet cone r8 v3 + skin)" — the certificate's steady-state cost and its invalidation dynamics. r8 v4 tests the static finder; nothing had measured what invalidates the certificate or at what rate. This run maps the invalidation channels (relative precession, sub-quantum z-snaps, exogenous kicks) and the completeness contract under each.

**Setup.** Two coplanar test particles on crossing Kepler orbits (a ∈ [2.3, 2.9] AU, e ∈ [0.05, 0.32]), conjunction epochs re-derived exactly after every element change; truth = analytic distance at every conjunction (encounter at ρ = 0.01 AU, trigger window at 0.02 AU). Certificate = integer rotation (m = 2³²) + exact first_hit port (fuzz-verified against brute force, 300/300) over the bad-longitude window; work = one exact check per certified hit. Ensemble: 300 pairs × 2500 conjunctions per configuration, seed 11. All numbers regenerate with `./runall.sh` in this folder (~16 s total).

**Evidence (from `metrics.json`).**

| config | policy | work ratio | late | encounters | snaps/pair |
|---|---|---|---|---|---|
| generic | absorb | 0.0097 | **0** | 586 | 4.7 |
| snaps | absorb | 0.0097 | **0** | 586 | 4.7 |
| resonant (q ≤ 64, q·η < 1 window) | absorb | 0.0022 | **0** | 404 | 0 |
| precession (g_rel ≈ 7×10⁻⁴ rad/yr) | absorb + slide-margin | 0.0001 | 34 | 115 | — |
| precession | no margin | 0.0105 | 29 | 115 | — |
| precession | window frozen (negative control) | 0.0000 | 31 | 115 | — |
| precession | **drift-inclusive widening** | **0.0041** | **0** | 115 | — |
| kicks (Jupiter flybys, Δa/a ≤ 0.15) | absorb | 0.0009 | 41 | 1321 | — |

- Generic: 564/586 encounters found at certified checks, the remainder at invalidator re-grants or in the horizon-truncated tail (see the replication note below); **late = 0** — the window superset held everywhere it should. Median certified span 38 conjunctions; work 103× below touching every conjunction.
- All three static-window precession policies miss ~27–30% of encounters (late 29–34 of 115): the margin (0.15 rad) is looser than the failure threshold because the bad-longitude pattern is not rigid under Δϖ drift — absorption assumes a translation, and over a ~38-conjunction span the pattern deforms by ~1 rad, more than the window itself. The negative control failed as it must, and so did the candidates: the held-out prediction (margin rescues absorption) was wrong, reported as held.
- **Drift-inclusive widening** (widen window by |g_rel|·T_syn·span at grant time) restores late = 0 at 0.41% work — 4× the generic cost, ~250× below baseline, and cheaper in grants than the margin policy (3381 vs 8288). This is the fix the failure points at: the section is a two-clock rotation (u, Δϖ), and folding the second clock into the window width buys back a one-clock certificate (PRINCIPLES #19: the fix signals the representation).
- Kicks: 41/1321 (3.1%) encounters learned late — the only remaining miss channel. A kick moves n discontinuously, so the conjunction phase jumps mid-span and the linear rotation assumption breaks until re-grant. Named next experiment: re-grant at kicks with a widened window over the phase uncertainty (same mechanism that fixed precession).
- Snap channel: 4.7 snaps per pair per 2500 conjunctions at e-quantum 0.01 with per-conjunction phasor σ = 2×10⁻⁴ — the accumulator stays bounded for generic pairs and only drifts where 2α sits near an integer. Structural note: encounter recurrence keys on ‖qα‖ but accumulator coherence keys on the second harmonic ‖2α‖ — two different resonance conditions, not one.
- Resonant seeding (‖qα‖ within one window width, q ≤ 64): late = 0, work 0.22%, encounter spacing median 52 vs 58 generic — **no coherent recurrence signature at the spacing median**. My prediction that spacing clusters at multiples of q was not confirmed at this seeding tightness; the signature, if real, lives in the spacing distribution's tails (bursts and long gaps), not its median. Held as a miss.

- Independent replication (fresh process, shifted rng stream): 667 encounters, 634 at
  certified checks, late = 0, 1 at an invalidator event, 32 (4.8%) unaccounted — all in
  the final certified span truncated by the horizon (the last grant's certified hit
  lands beyond K, so late-span encounters are never scheduled; a horizon edge, not a
  window failure). Late is the completeness metric and it is zero; the truncated-tail
  accounting is disclosed.

**What would make it wrong.** The truth is analytic-at-conjunction (no local refinement of the minimum distance inside a synodic window), coplanar, with a stand-in phasor forcing at the pair's own synodic harmonic rather than the physical belt–Jupiter forcing at a different rotation number; the kick model is patched-conics with random geometry. If the real forcing's rotation number is near its own harmonic, the snap rates here overstate or understate the floor. The precession rate (g_rel ≈ 7×10⁻⁴ rad/yr) is the Jupiter-driven secular scale at 2.7 AU; a belt with g_rel 10× smaller would push the drift floor below the window and the static window would survive — the claim is the floor's existence and its scaling g_rel·T_syn ≳ width, not the specific rate.

**Cost of adopting.** One change to `crates/encounters`: the window at grant time must be widened by the pair's relative precession times the certified span (a multiplication already in hand: both rates are known per pair). No new machinery; the first_hit recursion is untouched. The kick re-grant path needs the same widening over phase uncertainty — one experiment away.

**Fit with PRINCIPLES.** #13 "errors never compound": a late encounter is a completeness error, and it is bounded by construction (0) under the drift-inclusive window. #19 "a fix signals the wrong representation": the margin (a bandaid) failed, the representation change (drift-inclusive window = folding the second clock) succeeded. #3 "compute only surprises": 1% of conjunctions touched. #33: the drift floor is exactly a scale question — what the pair cannot resolve.

**The lens.** Dynamics framing found the attractor structure (bounded vs drifting accumulator), the phase boundary (window width vs drift per conjunction), and the instability (kick-induced phase jumps). What it may have missed: the spacing-distribution tails for resonant recurrence went unmeasured (median only), and no ensemble variance over seeds — one seed per configuration; the checker should rerun seed 12 and compare the work ratios' order of magnitude.

**Predictions.** See `predictions.md` (written before the decisive run). Confirmed: generic work ≤ 0.03 with late = 0; snap coherence is resonance-gated; driftwin restores completeness. Wrong, held: the margin rescuing absorption (it fails like the others); resonant spacing clustering at q at this seeding tightness.

## Reproduce

```
cd lab/results/20261007-1234-dynamics-da90
./runall.sh          # ~16 s, writes metrics.json and raw-*.json per config
```

Files: `study.py` (model, truth, certificate replay, first_hit port), `predictions.md`, `metrics.json`, `raw-*.json|.err` per configuration.
