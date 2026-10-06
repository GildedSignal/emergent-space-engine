# Predictions (written before the members sweep)

Question: the plane's capacity on the fleet axis (`--members`), judged by the frame tail
(p99.9, hitches/hour, overflow), never the mean. Sweeps held at rtf 100, paced, 15 s,
seed 1: m ∈ {48, 192, 768, 3072} (fresh 48 baseline for internal consistency).
Machine: shared GitHub runner, 8 vCPU; load recorded by the harness (`uptime_before/after`).

Cases not tuned on (the sweep runs once, in one pass, after this file is written):

1. **Engine exponent.** Fleet cost per slice ∝ m^1.0 ± 0.1 (the battle scene is fixed
   density: per_row ∝ √n, spacing 5q constant; the chronon broad phase is a grid).
2. **View exponent and the wall.** View gather and view_json p50 ∝ m^1.0 ± 0.15, and they
   are unbudgeted, so the first hitches above 16.7 ms are view+json frames, not engine
   frames. Capacity m* (first hitches/hour > 0 at 60 Hz): m* ∈ [400, 1600].
3. **The budget is a count cap, not a cost cap.** Engine max per frame stays above the
   5.0 ms budget at every m (the check is between items; one slice/player item overshoots),
   and the overshoot (max − 5.0) grows ∝ m since one slice's cost ∝ m.
4. **Overflow before or after the wall.** overflow_frames become positive only when the
   fleet's mandatory per-frame work exceeds 5 ms; if overflow appears strictly before the
   first 16.7 ms hitch, claim 2 is wrong and the engine binds first (that would falsify
   this file's headline).
5. **Control: schedule independence.** Same seed and cut at m = 768, paced vs unpaced:
   identical `digest` and `cut_tick` (the certificate says budgets and pacing never touch
   outcomes; if this fails everything above is suspect).
6. **Stall vs compute.** At the capacity wall the hitches are compute (frame_cpu_ms
   hitch_counts > 0), not stalls: the tail is made of work, not descheduling.

Kill criterion for the premise "the plane scales on the fleet axis": if hitches/hour
above 16.7 ms exceed ~60 (one visible hitch per minute) at m ≤ 800, the plane as built
does not scale past ~10²–10³ fleet members, seven orders below the goal's 10⁹, and the
binding stage (measured, claim 2 vs 4) names the next job.
