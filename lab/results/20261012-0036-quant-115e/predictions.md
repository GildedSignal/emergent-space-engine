# Predictions (written before the decisive runs)

Pilot (already run, mean-level only, `cost_split` on this machine): whole-universe ~50 µs per
kick/open/boundary; pure `step::process` ~35 µs; readout 3.3 µs, secondaries 3.3 µs, tide 3.3 µs,
`root_state` 6.8 µs. The two decisive experiments below have **not** been run yet.

## Experiment A — the kick's stage budget (default plane scene, 30 G ticks settle)

Held-out cases (not tuned on): per-What latency distribution of `step::process` and `apply`;
boundary vs open vs kick cost; the tail ratio p99.9/p50 within each What.

1. `rebind` (bind + history retire + cycle-pool bookkeeping) is the largest single stage of a
   kick: **> 40 % of the kick's own time**. Physics inputs (readout + secondaries + tide) land
   at 25–35 %; force arithmetic + quantize together < 10 %.
2. Universe-side plumbing per event (`apply` incl. `root_state`, + requeue) is **20–35 %** of the
   whole-event cost; `root_state` alone stays 6–8 µs (≈ the pilot's 6.8).
3. Within one What class the tail is mild: p99.9/p50 ≤ 5 for kicks (the kick path has no
   data-dependent loops). Across classes, boundaries/opens cost 1.5–4× a kick (they plan the next
   interval: `next_periapsis`, `aligned`, possible bisections).
4. So the event's price is majority "bookkeeping + recompile", minority physics inputs. If (1)
   or (2) fails in the other direction (physics inputs > 50 %), my premise is wrong and the
   dossier says so.

## Experiment B — the per-frame scheduler tax (rekey ladder, N extra Home orbiters)

Held-out cases: the slope ns per kicked body per frame; linearity; behavior with a zero engine
budget (no events resolved); inert bodies (root-doll haulers, no source) as the near-zero control.

5. `advance`'s `rekey` cost grows **linearly** in the number of *planned* bodies (R² > 0.99),
   slope **30–200 ns per body per frame** on this x86 runner.
6. At 10⁶ kicked bodies that slope is **≥ 30 ms per frame** — over the 16.7 ms frame budget with
   **zero events resolved** (budgeted to 0). The tax is paid every presented frame regardless of
   work: a per-frame O(N) claim on the frame, which plane.md foundation 7 forbids
   ("Nothing takes an unbounded synchronous claim on the frame").
7. Control: root-doll bodies with no forces (inert tubes, `key_of` → None) add ≪ 5 ns each to
   rekey (short-circuit before `light_distance`'s sqrt and the heap set). If they cost like
   planned bodies, my "the tax is on planned bodies only" reading is wrong.
8. The belt arithmetic (not a measurement, stated with its assumptions in the dossier): at
   10⁹ bodies, 32 kicks/orbit, 1-year orbits, rtf 100, 4 cores, the allowed event cost is
   ~40 µs — today's x86 event (~50 µs) is the same order. The 10³–10⁵× gap to "billions like
   it's nothing" is not in the event's unit price at belt cadence; it is in per-frame O(N) passes
   (this run) and in cadence for short-period populations.

## Kill criteria for my own claim

- If rekey's slope is < 5 ns/body or sublinear at 10⁵+ bodies, claim B dies.
- If kicks' rebind share is < 25 % and physics inputs > 50 %, claim A's "bookkeeping dominates"
  dies and the event's price is genuinely physical.
