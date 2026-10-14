# Predictions (written before the decisive run)

Question: is the per-cycle **knot table** (built eagerly by every compile) one structure behind the
three measured walls — the kick's bind (46% of a fired kick), the kick's impact search (45%, ~25
readouts × 4.6 µs), and the memory after the first kick (~43 knots × 88 B of the ~5.1 KB/body)?

Scenes (shipped `plane`, single thread, cut at 8 game-s): **battle** seed 3 / 1,500 members / rtf 1;
**flying** seed 3 / 400 members / rtf 100. Instrument: additive counters in `crates/space`
(`census.rs`), no arithmetic touched; digest printed per arm under two schedules must agree.

- **P1 (tables are write-mostly).** Knots compiled per fired kick ~40–130; distinct bracket cells
  ever *read* per compiled table ≤ 60% on the battle arm, ≤ 10% on the flying arm (belt-like bodies
  have no crash search: their tables are read only at the kick's own state read).
- **P2 (the readout re-integrates; the table only brackets).** Per time→state readout, ≥ 15 integrand
  evaluations (quad panels ×4 + Newton rate nodes) on the general branch — the 4.6 µs/call measured
  by the frame-cost page is quadrature over the partial panel, not table lookup.
- **P3 (compile dominates integrand work where bodies are quiet).** Build-side integrand evaluations
  ≥ 5× read-side on the flying arm; ≤ 2× on the battle arm (crash searches re-integrate heavily).
- **P4 (the unification number).** Across both arms, ≥ 70% of all integrand evaluations in
  `orbit.rs` happen at build time — sums whose only read-side use is a bracket anchor plus the
  cycle increments, both of which the certified Carlson complete forms already reproduce to the
  table's own 2⁻³⁰ quantum.
- **P5 (identity).** The digest at the cut is identical under unlimited and 3 ms wall budgets on
  every arm (the counters change no bits).

If P1–P4 hold: the knot table is a cache that costs more than what it caches; the deletion path is
closed-form anchors (increments, already certified) + local inversion (incomplete forms, fenced),
which collapses kick cost, search cost and per-body standing memory in one adoption.
If P1 fails (tables read widely), the unification dies and the record should say so.
