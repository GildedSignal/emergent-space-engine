Working...
Fixed and verified. Root cause: the runner's first regen call at 07:49 raced run.sh's save-and-restore — the tree still carried the kick2 edits, so the forward `git apply` collided with the already-present `Some("kick2")` arm at `main.rs:518` (the tree was restored only afterwards, which is why the patch checks out clean now). regen.sh now applies the patch only if the tree is clean, treats reverse-check success ("already applied") as a valid state, reverses only what it applied itself, and hard-fails with diagnostics if the patch fits neither state.

Verification:
- Clean tree: exit 0 in 13.9 s (build 5.3 s), writes both JSONs, tree restored clean.
- Already-applied tree (the exact failure state): exit 0, `regen: work/patch.diff is already applied; using the tree as-is`.
- Every dossier number regenerates exactly: pairs/kick 812.8 (all eps), changed_fraction 0.0024/0.0777/0.0861, armed_stay_frac 0.2138/0.0671, flips 28.7/28.6 and 35.4/33.9 per kick, knife_share and at_risk 0.0000, resid_med_syn 1.04e-5/1.72e-3, c tails −111/+104, evals/kick 16,892/17,322 vs checks 41.5/42.7 and hits 37.4/38.7, dry scan 108 µs/kick, edge churn 0.00/0.33.

Claim: regen.sh was killed by a save-and-restore race, not a bad patch — it now regenerates every dossier number (812.8 pairs/kick, stay fractions 0.214/0.067, 16.9–17.3k evals against ~42 exact checks) in ~14 s from either a clean or an already-patched tree.
