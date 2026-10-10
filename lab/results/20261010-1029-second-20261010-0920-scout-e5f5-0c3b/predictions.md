# Predictions — second author on 20261010-0920-scout-e5f5

Written BEFORE the decisive run. The checker's named experiment: per-(cell, shell)
accumulators (FMM interaction shells, member quanta), deferral error bounded and
non-growing at O(1)-per-body cost, MC-anchored at two sizes.

## The scheme under test ("shells")

- Direct: an event broadcast exactly (arrival-timed, own s/d^2) to bodies in the 3x3
  leaf neighbourhood of its leaf. No per-event rings anywhere, so no
  ring/square complement to mismatch.
- Aggregate: one accumulator per (level l, cell D_l) holding (A, dipole p). Member
  set of the accumulator = bodies whose leaves first separate from the source's
  cell chain at level l (min-rule: smallest l with wrapped Chebyshev distance of the
  level-l ancestors in [2,3]). Flush when A >= theta_l = q*(1.5*c_l)^2 (the member
  quantum: nearest member body is at >= 1.5*c_l from the cell centre). The flush
  delivers (A, p) from the cell centre, arrival-timed at c=1, to member bodies only.
- Partition claim: every (receiver, event) pair goes through exactly one channel
  (direct XOR one accumulator). Verified by an integer coverage assert over the
  full l*-table — this is the canonical (integer) outcome; float errors only explore.

## Predictions (held out: I have not run the MC yet)

P1. Coverage assert passes: every receiver leaf has exactly one channel per source
    leaf (direct or exactly one ring), all 1024x1024 pairs at side 32.

P2. Cost, per body per time at q=0.01:
    - direct = 9*16 = 144 (the 3x3 broadcast; bigger than the ring's 34.8 — the
      price of a tree-aligned near field).
    - flush: each ring level delivers ~57/body/time (scale-invariant: rate
      F*A_l/theta = F/(2.25q) = 4.75 per cell per time, member count 12*4^l leaves).
      Total = 144 + 57*n_rings.
    - N=4096 (side 16, n_rings=3): ~315. N=16384 (side 32, n_rings=4): ~372.
      Measured two-size exponent ~0.10-0.15. Analytic to 10^6 (n_rings ~8): ~600,
      ratio to naive ~1.7e3 — the exact partition costs ~10x the leaky v2 scheme's
      2.1e4 ratio, still O(log N) per body.
    - writes ~ (n_rings+1) per body per time (~5).

P3. Error, dipole aggregates, q=0.01 (report in q units):
    - pending-residue term: per level ~12 pending accumulators cover a receiver,
      each < theta_l at distance >= 1.5 c_l: RMS ~0.6-1q per level, worst-aligned
      ~2-3q per level. Over 4 rings: median ~2-4q total, max ~10-25q.
    - dipole bias walk: per-arrival quadrupole-order bias ~0.05q at ~230
      arrivals/body/time: ~sqrt(230*12)*0.05q ~ 2-3q by t=12. Slow.
    - NET: median <= ~5q, max <= ~25q, and NON-GROWING from t=2 to t=12 (slope
      within noise; contrast v2 0.029->2.28 and drop 0.029->0.147 growing).
      The checker's letter "bounded <= L*q" (L=6 levels -> 6q): I expect the MAX to
      land 1.5-4x above 6q (the per-level worst alignment stacks); the median at or
      below it. If max <= L*q holds too, better than I derived.

P4. Scalar control (same scheme, aggregates carry A only, no dipole): monopole bias
    at member distance ~1.5-3 c_l is O(1) relative -> persistent per-arrival bias
    ~0.5-2q random-sign -> error grows ~sqrt(t): max at t=12 ~30-100q, visibly
    growing. If scalar does NOT grow, my bias model is wrong and I report that.

P5. Fine quantum q=0.001 (side 32): flush rate ~ 1/q -> deliveries ~10x P2's flush
    term (~3720+144); error in q units unchanged (the structure is q-scale-invariant
    except the leaf broadcast overlap). The quantum, not N, sets the bill (as the
    original dossier said).

P6. Memory: accumulator words ~ 1.5*(n_rings+1)/16 words/body nonzero (~0.5), plus
    in-flight emissions ~7 words/body: total news state ~7-9 words/body, comparable
    to v2's 9.5 (the memory side of the claim survives).

P7. Chunked flush timing (disclosed approximation): accumulator crossing is checked
    at chunk boundaries (<=0.125 time units); extra deferral absorbed in the
    pending bound; does not change growth class.

## Kill criteria

- If P1 fails (partition not exact), the scheme is mis-derived: report the pair
  counts that break.
- If P3's non-growth fails (dipole error grows >2x from t=2 to t=12 like v2), the
  claim "the FMM-shell partition fixes the leak" is REFUTED and the original
  dossier's rescue condition ("needs a different bookkeeping entirely") stands.
- If P4's scalar control does not grow, my monopole-bias model is wrong (report).

## Outcomes (appended after the decisive run; the section above was frozen first)

- P1 HELD: partition assert passed in every config; member counts uniform
  (9/40/147/588/240 leaves at side 32).
- P2 PARTIAL: direct = 144.7 measured (predicted 144). Flush 115-162 per ring
  vs predicted 57 (the [2,3] annulus holds 40*4^l leaves, not 12*4^l); totals
  425.0 / 585.6 vs predicted 315 / 372; two-size exponent 0.231 vs 0.10-0.15
  (top-ring wrap truncation at both sizes).
- P3 PARTIAL: non-compounding held (max +15.6% over a 3x horizon, vs v2 x79);
  magnitude missed (max 43-60q vs predicted <=25q; med 17-22q vs <=5q -- a
  receiver is covered by ~40*4^l pending accumulators per level, not 12*4^l);
  the letter "<= L*q" FAILS (med ~3Lq, max ~9Lq).
- P4 HELD: scalar control 98.5q vs dipole 59.9q at t=12 -- the monopole walk
  is real and the dipole is required.
- P5 FAILED BOTH: fine q=0.001 gives cost x4.1 (not x10) and error x8 worse in
  q-units (not invariant): the renewal overshoot E[s^2]/2E[s] ~ 0.042 floors
  the accumulator's effective quantum -- a new constraint neither the original
  run nor I had modelled.
- P6 HELD: accumulator words 0.41-0.64/body, emissions 0.26/body/time,
  in-flight ~5-10/body (1-word accounting), comparable to v2's 9.5.
- Unpredicted: the cold-start growth (0 -> 21.5q) was the top ring's warm-up
  transient (cycle 13.4 time units > T); the pre-history construction was
  needed before any growth claim meant anything.
