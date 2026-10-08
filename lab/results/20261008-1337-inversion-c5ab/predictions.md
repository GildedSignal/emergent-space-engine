# Predictions (written before the decisive run: scenes B–G and H1/H3)

Model (from the control A and debug_kick.py, corrected after the first Fermi estimate was wrong
by 1/delta-e): for equal-period co-orbital pairs, each of the two orbit crossings gives one
window |DeltaM0 − DeltaM*| < rho (the offset at the crossing is v·tau, full orbital speed; the
relative velocity ~ sigma_e·v never closes it). So:

- enc_pairs ~ n²/2 · 2 · (2 rho / 2 pi) per scene, independent of dispersion:
  n=1600 → ~81; n=800 → ~20; n=400 → ~5.
- circular phase rank of an encountering pair ~ n·|DeltaM*|/2π (+- rho·n/2π, negligible),
  with DeltaM* ≈ 2·Delta e·sin nu* for aligned apsides, and DeltaM* ≈ Delta-omega·(1 − 2e cos nu*)
  for spread apsides (uniform when omega is uniform).

## Held-out cases (not run yet)

- **B** (aligned, sigma_e = 1e-3, n=1600): miss_at_k4 ≈ 0 (threshold Delta-e > 4π/n = 0.0079 is
  5.6 sigma of Delta-e); k99 ≈ 2, kmax ≈ 3. All three keys similar.
- **C** (aligned, sigma_e = 1e-2, n=1600): miss_at_k4 ≈ 0.85 (Rayleigh tail beyond 0.56 sigma);
  k99 ≈ 22; kmax ≈ 20–25.
- **D** (aligned, sigma_e = 3e-2, n=1600): miss_at_k4 ≈ 0.98; k99 ≈ 65.
- **E** (fixed e = 1e-2, random omega, n=1600): ranks ~ uniform over the ring → miss ≈ 0.995,
  k99 ≈ 790, kmax ≈ 800, for all three keys (the true-longitude jitter is only ±4e rad ~ 10 ranks).
- **F** (sigma_e = 1e-2, random omega, n=1600): same as E.
- **G1/G2** (aligned, sigma_e = 1e-2, n = 400/800): miss ≈ 0.08 / 0.54; k99 doubles with n
  (≈ 5.5 / 11 / 22 at n = 400/800/1600) — rank scales linearly in n at fixed dispersion.
- **H1** (kick, delta-e = 1e-3, n=3200): encounters at rank ≈ 2·delta-e·n/2π ≈ 1 → k=4 catches them.
- **H3** (kick, delta-e = 3e-2, n=3200): rank ≈ 30 → 100% missed at k=4 under every key.
- **Churn** (rank exchanges per orbit, co-rotating): control = 0 (measured); B/C/D grow ~
  n²·sigma_e·c/pi with c of order 1 (order-of-magnitude only). exchanges_per_encounter in C of
  order 100× — the sort's maintenance already exceeds the encounters it certifies.
- **Key comparison**: mean-anomaly and mean-longitude keys agree everywhere (difference < 1 rank);
  the true-longitude key is erratically better or worse on single scenes (epoch luck), never
  systematically safe.

## What would make the inversion wrong

If miss_at_k4 stays ~0 in C/D/E/F at n=1600, the rank-4 premise survives realistic dispersion
and the gold's certificate is sound as specified; the dossier then reports that instead.
