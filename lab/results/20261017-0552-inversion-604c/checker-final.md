Working...
Check complete. Summary of what I did and found:

**Grade: silver** — written to `lab/results/20261017-0552-inversion-604c/check.md`.

**Reproduction** (runner's regen + my own rebuild from `work/patch.diff`): every counter agrees — 87/87 bails on the bare plane, slope 1.0002 candidates/ship, belt controls 186.2/187.1 with zero bails, form=3000 tier 65/65 bailed with 3,338 candidates and held_max 71. Wall-clock p99 differs with load (52.5 author / 44.5 regen / 46.3 mine at K=1000) exactly as the lab's orders-of-magnitude rule expects; the deterministic counts (over-budget frames 68 and 85, 23% game-time loss, 131.5 events/frame) reproduce exactly. The mechanism is confirmed in shipped code: `self.bodies` counts registrations across all dolls (`radial.rs:119,176`) and `move_reg` inserts each id into every bin of its range (`radial.rs:232-234`), so `hit` double-counts wide tubes against a `bodies/4` denominator other dolls inflate.

**Adversarial cases** (mine, all outside the author's tested set):
- **Decade up** form=10,000 extra=0: still 100% bail, candidates 10,038, **p99 445.8 ms** — the bail never turns off under concentration (`hit` grows 1.24/ship vs the threshold's 0.25/ship), which corrects cdf0's "small-N disease" scoping.
- **Formation only** form=3,000 extra=0: p99 134.6 ms — the ruin is the formation's own, not the belt walk.
- **Tier at the next belt decade** form=200 extra=10⁵: **zero bails**, kept 87/87 — the "200 ships re-kill the scans" crossing is a property of both populations, not a fleet constant.
- **Seed 2**: 87/87 bail, 32.1 + 1.00·K — law is seed-robust.

**Why silver, not gold:** (1) pre-registered P5 failed (frame does not stay smooth — honestly reported); (2) novelty is partial — the plane-scale bail and `bodies/4` mechanism were already recorded on `lab/wiki/scan-queue.md` by cdf0 (16 Oct: "Home's doll trips the N-relative rule exactly at the plane's flown N, 95% of coast captures") and 3999, uncited by the author; the dossier's "unseen" is wrong. New and real: the formation crowd law, the always-bail under concentration, the c439 "pin the near set" refutation, and the frame cost. I folded a provenance correction into the author's `wiki/promotion.md` in place. The one experiment to gold: per-worst-frame decomposition at K=1,000 splitting scan vs comb channels.

Tree restored clean (`git status` shows only `?? lab/results/`); no commits or pushes.
