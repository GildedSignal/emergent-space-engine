Grade: gold

**Abstract.** The claim reproduces and survives every probe I flew. Bit-exact from the re-applied patch (2 arms re-flown: every canonical counter and digest identical). Beyond the author's domain, six probes of my own, all identity-clean: N=2.5×10⁵ (ratio 7.832 at 0.65×N; exactly 1.000, 0 evictions at 1.31×N; bill N+30,111 — knee scaling holds at a fourth N); cap 120,000 = 1.2×N (ratio 1.000, hits exactly global — "7.0–8.5 at every cap below 1.31×N" is falsified); doubled cut (ratio 72.5 at cap 65,536 — the band and the wall tax are matched-cut constants); seed 5; ONCE at the knee (1.000); who at 2×10⁵ (mints 98.4% apply; ~85% of sampled hits the scan). The decision stands: no constant cap serves burn; admission is dead; the deletion is the phase-neighbour certificate. Cost: default-off instrumentation on the seam patch; nothing ships unless the seam is adopted.

**Reproduction.** `regen.sh` exit 0 (runner) and again by me after `git apply` in a clean tree: the coast anchor (41,053/41,524/763,888, `5e8c9e24`) and the full table regenerate. I re-flew `bound16384` and `retain` at 10⁵/20k/s1: demotions, promotions, hits, retained_now, kicks, bodies, frames and digest (`d3542eea`) all identical; only timing percentiles/wall differ (shared box — not canonical). The instrumentation is env-gated and default-off (verified in the bind.rs hunks: `ES_MINT_WHO`, `ES_RETAIN_ONCE` read env in `LazyLock`s; `#[track_caller]` histograms). The tree was restored clean after my runs.

**Predictions.** `predictions.md` predates the flights (file times vs `flights/` and `regen.log` order). P1's kill test did not fire (knee ≫ 32,768); P2–P5 held as the dossier reports, with the scan-share overshoot honestly reported. `ES_RETAIN_ONCE`'s refutation is four arms deep (16,384 worse, 65,536 better, both coast arms worse) — and my ONCE-at-knee arm (exactly 1.000) confirms the mechanism reading: without eviction pressure ONCE degenerates to FIFO, so its coast/below-knee losses are the cascade kill, not a policy win.

**Adversarial (mine, beyond the flown domain; all digests per-scene identical).**

| probe | result |
|---|---|
| N=250,000 (2.5×10⁵, out of range), cap 163,840 = 0.65×N | ratio **7.832** (band) |
| same, cap 327,680 = 1.31×N | **exactly 1.000**, 0 evictions, bill 280,187 = N+30,111 |
| 10⁵, cap 120,000 = 1.2×N (transition never flown) | **1.000**, hits exactly global's 1,528,451, promotions = demotions, 10,187 evictions all on dead fills |
| 10⁵, cap 130,186 = bill−1 | **1.000**, hits exactly global |
| 10⁵, cap 65,536, cut 40,000 (2× matched cut) | ratio **72.5**; extra promotions = hit deficit exactly (11,460,990 = 11,460,990); wall +77% vs global |
| 10⁵ seed 5 | bill 132,755; 1.000 at 131,072; 7.107 at 16,384 |
| `ES_MINT_WHO=2` at 2×10⁵ | mints 98.4% `readout←cartesian←root_state_raw←Universe::apply` (scan ~0); ~85% of sampled hits `encounter::Scan::compute` — the hit share still grows with N (26%→71%→~85%) |

**What the probes change (page corrected in place, no rewording):** two constants in the headline die, not the law. (1) "7.0–8.5 at every cap below 1.31×N": cap 1.2×N already serves every hit — the functional knee (zero extra promotions) lies in (0.65×N, 1.2×N]; the mint-bill razor is the no-*eviction* threshold, sufficient not necessary (bill−1 also serves everything; the evicted fills are dead). (2) The 7–8.5 band and the +14–30% tax are matched-cut constants: at doubled cut the same cap reads 72.5 and +77% wall, while the extra=deficit identity stays exact — the cascade compounds with horizon depth. The load-bearing content — knee linear in N, no constant cap serves burn, mints pinned to kicks, hits owned by the scan, admission dead — is confirmed at every N I flew, two beyond the author's range.

**Novelty.** Nothing in `docs/HISTORY.md` on the knee or `ES_RETAIN`. The page's prior state (0757 gold, b0ed silver) had the burn endpoints but neither the knee's localization and scaling, nor the call-site mechanism, nor the admission-family kill. This run closes b0ed's checker-named gold experiment — the designed handoff, not a repetition.

**Goal fit.** Board bottleneck #1 (bodies 10⁶→10⁹): it kills the "adopt S=16,384" premise and the admission family, prices the below-knee fence as a growing tax on the scan's own O(N) work, and leaves global retention's 10⁹ fence (~1.3 TB) unshippable — the deletion is open direction 2 (the phase-neighbour certificate). PRINCIPLES 3 ("Compute only surprises": the scan's re-read of a not-yet-kicked binding is not a surprise) and 6 ("Store the generator, not the generated": below the knee the cache degenerates to mint-per-read, honestly). Gold: reproduced, predictions held, premise shown wrong, adoptable within one step.

**What the author missed.** The transition between 0.65×N and 1.31×N (one flight would have caught both overstated constants); the dead-fill distinction (evictions ≠ re-mints), which turns the razor from "the knee" into a sufficient bound; the cut-dependence of the below-knee band and tax (their own "What would make it wrong" flags the scene family but not the cut); and the patch edits `lab/wiki/nladder.md` (conflict resolution) — the publisher's job, not the author's; the proposed page in the run folder is the right vehicle. Identity count is 27 arms, not 26.
