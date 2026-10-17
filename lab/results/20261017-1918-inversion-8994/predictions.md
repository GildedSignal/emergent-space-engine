# Predictions — 20261017-1918-inversion-8994

Written BEFORE the decisive runs (only an N=100 smoke test of the instrument's plumbing may precede them).
The probe: `wave.rs` — the ladder population (`plane_extra`, seed 1, 48 fleet, same draw as gate N1),
budget-free coast (`Budget::unlimited`), rtf 100, drained every frame, horizon 45,000 game-s.
The letter's test is the worst rolling 60-frame (one wall second) mean engine-ms: the shipped 12-ms
budget at 60 fps cannot keep up in any epoch whose 1-s mean exceeds 12 ms (lag grows without bound
there; the BEFORE ladder's 1.667-s lag class). All numbers Linux/x86, orders of magnitude.

## Anchors (already measured on shipped code, no prediction)

- The gate N1 window is 20 s of page time at rtf 100 = **2,000 game-s**; the merged AFTER ladder's
  per-body event columns are therefore the locals' stream divided by N (the belt has had no item yet).
- `belt_first 10000`: the belt's first items at **h p50 14,071 game-s** (belt_first.rs's own header:
  "all are born at tick 0 with one Δs: their first kicks come as one wave") — **7.0× past the gate
  window's end**, at every N.

## Predictions (held-out until after the runs)

- **P1 (wave exists and is N-linear).** A first-item epoch appears between ~8,000 and ~20,000 game-s
  at every N > 0, absent at N = 0. Its event mass ∝ N (I predict total events in the epoch grow
  10× from N=10⁴ to 10⁵ and 3× from 10⁵ to 3×10⁵, within ±20%: the belt is the whole of it).
- **P2 (the locals' floor stands).** At N = 0 over the same 45,000 game-s horizon: worst rolling 1-s
  mean ≤ 4 ms (the locals' comb, the AFTER ladder's own p99 4.1 ms class), no frame over 12 ms after
  the first second except the fleet exodus near frame 61.
- **P3 (the letter's verdict inverts at the gate's own headline).** Worst rolling 1-s mean grows
  ~linearly in N through the wave epoch. I predict it crosses 12 ms between 3×10⁵ and 10⁶ —
  i.e. BELOW the merged gate's N = 10⁶ — so the gate's "N = 10⁶, F1 pass, lag 0" is a property of
  its 20-s window (which ends before the population's first item), not of the flight: at 10⁶ the
  first comb epoch (~140-190 wall-s in at rtf 100) falls behind without bound under the shipped
  12-ms budget. Point prediction: worst60 ≈ 1-3 ms at 10⁴, 3-8 ms at 10⁵, 8-18 ms at 3×10⁵
  (crossing 12 ms only in the upper half of that band); if all three stay under 6 ms, P3 is WRONG
  and the gate's headline extends to the wave — also a result (it closes 917c's letter question).
- **P4 (the steady stream after the wave).** Past the first epoch (~20,000 game-s), the per-frame
  mean settles at the metronome's rate: events/game-s ≈ N × 3.5e-5 × 2 (kick+boundary, the two-comb
  identity), i.e. the letter's steady-state margin at 3×10⁵ is thin (predicted 1-s mean 1-4 ms)
  and at 10⁶ is already over budget (predicted 12-25 ms) even between waves.

## Kill criteria (pre-registered)

- If the wave epoch's worst60 at 3×10⁵ measures ≤ 6 ms AND the N-scaling is sub-linear (< 0.8 in
  log-log from 10⁴ to 3×10⁵), my "gate is window-bounded" claim is killed at the flyable rungs and
  the honest statement is the opposite: the letter survives the first comb to at least 3×10⁵ with
  margin, and the extrapolation to 10⁶ must be stated as unmeasured (memory caps a 10⁶ run here at
  ~2.4 GB > the 2 GB process limit).
- If refusals or dead appear at any rung (belt bodies refused at their first item), the run is about
  that instead: the wave would then be a law event, not a cost event.

## What would make the instrument itself wrong

`frame_to` with `Budget::unlimited` could itself change scheduling (no deadline pressure on the
drain): the control is the N = 0 arm against the AFTER ladder's own N=0 row (p50 0.022, p99 4.15,
max 10.38 ms) over the shared first 2,000 game-s — within 2× on p99/max the instrument is faithful.
