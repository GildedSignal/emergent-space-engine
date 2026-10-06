Grade: silver

**Abstract.** Claim: every law update can be one rounded triangular integer shear — exactly accumulated, rounded once — giving bit-exact invertibility and measure preservation by construction; floor walks, nearest/carried do not. Reproduced bit for bit (exponents, identities, digests, Mitchell 6.6×10⁻⁴). Adversarial reruns confirm floor walks (0.17 conjunction-free, 0.39 at 200 orbits) and the fixed-grid carry constraint (proof verified), but "bounded at 0.001" is window luck: fresh seeds 0.053, 200 orbits 0.075, and in a conjunction-free two-body scene nearest-shear (0.057) is float64-class (0.082). Exact accumulation costs 0.34× the software float (caveats below). Gain: rounding-rule and carry-modulus constraints for JANUS; adoption is a kicks/quantize rewrite. Not 10×, not yet on the plane.

## Reproduction

- `rustc -O` on `work/probe_a.rs`, `probe_b.rs`; `python3 work/probe_c.py`; empty `patch.diff` applied (no tree edits — verified). Every physics number in `dossier.md`'s table matches `work/probe_a.out` exactly (exps, fin_med, ident, min_d, onestep fails); probe B counts and probe C digits identical. Only ns/op moved (load 8.2 vs 3.3): mine 519/898/936/525/1006/220 (A1–A6) vs recorded 321/324/321/176/329/78; probe B 223/663 vs recorded 77/217 — ratios 0.34–0.35 unchanged.
- Timing: `predictions.md` (22:37:45) predates probe sources (22:55, 22:57) and outputs (22:59). Pre-registration is genuine.
- Numbers differing from the dossier text: it quotes probe B at "106 ns vs 329 ns (0.32×)" while its own `probe_b.out` says 77/217 (0.35×); and probe A "283–297 ns" vs recorded 321–329. Same story, but the prose does not match the saved evidence.

## Held-out predictions

Held: (1) bit identity A1–A4, A5 fails (robust in every scene I ran); (5) exact accumulation 1 digest; (7) 0.34× ≤ 1.5; (8) 0.086; (2) partially. Missed, honestly reported: A1 band, A5 ≥ 0.4, A6 ~ 0.4, (3) falsified, (6) falsified, (9) by 35%. The author's diagnosis of (6) is correct: my stress variant (masses to 2⁴⁶, 2⁻²⁰ grid, i128-safe d3) still shows 1 digest in 200/200 — the order-dependence of the truncating chain sits far below any rounding boundary at these lattices.

## Adversarial cases (mine)

1. **Fresh seeds** (16 new initial conditions, same scene): A1 0.152, A2 0.053, A3 0.054. The 100× separation of the headline (0.108 vs 0.001) becomes 3×. The *ordering* survives; the magnitude does not.
2. **200 orbits** (4× window): A1 0.393 (fin 0.34 — the floor walk accelerates with window), A2 0.057, A3 0.075. A2/A3 walk too; they are not bounded.
3. **Conjunction-free scene** (GM_P=0, pure stellar two-body, 200 orbits): A1 0.169, A2 = A3 = 0.057 (identical lists — with a massless planet the carry degenerates to nearest, a good internal consistency check), A6 0.082. Nearest-shear is *float64-class* here. "Exact measure preservation ⇒ B12-class guarantee from structure" is overstated: bijection plus unbiased rounding slows the walk ~3–7×, it does not bound it. What remains decision-relevant: A2/A3 stay under B12's 0.2 in every scene; A1 (0.39) and A5 (0.27) do not.
4. **A5 (adaptive rescale)** is worst-or-near-worst and non-invertible in every scene (16/16 one-step fails). The case for retiring the rebinding re-expression is robust.
5. **Finding 2 verified by hand**: with M=30, n2=0, (v,70)→(v+2,10) and (v−1,100)→(v+2,10); once a wider modulus can leave the carry ≥ the current one, the step is non-injective. The fixed-grid repair is sound, and `unkick`'s ceildiv construction is genuinely inverse (checked algebraically and by the identity tests).
6. **Probe C extremes**: 6.6×10⁻⁴ over [10⁻³⁰⁰, 10³⁰⁰]; a 6-factor chain over 4 octaves 2.2×10⁻³ — still inside 1%. Solid.

## Probe-quality nicks (conclusions unaffected)

- Probe B's float arm casts `dens[i]` (i128) to i64: **6510/19200 sources (34%) exceed i64::MAX and wrap**, so that arm is not faithfully "the plane's chain" for far sources (still deterministic per source, so order-independence and cost stand).
- Probe B's exact path adds `1<<61` where round-to-nearest at 2⁻¹⁰ needs `1<<51` — a constant ~512-quantum offset, invisible to order-independence but contradicting its own comment.
- The cost comparison precomputes the exact path's `gm·dx` and `d3` outside the timed loop while the float arm pays them inside; division dominates so the sign is probably right, but 3× is bench-shaped (and untested on M1, as the lens admits).

## Novelty

The shear-as-bijection is substantially prior art *in this repo, the same evening*: `lorentz.rs` (commit 7f81a9c, 22:20, 17 min before predictions) builds handoffs as integer shears with exact inverses, and law.md already says "whatever the rounding". `predictions.md` shows the author had read `lorentz.rs`; the dossier credits Paeth/Levesque/lifting but not the engine's own shear memo. Mitchell + 16-entry table and sigma-delta carries are already representation.md §4 (the dossier admits this). What is genuinely new and verified: the rounding *rule* at a repeated shear decides the error type (floor walks — a real refinement of "whatever the rounding" for dynamical sites vs rare handoffs); the fixed-modulus carry constraint; the cost point; the Mitchell budget numbers.

## Fit

Aimed at board focus #2 (changeover reversible and integer — JANUS) and the kick-cost lever. Principle 13 ("errors never compound") and 19 ("a fix signals the wrong representation") are the right frame; the measured content is the rounding rule, not a 10× cost move. Does not delete a component by itself (it argues for retiring the re-expression; A5's robust failure is the evidence).

## The one experiment that would make it gold

Wire it into the design's own cheap path: rewrite the kick chain's quantize site in `crates/universe` (force.rs/kicks.rs/step.rs) as exact accumulate + one nearest/carry shear on the fixed carry grid, retiring the rebinding re-expression, and pass the existing B12 gate on the plane (`behave --law plane`, median exponent ≤ 0.2, bit-identical replays) — the finding measured where it will live, not in a standalone probe. (Same lesson as the premise red-team's silver.)

## What the author missed

- No seed- or window-sensitivity check on the headline number; 0.001 was the 50-orbit median of one fixed seed table, and it does not generalize. "Bounded" should be claimed only as "3–7× slower walk, under B12's 0.2 at these cadences".
- The conjunction-free control that isolates the mechanism was one constant away (GM_P=0) and was not run; it shows nearest ≈ float64 absent chaos, so the rounding-rule gain is partly a chaotic-scene effect, not pure arithmetic.
- The internal prior art (lorentz.rs, law.md line 34) is uncited in the dossier's novelty framing.
- Probe B's two arithmetic slips (i64 wrap on the float arm; +2¹⁰-rounding offset on the exact arm) and the precompute asymmetry in the timed comparison.
- The dossier's quoted timings (106/329, 283–297) do not match its own recorded `.out` files (77/217, 321–329).
