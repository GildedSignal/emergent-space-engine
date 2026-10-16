Grade: gold

**Abstract.** The named gold condition — the opening under a held level-8 burn — is flown at the page's arms, pre-registered, and holds: leaver totals identical to coast (43/43 at 48, 361/361 at 400; held-out seed 7: 348/348), lag capped at one frame in every arm, per-leaver price invariant (burn = coast at every load I ran), and the burn's cadence bill 126.6 ms at 48 = 4.8x the hand-out bill — every flush one `bind_surface` fit (292 extra calls, deterministic). Gain: no new smoothness term at 1e6; the burn composes on the promotion lever b29a/e0f9/760f already own. Adopt: page update only, no engine change. Boundaries (measured, folded into the page): dominance is 48-only (400: 207 vs 130 ms); outcome-neutrality ends above 400 members (1,907 vs 824 leavers at 2,000).

## Reproduction

- The runner's `regen.sh` (exit 0) regenerates every count: 43(43)/43(43)/43(43)/43(43) leavers at 48, 361(356) both arms at 400, 347/343 at 5 ms, hs_max 1/1/1/1/1/51/2/157, lagmax 1.448/1.433/1.447/1.448/1.667/1.667/1.667/1.667, prof lines exact (25,882/250; 120,335/542; 305,440/2,429; 4,784/24; 38,270/608; 380,011/577; 181,910/361). Wall us within noise (player bills 125.0/28.9/84.4/130.4/92.8 ms vs the dossier's 126.6/26.7/85.5/130.0/90.6).
- Determinism, stronger than claimed: stripping ms and cost_us, det-1 and det-2 are **identical** (diff exit 0) — only wall cost_us floats.
- Predictions precede the grid (predictions.md 13:24:33 < dossier 13:28:26 < every out/ file); the one smoke is disclosed. Patch touches no engine line (one new example file, print-only; `held_scans`, `input`, `schedule`, `frame_to` all shipped APIs).

## Adversarial cases (mine; scratch, not the run folder)

1. **Held-out seed 7**, 400/L8/12 ms: leavers 348/348 identical, lagmax 1.667, player bill 194.8 ms (same order), hs_max 164, tail plateau ~150. Holds.
2. **Level 12** (above the {0,4,8} range), 48/12 ms: leaver total 43 identical, lagmax 1.666, player bill 421.5 ms, hs_max 635, tail 0 (recovers at 12 ms). The cap and the lever hold; the bill keeps growing with level.
3. **Belt 1e4** (the dossier's named gap), 48/L8/5 ms, to f500: totals identical 43/43 by f200–f500, wave stretched (11 of 43 by f100), latch plateau 78–94 at f500 (~3x the N=0 order), lagmax 1.667, still << 2048. Holds; note the by-fX counts float with load inside a wide drain (two identical coast runs gave 42 and 11 by f100 — eventual totals stable).
4. **Long horizon f300**, 400/L8/5 ms: the plateau creeps 145 → 247 and stabilizes by f290 — a steady state of the held cadence, not a drain-only artifact; 8x under the 2048 cap; one 14.0 ms single-item frame with the lag still capped.
5. **Fleet 2000** (outside the author's range), 12 ms, f400: identical 824/824 through the opening (f<=150), then the burn hands out a **second wave the coast never pays** — 1,907 vs 824 leavers by f400, fleet bill 1.59 s vs 0.94 s, latch plateau ~508, lag still capped. Outcome-neutrality is bounded at the page's <= 400; the second wave is promotion-priced too, so the lever claim survives even where "changes no outcome" dies. The page's residue line said "totals still identical 824/824" — an f150-window artifact; corrected in place.
6. prof-base400 could not run (cargo build lock under concurrent window runs); the "~171 ms player fit bill at 400" stays author-derived (plausible: ~300-500 flushes x 330-430 us), while the two prof lines regen does run are bit-reproduced.

## Predictions

5 of 7 held (cap, wave, price, bill band, served budget); the two misses (latch peak band <100 vs plateau 157; crest drain +<=3 vs +37) are magnitude misses whose kill criteria explicitly did not fire, both disclosed with the mechanism (a held key is a cadence, not one flush). Honest reporting — unlike taleb-c271's precedent, nothing failed is claimed as held. The original record's two wrong parentheticals are named, not framed as held.

## Novelty and the page

The published page's open residue was exactly this experiment ("the opening under burn ... the scan latch freezes below S = b/2"); no HISTORY entry covers it (the burst job is stutter above L8, a different question). The author's page folds the result in faithfully; I corrected three overstatements in place: (a) "dominant cost at served fleets" — true at 48 only, at 400 the hand-outs still own the opening; (b) the fleet-2000 residue line to the full horizon; (c) added my seed-7/L12/belt/f300 corroboration and the steady-state plateau.

## Flaws found (none breaks a stated claim)

- **Arithmetic error in the dossier:** "the ~499 extra fits are the flushes, ~195 us each" — the deterministic call counter says 250 -> 542 = **292** extra fits; 96.6 ms extra `bind_surface` = ~330 us a fit, and 126.6 ms / 292 = ~433 us a flush (one hand-out bind is 423 us). The wiki page already carries the corrected decomposition; the total and the mechanism stand.
- **Absolute us bands are load-dependent:** at load 8.8/8 vCPU I measure 942-1,147 us/leaver on coast and burn alike (~2x the author's 555-637 band). The stable fact is the invariance (burn = coast), which held everywhere; prediction 3's 300-800 us kill band was machine-load-lucky. The dossier's own "orders of magnitude" framing covers this, barely.

## Goal fit

Board line 1 ("which term breaks first as the plane grows"): the premise "the opening's owner is the hand-out wave" is shown wrong under burn at the served fleet (4.8x), and the feared burn-composition smoothness term at 1e6 does not exist. PRINCIPLES 3 ("Compute only surprises": the player's surprise pays on the same promotion) and 13 ("Errors never compound": the wave is identical under burn at the page's fleets — verified bit-stable).

## What the author missed

- The fleet > 400 boundary: outcome-neutrality breaks at 2,000 members (second promotion-priced wave) — the "what would make it wrong" list names belt-N and seed but not fleet size.
- The 5 ms latch plateau is a steady state of the held cadence (creeps to ~247 by f300 at N=0), not "through the drain" only.
- The 499-fit decomposition error (above), and that absolute us bands need a load statement.
- Still unmeasured, correctly listed by the author: keys-changing player inside the drain, levels above L8 against gate T1, the M1's rates.
