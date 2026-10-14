# dossier.md — 20261014-0059-second-...-redteam-f3ce-33f1 (lens: second author)

## Claim

The checker's named gold experiment, run as specified at the engine's Q = 2²⁰, **refutes
the rung's own severity premise instead of confirming it**: the shipped contact law
**passes** the frozen bar (median |Σres|/KE = 7.4×10⁻³ < 1% over 5 seeds at 200
contacts, β 0.6, 1000:1 — verdict VOID, the negative cannot fail), the worst seeds do
exceed it (1.3×10⁻²), and the pair-scaled carry **does not flip it in any of three
implemented forms** (best engaging variant: median 1.4×10⁻²) — because the walk is not
slow accumulation but **representation saturation**: Fermi pumping drives the light body
to γ ~ 30–170 within ~15 contacts, where its energy quantum 2mγ³|k| is an O(10⁻²)
fraction of pair KE per contact (measured: the light body's quantum grew 400× in four
contacts; single contacts book up to 3.7×10⁻² of KE at 2²⁰). The adoptable disposition
is the checker's other branch: **gate the law's certificate on mass contrast** —
equal-mass contacts re-measured exact at 1.4×10⁻⁶ — with a horizon-based bar (1% of KE
is crossed by the worst seed inside 200 contacts at engine Q).

## Bottleneck

Same as the parent run: the dense order's error budget (§2), adjacent to the encounters
bottleneck. What this deletes: the "adopt the pair-scaled carry" path is now measured
dead (three forms, root causes named — the score mixes incommensurate energy/momentum
units, and an on-shell radial shift pays ~its energy change again in momentum), so the
integrator's one-step action shrinks to the certificate gate plus a corrected r5 bar.

## Evidence (shipped code + the run's patch; `regen.sh` regenerates all numbers, ~4 min)

**Instrument (Q = 2¹⁶ diagnostics, pre-freeze).** Per-contact dumps
(`run.log`): the first head-on contact ejects the light body at γ ≈ 3.9; by contact ~15
it sits at γ ≈ 114 (|k| = 0.99996Q) while the heavy decelerates — standard Fermi
acceleration against the shuttling heavy. The light body's exact per-|k| energy step
ΔE (integer, from `four_momentum_v1` differences) grew from 8.4×10⁶ to 3.3×10⁹ in four
contacts; the carry's big steps (up to 0.46×KE₀ at 2¹⁶) are that quantum, not
accumulated small errors. The parent run's "median 8.4×10⁻⁴ of KE per contact" is this
γ³-weighted quantum, time-averaged.

**The frozen rung at Q = 2²⁰** (`r5-contact-carry.md`, `metrics.json`, `verdict.txt`;
probe `rt_r5.rs`, seeds 0–4, 200 contacts, ledger exact and subluminal at every step):

| config | scene | median |Σres|/KE | worst seed | per-contact max / rms |
|---|---|---|---|---|
| shipped | 1000:1 β0.6 | **7.4×10⁻³** | 1.3×10⁻² | 3.7×10⁻² / 1.0×10⁻² |
| shipped | 1000:1000 | **1.4×10⁻⁶** | 1.8×10⁻⁶ | — |
| pair-carry | 1000:1 β0.6 | 1.4×10⁻² | 5.3×10⁻¹ | 3.2×10⁻² / 9×10⁻³ |
| pair-carry | 1000:1000 | 1.4×10⁻⁶ | 1.8×10⁻⁶ | — |

`verdict.py`: **VOID — the negative passes every criterion** (shipped 7.4×10⁻³ ≤ 1%);
the candidate fails `frac1000` (1.4×10⁻² > 1%). Held-out seeds 11–15, run after the
tables: shipped median 5.2×10⁻³, fixed −1.4×10⁻² — same classes.

**The three fix forms** (all behind `RUNG_PAIR_CARRY=1`, flag-off behaviour
bit-identical; `cargo test -p emergent-lattice` 21/21 green with the flag off, one
digest test differs with it on — a law change, as predicted):
1. Wide radial window, score arbitrates (cap 64, then sized by |owed|+spread): worse
   than shipped at 2¹⁶ (2.94 vs 0.157 KE) — with a wide candidate set and no fidelity
   term, the minimizer trades huge trajectory errors for carry cancellation, and the
   disturbed state makes the next fresh error worse.
2. Single target shift (owed-equivalent, clamped): engages, still −1.87 at 2¹⁶ — the
   shift repays only the standing owed, never the fresh corner error of the contact
   itself, which is the larger term at high γ.
3. Per-corner in-contact repayment (final form): the coarse body rounds to physics;
   the fine body's target shifts so its energy lands exactly on
   old_E − E(corner) − owed_E (all integers). Engages at both Q (2¹⁶ median −0.33,
   2²⁰ median 1.4×10⁻²) but **cannot beat the fresh quantum**: the score's |r|² mixes
   energy units with momentum units that differ by ~Q/|k| per quantum, and an on-shell
   radial shift changes momentum by ~its energy change (dp/dE ≈ Qγ²/|k|), so energy
   repayment is systematically outvoted by the momentum terms it costs.

Two instrument defects found and fixed before the decisive runs, both worth a rung-rule:
the probe LCG's low-bit `range()` draw is **constant across consecutive seeds** (the
parent run's pair arm had one effective y-offset; its seed diversity came entirely from
the β draw — any rung drawing seed variety from low LCG bits has none), and a rational
cone check compared numerators against the integer cone, silently no-op'ing one fix
version (found because a "fixed" run came out bit-identical to shipped).

## Predictions

`predictions.md` was written before any 2²⁰ run, with the instrument history disclosed
in place. Score: 1 **failed as disclosed** (the named risk: shipped passes the bar —
median 7.4×10⁻³ vs the predicted ~2×10⁻² fail; the coin-flip landed pass); 2 held
(1.4×10⁻⁶); 3 **failed** (no fix form clears the bar); 4 held; 5 held (ledger exact at
every contact, both configs, all seeds); 6 held (every rerun of a fixed build is
byte-identical; `regen.sh` re-derives the stored logs); 7 held (held-out classes
match); 8 partially run (momentum carry tracked in code but not printed per seed at
2²⁰ — the 2¹⁶ diagnostics show it growing alongside the energy, same quantum);
9 held (21/21 green off; one digest differs on); 10 held at 2¹⁶ (γ = 114 measured),
indirect at 2²⁰ (per-contact max 3.7×10⁻² matches the γ-scaled quantum).

## What would make it wrong

The severity numbers are one scene class (head-on box pairs, β 0.6, masses 1000:1 and
10⁴:1 untested at 2²⁰ — the parent's checker measured 10⁴:1 worse at 2¹⁶, so the
engine-Q bar likely fails there; a 10⁴:1 arm at 2²⁰ is the obvious next probe). The
mechanism reading (Fermi saturation) rests on the γ history measured at 2¹⁶; at 2²⁰ I
inferred it from the step scale. The fix's failure is measured on three forms, not
proven for every sigma-delta variant: a score with commensurate weights (e.g. E-term
scaled by |k|/Q per momentum term) or a two-body 2-DOF actuator that moves energy
without momentum is untried — but each such variant changes the law's choice rule, so
the certificate-gate disposition does not wait on them.

## Cost of adoption, fit with PRINCIPLES

Adopted sentence for the integrator: **r5 exists now** (frozen file, verdict machinery
run, controls both sides — equal-mass passes at 1.4×10⁻⁶, shipped's worst seed fails at
1.3×10⁻²); **raise the bar to the worst seed or re-freeze at 10⁴:1**, and **gate the
law's certificate on mass contrast** (equal-mass contacts are exact; contrast contacts
carry a γ³-weighted quantum) rather than adopting a carry fix. Cost: local to the law's
certificate predicate; no caller changes. Fit: principle 2 (error type: the walk is a
saturating quantum, not compounding drift — though at fixed sub-saturating γ it does
diffuse); principle 13 (the design's "never compounds" is saved at engine Q only by
Q-scaled margins, not by mechanism); principle 19 (two bandaids found in the fix path —
the score's unit mismatch and the on-shell actuator coupling — are the wrong
representation speaking); principle 33 (the raindrop and the lion: the pair resolves
only influences significant at its own scale — the carry must be scaled to the pair,
and so must its certificate).

## The lens

A second author inherits the parent's frame and its checker's bar; I froze the bar as
given and it burned a VOID on a ~2× margin — the pre-registered risk, but I could have
run the checker's own Q-ladder arithmetic (their 30–100× reduction over 64× Q predicts
exactly this pass) before freezing, and asked for a worst-seed or 10⁴:1 bar up front. I
also spent the window's middle third on fix forms 1–2 that a half-page of actuator
algebra (dp/dE on-shell) would have killed on paper.
