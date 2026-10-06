Working...
Check complete. `check.md` written, nothing else in the run folder touched.

**Grade: silver** — real, reproduced, one named experiment from gold.

**What I did:**
- **Reproduced bit-for-bit** in a clean copy (11.4 s vs claimed 26 s): A/B1 16/37 misses, B16 35/37, nokick 19/19, all structural, 0 timing-stale. Verified the dossier's arithmetic (254.1 cand/body, |Δn| mean 0.355/max 0.75, churn ≈ 0.1–0.2 yr), all five quotes single-hit verbatim in the cached Readwise export, and all four cited plane costs in HANDOFF.
- **Ran 7 adversarial suites** beyond the author's: 3 extra seeds (result stable, A actually misses 52–59 %, not 43 %), λ sweep (per-kick closes only at λ≈16/orbit), k sweep (static k=64 still misses 19/19; only full-candidate-set catches), density sweep (N=100: per-kick already **0 misses** — the kill is density-scoped; N=1600: static 155/155, per-kick 83 %).
- **Found the C/D "hang" is a bug, not the host**: the author's policies push 4 heap entries per fire with no dedup — measured multiplicative growth (52 fires/yr → 123,141/yr by year 15; non-terminating by construction).
- **Completed the author's missing experiment** with a repaired one-entry-per-body heap: shear-sized displacement triggers reach **0/37 misses at 14.3 rebuilds/body/orbit** (η=half-window) — the first proof the proposed trigger works at all — but **matched cadence is indistinguishable** (2/37 at 6.7/orbit), because per-body shear rates are near-uniform in a uniform belt. The dossier's "must be relative-phase displacement, cadence is the wrong trigger" overstates: the defensible law is a size rule (budget = shear rate × window); displacement vs cadence only differ under heterogeneous shear (co-orbital formations).

Silver, not gold: predictions 3 and the A-control failed (the VOID honestly scoped in the dossier tail, but prediction 2's failure uncounted), the positive half of the headline never ran, no 10× realized (the working trigger costs 3.5–7× per-kick), and lesson 1 re-proposes the kick memo killed on 5 Oct without citing it. The gold rung is named: shear-sized maintenance on `crates/encounters`' real certificates, zero misses across seeds and densities, discriminated against cadence in a heterogeneous-shear scene.
