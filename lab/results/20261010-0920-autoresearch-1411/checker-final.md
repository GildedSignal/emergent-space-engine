Working...
Check complete. `check.md` written to the run folder; tree restored to HEAD (only untracked `lab/results/` remains).

**Grade: lead.**

What I did and found:

**Reproduced (exactness holds completely):**
- Rebuilt baseline (bench example only) and patched binaries from HEAD; all 4 tuning + 4 held-out world/log digests bit-identical between them.
- Three adversarial worlds of my own — relativistic-law trapped gas, two velocity classes at |x| ≈ 2³⁸ near the validation edge, boxed crowded-axes (class frames + walls together): digests identical.
- 300k-sample fuzz of `first_wall` against the pre-patch i128 expression, including 62.5k samples whose gaps exceed i64 and force the exact fallback path, plus all i64 corner combinations: 0 mismatches. The guard is exact, not just in-domain.
- 38/38 tests pass, matching the dossier.

**Not reproduced (the headline):** pinned-core A/B under the author's own protocol gives crowded −0.4%, gas-sparse/dense −2.1%, random-pass +0.1% — not crowded −15.3%; alternations overlap, contradicting "every kept run beat every baseline run". For crowded to gain 15%, `entry_time`'s divisions would need to be ~20% of its runtime; eliminating them moves my build ~1–2% — a ≥10× discrepancy in the profile claim, and the rdtsc profile it rests on was reverted and is not regenerable. The direction survives only on container worlds (`first_wall`), at 0–6%, near the author's own ±3% noise band.

**Verdict logic:** correctness is solid and the patch is free to adopt, but it moves no board bottleneck by 10×, deletes nothing, corrects no premise, and its claimed magnitude did not survive independent reproduction — lead, not silver. The run's real value is its named blind spot: per-pair "cannot hit before T" certificates deleting the ~20 neighbour visits per prediction (98.4% of `first_hit` calls return `None`) — that is the rung worth writing, and this patch can ride along with it.
