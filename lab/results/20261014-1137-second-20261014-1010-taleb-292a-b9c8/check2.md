Grade: silver

**Abstract.** Second author on taleb-292a, both instrument flaws fixed: 864/864 crossings complete on the odd-eighth grid, byte-identically reproduced; every dossier number confirmed independently. The w-column walk is bounded (≤ 3.68 radii to depth 512) and irreversible; circles are an exact orientation lottery (radius drift 0); fixed points common but w wobbles on 51/76; μ benign across [1,2) (1.0001/1.28/1.6/1.999: zero refusals, drift ≤ unity). Correction: mid-walk refusals are real at even phases (5/648 past step 64, steps 87–175, record 3.98 radii) — "zero refusals" is grid-specific and the "word handling differed" explanation dies. Gain: the anchor-w+t decision gets its error budget; cost: wiring only. Silver pending the per-class refusal budget.

## Reproduction

- Clean tree, `git apply work/patch.diff`, `regen.sh` path: **`seam2.json` reproduced byte-identically** (19 s; stdout matches: 864 chains, 0 refusals, P1 864/864, P2 852/852 nonzero ≥ 2.4×10⁵ ulps, rerun bit-identical, ~20.6 µs/crossing).
- Shipped-API claims verified in source: `Scalar::raw(n,bp)` = n·2^bp (`raw(φ,3)` really was 8φ; `raw(φ,−3)` is a true phase — scaled.rs:22); `Unit::of` takes any positive μ but the doll mass doc puts the mantissa in [1,2) (world.rs:34); `in_tube_units` and the decode's `to_doll` mirror bind.rs:252-258/127-132 faithfully; the doll-based word matches bind.rs:275.
- Every dossier headline recomputed from `seam2.json` with independent code: record 3.677 radii (p 8 M, e 0.5, φ 5/8 — d256 = 3.677 at all three words), circles 144/144 radius drift exactly 0 with position drift 1.71/2.00, per-crossing |Δw| max 0.357 (p 8 M, e 0.99, outbound) median 3.6×10⁻⁷, inbound medians 4.5×10⁻⁸/7.5×10⁻¹² vs outbound 5.7/7.6×10⁻⁴, fixed points 76 (25 w-fixed, 51 wobbling ≤ 3.8×10⁻³ turns), census {1:76, 2:7, 3:5, 4:2, 8:1, 14:1}, 20 late closures, 26/288 word-closure flips, word-invariance 219/244 within 2×, strong walkers d256/d64 median 1.03 max 4.61, quiet ≤ 7.9×10⁻⁹, μ paired 84%/71%, |Δk| median 1 ulp. All match.
- predictions.md predates the decisive run (file times 17 m → patch 10 m → seam2.json 7 m; the depth-64 smoke disclosed inside it). PD1/2/4/5/6/7 held; PD3 refuted and reported as such.

## Adversarial cases (mine)

Variant probe = the author's file with the phase exponent and MUS/PHIS/W0/CW knobs env-parameterized (mechanical; on the default grid it reproduces the author's 864-chain record **field-for-field**, so the variant is validated). Each run < 40 s.

1. **Depth 512, full 864 grid** (next decade of the swept number): 0 refusals anywhere; envelope still 3.677 (same chain); circles unchanged; strong-walker median 1.03. But max d512/d64 = 8.25 ≈ the linear 8×: one chain climbs linearly from ~0.45 to ~3.7 radii — "bounded" is a property of the envelope, not of every trajectory inside it.
2. **Even phases {1/4, 1/2, 3/4}** (axis-aligned, outside the author's odd-eighth grid): **6/648 refusals, 5 mid-walk, 5 past step 64** — `fit:Range` at steps 87, 142, 175 (p 8 M circles/near-circles and e 0.001 at φ 1/2; e 0.001 at 16·2⁸) and `cartesian:Range` at step 161 (16·2⁸ M, e 0.99, φ 3/4, both dolls). Record drift 3.98 radii; every walk class otherwise unchanged (circles radius-exact, |Δw| max 0.357, w wobbles on 31/47 fixed keys, μ benign). **The mid-walk refusal class the first checker saw is real on the corrected instrument; the dossier's explanation ("their probe's word handling differed") is wrong — it is a phase-class effect.**
3. **Retrograde start, w₀ = 1/2 turn**: 10/864 refusals, all at step 0 (entry encode), never mid-walk — including the e 0.99 class at p 16·2¹⁷/16·2¹⁹ that completes prograde. Corroborates the page's 10/864 at w₀ = 0 retrograde.
4. **μ = 1.0001, 1.6, 1.999** (the author tested only ≈ 1.28): 0 refusals in 1728 non-unity chains; drift ≤ unity at every scale (medians 4.3×10⁻⁴ vs 8.4×10⁻⁴ unity). The "μ benign" conclusion covers [1,2).

## Novelty

The corrected full-grid measurement is new to the record and legitimately updates the page's current best: the graded run's "never finds a fixed point", "μ unmeasured, not safe" and the 304-refusal census all die. But the phase structure, the bounded walk and the benign μ doll were first measured by the first checker's extensions (already folded into the live page); this run consolidates them on a corrected instrument at full grid and adds the fixed-point census, the exact circle-radius invariant, word-closure flips, saturation to 256 and the paired μ statistics. Confirmation and completion of a corrected record — not a newly broken premise. docs/HISTORY.md holds no seam/order-boundary entry; the wiki is the record and this run is its newest.

## Goal fit

Moves the `nladder`/`frame-cost` open direction (ephemeral promotion multiplies crossings) by replacing a broken instrument with a measured error budget. PRINCIPLES #13 ("we don't want errors that can compound") — measured as bounded but irreversible information loss, honestly sharpened; #19 (fixes signal the wrong representation) — the w column for circles; #34 — a guard's measurement, not a new law. Respected: shipped pub APIs only, controls both sides (P1 positive, P2 positive with the 12 zero arms disclosed, determinism), record kept machine-readable.

## Why silver, not gold

Reproduced and robust under every attack but one: the headline "864/864 chains complete with zero refusals … the checker's mid-walk `fit:Range` does not reproduce on this grid" is mis-scoped. The corrected grid swept only odd eighths; at even phases the mid-walk refusal class exists (0.8% of chains, steps 87–175). A design that multiplies crossings needs the refusal budget per phase/orientation class, and the record as written says the class does not exist. Two minor record defects: the μ label (0x147AE1/2²⁰ = 1.28 exactly, not "1.2846" — first checker caught it, the dossier keeps it) and the census arithmetic ("294" = 195+99+10 = 304).

## The one experiment to gold

Extend the corrected census to the phase/orientation classes on the same grid: even eighths and (w₀, cw) variants — a one-line PHIS/W0/CW change, < 2 min of runs (my cuts: 6/648 even-phase refusals, 10/864 retrograde entry, record 3.98 radii). Fold the per-class refusal budget into the record, fix the two defects, and the anchor-first wiring decision has its complete budget.

## What the author missed

- The even-phase classes — the axis-aligned points where the fit's angle conditioning degenerates and the mid-walk refusals live; their explanation of the first checker's refusals ("word handling differed") is refuted.
- μ at one scale (disclosed as open): now closed across [1,2) — benign everywhere.
- Depth beyond 256 (disclosed): the envelope holds at 512, but one strong walker climbs linearly (×8.25) to reach it; "saturates" should say the envelope saturates.
- Retrograde/other-w₀ arms: 10/864 refuse at entry (first checker had this; independently corroborated at w₀ = 1/2 turn).
- The census sum (294 vs 304) and the μ label in the dossier text.

Page corrections made in place: the "zero refusals" headline scoped to the odd-eighth grid with the even-phase class in Domain; the Contradictions entry settled; direction 2 updated (μ covered across [1,2); refusal class measured); the 294→304 arithmetic noted.
