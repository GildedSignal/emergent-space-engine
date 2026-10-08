# Dossier — 20261008-1719-dynamics-c13b (lens: dynamics and attractors)

## Claim

On B12's frozen chaotic ships, the Jacobi error of a bounded, state-only law produces net slopes and
window growth that no trend- or exponent-style statistic can separate from a slow leak (the
identifiability wall, now measured: per-ship slope |z| up to 6.3, mean z −2.0 on the bounded
control), while a recurrence-memory statistic — the rank correlation of the error difference with
the time gap over pairs matched on the heliocentric (E, L) deciles, judged against a stratified
permutation null — orders all seven controls correctly (clean ≈ 0.01, bounded 0.30, leaks 0.29,
compound 0.68, drift 0.72) with thresholds derived, not fitted; and the exponent's bounded-vs-compound
ranking is not even reproducible across machines (it swapped here), so B12's miscalibration is worse
than a wrong threshold: the statistic is noise.

## Bottleneck

The B12 redesign (board, Headed next #2; queue `q-b12-design`, Codex `b12-v2`): "the instrument: B12
cannot yet tell bounded from compounding error on chaotic ships". Gain: unblocks freezing the
motion-law stability gate; deletes the machine-dependent convergence re-check (my statistics read only
the law's own signed series, never the reference).

## Evidence

All numbers from `work/` (dump by the `#[ignore]` test `b12_series_dump`, added to
`xtask/src/behave/handoff.rs`; tree restored by run.sh, patch saved). 14 judged ships of the 16
frozen (this Linux run's reference), 1601 samples over 200 planet periods, 9 laws including three
planted slow leaks (1e-12, 1e-13, 3e-14 per period).

| law | median exponent (limit 0.2) | worst \|X\| (limit 1e-4) | S1 mean z | S2 median rho | S2 ships p<.05, rho>.1 |
|---|---|---|---|---|---|
| echo | 0.000 | 2.3e-15 | 0.11 | −0.008 | 0 |
| scaled 3e-13 | 0.000 | 8.6e-13 | 1.43 | −0.007 | 0 |
| scaled 1e-11 | 0.191 | 2.9e-11 | 1.43 | 0.011 | 0 |
| planted-bounded | 0.353 | 1.3e-05 | **−1.99** | **0.300** | 10 |
| planted-compound | 0.416 | 9.8e-07 | −1.10 | **0.677** | 12 |
| planted-drift | 1.355 | 2.4e-09 | −3.13 | **0.724** | 14 |
| leak 1e-12/P | 1.195 | 5.4e-10 | **+2.76** | 0.291 | 13 |
| leak 1e-13/P | 1.195 | 5.4e-11 | **+2.76** | 0.292 | 12 |
| leak 3e-14/P | 1.194 | 1.6e-11 | **+2.76** | 0.299 | 13 |

- **Exponent**: fails every law above the 1e-12 floor, including both bounded controls (0.353, 0.191
  — 0.191 passes only by luck of this window). Its ordering flipped relative to 6 October
  (bounded 0.493 > compound 0.305 there; 0.353 < 0.416 here): the ranking is not reproducible.
- **S1 trend blade** (OLS slope, z against circular shifts of the mean-removed increments): flags
  the leaks (mean z +2.76, 7–8/16 ships same-signed) and drift, but **falsely flags bounded (−1.99)
  and the scalings (+1.43)** — a bounded error's chaotic diffusion carries a net window slope. This
  is the wall: any trend statistic is unsafe on chaotic ships.
- **S2 memory blade** (this run's survivor): correct ordering on all seven controls; clean controls
  at the machine confound (|rho| ≈ 0.01, 0 ships); compound/drift at 12/14 ships. Margin
  bounded-vs-compound is thin (0.30 vs 0.68 in rho, 10 vs 12 ships) — the within-cell Lipschitz
  confound (finer matching on |Δ(E,L)| bands, not deciles) is the named next experiment.
- **Derived leak floor** ℓ_min ≈ z*·σ̂_slope·P (z* = 2.5): verified on both bases — echo base
  ℓ_min ≈ 1e-18/P (the 3e-14/P leak is flagged, as derived), bounded base ℓ_min ≈ 4.9e-9/P (a
  1e-11/P leak added to the bounded series is correctly invisible, 500× below the floor). The floor
  is the series' own noise: derived, and it behaves as derived.

Reproduce (≤ 60 s each): from the repo root,
`B12_DUMP_DIR=<run>/work cargo test --release -p xtask b12_series_dump -- --ignored --nocapture`
(67 s incl. build; note cargo runs tests with CWD = xtask/, so move the CSVs), then
`python3 <run>/work/quick.py` (24 s). Full per-ship series in `work/*.csv` (each ≤ 0.3 MB),
per-ship statistics in `work/analysis.json`.

## Predictions

`predictions.md` was written before the analysis. Held: leaks flagged by S1 (all three rates) and by
S2 (12–13/16, better than the predicted ≥12); drift caught by S2 (14/16; S1 alone insufficient, as
hedged); exponent miscalibration reproduced (bounded control fails); floor behaves as derived on
both bases. Failed, honestly: prediction 2 — S1's aggregate falsely flags bounded (6 ships at
p<0.05, predicted ≤5; mean z −1.99) — the diffusion's net slope is real, not a fluctuation; and the
bounded/compound exponent inversion did not reproduce (it reversed), which my kill criteria named as
a possible outcome and which strengthens the miscalibration claim.

## What would make it wrong

A real law whose compounding error is smooth and slow (below S2's matched-pair growth over 200
periods) would pass S2 — bounded by the derived floor, not eliminated; and the bounded/compound S2
margin (0.30/0.68) could close under a different matching resolution. Cost of adoption: S2 needs the
stratified permutation (~150 × cheap ranks, per ship) and the (E, L) conditioning, all inside
`behave` on the law's own states; the convergence re-check and its Linux/Mac asymmetry are deleted.
PRINCIPLES fit: "Errors never compound" (13) — judged by the error's memory, not its size; "the
right question, then the representation" (18) — at matched state, the question "has the error grown
with time, not distance" makes the math trivial; "a test that cannot fail is a control" — seven
controls, two directions. Fit with method.md #9 (calibrate on a planted pair before freezing): the
rho>0.1 ship rule is calibrated on the echo control's measured confound (0.01), an order of
magnitude below.

## The lens

The dynamics lens looked for the attractor and found the wall instead: on chaotic ships a bounded
error is a function on a compact invariant set, and its window statistics (slope, exponent,
variance growth) are the set's exploration, indistinguishable from accumulation at any finite
horizon — only the state-conditional structure separates them. What this lens may have missed: the
cost side (S2's permutations in a 60 s gate), and whether a game-length horizon (not 200 periods)
changes the floor enough to matter to Julien's error budget.
