# Predictions (written before the decisive runs)

Context: the checker graded `20261007-2344-spacex-dbf9` silver for one reason — the
record carried no code (`work/patch.diff` never saved; the checker recovered the edits
from this runner's dangling stash objects `a2246852` + `8e5e31a2` but `/tmp` is not a
record). The named experiment to gold: re-attach the code to the record and make it
regenerate. I reconstruct the full patch from the two danglers myself (the checker's
`/tmp/spacex-dbf9-recovered.patch` holds only the 4 tracked files, missing `live.rs`
and `tests/h_live.rs`), publish it in this folder, and rerun the record from it.

Cases I have NOT tuned on (I have seen the author's table and the checker's abstract,
but not the raw instrument output except through their reports):

1. **Patch applies and builds.** `git apply` of the reconstructed patch onto a pristine
   `a838a28` worktree succeeds, `cargo build --release -p xtask` succeeds, and
   `cargo test --release -p emergent-universe` reports 58 passed, 0 failed.
2. **All five evidence rows reproduce exactly** from the patched tree: created
   444/3,426/3,228/5,310/7,203; reabsorbed 0/25/48/317/1,963; live
   444/3,401/3,180/4,993/5,240; rates 14.8/1.14/1.08/0.177/0.036; rebinds
   24/2,551/3,570/10,732/51,976; on-generator 34/39, 19/76, 23/76, 5/76, 4/76.
3. **The dossier's "swallowed-at-tube-resolution = 0 in every run" bullet is false.**
   I expect the checker's numbers: 1 (seed 5, 3,000), 127 (30,000), 283 (200,000),
   each ≤ 0.5% of rebinds. If my reruns print 0 there instead, the *checker* misread
   and the bullet stands — either way the log is the truth.
4. **Held-out: 200,000 game-s, seed 5** (author ran seed 1 there; the checker's seed 3
   was at 300,000): created within 2× of seed 1's 7,203, rate within 2× of 0.036,
   and the balance identity created − reabsorbed = live_now holds.
5. **The 0.2 GB extrapolation re-derives** from the reproduced 7,203-bit row:
   7,203 / 76 / 2×10⁵ ≈ 4.7×10⁻⁴ bits/body/game-s; × 10⁹ × 3,600 ≈ 1.7×10⁹ bits ≈ 0.2 GB.
