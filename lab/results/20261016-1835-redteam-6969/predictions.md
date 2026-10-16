# Predictions (written before the decisive run)

Target premise: representation.md L37 / law.md L39 — "two comparable masses form
one doll with M = m1+m2; ν enters only through the effective-one-body energy map
at 1PN." The gate B11 judges precession only within (1% + 16/p), i.e. 80% at
p = 20M, and judges periods only where the 2PN next term is ≤ 5e-4 (a >~ 100M):
the strong-field binary domain is unjudged. Julien's approved scenes (rotating
holes, inspiral) fly exactly there.

Falsifier: the doll (exact Schwarzschild cycle at (E_eff, L_eff), real energy via
the 2PN-accurate EOB map, exactly r3 v3's `eob-doll` configuration) against the
2PN conservative truth (reduced ADM Hamiltonian, Buonanno–Damour 1999 eq 10,
invariant quadrature dφ/dr at fixed real invariants (E_NR, j)). All float, < 60 s.

Cases I did NOT tune on (the grid is chosen a priori): p ∈ {8, 10, 15, 20, 30,
50, 100} (Darwin semi-latus rectum, units M), e ∈ {0, 0.3, 0.6}, ν ∈ {0, 0.05,
0.125, 0.25}.

## P1 (control, must pass or the instrument is broken)
At ν = 0, the ADM-2PN quadrature matches the exact Schwarzschild advance
2π(1/√(1−6/p) − 1) with relative residual of truncation size only: ≲ 1% at
p ≥ 20, growing toward smaller p as ~ u² (u = 1/p), and roughly monotone in p.
If this fails, my transcription of the Hamiltonian is wrong and I fix it before
any claim.

## P2 (the ν term at 1PN — a sanity invariant, not the target)
At 1PN (drop H₄), at fixed real (E_NR, j), the doll's advance equals the ADM-1PN
advance to truncation size (O(u²) relative); any excess ν-dependence beyond the
energy map would falsify BD99's own theorem, so it must not appear.

## P3 (the decisive one)
At ν = 0.25, the doll's periastron advance at fixed real (E_NR, j) is wrong
against 2PN by a ν-term of order ν·u·(few):
- p = 10M: error between 1% and 15%, sign: doll OVER-precesses (doll k > 2PN k);
- p = 20M: between 0.5% and 8%, same sign;
- crossing 1% somewhere between p = 25M and p = 60M.
Held-out extrapolations the checker may run: error scales ~ linearly in ν at
fixed (p, e), and grows with e at fixed p (pericenter effect).

## P4 (error type, secondary)
The 2PN circular-orbit ISCO for ν = 0.25 moves OUTWARD from 6M (doll says 6M for
every ν), by between 0.1M and 2M in the 2PN-truncated potential.

## What would falsify my attack instead
If P1 fails and cannot be repaired, the instrument is broken (VOID). If P3's
error at ν=0.25, p=10 is < 0.3% (i.e. the energy-map ν-dependence absorbs the
2PN term at fixed invariants), the premise SURVIVES at strong field and I report
that as a licence with numbers.
