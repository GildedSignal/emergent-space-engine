Working...
Check complete. `check2.md` written; tree restored to base `5bb0a840`; the author's page corrected in place with my measurements.

**Grade: silver.**

What I did, in brief:

- **Reproduced** from a clean tree (patch applied, release build): the full mechanism table matches the author's files and the runner's 53-draw blind regen — gas 134–171 rollbacks at final lead 0, clumps/streams/quiet clean, margin 2.0 absorbing every conflict. The blind regen caught **0 fires** against the author's 1/14, the race the dossier itself discloses.
- **Caught the fire independently, three times**: battle s11 (1/6), fresh seed s19 (1/6), and — outside the author's tested range — a doubled 8704-body/24-fleet battle fired **2/4** with the exact shipped assert (`alloc.rs:1451`, fin_hi 1232 vs s0 1216). Incidence rises with N; the exposure is not seed-11-specific.
- **Refuted one secondary claim**: the margin-0.0 "progress collapse at chronon 3" never reproduced (0/7 fresh replicates; the cited `run.log` is 0 bytes). Already softened on the page; my data confirms it.
- **The gold-blocker**: `predictions.md` (written before the sweep — timing verified) pre-registered margin 2.0 at rates 300/600/1200; the decisive sweep silently ran margin 0.5 at rate 2400, and at 2.0 nothing fires. The dossier reports "P2 held" without flagging the post-hoc protocol change. Core finding real and valuable (fleets are the fix's test scene, churn without slack is inert); one pre-registered incidence ladder on the N × margin grid away from gold.
