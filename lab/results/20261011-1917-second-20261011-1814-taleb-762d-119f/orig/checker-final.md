Working...
Check complete. `check.md` written to the run folder; the tree is restored (patch reverted, no tracked changes).

**Grade: silver.**

**What reproduced** (fresh `git apply`, release build, same commands): everything load-bearing — the digest `fbb0c7d5…adc72` identical across budgets 5/1/0.2/0.05 ms and pacing; the members cliff at 0.2 ms (m4: 1239.5×, m400: 0.00089× with 186 events/s — identical to 4–5 digits, deterministic); level-15 low tail 0.681; paced worst frame 12.3 ms with clean p99.9; frame cost ×6.3 for ×13 bodies. Seven scene digests matched bit-exact across processes and loads.

**Adversarial results:** the cliff is *stronger* than claimed — m400 stalls even at 1 ms (0.044×), m100 (124 bodies) stalls at 0.2 ms, and it holds on seed 2 with digests that discriminate seeds. But the dossier's mechanism ("fixed 0.2–1 ms per-frame prologue before any event is bought") is falsified by the author's own data: events/s scale ~linearly with budget (186/1212/4527 at 0.2/1/5 ms = 4.1% of events at 4% of budget; the default scene is superlinear). A real prologue would starve events to zero at 0.05 ms. The floor is peak event density ÷ budget-sustainable throughput with presented time causally gated — a different guard than the O(1)-in-N prologue audit the dossier proposes.

**Other findings:** predictions were pre-registered (18:17 vs 18:19–18:29 artifacts) and honestly scored (P2 failed in letter, disclosed); table row 1 mixes scripted and coast runs against a coast-only reproduce command (the rtf 30000 row is not regenerable as instructed); "engine p50 2.9→8.8 ms" matches no saved column; digest-across-budgets was already claimed in H0210, so claim 3 is re-verification extended to the stall regime, while the budget-floor falsification of foundation 7's "overflow is a brief smooth dip" is new.

**Gold path:** one experiment — decompose the floor (events per game-second vs members, plus one profile of `Universe::advance` at m400) — decides whether the gate is a density floor or a prologue audit.
