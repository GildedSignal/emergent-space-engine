# predictions.md (written before the probes below were run)

Probes test the two engine-facing lessons of this library-lens run.

**Probe A — fit-cadence (JPL practice: fitted generator + certificate, event = certificate break).**
Perturbation: quadrupole tide from a binary companion on a test particle (e = 0, 0.3, 0.7).
Degree-10 Chebyshev fit per window; physics evaluations = (d+1) per fit; error measured on a dense grid.

- A1. At e = 0.3, fitting in mean anomaly (uniform-in-M) holds max relative error < 1e-6 with **at most 3 windows/orbit** ⇒ ≤ 33 evals/orbit, comparable to H0190's 32 kicks/orbit but with a per-window certificate.
- A2. Uniform-in-time fits at e = 0.7 need **≥ 3× more windows** than uniform-in-M (pericenter compresses the signal in t); uniform-in-M stays within 1.5× of its e = 0.3 window count.
- A3. Circular e = 0: time and M fits identical, ≤ 2 windows/orbit.
- A4 (held-out, untuned): stronger tide (companion at a/d = 0.02 vs 0.05) adds harmonics; window count grows by **≤ 2×**, not by an order of magnitude.
- A5 (held-out): the cheap certificate (last-Chebyshev-coefficient ratio) tracks the true max error **within one decade** (never under-estimates by more than 2×).

**Probe B — conjunction scheduling from elements (beat/CF practice).**
Two eccentric orbits; conjunction = equal true longitude. Brute force on a dense grid is the reference.

- B1. Conjunction *times* are predicted from the beat period of the mean motions to better than 1% of the beat, at one arithmetic op per prediction, zero per-step work (circular case: exact).
- B2 (held-out): the miss-distance sequence δ_k at successive conjunctions is quasi-periodic for e ≤ 0.3; a 2-frequency fit on the first half predicts the second half to **< 10% of δ's amplitude**.
- B3 (held-out): at e = 0.7 the 2-frequency prediction degrades to **> 20%** — the regime where Diophantic prediction alone must hand off to the two-body doll (expected failure, reported as such).
- B4. Near-commensurate pair (7:6 detuned by 1e-3): beat is long but the method still predicts conjunctions exactly; at exact commensurability the beat degenerates (already known from r4 v2 — control, expected VOID-ish).
