# Dossier — 20261012-0138-library-060f (lens: Julien's library)

**Claim:** B12-v2 should classify the Jacobi error series by the scaling of its range (a
Hurst-type Ĥ over dyadic tail octaves, per seed, verdict on the median seed, thresholds frozen
from a planted calibration) instead of a global growth exponent: on a planted calibration the
classes order monotonically with **zero per-seed overlap** between bounded and compounding
(Ĥ q90 = 0.009 vs q10 = 0.38), where the current exponent's threshold lands on a class median;
and the held-out failures freeze a design requirement neither B12 nor the recurrence ratio had —
**the instrument must state its discrimination horizon**.

**Bottleneck:** the instrument (HANDOFF risks: "B12 cannot yet tell bounded from compounding
error on chaotic ships"; redesign in flight as `q-b12-design`/`b12-v2`; H0215: the current
statistic "was shown to rank a bounded error above a compounding one"; taste log 6 Oct: the
recurrence-ratio fix "does not separate a slow leak from a bounded error"). Gain: unblocks
judging every motion-law change; deletes the per-run re-litigation of what "bounded" means.
Not the board's #1 compute bottleneck — argued for because it gates all of them and its redesign
is open now. All 14 build lenses were already assigned; this targets none of them.

**Evidence** (`python3 probe_b12.py`, 4.5 s, numpy 1.26, 64 seeds × 2¹⁴ samples per class,
seeded deterministically; full numbers in `probe_b12_metrics.json`):

| class (held-out*) | Ĥ median [q10,q90] | Ĥ verdict | gE median [q10,q90] | current verdict |
|---|---|---|---|---|
| bounded_band | 0.007 [0.00,0.01] | bounded | 0.122 [0.117,0.132] | pass |
| bounded_osc_noise | 0.045 [0.03,0.07] | bounded | 0.053 [0.031,0.083] | pass |
| diffusive_leak | 0.556 [0.38,0.68] | compounding | 0.529 [0.355,0.715] | fail |
| linear_leak | 0.424 [0.40,0.45] | compounding | 0.491 [0.473,0.508] | fail |
| explosive | 1.236 [1.24,1.24] | compounding | 0.752 | fail |
| *near_unit_root (AR ρ=.995) | 0.184 [0.12,0.25] | bounded | 0.202 [0.120,0.281] | fail (on the median) |
| *reflected_rw (walls ±80σ) | 0.414 [0.25,0.56] | compounding | 0.369 [0.226,0.474] | fail |
| *bounded_plus_jumps | 0.370 [0.12,0.82] | compounding | 0.523 [0.171,0.712] | fail |
| *sin_drift (drift ≪ band) | 0.041 [0.04,0.05] | bounded | 0.073 [0.070,0.078] | pass |

- Ĥ separates the calibration pair with no per-seed overlap (0.009 vs 0.38) and a monotone
  ordering over six classes (0.007 → 1.24). The current exponent compresses the same classes into
  0.05–0.75 and puts its 0.2 threshold on near_unit_root's median (0.202): per-seed intervals
  overlap across the bounded/leaky boundary there ([0.120,0.281] vs reflected_rw [0.226,0.474]).
- On these synthetic classes the current gate's verdicts happen to agree with Ĥ's on 8 of 9
  medians (my attempt to reproduce H0215's misranking with a fast-ramping band did not trigger
  it: gE 0.122 < 0.2). What is demonstrated is the margin, not a misranking count.

**Predictions** (`predictions.md`, written before the run): of 8 quantitative predictions, 3 held
(bounded, diffusive, explosive calibration bands; reflected_rw's value), 5 failed, each carrying
information: (a) linear_leak lands at Ĥ 0.424, not 0.9–1.05 — the noise I added compresses range
slopes; verdict still correct. (b) near_unit_root reads bounded (0.184) — correct per asymptotic
theory (correlation time 200 ≪ horizon 16 384); my prediction overestimated its memory. (c)
sin_drift reads bounded because its drift (0.33 of the band over the run) is below detection at
this horizon — both statistics miss it. (d) bounded_plus_jumps reads compounding (0.370 vs the
0.33 threshold, spread [0.12,0.82]): localized jumps inflate the tail slope; **both** statistics
fail this class. (e) The floor/stride sensitivity moved gE only 0.122→0.142 (≪ 0.2), so the
"sampling frequency" caution is not supported by this probe's max-accumulate form.

**What would make it wrong:** the synthetic classes mis-model the plane's real error series (the
real test is the plane's Jacobi series on the M1 — not run here, no such series in this tree);
the jump failure (d) is exactly the re-anchoring mechanism law.md adopts (re-compiling at
√(floor/C) accumulated offset), so a law with healthy re-anchoring could be failed by Ĥ as built.
**Cost of adoption:** small — the statistic is ~30 lines, no dependencies, deterministic; B12-v2
wires it as the exponent's replacement plus a horizon line in the gate text (T ≥ ~10× the
perturbation correlation time; drift detectable at c·T ≳ band amplitude). **Fit with
PRINCIPLES:** "Errors never compound... types of errors and not just errors" (13) — Ĥ measures
the type; "Write the kill criterion before the run, with controls on both sides" (heuristic) —
planted calibration pair, one of which (jumps) currently kills it; "a game is an illusion
spectacle, the oracles are guards, not shepherds" (34) — the gate states its horizon instead of
pretending omniscience.

**Named next experiment (the silver→gold step):** make the range jump-robust (e.g., trimmed
window ranges or two-octave local slopes) until bounded_plus_jumps separates with margin, then
wire Ĥ + the twin arm into `behave` B12 and run it on the plane.

**The lens:** Julien's library is Taleb-rich and physics-poor — it yields classification,
shock-testing and anti-overfitting discipline, but not the numerics (shadowing, backward error),
which the b12 builders know better; the quotes' authority is Julien's reading, not evidence. The
bigger miss: with 60 minutes I probed one statistic on synthetic series and never touched the
plane — an author with engine access should reproduce the margin on a real error series before
any freeze.
