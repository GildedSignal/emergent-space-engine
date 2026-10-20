# Predictions — 20261020-2004-second-20261020-1815-library-a2c0-20f2 (second author on a2c0)

Written 2026-10-20 20:15:55 UTC, BEFORE the decisive re-flight F1 and before the final
analysis script runs. Disclosed context: the run is the checker's named gold experiment,
done as a log read where possible. I have already READ 23a6's and a0a1's committed
artifacts (necessary to discover that the per-answer series exists), so the D-series
below is pre-registered as bands with kill bars, informed by that reading — the decisive
test of them is F1 (regeneration from shipped code + the patch) plus the corrected
arithmetic. The R-series are pure regeneration claims I have not tested yet.

The two named experiments (check.md, "The one experiment for gold"):
(a) pin δ from the per-answer skip series — it EXISTS in 23a6's committed
    e3_1e5_on.err (per-answer t/cand/tests/skip_bnd), so δ is pinned by log read,
    plus one flight (F1) proving the series regenerates;
(b) the ALL-walks-per-era count at 1e5 vs 3e5 — countable from committed artifacts
    (CAP radial=ALL lines; a0a1's b1/c2/a1, 23a6's w1/w2/w3/e3/e4/e5), with F1
    re-counting the 1e5 cut leg.

## Registered

- R1 (F1 regeneration): the re-flown e3 replica (1e5 burn cut 30k gs, ON, anatomy)
  reproduces the committed digest `8eecf1fa…` byte-identical, 41 belt-wide answers
  (cand 99,715), the SAME per-answer tests/skip_bnd counts (integer-exact decisions;
  only wall ns may vary), the cold answer at tests = 88,873, and 81 `radial=ALL`
  capture lines. Kill K1: any count or the digest differs.
- D1 (the δ pin, at the ACTUAL gaps): the belt-wide answer gaps are NOT the assumed
  uniform 732 gs: they are 165.25 gs (2^25 ticks × TICK_SECONDS) then 330.5 gs
  (2^26) in the committed series, spanning gs ~19.7k–29.9k. Per-answer
  δ_eff = miss/(λ·gap) with miss = (per-answer µs/body − c_check)/c_read lands in
  [0.05, 0.32], drifting upward through the flight. Letter (a2c0's): δ_eff < 0.5 at
  every answer. Kill K2: any answer shows δ_eff > 0.5 under the measured c_check.
- D2 (the clustered δ=1 branch dies): observed warm misses are 0.04–0.5% per answer
  against λ·gap = 0.8–1.6% of bodies kicked per gap, so at most ~1/3 of kicks can be
  dirtying anything — every-kick-dirties (δ=1) is excluded by the series itself, not
  just disfavored.
- D3 (mechanism correction): the miss series shows slack-dynamics signatures the
  kick-Poisson model does not produce: growth at CONSTANT gap (44→203 tests over the
  165-gs legs) and a spike-then-decay at the gap doubling (→~480, decaying to 142).
  δ is an effective ratio (memo invalidation per kick-slot), not a law constant; the
  invalidation is dominated by the bound's own slack (cap·dt crossing the distance
  margin as the player burns into the belt) — the bound's memo, not the kick stream,
  sets the answer cadence's cost.
- D4 (c_check measured, the degenerate corner dies): per-answer
  c_check = (ns − read_ns)/cand ≈ 27–29 ns/cand, flat across warm answers — at the
  top of a2c0's assumed [0, 0.02–0.03] ceiling and far from the ≥ 0.0405 µs corner
  where 23a6's 41-s-at-era-cadence sentence would survive. Kill K4: c_check > 40 ns.
- D5 (the cold lump IS the era-cadence answer): the one cold answer's miss is 89.1%
  at ~30k-gs staleness (≈ one era), so ONE era-cadence answer at 1e9 costs
  ≈ 3.86 µs/body = 3,860 s = 55× the 69.75-s era budget: the 41-s sentence is dead
  by measurement (a2c0's "never 41 s" holds; its δ-band rows 4.1–20.9× undershot;
  its δ=1 row 46.2× is the close one). The bound makes answers cheap only at
  ≤ ~330-gs cadence — and sustaining that cadence pays c_check × ~112 answers/era
  ≈ 3.1 µs/body/era in checks alone.
- D6 (ALL-walk N-scaling corrected): counted per-era rates from the artifacts:
  3e3: 120–246/era (3 legs), 1e5: 42.8–78.8/era (4 legs), 3e5: 86.3–86.8/era
  (2 legs) — no monotone N-growth; the N^0.74 reading dies by duration
  misattribution (c2 covered 56,035 gs, not 30k; the 3e5 wall legs 40.2–40.7k gs,
  not 19.5k). F1's 1e5 cut leg re-counts inside 60–95/era. Kill K3: outside.
- D7 (the corrected ledger): capture 3.2–6.4 h/era (43–87/era × 267 s), answer
  channel ~1.1–2.2 h/era (checks × cadence + cold amortization + warm reads, from
  the measured series), kick comb 12.75 h (a31c) — total ~18–21.5 h/era, ordering
  kick ≥ capture ≥ answers SURVIVES, the adopt order (tier, then partition) is
  unchanged; the answer share rises from a2c0's ≤ 2.5% to ~5–12% (it is still the
  smallest term).

## What would make the run wrong

F1 failing K1 (the series does not regenerate from shipped code + patch on the current
base — then every derived number stays a band on committed artifacts, silver not gold);
an ALL per-era count at 1e5 outside K3's band (the legs disagree and the N-flat premise
needs its own flight); c_check > 40 ns (K4, the degenerate corner revives and D5
weakens to a band). The 3e5 ALL legs cannot be re-flown inside the 2-GB cap (a1/w3
peaked 5.1–5.9 GB) — they stand on two committed independent runs, disclosed.
