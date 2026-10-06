Working...
Check complete. `check.md` written to the run folder; nothing else there touched (all reproduction ran in a `/tmp` copy).

**Grade: silver.**

What I did and found:

- **Reproduced exactly.** Both dossier commands regenerate every stored cell (uniform 250/500 in 27 s, phalanx/clumped in 48 s; wall times differ ≤0.1 s). patch.diff is empty — nothing to apply.
- **The kill is genuine.** 5 of the claimed REAL misses re-adjudicated with my own 4M-point sampler (not the author's): all real (8.10e-5 … 5.87e-6, all < ρ). The diagnosed tangency mechanism verified root-for-root on pair (13,134): two alignment roots 0.1254 apart, d≈1.34/1.45e-3 at each, true min 8.1e-5 between, |ΔΛ|=7.7e-5 with no crossing.
- **My adversarial cases strengthen it:** highe (e 0.7–0.9) misses 54%, resonant misses 80% — structural across regimes. Shared solver exonerated (≤2e-7 rad at e=0.95). The two "FALSE ALARM" labels are adjudicator-anchor artifacts (golden-path hits register no roots), so the watch's precision is actually perfect by construction.
- **Why not gold — the record, not the physics:** uniform:500 "epochs/body 5.3" is contradicted by the shipped code (13.17; the "flat, O(N²) never materializes" narrative is false — epochs/body grows ∝N, 270/body at highe); cl_caught "1" vs actual 0; P7 silently dropped (my run: evals hold, recall collapses to 20%); P3's own two-point slope 0.39 already exceeded its 0.3 kill; the adoptable hybrid (per-body band filter + tier's windows/walk) is proposed, not built.

The named gold experiment: build that hybrid in `crates/encounters`' harness at belt scale and show zero adjudicated misses with per-body setup.
