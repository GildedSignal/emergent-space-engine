# Rung r5: the dense order is the sparse order, bit for bit (CPU arm)

Frozen by lab run 20261017-1330-redteam-68e7 before its execution (the integrator adopts or
amends before it counts as directed). Design: [docs/representation.md](../../../../docs/representation.md) §3 ("Two
evaluation orders of the same event graph, with identical bits"); law.md "Both orders give
identical bits" (B8). This replaces the recorded blocker "r5 remains uncreatable in this
lab" (wiki representation-premises, 20261017-1018-redteam-13c6): the dense order is not only
Metal. Its CPU arm is `emergent_lattice::chronon::Chronon`, portable; only the GPU arm
(`MetalChronon`, `metal_identity.rs`) is macOS-gated and stays with an M1-side run.

**Question.** The same battle (a free-fall frame of `crates/engine`, lattice contacts under
`es-lattice-relativistic-v1`, parent's tide as integer kicks at epochs, carries live):
evaluated in lockstep (`Chronon`, the reference grid) and sparse (`EventCore`), do world
digest, log digest and tide digest (`Outcome`) come out identical, across threads? The
planted negative applies the epoch kick one chronon late in one order only: it must break.

**Configurations.**
- `cpu-pair` (candidate): ten scenes × threads {1, 4}, both orders unshifted.
- `cpu-pair-shifted` (positive): both orders with the kick one chronon late
  (`with_epoch_shift(1)`). Shifted together, the orders must still agree — a changed law,
  not a changed order.
- `cpu-pair-late` (negative): lockstep unshifted against sparse shifted. It must disagree.

**Cases.** Eight scenes are `identity.rs`'s frozen ladder verbatim (s0–s7: 50–2000 bodies,
q 512–2048, scattered and formations, epoch 256 down to 1, s7 a kick-refusing storm), to
4096 chronons; two held-out scenes are this run's draw, registered in `predictions.md`
before the run (h1: 2500 bodies, q 512, seed 11, scattered, div 32, k 12; h2: 3000 bodies,
q 2048, seed 12, formation, div 8, k 14).

**Metrics,** one set per configuration (`metrics.py` assembles them from the harness rows):
- `identical_fraction`: the fraction of compared runs with equal `Outcome` (candidate:
  scenes × threads; the controls: scenes).
- `covered_scenes`: scenes with contacts > 0, kicks (epochs) > 0 and a live carry — the
  equality is about a kicked, contacting battle, not an empty one.
- `contacts_total`, `secs_lockstep`, `secs_sparse` (reported, not gated; this box is
  shared, orders of magnitude only).

**Output.** `metrics.json`, plus the harness's per-scene rows (`rows/r5-*.json`).

**M1 extension (not executable in this lab).** The same configs with `MetalChronon` as the
dense order, and the GPU/CPU arms of `metal_identity.rs`'s scenes, run on an M1; identical
criteria. The stub on Linux makes that arm VOID here by construction, which is why it is
not a config of this rung.

```configs
cpu-pair candidate
cpu-pair-shifted positive
cpu-pair-late negative
```

```criteria
ident behaviour identical_fraction >= 1
cover behaviour covered_scenes >= 10
```
