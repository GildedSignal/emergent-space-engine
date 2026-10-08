Grade: silver

**Abstract.** Claim: news arrival rate at one body grows R² under per-(body,source) cursors but only ∝ log₂R (constant increment per octave shell) once sub-quantum events accumulate in cell-owned shell aggregates — so the growing light cone (Julien's OC#50 risk, HANDOFF:74) is a budget choice of Q, not a wall. Reproduced bit-for-bit (0.61 s); extended with the author's own code to R=8192 (+45/octave, naive ×4/octave); closed the admitted gaps: an off-centre observer keeps the log law (+88/octave, only c₀ moves), and falloff a⁻¹ restores near-R². Not gold: a closed-form identity in Monte-Carlo dress, not the engine's event stream; adoption is a design input (cursors inside r_cut=√(δ/Q), ~32 accumulators/cell ≈ 2.6 GB at 10⁷ cells). One defect: a π density bookkeeping error.

## Reproduction

- `python3 news_scaling.py` in a clean copy (/tmp): every number in the dossier regenerates, `news_scaling.json` byte-identical, 0.61 s. `work/patch.diff` is empty (0 B) — no tree edits, all work self-contained; nothing outside the run folder to apply.
- `predictions.md` (mtime 5 min before `run_out.txt`/`news_scaling.json`, 1 min): written before the decisive run. All six held: P1 smooth slope −0.008, grid check 0.749 vs analytic 0.741; P2 naive ×4 per octave exactly (α=2.0); P3 constant +43.8…44.8/octave; P4 r_cut=√(δ/Q) crossovers visible at R=64/16/128, exponents flat across Q; P5 cataclysms add 0.048–0.051 ≈ Λ=0.05 to both channels; P6 m=1 increments +1.77, +1.82/octave ∝ ln R.
- Bursty case matches spread to 3 digits (76.03/119.9/164.2/208.7/253.1) — correlation cannot inflate the accumulator, as claimed.

## Attack (my own cases)

1. **Extended sweep, author's own `run_event_case`**: R=1024→8192: quantum +44.8/+45.3/+46.1 per octave; naive exactly ×4/octave. The log law holds over 4.6 decades, beyond the author's range.
2. **Non-central observer** (the author's admitted unverified case): receiver at r=25 in the disk, observer-centred octave shells, softened 1/(d²+1) sizes, MC over annulus∩disk: 251.7/342.6/430.6/518.4 at R=256…16384 — increments +91/+88/+88, constant. The log law survives; only c₀ changes, exactly as the author predicted in "What would make it wrong".
3. **Falloff dependence**: s∝a⁻¹ gives ×3.66/octave (≈R², the wall returns); a⁻¹.5 ×1.65; a⁻² ×1.22 (the +44 additive). The 1/a² load-bearing caveat is honest and measured.
4. **Closed-form audit** (this found a defect — see below): the simulated naive rate is λπR², not the dossier's λN(R)=λρπR²; per-octave closed form 2πλδln2/Q = 43.6 matches measured 44.

## Novelty

No prior entry measures this law. `docs/HISTORY.md` H0190–H0215 and the taste log have nothing on news-rate scaling; the closest are the prior silver `20261006-1738-b-news-gravity-e300` (the in-system cursor *mechanism*; its checker showed light delays round below the kick quantum at plane scale, i.e. the scaling regime is unreachable there), the register's P6 ("influences below one quantum accumulate"), and queue items b-news-gravity/b-h-live. The dossier frames this correctly ("builds the cursor mechanism, not the scaling law"). Known-in-spirit from PDES null messages / FMM / LOD (the candidates section says so); new on the record are the crossover r_cut=√(δ/Q), the Q-sweep behaviour, and the memory Fermi.

## Goal fit

Answers Julien's named open risk (OC#50, PRINCIPLES register: "**Open:** a HANDOFF risk"; HANDOFF.md:74 verbatim — though the dossier misattributes the quote to "the board", whose scaling risk is encounter candidates). Fits P3/P6/P7/P23 as quoted. It argues a premise is wrong (the cone is a budget, not a wall) — but at toy level.

## Why silver, not gold

- **The measurement cannot fail by construction.** The quantum channel counts floor(Σs/Q) per octave shell per window; N_shell·s_shell = const for 1/a² sizes is a one-line integral that `predictions.md` P3 itself derives before the run. The Monte Carlo confirms bookkeeping; the only falsifiable content is the model choice (falloff, density), and the m=1 and cataclysm "cases" are pure closed forms with no stochastic content. This is a derivation dressed as an experiment — useful, but not evidence from the engine. The premise red-team's lesson applies verbatim: "claims must be measured on the design's cheap path."
- **Bookkeeping defect (found in attack 4):** `run_event_case` never multiplies the Poisson mean by ρ — the simulated disk has π× the stated sources (ρ_eff=1, not 1/π). So the dossier's "λN(R)" identification is off by π (1.05e4 claimed vs 3.29e4 simulated at R=1024), and the quoted analytic constant "λ·1.5πδρ/Q = 47" is miscalculated (evaluates to 15 with the stated ρ=1/π, 47 only with ρ=1). The correct closed form for what was simulated, 2πλδln2/Q = 43.6, matches the measured 44 — so the "~6% deficit from the r_cut cutoff" story is wrong accounting. Exponents, crossover radii and the head-to-head ratios (130×/10³×/18× at R=1024) are unaffected; every absolute rate shifts by π.
- Minor: "std ≤ 0.15% for R ≥ 32" — the stored spread is 0.20–0.27% at R=32/64 (≤0.15% only for R ≥ 128).

## The one experiment that would make it gold

Wire the two channels into the engine's own news path (`crates/universe` cursor, b-news-gravity's territory) and run them on the plane's real event stream at a growing horizon: measure arrival counts and cost per frame on the design's cheap path, with the accumulator's Q set by the receiver's certificate floor — the log law and the r_cut crossover either hold on real events or the toy's identity is missing engine physics (directional cancellation, correlated kicks). A rung with naive vs accumulator as configurations and a cost criterion would fit the lab's directed form.

## What the author missed

- The π density bug and its three downstream errors (λN(R), the constant 47, the 6% deficit story) — the check an analytic prediction is *derived from the code's actual constants* would have caught it.
- That P5/P6 and the bursty case are deterministic closed forms, so calling all six predictions "held" overstates their evidential weight; only P2–P4 touch randomness.
- The board/HANDOFF misattribution (the quote is HANDOFF's risk line, verbatim; the board's ranked risks are encounters and kicks).
- The view (photon) channel and H_live affordability are honestly deferred to b-readout-cost/b-h-live — good — but the dossier's own Fermi (2.6 GB of accumulators) competes with the 4 GiB budget before those answers arrive; that tension is unexamined.
