Working...
Check complete. Summary:

## Verdict: KILL of `eob-doll` (confirmed) — Grade: silver

**Reproduction** — every one of the 32 metric values bit-identical from the author's scripts in a clean tree (~25 s); `binaries.json`/`assists.json` byte-identical; transfer reference agreement 8.168e-11; same 4 ν-misses at the same seeds.

**Oracle values verified three ways** — ports are verbatim against `gr_oracle_extended.rs` (including re-deriving the author's exact e→0 limit); Schwarzschild quadratures vs my own Binet ODE to ≤1.1e-9 (advance) and ≤5.8e-14 (period); Damour–Deruelle vs my own EIH 1PN ODE within the integrator's own frozen 2PN-residual bands (20/p, 100/p²). The energy-map inversion and frequency rescale re-derived exactly.

**Adversarial findings:**
1. **Exponent bug (undisclosed)**: `run_reference`'s landing condition can never fire for the final target (it equals `t_end` and `h` is capped by `t_end − t`), so the fit ran on **99 of 100** handoffs. Corrected value over the true 100: **0.2328** vs stored 0.2303. Both fail the 0.2 gate; robust across every full-window reading (0.23–1.32). `metrics-check.json` carries 0.2328; `verdict.py` agrees with the author on every criterion → no DISPUTE.
2. **False dossier claim**: the raw *heliocentric* Δv (the rung's letter, which the author replaced planet-comoving calling it "unpassable by construction") actually passes **64/64 at worst 0.0019** — 5× looser than the author's own reading. Immaterial to the outcome, but the stated justification is wrong.
3. The 4 ν-misses confirmed at exact seeds (9–19% of a near-zero oracle ν-term, signs agree); no predictions.md ever existed (dossier admits).

**Silver, not gold**: no held-out predictions, plus the two undisclosed liberties above. The physics content stands: ν needs nothing beyond the energy map given invariant-matched ingestion (1024/1024, 632/632, 500/504), and the blocker moves entirely to the SOI handoff layer — new relative to H0205/H0206.

Deliverables written: `metrics-check.json` and `check.md` (116-word abstract); nothing else in the run folder touched, no git commands run.
