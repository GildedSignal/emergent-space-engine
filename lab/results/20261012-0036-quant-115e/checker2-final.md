Working...
Verdict written to `check2.md`. Summary of the check:

**Grade: gold.**

**Reproduced from a clean tree** (patch applied myself): digest `e317b268…a5be` identical pristine vs instrumented, 11/11 test suites pass patched, rebind 70.6% (claim 70.7), Kick(0) p50 33.8 µs / p99.9 379.4 (claim 34.0 / 379), ladder 42–60 ns/body, inert control = planned cost. Mechanism verified in source: `rekey()` at universe.rs:493 is an unconditional O(N) per-body heap `set` inside `advance()`, paid by every presented frame; planets are root-doll sources so all ships are planned.

**Adversarial cases (mine):**
- **1,000,028 planned bodies measured directly:** 58.4 ms/frame, 99.98% rekey, zero events — the author's largest extrapolation (60–75 ms) holds at its floor; 3.5× the 16.7 ms budget.
- **Deadline-density spike** (author's named miss, all one phase) and **eccentric spread**: 58–60 ns/body — no amplification, distribution-insensitive.
- **Load counter:** my phase A at load 0.54 reproduced p99.9 = 379.4 exactly — the 11× tail is real, not machine noise.

**Predictions:** pre-registered (mtimes 00:42 vs bench 01:01); 6/8 held, the 2 failures conservative (tail worse, tax broader) and honestly reported.

**Flaws found (flagged, none load-bearing):** the dossier's "(load was 0.9–1.0)" is contradicted by its own bench header (load 2.07); tail stage unattributed; the lazy-rekey bit-safety argument covers settles but not per-frame presented horizons; 1M bodies = 1.88 GB live, so storage is the next wall on the same road.

Tree restored to pristine (`?? lab/results/` only); nothing else in the run folder touched; no git operations run.
