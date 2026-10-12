Working...
Check complete — `Grade: gold` written to `lab/results/20261012-0036-quant-115e/check.md`, tree restored to pristine (only `lab/results/` untracked, as found).

**What I verified:**

**Reproduction.** Applied `work/patch.diff`, ran `kick_budget` twice (load 1.96 and 1.20) plus `digest_control` on pristine sources: identical digest `e317b268…a5be`, identical counts (49,619 items), bit-stable stage shares (rebind 70.7 %, force 2.5 %, 11.2× kick tail), Phase B at load 1.20 matching the author's 256k row to 0.4 %. Eleven test suites pass on both pristine and instrumented trees. The pilot the predictions quote regenerates exactly on the pre-existing `cost_split` (49.9/34.8/6.82 µs) — pre-registration is credible; predictions 1,2,5,6,8 held, 3 and 7 failed and were disclosed as failures.

**Adversarial cases (mine).**
1. **10⁶ planned bodies** — the headline extrapolation, unmeasured by the author: 84.7 ms/frame, linear (85.0/85.3/84.7 ns/body at 256k/512k/1M), 5× over the 16.7 ms budget with zero events; peak RSS 1.93 GB.
2. **Far-belt bodies (3–6 AU)**: same tax as near-Home (84.6 vs 85.0 ns/body) — position-independent, "no body class escapes" holds where the author never probed.
3. **Load swing** on the same binary: 59.8 → 85 ns/body (load 1.20 → 1.92); O(N) shape and over-budget verdict invariant. Structurally confirmed: `advance` → `rekey` unconditional, `rekey` requeues every body through the calendar's heap sift.

**Why gold.** Two premises of the shipped plane fall on its own path: the presented frame takes an unbounded O(N) synchronous claim (violating plane.md foundation 7, quoted verbatim in the dossier), and the kick's price is bookkeeping (70.7 % rebind vs 2.7 % force) — killing cheaper-force-math/splits as the lever. Belt arithmetic verified independently (1.7×10³ events/frame, 39 µs/event budget vs 35.5 µs ship item). Novel against HISTORY, docs and examples (`cost_split` was mean-level on one record; H3102 measured only the 28-body default scene).

**Named misses:** Phase-A absolutes in the dossier come from an unsaved lighter-load run (34.0/26.8 µs vs the saved artifact's 37.7/29.4 — shares identical); the ≥10³× rekey deletion is extrapolated, not built (lazy rekey + deadline-spike capacity is the queued one-step build); the tail's internal stage is unresolved.
