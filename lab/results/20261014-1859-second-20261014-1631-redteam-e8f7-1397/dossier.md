# Dossier — 20261014-1859-second-20261014-1631-redteam-e8f7-1397 (lens: second author on e8f7)

**Claim.** The checker's named gold experiment is done and passes: the composed-key fix for
the doll-chain simultaneity key — chain the shipped `lorentz::Frame`s and read the key off
the composed event map — runs on the design's own path (real `Frame::of`/`Frame::inverse`,
coefficients at 2^-100, event words at ae29's 2^-64 tick) and holds to **4.7e-10 ticks
worst case over 162 cases** (the 108-cell grid, β up to 0.99, planar nine-shear arms with
θ₁ ≠ 0 including the rotation-flip path, depths to 8, the t_B channel), i.e. ≤ 1 tick with
nine orders of margin, while the additive keys it replaces miss by up to **45,616 ticks**
(the understated worst case, now measured, not extrapolated) — so both controls of the
freeze-ready P6 arm have numbers and the ae29 re-emit spec is complete.

**Bottleneck.** Not a hot-path cost: the guarded invariant is the causal ordering the one
queue and the light-cone partition stand on (board "gravity at c"; PRINCIPLES #23). e8f7
falsified the additive key as designed (silver: the positive control was never run by the
author). This run supplies exactly that control on shipped code; it deletes the last open
prerequisite of the adoption (wiki `handoff`, open direction 1). No speed gain is claimed.

**Evidence.** External Rust probe (`probe/`, its own `[workspace]`, no crate edits) calling
`emergent_universe::lorentz::{Frame}` on events; f64 Lorentz oracle at the engine's own
read-back parameters (velocities snapped to dyadic words at 2^-40, read back through
`norm2`/`to_f64`, so oracle, additive keys and integer key all see identical parameters);
debug build (checked arithmetic — no `i128` overflow anywhere). Offsets in light-ticks,
c = 1. The original run's falsifier is vendored verbatim and regenerates the frozen record
(79/108 ≥ 1 tick, 52 ≥ 10; worst 4,069.9/5,066.9; named 15.18/15.18, 178.63/357.27,
130.07/140.47; depths 15.2/78.1/227.5/511.9/994.7/2,921.0) — snapped parameters agree with
the float-only record to four digits.

- **Positive control (the named experiment):** composed integer key, max |err| per group —
  G1 (108 cells) **7.3e-12**; G2 extended (β₂ 0.5–0.9, θ 45°/60°, β₁ up to 0.99)
  **1.3e-10**; G3 planar (θ₁ ∈ {20°, 30°}, θ₂ ∈ {75°, 110°}, φ ∈ {0°, 90°}) **7.3e-12**;
  named rows **5.8e-11**; depth 2–8 collinear and planar **6.4e-12**; t_B **3.6e-12**;
  worst overall **4.66e-10** at d = 8·10⁴ (t ~ 2·10⁵). Scaling signature: err(8·10⁴)/err(10⁴)
  = **8.00** — the measured error is the f64 oracle's own noise; the integer path's bound is
  ≤ 18 shears × 1 quantum ≈ **1e-18 ticks** by construction (nine shears per link, one floor
  each), plus ≤ 2^-84 from coefficient truncation at 2^-100 on ≤ 2^81-word values.
- **Negative control, same harness:** the additive keys on the same parameters reproduce the
  record exactly (numbers above; the perp-offset arm 0.00/0.00, as the analytic law
  predicts — only along-velocity offset shears).
- **The understated worst case, measured** (checker's [INFERENCE] ~4.6e4): (β₁ 0.9, β₂ 0.9,
  θ 45°, d 10⁴) → V1 **26,721.0**, V2 **45,615.6** ticks (predicted pre-run from the
  verified analytic law: 2.67e4 / 4.56e4). The β₁ 0.99 rows reach V1 35,153.8. The
  additive key is now falsified up to 9× the record's worst cell.
- **t_B channel, on the integer path** (t_B = 10⁴, no offset): collinear t_root =
  **16,666.67** = γ₁γ₂(1+β₁β₂)·t_B — an unscaled child tick misses **6,666.7** (66.7 %),
  the per-link product γ₁γ₂ misses **3,333.3** (33 %), the composed key errs **3.6e-12**;
  perpendicular t_root = **13,333.33** = γ₁γ₂·t_B — there γ₁γ₂ is the right carrier
  (miss **0.0** exactly), composed errs 3.6e-12. e8f7's wiki correction (the carrier is
  the composed map's [0,0], not γ₁γ₂) is now measured, not just derived.
- **Instrument self-check** (depth 1, β 0.5, θ 0.35, offset (3000, 4000)): additive err
  −4.5e-13 (float noise; exact at depth 1 as the design requires), composed key **bit for
  bit the oracle** (err 0.0).

Reproduce (each command; the whole `regen.sh` is ≈ 1.4 s of Python plus a cargo build,
~30 s warm / ~2 min cold):

```
bash regen.sh                       # everything, with frozen assertions
cd probe && cargo run -q            # the 162-case probe alone (0.1 s after build)
python3 analyze.py                  # asserts every number above against predictions.md
```

**Predictions.** `predictions.md` was written after instrument validation (one SELFTEST
line), before the decisive run. Every pre-registered item held: positive control ≤ 1e-9
everywhere (measured ≤ 4.7e-10); scaling signature in [2, 32] (measured 8.00); the record
reproduced within 1 % (it reproduced to four digits); worst cell 2.67e4/4.56e4 predicted,
26,721.0/45,615.6 measured; t_B carriers 16,666.67/13,333.33 with misses 6,666.7/3,333.3
and perpendicular γ₁γ₂ exact — all as pre-registered. The kill criterion (any |composed|
≥ 1 tick, or a word overflow) never fired.

**What would make it wrong.** The probe applies the chain per event (`Frame::inverse` per
link); the re-emit may instead compose one cached map per doll (shears applied to the map's
columns, refreshed at re-anchor). The shear count and the one-floor-per-shear bound are the
same, so the ≤ 1e-18-class guarantee transfers [INFERENCE: argued, not measured]; both forms
sit far below the f64 oracle's noise, so the measured agreement cannot distinguish them —
that is the honest limit of this instrument. The oracle is f64 (the analytic law it
instantiates was already verified to 5.3e-12 by e8f7 and to 1e-12 by its checker outside the
grid); the scaling signature separates oracle noise from real error. Velocities snap to
2^-40 dyadic words — coarser than a cell-owned exponent would be, but oracle and both keys
read the same read-back parameters, so the comparison is self-consistent, and the record's
float numbers reproduce to four digits. Cost of adopting the fix: ~9 integer shears per
link per event walk against ae29's one multiply-add (still noise against a 75–160 µs kick),
one composed map per doll refreshed at re-anchor where ae29 already refreshes the frozen
shear; no new machinery — the crate's own shears acting on the operand its header already
names ("events `(t, x)`"). Unmeasured and unchanged from e8f7: key staleness under thrust
between re-anchors; the Wigner rotation's effect on the spatial readout.

**PRINCIPLES.** #19: "if you find yourself fixing things that's oftentimes a signal that it
is the wrong representation" — the product form is the representation that "feels right":
measured in, falsification out, one instrument. #17: "leveraging EACH part of the computer…
the best part is no part" — the fix reuses the crate's existing shear algebra on events; no
new part. #23: "beyond c=1 means paradoxes… it allows to cheaply partition compute" — the
partition is only as sound as the key, and the key is now certified on the shipped path.
#10: "Run the simplest falsifying test first" — the positive control was the simplest test
that could have killed the fix; it did not.

**The lens may have missed:** as second author I ran the named experiment and little else —
planar coverage is two (θ₁, θ₂) families plus one planar depth chain, not a sweep; the
cached-composed-map variant is argued by bound transfer; I did not re-measure e8f7's
analytic-law cross-checks (its checker already extended them to 1e-12 outside the grid); and
I measured correctness only, never the re-emit's frame cost on a real doll tree.

**Wiki:** page `handoff` updated in `wiki/handoff.md` (Keys section, open direction 1, Runs).

Wall time: probe 0.1 s; falsifier 1.4 s; analyze 0.04 s; total with build under 3 min.
