# Dossier — run 20261009-1936-constraint-8af7 (constraint lens)

## Claim

On main, the frame's constraint is not kicks but the view's readout: the light-cone gather
owns 54–74% of every frame's CPU at the player's rtf, and 97% of it is the tube decode
(`Binding::cartesian`, the exact integer Kepler solve) at ~4.6 µs a call, ~2.5 calls per
emitter per frame — an O(N)-per-frame cost that caps the whole visible universe at ~2×10³
bodies per 16.7 ms frame at rtf 100, six orders short of the goal.

## Bottleneck

The board's focus (1 Oct) says "kicks dominate the engine's cost". True inside the engine —
but the engine is 24–32% of the frame; the gather is 54–74% at every rtf from 1 to 1000 and
at 71 and 410 bodies. Work on kicks buys at most a third of a frame; work on the readout
buys the frame. Expected gain of attacking the named constraint: the gather is ~7.3 µs per
body per frame, of which the decode is ~97%; a per-distinction gather (or a 10× cheaper
decode) removes most of the frame at the current scale and unblocks all N scaling.

## Evidence

All on Linux x86 cloud (8 vCPU, shared): orders of magnitude only; the integrator
re-measures on the M1. Machine state recorded in every run's JSON (loadavg 0.3–1.4).

1. **The whole frame, defaults** (rtf 1, paced 30 s, 39 bodies):
   `xtask universe --bench --seconds 30` — frame p50 3.30 ms, p99 4.94, zero hitches;
   shares: view_gather **73.7%**, view_json 14.8%, wire 6.5%, **engine 5.0%**.
2. **The player's regime, unpaced** (`--bench --seconds 10 --rtf {10,100,1000} --unpaced`):
   rtf 1000 held with frame p50 1.67 ms. Gather share 64–75% at every rtf. Engine share
   rises 6%→29% with rtf but never leads.
3. **Scale** (`--rtf 100 --unpaced --members {48,480,4800}`): bodies cap at 410 (the
   scenario hands out ~430 members; the members axis saturates). At 410 bodies: frame p50
   4.8 ms, p99 10.1 ms, engine-budget overflow on 17% of frames; gather 3.0 ms (54%),
   engine 0.47 ms (32%), view_json 0.66 ms. Gather ≈ 7.3 µs per body per frame, ~linear
   (71→410 bodies: 0.75→3.0 ms).
4. **Inside the gather** (counter-only instrumentation; digest control below):
   bodies loop **99.4%** of gather; fleet-motions loop 0.9%; Newton needs **0.72–1.0
   evals per emitter per frame** (the ViewCache works; the solver is not the problem).
5. **Inside the readout**: `state_rate` = 97% of the bodies loop; per Newton eval it makes
   ~2.5 `Binding::cartesian` calls; **435,648 cartesian calls at 4.59 µs each = 2.0 s over
   600 frames** (the view's `state_rate` accounts for 1.80 s of it; the engine and
   scheduler the rest). The `secondaries` fan-out (sources read per call + a Vec
   alloc) is 6% — not the cost at plane scale. The decode is the exact integer Kepler
   solve: knot binary search + ≤72 iterations of an i128 quadrature (`outbound_at`,
   crates/space/src/orbit.rs:716) plus ~20 fixed-point ops in `read`.
6. **Kicks for contrast** (`--kick-bench --seconds 30 --rtf 100`): resolver median 35 µs
   (made) / 92 µs (leavers); exact memo hit 0%, quantized 95.5% (51 shapes / 1125
   rebinds) — reproduces the 5 Oct finding.
7. **The engine's own tail**: at 410 bodies, player-kind events cost 1,750 µs/item vs
   fleet 29.5 µs (60×) — with 17% of frames overflowing the engine budget, the engine's
   tail is the second constraint, not its median.
8. **Gate** (`behave --law plane`, default gate set, 99.5 s wall; log in
   `logs/behave-plane.txt`): G1–G6, B7, B9–B11 FAIL by construction (answered
   "unanswered/inf" — they judge the `space` compiler, not the plane adapter), B12 shows
   the known miscalibrated statistic, **B13 reproduces the handoff exactly (60/64, worst
   2.12e-2)**, and **B14 consumes its whole 60 s timeout, so B17 never runs**: the plane's
   behaviour suite is paced by one gate's budget. The default gate list invites reading
   those by-construction FAILs as regressions; a checker should pass
   `--gates B12,B13,B14,B17` for the plane.
bench). **Digest control:** members 480 / rtf 100 / 10 s gives
`aadaa1c81e2bcc49123e02d9fbd17de1cb784512de9c6ef30b0f61349fdf1366` before and after
instrumentation — counters change no bit.

## Predictions

Written before the attribution run (predictions.md). Held: P1 (bodies loop ≥55%: 99.4%;
fleet <15%: 0.9%), P2 (evals 0.7–1.0 per emitter ≤2.5; state_rate ≥1.5 µs: 10 µs;
readouts ≥40% of gather: 97%), P3 (gather ~linear in bodies: 3.9× for 5.8×). P4
(allocation <20% of bodies loop) held by arithmetic (3% of the loop is outside
state_rate) but was not separately measured — inference, not observation.

## What would make it wrong

- Measured on the cloud box: shares, not absolute times, carry the claim; if the M1's
  gather/engine ratio differs by >2× the constraint naming could flip back to the engine.
- If the real game view gathers only a culled subset (not every body), the O(N)-per-frame
  cap applies to the visible set, not N; the constraint then re-ranks at the culling
  threshold — but the plane's shipped debug view does gather all alive bodies.
- The 4.6 µs decode is the *exact* integer solve; if a cheaper exact form exists (the
  integrator's motion-law v2 owns that question), the constraint moves as claimed in
  "next".

## Exploit, subordinate, elevate (the lens's discipline)

- **Exploit (cheapest, no law change):** the decode is re-run from a knot-linear start
  every call; the crossing root (already memoized per emitter) makes consecutive frames'
  elapsed times monotone, so the previous frame's converged `psi` is a warm start inside
  the same knot bracket — same integer answer, fewer quadrature iterations. Second: the
  two extra `cartesian` calls per eval come from `partial`'s mid-point field read
  (observe.rs:142-152); a reader past a kick boundary re-derives what the engine already
  derived when it timed the kick.
- **Subordinate:** nothing else should get attention while the gather leads: kick work
  (6.5× under the gather at rtf 100), the changeover, encounters — all mirages at frame
  level until the readout is per-distinction. The engine's 5 ms budget already exceeds
  the gather's whole claim; its 17% overflow frames are the player-kind tail (1.75
  ms/item), not its median.
- **Elevate (the structural move, already queued as "the readout's cost"):** make the
  gather per-distinction, not per-body: re-derive an emitter only when one of its
  observables (direction, colour, brightness) crosses a perceptual quantum — the light
  cone as an event queue ("compute only surprises"). Target: per-frame view cost ∝
  distinctions created per game-second (H_live), not bodies.
- **Where the constraint moves next:** after the gather, to view_json+wire (0.84 ms,
  17%, itself per-emitter serde work), then to the engine's tail (player-kind events,
  60× a fleet item), and only then to kicks' median.

## Fit with PRINCIPLES

- "Compute only surprises. … Nothing is evolved that can be derived when looked at
  (clocks, redshift, views)" — the view derives, but re-derives every emitter every
  frame regardless of whether anything the player can distinguish changed.
- "The right question, then the representation … we just need to have the right
  representation so that math is trivial" — the exact integer Kepler solve is re-paid
  per body per frame; the representation (a per-distinction view over the tubes) is the
  open question.
- "A fix signals the wrong representation" — the 5 ms engine budget and the kick
  cadence are not where the frame is lost; tuning them now would be the bandaid.
- "Priority is slack, not proximity" and "the zoom level is the minimap" — a
  per-distinction gather is exactly slack-ordered view work.

## The lens

The constraint lens trusts totals over opinions, and totals here are one frame loop on
one scene: the scenario caps members at ~410 (the belt, B18b, is the real N axis and was
not run — 60 minutes), the cloud box is not the M1, and one harness measured everything
(the digest control and the kick-bench's agreement with the 5 Oct note are the only
independent cross-checks). What the lens may have missed: whether the gather's share
holds when the browser and HTTP enter (wire here is serialisation only), and whether
`behave`'s plane gates hide a cost the bench never reaches. The instrumentation patch is
this run's own; counters read to zero cost nothing if the integrator keeps them.
