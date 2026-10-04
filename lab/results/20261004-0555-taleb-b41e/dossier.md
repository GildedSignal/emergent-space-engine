# Dossier — run 20261004-0555-taleb-b41e (lens: Taleb)

## Claim

The plane compiles a fresh cycle trajectory on 98.6% of all rebinds (29,402 rebinds → 28,997
distinct exact keys) because its `Catalogue` is a keyless arena, and the law's shared memo
(`docs/law.md`, State: "shared by every tube with the same key") would hit **95.25%** of those
rebinds at the already-vetted 12-bit quantum — turning ~21× of the compile work into 59 ns
lookups, with bit-identical state reconstruction (300/300, residual ≤ 52 bits), and capping
catalogue memory at distinct live keys instead of live bindings (~848 B/entry unshared ⇒ ~850 GB
at 10⁹ real bodies, 100× the 8 GB budget; sharing is a requirement, not an optimization).

## Bottleneck

Board #3 (cost at a billion: fewer/cheaper events) and #5 (10⁹ in 8 GB), via the handoff's live
item 3 ("a kick costs 29 µs, 15 of them in rebinding fit and compile"). Expected gain: measured
21× fewer compiles per scene on the rebind stream; per kick, the compile is replaced by a lookup
on 95% of rebinds (2.36 µs → 59 ns on this box; on the integrator's M1 split, ~15 µs → lookup,
≈ 2× the whole kick — inference, cloud timings are orders of magnitude only). What it deletes:
the per-rebind `Orbit::compile` + `Arc<Entry>` allocation on the kick path — the single largest
removable component of the plane's measured kick cost.

## Evidence

Machine: 2 vCPU cloud container, load 0.53, 1.9/7.9 GB used (recorded in `decisive-run.txt`).
Scene: `scenario::plane(seed 1, sparse, 1 thread, members 1024)`, 1800 frames at rtf 100, config
default `step_log2 = 7` (128 kicks per radial period per ship).

```
rebinds=29402 distinct_exact=28997 (98.6%) distinct_memo12=1398 memo_quantize_errors=0
memo_hitrate_stream=0.9525  top multiplicities [152,146,146,146,...]
kick_us median=26.21 p99=36.47  (pure resolver, replay)
from_state=9.08us  orbit_compile_alone=2.36us  memo_key_lookup=59ns
exactness: memo_reconstruct_bit_identical=300/300 failures=0 max_residual_bits=52
memory: entry 184 B shallow + 664 B deep (knots) = 848 B; catalogue_live=1052
kicks_per_frame: median 0, max 23 (bursts; budget-bounded per plane.md §7)
```

Reproduce (each ≤ 60 s; patches: `crates/space/src/binding.rs` adds
`Rebinding::from_state_memo`, `crates/universe/src/bind.rs` adds the `REBIND_KEYS` observer,
`crates/universe/examples/memo_probe.rs` is the probe):

```sh
cargo build --release -p emergent-universe --example memo_probe
./target/release/examples/memo_probe 1024 1800        # decisive (4.4 s)
./target/release/examples/memo_probe 256 60           # smoke
cargo test --release -p emergent-universe             # patches change no behaviour
```

Interpretation limits, stated: `from_state_memo` still compiles the memo key (the timing pair
shows fit-dominance on x86: compile is 26% of `from_state` here); the claimed saving is
`hit_rate × (compile − lookup)`, arithmetic on measured parts. The M1's 15 µs compile share is
the integrator's measurement, not mine.

## Predictions

`predictions.md` was written before the decisive run. Held: (1) distinct-exact ≥ 0.95 → 0.986;
(2) hit rate ≥ 0.75 → 0.9525 (smoke 0.69); (3) 100% bit-identical reconstruct, ≤ 60 bits → 52;
(5) entry 0.6–1 KB → 848 B. Held partially: (4) compile is a minority share on this box (26%),
so the cloud kick saving is ~9% (I predicted 10–25%); the ~2× M1 figure remains inference.
Not falsified, not fully shown: (6) fleet members are lattice bodies and produced no tube
rebinds (bodies stayed 28), but 29,402 rebinds vs 365 replayed ship kicks means most rebinds
fire inside `frame`/`settle` (doll centres, handoffs, leavers) — the observer sees them all;
per-source attribution was not built.

## What would make it wrong

- Behaviour gates: a memo-key law changes each cycle by the 2⁻¹² (E, L) quantum, so precession
  and period shift at ~10⁻⁴ relative — B2's 0.1% period band is passed with little margin, and
  B1/B9 have never been run on memo keys. If they fail, the quantum (or the gate) must be
  re-derived; the exactness control does not cover behaviour, only state at events.
- The hit rate is measured on one scene (one star system, 28 tube bodies, correlated ships).
  A decorrelated galaxy could live in more cells; the Zipf-fleet scenes of B15 are the
  favourable case (formation lattices share keys by construction) and must be measured.
- The 12-bit quantum is the space crate's weak-envelope choice (orbit.rs); if the plane's
  scenes need finer (E, L), hit rate falls as bits rise.

## Cost of adoption, and fit with PRINCIPLES

One step: key `crates/universe`'s `Catalogue` by `(memo_key, clockwise, passage edge)` with
refcounted entries — the pattern already ships in `crates/space`'s `Catalogue.ids`
(`HashMap<(OrbitKey, bool, Option<Scalar>), u32>`); `from_state_memo` is the drop-in fit and the
exactness control is this run's. Cost: the residual grows to ~52 bits (inside the documented
65-bit word), the memo must be law-versioned (never reused across LAW_IDs), and B1/B2/B9 must be
re-frozen on memo keys. Fits: "Compute only surprises" (§3: a recompile of a cycle already
compiled for a cell within one quantum is work for no reason); "Store the generator, not the
generated" (§6); "Errors never compound" (§13: the residual is exact, integers, carried — not
dropped); "The memory floor is information" (§24: distinct live keys, not live bindings, are the
information). Julien, 29 September: "there's no way that it can't be cheap … thanks to simple
laws"; the memo is the cheap half of the tube's 16 bytes, currently unbuilt on the plane.

## The lens (Taleb) and what it missed

Via negativa found the missing part (a fence that exists in prose — law.md's shared memo — and
in `crates/space`, but not on the thing that flies); the fat-tail reading (850 GB at 10⁹ if
entries stay per-binding) sizes the allocator's memory for the worst case, not the mean. What
the lens may have missed: the fit (not the compile) dominates the kick on this box, so the
memo alone does not reach the 10–100× the board wants — fewer kicks per orbit (q-correctors)
and a cheaper fit matter as much; and no adversarial *dynamics* was run (no resonance, no flyby
storm) — the hit rate under a shock that decorrelates a fleet in one pass is unmeasured, which
is the Taleb question this Taleb run did not answer.

Self-grade: **silver** — real, reproduced, predictions held; one named experiment from gold:
re-freeze B1/B2/B9 on memo keys (positive control: exact keys) and measure the hit rate on a
B15 Zipf-fleet scene.
