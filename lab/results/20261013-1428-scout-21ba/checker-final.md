Working...
Check complete. `check.md` written, tree restored (patch reversed, my probe removed, runner's probe-out.txt in place; only `lab/results/` untracked, as at start).

## Verdict: **gold**

**Reproduced**: `regen.sh` exit 0; all 18 rows bit-identical in every physics column (only compile-time jitter differs). The mapping holds at source level, not just numerically — `node()`'s `excess` is exactly `(1/√(1−q·a)−1)/q`, the factor 2 is `scale(1)`, Δφ is stored Q30 (`lib.rs:65`), and `q_key = 1/(p·k)` is `bound`/`compactness` verbatim. I re-derived the closed form independently (cosψ = 2sin²u−1 substitution).

**Attacks — all confirm, past the author's grid** (independent probe, AGM-K instead of RF):
- e = 0.99999: relerr 3.4×10⁻¹⁰, knots 282, compile 325 µs — explosion continues, closed form flat
- q = 0.2375, m = 0.947: 8.7×10⁻¹¹; p = 2² refuses exactly at the m→1 separatrix
- e→0 and untested e: 3.2–6.3×10⁻¹⁰ throughout
- **τ/t channels verified** (the author's largest cited-not-measured qualifier): source-derived `tn`/`d`/scale give 2.3–7.6×10⁻¹⁰ agreement on every strong row — the author's named next experiment, done here

**Novelty**: the Opus memo (§4 "Rejected") named Carlson's integrals and deferred them on two premises now both measured false; the revisit condition ("compiles show in a profile") is met. Premise flip + first verification on shipped code.

**Page corrections** (three): "verified exact" → "to its Q30 output quantum"; 197 → 191 µs (regenerable number); checker note appended with the τ/t verification and extended domain. The author's resolution of the page's standing merge conflicts was schema-legitimate.

**Not gold-blocking, stated in check.md**: the 10²–10⁴× is f64-measured; the integer Carlson port is unpriced (9384's 54 ns isqrt prices its only non-add primitive); the crossing-table/readout half of the walk is unpriced; and the constant 3–5×10⁻¹⁰ level is an envelope with a second, unseparated source (it falls to 10⁻¹¹–10⁻¹³ at high q).
