# Predictions (written before the decisive run)

Probe: `b12probe.py` — a candidate B12 statistic for the redesign (queue item 1).
Mechanism: judge the residual series' growth CLASS (bounded / sub-diffusive leak /
diffusive / ballistic) by the slope β of log(MSD − noise floor) vs log t over a
window ladder. Constants tuned ONLY on models 1–3 (bounded, diffusive, ballistic).
Models 4–5 are held out, evaluated once:

- Model 4, slow leak (true β ≈ 0.25 — the case that broke the recurrence ratio,
  board 6 Oct): classified NOT-bounded in ≥ 90 % of 100 seeds at T = 4096.
- Model 5, bounded with rare jumps (stationary + occasional ±10q jumps):
  classified bounded in ≥ 90 % of seeds at T = 4096.
- False alarms: bounded model misread as leak in ≤ 10 % of seeds.
- Horizon: at T = 1024 the slow-leak detection rate falls below 70 % (the gate
  needs a minimum orbit horizon; the ladder's short windows under-resolve β < 0.3).
- Chaos is not the signal: a stationary AR(1) residual with strong serial
  correlation (mimicking chaos-amplified rounding, model 1b) is classified
  bounded in ≥ 90 % of seeds — the classifier reads the error class, not the
  trajectory.

Gate audit (lesson 5): among frozen gates with recorded verdicts in
`artifacts/evidence/`, I expect to find at least one never-failing judge —
a control that cannot fail — worth deleting by the "best part is no part" rule.

## Amendment (after the decisive run; estimator history disclosed)

Two estimators were tried and failed on TUNING models (1–3) before the final one:
partial-MSD log-slope (single-trajectory: unusable noise, factor-2 threshold bug)
and plain segment-ANOVA F (read chaos's autocorrelation τ≈19 as leak — exactly
failure (e)). The final statistic (blocked-difference F, kseg=32, fcrit=3.5,
τ-guard) was tuned ONLY on models 1–3. Models 4–5 were exposed during those
failed iterations, so their held-out status is compromised in structure (not in
thresholds); a checker should re-run with new seeds and its own leak/jump sizes.
`python3 b12probe.py short` (≈2 s) reproduces everything.

Outcomes vs predictions:
- (a) slow leak ≥90% not-bounded at T=4096: HELD (94/100 compounding, F med 11).
- (b) bounded+jumps ≥90% bounded at T=4096: HELD (99/100).
- (c) false alarms ≤10%: HELD (0–1%, F p90 ≈ 1.3 vs fcrit 3.5).
- (d) T=1024 slow-leak detection falls below 70%: MISSED — detection stays 95%;
  what collapses is the bounded verdict, which returns void (τ-guard), never
  wrong. Better than predicted; reported as a miss.
- (e) chaos (AR(1) ρ=0.9) not read as leak: HELD at T=4096 (100/100 bounded);
  at T=1024 void by the guard.
