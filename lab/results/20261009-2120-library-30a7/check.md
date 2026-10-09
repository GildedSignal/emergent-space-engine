Grade: silver

**Abstract.** Claim: naive continued-fraction/beat prediction of a pair's next close conjunction misses ~90% (median fA 0.067 at e ≥ 0.25), killing the r8 "next" note's Diophantine shortcut. Reproduced bit-identically (2.5 s); predictions were pre-registered (mtimes 21:24:55 < script 21:26:06 < output 21:27:33). My attacks strengthen the kill: fA stays 0.05–0.083 for windows ±3 to ±15, 0.05 at top 10%, drops to 0.017 under J2-like precession; e-degeneracy confirmed. But predictor B's death mechanism is mis-stated: skinned, it either scans (α ≥ 0.1: index coverage 1.0) or misses (α < 0.1: median recall 0.567 at 66% coverage) — the "≥3× skin" prescription is falsified; the drift-corrected generator is untested. Cost to adopt: one design edit (strike naive CF from r8 v3/v4). Gain: stops a wrong predictor entering the encounters design.

## Reasons

1. **Reproduction.** `cf_probe.py` copied to a clean dir, run twice: output bit-identical to `cf_probe_out.json`, 2.5 s, pure stdlib, seed 20261009. `work/patch.diff` is empty and `git status` shows no tree edits, matching the author's claim.
2. **Pre-registration.** File times prove the order: predictions.md 21:24:55, last script edit 21:26:06, decisive output 21:27:33. P1/P2 failed as pre-registered and the failures are honestly reported as the result; P3 reported as n=3 with no claim; P4 checked trivial (0.033 vs 0.067).
3. **Quote/cache verification.** 11/12 quoted fragments are exact substrings of the cached export; book/highlight counts are exact (770 books, 4,580 highlights). One miss: the barbell quote reads "not **the** elimination, of uncertainty" in Taleb's highlight, "not **an** elimination" in the dossier — a one-word misquote, meaning and attribution intact. P5 "7/7 verbatim" is therefore overstated by one anchor.
4. **Adversarial cases (mine).**
   - Window/top robustness: median fA 0.050–0.083 across WINDOW ∈ {3,7,15}, TOP ∈ {5%,10%}; even WINDOW ±200 gives only 0.40. The CF structure is simply absent.
   - J2-like apsidal precession (gdot 1e-3, 1e-2): median fA 0.033, 0.017 — worse, as the dossier predicted.
   - e-degeneracy: median miss p95/p5 spreads 1.77 → 3.7 → 4.4 across e ∈ [.05,.15), [.15,.30), [.30,.50); "close" is phase-selected only at high e, as claimed.
   - Headline numbers: median fA over the 20 seeds with e2 ≥ 0.25 is exactly 0.067; lin_res/eps is 2.72 median but ranges 1.60–15.89 (dossier says "2.5–12×" — tails understated both sides).
   - Predictor B controls (the lens's blind spot): with a ±3-index skin and the close-set eps, B's predictions tile the axis at fast beats (α ≥ 0.1: median index-coverage 1.00, recall 1.0 — a scan, precision 0.30) and miss at slow beats (α < 0.1: median recall 0.567 at 66% coverage, worst seeds 0.0–0.17; null fixed-grid control recalls 0.517). So B dies in both regimes, but by window-width-and-per-hop drift, not the global linear-fit drift the dossier cites.
5. **Novelty.** No mention of continued fractions, Diophantine approximation or convergents anywhere in docs/HISTORY.md, docs/ or other lab results; the killed premise is the board's own r8 v2 "next" note, still live in the r8 v3/v4 plan. Lessons 2/4 (inversion, barbell) overlap the H0158-era work-allocation principles — the dossier discloses this itself.
6. **Goal fit.** Encounters/q-candidate-degree, the 5 Oct top scaling risk. The kill corrects a live design plan before it is built; PRINCIPLES P9 (a failed experiment kills a configuration, never the method) is respected — the dossier diagnoses which half of the note broke.

Not gold: the probe is a 2-body coplanar toy (K=600, zero precession, no element changes), not the belt rung's own data; lessons 1–4 are unmeasured review rules (analogies, as the dossier admits); and the surviving prescription is wrong (below).

## The one experiment for gold

Run the probe's own escape hatch — a drift-corrected (two-frequency) conjunction generator — on the belt rung's real data with J2 precession and genuine element changes, measuring recall against a scan and work per real encounter. If it holds recall with work/orbit decaying (pay once per element change), the encounters design gets its per-pair predictor; if it dies like the naive ones, "pay once per element change" is killed at rung level. Either outcome, at rung level with pre-registered predictions, is gold.

## What the author missed

- **The operative failure mode of predictor B.** The exact-index metric (no skin) is a strawman no design would deploy; skinned, B fails by *scan degeneracy* (eps ≳ beat hop at moderate e ⇒ windows tile the index axis) and by per-hop drift at slow beats — not by the global drift ratio quoted. The dossier's numbers are right; its mechanism is not.
- **The "≥3× skin" prescription is falsified by its own data structure.** A skin rescues recall only by paying near-scan coverage (91.5% median; 100% at fast beats). What reaches the integrator must be "drift-corrected or nothing", not "or carry a ≥3× skin".
- No cost model: predictions per close event (3.2 median, skinned) is never set against the board's 427 encounters / 1.7M candidate pairs, so the gain of any surviving predictor is unquantified.
- One-word misquote (Taleb barbell), and the drift range stated 2.5–12× where the rows give 1.6–15.9.
