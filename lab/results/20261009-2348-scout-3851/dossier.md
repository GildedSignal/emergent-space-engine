# Dossier — scout run 20261009-2348-scout-3851

## Claim

The epoch-tide law for a doll on an eccentric tube needs a Floquet
certificate: a member's tide equation is Hill's equation, orbit-averaged
tides (the 114× lever, H0190) are blind to 100% of its parametric pumping
bands, and the member's monodromy over one compiled radial cycle — shared
per (E, L) memo key, one 2×2 product per member, zero steady-state cost —
is the exact cheap certificate, replacing sampling laws entirely.

## Bottleneck

Board item 4: "the Schwarzschild tide in the Fermi frame (phase 2, after
gate E9)"; law.md's dense order applies the member tide "as exact integer
kicks at epochs" and H0190 wants orbit-averaged tides. Expected gain: the
certificate decides *where* averaging is legal, so the 114× saving survives
where it is safe and compounding pumping (principle 13's forbidden error
type) is never silently shipped; it also deletes the epoch-cadence question
(how many kicks per orbit) in favour of one exact per-doll chart. What it
lets us delete: per-member kick scheduling inside dolls whose chart is
clean, and any temptation to sample the tide finely "to be safe".

## The candidate (requirements first, then the best solution anywhere)

Requirements as numbers: doll on an eccentric equatorial geodesic
(E9's grid: r_p/M = 10…10⁶, e ≤ 0.6); members with binding Ω_m
(moons of a 10⁻³-mass-ratio doll: Ω_m ≈ 2–20 × the doll's azimuthal rate;
fleets under station-keeping similar); error type: member energy pumping
(compounding — forbidden), not error size; deterministic, 60 s tests, ≤ 2 GB.

Fields with the same structure (a particle in a periodically-driven
restoring field): **Paul traps and alternating-gradient synchrotrons** —
they hold beams for hours on exactly this stability chart (Ince–Strutt;
Courant & Snyder 1958), and their known failure mode is parametric
resonance bands at 2ω = kΩ_drive with widths set by the drive's Fourier
amplitude; **lunar theory** (Hill 1878 — the equation's name); **Kapitza
1951** (averaging is safe only when the drive is *fast*; here the drive
Ω_r is *slow* compared with a bound member's ω_eff — the opposite, unsafe,
regime); **Io's tidal heating** (Peale et al. 1979) — eccentricity-driven
periodic tides pumping internal energy, the astronomical skin-in-the-game
case; the **eviction resonance** of satellite dynamics (periapse
commensurability with the parent) and **transient resonances in EMRIs**
(Flanagan & Hinderer 2012) [UNVERIFIED at source; web search on this box
returned title-stripped feeds]. Mechanism mapped onto our cells: the doll
*is* the focusing lattice; the member's Hill equation over one compiled
radial cycle *is* the lattice cell; the certificate is the 2×2 monodromy's
trace (|tr| ≤ 2), computable from the λ(τ) table the compiled tube already
holds — no new integrations, shared by every tube with the same (E, L) key.

## Evidence (float prototype; exact commands, each < 60 s on this box)

Model: x″ + (Ω_m² − α·λ(τ))x = 0, λ = u³(3γ²−1) — the phase-2 closed form
(run 20261006-0220-q-fermi2-tide-v2-26a7) — α=+1 the moon-like radial
channel (tide reduces stiffness), α=−1 the compressive channel. Truth is
RK4 Floquet over one radial period, cross-checked against scipy solve_ivp
to 1e-6; convergence (step halving) ≤ 2×10⁻⁵ on traces, worst case
(r_p=10, e=0.6, where γ_p = 1.097 and λ varies 50× per orbit). Grid:
Ω_m ∈ [0.02, 16]×Ω_r, 601 points; 24 held-out cases. Machine: 8 vCPU
Linux cloud box, load 0.90/0.63/0.67 at start; orders of magnitude only.

Commands (from `lab/results/20261009-2348-scout-3851/`):

```
python3 falsifier.py '[{"rp":100,"e":0.3,"alpha":1},{"rp":100,"e":0.3,"alpha":-1}]' cal5   # ~14 s
python3 falsifier.py '<e=0 grid: rp {10,30,1e3,1e4} x alpha {+1,-1}>' e0                     # ~51 s
python3 falsifier.py '<same, e=0.3>' e03                                                     # ~51 s
python3 falsifier.py '<same, e=0.6>' e06                                                     # ~51 s
python3 analyze.py                                                                           # <1 s
```
(exact JSON arguments are in the shell history of this run and regenerate
`results-e0/e03/e06.json`; `results-cal*.json` are calibration and the two
disclosed mid-run bug fixes below.)

Numbers (all growth exponents per orbit):

1. **Bands exist and pumping is fast.** α=+1, e=0.6: 11–14 truth bands;
   peaks reach 2.5/orbit at e=0.3 (k=2) and >1/orbit for k=2–4 at e=0.6 —
   energy e-folds in a few doll orbits. Nothing slow: this is ruin-speed.
2. **Averaging is blind everywhere.** The avg law (constant λ̄) reports
   zero parametric bands in 24/24 cases — 100% missed. It also places the
   static Hill-loss edge (√λ̄) up to 24% below the true loss region, because
   the k=1 band merges into it. Where the averaged tide is used inside a
   doll whose chart has a band, the law ships a compounding error by
   construction.
3. **The compressive channel is the safe one** (a held-out prediction that
   failed informatively): α=−1 has no bands ≥0.05/orbit at e=0.3 and only
   ≤3 weak ones at e=0.6 (1/4 radii ≥0.05), because ω_eff² = Ω_m²+λ̄ never
   cancels, so only harmonics k≥4 reach. Channel sign matters more than
   eccentricity for averaging's safety.
4. **Exact-segment epochs at K=32 reproduce truth**: 55/58 bands matched,
   centers within grid resolution, worst peak error 17%. The impulse form
   (velocity kicks between free-oscillator drifts) does not: worst peak
   error 100% (some bands erased), 6/58 badly off-center, and at e=0 it
   misestimates the Hill-loss rate by 0.65/orbit exactly at the static edge
   (Ω_m = 1.410 vs edge 1.414) — the impulse reading of "exact integer
   kicks" is wrong even for a constant tide; the segments must hold the
   tide and propagate exactly.
5. **Cadence cliff**: hold4 is off by ≥30% on 40/42 e=0.6 band peaks;
   hold1 fails qualitatively in 8/16 eccentric cases (spurious ≥0.5/orbit
   bands where truth is stable). The safe cheap law is not "more epochs"
   but the certificate itself: the doll's band chart from one monodromy
   sweep (600 2×2 products) per (E, L) key, consulted once per member.
6. **Moons sit in the chart** (8/8 α=+1 eccentric cases): at e=0.3 the k=1–2
   centers and at e=0.6 the k=2–3 centers lie at 1.7–3.4 × Ω_az — the
   outermost moons (0.9–0.7 Hill radii, Ω_m ≈ 2–3.5 × Ω_az) overlap band
   structure in every case. Relativistic widening is real in the drive
   (λ̂₁/Ω_r² at r_p=10 is 1.55× its r_p=10⁴ value at e=0.6) but the static
   edge in Ω_az units is unchanged (0.97×): precession and the periapsis
   boost cancel there — bands widen, the Hill radius does not.
7. **The closed-form band map is only a diagnostic**: centers from
   2ω_eff = kΩ_r match 16/16 at e=0.3 but 15/42 at e=0.6 (pulsed drive,
   rich Fourier tail, bands merge) — so the certificate must be the
   monodromy, not a formula; the monodromy is just as cheap.

## Predictions

In `predictions.md`, written before the sweep. Held: P2 (averaging blind,
0/24), P3 for hold32/hold4 (55/58 and 40/42), P6 (8/8 moon-range overlap),
P7's drive-widening (1.55 ≥ 1.4). Failed, reported as held: P1 (the
moments-only center map — holds at e ≤ 0.3, fails at e=0.6: the certificate
must be the monodromy), P4 as worded (α=+1 keeps its static band at e=0 —
correct physics my wording ignored; and kick32 breaks it, which is finding
4), P5 (compressive channel safer than predicted — finding 3), P7's static
edge (unchanged in Ω_az units — finding 6).

## What would make it wrong, adoption cost, fit

Wrong if: the true in-plane Fermi tide couples the two channels so bands
shift materially (the 2×2 monodromy on the full Marck matrix, with
parallel-transported axes, must replace the scalar prototype — same
certificate, one size up; the build b-fermi-phase2 needs it); if members'
Ω_m in real dolls sits outside [0.02,16]×Ω_r (station-kept fleets at very
high Ω_m are covered; unbound fly-through members are not the tide's
problem); if E9's ten-period horizon hides what Floquet sees — it does:
E9 judges the frame's local evolution, not many-cycle member pumping, so
this failure mode is invisible to every current gate (B14 classifies moons
at 50 orbits; a band member can pass 50 orbits before classification flips
at growth <0.06/orbit). Adoption cost: small and local — one band chart per
(E, L) memo key in the cycle memo, one membership test per member per
element change; the averaging lever survives outside bands, the epoch law
holds-and-propagates exactly inside them. Fit: "Errors never compound"
(#13) — averaging inside a band compounds by construction; "regimes are
chosen by dimensionless numbers" (#4) — band membership is exactly such a
number, read from the tube's own compiled frequencies; "Compute only
surprises" (#3) — the chart is computed once per doll, not per body.

## The lens (what the scout lens may have missed)

Scout looked outward for the mechanism and found it in accelerator/trap
stability charts; it may undervalue in-house constraints — the integer
law's kick quantization could shift band edges by quantum-scale detuning
(the float chart is a map of where to look, not the certificate's final
bits); and the 1-D prototype treats members as linear oscillators, so
finite-amplitude moons (Kepler, not harmonic) will saturate band growth at
finite eccentricity — the *detection* stands, the peak magnitudes are
linear-theory upper bounds. The EMRI and eviction-resonance anchors are
UNVERIFIED at source on this box.

## Disclosure

Two bugs were found and fixed mid-run, before the predictions file and the
decisive sweep: the kick law's force sign (cal2→cal4) and its missing
own-oscillator drift (cal4→cal5); calibration files from before each fix
are retained. No data files were edited after their runs; predictions.md
predates results-e0/e03/e06.json (timestamps in git when published).
