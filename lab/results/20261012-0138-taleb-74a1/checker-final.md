Working...
Check complete and written to `lab/results/20261012-0138-taleb-74a1/check.md` — nothing else in the run folder was touched.

**Grade: silver.**

**What I did:**
- **Verified integrity first:** `work/enc/src/*.rs` is byte-identical to `wt/cx-b-coorbital-cert:crates/encounters/src` (only Cargo.toml de-workspaced); the branch is one unreviewed, unmerged commit (`adce00d6`), as the dossier claims. Rebuilt the probe from source — the `/home/glmlab/lab-target-1` path is just the global `CARGO_TARGET_DIR`.
- **Reproduced every load-bearing counter bit-for-bit:** 31,860,946 window pairs vs 396,000 tier pairs at n=8000 (exponent 2.01, 99.58% of n²/2, contacts 0); ULP cliff 499→124,750 and 1,999→1,999,000; the panic at exactly `phase.rs:35`; cone-gating leaving exactly the tree's 396,000 candidates. Wall times ~1.5× the author's (shared machine), inside the predicted band. All four claimed mechanisms confirmed in the branch's own code (`reach` at phase.rs:65, exact-`==` shape gate at :55, cone-skipping `st.phase ||` at :186, assert at :35).
- **Four adversarial cases of my own:** dispersion *with* real contacts (quadratic persists, 0 misses — the zero-contact scenes weren't a pathology); a safety attack on `reach` (varied e/ϖ, TAU seam, forced conjunctions, shared-shape subgroup — 10/10 contacts, 0 missed); horizon scaling (2ρ dispersion → 98.3% of all pairs at H=20); the branch's own test suite (11/11 pass, no hidden failures).
- **Novelty:** confirmed absent from HISTORY.md and the board; it's the complementary *dispersion* axis to the gold's *concentration* finding.

**Why not gold:** prediction 4 said neighbours ∝ da with ratio ≈16 from 5e-4 to 8e-3; measured 1.78× (saturation at n²/2), yet the Predictions section claims "all five held" — the integrator's 1-October precedent caps exactly this at silver. The miss direction *strengthens* the thesis, so silver, not lead. Gold is one honest re-adjudication plus one unsaturated scale point (da ∈ {1e-4, 2e-4}) away. The technical content itself is fully sound and the adoption advice stands: do not merge the branch without the `is_candidate` pre-filter, the k-gate fallback, and the assert→fallback.
