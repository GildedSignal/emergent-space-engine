The design'**Claim:** The design's cost table and its gate ladder both miss the steady resonant band of any belt near a planet — measured at 5.8% of a belt at Jupiter's mass ratio, 28.6% at μ=10⁻², 0% when cold, priced by nothing and gated by nothing — and the 1PN two-body doll is unfenced exactly where it is wrong by 10.2% in periastron advance (p=20M, ν=0.25), an error B11's 1PN oracle is structurally blind to.

Supporting detail, briefly:

- **A1 (belt, measured):** 2-D CR3BP float falsifier, 800 particles, T=1200 planet orbits, a-diffusion classifier calibrated on a μ=10⁻⁶ control. The chaotic fraction runs 0.75% → 2.1% → 5.8% → 28.6% across μ=10⁻⁶…10⁻²; cold belts are clean; drifters pay ~1 exact conjunction per synodic period forever (≈4.9×10⁵ bodies in a 2²³ belt at Jupiter μ). No gate has a belt-with-planet scene (B18-belt is planet-free, B15 has no belt, B17 tests two single resonances). My pre-registered kill threshold (≥15% at Jupiter μ) did **not** fire there — it fires at μ≥10⁻²; reported as held.
- **A2 (binary doll, measured):** the doll's advance vs the true 2PN advance (Damour–Schäfer/Kopeikin eq. 13, parse validated against exact Schwarzschild at ν→0): 10.2% at p=20M, 1% only at p≈267M — five times B11's own tolerance, invisible to its 1PN oracle by construction. Fix: ν/p fence + 2PN A(u).
- Also filed: ungated longitude continuity under kicks (A3), r5 must plant a handoff-inside-dense case (A4), stale Minsky/Binet premise still asserted in representation.md §1 (A6), and one premise that **survives**: the past-light-cone gather's single-crossing monotonicity (dt_ret/dt = 1/(1−n̂·β) > 0).
- Instrument lesson recorded in `run.log`: a two-particle Lyapunov estimator counted Kepler shear as chaos and was replaced mid-run (disclosed).

All files in `lab/results/20261006-0916-redteam-e84d/`: `dossier.md`, `predictions.md`, `belt_chaos.py`, `sweep.jsonl`, `eob_2pn.py`, `kopeikin.pdf`, `run.log`, `author-final.md`.
