# Dossier — 20261013-1145-second-20261013-0350-components-c914-00d2

Second author on c914 (silver). The checker's named experiment: run the same division
floor (Newton prototype included) on arm64 — "if the reciprocal also loses there, the
kill generalizes to the target machine and this is gold; if it wins, the lever revives
with a measured number, which is just as good a result." No M1 and no hosted arm64
runner is reachable from this lab box, so the experiment runs as the cheapest decisive
part: the c914 kernels, verbatim, cross-compiled for aarch64 (musl, rust-lld) and run
under QEMU-user TCG 7.2 — an architectural proxy on two axes, not an M1 measurement.
Everything regenerates via `regen.sh` (~5 min).

## Claim

**The multiply-only exact Newton reciprocal also loses on aarch64 — 2.8–2.9× the soft
routine's wall under TCG and 1.49× its executed instructions under an unbiased census —
and the aarch64 "soft" routine is itself already multiply-only on the fast_quad shapes
(zero `udiv` executed), so on the target architecture there is no divide instruction
for the "cheaper divisions" lever to remove: c914's kill of open direction 1's division
branch generalizes off-x86 in the only axis available without an M1.** One number
survives for the integrator's M1 re-measure to falsify: the same-mix 1.49× instruction
deficit (and the TCG 2.8–2.9×), not a wall time.

## Bottleneck

Board's `kick-jet`: "what is the cheapest exact kick on the shipped representation."
c914 bounded the division branch at ~1.2× on x86 (divisions 20–35% of the compile,
at their hardware floor) but the kill was x86-only; the checker named the aarch64
question as the difference between silver and gold. This run closes the reachable
half: no gold was reachable without an M1 (disclosed below), but the proxy's two axes
agree on the direction, and the structural fact (the compiler's aarch64 division is
multiply-only) removes the mechanism by which a cheaper-division win was imagined.
What it deletes: the expectation that the M1 re-measure might revive the lever; what
it leaves: the M1 re-measure as confirmation, with a 1.49×/2.8× expectation to beat.

## Evidence

All from `regen.sh` → `measure.sh` (raw: `probe-arm.txt`, `census-out.txt`). Arm64
binary: `aarch64-unknown-linux-musl`, release, workspace thin-LTO profile, kernels
extracted VERBATIM from the patched `div_bench.rs` by `mk_arm_bench.sh` (diff-checked;
the harness adds only a mode dispatch). Box: shared i7-4790, 8 vCPU, load recorded in
the probe. Operand shapes: c914's pairs_4096 (dividend < 2^127, divisor ∈ [2^20, 2^62],
high limb < divisor), quotient-chained.

1. **TCG wall (ns/div, 3 runs per pass, 2000×4096 divs each; two passes on record,
   loads 3.7 and 2.8):** soft `u128/u128` (__udivti3) **134–150** (133.7–136.1 /
   141.2–149.8); i128 133–142; `div_asm` two-limb recursion (the patch's non-x86 arm)
   **94–100**; Newton reciprocal **389–423** (388.6–391.6 / 415.2–422.9). Newton/soft
   = **2.8–2.9×**; Newton/asm = 4.1–4.2×; asm/soft = 0.67–0.70×. Exactness on all
   4,096 pairs: asm 0 mismatches, newton 0 mismatches (both builds, both passes).
2. **Executed guest instructions per division** (singlestep exec trace, N=12 vs 2N=24
   difference method — startup and the post-loop exactness sweep cancel): none
   (chain only) 3.0; soft **169.9**; i128 188.7; asm **88.3**; newton **253.0**.
   Newton/soft = **1.49×**. Independent cross-check: the difference-based mnemonic
   census (census2.py) reports 169.9/88.3/253.0 — the two instruments agree exactly.
3. **Executed-mnemonic census (capstone over the trace):** soft's hot path is
   csel 15.7, lsr 15.0, cmp 13.7, lsl 12.7, mov 11.0, add 7.9, **clz 7.8**, mul 4.3,
   … and **zero `udiv` above 0.1/div** — compiler-builtins 1.90's
   `specialized_div_rem::u128_div_rem` (804 B static) divides by reciprocal-by-
   multiply on these shapes. Newton is umulh 20.0, mul 17.0, mov 28.0, cmp 23.0 —
   the same instruction mix, 1.49× more of it. asm is the only variant executing
   hardware `udiv`: 2.88/div, in an 88.3-insn routine.
4. **x86 controls, same box, same day (the c914 record regenerates):** the shipped
   `div_bench` div mode printed 30.6–38.3 / 35.0–43.8 / 31.0–35.9 / 31.7–33.7 ns
   (soft/i128/divq/newton) across three passes (c914's frozen record: 30.2/35.0/31.4/
   31.6); the harness (same kernels, workspace example) 30.2–32.0 / 35.7–39.1 /
   30.9–31.7 / 31.5–32.0 under quiet load (one load-2.8 pass printed 37.9–49.3 across
   modes; ratios stable; `probe-arm.txt` freezes the regen pass, the earlier passes
   are quoted from the session log). One reproduction note: a
   standalone (non-workspace) rustc build of the same kernels slows Newton 2.6× by
   outlining `__fixunsdfti` — the harness must build inside the workspace (as
   `regen.sh` does) for the x86 control to reproduce c914.

## Predictions

`predictions.md` was written before the decisive runs (mtime-checked; only ROUNDS=3
plumbing smoke tests preceded it, and their numbers are quoted in it as "smoke").
Held: soft wall band (134–150 across two passes, in 130–230), newton wall band
(389–423 across two passes, in 350–500), "newton ≥ 2× soft" (2.8–2.9×), the x86
control (P3, all bands on the quiet passes), and
both held-out instrument checks (chain-only mode = 1.8% of soft, well under 15%;
N-vs-2N closure exact). **Failed, and the failures are the result:** the instruction
bands (predicted newton 300–600 and soft 60–150, i.e. a 3–6× ratio; measured 253 vs
170 = 1.49×) — because I assumed aarch64 `__udivti3` would be a shift-subtract/Knuth
routine with hardware `udiv`s (P2 said "1–3 hardware udivs"); it is not, it is
multiply-only (census fact 3). asm's wall band also missed low (97–100 against
110–190): the two-limb recursion is cheaper than I guessed. The headline prediction
— Newton also loses on aarch64 — held on both axes.

## What would make it wrong

- **QEMU TCG is not an M1.** Absolute numbers are meaningless; the two axes are the
  claim. The wall axis (2.8–2.9×) is distorted per-instruction (Newton pays
  ~1.6 ns/insn under TCG vs soft's ~0.8 — TCG prices Newton's long multiply chains
  more harshly than the branchy routine). The census axis (1.49×, same mix) is
  distortion-free, and a same-mix instruction deficit of 1.49× is expected to survive
  on any core whose multiplies are already ~1/cycle throughput — but the seed's `fdiv`
  and `__fixunsdfti` (1/div each, below the census print cutoff) are the residual
  wild cards. **Only the integrator's M1 run closes this**; the expectation to beat
  is 1.49× instructions / ≥1.5× wall, not the TCG 2.8–2.9×.
- If compiler-builtins changes `u128_div_rem` (or LLVM lowers `u128/u64-widened`
  differently), the soft baseline moves; the census pins the 1.90.0 behavior at this
  commit (frozen in `probe-arm.txt`).
- The asm-mode finding (two-limb recursion 0.67× soft's TCG wall, 0.52× its
  instructions, at 2.9 hardware `udiv`s) is a TCG+count observation on these shapes,
  not an adoption claim: TCG overprices those udivs (host `divq` ~30 cycles vs the
  M1's ~7–9), so the real margin is unknown; it is recorded because the patch's
  non-x86 arm already ships it.

Cost of adoption: none — nothing to merge; the instrument (extractor + cross-build +
census) is ~300 lines of scripts in this folder, and the c914 patch stays as the
probe. Fit with PRINCIPLES: "Compute only surprises… the cheapest compute is compute
not done" — on the target architecture the division-as-multiply is already done by the
toolchain, so the remaining deletion is panels (a law change), exactly as c914
concluded for x86; "Measure before claiming" — the aarch64 half of the floor is now
measured on two axes instead of assumed; "a failed experiment kills that configuration,
never the method" — the configuration (micro-optimizing the wide division, now on both
architectures' proxies) is dead, the floor→idiot-index method is not.

## The lens (second author)

The lens' risk was instrument worship: QEMU is a proxy, and I initially framed TCG as
"biased toward Newton" from first principles (guest udiv → host division) — the data
refuted that framing (soft executes no udiv at all; TCG's per-insn pricing penalizes
Newton instead), and the dossier's argument rests on the census, not the wall. What
this lens may have missed: the compile grid (division *share* of the compile on
aarch64) was not re-measured under TCG — out of scope for the named experiment, and
TCG's per-insn pricing distortions would make that share uninterpretable anyway; the
leaver `Passage::compile` under-sampling carries over from c914 unchanged.
