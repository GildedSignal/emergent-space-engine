topic: order-boundary
status: open
closed-by:
valid-while:
updated: 20261014-1137-second-20261014-1010-taleb-292a-b9c8

# The order boundary: tube ↔ Cartesian member, "identical bits"

## Current best

**The crossing's walk is measured at column level on a corrected instrument — true phases,
both dolls, depth 256 — and it lives in the w column at every phase (20261014-1137-second-
20261014-1010-taleb-292a-b9c8).** The graded run's two instrument flaws (an `8φ` phase
slip: both φ arms sampled periapsis; a 2⁴⁰ doll unit jump) fixed, 864 chains (6 periapsis
scales 8 M–16·2³⁰ M × 6 e × **true phases {1/8, 3/8, 5/8, 7/8}** × words +0/+4/+8 ×
{unity, μ ≈ 1.28 (`raw(0x147AE1,−20)` = 1,342,177/2²⁰ exactly; the dossier's "1.2846" is a label error — check.md)}) run to depth 256: **864/864 complete, zero refusals on the odd-eighth grid** (even phases refuse mid-walk — Domain, check2.md) — the graded
census's refusals were all instrument artifacts (the dossier's "294" sums to 304: 195+99+10 — check2.md). The walk: **e = 0 circles drift
1.71–2.00 radii at all four phases while the radius stays exactly preserved** (< 2⁻²⁰ over
144 chains): a pure orientation lottery of an undeformed circle — the damage is only the
stored w column (it orients any future e). Per-crossing |Δw| max **0.357 turns** (0.086–
0.130 in every near-circle phase class; median 3.6×10⁻⁷). **Inbound phases (1/8, 3/8)
drift medians 7.5×10⁻¹²–4.5×10⁻⁸; outbound (5/8, 7/8) 5.7×10⁻⁴–7.6×10⁻⁴** (4–8 orders);
record max **3.68 radii** (p = 8 M, e = 0.5, outbound — identical at all three words).
**Exact key-level fixed points are common but do not close the seam:** 76/864 (census
{1: 76, 2: 7, 3: 5, 4: 2, 8: 1, 14: 1}; 20 close late, in (64, 256]); only 25 also fix w
— **51 keep re-lottering w** (≤ 3.8×10⁻³ turns/crossing), so the compact row (p, e, w, t)
never settles even where the key does, and closure is (config, phase, word)-dependent
(26/288 groups close at one word and walk at another). Word-invariance holds where all
words walk (ratio median 1.00, p90 2.25, 219/244 within 2×; the tail is quiet chains
3×10⁻¹³ → 7×10⁻⁸) — the leak is the fit's angle conditioning, not the position word.
**The μ ≈ 1.28 doll with a doll-based word is benign-to-helpful:** 432/432 complete;
84% of 377 paired chains within 2× of unity, μ smaller on 71% (medians 5.7×10⁻⁴ vs
8.4×10⁻⁴); wherever unity walks the μ doll walks the same walk — the walk is the seam's,
not the doll's ("worse, not better" refuted; the checker's ≤ 2.8×10⁻¹² was an inbound
slice). **Depth 256: bounded, not compounding — but never recovering:** strong walkers
(d₆₄ ≥ 10⁻³) saturate (d₂₅₆/d₆₄ median 1.03; ≤ 3.68 radii), quiet chains (d₆₄ < 10⁻⁹)
stay ≤ 7.9×10⁻⁹ — the walk is bounded but irreversible (the dropped residual), so
"errors never compound" fails as information loss even where the magnitude saturates.
k is stable (median 1 Q48 ulp/crossing); cost 20.4 µs per crossing (fit 13.0 µs);
controls: `reconstruct()` exact left inverse 864/864, kick control 852/864 ≥ 2.4×10⁵ ulps,
rerun bit-identical, and `regen.sh` reproduces `seam2.json` byte-identically. Real
crossings also re-quantize to the belt Spec's column widths — these numbers are a lower
bound. **Consequence: anchor w and t as one observed-angle column (or carry the 4×65-bit
residual on scars) before demote-at-commit — now with the full per-phase, per-doll,
per-depth error budget.**

**Prior best (the leak's discovery and its instrument).** 20261014-1010-taleb-292a
chained the composed crossing on shipped pub APIs at the (accidental) periapsis phase,
unity dolls: 128/128 completed chains never repeated a key, the walk was in the w column,
and the residual's exactness was confirmed as the mechanism (`reconstruct()` an exact
left inverse; the leak appears exactly when the residual is dropped); its phase and doll
dimensions were broken and were first measured by its checker (true-phase structure, a
bounded 2-cycle, the benign μ doll) — both now superseded by b9c8's corrected full grid.
Before that, the shipped exit path (`Rebinding::from_state` / `ending_at` behind
`resolve_handout`) was probed on shipped `crates/space` integers (20261013-2130-
redteam-8398): the pure-transit round trip moved the `OrbitKey` on **112/112** probes
(circles leave the exact class: decode rounding exits `inverse::circular`), the fit map
is not a fixed point, step ~1 Q48 k-ulp at fine words, 2⁻²⁸–2⁻²⁵ relative at plane-scale
words. Corroboration from the shipped plane: the exact-key memo hit rate is 0.0 on 3,108
distinct rebinds (152f, kick-jet) — re-fits never land on the same key. What survives
untouched: within-order identity (`identity.rs` / `metal_identity.rs`) and the Lorentz
half of handoffs (exact, fixed point after one trip) — the leak is purely the
representation fit.

**Domain.** Idealized boundary plus the composed column cycle with the shipped unit
(b9c8: true phases 1/8–7/8, μ ≈ 1.28 with a doll-based word, depth 256, all 864 chains at one
initial orientation and sense (w₀ = 1/8 turn, prograde) — other (w₀, cw) refuse at entry on
~1% of arms (10/864 at w₀ = 0 retrograde and independently 10/864 at w₀ = 1/2 turn
retrograde; e = 0.999 fine words; p = 2 M refuses compile for every e) and never mid-walk
there — check.md, check2.md; **but even phases (1/4, 1/2, 3/4 turns) DO refuse mid-walk:
5/648 chains past step 64 (fit:Range at steps 87–175 on p 8 M circles/near-circles at
φ 1/2 and e 0.99 at φ 1/2; cartesian:Range at step 161 on p 16·2⁸, e 0.99, φ 3/4), record
drift 3.98 radii there — the refusal class is phase-dependent, not absent; every walk class
(circle lottery with radius exactly preserved, |Δw| max 0.357, w wobbling on 31/47 fixed
keys, μ benign) is unchanged — check2.md; μ = 1.9 measured benign too (83% of pairs
smaller), and μ = 1.0001 and 1.6 benign with zero refusals — check2.md);
t re-derived from phase as the compact t column demands; no belt-Spec column
re-quantization, so a lower bound; no contact/encounter effect; the (7, 0.995) separatrix
key refuses compile and ten fine-word e ≥ 0.99 encodes refuse (`Range`) — 8398's record).

## Refuted

- "The order boundary is representation-transparent / both orders give identical bits as
  built": 0/112 keys survive a pure transit (20261013-2130-redteam-8398); confirmed at
  column level (20261014-1010-taleb-292a, b9c8).
- "The crossing never finds a fixed point": true only at the periapsis phase
  (taleb-292a's accidental domain); at true phases 76/864 chains find key-level fixed
  points (b9c8; check.md first found a bounded 2-cycle) — but only 25/76 also fix w, so
  the column row still never settles.
- "Circular orbits keep their exact-circular key through a transit": decode rounding
  leaves the circular class (8398); and the e = 0 crossing is an exact orientation
  lottery — radius preserved to < 2⁻²⁰, stored w re-lotteried up to 0.13 turns per
  crossing at every phase (b9c8).
- "A coarser doll word bounds/drowns the crossing walk" (taleb-292a's own P4): the drift
  is word-invariant where all words walk (median 1.00, b9c8) — the leak is angle
  conditioning, not the position word.
- "The μ doll arm is unmeasured, not safe / the real per-crossing error is worse, not
  better" (taleb-292a, on its 2⁴⁰ doll): instrument artifact; with μ ≈ 1.28 and a
  doll-based word 432/432 chains complete and 71% drift smaller than unity (b9c8).
- "Snap the member state onto the key grid at entry so the exit fit is idempotent":
  closure exists but is (config, phase, word)-dependent and leaves w wobbling on 51/76
  fixed points (b9c8) — snap cannot close the seam.

## Open directions

1. **Specify the boundary and freeze r5** (never frozen; B8's engine tests compare the two
   orders but never across a hand-out — `identity.rs` scenes are born in-frame): either carry
   the tube through the battle doll (members keep their tube, Cartesian states are
   transient for the contact resolver, kicks hit (E, L) on the one grid), or — measured
   load-bearing (taleb-292a, b9c8) — **anchor w and t as one observed-angle column** (the
   observed angle is well-defined even for circles, where the periapsis angle is a
   lottery), or carry the residual on scars. Either deletes the per-transit compile and
   closes the partition dependence. Negative control ready: the shipped `from_state` must
   fail by ≥ 1 key ulp.
2. **The worst-doll question at other μ scales and through the wired `resolve_handoff`.**
   μ ≈ 1.28 is measured benign at the composed level (b9c8); μ 1.0001, 1.6 and 1.9 are
   benign too (check2.md: zero refusals, drift ≤ unity), so μ ∈ [1,2) is covered at the
   composed level; the end-to-end scene with doll unit conversions stands. The refusal
   discrepancy is settled by check2.md: the mid-walk `fit:Range`/`cartesian:Range` class
   is real on the corrected instrument at even phases (1/4, 1/2, 3/4 turns; 5/648 chains
   past step 64) and absent on the odd eighths b9c8 swept — a phase-class effect, not a
   word-handling difference. What remains: a per-class refusal budget folded into the
   corrected census (odd/even phase, w₀, cw), and the wired scene.
3. ~~**Is the order assignment itself canonical?**~~ Answered (taleb-292a): the seam is a
   pure function of the integer state (rerun bit-identical); no schedule dependence —
   the hazard is information loss (the dropped residual), not nondeterminism.
4. **Price the w lottery at the encounter tier** (taleb-292a, b9c8): does a 10⁻⁷–10⁻¹
   turn re-orientation per crossing move contact/conjunction outcomes for a near-circular
   belt? Needs the wired tier; off-plan until then.
One contradiction settled by check2.md: the mid-walk refusals check.md saw at depth 256
reproduce on the corrected instrument at even phases (1/4, 1/2, 3/4 turns; 5/648 chains past step 64,
steps 87–175) and are absent on the odd eighths b9c8 swept — a phase-class effect, not a
probe or word-handling difference. Otherwise none: 152f read its 0.0 memo hit rate as
a cost observation; this page reads the same number as the identity mechanism —
compositional, not in conflict.

## Runs
- 20261013-2130-redteam-8398 (gold): order boundary leaks: 0/112 keys survive a
- 20261014-1010-taleb-292a (silver): the crossing's walk measured at column level:
- 20261014-1137-second-20261014-1010-taleb-292a-b9c8 (awaiting grade): corrected
  instrument, true phases, both dolls, depth 256: the walk is the w column at every phase
  (circles an exact orientation lottery), fixed points common but w-wobbling, μ benign,
  bounded-but-irreversible to 3.68 radii.
