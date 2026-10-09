Working...
Check complete. `check.md` written to the run folder; nothing else touched, no git operations.

**Grade: silver.**

What I did and found:

**Reproduction** — clean copy of `work/` (patch.diff empty), `sh repro.sh`: all 12 runs **bit-identical** to the author's `runs.txt` in 53 s. Every dossier number traces to a reproduced line (μ-decade ratios 83.9/108.9 ≈ 10², slope 2.0 confirmed; floor, naive control, Carlip, E, solar, G, dt-halving all exact). Predictions preceded the decisive runs (mtimes 05:37 → 05:49 → 05:51).

**My attacks** (6 runs, scratch in `/tmp/check93a4/work`, regenerable from one-line seds documented in check.md):
1. **Isolation control** (sources slaved to truth — the control the author lacked): the pure read error is **flat at 3.32e-7 over 30 orbits** (μ=1e-3) and bounded at 5.11e-5 (μ=1e-2). This *proves* their chaos attribution: the free-run growth was inter-law source divergence, not the read. Strongest possible support for the central claim.
2. **Crossing reader R=2**: dE → 9.95e-2 monotone — the frozen kill criterion's letter fires; physics is encounter-chaos metric saturation (truth self-exchange 0.37 vs the 1e-3 threshold).
3. **Close sources rJ=1.2rS**: mutual tube read diverges (dS/rS → 4960) — the encounter regime law.md assigns to changeovers, not tubes.
4. **μ=1e-2 R=5**: monotone to 2.3e-2 — trips the letter cleanly (their own case E at R=10 also trips as written).

**Novelty/goal** — kicked-source edge genuinely untested by `q-gravity-at-c` (free-fall only) and memo R5; rung-gap audit verified (no r5/r6 in `lab/rungs/`, no B-gate covers retarded reads, contact-frame id-rule gap real). Not gold: no 10× move, nothing built deleted, premise confirmed rather than broken, and the "survives in-domain" headline needs the encounter qualifier.

**Gold path**: make the isolation control the decisive metric, add an encounter clause to the kill domain (mirroring B12/B13's oracle-domain exclusions), freeze the proposed two-sided rung — one step.
