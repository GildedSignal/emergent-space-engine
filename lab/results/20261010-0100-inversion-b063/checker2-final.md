Working...
**Grade: gold** — written to `lab/results/20261010-0100-inversion-b063/check2.md`.

**Reproduction:** clean copy in `/tmp/check2`, empty `patch.diff`; `harness.py` (13.3 s), `s2_hot.py` (7.7 s), `probe_crossing.py` (9.3 s) — `metrics.json` and `s2_metrics.json` **byte-identical** to stored. Timestamps confirm pre-registration (predictions 01:09 → metrics 01:12:51 → dossier 01:20).

**My adversarial attacks (all under 2 GB, ~22 s):**
1. **Kill robustness** — fresh seed 42, cold fleets e=0.05, small Δϖ: M-ordering catch@4 = 0% in every variant; failure is continuous in crossing angle.
2. **Strongest gold defense closed** — the λ-ordering's 100% catch at lead=P is an exact-equal-a periodicity artifact; with per-fleet a-spread = ρ (still inside the cone) no lead in P…P/1024 rescues either ordering (M 0%, λ best 8.7%).
3. **Control on fresh seed** — S0 intact at ρ=1e-4; at ρ=1e-3/lead=P it decays (0.909, k99 7 ≈ stored 6): rank-4 is a scene artifact, as claimed.

**Novelty/goal fit:** no H entry inverts gold `20261006-0346-taleb-09b5`; its premise still lives verbatim in `lab/lenses/b-coorbital-cert.md` and `lab/queue.txt:10` (build in flight) — the correction (certify crossing-freeness via the cone's own outputs; k = law of ρ·n·lead, O(10²) at 10⁶) adopts before landing at zero code cost. Premise of an adopted gold shown wrong + reproduced + predictions substantively held = the gold bar.

**Recorded blemishes:** stale S0 guard after a disclosed post-prediction scene change (±ρ/4→±ρ/2, 98.8 vs ~37/orbit bound); P3 counted held despite the degenerate lead=P corner; headline "95–100% miss" is 52% in the most favorable corner; "64 sorts/orbit" assumes full re-sorts; scenes all coplanar/prograde — retrograde counter-fleet untested; empty `run.log`.

One disclosure: my directory-wide novelty grep surfaced a few lines of `check.md`/`checker-final.md` before I could exclude them. I did not use them; every number and the grade above come from my own reproduction and probes.
