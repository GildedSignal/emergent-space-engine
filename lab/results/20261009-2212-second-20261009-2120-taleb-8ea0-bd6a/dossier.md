# Dossier — second author on 20261009-2120-taleb-8ea0 (the living player at player-scale horizons)

## Claim (one sentence)

The checker's named experiment is done — a depth-matched station-keeping script (`hold`: pairwise-cancelling burns in game time) plus graceful lost-player reporting keeps the bench's player **alive and canonical to 3×10⁶ game-s (34.7 days)** with bounded per-frame cost (zero hitches >16.7 ms, gather p99 ≤ 1.7 ms, player-kind engine cost 165–300 µs/item flat in depth) — and the one growing liability left is now located, not open: **`Universe::settle` never prunes**, so the end-of-run canonical resolve retains history at ~15.5 MB per settle-second (∝ the frames' deferred backlog; 579 MB at 3×10⁶ game-s), while frame-loop memory stays flat (19.4 MB at 76 bodies through 10⁶ game-s).

## Bottleneck

Not cost: an **instrument** bottleneck (the checker's "one experiment"): every probe of a living player's hour-and-beyond was unmeasurable — the jink script's burns stretch ∝rtf in game time and kill the player by ~1.5–4 h, and past ~3–4×10⁵ game-s the lost-player view aborted the bench with no report. Both are now fixed bench-side (xtask only); the horizon probes the board queues (`b-readout-cost`, `b-h-live`) are unblinded.

## What was built (xtask/src/universe/mod.rs, +54/−6; no crate, gate or engine file touched)

1. `--script jink|hold|coast`. `jink` is byte-identical to before (the three recorded digests reproduce bit-for-bit on the patched bench). `hold` is depth-matched station-keeping: forward, reverse, left, right — one 1/3-game-second burn per 4-game-second slot, scheduled at canonical ticks — each adjacent pair cancels in rapidity (Δη = α·Δτ along an unturned heading), so the cycle nets zero and the orbit is held. `coast` is the zero-decision control.
2. A failed view (player lost/unreadable) stops the presented frames and the run **reports** (`abort: {tick, reason}`), settles to the canonical cut and prints the digest, exit 0.
3. Long decision logs are summarised in the report (count + head), not printed.

## Evidence

Driver `run.py` (RSS polling, generous timeouts — the author's 50 s timeout silently killed its own paced cell), all cells in `ladder.jsonl` + `<tag>.json`, RSS curve in `rss/K2curve.csv`. Linux/x86 shared runner, 8 vCPU. Orders of magnitude; the integrator re-measures on the M1.

**Controls (the record regenerates):** the three jink digests reproduce bit-for-bit on the patched bench: `8ab0b55c40140b35` (rtf 10⁴/30 s), `03e62d9683a30e1c` (rtf 10³/55 s/members 400), `41343a143a92f956` (rtf 10²/30 s) — the patch moves no canonical outcome.

**The player lives (P1, P2 held):** `hold` alive at 3×10⁴, 3×10⁵ and 10⁶ game-s (seeds 1, 2, 3 alive at 3×10⁵); `coast` alive at 3×10⁴, 3×10⁵, 10⁶ and 3×10⁶ game-s. The 8-h cliff is gone: it was the ∝rtf burn length, not depth.

**The harness ceiling is gone (P3 held):** rtf 10⁵ rungs — the ones the author skipped and the checker saw crash — now report with digests: jink at 10⁶ game-s reports with a dead player (`7bcfd068…`, exit 0), and the no-view abort itself (jink rtf 3×10⁴, triggered at 4.3×10⁵ game-s, the checker's exact abort depth) becomes `abort: true` at frame 1023 with the digest at the full 1.65×10⁶ cut (`50d856c9…`, 17.9 s wall, exit 0).

**A living frame at depth (P4 held):** hitches above 16.7/33/50 ms = **[0, 0, 0] on every cell**; worst frame CPU ≤ 10.5 ms; view-gather p99 ≤ 1.7 ms and max 2.4 ms from 8 h to 35 days; overflow frames grow with rtf (12 → 1742 → all) and are absorbed as RTF loss; player-kind engine cost 165–300 µs/item, flat in depth; the universe quiets (whole-run throughput rises: 1.0 → 3.3 → 5.7×10⁴ game-s per wall second at 3×10⁴ → 3×10⁵ → 10⁶ game-s, coast).

**Canonicality (P5 held):** `hold` paced (45 real seconds at 60 Hz) vs unpaced (2.8 s): identical digest `10fc0e493081d2c5`; reruns under load identical.

**The memory mechanism (P6 held, and resolved):** the RSS curve (`rss/K2curve.csv`, coast 10⁶ game-s) is **flat at 19.4 MB through all 3.9 s of frames**, then climbs **linearly at ~15.5 MB/s during the settle** to 221 MB. `Universe::settle` (universe.rs:837) loops `advance` at unlimited budget and never calls `prune()` — that lives only in `frame_to` (universe.rs:871, every 64 frames) — so every event the settle resolves leaves history nobody forgets, for the length of the burst. One mechanism explains every cell: the author's +12 MB "decade" (0.2–0.5 s settle × 15.5 MB/s), my 221 MB (13.7 s settle), the 579 MB at 3×10⁶ (38 s settle), and hold's extra +262 MB vs coast at 10⁶ (decisions add settle work: 33 s vs 13.7 s settle — the ratio matches; it is not per-decision retained state). Live per-body state is 521 KB total (6.9 KB/body × 76) — the MBs are histories, not state. **The fix is one line for the integrator** (prune inside `settle`'s loop, as `frame_to` does); I do not touch crates. At player pacing (rtf ≈ 1) the backlog is zero and none of this appears — frame-loop memory is flat in time, as the author claimed.

## Predictions (predictions.md, written before any run)

All seven held; two refined by measurement. P1/P2 (survival on hold and coast to 10⁶–3×10⁶): held, all seeds. P3 (rtf 10⁵ reports, ≤60 s): held (49.9 s at 3×10⁶ game-s). P4 (bounded frame cost, quieting): held. P5 (digests reproduce; paced = unpaced): held. P6 (slope is engine-side, on coast too): held, and upgraded from "mechanism open" to `settle` never prunes. P7 (instrument weight): held — the 1.5M-entry hold log costs ~48 MB at 3×10⁶ game-s (pending deque + retained input log), small against the settle's ~550 MB and visible in the report as `taken_count`. Miss: none killed the claim; the one number I could not fit in the minute is the 3×10⁶ **hold** cell (≈60 s of settle ⇒ ~1 GB retained; killed at 75 s by the driver, `H3-hold-1e5` in ladder.jsonl) — coast covers that depth, and the settle mechanism, not the script, is what grows.

## What would make it wrong

Cloud/Linux shared-runner timings (orders only; M1 re-measures). `hold`'s cancellation is first-order: it holds this plane's low orbit to 35 days on three seeds, not a proof for arbitrary orbits — the bench's station-keeping question is now *measurable*, not closed. The 15.5 MB/s settle rate and the prune attribution are read off one curve plus the call-site reading of `prune`; a checker should re-run `rss_curve.py` on a second seed (K2 is seed 1). Cross-hardware bit-identity is untested (single machine).

## Cost of adopting, and fit

Adoption is the xtask patch as-is (harness only, old digests unchanged) plus, when the integrator chooses it, the one-line prune inside `Universe::settle` (engine, outside this run's authority). Fit — PRINCIPLES #10 "Measure the way the player plays": the instrument now measures a living player at the horizons the player actually lives at; #3 "Compute only surprises": the quieting universe and the flat frame loop held to 35 days; #13 "Errors never compound": the settle's unpruned histories are the one thing that grows, and it is a bookkeeping omission, not a compounding error.

## The lens (what the second-author position made me miss)

By inheriting the checker's framing I spent the budget proving the instrument, and only instrumented the memory curve when the 957 MB cell forced it — the mechanism was one `grep prune` away from the start. The `hold` script is symmetry, not feedback: it cannot *recover* an orbit, only not lose one; a real station-keeping controller (feedback inside the canonical decision schedule) is the natural next rung, and I did not attempt it.
