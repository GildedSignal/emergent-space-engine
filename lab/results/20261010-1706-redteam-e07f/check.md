Grade: silver

**Abstract.** Claim: r1's frozen Binet cells make stability a property of the band, not the
body: the ISCO is a cliff with a wrongly-stable strip inside 6M ([5.9073, 6.0) at m=16
centre, −1.54%; +2.81% inner-edge); a near-circular ship at r = 5.95M parks forever at zero
crossings where exact GR plunges in 8.8 orbits; refinement never cures it (dyadic-phase
lottery at every m); r1's frozen `isco` gate is blind. Reproduced bit-identically;
independent probes confirm strip, park (step-converged, sticky to ε ≤ 1e-2), staircase
(31.5% / 181.8%) and blindness. Not gold: the shipped law (`space-darwin16-v1`, law.md,
30 September) already replaced the in-band map with a Darwin (E,L) cycle, and no r1 re-run
is queued. Adoption: mirror B19's ISCO clause into r1.

## Reasons

1. **Reproduction.** `python3 binet_isco.py` (3.35 s) and `python3 addendum.py` (8.81 s):
   outputs diff-identical to the stored `.out` files; timings match the dossier (3.5/8.9 s).
   `work/patch.diff` is empty, so the tree is untouched. Every headline number in the dossier
   traces to a stored output line.
2. **The premise is the frozen text, verbatim.** r1 line 9: u_k at the band's geometric
   centre, rings 2^(k/m); line 10: in-band u″ + (1−6u_k)u = 1/L² − 3u_k², "a rotation when
   1−6u_k > 0" — the rung itself decides stability per band. Un-frozen (u_k → u) it is
   exactly the author's oracle u″ + u = 1/h² + 3Mu². The sampler (line 21, p ≥ 6.5+2e) and
   the ISCO probes (line 25, r = 7 and r = 5.5) match the dossier's blindness argument, and
   representation.md §1 ("the innermost stable orbit (where 1−6M·u_k < 0) … and plunges all
   emerge") is the design text the finding kills.
3. **Pre-registration.** File times: predictions.md 17:15:30 < binet_isco.py 17:15:57 <
   binet_isco.out 17:16:05 < addendum 17:17. predictions.md keeps its hand-derived band
   [5.9067, 6.1669) against the measured [5.9073, 6.1688) — an uncorrected slip, good
   evidence it was written before the run. Six of eight predictions held in substance; the
   two misses (mirror mechanism, m=32 strip side) are reported as held-out failures in the
   dossier. Honest.
4. **My adversarial cases (all confirm the finding).**
   - Strip arithmetic re-derived from scratch: band 41 = [5.9073, 6.1688), centre 6.0367,
     1−6u_k = +0.0061 > 0 → the whole band, including [5.9073, 6.0), is "stable". The shelf
     equilibrium r_eq = 6.054 sits inside the band: a genuine attractor of the band dynamics.
   - Plunge robustness: exact plunge at φ = 55.2 unchanged for dφ ∈ {1e-3, 5e-4, 2.5e-4};
     eps sweep 1e-3/1e-4/1e-5 gives 8.8/12.8/16.8 orbits — clean hyperbolic scaling, not an
     integrator artifact.
   - Shelf stickiness: at ε = 1e-3 the band orbit parks to φ = 2000 with 0 crossings (m16);
     at ε = 1e-2 still bound (30 crossings); it breaks only at ε ≥ 3e-2. The parked-fleet
     claim holds in its stated near-circular scope.
   - m=8 mirror: r = 6.05 under m8 centre is wrongly unstable ([5.6569, 6.1688), centre
     5.9073): apoapsis pumped +4.6% (6.331) vs exact [6.044, 6.056], no plunge. One side or
     the other at every m, as claimed.
   - Photon capture (the dossier's unmeasured item): my integrator nails exact b_crit =
     5.19615 = 3√3; band m16 gives 5.19535 (−0.015%), m32 −0.004%. r1's ±3% light cases do
     not flip — the dossier's "less sensitive" guess is measured true.
5. **Novelty.** No HISTORY entry or doc records the strip, the phantom shelf or the ω_r
   cliff; H0205 recorded r1's ISCO criterion as passing without noticing; git log is clean.
   The m-sweep dyadic-phase argument (per-band refinement provably cannot remove the strip)
   is new.
6. **Why silver, not gold.** The premise it kills is already retired in the shipped law.
   law.md's cycle section (`space-darwin16-v1`, 30 September) replaced the in-band
   area-preserving map with the cycle compiled from (E,L) roots in Darwin phase — stability
   there is per-body, so the phantom shelf is not established for what the player touches,
   and the dossier never cites law.md; its "what would make it wrong" even asserts the
   design's text says band-frozen (true of representation.md §1, false of the operative law
   doc). The r1 clean re-run it aims at (H0205's limitation) is absent from lab/queue.txt
   and from HANDOFF's plan; the current frozen gates already embody the proposed check (B19:
   "no stable bound cycle inside the ISCO of its sense") and plunge tubes (`b-plunge-tubes`)
   are the live plunge work on the current law. Real, correct, cheap to adopt — but with no
   scheduled trigger and no demonstrated defect in the shipped law, it is one experiment
   short of gold.
7. **Minor errors (none touch the headline).** The dossier says the ISCO probes are "±10%";
   r1 line 25 says 1%. Attack 4's ∂ω_r/∂r values (0.45 at 6.05, 0.066 at 8) do not
   reproduce: 3/(r²√(1−6/r)) gives 0.90 and 0.094 (the divergence-at-the-rim claim stands).
   The mirror prose is loose twice: the hyperbolic fixed point (r ≈ 5.956) lies inside the
   band, not below it, and the run's own output has periapsis 6.044 inside the wrongly
   unstable strip, so "periapses forbidden in the strip" overstates.

## The one experiment that would make it gold

Run the falsifier on the shipped representation, not the frozen one: the (E,L)-rooted
Darwin-compiled cycle of law.md (`space-darwin16-v1`), via the plane's own law path
(`behave`) or a float64 port of its spec — near-circular sweep across the band containing
6M ± 1 band (plunge iff r < 6 against the oracle) and the ω_r staircase bound. If a shelf or
cliff survives there (integer (E,L) quantization, ψ-cut band edges), this is a live-engine
defect and the finding is urgent gold. If not, the finding stands as the reason band-frozen
cells stay dead, plus a two-case r1 gate fix.

## What the author missed

- **law.md replaced the in-band map on 30 September.** The strip is a property of r1's
  frozen configuration family and representation.md's premise, not of es-space-v2 as shipped.
  The lens's own float64 caveat (integer/Minsky law) points at the wrong gap; the
  representation, not the arithmetic, moved.
- **The lab's plan has moved past r1**: no r1 re-run in lab/queue.txt or HANDOFF; B19
  already freezes an ISCO outcome-class clause (Kerr); b-plunge-tubes is the live plunge
  item. The finding's urgency should have been argued against that board, and was not.
- **The outward-perturbation nuance**: exact GR at 5.95 with ε = −1e-3 does not plunge — it
  binds in a zoom-whirl with a razor-thin barrier (r ∈ [5.956, 6.102]). The park-vs-plunge
  wrongness covers the inward class (half the perturbations); a player-facing sentence
  should say so.
- The photon-capture threshold he flagged as unmeasured: −0.015% (m16); his guess was right,
  and I measured it for him.
