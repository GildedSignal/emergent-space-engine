# Check 2 (blind to the first) — 20261015-1450-second-20261015-1338-quant-1d52-0757

Grade: gold

**Abstract.** The bounded retained-entry cache (`ES_RETAIN_HOT=<cap>`, a global FIFO ring over the seam's per-slot caches) is built over the committed seam and closes 1d52's named experiment. I reproduced all 23 flights from the clean base + `work/patch.diff` with a private build: digests bit-identical per scene across 5–7 arms, every deterministic number exact (10⁵ coast 20k cap 16,384: 131,751 promos = 1.005×dem, 85.3% hits, retained_now 16,384; burn 10⁴ cap 65,536: exactly 1.00×dem, 0 evictions, hits = global's 584,807; inert without the seam), rss 388–415 MB vs global's 548–554 and shipped's 538–539. My adversarial cases — seed 7, cap 1, rtf 100, and burn at 10⁵ (10× the author's burn domain) — all keep identity and the bound; burn 10⁵ shows the working set scales with N (130,187: 7.22×dem at cap 16,384; exact containment at 131,072). Cost to adopt: one env-gated knob, cap × ~1.4 kB standing; the 10⁹ re-mint bill composes to ~0.15 cores.

## Reproduction

- Clean tree at `c989260f`, applied `work/patch.diff` myself, built in a **private** target dir, flew all 23 arms (`/tmp/ck2-fly.sh`, mirrors `fly.sh`). The runner's `regen.log` was contaminated mid-run: a sibling checkout rebuilt the shared `lab-target-0` binary at 15:34 (between flights 12 and 13), so flights 13–23 printed a counter format that does not exist in this patch (no `inflight`/`evictions`/`cap` line anywhere in it) and `table.py` died on it. Not the author's fault; `regen.sh` should freeze a private copy of the binary before flying. My clean run regenerates the dossier's full table exactly — digests (`5e8c9e24`/`a287f479`/`5caeb1b6`/`2109a2e0`), promotions, hits, shares, retained_now, evictions, cap-probe curve (512: 83.6%/1.12×; 65,536: 85.3%/1.00×), and the author's assertion bars.
- Code reviewed: the ring's accounting is sound — each fill pairs exactly one decrement (Drop-take or evict-take; a stale registration takes `None` and costs nothing), retained_now ≤ ring ≤ cap structurally; the only lock nesting is ring→slot (the slot guard is dropped before the ring is taken); demotion fires only under `lazy_entry_on()` at kick-settle, so `ES_RETAIN_HOT` without the seam is structurally inert (confirmed in flight: digest = shipped, counters 0). `Orbit::compile` is a pure function of the key (no statics), and the digest hashes the key identically from both slot variants — identity is structural, and my rtf-100 flight (10× the frames, a different read interleaving) confirms eviction scheduling cannot leak into it.
- Suite on the patched tree: lib+tests **77 passed, 0 failed, 3 ignored** (the dossier's "46/0/2" undercounts; same verdict); the `nladder` example link failure is the pre-existing macOS-only `proc_pid_rusage`, as stated.

## Predictions

`predictions.md` predates the scripts and dossier (56 m vs 34/32 m). P1 (identity) and P2 (bound) held on every flight including mine. P3/P5 held; P4/P6 held at the named arm and fired at 48k/burn — disclosed. P7 and P8 fired and the misses are reported as the finding (the coast cliff is soft in cap space; burn's working set is ~40k, not ~4k) — the honest-miss pattern the lab wants. Kill rule untriggered. All 23 author flights used seed 1 (the held-out-seed standard was left to the checkers); covered below.

## Adversarial (mine; each beyond the author's flown domain)

1. **Seed 7, coast 10⁵/20k** (author flew only seed 1): identity across ctl/seam/hot(4,096)/hot(16,384); 1.023×dem at 4,096 and 1.005× at 16,384; bound holds; rss 393/411.
2. **Burn at 10⁵** (author's burn domain was 10⁴): identity across seam/hot/16,384/131,072/global. Cap 16,384 thrashes — 940,718 promos = **7.22×dem**, 43.3% hits, 924,334 evictions: **burn's working set scales with N** (130,187 at 10⁵ vs ~40k at 10⁴). At cap 131,072: promotions = demotions exactly, 0 evictions, hits 1,528,451 = global's exactly — containment holds once the cap covers the working set, pricing it at cap-proportional memory instead of global's. This falsifies reading the recommended 16,384 as a universal default; the run's own thesis ("cap = working set + headroom; re-derived under law change") predicts it, and I folded the caveat into the page's open direction 1.
3. **Cap 1** (maximal churn): identity, retained_now = 1, 595,722 evictions, 4.55×dem — graceful, no pathology.
4. **rtf 100** (12,001 frames vs 1,201): digest identical to rtf 1000 and across arms; promotions move 134,359→134,486 (+0.1%).

## Novelty

The wiki's open direction 1 (from 1d52) named exactly this build as the missing adoptable piece ("the adoptable bounded cache is named, not built"); docs/HISTORY.md has no entry for it. This run builds it, flies it, and prices the cap curve and the working sets — new measurements, not a repetition. With this, three runs on the seam chain (e0f9, 1d52, 0757) agree on the current best's sentence, but 1d52 was silver and e0f9 ungraded here, so the page stays open (not three golds); I leave `status` as the author set it.

## Page

Faithful to the evidence except open direction 1's default-cap parenthetical ("16,384 … covers … burn 92.0%; 65,536 reproduces global's hits everywhere flown"), which held only inside the flown burn domain (10⁴); corrected in place with the measured N-scaling. The Current best's "at a sufficient cap" scoping is accurate.

## Goal fit

Board bottleneck #1 (28 → 10⁹ bodies). The package the seam lacked is now measured: 962 B/body standing kept (vs shipped 1,633–1,635 at 10⁵, and global retention's 548–554 MB rss) with promotions at the kick floor — the bare seam's ~6.8–19.6×dem promotion bill composes to ~130 cores at 10⁹, the bounded cache to ~0.15 cores (≈800×), for cap × ~1.4 kB standing (23 MB at 16,384 = 0.002% of the 10⁹ store). PRINCIPLES 6 ("Store the generator, not the generated") via negativa on the cache itself; P17 ("the best part is no part"): cap 0 is the seam, cap ≥ working set is global retention — the knob spans both measured ends. Default-off, one step to adopt.

## What the author missed

- The re-mint rate in the 10⁹ composition is misstated one decade: 698/(10⁵ × 2×10⁴) = 3.5×10⁻⁷ per body per game-s, not 10⁻⁸ (the headline ~0.15 cores is consistent with the correct value; the intermediate exponent is a typo).
- Burn was flown only at 10⁴; its working set is N-scaling (the cap is a per-scene quantity, the finding this run half-saw — "burn's working set is the wave's concurrently re-read bodies" — but did not stress in N).
- All 23 flights on seed 1; no held-out seed inside the run itself.
- The suite line undercounts (46/0/2 vs 77/0/3 measured) — same verdict, sloppy tally.

## Verdict rationale

Reproduced exactly on every deterministic number; pre-registered predictions with honestly reported misses; identity and the structural bound survive every adversarial case I could fly, including three outside the author's domain; the one degradation found (burn at 10⁵ under a fixed cap) is predicted by the run's own rule and is now measured into the page. It moves the board's first bottleneck by ~800× on the promotion bill at 10⁹ while keeping the memory win, deletes global retention's memory cost, and is adoptable in one step. Gold.
