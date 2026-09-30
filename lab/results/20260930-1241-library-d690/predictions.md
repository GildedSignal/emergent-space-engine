# Predictions — library run 20260930-1241 (written BEFORE the decisive experiment)

Tuned case: N = 1,000, ring lattice (k=4), target faction fraction f* ≈ 0.3. Both laws are
tuned there only (mean fraction and update rule matched); everything below is held out.

Decisive experiment A — law form (binary minority-threshold vs graded response):
1. Cross-population SD of the time-averaged faction fraction (the aggregate the geometry
   consumes): binary rule gives **less than half** the graded rule's SD at every held-out
   N ∈ {10^4, 10^5, 10^6} (Taleb's "variance of the results is lower" claim).
2. Attractor independence: across 10 independent populations, binary converges to the same
   fraction within ±0.03 in ≥ 9/10 populations at N = 10^5; graded's spread shrinks no
   faster than 1/sqrt(N).
3. Surprise-rate tail (what the allocator feels, board B4): binary flip-rate p99/p50 stays
   ≤ 3× the graded rule's. **If binary shows a ≥10× heavier tail (avalanches), the lesson
   inverts** — binary laws would be smoothness-hostile and I must report that.
4. Held-out stress: with 1% of agents force-flipped per step (player wildcard), binary's
   aggregate SD stays bounded (< 2× its noise-free SD); graded's grows.

Experiment B — aggregate exactness threshold (Asimov's N-count):
5. Poisson check: SD of a cell's fraction fluctuation times sqrt(n) is constant within
   ±5% across n ∈ {10^2, 10^3, 10^4}.
6. Threshold: with a relative quantum eps_rel = 2^-8 on the stored count, the occupancy
   above which individual identity is unobservable noise is n* = (1/eps_rel)^2 ≈ 6.6e4.

Failure kills the lesson, not the method. A miss on 1–2 demotes the Taleb lesson to a
lead; a miss on 3 is the interesting inversion; a miss on 5 kills the threshold rule.
