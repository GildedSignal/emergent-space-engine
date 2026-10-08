Working...
All green: 3/3 crate tests pass, batteries archived, patch saved (`work.patch`, 297 lines), binaries under 5 MB, no git operations. The run is complete.

**Claim:** per-pair encounter-window setup in `crates/encounters` drops 1.4–4.3× (9.2→3.2 µs/pair at n=10⁴; setup evals 20.3→0.05) with every encounter still found on all 14 verify belts (missed=0, identical hit rates), because the merged-arc numeric crawl for near-identical orbits is replaced by a closed-form superset window derived from the encounter's necessary angular condition — while long-horizon (≥1000-orbit) steady state at small n pays up to 1.6× more events per encounter, with break-even at ~1700-orbit certificate lifetimes.
