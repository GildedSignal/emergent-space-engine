Working...
Check complete. `lab/results/20261008-1613-inversion-ef21/check.md` written; nothing else in the run folder touched (work done from `/tmp/check-ef21`; `work/patch.diff` was empty, no tree edits to apply).

**Grade: silver.**

The verdict in brief:

- **The physics is real and decisive.** The frozen kill criterion in `predictions.md` fires: at identical mean-motion concentration (Δn/n 0.048 vs 0.043), the co-orbital rank ≤ 4 certificate misses 0.0% of contacts on the gold's train formation and 99.4% on a periapsis-dispersed ring. Reproduced from the shipped `probe.py` at the author's scale and mine; seed-independent (fresh seed 97.98%); ϖ spread alone with e fixed breaks it (94.7%); sieve truth validated twice against dense all-pairs brute force (0 missed, ≤4% distance error).
- **It is aimed exactly at the live design.** The certificate is still an unbuilt item in both build lanes, and its own lens (`b-coorbital-cert.md`) demands "zero misses … and a dense ring" — a ring with ϖ dispersion fails that by 99%. My jitter sweep pins the safe domain: ϖ spread ≲ 0.05 rad is safe, 0.2 rad already misses 18%. The trigger must gate on periapsis alignment, not concentration.
- **Why not gold:** the author exceeded the deadline before writing `dossier.md` ("Deadline exceeded"), never logged the brute-force validation their own VOID condition requires, and left three out-of-band held-out predictions (RING contacts 10× under, k-for-zero-miss 510 vs 100–300) unacknowledged. Same ruling the integrator gave r3 v3 for a missing record: decisive physics, incomplete record → silver, one step from gold.
