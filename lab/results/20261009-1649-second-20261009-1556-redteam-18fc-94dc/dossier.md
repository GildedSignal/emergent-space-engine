# Dossier — run 20261009-1649 (second author on 20261009-1556-redteam-18fc)

## Claim

The checker's named gold experiment (the kinked tube) is done and the claim then holds: **the
view-gather premise survives kinked tubes at closing β → 1 on the shipped code** — with emitters
kinked by the engine's own stepper, every crossing is found (0 drops in 6000 gathered emitter-frames
per case), cold and memo views are bit-identical (0 disagreements), and an independent bisection
oracle agrees on every emission tick (0 mismatches), at 1.15–1.92 readouts/emitter — the kinks are
free. The strong-kink regime stays out of reach by physics, not by engine defect: a relativistic
tide deflects a 0.9999c emitter by ~4e-8 relative, and even the densest configuration the engine
accepts (12/12 emitters kinked, 244k kicks) leaves the gather unchanged.

## Bottleneck

Not a bottleneck mover: it closes the named experiment and removes the kinked-tube caveat from
r6's edge cases. Nothing is adopted; the r6 criteria gain one case family (below) and one scope
note: thrusting relativistic *emitters* do not exist in the engine (only the player thrusts, and
the player is the observer), so kinked-tube content at β → 1 is what the stepper's clock kicks
make of it — 1–2 rebinds per flight at the game's step size, ~60 per flight at `step_log2` 20.

## Evidence

All numbers from the shipped crate plus one new example (`crates/universe/examples/view_kink.rs`,
also in `work/`); no library code edited. Linux x86. Kinks are made with the engine's own
machinery: a 1/999 secondary (a Jupiter, `make_source`) on the convergence point of 12 Toward
emitters makes `has_forces` true, so `settle` runs the motion-law-v2 clock and its kicks rebind
the emitters' tubes; the source's placement is calibrated in-build (verified to ≤ 0.1 root units).
The oracle is a bisection on `g(t) = t + |x(t) − xo| − t_now` (monotone along a timelike tube), an
independent search that shares only the worldline reads. Commands (≤ 60 s each, ~2 GB peak far
below):

```
cargo run --release -p emergent-universe --example view_kink -- run 1 600
cargo run --release -p emergent-universe --example view_kink -- run 100 600
cargo run --release -p emergent-universe --example view_kink -- run20 1 600
```

rtf 1 (`work/kink-rtf1.txt`; 3383 ticks/frame, 600 frames, 12 emitters, source 1/999 at P+[0,2e4]):

| case | reads/em | max/fr | drops | disagr | oracle | kinks swept |
|---|---|---|---|---|---|---|
| control straight 0.9999 (log2 7) | 1.78 | 57 | 0 | 0 | 0 | 0 |
| kinked 0.9 toward (log2 14) | 1.19 | 29 | 0 | 0 | 0 | 0 |
| kinked 0.9999 toward (log2 14) | 1.78 | 57 | 0 | 0 | 0 | 8 |
| kinked obs 0.9c × 0.9999 (log2 14) | 1.92 | 46 | 0 | 0 | 0 | 5 |
| kinked 0.9999 + stale-jumps (log2 14) | 1.80 | 91 | 0 | 0 | 0 | 8 |

rtf 100 (`work/kink-rtf100.txt`): same shape — kinked 0.9999: 1.15 reads/em, max 73, 0/0/0, **10/10
kinks inside the swept emission range** (the arrival burst sweeps the emission tick across every
rebind tick). The dense case (`work/run20.txt`, log2 20, 12/12 emitters kinked, 244k kicks,
680k refusals, settle 37 s): **reads/em 1.78, max 57, drops 0, disagreement 0, oracle 0** —
bit-identical cost to the straight control.

Why it survives (mechanism, confirmed by the numbers): a rebind is a corner in `g`, so the
convexity shortcut (`g(t+1) ≥ g(t) + g'(t)`) can fail locally, but `g` stays monotone (a tube is
timelike) and the walk is bracketed, so the *answer* cannot depend on the guess; kinks and stale
slopes (the stale-jump case: 5 jumps of 40 frames, max 91 readouts, recovered in one frame) cost
readouts only on the straddling frames. The oracle agreeing on every tick is the bracket contract
itself holding on the kinked chain.

The regime limit, measured (`work/sweep.txt`, `work/slow.txt`): the deflection of a 0.9999c emitter
through the 1/999 source at 2e4 root units is 4.8e1 root units over a 1.2e9-root-unit flight
(~4e-8 relative) — a tide is that small against a relativistic kinetic energy, whatever the step
size; no source mass the engine accepts (up to 1/1) changes the order. At the game's `step_log2` 7
the emitters' clock steps are 1e8–2e9 ticks (0 rebinds in the window); 14 gives 1–2 rebinds per
flight; 20 (37 s settle, 244k kicks) is the densest and still leaves the view unchanged.

## Predictions

`predictions.md` was written at 17:20, before all decisive runs (file times 17:21–17:25).
**P1–P5 held exactly** (controls, kink existence and sweep coverage, 0 drops / 0 disagreement /
oracle agreement, stale-jump recovery, reads/em ≤ 1.92 against a predicted ≤ 4). **P6's timing
claim was wrong and is reported as wrong**: I predicted log2 20 would not settle in ten minutes
(the sweep's wall clock had cut that combo); measured standalone it settles in 37 s — so I ran the
denser case too (`run20`), and it also held, which strengthens the claim beyond the prediction.

## What would make it wrong

- The kinks measured are small in *velocity* (each rebind's Δv is a few quanta; the whole flyby
  deflects ~4e-8 relative). A genuinely thrusting relativistic emitter — content the engine cannot
  express (only the player has thrust, and the player is the observer) — could kink harder; the
  audit is complete for every kink the shipped laws can produce, not for that hypothetical.
- The bisection oracle shares the worldline read (`state_rate`) with the gather, so a bug in the
  read path itself would hide from both. Mitigated, not closed: the straight control (0 mismatches)
  and the original run's construction-level oracle cover the read path on the same geometry, and
  the worldline is the stepper's gated product, not the view's premise.
- The engine refused ~73% of the clock's fine-step items (680k refusals at log2 20, mostly the
  bound player's kicks). Recorded, not diagnosed: a motion-law-v2 question (why a bound orbit
  refuses most kicks at fine steps), outside this run's scope and harmless to the view (refused
  bodies stay readable; 0 unalive-frame-counts).

## Cost of adopting

Nothing in the engine. For r6 (open, law.md:88): add the kinked family — `view_kink run 1 600`,
`run 100 600`, `run20 1 600` — as edge cases with the criteria "no drop while alive, cold = memo,
gather tick = bisection tick", and the scope note above. The `seen`-column cosmetic from the
original run's checker stands (integer division; not fixed here — no crate edits).

## The lens

The second-author lens trusts the checker's framing, and the framing assumed "a thrusting emitter"
was expressible content. It is not: the experiment had to be re-derived from what the engine can
kink (clock kicks on a relativistic tube), which is exactly where the answer became informative —
the strong-kink regime is empty *by physics* (principle 9: the configuration, not the method, is
what fails to exist). What this lens may have missed: the 0.9c kinked case ended with 0 kinks
swept (its first light arrives later than the window; recorded in the tables, the 0.9999 cases
carry the exposure), and the refusals anomaly was left for the motion-law owner.
