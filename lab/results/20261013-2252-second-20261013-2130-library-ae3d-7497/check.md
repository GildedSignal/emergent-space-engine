Grade: gold

The checker-named experiment is done and the claim holds: on four shipped `plane`
settles the per-body kick distribution is not heavy-tailed — the tube bulk is flat
per orbit by construction (CV 0.17–0.20), the three-decade per-second spread is
period and clock regime, and the head is the burn driver (70.6% at 48 members,
diluted to 2.6% at 4,000) — so rule 2 dies and promotion stays a fixed fraction.
Reproduced bit-for-bit on a clean tree; the probe is proven digest-neutral
(`e0972a1c…`). Gain: deletes the ladder's rank-rule rungs and surprise-rate
instrumentation, pointing promotion cost at ephemeral `resolve_handout` and
compaction scheduling. Adoption is one design decision. One prose ratio did not
reproduce; the page is corrected.

## Reasons

1. **Reproduction (clean tree, patch applied by hand).** `git apply work/patch.diff`,
   build, then my own `frame_digest 8 L15` on the patched tree gives the stored base
   digest `e0972a1ce81d30950df93a0b1ec8d37c` (kicks 1684, encounters 597, 4 schedules
   agree) — digest-neutrality re-proven, not just trusted from regen.log. All four
   scenes rerun: every deterministic number identical (76/73/71/3,988 bodies;
   9,176/96, 10,800/969, 2,142/48, 78,299/88 kicks body/origin; CV 0.179/0.173/
   0.189/0.189; player 21.1/17.9/70.6/0.2%; members p50 5, mean 20.6, max 174, Gini
   0.549, max/med 4.68, 22/3,769 with sub-kicks; Orbiter 2 rows 212.4/202.0/212.1/
   212.1; haulers 0–2 kicks at 40,000 game-s, 0 at 3,600). Store rows: 12.347
   bits/member at 7–8 ns, storm 48.38 with fallback (0 mismatches), convoy compaction
   1.27 ms / 2,570 repacks; hot max 10.5 µs vs the dossier's 10.9 — timing jitter
   only, disclosed as orders of magnitude.

2. **Predictions.** `predictions.md` (22:57:03) predates the probe directory's
   creation (23:07:49); the author's original captures were overwritten by the
   runner's regen (23:15+), so per-file proof is gone — directory mtime plus the
   disclosed half-failures is the evidence, stronger than the first run's (whose
   captures predicated predictions). Outcome as reported: P1 held (my seed 3:
   CV 0.203); P2 half-held, honestly dissected (per-orbit spread 42× is
   extrapolation from ~1 kick; per-second the haulers are uniform); P3's decisive
   half held exactly (burn player 70.6% ≥ 30%; top-3 76.9% ≥ 50%) and the letter
   miss (21.1% vs <20%) is reported and re-read correctly as frequency; P4 held —
   it is the verdict. None of the pre-registered kill criteria fired (CV > 1?
   no. idle top-1 > 30%? max 28.1%. burn player < 10%? measured 70.6%).

3. **Adversarial cases (mine; two outside the author's tested set).**
   (a) *Seed 3, idle m48* (untested seed): bulk flat (CV 0.203, Gini 0.114, top-1
   10.4%), idle player 13.3% — the seed range widens the letter of P3 downward.
   (b) *Held L12 burn inside the 4,000-member battle* (untested combination): the
   player takes 2.6% of body kicks — the driver head dilutes into the member stream
   exactly as the fixed-fraction reading predicts; members per-lived-second Gini
   0.41, top-1 0.2%, no rank.
   (c) *Span decade, 400,000 game-s* (10× the author's longest): bulk CV 0.182
   unchanged; Orbiter 2 at 212.39/orbit against 212.37 at 40,000 game-s — the
   cadence is deterministic across a decade of game time, no drift-induced tail;
   haulers at 14–15 kicks stay ~4×10⁻⁵/s. One instability found: the idle player's
   per-second share grows with span (21.1% → 28.1%) as the battle's bursty member
   churn amortizes — still under the 30% kill bar, mechanism unchanged, and the
   stable statistic (per orbit, flat with the orbiters at 250.3/orbit) is what the
   claim uses. Noted on the page.
   (d) *40,000 members* (the next members decade): killed at ~447 s, exit 137 —
   over this window's 2 GB process budget. Unmeasured; named as the open edge
   (and a datum for the ladder's memory-per-live-body question, though this probe's
   logging shares the blame).
   (e) *Statistical attack on "no rank structure"*: members' raw kick counts are
   overdispersed (CV 1.27 vs Poisson's 0.22) — the member stream is dispersed, not
   flat — but headless: the top 10 bodies hold 2.2% of the stream, max/med 4.68,
   top member 0.07%, and passage sub-kicks land on whichever members the battle
   handed out deep in the well. The conclusion stands on the headless numbers; the
   dossier's derived ratio "per-lived-second top-10%/median 1.0–1.2" is **not
   reproducible under any natural reading** (p90/median 4.05; top-decile mean over
   overall mean 2.34) and is defined nowhere — corrected on the page to "top-10%
   holding 2.3× their uniform share: dispersed but headless". This is the run's
   one blemish: a prose ratio, not in the evidence table, not load-bearing.

4. **Novelty.** The `nladder` page's open direction 1 was exactly this falsifier,
   written by the first run's checker as the one experiment to gold; no H entry or
   wiki page measures the per-body kick distribution's shape (kick-cadence's 43
   runs decide *which cadence certifies behaviour* — adjacent question, distinct;
   the author cites 27ce/7f97 for the hauler over-provisioning and 174d/0f2a for
   the waterfall it re-measures). The `resolve_handout` 486–585 µs sticky citation
   is verified against the frame-cost page. This is the second graded run on the
   topic (the first was silver): not three agreeing golds — the page stays open.

5. **The page.** Corrected in place, five overstatements: CV/Gini bounds restated
   over the seeds actually run (0.17–0.20, ≤ 0.12); "per-body numbers identical"
   → near-constant ±5% (Orbiter 2 202–223/orbit — the page's 210.6–212.4 had
   silently dropped seed 7's 202.0 that the dossier itself lists); idle player
   share 13–28% across seeds and spans; the m48 sub-kick counts (the dossier's
   "8/38 with 14–261" conflated seed 7's count with seed 1's range: measured 10/38
   at 14–261 and 8/37 at 4–196); the member top-10% ratio (above). The fold-in
   itself (rule 2 struck, direction 4 promoted to primary, runs appended) is
   faithful to the evidence.

6. **Goal fit.** Board focus 1's live question "the smallest promotion between a
   compact body and a live one", decided by measurement on shipped code at the
   moment the ladder is in flight. PRINCIPLES #3 "Compute only surprises" (the head
   is drivers — already events on the light cone); #19 "A fix signals the wrong
   representation; one law at every scale" (one cadence law explains the bulk; a
   promotion-by-rank rule would have been the second convention); #1 "The cheapest
   compute is compute not done" (a rank nobody needs to measure). Gold on the
   "deletes a component / shows a premise wrong" limb: the rank-rule rungs and
   surprise-rate instrumentation are deleted from the ladder design, adoptable
   within one step, with the domain honestly scoped to the plane and the belt
   named as the revival path.

## What the author missed

- The unreproducible "1.0–1.2" ratio (defined nowhere; the honest member picture is
  dispersed-but-headless, and it is the headlessness that kills the rank rule).
- The span-dependence of the idle player's per-second share (21→28% over a decade
  of game time): harmless against the 30% kill bar, but anyone reading per-second
  shares for promotion should use the span-stable per-orbit statistic.
- The 40,000-member edge is unmeasured and did not fit this window's 2 GB budget
  (exit 137) — the ladder's own next question, now named on the record.
- The belt (conjunction clustering) as rule 2's honest revival path is named but
  unmeasured; the claim's domain is and says it is the plane.
