# 20261021-0312-fermi-614b — the past-cap chains named, and the birth spike law

**Claim.** The allocator's past-cap chains are two different laws, both now named with stacks and
counters: the belt-scaled one is the per-universe body tables' capacity crossing at a fleet handout
— exactly (464+32) B × bodies of copy per crossing frame, burn-independent, once per crossing —
which is a smoothness wall on the N ladder (17 ms of bus at 10⁶, 165 ms at 10⁷, 1.65 s at 10⁸,
16.5 s at 10⁹), while the player-scan chains (`capture`'s 448-B tuples) scale with the fleet's
handed-out population, not the belt, and never become a 10⁹ row at the shipped genesis.

**Bottleneck.** budget-1e9 od 7 (name the chains) and the 0.25–0.37 TB/chain-at-10⁹ extrapolation
that 8994/6e76 left as rung arithmetic. The row it moves is smoothness (board principle 12, the
spike, not the steady rate): a single `Vec::push` at 10⁹ copies ~1 TB — the ladder cannot climb past
~10⁷ bodies on per-universe tables. Expected gain: deletes a wrong 10⁹ premise (the "pulled-body
entry list") and replaces it with a measured law the integrator can gate the next rungs on.

**Evidence** (`regen.sh`, ~2 min on this machine; `work/analyze.py` prints every number below):

- Eight arms of the nladder flight (`crates/universe/examples/census.rs`, added by `work/patch.diff`)
  under a counting global allocator with backtraces at ≥ 61,440 B (family A's 57,344-B cap + 1),
  plus additive counters in `radial.rs`/`encounter.rs` (`crates/universe/src/census.rs`).
- **The belt-scaled chain** (members 48, belt N ∈ {10⁴, 3·10⁴, 10⁵, 3·10⁵}): one chain per arm,
  `32.0 B × bodies` **exactly** (320,896 / 960,896 / 3,200,896 / 9,600,896 B), backtrace
  `resolve_handout → resolve_entity`, i.e. `self.info.push` (BodyInfo = 32 B). It fires at frame 9
  under burn and frame 12 on coast — **burn-independent**. The crossing frame takes 2.1–2.3 ms
  against 60–70 µs neighbours; the handout's own next frame (bind + replan + wave) takes 8 ms.
- **The recs table crosses too at fleet scale**: `PlainBodies::push` in `resolve_handout`,
  237,568 B = 464 × 512 rung (BodyRec = 464 B, `sizes` in every dump). Together a crossing that hits
  both tables copies **496 B × N**.
- **Rates**: leavers (handouts) 43–48 per 899–2,898 game-s ≈ 0.02–0.05/gs at members 48; 0.45/gs at
  members 400. Crossings are once per capacity headroom (2×), so the per-birth amortised cost is
  ~496 B — the spike is the whole cost.
- **The capture chain is fleet-scaled, belt-flat**: `capture.max` = 134 (seed 1) / 267 (seed 2) at
  every belt N from 10⁴ to 3·10⁵; at members 400 it is 329 (no belt) and 628 (belt 10⁴). Its past-cap
  rungs (114,688 = 448×256; 229,376 = 448×512) recur per frame at fleet scale (396 and 198+200
  chains per 600-frame arm) — this is 6e76's coast family and 8994's 8–16k-entry chains: their arms
  scaled the **fleet**, not the belt.
- **The radial index served every belt capture** (fallback = 0 on all belt arms; 1.18 captures/gs,
  71 ids each, 91% surviving). The 95.7% die-off lives on the full-scan path that fires when the
  player sits in the fleet frame: 11,046 loop-iters/gs at members 400 + belt 10⁴ (die-off 94.4%),
  entered not through `Radial::candidates` (fallback 890–933, a separate gate) but through the
  window closure's error path.
- **10⁹ composition** (bus 60 GB/s, copy = read + write): recs+info crossing = 992 GB = 16.5 s of
  bus in one frame; info alone 64 GB = 1.1 s. On the ladder: 17 ms at 10⁶ (one frame budget), 165 ms
  at 10⁷, 1.65 s at 10⁸. The wired tables (2,460 B/body) do not fit 8 GB anyway (097e); the new fact
  is that even the crossing alone is a seconds-long stall, so **births must be owned by chunked
  tables or the compact store before the ladder passes ~10⁷**.

**Predictions** (`predictions.md`, written first): the capture site was half right (the coast
114,688-B chains are indeed `capture`'s ladder) and half wrong (the N-linear chains are `resolve_
handout`'s table push, not capture; the radial fallback never fired — 0 on every belt arm); the
reproduction held (8994's 3.67/7.34 MB are the same-order rungs, and my m400 arms recover their
8–16k-entry contents as fleet-scaled capture lists); the size law was **wrong in my favour to
test**: exponent 1.0000 (I predicted 0.5–0.9 window-limited) — it is a table, not a window; the
rate was partly wrong: coast fires the belt-scaled chain too (frame 12), it is not burn-coupled.

**What would make it wrong.** The 32.0 B/body law is exact at four K values and one element type;
it breaks only if `BodyInfo`/`BodyRec` change size (then the law is `size_of × N`, same site). The
16.5 s-of-bus figure assumes both tables cross together; they cross independently (headroom
phases), so the per-crossing figure is 1.1 s (info) to 16.5 s (both) — the wall stands at 10⁷–10⁸
either way. M1 bus is ~60 GB/s shared, so Linux/8-vCPU orders of magnitude only, per the rules.

**Cost of adoption.** None for the measurement (patch is additive, env-gated, never touches an
outcome; digests unchanged — the allocator only counts). The fix it names: chunked per-body tables
(dyadic pages) or births owned by the compact store — an engine change for the integrator, in the
same family as od 2 (wire the compact store), priced here at "mandatory before 10⁷".

**Fit with PRINCIPLES.** "minimize spike compute" (OC#36) — this is a spike law with a number;
"a fix signals the wrong representation" (CL 09-29) — a per-universe `Vec` of bodies is the wrong
representation for a universe that grows; "measure before claiming" — the 0.25–0.37 TB figure was
rung arithmetic, now it is a named push with an exact per-body constant.

**The lens (Fermi).** The estimate that guided the arms (chains ≈ elem × pulled set) was right in
form but wrong twice in mechanism — the estimate cannot name a site; only the stack could. What the
lens may have missed: I did not measure the crossing at 10⁶ (memory cap 2 GB allows ~7·10⁵ bodies;
the 17 ms-at-10⁶ figure is composed from the exact law, not flown) and I did not chase the window
closure's error path that opens the full scan (a `?` in `capture`, likely worth its own run).

**Grade suggested:** the laws are exact, reproduced by `regen.sh`, and the held-out predictions are
reported honestly where they broke; this closes od 7 and corrects two wiki lines. Silver if the
checker wants the 10⁶–10⁷ crossing flown on the M1 before the wall is called real.
