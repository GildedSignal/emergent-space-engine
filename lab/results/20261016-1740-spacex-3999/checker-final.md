Working...
Check complete. Verdict written to `lab/results/20261016-1740-spacex-3999/check.md`:

**Grade: gold**

**What I did:**
- **Reproduced** — regen.sh (exit 0) plus my own runs with the patch applied by hand: 10⁴ seed 3 (new seed), 3×10⁵ seed 1 (3× the author's top N; 10⁶ would breach the 2 GB box), and a 10⁴ seed 1 rerun bit-identical to the regen on every deterministic cell. The N−314 constant holds at every N and seed; per-read flat at 4.2–4.8 µs to 3×10⁵; zero encounters everywhere.
- **Verified probe fidelity** line-by-line against shipped code: the `bodies/4+64` rule (radial.rs:254), the capture loop (encounter.rs:174–189), `Scan::compute` (encounter.rs:130–154), the mint inside the player's item (universe.rs:762–773), the drain bar (universe.rs:1189). Patch is one print-only example; tree clean.
- **Attacked** — the pricing math recomputed independently: max|ν−M| = 2e exact to four digits; the 4.5–9% kept band verified; and under the most optimistic sound per-body margin (5.6% ≈ 23 ms at 10⁵) the "tens of µs" cure still cannot reach its price — the conclusion is robust to every band choice.
- **Novelty** — the topic page's own record leaves this regime unmeasured; cdf0's checker withheld gold on exactly this hole; this run fills it and re-prices open direction 1.
- **Page** — faithful; corrected one overstatement in both places ("≥ bodies/4 into every core bin" → "fills every in-band window past bodies/4", since the rule sums the window's ~2 bins and edge bins at 3.0 AU carry ~11%).

Predictions were genuinely pre-registered (P1 refuted honestly, and the refutation is the result); seed 2 held out and held. Gold under "shows a premise is wrong": cdf0's small-N scoping and the angular cure's price both die in the belt band.
