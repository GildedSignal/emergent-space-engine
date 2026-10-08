# Dossier: H_live — the belt's live information is bounded and mostly free

## Claim (one sentence)

In the plane's belt, live distinguishing information saturates rather than accumulates: a static birth program scars every body (measured: 100% by 7.6 kyr), but the ensemble's evolution is programmatic (proper-a chaos is 12.5%, concentrated at resonances, flat in time) and a re-programmed synthetic belt evolves statistically indistinguishably from the true one — so 10⁹ belts fit in 8 GB if (and only if) either the program carries the secular drift or unobserved bodies are legally re-programmed; the player's channel, not the belt, dominates H_live.

## Bottleneck

Board risk "Distinctions created per game-second (H_live) … not measured yet" (HANDOFF; plane.md "Measured on the whole"). Decides whether 10⁹ bodies fit in 8 GB. Gain: deletes the naive-tube memory plan (16 GB, fails) in favour of a program+scars plan measured at ~2 GB worst case, ~tens of MB with re-programming — the difference between the goal being reachable and not.

## Evidence (machine: Linux x86, 8 vCPU, load 2.0, 13.9 GB free; all runs ≤ 370 s wall, ≤ 100 MB)

Scene: Sun + Jupiter (9.55×10⁻⁴ M☉, a=5.2 AU, e=0.048, exact analytic Kepler), 2,000 massless belt bodies, banded a∈[2.2,3.4], Rayleigh e (σ=0.05), uniform angles (B18b family). Test-particle Wisdom–Holman: exact universal-variable Kepler drift (validated: max |Δa/a| = 0.0 over 1.85 kyr drift-only), Jupiter impulse kicks, dt = P_J/64 = 0.185 yr. T = 71 kyr (5,993 J-orbits).

- **Controls.** Drift-only: |Δa/a| = 0.0 exactly. dt-refinement (P_J/256, equal t): median osculating-|Δa/a| 8.7×10⁻⁴ vs 7.8×10⁻⁴ at P_J/64 — dt-independent, so the osculating-a spread is physical forced oscillation, not quadrature error. This control killed my own pre-registered 10⁻⁴ marker (see Predictions): |Δa/a|>10⁻⁴ is true for 90% of bodies everywhere, resonance-agnostic — it measures the forced oscillation, not chaos. Replacement chaos marker (defined from the A1 half only, before A2/D ran): proper-a drift = |⟨a⟩₍last 18 kyr₎/⟨a⟩₍first 18 kyr₎ − 1| > 10⁻³.
- **P1 (chaos fraction).** 12.5% of bodies drift >10⁻³ (3.6% > 3×10⁻³, 1.0% >10⁻²), concentrated: 48% in the 2:1 band (3.22–3.32 AU), 12% at 3:1, 5.5% at 5:2, 5.7% off-resonance. Rolling 18-kyr windows through the second half: 11.2–12.2%, **flat — saturating, not growing**.
- **P2 (static program scars everyone).** Fraction outside the birth quantum cell in (e cos ϖ, e sin ϖ): 100% from the second snapshot (7.6 kyr) — free-e precession (~10–20 kyr period) moves everyone. The ensemble stays low-dimensional: per-band forced vector |⟨e·e^{iϖ}⟩| grows smoothly 0.001→0.043; refit-Rayleigh KS 0.085 (structured residue) vs birth-Rayleigh KS 0.204 and rising 3× faster.
- **P3 (re-programming legality — decisive).** Synthetic belt built at T/2 from a fitted program (smoothed a-histogram with gap structure, per-band empirical e, uniform angles, fresh ordinals), both evolved T/2→T: KS(a) synth-vs-true 0.0305 against the seed-noise floor 0.0225 (1.4×, threshold 3×); KS(e) 0.038 vs noise 0.0415 (inside noise); scattered bodies (a>4 or e>0.3) 17/19/21 (A/D/B, Poisson σ≈4); chaos fraction 12.5/13.5/12.5%. **The re-programmed belt's observable future is statistically indistinguishable from the true one.**
- **P4 (gap carving): failed as predicted-in-the-boundary.** 3:1 gap depth 0.296→0.299 over 71 kyr: no carving (real timescale ~Myr). Held as an honest miss of the "grows 2×" arm; the claim's boundary is stated below.

Numbers: `metrics.json`; scripts `belt.py`, `mk_synth.py`, `analyze.py`; estimate `fermi-estimate.md`. Reproduce: `python3 belt.py A1 --steps 192000 --seed 1` (174 s), `python3 belt.py A2 --steps 192000 --resume A1-state.npz` (192 s), `python3 belt.py B --steps 384000 --seed 2` (366 s), `python3 mk_synth.py A1-state.npz D-state.npz 99 && python3 belt.py D --steps 192000 --resume D-state.npz` (183 s), `python3 belt.py C --steps 10000 --seed 3 --nojup` (8 s), `python3 analyze.py`.

## Predictions

Written before the decisive A2/D runs (`predictions.md`). P1's threshold arm held (≥3%, resonance-concentrated) after the disclosed reinterpretation of the marker; its 10⁻⁴ marker was my error, caught by my own dt-control and replaced before any final-run data existed. P2 held both arms (≥80% static scars; refit absorbs). P3 held on every metric. P4 failed its growth arm — the timescale, not the method (a failed expectation is not a failed method, H0183); gap carving needs ~Myr runs or a resonant-exact setup.

## What would make it wrong

1. **Mass.** The belt here is massless (restricted problem): pair correlations from mutual encounters — real live information — are absent. A massive belt, fleets, or co-orbital formations (taleb-09b5 gold: concentrated workloads) are not exchangeable; the shuffle's legality there is untested.
2. **Time.** 71 kyr; gap carving, resonant-island stickiness and chaotic-zone growth act on Myr. The flat f_chaos could rise toward the 2:1 band's 48% as the outer belt mixes.
3. **The player.** Singled-out bodies (observed, named, owned) are not exchangeable by construction; the shuffle must exempt them, or "observation never changes outcomes" (standing decision) is violated in spirit.

## Cost of adoption, and fit with PRINCIPLES

- `shipmem`'s program family must carry the secular drift (per-band forced vector + e-residue structure), not just the birth law: a static program scars 100% of bodies — this deletes the "birth program + scars" reading of B18 and replaces it with "drift program + scars".
- The shuffle (re-program of unobserved bodies) is a candidate **law event**: canonical epoch + canonical key, never allocator-driven (schedule-independence, B8), exempting observed bodies. It is the difference between 2 GB and tens of MB at 10⁹.
- PRINCIPLES: "Store the generator, not the generated" (§6) — measured to hold under perturbation, not just at birth. "The memory floor is information-theoretic" (§24): the floor here is f_chaos·(tube entropy) with identity, ~0 with exchangeability. "The player is the only wildcard" (§5): quantitatively — the belt's H_live ≈ 7×10⁻³ bits/game-second (rtf 100) against the player's ~10² bits/s; five orders separate them.

## The lens (what Fermi may have made me miss)

The estimate-first discipline pushed memory to the foreground and left the compute side (events/game-second at 10⁹) as a back-of-envelope; the news/gravity-at-c log (an unbounded-term risk named in the law's §32) was not measured at all. The information-theoretic frame also begged for a strict Kolmogorov measure; the operational one used here (evolution-matching after re-programming) is the player-relevant floor, not the absolute one.
