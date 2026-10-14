# Dossier — 20261014-1010-spacex-f9b4 (lens: SpaceX)

**Claim.** The gold experiment 5a3b named is done: a **static, pure-integer, key-derived
edge rule** (geometric rungs anchored at both turning points) replaces the shipped
16/octave EDGE ladder on the shipped walk machinery at a **4.96× median panel cut
(3.54× compile time) on the expensive band e ≥ 0.9**, holds the compile's 2⁻³⁰
certificate on **69/73 keys — the same count as the shipped ladder** — extends to
`Passage::compile` (the leaver rebind's walk, 3.5–5× panel cut), and the mechanism it
exposes (which turning point binds, and where) is itself the map for the build.

**Bottleneck.** The kick at ~10³·³ over its floor (board, third row): the fired kick
is 46% bind, and the bind's expensive half is the compile's panel walk on high-e keys
(closed-form-kernel page). 5a3b measured the panel floor (12–27 panels at e ≥ 0.9,
p ≥ 20) but by adaptive bisection that cannot run per compile, and named the missing
piece "a *static* edge rule from the key … that demonstration is the gold
experiment." This run is that demonstration.

**The rule (all integer, all from the key; `cut`, CAP, the dyadic layer, the 4-point
Gauss quad and the readout untouched).** Edges in the walk's own x variable
(x = k + (1−k)cos ψ, periapsis x=1, apoapsis x=2k−1):
1. **Apoapsis rungs** (always on): x = x_a + (1−x_a)·2^(−j/2), j = 1, 2, …, down to
   x − x_a = x_a >> 4 — geometric doubling in ψ toward the apoapsis turning point
   (the t/τ channels' 1/u² shoulder). The taper is `isqrt(1 << (124−j))`: exact
   integers, no table.
2. **Periapsis rungs** (near-separatrix only): x = 1 − 2^(−j), down to
   1 − x = δ/(2q), δ = 1 − q(4k+2). This is the walk's own algebra — near periapsis
   1 − q·a = δ − 2q(1 − x) — so the rungs stop exactly at the advance channel's
   g-spike scale and **vanish entirely far from the separatrix** (δ/(2q) > 1 at
   p = 20, e = 0.99: zero periapsis rungs; one mechanism, every key).
Arm `c` (the frozen candidate) = apoapsis taper with the stop 4× deeper than `b`.

**Evidence** (Linux/x86, shared cloud, orders of magnitude; every number from
`regen.sh`, ~3 min: patch → build → sweep → `ref.py` → suite):
- Grid 8×9 (p ∈ {7.1, 8, 10, 20, 50, 200, 10³, 10⁵} × e ∈ {0.1 … 0.99999}) + 10
  held-out keys + 3 hyperbolic passages. Certificate: summed error ≤ 2⁻³⁰ relative on
  all three channels vs an mpmath 50-digit reference (`ref.py`, independent of the
  walk). **Control:** the ladder arm reproduces the record's own validation band
  (2.2–7.3×10⁻¹⁰ at p ≥ 10; its known p = 8 m→1 degradation 3.7×10⁻⁷ reappears).
- **Certificate: c passes 69/73, ladder passes 69/73.** Disjoint single misses: the
  ladder alone fails (8, 0.99) at 5.4×10⁻⁹; c alone fails (6.7, 0.3) at
  7.4×10⁻⁹ — and that residual is **placement-immune**: c with a doubled apoapsis
  depth (21 panels vs 13) reads the same 7.4×10⁻⁹, so it is node arithmetic (the
  fixed-point quad at q ≈ 0.19), not panel count, that owns it. The three shared
  misses (p = 8, e ≥ 0.999) are the shipped walk's own degradation band, where c is
  **6–220× more accurate** than the ladder (1.7×10⁻⁹ vs 3.7×10⁻⁷ at e = 0.99999).
- **Panels and time, e ≥ 0.9 (36 keys): ladder/c median 4.96× panels (2.61–6.27),
  3.54× time (1.94–4.48).** (8, 0.99999): 294 → 75 panels, 463 → 155 µs.
  (20, 0.99): 125 → 27, 166 → 38–49 µs (5a3b's projection band was 26–38 µs).
  (10⁵, 0.99999): 282 → 45, 307 → 54–71 µs, 1.59 µs/knot — the record's own
  1.1–1.7 µs/knot, so the win is panels, not per-panel cost. Mid band (0.3 ≤ e <
  0.9): 1.81× panels, 1.34× time. e < 0.3: parity panels, 0.77× time (probe
  overhead: an env read and a heap Vec per compile; a build hardcodes the rule).
- **Passages** (`Passage::compile`, 89–97% of the leaver rebind per 5a3b; same patch
  point, no separate tuning): 114 → 24, 184 → 53, 124 → 25 panels; 3.3×/2.1×/3.4×
  time. Certificate not wired there (the tail has its own quad); count only.
- **Mechanism, measured:** periapsis-only geometric arms fail the certificate at
  e ≥ 0.9 (m=1: 25/73, t/τ errors up to 7.6×10⁻⁷) — the apoapsis 1/u² shoulder is
  what the ladder's density was buying; mirrored m=1 still fails (1.8×10⁻⁹ at
  (20, 0.9)); 2 rungs/octave at the apoapsis is the cheapest passing taper on dev.
  Near the separatrix (p → 6+2e) the binding spike crosses to periapsis — apo-only
  fails there, the δ/(2q) rungs fix it, and the fix switches itself off at p ≥ 10.
- **Identity control:** with the probe off (env unset = the shipped ladder arm,
  routed through the refactor), the crate's suite is green — 53 tests, 0 failed
  (`cargo test --release -p emergent-space`), so adoption touches no shipped path.

**Predictions** (`predictions.md`, written before the sweep; dev tuning set p = 20,
e ∈ {0.1, 0.5, 0.9, 0.99} only): P5 (m=1 fails at e ≥ 0.9), P3 (time ≈ panels ± 30%),
P6 (passages ≥ 3×), P2's direction held (median 4.96×; the letter "≥ 3× at every key"
fails on 3 of 36 keys, min 2.61 — the p = 7.1 rows). P1 held on 72/73 keys: the single
miss is (6.7, 0.3), reported above with its diagnosis. P4's letter failed for a:4
(1.25×10⁻⁹ vs the ladder's 4.7×10⁻¹² at (8, 0.7)) and was repaired by arm c
(1.8×10⁻¹⁰, absolute bar passed, panels 45 → 21) — a post-hoc depth constant, tuned on
the failing key, labelled as such; P7's ≤ 2×-ladder clause holds at p ≥ 10, not at
p = 8 rows where both pass (c's errors there are 2–60× the ladder's yet under the
bar — the arithmetic-phase effect again).

**What would make it wrong.** The mpmath reference and the scaling formulas (the
control validates them to the record's band, but they are mine, not shipped); the
timing wobble on this shared box (±30% run to run — orders only); the passage arm is
untuned and uncertified (the tail's quad may need its own depth rule); and the
certificate bar itself is 5a3b's reading of "the compile's verified certificate" —
if the integrator freezes a different bar at the canon reset, the pass counts move
(the raw errors are in `verdicts_all.csv` for either reading).

**Cost of adoption.** One build, as 5a3b priced it: replace the band loop in
`OrbitShape::bound` and `Passage::compile` with the rule (a ~40-line function,
already written in the patch), hardcode it (drop the env parse and the Vec), freeze
the two constants (2 rungs/octave; stops x_a >> 4 and δ/(2q) >> 2). It is a canon
reset — knots move — so the certificate re-freeze the record already prescribes for
any panel-count change, replay-digests change with it. `crossings` consumers are
benches only (5a3b's audit). Fit with PRINCIPLES: "the cheapest compute is compute
not done" (16 panels/octave → ~0.5); "Discrete by design, cheapest arithmetic"
(pure integers, no Carlson kernel, no table); "A fix signals the wrong
representation" — the ladder was uniform in log x, but the walk's difficulty is
two turning points plus one separatrix scale, and the rule is exactly those three
quantities.

**The lens.** SpaceX deletes first: this deletes ~80% of the panels and the whole
EDGE band machinery (a 17-entry table plus octave arithmetic) in favour of two
shifts and two isqrts. The blind spot it paid: I nearly shipped the elegant
one-sided rule (a:4) because it passed dev — the separatrix band only showed up on
the full grid, and the fix came from the walk's own algebra, not from more
cleverness. The remaining (6.7, 0.3)-class residual is where this lens says stop:
it is not a panel problem, and panel rules should not chase it.
