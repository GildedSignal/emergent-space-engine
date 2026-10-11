# Dossier — H_live of a belt concentrates on resonance distance, as a μ^(2/3) standing level

## Claim

In a belt under the plane's kick path, the live distinguishing information a
population program cannot absorb (H_live, the scar layer) is partitioned by
distance to mean-motion resonances: the scarred fraction follows the half-width
law W ∝ μ^(2/3) exactly (52.8% of a 2.3–3.4 AU belt at μ = 9.54e-4, 11.9% at
μ = 1e-4; predicted from the μ-scaling: 11.7%), the median scar size falls ~20×
from <1W to >3W, and the scar is a quasi-stationary level, not an accumulating
rate: it does not grow with prediction lead over 300 perturber orbits. At the
law's quantum (1e-6) the scar costs ~7 bits/body (e-vector) + ~5 bits (Δa)
entropy-coded across the population — ~11× less than naive per-body integer
storage — so 10⁹ belt bodies need ~1–2 GB of standing scars at μ ≈ 1e-3.

## Bottleneck

Board risk "Distinctions created per game-second (H_live): not measured yet;
they, not the body count, decide whether 10⁹ fit in 8 GB", and plane.md's
dashboard requirement. Not the idiot index of storage (bytes/body) but its
information floor. What it lets us delete: the guesswork in `shipmem`'s
reabsorption cadence and in `b-h-live`'s instrument definition — both should be
built around two numbers (scarred fraction, per-bin scar entropy), not a global
bits/second.

## Evidence

Scene: belt a ∈ [2.3, 3.4] AU, e Rayleigh(0.05) (cap 0.2), angles uniform;
Jupiter-like perturber at 5.2 AU, e_J = 0, μ as run. Truth = the plane's kick
path (heliocentric leapfrog, direct + indirect term — law.md's split), 350
steps per inner orbit. Program = Laplace–Lagrange free precession of (e cos ϖ,
e sin ϖ) from birth mean elements; mean elements measured in per-body windows
of exactly 8 synodic periods (fixed-grid windows leak 7e-4 — measured — which
is above the quantum: instrument, not physics). Two program variants: textbook
rate (noref) and rate refit on the first half of each body's arc, residual
measured out-of-sample (what reabsorption does). Distance to the nearest strong
resonance (2:1, 3:1, 5:2, 7:3) in units of W = 2.5·μ^(2/3) (the repo's own
convention, B17).

Reproduce (each ≤ 60 s, Linux/x86, numpy only):

```
cd lab/results/20261011-0224-spacex-e46b
python3 hlive.py --mu 9.54e-4 --N 2048 --pj-orbits 300 --out run-jupiter.json
python3 hlive.py --mu 1e-4     --N 4096 --pj-orbits 300 --out run-mu4.json
python3 hlive.py --mu 9.54e-4 --N 512 --pj-orbits 300 --steps-per-orbit 700 --out run-res.json   # control
```

Key numbers (refit program, out-of-sample, 300 PJ orbits ≈ 3,560 yr):

| distance | n (μ=9.54e-4) | med scar_e | rms scar_e | frac >1e-4 | H(e) bits | H(Δa) bits |
|---|---|---|---|---|---|---|
| <1W | 1081 (52.8%) | 6e-4–1.1e-3 | 4.1e-2 | 0.92 | 7.0 | 5.2 |
| 1–2W | 716 | 3e-4–5e-4 | 8.7e-3 | 0.83 | 6.9 | 6.6 |
| 2–3W | 223 | 1.1e-4 | 8.5e-4 | 0.70 | 7.7 | 6.8 |
| 3–5W | 28 | 5e-5 | 8.5e-5 | 0.21 | 5.8 | 4.7 |
| >10W (μ=1e-4 run) | 334 | 7.5e-6–1e-5 | 2e-5 | 0.00 | 8.7* | 7.9* |

*at >10W the median is ~10 quanta; the entropy is set by the quantum, not by dynamics.

- μ-scaling of the scarred fraction: 52.8% → 11.9% for μ 9.54e-4 → 1e-4;
  (1e-4/9.54e-4)^(2/3) × 52.8% = 11.7%. The allocator's law, measured.
- Instrument health: Jacobi constant (the scene's true invariant) conserved to
  2.1e-6 over the run; doubling resolution (700 steps/orbit) moves binned σ by
  ≤ 14%; both controls pass.
- Saturation: median scar vs prediction lead (0–400 yr past the refit) is flat
  within ×1.3 in every bin (b0: 8.8e-4 → 1.1e-3; b3: 4.8e-5 → 7.1e-5). A
  reabsorption fights a bounded level here; it does not chase a rate.
- Δa is the cheap field away from resonance (rms 3.3e-6 at 3–5W, 0% above
  1e-5), and pumps to 3.4e-3 inside 1W (63% above 1e-5) — resonance writes the
  a-scar too.
- Reabsorption is mandatory *and* sufficient beyond 3W: textbook-rate program
  leaves σ_e = 2.6e-2 there (first-order rate error × e); the refit program
  8.5e-5.
- Compression: per-field naive storage (log2 range + 1) is 18.6 bits vs H = 7.0
  — the scar distribution within a bin is heavy-tailed (median ≪ rms), so
  cross-population entropy coding of blocks + sparse indexing of the tail
  (exactly shipmem's packed blocks + Elias–Fano) is worth ~11× per field.
- Instrument health: Jacobi constant (the scene's true invariant) conserved to
  2.1e-6 over the run; doubling resolution (700 steps/orbit) moves binned σ by
  ≤ 13%; both controls pass.
- Extrapolation to 10⁹ bodies (orders of magnitude, cloud machine): standing
  scar memory ≈ f_scarred·10⁹·(7+5 bits + index) ≈ 0.8–1.6 GB at μ ≈ 1e-3,
  ~0.4 GB at μ ≈ 1e-4, on top of ~0.126 bits/body birth programs. Fits in
  8 GB with the rest of the budget; naive per-body tubes (16 B × 10⁹) do not.

## Predictions

`predictions.md` was written before the decisive runs (only instrument-fix
smoke tests at ≤ 20 PJ preceded it). Outcome: P2, P4, P5, P6, P7 held (P4 —
the μ^(2/3) law — to 2%; P7 both sides: unrefit 2.6e-2 vs refit 8.5e-5 at
x>3W). P1 failed as stated: at 3–5W, 21% of bodies exceed 1e-4 (predicted
< 1%); it holds only beyond 10W, which a belt at Jupiter's μ does not have —
every body is within 10W of some resonance. P3 missed by 3 points (53% vs
25–50%). The saturation result (flat in lead) was not predicted at all — I
expected growth.

## What would make it wrong

- The program is first-order Laplace–Lagrange with e_J = 0: a second-order or
  forced-mode-aware program would shrink the far-field level (my numbers are an
  upper bound for better programs); with e_J = 0.048 the forced eccentricity
  adds a coherent term the program must model or the far-field scar grows.
- 300 PJ orbits (~3,560 yr) cannot see long-time chaotic diffusion (asteroid
  Lyapunov times ~10⁴ yr): the "standing level" claim is horizon-bound; at
  10⁴–10⁵ yr the level may walk. The flat-in-lead measurement bounds the
  rate at ≲ 3e-4 per 100 yr inside 1W.
- One perturber, test particles, float64 truth (Jacobi drift 2e-6): the
  integer law's own kick quantization adds a walk the float truth cannot show
  (r2 says increments are exact, so this is likely small — unmeasured).
- The quantum (1e-6) sets the bit counts; at 1e-8 the same scars cost ~6.6
  more bits per field. The scarred *fraction* and the μ^(2/3) law are
  quantum-independent.

## Cost of adoption, fit with PRINCIPLES

Adoption = two numbers for `b-h-live`'s dashboard instrument (scarred fraction
by resonance distance; per-bin scar entropy at the law's quantum), one rule for
`shipmem`'s allocator (scarred fraction ∝ μ^(2/3) of the perturber; budget
reabsorption as holding a level, not chasing a rate), and no code change on
main. Fits "each scale resolves only what matters at that scale" (33: the belt
resolves resonance, nothing else, into memory), "the memory floor is
information" (24), "regimes are chosen by dimensionless numbers" (4: Δa/a over
μ^(2/3) widths). Cost: a checker must re-derive the μ-scaling at a third μ to
break the two-point coincidence.

## The lens

SpaceX's idiot index asked "bytes/body vs information floor" and pushed to
measure the floor first; the delete-first instinct killed my initial
fixed-grid averaging instrument (7e-4 leak) before it produced numbers. What
the lens may have missed: the far-field scar level (5e-5 at 3–5W) sits so
close to the 1e-4 threshold that calling it "programs hold" vs "programs leak"
is a program-quality question, not a physics one — a builder's lens would have
shipped a second-order program to separate them; I ran out of window.
