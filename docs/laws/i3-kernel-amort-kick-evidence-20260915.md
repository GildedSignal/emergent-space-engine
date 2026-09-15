# I3 kernel amortization + kick path — 15 September 2026

Not canonical gravity. `CANONICAL_GRAVITY_ACCEPTANCE = diagnostic-only`. `production_law` null.
Not I3 exit. Not I4–I6. Nested Charge `ledger_total` is the denominator.
Gates declared before this slice’s runs: `KERNEL_POS_BAND = KERNEL_A_BAND = KERNEL_KICK_POS_BAND = KERNEL_KICK_A_BAND = 0.05`. None were widened. Frozen H0134 evidence is unchanged.

## What ran

Worktree `/private/tmp/emergent-full-engine-integration`, branch `codex/full-engine-integration`, parent `954a8c7`. Target `/Users/julien_laurent/.cache/emergent-space/full-engine-integration-target`. `CARGO_BUILD_JOBS=1`, `--offline --locked`, `--test-threads=1`.

| Command | Result |
|---|---|
| `cargo test -p emergent-law-lab --lib i3_ -- --test-threads=1` | PASS (10) |
| `cargo test -p emergent-law-lab --lib coupled_ -- --test-threads=1` | PASS (54) |

## 1. Quiet amortization (circular `a=4`)

Construction still collocates only `[0, KERNEL_MEMORY]`. Nested split:

| H | Bootstrap | Jacobian | Advance | Cert | Total | Collocation | Δx | Δa | Rank | Mem | Fill |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 8 | 870 | 180 | **84** | 1 | **1137** | **2300** | 0.00403 | 0.00115 | 4 | 6 | 144 |
| 12 | 870 | 180 | **132** | 1 | **1185** | **3176** | 0.00954 | 0.00258 | 4 | 6 | 144 |

Rank / Jacobian `n` / memory / fill-in stay bounded. Advance is what grows with H (84→132). Bootstrap is **flat** and still **73% of the H=12 kernel ledger** — setup is not invented away. The skip is that collocation grew 2300→3176 while kernel stayed ~1.2k.

**KEEP** the quiet domain at H=8 and H=12 under the predeclared 0.05 gates.

## 2. Kick path (explicit)

Kernel through quiet prefix, apply kick, resume kernel march. Remainder vs kicked collocation. Recouple-suffix and prefix-repair are fallbacks, not guessed events.

| Case | Path | Ledger vs collocation | Δx | Result |
|---|---|---|---|---|
| Weak Δv=0.02 at t=2, H=8 | kernel-resume | **1139** vs **2525** | 0.00402 | **KEEP** |
| Strong `laboratory_kick` Δv=0.125 at t=1.25, H=8 | kernel-resume | 1149 vs 2556 | **0.216 > 0.05** | **REJECT**; do not mint |
| Prefix + recouple-suffix (weak, after a first-pass covering miss) | recouple | 2932 vs 2525 | — | **REJECT** (more expensive) |
| Prefix-repair of quiet collocation, weak H=8 | repair | 2257 vs 2525 | — | cheaper than recouple; not the kernel skip |
| Close-entrant (3-body) | refuse | recouple 2635 | — | **fallback** |
| Distant tide | refuse n-body | — | — | **fallback** |

## I3 exit

Not proven. Quiet H=12 and weak-kick H=8 are movement: matched GEM, cheaper nested cost, bounded operator. Remaining holes: bootstrap still dominates kernel setup; strong kicks miss 0.05; close-entrant/n-body still recouple; interval-wide GEM authority missing.

## Next

Do not start I4–I6. Discriminating leftover: a kick/entrant representation that matches GEM after a strong Δv without paying full collocation, or admit I3 cannot skip sequential GEM on noisy/close-entrant domains.
