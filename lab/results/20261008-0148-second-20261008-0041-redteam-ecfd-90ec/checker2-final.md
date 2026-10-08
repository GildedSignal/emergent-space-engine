Working...
Check complete. `check2.md` written; tree restored to as-found (only `lab/results/` untracked).

**Grade: gold.**

**What I did:**

1. **Reproduction, all bit-identical:** `falsifier.py` → output matches the published prior run on `claude/lab-20261008-0041-redteam-ecfd` byte-for-byte; patched `advance_grid` Rust example and `falsifier2.py` regenerate `rust-advance.json`/`second-out.json` byte-for-byte. Timings 1.3/3.0/0.6 s.

2. **Predictions:** `predictions.md` (01:56) predates `falsifier2.py` (01:59) and all outputs (02:01). P1/P2 held in the pre-stated bands; both kill criteria verified unfired; the C1/C2 corrections recompute exactly (34.15–717.66; min flip margin 2.5534).

3. **Four attacks:**
   - **Nudge scaling:** artifact/(−nudge) constant to 6 digits over two decades — the floor identification is mechanistic, not fitted.
   - **Untuned e=0.9:** collapse + exact ν-linearity reproduce (ratios 10.000, 2.4996–2.4999).
   - **Real B11 path** (my decisive probe, ported EIH invariants → `Binary::key()` → `Orbit::compile`, oracle 6π/j²): B11 passes 21/21, but worst margin is **1.067×** at (p=20, ν=0.01) — not ≥2.5× — because the ν-path keys land outside the measured (p,e) family (+22% advance displacement at p̄=20). This confirms the author's disclosed caveat is load-bearing and *deepens* the finding: the frozen gate's allowance is nearly consumed at strong field by a non-GR invariant-labeling residue, not by anything GR-shaped.
   - **GR reference:** Damour's review (1212.3169) gives D(u)=1+6νu²; via the mass shell H²_eff = A(1+j²u²)+(A²/D)p²ᵣ, the script's s=−1 coefficient A²(1−6νu²) is the correct standard 2PN term — the code's "D̄" comment mislabels the inverse, physics unaffected.

4. **Novelty/goal fit:** no B11-oracle entry in HISTORY.md or the taste log; the only same-class finding is B13's. Premise-wrong finding on the board's live question (motion law v2 binaries), adoptable in one step — the exact Darwin oracle already exists in `xtask/src/behave/oracle.rs`.

**Recorded as missed:** the transfer is compiler-level, not doll-level (`Space::binary_cycle` never touches the measured `QuantizedMemo` family); the sign-flip test through the actual gate path is unmeasured and belongs in the oracle re-point.
