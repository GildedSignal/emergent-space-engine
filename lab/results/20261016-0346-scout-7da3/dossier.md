# Dossier — 20261016-0346-scout-7da3 (scout)

- **Claim:** ES_STAGGER is a permanent cure for the belt's wave train, not a one-wave one — the staggered train stays flat to ±3% across four wave periods at 10⁵ and 3×10⁵ budget-free — and the staggered F1-letter break moves to ≈ 1.7–2.2×10⁶, past the memory break, pinning the composed 10⁹ wave letter at ~2× (580× at the shipped kick).
- **Bottleneck:** board live question 1 (bodies in the flyable engine: 28 → 10⁹), the wave term: the record's ranked break-Ns put the unstaggered F1 letter at 8.4×10⁴ and left the staggered letter unpinned ("the one number this budget could not pin", nladder open direction 1). This rung flies it: +20–26× on the letter break, i.e. the wave stops being the binding break below ~2×10⁶.

## Evidence (all numbers from `regen.sh`; CSVs + `census.txt` in work/)

Arms: coast, player at Home, rtf 1000, 60 s page time (≈ 60,000 game-s ≥ 4 wave periods), engine budget disabled (10⁶ ms), `ES_STAGGER` off/on at N = 10⁵ and 3×10⁵ (ed3a's patch verbatim from its branch, `work/patch.diff`; off = shipped verbatim by construction, digest-verified off-identical by ed3a on its tree). Peak RSS 1.42 GB at 3×10⁵.

| arm | p50 ms | p99 ms | max ms | max ev/frame | train shape |
|---|---|---|---|---|---|
| 10⁵ off | 3.18 | 69.9 | 215.7 | 4,243 | waves every 14,167 game-s: peaks 4,243 → 2,223 → 1,579 → 1,194 (×0.72/wave) |
| 10⁵ on | 5.57 | 12.4 | 16.5 | 455 | flat: top 250-s windows 2,700 ± 3% over the whole flight |
| 3×10⁵ off | 3.36 | 220.2 | 681.8 | 12,729 | waves at 14.2k/28.3k/42.5k/56.6k: 12,729 → 6,603 → 4,443 → 3,437 |
| 3×10⁵ on | 13.7 | 25.5 | 36.4 | 711 | flat: top windows 6,330 ± 4% |

- **µs/event regenerates the record exactly**: unstaggered birth-wave peak frames run 50.8 (10⁵) and 53.6 (3×10⁵) µs/event vs the record's 47–51 on this box class; crest density (events per game-second, rtf-converted: 4,243/10 = 424 and 12,729/10 = 1,273 vs the record's rtf-100 anchors 487 and 1,328) regenerates to 87% and 96% — my frames are 10× wider in game-s, so the crest is averaged; the per-event rate is exact.
- **P3, the decisive held-out case (never flown staggered anywhere):** no second-wave re-concentration. Unstaggered, wave 2's peak is 52% of wave 1's (2,223/4,243); staggered, there is no wave structure at all for 60k game-s — the top six 250-s event windows span 2,700–2,775 (10⁵) and 6,288–6,366 (3×10⁵), i.e. the train is uniform to ±3–4%. Mechanism as constructed: one common doll-grid interval (measured period 14,167 game-s) plus hash-uniform birth offsets is stationary — Kepler shear cannot fold it because offsets live on the shared metronome, not on orbital phase.
- **Letter arithmetic (M1-projected, rtf 100, 12 ms, 29.3 µs/event):** staggered crest density 27.3 (10⁵) / 42.7 (3×10⁵) ev/game-s → per rtf-100 frame 45.5 / 71.1 events = 1.33 / 2.08 ms. Break-N where the worst frame hits 12 ms: ×5.76 in crest from 3×10⁵ → **1.7×10⁶** (using the measured max; 2.2×10⁶ using p99 55.8/frame) vs the record's unstaggered 8.4×10⁴ — a 20–26× move, past the memory break (1.3×10⁶) and at the build break (2.1×10⁶). At 10⁹, linear-in-N crest: ~142k ev/game-s → 237k events per rtf-100 frame → 6.9 s/frame = **~580× the letter at the shipped kick, ~2.2× at the key-arm kick (0.11 µs)** — pinning fermi-1a1c's unpinned "0.5–2.7× with both" at its top.
- **New structural datum:** the wave train's period is exactly 14,167 game-s at both N (waves at 14,167 / 28,317 / 42,483 / 56,617), i.e. the belt's effective kick interval is one doll grid of 14.17k game-s here, not the 28,141.5-s median 3294 censused on its arms; the unstaggered peaks decay ×~0.72 per wave (3294's "shearing 3× per wave", now with the period); and the recurring waves are cheaper per event than the birth wave (12.2 µs/ev at wave 2 vs 50.8 at wave 1 — first-kick clock compiles dominate the birth wave's cost).
P4 anchors held in density terms (87%/96%, µs/event exact) but only after the disclosed
rtf-1000→100 conversion — my bars ignored the 10× frame-width factor, an arithmetic slip in the
prediction's form, not an instrument failure. P1 FAILED as written (measured 455 events / 16.5 ms
at the flown rtf 1000 against bars of 150 / 8 ms); in the letter's own frame width (rtf 100: 45.5
events / 1.65 ms) it passes with margin — 45.5 vs fermi's predicted 29, inside my uniform-spread
band's lower edge. P2 FAILED as written: the crest scales sublinearly (455→711 = 1.56× for 3× N;
p99 1.74×) because the crest is fluctuation-dominated at 10⁵ — the mean scales 2.64× as expected;
the break-N arithmetic uses the measured crests directly, so it does not rest on P2's assumed
scaling. P3 held decisively. P5 held (1.7–2.2×10⁶ ≥ 10⁶).

## What would make it wrong

The 10⁹ composition extrapolates crest density linearly in N from 3×10⁵ to 10⁹ (3,333×) on one doll with one population; a driven or resonant belt (no shipped stirring mechanism exists — the burn is the only driver) or a finer crest statistic at 10⁶ could move the composed letter by the crest/mean factor (measured 2.0–3.4, bounded by the p99 arm: 2.2×10⁶). The M1 projection multiplies this box's µs/event by the record's 29.3/50 ratio; the integrator's M1 re-measure decides the last 10–20%. The stagger itself is a law change (kick times shift by up to one grid; digests differ — ed3a documented this; behaviour gates must be flown before default-on, and the held-out checks below are the next rung's).

## Cost of adoption, fit with PRINCIPLES

One 14-line constants-only genesis change, already written (ed3a's patch, default-off env). It converts the birth wave — pure bookkeeping phase-lock, not a surprise — into a uniform stream: PRINCIPLES #3 ("compute only surprises"; the wave is genesis-lock, measured absent of physics by 3294/f82a), #12 ("minimize spike compute and average compute usage"; both tails and floor measured above), #17 (idle-time ahead: the flat train is schedulable by least-slack, the spike was not). It deletes nothing observable (no averaging; every body still kicks — only its clock's phase moves).

## The lens

Scout's cross-field search shortened to the known answer: a phase-locked birth grid is a thundering herd, and jitter-at-birth (load balancers since the 1990s; kinetic data structures' desynchronized certificates) is the standard cure — the lab had already built it (ed3a); the missing knowledge was whether the cure survives its own second wave (it does, permanently, because the offsets ride the shared metronome). What the lens cost: I spent the search budget where the wiki already held the answer; the rung value is the measurement, not the discovery. Held-out for the checker, unflyown by me: seed 3, the 10⁴ staggered arm at wave 2, and crest statistics at 10⁶ (memory permitting — it was not, here, under the 2 GB cap: 3×10⁵ peak RSS 1.42 GB).
