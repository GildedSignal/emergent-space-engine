# Dossier — second author on 20261010-1407-fermi-fc48: the floor at 10⁹, with the phase dof

## Claim

The named experiment confirms the checker's arithmetic — the 3-field sorted
floor falls with N and lands at **61.6 / 62.1 bits/body = 7.70 / 7.77 GB at
10⁹, under the 8 GB budget** — but that floor covers 3 of the tube's 4 fields:
the phase (t_p, 64 bits per radial cycle, uniform by construction at 63.96
bits/sample) is carried by every exact non-replay encoding, so the 4-field
floor at 10⁹ is **125.5 / 126.1 bits/body = 15.7 / 15.8 GB, ≈ 2× over
budget**; the original headline verdict ("no exact encoding at the tube's own
quanta fits 8 GB at 10⁹") therefore **holds with corrected numbers**, the
checker's "under budget, ≤ 3% margin" restatement is a field-scope artifact,
and the scar form is near-optimal (+0.9 bits over the floor right after the
first pass, +23 bits by 10³ orbits) — the wall is the tube's own quanta, so
the requantization-law adoption (coarser storage quantum, remainders
carried, t_p anchored) stands with a real margin, not 3%.

## Bottleneck

Same as the parent run (H_live decides whether 10⁹ fit in 8 GB; B18's
belt clause). This run closes the gap the checker named: the −log₂N
extrapolation (done, empirically) and the encoding-class question it flagged
as "the actual decision B18's stirred clause needs, and it is unexamined"
(done: the phase dof is the decider).

## Evidence

All from this folder. Commands: `python3 hlive.py` (78 s; regenerates
`hlive.json` **byte-identically** to the shipped one — verified with `cmp` —
and an identical `final_state.npz`), `python3 floor.py` (0.2 s; 75.5/76.1 as
shipped), `python3 floor9.py` (0.8 s; writes `floor9.json`). The T_ORBITS=2
quick path, which crashed in the shipped script, now runs in 0.4 s (slope-fit
guard; the full-run JSON is unchanged by the patch, re-verified).

**A. The checker's experiment — N-scaling of the 3-field floor** (subsamples
of the shipped state + fresh birth states, Miller–Madow-corrected adaptive
coarse-grain; at N=2¹⁶ it reproduces floor.py's fixed B=2²⁴ to 0.01 bits):

| state | H₁ (bits/sample) | slope vs log₂N | floor₃(10⁹) |
|---|---|---|---|
| birth | 90.03 ± 0.02 (analytic 90.09) | −0.996 | 61.58 bits = 7.70 GB |
| final | 90.59 ± 0.03 | −0.996 | 62.14 bits = 7.77 GB |

One H₁ fits every N from 2¹² to 2²⁰ (fresh seeds included); the −log₂N term
is real and the checker's 61.6/62.2 is confirmed to ±0.1 bits.

**B/C. The missing dof.** The tube's stored state is (E, L, ϖ, t_p) —
law.md: "position and velocity are derived when asked". floor.py's floor uses
(a, e_vec) (its own v2 note derives ϖ from e_vec, ±~1 bit of grid Jacobian)
and omits the phase. Birth phases are U[0, 2π) by the shipped generator:
**63.96 bits/sample** at the 64-bit per-cycle quantum (measured on the
replicated draw; the shipped rows' H_tp_mod saturating at 63.9 is the
independent cross-check). The phase is independent of (a, e_vec), so:

| encoding class at 10⁹, tube's own quanta | bits/body | GB | vs 8 GB |
|---|---|---|---|
| sorted multiset, 4 fields — **the floor** | 125.5 / 126.1 | 15.7 / 15.8 | **1.96× over** |
| sorted multiset, 3 fields (phase dropped) | 61.6 / 62.1 | 7.7 / 7.8 | under — but not a state |
| program + scars, identity kept (shipped form) | 126.4 → 149.3 (1→10³ orbits) | 15.8 → 18.7 | 1.97–2.33× over |
| strict 16-byte reading ((E,L) share 32 bits) | 90.4 | 11.3 | 1.41× over |

**D. Strict 16-byte tube reading** (robustness): the belt's (E, L) support is
a thin band (H₁(EL) = 22.9 of 32) + ϖ 32.0 + t_p 64 − log₂N + log₂e =
90.4 bits/body = 11.3 GB. Still over; the verdict does not depend on how the
tube spec's 32 bits are read.

**E. Operational encoders** (the checker's optional ask): a faithful port of
`crates/shipmem/src/program.rs::Ef` run on the real quantized a-cells sits
**+1.06 bits/key** above the uniform multiset bound at k = 2¹⁶ and 2²⁰
(18.56 vs 17.50; 14.56 vs 13.50). On full tube keys at 10⁹, EF costs 127.2
bits/body on a belt-tight universe, 132.6 on the full 160-bit grid, vs
floor₄ 126.1. The 2× gap to the 64-bit budget is encoder-independent.

**Rate of margin loss.** H₁ grows 0.056 bits per doubling of t (0.56 bits
over 1024 orbits — the scar form grows 2.95/doubling, the absolute multiset
barely moves), so even the 3-field class's margin at 10⁹ persists ~43
doublings (t × 10¹³); the checker's "~10⁴ orbits" crossing was an unmeasured
σ-extrapolation. The 4-field class never fits.

## Predictions

All six in `predictions.md`, written before `floor9.py` ran. Held: P1
(byte-identical regeneration + 75.5/76.1), P2 (slope −1.00 ± 0.02 measured
−0.996; H₁ 90.0/90.6; floor₃(10⁹) 61.5/62.1 predicted, 61.6/62.1 measured),
P3 (phase ≈ 64, floor₄ ≈ 125.5/126.1 predicted, 125.5/126.1 measured), P4
(strict reading 92 ± 3 predicted, 90.4 measured), P5 (EF gap ≤ 3 bits,
measured +1.06), P6 (scars−floor₄: ≈ 0 then +23, measured +0.9 → +23.2).
The kill criterion (floor₄(10⁹) < 64 bits) did not trigger — within the
tube's own quanta it mathematically cannot (the phase alone is 35.5 bits/body
at 10⁹ after sorting), which is the point.

## What would make it wrong

- **The phase could be recomputed, not stored** (replay-cache): the whole
  evolution is deterministic, so the state's information content is 0 given
  program + dynamics. That is a compute-for-memory trade, not an encoding:
  one full materialization at 1024 orbits is 874 kicks/body ≈ 9×10¹¹
  evaluations at 10⁹, per pass, against 15.7 GB stored. Whether encounter
  certificates tolerate it is the parent run's open design question; if they
  do, the 8 GB verdict applies only to the non-replay regime.
- The phase quantum (64-bit per radial cycle) is the spec's own; a coarser
  phase field shrinks floor₄ bit-for-bit. That is exactly the requantization
  law being proposed, not a defect of the measurement.
- The belt is the repo's own (belt.rs) and one stirring source; a belt among
  strong resonances heats faster (raises H₁, tightens the verdict).
- Identity-as-gauge is assumed legal for the sorted class (the checker's
  caveat): the multiset form cannot answer "body #i", only physics queries.
  The identity-keeping class is measured separately (the scar row) and is
  also over budget.

## Cost of adopting, and fit with PRINCIPLES

Adoption is the parent run's, now with honest numbers: a stirred-population
doll with a storage quantum ~2⁹–2¹² coarser than the tube's, remainders
carried as integers (principle 6: "influences below one quantum accumulate"),
t_p re-anchored at kicks. Principle 24 ("the memory floor is information"):
measured, that floor at 10⁹ is 15.7 bytes-worth per body once the phase is
counted — the 7.7 GB figure was 3 of 4 fields. B18's frozen bar (≤ 2× floor
+ 2 bytes at 10⁹) is passable for neither class of a stirred belt at the
tube's quanta (floor₄ + overhead ≈ 16 GB vs 8); the stirred clause must
either requantize or accept the replay trade.

## The lens (second author) and what it missed

The lens inherits the parent's harness (same belt model, same kick law), so
its reproduction is not independent where that model is wrong; the N-scaling
and phase measurements are the genuinely new parts. It may under-weight how
much of the 126-bit scar cost is the t_p scar specifically (53→64 bits):
if the engine anchors t_p at kicks as proposed, the *stored* state's phase
content collapses and floor₄ stops being the binding number — the binding
number would then be the 3-field floor (7.7 GB, fits) plus whatever anchor
state is kept per body, which no one has measured. That measurement, not
this one, decides B18's clause.

## Record hygiene (corrections now on the record)

- `hlive.py` patched: slope-fit guard so `T_ORBITS = 2` works (0.4 s); full
  run re-verified byte-identical after the patch.
- `floor.py`'s printed GB line ("75.5 bits/body = 9.44 GB at 1e9") embeds
  the −log₂N error; its bit numbers are right, the GB line is superseded by
  `floor9.py`.
- `hlive.json`'s internal `floor` field (65.5) is the capacity-capped
  B=2¹⁶ estimate superseded by `floor.py`/`floor9.py` (the parent dossier
  never said the json disagrees with it).
- The parent claim's "raw scars 107 bits/body = 13.4 GB" matches no shipped
  number; the correct orbit-1 figure is 126.4 bits = 15.80 GB at 10⁹.
- σ_e grows 2.9× (not "doubles"); the B-ladder convergence is 55.7→58.1
  across B = 2²⁰–2²⁶ (the adaptive, bias-corrected estimator is stable to
  ±0.02 instead).

Wall time: 0.04 s (dossier); runs: 78 s + 0.4 s + 0.2 s + 0.8 s.
