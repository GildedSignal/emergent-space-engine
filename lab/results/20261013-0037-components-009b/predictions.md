# Predictions (written before the decisive run)

Setup: `bind_probe` (plane scene, settle) on the baseline arm, where `bind()` compiles a full
trajectory, checks the integer word, and on a word transition throws the first compile away and
binds again (universe/bind.rs). Probe counters: calls, transitions, ns in the first pass, total ns.

- P1 (frequency): word transitions are a visible share of binds in the plane regime — I predict
  ≥ 10% (leavers flip to a Passage whose outer radius exceeds the old word; doll captures/handoffs
  rebind in a tighter child word). If < 5%, the double compile is nearly dead code at plane scale
  and the honest claim shrinks to "the waste exists but is rare here".
- P2 (price): a transition bind costs ≈ 2× a non-transition bind (two fit+compile+readout passes
  vs one): ns_first ≈ ½ × ns_all on transition-heavy workloads; ≈ 1× with zero transitions.
- P3 (fix, digest identity): choosing the word from the fit's key *before* compiling (probe fit →
  word → one compile) returns bit-identical `Bound`s, so the plane digest and the universe suite
  are unchanged. Total bind time drops by ≈ (transitions/calls) × ~45%.
- P4 (held-out, wall): whole-settle wall time drops by less than bind time (binds are most of the
  kick, but not all of the settle). I will also probe a bigger scene (400 members) and a different
  seed; if the transition share moves by more than ~2× across them, the frequency claim is
  scene-dependent and must be reported as such.

Kill criterion for the fix idea: transitions ≈ 0 on every probed scene, or digests move.
