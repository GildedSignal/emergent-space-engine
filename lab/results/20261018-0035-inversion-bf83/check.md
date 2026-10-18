Grade: gold

**Abstract.** Claim: the game's own fleet battle (`worlds::galaxy` 12 fleets, `Law::Relativistic`, sabotage off, shipped `min_region 32`) fires the shipped finality assert at `speed_margin 0.5`, while belt shapes stay clean and gas churn is inert without slack. Reproduced independently: 3 fires in my 12 fresh battle draws at margin 0.5, all seed 11 (0 on ~40 draws of seeds 12–24), one at a 4× horizon (20 s, present ~15k); every arm's rollback/lead profile matches (gas 134–171 rollbacks, lead 0; margin 2.0 absorbs all conflicts, 0 rollbacks). Gain: corrects the exposure premise — fleets, not churn, are the hazard — so direction 1's engine fix is tested on fleet scenes, not gas. Adoption cost: none (a reproducer command and a test-scene choice). Refuted in check: the margin-0.0 "stall" (degrades, never stalls).

## Reasons

**Reproduction.** Applied `work/patch.diff` (one new example, no engine change — verified: assert at `alloc.rs:1451` is the shipped `"would revise its published tick"`; `Config::default` = `speed_margin 2.0`, `min_region 32`; shipped finality tests do run at `speed_margin 0.0`). Ran the dossier's exact command plus 46 battle draws of my own:
- Fires: author 1/14; runner's regen 0/53; me 3/12 at rate 2400 (seed 11: retries 2/6, long horizon 1/6; quiet rerun loop 0/8). Pooled margin 0.5: 4 fires / 62 draws, every one seed 11 (seed-11 subset: 4/25) — the author's P5 seed-skew law holds exactly, and matches the page's standing s11 skew (bc0f, e517).
- Arm profiles all reproduce: battle rollbacks 1–5 with lead 200–1,088; clumps 9–27 rollbacks at `min_region 1` with lead to ~1,504; streams 10–12 rollbacks; gas 134–171 rollbacks with lead exactly 0; margin 2.0 → 0 rollbacks everywhere.
- **New fact confirmed beyond the author's record:** the battle conflicts *at shipped `min_region 32`* (rollbacks 1–5 in every operator's draws) where bc0f's churn family at 32 had `rb exactly 0, 9/9`. The game's fleets reach through the knob that protects every synthetic scene — this is the run's strongest adopted sentence.

**Predictions.** `predictions.md` predates the sweep (mtimes 16m vs 7m before my read; content matches the pre-run design). P2 (the decisive one) held in the author's run and mine; P3, P4, P5 held; P1 failed and is disclosed with a diagnosis my reproduction verifies (the instrument detects fires — I caught 3; gas was the wrong positive control, mechanistically: lead 0 ⇒ `fin_hi ≤ s0` always, the assert's exact negation). P6 dropped, disclosed. Honest record.

**Adversarial cases (mine).** (1) Rate 600, the axis the author's own predictions promised then dropped: it is the keeping-up rate (present pinned at 2,698 = 4.5 s × 600 on all seeds), lead ~240, 0/12 fires — the axis is dead; 2400 was the right choice, but the deviation from the pre-registered arms should have been named. (2) Fresh seeds 21–24: 0/8, profiles unchanged. (3) Horizon 4× the author's (20 s, present 14.3k–15.4k): 1 fire in 6 — the exposure persists past the author's window. (4) Margin 0.0 on gas, 3 replicates: present 3,086/4,446/4,656, rollbacks 250–259, exit 0 — **the "present stalls at chronon 3" progress-collapse claim is refuted**; margin 0.0 degrades progress ~2× and multiplies rollbacks, it does not stall. Page corrected in place.

**Novelty.** First use of `worlds::galaxy` in any harness (grep over crates + all local run folders). The page's prior fires are all selfchurn/batch/crossing families at `min_region 1` with instruments or sabotage; the game generator unsabotaged at shipped knobs is new, and direction 5 names exactly this question. Not in HISTORY.

**Page.** Faithful to the evidence except two overstatements, corrected in place: the margin-0.0 stall (one draw stated as a law) and "crossings never fire" (bc0f has a crossing-family crash in another window; now scoped to this horizon). Added the checker numbers.

**Goal fit.** Directly serves direction 1 (the top open direction): the fix's test scene is fleets, and the e517 state certificate `armed ≤ 0 ∧ D ≤ 0` should be evaluated on converging-fleet scenes. PRINCIPLES: "not making mistakes matters more than doing things efficiently, don't multiply by zero" — a panic is the zero, and this run stops the fix from being validated on a scene class (gas) that cannot fire without slack. Protocol honours the page's direction 4 (seeds × replicates, controls both sides: quiet negative, gas churn, margin-2 clean).

## What the author missed

- The fire is load-coupled: my 3 fires all landed inside concurrent draw batches; 0/8 in a quiet loop, 0/53 in the runner's regen. Incidence is a function of scheduling pressure — worth a line in the protocol, and the reason one-checker-regen silence (0/53) is not evidence of absence.
- No instrumentation (admitted): porting e517/fd35's print-only PRE/HAZ to the fleet scene would make the fire state-decidable (`D > 0` at certify) instead of a race — the natural next run, and it would measure *which* fleet pair crosses.
- Dossier number ranges not backed by any saved artifact and off from what regenerates: battle "rollbacks 1–3, lead 224–512" (actual 1–5, 208–1,088) and margin-2.0 "0–1, 224–384" (actual rb exactly 0, lead 576–720); `run.log` is empty. Qualitative claims unaffected.
- The margin-0.0 stall was one race draw generalized into "ruin".
