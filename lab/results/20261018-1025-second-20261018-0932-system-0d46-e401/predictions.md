# Predictions (written before the decisive run)

Second-author run on 0d46 (silver). The checker's named gold experiment, in its own order:

1. **D (the decomposition, asked first).** The shipped gather's body loop splits into the crossing
   walk (Newton + `state_rate` readouts: binding_at, tube decode, doll-chain, rate) and the row
   math (lookups + `push`). 51bf found the crossing loop 95% on the 28-body plane. On the crowd
   (428 bodies, mostly handed-out members of one ring in Home's doll, warm cache ~2 readouts per
   emitter) I predict **the crossing call is ≥ 60% of the body-loop time** (D1). If it is < 50%,
   row math dominates and the gather half of 0d46's claim weakens to the scan half — I will say so.

2. **C (the census / coverage).** The handed-out members group by (compiled orbit key, periapsis
   angle, doll). efd4 found 513 entries → 2 intern keys on a formation. I predict **≥ 300 of the
   428 bodies sit in shared-key groups of size ≥ 8** (C1). Eligibility: a member is tier-eligible
   only while its readout is a pure tube (no live kick/partial step at the emission probes) and it
   has not rebound between `t_now` and its emission tick. I do not know the live-kick fraction and
   pre-register it as the main coverage risk: **≥ 30% of crowd members eligible per frame** (C2);
   the ineligible ones degrade to the individual read by construction.

3. **A (the audit).** Tier rows are built from one shared closed form (R, ω fitted from two
   reference decodes, a shared per-frame doll-centre line C(t) = C0 + VC·(t − t_now), per-member
   phase word = the tube's periapsis time) and the same `push` math as the shipped row. Compared
   against the shipped rows with 2df1's standard (sky-polar pixel at R_SKY = 432 px over
   log10 ls ∈ [−5, 3.6]; panel tolerance 1e-4 relative on light_seconds, closing, shift), I
   predict **≥ 99% of audited rows display-exact** (A1) and **max |Δt_e| ≤ 1 tick** on ≥ 99% of
   rows (A2). The named risk: the polar-angle test (ω fit error × the ±9,500-tick emission window)
   and the dropped per-member turn/residual words (≤ 2 position quanta each).

4. **P (the price).** Shipped per-body on this box: ~7–13 µs (0d46 author/checker band). I predict
   the tier's per-body cost **≤ 0.3 µs** (closed-form bracket solve + row math; P1) and the census
   walk **≤ 1 µs/body** (it is the scan's capture walk, one `binding_at`; P2) — so the gather's
   crowd term falls ≥ 20× and the census is the one walk both walkers share (the scan's 224 B per
   candidate pin rides the same words — the two wins separated: per-frame CPU for the gather,
   per-capture bytes for the scan).

Kill criteria for the gold claim: crossing < 50% of the body loop, or audit display-exact < 95%
at panel tolerance, or tier cost ≥ 1 µs/body. Then the claim shrinks to the scan half (0d46's own
named risk) and I report which.
