# Predictions — 20261004-0555-spacex-450b

Written before the decisive sweep (`./replica sweep`). What I have already seen: the reference
convergence runs (`./replica ref`, dkd@4096 vs y6@~8208 sub-kicks/orbit agree to ≤2.4e-6 relative
on the precession slope for all bound cases), which fixed the references and the scene list. The
sweep's coarse-N frontier — including all held-out cases below — is untouched. Tuning happened only
on: making the two references agree (scene validity), not on any scheme's step count.

Cases: A prograde 0.30 R_H e=0.15 (precession case), B 0.30 R_H e=0.05 (Jacobi case),
C–D held-out e=0.30 / e=0.60, E held-out retrograde, F held-out retrograde 0.60 R_H (8× deeper
tide), G held-out prograde 0.45 R_H (near the stability edge). Gates: precession slope within 10%
(B14), mean e over the last 100 planet orbits within 10% (B14), Jacobi relative error ≤ 1e-4 with
log-log growth exponent ≤ 0.2 (B12/B5 style). Cost = kick applications per orbit (each is a rebind).

1. **dkd (the plane's law, 1 kick per phase step) passes all three gates on A–E at N = 8 kicks
   per orbit, possibly as low as 4.** So the plane's 1/64 carries ≥ 8× margin for moon behaviours:
   a deletion, not a new scheme.
2. **y4 (3 sub-kicks per macro step) at equal TOTAL kicks/orbit beats dkd's Jacobi error by ≥ 10×,
   but its minimal passing kicks/orbit is at best ~1.5× lower than dkd's — short of the 4× gold
   bar of the q-correctors brief.**
3. **y6 never pays at these tolerances** (9 sub-kicks per macro step; order 6 only pays beyond
   ~1e-6 error, far from a 10% behaviour gate).
4. **y4q (weights rounded to 1/256, the dyadic integer path) matches y4 within a factor 2 on every
   gate**: weight quantization does not break the order advantage.
5. **Held-out D (e = 0.60): dkd needs ≥ 2× more kicks/orbit than on A** for the same gates
   (pericenter carries the tide's phase variation; uniform phase steps under-resolve it).
6. **Held-out F (retro 0.60 R_H): dkd needs ≥ 16, likely 32 kicks/orbit; y4 passes at 6–12
   sub-kicks/orbit; the ratio stays < 4×.**
7. **Held-out G (0.45 R_H prograde) is chaotic or near-chaotic**: the two references will disagree
   on the precession slope by > 1%, or e wanders; then precession is undefined there and
   bound/escape classification is the only gate, expected to match at every N ≥ 8.
8. **Net expectation: no gold.** The adoptable result is the deletion (64 → 8 kicks per orbit,
   behaviours unchanged, one constant), reported as the measured margin, plus "higher-order splits
   do not pay at behaviour tolerances" as the reason q-correctors is one experiment poorer.

Falsifiers of the whole direction: dkd needs N ≥ 32 already on A (no margin to delete); or y4 needs
MORE total kicks/orbit than dkd at equal behaviour (negative sub-steps + rebinding cost dominate).
