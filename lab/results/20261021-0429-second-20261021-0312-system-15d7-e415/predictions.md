# Predictions — 20261021-0429 (second author on 20261021-0312-system-15d7)

Written before any decisive run. The checker's named gold experiment: fly the deletion
(`kick_clock` takes the anchor over, gates the comb per kick on leave-safety, digest
re-frozen), re-run the census, plus one adversarial E→0/assist arm. Cases below are not
tuned on; the belt numbers come from the first run's frozen record, the seed-7 case from
the checker's own held-out run.

**P1 — instrument neutrality (control, must pass).** With the patch applied and
`ES_BOUNDARY_CUT` unset, the completed belt flight (`boundary_bill 30000 5000`) reproduces
the frozen record bit for bit: digest `f9af771e…`, kicks 1,290,749, encounters 24,264,
contacts 0, combs 1,267,977 (clock 510,004), fires crash 0 / leave 0 / handoff 18 (all
`release`, doll 2, bodies 30028-30068), kick-surface fires 0; the two plunge tests pass
with zero boundary fires.

**P2 — the deletion, belt.** With `ES_BOUNDARY_CUT=1`, the same flight: kicks 1,290,749,
encounters 24,264, contacts 0 all IDENTICAL; clock-stepped combs 0 (every one of the
510,004 deleted at the kick that would have planned it; gate-cut ≈ the clock kicks);
non-clock combs unchanged with the 18 releases at the same ticks and bodies; the **tubes
digest** (every per-body field the shipped digest hashes except step / interval / anchor /
plan items / event count) IDENTICAL to the baseline's; the full digest DIFFERS (anchor
written at the kick, no Boundary items, lower event counts — the re-freeze). If the tubes
digest differs, or any fire trace differs, the deletion changed physics and the claim dies.

**P3 — held-out seed.** Seed 7 (the checker's case), 3×10⁴, 200k gs, both modes: identical
tubes digests; baseline has 0 clock fires, deletion has 0 clock combs.

**P4 — adversarial, the 3b88 wall class.** B13's assist draws at step 8, each flown with
the gate off and on: per draw the outcome (alive, kicks, refused, lost, the 1% error
class, tubes digest) is IDENTICAL; across the suite both gate counters are live — GATE_CUT
on the bound approach legs, GATE_KEEP > 0 precisely on draws whose exit leg is near-escape
(post-assist heliocentric E ≥ 0, or bound with apoapsis −1/E ≥ 2^40): there the comb stays
and its certificates remain scheduled. A draw whose class flips kills the deletion.

**P5 — plunges under the cut.** The plunge suite passes with `ES_BOUNDARY_CUT=1` (plunges
carry no Darwin key, and a periapsis under the surface is the planned `What::Crash` item's
own tick): zero boundary crash fires, outcomes as shipped.

**Mechanism registered (what would falsify the gate itself).** The gate reads the binding
the kick leaves: a bound arc (`k = 1/(1+e) > 1/2`) with apoapsis `periapsis/(2k−1)`
inside `2^leave_log2` cannot reach the edge on that arc (r ≤ apoapsis exactly on the
tube), and the next kick re-checks; the margin is exact up to one ulp of the truncated
division. If any body leaves the system while its gate held, the gate is wrong.
