Working...
Check complete. `check.md` written to the run folder; tree restored pristine (only untracked `lab/results/` remains); no commits.

**Grade: silver.**

Verdict in brief:

- **Reproduced** in a clean tree using the author's own documented baseline procedure (stash `pairs.rs`, strip `prof_exp`): kick 7,177–7,531 → 4,484–4,545 µs at ρ=1e-4 (1.61× vs claimed 1.72×); 41.0k → 20.0k at ρ=1e-3 (2.05× vs 2.08×). Held-out set e evals **bit-exact** against the dossier: 1,855,085/6,001,758/21,013,262 → 1,071,943/3,663,409/13,756,498 (0.578×/0.610×/0.655×).
- **Gates held**: 14/14 shipped belts missed=0 false=0; predictions honestly reported (P2 failed in the author's disfavour and was declared a miss — good pre-registration evidence).
- **Attack**: four adversarial belts of my own (σ_e=0.4, all-Wide coorbital w=1e-6, ρ=3e-3 hot, wide-a 150-orbit) — all zero missed/false with full count-identity vs the true baseline.
- **Not gold** because the magnitude bar isn't met: 1.6–2.1× on the metric, nothing deleted, no premise overturned — it cheapens the setup the 6 Oct gold measured rather than beating the slack skin above it. The gold experiment is named: the tangency-native window that deletes the shelf-crawl class (78% of sweeps at D<3ρ).
- **Author's misses**: "bit-identical event lists" overstates the instrument (counts were compared, not lists); the two-interior-minima risk was argued away, not probed; the ρ=1e-3 surprise mechanism unmeasured.

One process note from my side worth recording: my first baseline build accidentally reused a stale patched binary (the tree had the patched `pairs.rs` at build time), which briefly looked like a total non-reproduction. Rebuilt strictly from `git show HEAD:…` — everything then reproduced. The author's stash-and-strip procedure is sound but fragile in exactly that way.
