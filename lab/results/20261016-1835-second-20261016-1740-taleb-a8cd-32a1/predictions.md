# Predictions (written before the decisive experiments)

Question: the parent run (20261016-1740-taleb-a8cd, silver) proved the B12 corpus is
libm-conditional; the checker held gold back on one named experiment — a clean-tree regen whose
steps 1–5 are non-empty and identical — and named one missed experiment: does a CR-only seed path
give back a stable corpus ("judged 16/16")? This run does both.

## The gold leg (the clean-tree regen)

- PG1: with the phantom `work` workspace member dropped from patch.diff (libm stays as xtask's
  dev-dependency; Cargo.lock carries its checksum), `regen.sh` from a restored tree applies the
  patch and steps 1–5 run and are **non-empty** (the parent's delivered regen.log had them all
  empty: the missing-manifest death).
- PG2: the numbers are **bit-identical** to the parent's (same box, xtask/crates unchanged
  between a523ace9 and c9657cd1 — verified by diff): the seven deterministic reds (B12 false for
  Echo; ship 3 = #57 at 7016 kicks, across_kick 24.37109375, 8.409466703853747e-8); census
  judged 14/11/8 at pristine/±1 ulp, musl 15/16; crossings
  [10,8,8,14,16,30,22,22,12,34,42,8,28,12,12,22]; ulp-stability 7016 → 5423/5424 kicks with
  8.409e-8 / 4.563e-9 / 1.478e-7.

## The CR experiment (the checker's named missing probe)

The seed path's non-CR calls are `cbrt` (in `hill`), `powf(r,−0.5)`, `cos`, `sin`; the draws
themselves are portable (SplitMix64 + correctly-rounded arithmetic). `work/crseeds.py` rebuilds
the seed path correctly rounded at 60 digits (already validated: its r and α match the parent's
glibc prints on the five cross-checked ships — α bit-identical, r 0 ulp on all five, so glibc's
cbrt/powf/trig are CR on these inputs and the CR table is a sound object).

- PC1 (portability control): the Rust probe's assertion that the table's k and α bits equal this
  box's `sample::handoffs` draws passes for all 16.
- PC2 (distance): glibc-vs-CR seed distances are 0 ulp on every component for most ships; where
  they are not, ≤ 1–2 ulp (glibc is CR on the parent's flagged calls; the unchecked `cbrt(mu/3)`
  is the one that may differ, and it would move r on all ships at once).
- PC3 (the corpus): CR seeds do **not** give back the frozen corpus. The parent's ±1 ulp census
  (14→11→8 judged) says any last-bit change reshuffles a chaotic 200-period walk, and CR differs
  from glibc by last bits (PC2). Central guess: judged 13–16 out of 16, ≠ the frozen 16/16, with
  at least one ship's crossings below 20. If CR seeds *did* return exactly the frozen corpus
  (16/16 judged, all crossings ≥ 20), the seed leg of fix (b) alone would repair the instrument —
  that is the kill criterion for "the walk must go CR too".
- PC4 (the failing observable): `j_run` on the CR seed of kept index 3 (#57) is past
  `build_scene` pure integer arithmetic, so its value is machine-independent by construction. It
  lands inside the parent's measured ulp scatter (kicks 5423–7016, over-work 4.6e-9 … 1.5e-7).
  Which side of the 5e-8 bar it lands on is a coin I do not call: either outcome is a result
  (pass everywhere, or fail everywhere — the point is it stops being a per-machine coin flip).

Kill criteria: if PG1/PG2 fail (steps empty or numbers differ), the parent's record does not
regenerate and the silver stands with cause. If PC1 fails, the CR table is not the same
candidates and every CR number below it is void.
