# Dossier — 20261021-0429-second-20261021-0312-system-15d7-e415 (second author on 20261021-0312-system-15d7)

## Claim

The checker's named gold experiment is flown: the belt's BOUNDARY comb is **deleted for real**
under a per-kick gate — bound arc (`k = 1/(1+e) > 1/2`), apoapsis `periapsis/(2k−1) < 2^leave_log2`,
read off the binding the kick leaves — with the kick writing the anchor's boundary value bit for bit;
on the completed 500,000-gs (~18-era) belt flight at 3×10⁴ this removes **all 510,004 of 510,004
clock combs** while the **tubes digest is IDENTICAL** (every per-body field the shipped digest hashes
except the bookkeeping the deletion changes by design), with identical kicks/encounters/contacts and
fire traces and one re-frozen digest — and on the adversarial arm (B13's assist draws, the 3b88 wall
class) **64/64 draws are identical with the comb KEPT on 24/24 near-escape exits**. Zero certificates
are lost; the deletion is an adoption-ready law change, not a measurement.

## Bottleneck

Board row **Macro, kicks per body (~10³ at stake)**, nladder od 2. The first run (15d7, silver)
proved the comb never fires and priced the deletion; the checker held gold back on exactly one
experiment: fly it. Flown: the belt's clock bodies now emit ~1 event per half-era instead of 2
(19.9% of this scene's comb+kick stream; for a pure clock stream the comb share is 49.7% → ~1.98×
fewer stream events; a31c's 1.2× wall estimate at 10⁹ stands, ~2.4 h/era of the 12.8+2.4 h
alternation). Nothing else to delete on this row's comb half.

## Evidence

All numbers regenerate: `regen.sh` (≤ 15 min; every command ≤ 420 s) from shipped code +
`work/patch.diff` (counters kept from 15d7, the gated deletion behind `ES_BOUNDARY_CUT`, the
`tubes_digest` identity certificate, the example's seed arm, and the `b13_cut` xtask test).

1. **Instrument neutrality (P1).** Gate off, the flight reproduces 15d7's frozen record **bit for
   bit**: digest `f9af771e9887a6fbc704a60b567aff26`, kicks 1,290,749, encounters 24,264, contacts 0,
   combs 1,267,977 (clock 510,004), fires crash 0 / leave 0 / handoff 18, kick-surface 0
   (`belt-base.txt`; wall 134.6 s under load).
2. **The deletion (P2).** `ES_BOUNDARY_CUT=1`, same flight (`belt-cut.txt`): **tubes digest
   `468b7061…` identical**; kicks 1,290,749, encounters 24,264, contacts 0 identical; combs 757,973
   (**clock 0**: 1,267,977 − 757,973 = 510,004, every clock comb); the 18 releases at the same ticks
   and bodies (`diff` of the fire traces: identical); gate cut 531,287 / keep 0; the full digest
   moves to `3c9236a6…` — the re-freeze (anchor written at the kick, no Boundary plan items, lower
   per-body event counts), the only intended law-visible change.
3. **Held-out seed (P3).** Seed 7 (the first checker's own case), 200k gs: baseline combs 500,639
   (clock 203,311) — the checker's exact numbers — and the deletion gives identical tubes digest,
   clock 0 (500,639 − 297,328 = 203,311), fires 0/0/11 identical (`seed7-*.txt`).
4. **Adversarial, the 3b88 wall class (P4).** `b13_cut` (`b13-cut.txt`): B13's 64 assist draws at
   step 8, each flown gate-off and gate-on: **64/64 identical** (tubes digest, alive, kicks, refused,
   lost, the 1% error class). The exit leg is near-escape (heliocentric E ≥ 0, or apoapsis −1/E ≥
   2^40) on 24 draws — **the comb stayed scheduled on 24/24** (18 of them pure keeps: gate cut 0);
   46 draws cut combs on their bound legs (e.g. draw 1: 550→0) and 49 kept them somewhere; mixed
   draws cut before the assist and keep after it (draw 21: cut 241 / keep 466).
5. **Controls (P5).** The plunge suite passes with the gate off AND on, zero boundary fires both
   times; the universe lib passes 10/10 both ways (`plunge-*.txt`, `tests-off.txt`). One known
   coupling: `motion.rs`'s `a_ships_step_is_the_clocks_step_of_its_state` samples "right after a
   kick" THROUGH the boundary item (motion.rs:388), so under the cut it finds 0 samples and its own
   `looked > 500` assert fires — its physics assertions never ran (all departures 0.0); the adoption
   patch re-points that sampler at the kick item. Wall at this scene: 134.6 vs 135.4 s (load noise
   dominates; the 510,004 deleted boundaries at the page's 5.9–8.6 µs are ~3.0–4.4 s of payload —
   orders of magnitude only, cloud box).

**Why zero certificates are lost (mechanism, exact).** The gate reads the binding the kick leaves:
on a bound arc `r` never exceeds the apoapsis, so the leave check at the deleted boundary tick could
not have fired; the next kick re-evaluates the gate on the new tube (no margin needed — between
kicks the drift conserves the orbit). A periapsis under the surface is the planned `What::Crash`
item's own tick (`plan_terminal` runs after every kick), which is where plunges actually die (P5).
The gate is exact to one ulp of the truncated apoapsis division.

## Predictions

`predictions.md` was written before any decisive run (mtimes: it predates every evidence file).
P1–P5 all held as registered; P4's "keep on near-escape" landed at 24/24, stronger than the
registered "GATE_KEEP > 0 on near-escape draws".

## What would make it wrong

- A population that leaves while its gate held: impossible on the tube (r ≤ apoapsis < edge, exact),
  but a doll-edge semantics change (leave_log2, moving dolls) must re-fly the census.
- The wt/cadence merge moves belt kicks off their phase — the crash arm's belt argument (both apsides
  far above the surface) is unaffected, but the census should be re-flown there (wiki od 2 says so).
- The anchor's ramp readers: 18 eras of coast prove the kick-written anchor keeps `lead` and the
  partial step bit-identical; burns and encounters ride the same `Kick` record, but a view-fidelity
  rung under burn is the honest next look (out of this run's scope).

**Adoption cost:** one law change and one digest re-freeze (as the wiki already prices for the
stagger/TTL arms), plus the motion.rs sampler re-point; the patch is 13 lines in `kick_clock` +
`leave_safe`. Fit with PRINCIPLES: 3 ("Nothing is evolved that can be derived when looked at
(clocks…)"), 14 ("no work for no reason, so no ticks"), 19 (the comb was the clock's artifact, not
the law's — the gate reads the stored generator itself).

**The lens (second author):** I inherited the first run's frame and could have inherited its blind
spots; the tubes digest (not in 15d7) is my guard against a deaf comparison. What this lens may
have missed: the deletion's effect on the *held-scan* schedule is unmeasured (the scan rides the
player's items here, but a belt-local scan design would inherit the missing events), and the
wall-time non-claim is honest only as an order of magnitude.
