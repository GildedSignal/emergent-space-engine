Working...
**Grade: silver** — written to `lab/results/20261015-1926-spacex-8b89/check2.md`.

**What I did (blind to check.md):**
- **Reproduced**: applied `work/patch.diff` to clean base 9626abf8 myself, built, froze my own binary; runner's regen 16/16 flights ALL IDENTITY; verified the patched `digest()` preserves base field order (so the ctl anchors — incl. `5caeb1b6…`, f55d's published belt digest — are genuinely the shipped digests); cross-checked every dossier number against regen.log.
- **Three adversarial cases, each outside the author's domain, all bit-identical**: N=3×10⁴ coast (3× the max flown; standing 20.4 MB → 1.7 kB, rss 171 → 80 MB), seed 7, and a pure stargraze stream never flown pure (319 passages → 2.3 kB standing, rss 796 → 16 MB, 49×, plunges 0). Event counters (kicks/opens/boundaries) identical on every arm.
- **Tests**: the five test files the patch touches pass; **predictions** predate the decisive run (P1/P2/P3/P5 held, P4 half-held, honestly reported).
- **Page**: faithful, conflict resolved by keeping both entries, no rewording — no corrections needed.

**Why not gold**: the adoptable configuration (ALL + `ES_RETAIN_HOT`) is only asserted to compose, never flown; bare ALL's wall tax is 3.1–6.1× ctl and does not diminish with N, so it's unshippable alone; no ≥10⁵ rung flight. One experiment closes it: the composed arm at 10⁵ at the measured knee — identity + kick-floor promotions + the memory win surviving.

Tree restored to clean (`git apply -R` verified, only untracked `lab/results/` remains); nothing else in the run folder touched; no commits.
