# Predictions (held out before the decisive run)

Toy: one doll (radius R, light speed c=1 unit/tick), one central source (mass m) whose
news events (thrust/contact/rebind — the only creators of ghosts, per law.md "gravity is
news") arrive at Poisson rate λ. Readers (ships) at radii uniform in [1, R], each kicking
at cadence Δ, each resolving the source individually only where its pull exceeds one kick
quantum Q: r_q = sqrt(G·m/Q). A news event k needs a ghost (the pre-news tube,
extrapolated) exactly while some resolvable reader's extrapolation window still crosses
it: reader at r needs ghost k during [t_k, t_k + r/c].

Policies: KEEP-FOREVER (the feared unbounded log); TTL = R/c (the naive doll bound);
TTL = min(r_q, R)/c (the influence-decay bound); TTL = min(r_q,R)/(2c) (negative control).

Not tuned on: the sweep over m (5 decades), λ (4 values), and a many-source hierarchy
run (members of mixed masses in nested dolls). My predictions there:

1. **KEEP-FOREVER grows linearly** with game time (live chain ≈ λ·t); the other three
   flatline. The wall exists only under KEEP-FOREVER.
2. **Flatline level = λ · min(r_q, R) / c** (Little's law), within Poisson noise (±3·sqrt(level)
   per checkpoint). It is independent of game time, reader count and doll radius once
   r_q < R.
3. **TTL = R/c over-retains** by exactly the factor R/min(r_q,R) when r_q < R: it holds
   ghosts no resolvable reader will ever read (wasted memory, zero benefit).
4. **The negative control misses reads**: TTL = min(r_q,R)/(2c) serves reads needing a
   ghost at rate ≈ λ per source (read windows beyond the TTL are unserved, Misses > 0),
   while TTL = min(r_q,R)/c has exactly 0 misses in every run. A policy with 0 misses and
   lower memory than TTL = min(r_q,R)/c does not exist in this toy (it is the exact
   min-plus death time).
5. **Work is the frontier, not the volume**: with the player at the origin emitting one
   action every Δ_a, cells touched per frame ∝ frontier length (∝ t in 2-D, linear), not
   ∝ enclosed area (∝ t²): the ratio (area-work / frontier-work) grows ∝ t. Per-frame
   causal work under gather-at-the-cone is constant while the cone quadruples in area.
6. **Hierarchy run**: small-mass members (r_q inside their sub-doll) contribute zero
   ghosts to the parent doll's chain — their news is absorbed below the parent's quantum
   (the aggregate is the shadow). The parent chain's flatline is set by the masses whose
   r_q exceeds the sub-doll radius only.

If (2) or (4) fails — flatline not at λ·min(r_q,R)/c, or misses appear at the exact
bound, or a shorter exact policy exists — the claim "causal memory is bounded by
influence decay" is wrong as stated, and the light-cone wall is real for news gravity.
