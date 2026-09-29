# Rung canary 20260929-1832-rung-kepler-kill — dossier

**Claim.** Forward Euler at h = T/200 does not keep the e = 0.5 Kepler orbit bound: it unbinds after only **3.48 revolutions** (E ≥ 0 first at t = 77.7 orbit-units, step 15,547), failing B1; the frozen negative stays at |ΔE| = 0 but sweeps 0 revolutions, failing R1. Verdict: **KILL**, exactly as the canary expects, and the rung has teeth on both sides (no VOID: the negative fails).

**Bottleneck.** None directly — this is the canary that calibrates checker lenses before real rungs count.

**Evidence** (cloud container, Linux/x86; orders of magnitude only):

| config | energy_growth_exponent | bound_fraction | steps_per_orbit | orbit_closure_count | fails |
|---|---|---|---|---|---|
| euler (candidate) | −0.000292 | **0.007773** | 200 | 3 | B1 |
| frozen (negative) | −3.7e−13 | 1.0 | 200 | 0 | R1 |

Reproduce (1.6 s total, stdlib only): `python3 lab/results/20260929-1832-rung-kepler-kill/kepler.py` — writes `metrics.json` and `picture.svg`. Preview with `python3 lab/verdict.py lab/canaries/kepler-kill.md metrics.json metrics.json` → `Verdict: KILL; killed: euler`.

Diagnostics worth keeping: the spiral opens fast (r > 4 by orbit-unit 3.1) and the body then lingers at large radius, so *time* to unbind (77.7 orbit-units) is much longer than the revolution count (3.48); angular momentum is not conserved and **grows** L: 0.866 → 1.402 (+62%); E plateaus at +0.037 with r_final ≈ 1.7×10⁴.

**Predictions** (`predictions.md`, written before the run). Held: B1 fails (qualitative and mechanism — I derived dE/dstep = h²(r−0.375)/r⁴ > 0, monotone outward drift, ~0.1–0.3 per revolution early on); exponent ≈ 0 because every window sits on the post-escape plateau (measured −0.0003); steps_per_orbit = 200 for both; frozen all-zero with closure 0. Missed: the unbind *time* (predicted 4–15 orbits, measured 77.7) — I conflated time-units with revolutions; the derivation was per-revolution, and huge apoapses stretch time per revolution.

**What would make it wrong.** The exponent criterion E1 is structurally blind here: its windows span the last 90% (t ≥ 1000 orbits), and the drift finished by orbit 77.7, so a flat plateau passes E1 (slope −0.0003 ≤ 0.2) for an integrator that destroyed the orbit in 3.5 revolutions. The kill rides on B1 alone. A future rung grading integrators that survive long runs needs windows that cover the early drift. Also orbit_closure_count is a weak tooth for precessing-but-bound cases (it passed with 3). Cost of adopting: none — nothing to adopt; a configuration dies. Fit with PRINCIPLES: "A failed experiment kills that configuration, never the method" (#9); the frozen arm is the control that fails, per "a test that cannot fail is a control"; forward Euler's outward spiral is the canonical compounding error (#13, "divergence is not a joke and it compounds").

**The lens.** Directed rung, single frozen case: no seeds, steps or tolerances varied, so nothing here bounds forward Euler at other h — only this point dies. The author could not choose a question; the one genuine surprise the lens allowed (L grows 62%, revolution count ≪ time-orbits) is reported above for whoever writes the next stepping rung.
