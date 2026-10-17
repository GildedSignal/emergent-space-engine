# Predictions (written before the decisive run)

The premise under test (representation.md §3 L70, premise 4 of the census): the sparse and
dense orders of one event graph give identical bits, on the existing crates. The recorded
blocker (wiki representation-premises, 20261017-1018-redteam-13c6): "r5 remains uncreatable
in this lab: lattice-metal's dense order is #[cfg(target_os = "macos")] and compiles to a
stub on Linux — an M1-side run owns it."

My attack: the dense order is not only Metal. law.md L50 says "CPU, or Metal on the GPU";
the CPU dense order is `emergent_lattice::chronon::Chronon` (portable), the sparse order is
`emergent_lattice_event::EventCore`, and `crates/engine/tests/identity.rs` already pairs
them over 8 seeded battle scenes — ungated by any `cfg`. Only the GPU arm (MetalChronon vs
CPU, `metal_identity.rs`) is Mac-only.

Cases I have not tuned on, and what I expect:

1. **P1 (the 8 frozen suite scenes, Linux, agonbox).** Every scene: lockstep and sparse
   agree on world digest, log digest and tide digest (Outcome equality), with contacts > 0,
   kicks (epochs) > 0 and sub-quantum carries present, at 1, 4 and 8 threads. Expected:
   all pass. Basis: the suite is the B8 judge, believed green on the M1; nothing in the
   crates is OS-gated except Metal.
2. **P2 (held-out scenes, my draw, not in the frozen ladder).** Two fresh battles —
   (a) 2500 bodies, q=512, seed 11, scattered, div 32, k=12; (b) 3000 bodies, q=2048,
   seed 12, formation, div 8, k=14 — run to 4096 chronons. Expected: identity holds in
   both (same Outcome, both orders, 1 and 4 threads).
3. **P3 (negative control).** Kicks applied one chronon late in one order only
   (`with_epoch_shift(1)`): identity breaks (different Outcome) on every scene, suite and
   held-out. Shifted in both orders: identity restored. Expected: breaks on all, restored
   on all — the rung can fail.
4. **P4 (cost, order of magnitude only).** At these sizes (50–3000 bodies) on Linux the
   sparse order is not faster than lockstep (within ~10×, either way); identity, not
   speed, is the premise. No speedup claim is made.
5. **P5 (what stays open).** The GPU arm (MetalChronon bit-identity, and GPU/CPU at
   scenes the stub cannot run) is genuinely Mac-only; a Linux run cannot execute it. The
   r5 rung I freeze therefore carries the CPU arm as its configs and names the M1 arm as
   an extension, not a config.

Kill criterion for my own claim: if any P1/P2 scene differs between orders on Linux, the
premise "identical bits" is broken in the field (not just unguarded), and that is the
result — a premise kill, reported as such.
