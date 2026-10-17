# predictions.md — 20261017-2038-scout-8dfb

Question: does the inclined Kerr geodesic (Carter Q ≠ 0) compile into the law's own
compiled-cycle shape — a finite set of per-(E, L_z, Q) constants (two Mino periods, two
azimuthal advances, two clock advances), each a complete elliptic integral in the Carlson
kernel family the law already ships (RF/RD/RJ; cd6e/de99) — verified in float against
direct integration of the coupled geodesic equations?

## The decisive experiment (one instrument, `falsifier.py`)

Per orbit (a, p, e, θ_inc): derive (E, L_z, Q) from the turning-point conditions;
RK-integrate the four first-order Mino-time geodesic equations (r, θ, φ, t) across
several cycles; extract the six torus constants; compare against the same six from the
separated 1-D closed-quadrature integrals (30+ dps) and from the Carlson-kernel
reductions. Controls on both sides (below).

## Pre-registered expectations (written before the run)

P1 — physics/separation (the decisive claim): on the main grid
(a ∈ {0.2, 0.6, 0.9}, p ∈ {8, 12}, e ∈ {0.1, 0.5}, θ_inc ∈ {30°, 60°, 120°}, pro/retro
by L_z sign) every one of the six constants from the separated integrals matches the
coupled RK integration to ≤ 1e-8 relative. I expect the RK to be the limiting side
(~1e-10); if any row disagrees > 1e-6, my derivation or transcription is wrong — that
kills this instrument (the configuration), not the separation method.

P2 — kernel mapping: the Carlson RF/RD/RJ evaluations of the six constants agree with
closed quadrature to ≤ 1e-13 (they are the same integrals; the reduction is the claim).
The third-kind pieces (the L_z/sin²θ polar term; the Δ = 0 pole terms of the clock) are
where I expect any failure: prediction ≤ 1e-12, flagged if > 1e-9.

P3 — Schwarzschild control (negative side): at a = 0 with any inclination, the azimuthal
advance per polar cycle must be exactly 2π (the orbit is planar; one θ-libration = one
revolution) — both paths ≤ 1e-12 from 2π. A nonzero value falsifies the polar reduction.
At a = 0 the per-radial-cycle advance must be independent of inclination (Schwarzschild
is spherically symmetric): the radial constants at θ_inc = 30° and 90° agree bit-class
(≤ 1e-12 relative).

P4 — equatorial degeneration (positive side): as z = cos²θ_min → 0 the radial constants
converge to the equatorial (Q = 0) values (≤ 1e-6 at z = 1e-6, linear-ish), and Λ_θ → 0
(the polar libration collapses onto the equatorial plane).

P5 — cost: one six-constant readout through the Carlson path in float ≤ ~10 µs x86
(order of magnitude only; the plane's shipped read class is ~4 µs).

## Held-out rows (not tuned on; the checker may add more)

a = 0.998 (extremal), e = 0.9, θ_inc = 150° (retro), p = 6.8 (near-separatrix at
a = 0.9, e = 0.5 — I expect the WORST agreement here; RK through slow turning points is
the known soft spot; prediction ≤ 1e-6, honestly possibly worse: if it fails there I
report it as the instrument's edge, not the law's).

## What would make the adoption wrong

Resonant tori (Λ_r/Λ_θ rational) are fine for readout in Mino time but the
coordinate-time readout's Newton inversion is untested here; the plunge separatrix
(Λ_r → ∞) needs the refusal path; the integer port (Q's word width, the exact integer
advance law) is unpriced; self-force/radiation is out of scope (test particles only).
