# Slack skin: review receipt

Branch `wt/cx-b-encounter-skin`, base `a838a284a27a6813434362cc2adfde946d2085db`. Uncommitted; never merged. Derivation and API: `crates/encounters/src/skin.rs`. Full detail lines, source hashes, machine-state reads and raw before/after logs: `summary.json` and adjacent files.

The cache retains expanded-radius Binet sections and their unchanged scheduling tubes. A global analytic position bound over the query interval authorizes reuse; final minima use the current tubes at the physical radius. It includes phase-only, shape, orientation and period changes, including empty certificates. Large changes select the original unpadded construction. Discovery still scans current candidates; no wake calendar. This is the existing float research regime, not a canonical integer or integrated engine qualification.

| Named gate / probe | Before | After |
|---|---|---|
| Crate tests | 3 passed, 0 failed | 28 passed, 0 failed; complete command 53.08 s, peak child RSS 326,696,960 bytes |
| `verify a` | 540 truth, 540 matched, 0 missed/false | Identical non-timing counters |
| `verify b` | 1,217 truth, 1,217 matched, 0 missed/false | Identical non-timing counters |
| `verify c` | 6,623 truth, 6,616 matched, 0 missed/false (existing edge margin) | Identical non-timing counters |
| r8 kicked truth construction, epsilon 1e-8..1e-4 | Baseline 0/787 missed | Skin 0/787 missed; 733 independently soundness-checked, 54 additional dense contacts have zero extras vs baseline |

Setups per kick (256 kicks, N=1000, maintenance only), baseline → skin: epsilon 1e-8: 84.5625 → 0; 1e-7: 84.5859 → 5.2891; 1e-6: 84.6680 → 15.8789; 1e-5: 84.6133 → 60.7500; 1e-4: 84.7773 → 84.7773. Cold setups: 1,353 in both paths. At 1e-6, 5.33x maintenance setup reduction (4.25x including cold setup); total evaluations including startup 562,760 → 111,947 (5.03x). No evaluation regression at any swept epsilon. This does not reproduce the lab's 12.6x setup headline.

Controls pass: literal skin misses a phase-only kick; the bounded cache catches it; empty exclusion resets before contact; short reuse/long-period-drift reset; unchanged tubes never age. The full frozen r8 workload/cost/scaling gates were not run. Test counts and probes are component evidence, not independent qualification. The cold aggregate-command timeout and two erroneous new-test setup-count assumptions remain recorded; final corrected suite passes. Swap/thermal reads and RSS-enforcement attempts were denied by the sandbox; max RSS was measured via getrusage.
