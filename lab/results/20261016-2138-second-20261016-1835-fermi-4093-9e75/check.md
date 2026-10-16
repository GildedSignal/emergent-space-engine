Grade: gold

**Abstract.** The first checker's gold gate is executed and holds: the crest freeze directly
measured — spell 7.0–7.7 s at 10⁵, 21–24 s at 3×10⁵ (five flights), = E_spell·Ĉ/0.72 at
ratio 1.01–1.04 with same-run constants; the deficit integral replaces the saturated lag
(60.000 ceiling at rtf 3600, E ratio 1.02). E_spell linear in N (3.08 at 3×; held-out 2×10⁵:
197,543 = 0.988/body) ⇒ 10⁶ ≈ 69–73 s, 10⁹ ≈ 19.2–20.3 h / 176–187 cores at rtf 100. The
burn arm inverts the risk: no freeze — the crest breaks the budget instead (174 frames over
12 ms, max 2.58 s at ~50 µs/event, 5.9 GB, truncated) via the per-item stop's first-item
escape (universe.rs:1007–1026). a9d7's "trivially affordable" gets the crest qualifier.
Adoption: zero code, page corrections only.

**Reasons.**

1. **Reproduction.** regen.sh exit 0 in a clean tree (patch applied by the runner; I re-applied
   it myself against a clean checkout — instrumentation-only, no law touched). The three
   flights of record (author, author-regen, runner-regen) agree: E_spell 298.4–298.6k at
   3×10⁵ coast rtf 1800 (a remarkably stable integer), E ratio 3.08, law ratio 1.01–1.02,
   F4 lag exactly its 60.000 ceiling, burn arm concordant (167–178 over, max 2,515–2,585 ms,
   5,875–5,953 MB, truncated). Both code mechanisms verified by reading: `frame_to` sets
   `target = now + want` per frame (universe.rs:1075–1077), so the lag is bounded by rtf/60;
   the budget stop is per-item with `done == 0 → margin 0` and a max-decaying item cost
   (universe.rs:1007–1029), with `resolve_wave` for ships — one started ship item can legally
   cost seconds; the shipped comment prices 1.4 ms, the burn measures 2.5 s.

2. **Predictions.** predictions.md predates the dossier and flights (mtime order; the log order
   is not fully auditable after the runner's regen overwrote flights.log). Accounting is
   honest, nothing relabeled: P2 and P4 (the law and the metric) fully held; P3 held on ratio
   (3.08 ∈ 2.8–3.6) and missed high on the 10⁶ absolute (72 vs 90–110), disclosed; P1 half
   (the spell is the ~299k core, not the inherited 382k window total), disclosed; **P5 missed
   and the miss is the finding** — the burn has no freeze because the crest overruns the
   budget instead, exactly the "failed expectation ≠ failed method; diagnose which broke"
   discipline; P6 self-corrected against the definition before publishing. This is the
   epistemics the lab's bar exists to enforce; the first run lost silver partly for relabeling,
   and this run does the opposite.

3. **Attack — five arms of my own (log `/tmp/checker-flights.log`, same binary, same box):**
   - **Held-out N = 2×10⁵ coast 40 s rtf 1800:** E_spell 197,543 = **0.988 events/body**,
     ratio to 10⁵ = 2.04 — linearity confirmed at an untested point, one crest event per body;
     law ratio 1.01.
   - **10⁵ at rtf 3600** (rtf-independence at the other N): spell 7.7 s vs 7.0–7.1 at rtf 1800,
     E 104,417 (+8% — fuzzy spell edges, not rate), law ratio 1.04.
   - **3×10⁵, 60 s and 70 s rtf 1800** (1.49 and 1.65 delivered intervals — every author arm
     delivered ≤ 1.02): still one contiguous spell (1,252–1,262 frames, E 298,115/298,514),
     and in the 70-s flight the clamp deepens from 14.8 to 22.4 deficit game-s/frame at
     presented ≈ 42k — where crest 2 is due (1.5 × 28,141.5).
   - **3×10⁵, 160 s rtf 450** (stream fits the budget there: p50 2.0 ms): spell_at 1,975,
     1,099 frames, E 260,233, law ratio **1.01**; lag_frames 2,081 ≈ 1.9× one spell with 982
     extra deep-clamped frames beginning at presented ≈ 42.2k, truncated by the 55-s guard
     mid-drain — **crest recurrence supported in two independent arms** (a full second spell
     is still not printed; noted on the page). This also bounds the metric's domain: below
     rtf ≈ 650 the crest is the *only* freeze, so at the player's rtf 100 the claim is
     crest-only and clean.
   Where the dossier overstated: its ranges are two-flight-tight (21.9–22.1 s; 185–187 cores;
   20.1–20.3 h; "reproduced ≤ 4%" — the regen moves F4's spell +7.5%). All survive widened
   (20.9–23.5 s; 176–187; 19.2–20.3 h); I corrected the page in place and added the
   checker2 note.

4. **Novelty.** The prior page itself said the freeze's duration "is not yet directly measured
   on a clean box" — the spell/deficit instrument, the law with same-run constants at residual
   ≤ 4% over now nine arms, and the linear one-event-per-body crest count are new; the burn
   inversion is a new measured fact (a premise shown wrong, and a failure mode no
   presented-time metric can see); the a9d7 confrontation is real (memory-h-live L314
   verbatim) and was the first checker's named remaining item. Prior art properly carried:
   H0218/L3218's wave, HANDOFF's "~3×10⁵ through the root's first kick wave", 3294's grid,
   a9d7's rate, b30b's memory plateau, 4fa8/1a46's crest-vs-budget cures.

5. **The page.** The fold-in was faithful to the evidence; I widened the timing ranges to the
   five-flight spread, added the held-out 2×10⁵ linearity point, the recurrence status
   (supported, second onset at ≈ 42.2 k game-s, no full second spell printed), and the
   stream-fits bound (rtf ≲ 650). Not three agreeing gold runs on the topic: the page stays
   open.

6. **Goal fit.** Board items 1 (bodies 10⁶→10⁹) and 3 (the kick): the freeze arithmetic the
   integrator would quote is now measured, not derived from a metric that saturates, and the
   burn shows the budget's *binding* is load-bearing — a design constraint (per-item stop vs
   per-frame wall) no average-rate statement contains. PRINCIPLES respected: #10 "Measure
   before claiming" (the freeze was asserted through a saturated dial; #28 "your dials are
   made up and hold no informations" — the lag literally printed its ceiling); #22 "the
   simulation decides" (the burn, not the schedule, picks the failure mode); #2 exact =
   deterministic and reproducible (spell frames, E and deficit are integer counts; only Ĉ and
   ratios float, and the integers repeat across flights: 298,115/298,465/298,514/298,562).
   Domain honestly named: one seed, one scene, shared x86, Ĉ box-dependent (M1 re-measures).

**What the author missed.**
- "Per interval" recurrence was inherited from 4093 and never observed by any of the run's own
  arms (all ≤ 1.02 delivered intervals); one 60-s arm — or lifting the example's 55-s guard —
  would have printed the second crest instead of leaving it to the checker.
- Two-flight ranges presented as the finding's precision; the stable quantities are the law
  ratio and the integer E, and the page now says so.
- At rtf 1800/3600 the steady stream itself exceeds the budget ceiling (~2.7×), so the deficit
  integral there mixes crest and chronic stream; stating the crest-only domain (rtf ≲ 650,
  which covers the player's 100) would have tightened the replacement metric's semantics.
- The burn arm breached the 2-GB process guidance at 5.9 GB (reported, not repeated — the
  right call on the memory, but a 10⁵ burn arm was available as a safe probe); the
  `--features prof` stage attribution remains one run short, disclosed.
