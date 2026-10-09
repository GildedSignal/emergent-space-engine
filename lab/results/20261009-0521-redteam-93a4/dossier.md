# Dossier — redteam-93a4: gravity-is-news under kicked sources

- **Claim.** The "gravity is news" tube read (a body pulls toward the source's
  tube, evaluated where the reader's past light cone last saw it and extended
  along the dominant drift) has an energy error that is **second order in the
  source's kicks** (measured 2.9e-7 / 3.4e-9 / 3.2e-11 at kick strength
  μ = 1e-3 / 1e-4 / 1e-5) and **bounded**, while naive retarded gravity
  spirals at the same scene (1.2e-2 in 10 orbits); the premise survives
  in-domain, no acceleration term is needed in tubes, and the comparable-mass
  boundary (where it fails at O(1)) is exactly where the design puts the
  binary doll.
- **Bottleneck.** The foundation Julien froze on 5 October ("gravity must
  travel at c… can't construct layer upon a flawed foundation"); the motion
  law v2 reads U_P through this cursor and `b-news-gravity` is queued. The one
  probe behind the premise (`q-gravity-at-c`) tested **free-falling** sources
  only. In the real law every source is itself being kicked, so the tube a
  reader extrapolates across the light time misses the kicks the source
  received inside the delay. This run measures that error and its type.
  No 10× speed gain is claimed; what moves is risk: the foundation's untested
  edge is now measured, with both-side controls, and it deletes the candidate
  "add the retarded acceleration to tubes" before that build spends a window
  on it.

- **Evidence** (float toy, 4 bodies, G=c=M=1; dominant mass fixed; sources
  S, J (mass μ) near-circular, kicked by each other; reader T massless at
  R radii; truth = instantaneous Newtonian, same Verlet steps in lockstep;
  commands and full output in `work/runs.txt`, each ≤ 30 s, `work/repro.sh`
  regenerates everything):
  - **Free-fall floor (positive control):** with kicks off, tube-now is exact
    for circular free-fall — max|ΔE_T|/E = **2.1e-9 over 30 T-orbits**, the
    sources bit-identical (dS/rS = 0). Independently reproduces
    q-gravity-at-c's "news equals instantaneous to 1e-7" in a fresh harness.
  - **Naive retarded (negative control, must fail):** ΔE_T = 3.0e-3 → 1.2e-2
    → 3.4e-2 at 3/10/30 orbits; the sources' own mutual retarded interaction
    spirals (dS/rS = 2 at 10 orbits). Laplace, reproduced.
  - **Decisive (tube, kicked sources, κ = 0.3, R = 5):** max|ΔE_T| =
    2.9e-7 (3 orbits) → 3.4e-5 (30) → 1.7e-4 (100), i.e. 10–100× below the
    truth's own perturbation exchange (2e-3). **μ-sweep:** 2.88e-7 /
    3.43e-9 / 3.15e-11 at 3 orbits for μ = 1e-3/1e-4/1e-5 — slope 2.0 in μ.
    At μ = 1e-5 the error is **flat** (3.15e-11) for 30 orbits. The drift
    extrapolation carries the aberration cancellation (Carlip 2000) for the
    dominant field; only the kicks' curvature inside the light time survives,
    at second order. Attribution of the growth at μ = 1e-3 to scene chaos,
    not the law: dS/rS grows ×100 per decade at **every** μ (μ-independent
    Lyapunov rate), while the energy error at fixed time scales μ²; and
    dt-halving leaves the 3-orbit value at 2.88e-07 (not the integrator).
  - **Carlip term (tube + ½·(a_total − a_drift)·τ²):** bounded transient at
    4.1e-5, instantaneous error decaying to 6e-7 — **no amplitude gain**.
    Tubes need not carry kick accelerations. (My first version of this variant
    added the total acceleration and double-counted the drift: 2e-3, garbage —
    noted so the checker does not rediscover it as a law failure.)
  - **Strong kicks (μ = 1e-2, R = 10):** max|ΔE| saturates at 1.8e-3
    (non-monotone), 7× below the truth's own oscillation; the scene is
    chaos-dominated at that μ regardless of law.
  - **Solar-like (κ = 0.05, μ = 1e-3):** ≤ 8.3e-9 over 3 T-orbits.
  - **Beyond domain (comparable masses, no dominant drift, straight-line
    tube; scene G):** at κ = 0.1 the binary's own mutual tube read diverges by
    one binary separation within ~11 binary periods (ΔE ~ 2e-2, O(1)); at
    κ = 0.01 the energy error is bounded at 1.0e-3 with trajectories walking.
    The binary doll (EOB) is not optional; this quantifies why.

- **Predictions.** `predictions.md` was frozen before the decisive runs.
  Held: free-fall floor (2.1e-9 vs ≤1e-9 predicted, factor 2), solar-like
  bound, naive control spiral (slower than predicted: 1e-2 at 10 orbits, not
  3), beyond-domain failure, amplitude range of the decisive case. Missed:
  strict boundedness at μ = 1e-3 (it grows, but at the scene's μ-independent
  chaos rate — the μ² law error itself is bounded, flat at μ = 1e-5); the
  Carlip term does **not** buy 10×; E's amplitude is ~10²× C, not 10×
  (scene chaos at μ = 1e-2).

- **What would make it wrong.** The toy's sources are near-circular and the
  tube propagation is exact only for the circle (the real law compiles the
  exact Darwin cycle, which is stronger, so this understates the design);
  eccentric, e ≳ 0.3 kicked sources could behave worse. The dominant mass is
  fixed (infinite m); a live dominant mass exchanges momentum and its own
  news-read adds a channel. Magnitude 1e-2-mass secondaries at κ = 0.3 are
  beyond any scene the gates freeze today. If a run with eccentric kicked
  sources at game compactness shows a μ² error that is secular rather than
  bounded, the premise is killed and the read needs the acceleration term or
  a fixed point. Cost of adoption: zero — this is evidence, not code; it
  constrains `b-news-gravity` (cursor + drift only; no acceleration term;
  binaries must be dolls).
  Fit with PRINCIPLES: it is the measured answer to "gravity must travel at c
  … never construct layer upon a flawed foundation", and it is error **type**
  over error size (principle 13: the law's own error is bounded and second
  order; only chaos — which no law escapes — grows).

- **Ranked attacks on representation.md's premises (lens deliverable).**
  1. **Gravity is news with kicked sources** — attacked here; **survives**
     with the μ² bound and the quantified doll boundary. Rung that should
     catch a failure: **none exists.** No B-gate exercises retarded reads;
     a planted naive-retarded law passes every current gate at solar scale
     (Laplace's spiral is ~1e-12/orbit there — my control only fails at
     compactness κ ≳ 0.05). Proposed criterion, cheap and two-sided: this
     run's scene (κ = 0.3, R = 5, μ = 1e-3, 30 reader orbits, ≤ 30 s), naive
     retarded as the planted law that must fail, free-fall tube as the
     positive control.
  2. **Two-body doll / EOB (ν in the energy map)** — confirmed already by
     r3 v3 (float) and B11 (integer); scene G now measures the *consequence*
     of not having it: O(1) failure within ~11 binary periods at κ = 0.1.
     Rung: r3 exists; adequate.
  3. **Dense order bit-identical to sparse** — r5 is named in law.md but
     **no rung file exists in lab/rungs/**; B8 asserts the property on an
     engine that does not yet have both orders. The one structural gap a
     60 s probe cannot build: the spec's contact law resolves "in the frame
     of one of the two bodies" without a canonical choice rule (by id), which
     bit-identity requires. Letter-level, one line.
  4. **View gathered at the past light cone** — r6 likewise has **no rung
     file**; the readout-cost build is queued. The premise "each visible tube
     crosses the observer's past light cone once" is true in flat spacetime
     for any sub-luminal motion (d/dt of |x_b(t) − x_obs(t₀)| exceeds −c, so
     the crossing equation is strictly monotone) — worth recording as a
     survives-with-proof item; lensing crossings are handled by deflection(b).
  5. **Kicks and cycle derivatives absorbing perturbations** — r4 v1–v3, r9
     and events3/4 killed the first-order layers; the v2 redesign (extended
     phase space, Sundman step) has frozen probes P1–P8 and is in flight.
     Nothing this window could add.
  6. **≈ 0 cost for undisturbed bodies** — the memo artifact and the jet
     re-anchor (df81, one checker) cover the memo side; the un-measured half
     is H_live (distinctions per game-second, `b-h-live` queued).
  Blind spot noted: items 3–6 are evidence-audit findings, not fresh
  falsifiers; the one fresh falsifier here is item 1.

- **The lens.** A premise red-team overweights exotic cases; I ranked by what
  the player meets (compact scenes, binaries) and kept two-side controls on
  the single falsifier I ran. What the lens may have missed: the harness is
  Newtonian — the oracle for the read's error is instantaneous Newtonian
  gravity, not 1PN GR; at κ = 0.3 genuine post-Newtonian terms (which the
  design handles in the drift) are mixed into "truth" at the same order as
  the effects measured, so the μ² bound is a statement about the *read*, not
  about GR fidelity.
