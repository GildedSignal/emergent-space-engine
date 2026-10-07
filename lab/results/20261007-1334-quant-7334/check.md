# Check — 20261007-1334-quant-7334

Grade: silver

**Abstract.** Claim: a Jupiter-forced belt scars 100% of bodies within one orbit under the shipped
scar semantics; the scar field is 22–38 bits/body (2.8–4.8 GB at 10⁹) yet creates ~0 bits per
game-second, so program+scars survives only if the program embeds the compiled secular field.
Reproduced bit-for-bit from `belt_hlive.py` (38 s: 23.07/33.82/38.43 bits at t=1 yr; flat to
100 yr; tail +9.5%). Adversarial: solver noise is 160–1050× below the scar spread (dt 1/32 vs
1/128); a 2:1-resonance belt leaks +0.66 bits/decade; the kNN floor is robust to adding birth
phase (−1.8 bits). Gain: kills the naive belt store (180× over the 0.126-bit born floor). Cost
to adopt: a design constraint on b-h-live/b-belt-wire, nothing to build. Silver because P2 and
P3 were falsified (honestly reported) and the constructive half — the compiled secular field
actually re-deriving the belt — is asserted, not measured.

## Reasons

1. **Reproduction: exact.** The shipped command regenerates every dossier number (deterministic
   seed): main-scene H_raw 23.07/33.82/38.43 bits at 1 yr, 22.50/33.36/38.36 at 10 yr,
   23.41/33.98/38.46 at 100 yr; H_knn 23.76→22.63; scarred fraction 1.000 at 1 yr; tail 25.63
   vs 23.41 (+9.5%). Ledger arithmetic checks at 2⁻²⁰/2⁻²⁴ (2.9/4.3 GB); the headline's top end
   is understated — 38.5 bits is 4.8 GB, not 4.3 (see Misses). Note: the reproduce command
   rewrites `hlive.json`; I ran it, content regenerated identically (7688 B, same values).
2. **Predictions.** `predictions.md` mtime 13:44 < decisive output 13:55 (log order consistent).
   P1 held (100% ≤ 1 yr, predicted ≥90% ≤ 10 yr). P2 falsified as stated (residual ≫ 1.5
   bits/body) and reported; the surviving refined claim (growth ~0; derivable only by an exact
   secular map, not smoothing) is what the data shows. P3 falsified (+9.5%, not ≥3×), reported.
   P4 honestly reported untested. Falsified held-out predictions bar gold by lab precedent
   (1 October red-team).
3. **Attack.**
   - *Instrument:* dt=1/32 vs dt=1/128 on identical bodies — per-body |Δ(deltas)| is 1.3–8×10⁻⁸
     against a scar spread of 2.3–8.5×10⁻⁵ (ratios 160–1050×), flat over 30 yr. The scar is
     physics; entropy contamination is <0.01 bits even at the 2⁻²⁸ grid.
   - *Resonance:* belt at a∈[2.46,2.54] (2:1): H_raw@2⁻²⁰ grows 29.3→33.7 over 100 yr
     (+0.66 bits/decade) while my same-code control belt stays flat (23.0→23.3). The flat-in-t
     claim is regime-bound — the author named this limit but never ran it. Growth is log-like,
     not the linear "unscalable" regime.
   - *Floor robustness:* adding birth mean anomaly to the kNN metric gives 20.81 vs the shipped
     22.60 (H_raw 22.47): no cheap smooth model in birth state captures the wound field; the
     disclosed post-hoc metric choice did not manufacture the result.
   - *Scene size:* N=16384 (pre-registered) vs 8192 (run): H_raw 22.51 vs 22.47, H_knn 22.64 vs
     22.60 at 30 yr — immaterial.
4. **Novelty.** HANDOFF lists H_live as "not measured yet"; no H entry measures a live scar
   field. Distinct from components-98bc (the born floor, 0.126 bits/body) and complementary to
   the queued b-h-live build (which defines H_live from engine state; this probes it on a float
   reference first). The named fix (compiled averaged field) is H0190's machinery — the run
   gives it a new obligation, not a re-derivation.
5. **Goal fit.** Board: "fitting 10⁹ in 8 GB … decided by distinctions created per game-second"
   — this is that measurement, and it kills a premise: birth program + per-body scars is not a
   cache in the secular regime (it stores the derivable at 22–38 bits/body, ~the whole budget).
   PRINCIPLES: "Compute only surprises … Nothing is evolved that can be derived when looked
   at"; "Store the generator, not the generated." Floats explore; no canonical outcome is
   decided, correctly disclosed.

## The one experiment for gold

Close the constructive half: run the belt through the compiled secular generator (H0190's
orbit-averaged kick machinery, or a Laplace–Lagrange re-derivation at the birth state) and
measure the residual scar entropy at the same grids — gold when the residual collapses toward
the born-floor class in the quiet belt AND the 2:1 strip quantifies where the compiled field's
own H_live is nonzero. That turns "the fix is asserted" into a measured both-sides, adoptable
into b-belt-wire in one step.

## What the author missed

- **The scar omits the phase column.** The shipped tube also carries periapsis time/phase;
  secular Δa winds phase ∝ t, so that column's entropy grows ~log t at fixed grid (+6–7 bits
  per 100× time). Reinforces "not a cache", but "flat from 1 to 100 yr" is optimistic at the
  finest grids.
- **The resonance strip was one cheap run away** (my B: +0.66 bits/decade at 2:1) — listed
  under "what would make it wrong" but never measured.
- **Verification numbers not regenerable:** "round-trip 2×10⁻¹⁵, energy drift 1.4×10⁻¹¹" appear
  in no shipped artifact; at the scene's e the drift figure is unverified, and my harsher
  round-trip (e≤0.2, dt=1/32) gives 7×10⁻⁷ (fixed 5-iteration Newton; breaks outright at
  dt=0.5). Immaterial to the result (see 3a), but the dossier quotes numbers the shipped code
  cannot produce.
- **"Seeds, scenes and grids unchanged since" is inaccurate:** predictions pre-registered
  N=16,384; the run used 8,192. Measured immaterial (3d), but it is an undisclosed scene change
  contradicting the dossier text.
- **Ledger top end:** 38.5 bits/body is 4.8 GB at 10⁹, not the headline's 4.3 (which pairs the
  2⁻²⁴ cost with the 2⁻²⁸ bit count). One seed, one forcing (disclosed).
