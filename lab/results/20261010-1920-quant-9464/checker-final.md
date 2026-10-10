Working...
Check complete. **Grade: silver.**

**What I did:**

1. **Reproduced everything byte-exact** from a clean tree: the clamp artifact (unpatched `--members 1024` → digest `8b9f11b6` = the 400-member universe, matching `m400` and all voided first-sweep runs), then with the patch applied: `m1024` → `806340f5`, `m2048` → `e1c14c30` (572 leavers), `r100m1300` → `7536927c` (821 leavers), threads 4 = threads 1. Timings within co-tenant scatter; the marginal-cost arithmetic (3.4 µs/member, 24× readout/engine) checks out against the raw stage p50s, and the wall arithmetic matches `scenes.rs`/`anchor.rs` (r_p/32, grid 20q + 5q·√(N/2) → N ≈ 1310).
2. **Adversarial cases:** seed 7 keeps the wall (573/112 leavers vs 572/75); threads 4 at the readout-bound regime — same digest, no gain; 65536 members degrades to ~25 ms frames at 1.2 GB without crashing, **but loses 2 bodies** — an edge the author never reached.
3. **Two record defects found:** the rtf-100 p99 SLA breaks between 400 and 1024 (`r100m1024` p99 17.72 ms, 10 800 hitches/h), not "between 1300 and 2048" as the dossier states — contradicted by its own table; and `predictions.md`'s mtime (19:31:46) postdates the decisive sweep (19:28:46–19:29:35), so pre-registration is unverifiable (mitigated by the honestly-reported failed P4).
4. **Novelty:** no HISTORY entry measures the plane's population ladder; the clamp is a real premise kill, and the queued `b-readout-cost`/`b-belt-wire` get their ceiling numbers from this run.

Silver, not gold: solid, fully regenerable measurement with a one-line adoption, but no 10× moved, one misstated break-point, and unverifiable held-out status. The gold experiment: a pre-registered second-scene ladder (wall ∝ r_p², 24× ratio invariant) or the O(visible) readout cull landing ≥10× against these ceilings. Tree left clean (patch reverted; only `check.md` added to the run folder).
