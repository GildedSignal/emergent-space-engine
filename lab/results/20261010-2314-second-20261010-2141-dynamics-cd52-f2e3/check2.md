Grade: gold

**Abstract.** The silver's record now regenerates (`fit2.py` → byte-identical
`results2.json`; the shipped `fit.py` regex parsed only 6 of 19 rows, E1/E2
absent), and the checker-named experiment splits the claim — confirmed under
attack: λ is dt-rising at every cell (held-out seeds 4/5: ratios 1.51/2.17;
s2048 continues the rise; my fixed-K probe keeps 72–80% of λ for 10× smaller μ
at K = 0.39), so "manufactured chaos" is dead and λ_max ≈ 0.1–1 Ω, monotone in
K, is the belt's real surprise floor; meanwhile μ=1e-4 stays corrupt even at
s1024 (fb 1.3e7), so no fixed-cadence point stands there and K ≲ 0.1 becomes
the changeover trigger. Adopt: the ~free conjunction census + two gate radii in
`xtask universe --bench`, K as the regime trigger, scar cadence from λ(K).

**Reproduce.** Clean tree, `patch.diff` empty (0 B). Built `belt2.c` fresh
(selftest 1.636e-11 / 1.031e-10). Reproduced bit-exactly, cross-machine: all
five anchors (neg, pos_s1, n200_s1, m5n200_s1, wm5_s1) — RESULT lines match
`matrix2_raw.log` rows and curve files are byte-identical to the author's `a_*`;
the full decisive matrix (B/C/D/A + heavy, 41 runs) — every RESULT/CONJ line
identical to the four raw logs, all 40 `r2_*` curves byte-identical;
`python3 fit2.py` → `results2.json` byte-identical (E1 ratios 0.12/0.53/0.51/
0.29/1.00, E2 α = 0.821, R² = 0.799); `python3 analyze.py` → `analysis.txt`
byte-identical. The census provably leaves the dynamics untouched (`belt2
--conj` ≡ `belt_lyap`). The shipped `fit.py` bugs are real: its `[\d.e-]+` regex
parses only 6 of 19 RESULT rows (exactly the clean seed-2 rows; even
`dH = 0.000e+00` is dropped), E1/E2 absent from the shipped `results.json`;
and it read pre-fix `{label}_s*.dat` curves (cad128 had none). The `cad64` rerun
is bit-identical to `matrix2`'s `n200` row, as claimed.

**Predictions.** `predictions.md` (23:21:01) predates all decisive logs
(23:24:37+); the anchors it discloses ran first (23:19:45–58). Verdicts match
the dossier's honest reporting: P6/P7/P8 HELD; P2 failed upward — the
pre-registered discriminator ("falls ≥ 30% monotonically") is excluded at every
cell; P3/P4/P5 failed as universals and are reported as failures.

**Attack (four cases, none seen by the author).**
1. *Held-out seeds 4, 5* (N=200, μ=1e-5, T=50): λ_exp 2.52/2.43 (s64) vs
   3.80/5.25 (s1024) — dt-ratios 1.51 and 2.17; no collapse out of sample.
2. *Fixed-K probe* — the experiment the dossier names but does not run: N=158,
   μ=1e-6 gives K = 0.392 ≈ n50/μ=1e-5's 0.391. λ_exp ratio 0.72 (s64) / 0.80
   (s1024) for a 10× mass drop at fixed K (against 0.38 along the author's
   fixed-N axis), dt-rising (1.31→1.65), census clean: WT mass-insensitivity
   approximately holds at fixed K — the missing leg of the refutation.
3. *s2048* (N=200, μ=1e-5, T=25, s1): λ_exp 4.71 vs 3.79 (s1024) vs 2.67 (s64)
   — the rise continues, no plateau, no collapse; the census sampling bias is
   live (n_sqrt 0→2 from s1024→s2048).
4. *μ=1e-4 pushed to s1024* (T=200, s1; author stopped at 256): still deeply
   corrupt — fb 1.28e7, dH 2.17, n_sqrt 11, λ_exp 165 (the gate flags it). "No
   clean fixed-cadence operating point at μ=1e-4" extends beyond the tested
   range.

**Novelty.** No λ/belt-surprise measurement exists in docs/HISTORY.md (belt
entries are the memory program, gold 20261006, and B18b's frozen gates). The
changeover line (r10 KILL, q-changeover/JANUS) gains its first dimensionless
trigger, K ≲ 0.1; Wisdom–Tremaine is cited literature, not internal prior art.
The run overturns the predecessor silver's load-bearing mechanism claim on that
run's own instrument.

**Goal fit.** Board focus: the changeover's domain and "10⁹ in 8 GB … decided
by distinctions created per game-second" — this measures that floor's magnitude
and its regime trigger. PRINCIPLES 4, "Regimes are chosen by dimensionless
numbers" (K chooses fixed-cadence vs changeover); 3, "Compute only surprises"
(the floor is physical, not the integrator's); 22, "the simulation tells us
what's next not us". Cost to adopt: census (~free) + two gate radii in the
bench; one step.

**Gold because:** fully reproduced bit-exact; it shows a premise is wrong (the
silver's "manufactured chaos" mechanism) with a regenerated record, replaces it
with a measured, monotone-in-K physical floor, and is adoptable within one
step. Every number I regenerated or attacked — the author's never-piloted
seeds, a finer step, a fixed-K cell, μ=1e-4 at s1024 — agrees with the
dossier's claims.

**What the author missed.**
- Prose slips, none load-bearing: "5 of 11 labels" (the shipped results.json
  holds 4; a rerun parses 6); "dH 0.16–33" (cad8 seed-level reaches ~69; 33.07
  is cad64_s1 only); "n_sqrt = 5–15" (observed 5–10 in this run's μ=1e-4 cells).
- λ's estimator is not shown to converge: still rising at s2048 (4.71), so the
  floor values are lower bounds; no exponent spectrum/KS entropy (inherited).
- The pre-registered REFUTED condition (P2 ∧ P4 ≥ 0.6) was not met as written
  (P4 = 0.38): the refutation rests on the dt-axis plus the K-correction, whose
  fixed-K leg the author only named — supplied by check 2 here.
- The census detector bias across cadence (admitted) is visible in the s2048
  run; gate-passing at fine cadence undercounts dips between steps.
- The anchor runs were not logged (only curves survive); `matrix2b_raw.log` is
  an extraction — verified faithful, byte-for-byte, against `light2_raw.log`.
