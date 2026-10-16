# Predictions — 20261016-2229-quant-7343

Written before the decisive run. The run decomposes the in-belt scan read (cdf0/3999's
4.07–4.85 µs/read, one cartesian readout per candidate) into its stages on shipped code,
at the belt band (N = 10⁴ ladder rung, seeds 1 tuned, 2 held out).

- **P1 (reproduction).** A mid-band belt body's scan (r ∈ [2.0, 2.6] AU, root doll) trips
  the radial fallback (`candidates → None`), reads ~N bodies, finds 0 encounters, and the
  whole answer costs 3.5–5 µs per read at N = 10⁴ — 3999's regime, reproduced.
- **P2 (stage split).** The tube solve (`entry.trajectory.state`, inside decode) carries
  > 55% of a read; the turn + residual fit + i64 pack (`readout − decode`) < 30%; the
  Scalar wrap (`cartesian − readout`) < 10%; the integer predicate (`sub2`/`mul`/`fixed`/
  `hit`) < 10%.
- **P3 (tail and layout).** Per-read p99/p50 ≤ 2.5 in body order, and body order vs
  Arc-address order differ < 2×: the read cost is compute, not memory layout.
- **P4 (the 50× price).** One checked Scalar `mul` costs 5–20 ns, so a 4 µs read is
  ≥ 10² Scalar-equivalent ops — structural (knot-table search + panel evaluation + wide
  i128 chains), not a wrapper tax. Deleting overhead (Res wraps, checks, turn, packing)
  cannot reach even 3×; the "~50× cheaper reads" way out is dead on this representation —
  the slack must be taken by not reading (phase-neighbour rank / population answer).
- **P5 (held-out, band edge, seed 2).** An out-of-band window (r > 3.2 AU or a non-belt
  root-doll body) returns `Some` candidates with < 10 kept, and the per-read cost is
  unchanged (~4 µs): the read is per body, regime-independent.
