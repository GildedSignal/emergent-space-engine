Working...
Check complete. `check.md` written to the run folder; nothing else there changed in content (the reproduction rewrote `falsifier-out.json` bit-identically, as the dossier's own command does).

**Grade: silver.**

What the check established, in brief:

- **Reproduction**: bit-identical from the shipped script; predictions.md (19:32:24) precedes run-decisive.log (19:32:30); patch.diff empty; all headline numbers match.
- **Decisive attack**: at the operating ε=1e-6 the quantum gate is 100% saturated — the reported 3.9×10⁴ events/unit is the *assumed cap* (pair count × 1/source-orbit), not a measured bound. Uncapped requirement: 1.4×10¹² ≈ naive pairwise (2.55×10¹²). The gate binds only at ε≥1e-3. "Flat in N" at saturation is a grid identity.
- **Code/text contradiction**: dossier claims cap = ν=8 kicks/orbit; code caps at 1.0 → headline understated 8× (true ratio 0.123, not 0.015, at 10⁶). Conclusion survives, number doesn't.
- **Robustness credit**: coherent kicks and 50%-ship-mass leave the capped result unchanged.
- **Number errors**: "~1 event per game-hour" is actually 1.0×10⁻⁵ at 100×; "~10⁻⁴ at 10⁹" is 1.5×10⁻⁵ (both conservative); cascade "peak" is a histogram density over 700 fixed N-independent samples — a control that cannot fail.
- **Novelty**: OC#50 open with no owner; gravity-as-news already exists (memo §5, R5 cursor), but the traffic law, dead-reckoning/MVCC/GVT mapping, and snapshot-age-by-geometry argument are new to the repo.
- **Gold experiment**: quantize far-field news to one update per source-orbit per consumer aggregate on the plane, and test B12/B14-class gates against a full-news reference — validating the cap kills the 10¹² wall with evidence. It sits one step inside the queued b-news-gravity build.
