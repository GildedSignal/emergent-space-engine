Working...
Check complete. `check.md` written: **Grade: silver**.

**Verdict basis:**

- **Reproduced** — runner's regen exit 0; all four arms match the dossier (mints 58, frozen arms answers=1/held 115/no drain in coast, serving arms 58/58/held 0, quiet warmup mints 0). Deltas are timing-side only: pilot S 2.97→4.20 ms, λ 14.5→14.1–14.4, RSS 53→53.5. The latch's code claims all verified in source: universe.rs:1190 (`room < 2·max(scan_ns, 0.75 ms)`), :1205 (decay only via served answers — the one-way latch), :1017 (count-cap inline path), and the duplicate Arc push at encounter.rs:192→universe.rs:1165.
- **Adversarial arms (new axes, all ≤17 s):** the frozen N=1000/seed-1 scene **serves at b=12 ms** (58/58), the serving N=500 scene **freezes at b=1 ms with answers=0** (the SCAN_MARGIN_NS floor — a miss in the dossier's "S > b/2" law), and N=4000 (outside the flown range) stays frozen with the per-scan pin linear (≈125 B/body, RSS 83.7 MB). The threshold is genuinely the dimensionless S/(room/2).
- **Not gold:** held-out P2 failed as stated (seed 7 serves), honestly reported; and the quantitative bands needed correction — the same N+seed gave S = 2.97/4.20/3.35 across three runs, so the boundary is run-fuzzy, not just seed-fuzzy, and the latch holds the *worst* (cold, first) answer, not the mean (pilot's steady flush S ≈ 2.1 ms vs the 4.2 ms that latched). Novelty is real but partial: taleb-51b7 already read the belt-scale case correctly; new here are the threshold law, the hysteresis mechanism, the sub-latch free regime at 10²–10³, and the candidate-set cure's criterion.
- **Gold experiment named:** build the candidate-set reduction and show S < room/2 through a burn at the player's N → B = 0, deleting the seam's bill — a measured ≥10×, not a criterion.

Page `wiki/scan-queue.md` corrected in place where it overstated (s band 1.7–4.2 µs/body, N_freeze ∈ [600, 1470], B ≤ 4 transient, margin floor, budget straddle). Topic stays open (one run). Nothing else in the run folder touched.
