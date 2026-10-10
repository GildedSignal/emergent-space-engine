Working...
Check complete. `check.md` written — **Grade: gold**.

**What I did:**
- **Reproduced** the dossier's full command set in a clean copy: all 8 stored JSONLs regenerate **byte-identical** (191 s vs author's 192 s). Selftests pass; the kernel-exactness claim is a trig identity I verified independently (2·atan(μ/bv²) ≡ 2·asin(1/e), worst rel err 2.3e-16).
- **Predictions audit:** `predictions.md` 15:52 → code final 16:19 → runs 16:26–16:29. Eight pre-registered; five held (two stronger than claimed), three failed and honestly reported as the informative result (N-flatness, self-limiting mass scaling, 0.11-bit Coulomb cost).
- **Five adversarial cases:** fresh seeds (±20%, exponent 0.57 ✓); 2:1 resonant two-ring, the author's named hole — **stays sub-diffusive** (σ_E exp 0.37), no coherent pumping at belt masses; N=1024 — flatness holds (σ_E 1.58e-3 vs 1.69e-3 at 256); high-e crossing belt — no pathology; μ=3e-4 row (stored artifact missing) — reproduced at 7.8e-2@6 orb vs 6.9e-2.
- **Novelty:** HANDOFF line 70 said H_live "not measured yet"; distinct from 98bc's birth-program statics. Direct hit on the board's 10⁹-in-8 GB decider; adoption is one rule line, no code.

**Gold despite one real erratum I found:** the differential-entropy constant is √(2πe) ≈ 4.13, not 2.07 — the dossier undercounts 4 bits in the favourable direction, making a physical belt at q=1e-6 marginal (~31–43 bits vs the 34.4 budget) rather than comfortably fitting. The actionable verdict (q ≤ 1e-5 fits, −13.3 bits/decade lever) survives correction; the per-body-store deletion (7×–1000× off the floor) stands.

Folder otherwise untouched; no git operations.
