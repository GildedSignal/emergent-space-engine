Grade: silver

**Abstract (for the integrator).** Claim: the encounters tier's three adopted parts do not
collapse into one storeless watch; the per-body equation-of-center band (2N certificates,
zero setup) is a sound necessary filter but misses tangency-dip encounters, firing the
pre-registered kill. Reproduced bit-for-bit from the dossier's commands (all four scenes;
27 s + 48 s). I re-adjudicated 5 of the claimed REAL misses with my own 4M-point sampler:
all real; the (13,134) dip verified root-for-root (roots 0.1254 apart, d≈1.4e-3 each, true
min 8.1e-5 between). My adversarial scenes strengthen the kill: highe 54% missed, resonant
80%. Gain: the tier's O(N²) store is measured deletable (cone pairs 0.14–0.69·N²/2 vs 2N
certs) and its windows are exonerated as second-order structure. Cost to adopt: the hybrid
fragment is proposed, not built. Not gold: two table cells the shipped code contradicts
(epochs/body "5.3" vs actual 13.17; cl_caught "1" vs 0) and a silently dropped prediction.

**Reasons.**

1. **Reproduction (exact).** `python3 watch.py uniform:250:1 uniform:500:1` and
   `phalanx:250:4 clumped:250:3` in a clean copy regenerate every stored cell (wall times
   differ ≤0.1 s). Encounters, misses, evals/enc, cone pairs, pp_evals max all match.
   patch.diff is empty (all work inside the run folder; nothing to apply).

2. **The kill is real and honestly earned.** predictions.md (14:08) predates watch.py
   (14:22) and metrics.json (14:24). P1 was pre-registered as the kill and fired. I
   independently re-adjudicated 5 misses across three scenes with my own sampler: min
   distances 8.10e-5, 6.64e-5, 5.87e-6, 6.17e-5, 1.44e-5 — all < ρ, matching the author's
   adjudication. The diagnosed mechanism is verified: two alignment roots 0.1254 apart with
   d≈1.34e-3/1.45e-3 at each, the true minimum 8.1e-5 between them with |ΔΛ| = 7.7e-5 rad
   and no crossing — a tangency, exactly as reported. P2 and P6 held (conjunction-less
   6.9% belt / 37% phalanx, band catches 13/16 phalanx; cone fraction 0.14–0.69 of N²/2).

3. **Adversarial cases (mine) strengthen the kill.** highe:250:2 (e 0.7–0.9): 7 of 13 truth
   encounters missed (54%); resonant:250:5: 4 of 5 missed (recall 20%). The failure is
   structural across regimes, not a σ_e = 0.01–0.05 artifact. The shared Newton-Kepler
   solver is not the culprit: residual ≤ 2e-7 rad at e = 0.95, far below ρ. The watch's
   precision is perfect by construction (every hit is a direct distance evaluation); the
   harness's two "FALSE ALARM" labels at highe are adjudicator-anchor artifacts — golden-path
   hits register no roots, so adjudication anchors at T/2 and searches the wrong window.

4. **Novelty.** No HISTORY or board entry tests a storeless band watch or the
   equation-of-center unification; this is new work, connected to (not redoing) r8 v2's
   conjunction-less leak and taleb-09b5's phase train.

5. **Goal fit.** Board focus item 3 and the top scaling risk: the measured cone fractions
   re-derive the materialized tier's O(N²) memory exposure at fixed geometry, and the
   negative result narrows q-skin's successor to "setup → per-body constants, windows
   stay". Respects PRINCIPLES #9: the failed experiment kills the configuration
   (unification), never the method (the tier's windows are exonerated as the second-order
   structure). Honest self-diagnosis; the author's own pre-registered kill makes the report
   trustworthy.

6. **Why not gold.** The record, not the physics: (a) the uniform:500 "epochs/body 5.3"
   cell is contradicted by the shipped code (6,587 epochs → 13.17), and the "flat and
   small / the O(N²) never materializes as work" narrative built on it is false —
   epochs/body grows ∝ N at fixed geometry (1,262 → 6,587 total for ×2 N) and reaches
   270/body at highe; epochs per **pair** is the bounded quantity. (b) cl_caught "1" vs
   actual 0. (c) P7 was silently dropped — my run answers it: evals hold (6.3e4/enc, within
   the predicted 3×) but recall collapses to 20%, a material omission for a soundness
   claim. (d) P3 is called "not decidable" though its own two points give slope
   log(7.80/5.95)/log 2 = 0.39, above the pre-registered 0.3 kill. (e) The adoptable
   fragment (per-body C_e band epochs as the candidate filter, tier's windows and walk
   inside epochs) is proposed but neither built nor measured — gold's "adopted within one
   step" is not met.

**The one experiment that would make it gold.** Build the hybrid in `crates/encounters`'
own harness: per-body C_e constants + closed-form band epochs as the candidate filter
(deleting the store), the tier's per-pair second-order windows and Diophantine walk inside
epochs. Belt scale (N ≥ 1e5, ρ = 1e-4): zero adjudicated misses including tangency and
resonant scenes, setup cost per-body not per-pair, work per real encounter ≤ the tier's.

**What the author missed.**
- P7's answer existed one run away and was dropped without a word: resonant recall 20%.
- The false "flat epochs" narrative — the honest invariant is epochs per pair, not per
  body; per body it grows with N and with e² (270/body at highe, evals/enc 8.95e6).
- The FALSE-ALARM adjudicator-anchor bug (roots unregistered for golden-path hits);
  harmless here but it would corrupt any precision claim at high e.
- The stored metrics.json omits the two uniform scenes the dossier table cites; they
  regenerate exactly, but the frozen record does not contain them.
- P3's own two-point slope already exceeded the pre-registered kill threshold.
