# work/ — how to reproduce BASE vs KEPT

- `patch.diff`: the deliverable — two bit-identical dedupes (`poly`'s `z²` in
  `crates/space/src/binding.rs`, `node()`'s `cos ψ`/`x(ψ)` in
  `crates/space/src/orbit.rs`) on top of HEAD.
- `instrumented-attribution.diff`: HEAD + patch + feature-gated (`profile`)
  phase timers and op counters. Zero effect on normal builds; build the bench
  with `--features profile` to see the phase split and op counts quoted in the
  dossier.

BASE (pristine) vs KEPT (patched), same load:

```
# KEPT (tree as this run leaves it)
cd ../bench && cargo build --release && ./target/release/rebind-bench tune 3
# BASE (revert the two files to HEAD)
git checkout HEAD -- crates/space/src/binding.rs crates/space/src/orbit.rs
cargo build --release && ./target/release/rebind-bench tune 3
# restore KEPT
git apply ../work/patch.diff
```

Interleave the two binaries run-for-run; the machine is shared (load 1.4–2.1
during the run) so absolute numbers drift by a few percent within minutes.
Expected: identical digests (`fd33f759b10e569f` tune, `c45b567dfc5b395c`
held-out), p50 within ~1% of each other.

Attribution build:

```
git apply ../work/instrumented-attribution.diff   # from HEAD
cd ../bench && cargo run --release --features profile -- tune 3
```
