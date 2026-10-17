# Predictions (frozen before the decisive D-runs)

Scene: the checker's named archipelago probe. `tax` battery, 128 cannon cells (stagger 30,
the conflict wave that latches E≥128 alone) plus a quiet sea of 1,280 one-world cells at
pitch 784·q = 200,704 (quiet-quiet edge gap ≈ 200k: bridged by a latched quiet forecast
v = 2·(2E+E−1) ≥ 736 at E≥128 within the ≤ 272-chronon plan lookahead, not bridged at
E≤64 where v ≤ 254·272 = 69k). Two couplings:
- **D1 coupled**: sea at x0 = 156,250·q = 40.0M — inside the wave region's pumped forecast
  reach (pilot: cap64 panics here, shipped swallows the sea);
- **D2 decoupled**: sea at x0 = 400,000·q = 102.4M — beyond any pumped reach (pilot: cap64
  clean); only the global latch couples wave to sea.
Arms: shipped, ES_CAP=16, ES_CAP=64. Horizon 6,000 (2×3,000), margin 2.0, min_region 1.
Known from pilots/calibration (not predictions): 64-cell sea versions of D1/D2; the
stagger sweep 300–99,999 with no sea (shipped panics at ≥ 30,000, E up to 2²⁷; clean ≤ 1,000).

## The cases I have not tuned on, and what I expect

- **PD1 (D1, coupled, 1,280-cell sea):** shipped finishes with the sea swallowed whole
  (end regions ≤ 8, escal ≥ 2²⁰, merges far above the wave-alone ~100) and a digest
  identical across its 2 draws; cap16 and cap64 break the shipped rollback invariant
  ("would revise its published tick", alloc.rs:1510) or DNF in at least 1 of 2 draws each,
  producing no digest. If a cap arm survives both draws with a digest equal to shipped's,
  the panic was a flaky draw and must be reported as such.
- **PD2 (D2, decoupled):** all arms finish; digests bit-identical across arms. Shipped's
  sea still collapses (the latch is global: end regions small, merges high, wasted-ops
  above the caps'); the caps' sea stays fine-grained (end regions ≳ 1,200, merges ≈ the
  wave's own). Walls within 2× either way (a quiet swallowed giant and a fine-grained sea
  are both viable at 11.6k bodies) — no adoption-relevant wall separation expected.
- **PD3 (the basin is shipped's, not the cap's):** at stagger 30,000 with no sea, cap64
  panics like shipped (the invariant break needs only a deep restore, not wide margins).
  If cap64 survives where shipped panics, the basin needs the wide latch — reported either
  way; this decides whether the panic class belongs to the ratchet or to rollback depth.
- **PD4 (the checker's 28,160 datum, if time):** at 2,560 cells / stagger 30 / horizon
  1,500, cap64 finishes < 120 s with ≳ 5,000 end regions; shipped's regions collapse
  (≤ 200 end) and it finishes ≥ 2× slower or DNFs ≥ 250 s. If both finish, digests
  identical (the certificate never moves).

## Kill criteria (frozen)

- ES_CAP stays killed (and the kill hardens to a certificate break) if any same-scene,
  draw-stable pair shows a cap arm panicking/DNFing where shipped finishes.
- ES_CAP's verdict flips to "conditional on quiet-heavy scenes" only if some scene shows a
  cap arm strictly better on a stable signal (wall or wasted-ops, digests intact, no
  panic) while shipped pays a real over-merge tax.
- Shipped's own panic basin (stagger ≥ ~30k, no sea needed) is reported as a separate
  finding regardless of the cap verdict: a reachable invariant break in the shipped
  allocator, arm-independent if PD3 holds.
