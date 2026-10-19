# Predictions — 20261019-0325-taleb-90b7 (formation burst law)

Written after the smoke test (aligned n=400 H=2048, instrument validated: shock train,
period 330, peak 195 ≈ n/2 per chronon, constant across 6 shocks) and BEFORE the
decisive grid (n ∈ {400,1600,6400} × σ ∈ {0, q/256, q/64, q/16} × seeds {1,2}, thermal
controls at matched box/fill/speed; horizons 2048/4096/8192 ≈ 6 shocks each).

Held-out cases (not tuned on): every σ > 0 arm, every n = 1600/6400 arm, seed 2, the
thermal controls, and the decay/amplitude laws below.

- **P1 (sustained coherence, the claim's spine).** The shock train does NOT thermalize:
  at σ = 0 the peak amplitude is exactly constant across all shocks (measured already in
  smoke: 195/184/195/182/195). At σ = q/256 I predict peak_k decays < 20% by shock 6
  (recurrent ruin); at σ = q/64 decay 20-60%; at σ = q/16 the train dissolves into the
  anti-bunched baseline by shock ~3-4 (F64_late < 5). Kill criterion for the dossier's
  headline: if σ = q/256 already dissolves, "sustained" dies and the fleet burst is a
  ringdown like genesis.
- **P2 (the peak scales with n, not with rate).** Worst-chronon contacts ≈ c·n with
  c ≈ 0.5 (0.45-0.55 band) at every σ ≤ q/64 — the allocator's worst frame is linear in
  fleet size, set by geometry (one mirror plane), independent of the mean rate. The mean
  per-chronon rate stays < 5% of the peak at σ ≤ q/64 (concetration: top-1% of chronons
  carry > 50% of all contacts).
- **P3 (F64_late is the separator, and it is huge).** Thermal controls: F64_late 1-4,
  per-64 max/mean < 4 (the wiki's baseline). Aligned: F64_late > 10³ (period >> window,
  spikes carry everything). σ = q/256: F64_late > 100. If F64_late at σ = q/256 lands
  < 20, the formation risk is priced by dispersion alone and the wiki's "unpriced half"
  closes with "bounded by σ·t smear".
- **P4 (smear width grows with σ, not with n).** Burst width (≥half-peak span) at shock 1:
  ~15-25 chronons at σ=0 growing roughly ∝ σ (q/64 → 30-80, q/16 → >150), and at fixed σ
  roughly n^0 (extent grows with n but so does speed constancy; prediction: width grows
  ≤ 2× from n=400 to n=6400 at fixed σ, i.e. sub-linear in extent).
- **P5 (cost is affine inside the shock).** ops-per-contact inside burst chronons stays
  within 2× of the thermal arm's ops-per-contact at the same n (the stepper's charged ops
  don't blow up on simultaneous batches; components are near-disjoint pairs).
- **P6 (seed robustness).** Seed 2 reproduces every statistic above within ±15% at
  σ ∈ {q/256, q/64}; the aligned arm is seed-free by construction (rng never called).
- **P7 (wall events ride the train).** Wall-flip counts per shock ≈ n (both fleets
  reflect at the side walls within a few chronons), synchronized with the contact train;
  at σ = q/16 the wall train smears like the contact train.

What would make the headline wrong: P1's σ = q/256 arm dissolving (then the formation
burst is one ringdown, not sustained ruin — the wiki's ringdown result extends to
formations and the allocator sizes only the first shock); or P2 failing (peak sub-linear
in n — then the burst is mean-like, not Extremistan).
