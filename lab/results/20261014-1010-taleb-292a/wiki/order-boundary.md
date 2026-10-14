topic: order-boundary
status: open
closed-by:
valid-while:
updated: 20261014-1010-taleb-292a

# The order boundary: tube ↔ Cartesian member, "identical bits"

## Current best

**The crossing's walk is measured at column level, it lives in the w column, and no word
choice can bound it (20261014-1010-taleb-292a).** Chaining the composed crossing the
ephemeral-promotion design will multiply (columns → compile → state at phase → cartesian
→ columns′, shipped pub APIs, the shipped `decode` unit handling) on 432 configurations
(p 8 M–16·2³⁰ M, e 0–0.99, word +0/+4/+8, depth 64 — **both φ arms sampled periapsis**, a
`raw(φ,3)`=8φ·P sign slip, so the intended phases 1/8 and 3/8 were never run, and the
"μ≈1.28" doll was μ≈1.4×10¹² (same convention), all 216 of its arms refusing — check.md):
**128/128 completed chains (all unity, all at the periapsis phase) never repeat a key**
(3 one-step repeats), per-crossing |Δw| median 1.4×10⁻⁵ turns, max **0.31 turns per
crossing** (near-circles e ≤ 0.001; strong-field/high-e arms at p 8–4096 M), k stable
(median ≤ 1 Q48 ulp/crossing; 6–14 directed walks, worst −2.3×10⁶ ulps over 64 — an e = 0
circle at p = 8 M), decoded state drift over 64 crossings median 6.4×10⁻³ of the radius
(min 3.9×10⁻⁷ at p = 16·2³⁰, **e = 0.99**, max 3.36 — scrambled), **identical to 3 digits
across word coarsenings +0/+4/+8 (per-config too: 44/44 paired chains within 2.1×, median
ratio 1.00 — check.md): the leak is the fit's angle conditioning (Q32 periapsis angle,
Q61/Q62 trig), not the position word**. Cost 22.8–32 µs per crossing (fit 13–19 µs — b29a's
refit class). The
residual's exactness is confirmed as the mechanism: `reconstruct()` is an exact left
inverse on 128/128 (controls: a real kick moves k by 1.3×10⁷–9.7×10¹¹ ulps; rerun
bit-identical) — the leak appears exactly when the residual is dropped, as the compact row
(`shipmem::Body` = p, e, w, t) does. **Direction 3 answered: the seam is a pure function
of the integer state — no schedule dependence; the hazard is information loss.** The μ
doll arm as built is an instrument artifact (the 2⁴⁰ unit jump, not a word-margin effect);
99 extreme-apoapsis arms and 10 fit arms refuse and are
counted. Real crossings also re-quantize to the belt Spec's column widths — these numbers
are a lower bound. **Consequence for the adopted design: demote-at-commit cannot land on
today's columns; w and t must be anchored as one observed-angle column (or the 4×65-bit
residual carried on scars) first** — b29a's "w/t anchoring is a wiring decision" is now a
measured error budget. **Checker extensions (check.md): the walk is strongly phase-dependent
— at true phases the drift spans 10⁻¹³–10⁻⁷ (inbound 1/8, 3/8) to O(1) (outbound, strong
field, up to 3.7), one bounded 2-cycle exists (p 16·2³⁰, e 0.99, φ 1/8), the near-circle
lottery walks ~1.7 radius at every phase, depth 256 shows saturation with mid-walk refusals
(fit:Range — the promote-to-live trigger), and the μ doll with a doll-based word completes
108/108 with drift ≤ 2.8×10⁻¹²: the doll conversion is benign-to-helpful, refuting the
"worse, not better" caution.**

**Prior best (the leak's discovery).** The shipped exit path
(`Rebinding::from_state` / `ending_at` behind `resolve_handout`, bind.rs:265-266) was probed
on shipped `crates/space` integers: the pure-transit round trip key → decoded state → refit
moved the `OrbitKey` on **112/112** probes (0/112 kept the key; 15 keys, p 7–1000, e 0–0.999,
four phases, two word scales), including circles (e = 0 → dk = 2^19 Q48 ulps: decode rounding
pushes the state out of `inverse::circular`'s exact class, so even class is not preserved),
and the fit map is **not a fixed point** (second-transit refits moved the key again on all
11 keys that ran — three high-eccentricity keys refuse silently in the control loop —
periapsis-angle wrap-by-one at e = 0.9, residual2 ~10⁻⁹ relative): repeated transits walk
(principle 13). Step size ~1 Q48 k-ulp at fine words, 2⁻²⁸–2⁻²⁵ relative at plane-scale
words (the (p 20, e 0.7, inbound 3/4) coarse row drifts 655665 Q48 ulps ≈ 2⁻²⁸·⁷); the
worst fine-word future divergence in the stored table is 1.92×10¹¹ position ulps at
(p 8, e 0.99, inbound 3/4) — phase mis-anchor near periapsis, not uniform noise.
Single-transit error is below any player floor; the live risks are the unbounded walk
(checkers, check.md and check2.md: no full-key repeat in chained transits to depth 16 and to
depth 64 on six configurations, and at fine words the drift is one-signed — a directed walk,
−1 k-ulp per transit, floor-bias; at coarse words the drift is +7.0×10⁷ ulps over 64
transits) and the per-transit cost (each crossing mints a Catalogue entry + one compile,
5.8–374 µs — the same lever as frame-cost's sticky promotions and hand-out retries).
Corroboration from the shipped plane: the exact-key memo hit rate is 0.0 on 3,108 distinct
rebinds (152f, kick-jet) — re-fits never land on the same key. What survives untouched:
within-order identity (Chronon vs EventCore vs Metal digests, engine `identity.rs` /
`metal_identity.rs`) and the Lorentz half of handoffs (exact, fixed point after one trip,
`lorentz.rs` tests) — the leak is purely the representation fit.

**Domain.** Idealized boundary plus the composed column cycle with the shipped unit
handling (taleb-292a: unity dolls, **one phase** — both φ arms sampled periapsis and the μ
doll was mis-scaled by 2⁴⁰, so both dimensions are checker-measured in check.md: true
phases 1/8–7/8 and the μ doll with a doll-based word, 108/108 complete, drift ≤ 2.8×10⁻¹²;
t re-derived from phase as the compact t column demands; no belt-Spec column
re-quantization, so a lower bound; no contact/encounter effect). The prior run: no doll
unit conversions — the shipped path adds rounding; the (7, 0.995) separatrix key refuses
compile and ten fine-word e ≥ 0.99 encodes refuse (`Range`). Checker extensions (8398's
check.md, check2.md): the leak persists at p = 10⁴–10⁷, e = 0.9999, retrograde sense, and
unbound passages (where k can be stable while the full key still walks); no convergence to
depth 64.

## Refuted

- "The order boundary is representation-transparent / both orders give identical bits as
  built": 0/112 keys survive a pure transit; no fixed point (20261013-2130-redteam-8398);
  confirmed at column level, 128/128 chains at the periapsis phase, no key repeat to
  depth 64 (20261014-1010-taleb-292a; check.md: phase-dependent — one bounded 2-cycle at
  φ 1/8, near-circles walk at every phase).
- "Circular orbits keep their exact-circular key through a transit": decode rounding leaves
  the circular class (8398); and the e = 0 circle at p = 8 M carries one of the directed
  k-walks (−2.3×10⁶ ulps over 64, taleb-292a).
- "A coarser doll word bounds/drowns the crossing walk" (taleb-292a's own P4): the 64-cycle
  state drift is identical to 3 digits at word +0/+4/+8 — the leak is angle conditioning,
  not the position word (20261014-1010-taleb-292a).
- "Snap the member state onto the key grid at entry so the exit fit is idempotent": no
  fixed point or short cycle on the fit's own image at column level at periapsis
  (3 one-step repeats / 128 chains; taleb-292a), consistent with 8398's second-transit
  refits — snap cannot close the seam (one 2-cycle exists elsewhere, check.md — not a
  general closure).

## Open directions

1. **Specify the boundary and freeze r5** (never frozen; B8's engine tests compare the two
   orders but never across a hand-out — `identity.rs` scenes are born in-frame): either carry
   the tube through the battle doll (members keep their tube, Cartesian
   states are transient for the contact resolver, kicks hit (E, L) on the one grid), or —
   now measured load-bearing (taleb-292a) — **anchor w and t as one observed-angle column**
   (the observed angle is well-defined even for circles, where the periapsis angle is a
   lottery), or carry the residual on scars. Either deletes the per-transit compile and
   closes the partition dependence. Negative control ready: the shipped `from_state` must
   fail by ≥ 1 key ulp.
2. **An end-to-end scene through `resolve_handout` with doll unit conversions.** The μ doll
   arm is now measured at the composed level (check.md: benign-to-helpful, ≤ 2.8×10⁻¹², the
   coarser tube lattice may even close the fit — possibly the cheapest answer to the w/t
   contract); what stands is the worst-doll question at other μ scales and through the
   wired `resolve_handout`. (The walk's convergence depth is measured: none to
   depth 64, directed at fine words — check.md, check2.md; column level: no repeat on
   128/128 at periapsis, one bounded 2-cycle at (p 16·2³⁰, e 0.99, φ 1/8) — taleb-292a,
   check.md.)
3. ~~**Is the order assignment itself canonical?**~~ Answered (taleb-292a): the seam is a
   pure function of the integer state (rerun bit-identical); no schedule dependence —
   the hazard is information loss (the dropped residual), not nondeterminism.
4. **Price the w lottery at the encounter tier** (taleb-292a): does a 10⁻⁵–10⁻¹ turn
   re-orientation per crossing move contact/conjunction outcomes for a near-circular belt?
   Needs the wired tier; off-plan until then.

## Contradictions

None. 152f read its 0.0 memo hit rate as a cost observation; this page reads the same
number as the identity mechanism — compositional, not in conflict. taleb-292a's
word-invariance refutes its own prediction (P4), not any prior run's claim.

## Runs
- 20261013-2130-redteam-8398 (awaiting grade): order boundary leaks: 0/112 keys survive a
  pure transit, no fixed point; circles lose their class; r5 absent.
- 20261014-1010-taleb-292a (awaiting grade): the crossing's walk measured at column level:
  no key repeat on 128/128, the w column is the walker (median 1.4×10⁻⁵, max 0.31 turns per
  crossing near circles), state drift 6.4×10⁻³ median over 64 crossings, word-invariant;
  seam canonical (pure function); demote-at-commit blocked on w/t anchoring or residual carry.
