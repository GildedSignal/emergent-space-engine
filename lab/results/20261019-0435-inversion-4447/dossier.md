# Dossier — 20261019-0435-inversion-4447 (inversion)

## Claim

The burn-mode memory ratchet on the shipped ladder is **unbounded in play time and ~K-proportional
mid-flight**: a single held L8 burn takes RSS 41→1,601 MB by 560,764 game-s at K=10⁴ (guard-stopped
while still climbing 3.4 MB/1k game-s) and hits the same 1,601 MB guard by 332,604 game-s at 3×10⁴ —
so d839's checker's "then flat" was truncation (the flight ended inside the 40–60k local plateau),
and dcf1's "the burn-mode byte wall is gone on current main by ~3 orders" held only inside the
pre-departure window (their flight ended at the SOI switch, frame 948, the phase boundary where
this ratchet begins).

## Bottleneck

Board item "memory at 10⁹" / the memory wall of the N ladder (28→10⁹), and the failure mode my lens
hunts: **memory that grows with play time** (one wall-hour of held L8 = 989 MB at 10⁴, ~1.6–2.2 GB
at 3×10⁴). The approved plan's frozen budgets (4 GiB, 30 FPS, one hour, 20 GiB — HANDOFF: "open,
not dropped") survive one hour only ≈2.5× at 3×10⁴; on the two-point mid-flight K-scaling the 10⁵
rung breaches 4 GiB in ~70k game-s ≈ 12 wall-min [INFERENCE]. Nothing to build here: the record's
named fix (b77d-1fcf/b8e2/acf2 — count pinned bytes at capture + answer-or-expire at a game-s
cadence) is simply not on main, and this flight prices its absence.

## Evidence

All numbers regenerate with `bash lab/results/20261019-0435-inversion-4447/regen.sh` (~7 min warm;
three flights 86/139/73 s — over the 60 s guide, disclosed: the question is a long-horizon one;
each flight is a single unpaced run of the shipped `nladder` loop). Instrument: my patch to
`crates/universe/examples/nladder.rs` (work/patch.diff) — the lab's standard Linux `/proc`
footprint replacement (the shipped `proc_pid_rusage` cannot link here) plus three env-gated gates,
off = the shipped loop: `LADDER_PROBE` (one line per 500 game-s: gs, VmRSS, VmHWM, held_scans,
frame events), `LADDER_CAP_S` (wall cap, default the shipped 55), `LADDER_RSS_MB` (stop when
VmHWM passes it — my 2 GB process guard). Seed 1, rtf 100, engine budget 12 ms, sequential flights
on a quiet box (load 0.08 before, 0.87–1.14 after — my own flights; 8 vCPU).

- **A1, burn K=10⁴** (`nladder 10000 burn 8000 100 12`, 1,119 probes): RSS 40.7 MB @ 0.5k gs →
  1,601 MB @ 560.9k gs, monotone, guard-stopped while still climbing; last-mile slope
  (558.9→560.9k) = 3.4 MB/1k gs. Window slopes (MB/1k gs): 1.1 (0–15k) / **5.7 (15–40k)** /
  **0.8 (40–60k — the local plateau d839's checker's flight ended inside)** / 1.7 / 2.3 / 2.9 /
  **3.2 (400–561k)**: the slope dips once, then **rises**; final-40% = 3.0 ≥ my pre-registered
  ratchet bar of 2.
- **A3, burn K=3×10⁴** (d839's checker's exact arm, 664 probes): guard at 332,604 gs; windows
  4.4 / **16.3 (15–40k — reproduces their 13–16 exactly)** / 1.1 / 2.9 / 3.0 / **4.6**: the
  mid-flight slope is ~K-proportional (5.7→16.3 for 3× the bodies); no saturation; late slope
  rising.
- **A2, coast control, same binary, same horizon** (`10000 coast 8000 100 12`, 480,000 frames,
  800,010 game-s): RSS 27→70 MB, slope 0.02 MB/1k gs, held_max = 1, 0 frames over budget. The
  negative control passes: the ratchet is burn-specific, the instrument sound.
- **Mechanism census (both burn arms):** `held_scans` grows monotonically and never latches
  (741 / 589 at the guard; SCAN_BACKLOG 2048 never engaged); RSS/held compounds 0.2→2.16 MB
  (10⁴) and 0.9→2.72 MB (3×10⁴); the growth lives outside the dashboard's accounting (bpb
  18,827 B/body ⇒ 189 MB of 1,601 at 10⁴ — the dashboard under-counts ~8.5×, confirming 4a71's
  ~12× note on a different channel; catalogue constant 10,076/30,076; build per-body constant
  2,463/2,372 B). The player is interstellar from gs ≈ 1.6k (doll 0 at frame 948) and the ratchet
  runs 560k game-s past departure: **the mint channel does not need the belt near** — dcf1's
  "~300 locals cap the candidates" (radial index) held only while the player was inside the
  system.
- **Budget arithmetic** (final-slope extrapolation; a lower bound on urgency since slopes rise):
  4 GiB at ~1.39M game-s ≈ 3.9 wall-h (10⁴) and ~880k game-s ≈ 2.4 wall-h (3×10⁴); one wall-hour
  of held L8 (360k game-s at rtf 100) = 989 MB (10⁴, probe line `gs=360… rss_mb=988.8`) and
  ~1.6–2.2 GB (3×10⁴, guard-level at 332.6k).
- **The frame channel is mild at these K** (not 4a71's O(N)-walk pin): 66–69 frames over 12 ms of
  200k–336k (0.02–0.03%), p99 4.1–4.7 ms, worst 42.5 ms; events 2.0M, kicks 1.0M, refusals 0,
  player alive throughout.

## Predictions

Written before any flight, including calibration (`predictions.md`). P1 (final-40% slope ≥ 2 ⇒
ratchet, no plateau): **held** (3.0 at 10⁴, 4.6 at 3×10⁴). P3 (coast flat ±2 MB): **held** (0.02
MB/1k gs). P5 (no scene-exhaustion before 100k gs; the interstellar state does not stop the mint
channel): **held** — growth ran to 561k gs with the player gone from 1.6k. P2 (growth rides
held_scans, RSS/held of constant order 0.1–3 MB): **half-held** — the channel is the scan
channel's (held 0 ⇒ flat; held grows ⇒ RSS grows; catalogue and build-per-body constant), but
RSS/held is not constant: the per-retained-scan bytes compound (0.2→2.16 MB), so the b8e2
constant-pin queue model needs a growing-retention term on this horizon. P4 (over-budget frames
not decreasing): qualitative only — the probe did not log per-frame ms; the ladder line's totals
and the worst-frame list (first over at frame 11,094; worst cluster 102–106k) point the right way,
0.02% absolute. My P2 band "0.1–3 MB" was tuned on nothing (no prior RSS/held datum existed) — it
happened to contain the late values and miss the early ones.

## What would make it wrong

- A counting-GlobalAlloc census could attribute the bytes differently inside the scan channel
  (capture Vec vs dead-candidate Entry retention, b77d-1fcf's split): my instrument pins the
  channel (held-conditional, outside the dashboard) but not the internal split.
- The 10⁵ breach time rides a two-point K-scaling of the mid-flight slope; a 10⁵ flight (build
  2.34 GB > this box's 2 GB cap) would settle it.
- rtf/budget are the utilization knob (b8e2): the ratchet's *rate* is convention-dependent; the
  *unboundedness* verdict is not (both arms still climbing at the guard, coast flat).
- If the drain's answer cadence under a paced player loop differs from this unpaced loop, the
  absolute slopes move; the page's own convention (rtf 100, 12 ms, unpaced nladder) is what I flew.

Cost of adopting: nothing to adopt — it kills dcf1's "wall gone" outside its domain and restores
the fence (byte-count at capture + answer-or-expire) as a live requirement before any long burn
is flown at 10⁵+.

PRINCIPLES fit: 13 ("basically we don't want errors that can compound that's the goal") — here it
is memory, not state error, compounding on the one wildcard (5: "the player is the only wildcard");
25 ("not making mistakes matters more than doing things efficiently, don't multiply by zero") —
the unfenced burn is a ruin path, and the cheapest compute is compute not done (1): the fence
deletes the retention, not the answers.

## The lens

Inversion asked how the memory story fails when played long, and the record's own two same-day
readings were the contradiction to resolve: both were short-horizon truncations of one wave-shaped
ratchet (d839's ended inside a local plateau, dcf1's ended at the phase boundary). What the lens
may have missed: the byte-level mechanism inside the scan channel (needs the counting-allocator
census), the paced-loop rate, and 10⁵ itself.
