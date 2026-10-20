# Dossier — 20261020-1326-inversion-3b88 (inversion lens)

## Claim

B13's step-9 `inf` — the one anomaly the cadence gold (20261020-0036-scout-7076) left
"unattributed" — is not a cadence effect at all: it is the plane's **i64 tick wall on
near-escape orbits**. One assist leaves the ship barely bound to the star; the fitted
cycle's period (3.195e19 doll-s = 3.195e19 ticks at clock_exp 0) exceeds `i64::MAX`
(9.22e18), `next_periapsis`'s tick conversion overflows (`step.rs:275` →
`Refused("periapsis")`), the kick is dropped, and once past its periapsis a boundary
that cannot plan ends the body (`step.rs:845-849`): the ship is lost. The same flyby
passes at 256 and 1024/orbit only because its kick-grid phase fits an expressible
period on the same swing. The full-draw scan closes the inversion: the wall is not
step-9-specific — at 256/orbit the stream loses a different ship (draw 104, same
fault) whose death falls outside the gate's first-64 window, so B13 reads PASS where
at 512/orbit the victim (draw 27) falls inside it and B13 reads FAIL. The verdict
flip between octaves is which wall-hit the gate's window samples.

## Bottleneck

Not a compute term; a record correction plus a named deletion target. The cadence
ladder's legality frontier carries a **quantization lottery at the escape boundary**:
orbits with binding energy below |E| ≈ 5.7e-13 doll-units (T = 2π(1/2|E|)^{3/2} >
2^63 ticks, clock_exp 0) cannot have their next periapsis expressed, whatever the
cadence. Measured hazard on B13's stream, per octave: **1/229 at 256, 2/229 at 512,
0/229 at 1024**, all the identical fault. Single-octave B13 verdicts therefore sample
this hazard;
they do not certify absence of the wall. For 10⁹ nothing changes today (the belt is
deeply bound), but any near-escape population (assists, ejections, scattering) hits
the wall at every cadence. The fix is a law-side one-liner class, not a cadence
choice: a near-escape cycle's next periapsis is beyond any representable tick — the
plan should read that as "no periapsis within the horizon" (saturate / `Ok(None)` /
Passage fallback), which deletes the refusal class outright. Expected gain: removes a
`lost`-ship class and de-noises every future cadence verdict; nothing else to delete.

## Evidence

All numbers regenerate from shipped code + `work/patch.diff` (two print-only ignored
tests, `b13_escape_refusal` and `b13_draw_scan`, both in `xtask/src/behave/plane.rs`);
`regen.sh` runs everything below in ≈ 9 minutes.

1. The anomaly, reproduced with the gate itself
   (`cargo run --release -q -p xtask -- behave --law plane --gates B13 --plane-step N`,
   with `PLANE_TRACE=1`):
   - step 8: **PASS 64/64, worst ΔE 5.30e-3** [4.4 s]
   - step 9: **FAIL 63/64, worst ΔE inf ΔL inf** — trace:
     `plane_trace step_log2=9 lost at sample 1 of 1 (kicks=926 handoffs=0 refused=0 lost=1)` [8.7 s]
   - step 10: **PASS 64/64, worst ΔE 3.32e-4** [17.2 s]
   The judge maps a law refusal to `inf` (`assist.rs:125`); the trace says the ship
   was **lost**, not refused at the boundary.
2. The row, identified with the shipped diagnostic
   (`B13_STEP=9 cargo test --release -p xtask b13_by_draw -- --ignored --nocapture`):
   `draw 27: q 4.06 R_p, v_inf 16.1 km/s: dE err inf; alive false, kicks 926 refused 0
   lost 1, closest in the reference 2.08 R_p; fault Some((Kick(0), Refused("periapsis")))`
   — and no failing draw at steps 8 or 10.
3. The mechanism (`cargo test --release -p xtask b13_escape_refusal -- --ignored
   --nocapture`, added by this run's patch; draw 27 at steps 8,9,10):
   - step 9, fault #0 at tick 910984136830 **in doll 0 (the star's doll)**:
     `Kick(0) Refused("periapsis"); state r 5.280e8 v 6.155e-5 doll-units; binding
     cycle: period 3.195e19 doll-s = 3.195e19 ticks at clock_exp 0` — past
     `i64::MAX` = 9.223e18, so `i64::try_from` at `step.rs:275` is the refuser.
   - min kick E about the doll centre, the three octaves: **−1.171e-9 / −1.172e-9 /
     −1.172e-9** doll-units — the swing past escape is physically the same; the
     octaves differ only in where their grid samples the E→0 crossing.
   - end states: step 8 alive, dE err 4.49e-3; step 9 dead; step 10 alive, dE err
     2.00e-4 (both unremarkable against their octave's worst rows).
4. The prevalence (`B13_STEP=N cargo test --release -p xtask b13_draw_scan -- --ignored
   --nocapture`, added by this run's patch; all 256 draws of the stream, failures
   printed only):
   - step 9: **2/229 flown draws lost**, both `Some((Kick(0), Refused("periapsis")))`
     — draw 27 (closest 2.08 R_p) and draw 104 (q 5.83 R_p, v∞ 17.7 km/s, closest
     **5.70 R_p** — nowhere near a graze); 27 inside-planet draws skipped as
     out-of-domain. [100 s]
   - steps 8 and 10 (observed, `scan-8.txt`/`scan-10.txt`): **step 8 loses 1/229 —
     draw 104, the identical fault** (kicks 358); **step 10 loses 0/229**. The wall
     is therefore NOT step-9-specific: at step 8 its victim (draw 104) falls outside
     the gate's first-64 window, so B13 reads PASS 64/64; at step 9 a victim (draw
     27) falls inside it, so B13 reads FAIL. The verdict flip between octaves is
     which wall-hit the gate's window samples, nothing about cadence. [85 s]
5. Code anchors (shipped, unmodified): `crates/universe/src/step.rs:257-276`
   (`next_periapsis`; the `i64::try_from(...)` → `Error::Refused("periapsis")`),
   `:845-849` (a refusal keeps the old binding; a boundary that cannot plan its next
   step ends the body), `xtask/src/behave/assist.rs:125` (refusal → `inf`).

## Predictions

`predictions.md` was written before the instrumented runs. P1 (exactly one seed dies
at step 9, the same seed passes at 8 and 10) **held** — draw 27, and the per-draw
census shows no other failing row. P4 (the same seed's errors unremarkable at the
brackets) **held** (4.49e-3 / 2.00e-4 vs octave worsts 5.30e-3 / 3.32e-4). P2 (death
during the flyby, near the planet) **refuted**: the death is after the flyby, in the
star's doll, r 5.28e8 doll-units from the star — the assist leaves the ship barely
bound to the *star*. P3 (grazer-tail geometry) **refuted**: reference closest 2.08 R_p
is mid-distribution (sampler floor 1.2 R_p), and the second casualty is at 5.70 R_p.
The pre-registered kill criterion (the row is not a death) did not trigger. The
prevalence scan (1-2/229 per octave) was not predicted — it was prompted by P3's
failure.

## What would make it wrong

The period 3.195e19 is read from the *standing* binding at fault time (the refused
refit is discarded and unreadable); if the checker shows the refusal is raised on a
candidate orbit whose period differs materially, the wall-crossing orbit's identity
shifts — the wall itself (`step.rs:275`, `i64::MAX` ticks) and the octave-independence
of the swing stand regardless. The 0/229 brackets are one stream at two octaves: they
show the lottery can miss, not that other streams cannot hit at 8 or 10. Adoption
cost: the fix is a law change (a digest move; B-gates re-flown) — but it is one
boundary condition in `next_periapsis`, and it deletes a `lost`-ship class instead of
tuning cadence around it. Fit with PRINCIPLES: #19, "a fix signals the wrong
representation … the right representation always just feels right" — the plan asks
for a tick that cannot exist; the right answer is "beyond the horizon", and the
representation already has that word (`Ok(None)`). #13, "errors never compound": a
wall-hit ends a body outright — no compounding, but a population near escape is
unflyable at any cadence, which is the "orbits with no tube" risk in HANDOFF, now
with a measured mechanism. #2: the gate's `inf` is an outcome class, not an error
magnitude; reading it as accuracy would have mis-priced the octave.

## The lens

Inversion asked what the newest gold silently assumed (monotone legality in
cadence). What it may have missed: whether B12/B17's classes brush the same wall at
their octaves (not flown here); whether the plane's real populations (the belt at
split8, the fleet) ever enter the |E| < 6e-13 band (the belt is deeply bound —
unlikely, but unmeasured); and the wall's clock_exp dependence (a doll with
clock_exp < 0 moves the wall proportionally — deeper dolls may hit it at larger |E|).
Each is one scan away with the tests this run leaves in the patch.
