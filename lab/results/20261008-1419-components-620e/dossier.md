# Dossier — 20261008-1419-components-620e (components lens)

**Claim.** The kick event — the engine's dominant cost — is 25× above its floor, and the gap is
not the force law's arithmetic: the rebind (`bind`, ~68% of a fired kick) and the per-body
recomputation of shared epoch data (the secondaries' tube readouts, ~27%) dominate, while the
entire force evaluation is ~6%; a measured integer-band evaluator does the force at 8–10× less
than today's `Scalar` path and agrees with it below the ship's real velocity quantum.

**Bottleneck.** Board: "kicks dominate the engine's cost". Expected gain: 25× on the per-kick
path (orders of magnitude on the plane's event throughput; at 10⁹ bodies × 0.3 fired
kicks/orbit, today's ~28–41 µs/kick is ~1 h of one core per orbit; the floor's ~1.1–1.7 µs makes
it ~2–3 min). What it deletes: the per-kick rebind (replaced by the already-adopted jet,
re-anchored at 0.05 compiles/kick), the per-body secondaries evaluation (shared per kick epoch:
block steps share boundaries, law.md "A body's state between kicks"), and the `Scalar` soft
arithmetic on the kick path (replaced by one shared exponent per band — already the law's stated
number rule).

**Evidence** (Linux x86, shared runner, load 5.83/8 cores — orders of magnitude only; ratios are
the robust numbers, stable across 5 runs including two at 1.4× load):

| part of one fired level-0 kick | ns | share |
|---|---|---|
| `bind` (the rebind, fires on ~99% of distinct kicks) | 18,600–28,600 | 68% |
| `Ctx::secondaries` work (3 planets' `cartesian` + Vec) | 7,500–10,600 | 27% |
| `force::acceleration` (`Scalar`) | 1,590–2,270 | 5.8% |
| `Binding::readout` (the state read, for scale) | 2,470–3,440 | — |
| **floor version**: integer-band force, body part only | **190–220** | — |
| floor version with origin fall (apples-to-apples) | 375–440 (5.2–5.9× vs `Scalar`) | — |

Sum today ≈ 28–41 µs per fired kick; floor ≈ 1.1–1.7 µs (integer force 0.2 + 0.05·bind ≈ 0.9–1.4
+ shared-epoch secondaries ≈ 0); **idiot index 25×**, and 80% of the *floor itself* is the jet's
re-anchor — the kick economy is rebind-bound all the way down.

Exactness of the floor evaluator (held-out sweep, 64 xorshift belt positions, not tuned on):
per-secondary pulls agree to 0.1–0.3% (worst components quantize at the band floor 2^-80, as
designed); max kick deviation 1.6 quanta of an artificially fine 2^-30 velocity word at
h = T/32 — about 10⁻⁵ of a real belt ship's velocity quantum (v ≈ 1.7e-4 c ⇒ word ≈ 2^-13), i.e.
below the carry's accumulation quantum. One residual: a ~3e-3 relative disagreement on isolated
components that I did not isolate in time (the per-secondary debug block in the bench pinpoints
it in minutes for any checker).

Reproduce (each ≤ 60 s):
```bash
cargo build --release --bin kickfloor -p emergent-universe
/home/glmlab/lab-target-3/release/kickfloor   # or target/release/kickfloor
```
Bench: `crates/universe/src/bin/kickfloor.rs` (copy in `work/`), raw outputs in
`kickfloor-out.txt`, machine state in `machine-state.txt`. Scene = the plane's Cinder/Home/Giant
masses and radii (`crates/universe/src/scenario.rs`), belt positions between Home and Giant.

**Predictions** (`predictions.md`): (2) partially held — the integer path is 5–10× faster, not
10–40× (u128 products in the Newton are the cost; a further ~2× is available with truncated
seeds). (3) held — the rebind is 12.6× the force evaluation and dominates. (4) held — the
secondaries readout is 4.7× the force evaluation. (5) held — today 28–41 µs, floor 1.1–1.7 µs,
idiot index 25× (predicted 20–60). (1) **missed as pre-registered**: the first run failed my own
kill criterion (deviation = 1.0 relative) — a bookkeeping bug (acceleration output band; sign of
AF in the final shift), found from the per-secondary debug and fixed; after the fix the deviation
is 1.6 quanta at 2^-30, still above my pre-registered 0.1, with the unexplained 3e-3 component
residual above. The exactness claim is therefore **tuned on the failure** and needs an
independent checker before adoption.

**What would make it wrong.** The 0.05 compiles/kick is the adopted design number
(redteam-20261006-0346-redteam-df81), not re-measured here. Epoch-sharing assumes kick epochs
coincide across members (block power-of-two steps give that; the hit rate at real belt step
spreads is unmeasured). The integer path must be *defined* as the law (deterministic truncation
at the band), not checked against `Scalar` — that is a law change requiring the integrator, not a
drop-in. And the 3e-3 residual could hide a real bug in my Newton chain rather than rounding.
Adoption cost: ~250 lines (the evaluator), a per-(doll, tick) secondaries cache, and wiring the
jet — all inside `crates/universe`, no spec change beyond declaring the band arithmetic
canonical. PRINCIPLES fit: #1 "The cheapest compute is compute not done" (the rebind on 99% of
kicks); #3 "Nothing is evolved that can be derived when looked at" (the origin fall is
body-independent, recomputed per member today); #16 "no it's about what's cheapest to compute"
(band integers over per-op-normalized `Scalar`); #12 (per-kick cost is what the allocator's p99
breathes).

**The lens.** One component, measured alone, can move cost to its neighbours: I did not measure
the plan-Vec inserts per kick, the `Segment` clone each rebind pushes into history (pruned, but
paid), or the `ext.time` solves of the clock path; and single-thread ns/op says nothing about
p99 frames at billion-body memory traffic. Those are the neighbours the integrator should see
measured next.
