# Dossier — 20261018-1717-fermi-dcf1 (Fermi lens)

## Claim

**The burn-mode observer wall that sizes the scan fence is dead on current main by ~3 orders of
magnitude: at K = 3×10⁵ under continuous L8 burn (and at the adversarial 5 ms corner, and across
the SOI doll switch) the per-mint (K+38)·224 B byte law no longer touches memory at all (VmHWM
slope K-flat at 0.026 MB/game-s where the law predicts 47 MB/game-s), held scans stay bounded
(≤ 187 ≪ the 2,048 cap), zero frames exceed the page's 12 ms budget, and the first N-growing
terms at the ladder are now the build's 2,340 B/body and the view gather's 5.0 µs per seen body
(seen = N+61: every ladder body is in the player's view), linear to 1.5 s at 3×10⁵ — ~5 s per
gather at 10⁶.**

## Bottleneck

The board's top item (bodies in the flyable engine: which term breaks first as the plane grows).
The load-bearing number under test was taleb-2403's fence-sizing inference — "the 8 GB-at-687-game-s
wall at 10⁶ rescales to ≈ 51 game-s under continuous L8 burn" — which chains acf2's coast byte law
(bytes_touched = λ·(K+38)·224 B per game-s, 8 GB at 687 game-s at 10⁶) onto the measured burn mint
multiplier (13.5× coast). The inference rode the unflown decade 10⁵→10⁶ (the 10⁶ build alone is
~2.4 GB, over this window's process cap) and was marked [INFERENCE] on the nladder page. Expected
gain from testing it: either the fence's cadence really must be sized for >6–14 answers/game-s at
10⁶ (a design constraint), or a whole worry is deleted and the ladder's breaking terms re-rank.
This run measures the unflown interior rung 3×10⁵ and finds the second: **the worry is deleted
(not the fence — b8e2's byte-counting-at-capture remains cheap insurance, but nothing under burn
pressure it at this scale on current main).**

## Evidence

Seven flights of the shipped ladder harness (`cargo run --release -p emergent-universe --example
nladder -- <N> <coast|burn> <s> [rtf] [budget_ms]`; the page's own protocol: frame_to, 12 ms
engine budget, rtf 100, seed 1, one process per flight) on this tree = main + a print-only probe
(`/proc/self/status` VmRSS/VmHWM per frame instead of the macOS-only `proc_pid_rusage`; one probe
line per frame; nothing else changed — work/patch.diff). Linux/x86, 8 vCPU, load 0.7–1.3
(state.txt), orders of magnitude only.

| flight | game-s | p50 ms | p99 ms | over 12 ms | held max | HWM MB | HWM MB/game-s | law predicts |
|---|---|---|---|---|---|---|---|---|
| 1e4 coast | 497 | 0.04 | 5.6 | 0 | 1 | 28→34 | 0.012 | 0.11 |
| 1e4 burn | 497 | 1.04 | 10.6 | 0 | 17 | 28→41 | 0.026 | 1.6 |
| 1e5 burn | 497 | 0.99 | 10.6 | 0 | 13 | 238→251 | 0.026 | 16 |
| 3e5 coast | 497 | 0.05 | 6.3 | 0 | 1 | 705→711 | 0.012 | 3.4 |
| 3e5 burn | 497 | 0.99 | 10.6 | 0 | 13 | 705→718 | 0.026 | 47 |
| 3e5 burn 16 s (crosses the doll switch at frame 948) | 1,497 | 0.76 | 10.8 | 0 | 187 | 706→731 | 0.017 | 47 |
| 3e5 burn, 5 ms corner | 483 | 1.11 | 5.1 | 4 over 5 ms | 130 | 705→718 | 0.027 | 47 |

(summary.txt = analyze.py over logs/*.log; "law predicts" = λ_coast 0.0526 / λ_burn 0.728 per
game-s × (K+38)·224 B.)

1. **The retention/touch law is gone, not just the retention.** A single old-law mint at 3×10⁵
   materializes (3×10⁵+38)·224 B ≈ 67 MB of candidates Vec (written pages, resident while alive);
   one such transient would lift VmHWM by ≥ 67 MB. Total HWM growth over whole flights is
   6–26 MB at every rung, coast and burn — K-flat at 0.012–0.027 MB/game-s. The per-mint O(K)
   walk no longer touches the window's row set on this tree. Mechanism [INFERENCE, from the
   flyable-frame page's "2df1's row-set deletion, wired"]: the capture stopped materializing the
   full candidate row set; this run did not date the merge.
2. **The fence-sizing inference's number dies with it.** At the measured slope, 8 GB of scan pin
   at 10⁶ is ~300,000 game-s away (0.026 MB/game-s), not 51 game-s — off by ~4 orders. Held scans
   stay bounded everywhere: 13–17 (6-s burns), 187 (16-s burn, across the doll switch — the
   backlog forms and drains), 130 (5 ms adversarial corner). No pin approaches the 2,048 cap.
3. **The engine frame is N-flat and the player's stream is byte-identical across K.** p50/p99 at
   1e5 burn = 0.99/10.62 ms and at 3e5 burn = 0.99/10.61 ms; kicks 1,495, events 5,527,
   boundaries 1,398 identical digits at both rungs (2403's seed-identity finding extends across
   K: the burn's event stream is structural, K-independent); zero frames over 12 ms at the page
   budget in every arm.
4. **What does grow with N, measured at 1e4/1e5/3e5:** the build (0.43 s/27 MB → 4.3 s/237 MB →
   13.4 s/705 MB; 2,340–2,459 B/body — 2.34 GB at 10⁶, the known unflown rung on this box, and
   the compact-store question at 10⁹), and the view gather: seen = N+61 (every ladder body is in
   the player's view), warm 51.4 / 502.5 / 1,502.7 ms = **5.0 µs per seen body, linear** — ~5 s
   per gather at 10⁶, ~5×10³ s at 10⁹. On current main the view gather, not the scan pin, is the
   ladder's first N-growing per-body term (the view page's domain; 0d46's ~300× gather deletion
   was refuted there).
5. **Reconciliation with the record.** 2403's own checker arm (10⁵ burn, 5 ms corner: held 705,
   footprint 237→274 MB) already retained ~52 kB per held scan — ~430× under (K+38)·224 B at that
   K; the inference chained that era's byte law onto the new-code mint rate. The mint *rate*
   (13.5× burn/coast) is not contradicted by this run — my instrument cannot count mints answered
   within their frame of arrival (held-polling lower bound only: ~0.13/game-s over 1,497 game-s);
   what is dead is the per-mint byte term the fence sizing multiplied it by.

**Reproduce** (regen.sh, ~5 min: patch applied, build ~16 s cached, 7 flights, analyze):
`lab/results/20261018-1717-fermi-dcf1/regen.sh` → prints summary.txt row per flight.

## Predictions

predictions.md was written before any flight (the build was still running). Outcome:
- The pre-registered kill criterion FIRED: "if the slope is neither ≥ 10 MB/game-s nor accompanied
  by held → 2,048 pinning, the page's law is missing a term at this K." Slope 0.026, held ≤ 187:
  the missing term is the row-set deletion (the per-mint O(K) touch itself).
- My own lean (H_A's slope at coast, "H_A appears but saturates at the cap") was WRONG at coast
  too: the touch law is dead in every arm, not saturated. Reported as held.
- Held band prediction (50–800, no pinning): held (measured 13–187) — direction right, band
  high; P5's "most burn frames over 12 ms" was wrong (0 over; the engine cuts work and stays in
  budget); P7's build 6–12 s: 12.9–13.5 s, edge-hit.
- λ and the burn/coast ratio: not measurable with this instrument (in-frame answers invisible) —
  disclosed, not claimed.

## What would make it wrong

- A **paced, loaded** flight (470f/b8e2's wall-owned-cleanup domain) could still pin: my claim is
  scoped to the per-frame budget/service law on a quiet box. But the per-frame budget (12 ms from
  each frame's start) is identical paced or unpaced — pacing only sleeps between frames — so the
  drain's service opportunity per frame is the same; the load axis is the open one.
- If the bench's mint path (`universe --bench`, the player loop 2403 timed) mints through a
  different item than the ladder's `frame_to` loop, the burn rate could differ; the byte-law
  refutation (HWM never spikes 67 MB at 3e5 in any arm) is path-independent.
- If the row-set deletion is reverted or the capture regains an O(window) materialization, the
  wall returns at the law's slope; this run's numbers date main at 17:17, 18 October.

Cost of adoption: none — a deletion of a sizing constraint (the fence no longer needs the burn
multiplier as a memory term; b8e2's answer-or-drop and byte-counting-at-capture remain as cheap
insurance). The re-ranking it forces: the next measured walls at the ladder are the build's
kB/body and the view gather's 5 µs/seen-body — both already owned elsewhere (memory-h-live, view).

PRINCIPLES fit: "Build the simplest falsifying test first" and "A test that cannot fail is a
control" — the inference sized a fence for a wall never flown at the rung it sized; seven
flights, ~3 minutes of compute, falsified it. "The best part is no part" — the deletion (row-set)
deleted the wall; the fence debate it drove is now moot at this scale.

## The lens

The Fermi lens catches estimates that disagree by >10× with reality; here the disagreement was
~1,800× and the error was *chaining constants measured on different code eras* (an old-code byte
law × a new-code rate). What the lens may have missed: I did not count mints directly (no engine
counter — a Drop-counting instrument à la acf2 would settle the rate question), did not fly
loaded/paced arms, and did not fly 10⁶ (the build cap; the 3×10⁵ interior point plus the HWM
transient argument carries the refutation, but the 10⁶ rung itself remains unflown).
