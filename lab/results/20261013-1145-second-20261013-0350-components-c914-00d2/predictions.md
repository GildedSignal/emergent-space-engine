# Predictions — 20261013-1145-second-20261013-0350-components-c914-00d2

Written before the decisive runs (only plumbing smoke tests at ROUNDS=3 ran; their
provisional numbers are quoted as "smoke" and I commit to bands wide around them —
nothing below was tuned on, and no full-length run has happened yet).

The checker's one experiment: run the c914 division floor (Newton prototype included)
on arm64. Instrument here: aarch64-unknown-linux-musl cross-build (rust-lld) of the
c914 kernels, verbatim, run under qemu-user TCG 7.2 (x86 host, i7-4790) — an
architectural proxy, not the M1. Two axes, stated with their bias:

- **TCG wall time**: every guest instruction pays roughly uniform translation cost,
  EXCEPT guest `udiv`, which lowers to a host division (~30 cycles on this host),
  and multiplies, which lower to ~3-cycle host multiplies. So TCG is biased TOWARD
  the multiply-only Newton and AGAINST the udiv-bearing soft/asm paths. Newton losing
  under TCG is therefore a conservative kill signal.
- **Dynamic guest-instruction census** (singlestep exec trace × capstone): unbiased
  per-instruction count, plus udiv/mul/msub/branch breakdown of the executed path.

## P1 — the headline fork (the checker's fork, resolved in the proxy)

**Prediction: the Newton reciprocal also loses on aarch64.** Bands:

- soft (__udivti3) TCG: **130–230 ns/div** (smoke 165);
- asm (two-limb digit recursion, the patch's non-x86 arm) TCG: **110–190 ns** (smoke 136);
- newton TCG: **350–500 ns** (smoke 428) — i.e. newton ≥ 2× soft, unlike x86 where all
  three tie within 5%.
- Instruction census: newton **3–6× more executed guest instructions** than soft
  (newton ≈ 300–600/div, soft ≈ 60–150/div). If newton's instruction count exceeds
  soft's, no plausible M1 microarchitecture reverses the ordering: at best every
  instruction costs 1 throughput cycle on the M1, so a 3–6× instruction deficit
  cannot be paid back by multiplies being cheap (they are already ~1/cycle there).

## P2 — the aarch64 structure (disassembly-level, checkable)

- aarch64 has no 128/64 divide instruction; `u128/u128` lowers to `__udivti3`
  (compiler-rt), which is a thin frame + `__udivmodti4` ≈ 60–70 instructions with
  1–3 hardware `udiv`s plus branches on the shipped shapes (dividend < 2^127,
  divisor ∈ [2^20, 2^62], high limb < divisor).
- Newton's aarch64 code is multiply/umulh-heavy (mul_hi → umulh+mul pairs) with an
  f64 seed (fdiv) and an `__fixunsdfti`-class conversion; straight-line but long.

## P3 — the x86 record regenerates (control, both sides)

Native x86 harness (same kernels, workspace example build) on this box today:
soft 28–36 ns, asm within 10% of soft, newton within 10% of soft, i128 33–40 ns;
exactness 0 mismatches for asm and newton on the 4,096-pair domain (the known
d=3 adversarial failure is outside pairs_4096). If any of these fails to hold,
the port lost fidelity and everything above is VOID.

## P4 — consequence for the claim (what gold would mean)

If P1 holds: c914's kill of the "cheaper divisions" branch generalizes to aarch64
in the only axis available off-M1, and the M1 re-measure (integrator) has a precise
expectation to falsify: the instruction-count ratio, not just a wall time. The lever
stays dead on both shipped-relevant architectures.
If P1 fails (newton ≤ soft on TCG wall AND ≤ 1.5× on instructions): the lever
revives on aarch64 with a measured number, and the wiki page must reopen it.

## Held-out cases (not tuned on)

- The `none` baseline mode (step-only chain) to subtract loop overhead — its
  per-step cost must be ≤ 15% of soft's per-division cost, else the harness is
  measuring the chain, not the division.
- Instruction census at two ROUNDS values (N and 2N, difference method): the two
  must agree within 2% or the counting instrument is broken.
