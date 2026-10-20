# Predictions — run 20261020-1729-second-20261020-1621-system-7fd3-aa42

Written before the decisive runs. The experiment is the checker's named one: run 7fd3's
census (verbatim instrument, plus two stage timers inside `Rebinding::from_state` that
reproduce a765's metric with the same counters) on a765's arm — `xtask universe
--kick-bench --seed S --rtf 100 --seconds 10`, seeds 1/7/42 — and on 7fd3's belt arm
(`nladder 10000 coast 60 1800`), so both metrics (7fd3's compile/rebind_wall; a765's
compile/(fit+compile+tail) inside from_state) are read off both scenes by one binary.

The fork (kill criteria pre-registered):

- **P1 — scene hypothesis.** On the kick-bench, census compile/rebind_wall ≥ 0.55, and
  a765's stage metric lands in [0.80, 0.92] (its stored originals: 0.894/0.882/0.877).
  Then 7fd3's 26% is a belt-domain fact; the "fit is 74%" redirect holds only on the
  belt, and a765's compile-bound reading stands on the plane population.
- **P2 — denominator hypothesis.** On the kick-bench, census compile/rebind_wall ≤ 0.35
  while the stage metric still lands in [0.80, 0.92]. Then both standing numbers are
  true in their own denominators (from_state stages vs the whole `Work::rebind` wall:
  word retries, history bookkeeping, passage edge), and every citation of "84-87%" or
  "26%" must name its denominator; the lever question becomes "what is the wall outside
  from_state", which neither run measured.
- Between 0.35 and 0.55: mixed; report both terms and the wall split, no clean kill.
- **P3 — belt cell (mechanism, no kill).** Belt: compile/rebind_wall ∈ [0.20, 0.32]
  (reproduces 7fd3 under load); belt stage metric compile/(fit+compile+tail) predicted
  0.45–0.75 — the belt's compiles are cheap, its fit+tail are not proportionally
  cheaper, so a765's metric on the belt sits between the two standing claims.
- **P4 — the scene term is the compile's e-dependence.** compile µs per mint: belt
  6–10 µs, bench 40–70 µs (cd6e's e-monotone belt→strong curve; a765's stored
  53.3–65.3 µs). If bench compile µs/mint ≈ belt's, the scene story is wrong.
- **P5 — bench reads/mint** (not load-bearing): the bench is resolver-only (no view
  gather, no boundary/readout traffic outside the replay), so reads/mint ∈ [0.5, 8]
  against the belt's ~20.
- VOID guard: if `ucensus[universe]` rebinds = 0 on the bench (the census does not fire
  on `step::process`), the instrument is mis-wired for this arm and nothing is claimed.
