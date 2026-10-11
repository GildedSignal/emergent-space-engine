# Dossier: second author on 20261011-1456-scout-126c — the record now regenerates, and the valley rescue holds on the law's fixed cuts

**Run:** 20261011-1600-second-20261011-1456-scout-126c-640f (second-author lens on the silver
20261011-1456-scout-126c). **Machine:** Linux CI, 8 vCPU. Wall: 27 s per full run.

## Claim

The silver's claim, now with the checker's named experiment done: extended Darwin variables
(cosh-phase continuation of the law's own Darwin cycle, root-structure classification,
anchored root pairing) cover plunge and near-radial sectors at bound-cycle panel cost —
including, new in this run, the near-separatrix valley on the law's **fixed integer cut
layout** (dyadic rungs toward the barrier top, log(1/δ) panel growth, oracle-verified
≤ 1e-6 for δ ≥ 1e-8 at ≤ 75 panels) and kicks landing **in** the valley (uniform panels
fail at δ ≤ 1e-6; the fixed ladder holds ≤ 1.1e-7 at ≤ 71 panels) — and every number in
`metrics.json` now regenerates from one command, `python3 falsifier.py` (27 s, two
consecutive runs bit-identical except the machine stamp).

## Bottleneck

Same as the silver's (board: "plunge and radial tubes", deletes the NoBoundOrbit refusal
class), plus the record bottleneck the checker named: "results that the shipped code could
not regenerate" (taste log, 5 October). This run deletes the latter for this
representation: the two orphaned keys regenerate, and the valley rescue is measured on the
compiler's own cuts rather than adaptive float bisection.

## Evidence (all in `metrics.json`; reproduce: `python3 falsifier.py`, ~27 s)

**The record.** E1–E6 are bit-identical to the prior stored record (`diff` command below);
`separatrix_valley_panels_to_1e-11` (43/83/133/205/3765) regenerates exactly, now called
from `main()`; `bound_control_apo_to_peri` is a live path (the shipped block was dead: at
`r_end = r₂` the plunge event is a tangential touch a direction-filtered event can never
fire on — and any `r₂+ε` with ε ≲ 1e-3·span dips below and back within one DOP853 step,
so the event still never fires). Consecutive runs differ only in `machine`/`wall_seconds`.

**The valley on fixed cuts (E7, `separatrix_valley_fixed_ladder`).** Layout: uniform base
of 32 panels + dyadic rungs η_U ± h₀·2^(−j/m) toward the barrier top η(r_U) down to
σ/2, where σ = |Im η*| is the phase image of the complex root pair (σ = 2.56·√δ at L̃² =
13) — every quantity a fixed function of (E, L), the same cubic the classification
factors; no integrand probing. Oracle-verified terminal errors (factored R):

| δ | panels m=1 | err m=1 | panels m=2 | err m=2 | oracle's own shift at rtol 1e-13 |
|---|---|---|---|---|---|
| 1e-2 | 32 | 5.0e-12 | 32 | 5.0e-12 | 6.4e-13 |
| 1e-4 | 41 | 4.1e-8 | 47 | 3.6e-8 | 1.3e-11 |
| 1e-6 | 47 | 1.7e-7 | 59 | 2.8e-8 | 8.3e-10 |
| 1e-8 | 55 | 3.0e-7 | 75 | 5.3e-8 | 4.9e-8 |
| 1e-10 | 61 | 6.5e-6 | 87 | 7.0e-6 | 4.1e-6 |

Against the tighter rtol-1e-13 truth the m=2 ladder reads 4.8e-12 / 3.6e-8 / 2.9e-8 /
**4.1e-9 / 2.9e-6**: at δ = 1e-8 the fixed layout is at 4e-9, and at δ = 1e-10 the
ladder's deviation is *within the oracle's own 4.1e-6 uncertainty* — the DOP853 truth
degrades near the barrier top because the crossing time depends on E² like 1/δ (the
stepper's error is amplified; the quadrature candidate has no such instability). Panel
growth is log(1/δ), ≈ 4 per decade, under the adaptive float bisection counts
(43/83/133/205/3765) at every δ ≤ 1e-4, and under both the P2 budget (96) and the bound
cycle's own B9 budget (~78 at m = 16) throughout. `Rfun = E² − V_eff` and the law's
root-factored R agree everywhere here (the Rfun cancellation floor I predicted did not
materialise as the limiter: the layout, then the oracle, limit first).

**Valley kicks (E8, `valley_kicks`).** A bound orbit kicked at deterministic phases into
E²_k = V_max(1+δ): uniform 64 panels give 1.6e-8…1.3e-7 at δ = 1e-4 (holds) but
7.5e-4…4.9e-3 at δ = 1e-6 and 9.0e-2…2.5e-1 at δ = 1e-8 (fails, reproducing the
checker's finding). The fixed ladder: m=1 ≤ 4.9e-7 at ≤ 53 panels; m=2 ≤ 1.1e-7 at
≤ 71 panels. **P7's true domain:** the kick claim holds with uniform-η panels only for
kicks clearing V_max by δ ≳ 1e-4 (σ ≳ panel width); below that the valley layout is
required, and with it the claim extends to δ = 1e-8 at the same panel budget.

**Bound control (revived `bound_control_apo_to_peri`).** All three seeds run. Reference:
a parametrization-free radial quadrature r = r₂ + (r₃−r₂)·sin²θ at the exact root
endpoints (absorbs 1/√R at both turning points; self-convergence recorded). Candidate vs
quadrature: 4.6e-10 / 8.1e-10 / 5.5e-8@8→4.4e-11@16 (mid-field / near-circular /
near-Vmax), flat because the 4096-panel θ-quadrature is itself the reference's limit
(recorded). The oracle's turn-event endpoint carries a √δ-amplified floor
(2√(|r_fin−r₂|/R′(r₂))/τ_half: predicted 4.2e-7, measured 3.7e-7 on the near-circular
seed) — recorded with its prediction, not hidden.

**A new trap, found and fixed (for the b-plunge-tubes builder).** `eta_of_r` at a turning
point: arccos′(±1) = ∞, so a few-ulp error in c = (u−f)/A becomes a ~1e-7 error in η, and
the missing turning-point sliver costs a further ~√δ in τ — a flat, panel-independent
~1e-9 offset (this, not the oracle's event, was the dominant part of the checker's
"endpoint-bookkeeping floor"). The turning points are η = −π, 0 **by construction**: use
them directly; same on the cosh branch (η₀). The shipped fix documents this in code.

## Predictions (`predictions.md`, written before the decisive run)

P-D held fully (E1–E6 bit-identical; both orphaned keys regenerate; two consecutive runs
agree). P-B held in structure but over-claimed accuracy: uniform fails at δ ≤ 1e-6 as
predicted, and the ladder holds ≤ 1e-6 at ≤ 71 panels (predicted ≤ 64, ≤ 1e-9 — the panel
count held, the accuracy claim failed by ~2.5 decades). P-A: panel counts held (32/41/47/
55/61 vs predicted ≈ 32/38/44/52/58), the ≤ 1e-9 accuracy target **failed** (4.1e-8…
3.0e-7 for δ ∈ [1e-4, 1e-8] at m=1; 2.8e-8…5.3e-8 at m=2; 4.1e-9 at δ = 1e-8 against the
rtol-1e-13 truth), the ≤ 1e-6 kill line held at every δ ≥ 1e-8, and at δ = 1e-10 the
comparison is truth-limited (oracle shift 4.1e-6 ≥ ladder deviation). The predicted
Rfun-cancellation floor did not appear (fun ≈ factored). The m=2 measurement is
post-prediction, disclosed as such in the code. P-C held (all three seeds run; the
near-circular 8-panel value 8.1e-10 is better than my ≤ 5e-8 line because the endpoint
trap fix removed the flat floor I had predicted would remain). No kill criterion tripped.

## What would make it wrong

- The layout's ~3e-7 (m=1) mid-range error is the transition rungs (m=2 cuts it ~6×;
  m=4 adds nothing): if the integer compiler's rung placement cannot follow the same
  ratio, its valley error is the m=1 column. The finest rungs and the base are not the
  limiters (safety=4 and base=64 change nothing at δ ≤ 1e-8).
- δ ≤ 1e-10 is unfalsifiable against this float oracle (its own error bar exceeds the
  candidate's deviation). The integer law's quadrature has no stepper instability, but
  that claim is inference, not measurement.
- The oracle and the candidate still share R's algebra; the first-integral violation
  (≤ 1.4e-13) and the sin²θ quadrature triangulate but do not remove this.
- Kerr, γ ≫ 1 direct plunges, and the L = 0 radial path remain outside, as in the silver.

## Cost of adopting, and fit

Same as the silver's (one sector extension of `crates/space`), now with the cut rule
concrete: base 32 + dyadic rungs to σ/2 at m = 2 rungs per octave, σ from the complex
root pair, η(r_U) from the critical radius — all integer-law-native (B9's "band edges
are cuts in ψ", m a per-octave integer). Fit: principle 19 — the fix for the valley was
not a new category but the law's own geometric bands applied to the distance from the
barrier top; and principle 13 — the layout error is fixed by construction (same cuts ⇒
same error every evaluation), it does not compound.

## The lens (what the second-author lens may have missed)

The named experiment was record-shaped, and I nearly shipped a "working" bound control
that was still floor-limited twice over (the oracle's event, then the candidate's arccos
endpoint) — only triangulating three references exposed the endpoint trap. The m=2 rung
choice is measured, not derived; the builder should re-derive the per-octave count from
the panel-error budget rather than adopt 2 because it measured well here. I did not
touch the integer side (bit-reversible carries, exact roots), so the "no float floor in
integer arithmetic" claim stays inference.

## Reproduce

```
cd lab/results/20261011-1600-second-20261011-1456-scout-126c-640f
python3 falsifier.py          # ~27 s, writes metrics.json, exit 0
# bit-identity of E1-E6 with the prior stored record:
git show origin/claude/lab-20261011-1456-scout-126c:lab/results/20261011-1456-scout-126c/metrics.json > /tmp/prior.json
python3 - <<'EOF'
import json
new = json.load(open("metrics.json")); old = json.load(open("/tmp/prior.json"))
print([k for k in old if k not in ("machine","wall_seconds",
      "separatrix_valley_panels_to_1e-11","bound_control_apo_to_peri") and new[k] != old[k]])
EOF   # -> []  (every prior physics key bit-identical)
```
