Working...
Check complete. **Grade: gold** — written to `check2.md`, with two in-place corrections to the author's page, tree restored pristine.

**What I verified independently:**

- **Reproduction (bit for bit):** applied `work/patch.diff` myself; the patched binary regenerates all three shipped digests (`b42da477…`, `8c242b02…`, decisive rtf100 `bedd3d9a…`) with census medians identical to the dossier table (cycles quad 10.39%/panels 45.9%/walk 9.59%; passages 0.68% — the 1/148 floor, exactly 624a's 0.7%). CSV facts check out: 8,710+7,379 closes all < period/64 (max 7.8e-3), 9,849 untagged resolver-internal mints (~9,850 claimed), 448-tail quad 5–6 panels.
- **Structural kill is code-true:** `from_shape` (orbit.rs:658–663) sinks period/proper/advance from `knots.last().sum` at mint — lazy compile cannot produce the clocks. Carlson-first ordering is the correct consequence.
- **Four adversarial arms, all outside the author's domain:** rtf 10 interpolates smoothly; seed 7 and 55 s (the bench's caps) hold every law; **rtf 1000 breaks the invariance laws** — 526/26,330 closes in [1/64, 1/16), medians move (walk 0.02%, reads 22, knots 9) — I reproduce the first checker's note to the digit, so the page's domain fence stands confirmed. Aggregate never-quad shares hold everywhere (90.2–92.5% cycles, 98.2–99.3% passages), as does the 27.6×/12.1× quad-call amortization behind the ~10× ceiling.
- **Predictions** predate the runs; P2/P3 held, P1 failed informatively and became the result, P5 honestly reported wrong.

**Author's misses:** "both reproduce exactly" overstates the fleet-cycles match (a bracket: 10.4–46% around 14.3%; exact only for passages and the default floor); 1991's passage-side numbers (~60% phase) never mapped; rtf 1000 unprobed by the author; `--members` caps at 400 (my 1000 run is bit-identical — no larger-N arm exists); the 448-tail probe/read range quotes only the top rows. Page corrected on the first point ("held within 2×") and a checker2 line appended.
