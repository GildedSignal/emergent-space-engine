Working...
Check complete. `check.md` written to the run folder; nothing else touched, no commits.

**Grade: silver.**

**Reproduced (clean tree, empty patch):**
- B13 at N=7 (60/64, worst 2.12e-2) and N=9 (58/64, 1.77e-1/1.28e0) — bit-identical to the logs; same 9 replaced draws at every N. The non-convergent refinement is real and deterministic.
- Kick bench: replay digest identical, median 44.2 µs (author 43.4), cycle_rebinds 23/23, zero memo reuse — confirmed.
- B14 N=3 timeout (60.1 s), which the author's killed sweep never logged — verified on their behalf.
- Predictions timing checks out (08:42:59 vs sweep 08:43:36); the pre-registered knee hypothesis is honestly reported killed.

**Why not gold:**
1. **B14 N=2 doesn't reproduce.** The dossier's load-bearing "completes in 59.75 s, 243/255, apsides 0/53" is in no log file, and both my runs (one isolated) hit `FAIL timeout` at 60.0–60.1 s — a 0.25 s margin against a frozen 60 s wall limit flipped under checker load. The behaviour numbers are unverifiable; "the only cadence its budget admits" is false here.
2. **The mechanism sentence is wrong.** The tree ships `b13_by_draw`; running it shows the N=9 failures are refusal-driven (`Space(NoBoundOrbit)`, 10–330 refused kicks, including draw #40 at q = 39 R_p — a far flyby), not "the 2–6 deepest flybys", and the failing set isn't stable across cadence (N=7: {18,27,50,57} marginal, zero refusals). The cadence-independent floor stands, with a better explanation the author's own named check would have found.

**Gold path:** record B14's verdict at an admissible cadence (oracle/law cost separation or a quiet logged run) and fold in the refusal mechanism — then "no fixed cadence passes the plane's frozen gates" stands on two regenerable pillars and re-aims board focus #1 as the dossier argues.
