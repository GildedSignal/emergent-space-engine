Working...
Check complete. `check.md` written to the run folder; nothing else there touched, no commits, scratch left in `/tmp/check0411`.

**Grade: silver** — real, reproduced, honest; one experiment from gold.

What I did (30 min):
- **Reproduced from a fresh build** (clean tree at 70f27a9, own target dir, 24 s build): every digest bit-identical across rtf {1,100,1000}, m400 (1 and 8 threads), budget variants; shares within 1–4 points (engine 5/18/24%, gather 71/67/65%); engine-per-game-second falling with rtf (0.041 ms at rtf 1000) with the mechanism verified in code — `resolve_fleet` caps the battle at the next entity's light-delayed deadline (`crates/universe/src/universe.rs:600–631`); thread-immune burst at m400 (engine p99 5.37→5.35 at 8 threads, overflow 126→320, worse); kick-bench memo rates exact (0% / 3.7%); B12/B13/B14-timeout gate state verbatim.
- **Held-out check passed on file times**: predictions.md 08:47:56 vs first sweep JSON 08:48:31, baseline numbers matching — and two predictions failed, honestly reported.
- **Adversarial**: seed 2 holds; unpaced run gives the same digest (stronger than claimed); `--members 4000` is silently clamped to 400 (`xtask/src/universe/mod.rs:32`) — so the headline ≈1,100-body view ceiling is an extrapolation 2.6× beyond the reachable 428 bodies, never observed.
- **Novelty**: H0210 already recorded the gather at 83% of a light frame, and the board already holds the slack skin as the p99 lever; new here is the quantification, the retarded-deadline cost law, and the burst's thread-immunity — a re-ranking, not a 10× move, so not gold.
- Also caught: "engine p99 5.3–6.3 ms in every config" is overstated (5.09 at rtf10, 2.95 at t8-rtf100), and absolute ms ran ~2.5× faster on my pass — only shares, ratios and digests travel between passes.

Gold path named in the check: lift the clamp and measure 1,000–2,000 bodies plus one LOD gather variant — turning the ceiling from extrapolation into a measured ≥10× lever.
