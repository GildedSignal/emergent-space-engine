# Dossier — the kick scheduler at belt scale: rhythm, smooth function, or certificate?

## Claim

At belt scale the kick cadence must be a function of the perturbation's local strength, not a standing rhythm: a fixed per-body cadence either wastes 8–10× kicks in the quiet belt or catastrophically diverges at deep conjunctions, while both state-function schedules tested — the motion law v2's smooth f′(U_P) and a certificate window (kicks only inside conjunction windows) — hold the behaviours; the window is the cheaper form (5.8–9 kicks/orbit) and f′ the more accurate one; a sparse-impulse secular carrier (few coarse kicks per orbit outside windows) explodes. The per-body cadence rule (q-cadence), the encounter skin (b-encounter-skin) and the secular carrier (q-secular/R2) are therefore one design decision — "what sets Δs" — not three builds, and the answer is: kicks are events, not a rhythm.

## Bottleneck

Board item 1 ("fewer kicks per orbit … kicks dominate the engine's cost") plus item 6 (candidate work must track real encounters). Three queued builds (q-cadence, b-encounter-skin, q-secular) attack the same cost from three sides; this run measures the ladder that decides their union. Expected gain if adopted: the standing cadence's 64–128 kicks/orbit becomes 6–9 kicks/orbit plus ~15 cheap position checks per orbit for belt-class bodies — order 10× on the engine's dominant cost, consistent with the slack skin's 12.6× (components-4643), here shown to hold without any slack gamble (the sound variant: zero kicks outside windows).

## Evidence

Float replica of the plane's own split (exact Kepler drift = the tube, kicks = planet direct + indirect term), restricted circular 3-body, μ = 0.01, a_P = 4, 6 phase seeds, truth = fixed dt at 1024 (belt) / 512 (hard) kicks per orbit, truth's own convergence checked against a 2× coarser truth (Δϖ agrees to 1.3–7.1×10⁻⁴ rad ≪ the compared errors). Bars: Δϖ error vs truth < 10% of truth's drift, final |Δe| < 0.01, survival. Commands, each ≤ 60 s wall except the belt run (Linux x86, orders of magnitude only):

```
cd lab/results/20261007-1550-system-9205/work
python3 belt_cadence.py belt   # 258 s: 3 belt scenes (a=2.35 off-res, 2.52 exact 2:1, 2.44 detuned), e0=0.05, R_w=1.9, 120 orbits
python3 belt_cadence.py hard   # 23 s: deep conjunctions, a=3.4 (d_min≈0.6), e0=0.15, R_w=1.2, 60 orbits
```
Output: `belt_cadence.json`, `belt_cadence_hard.json` (kicks and checks are per body orbit, medians over seeds).

**Belt scenes (weak conjunctions, d_min ≈ 1.5)** — every cadence survives; accuracy ladder (Δϖ rel. error → kicks/orbit): fixed-8 1.6%→8, fixed-16 0.76%→16, fixed-32 0.37%→32, fixed-64 0.18%→64, adapt-16 (v2's f′) 0.06%→133–163, **win-64 0.5–0.6%→5.7–7.3** (+15–16 position-only checks). Same ordering at all three resonance distances (2.35, 2.44, 2.52 — the exact 2:1 differs in no measurable way at this μ and run length).

**Hard scene (deep conjunctions, d_min ≈ 0.6)** — fixed-8/16/32 **diverge (ejection, seeds lost)**; survivors: fixed-64 0.34%→64, adapt-16 0.32%→30.5, adapt-8 1.1%→15.1, **win-64 0.71%→9.0** (+14 checks), win-128 0.73%→18 (window-limited: doubling inside cadence does not help).

**Sparse carrier (winsec, 1 or 4 coarse kicks/orbit outside windows): diverges at every scene (Cworst ≈ 8.4, seeds ejected; NaN rows in the JSON are those seeds).** The impulse error of a kick applied at dt ≈ P/4 with μ = 0.01 is O(μ·dt·n) per kick — the split needs the kick spacing to resolve the body's own orbit, whatever the perturbation's timescale.

Known instrument defects, reported as such: (1) the Jacobi formula in the replica is wrong (constant 0.26–0.36 for all cadences including converged truths) — survival and (e, ϖ) bars only; (2) the e-pump metric is degenerate in the belt scenes (secular e-amplitude ≪ 0.01, matched by everything); (3) `pump_ok`/`de_ok` count only non-diverged seeds.

## Predictions

`predictions.md` was written before the decisive run. What happened:

- P1 (fixed-16 passes off resonance, 8 fails): **half wrong** — 8 also passes; my belt scene is weaker than the runs the q-cadence lens cites (their μ and α differ). Bars were too loose here; the hard scene supplies the discriminating case.
- P2 (window-only fails off resonance, the DC field binds): **wrong, informatively.** Windows alone carry the secular exchange at these scales (0.5–0.6% Δϖ): the precession integral is dominated by the windowed kicks near conjunction. The expectation inherited from q-secular-v2's kill ("the averaging binds") does not extend to windows.
- P3 (adaptive f′ at ≤25% of fixed-64's kicks): **wrong on cost** — f′ pays 2–2.5× fixed-64 in the belt scene for 3× accuracy; it is the accuracy leader, not the cheap form.
- P4 (window + sparse outside carrier is the cheapest passer): **wrong** — sparse impulses diverge everywhere; the only sound outside-window states are zero kicks (windows) or the smooth f′.
- Held out and untested: the resonant-locking case (libration, e-pump) — my run length (60–120 orbits) cannot resolve it; named below as the case that can break the claim.

## What would make it wrong

1. **Resonant locking.** Near a first-order resonance with librating angle the exchange is phase-continuous; a window that opens only at conjunctions may mis-time the resonant phase feedback (r4 v2's over-pump). Needs the B17-style long run (10³+ periods) I did not have time for.
2. **The window switch itself.** v2's own diagnosis (memo §1.2) is that state-dependent switching of the conserved shadow quantity compounds; my window is a switch, and with the Jacobi instrument broken I could not measure its per-crossing jump. The ϖ/e bars hold over 60–120 orbits — B12's exponent question is open.
3. **Multi-planet coverage.** With several planets the windows can merge into near-continuous coverage (skin cost → Σ window fractions); at α → 1 (close-in planet) windows degenerate to a standing cadence. The win shrinks toward the smooth f′'s advantage.
4. Scene coverage: one μ, one a_P, circular planet, coplanar, e0 ≤ 0.15, 6 seeds, ≤ 120 orbits. Orders of magnitude, float replica, not the integer law.

## Cost of adoption, and fit with PRINCIPLES

Adoption is into the design of q-cadence / b-encounter-skin (one build, not three): the per-body Δs becomes "the certificate window's inside-cadence"; between windows the tube alone is read; the window's position-only checks (~15/orbit, no force evals) ride the encounter tier that r8 v3 already pays. Cost: the window-open predicate must be exact in integers and decided only at a body's events (the q-cadence lens's own rule), and the switch-jump must be measured before B12 is trusted on it.

- Principle 14 ("no work for no reason, so no ticks … you don't advance a ship tick by tick"): the standing cadence is a tick; the measurement says the quiet belt pays it for nothing.
- Principle 19 ("a fix signals the wrong representation"): six runs killed cheaper-kick fixes inside the rhythm; the rhythm itself was the wrong representation.
- Principle 33 ("each scale resolves only what matters at that scale"): the window is exactly "the raindrop matters to the ant".
- Principles 3 and 9: the divergent fixed cadences and the exploding sparse carrier are configurations killed, not the method.

## The lens

What the whole-system lens may have missed: elegant unifications hide a hard special case — here, resonant locking (above), which no run of mine exercised. I also did not test the view/encounter readout's cost under windowed schedules (the readout reads the partial state; between windows the tube is exact, so readouts should be free — asserted, not measured). The audit finding offered to the integrator alongside the measurement: three queued builds (q-cadence, b-encounter-skin, q-secular) are one decision point; running them as three optimisations of one rhythm would re-learn this run's kill list three times.
