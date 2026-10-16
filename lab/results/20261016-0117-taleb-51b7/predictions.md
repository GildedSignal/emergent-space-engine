# Predictions (written before the decisive arms)

Tuned on: beltburn/belt/home smoke at N=10³ and 10⁴ (8 s flights), never at 10⁵, never past 8 s,
never through the belt's first-kick wave (13,051–14,534 game-s = 130–145 s wall at rtf 100).

Held-out cases and what I expect there:

1. **beltburn 10⁵, 12 s wall.** Each held scan holds ~1.11 MB at 10⁴ (730−27 MB over 632 scans);
   candidates scale with N, so ~11 MB/scan at 10⁵. The mint is ~1–2 scans/frame (the burn re-keys
   the player every thrust kick) and answers (N × ~1.5–1.9 µs ≈ 150–190 ms) never fit the 12 ms
   budget. Prediction: the backlog grows ~1/frame, the probe self-fences at 1.9 GB within
   **2–4 s of burn** (~170 scans), p50 frame over 12 ms (capture alone = N × ~200 ns ≈ 20 ms
   standing). If instead held stays ≤ 10 or memory stays under 100 MB, my mint-rate reading is wrong.
2. **belt (quiet coast) 10⁵, 20 s wall.** The player's items fire at the root doll's cadence
   (kicks 2⁷ per Cinder period ⇒ one item per ~59,400 game-s ≈ 594 s wall): prediction **zero scans,
   held_max = 0, enc = 0, p50 ≈ 0.03 ms, memory flat** — the quiet belt is free; the ruin needs the
   player (or something) to change the player's binding. If held_max > 5 here, something else mints
   scans and the burn reading above is contaminated.
3. **belt 10⁴ through the wave (145 s wall).** The wave kicks every belt body (bindings change under
   the scan) but mints no player items. Prediction: wave-frame cost as in the merged record (max
   ~12–25 ms at 10⁴–10⁵, budget-drained), **held_max ≤ 2, memory ≈ the ladder's own 26→55 MB
   (10⁴)**, digest deterministic on a rerun. If held grows with the wave, the wave itself mints scans.
4. **belt 10⁵ through the wave (140 s wall).** Same but memory ends ≈ **520–540 MB** (the ladder's own
   266→525 MiB first-kick retention; player-in-belt adds nothing), no fence. If it fences, the belt
   player interacts with the wave beyond the record's home-player baseline.
5. **Digest identity.** beltburn 10⁴ 8 s re-run: identical digest (determinism across processes).
6. **The count-cap extrapolation (not flown, arithmetic only).** SCAN_BACKLOG = 2048 caps the backlog
   by count; bytes per scan ≈ 111 B × N. At 10⁴ the cap = 2.3 GB, at 10⁵ = 22 GB, at the goal's 10⁹
   belt = 240 GB — one player burn in a dense doll can demand more memory than the machine has,
   before any frame overruns: the cap is sized for the 28-body plane (~10 KB/scan), not the belt.
