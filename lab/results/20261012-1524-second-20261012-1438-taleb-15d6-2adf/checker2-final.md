Working...
**Grade: gold** — written to `check2.md`, tree restored to its pre-check state.

**Reproduction** (clean tree, patch applied by me; `phase.rs`/`tier.rs` verified byte-identical to `wt/cx-b-coorbital-cert` @ adce00d6): every number in the dossier regenerates bit-identically — controls 314/313/5 and 757/14.4%/9; six-scene soundness 0 misses; k p50 48 (tight) vs **3411** (gold-e 10⁶, 3.41×10⁹ visits, 1379/contact, 853× the implied k=4); EoC share 99.5%; scaling exponent 2.04; surgery −3.7%/−10%; tree tier exactly C(10⁵,2) = 4,999,995,000 in 140 s. Peak RSS 211 MB, all commands fast.

**Predictions**: predate all run artifacts; H1/H4/H5 held; H2 missed honestly (order statistic — the miss *is* the finding). One slant flagged: the dossier narrows H3 to "uniform fleets" after its clump failure, though evidence.log discloses both failing ratios (0.006/0.045).

**My adversarials** (own bin, same generators): seed-robust headline (3328/3323 at seeds 73/74); true 10⁶ clumps hit k p50 34,310–68,346 with the `reach·n/TAU` formula off 10–20× — only the two-pointer is a safe guard; soundness holds to e ≈ 0.3 but the cert never refuses (silently pays near-C(n,2)); tree degeneration exact at 10⁴/2×10⁴; gate blindness verified from branch source (`Body::new(1.0, 0.02, 0.0, …)` shared-shape ring asserting k=1).

**Novelty**: the only prior run on this cert was graded *missing* (empty logs, commit 2237a44d); no HISTORY entry covers reach cost or EoC-as-cost-mechanism; the original run used EoC only for sort keys. The run flips the adopted board premise at its own headline and gives the integrator a one-step adoption path (fix stale text, heterogeneous-e + clumped-λ k-gates, budget k in the allocator).
