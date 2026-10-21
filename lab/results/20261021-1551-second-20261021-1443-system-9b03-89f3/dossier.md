# Dossier — 20261021-1551-second-20261021-1443-system-9b03-89f3 (lens: second author on 20261021-1443-system-9b03)

## Claim

The checker's named gold experiment is done: the news-fed scan window is wired (`SCAN_NEWSFED=1`, `encounter.rs`: a kept candidate is *proved* identical to a full rebuild's through `(event_time, alive, binding_until)`, no engine write-side instrumentation) and exact — **8/8 flights bit-for-bit digest-neutral**, including the fallback arm and a 20 s horizon — and on the composed desync arm (`BELT_DESYNC=D`, every ship's kick cadence × D, the player's scan cadence held) the walk term falls with the kick dial in work units (30 k burn: 65.55 → 1.20 → 0.46 → 0.32 re-reads/scan at D = 1/8/64, a 205× fall against the shipped walk's flat 65.55), **but the µs cost of capture at shipped candidate counts is radial-bound (65–80 %) and the read-side signature costs ≈ the read it guards (+120–138 ns/id)** — so the walk rides the cadence dial in *work units* (the 10⁹ ledger's scan row), not in today's frame µs; at shipped C the immediate µs lever is the radial query, not the walk.

## Bottleneck

Board macro row (kicks per body) and 1fd7's post-desync ledger: the scan row ("walks 111–311×, cadence-invariant"). 9b03 measured its information (1.2–11.4 % news) and the checker's gold experiment was od 2+od 3 together: wire the exact pre-check, fly the news-fed window on the desync arm, digest-neutral, cost attributed. This run does exactly that. What it deletes if adopted: the per-scan `binding_at` walk (work ∝ news instead of ∝ C — the 10⁹ walk term) and the same-tick duplicate walks (memo hits now paid at signature cost: 48.6 % of burn captures). What it does *not* delete at shipped C: the radial membership query (65–80 % of capture µs, per-scan regardless of the dial).

## Evidence

All numbers from `regen.sh` (≈ 1–2 min: build + 18 deterministic flights; no wall budget inside a frame, so digests compare run to run). Patch: `work/patch.diff` (4 files: `body.rs` `binding_until`, `encounter.rs` news cache + counters, `step.rs` the dial on both laws' planning paths, `examples/scannews2.rs`).

| arm (6 s, rtf 100; digests shipped == newsfed) | scans | near/scan | cands/scan | fallback |
|---|---|---|---|---|
| 30,028 coast D=1 | 58 | 174.3 | 163.2 | 0 |
| 30,028 coast D=64 | 58 | 174.3 | 163.2 | 0 |
| 30,028 burn D=1/8/64 | 747 | 72.7 | 65.6 | 0 |
| 3,028 coast D=1/64 | 58 | 2,547.8 | 287.3 | 48/58 |
| 30,028 coast D=1, 20 s horizon | 193 | 194.4 | 177.1 | 0 |

**8/8 PASS** (digests in `matrix_*.log`, `horizon20_*.log`). Encounters/contacts identical everywhere; scan counts identical across D (the player's cadence is invariant under the dial, as required).

**The dial (work units; shipped walk is flat, news-fed walk falls).**

| arm | shipped re-reads/scan (all D) | newsfed D=1 | D=8 | D=64 | kicks D=1→64 |
|---|---|---|---|---|---|
| 30k burn | 65.55 | 1.20 (0.0165) | 0.46 (0.0063) | **0.32 (0.0045)** | 1,663→412 |
| 30k coast | 163.19 | 36.45 (0.209) | — | 3.67 (0.0211) | 1,318→67 |
| 3k coast (fallback) | 2,536.7 | 86.1 (0.0338) | — | 53.1 (0.0208) | 1,318→67 |

Fractions = re-reads per near id. The fall is bounded below by membership churn — ids entering the window as the player moves, real news, ≈ 0.3–0.6/scan, matching 687c's churn measurement: at D=64 the burn walk is churn-dominated (0.32/scan), i.e. the window pays only for what actually changed or arrived. Memo (duplicate delete): 362–365/747 = 48.6 % of burn captures (9b03: 47 % on the budgeted flight), 22/58 = 38 % on coast D=64.

**Cost attribution (`SCAN_TIME=1`, the author's admitted unflown measurement).**

| arm | shipped capture µs/call (radial) | newsfed µs/call (radial) | walk term shipped → newsfed | net |
|---|---|---|---|---|
| 30k burn (747 scans) | 19.9 (13.0) | 22.9 (12.9) | 6.9 → 0.9 µs | **+3.0 µs/call** |
| 30k coast, 20 s (193) | 92–119 (68–91) | 105–148 (76–97) | 16–28 → ~5 µs | **+13 to +29 µs/call** |

Shipped capture is **radial-bound**: 65 % (burn) to 76 % (coast) of µs is the membership query (the unbounded-list clone + sort inside `radial.candidates`), not the walk. The news path's per-id signature (3 dyn-dispatched trait calls + one scattered slot read) costs ≈ the `binding_at` read it guards: measured overhead +69 to +138 ns/id across runs (shared-machine jitter; two 20 s runs give +13 and +29 µs/call at 194 ids), against a shipped read of ≈ 92–160 ns/id incl. clone and tuple push — a net loss on burn, ≈ −25 % of the walk term on coast at best. The 6 s coast figure (+52 µs) is the one-time 30 k-slot cache build amortized over few scans. The walk's *information* rides the kick dial; today's *frame µs* do not, because the radial term does not.

## Predictions (predictions.md, written before the matrix)

- P1 digest neutrality on every arm — **held, 8/8**.
- P2 walk work falls monotonically with D toward a churn floor; shipped flat — **held** (0.0165→0.0045 burn; 0.209→0.021 coast; shipped 0.90–1.0 at every D). The kill criterion (D=64 ≥ half of D=1) never approached.
- P3 memo ≈ 45–50 % of burn captures — **held** (48.6 %).
- P4 newsfed capture µs < shipped — **wrong, and the run's finding**: the signature check costs ≈ the read (net +69 to +138 ns/id across runs); capture is radial-bound. Reported as the refutation of the µs half at shipped C.

## What would make it wrong

- The exactness proof rests on "current binding changed ⇒ `event_time` changed" (rebind retires; verified in `step.rs`) and on nothing reading the `kick` field in the scan path (verified: `readout`, `cartesian`, `same()`). A future reader of held scans that consults `b.kick` would need it in the signature.
- The dial is a single global factor on *all* ships (belt and locals), not ddeb's per-class floors (16/64/256); the composition measured is "cadence ↓ D× ⇒ scan news ↓", which is the dial's claim, not the census's exact 78× accounting.
- The µs attribution is Linux/x86 (orders of magnitude only); the coast 20 s timing still carries first-touch amortization in the newsfed slot cache (~5 MB at 30 k bodies — itself an adoption cost to note: the cache holds a Binding per ever-candidate body).

Cost of adoption: small and exact (digest-neutral by construction), but it buys *work units*, not today's µs; the µs lever at shipped C is the radial query (the unbounded clone + sort), which the news-fed form leaves untouched. A write-side dirty word beside each rec (one generation number bumped at rebind) would cut the check to one word — the measured condition for the news form to pay in µs at large C.

## The lens

Second author: what the checker named, done; what the composition hides, measured. The elegant unification (one dial for kicks and scans) survives in work units and dies in shipped-C µs — the scan has *two* terms, the walk (kick-coupled, now news-fed, exact) and the radial membership query (per-scan, C-coupled, now the row's µs owner). The 10⁹ ledger's scan row should price them separately. Missed by this lens: the growing-window corner (the player flying into the belt) was not flown — the churn floor here is measured on the plane's own orbits; and ddeb's per-class cadence (not one global D) is wiring on top of the dial, unflown.
