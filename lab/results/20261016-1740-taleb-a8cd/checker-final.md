Working...
Check complete. **Grade: silver** — `check.md` written, wiki page corrected in place, tree restored.

**What I found:**

1. **A delivery hole that breaks the run's own record.** `patch.diff` adds `work/` as a cargo workspace member, but no `work/Cargo.toml` was ever delivered — every `cargo test -p xtask` in regen steps 1–5 dies on the missing manifest, so the runner's `regen.sh: exit 0` is vacuous (regen.log steps 1–5 are empty). The author's "every number regenerable" claim is false as shipped. After recreating a minimal `libmprobe` stub, **every number reproduced bit-exactly**: the seven deterministic reds (B12 false for Echo; #57 at 8.409466703853747e-8 / 7016 kicks), census 14/11/8 judged at pristine/±1 ulp, musl corpus 15/16 with different members, ulp-stability triple 8.409e-8 ↔ 4.563e-9 ↔ 1.478e-7, freeze-commit control bit-identical at verified c84f5787, and the full suite 10-failed at ~533 s (then 9 on rerun — flaky tail as claimed).

2. **Attacks:** ±4 ulp (outside the author's range) → judged churns 14→9→12, mechanism holds a fortiori; the "flaky" scale test **fails even solo** under load (same `Option::unwrap` B10-refusal signature at scale.rs:187) — load-class stands but "passes when rerun alone" overstated; two full-suite runs (10 then 9 failures) confirm the load-wandering tail against the fixed seven.

3. **Novelty clean** — answers replay-gate's open direction 4 (7559) by mechanism; no prior libm/machine-channel claim anywhere in HISTORY or the wiki. Page corrections: "8 ships under 20 crossings" → **9**, the solo-pass overstatement, ±4 ulp datapoint folded in.

4. **Silver, not gold**, solely on the record: one edit (drop the `work` member or deliver its Cargo.toml) plus a clean-tree regen rerun makes it gold on every other leg — mechanism verified in source, pre-registered predictions held (P2 honestly amended), premise shown wrong against PRINCIPLES' "Floats never decide them", adoptable in one step.
