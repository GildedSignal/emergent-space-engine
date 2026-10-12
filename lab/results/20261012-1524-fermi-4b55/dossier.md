# Dossier — 20261012-1524-fermi-4b55 (Fermi lens)

**Claim.** At game scale, live distinguishing information is created by rebinds
through secondaries' spheres of influence (and contacts, and the player), not by
mutual encounters — a belt of ship-mass bodies is informationally inert for
~10²⁶ years — so H_live at 10⁹ bodies is bounded at ~5×10³ bits per game-second
(rebinds 36.5/s × 128 bits) and the 8 GB budget is decided by birth programs
plus the *repopulation* machinery, which is load-bearing because scattered
ships never re-smooth on their own.

**Bottleneck.** HANDOFF's named risk "Distinctions created per game-second
(H_live): they, not the body count, decide whether 10⁹ fit in 8 GB; not measured
yet"; board item "fitting 10⁹ in 8 GB … decided by distinctions created per
game-second"; it feeds the queued build `b-h-live`. Gain: the term decomposition
and order-of-magnitude prediction the builder needs (an estimate before
building), and a premise split: the encounter-certification scaling risk
(O(N²) candidate pairs) is a *compute* problem only — on the information side it
is dead at ship masses by 12 orders of magnitude.

## Evidence

Units: the doll's (GM_star = 1, a = 1, v_K = 1, orbit = 2π); physical anchor
a = 3 AU, M_star = 1 M☉ → 1 orbit = 1.64×10⁸ s. Quantum q_v = 10⁻⁵ v_K
(player-differentiation floor, conservative-fine).

**Layered Fermi decomposition (who creates bits):**

| term | rate at 10⁹ (fixed annulus, 10⁵× r8 density) | bits | verdict |
|---|---|---|---|
| mutual encounters, ships 10⁶ kg | δv = 2μ/(ρ·v_rel) ≈ 10⁻¹⁷ v_K per encounter; quantum-crossing time 2.4×10²⁶ yr | 0 | inert |
| mutual encounters, asteroids 10¹³ kg | crossing time 2.4×10¹² yr | 0 | inert |
| mutual encounters, dwarfs 10¹⁸ kg | crossing time ~240 yr (≈47 orbits) | on | regime boundary m_crit ≈ 3×10¹⁸ kg |
| rebinds (SOI transits, planet μ=10⁻³ mid-belt) | see P3 below | 128 bits (a 16-byte tube) | dominant |
| contacts (10 m ships) | 1.1×10⁻³ per game-second, universe-wide | 256 bits | nil |
| player | ~10 decisions/s at canonical ticks | ~10 bits/s | nil |

Every SOI transit is a full rebind by construction: the deflection at the SOI
edge is 0.31 v_K for any quantum coarser than 10⁻⁵ (inside the SOI the planet
dominates — that is its definition).

**Monte Carlo** (`h_live_fermi.py`, then `crosscheck.py` after two bugs were
found; both ~2–3 min, numpy, Linux x86 shared runner, load 0.5–1.4, 8 vCPU):

- **P2 impulse check (held).** Impulse vs exact hyperbolic scattering:
  ratio 1.02 median for deflections < 0.5 rad (predicted 0.7–1.4), 2.58 for
  deflections > 2 rad (predicted ≥ 2). The diffusion layer's formula is sound.
- **P4 masses (held, trivially).** Crossing times above; the critical mass for
  per-encounter scarring is μ_crit = q_v·ρ·σ_e/2 → 3.0×10¹⁸ kg.
- **P5 contacts (held).** 1.1×10⁻³ contacts/game-second at 10⁹ vs the predicted
  bound < 10².
- **P1 encounter rate (FAILED, reported).** My conjunction machinery measures
  medians of 5×10⁻⁶–1.3×10⁻⁴ per body per orbit on r8-v2-style belts
  (N = 5×10³, 20 orbits), against my analytic swept-area estimate 6.8×10⁻³ and
  r8 v2's belt-0 truth 2.1×10⁻³. Dense-scan adjudication below.
- **P3 first version was a harness bug:** the SOI count reused the all-pairs
  machinery, counting belt–belt encounters at threshold R_SOI (54/body/orbit,
  absurd). Corrected to planet-vs-belt only.

**Reproduce:**
```
cd lab/results/20261012-1524-fermi-4b55
python3 h_live_fermi.py      # ~2 min: 8 belts, diffusion, 1e9 table (P3 superseded)
python3 crosscheck.py        # ~2.5 min: dense scan vs machinery, planet-only SOI, P2
```
Numbers land in `h_live_results.json` and `crosscheck_results.json`.

**Final numbers (from `crosscheck_results.json`, the adjudicated run):**

- Dense brute-force scan (hot belt, N = 200, σ_e = 0.05, ρ = 10⁻³, 20 orbits,
  17,771 time steps, 8,000 tracked pairs): **2.03×10⁻² encounters per body per
  orbit**. Epicyclic analytic Γ ≈ 3πΣρA: 4.8×10⁻² — **within 2.4×**. My
  conjunction+Newton machinery scored **0** on the same belt: it evaluates the
  distance at the longitude crossing only, while the true minimum of the 2D
  relative track generally falls elsewhere; both its earlier "window" and
  "Newton" variants share that defect. The machinery is dead; the analytic
  formula stands, within ~2.4× on the adjudicated case (and plausibly ~10× on
  r8's colder belts — belt 0's 2.1×10⁻³ is bracketed by the formula over the
  16 belts' (ρ, σ_e) draws). P1 is therefore reported as: analytic held on the
  dense-scan control; my MC implementations failed and are not evidence.
- **P3 corrected (held): 5.98×10⁻³ SOI transits per body per orbit** (1,197
  transits, 10⁴ bodies, 20 orbits, one planet of μ = 10⁻³ at a_p = 1.25),
  against the predicted 0.01–0.05 — a factor 1.7 below the lower edge.
- **At 10⁹ bodies:** rebinds 36.5/s universe-wide → H_live ≈ 4.7×10³ bits/s
  (590 B/s; 2.1 MB per hour of play). Contacts 1.1×10⁻³/s. Player ~10 bits/s.
  **Total H_live ≈ 5×10³ bits/s.** Birth programs 15.75 MB (components-98bc's
  0.126 bits/body). Singleton saturation without repopulation: 167 orbits ≈ 870
  game-years ≈ 8.7 wall-years at rtf 100 — finite but long; the term that can
  actually approach 8 GB is the mixed-population entropy after repopulation
  (0.126 → up to ~30 bits/body ≈ 3.75 GB at q_v = 10⁻⁵), which is what
  `b-h-live` must measure.



## What would make it wrong

- Belts populated by bodies ≥ 10¹⁸ kg: mutual scarring turns on (regime
  boundary above) and every ρ-scale encounter costs ~3–8 bits.
- A quantum much finer than 10⁻⁵ v_K: crossing times scale as q_v², but rebind
  dominance is q_v-independent below ~0.1 v_K.
- Gameplay that keeps ships inside secondaries' SOIs for long stretches: rebinds
  then track player decisions — still bounded by input, but H_live stops being
  a property of the belt alone.
- The mixed-belt program floor: I bracket it (0.126 bits/body at birth vs up to
  ~log₂ occupied quantum cells ≈ 30 bits/body fully mixed at q_v = 10⁻⁵ →
  3.75 GB at 10⁹) — where a real scattered belt lands is exactly `b-h-live`'s
  measurement.

**Predictions.** See `predictions.md`. P2 held (1.02 / 2.58). P4 held
trivially (2.4×10²⁶ yr at ship mass). P5 held (1.1×10⁻³ vs < 10²). P1's
analytic half held on the dense-scan control (2.4×) while both my Monte-Carlo
variants failed to zero and were withdrawn as evidence — the pre-registered
"if P1 fails, find which term broke" branch fired: the broke term was my
machinery's single-time evaluation per conjunction, not the analytic formula.
P3 held within a factor 1.7 of its lower edge after the harness bug was fixed
(first version wrongly counted belt–belt pairs at R_SOI scale: 54/orbit).
The H_live verdict never rested on P1's normalization: it rests on δv ∝ μ
(twelve orders of margin at ship mass) and on geometry.

**Cost of adoption.** No code changes: this is the estimate that precedes
`b-h-live`. Design consequences it hands over: (1) measure H_live as
quantum-crossing deviations (rebinds, contacts, player decisions) — counting
encounter-certificate events as bits would overstate H_live by ~5 orders;
(2) repopulation (refitting scattered singletons into new population programs,
in idle time) is load-bearing, not an optimization: without it the singleton
store grows linearly to saturation in ~1/Γ_rebind orbits;
(3) the memory budget at 10⁹ is birth programs (16 MB) + rebind accumulation +
the mixed-population entropy (the only term that can approach the budget).

**Fit with PRINCIPLES.** #6 "Store the generator, not the generated …
influences below one quantum accumulate": the accumulation lives in the doll's
field, not in per-ship scars — confirmed quantitatively. #24 "the memory floor
is information": the floor is 0.126 bits/body (measured, components-98bc) plus
mixing entropy, ~5 orders under naive 16-byte tubes. #4/#33: regimes by
dimensionless numbers — μ/μ_crit decides whether a belt is informationally
inert. #22 "the simulation tells us what's next, not us": the term
decomposition came from the physics, not from the certificate machinery's event
counts.

**The lens (what Fermi may have made me miss).** Fermi compresses, and my first
analytic rate (swept area) disagreed with my own machinery by ~2 orders — the
same failure class as the memo artifact: numbers agreeing because they share
assumptions. The dense scan was the control that had to exist. The lens also
brackets rather than measures the mixed-entropic floor, and treats the belt as
2D (inclinations lower density, so mutual rates here are upper bounds).
