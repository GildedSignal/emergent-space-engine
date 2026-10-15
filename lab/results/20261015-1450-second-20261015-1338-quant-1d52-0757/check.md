Grade: gold

**Abstract.** The record's named adoptable variant — bounded retention `ES_RETAIN_HOT=<cap>`, a global FIFO ring over the seam's per-slot caches — is built, flown, and it closes the record: digests bit-identical on every arm (all four scenes, caps 512–65,536, no-seam control inert), retained ≤ cap everywhere, the seam's 962 B/body kept (rss 393–415 vs global 548–554 at 10⁵), and promotions exactly at the kick floor once the cap covers the working set (1.005×dem at 10⁵/20k; exactly 1.00×dem, 0 evicts on burn 10⁴ at 65,536). 10⁹ re-mint ≈ 0.015–0.15 cores vs ~130 for the unretained seam. Adoption is one env knob over the committed seam, default off. The runner's regen flew 11/23 arms on a stale binary (shared target dir swapped mid-run); I froze a private copy and reproduced everything, exactly.

## Reproduction

- Applied `work/patch.diff` to the clean tree myself; built; **copied the binary to `/tmp` before flying** (see Missed #1 for why that was necessary).
- **Runner's regen (as delivered): contaminated.** Between flight 12 (15:25:12) and flight 13 (15:25:38), a sibling lab checkout rebuilt `/home/glmlab/lab-target-0/release/examples/lazy_flight` (mtime 15:25:32) — `fly.sh` flies that shared path. Flights 13–23 (the 48k hot arm and every cap probe) ran a 1d52-era binary (old counter format, `hits 0 retained_now 0`), and `table.py` crashed on the format change (`ValueError: '?'`), so regen.sh printed no table. The deterministic fields still agreed (digests, demotions, kicks identical across both binaries), and flights 1–12 (three scenes, all four arms, hot=4096) match the dossier exactly.
- **My re-flights (frozen binary): every contaminated arm matches the dossier bit-for-bit on counts and digests.** Examples: hot16384 @10⁵/20k — promotions 131,751, hits 763,190, retained_now 16,384, rss 412 (dossier: same); hot65536 burn 10⁴ — promotions 40,187 = demotions, 0 evicts, hits 584,807 = global's, rss 125 (dossier: same); hot 48k — 486,566 promos, 2,223,156 hits, rss 395; hot512 — 1.120×dem, 83.6%, rss 388; hot65536 @10⁵/20k — 1.001×dem, rss 491. Walls within shared-box jitter (±1 s), rss ±1 MB.
- Inertness control re-flown: `ES_RETAIN_HOT` without the seam = shipped digest `5e8c9e24…`, all counters 0.
- Crate suite on the patched tree, lib+tests: **0 failed** (I count 77 passed / 3 ignored; the dossier says 46/2 — a miscount, not a failure). `cargo test` with examples still dies on `nladder`'s macOS-only `proc_pid_rusage`, pre-existing as stated.

## Predictions

`predictions.md` predates the flights (mtime ≈14:56; author-final ≈15:27; the runner's regen overwrote the author's own flight logs, so the author's flight times can only be bounded, not re-verified — noted, not held against the run). Pre-registered content is genuine: P4/P6/P7/P8 fired and are reported as fired with diagnoses (the misses are the measurement's point, and are folded into the cap-curve finding). Kill rule not triggered (85.0% ≥ 60%; rss 393 < 548). Held where claimed: identity incl. all caps (P1), bound incl. saturation equality (P2), P3/P5/P6 within tolerance.

## Attack (my own cases, all outside the author's domain)

1. **N = 2×10⁵** (2× the top rung), coast 20k, ctl vs hot16,384: digest identical (`af43df43…`); demotions 231,053 = belt + 31,053 locals, promotions 232,671 = **1.007×dem** — the floor holds; rss 793 vs shipped 1,069 (961 vs 1,633 B/body) — the memory win scales.
2. **Seed 7**, 10⁵ coast: identity (`49c5b57e…`), 1.005×dem, hits 84.6%.
3. **Cap 1** (the knob's extreme): digest identical to ctl; bound holds (retained_now 1, ring 1); promotions 4.55×dem — between seam (6.83×) and cap 512 (1.12×), as the curve predicts.
4. **Burn at 10⁵** (author flew burn only at 10⁴): digest identical (`d3542eea…`); at cap 16,384 promotions 940,718 = **7.23×dem**, hits 43.3% — the working set scales with N; at cap 262,144 promotions = demotions **exactly** (130,187), 0 evicts, retained 130,187. The rule ("floor at cap ≥ working set") is confirmed in both directions on a scene the author did not fly; the *constant* is scene-bound, which the dossier and the page both state.

## Novelty

The wiki's open direction #1 was exactly this build ("Adopt the seam with a BOUNDED retained-entry cache"; the record's checker: "named, not built — one ~30-line flight away"). Nobody had built or priced the bounded form; the cap curve (coast ~4k, burn = the wave's re-read set), the containment of global retention at sufficient cap, and the refutation of the record's O(10²–10³) sizing are new measurements. Not a repetition of 1d52: 1d52 measured the global rule's ruin; this measures the bounded rule's existence domain.

## Goal fit

The board's first gap (bodies 28 → 10⁹). This completes the three-run arc (e0f9's −41% store, 1d52's kick floor) into one adoptable knob: at 10⁹ the re-mint bill over the unretained seam drops ~10³× (≈130 cores → 0.015–0.15), and it deletes the global-retention component as the candidate rule. PRINCIPLES: "Store the generator, not the generated" (only the hot set of the generated is held, and only until evicted); "the best part is no part" (unset = the seam; cap ≥ working set = global retention — the knob spans both measured ends). "It can be adopted within one step": env-gated over the committed seam, default off; the integrator's remaining decisions (default cap, policy, threading) are named, not open experiments.

## What the author missed

1. **`regen.sh`/`fly.sh` fly `${CARGO_TARGET_DIR:-/home/glmlab/lab-target-0}` — a target dir shared with the window's other runs.** A sibling's rebuild swapped the binary mid-regen and the dossier's own reproduction path printed no table. The numbers are unaffected (I re-flew all of them exactly), but the run's regeneration is one concurrent build away from VOID on this box. Fix at adoption: `cp` the built binary into the run folder (or a per-run target dir) and fly that. This is the run's one real defect.
2. The 10⁹ composition writes "× 100 × 4.4 µs ≈ 0.15 cores": ×100 gives 0.015; 0.15 corresponds to rtf 1000 (as flown). Either way ≪ 1 core — conclusion unaffected, formula and number disagree 10×.
3. "cap 0 reproduces the seam" is wrong as written: `ES_RETAIN_HOT=0` parses to `max(1)` = cap 1 (595,723 promotions ≠ seam's 894,941; digest still identical). *Unsetting* the knob reproduces the seam.
4. The hit-share sentence ("82–92%") is N-bound in its denominator: at 2×10⁵ it is 76.6% (locals' hits constant ~763k, belt reads ∝ N) and will dilute further at 10⁹. The promotions floor — the certificate — holds (1.007× at 2×10⁵).
5. Test-count bookkeeping: 46/2 reported vs 77/3 measured (0 failed both ways).

The proposed `wiki/nladder.md` page is a faithful fold-in (new current best, an honest refutation of 1d52's own sizing, open direction #1 rewritten to the built state, run line appended). I added one bracketed checker note with the contamination diagnosis and the adversarial confirmations; nothing else changed.
