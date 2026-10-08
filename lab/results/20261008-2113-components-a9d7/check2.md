Grade: gold

Abstract: On the plane's own law, fired kicks are so rare (3.6×10⁻⁵ per body per game-second, invariant across seed, N = 256→2048, belt position and e ≤ 0.9) that the H_live *rate* at 10⁹ bodies is ~0.4 MB/s — affordable — but each kick costs ~86 bits because the velocity lattice sits at 2⁻⁷⁴c, so the accumulated deviation (~104 bits at 139 days, ballistic, +2 bits per time-doubling) breaks the 64-bit/body budget from the first kick: the floor is the lattice exponent, not the count or the rate. Reproduced bit-exactly (identical digests) and through the author's own scripts on clean reruns; my requantization control (86 → 17.9 bits at σ/100) confirms the mechanism. Adoption cost: none for the measurement; the deviation-native-lattice fix needs one B5/B12 exactness run.

## Reasons

1. **Reproduction, bit-exact.** `work/patch.diff` applied to a clean tree, built, all four cases rerun in a scratch dir: every digest matches the author's stored summaries (s2 `44b95de8…`, s3 `4cd0e769…`, inner `042dd23c…`, outer `9f4b7b2d…`), same rows and item counts. The author's `shrink.py` + `analyze.py` on my rerun's s2 give 219,822 kicks, 3.578e-5/body/s, 85.91 bits/kick, net 103.74 bits, +2.035/log₂t, carry 34.18 bits, 1,497.5 B/body — every dossier cell. An independent reimplementation of mine from the author's stored xz files matches s3/inner/outer as well (87.3/79.3/88.7 bits; 106.3/93.1/109.7 net; slopes 2.21/1.89/3.06; carry range ±65,535 ≈ ±2¹⁶, bounded).

2. **Predictions.** `predictions.md` (21:21:56) precedes every data file (21:25+). Held: rate ~3.5e-5; magnitude-class entropy 2.1–2.5; carry bounded ±2¹⁶ (34 bits); store ~93× the tube; gross stream GB/hour order. Missed, all disclosed: H(dv) 86 vs 4–14; inner/outer ratio 1× vs ≥20×; net 104 at 139 d vs 6–20 at 10 y; stray 97% vs <5%. The misses are the finding itself: the author's model ignored the lattice exponent, and the measurement corrects it (H0183: a failed expectation diagnosed, not hidden). The rows-are-fires premise holds: zero dv=(0,0) rows in s2 and outer; merged double-fires (captured − rows = 1.4% in s2, 19% in my eccentric case) preserve the net deviation exactly (the total dv is read across the merge) and bias the rate only by that fraction.

3. **Attacks (all failed to break it).**
   - *Eccentric belt* e ≤ 0.9 (my `hlive_adv`, seed 17, n=256): rate 3.60e-5, 87.1 bits/kick — the two headline verdicts survive a hot belt; store grows to 3,242 B/body (the changeover cost the author's blind spot predicted).
   - *N-scaling*: n=2048 spread gives 3.60e-5 and 87.4 bits — rate and per-kick cost invariant 256→2048; the 10⁹ extrapolation stands (the author had only 256→512).
   - *Lattice requantization control* on the author's s2 data: 85.91 bits native → 17.91 at 2⁻⁴⁰c (σ/100) → 4.21 at ~σ; σx = 2⁴⁰·⁸ quanta exactly as claimed. The causal claim — the lattice exponent, not the dynamics, sets the cost — is verified on the author's own data.
   - *Growth curve* recomputed at all 16 samples: smooth and monotone, 95.7 → 103.7 bits, slope 3.3 → 1.8 (concave). The +2.0/doubling extrapolation is fair; the verdict does not depend on it (86 > 64 at the first kick).

4. **Novelty.** HANDOFF line 70 lists H_live as "not measured yet"; law.md names it as what the allocator reads; no HISTORY entry measures it. Distinct from r2 (carry widths) and gold components-98bc (program bits, 0.126). The inversion — rate affordable, lattice fatal — appears nowhere earlier.

5. **Goal fit.** Moves the board's "fitting 10⁹ in 8 GB, decided by distinctions created per game-second" by showing the premise wrong: the deciding quantity is the per-distinction lattice cost, not the rate. PRINCIPLES 24 ("The memory floor is information"), 16 ("what's the biggest quantization that we can get away with?"), 19 (a fix signals the wrong representation). It also feeds B18: the gate should demand the deviation quantum.

## What the author missed

- The lens brief (b-h-live.md) asked for the measure in `xtask universe --bench` and the dashboard page, with tests and gates run both ways; the run ships a standalone example with no dashboard integration and does not state the deviation from the brief.
- The documented reproduce chain breaks as written: `shrink.py` reads `{run}-kicks.csv.xz` while hlive writes raw `.csv` (the compression step, and outer's a/b split, are undocumented). One command fixes it; I verified the chain end-to-end after compressing.
- The pre-registered cases were not run as registered (n 4096/2048 predicted; 512/384 run) — N-invariance beyond 512 was unmeasured until my 2048 run.
- The 10-year figure extrapolates ×25.6 in time from a 139-day horizon with a concave slope; 113 bits could plausibly be ~108–110. The verdict is unaffected.
- Position/timing deviations are unmeasured (velocity-only, disclosed): the true scar is plausibly ~2× the 104 bits, so the 18 GB figure is conservative.
- The stray-items anomaly (2.5% in inner vs ~97% in s2/outer) is explained by assertion ("one engine item per fire") rather than diagnosed; the entropy rows are unaffected.
