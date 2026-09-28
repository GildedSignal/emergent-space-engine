# Premise probe results — GLM run, 28 September 2026 (draft for the integrator)

Float-lab probe, non-canonical, 64-bit floats, orders of magnitude only. Scripts: `glm_k1.py` … `glm_k5.py`, `glm_k6_econ.py` in this directory (pure stdlib Python 3). Frozen criteria: `KILL_CRITERIA.md` (untouched). Build-on: `/private/tmp/glm-scratch/reanchor.py`, `phase.py` (error-feedback sigma re-anchoring reused throughout).

Machine state: MacBook Air M1, load 2.1–7.5 during runs, swap 11.9/13.3 GB, no thermal warnings.

## Verdicts

| Criterion | Measured | Threshold | Verdict |
|---|---|---|---|
| K1 parent formula | 32.5 kicks/orbit | > 1e3 kills | **PASS** (estimate ~30 confirmed) |
| K2 quadrupole averaging + short-period | 0.285 kicks/orbit; cut = 114x vs K1 | cut < 10x kills | **PASS**, but the ~500x claim is not reached (octupole-limited) |
| K3 J2 = 1.0826e-3 in formula | 32.3 kicks/orbit (1.0x K1); as kicks: 3.3e5/orbit | > 10x K1 kills | **PASS** (J2 must live in the formula) |
| K4 handoff carries | beta_E = -0.069, beta_L = +0.062 over 100 handoffs | beta >= 0.8 kills | **PASS** (carries bounded, ≤ 0.07 E-quanta) |
| K5 binary 0.8 | 3.4e7 kicks/orbit | > 1e3 recorded | recorded: binaries need a two-body parent |
| position calls | K1-style 1.2e-2 /s/body (0.6 core per 1M ships at 50 us); K2-style 1.0e-4 /s/body (0.01 core) | — | event-driven cost fits G2.5a |

## Headline side-finding (not a frozen kill)

Between handoffs on a lunar transfer the single-parent Kepler formula takes ~6e5 lattice kicks per handoff (~6.2e7 kicks over the 100-handoff chain, ~3.6e4/day). A lunar-distance leg is not representable as Earth-Kepler + kicks at dv = 0.27 mm/s: averaged tides in the formula, or an earlier two-body handoff, are load-bearing.

## K2 detail

- Formula: Kepler conic + bounded short-period terms of the Moon/Sun quadrupole (identity and SP terms stated in `glm_k2.py`, decomposition self-checked to 8e-22 m/s²).
- Residual = exact tide − quadrupole, measured 0.019 x quadrupole = r/d_Moon = 0.0176: the octupole. It caps the cut at ~1/(r/d) ~ 55x in amplitude; measured 114x in kick rate. The ~500x claim would need octupole averaging too (or a much smaller r/d).
- Secular rates (Moon 1.14e-10 rad/s, Sun 5.2e-11 rad/s) stated and vanishing for the circular equatorial probe orbit.

## K4 detail

- Handoff on the tidal ratio rho = (GM_M/d_m³)/(GM_E/d_e³), 10% hysteresis (rho=1 surface is 72,100 km from the Moon; Hill 61,500 km).
- Vehicle A, one continuous trajectory (best of an offline geometry search, scratch): 46 handoffs in 2,564 d, ends by Earth impact; beta_E = −0.071, beta_L = −0.096.
- Vehicle B, one ship, commanded transfer sequence (10 re-injections at perigee, carries persistent): 100 handoffs in 1,734 d; beta_E = −0.069, beta_L = +0.062; half-step itinerary: −0.21 / +0.03. All |beta| << 0.8.

## Reproduce

`python3 glm_k1.py` (1.8 s), `glm_k2.py` (4.0 s), `glm_k3.py` (0.9 s), `glm_k4.py` (8.9 s), `glm_k5.py` (< 0.1 s), `glm_k6_econ.py` (0.6 s). All < 60 s each on the busy machine above.
