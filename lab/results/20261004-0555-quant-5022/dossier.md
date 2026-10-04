# dossier.md — q-correctors (quant lens), run 20261004-0555-quant-5022

**Claim.** The plane's kick cadence (1/64 of the radial period) is already at the uniform cliff: no cadence
reduction and no higher-order split cuts kick events per orbit at equal behaviour in the hierarchical regime —
Yoshida-4 is killed outright (apsidal bias up to 5×), plain coarsening caps at 4× per seed and 1× uniformly —
so bottleneck 1's 10× must come from the averaged/doll path, not from the raw kick layer's cadence.

**Bottleneck.** Board #1: "fewer kicks per orbit at the same behaviour (correctors, higher-order splits):
kicks dominate the engine's cost." Each kick is one event (a rebind, ~29 µs today), so events/orbit is the
machine-independent cost. Expected gain if the premise held: 8–10×. What it deletes if it holds: the rebinding
load directly. Measured: the premise is dead for the raw layer.

**Evidence** (all commands from `lab/results/20261004-0555-quant-5022/`, each run ≤ 6 s on 2 vCPU x86;
cost metric is kick events per orbit — machine-independent):

- `cc -O2 -o cadence cadence.c -lm && ./cadence 0.55 0.05 1e-3 1.0 kdk 64` — faithful float prototype of
  `crates/universe` step.rs+force.rs: exact Kepler drift in mean anomaly, midpoint impulse kick
  (direct+indirect planet term), rebind per kick; SyMBA never engages (hierarchical seeds).
  `rk4.c` verifies the invariant J* = v²/2 − 1/r − μ/|r−r_p| − h_z + μ(r·r_p) to 1e-13 on the raw ODE.
- `./tuning.sh` (T1–T3), `./decisive.sh` (held-out H1–H5, B1; `decisive.jsonl`), `python3 verdict.py` —
  mechanical pass/fail against the gates frozen in `predictions.md` (written first).
- Held-out verdicts, non-resonant judged-in seeds (H1 0.62/e0.30/μ1e-3 near 2:1 detuned, H2 0.48/e0.10/μ3e-4,
  H5 0.55/e0.60/μ1e-3): **kdk-64 PASSES all (apsis within 0.2–5.2% of the 1024-event reference)**; H2 and H5
  pass down to 16 events; H1 fails at 32 (−10.6% apsidal); minimum uniform cadence = 64 → gain 1×.
- **y4 killed**: at 24 events its apsidal rate is off by −8% (T1), −57% (T2), +530% (H1), −43% (H2);
  its J error is also 5–50× plain kdk at equal event count. Negative-weight kicks wreck the secular
  precession — the same phase-content mechanism r4 found for arc-integrated kicks.
- Controls: positive kdk-64 passes everywhere judged-in; negative kdk-4 on B1 fails (e 1.66× reference,
  apsis −47%). Judged out (frozen rule): B1 (resonant, reference pumps e 0.02→0.129), H3 and H4
  (conjunction gaps ≈0.12–0.2 ≈ 1.5–2 Hill radii at μ ≥ 1e-3: ejection inside 2048–4096 orbits at every
  cadence tested, including the 1024-event reference for H4 — the raw layer has no reach there at any cadence;
  the averaged/doll representation must own that regime, consistent with r9).
- **Error type flag (principle 13):** J* drifts linearly (exponent α ≈ 1.0) at *every* cadence tested,
  including 4096 events/orbit (rate ∝ μ·H): the time-dependent midpoint kick is not extended-symplectic.
  A B12-style gate at μ ~ 1e-3 over ≥ 10³ orbits will see ~1e-4–3e-4 of Jacobi walk regardless of cadence.

**Predictions** (`predictions.md`, written before `decisive.sh`): 8 predictions, 4 held (B1 chaotic, no 8×
anywhere, y4 killed, linear J drift), 4 wrong in detail and informatively so: H2 needs 16 not 4 (precession,
not J, binds), H5 passes at 16 not 64 (pericentre fear overblown: steps are in mean anomaly), H3/H4 are
chaotic over the horizon rather than "needs 32/64". The binding behaviour is always apsidal precession and
e-pumping — never the Jacobi error, which alone would have passed every configuration.

**What would make it wrong.** The prototype is 2D, circular planet, massless ship, no SyMBA engagement;
a real secondary's eccentricity or the changeover could bind earlier (then 64 is even more necessary) or,
for tidally-dominated far fields, later. Floats explore; the integer engine should re-measure the two
surviving claims (64 at the uniform cliff; y4's apsidal bias) on its own grid. If a per-body cadence
selector by dimensionless numbers (synodic detuning, gap/Hill) were validated on a population, quiet
regimes could take 4× — never 8–10× uniformly, per this data.

**Cost of adopting.** Nothing to adopt as code (no engine change); the adoption is the *negative*: stop
spending on cadence/higher-order splits for the raw layer (the queue's `q-correctors` premise), and move
bottleneck 1's 10× to the averaged secular path (0.3 events/orbit, H0190) with a certificate for when
averaging is valid. Fit with PRINCIPLES: "a fix signals the wrong representation" (19) — the cliff is the
representation's, not the integrator's; "compute only surprises" (3) — an unperturbed orbit's kicks are not
surprises; "the best part is no part" (17).

**The lens.** Quant missed the physics risk: three of six held-out seeds were not quietly hierarchical
(chaotic ejection), which cost reruns; and the first draft's "J error" metric was a dial holding no
information (missing the indirect potential) — the RK4 control caught it. What the lens bought: cost as
countable events, frozen gates with both-side controls, and the multiple-testing count (13 tuning variants,
disclosed) before any held-out claim.

**Proposed grade: silver.** Real, reproduced, held-out-confirmed negative with a killed half-premise (y4);
one experiment from gold: the per-body dimensionless cadence selector plus the averaged path's own validity
certificate, judged on a frozen population.
