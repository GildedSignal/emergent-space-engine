Grade: silver

**Abstract.** Claim: the game's fleet scene (`worlds::galaxy`, `Law::Relativistic`, margin 0.5) fires the shipped finality assert unsabotaged; belt-shaped scenes stay clean. Reproduced: the whole mechanism table (53 blind regen draws — gas 134–171 rollbacks with final lead 0, clumps/streams/quiet clean, margin 2.0 absorbs every conflict) plus three independent fires of my own: battle s11 1/6, fresh seed s19 1/6, and 2/4 at a doubled 8704-body/24-fleet battle (exact `alloc.rs:1451` assert, fin_hi 1232 vs s0 1216) — incidence rises with N, the first rung above the author's range. Gain: the engine fix's test scene should be fleets, not gas (churn without slack is inert); a main-constructible reproducer. Adoption cost: none. Short of gold: the pre-registered decisive arm (margin 2.0, rates 300–1200) was changed post-hoc to 0.5/2400 without the dossier flagging it, and the chronon-3 stall is a one-draw artifact (0/7 fresh replicates).

## Reasons

**Reproduction (clean tree at base 5bb0a840, patch applied by me, release build 11 s).**
- The dossier's table matches `sweep-results.txt`/`battle-extra.txt` line for line (14 battle draws at margin 0.5, 1 fire s11 rep1, exit 101; clumps 0/12 at rb 9–27 (mr1) and rb 1 (mr32); streams 0/6 at rb 10–12; gas 0/6 at rb 135–171, final lead 0; battle margin 2.0 0/6 with rb 0).
- The runner's blind regen (`regen-results.txt`, 53 draws): every rollback/lead number reproduces; **0 fires** — the headline 1/14 is a race point estimate, exactly as the dossier's own "What would make it wrong" warns.
- My own fire hunt: battle s11 margin 0.5 → **1/6 fires** (exit 101); the fire is real and reachable by an independent hand.

**Adversarial cases (mine, five, two outside the author's tested domain).**
1. *Fresh seeds (17–19, outside 11–16):* seed **19 fired 1/6**. The exposure is not seed-11-specific.
2. *First N rung above the range* (galaxy 8704 bodies, 24 fleets, span 12, margin 0.5): **2/4 fires** (s21 both reps), exact shipped assert. Incidence grows with the battle's scale — the direction the 10⁹ goal cares about.
3. *P6, the dropped arm* (battle min_region 1): 0/4 fires, rb 1→5–6. More splits give more conflicts, as predicted; incidence inconclusive at 4 draws.
4. *Gas margin 0.0 ×3:* rb 247–254, present 3,956–4,700, regions 512→1 — degraded but **never stalled at chronon 3**. With the regen (present 3086) that is 0/7 replicates for the stall; the author's "progress collapse" is a one-draw artifact, and the dossier's cited evidence file `run.log` is **0 bytes** — the probe's stall/region numbers are not in the record.
5. *Gas at rate 600 under load:* 0/3, rb 138–143, final lead 0 (present 1.2–1.7k — the engine did not keep up on this loaded box). The keeping-up lead is machine-load-coupled; the "churn without slack is inert" reading holds everywhere I probed it, and remains a necessary-condition pair (slack AND unplanned meeting), not a sufficient one.

**Held-out predictions.** Timing is clean: `predictions.md` (00:39) predates `sweep.sh` (00:45) and `sweep-results.txt` (00:47). P3/P4/P5 held; P1 failed and is honestly reframed (gas was the wrong positive control — no slack); P6 dropped, disclosed. But **P2 as pre-registered did not hold and was not run as written**: the arms say margin 2.0, rates 300/600/1200; at margin 2.0 nothing fires (0/6 author, 0/6 regen), and the decisive sweep silently moved to margin 0.5 at rate 2400. The dossier's Evidence and What-would-make-it-wrong sections are open about the margin, but the Predictions section reports "P2 held" without flagging the post-hoc protocol change — the same class of miss the lab has graded down before (r3 v3, r4 v2).

**Novelty.** The page's direction 5 named exactly this gap ("a stirred belt or a battle is sustained overlap by construction"); b966/01e7/bc0f reached the assert only on synthetic selfchurn/batch harnesses, e517/fd35 on the finpol instrument. bf83 is the first unsabotaged reachability from the game's own scene generator (`worlds::galaxy` fleets), plus the scene-class separation (fleets fire; clumps/streams/gas clean) and the margin-axis warning. A genuine increment, not a repetition.

**The page.** The bf83 paragraph is faithful to the evidence as corrected (the chronon-3 stall already reduced to "one draw, not a law"); I folded my checker2 numbers in place (s19 and 8704 fires, the 0/7 stall tally, the load-coupled lead). The "seed-11-skewed" framing should now read as fat-tail skew across seeds, which my edit says.

**Goal fit.** Answers the first half of an open board direction (allocator-ratchet 5) and steers the engine-side fix's test scene before it is built. PRINCIPLES: "not making mistakes matters more than doing things efficiently, don't multiply by zero" — a panic on the game's own scene is the zero, and this run prices which scene class produces it. Nothing to adopt in the engine; the reproducer is main-constructible (`exposure battle 11 2400 32 0 0.5`).

## The one experiment to gold

A pre-registered incidence ladder on the fleet scene, predictions first: N ∈ {4352, 8704, 17408} × margin {0.5, 1.0} × ≥3 seeds × ≥3 replicates at recorded load, reporting the fire rate per rung (my 1/6 → 2/4 is its first edge) — plus one firing fleet draw under e517's fin_hi/PRE instrument to name the armed/D state the fix must kill. That converts "reachable, race-decided" into a rate and a state certificate on the game's scene, which the fix can gate on.

## What the author missed

- The pre-registration deviation (margin 2.0 → 0.5, rates 300/600/1200 → 2400) undisclosed in the Predictions section; at the pre-registered margin the named result does not exist.
- `run.log`, cited as the probes' record, is empty; the stall and the 2,304-region figure are unrecorded and the stall is refuted (0/7).
- The N axis: never varied. One rung up (8704) doubles-plus the observed incidence (2/4) — the most game-relevant number in the check was one 18-second experiment away.
- Seeds beyond 16: s19 fires at 4352; "seed-11-skewed" was an artifact of six seeds.
- No instrumentation of the firing draw (disclosed in The lens; it leaves the fix's state certificate unevaluated on the one scene class that fires).
