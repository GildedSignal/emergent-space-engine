# Dossier — 20261014-1631-redteam-e8f7 (lens: premise red-team)

**Claim.** The doll-chain simultaneity key — the designed replacement for the shipped "one tick
is the same time in every doll" convention — is falsified as a *sum of per-link shears*: at
depth ≥ 2 with relativistic links it mis-keys events by an exact, pre-registered law,
(γ₁−1)·sinh(η₂)·(v̂₂·x) for the chain-tracking form and +sinh(η₁)(γ₂−1)cosθ·(v̂₂·x) for the
frozen form, giving 15–5,067 ticks on the relativistic grid (79/108 cells ≥ 1 tick) against a
1-tick event granularity, with a third channel (the doll tick itself needs γ₁γ₂, missed by
33 % at ββ 0.5); the fix is already in the tree — compose the links' integer-shear boosts
(`lorentz.rs`) and read the key off the composed event map.

**Bottleneck.** Not a hot-path cost: the guarded invariant is causality itself — the key is
what orders the one queue and the light-cone partition (board item 4, "gravity at c";
PRINCIPLES #5 "priority is slack", #23 "nothing past c"). The shipped convention is already
known wrong at depth 1 high β (ae29's control: −110.52 ticks); this closes the other half:
the adoptable fix, as specified, is also wrong, at exactly the scenes the game sells
(relativistic nested dolls: a player battle group at β 0.3 with formations inside it, an
inspiral binary inside its nucleus doll). Expected gain of adopting the corrected form: none
in speed; it deletes a wrong convention that would otherwise be frozen in at adoption time
(ae29 is queued for re-emit). Cost of the wrong key landing: cross-doll event pairs within
10²–10³ ticks of each other's cones are computed in the wrong order — a causal-order error,
the worst error type here, and invisible to every gate.

**Evidence.** Float oracle: exact 2+1 Lorentz matrices, no shared code with any engine
harness; validated against the pre-registered analytic error law to 5.3e-12 over the whole
108-cell grid. Offsets in light-ticks (c = 1).

- Controls (both hold): depth 1 (β₂ = 0): error **0.000e+00 exactly**; depth 2 at moon speed
  (β₁ 0.5, β₂ 10⁻⁵, d 2·10³): **3.09e-3 ticks** — consistent with the record's ±0.49-tick
  depth-2 probe, which was integer-rounding-dominated at that β.
- Held-out kill rows: player group (β₁ 0.3, β₂ 0.3, 90°, d 10³): **15.2 / 15.2 ticks**
  (chain / frozen); inspiral-scale binary doll (0.5, 0.5, collinear, 2·10³): **179 / 357**;
  high-γ grandchild (0.9, 0.1, d 10³): **130 / 140**; perpendicular offset: **0.0 exactly**
  (only the along-velocity offset shears; the Wigner axis error −8.2° is real but second-order
  for the key).
- Kill grid (β₁ ∈ {0.1,0.3,0.5,0.9} × β₂ ∈ {0.01,0.1,0.3} × θ ∈ {0°,90°,180°} × d ∈
  {10²,10³,10⁴}): **79/108 cells ≥ 1 tick, 52 ≥ 10**; worst cell (0.9, 0.3, collinear, 10⁴):
  **4,070 / 5,067 ticks**.
- Doll-tick channel (β₁ = β₂ = 0.5, t_B = 10⁴): exact carries γ₁γ₂ = 1.3333; unscaled tick
  errs **6,667 ticks** (66.7 %), inner-γ-only **5,120** (51.2 %).
- Depth compounding (β 0.3 per link, d 10³): 15 → 78 → 227 (chain form) at depths 2/3/4.
- Code context, read at source: `crates/universe/src/universe.rs` ships "**The root clock is
  canonical.** A tick is the same physical time in every doll"; `crates/universe/src/step.rs`
  flags the hole itself — "the law's open question: a boost also maps an event's time";
  `crates/universe/src/lorentz.rs` already composes boosts exactly as products of three
  integer shears ("whose unrounded products are exactly the rotation and the boost").

Reproduce (0.15 s + a 5 s checker sweep of its own):

```
cd lab/results/20261014-1631-redteam-e8f7 && python3 falsifier_key_depth2.py
# or through regen.sh, which applies work/patch.diff (empty this run) first
```

**Predictions.** `predictions.md` was written before the run. What happened: the analytic law,
both control values (0 exactly; < 1 tick at moon speed) and the inspiral/high-γ rows
(predicted 180/360 and 130; measured 179/357 and 130) held; the player-group row came in at
15.2 ticks against a predicted 25–50 — my pre-registered *coefficient form* was confirmed
exactly (oracle cross-check 5.3e-12), so the miss is my arithmetic in the prediction prose,
not the law; the conclusion (≥ 1 tick, ≥ 15× granularity) is unchanged. The kill criterion
fired exactly as frozen.

**What would make it wrong.** The oracle and the analytic law agreeing is the strong part
(two independent derivations of the same matrix algebra). The weak part is the target's
reading: if ae29's re-emit composes the chain's boosts (products, not sums) and carries γ
factors on the child tick, this falsifier does not apply — but then the wiki's description
("the doll chain's integer simultaneity shear sinh(η)·x̂, frozen per entity") misdescribes
it, and `step.rs`'s open question stands anyway. Cost of adopting the fix: the composed-map
bookkeeping per doll (one matrix refresh per re-anchor, where ae29 already refreshes the
frozen shear); no cost to scenes without relativistic nested dolls. Integer-word effects
(the shear's ≤ 1-quantum rounding) are below every number here by construction (float math
sits at 10⁻³–10⁻¹² ticks where the integer path measures ±0.49).

**PRINCIPLES.** #19: "if you find yourself fixing things that's oftentimes a signal that it
is the wrong representation … the right representation always just feels right" — a time key
that is a *sum* where the physics is a *product* is the wrong representation found before the
bandaid count grew. #23 "beyond c=1 means paradoxes … it allows to cheaply partition
compute": the partition is only as sound as the key. #13 "types of errors and not just
errors": this is an ordering error, not a magnitude error. Fit with the method (draft):
events keyed by composed provenance, not by additive convenience.

**The lens may have missed:** red-teams overweight exotic cases — I ranked this by the
game's own sells (formations-in-formations at high c, inspiral binaries), but no *shipped*
scene today has a relativistic depth-2 doll, so nothing player-visible breaks this week; the
harm is freezing the wrong key at adoption (ae29 is in the adopt queue). Also unprobed here:
key *staleness* under thrust between re-anchors (adjacent, unmeasured), and whether the
frozen per-entity axis should carry the Wigner rotation for the *position* readout (the
−2.7°/−8.2° angles measured here affect the spatial side, which `bind.rs`'s turn machinery
may already own).

**Rung criterion that should have caught it:** none exists. P6/B8/B13 key depth-1 dolls; the
one depth-2 probe on record ran at moon speed; r3 judges handoff physics through B12's
Jacobi constant; r5 has no relativistic nested dolls. The freeze-ready addition: a P6 arm
with β₁·β₂ ≥ 0.09 (depth 2) whose negative control is the additive key (must miss by ≥ 10
ticks) and whose positive control is the composed-boost key (must hold ≤ 1 tick).

**Wiki:** page `handoff` (the Keys section); update written to `wiki/handoff.md` in this folder.
