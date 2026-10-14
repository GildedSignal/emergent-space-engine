# Predictions (written before the decisive run)

Question: the ladder's flights stop at the belt's first kick wave (20 s flights before it, 200 s
flights just past it), but the belt's kicks recur as a train (one item every ~26-29 k game-s per
body, the cohort coherent). What stands between waves? Inversion of the merged claim "only what
is held per body grows": assume the opposite — that what is held grows with *play* (waves), not
with N — and check whether main is already on that path.

Scene: the plane bit for bit, `plane_extra` N extra bodies, seed 1, coast, rtf 100, 12 ms
budget, 60 fps frames, settled at the cut for a canonical digest (the player stays at Home; the
in-band player is 625b/d7e3's measured ruin, not re-measured here). Probe:
`examples/wavetrain.rs`, sampled every 250 game-s (memory, catalogue, held, lag) and 5,000
game-s (bytes/body, retired-history census over a fixed 4,096-body belt sample, refusals).

Arms: A = N 3×10⁵, cut 150,000 game-s (~5 waves; the largest N whose post-wave memory ~1.56 GB
fits this box's 2 GB/process rule). B = A rerun (determinism). C = N 2×10⁵, cut 150,000
(scale-invariance of the per-body steady state).

Code reading that motivates each prediction (bind.rs free-list catalogue; prune keeps the last
retired binding only; keep-window = 2×light-distance + 2²⁶ ticks ≈ 2.8 k game-s ≪ wave
spacing):

1. **Memory is a step, not a staircase.** rss steps at wave 1 (~13-14.5 k game-s) from ~2.6 to
   ~5.1 KB/body (Arm A ≈ 0.79 → ≈ 1.55 GB) and waves 2-5 leave it within +3% of the
   post-wave-1 value; b_per_body ends 5.0-5.2 KB. *Falsified* if rss grows by more than +5% per
   wave or the process is killed for memory.
2. **The catalogue's free list works.** Live entries ≈ bodies (±5%) at every sample; transient
   growth only inside a wave. *Falsified* if live entries grow by ≈ +N per wave and stay.
3. **History returns to one retired segment per body between waves** (census h2 = 0, hmax ≤ 2
   briefly during a wave). *Falsified* if h2 > 0 between waves or hmax ≥ 3 persists past a
   wave + 3 k game-s.
4. **Lag recovers.** Each wave costs ≤ ~2 s of presented-time lag, back to 0.000 before the next
   wave; no permanent backlog. *Falsified* if the lag at wave k+1 starts where wave k ended.
5. **Frames hold at every wave** as at wave 1 (max ≈ 12-13 ms, 0-2 frames over 12 ms per wave).
6. **Determinism.** Arm B reproduces Arm A's digest and every counter exactly (rss within
   noise); the w:/h: trajectories match line for line.
7. **Held-out (not tuned):** Arm C's per-body steady state matches Arm A's (b_per_body within
   5%, catalogue ≈ bodies, h2 = 0 between waves) — the wave train's memory behaviour is
   scale-free in N on 2-3×10⁵.
8. **Held-out (recorded, no claim):** encounters and dead bodies per wave (the belt's ongoing
   collision rate; no prior measurement to predict from).

What each outcome means: (1-4 confirmed) the record's "2.6 → 5.1 KB a body" is a step, the
score at 10⁶ (5.1 GB, over the 4 GiB bar) is *stable in play time*, and the binding constraint
for longer flights is the CPU cadence (ladder break 1), not retention; the certificate extends
to play-length flights. (1 or 2 falsified) memory grows with play at the plane's claimed scale —
the project's named failure mode, on main, measured.
