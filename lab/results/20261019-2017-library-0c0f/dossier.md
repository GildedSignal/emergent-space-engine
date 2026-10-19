# Dossier — 20261019-2017-library-0c0f (library lens)

**Claim.** The ladder's named next wall — wave compute at 2×10⁵ — is decomposed for the first
time: it is a synchronized **arrival burst** (worst frame 33,069 events against a 90-event
median) riding a **half-idle budget** (median frame spends 45–55% of the 12 ms), so it is
deletable (birth-phase synchrony) and harvestable (compute-ahead in the ebb) before it ever
needs a scheduler — and the page's open directions re-rank: wave decomposition at 2×10⁵ above
the split's 2.30× re-read at 10⁵ (a memory question on a channel the TTL fence already deletes).

**Bottleneck.** nladder (board item 1: 28 bodies vs 10⁹). 7b6f (gold) closed the memory
question at 10⁵–2×10⁵; its checker's fresh arm left one undecomposed fact: "at 2×10⁵ the
first kick wave costs 1.2–1.3 s frames — the next wall at that rung is compute, not memory."
Gain on offer: the wave is 55 over-frames of 660 (8.3%) and p99 = 32× budget — deleting it is
the difference between a rung that flies at the player's cadence and one that stalls 1.7 s.

**Evidence.** Shipped `nladder`, burn, rtf 2000, 12 ms budget, Linux (print-only `/proc`
footprint probe, `work/patch.diff`, disclosed; no engine change), sequential flights:

Run-to-run spread (regen's own flights, schedule-elastic on the shared box; `work/arm_*.txt`
hold the latest regen): p50 5.4–8.0 ms, max 820–1,053 (10⁵) and 1,676–1,974 (2×10⁵), over
104–120 and 42–55, max ratio 1.78–2.07, p99/budget 13–40×, arrival ratio 177–400×, 2–9 of
the first 12 printed over-frames inside the wave — the laws the dossier claims (arrival-driven,
K-proportional max, half-idle median) are stable across reruns.

| arm | p50 ms | p99 ms | max ms | over | worst-frame events | lag |
|---|---|---|---|---|---|---|
| 10⁵ (1,020 frames) | 6.12 | 150.6 | 891.8 | 104 (10.2%) | 17,347 vs 92 median (188×) | 32.4 s |
| 2×10⁵ (660 frames) | 5.39 | 380.8 | 1,675.6 | 55 (8.3%) | 33,069 vs 90 median (367×) | 32.1 s |

- The over-frames cluster in the first kick wave: frames 465–490 at 10⁵ (= gs ≈ 15.4k, the
  record's own wave onset), 451–486 at 2×10⁵; 9/12 and 7/12 of the printed over-frames sit
  inside it. The wave is arrival-driven (P3: 188×/367×), K-proportional in max (P4: ratio
  1.88), and the presented time cannot hide it (85/79 frames behind, worst lag 32 s).
- Cross-check with the record: 2×10⁵ ends at 1,590 MB / 20.3k gs ≈ 7b6f's guard at 20,638 gs;
  the memory channel coexists but the frame channel is the new binder.
- Commands (≤ 4 min): `bash lab/results/20261019-2017-library-0c0f/regen.sh` — applies the
  patch, builds, flies both arms, prints the scorecard. Corpus: `work/readwise_pages.json`
  (770 docs, 4,590 highlights, 4.4 MB, fetched via the Readwise export API following
  `nextPageCursor`); every quote below is verbatim by highlight id from `work/highlights.jsonl`.

**Predictions.** `predictions.md` written before the flights: P3 (arrival-driven, ≥20×) and
P4 (max ratio ∈ [1.5, 8]) **held** (188×/367×; 1.88). P1 **failed on its letter**: p50 is
45–51% of the budget at rtf 2000, not ≤ 25% — the ebb fraction is cadence-defined, and at the
play cadence the record's own rtf-100 arms (p50 ≪ budget) support the ebb reading. P2
**half-held**: the shipped line prints only the first 12 over-frames; those cluster in the
wave window, the full distribution is not printed (a checker can print it).

**What would make it wrong.** (1) A staggered-birth arm (different belt phase, e.g.
`LADDER_SEED`) that still shows the 1.7 s wave would kill "deletable synchrony" — then the
burst is a law property and the scheduler question returns. (2) The rtf-2000 concentration
inflates per-frame spikes ~6× vs the player's cadence (record: max 322 ms at 10⁵ rtf 100 vs
892 here); if the M1 flight at play cadence shows over ≈ 0, the wall is an artifact of the
compressed cadence and re-ranks below memory again. (3) The ebb harvest fails if arrivals are
not known ≥ 1 frame ahead (kick grids are position-derived, so this should hold — unmeasured).

**Cost of adoption.** Nothing to adopt in the engine: the output is a re-ranking of the
page's open directions plus two pre-priced next arms (stagger, compute-ahead), each one
flight. The `/proc` probe is cfg-gated and print-only.

**Fit with PRINCIPLES.** "i care about the p95/99 results i want the game to be smooth"
(§12) — the wave is exactly the tail §12 forbids; "\"Use idle time to compute ahead\" yes
this is a whole important idea of this project" (§17) — the measured ebb (45–55% idle at
median) is that idea's fuel; "a fix signals the wrong representation" (§19) — a shared birth
phase, not missing scheduling machinery, is the wave's simplest cause.

---

## The five lessons (the lens deliverable, ≤ 40 lines)

1. **Delete the synchrony, don't schedule it.** "Always wait until the end of designing a
   process—after you have questioned all of the requirements and deleted unnecessary
   parts—before you introduce automation." — Musk, in Isaacson, *Elon Musk* (id779884732);
   "Delete any part or process you can… if you do not end up adding back at least 10% of
   them, then you didn't delete enough." (id779884739; the bar e181 already used for the
   fence). Mechanism: the algorithm's order makes deletion falsifiable and automation a last
   resort. Change: the wave is a requirement artifact (shared kick-grid phase at birth), so
   price the birth-stagger before any allocator. Test: one flight per phase offset; collapse
   ⇒ artifact (target: max 1,676 ms, over 55 at 2×10⁵).
2. **The constraint moved; move with it.** "The rate-determining step is the slowest part of
   this chain… forming a bottleneck that ultimately defines the amount of time needed."
   — Young, *Ultralearning* (id507901155). Mechanism: constraint-following — memory bound
   10⁵ (7b6f); the frame binds 2×10⁵ (p99 = 32× budget). Change: re-rank the page — the split
   re-read at 10⁵ sits below the wave decomposition at 2×10⁵. Test: this run's probe (2 min).
3. **Spend the ebb on the wave.** "At LGE, they made a science of the gathering and release
   of intensity… the better we are at recovering, the greater potential we have to endure and
   perform under stress." — Waitzkin, *The Art of Learning* (id674778852). Mechanism: peak
   capacity is built in recovery intervals, not by raising steady effort (Julien's
   compute-ahead, CL 09-25). Change: a compute-ahead arm — next-frame-due kicks evaluated in
   the measured 45–55% idle median, a schedule move, no law change. Test: one env-gated arm
   at 2×10⁵; over and p99 vs 55 / 381 ms.
4. **The law is better than you think.** "I've very often made mistakes in my physics by
   thinking the theory isn't as good as it really is, thinking that there are lots of
   complications that are going to spoil it." — Feynman, *Surely You're Joking* (id678770477).
   Mechanism: adding machinery the representation already carries; the shipped calendars
   (`child_ticks`, per-doll) already schedule by deadline, and the steady engine is 350×
   under its worst frame. Change: treat the wave as a scene artifact until a staggered-seed
   arm fails to collapse it. Test: same flight as lesson 1.
5. **Nothing efficient until the break risk is gone.** "If something is fragile, its risk of
   breaking makes anything you do to improve it or make it 'efficient' inconsequential unless
   you first reduce that risk of breaking." — Taleb, *Antifragile* (id1006185301); "Knowledge
   is subtractive, not additive" (id764888575). Mechanism: p50 5.4 ms "looks fine" while p99
   is 32× budget and the player's presented time falls 32 s behind. Change: the compute-wall
   rung's gate is max_ms/over at the worst wave across seeds (B15's rule), never average kick
   cost. Test: this run's digits are the baseline (1,676 ms / 55 / 32.1 s).

**The lens's blind spot.** Practitioner analogies are cheap where physics decides: the wave
could be a genuine law property of kick grids, and no Skunk-Works maxim deletes physics. The
probe exists to keep lesson 1 falsifiable; a library run without it would have been a
catalogue. Also: this corpus (770 docs) holds no Kelly/Skunk Works/Shannon highlights — those
names in AGENTS.md are bookshelf, not Readwise; the lessons above draw only on what was
retrieved verbatim, and nothing here needed the UNVERIFIED mark.
