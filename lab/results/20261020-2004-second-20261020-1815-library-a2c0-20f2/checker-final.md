Working...
Check complete. **Grade: gold** — written to `check.md`, page corrected in place, tree restored clean at base `6db15364`.

**What I did:**

1. **Reproduced**: applied `work/patch.diff` at the base commit myself, re-ran `./regen.sh` (48.7 s, exit 0) — F1 digest `8eecf1fa…` byte-identical to 23a6's committed e3, all 41 (t, tests, skip_bnd) triples equal, every count-level line matching. Recomputed the δ pin by hand from the raw ANS rows (0.044%→0.333% over 18 constant-gap legs, peak 0.488%, δ_eff 0.053–0.399, 28/40 in a2c0's band — recounted), the c_check rows, the duration corrections against each leg's own ladder line, and the ledger arithmetic with page-verified constants (TICK at view.rs:23, 12.75 h/69.75 s/27.9k era).

2. **Four adversarial flights** (archived as `work/flights/chk_*`): **seed 2** — letter holds (δ 0.055–0.359), growth reproduces; **`ES_BOUND_VERIFY` at 1e5** — zero false skips in ~1.87M decisions (never flown above 3e3); **coast** — no belt-wide answers at all (approach-driven, as the slack mechanism requires); **45k-gs cut, outside the tested window** — the miss hits **tests = 0 for eleven consecutive belt-wide answers** (~2k kicked bodies per gap: kick-Poisson dead outright, cleaner than the author's own argument), then a late re-approach reaches δ_eff ≈ 2.2 — so the δ<0.5 letter and δ=1 exclusion are window facts. Appended that scoping to the page.

3. **Defects found**: the pre-registration mtime is unverifiable (predictions.md touched 20:24:43, after F1 ~20:16 — the bands' misses argue substance, noted in check.md); the page's era-answer band (1,683–4,082 s = 24–59×) did not regenerate — corrected to the regenerable 1,648–3,998 s = 24–57×; the dossier's "flight's own 5.051e-5" is the committed draw (re-flights read 5.049e-5).

Gold because: the checker-named experiment is flown whole, byte-identical reproduction, two premises dead by measurement (δ as a constant; kick-Poisson invalidation), the ≥40.5-ns corner killed by counts, the capture N-scaling corrected before the silver ledger hardens — adoptable at zero cost, with all my held-out arms confirming.
