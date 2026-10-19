# Predictions (written 2026-10-19 ~18:35 UTC, before all decisive flights)

Checker's named gold experiment for 88e9 (silver): "Pre-register the share law at 10⁵ (predicted
2.63×) and fly both arms with wave-aligned windows spanning ≥ 3 full waves (guard raised for OFF),
plus one second seed at 3×10⁴. If the ratio lands in a pre-registered band around each prediction
and slope/stream closure stays ≥ 90% at both rungs, the identity is flight-verified at two rungs
beyond tuning and the scaling column's first entry is measured." This run flies exactly that.

## Instrument (calibrated, pre-registered)

Binary: main f520ad99 (= 88e9's base 9b0fdb9b + wiki-only commits) + `work/patch.diff` = 88e9's
patch verbatim (f80a probes, `LADDER_RSS_MB` guard, env-gated `BELT_SPLIT`; OFF ≡ shipped) **plus
two print-only additions**: a `LADDER_SEED` env dial (default 1 = the shipped hardcoded seed) and a
`kicks=` counter in each probe line (`p.u.stats.kicks`), so closure becomes windowed-kicks vs
windowed-slope — fixing the flight-wide-average bias the checker flagged. Scene and flight law are
88e9's arms unchanged: `burn`, rtf 2000, engine budget 12 ms, 1 thread, 48 members.

Calibration (this run, `work/calib_off_seed1.log`, seed 1, 3×10⁴, 13 s): hist_total 30,811 /
31,187 / 61,388 / 62,065 at gs ≈ 5k/10k/15k/20k vs 88e9's OFF 30,811 / 31,127 / 61,299 / 61,945
(≤ 0.2%, run jitter from the wall-clock budget; gt1 275/351/30,061/30,063 identical). Instrument
match. No arm has been flown at 10⁵ or seed 2 before this file.

## Constants (from 88e9's own flown OFF arm, seed 1, 3×10⁴; no re-derivation)

Total kick stream 2,531 per 1k gs = belt B₀ = 1,066 (30,000/28,141) + locals L = 1,465. The locals
(48 members + Home system) are scene-fixed: L(N) = 1,465. The belt scales with N:
B(10⁵) = 1,066 × (100,000/30,000) = 3,553 per 1k gs. Share law at 10⁵:
OFF stream = L + B = 5,018; ON stream = L + B/8 = 1,909; ratio = **2.629** (88e9's 2.63).

## Window rules (registered before the flights; applied mechanically by `work/analysis.py`)

- **W_OFF(10⁵)** = [first probe > 18k, last probe ≤ 108k] gs. Expected: OFF belt wave 1 at
  ~11–16k stays outside; waves 2–4 (~39–44k, 67–72k, 95–100k) inside = ≥ 3 belt periods (84k gs).
- **W_ON(10⁵)** = [wave1_start − 2k, min(wave2_start − 2k, last probe)] gs, waves read from ON's
  own Δhist bursts (nominal: wave 1 ≈ 88–128k — de7b's 8× deferral — wave 2 ≈ +225k). Wave 1 fully
  inside, wave 2 outside; locals steady throughout. Each arm is windowed over ≥ 1 full belt wave of
  **its own** cadence: a single matched window cannot do it (ON's wave is 225k long; a window
  holding 3 ON waves costs OFF > 4 GB, and a matched [20k,105k] window straddles ON's wave-1 edge,
  reading the ratio ~3.1–3.4 for placement, not law, reasons — reported as a diagnostic, not a test).
- **W(3×10⁴ seed 2)** = [140k, 245k] gs, matched, identical to 88e9's window (comparability).

## Rung A — 10⁵, seed 1 (the named experiment)

- **A1** OFF windowed stream ∈ [4,520, 5,520] per 1k gs (share 5,018 ± 10%). Outside → B does not
  scale with N; the scaling column dies at its first entry.
- **A2** ON windowed stream ∈ [1,720, 2,100] per 1k gs (share 1,909 ± 10%).
- **A3 closure (the mint identity):** Δhist/Δkicks ≥ 0.90 in each arm's own window. Below 0.90 in
  either → the "slope IS the stream" identity fails at that arm (88e9's law loses its precision
  claim; silver content, reported).
- **A4 slope ratio** (OFF/ON hist slopes, own windows) ∈ **[2.30, 3.00]**, center 2.63. ≥ 4.0 →
  the ÷S reading wins at 10⁵ (refutes 88e9). < 2.30 → the share law overpredicts at 10⁵.
- **A5 stream ratio** (windowed Δkicks OFF/ON) ∈ [2.37, 2.89] (2.629 ± 10%).
- **A6 guards:** no RSS-guard trip before each window's end; RSS(OFF)@108k and RSS(ON)@~311k each
  ≤ 1.75 GB. Refusals 0, dead 0, both arms.

## Rung B — 3×10⁴, seed 2 (the author's disclosed gap: seed spread)

- **B1 slope ratio** (matched window) ∈ **[1.50, 2.10]** (seed 1: 1.76, checker regen 1.78; the
  mint law is a count identity, so seed moves placement, not law).
- **B2 closures** ≥ 0.90 both arms on windowed kicks (seed 1's ON 86.8% was measured against the
  flight-wide rate; the windowed counter removes that bias).
- **B3 stream ratio** ∈ [1.43, 1.75] (share 1.587 ± 10%).
- **B4** OFF slope ∈ [2,070, 2,800] per 1k gs (seed 1: 2,432 ± 15%).

## What is not claimed here

The 10⁶–10⁹ rows of 88e9's scaling column stay arithmetic. The compact-side τ ×8 stays unflyed
ledger arithmetic on 0659 (untouched). The split's legality stays cited (7f97 B17, f790, 98cb).
RSS ratios are reported as diagnostics (b911/88e9 already priced B/binding); no RSS band is
registered except the guards.
