# Dossier: the burn's cadence — the engine paying events for a state that cannot say "under thrust"

## Claim

The thrust-cadence clamp (`step.rs::thrust_step`, one kick per 1/64 of |v|) is the engine buying,
in events (817–2,990 player items per held burn; the L8+ burst; 0.46–1.67 s presented lag), a
readable state that cannot express a body under thrust between flushes — the same one word of
state the view re-derives per read (`held_thrust`, 7b86's a-slot) and gravity-news needs on the
version payload (½aT², 7ab4). Measured on shipped code, it buys the wrong things: deleting it
breaks the velocity word (prograde flushes refuse, the burn leaves the canonical state
entirely), refining it 16× costs 4–8× the events and still leaves the shipped arm 0.87–1.75%
off the fine limit. Neither direction is right; the burn's generator carried in the readable
state is, and this run prices its exact contract.

## Bottleneck

`frame-cost` (the flight sweep's L8+ stutter) and, by the same slot, `view`'s open direction 2
and `gravity-news`'s open direction 1 — the "one adoption, three bottlenecks" the view page
asked to price. Expected gain: deletes ~100% of the burn's event stream (the tide itself needs
0–24 events on the same flights, 20261013-0236-second-…-0f2a) and the L8+ lag, with no law
change to the physics if the carry composes exactly (`thrust::owed` is exact over any dτ).

## Evidence

All on shipped code plus this run's patch (`work/patch.diff`: an `ES_BURN_CADENCE` knob in
`thrust_step` — `ship` = shipped bits, verified digest-identical to env-unset on the coast
control — `f8` = 1/256, `fine` = 1/1024, `off` = clamp deleted), probe
`crates/universe/examples/burn_cadence.rs`: the page's paced flights (12 ms budget, rtf 100,
60 Hz), decisions scheduled at fixed canonical ticks (so every arm sees the same decision
ticks; readout differences are the cadence law's alone). Seed 1; seed 3 reproduces every count
and end speed to 6 digits (the flights are level-set, not seed-set).

**8 s flights, seed 1** (`regen.sh` tables `8s_*`):

| flight | arm | player items | worst frame items | lag s | refusals | end |v|/c | max owed dv (c) |
|---|---|---|---|---|---|---|---|
| forward L8 | ship | 817 | 31 | 0.698 | 0 | 1.971e-3 | 2.3e-5 |
| | fine | 9,688 | 78 | 1.662 | 0 | 1.999e-3 | 4.6e-7 |
| | off | 13 | 1 | 0.038 | 0 | 4.9e-5 | 2.0e-3 |
| forward L12 | ship | 2,442 | 65 | 1.525 | 0 | 3.2246e-2 | 2.4e-4 |
| | fine | 11,324 | 78 | 1.664 | 0 | 3.2939e-2 | 9.5e-7 |
| | off | 12 | 1 | 0.038 | 1 | 4.3e-5 | 2.9e-2 |
| forward L15 | ship | 2,815 | 64 | 1.646 | 0 | 0.25110 | 1.9e-3 |
| | fine | 12,039 | 77 | 1.656 | 0 | 0.25557 | 3.8e-6 |
| | off | 78 | 1 | 0.038 | 35 | 7.8e-5 | 7.7e-3 |
| reverse L8 | ship | 1,281 | 41 | 1.667 | 0 | 2.104e-3 | 1.5e-5 |
| | off | 18 | 1 | 0.038 | 0 | 1.966e-3 | 1.0e-3 |
| turn-then-burn L8 | ship | 802 | 31 | 0.291 | 0 | 1.695e-3 | 1.5e-5 |
| | off | 28 | 1 | 0.038 | 0 | 1.533e-3 | 7.3e-4 |

Coast (no decisions): all arms bit-identical (digest `c1aa22…` 16 s, `2f7697…` 8 s), lag 0.038 s
— that 0.038 s is the flight loop's own floor, and the `off` arm returns to it at every level.

**16 s flights, seed 1** (held out): ship 2,098/2,594/2,990 player items (L8/L12/L15; lag
0.456/1.586/1.666 s; end |v|/c 0.004302/0.069691/0.488862); `f8` 8,010/9,853/10,883 (end
0.004334/0.070298/0.492695); `fine` 17,661/23,326/23,504 (end 0.004356/0.070530/0.493137);
`off` 14/13/155 (refusals 1/1/73, every fault `Refused("velocity outside the word")`, end
4.9e-5/4.3e-5/7.8e-5 — the prograde burn never enters the canonical state). Retrograde at 16 s:
ship 1,421 items vs off 52, end |v|/c 0.004490 vs 0.004468 (0.5% low, no refusals).

Three findings, each way the waterfall's cost is currently justified:

1. **The events are real and deletable only by deletion.** `off` collapses the burn's player
   items 27–230× and the burst to 1; but prograde flushes then refuse at the velocity word
   (the lump does not fit the old exponent), the flush chain also starves itself (each flush
   raises the orbit, the raised orbit's step grows past the flight: 13 items where coast alone
   spends 77), and the burn ends entirely owed — the readout grid shows the canonical position
   tracking pure coast while the owed dv reaches 7.7e-3–2.9e-2 c. The clamp's actual contract
   is the **velocity word**, exactly as its comment claims.
2. **The events are not buying accuracy.** The shipped arm's end speed is 0.87–1.75% below the
   same law at 1/1024 on every prograde flight (1.24%/1.20%/0.87% at L8/L12/L15, 16 s); the
   1/256 arm lands between, 0.09–0.5% from fine (L15/L8) — superlinear convergence, so `fine`
   ≈ the law's limit. Paying 4–8× the events for 1/256 buys 0.1–0.7%; the shipped cadence keeps ~1%.
3. **The events are not buying smoothness either.** The `fine` arm's lag is 1.58–1.66 s — the
   same stutter as shipped (the paced frame's budget caps work per frame, so the lag survives
   any sampling); only `off` reaches the coast's 0.038 s. The stutter is the burst's existence,
   not its size.

## Predictions

`predictions.md` (written before the 16 s, seed-3 and f8 runs). P1 (events collapse; lag →
coast floor) held everywhere. P2 (deletion breaks the burn: refusals, burn lost, envelope ≥
10⁻³ c at L15) held, including the direction split the prediction missed: retrograde burns
(orbit-lowering) land without refusal but 7–10% low at 8 s (0.5% at 16 s). P3 (f8 between ship
and fine) held monotonically; its "≈ half the gap per halving" failed — convergence is
superlinear (f8 sits 0.09–0.5% from fine, not ~half the gap). P4 (items double at 16 s) held only at L8
(2.6×); at L12/L15 items grow 1.06× because the step grows with |v|. P5 (seed 3 within 3×)
held exactly — identical counts and end speeds.

## What would make it wrong

The carry I price assumes the flush can compose exactly from a carried generator (true in
rapidity: `thrust::owed` is closed-form). Two measured warnings: (a) the carried Δv must carry
its own exponent — the shipped flush refuses at the word instead of stepping it; (b) the
position half has no closed form on the curved tube (the shipped ramp carries the tide's dv but
no burn displacement at any cadence — the between-flush position error is the ½aτ² the envelope
measures, ≤ |v|/64 per interval shipped), so a carried position term is a truncated ramp: it
must re-anchor without accumulating (the kick-jet lesson, b33f/6c47: a carried state re-anchored
to itself random-walks). The untested hard case (the lens's own warning): a burn toward the
planet at carried cadence — the crash planner reads the burn-blind tube, so the warning can
arrive up to one step late; not measured here (no prograde flight crashes).

## Cost of adopting, and fit with PRINCIPLES

The carry replaces the clamp's three call sites with: the owed generator already in
`BodyRec::thrust` (α, heading, since — no new state), an exponent step on the flushed word, the
½aτ² term in the readers' ramp (`observe::credit`/`partial`), and events only on the tide's
quantum or key changes (0–24 per burn, the counterfactual already measured by 0f2a). It deletes
the burst frame and the L8+ lag class outright. "if you find yourself fixing things that's
oftentimes a signal that it is the wrong representation" (CL 09-29, principle 19): the clamp is
exactly such a fix — a sampling rule standing in for a state the representation cannot hold;
"we only care about changes" (CL 09-29 08:24): a held burn at constant α is one change, not
2,990.

## The lens

The whole-system lens found three bottlenecks independently re-deriving one word of state; what
it may have missed is the hard case it is built to miss: the dive/resonant regime where the
field's own cadence coarsens (0f2a's plunge: steps to ~2³² ticks) — there a carried burn must
still trip the impact and handoff planners, and this run's flights never dive with the burn
held toward the planet.

## Reproduce

`./regen.sh` (≈ 5–6 min): builds the patched example, verifies `ship ≡ unset` digest for digest,
then runs ship/off/fine/f8 at 8 s seed 1, ship/off/fine at 16 s seed 1, ship/off at 8 s seed 3,
and prints the tables above plus the staleness envelopes (`analyze.sh`). Raw tables and readout
grids in `work/table_*.txt`, `work/burn_cadence_*.tsv`, `work/heldout*.txt`.
