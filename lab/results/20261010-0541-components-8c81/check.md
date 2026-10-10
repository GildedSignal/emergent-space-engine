Grade: silver

**Abstract.** The plane's kick rebinds on every kick: 33.3 µs pure, 50.4 µs per item, against a ~1.5 µs floor (idiot index 22× pure, 34× per item). Reproduced: 34.3–34.6 µs, 3000/3000 rebinds and, in my own probe, 400/400 on **all 23 ships** (30–44 µs); 51.9 µs/item over the identical 49,619 items; crossing read 0.38 µs vs cold solve 2.97 µs; knots 6/16/42/86; Entry 176 B + Segment 184 B; the first kick fires ~7×10⁹ velocity quanta, 10 orders above the quantum, as claimed. But the gain from the named fixes is ~2.7×, not 34×: the floor's 0.1 µs force evaluation is asserted (measured 6.8 µs). Known already: H0210 "kicks cost 29 µs"; the taste log's ~99% recompile. Adopts nothing; it is diagnosis.

## Reproduction (clean tree, `git apply work/patch.diff`; Linux x86 shared runner)

| Number | Dossier | Mine |
|---|---|---|
| Pure kick resolve | 33.3 µs, 3000/3000 rebinds (100%) | 34.3 µs, 3000/3000 (kick_floor); 34.6 µs (cost_split) |
| Whole universe | 50.4 µs per item, 49,619 items | 51.9 µs, **49,619 items, exact count** |
| own readout / secondaries / tide | 3.35 / 3.27 / 3.35 µs | 3.39–3.48 / 3.40 / 3.43 µs |
| root_state after every event | 6.8 µs | 6.87 µs; `root_state_raw` (what `apply` actually calls, universe.rs:531) 6.96 µs — same |
| signed_state / crossing_state | 2.83–4.3 / 0.346 µs | 2.97 / 0.383 µs (8×) |
| compile at e = 0.01 / 0.70 / 0.95 | 5.4–9.3 / 32 / 128 µs | 8.1 / 33.7 / **63.5 µs** (the 128 is 2× off; the trend holds) |
| knots at e = .01/.30/.70/.95 | 6/16/42/86 | 6/16/42/86 |
| Entry / Segment | 176 / 184 B | 176 / 184 B (Binding 176 + Tick) |

Commands from the dossier all ran under 60 s after one 10 s build. Code reading confirms the mechanism: `kick` (step.rs:372–381) fires `dvq != [0,0]` against the velocity word `choose_units` sized to hold the state, then `rebind` (step.rs:307–328) always retires a Segment and emits a new Entry; `apply` (universe.rs:530–533) pays `root_state_raw` after every event.

## Adversarial cases

1. **Not a one-ship artifact.** I probed all 23 ships: 400/400 rebinds each, 100% everywhere, 30–44 µs per kick (Home orbiters ~40–44 µs, deeper-doll ships ~30–34 µs). The claim generalizes across the plane.
2. **The quantum gap, measured.** The first kick's `rec.b.kick.dv` = 7.4×10⁹ / 6.3×10⁹ quanta — Δv sits 10 orders above the quantum, exactly the dossier's mechanism; the sub-quantum carry indeed never fires.
3. **The root_state attribution.** `apply` calls `root_state_raw`, not the ramped `root_state` cost_split measures; I measured both: 6.96 vs 6.87 µs — no difference, the claim stands as measured.

## Predictions

`predictions.md` (05:50:36) precedes the probes (05:54:04) and the dossier (05:54:42) — written before the decisive run. P1 (≥90% rebind) and P3 (crossing 0.1–0.6 µs) held, P4 half-failed and is reported as split, honestly. But the held-out set is thinner than presented: P2 (rebind ≥50%) and P5 (overhead ≥30%) were already determined by numbers predictions.md itself lists as measured (from_state 12.8 + compile 5.4 vs pure 32.8; 17.6/50.4 = 35%), and P1's ≥90% was on the public board as ~99% (taste log, 5 October). Only P3 was genuinely quantitative and held (at its edge).

## Novelty

Partly known. H0210 already records "kicks cost 29 µs" and queues "kick cost (Sol)"; the taste log (5 October) already has "the plane recompiles an orbit on about 99% of kicks" with the jet/re-anchor wiring in flight (Sonnet); law.md already adopts the jet at 0.05 compiles/kick. Neither H0210 nor the taste log is cited against the claim. Genuinely new here: the decomposition (rebind ≈ 69% by subtraction, bounded by from_state+compile), the readout extremes (signed 2.97 vs crossing 0.38 µs) and the phase-carry argument, knots-vs-e, the per-kick byte weight, and the all-ships generality.

## Goal fit

Board focus item 1 (kicks dominate the engine's cost; fewer/cheaper kicks). PRINCIPLES P1 "the cheapest compute is compute not done" and P3 "Nothing is evolved that can be derived when looked at" — the rebind re-derives a whole compiled orbit per kick. Honest about cloud orders of magnitude and one machine.

## Why silver, not gold

The numbers reproduce, but nothing moves 10× and nothing is adoptable from this run: the main lever (jet/re-anchor, ~69%) was already adopted and is being wired; the run wires nothing. And the 34× headline leans on the floor's weakest link: "evaluate tide + secondaries… ~0.1 µs" is asserted, while the measured cost is 6.8 µs — and `secondaries` and `tide` are *themselves* readouts of other bodies (`state_of`, ctx.rs:81,101), so reaching that floor requires the phase-carry fix to extend beyond the ship's own state, unmeasured. With measured pieces, the named fixes deliver ≈ 50.4 − 21.9 (rebind→1.1) − 3 (readout→0.38) − 6.8 (lazy root_state) ≈ 19 µs/item: **~2.7×, not 34×**. "What would make it wrong" flags the re-anchor rate but not this hole.

## The experiment that would make it gold

Extend the phase-carry to the force reads — the kick's own state *and* the `secondaries`/`tide` `state_of` reads at crossing granularity — on a branch, and measure per-item cost against 50.4 µs. If the force evaluation drops from 6.8 µs toward the floor and the per-item lands near the predicted ~19 µs (with the jet), the index's deletions are demonstrated rather than asserted; if it stays at ~6.8 µs, the honest index is ~4–6× and the claim must be rescaled.

## What the author missed

- The 0.1 µs force-evaluation floor is asserted, not measured, and its realization requires carrying the phases of *other* bodies (the moon's, the centre's), not just the kicker's — the load-bearing number in the 34× is the run's only unmeasured one.
- The 34× index divides a whole-universe per-item cost by a pure-kick floor; 22× (pure path) is the apples-to-apples figure — disclosed, but the claim leads with 34×.
- H0210's 29 µs and the taste log's ~99% recompile (five runs) are prior art for the headline facts and go uncited.
- "The Calendar queue is already at its floor" is asserted; no queue measurement appears in the run.
- e = 0.95 compile is 63.5 µs on this machine against the dossier's 128 µs (cloud variance, order preserved — but the dossier's table carries one significant digit too many for a shared runner).
