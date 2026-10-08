# Predictions (written before the decisive run)

The decisive experiment: `xtask universe --jet-probe` decomposes each rebinding kick of the
plane's own scene into (a) the compiled-cycle rebuild (`Rebinding::from_state`, the path
`bind_in` takes on every rebind), (b) the whole rebind (`bind`), (c) the rest of the resolver,
and measures how long a body's orbit stays inside one quantized memo cell across its
consecutive rebinding kicks (the reuse the law's adopted "re-anchored jet" would enjoy).

Cases I have not tuned on, and what I expect there:

1. **Compile share.** `from_state` (root fit + band cuts + integer Gauss–Legendre panels +
   derivative tables) is ≥ 50% of a rebinding kick's resolver time. The rest (drift readout,
   ~4 secondaries' forces, sigma-delta, turn, residual) is a handful of Scalar operations by
   comparison.
2. **Sub-quantum carried kicks** (dv below the velocity quantum: no rebind, no compile) are
   < 20% of ship kicks on this scene at rtf 30. The tide at these radii moves most kicks over
   the quantum; if this is wrong the compile problem is smaller than the bench suggests.
3. **Cell residence.** For ships born in a doll, the median run of consecutive rebinding kicks
   inside one quantized 12+12-bit memo cell is ≥ 4 kicks. For leavers (fleet members fresh in
   the doll, often on flyby passages with no cycle at all) I expect shorter runs and a large
   Passage fraction, where the jet does not apply.
4. **Ceiling.** With the measured residence R and compile share c, wiring the jet (recompile
   only on cell exit, increment otherwise at ≈ one readout) cuts the rebinding kick's median
   cost by ≥ 2×. If (2) or (3) fail low, the ceiling shrinks toward 1× and the finding is a
   kill: the compile is not the plane's kick problem.

Cloud/x86 timing: orders of magnitude only.
