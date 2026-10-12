Working...
Check complete. `check.md` written to the run folder; nothing else touched, no stray processes, no git operations.

## Verdict: **lead** — the headline is an instrument artifact

**What reproduced** (in `/tmp/chk2b28`, shipped `belt.py`): formations bit-exactly (per-seed `[332,222,61]`, `[91,303,72]`, `[5,5,4]`, `[4,3,3]`); control enc=3552 and the mu=1e-9 run enc=12234 **exactly**; the A-table within 1.3% (sign-flip 1.44→1.34 / 0.98→0.67 / 0.95→0.36; e² growth; no cascade, maxwin/first ≤ 1.02).

**What broke:**

1. **Zeno re-fire artifact (decisive).** With pair-ids logged, the mu=1e-9 run's 12234 encounters sit on 526 distinct pairs (control: 555 on 551) — the top pair "encounters" 298 times inside **0.2 orbits** (median gap 0.001 orbit). 96% of encounters are ≥10-repeat re-fires. `conj_time` at t_enc is ill-conditioned (λi≈λj); a weak kick leaves the next "conjunction" microseconds away, resolving one deep approach into hundreds of impulses — exactly what the adopted m-meso-motion silver (one exact pair event per close encounter) exists to prevent. Burst-deduplicated, the real rate is **173 events vs 555 control — a mild quench, not a 17.8× unlock**. The weak formation is the same storm (332 enc on 4 pairs); the strong formation is clean (gaps ~682 orbits), so the "40× over-count" compares an inflated arm against a clean one.
2. **Record integrity.** Stored A/B JSONs are not regenerable (pairs=130816 complete-graph vs shipped 128627; belt.py's mtime falls between the B and C runs — an undisclosed mid-run pair-criterion edit). Minor: "kicks 2e-8" is actually ~1e-5 (median |Δe| 1.44e-5); the "machine noise doesn't unlock" control is vacuous (nokick never re-derives elements).

**What survives:** the R sign-flip and no-cascade results at mu≥3e-8 are measured on clean events (max 3 repeats) and reproduce — real, novel vs HISTORY, but far from the run's central claim. The redeeming experiment is named in check.md: re-run with a changeover/dedup instrument, pre-registered.
