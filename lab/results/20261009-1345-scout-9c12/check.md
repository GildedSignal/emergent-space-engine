Grade: silver

**Abstract.** Claim: the player-influence cascade is a branching random walk absorbed at the certificate floor; Julien's convergence bet holds at belt scale with today's floors and fails super-linearly under planet flybys, floors ≲ 1e-9, compounding error, or co-orbital fleets — in bytes, not compute. Reproduced bit-for-bit (26 s: base 0 births; q=1e-9 → 719 live; crossers 10,373, exponent 0.0716/orbit; fleet 172,875). Source verified (Hu–Shi, arXiv:0911.2227). Predictions pre-registered; P1/P3/P4 held, P2 (7×) and P5 (3.5–5×) missed — the miss is the finding (Malthusian joint rate). My attacks: "base rate is 0" is a Poisson zero; verdicts robust to seeds, ε₀, floor. Gain: the open light-cone risk becomes two dimensionless numbers. Adoption: a criterion, no new component. Gold needs reabsorption measured (b-h-live/B18b).

## Reproduction

Clean copy of `probe.py` run in `/tmp`: all eight configurations match the stored `out-*.json` and the dossier table exactly — base 8 live / 0 births / 838 dusted (seed 7: 942), q=1e-8 → 160, q=1e-9 → 719 (7.3 → 6.8 births/orbit), cross-p1e-2 → 10,373 (exponent 0.0716), cross-p1e-1 → 600,000 capped / 30,288,901 births, chaos → 845 (0.1 → 11.6, ×116), fleet → 172,875 (495 → 1,832). Play-scale n_live(3) all match. Wall 26.0 s. Seeds are fixed and deterministic.

Timing/hygiene: `predictions.md` (13:57:33) precedes the outputs (14:00:05+). The disclosed mid-run instrument fix is credible, but the dossier's pointer to "`work/`-visible history" is dead: `work/patch.diff` and `run.log` are both 0 bytes. The final instrument is self-contained and reproduces everything, so nothing rests on the missing history, but that sentence overstates the record.

## Predictions

P1, P3, P4 held as pre-registered. P2 missed in magnitude, badly: bracket [15, 35] for n_live(100) at ν_p = 1e-2 vs 10,373 observed (≈ 300×), exponent 0.0716 vs predicted ≈ 0.01. P5 missed 3.5–5×. The author reports both honestly and the miss is itself the mechanism (amplifier children sit at the ε cap where nearly every encounter births, so the growth rate is the joint loop's, not the flyby channel's). Honest, but two of five quantitative predictions failing is not "the held-out predictions held."

## My attacks

1. **Base-case seed sweep (20 seeds):** births per 100 orbits = [0,4,0,3,2,3,1,0,1,1,1,1,3,0,1,1,0,1,1,1], mean 1.25 — "0 births" is seed luck, consistent with the author's own theory (8·1.1·1.6e-3 ≈ 0.014/orbit). Long horizon T=5000: first birth at t=105, steady late rate 0.0130/orbit, n_live=83. So the dossier's "the base belt's rate is 0, so it never saturates" is wrong: at ~2e9 belt orbits in 1e10 yr the base pump also saturates N (~4e8 yr). This *strengthens* the thesis — every configuration saturates at qualification scale, so reabsorption is the whole question — but it is a wrong line in the dossier.
2. **Crosser exponent across seeds 1–5:** 0.0738, 0.0733, 0.0628, 0.0760, 0.0737 — the claimed 0.0716 is representative; supercritical on every seed (one delayed-takeoff seed ends at n_live 185, still growing).
3. **Calibration attacks:** ε₀ ×10 (0.008) → 23 live, 0.30 births/orbit late; ε₀ ×100 → 160 live, 1.40/orbit; q=1e-7 → 23 live, 0.30/orbit. Belt-scale boundedness survives bigger burns and fills the 1e-6/1e-8 bracket monotonically. No hidden cliff.

## Novelty

No entry in docs/HISTORY.md or the docs touches the influence-series boundedness question (grep: light cone, influence, branching, frontier). The cited risk is real and unowned: HANDOFF line 74 ("The light cone keeps growing… we cannot handle the universe anymore"), and no queue entry owns it (`b-h-live` measures the belt's live distinctions, queued last). The foreign frame is correctly sourced: Hu & Shi, "The critical random barrier for the survival of branching random walk with absorption," arXiv:0911.2227 (Nov 2009), verified to exist. First measurement of OC's "a series that converges i bet."

## Goal fit

Moves a named open risk (the growing light cone, the one with no queue owner) from fear to two dimensionless numbers: birth condition ε·f/q per channel, and (birth rate)·T vs N. Respects PRINCIPLES 3/4/5/6 as quoted (quotes checked against the text; "influences below one quantum accumulate" is principle 6, accurately used for the dust pools). Shows a premise wrong in the useful direction: c-bound cone growth is not the threat; branching is.

## Why silver, not gold

Reproduced and novel, but: (a) two of five held-out quantitative predictions missed (one bracket by ~300×); (b) it is a hand-calibrated toy — scalar ε, linearized transfer (admittedly order-of-magnitude at f ≫ 1), borrowed 1.1/orbit from r8, no dust→dust propagation; (c) one dossier line is falsified by my seed sweep ("base rate is 0, never saturates"); (d) the "bytes, not compute" dichotomy is true in the toy by construction (encounter rates are fixed Poisson regardless of ε; the probe cannot falsify it — live scars changing orbits could change rates, unmodelled).

**The one experiment to gold:** measure the reabsorption side — program re-fit absorbing scars at the measured birth rates on the real belt (`b-h-live`/B18b) — or, in the toy, let re-fit run as a competing process and show the frontier stays bounded where the bet says it should. That converts the criterion from plausible to demonstrated.

## What the author missed

- The Poisson-zero: two seeds cannot distinguish rate 0 from rate 0.014/orbit; a 20-seed sweep costs 1 s and the long-horizon run 4 s. The "never saturates" extrapolation should be retracted in the dossier.
- The dead evidence pointer (`work/patch.diff`, `run.log` empty) after claiming the fix was visible there.
- "Never encounter rates" is assumed by the toy's fixed Poisson rates, not measured.
- Play-scale orbit counts (3 belt orbits in one hour at 100×) imply a very close-in belt; unexamined scale assumption, order-of-magnitude only.
