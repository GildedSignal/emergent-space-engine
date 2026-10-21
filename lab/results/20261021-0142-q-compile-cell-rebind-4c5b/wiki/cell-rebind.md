topic: cell-rebind
status: open
closed-by:
valid-while: crates/space@9ce84b67 + 20261018-2312-system-9eeb's patch (orbit.rs served/from_shared, binding.rs:422) + 20261019-1452's patch (both prior patches + timing counter, servetime, ES_QWEAK guard, memo.rs 0.85); census arms: main@f7c3's patch (print-only rebind hook, beltcensus example)
updated: 20261021-0142-q-compile-cell-rebind-4c5b

# The rebind served from the law's quantized cell, exact key carried

## Current best

**Standing shapes are O(1) in N and the served belt stream is the exact stream; adoption is belt-scoped, because at 11+11 the plane-wide serve fails B13 (6e91 gold; f7c3, ef8c, 9eeb silver).**
Census, live stream (f7c3): standing cells 1,095 at 2,699 bodies → 1,831 at 299,699 (∝ N^0.11; the stream equals birth cells over 2–3.2 intervals); checker: 2,141 cells at 10⁷ (2.03 MB, 0.20 B/body); hard ceiling 2 exponent × 2,048 = 4,096 cells ≈ 3.4 MB at any N.
Census, key-space (ef8c): 1,731 cells at 10⁵ / 1,960 at 10⁶, serve error 4.6e-4 / 1.6e-4, standing tables 644 B/body → 1.63 MB at 10⁶.
Rebind CPU on the belt's own keys (6e91; checker 2 at 10⁴: compile 4.84 µs, hit 0.728): exact compile 4.95 µs (99,699 genesis keys; live 4.87–5.71), served hit 0.641 µs (live 0.759–0.769; hits 99.1–99.6%) = 7.8×; belt rebind rate 3.04–3.36e-5/(body·game-s).
10⁹ row (6e91, supersedes f7c3's composition): 0.15–0.17 cores compiled → 0.019–0.022 served; f7c3's "3.7–4.5 compiled cores" priced the belt at the plane scene's 104 µs compile (20×) — its served estimate (~0.02–0.04 cores) was right; the deletion is 7.8×, not ~100×.
The gold rung (6e91): plane-wide serving at 11+11 fails B13 — 46/64 flybys within 1e-2 vs the exact arm's 60/64 (its own worst 2.12e-2 is this box's pre-existing libm red, B12's disease a8cd), worst ΔE 5.93e-1 (59× the band, 28× the exact arm), deterministic solo/loaded/guarded; the −14 draws are the serving signal.
Mechanism (6e91, checker 2): ΔE ≡ ΔL, a common-mode phase offset through the encounter window — a ≤2⁻¹¹ period shift amplifies along the ~300–800-kick approach; 20 draws outside 1% over q = 2.3–44.5 R_p, all alive; errors do not correlate with kick count (382 → 4.5e-1 vs 844 → 1.8e-2): encounter-phase alignment, not accumulation length.
Width-limited, near-linear (checker 2, gold): 14+14 (8× finer) reads 53/64, worst 9.31e-2 — a 6.4× drop for 8× width; if linear, B13's band needs ~6 fraction bits (11→17).
The served belt stream is the exact stream (6e91; seeds 2 and 3 agree within the same noise): belt recurrence 0.9510→0.9509, cells 1,425→1,429; the 29,097 identical belt rebinds are structural (9,699 × 3 fires), not bit-identity; whole-plane kick counts are wall-budget-limited, not an invariant.
Knot hazard (ef8c): the plane's B9 knot invariance does not transfer — 0.80–0.82% of belt members sit on a knot-count boundary, constant across 10⁴–10⁶ and seeds; serving needs a knot guard (compile on mismatch ≈ 0.8% builds).
The wiring as measured (9eeb; its adoption half superseded by 6e91): the carried cell serves 96.7% of the plane's rebinds, FIT −64% (2.8×), gates hold on the plane's bands; memo.rs guard 0.9→0.85 (belt-served 0.95–0.99); B12 is a broken instrument here, B17 times out at the frozen 60 s on both arms.
The carried form is the measured form: the shipped `QuantizedMemo::get` returns `from_shape(decode())` — the exact key is carried, never snapped to the cell (lineage: r2's exact increments; the 5 October correction — an exact memo never hits on distinct kicks).
Unmeasured successors (6e91): serve the belt's keys only (a population B13 never flies), or measure the amplification vs width before stepping the ladder.

## Refuted

- "Adoptable behind the gates" at 11+11, plane-wide (9eeb/f7c3's adoption half): refuted at B13 — 46/64 vs 60/64 within 1e-2, worst ΔE 5.93e-1, deterministic; the belt-scoped memory half is not refuted (6e91).
- The strong-branch exact serve as the B13 rescue (od 4): `ES_QWEAK=1` (weak branch served) reads 47/64, worst 5.92e-1 — the failing plane keys are weak-branch (6e91).
- f7c3's "~3.7–4.5 compiled cores at 10⁹" (the 104 µs plane-FIT composition): superseded by 6e91's measurement on the belt's own keys — 4.95 µs a compile, 0.15–0.17 cores; the belt was priced at the plane scene's compile (20×).
- "The plane's B9 knot invariance transfers to the belt": 0.80–0.82% of belt members land on a knot-count boundary at every scale and seed (ef8c).
- The write-back form (the orbit's key snapped to the cell): law.md — "re-rounds at every kick, a random walk (principle 13)"; the carried form is the one measured (r2; the 5 October correction).
- "The belt census is the open measurement / the memory half is unproven at scale": measured — cells saturate O(1), the stream adds ~nothing over 2–3.2 intervals (f7c3); 9eeb's FIT correction stands (2.8× plane scene; 7.8× the belt's own keys, 6e91).
- "Belt rebinds 29,097 identical at 10⁴" read as bit-identity: structural (9,699 bodies × 3 fires); the recurrence and cell deltas carry the signal (6e91, checker 2).

## Open directions

1. **Belt-scoped serving** (moves two rows: standing tables ~400× at 10⁶ → the 4,096-cell ≈ 3.4 MB ceiling [macro live set, ~10²–10³]; kick CPU 7.8× [micro kick cost, ~10–10²]): the served belt stream is the exact stream and B13 never flies belt keys — efd4's intern + refcount keyed by cell, eviction optional.
2. **The width ladder vs B13** (gates any plane-wide return; micro kick row): the encounter, not the cycle, sets the width — a 2⁻¹¹ shift amplifies 59× through an assist; measure the amplification vs width near grazing draws before stepping 11→17 (6e91; checker 2 confirmed the direction).
3. **Turnover under stirring or burning** (bounds od 1's CPU ceiling): cold-build turnover unmeasured past 3 fires (≈0 measured); if turnover reaches the fire rate, CPU returns to the 0.15–0.17-core compile ceiling at 10⁹, not ~4 (f7c3, 6e91).
4. **The resonance guard** (a gate risk for od 1): a population straddling a mean-motion boundary is unmeasured (6e91).
5. **Carlson wiring for cold builds** (≤1.1× on the kick row): the belt's cold-build share is ≤1.1% (f7c3) — Carlson matters only for the locals.

## Contradictions

- law.md's "Not adopted: a quantized (E, L) memo for kicks" (the write-back reading) vs this page's carried form — resolved by construction and measurement (exact recurrence 0.000, hashes stable), but the law text is its owner's to re-word.
## Runs
- 20261018-2312-system-9eeb (silver): the carried cell serves 96.7% of the plane's rebinds (58 cold builds serve 1,764); FIT −64%; gates hold.
- 20261019-1316-components-ef8c (silver): the belt census — 1,731/1,960 cells at 10⁵/10⁶ (key-space), serve error 4.6e-4/1.6e-4; B9 does not transfer.
- 20261019-1316-system-f7c3 (silver): the belt census — cells saturate 1,095→1,831 over 2,699→299,699 bodies (live stream); ceiling 4,096 ≈ 3.4 MB.
- 20261019-1452-second-20261019-1316-system-f7c3-6e91 (gold): the gold rung — B13 kills plane-wide 11+11 serving (46/64); belt compile 4.95 µs, serve 0.641 µs (7.8×); belt stream exact.
