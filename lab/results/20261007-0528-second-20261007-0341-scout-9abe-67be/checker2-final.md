Working...
Check complete. Summary of the blind second check:

**Grade: gold** — written to `check2.md`.

**Reproduced (clean tree, shipped code only):**
- Scout record (`cadence.py S2c,S2d,S2c2,S3,S4`, 7.8 s): 60 diffs, all `wall` timings, zero physics diffs.
- Decisive lattice (`lattice.py full`, 80 s): 104 diffs, **all** wall fields — bit-identical physics.
- All headline numbers recomputed with my own code from the stored record: 29/30 first-order uncertifiable (one fluke, FIXED-64), 17 certifiable, baseline 466.8 vs oracle 409.6 evals/orbit → 1.140× evals / 1.237× kicks, winner counts exact, TRIG2G holds nowhere; gatesens 17/25/38 certifiable at cuts 1.14/1.18/1.05×.
- Precedence bug verified numerically (`2**(2/3)**1.5` = 1.4583 → n_per 0.68571; −2.285 W to 3:2, +0.981 W for S2d). `layer2` ≡ shipped layer on 22 policy-scene pairs.
- Pre-registration holds on mtimes: predictions.md (05:38:24.7) precedes out_full.json (05:39:53), pilot disclosed.

**Adversarial (3, all strengthening):** truth converged at 3× resolution at both centres; FIXED-128/256 and a finer trigger floor still fail at first-order centres (structural, not policy-set-limited); μ-scaling puts the violent-zone boundary between 1e-4 (still dead) and 1e-5 (FIXED-16 holds), quantifying the author's disclosed caveat.

**Two prose defects found (reported, headline-neutral):** "5:3: 0 certified" is wrong by the run's own gate (2/15 hold, both phase π/2, already inside the 17), and "AVG" is a midpoint-sampled kick, not the orbit-integrated compiled average the dossier invokes for S3.

Nothing else in the run folder was modified; scratch work stayed in `/tmp/chk2`.
