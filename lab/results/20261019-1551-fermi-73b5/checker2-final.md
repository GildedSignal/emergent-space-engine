Working...
Check complete. Summary of what I did and found:

**Verdict: `Grade: gold`** (written to `check2.md`, with the page's two overstated letters corrected in place).

**Reproduced**
- `regen.sh` exit 0 (runner); I re-ran the harness myself — `book` output **bit-identical** to e828's committed `book.txt` on their branch; `work/epochflux.rs` **byte-identical** to e828's committed harness (extracted from their `work/patch.diff`).
- All cited quotes verified **verbatim** from the cited runs' branches: 1a29's "n−1 = 355 cores per 10⁴-cell occupancy at 1 µs/eval, 1 kick/body/interval on the checker's 28141.5-s clock" (→ 355.3 recomputed), 1176's "E_cell ≈ (n/2)·E_pair … ~3.5×10⁻⁴ cores" and "140× under", e828's "5.7×10⁹ ticks per kick / 1.1×10¹⁵ ticks per synodic".
- The divisor adjudication is sound **under both wirings** (per-pair epoch and per-cell batch re-scan amortize to the same (n−1)/E_pair per kick) — 1176's E_cell divisor understates n/2 = 10³–5×10³ either way.

**Adversarial probes (beyond both runs' grids)**: fresh seed 31337 reproduces the P=1 column and the saturating E-shape; κ = 2⁻²⁹ (64× weaker than the quantum, outside both κ grids) zeroes the P=1 column on the only leaking seed — the weak end of the κ-saturation law.

**My independent find** (outside the author's tested range): the dossier's claim 3 constant is wrong. Clock-consistent, from `view.rs:23` (TICK_SECONDS = 4.925 µs game tick) vs `kepler.rs:29` (`TAU·a^1.5·2³²` replica ticks → 1.169 ms each) and the harness's actual belt (a = 2.0, not 2.5): **r ≈ 6×10⁻⁹–2.3×10⁻⁸**, so e828's 5×10⁻⁶ is ~10²·⁵–10³× high (game-tick/replica-tick mix × dropped TAU) — not the page's "~10⁶×". Direction and every conclusion survive with more margin (P = 4 is ~10⁸–10⁹× off; leak certification gains orders). Page fixed: the factor letter and one stale `r·E ≤ 5×10⁻³` → `3×10⁻⁵`.

**Author-missed items recorded**: the r constant (dossier still asserts it and "P1–P5 all held"); the misattributed "e828 bound 8.1×10⁻⁸–2.0×10⁻⁸" (it's 5.2×10⁻⁶/E, not e828's actual P=1-column bound and not a bound on that column — certification survives via e828's own column at E=1024 anyway); the wiring-independence argument left implicit; patch.diff carries the harness twice (harmless).

One process note: my second page edit misfired against a shifted line number and briefly swallowed the "churn row" sentence — caught on re-read and restored; the final paragraph was re-read end-to-end and is coherent. Nothing else in the run folder was touched.
