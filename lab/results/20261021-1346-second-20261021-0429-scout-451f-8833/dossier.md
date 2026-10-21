# dossier.md — 20261021-1346-second-20261021-0429-scout-451f-8833

**Claim.** The checker's named gold experiment is done — both one-line fixes
plus a third instrument fix the measurement forced (the Fermi log-map's dual
projection) — and the fleet doll's second-order law falls out clean: the exit
error of the linear interior law over one relativistic flyby is exactly
**err = k·(ξ₀/r_p)** (no floor, spread ≤ 7% over ξ/r_p ∈ [10⁻⁴, 3×10⁻²]), and
the in-plane excess the checker left open is **instrument prey, not law**: with
all-order (numerically parallel-transported) member ICs, 92–99.5% of the
in-plane channel at β 0.9/0.95 is the O(ξ²) truncation of the cheap IC,
which drifts linearly in τ; the physical remainder is nearly angle-isotropic,
scales as M/r, and is ~10× *smaller* along motion.

## Bottleneck

Board row "families and formations": how long a member's certificate lasts
against its separation. 451f (silver) measured z-channel "c₂ = 78/129/239"
with two broken headline readings; the checker's gold experiment was the two
fixes plus the full grid (angles × β × r_p {18,100}M + τ shapes). This run
does that and answers the checker's open question ("the sign-fixed in-plane
excess ~9× z at 3×10⁻² is either the real second-order law or the next
instrument's prey").

## Evidence (all from `bash regen.sh`, ~3 min; tables in `analysis.txt`)

**Instrument (three fixes, each held to a control).**
F1 sign: member IC velocity = parallel transport u₀ − Γ(u₀,w), normalized
(member u·u at τ=0 ≤ 3.6×10⁻¹⁵, was up to 0.13; Fermi ξ̇(0) at the tidal-ramp
floor, no ∝ξ growth). F2 stage-E: E(u) sampled at the four RK4 stage states
(coupled RK4); the frozen scheme reproduces 451f's z bit-close (6.7227 vs
6.7232×10⁻³ at 10⁻⁴, rel 8.4×10⁻⁵; 2.3% at 3×10⁻² — my member RHS is
vectorized), and the O(h) floor dies: z@10⁻⁴ 6.7×10⁻³ → 4.076×10⁻⁴, **flat to
4 digits across nsteps 2000→16000** (reference u·u drift 3.8×10⁻¹⁰ →
1.2×10⁻¹³ over the same ladder). F3 map: the log-map's quadratic term must
project the Christoffel's upper index on the **dual** tetrad; judged against
the true exponential map (geodesic-integrated), the dual form is 5–417×
closer (along 3×10⁻²: 7.6×10⁻² → 3.3×10⁻³). Controls: eigenvalues tie 4c79's
closed forms to 1.1×10⁻¹⁴ at 7 points; reference/member u·u and orthonormality
≤ 2×10⁻¹⁰ at β 0.95; vectorized-vs-loop RHS 4.4×10⁻¹⁶.

**The law (fixed instrument, one flyby, τ = 8r_p/β from periapsis).**
err = k·u with u = ξ₀/r_p, spread ≤ 7% over 2.5 decades (z: 0.0–0.1%):
k_trunc (cheap O(ξ) ICs, the doll as it would launch members) —
along 14.6/178/666, radial 14.4/35.5/67.8, z 2.42/4.08/7.59 at β 0.5/0.9/0.95
(r_p 18M); r_p-independent in-plane (ratios 0.97–1.22 along), z 0.17.
k_exact (all-order ICs = the physical channel) — near-isotropic 2.4–5.7
in-plane and 2.3–3.1 in z (r_p 18M), along suppressed to 0.24–0.76;
**every channel scales as M/r** (r_p100/r_p18 = 0.127–0.21 vs 18/100 = 0.18);
β-dependence weak (ratios 0.3–1.7, not the γ² of the linear tide).
The τ-growth fingerprint: the truncated-IC channel grows linearly in τ
(err(τ)/err_exit ≈ τ/T, e.g. 0.250 at snap 0.25) — an initial-velocity error
free-drifting; the exact-IC channel also injects early (≤ 25% by τ ≈ 4r_p).

**Verdict on the checker's leftover.** The "~9× z" in-plane excess (their
radial probe 1.1/2.0 at β 0.9/0.95 — mine: 1.064/2.026, a third reproduction
tie) is 92–95% IC convention at β 0.9/0.95 (k_exact/k_trunc: radial 0.08/0.05,
along 0.00/0.00); z keeps 41–58% physical there, and at β 0.5 z is ~all
physical (ratio 1.08–1.17). 451f's "c₂" is a quadratic fit of a linear law:
c₂ ≈ k/u_max, which also explains its "resolution robustness" with no floor to
cancel. The "true z residual at 10⁻⁴ is 0.24–0.7%" claim refuted: it is
0.024–0.076% and equals k·u (law, not floor).

**Certificate (the board's question).** Linear law holds 1% over one flyby
for ξ₀/r_p < 0.01/k. Cheap doll: 6.9×10⁻⁴ (β 0.5), 5.6×10⁻⁵ (β 0.9),
1.5×10⁻⁵ (β 0.95) along motion — and r_p-independent, so the M1 fleet at β 0.9
must refine along-motion members at ξ/r_p ~ 5×10⁻⁵ or launch them with exact
ICs. Exact-IC doll: ~1.7×10⁻³ at r_p 18M (worst in-plane), loosening as M/r
(~10⁻² at 100M).

## Predictions (predictions.md + addendum, both written before their runs)

#1 FAILED in form, cleanly: no c₂·u² — err ∝ u exactly (the finding; purity
held: one power law, no floor). #2 HELD (repro 8.4×10⁻⁵/2.3%; fixed flat
under 8× refinement; ≥10× below frozen). #3 FAILED: no rad>z>along ordering;
k(α) has a node rotating with β (near π/4 at β 0.5, near π/8 at β 0.9) — but
the pattern is 92–99% IC convention. #4 FAILED for the cheap doll (in-plane
r_p-independent, z 0.17), HELD for exact ICs (all channels ≈ M/r). #5 HELD for
z (1.68/1.86 ≈ γ², matching 451f's frozen read), FAILED in-plane (12–46×, not
[1.5,8]); the physical channel is weakly β-dependent. #6 resolved to branch
C: the excess is instrument prey; the certificate loosens ~50× with exact ICs.
#7 FAILED: only ~10% of exit err by τ = 0.1 (the channel injects at τ ≈ 0 and
drifts; my "tide accumulates through the passage" reading was wrong — the
tide IS at τ = 0, the flyby starts at periapsis). Addendum A FAILED (my
scaling estimate for the propagated IC truncation was ~10⁴ low — the γ⁴-boosted
tetrad terms dominate); B HELD; C is what happened; D held for what is
physical (the truncated node is convention); E held (z 0.17, exact in-plane
0.13–0.21).

## What would make it wrong

k_exact still contains the deviation ODE's own convention choices (Fermi
simultaneity at O(ξ²), the map's O(ξ³) truncation ≤ 3% of signal) — a
closed-form second-order Fermi force (Marck/Manasse–Misner cubic terms) could
shift k_exact by its own convention, though not the M/r scaling or the
IC-convention split (that is measured by IC substitution alone). The truth
side (member RK4, 4000 steps) is converged flat, so k is not numerical. The
τ-linear growth of the exact-IC channel is *consistent with* early force
injection but does not by itself prove the channel is force, not residual
convention; the closed-form check named in open directions settles it.

## Cost of adopting, fit with PRINCIPLES

No engine change yet; the deliverable is the certificate sentence and the
instrument. PRINCIPLES 33 (each scale resolves only what matters at its
scale): the certificate is exactly when the linear scale stops resolving — now
a one-line rule (err = k·u, k by channel and IC convention) the fleet doll
can carry per member. P2 (error type over size): the in-plane failure was a
type (IC convention), and killing it was representation, not tuning. P26
(steal from skin in the game): the exact-IC launch is the EMRI community's
osculating bookkeeping reduced to one parallel transport per member.

## The lens (second author)

Starting from the checker's named experiment worked: every probe of theirs I
re-measured tied (×70 sign drop in radial, the halving ladder, the 1.1/2.0
values). What I nearly missed: the err ∝ u shape was visible in my first
timing cell, but I still wrote the predictions in the c₂ frame — the record's
vocabulary bent my reading exactly as it bent 451f's. The dual-map fix came
from distrusting a 20·u² "truncation" constant and testing against the exact
exponential map; derivation alone had it right but the measurement was what
licensed the change.

## Reproduce

`bash regen.sh` (~3 min): control, mapcheck, flyby (truncated ICs), flyby2
(exact ICs), conv (repro + ladder), analyze.py → analysis.txt; asserts every
control and exits nonzero on failure. Raw JSONs in this folder;
`ref-451f-flyby.json` is 451f's stored grid (repro reference).
