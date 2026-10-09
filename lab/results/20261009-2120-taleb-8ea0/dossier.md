# Dossier — the plane at player-scale horizons (a Taleb rung ladder)

## Claim (one sentence)

The plane carries **no growing compute liability with game time** — canonical work per game-second *falls* with depth (to 3×10⁵ s ≈ 3.5 days), frame-time tails stay bounded, the cut settle never bursts, the digest is canonical at every rung and bit-reproducible across processes — but **the bench's own scripted player is dead past ~1.5–4 h of game time on every script spacing tried**, so no current harness measures a *living* player at player-scale horizons; and memory, flat in time at 428 bodies, shows one unexplained +12 MB decade in the 76-body deep rung.

## Bottleneck

Not a cost bottleneck: a **risk line**. Board/handoff "Risks to attack first" + lens ruin-list ("swap death", "the player plays an hour"): every test and probe stops at ≤ 60 s wall (the `--seconds ≤ 55` guard says so), so *nothing on the record says what an hour-and-beyond of game time does to cost, tails, memory or the flight*. The horizon is reachable inside the rule by raising `--rtf` at fixed wall seconds — the bench's canonical cut (xtask/src/universe/mod.rs:99-102) makes the digest pacing-independent, so rtf is a pure load knob. This rung ladder measures the growing-liability premise directly, on the player's own frame loop (`universe --bench`).

## Evidence

All runs: `./<target>/release/xtask universe --bench --seed 1 --rtf R --seconds S [--unpaced] [--members N]`, release build at 741d05e-lineage main, Linux/x86 shared runner (8 vCPU; per-run machine state embedded in each report; in-container loadavg unavailable — noted). Driver `ladder.py` (RSS polling + timeout + JSONL) → `ladder.jsonl` (16 runs, each ≤ 55 s). Orders of magnitude only, per lab rules; the integrator re-measures on the M1.

**Ladder B (fixed 30 s wall, rtf 1→10⁴ → 30→3×10⁵ game-s):**

| game-s | 30 | 300 | 3 000 | 30 000 | 300 000 |
|---|---|---|---|---|---|
| wall s (process) | 1.6 | 2.0 | 2.0 | 3.4 | 6.6 |
| overflow frames | 1 | 3 | 3 | 5 | 149 |
| RSS max MB | 6.0 | 9.7 | 11.9 | 13.6 | 25.3 |
| gather p50/p99 ms | 0.48/1.01 | 0.83/1.15 | 0.70/0.95 | 1.18/1.41 | 1.69/1.89 |

- **Compute per game-second falls** (~8× per 10× horizon: fixed per-frame costs amortise; events/game-s itself *declines* with depth at fixed rtf: 467→153 events/s from 500→5 500 game-s — cost tracks events, not time or bodies; "compute only surprises", measured).
- **Frame tails bounded everywhere**: worst frame 12–13 ms even at 428 bodies with 550/3 300 frames overflowing the 5 ms engine budget (run C: rtf 1000, 55 s, members 400 — 6× the default fleet): hitches above 16.7/33/50 ms = **[0, 0, 0]**, worst 13.1 ms; the overflow is absorbed as RTF loss, exactly plane.md §7's contract. Digest canonical at every rung.
- **The cut settle never bursts**: gap (process wall − frames wall) 0.05–0.2 s at every rung including 3×10⁵ game-s and members 400 (0.71 s). No unbounded synchronous claim materialised.
- **Memory**: flat *in time* at 428 bodies (63.2 MB at 5 000 game-s vs 63.1 MB at 55 000 — run E vs C), `bytes_per_body` flat (~4.8–5.1 KB at 76 bodies, 6.2 KB at 428). One unexplained growth: 13.6→25.3 MB between 30 000→300 000 game-s at 76 bodies (mechanism not identified; ≈0.14 MB per game-hour — no ruin slope, but it is the only monotone-in-horizon quantity found).
- **Reproducibility**: exact rerun of A(rtf 100, 30 s) reproduced the digest bit-for-bit across processes and load (`41343a14…`, three independent invocations); seed 2 differs (`798c0d9a…`). Controls both sides pass.
- **The flight-envelope cliff (the finding that matters)**: player alive at 5 500 game-s (rtf 100); dead ("You" in `lost_bodies`) at 15 000 (rtf 1000), 15 015 (rtf 273), 16 500 (rtf 550), 55 000 (rtf 1000), and already at 5 000 game-s with rtf 1000 + members 400. Death correlates with the script's game-time burn length (∝ rtf: 33 game-s at rtf 100, 333 at rtf 1000 — the script comment itself warns "a long burn from low orbit ends in the planet") and with depth. The universe resolves canonically either way; but **every probe of a living player's hour-and-beyond is currently unmeasurable with this harness** — the bench's player is a dead orbit past the cliff.

Reproduce the two key cells (≤ 60 s each):
```
xtask universe --bench --seed 1 --rtf 10000 --seconds 30 --unpaced   # 3.5 days of game time, 6.6 s wall
xtask universe --bench --seed 1 --rtf 1000 --seconds 55 --unpaced --members 400  # 6x fleet, worst frame 13 ms, 0 hitches >16.7 ms
```

## Predictions (predictions.md, written before any run)

- P1 (engine cost/game-s flat): **held, stronger than predicted** — it falls.
- P2 (gather is the fragile end, <5× growth): **held as a bound** (≤2.5× to 3.5 days); the gather is not the liability at these emitter counts.
- P3 (tails bounded; overflow > 0 at rtf ≥ 10⁴): **held** (149 overflow frames at rtf 10⁴; 550 at members 400 — and still zero hitches above 16.7 ms).
- P4 (settle grows, dominates around rtf 10³–10⁴): **wrong** — the settle stays ~0.2 s; deferral inside frames, not a cut burst, carries the backlog.
- P5 (memory flat ±20%): **wrong in one cell** — the 76-body deep rung grows +12 MB/decade (mechanism open); held everywhere else, including time-flat at 428 bodies.
- P6 (scripted player survives the hour): **wrong** — dead by 1.5–4 h on every spacing; the cliff confines all live-player measurement to ≤1.5 h.

## What would make it wrong

Cloud/Linux shared-runner timings (orders of magnitude only); the M1 re-measures. The rtf ladder changes the script's game-time burn spacing (burns are ∝rtf longer in game time), so *player-fate* comparisons across rtf are confounded — I report the cliff as a harness limit, not an engine bug, for that reason. The memory growth is one rung pair (30 000→300 000 game-s); a checker should repeat it (and an rtf-10⁵ cell, which I could not fit in the minute) before believing the slope. Cross-hardware bit-identity is untested here (single machine).

## Cost of adopting, and fit

Adoption is a harness fix, not an engine change: give the bench script station-keeping (or depth-matched decision logs) so the player stays alive at player-scale horizons — then the live-gather/thrust/handoff paths become measurable past 4 h. Zero engine risk; it unblinds every future horizon probe (including b-readout-cost and b-h-live, both queued). Fit — PRINCIPLES: "Measure the way the player plays" (#10) and "Compute only surprises" (#3) are the two lines this rung measured; both held on the engine side. The cliff is exactly the lens's point: the instrument died before the machine did.

## The lens (what Taleb made me miss)

This lens hunts fragility, so it nearly missed the *good* news: the budget/deferral spine is the antifragile part — load doubles, frames stay under deadline, backlog becomes RTF loss. By staring at tails I also underweighted the events/game-s *decline* (the quieting universe), which is the board's own thesis working. And the 60-minute budget forced single-cell evidence for the memory slope; a fat-tail lens should have run three seeds per rung — the checker should.
