# Dossier — 20261015-1926-quant-c4d3 (quant lens)

## Claim

The shipped `Orbit::compile` at the ladder belt's true keys costs **p50 4.4–4.5 µs
(mean 4.7, p99 8.0, max 12.5; e-monotone 3.4→8.3 µs over the belt's own e, flat in p)**,
the full shipped promotion path (`add_body`: compile + catalogue insert + `bind_exact`
+ store) is **p50 9.2 µs, flat in N from 25k to 200k** — so quant-262f's batched belt
promotion (**11.7 µs as timed, 12.8 honest with the coefficient solves**) is a ~2.7×
**regression** per promotion against the shipped scalar path at the belt mix, its native
~4 µs projection is mere parity, and the record's "wave compute cuts ~3–8×" (262f,
against a669's ~30 µs/kick-compile anchor) **dies at the belt**: the compile is ~7% of
the wave's 59–76 µs/kick CPU, and b172's in-flight promote-compile arithmetic
(0.56 s/132,061 = 4.2 µs; 4.74 s/940,718 = 5.0 µs) corroborates the 4.4–4.5 µs directly.

## Bottleneck

The board's kick line ("the cheapest exact kick on the shipped representation"): the
kick sits 75–160 µs against a ~50 ns floor, and the first-kick wave is the belt's
promotion bill. Kick-jet open direction 4 names this exact missing number ("the shipped
compile timed at true belt keys — this run cites a669/b30b instead"). Pricing it
decides whether the batched-promotion adoption (262f) is worth building: it is not, at
the belt. What it deletes: the native port / SIMD-ratio follow-ups scoped for the belt
wave (open direction 4's remaining belt items); the lever moves to the wave's
attendants (~85–93% of the per-kick CPU) and to the strong-field/high-e tail where the
shipped compile really does cost 29–192 µs (grid below) and cd6e's closed forms keep
their win.

## Evidence

All numbers from pristine shipped code (no patch to `crates/`), Linux x86 i7-4790, load
~0.6, 13 GB free; orders of magnitude only per lab rules (the integrator re-measures on
the M1). Keys are bit-identical to the flight's: `scenario::ladder_ship` → `add_body` →
`spec_binding` → `OrbitKey::bound(unit.to_tube(periapsis), e_q48)`, and doll 0's unit is
`Unit::ONE` (`DollRec::root`), so `to_tube` is the identity (`crates/universe/src/scenario.rs:260`,
`universe.rs:343-346`, `world.rs:124-136`).

Belt mix (verbatim from the ladder): a uniform in [2,3) AU, e Rayleigh σ=0.07 redrawn
above 0.4, p = a(1−e); measured median e 0.082 (= σ√(2 ln 2)), max e 0.33–0.34,
q ∈ [3.3e-9, 8.3e-9] — the weak branch throughout.

Shipped `Orbit::compile`, per-key min of 3 passes, n=199,700 keys (seed 1) and two
held-out seeds (predictions written first, `predictions.md`):

| arm | n | p50 µs | mean µs | p99 µs | max µs |
|---|---|---|---|---|---|
| seed 1 | 199,700 | 4.44 | 4.71 | 7.85 | 11.89 |
| seed 5 (held out) | 99,700 | 4.45 | 4.72 | 7.97 | 12.53 |
| seed 42 (held out) | 99,700 | 4.50 | 4.76 | 8.02 | 12.45 |

By e band (seed 1): 3.43 / 3.59 / 4.35 / 5.45 / 8.33 µs p50 for e in
[0,0.02)/[0.02,0.05)/[0.05,0.1)/[0.1,0.2)/[0.2,0.4) — monotone, and the redraw cap at
e=0.4 truncates the expensive tail the 36-key grid saw. p-invariance inside the band:
e=0.07 compiles at 3.69/3.72/3.73/3.69/3.69 µs for p = 1/2/3/5/20 AU (±2%).
Shape control, same binary (min of 200): strong field p=100 M: e=0.001→5.4, 0.5→29.2,
0.9→75.1, 0.999→192.1 µs (p≤10⁴ M identical; p=10⁶ M cheaper: 3.2/17.6/45.1/116.0) —
cd6e's e-monotone law reproduced in shape, and the belt lives at its floor. p=7 M with
e≥0.5 is refused (plunge), as the law says. Control: `ladder_ship`+`OrbitKey::bound`
costs 57–240 ns — the timer's floor, ~5% of the cheapest compile.

Shipped promotion path `add_body` at the same keys (one pass, in-universe):

| n | mean µs | p50 µs | p99 µs | max µs |
|---|---|---|---|---|
| 24,700 | 9.83 | 9.40 | 16.11 | 151 |
| 49,700 | 9.54 | 9.19 | 14.65 | 146 |
| 99,700 (seed 1) | 9.50 | 9.18 | 14.35 | 227 |
| 99,700 (seed 5, held out) | 9.54 | 9.21 | 14.32 | 163 |
| 199,700 | 9.57 | 9.23 | 14.76 | 199 |

Flat in N (p50 9.19–9.40 across a 8× range); the front/back-half offset (8.3 vs 10.8 µs
mean) is constant across N — warm-up, not growth. Attendants (bind + catalogue insert +
store) ≈ 9.5 − 4.7 ≈ 4.8 µs mean, i.e. half the promotion path. RSS 209 MB at 99.7k
bodies ≈ 2.1 kB/body (the record's ~2.46 kB birth figure stands).

Composition against the record: compile 4.4 µs = 6–7% of the wave's 59–76 µs/kick CPU
incl. attendants (b30b's anchor); the whole promotion path 9.2 µs = ~14%. 262f's
batched promotion, honest 12.8 µs/promotion (its checker's number), is 2.7× the shipped
promotion path and 2.9× the shipped compile at these keys.

### Commands (each ≤ 60 s)

```
cargo build --release -p emergent-universe --example belt_compile --example belt_bind
T=/path/to/target/dir   # this box: $CARGO_TARGET_DIR/release/examples
$T/belt_compile 200000 1 3          # decisive: seed 1, n=200k, 3 passes
$T/belt_compile 100000 5 3          # held out
$T/belt_compile 100000 42 3         # held out
$T/belt_bind 100000 1               # promotion path + N-flatness (also 25000/200000, seed 5)
```

`regen.sh` reruns all of the above and prints the deterministic content (e-bands, refusal
pattern, grid) as checksums plus the headline timings; the counters and bands are
deterministic, only timings wobble — the regenerated runs landed on p50 4.43–4.45 µs
compile and 9.17–9.23 µs promotion path, REGEN OK.

## Predictions

Written and frozen before the decisive runs (`predictions.md`). P1 (p50 ∈ [3.5,5.5],
p99 ≤ 12, max ≤ 25 at held-out seeds), P2 (e-monotone 3.4→8–11), P3 (p-invariance
±10%) and P4 (the record correction) all held, on both held-out seeds. P5's kill test
(p50 > 15 µs ⇒ harness misses in-flight cost) did not fire.

## What would make it wrong

- The wave's promotions on the seam builds (which is what actually demotes/re-mints in
  flight) could carry costs `add_body` does not — but b172's in-flight promote-compile
  counters (4.2/5.0 µs) already sit at my number, so the in-flight price agrees.
- 262f's batched form could still win where compile inputs repeat within a batch
  (identical keys) — but the belt's keys are distinct (2^48 e-mantissas; the exact
  memo already measured 0% hits on the plane), so no.
- Cross-box wobble: both prices are Linux/x86; if the M1's shipped compile at belt keys
  ran >2.7× slower than this box, the batched form would regain parity — the M1
  re-measure (one command above) decides.
- If a future scene mints belt bodies with e > 0.4 or p ≪ 1 AU, the compile wall
  returns (29–192 µs on the grid) and cd6e's closed forms become the lever again; my
  claim is scoped to the ladder's belt mix as shipped.

## Cost of adopting / fit with PRINCIPLES

Nothing to adopt — this run **prevents** an adoption (the native batched-promotion
port for the belt wave). It fits "the cheapest compute is compute not done" and the
quant lens's "edge before the bet": the edge was measured before the port was built,
and it is ~1×. It also satisfies "Measure before claiming": 262f's edge leaned on an
anchor (a669's ~30 µs) whose domain was not the belt; the lab's own rule (check the
oracle's domain before blaming the law) applies to cost anchors too.

## The lens

The quant lens prices the bet and may under-weight the law's shape: I measured cost,
not correctness — no digest or behaviour gate was run (none is needed; the code is
unmodified). I also did not measure the wave's non-promotion attendants in flight
(the ~50–65 µs/kick beyond the promotion path); naming them precisely needs the seam
binary and a flight, which is the natural next run on this thread.
