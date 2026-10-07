Grade: silver

**Abstract.** Claim: the silver's setups cut converts into a total-evals cut at the plane's
kick size via three corrections. Every counter reproduced bit-for-bit from `work/patch.diff`:
belt 1767 vs 2898, 64-orbit 1540 vs 2703, ring 28650 vs 47600, fleet 17068 vs 61452 (3.6×),
and the 256-orbit inversion 27007 vs 2690 — all 0 missed/0 false, counters deterministic.
Tests 7/7; killing terms 3b+6 fails 1e-6/1e-4 as claimed. My adversarial: seed 4242 (0/0,
1.73×), κ=2 (0/0, 4.4×), fleet 1e-4 (0/0 of 1233 — the author's unfinished case closes at
parity). Gain: wall 3.0–3.7×, per-kick p95/p99 down 3–4× at young certificates. Cost:
additive in `skin.rs`, linear store (46.5 MB at N=1500); the required max-age refresh is
unimplemented.

1. **Reproduction, exact.** Applied the patch (`patch-mine.diff` is byte-identical), built offline, ran the dossier's commands plus `work/record.sh`'s case list. Every counter line regenerates exactly: belt 1e-6/1e-4 (the stale-record case, 0/0 of 73)/1e-8, orb=64 (0/0 of 257), orb=256 notruth (976 s wall, wk_p95 30.8 µs), ring 1e-6 (three identical runs — counters are process-deterministic), fleet 1e-6, seed 777 1e-4 (4628 vs 2718), ε=1e-2 (6542 vs 2754). One artifact of my own making, resolved: my mid-batch rebuild raced one adversarial rerun; clean reruns settled it against the stored line.
2. **Predictions.** Pre-registered (file times precede all work outputs). Held: pad s/2 exactness everywhere, trig 0.00 at 256 orbits, skin wall below always at 16/64. **Refuted:** the long-horizon economics (≤350/kick and ≥8× below always at 256; measured 10× *above*). The pre-registered falsifier fired, the author disclosed it, and it became the run's second finding — but gold requires held-out predictions held.
3. **Attack.** Term-kill control verified (3b+6 out → 1e-6 and 1e-4 fail, 1e-8 passes). Pad-s probe: 2202 vs 1767 evals/kick — correction 1's direction and size confirmed. κ=2.0 (harsher than the author's κ=1.0): 0/0, cut grows to 4.4× — the skin amortizes better under more kicks, so the win region extends up in kick rate, not just down.
4. **Novelty.** No HISTORY entry or board item covers the evals decomposition, the s/2 pad sizing, the exact-tolerance re-proof, or the widening-with-age limit. The skin itself is the silver's (20261006-2240) on the components gold's premise (20261006-0737); this run is the increment that makes its economics true in total cost, and corrects the first checker's attribution (the horizon query was 3 evals/kick, not the story).
5. **Goal fit.** Board focus line 3 (a skin over the Binet cone). PRINCIPLES §27 "The goal, never a proxy": judged on total evals and wall, the counter kept as diagnosis; §14 "No work for no reason": a discarded query deleted. The 256-orbit limit is itself adoptable knowledge: the skin is a young-certificate cache, so any adoption must bound certificate age.

**Why not gold.** The long-horizon prediction failed (into an honest finding), and the measured gain is 1.6–3.6× total evals (3.0–3.7× wall) — not the 10× bar. The author's own lens section says as much.

**The experiment that would make it gold.** Implement and run the max-age refresh the dossier derives (~70 orbits at the measured q(age)) plus a cheaper initial padded scan; require no horizon where the skin loses to `always`, belt total evals ≥5–10× at 16–64 orbits, 0/0 exactness, and `belt10k` completed (the store-at-scale number is still an extrapolation).

**What the author missed.**
- Fleet 1e-4 runs in 50 s and is 0/0 of 1233 (skin 63334 vs always 60718, parity): the record's only exactness hole was already closed, and at parity, not a loss — undersold.
- The crossover age (skin = always, between 64 and 256 orbits) is unmeasured; q(age) is sampled at three ages with exponent ~1.6 (16→256), called "~quadratic" loosely.
- The per-setup narrative "~322 → ~210 evals" does not reconcile with the shipped counters (~157 → ~126 by my measurement); the totals and the direction reproduce, the story numbers do not.
- The one-time initial padded scan (13.76 setups/kick at 16 orbits, 99k certificates) dominates young-horizon cost and is untouched; deleting it is where a further ≥2× on the belt lives.
- `results.jsonl`'s line ordering shows concurrent assembly (the orb=256 header at line 2, its always line inside the orb=64 block); every line regenerates, but the file is curated, not raw sequential script output.
