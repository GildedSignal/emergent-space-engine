Working...
Check complete. Summary:

**Verdict: KILL** (`lab/verdict.py`, author + checker metrics agree on all 18 outcomes) — `eob-doll` dies on `prec` (0.0625 < 0.99) and `nu` (0.981 < 0.99); `test-mass` and `newton-doll` fail exactly the gates they were built to fail. A KILL of configurations, not of the method.

**Reproduction** — every published number reproduces **bit-for-bit** in a clean copy with a fresh `gcc -O2` build: all three binary metric sets, the 103-crossing reference, both handoff exponents (0.03630 / 0.03626), both flyby fractions (1.0, worst 5.710e-3), and `picture.png` regenerates to identical bytes. `metrics-check.json` and `check.md` are written; nothing else in the run folder was touched.

**Oracle verified** — `oracle.py` is a verbatim port of `xtask/src/gr_oracle_extended.rs`; I re-ran the author's Rust check (matches), ran `cargo xtask gr-oracle`, and integrated the harmonic 1PN EOM myself (adaptive, tol 1e-13). My own invariant mapping + quadrature independently confirms the kill's physics: doll−DD advance = +0.79% at p=1000, +8.4% at p=100, +68.7% at p=20 — genuine 2PN content of the exact metric, not a bug; min passing p = 800.3. The 4 ν-failures are all p<170 (2PN contamination).

**Adversarial cases run** — autonomous doll chain (no reference re-initialisation): exponent 0.025, still passes, so the author's per-segment shortcut hid no compounding; independent Python 3-body flyby reference agrees with the C reference to 9e-10 at matched epochs; flyby error grows ∝ b as predicted; energy-conservation probe of the invariants.

**Flagged to the integrator** (in `check.md`): missing `dossier.md`; the figure-eight transfer was silently replaced by a retrograde co-orbital orbit after `design.py`'s shooting failed to converge (residuals kept in `design.json`); the handoff metric is hollowed by construction (passes honestly anyway); ship cases carry no GR signal (schw ≈ kepler to 1e-6); and `cargo xtask gr-oracle` prints **ORACLE DISAGREES in main** — pre-existing, 12 rows at e=0.5 failing their 2PN-residual bands, which I traced to `eih_invariants`' turning radii being only 1PN-consistent at high e. That last item deserves integrator attention independently of this rung.
