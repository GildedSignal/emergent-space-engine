Working...
Check complete. `check2.md` written; tree restored to clean (only untracked `lab/results/`).

**Grade: silver.**

What I did and found:

- **Reproduced exactly** from `work/patch.diff` in a clean tree: arms A/B digests match the author's and the original run's (`632b4b53…`), and `live`/`hist`/`hist_after_prune` match **to the KB** (903,411 / 572,188 / 82,708 KB); RSS within 0.15%, trim 0.14%. Predictions timeline clean (11:38 vs arms 11:39+).
- **Mechanism holds:** 10.2 kB/kick flat across four arms; 19.2 kB/handout construction marginal in C's clean phase; `settle` provably bypasses prune (universe.rs:876 vs :909); dashboard lie measured at 20×.
- **The decisive control is broken:** arm B was never "no battle" — the author's own bench-B2 JSON shows 1,089 slices and 4,501 encounters during play. A 2,000-lu gap is ~4×10⁻⁶ of the fleet extent against the frame's r_p/32 ≈ 1.6×10⁸ lu size rule. The dossier's "zero encounters" is a headline its own log contradicts — that costs gold under the lab's rules.
- **My adversarial runs supply the missing control** and agree with the physics: true dissolve at gap 9.7×10⁹ → 1.28 GB (all ships kick from t≈0); never-meet at gap 3×10¹⁰ → 402 MB with 234 MB of pure cadence-kick history, zero encounters. Memory = kicks × 10.2 kB regardless of cause; encounters only raise the kick rate (~2.4×).
- Minor: "all 40,000 construct" overstates (guard at 38,026 bodies); `account_after_prune` drops the real prune's `oldest − 2²⁶` floor (immaterial at the post-settle state — verified).

One experiment from gold: rerun B with a dissolving gap and correct the control description — my runs of exactly that already land on the author's mechanism.
