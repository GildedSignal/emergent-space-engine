# Dossier — 20261015-0250-second-20261015-0128-inversion-3ca8-f50d (second author, inversion lens)

**Claim.** The checker's named experiment is done and the claim inverts to gold as they
predicted: with the twin rebuilt as the **exact continuum limit of the shipped rule** —
the receding-skip gate mirrored and the law's own reflection (f64 Householder about
N = (d·P_s, E_tot·d), validated per-contact to ≤ 2.5e-6 rad at every impact parameter) —
the shipped dense-order engine **matches its own continuum limit on every class metric,
in every scene and seed tested**: quantization is innocent at the ensemble level. The
first run's 15–45% deviations and 5× max-dwell were instrument error (its twin reflects
crossed-in-bin pairs the engine skips, and reflects about the SR COM mirror rather than
the law's tilted axis). The dense order's real fast-contact semantics stands: **87.5% of
detected contacts in the relativistic gas exchange no impulse** (bin-crossing
pass-through, Q-independent; 57–61% in the two-body pump; 85.6–88.8% across scenes), and
the checker's unattributed neg-scene residual was the final-γ phase snapshot of a
ceiling-trapped light (my `srskip` arm reproduces their 247 exactly; all four neg arms
agree within 2% on dwell and max γ).

**Bottleneck.** Truth risk "a law that mints false behaviour classes", the inversion
list's #1. This closes the chaos-shadowing page's open direction 1 (the exact twin) and
prices direction 3 (the tilted axis: with the skip held fixed, replacing the law's
reflection by the physical one shifts max-dwell by 0.67–1.13× — inside trajectory
scatter in these scenes) and most of direction 2 (pass-through measured across five
scenes; game-scale pricing still open). It also deletes, with a valid instrument, the
"raise Q to heal dense-order classes" adoption path the first run refuted against the
wrong reference.

**Evidence.** All numbers from `sh regen.sh` (≤ 9 min): shipped `Chronon` under
`Law::RelativisticV1` vs the `exact` twin, `cargo run --release -p emergent-lattice
--example shadow2 -- <scene> <arm> <q_log2> <t_log2> [seed]`; the full table is
`out/table.txt`, built by `table.py`. T = 2²⁰ chronons, Q = 2²⁰ unless said.

- **Instrument validated four ways.** (i) *Glancing micro* (the first run's named missing
  probe): engine vs `law_reflect` agree to ≤ 2.5e-6 rad and ≤ 1.1e-6 β at every
  impact parameter u = b/reach ∈ {0, .2, .45, .54} and incoming β ≤ 0.999 (Q = 2²⁰) —
  the lattice rounding scale; `sr_disc` (the physical mirror) differs from the law's
  reflection by up to **0.155 rad** oblique and coincides head-on, reproducing the
  checker's tilt. (ii) *Pre-contact identity*: neg scene, T = 2⁹/2¹⁰: engine and exact
  identical to the printed digit (γ 1.00005, heavy 1.25000, 0 contacts). (iii) *pos
  control* (equal masses, β 0.05): contacts 4452 v 4397 (1.013×), final γ quantiles
  equal to 4 decimals. (iv) *The float twin reproduces the first run* (pump s1:
  trapped 45 v 58, dwell 0.830×, max dwell 5.51× short — their 5.3–5.7× band).
- **Decisive (pump, 1000:1, β 0.6, 64 lights, seeds 1–5), engine v exact:** trapped
  45/53/52/52/45 v 49/49/50/50/47 (|Δ| ≤ 8%); dwell-γ2 totals 794–807k v 800–808k
  (0.987–1.008×); **max continuous dwell 102/122/108/127/123k v 126/97/159/130/97k
  (0.68–1.26×, both signs — the 4.8–6.2× artifact dies)**; contacts 0.997–1.006×;
  final γ p50 0.86–1.12×; pass-through 87.49–87.60% on all five seeds.
- **Q-flat against the correct reference:** the exact twin is Q-free (bit-identical at
  any q_log2); engine at Q = 2¹⁶/2¹⁸/2²⁰ v it: trapped 51/55/45 v 49, dwell
  801/807/794k v 805k, max dwell 105/110/102k v 126k, contacts 280.1/279.6/279.2k v
  280.1k. Flat.
- **neg (two-body pump, all four arms):** engine / exact / float / srskip: dwell
  1032/1017/1042/1042k (97–99% of T), max γ 251.0/246.6/250.6/250.5, contacts
  499/562/542/530 — one class; contacts spread ±12% (trajectory decorrelation). Final γ
  151/34/187/247: a phase snapshot, not a class metric (the checker's "247 v 151
  unattributed residual" is this snapshot; my srskip arm lands on their 247 exactly).
  Pass-through 57–61% in the skip arms.
- **New scenes.** `soft` (100:1, β 0.8, seeds 1–2): trapped 19/22 v 23/27 (−17/−19%),
  dwell 1.023/1.005×, max dwell 1.041/1.238×, contacts 1.000/1.002×, pass-through
  85.6%. `tall` (128 lights, 512×8): trapped 82 v 83, dwell 1.020×, max dwell 1.091×,
  contacts 1.0004×, pass-through 88.8%.
- **Tilt isolation** (`srskip` v `exact`, skip held fixed, pump s1/s2): max dwell
  84.4/110.3k v 125.9/97.4k, trapped 45/50 v 49/49, dwell 799.7/796.1k v 804.5/805.3k —
  the tilted axis moves ensemble statistics by less than seed scatter here.
- **Ledgers exact:** every engine residual finite (checked programmatically).

**Predictions** (`predictions.md`, written before the decisive run): 5 of 7 held — pos
control (1.3% v predicted 5%), pump all bands (trapped ±8% v ±20%, dwell ≤ 1.3% v 10%,
max dwell ≤ 1.26× v 1.5×, contacts ≤ 0.6% v 5%), Q-flat, new scenes within bands,
ledgers. Missed: (a) neg final γ "within 1.15×" — measured 4.42×, and the miss is the
metric's, not the twin's (max γ 1.018×, dwell 1.014×); (b) I predicted pass-through
highest in `soft` (fastest heavy); measured 85.6% < pump 87.5% < tall 88.8% — the rate
tracks the lights' closing-speed distribution, not the heavy's β alone.

**What would make it wrong.** The twin mirrors `resolve_law`/`chronon::step` as read at
the base commit (234d0182; the patch touches no library file) — a law change voids it.
The domain is Fermi-pump gases: mass ratios 1:1 to 1000:1, β ≤ 0.8, ≤ 129 bodies, one
channel geometry family, T = 2²⁰, five seeds; ultra-relativistic (γ ≫ 250), cold dense
gases, and resonant three-body regimes are untested, and the tilt's ensemble effect is
bounded only by trajectory noise here (a systematic shift below ~20% would be invisible
to this design). Batch interactions with > 2 bodies per bin are validated statistically
(contacts 1.000× in soft/tall), not per-event.

**Cost of adopting / consequence.** Nothing to adopt in the engine. The `exact` arm is
now the reference instrument for the page's open direction 4 (freeze the
trapping-statistics rung on the shipped law, 5cad's missing rung): the rung's positive
control is engine v exact on these metrics, its negative the first run's float twin
(must fail by ≥ 4× on max dwell). The pass-through rule property (87.5%) is the number
the integrator should price at game scale (flyby closing speeds inherit the skip).

**Fit with PRINCIPLES.** "A failed expectation is not automatically a failed method:
diagnose which one broke" (H0183): the first run's headline failed because the
instrument broke, and the method (continuum twin + class metrics) now stands validated.
"we want determinism ≠ realistic trajectories" (#20): held here in the strongest form —
trajectories decorrelate (neg contacts ±12%) while every class statistic tracks the
continuum. "A test that cannot fail is a control" (#10): the micro table can fail and
did, on my own print bug (heavy v light column swap), before any ensemble number was
taken.

**The lens.** Second authorship: I inherited the question and the instrument's skeleton;
what I added is the exact continuum limit and the scene/seed spread. What this lens may
have missed: I did not sweep impact-parameter distributions inside the many-body scenes
(the pass-through rate is measured, its geometric decomposition is not), and I priced
the tilt only through max-dwell scatter — a targeted tilt sweep (fixed seeds, tilt on/off)
would bound it more tightly if the integrator intends to correct the reflection.

## Reproduction

`sh regen.sh` from the run folder (~9 min, one process at a time, < 100 MB each):
rebuilds `shadow2`, runs micro, pre-contact identity, all controls, the five pump seeds,
the Q arms, `soft`, `tall`, and prints `out/table.txt` — every number above is in it.
Raw JSON per arm beside it in `out/`.
