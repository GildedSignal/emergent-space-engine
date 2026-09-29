# check.md — 20260929-1832-rung-kepler-kill (directed rung canary)

**Verdict (lab/verdict.py on metrics-check.json): KILL; killed: euler** — `euler candidate fail B1`, `frozen negative fail R1`. With the author's metrics.json as the second file: same KILL, zero outcome differences, so no DISPUTED. This is the canary's expected verdict, and the negative control failed a criterion, so the test has teeth (not VOID).

## Abstract (for the integrator)

Canary kepler-kill reproduced exactly and independently: forward Euler at h = T/200 unbinds the e = 0.5 Kepler orbit at step 15,547 (bound_fraction 0.007773 → B1 fail) after 3.475 revolutions; the frozen control fails R1 with 0 revolutions. The author's script reruns byte-identical and deterministic (1.9 s); my from-spec implementation agrees on every metric. The one deviation — window 0 also collecting steps below 0.1·t_end, exponent −2.9e−4 versus −1.1e−9 strict — changes no criterion outcome. Nothing to adopt: the rung kills a configuration (forward Euler at this h), as designed. Rung-design note worth keeping: E1's last-90% windows are blind to drift that finishes by orbit 78; B1 carried the kill alone.

## Reasons

**Reproduction.** Copied the author's `kepler.py` to /tmp (it writes outputs beside itself; the author's folder was not touched), `patch.diff` is empty and the tree is clean apart from untracked `lab/results/`. Output `metrics.json` byte-identical to the author's; a second run `cmp`-identical (deterministic). Diagnostics match the dossier: escape at orbit 77.735, r > 4 at orbit 3.135, E_final +0.0369, r_final ≈ 1.70e4, L 0.8660254 → 1.40209 (+61.9%).

**Independent implementation.** I wrote a second implementation from `lab/canaries/kepler-kill.md` only (different structure: strict windows, alternative revolution counter). Agreements: euler first unbound step 15,547 (bound_fraction 0.007773), steps_per_orbit 200.0, orbit_closure_count 3 (3.4750047834 rev); frozen exponent ~0 (−4.2e−29 vs author's −3.7e−13 — both floating-point noise at the 1e−16 floor), bound_fraction 1.0, steps 200, closure 0. The rung file is committed (6b22aee) and byte-matches the frozen text in my prompt.

**One deviation found (reported, not fixed).** The spec says the 20 windows span "from t = 0.1 t_end to t_end (the last 90% of the run)"; the author's window 0 also collects steps 1…0.1·t_end. Strict windows give euler exponent −1.08e−9; my replication of the author's boundary matches his −0.0002919153602862 to 13 digits, isolating the difference to exactly this convention. Outcome-neutral: both ≪ 0.2, and the frozen window maxima are identical either way.

**Oracle values.** E0 = −0.5, L = 0.8660254037844386, T = 2π, apoapsis 1.5, initial speed √3 — all verified exactly. One nit in the rung text, not the author's work and unused by any metric: float64 `L/1.5` is 0.5773502691896257; the rung prints …258 (a correctly-rounded decimal of √⅓, one ulp above the double).

**Held-out predictions.** `predictions.md` mtime 18:38:12 precedes the final `kepler.py` 18:40:33 and its outputs 18:40:39 (`run.log` created 18:32:31). All qualitative predictions held: euler fails B1, euler passes R1 and E1 (≈ 0), frozen fails R1, steps_per_orbit 200 for both. The quantitative miss (unbind in 4–15 orbits predicted vs 77.7 orbit-units measured) is honestly reported in the dossier. I verified the mechanism claim: measured one-step dE > 0 at all 10 sampled exact-orbit states (periapsis to apoapsis, both velocity signs), consistent with the author's h²(r − 0.375)/r⁴ sign analysis.

**Adversarial checks.** (1) Strict-window recomputation (above). (2) Second revolution counter — unwrapped polar angle vs atan2(cross, dot) — agrees to 5e−12 revolutions, so closure 3 is robust. (3) Double full runs, byte-identical. (4) Independent first-steps update straight from the rung sentence "x += h v and v += h a(x) both from the old state": dE = +1.96e−2 after one step from periapsis — the drift is immediate and outward. (5) Interpretation adjacency: bound_fraction as (n−1)/N vs n/N gives 0.007773 vs 0.0077735; every failure is far from its threshold (B1: 0.0078 vs ≥ 1.0; R1: 0 vs ≥ 1) and every pass far inside (E1: ~1e−9 vs ≤ 0.2; C1: 200 vs ≤ 256). No reading I tried flips any outcome; the KILL is robust.

**Novelty.** No HISTORY entry (searched for canary/rung/verdict/Kepler; recent tail checked separately) or doc runs this canary; verdict.py and the kepler-pass/kepler-kill rungs were committed one commit before this run (6b22aee). The physics conclusion is textbook and consistent with the board's stepping picture (probe 1, H0190, Calvo & Sanz-Serna prior-art scout) — the canary claims no new physics, only calibration of the checker lens, and that is what it delivered.

**Goal fit.** PRINCIPLES #9: "A failed experiment kills that configuration, never the method" — exactly what verdict.py returns, and only the configuration (forward Euler at h = T/200 on this case) dies. Per lab/README "Canaries calibrate the checkers": this rung exists to grade a checker lens, and it forces the checker to reproduce, attack and run verdict.py. Fit is correct.

## What the author missed

- The window-0 boundary deviation from "the last 90% of the run" (outcome-neutral here, but it would matter for a metric whose early window maxima differ from late ones).
- The E1-blindness point he raises is stronger than stated: it is not specific to this rung — any rung whose drift completes inside the first 10% of the run gets an E1 pass by construction. The integrator should decide whether future rungs compute the exponent over windows that start at first escape (or before it), since B1 then carries the whole kill.
- Cosmetic: the rung text's apoapsis-speed oracle is one ulp above the float64 value of L/1.5 (see above).
