# Predictions (written before the decisive run)

Run: `hlive 3600 1 400` on this Linux box (8 vCPU), then `hlive 1800 1 400` and `hlive 3600 2 400` as un-tuned variants; extrapolation to 10⁹ bodies on the M1 (8 GB, ~10¹⁰ ops/s, ~60 GB/s).

Cases I have not tuned on:

1. **New info per event.** Delta between successive residuals, per component: **median 10–50 bits, p99 < 120 bits**. (The kick's integer impulse in root units; i128s should be mostly empty.)
2. **Residual now.** Residual bit-length per component: **median 40–100 bits** (the i128 mostly empty, the tube absorbs the bulk of the state).
3. **Reabsorption.** Mean residual bits (4 components) late vs early in the run: **ratio < 1.3** (bounded; consistent with the plane recompiling an orbit on ~99% of kicks). Ratio > 2 = a leaking walker population, and the HANDOFF risk is confirmed as real.
4. **Footprint today.** `bytes_per_body` on the plane: **100–400 B** (tube 16 B + residual 64 B + records/index).
5. **Event rate.** Kick+handoff events per body per game-second on the plane (ships on hours–days orbits): **0.01–1**.
6. **Compressibility.** Zigzag-varint delta stream compressed with zlib: **< 6 B/event**.

Extrapolation verdicts (the actual claim, predicted):

7. **H_live at belt scale** (orbital period 10⁷–10⁸ game-s, 32 kicks/orbit, ~30 bits/kick): **10⁻⁵–10⁻⁴ bits per body per game-second**, so 10–100 KB/s of new live information across 10⁹ bodies — at least 4 orders of magnitude under the M1's 60 GB/s and no threat to 8 GB within any play session.
8. **The binding term at 10⁹ is not H_live but today's stored representation**: bytes/body as measured (prediction 4) × 10⁹ ≫ 8 GB, while the belt program floor (0.126 bits/body, gold components-98bc) shows the generator representation closes it with ~7 orders of margin.
9. **H_live only threatens at inner scale** (period ~10⁴ s: 10⁶–10⁹ bodies deep in a system): 3×10⁻³ bits/body/s × 10⁹ = ~3 MB/s game-time; fills 8 GB in ~10³–10⁴ s **if and only if residuals accumulate** (prediction 3 is the test of that "if").

Kill criteria for my own estimate: if measured delta median > 80 bits, or reabsorption ratio > 2, or bytes/body > 1 kB, then the information budget does NOT close as predicted and the HANDOFF risk is the real top bottleneck.
