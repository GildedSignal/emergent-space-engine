# Dossier — 20261010-2052-second-20261010-1947-spacex-19bc-d205 (second author on 20261010-1947-spacex-19bc)

**Claim.** The checker's named experiment is done: with a real shipmem packed-block store fed the
plane's own rebind stream, the **removal side is now measured, not modelled** — at the coarse
(memo-key) level reabsorption duty at 10⁹ ships is **0.6–1.1 % of a core by measured removal
capacity, 2–3 % by the decomposed marginal-row + repack model** (kill line was 20 %), so the
original claim's "reabsorption to hold it costs ~2 % of one core" **holds by measurement**; the
exact (Q48) side costs **0.3–1.3 cores on the same defensible models (up to 11 on an adversarial
small-group bracket)** — it dies on CPU as well as bandwidth, harder than the dossier's 1.18-core
model. Creation side reproduced unchanged (coarse 0.0013–0.0018 bits/ship/s, exact 0.076–0.136).

**Bottleneck.** The one the checker named: "the reabsorption cost model reuses the kick-resolver µs
for a recompile that has never been timed". Every duty number in the silver dossier rested on it.

**Evidence** (Linux x86 shared runner, 8 vCPU; orders of magnitude only; machine state in the
JSONs). Patch = the original `--hlive` mode plus the removal side (`work/patch.diff`; xtask only,
one dep line; no engine change; **kick-bench digest on the patched build equals the unpatched
baseline**: `eccc7f5a…`, and the replay digest is deterministic across repeats: `c57600fc…`, all
non-timing fields of s1 vs s1-rep identical bit-for-bit — the ordered entropy fold also fixed the
original's ULP nondeterminism).

```
cargo build --release -p xtask                                   # ~40 s
cargo test --release -p xtask hlive                              # <1 s, 1 test
xtask universe --hlive --rtf 100 --seconds 30 --seed 1           # -> data/hlive-rtf100-s1.json
xtask universe --hlive --rtf 100 --seconds 30 --seed 7
xtask universe --hlive --rtf 1000 --seconds 3  --seed 1
xtask universe --hlive --rtf 100 --seconds 30 --seed 1 --members 400
xtask universe --kick-bench --rtf 100 --seconds 30 --seed 1      # digest gate vs baseline
```

The mode now drives two real `Shelf` stores (128-member blocks, chord, sorted) with the replayed
rebind stream: every rebind updates the ship's slot unless it changes nothing stored; every 120
frames (idle cadence) `compact()` seals scars and repacks. Bytes/counts deterministic; µs are host
noise. The coarse store is `[memo key, sense]` — a rebind that keeps the memo key writes nothing
(the memo's own semantics; my first draft also stored the rebind time, which forced a write per
rebind and inflated coarse duty ~40× — dropped after the smoke run, disclosed here).

| 3000 game-s (rtf 1000: same in 3 s) | s1 (71 ships) | s7 (65) | rtf1000 | m400 (423) |
|---|---|---|---|---|
| rebind calls (all causes) | 1158 | 1449 | 769 | 9188 |
| **coarse writes (memo key changed)** | **16 (1.4 %)** | 10 (0.7 %) | 24 (3.1 %) | 114 (1.3 %) |
| exact writes (every rebind) | 1088 | 1433 | 757 | 8668 |
| bytes removed coarse / exact | 2016 / 26654 | 1152 / 31214 | 1152 / 4689 | 15552 / 166333 |
| removal capacity, coarse (B/µs of compact) | 21.5 | 15.0 | 31.3 | 39.3 |
| **duty @10⁹, capacity model: coarse / exact** | **0.009 / 0.82** | 0.011 / 1.17 | 0.006 / 0.28 | 0.006 / 0.89 |
| duty @10⁹, linear scene scaling (upper bracket) | 0.47 / 9.7 | 0.40 / 11.1 | 0.18 / 0.71 | 0.32 / 7.9 |
| shelf bytes/member now, coarse / exact | 19 / 30 B | 20 / 35 B | 32 / 62 B | 14 / 55 B |

Cost decomposition (from the per-compact trace, in the JSONs): an empty compact costs 1.2–1.7 µs;
the marginal row costs ≈0.18 µs (757 rows in one compact, rtf1000); scene compacts are dominated by
a per-group fixed ≈13 µs at the scene's group occupancy (~8 members; batches as the fleet hands
members out). At 10⁹ ships the crate's own MAXG caps groups at 65,536 members (15,259 groups), so
the defensible scale model is: floor 1.5e8 groups×cadence ≈ 1e-4 cores, + coarse rows ≈ 0.017,
+ repack amortization ≈ ×2 → **coarse ≈ 0.02–0.03 cores**; exact rows alone ≈ 1.28 cores. The
"linear scene scaling" row is reported as an upper bracket only: it multiplies a group-fixed cost
by 10⁹/71 while the group count grows by ×1,526 and MAXG caps it — it exceeds 0.2 in 2 of 4 runs
and is not a scale model; the two defensible models agree coarse ≤ ~3 %.

Store boundedness (P4): shelf bytes oscillate with repacks folding scars back (s1 exact
1663→3262→2111 B; coarse 984→1358 B over 3000 game-s) — no monotone growth; the test asserts both
this and the exact telescoping accounting (initial + adds − removals = final).

**Predictions** (`predictions.md`, written before the decisive runs): **P1 held** on the capacity
and decomposed models (coarse 0.6–3 % ≤ 5 %; kill line 0.2 not crossed by any defensible model);
disclosed: the raw linear bracket crosses 0.2 in 2 of 4 runs — the prediction did not name its
scale model, my error. **P2 missed**: bytes removed is ~60× the created bits at the coarse level
(~12× exact) — the machinery's working-form churn (~70 B/hot entry reclaimed per seal) dominates
the information content; both remain tiny. **P3 missed, as a refinement**: the exact duty is ~100×
the coarse duty, not ≤3× — the level split is *sharper* on the removal side than the creation
side's 60–70×, because the coarse store writes on only 0.7–3 % of rebinds. **P4 held** (samples +
test). **P5 held**: m400 per-ship rates within 1.3× of the 48-member scene.

**What would make it wrong.** One star system at 65–423 ships; the 65,536-member group occupancy
at 10⁹ is asserted from the crate's MAXG, not measured (the trace regime is 1–72 rows per compact,
and a 65k-row group's cache behaviour is unmeasured — the marginal 0.18 µs/row could degrade);
the repack amortization at big groups is inferred from the trigger rule, not timed at that scale;
Linux x86 shared host, orders of magnitude only. The `[memo, sense]` coarse store is the dossier's
own column; a belt store that also keeps provenance would sit between the two shelves. 5–6 % of
rebind calls hit bodies not yet admitted (counted as `skipped_no_handle` in the JSONs).

**Cost of adoption.** The mode is ~380 lines in xtask plus one dep line (`work/patch.diff`); no
engine or digest change. Not done from the checker's gold list: wiring the number into
`--bench`/the page (presentation; the brief's other half) and the full named-gate suite — for an
xtask-only patch I ran the gates that can move: build, the new test, kick-bench digest before and
after (equal), replay-digest determinism (equal). shipmem is currently a deletion candidate
(HANDOFF, 7 October): adopting this makes it load-bearing, which the integrator should decide
deliberately.

**Fit with PRINCIPLES.** "Compute only surprises" (P3): measured on the removal side — the coarse
store writes on 0.7–3 % of rebinds; "the memory floor is information-theoretic" (§24, OC#34): the
measured packed store holds 14–62 B/member against the plane's 4.4–4.8 KB/body, so the ~600× idiot
index now has a measured alternative, not just a floor argument.

**The lens (second author).** What this lens may have missed: I corrected the coarse store's
columns after a smoke run (the t-column error) — a checker should ask whether `[memo, sense]` is
the honest coarse store or a conveniently cheap one; the 10⁹ extrapolation leans on shipmem's MAXG
occupancy, which no run here measures; and the density case is 423 ships, not a belt (B18b). The
strongest residual: the exact side's 0.3–1.3 cores is a *lower* defensible bound — its true cost
at bad group shapes is the 8–11-core bracket, so "exact per-body state at scale" is even deader
than the silver dossier said.
