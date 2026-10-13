# Dossier — the news scar: gravity-is-news under a thrusting source

Run 20261013-0236-redteam-7ab4 (premise red-team lens; target `docs/representation.md`,
§1 "a change travels at most one cell per cell-update" and law.md:33 "gravity is news").
Probe: `news_scar.py` (pure float64 Python, no deps), decisive log `run2.txt`, all numbers
`scar.json`. Cloud Linux/x86 shared (8 vCPU): orders of magnitude only. Whole battery 3.4 s.

## Claim

The news representation's *rebind* half is right and now has an error model — every rebind
of a source leaves each consumer a permanent, one-sided orbital scar of
**|ΔE| ≈ 0.7·(β_c²/2)·|δv|** (β_c = consumer's orbital speed about the source; fitted
exponent **1.963** over β_c 0.003–0.3) — invisible at solar-system β_c (5.5×10⁻¹⁰) and
percent-level exactly in the strong-field regime the game sells; but its *thrust* half is
wrong as specified: under a sustained burn the free-fall tube readout lags the design's own
1PN oracle family by a **cadence-invariant ½·a·T²** (T = light time source→consumer), so the
consumer permanently absorbs **β_c²/2 of the source's total burn Δv** (measured: a 2P burn
at β_c = 0.3 leaves ΔE = 2.2×10⁻², 200× B12's 10⁻⁴ budget), and no gate, rung or oracle in
the lab can see any of this — the fix is one payload change: **versions must carry the
source's acceleration** (quadratic tubes), not rekey faster.

## Bottleneck

Board item 0 (the representation) → law.md:33, the causality primitive under everything
("gravity must travel at c … we can't get lazy here and construct latter upon a flawed
foundation"). The record has measured news only for freely falling sources (a237: binaries,
flybys, 10⁻⁷ agreement; e300: gates byte-identical *because* their scenes never rebind
inside a light window) and the switch *onset* (a237 S4). Nobody had measured what a rebind
or a burn *leaves* in the consumer. Gain: an error model for the causal half of the law
(where it is safe: β_c < 0.05; where it needs the acceleration term: any thrusting source),
and a freeze-ready criterion where r5/r6 were never frozen. Deletes nothing; fixes a
representation payload before it freezes.

## Evidence (each command ≤ 60 s; reproduction: `bash regen.sh`)

Scene: test moon on a circular orbit (r = 1, v = 1, G = M = 1, P = 2π) about a source; at
t_k the source's motion changes (impulse |δv| = 0.01, or sustained burn a = 0.05 for
D = 2P). Units scaled so β_c = v/c is the only knob (c = 1/β_c, light window T = β_c).
Three readouts: **inst** (source's true state at t — today's plane and the 1PN near-zone
oracle's instantaneous gauge), **news** (law.md:33: newest tube version whose emission the
consumer's past light cone has met, that free-fall tube evaluated at now; switch located by
bisection to 10⁻⁵·T), **ret** (retarded position — Laplace control). Velocity-Verlet,
dtA = T/60 (window) and P/600 (tail); twins, controls on both sides.

**E1 — the impulsive rebind scar (P1, P2 held).** Permanent scar = |ΔE| of the moon about
the (post-kick, inertial) source, measured 2P after the cone, mean over 4 kick
geometries:

| β_c | mean scar/&#124;δv&#124; | pred β²/2 | at-switch Δv/&#124;δv&#124; | ret/&#124;δv&#124; (control) |
|---|---|---|---|---|
| 0.003 | 3.74e-6 | 4.5e-6 | 6.5e-6 | 5.5e-2 … 1.1e-1 |
| 0.010 | 3.61e-5 | 5.0e-5 | 6.3e-5 | 1.1e-2 … 3.6e-1 |
| 0.030 | 3.19e-4 | 4.5e-4 | 5.6e-4 | 2.3e-2 … 1.1e+0 |
| 0.100 | 3.49e-3 | 5.0e-3 | 6.5e-3 | 6.6e-2 … 3.7e+0 |
| 0.200 | 1.38e-2 | 2.0e-2 | 2.7e-2 | 5.1e-1 … 7.3e+0 |
| 0.300 | 3.16e-2 | 4.5e-2 | 6.4e-2 | 1.3e+0 … 1.1e+1 |

Fitted exponent vs β_c: **1.963**; k̄ = 0.70 (geometric tidal projection, spread 0.086–1.2
over kick geometries). The scar at the cone arrival equals the final scar (at-switch ≈ ΔE
within ~1.5×): all of it is accrued *inside* the light window, nothing after — one-sided in
time, permanent. `twin_no_kick` = 0.0 exactly (positive control: news ≡ inst with no
rebind, the mechanism identity e300 could only verify diagnostically). Switch lands
+1.2×10⁻⁷…1.3×10⁻⁵ late (bisection residue), never early.

**E2 — the sustained burn (P4 held; the kill).** Source burns a = 0.05 for 2P; news rekeys
its free-fall tube every epoch = T/8 and T/32. The readout's position error at version-age
≈ T (steady state, 11–20 samples each):

| β_c | epoch T/8 | epoch T/32 | pred ½aT² |
|---|---|---|---|
| 0.05 | 0.0001 | 0.0001 | 0.0001 |
| 0.10 | 0.0002 | 0.0003 | 0.0003 |
| 0.30 | 0.0022 | 0.0023 | 0.0022 |

Cadence-invariance confirmed (4× finer rekeying buys nothing): the lag is the light time,
not the rekey rate — **the version ring cannot represent an accelerating source**; its
payload is (position, velocity) and the design's own oracle family (1PN near-zone,
instantaneous gauge — B13's reference, B16's boosted quadrature) carries the acceleration.
Consumer damage: permanent ΔE = 1.2×10⁻⁴ (β 0.05) → 2.2×10⁻² (β 0.30), matching the summed
per-rebind law **β_c²/2 · a·D** = 0.028 predicted, 0.022 measured. The moon's end velocity
differs by O(1) — its whole orbit is another orbit.

**E3 — magnitudes at real scales (from the fit).** Per rebind, scar/&#124;δv&#124; = β_c²/2:
a Jupiter moon (β_c 3.3×10⁻⁵): 5.5×10⁻¹⁰; Mercury about the Sun: 1.3×10⁻⁸ — invisible,
which is *why* e300's gates printed byte-identical. A consumer at r = 20M about a compact
mass (β_c ≈ 0.17): **1.4×10⁻² of every rebind** of its doll origin — and the origin falls
by one uniform vector per kick epoch (law.md:37), so strong-field consumers take percent-level
steps at kick cadence. Strong-field binary: the news-lag term (β²/2·a_pert on the origin)
exceeds the consumer's *direct* tidal signal from the perturber (r_c/d ≪ β²/2 at 20M in a
100M binary) — the lag is the dominant perturbation channel there, and it is one-sided.

**E4 — P3 control.** ret (Laplace) is worse than news by 3–4 orders everywhere (E1 column);
it also disagrees with inst *after* the cone (no extrapolation), as a237 found. Both sides
of the instrument behave.

**E5 — P5.** dtA halved (T/60 → T/120): scar changes 0.000 relative — representation
error, not integrator error.

Harness honesty: two earlier builds were wrong (a division-by-zero in the cone bisection;
the source's true worldline never moved after the impulse — that run's "scar" was the
source drift itself). `run1.txt` (broken β-sweep of the second build) and `run2.txt`
(decisive) are both kept. Post-fix, the controls pin the harness: twins exact, ret fails
big, news switches only late-never-early.

## The ranked attacks (the lens's deliverable)

Ranked by what the player is most likely to see, not by exoticism:

1. **Gravity-is-news under thrust (this run).** The premise sentence "a change of the
   source's motion (thrust, contact, rebinding) reaches the body only when its light cone
   does" is true, but the *readout between switches* extrapolates free fall, and under
   sustained acceleration that is the wrong law at first order: lag ½aT², cadence-invariant
   (E2), consumer damage β²/2·a·D. The player burns every session; strong-field consumers
   are the game's selling point. **Rung that should have caught it: none exists** (r5/r6
   never frozen; no news criterion anywhere; B16 is light-only). Criterion proposed below.
2. **News has no instrument at all.** Every named gate is byte-identical under news (e300
   E1) — not because news is no-op but because no gate scene rebinds inside a light window;
   the plane cannot resolve arrival at stellar scale (kick steps 25–500 ticks vs delays
   4–32, e300 E3) nor express mutual β above the star's escape speed (e300 E3). The law
   adopted a causality primitive with no oracle, no rung and no gate; my float probe is the
   first instrument for its error model. **Rung: none.**
3. **Dense ≡ sparse bit-identity (premise 4) is unmeasured.** law.md:50 "both orders give
   identical bits"; B8 lists it; no graded run in the lab record exercises the two orders
   on one scene (lattice-event vs lattice-metal); r5 unfrozen. Risk: silent divergence at
   the regime seam. **Rung: r5, unfrozen — freeze it before the dense order is wired.**
4. **The design doc carries dead mechanisms as live ones (premise 2).** representation.md:32
   still presents Minsky's two-addition map as "the primary in-cell solution"; the shipped
   law replaced the in-band area-preserving map on 30 September (law.md:20: first-order
   slope error in every cell holding a turning point). Same class as line 67's retired jet
   (already recorded in kick-jet's contradictions). The doc — my lens's target — is the
   thing a new builder reads first. **Rung: r1 caught the physics; the doc never absorbed
   the kill.**
5. **"Undisturbed orbits ≈ 0 cost" (premise 6) is false on shipped code.** Measured: O(N)
   per frame with zero events, the rekey/rebind bookkeeping and the view's O(all-bodies)
   gather (56–74% of frame) — the frame-cost topic's 37 runs; wt/frame in flight. The
   premise is true of the law, not yet of the engine. **Rung: B9/B15 exist, frozen,
   unfaced.**
6. **Two-body doll (premise 1): survives.** Its first 2PN measurement holds (+0.36% worst
   periastron at ν = 0.25, ecfd); the open wound is B11's oracle (certifies nothing
   GR-shaped, same defect family as B12/B13/B17). **Rung: B11 — its oracle must be fixed
   to 2PN before it can catch anything.**
7. **The view at the past light cone (premise 5): wrong three ways, fix converged**
   (delay(b) memo, (b, sense|Q) key, k=0 pair; view page, 22 runs) — in flight, not
   re-attacked here. **Rung: r6, unfrozen; B3/B16 judge deflection only.**
8. **Kicks via cycle derivatives (premise 3): dead by six golds**, retired in law.md:36
   (representation.md:67 still says multiply-add — see attack 4). Confirmed dead; no rerun.

**Proposed criterion (freeze-ready, for the rung that does not exist — `r-news`):**
(a) *arrival*: burn/no-burn twins bit-identical until the cone; the switch at the first
tick the cone passed, never early (controls: ret must fail it, inst must fail it); (b)
*scar*: per rebind, consumer's |Δa|/a ≤ 2·β_c²·|δv|/v_c (k̄ 0.70 + margin), bounded
random-walk under alternating kicks, zero under no-rebind; (c) *burn*: under sustained
source thrust, free-fall-version readout lag = ½aT² (must fail at β_c ≥ 0.1); with
acceleration-carrying versions, lag ≤ 10⁻²·aT² (must pass). Types and behaviours, no
trajectory identity (r2's lesson).

## Predictions

Written before the decisive run (`predictions.md`). **Held:** P1 (exponent 2.0 ± 0.1 —
measured 1.963; one-sided in time: at-switch = final), P2 (magnitudes within factor 0.7 —
measured k̄ 0.70; invisible at moon β, percent at β 0.3), P3 (ret worse by 3–4 orders),
P4 (plateau ½aT², cadence-invariant, damage = β²/2·a·D), P5 (dt-invariant, 0.000 rel),
P6 (the premise survives the impulse; the wound is the thrust half and the missing
instrument). **Missed/refined:** P1's "one-signed across seeds" was ill-posed — the tidal
projection factor k varies 0.086–1.2 with kick geometry (I varied phase and kick direction
together); what is one-sided is the *time* structure (all damage inside the window), which
is the claim that matters.

## What would make it wrong

The ½aT² kill rests on the 1PN near-zone oracle family the lab itself uses (instantaneous
gauge); a fully causal 2PN retarded-oracle computation could move the required payload
(jerk, not acceleration) — my probe is 0PN Newtonian forces over exact causal bookkeeping,
not a GR integration. β_c > 0.4, eccentric consumers, inclined kicks and the integer law
are untested; k̄'s spread means single-geometry rows can sit 10× below the mean. The
scar's *direction* (news right, inst acausal) is an interpretation: the measured fact is
the difference and its law.

Cost of adoption: one more vector per tube version (the source's acceleration at emission;
+8–16 B on a ring that is 20 B–2 kB per source today), quadratic readout (≈2 extra
multiply-adds per news evaluation), and the `r-news` rung. Nothing else moves: for
impulsive rebinds the representation is already right, and at solar-system β_c the whole
effect is 10 orders below the floor.

## PRINCIPLES fit

- #13 "basically we don't want errors that can compound": the scar is one-sided and
  permanent; under correlated kicks (the near-plunge band's one-signed drift, d617) it
  accumulates linearly — the exact error type this principle bans, now with a law and a
  bound.
- #19 "a fix signals the wrong representation": rekeying 4× faster bought 0.0022 → 0.0023;
  the fix is the payload (acceleration on the version), not the cadence.
- #23 "Nothing past c": news is the principle made mechanical; this run gives its error
  model and the first instrument that can fail it.
- #10 "the simplest falsifying test first": 3.4 s of float, controls on both sides.

## The lens

A premise red-team overweighting exotic cases would have led with the dense/sparse seam or
2PN; I ranked by player visibility (burns are the player's only lever; strong-field
consumers are the pitch). What the lens may have missed: I did not touch the integer law,
the plane's actual wiring (e300's cursor), or GR beyond the near-zone gauge argument; the
adjacent hole this run names but does not measure — a fleet doll whose origin *thrusts*
(the dense order's Fermi frame is defined along a geodesic, representation.md:23; a
burning fleet centre is not on one) — may be the bigger representation break, and belongs
to whoever builds b-fermi-phase2.
