# Dossier — 20261009-1210-constraint-c10d (lens: the constraint)

## Claim

The plane's frame constraint is not the engine (kicks) but the view's per-body light-cone
crossings: 66–84% of frame CPU, 97% of the gather, ~16 µs per visible body per frame and
linear in N — so the view, not the engine, is the wall between the plane and the goal's
scale, and the queued readout-cost fix (2.6×) moves the wall by less than one order of
magnitude.

## Bottleneck

Board focus line 1: "fewer kicks per orbit … kicks dominate the engine's cost". Measured on
the whole flown plane, the engine is 4.7% (rtf 1) to 23% (rtf 100, 71 bodies) of frame CPU
and **falls to 6% as bodies grow** (299 bodies): the view gather takes 64→84%. Within the
gather (probe patch, section timers): per-body crossing searches are 97% (2,001 ms of a 30 s
run; player readout 68 ms, fleet members 31 ms). Each crossing is a warm Newton bracket at
0.9–1.55 readouts per body per frame (cache warmth measured), ~14 µs per readout through
the motion-law v2 partial-step path. Expected gain from fixing the representation: the
view's cost must track *changes* (arrival-rate-carried crossings, re-bracketed on threat),
not bodies — the same cadence move the engine already made (kicks per orbit, not per tick);
order 10× at today's N, and it deletes the O(N)-per-frame wall entirely (the ceiling moves
from ~10³ visible bodies to whatever the change rate allows).

## Exploit, subordinate, elevate (the lens's step 3)

- **Exploit the constraint as it is:** the ViewCache already carries each emitter's root
  and arrival-rate slope (`ViewCache::put`); the crossing is re-bracketed every frame only
  because nothing certifies the carried guess. The cheapest change is a certificate: carry
  each crossing as an event advanced by the arrival rate, re-bracket when the rate's own
  motion can have moved the bracket (the same exactness argument the slack skin owes), and
  extrapolate between re-brackets exactly as the fleet loop already does (0.1 µs/member).
- **Subordinate:** the engine's 5 ms budget already yields; nothing else starves the view.
  The readout-cost build (b-readout-cost) should be subordinated to this — it shrinks the
  re-bracket's cost but leaves the per-body-per-frame charge, which is the wall.
- **Elevate:** only if the certificate cannot be made exact does the readout path need a
  bigger part (a cheaper tube read); try the certificate first.

## Evidence (all commands ≤ 60 s; Linux/x86, orders of magnitude only)

Machine: GitHub Actions runner, 8 vCPU shared; load 0.4–1.2 during runs; digests identical
across repeated runs. Run-to-run p50 swings ~4× (3.5→0.85 ms, same digest) on this box, so
all claims use within-run shares and slopes, never cross-run absolutes.

1. Whole plane, as the player runs it (`cargo run --release -p xtask -- universe --bench
   [--rtf 100]`, 30 s each; `bench-rtf1.json`, `bench-rtf100.json`):
   - rtf 1: gather share 0.739, engine 0.047; frame p50 3.3 ms, 39 bodies.
   - rtf 100: gather share 0.697, engine 0.175; 76 bodies; kicks 1360, engine_cost_by_kind:
     fleet 57 µs/item, ship 309 µs, player 1412 µs; planets/moons 0 (compiled drift).
   - kick-bench: kick resolver median 50 µs (p99 62), leaver rebinding 369–443 µs.
2. Gather split (probe patch, this run's `work/patch.diff`): body crossings 2000.7 ms,
   player 67.9 ms, fleets 31.0 ms over 30 s at rtf 100 → **97% of the gather is the
   per-body crossings** (`bench-rtf100-probe.json`).
3. Scaling sweep (`sweep-haulers-{12,60,240}.json`, `--rtf 100 --seconds 10`,
   `PROBE_HAULERS` probe): body crossings 2.75 / 3.63 / 6.51 ms per frame at 71 / 119 /
   299 bodies → **16.5 µs per visible body per frame, linear** (18.2 then 16.0 µs on the
   two intervals); gather share 0.64 → 0.74 → 0.84 while engine share falls 0.23 → 0.15 →
   0.06. `gather_last_readouts` 66/150/465 → 0.9–1.55 readouts per body per frame.
4. Fleet members, the existence proof in the same code (`sweep-members-{4,400}.json`):
   0.005 → 0.042 ms per frame for 4 → ~390 in-frame members ≈ **0.1 µs per member** — the
   extrapolated retarded-time read (no Newton, no partial-step readout) is ~150× cheaper
   per emitter than the bodies' crossing path. Members cost the view only when they leave
   the frame and become bodies (bodies_end 32 vs 409).
5. Fermi to the goal: at 16.5 µs/body/frame the view alone eats a 16.7 ms frame at
   ~1.0×10³ visible bodies; with b-readout-cost's 2.6 µs readout and 1.2 readouts, at
   ~5×10³. Billions of bodies need the view's cost on changes, not on N.
6. Gates (`behave --law plane`, `engine-judge`, this box): the plane fails G1–G6/B7/B9–B11
   *by design* (it answers None outside its boundary, plane.rs's own note); B12 FAIL (the
   known miscalibrated statistic, redesign in flight), B13 FAIL 60/64 judged within 1e-2
   (matches HANDOFF), B14 FAIL on a 60.1 s timeout over the 60 s limit (this shared box;
   B16/B17 were not reached after it). engine-judge: E1–E5, E7, E8 PASS; E6 UNSUPPORTED
   (no prepared-mutants.json here); E9 FAIL phase 1 as designed. No surprise against
   HANDOFF — the constraint story above does not rest on them.

## Predictions

`predictions.md` was written before the sweep. Held: (1) linear per-body slope (16.5 µs,
intervals 18.2/16.0); (2) members ~40× cheaper (measured ~150×, even stronger); (3) warm
crossings 1–2 readouts (0.9–1.55). Partially held: (4) ships vs planets per-kind split not
measured directly — readouts are counted per gather, not per kind; the engine's cost split
(planets 0 ns, ships 309 µs/item) and the code path (crossing → `state_rate` → partial
step) support it but this run does not isolate it. Held: (5) ceiling at ~10³ visible
bodies (order of magnitude).

## What would make it wrong

- If the view's per-body cost is not what frames wait on at scale (e.g. the engine's kick
  load grows superlinearly with N and retakes the frame first) — but at 299 bodies the
  engine share is *falling* (6%), not rising, and kicks scale with events per orbit, not
  per frame per body.
- If crossings cannot be carried exactly by the arrival rate without re-bracketing every
  frame (the bracket g(t) ≤ 0 < g(t+1) needs the worldline's curvature bound; a proof is
  required, same shape as the slack skin's exactness argument). The 0.9–1.55 warm readouts
  say the guess is already good; the exactness of skipping the readout is unproven here.
- If the player's differentiation floor lets emitters be batched coarser (angular radius,
  luminosity quantisation), the win could be even larger than 10×; not measured here.

## Cost of adopting, and fit with PRINCIPLES

Adoption is a design change to the view, not code: crossings become events carried by the
arrival rate (the cache already holds root and slope — `ViewCache::put`), re-bracketed when
the rate's motion threatens the bracket, exactly as kicks are paid per element change. It
composes with b-readout-cost (cheaper readouts still help the re-brackets). PRINCIPLES:
"Compute only surprises … Nothing is evolved that can be derived when looked at (clocks,
redshift, views)" (#3) — the view re-derives every crossing every frame; "The view is an
instrument" (#28) — its cost must sit at the player's differentiation floor, not at N;
"The right question, then the representation" (#18).

## Where the constraint moves next

Once the view tracks changes: to the readout's per-eval cost on the *re-bracket* path
(b-readout-cost, already queued — the two compose), then back to the engine's kick cadence
at N (the board's line 1), which retakes the frame once the view stops charging per body
per frame. At the far end, the wire/JSON (7–15% today, every emitter re-serialised every
frame) becomes the next fixed-per-N cost.

## The lens (what it may have made me miss)

Goldratt's lens reads one constraint off the dashboard; it can miss costs that are not on
the dashboard at all (H_live, memory footprint at 10⁹, the encounters tier — none exercised
by the plane at 39–299 bodies). The sweep's universe is still one star system; the
"visible bodies" slope says nothing about bodies too dim to see (the gather walks them
anyway — that is part of the finding, but the dim-emitter cull is unmeasured). Machine
variance on this shared box is 4× on p50s; slopes and shares only.
