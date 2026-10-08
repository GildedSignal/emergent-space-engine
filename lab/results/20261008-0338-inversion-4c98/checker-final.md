Working...
Check complete. `check.md` written — **Grade: silver**.

**Reproduction:** all 8 runs (`fleet`, `loose-fleet`, `fleet+crossers`, `fleet+belt` × 2 seeds) regenerate **bit-identically** except `wall_s`; the per-population split and the cadence-coupling table (33.6→11.0→6.1→3.0, ratios 0.33/0.56/0.49) reproduce exactly. Predictions were pre-registered (03:45 vs data 03:54). Truth instrument verified sound: a dense 16,001-sample rescan found no missed sub-ρ minima.

**Why not gold:**
- Two held-out predictions failed: P3 in magnitude (p99 11.0 vs >20; kill direction intact) and P6's clause "no practical cadence brings crossers under k=4" is **false** — at 64 refreshes/orbit p99 = 3.0; the surviving argument is the 64× sort cost, honestly restated by the author.
- My adversarial case falsifies the dossier's own scope sentence "survives inside any lone formation": an e-spread formation (same a, Δn≈0, e∈[0,0.3]) misses **9–10%** at k=4 — intra-orbit longitude-rate spread (~2e·n) breaks rank with Δn = 0, so the trigger must gate on differential longitude rate, not Δn alone. The gold's literal domain survives: a same-orbit train at e=0.3 has 0 misses, max rank 2.

**Why silver, not lead:** the core inversion stands reproduced — fleet-scope misses 100% of cross encounters (structural), global-scope 7.4–21.7% at k=4, and rank = Δn·Δt_refresh·N/2π with linear cadence coupling. It confines the in-flight co-orbital build pre-freeze at the cost of one spec constraint. The named gold experiment: fold the eccentric term into the trigger and pre-register the corrected domain.

Folder state: author's JSONs restored after my reproduction overwrote them; only `check.md` added.
