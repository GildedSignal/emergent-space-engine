# Dossier — 20261011-1729-scout-6765 (lens: scout): the galaxy doll

**Machine:** GitHub Actions linux, 8 vCPU, 13.6 GB free at start, loadavg 1.55→1.58
(shared, quiet), every process < 50 MB. **Wall:** the decisive run is 0.5 s
(`python3 galaxy_doll.py full`, writes `galaxy-out.json`; log `galaxy-log.txt`;
tuning history in this text). Cloud x86: timings are order-of-magnitude only.

## Claim

The galaxy doll is the plane's own compiled-cycle law one level up and, at every
playable scale, mostly a **frozen program**: in 2D the smooth galactic field has
exactly the integrable (E, L) rosette structure the compiler already owns —
measured, held-out: relative error ≤ 1e-6 at ≤ 16 four-point panels on every
case, per-cycle error 4.1e-12 rad identical every cycle (2.4e7-cycle re-key
interval at a 1e-4 rad floor), β∞ = 0.9 scatter transits agreeing with an
independent leapfrog to 5e-10 rad — while the disc itself never turns (5e-3
orbits per 100-h session even at rtf 1e8) and GR is deleted above the hole's
doll because the GR precession seam lies **inside** the nucleus's Newtonian
sphere of influence at every horizon (5e-4 to 0.13 of r_SOI, Sgr A*-like, Θ =
1e-3 rad). No new component: the same tubes, kicks and news, one scale up.

## Bottleneck

HANDOFF "Headed next" #5's last item, "the galaxy doll" — the only item on that
list with no run (surveyed every `claude/lab-*` branch since 6 October: B12, the
law-v2 finishers, Kerr, Fermi 2, inspiral and the scale items all have owners).
The goal's namesake scale ("billions of entities across a galaxy like it's
nothing"). **Gain:** a deletion plus a boundary rule. It deletes any N-body or
dense-order fallback for the disc (the smooth field is a compiled program;
bodies are tubes on it; the disc never completes an orbit at any playable rtf),
fixes the nucleus doll's outer edge (the SOI provably covers GR), and defines
what actually computes at galactic scale: the player's coast, the news cone,
the nucleus. Not a speedup of the plane — a statement of what the galaxy is.

## Requirements (numbers, tied to PRINCIPLES)

- Billions of bodies, every body real, never averaged (B18b, gold
  components-98bc: a smooth belt is a bijective program at 0.126 bits/body).
  The galaxy doll is that program's frame. Principle: "NO ELITE style".
- Zero work per orbit in the smooth field (B9's tail; principle 3, "Compute
  only surprises").
- Error type over size (principle 2/13): cycle errors identical every cycle,
  linear accumulation, re-key on a derived interval — the r2/B5 discipline.
- Cost class: the plane's kick path is compile-dominated (~140 quadrature
  panels per kick, quant-ba35 / autoresearch-bb4d); a galactic cycle compile
  must land in the same class.
- The 0.9c stream (B15's scene) and the high-c player (the goal: "lets the
  player feel what living at high c would feel like"): unpowered coasts are
  scatter orbits through the program field.
- Each test ≤ 60 s, < 2 GB (this falsifier: 0.5 s, < 50 MB).

## The candidate, and the ranking (scout's search)

**Adopted: (E, L) rosette cycles in the smooth axisymmetric program field.**
In 2D, rotation symmetry + energy make the smooth field exactly integrable
(L is conserved; every bound orbit is a rosette on one annulus; scatter orbits
have one turning point or none — plunge classification is the same root-count
integer decision as the plane's radial cubic). The turning-point ψ-substitution
panel quadrature (law.md §Motion, `space-darwin16-v1`) generalizes verbatim
from the Schwarzschild radial function to any monotone Φ(r) held as the disc
program; per-band fixed point, mirror-doubled outbound half, Gauss–Legendre
4-point panels.

- This is the 2D degenerate case of galactic **torus construction**: McGill &
  Binney 1990 (generating-function tori), Sanders & Binney 2014 and the Torus
  Mapper (verified to exist: review Sanders 2016, MNRAS, and the tm package).
  Their per-evaluation cost claims: UNVERIFIED. Their hard problems — 3-DOF
  tori, triaxial chaos (Carpintero et al. report up to two-thirds chaotic
  orbits in cuspy triaxial systems, verified to exist as contrary evidence) —
  **dissolve in 2D axisymmetric**: the smooth field is exactly integrable, so
  "what fraction of orbit space is torus-coverable" is 100% by construction
  (principle 32: the symmetry is found by representation).
- Rejected: **epicyclic / shearing-sheet local frames** (Toomre 1964,
  Goldreich & Lynden-Bell 1965, UNVERIFIED at source) — first order only; the
  same flaw that killed Clohessy–Wiltshire at system scale (H0203: 7.7× after
  one period).
- Rejected: **tree/FMM N-body per step** (Barnes–Hut and descendants, the
  industry default) — per-body per-step work, no compiled repetition,
  compounding error, memory traffic O(N); violates principles 1, 3, 13, 14.
  (The literature optimizes its requirement — one-shot fidelity per step —
  not ours: zero work for predictable repetition.)
- Rejected: **orbit-superposition DF evolution** (Schwarzschild modelling) —
  averages bodies.
- Complementary, not competing: **multipole cells** (board bottleneck 1) hold
  the field's sources; the doll holds the motion.

**Known failure modes of the adopted candidate** (each maps to an existing
rule): coherent non-axisymmetric lumps (spiral arms, a bar) create a resonance
web where averaging dies (r4's rule: phase-locked kicks near resonance; the
compiled cycle yields the epicyclic frequency for free — measured κ/Ω below);
a strong bar breaks axisymmetry in its region (the bar becomes its own doll or
the dense order); the nucleus's GR is not in the Newtonian program (delegated
to the hole's doll inside its SOI — measured below).

## Evidence (all numbers regenerate from `python3 galaxy_doll.py full`)

Potential: finite Mestel disc, Φ = ½v₀² ln(1+(r/r_c)²), r_c = 0.05, galaxy
edge R_g = 8, C¹-matched Kepler outside; optional nucleus −M_BH/√(r²+ε²).
Oracle = same quadrature at 512 panels; independent instrument = leapfrog KDK
(dt-halving checked); two analytic controls.

**E1/E2 — held-out rosettes (panels to reach relative error, both Δφ and Δt):**

| case | to 1e-6 | to 1e-9 | err at 32 panels (Δφ, Δt) |
|---|---|---|---|
| B eccentric (rp 0.4, ra 3.0, e 0.76) | 8 | 16 | 9.9e-13, 5.7e-12 |
| D outer, crossing R_g (5.0, 11.0) | 4 | 8 | 7.0e-14, 3.1e-12 |
| E nucleus-mixed (rp 0.02, M_BH 0.05) | 16 | 32 | 3.2e-13, 4.3e-12 |
| C core control (0.0006, 0.0024) | 4 | 8 | 4.7e-11, 1.8e-10 |

Same class as the plane's ~140-panel kick compiles, at its 1e-6 floor with an
order to spare. Compile cost 132.8 µs at 32 panels (Python, cloud x86 — order
of magnitude only).

**Analytic controls (both pass):** harmonic core, held out at r_a/r_c = 0.048:
Δφ/π − 1 = 1.44e-4, exactly the measured (r_a/r_c)² law (9.995e-5 at 0.04) —
the core limit is Δφ → π (closed centred ellipses). Flat zone, near-circular
at r = 3.0 (held out): Δφ/π = 1.414005, inside the predicted [1.4139,
1.41410], approaching √2 (the isothermal κ = √2Ω; confirmed numerically
here at five radii, 1.4212 at r = 0.5 → 1.4141 at r = 4; textbook source
UNVERIFIED).

**Error type (P5):** 10⁴ cycles advanced by pure additions differ from N·Δφ by
6.5e-9 rad total (machine rounding, ~eps per addition); per-cycle error 4.1e-12
rad at 32 panels; re-key interval 2.4e7 cycles for a 1e-4 rad floor.
Independent leapfrog, case B, 30 cycles: compiled advance vs stepper final
azimuth differ by 2.7e-5 rad, within the stepper's own dt-convergence (2.0e-5);
the compiled per-cycle error is 7 orders below the instrument.

**Scatter transits (E5, the player's coast; compiled vs leapfrog, 64 panels):**

| case | r_p | deflection (compiled / leapfrog) | error | Δt rel err |
|---|---|---|---|---|
| β∞ 0.9, b 0.5 | 0.479 | −3.556e-2 / −3.556e-2 rad | 5.0e-10 | 7.8e-6 |
| β∞ 0.9, b 2.0 | 1.946 | −3.453e-2 / −3.453e-2 | 2.5e-9 | 2.3e-5 |
| β∞ 0.3, b 0.5 | 0.365 | −2.123e-1 / −2.123e-1 | 5.8e-8 | 1.9e-6 |
| v∞ 1, b 0.05 | 0.014 | −8.551e-2 / −8.586e-2 | 3.5e-4 | 2.6e-5 |

At 0.9c the route through the galaxy bends by ~2°: nearly straight, one
compiled transit, zero work after. The slow deep-core case is the hardest
(quadrature-limited at 64 panels; the leapfrog's own convergence there is
2.9e-6).

**The GR seam (E3, arithmetic, Sgr A*-like: 4×10⁶ M_sun, v₀ 220 km/s,
Θ = 1e-3 rad):** r_SOI = GM/v₀² = 9.3×10⁵ r_s (0.36 pc). The radius where
accumulated GR apse drift N(r)·6π r_s/r crosses Θ: 492 r_s (H = 10⁵ s),
3.1e3 (10⁷), 2.0e4 (10⁹), 1.2e5 r_s = 0.047 pc (10¹¹ s). **The seam is inside
the SOI at every horizon** — by 1900× at short horizons, 7.5× at H = 10¹¹ s.
A 10⁸ M_sun nucleus: seam 136–3.4e4 r_s, ratio to SOI even smaller (seam/r_s
∝ M^-0.4). Only at the tube-quantum threshold (Θ = 1e-6 rad) and H ≥ 10¹¹ s
does the seam poke outside the SOI, by ×2. **The design's existing SOI doll
boundary automatically covers GR; no new component, and the horizon argument
makes the deletion above it safe.**

**The frozen disc (E8, arithmetic):** a Milky-Way-like disc (8 kpc, 220 km/s,
T = 2.23×10⁸ yr) completes per 100-h session: 0 orbits at rtf 100, 5e-7 at
10⁴, 5.1e-5 at 10⁶, **5.1e-3 at rtf 10⁸**. One disc orbit per session needs
rtf ≈ 2×10¹⁰. Meanwhile the player's news cone after 100 h at rtf 10⁶ reaches
~3.5 kpc (44% of the disc radius): **at galactic scale, dynamics travel with
the player and the news, never with the disc.** The galaxy doll's steady state
is memory and view, not integration.

**Epicyclic frequencies from the compiled cycle (free by-product, the
resonance web's input):** κ/Ω = 1.4212 (r 0.5) → 1.414005 (r 3) → 1.414091
(r 4), monotone 2 (harmonic core) → √2 (flat). Corotation, ILR and OLR radii
for any pattern speed follow by subtraction; **resonance widths under a
realistic arm/bar spectrum are unmeasured — the named next experiment.**

## Predictions (`predictions.md`, frozen before the decisive run)

7 of 9 held. **P1 pass** (all cases ≤ 16 panels to 1e-6, ≤ 32 to 1e-9 —
better than the ≤ 32/≤ 64 bars). **P3 pass** (1.44e-4 vs 1.4e-4 predicted,
exact). **P4 pass** (1.414005 ∈ [1.4139, 1.4141]). **P5 pass.** **P6 pass**
(deflection errors 5e-10…3.5e-4 against bars 1e-4…1e-3; Δt ≤ 2.6e-5 against
1e-4). **P8 pass** (disc orbits ≤ 5.1e-3 at rtf 1e8). **P9 pass** (132.8 µs
inside 30–300 µs).
**P2 fail, informative:** predicted the R_g band cut would be required
(≥ 10× worse without); measured, cut vs no-cut differ by < 3% at every panel
count (2.2e-6 → 7e-14 from 2 → 32 panels, identical rows) — a C¹ potential
match needs no cut machinery at the 1e-6…1e-9 floor. The plane's cuts are
load-bearing for its C⁰ force cells, a smoothness class this falsifier does
not test; the galaxy's program field may be C¹ piecewise for free.
**P7 fail, informative:** predicted the GR seam outside the SOI by 3–130×
(my hand arithmetic had r_SOI off by 10³); measured the seam **inside** at
every horizon (5e-4–0.13 of SOI). The failure strengthens the design: the
SOI boundary covers GR with margin.
Disclosed code history: the first decisive run had an azimuth bug
(`atan2(vinf, 0)` = π/2) flagged in advance by P6's risk clause, and its D
case never crossed R_g (rp 4, ra 7.5 vs R_g 8 — a mis-specified control);
both fixed, everything re-run. All numbers above are from the final
`galaxy_doll.py` as shipped in this folder.

## What would make it wrong

- A compressed game galaxy whose disc actually turns within a session
  (rtf ≥ 10¹⁰, or a 100× smaller disc): then the resonance web with coherent
  lumps decides the kick budget, and this run did not measure resonance
  widths — only the frequencies that locate them. If the web covers a
  sizeable disc fraction, phase-locked kicks (r4's rule) become the galaxy's
  main cost, and the "frozen program" claim dies with it.
- A strong bar: axisymmetry — hence integrability — fails in its region; the
  bar needs its own doll or the dense order. Unmeasured here.
- Star-star relaxation at galactic scale is assumed negligible (Chandrasekhar
  far beyond any horizon; UNVERIFIED at source here) — if the game compresses
  densities by orders of magnitude, encounters return and the belt results
  (H_live runs) apply instead.
- The nucleus-mixed case needed 32 panels for 1e-9; a cuspier nucleus or a
  tighter periapsis could climb out of the plane's cost class — the seam rule
  still delegates the whole region inside r_SOI to the hole's doll.

## Cost of adopting, and fit with PRINCIPLES

Adoption cost: none new — re-uses the cycle compiler, tubes, kicks, news; the
one rule it adds is the nucleus edge = Newtonian SOI (measured to cover GR).
"The cheapest compute is compute not done" (1): the disc is a frozen program
at every playable rtf. "Compute only surprises" (3): galactic dynamics travel
with the player and the news cone (5.1e-5 disc orbits vs a 3.5 kpc cone).
"Symmetry is found, not given... under the right representation many
symmetries can appear" (32): 2D rotation symmetry makes the galaxy the same
integrable law as the two-body doll — the field's hardest open problems
(3-DOF tori, triaxial chaos) never arise. "Averaging an orbit... is not the
same thing" (kicks rule): orbits are averaged into compiled cycles, bodies
never are.

## The lens

Scout's blind spot: it searches for solutions that exist, and under-reports
negative space — this run's headline is that the galaxy needs **no new
mechanism**, which a solution-hunting lens is biased against finding. Second:
cloud x86 timings (orders of magnitude only; the integrator re-measures on
the M1). Third: the rosette error table's oracle is the same quadrature at
higher panel count (same-harness risk), guarded by the independent leapfrog
on case B and two analytic controls.
