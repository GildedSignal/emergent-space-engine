Working...
Check complete. `check.md` written to `lab/results/20261011-1814-spacex-a110/`; nothing else in the run folder was touched.

**Grade: gold.**

**What I verified:**

- **Reproduced exactly, from the dossier's commands in a clean /tmp copy** (no patch needed — `work/patch.diff` is empty): the full probe2 table (convoy encounters 39/535/542/536 at σ_e=0/0.003/0.01/0.03, rank max 3/7/11/21, frac≤4 1.00→0.56; ring 1.00→0.54) and the falsification (synodic engine 0 vs integration 125). The dossier's "116"/"125" ring totals are probe2's births-excluded 91/124 plus t=0 births — consistent.
- **Adversarial cases, all supporting the claim:** dt-sweep converges upward (94→125→131→133, so dt=0.05 undercounts ~6% — channel real); frac≤4 = 0.55–0.64 across four seeds; mechanism confirmed on a 7.6e-5-miss pair (|Δλ_mean| 0.0134 inside the 0.059 band, mean longitudes ~745 orbits from meeting); the 78 mean-longitude events in the window contain **0** encounters — all encounters are epicyclic, stronger than the dossier's "~8 synodic" estimate; rigid and weak-differential precession change nothing; n=2048 confirms the fleet-scale formula as a median (predicted k=9.2, measured median rank 9) and confirms per-body encounter rate ∝ n·σ_e (0.26→1.97/body/orbit).
- **Novelty:** no HISTORY/docs entry qualifies taleb-09b5's rank-4 claim with e-noise or gives the timing machinery a band term; `crates/shipmem/src/pop.rs:167-184` births convoys with per-member e/l/w jitter, so the "fleets have e=0" hidden requirement is real and false.

**Defects recorded (cost the record, not the claim):** the retracted `results.json` is not bit-regenerable — `abs(hash(name)) % 10_000` is PYTHONHASHSEED-salted (verified: 7230/9305 across processes); its one still-cited number (cone ≈ 4095/4096 pairs) regenerates and is seed-insensitive. The "~8 synodic" is an unmeasured (conservative) estimate; the pre-registered predictions were voided by the author's own broken instrument, which they caught, disclosed, and retracted — the 5 October lesson applied correctly.

Gold because it shows a premise of an adopted gold is wrong (the certificate silently drops 44% of fleet encounters at σ_e=0.03; mean-motion timing under-enumerates 0-to-125), reproduces exactly, survives my attacks, and is adoptable in one step: size the certificate's neighbour set or cadence by the epicyclic band and add the band term to conjunction timing, inside `b-coorbital-cert` before it freezes.
