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

## AMENDMENT (2026-10-19 18:29 UTC, after one flight, before all others)

The 10⁵ OFF arm was flown under this registration (`work/a_off_100k.log`) and **refuted the
registration's premise**: the guard tripped at 38.6k gs (RSS 1,751 MB), before the belt's second
wave (~44k). Between waves 1 and 2 the arm retains ≈ 10 KB per belt body beyond base+bindings
(RSS 502→1,494 MB over gs 20k→35k with Δhist only 2,466; the same ramp at 3×10⁴ is 244 MB/30k
bodies ≈ 8.1 KB/body), so at 10⁵ ≈ 1 GB accrues before wave 2 and **no ≥3-wave OFF window exists
under the box's 2 GB cap**. The checker's named 10⁵ ratio is unflightable on this machine; the
10⁵ flight is kept as **rung C (the wall, measured)**, and the named experiment is flown at the
highest flightable rung, **5×10⁴** (the checker's own adversarial rung — OFF flew 180k gs there,
so [20k,105k] fits): the share law re-predicted from the same constants, the same closure bar,
plus the wave-aligned windows and windowed-kick closures the checker's 1.4-wave attack lacked.
No 5×10⁴ or seed-2 arm has been flown by this run before this amendment.

### Rung A′ — 5×10⁴, seed 1 (the named experiment at the highest flightable rung)

Share law: B = 1,066 × (50,000/30,000) = 1,777; L = 1,465; OFF stream = 3,242, ON stream =
1,687 per 1k gs; ratio = **1.922**.

- **W_OFF(5×10⁴)** = [first probe > 18k, last probe ≤ 108k] (belt waves 2–4 inside = 3 periods;
  wave 1 outside). **W_ON(5×10⁴)** = [wave1_start − 2k, wave1_start − 2k + 225.1k] clipped to the
  last probe — exactly one ON belt period, containing wave 1 whole and wave 2 not at all. (A
  matched-window pair cannot realize the steady ratio: OFF's wave is 28k, ON's 225k; each arm is
  windowed over whole waves of its own cadence.)
- **A′1** OFF windowed stream ∈ [2,920, 3,570] per 1k gs (share 3,242 ± 10%).
- **A′2** ON windowed stream ∈ [1,520, 1,860] per 1k gs (share 1,687 ± 10%).
- **A′3** closures Δhist/Δkicks ≥ 0.90 in each arm's own window.
- **A′4** slope ratio ∈ **[1.70, 2.15]** (share 1.922 ± 10%, widened by the registered closure
  allowance [0.90, 1.00] per arm). ≥ 4.0 → ÷S wins; < 1.70 → share law overpredicts here.
- **A′5** stream ratio ∈ [1.73, 2.11] (1.922 ± 10%).
- **A′6** guards: no trip inside either window; OFF RSS@108k and ON RSS@~311k ≤ 1,800 MB;
  refusals 0, dead 0. (The checker's misaligned 1.4-wave windows read 2.36 with closures 88%/74%;
  if aligned windows still read > 2.15, the share law's precision at 5×10⁴ is refuted — that is
  the falsifier this rung exists to test.)

### Rung C — the 10⁵ wall (measured on the flown OFF arm; ON arm to be flown as confirmation)

- **C1** OFF(10⁵) cannot reach its second belt wave under 1.8 GB (measured: guard at 38.6k gs,
  wave 2 ≈ 44k). **C2** ON(10⁵) also trips before completing wave 1's window needs (predicted
  trip ≈ 120–140k gs, mid/just past wave 1 at 88–128k; if ON instead flies past 150k, C2 is
  wrong and the wall is OFF-side only — reported either way).
B(10⁵) = 1,066 × (100,000/30,000) = 3,553 per 1k gs. Share law at 10⁵:
OFF stream = L + B = 5,018; ON stream = L + B/8 = 1,909; ratio = **2.629** (88e9's 2.63).
These 10⁵ constants feed rung A below and rung C; rung A′ recomputes the same law at 5×10⁴.

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
