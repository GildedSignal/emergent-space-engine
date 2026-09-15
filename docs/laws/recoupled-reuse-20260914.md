# Recoupled three-body interval reuse and repair (2026-09-14)

Isolated `es-linearized-retarded-gem-response-v0` on
`/private/tmp/emergent-coupled-response`. Not `production_law`. Not
`Engine::advance`. Laboratory measurement, not gravitational qualification.

Workload was declared before results:
`docs/laws/recoupled-reuse-workload-declaration-20260914.md`.

## What landed

`reuse_recoupled_interval_functions` and
`repair_recoupled_interval_functions` take the **recoupled three-body
compile** as the object. They copy complete certified interval functions
that end at or before the per-body causal cut, then repair the suffix
through the horizon. They refuse a pair (Job 2 pair fill-in). They
refuse empty extra / extra-ray. They do not copy pair interval functions
into the recoupled object.

H0117 stands: recouple leftover 0, source ops 1537 vs 1537.
H0112 stands: `share_compiled_pair_exterior` still refuses
`laboratory_encounter` id 99. Post-cone
\(|a\leftarrow\mathrm{entrant}|/|a\leftarrow\mathrm{partner}|=1.5193625031062006\).
Do not weaken 1.519.

## Measured (declared comparison)

Quiet pair plus named recouple of id 99 through H=6, dt=1/32. Distinct
late kick on id 0 at t=5, \(\Delta v=(0,0.05)\), same three masses.

- copied complete certified recoupled interval functions: **86**
- leftover versus independent `compile_source_response` of the same
  recoupled genesis plus that kick: \(\max|\Delta x|=4.768153\times 10^{-8}\)
  at 16 samples (bodies 0, 1, 99). Suffix-collocation remainder, **not**
  recouple leftover-0 identity.
- source_evolution 6 on reuse
- source ops (evolution + retarded solves): **1118 vs 1613**.
  \(1-1118/1613\approx 0.307\). Not 99.9%. Reconstruction 86 is off source ops.
- Repair 1 stays charged, off source ops.

Mid-horizon kick on id 0 at t=3 (invalidates certified blocks):

- copied complete certified prefix blocks: **73**
- leftover versus independent same-IC mid-kick compile:
  \(\max|\Delta x|=1.440815\times 10^{-3}\) at 16 samples. Named remainder:
  `worldtubes_from_interval_functions` uses `inertial_end` (omits ½\(ah^2\))
  over a longer suffix. Not papered to 0. Stays inside pair radius
  \(\approx 0.020278\), not encounter-scale \(0.364\).
- source_evolution 19 on repair
- source ops: **1022 vs 1656**. Repair charge 1. Not 99.9%.

Required ship/ray/clock/contact returned values on reuse, repair, and
the independent kicked compile. Extra-ray still cannot be labelled
equivalent completed source histories. Pair passed to the recoupled
reuse/repair API refuses.

Disk ~18 GiB free. Swap ~3.4 / 4.1 GiB used.

`cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1`
PASS (46).
`cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1`
PASS (8). wgpu not compiled. Qualify not run. `production_law` null.
Default `Engine::advance` stays `es-inertial-causal-v1`.

Six-card host: three-bodies / fleet look-for name recoupled
compile-once/reuse; solar / galaxy / black-hole remain unsupported.

## What this is not

Not finishing `/goal`. Not 99.9%. Not pair-interval fill-in after
recouple. Not H0110 pair late-kick as the recoupled object. Not H0117
1537 vs 1537 as a reuse fraction. Not evolve-then-copy. Not extra-ray
as equivalent completed source histories. Not weakening 1.519. Not
Einstein two-body. Not FMM.

H0119 closed the ½\(ah^2\) knot hole. H0120 put the extra kick knot on
the certified prefix grid (mid-horizon leftover 0 at 16 samples). See
journal-home `docs/laws/prefix-kick-knot-20260914.md`.
