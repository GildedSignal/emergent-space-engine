# Dossier — 20261019-1656-second-20261019-1551-dynamics-e3b7-9b3b (second author on e3b7)

## Claim (one sentence)

The checker's corrected claim now holds on a regenerating record — **Bounce+tide
together fail the cold-belt gate, the kicks alone hold it** (Pass belt flat through
H = 49152, cold and thermal, maxk frozen, digest-identical to the checker's
independent flight `b73b06dc…`) — and the new isolated-orbit ladder locates the
pump's entire address: **the rounded tide is bounded (≤ 1% radius drift, 14 orbits)
for every pericenter outside the field's own DK_CAP clamp zone (r_p ≳ 2.1q, e ≤ 0.97
at a = 70q) and ejects any orbit whose pericenter enters it (e ≥ 0.975 ⇔ r_p ≤ 1.75q,
within 14 orbits, by as few as 3 clamped chronons), reproducing the belt grinder's
endpoint speeds (577–708k vs the belt's 686–740k) in a single body.**

## Bottleneck

chaos-shadowing open direction 2 (the gravity-held belt's plateau lifetime), through
the board's smoothness line. The named experiment converts the silver into an
adoptable statement and redirects the fix with a measured boundary: not cadence, not
the outer per-component rounding — only the inner clamp zone below r ≈ 2q (≈ 2 body
radii) injects energy. The missing gate gets its constant: **a cold gravity-held belt
must keep every body's pericenter above the clamp radius for ≥ 5× the belt's
dynamical time** (equivalently e < 1 − 2q/a_max… any body's e < 1 − 2q/a); e3b7's
scene fails it only because Bounce contacts walk bodies' e across 0.97.

## Evidence

Everything regenerates: `regen.sh` (~9 min; one flight > 60 s: G_s1 at 159 s).
`work/analysis2.json` holds every number below; `digest_expect_ok` all true.

**Digests (this tree, shipped `Chronon` + `Law::RelativisticV1`, patch adds only
`--pass`/`--every` and the orbit example; default path unchanged):**
- Original ladder, bit-for-bit: G_s1 `e3462444…`, C_s1 `634d9918…`, GW_s1 `79b89629…`
  (walls 14896), G_s2 `420ef2ff…`, C_s2 `e903ff6d…`, C0 `e8a69ff7…`.
- **A1 = the checker's independent Pass flight, bit-for-bit: `b73b06dc…`** (my `--pass`
  knob is exactly their knob; contacts 3 072 187 recorded, velocities untouched).
- **A4 = the checker's cadence flight, bit-for-bit: `e98306bb…`** — their undocumented
  variant recovered: kick every 4th chronon (t%4==0) with MU pre-scaled by 4 before
  rounding, cap ×4. Onset 12236 — their exact number. (Three natural variants
  discarded first: post-clamp ×4 `f53fe500…` onset 13104; phase (t−1)%4 `89cd6c20…`;
  pre-round with unscaled cap `ed4d26e9…` — all show the same onset invariance, so
  the cadence conclusion is variant-robust even where the digest is not.)

**1. The named experiment (Pass controls; the tide alone holds the belt).**
- A1, C0 scene (thermal 0), H = 32768: maxk 91993 → 92196 (+0.22%), **frozen since
  t = 19362**; esc 0; rms constant 77.7q; ke +0.02%.
- A2, same scene, H = 49152 (1.5× the checker's horizon, 3× the Bounce onset):
  identical frozen state (92196 since t = 19362; esc 0; ke +0.00%). P2's kill branch
  did not fire.
- A3, the thermal cold control itself (±q/256) under Pass, H = 49152: esc 0, ke
  −0.05%, rms 77.7 → 79.3q, maxk 95298 → 104180 — drift +9.3% but **frozen since
  t = 5306** (zero growth over the last 43 846 ch; the drift is the initial
  pericenter-sampling transient, not a walk). Its Bounce twin: 449/800 evicted,
  72 918 812 contacts, maxk 686 460 (n_in 309).
- Corrected fleet-season numbers, recomputed from this run's own TSVs and equal to
  the checker's: season peak 64-ch window (t ≤ 8192) 102 874 at t = 7808 = **173.8×
  the cold control's same-time window (592)**; the dossier's "2276×" global max
  183 685 is the late grinder's (t = 47 744) where the cold control's same-time
  window is 184 250 (ratio 1.0); shell (140–250q) 77 bodies at t = 4096, 21 at 8192;
  esc_max/esc_last 1379/1371 (s1), 1374/1373 (s2); esc50 t = 2211; discriminator
  corrected: cumulative contacts 1352 and maxk 379 827 at t = 12 288 (the 727k with
  21 862 contacts is the t = 16 384 endpoint); C0 rms 77.7 → 91.8q, first esc 13 022.

**2. The eccentricity ladder (new; single body, same shipped field, H = 98 304 =
14 orbits at a = 70q; verdicts read integer rmax columns only — the orbit example's
digest is constant, no events, and is cited for nothing).**

| a=70q e → | 0 | 0.01 | 0.06 | 0.2 | 0.5 | 0.8 | 0.97 | 0.975 | 0.98 | 0.985 | 0.99 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| r_p (q) | 70 | 69.3 | 65.8 | 56 | 35 | 14 | 2.1 | 1.75 | 1.4 | 1.05 | 0.7 |
| rmax drift | 0.1% | 0.35% | 0.18% | 0.48% | 0.9% | 0.15% | 0.0% | **ejected** | **ejected** | **ejected** | **ejected** |
| first esc t | — | — | — | — | — | — | — | 7045 | 5128 | 22559 | 8225 |
| clamped ch | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **3** | 6 | 24 | 118 |
| maxk | 65674 | 65813 | 70100 | 80422 | 113411 | 196758 | 526815 | 577391 | 634726 | 708350 | 612611 |

- Achieved e equals target to 3 digits everywhere (e.g. 0.5 → 0.503, 0.8 → 0.800);
  bounded arms stay Keplerian (maxk = v_p = v_circ·√((1+e)/(1−e)) to 0.1%).
- a = 36q: circular bounded (27 orbits, drift 0.38%); **e = 0.5 bounded (r_p = 18q,
  the grinder remnant's own scale, drift 0.0%)** — the remnant zone is not
  intrinsically unstable; its destruction is contact-driven. a = 70q + 1 quantum
  tangential: bounded (drift 0.01%), folding the checker's isolated flights in.
- The held/destroyed boundary sits at r_p ∈ (1.75, 2.1]q — exactly the DK_CAP zone's
  outer edge (|dk_raw| > q/16 first at r ≈ 1.5q diagonal to 2.09q aligned). ejection
  endpoint speeds 577–708k bracket the belt grinder's 686–740k ≈ v_esc(1q): **the
  grinder is the clamp-zone slingshot, reproduced with one body and no contacts.**
- Boundary arms 0.975/0.98/0.985 were flown after predictions.md (bracketing
  refinement of P5 branch (ii), disclosed; the pre-registered arms were
  0/0.01/0.06/0.2/0.5/0.8/0.97/0.99).

## Predictions

`predictions.md` written before any decisive flight. P1 held (digest `b73b06dc…`
bit-for-bit; flat). P2 held (flat to 49 152, frozen tail). P3 held (thermal Pass
flat, frozen since t = 5306 — the +9.3% transient is reported, not smoothed away).
P4 held (variant recovered, digest `e98306bb…`, onset 12236). P5 resolved to
branches (i)+(ii) as predicted: no pump at contact-seeded e (0.06 drift 0.18%), pump
only at the clamp zone (e ≥ 0.975); branch (iii) refuted — "the kicks alone hold it"
is TRUE at every contact-relevant eccentricity, and the checker's redirect
("pericenter pump on contact-eccentricized orbits") is refuted in its letter and
confirmed in its address: the pericenter that matters is the one inside r ≈ 2q,
which contacts must walk e past 0.97 to reach.

## What would make it wrong

- The boundary is measured at a = 70q (a = 36q only at e ∈ {0, 0.5}); a tide with
  symmetric/rotational rounding, a different DK_CAP policy, or a per-cell tide (the
  engine's frame) moves or deletes the clamp zone — the method (integer rmax-drift
  ladder) survives, the constant does not.
- 14 orbits bound the drift at ≤ 1%, not exactly; a slower pump below that is
  invisible here (the belt's own onset needed ~2 orbits).
- The contact e-walk inside the many-body belt (e: 0.06 → 0.97) is inferred from the
  endpoint speeds and the Pass/Bounce contrast, not isolated directly; a run that
  tracks per-body e-histograms through the belt's self-destruction would close it.
- Not tested: self-gravity, J2/multipoles, 3D, horizons > 98 304 ch.

## Cost of adopting / fit with PRINCIPLES

No crate change; the harness and both examples stay in this run's patch. The gate
any belt wiring must pass is now a number: **pericenter stays above the clamp radius
(r ≈ 2q ≈ 2 body radii) for ≥ 5× the belt's dynamical time** — checkable per body as
e < 1 − 2q/a from the same integer columns this ladder used. The fix list narrows to
two: `Response::Pass` for gravitating-only belt bodies (flat to 49 152 ch, this run)
or an exact inner zone; cadence and the outer rounding are dead ends with digests.
Julien, P19: "a fix signals the wrong representation" — the clamp is now the
measured address of the wrong representation, not a guess. P2 ("error type over
error size"): the boundary is a type boundary (held/ejected), read off integers.

## The lens

The second-author lens risked trusting the checker's flights without regenerating
them; both digests were reproduced bit-for-bit instead, which is what turned their
cadence arm from "conclusion" into record. What this lens may have missed: the
belt-interior e-walk is inferred, not measured; the ladder is 2D central-field only;
and the A3 "+9.3%" needed the frozen-tail reading to stay honest — a lens that
averages would have called it flat or drifting, both wrong.
