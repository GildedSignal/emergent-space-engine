# Dossier — 20261008-1337-fermi-ab86 (Fermi lens)

**Claim.** At 10⁹ belt-like bodies on the 8 GB M1, H_live is not a dynamical risk:
encounter-created distinctions grow only as ½·log₂(play decades) (measured slope
0.499) and re-encode at ≤ 1 MB/game-s, so the binding memory term is the
catalogue-width quantum — the decorrelated-population ceiling is 28–38 bits/body
against the 36 bits/body budget — making H_live a design choice (element quanta,
and which bodies are pinned by observation) rather than a runaway.

**Bottleneck.** HANDOFF's "Distinctions created per game-second (H_live) … decide
whether 10⁹ fit in 8 GB; not measured yet" (board item "fitting 10⁹ in 8 GB",
risk list). Gain: replaces an unmeasured fear with a closed budget — deletes the
imagined need for an entropy meter over the live engine and redirects the queued
`b-h-live` build at two cheap measurements (ceiling at the law's quanta; pin rate
from the view). No 10× compute gain claimed; this is a kill-early result: it kills
the configuration "H_live can grow linearly in steady play" for diffusive belts.

**Evidence** (all numbers from `fermi_budget.py`, reproducible: `python3
lab/results/20261008-1337-fermi-ab86/fermi_budget.py` — 3.4 s, < 1 GB, numpy only;
full output in `run.log`). Belt: 1.8–3.4 AU, N = 10⁹, B18b-shaped (banded p,
Rayleigh e, uniform angles); 2D coplanar, shear-dominated encounters. Machine:
GitHub Actions Linux, 8 vCPU, load 0.96, 9 GB free — no timings claimed, so
machine-independent; the one timing-class input (60 ns/kick) is assumed for the
cross-check only.

*Stock* (4.5 GB of the 8 GB for shipmem → 36 bits/body):
- smooth program 0.126 b/b = 16 MB (gold components-98bc);
- scar stock from encounter diffusion: 2.7 b/b after 1 orbit, 5.6 b/b after
  3×10⁴ orbits — +1.66 b/b per decade of play, i.e. +8 b/b from 1 hour to 10
  years of play;
- ceiling (decorrelated population = program gone, marginal entropy at quanta
  (δa/a, δe, δφ)): (2⁻¹⁰, 2⁻⁸, 2⁻¹⁶) → 33.9 b/b = 4.2 GB; (2⁻¹², 2⁻¹⁰, 2⁻¹⁶) →
  37.9 b/b (over budget); (2⁻⁸, 2⁻⁶, 2⁻¹⁴) → 28.0 b/b (22% headroom). The angle
  quantum alone is 16–19 b/b.

*Rate* (asteroid-like, m = 10¹³ kg): Γ(Δv>q) = 4·n·G·m/q — Ω cancels in the
shear-dominated 2D belt; measured by Monte Carlo at 3.432×10⁻² vs analytic
3.432×10⁻² per body per orbit at q = 10⁻⁶·v_orb. At rtf 10⁶ that is 2.6×10⁵
events/game-s → ≤ 1 MB/s of catalogue writes (60 GB/s available). Macro events
(b < r_H, the m-meso exact-pair regime): 7.1×10⁻³/body/orbit → 7×10⁶ events/orbit
≈ 30 MB of product state per orbit if each costs 34 bits. Ship-mass bodies (1 kt):
Γ is 10⁷× smaller — ships' distinctions come from the player and decisions
(off-plan), not from gravitational diffusion.

*Compute cross-check* of the board's "190 cores at today's rates": reproduced
within one order at matched conditions — 500 steps/orbit at 1 µs gives 47
perf-cores at rtf 5×10⁴ and 190 at rtf 2×10⁵; with H0190's 32 kicks/orbit at
60 ns the load is 3.6 cores even at rtf 10⁶. The headline was a condition
statement, not an error.

**Predictions.** All four held (`predictions.md` written before the run):
P1 within 0.1% (Monte Carlo validates the sampling, not new physics); P2 slope
0.499 vs 0.5 predicted, kill threshold ≥ 0.8; P3 ceiling 28–38 b/b inside the
predicted 20–80; P4 within 4× with the reconciling knob (rtf) named. One
instrument error found and fixed mid-run: the first P3 estimator was a saturated
3-D plug-in returning log₂(NS); replaced by per-dimension histograms with
occupancy ≫ 1 (both versions in git-visible script history of this folder's
patch; only the fixed one is in `run.log`).

**What would make it wrong.** (i) Resonant or repeated-partner encounters: the
Monte Carlo is incoherent Poisson; Kirkwood-type long-lived correlations are not
described by smooth marginals — if they must be stored as individuals rather than
as a resonant-swarm program, the ceiling applies at swarm size. (ii) If the store
must keep body-identity for all bodies regardless of observation (no
exchangeability), the 28–38 b/b ceiling binds immediately and the belt can never
leave program form. (iii) The shear approximation is borderline at the resolvable
cutoff (b* ≈ 2.2 r_H, v_esc ≈ v_rel there), so Γ at fine q could be ~2× off —
an order too small to move any conclusion. **Adoption cost:** near zero — it
constrains `b-h-live` and B18: fix element quanta so the decorrelated ceiling ≤
~28 b/b, and measure pin rate (bodies whose identity↔state correspondence is
causally pinned by observation or event records) instead of building a dynamical
entropy meter. **Fit with PRINCIPLES:** 24 "The memory floor is information …
information theory says so" — this derives the floor's number; 3 "Compute only
surprises. Cost follows change and entropy" — the surprise rate measured tiny;
33 "a body resolves only the influences that are significant at its own scale" —
pinning is scale-local (the view is the instrument). Inference flagged: that
re-assigning exchangeable bodies beyond the light cone of their pinning records
is unobservable is argued, not measured.

**The lens.** Fermi estimates smooth-physics rates from toy models; it cannot see
structure: resonant swarms, collisional debris chains (correlated fragments of
one parent — likely programmable, but untested here), and fleet co-orbital
concentrations (taleb-09b5) all create correlation, and correlation, not
diffusion, is the channel that can grow H_live linearly. The checker should test
one resonant case before adopting the "bounded" half.
