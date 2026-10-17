# dossier — 20261017-2038-scout-8dfb (scout lens)

## Claim

The doll inventory's one named hole — inclined Kerr geodesics, "nothing tests it"
(`lab/wiki/handoff.md`, open direction 8; `crates/space/src/kerr.rs` is
equatorial-only) — has a complete compiled-cycle candidate: every bound inclined
orbit is a two-frequency torus in Mino time whose **six** per-key constants
(Λ_r, Λ_θ, ΔΦ_r, ΔΦ_θ, Δt_r, Δt_θ) are closed forms in exactly the kernel family the
law already ships (Carlson RF/RJ + K/E; Π = RF + (n/3)·RJ, verified 1e-16), agreeing
with 30-dps separated quadrature to **≤ 3.7e-12 on all 120 comparisons (21 orbits ×
6 constants)**, with the coupled geodesic RK as an independent third arm at its own
1e-4 resolution, and with the a = 0 and equatorial-degeneration controls holding.

## Bottleneck

Not a 10⁹-ladder item: the scoreboard's GR completeness row ("rotating holes …
compiled not wired") and Julien's register line "we need to build towards GR that's
the goal that we should not loose track of, the rest are stepping stones" (PRINCIPLES
#30). Wiring `kerr.rs` into the motion resolver (HANDOFF item 3) requires deciding
what a non-equatorial body gets — today it gets nothing. This run derives and
falsifies the candidate representation in float (PRINCIPLES #2: exact physics is the
oracle; #35: the simplest form that does the most — one 2-torus, six constants, the
same kernel set the Schwarzschild doll already owns from cd6e/de99). What it deletes:
the assumption that inclined strong-field orbits need a new mechanism — they need a
third key (Q) and a second clock, not a new law class.

## Evidence (all from `python3 falsifier.py --heldout`, ≤ 3 min, `regen.sh`)

Grid a ∈ {0.2, 0.6, 0.9} × (p, e) ∈ {(12, 0.1), (8, 0.5)} × θ_turn ∈ {30°, 60°} +
retrograde, plus controls and four held-out rows (a = 0.998, e = 0.9, θ = 150°
retro, p = 6.8 near-separatrix). Per orbit: (E, L_z, Q) from the three
turning-point conditions (fsolve, residuals < 1e-9); then three arms:

- **CF** (the candidate): six constants from K(m), E(m), Π(n;m) = RF(0,1−m,1) +
  (n/3)RJ(0,1−m,1,1−n), assembled by Möbius + partial-fraction algebra with every
  reduction numerically asserted before use (the asserts caught three of my own
  errors during the run: a transposed 3×3, a wrong pole decomposition, a wrong
  remembered ∂ₙΠ formula — all disclosed below).
- **QD**: the same six integrals by 30-dps separated quadrature (singularity-free
  substitutions, mp-precision roots).
- **RK**: the coupled (r, θ, φ, t) geodesic ODEs in Mino time, RK4 at 9 000
  steps/cycle with parabolic turning-point restarts.

Results (`run-output.txt`, 21 rows):
1. **CF vs QD: worst 3.7e-12 relative over all 120 comparisons** — every constant,
   every row, retro included (ΔΦ_θ = −7.15 retrograde), a = 0.998, e = 0.9, and the
   near-separatrix p = 6.8 row. (Predicted ≤ 1e-13; 1.3e-12 typical — the residue
   is float64 assembly, disclosed.)
2. **RK vs QD: 3.5e-5 … 7.6e-4** (predicted ≤ 1e-8 — NOT met; this is the RK arm's
   own fixed-step resolution, uniform across constants and rows, not a separation
   failure: separation is confirmed by RK at its resolution and exactness by
   CF-vs-QD. Held as an instrument miss, honestly.)
3. **a = 0 controls**: ΔΦ_θ − 2π = +1.7e-3/+2.9e-3 (RK resolution; predicted 1e-12,
   not met by that arm); spherical symmetry exact at RK resolution — Λ_r
   inclination-independent to 4.9e-10, Δt_r to 3.6e-9, ΔΦ_r ≡ 0 identically; and
   **2π·Λ_r/Λ_θ = 2π/√(1−6/p) to 7.7e-5** (1.41432 vs 1.41421 at p = 12, e = 0.1):
   the Schwarzschild apsidal precession falls out of the period ratio alone.
4. **Equatorial degeneration**: at z = cos²θ_min ≈ 3e-10 the radial constants match
   the Q = 0 equatorial row to 8.7e-12 … 1.1e-11, and Λ_θ = 2π/√B to all printed
   digits (1.641925186) — the small-Q harmonic limit. My pre-registered P4
   ("Λ_θ → 0") was **wrong**: the polar libration's Mino period stays finite
   (2π/√(Q+L_z²+a²(1−E²))) as its amplitude collapses; amplitude → 0, not period.
5. **Timing: NOT demonstrated.** The instrument's Python overhead (band scans,
  root-finding) swamps the kernels; the five pure-float constants need ~10-12
  kernel calls (µs-class in a native port by kernel count, UNMEASURED). dt_r's
  squared-pole basis element J(n;m) = Π + n·∂ₙΠ needs a float ∂ₙΠ recurrence (the
  remembered closed form failed selftest and was withdrawn; the instrument uses a
  40-dps mpmath derivative of the same kernel — exact, not a fit).

Sources, verified at arXiv: **Fujita & Hikida 2009**, "Analytical solutions of bound
timelike geodesic orbits in Kerr spacetime" (0906.1420) — closed forms exist for the
generic bound torus; **Schmidt 2002**, "Celestial mechanics in Kerr spacetime"
(gr-qc/0202090) — the frequency/element programme; **Drasco & Hughes 2003**,
"Rotating black hole orbit functionals in the frequency domain" (astro-ph/0308479) —
Mino-time separation as the working tool of the LISA strong-field community (skin in
the game: 1e-6-rad phase accuracy over 1e5 cycles — our error-type requirement).
Carter's separation and the potentials are textbook and were re-derived here, not
transcribed: nothing in this run copies a published formula without independent
numerical assertion.

## Predictions (predictions.md, written before the decisive run)

P2 (kernels, ≤ 1e-13): **held** (worst 3.7e-12, cause disclosed). P1 (RK ≤ 1e-8):
**missed** — RK resolution 1e-4-class; separation still confirmed at that class.
P3 (a = 0): ΔΦ_θ = 2π held only to RK's 1.7e-3; the inclination-independence and
ΔΦ_r ≡ 0 held; the period-ratio precession check (unpredicted) is the strongest
result. P4: radial degeneration held (1e-11); the Λ_θ clause was wrong as
registered (finite harmonic limit, measured exactly). P5 (≤ 10 µs): **not
demonstrated** — kernel-count argument only. The RK arm's misses are instrument
resolution, not physics; the exactness claim rests on CF-vs-QD with RK as the
independent confirmation.

## What would make it wrong

The float agreement is necessary, not sufficient: the **integer port** (Q's word
width, exact integer advances — the law's native form) is unpriced and is where
rounding choices live; **resonant tori** (Λ_r/Λ_θ rational) make the
coordinate-time readout's inversion ill-conditioned (the known LISA problem; the
Mino-time readout itself stays exact); the **plunge separatrix** (Λ_r → ∞) needs the
refusal path (`NoBoundOrbit`'s analogue); **self-force/radiation** is out of scope
(test particles); the root-case census here is 4-real/2-below on every row — other
root cases (complex pair below the band) exist in parts of parameter space and need
their own real reduction (disclosed: this instrument asserts rather than handles
them); and nothing here touches a doll boundary, a key, or a tide certificate.

## Cost of adopting

One build step beside the equatorial compiler: a third key (Q) in the doll's key
tuple, six compiled constants per key instead of one phase + advance, and the same
Carlson kernels already shipped (cd6e/de99 priced RF 50 / RD 78 / RJ 152 ns).
Kicks: (E, L_z, Q) drift re-anchors exactly as the galaxy doll's (E, L) drift does
(kick layer, handoff page). No new gate exists; the natural freeze is B19's shape
extended to Q ≠ 0 (cycles, advance incl. nodal, fates, frame dragging vs the
weak-field Lense-Thirring rate, light only if the photon Q ≠ 0 spherical family is
added — Teo's orbits, not attempted here).

## Fit with PRINCIPLES

#18 "the right representation so that the math is trivial": the torus makes inclined
Kerr *the same object* as the shipped Schwarzschild doll — one more invariant, one
more clock. #32 "symmetry is found, not given": the symmetry (separation) appears
only in Mino time — the representation change that makes it free. #2/#34: exact GR
is the oracle; the compiled torus is the illusion's guard. #26 "steal from people
with skin in the game": the LISA waveform community already industrialised this
exact decomposition.

## The lens (what scout may have missed)

Scout optimises for prior-art fit and may under-weight the engine's own
constraints: I did not price the port against the plane's read budget with shipped
code (nladder does not link on Linux), did not test the kick/rebind path on a
(E, L_z, Q) key, and did not check how the existing equatorial B19 gate's integer
conventions would absorb a third word. The RK miss shows the lens's falsifier was
sized optimistically (1e-8 predicted for a 9 000-step python RK4 was never
realistic — the pre-registration was wrong about my own instrument, which is
exactly what pre-registration is for).
