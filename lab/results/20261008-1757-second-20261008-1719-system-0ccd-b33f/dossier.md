# Run 20261008-1757-second (on 20261008-1719-system-0ccd) — the jet wired: the speed is real, the wiring cancels the physics

## Claim

The silver's named gold experiment is done: the re-anchored jet wired into `Work::kick`'s rebind
path behind a flag (`ESE_JET`) delivers the promised speed — a measured **2.75×** on the plane's
kick median at rtf 100 (84.3 → 30.7 µs; 3.2× at rtf 30), with the increment's true cost **9.5 µs**
(well under compile/2), **4.8 % compiles per kick** (the law's own ≈0.05), bit-exact determinism,
and the jet-off digest identical to shipped — **but the claim as stated is refuted**: re-placing
the tube on the old cycle with an exact offset (what the `Entry`'s tables actually give) cancels
the secular effect of correlated kicks, failing a universe-suite invariant (the kicked ship's
push 6.3×10² against the origin's 7.7×10³ lattice units, cos −0.07, limit 5 %) and corrupting
B13's assists (60/64 → 41/64, worst ΔE ∞ at the law's 2⁻¹¹ rule; still 4× the shipped worst at a
43× tighter rule). The jet as adopted needs the *key* to track the drift first-order
("stored derivatives" of (E,L), which the entry does **not** carry); without it the lever is a
law change, not a speedup.

## Bottleneck

The same as the silver's: board focus 1 (kicks dominate cost) and 3 (cheaper events); the compile
is 53–71 % of a rebinding kick. This run answers the question the silver left open — what the
wiring costs in behaviour — and kills the "one flag away" reading of it.

## Evidence

Machine: shared 8-vCPU Linux runner (orders of magnitude only). All commands from the repo root,
each < 60 s; the patch is `work/patch.diff` (engine + probe); raw JSONs in `data/`.

```
git apply work/patch.diff            # or: the run's own tree
cargo build --release -p xtask                                   # ~40 s
env -u ESE_JET cargo run --release -q -p xtask -- universe --kick-bench --seconds 30 --rtf 100 --seed 1
ESE_JET=1     cargo run --release -q -p xtask -- universe --kick-bench --seconds 30 --rtf 100 --seed 1
ESE_JET=1     cargo run --release -q -p xtask -- universe --jet-probe   --seconds 30 --rtf 100 --seed 1
ESE_JET=1     cargo run --release -q -p xtask -- behave --law plane --gates B13
env -u ESE_JET cargo run --release -q -p xtask -- behave --law plane --gates B12,B13,B17
ESE_JET=1     cargo test --release -p emergent-universe --test lifecycle the_origin_takes
env -u ESE_JET cargo test --release -p emergent-universe            # 55 green
```

**1. The record regenerates** (the silver's numbers, from its own patch): seed 1 rtf 30 gives
630 rebinding kicks, residence median 6 / mean 13.58, kick med 87.7 µs (stored 88.9), bind 68.3
(68.6), readout 3.29 (3.32), digest `1a0dae74a20c907e…` and replay digest — **bit-identical** to
the stored JSONs; only wall-clock medians differ (this box's compile med 53.3 vs stored 63.5).

**2. The realized speed** (`--kick-bench`, resolver-only, distinct kicks):

| run | off med µs | on med µs | factor | compiles/kick | p99 off→on |
|---|---|---|---|---|---|
| seed 1, rtf 30 | 98.8 / 88.0 | 30.4 / 27.4 | 3.2× | 5.8 % (77/1326) | 410 → 411 |
| seed 1, rtf 100 | 84.4 | 30.3 | 2.79× | 4.8 % (119/2486) | 409 → 409 |

Two jet-on runs: identical digests (`a48ca4a3…`/`e152863f…` at rtf 30). Jet-off digest
`eccc7f5a3d78` — identical before and after the patch. Zero refusals anywhere. The jet-probe at
rtf 100: 1158 kicks = 1125 renewals + 33 declines (passages etc.), increment med **9.48 µs**
(p99 13.2) against the one-readout proxy 3.3 µs and compile/2 ≈ 26 µs — prediction 3's band
(5–15 µs) held; the lever survives the increment's true price.

**3. The error law at half a kick-interval** (probe, jet vs exact rebind, read ahead):
position rel med 5.1×10⁻¹⁰, p99 3.9×10⁻⁸; velocity rel med 2.8×10⁻¹¹, p99 5.7×10⁻¹⁰; zero
readout failures. Between single kicks the wiring is exact to spare — the failure is secular,
not per-event.

**4. The refutation.** (a) `behave --law plane --gates B12,B13,B17` **jet-off control**:
B12 FAIL (statistic known miscalibrated, HANDOFF 6 Oct), B13 FAIL 60/64 worst 2.12×10⁻² (the
recorded shipped state), B17 timeout under load — so B12/B17 cannot adjudicate here; B13 can.
**Jet-on** (law's rule, anchor 2⁻¹¹ of the word): B13 **41/64, worst ΔE ∞**, `jet_stats
renewals=4077` — the jet fires in the judged path and breaks assists. Anchor tightened 43×
(2⁻¹⁹): 60/64 again but worst 7.99×10⁻², still 4× the shipped worst, renewals down to 376 — a
threshold does not rescue it. (b) `cargo test -p emergent-universe`: 55/55 green jet-off;
jet-on `the_origin_takes_the_dolls_kicks_like_a_ship` FAILS — over ¾ of an orbit the kicks push
the ship 6.26×10² lattice units against the origin's 7.72×10³ (limit: 5 % agreement, cos >
0.9986; measured cos −0.074). The mechanism, visible in these two numbers: each renewal
re-places the tube on the *unchanged* cycle and absorbs the kicks' accumulated displacement into
the offset — which the re-anchor rule caps — so correlated kicks are **cancelled** instead of
accumulated. F1 (redteam-df81) let the cycle's increments track the drift (error C·δ²); this
wiring freezes the cycle, so the first-order secular motion never enters it. B13's ∞ worst is
the same cancellation inside a flyby.

## Predictions

`predictions.md` was written before the decisive runs. Held: 2 (2.75 ≥ 1.7× realized), 3
(increment 9.5 µs, inside 5–15), 4 (4.8–5.8 % compiles), 5 (bit-identical digests; differs from
jet-off), 6 (suite green jet-off). **Failed: 1 — the gates did not stay green** (B13 regressed;
the lifecycle invariant broke), which the prediction itself named as the refutation condition.

## What would make it wrong

- The gates' own defects (B12's statistic, B13's marginal 60/64, B17's timeout) mean the
  *pass/fail line* is soft; but the lifecycle failure is a 12× discrepancy in a judged
  invariant, not a marginal gate miss, and it reproduces on demand.
- A wiring that also moves the key by the stored (E,L) sensitivities — the multiply-add the law's
  text names — could restore the secular motion; that part is unbuilt, its cost unmeasured, and
  the law crate exposes no such derivatives today (the entry carries phase tables, not
  invariant sensitivities). Until it exists and passes these same two checks, the 2.75× is not
  bankable.

Cost of adopting: none from this run — the patch is the refutation's instrument, not a merge
candidate (the speed half is confirmed and the flag-off path is untouched; the flag-on path is a
law change). Fit with PRINCIPLES: "A fix signals the wrong representation" (19) — the split
compiler/renewal is right, but renewing the phase while freezing the cycle is the wrong
representation of a kick; "Errors never compound" (13) — here they are not compounded but
*cancelled*, the mirror failure; "a failed expectation is not automatically a failed method"
(H0183): the jet's mechanism needs its derivative half, this configuration dies.

## The lens (second author)

What I may have missed: I did not build the key-tracking derivative update (the possible rescue)
— priced as out of scope for one window, and the burden of proof now sits with it; a denser
scene (the checker's `--members 200`) might change the renewal/decline mix, but it cannot rescue
a secular cancellation; and my placement reuses `at_radius`'s outbound-leg convention, so a
subtle leg-selection bug could masquerade as cancellation — the half-interval error (10⁻⁸) and
the determinism make a gross placement bug unlikely, but a targeted single-orbit differential
against the exact rebind over one full residence would close that door.

Grade suggested: **gold as a refutation** — the silver's record regenerates, its named experiment
is done, and the claim ("wiring buys 1.7–2.7×" with behaviour intact) is cleanly false as
wired: the speed is real (2.75–3.2×), the wiring cancels secular kicks, and the missing
derivative half is now a priced, named prerequisite.
