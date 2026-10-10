# Dossier — 20261010-1152-dynamics-ad35 (dynamics lens)

**Claim.** In the non-resonant circular-tide regime the kick layer has no cadence
bifurcation at all: its error is a systematic frequency offset obeying
rho ≈ 0.5·n^−2.1 that is independent of the tide strength (mu varied 100×,
R/a 4.0 vs 5.27) — so cadence is a certifiable precision knob (n = 4–8 already
gives rho 0.6–3%, far inside the 10% gates), not a stability threshold to hunt;
behaviour corrupts only at n = 2, and no chaos exists for the map to inherit or
inject (twin control). Seed-to-seed rho spreads 10–100×, which explains the
earlier runs' 4–16–64 disagreement as single-seed tuning noise.

**Bottleneck.** The board's #1 focus: kicks dominate engine cost; `q-cadence` is
queued and the prior runs disagree on the needed cadence (8, 16, 64 per orbit).
If rho(n) is a law with no threshold, the plane's fixed cadence can drop to
n = 4–8 wherever the tide is circular and off-resonance — 8–16× fewer kicks at
equal behaviour (kicks are the engine's dominant cost). Nothing is deleted; one
search is (the hunt for a per-body stability threshold inside this regime).

**Evidence.** All in this folder; scripts `work/sweep.py`, `work/analyze.py`.

- Model = the law's own form (docs/law.md "Perturbed motion"): exact Kepler
  drift (universal variables, round-trip error 1e-16, control) + tidal kicks of
  a circular outer perturber, DKD split, cadence n per radial period. Truth:
  DOP853 rtol 1e-12 (Jacobi constant conserved to 5e-11 over 150 orbits,
  control). 6 seeds, inner e0 = 0.1, planar. Circular restricted 3BP.
- Decisive grid (`work/decisive.json`, wall 898 s; command:
  `python3 sweep.py scan 5.27 0.002,0.005,0.02,0.05,0.1,0.2 2,4,8,16,32,64,128 150 6 decisive.json`):
  - rho (relative precession-rate error vs truth, median over seeds):
    n=4: 0.018–0.051, n=8: 0.0045–0.0078, n=16: 0.0011–0.0018, n=32:
    0.0003–0.0005, n=128: <2e-4 — across mu = 0.002…0.2 (eps 1.4e-5…1.4e-3).
    Fit: rho = 0.50·n^−2.11; spread across the 100× mu range at fixed n: 1.7–2.8×.
  - Eccentricity-vector error amplitude: dz_end ∝ mu^1.11 · n^−2.0
    (exponents 2.02/2.02/2.01/2.08/2.00/1.98 per mu over n ≥ 8).
  - Jacobi-constant error: bounded attractor everywhere (log-log slope −0.11…+0.13
    at all 42 configs), amplitude ∝ mu·n^−2. No invariant walk at any cadence.
  - Chaos: map-twin end separation 2.2–2.8e-9 equals truth-twin 1.9–2.4e-9
    (ratio 0.9–1.2) at every (mu, n): the separation is neutral Kepler shear,
    identical in truth and map. The map adds no chaos; there is none to inherit
    at these eps. (The probe's apparent lambda ~0.013/orbit was shear
    misread as exponential.)
  - Negative control: n = 2 corrupts behaviour (mu=0.2: e-error 2.7e-2, i.e.
    e pumped by 27% of itself; rho 0.49). n = 4 is the floor of the safe regime.
- Held-out (`work/heldout-mu.json`, `work/heldout-R.json`, walls 117 s / 97 s):
  mu=0.035: rho(n=32) = 2e-4, rho(n=16) = 1e-3 — the n^−2.1 law holds within
  2×. mu=0.02 at R=4.0 (eps ×2.28): rho(n=16) = 1.0e-3 vs 1.1e-3 at R=5.27 —
  rho is also R-independent; the certificate needs only n.
- Seed spread (P4): rho max/min at n=4 is 10–100× (mu=0.035: 5e-4…4.8e-2).
- Machine: loadavg 1.85, 13.6 GB available (full state in the JSONs);
  Linux/x86 cloud, orders of magnitude only.

**Predictions** (`predictions.md`, written after tuning on one config): P1's
mu^1 law and its borders (n* up to 64) **died** — rho is mu^0; the corrected
n^−2.1 law held on both held-out cases. P2 (diffusion border at strong tide)
**died** — no cadence bifurcation exists. P3's chaos premise **died** (no
chaos; twin equality held). P5 (eps ×2.28 scaling) **died** — rho is
R-independent. P4 (seed spread ≥3×) **held** (10–100×). P6: negative control
held; the positive threshold missed by 2.5× (dz_end 2.5e-8 vs predicted ≤1e-8).

**What would make it wrong.** A resonant or eccentric tide (the earlier runs'
wall: `20261003-0520-dynamics-a9c2` — no rate up to 64 matches a librating
truth inside a resonance band), a hot inner eccentricity, a horizon ≫ 150
orbits, or the integer law's quantization coupling into the kick cadence. All
four are outside the tested domain; the certificate claims nothing there.
**Cost of adoption:** a line in the kick section (cadence from rho spec, n ≥ 4,
domain = circular off-resonance tides) plus the q-cadence rung testing it on
the plane's mixed scenes; no code. **Fit with PRINCIPLES:** "steps are there to
solve a problem of how much error we are ok with… we want them consistent
across the different types of simplifications" (bottleneck 0) — one law for
every body in the domain; "the simulation tells us what's next not us" — the
error, not a scheduler, sets the cadence; rough first (floats exploring,
certificate to be frozen in the rung). **Led, not gold:** the domain is one
regime of one model; the 10× gain is an inference from the plane's assumed
cadence, not measured on the plane.

**The lens.** The attractor view found the bounded Jacobi attractor and killed
the bifurcation hunt, but the error-shape exponent gamma (0.56…1.34 across mu)
proved horizon- and seed-fragile (mu-scan at 100 orbits/4 seeds reads 0.85–0.87
flat where the decisive run reads 0.51–1.35): a warning that gamma from a
single window is not a regime signal at these eps. The lens also nearly
mistook Kepler shear for chaos — the twin control (map twin vs truth twin)
is what separated them, and it should be standard in every stability probe.
