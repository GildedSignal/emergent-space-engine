# Predictions (written before the decisive experiment)

The question: does a compact same-(E,L) family (a formation) share one integer kick
stream — identical fired `dvq` for every member, hence one binding — and what
separation/word makes that certificate hold? Mechanism under test (from the shipped
code, `step.rs::quantize` + `force::acceleration`):

- Members at separation δx see accelerations differing by δa ≈ H·δx, H the sources'
  Hessian (Giant dominates in the root doll: μ_G/R³; the star's tide in a child doll:
  1/r³; the origin's fall contributes zero — it is x-independent).
- `quantize` fires `dvq = (carry + dv)/2¹⁶` in carry units; members' streams stay
  bit-identical iff the accumulated differential velocity ∫δa dt never crosses one
  quantum of the shared word (then carries may differ sub-quantum, but no fired kick
  ever differs).
- The shipped velocity word keeps 61 significant bits (`to_word`), so the quantum is
  ~2⁻⁶¹·v; a family word at the behaviour floor (the memo code's own 11 fraction
  bits) gives a quantum ~2⁻¹¹·v.

Predictions, each with its kill criterion:

- **P1 (the shipped word kills sharing at any real separation — the mechanism behind
  225d's "one kick erases").** At the 61-bit word, the oscillatory differential
  amplitude A = H·δx/n_syn exceeds the quantum for δx above ~10⁻⁵ root units
  (micrometres); the first differing firing happens within < 1% of a synodic period
  for δx ≥ 1 root unit (1.5 km). Kill: if two members at δx = 1 root with identical
  carries fire identical kicks for ≥ 1 orbit at the 61-bit word.
- **P2 (the family word restores the certificate for compact formations).** At the
  11-fraction-bit family word, A/quantum = 2⁻¹¹·v scale ⇒ the certificate holds
  (zero differing firings over ≥ 50 synodic periods) for δx up to ~10⁹ root units
  (≈0.05 AU) at 1 AU, scaling as δx·H/n_syn. Kill: differing firings within 50
  synodic periods at δx = 10³ root (1,500 km) and the 11-bit word.
- **P3 (the member error stays inside the law's error model).** The sub-quantum
  differential error per member is bounded by A ≈ H·δx/n_syn: at δx = 10³ root the
  relative velocity error < 10⁻⁷·v (B2's period bar is 10⁻³). Kill: measured A at
  δx = 10³ root exceeding 10⁻⁵·v.
- **P4 (chaos, not the oscillatory tide, sets the long horizon).** Away from
  mean-motion resonances with the 2⁻¹⁰ planet at 4.94 AU the differential is bounded
  (no secular slope beyond the oscillation); near a p:q resonance (period ratio with
  the planet) the differential grows (exponentially or linearly), splitting families
  there at T ≈ quantum/(growth rate). So "which bodies must stay fine": the resonant
  fraction. Kill: bounded differential everywhere including exact resonance, or
  unbounded growth everywhere (then no family certificate at any radius).
- **P5 (phase-spread rings split immediately at any width** — the negative control,
  225d's geometry): members on the same orbit but a large phase offset (δx ~ orbit
  scale) differ by O(1) in dv and fire differently at the first kick, both words.
  Kill: identical firings at any width for a phase-spread pair.

Method: the shipped `force::acceleration` on the shipped scene's secondaries (exact
integer Scalars, same function the kick calls), a variational twin for the
differential growth (A, secular slope, resonance sweep 2.0–3.0 AU), and a direct
integer simulation of the family's kick stream (quantize + carry, two words, δx
sweep 1..10⁶ root units). All in one example, < 60 s.
