# Predictions — 20261021-0429-spacex-9d3a (read census / demotion)

Tuned on: N=1000, 6 s, view=none only (one smoke run). All arms below are held out.
Arms: N=0 view=frame (dense control), N=1e5 view=sparse, N=1e6 view=sparse; 20 s each, coast, rtf 100, 12 ms budget, seed 1 (the harness's fixed plane).

- P1 (the claim): at N=1e5 and 1e6, ≥ 90% of build-born generations (the belt's standing compiled orbits) get **zero reads after their birth frame** over the 20 s flight. Basis: the belt's rebind rate is ~3e-5/(body·game-s) [cell-rebind 6e91], so ~6% of belt bodies see any event in 2,000 game-s, and observe is player-local (frame wall flat in N, nladder N1).
- P2: live fraction of live entries at slack 1 frame ≤ 0.15 at 1e5/1e6; ≤ 0.40 at slack 60 (1 s).
- P3 (positive control, dense side): at N=0 with per-frame view gathers, median reads per generation ≥ 8 and live fraction at slack 60 ≥ 0.8 — the plane's own population stays hot, reproducing 4ea0's 68-77 reads/generation in order of magnitude. If this fails the instrument is blind and the run is VOID.
- P4: rebuilds (reads after a gap) on build-born generations at slack ≥ 300 frames (5 s) ≈ 0 at 1e5/1e6: nothing returns after 5 s idle, so a 5 s demotion timeout adds ~no rebuild CPU.
- P5: view-gather reads are < 5% of all reads at 1e5 (sparse gathers, one per 10 s).

Kill criterion for the demotion premise: if ≥ 50% of belt (build-born) generations average ≥ 1 post-birth read per 100 frames, the standing orbit is a live read cache, not dead weight — demotion is dead on the shipped read path and the dossier reports the read path (who) as the blocker instead.

Falsifier for the whole frame: `misses` must be 0 (single-threaded assumption) in every arm, else the census undercounts and nothing counts.
