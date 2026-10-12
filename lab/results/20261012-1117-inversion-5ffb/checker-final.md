Working...
Check complete. `lab/results/20261012-1117-inversion-5ffb/check.md` written; nothing else in the run folder touched, no git operations.

**Grade: silver**

**What I verified:**
- **Provenance:** all 7 certlab sources hash-match the branch's evidence manifest; `phase.rs` differs only by the documented `tree_events` hook (verbatim `else` branch of `group_events`).
- **Bit-exact reproduction:** `invert bounds` (3/3 rows), `invert fuzz` (32 scenes, 20,396 contacts, 0 cert/emit/tree misses), and — via my own driver — the mild-e rows (cert_pairs 193147/777626, exponent 2.0094, ratio 3.5/3.4, `same_contact_set=true`), the ρ-scan (ρ↓100×: contacts 74→3→1, cert_pairs −0.5%), and drift-refuse (phase=true, reach_frac 0.467, tree never consulted, t=120.2s).
- **Independent attack:** re-derived the bounds analytically — the coded |f−E| term is exactly asin(e) (attained at E=π/2), confirming the audit and the author's P9 retraction; `centre = e + asin(e)` and `scale` are sharp. The certificate's math is sound; the finding is purely the cost-blind trigger.

**Why silver, not gold:** three held-out predictions failed (P4, P7, P9 — each honestly diagnosed, two strengthen the claim), and the record has defects: the shipped `invert cost` contains no `cost_series` calls, so the dossier's central rows (items 3–5) are not regenerable as shipped (I regenerated them externally); RESULTS.txt is curated (missing header lines and the drift n=4000 row); run.log, cited for timings, is 0 bytes.

**Gold path:** implement the cost-aware trigger in `group_events` (occupancy vs tree cost, ρ-aware `reach`) and show contact sets unchanged, tight formations kept, and work per real encounter flat in n — plus restore the series calls so the code regenerates its own evidence.
