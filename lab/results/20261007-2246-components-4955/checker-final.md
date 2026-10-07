Working...
Check complete. `check.md` written to the run folder; nothing else there touched; scratch removed.

**Grade: silver.**

What I did:
- **Reproduced** the full decisive grid from the dossier's commands (empty patch, clean build): every cell matches — wheel at 10⁶ within ±6% (179/68/219/184 vs author 188/69/224/187 ns/event), 10⁷ wheel 318 vs 343, rebuild spike 1.06 s vs 1.2 s; heap-side numbers compress on the quieter box, so ratios land at 2.2–6.6× vs the author's 2.1–9×, same directions, no inversion. All dossier medians re-derived from `metrics.jsonl` cell by cell.
- **Exactness**: `verify ok` on 14 configurations of my own (four workloads, fresh seeds, n up to 100k, cancels included); `CalendarU64` confirmed line-for-line the shipped algorithm, so the Scalar-key isolation is sound; the wheel's rebuild can't mis-bin (only fires with all buckets empty).
- **Attacked** with four adversarial workloads at n=10⁶ × 3 seeds — re-set storms at 1/8 and 1/4 rates, a bimodal two-clock scene, an all-same-tick volley. All exact; the wheel still beat `calendar_u64` 1.5–6.4× on every one. The design's robustness claim survived everything I threw at it.
- **Novelty**: no prior measured comparison ("calendar queues (1988)" appears only as a mention in archived engine.md); the timing-wheel lineage is correctly cited as prior art with skin in the game.
- **Predictions**: written before the grid (mtimes + machine-state.log consistent); held-out cells held; misses disclosed honestly.

Why not gold: gain is 2–9× on the component, the queue is not a ranked board bottleneck, and the load-bearing claim — the queue's share of the engine's own per-event cost — is asserted, never measured. Plus one number the log contradicts: the "24 ms at 10⁶" rebuild spike is actually formation's burst; belt 10⁶ measures 80–130 ms in both our logs. The gold experiment is one step: wire the wheel (or just u64 keys) behind the shipped interface and measure the plane's cadence end-to-end.
