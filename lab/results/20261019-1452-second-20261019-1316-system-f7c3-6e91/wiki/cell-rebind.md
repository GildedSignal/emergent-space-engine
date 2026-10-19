topic: cell-rebind
status: open
closed-by:
valid-while: crates/space@9ce84b67 + 20261018-2312-system-9eeb's patch (orbit.rs served/from_shared, binding.rs:422) + 20261019-1452's patch (both prior patches + timing counter, servetime, ES_QWEAK guard, memo.rs 0.85); census arms: main@f7c3's patch (print-only rebind hook, beltcensus example)
updated: 20261019-1452-second-20261019-1316-system-f7c3-6e91

# The rebind served from the law's quantized cell, exact key carried

## Current best

**The gold rung is flown and it splits the claim: the gates kill the wiring at 11+11, and the
belt's rebind CPU was never the wall (20261019-1452-second-…-6e91; both prior patches applied,
one wall-clock instrument on both arms).** With the served rebind wired (`ES_QMEMO=1`),
**B13 fails: 46/64 flybys within 1e-2 against the exact arm's 60/64, worst ΔE 5.93e-1 (28× the
exact arm, 59× the band), deterministic across solo, loaded and strong-branch-guarded runs** —
the exact arm's own red (60/64, worst 2.12e-2) is bit-identical on a clean stashed tree, i.e.
this box's pre-existing libm condition (B12's disease, a8cd), so the −14 draws are the serving
signal. Per-draw: 20 draws outside 1% spread over q = 2.3–44.5 R_p, all alive, and **ΔE ≡ ΔL**
— a common-mode phase offset through the encounter window; the ≤2⁻¹¹ period shift accumulates
along the ~300–800-kick approach. The strong-branch exact guard (od 4) does not rescue it
(47/64: the failing keys are weak-branch). B12 reads text-identical `worst err inf` both arms
(broken instrument here); B17 times out at the frozen 60 s limit both arms, solo. **The
measured constants replace the composition:** the belt's own exact compile is **4.95 µs**
(microbench on its 99,699 genesis keys; live stream 4.87–5.71 µs/call) — not the cited 104 µs
plane-FIT figure — and the served hit **0.641 µs** (7.8×; live 0.759–0.769 µs/call, hits
99.1–99.6%); belt rebind rate measured 3.04–3.36e-5/(body·game-s); **10⁹ row: 0.15–0.17 cores
compiled → 0.019–0.022 cores served** — f7c3's "3.7–4.5 compiled cores" priced the belt at the
plane scene's compile (20×); the CPU deletion is 7.8×, not ~100×. **The belt stream under
serving is the exact arm's stream** (belt recurrence 0.9510→0.9509, cells 1,425→1,429, belt
rebinds 29,097 identical at 10⁴; 0.9913→0.9917 at 10⁵, cells +0.3%; checker, seed 2:
0.9512→0.9512, cells 1,420→1,419 — whole-plane kick counts are wall-budget-limited, not a
bit-identical invariant: the author's 167,262/167,262 read 166,985/167,352 on regen), so
f7c3's O(1) standing-memory core survives
untouched; the memo.rs guard recalibrated 0.9→0.85 (passes both arms; belt-served 0.95–0.99).
Successors: serve the belt's keys only (a population B13 never flies), or step the width
ladder — but if the encounter amplification is linear, B13's band needs ~6 fraction bits
(11→17); unmeasured (20261019-1452-second-…-6e91).

[Checker 2, 20261019 (grade: gold): clean-tree re-apply reproduced everything decisive
bit-identically (B13 60/64 → 46/64 → 47/64 QWEAK, controls green). Four attacks: seed 3 belt
(recurrence 0.9516→0.9510, cells +1.2% — serving still does not move the belt stream);
microbench at 10⁴ (compile 4.84 µs, hit 0.728 — the 4.95 µs and the 104 µs rebuttal hold at
both scales); a width probe outside the flown range — 14+14 (8× finer) reads 53/64, worst
9.31e-2, a 6.4× drop for 8× width, so the error is width-limited and near-linear and od 2's
11→17 estimate is confirmed in direction; determinism re-run identical. Two notes: "belt
rebinds 29,097 identical" is structural (9,699 bodies × 3 fires), not bit-identity — the
recurrence/cells deltas carry the real signal; and the per-draw errors do not correlate with
kick count (382 kicks → 4.5e-1 vs 844 → 1.8e-2): the amplification is encounter-phase
alignment, not accumulation length.]

**The belt's census is flown and the cells saturate: the standing set is O(1) in N — the
f7c3/ef8c record below, now with the CPU half re-priced by 20261019-1452 (4.95 µs compile,
0.641 µs serve, 7.8×).** [f7c3, live stream: birth cells 1,095 (2,699) → 1,831 (299,699),
∝ N^0.11; stream = birth cells exactly over 2–3.2 intervals; checker: 2,141 cells at 10⁷,
2.03 MB, 0.20 B/body, β = 0.083; ceiling 4,096 cells draw-bounded (one gap octave occupied,
second opens ~3×10⁶). ef8c, key-space: 1,731 cells at 10⁵ / 1,960 at 10⁶, serve error
4.6e-4/1.6e-4, standing tables 644 B/body → 1.63 MB at 10⁶, and the plane's B9 knot
invariance does NOT transfer — 0.80–0.82% of belt members sit on a knot-count boundary, the
knot-guard hazard.]

## Refuted

- **"Adoptable behind the gates" (9eeb/f7c3's adoption half, at 11+11): refuted at B13** —
  46/64 within 1e-2, worst ΔE 5.93e-1, deterministic; the exact arm's own 60/64 red is this
  box's libm (clean-tree control bit-identical), so the −14-draw delta is the law change
  (20261019-1452-second-…-6e91). The belt-scoped memory claim is NOT refuted: the served belt
  stream is the exact stream.
- **The strong-branch exact serve as the B13 rescue (od 4's guard): refuted** — with
  `ES_QWEAK=1` (weak branch only served) B13 reads 47/64, worst 5.92e-1: the failing plane
  keys are weak-branch (20261019-1452-second-…-6e91).
- "The plane's B9 knot invariance transfers to the belt": it does not — 0.80–0.82% of belt
  members land in a cell whose representative compiles a different knot count, constant
  across 10⁴–10⁶ and seeds (20261019-1316-components-ef8c).
- The write-back form (the orbit's key snapped to the cell): law.md "re-rounds at every kick, a
  random walk (principle 13)" — the shipped `QuantizedMemo::get` returns `from_shape(decode())`;
  the carried form is the one measured (lineage: r2's exact increments, the 5 October
  correction that an exact memo never hits on distinct kicks).
- "The belt census is the open measurement / the amortization win's memory half is unproven at
  scale": measured — cells saturate at O(1), the stream adds ~nothing over 2–3.2 intervals
  (20261019-1316-system-f7c3); the FIT half of 9eeb's correction stands (2.8× on the plane
  scene, and 7.8× on the belt's own keys at 20261019-1452).

## Open directions

1. **The adoption shape, after the gate:** plane-wide serving at 11+11 is dead (B13); the
   surviving shapes are (a) **belt-scoped serving** — the served belt stream is the exact
   stream (belt rebinds 29,097 identical at 10⁴, both seeds; whole-plane kicks are
   wall-budget-limited), and B13 never flies belt keys — or (b) the width ladder
   re-flown against B13 first. efd4's intern + refcount keyed by cell; eviction optional
   (4,096 ceiling ≈ 3.4 MB).
2. **The width ladder, now with its true driver:** the encounter, not the cycle, sets the
   width — a 2⁻¹¹ period shift amplifies 59× through an assist (ΔE ≡ ΔL, common-mode phase).
   If linear, B13's band needs ~6 fraction bits (11→17); if superlinear near grazing draws,
   no width fixes it. Measure the amplification vs width before stepping (20261019-1452).
3. Compose with Carlson wiring (kick-jet open 1) for the cold builds; at the belt the
   cold-build share is ≤ 1.1% (f7c3) — Carlson matters only for the locals.
4. ~~The strong-branch exact serve as a guard~~ **refuted as the B13 rescue** (the failing
   keys are weak-branch, 20261019-1452); the resonance guard question (a population
   straddling a mean-motion boundary) stays unmeasured.
5. Turnover (f7c3's successor): a stirred or burning belt's cold-build turnover is unmeasured
   past 3 fires (≈0 measured); if turnover approaches the fire rate, CPU returns to the
   compile ceiling — now known to be 0.15–0.17 cores at 10⁹, not ~4 (20261019-1452).

## Contradictions

- law.md's "Not adopted: a quantized (E, L) memo for kicks" (the write-back reading) vs this
  page's carried form — resolved by construction and measurement (exact recurrence 0.000,
  hashes stable), but the law text is its owner's to re-word.

## Runs
- 20261018-2312-system-9eeb (silver): the carried cell serves 96.7% of the plane's rebinds —
- 20261019-1316-components-ef8c (silver): the belt census — 1,731/1,960 cells at
- 20261019-1316-system-f7c3 (silver): the belt census — cells saturate (1,095→1,831 over
- 20261019-1452-second-20261019-1316-system-f7c3-6e91 (this run): the gold rung — B13 kills
  the 11+11 wiring (46/64, worst 5.93e-1, ΔE≡ΔL phase mode); the belt's compile is 4.95 µs
  not 104 (10⁹: 0.16→0.02 cores, 7.8×); the served belt stream is the exact stream; guard 0.85.
