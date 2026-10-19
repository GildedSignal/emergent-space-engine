# Dossier — 20261019-0141-second-20261018-2312-dynamics-84b2-ded5 (second author on 84b2)

**Claim.** The checker's named gold experiment is flown and decides for the original
claim: at n = 12800 the genesis ringdown **is extinct within the horizon ∝ side**
(block F64 404-421 → ≤ 6 from blocks 5-7 on, t = 10240-14336 post-burn; tail flat at
0.9-3.6 = the anti-bunched baseline), the late steady state is the **same object at
every scale flown** (late-window F64 1.1-2.6 at n = 12800 vs 1.6-2.8 at n = 400-3200),
the 1.4 → 2.4 → 3.4% whole-run m trend was a **fixed-window artifact** (3.37-3.54 →
2.79-2.94 → 2.00-2.10% at H 8192 → 12288 → 24576 on one series), and with the record
cells fixed to the regenerated numbers the bounded-modulation deletion — no
batch-shaping or dephasing machinery for thermal dense scenes — **holds across the
octave**.

**Bottleneck.** Board #4 (smoothness/allocator), the exact gap the silver run left:
the checker measured whole-run m = 3.43% at n = 12800 against the dossier's "bounded
at 1.3-2.4%" letter and left the deletion unextended past n = 6400. This run flies
the octave at horizon ∝ side and prices the steady state with a scale-free
instrument. What it deletes stands: any N-dependent allocator margin for thermal
dense scenes, now at n ≤ 12800 (32× in n). Zero code, one measurement rule.

**Evidence.** Shipped `Chronon` + `Law::RelativisticV1`, Q = 2²⁰, `worlds::gas`
genesis (harness `crates/lattice/examples/breathe.rs` via `work/patch.diff`, base
52db369f; crates byte-identical to 84b2's base 8d9e7f88), fill 0.7, vmax 2¹⁶, burn
1024. **Integrity:** my regenerated n = 400/1600/6400 (seeds 1-3) and poly_r arms
are `diff`-clean against 84b2's committed data, and my 12800 seed-1 series is
**bit-identical to the checker's own committed arm through all 9216 ticks** they
flew (m at H 8192 = 3.43% = their cell exactly); block 4 was re-computed by hand
from raw rows and matches. Everything regenerates: `regen.sh` (~10-13 min wall,
9 arms in parallel + summary). Single quick command:
`breathe 400 0.7 65536 1 1024 8192 0` ≈ 6 s.

**1. Extinction at n = 12800 (the gold-deciding experiment; seeds 1-3, horizon
24576 = 102 side-units, 2.1× the 6400-relative horizon at which 6400 reached
baseline).** Blocks are 2048-chronon post-burn windows:

| seed | blocks F64 | all-≤6 from block | m@8192 | m@12288 | m@24576 | m_late4k | F64_late | mean64 |
|---|---|---|---|---|---|---|---|---|
| 1 | [407.5, 87.5, 56.9, 26.0, 18.5, 8.7, 6.6, 1.5, 1.8, 1.7, 1.3, 3.6] | 7 (t 14336) | 3.43% | 2.85% | 2.04% | 0.43% | 2.64 | 139659 |
| 2 | [404.4, 104.4, 48.6, 20.6, 11.2, 3.9, 1.9, 1.5, 2.1, 1.2, 1.4, 0.9] | 5 (t 10240) | 3.37% | 2.79% | 2.00% | 0.28% | 1.12 | 139170 |
| 3 | [421.0, 109.4, 59.5, 26.6, 17.7, 4.5, 1.6, 2.8, 1.9, 2.7, 1.8, 1.2] | 5 (t 10240) | 3.54% | 2.94% | 2.10% | 0.33% | 1.51 | 139914 |

The ringdown dies, monotonically, on every seed; no plateau, no return (blocks 7-11
flat at 0.9-3.6; F64_whole(H) = mean64·m² holds at every truncation, e.g.
58.13 = 139659·0.0204²). Extinction onset 10240-14336 post-burn vs 6400's 4096-6144
(ratio 1.7-2.5 across seed pairings against side ratio 1.41 — onset grows slightly
faster than side, and the flown horizon still covers it 1.7× past the latest
crossing). Allocator ratios at 12800: whole-run per-chronon p99/p50 1.093-1.099,
late-8192 1.044-1.045; per-64-window max/p50 1.013/1.009/1.009 late — **flatter
after the ringdown than with it included**: there is no smoothness cliff at the
octave, in either direction.

**2. The whole-run m trend was a fixed-window artifact (P4).** Same series, growing
window: m = 3.43 → 2.85 → 2.04% (seed 1; 3.37-3.54 → 2.79-2.94 → 2.00-2.10% across
seeds). The checker's 3.43% is reproduced exactly and is the H = 8192 reading of a
ringdown whose lifetime grows with the box. The sharper lesson (P4's "≤ 1.6%"
expectation missed at 2.0-2.1%): whole-run m **never** converges to the steady
state at fixed genesis — block 0's F64 ≈ 405 dominates the variance at any horizon
(1/12 of windows, ~30× the baseline F). Only windowed statistics converge; the
kill line (m(24576) ≥ 2.4% fails the deletion) did not fire.

**3. The scale-free instrument (the measurement rule, corrected).** Raw late-m
carries a 1/√mean64 counting floor — it fell 2.4 → 0.75% from n = 400 → 3200 while
F64_late stayed flat — so the checker's "late-window m" is n-invariant only across
small steps. The scale-free statistic is **late-window F64** (= mean64_late·m_late²,
window ≥ one lifetime past genesis):

| n | mean64_late | m_late4k | F64_late | source |
|---|---|---|---|---|
| 400 | 4079 | 2.38% | 2.31 | this run s1 (bit-identical); 84b2 s2-3: 1.61-1.81 |
| 1600 | 17530 | 1.18% | 2.44 | this run s1 (bit-identical); 84b2 s2-3: 1.74-2.81 |
| 3200 | ~35457 | 0.74-0.77% | 1.95-2.09 | 84b2 data (3 seeds) |
| 6400 | 68359-68801 | 0.65-0.87% | 2.86-5.15 | this run (3 seeds) — window still holds ringdown |
| 12800 | 139293-139808 | 0.28-0.43% | 1.12-2.64 | this run (3 seeds) — window 5 lifetimes past extinction |

The 6400 row is the tell: its H = 8192 "steady state" (F64_late 2.9-5.2) still
smuggles ringdown (blocks 2-3 of 4); flown to extinction, 12800 returns to the same
1.1-2.6 band the small boxes show. The steady state of the thermal dense order is
**scale-free in n** — the silver letter's 2.4% and the checker's 0.62% both
understate how flat it is.

**4. Record cells fixed (silver dossier's stale numbers → regenerated; every arm
bit-identical to 84b2's committed data):**
- 6400 ladder row: F64 **38.18-43.77** (3 seeds; was "38.18-39.05" = 2-seed), m
  **2.42%** (2.35/2.39/2.52; was "2.37%"), F1 1.34-1.46, mean64 68617-69032,
  b0 max/p50 1.115-1.117, blocks(s1) [117.2, 19.5, 7.3, 2.7].
- poly_r cell: **F64 17.26, m 2.26%, mean64 33798** (was "34.6, 3.19%, 33934",
  read from a partial file); block0 39.1, share 0.23 were already right. New: its
  late-4096 tail reads m 1.45%, F64_late 7.06 — radius spread leaves a slightly
  rougher (but still tiny) steady state than monodisperse.
- T range: **4.8-7.9·side measured** on resolved arms (censored arms read ≥ 6-8.5;
  was "5.7-9·side").
- `regen.sh` now **contains** the 12800 arm the silver dossier claimed and lacked.

**Predictions** (`predictions.md`, written before the decisive runs):
- **P1 (extinction, decisive): held.** late-m 0.28-0.43% ≤ 1.0%; no seed near a
  plateau (last-3 blocks 1.2-2.7); F64_late 1.1-2.6 in the pre-registered baseline
  band.
- **P2 (onset band 7000-13500): held on seeds 2-3 (10240); seed 1 crossed at
  14336, half a block past the band's top** — disclosed; the kill line (blocks 1-8
  all > 6) did not fire. Onset grows a little faster than ∝ side (1.7-2.5× vs
  1.41×) — the horizon rule needs ~2× the 6400-relative horizon, which is what was
  flown.
- **P3 (calibration): held** (6400 late-m 0.65-0.87%).
- **P4: direction held, number missed.** m fell monotonically with window
  (3.43 → 2.85 → 2.04%) but stopped at 2.0-2.1%, above the ≤ 1.6% expectation;
  the kill line (≥ 2.4% fails) did not fire. The miss is the lesson (§2): whole-run
  m is not a steady-state instrument at any finite horizon.
- **P5: held** (late p99/p50 1.044-1.045 ≤ 1.19; late max/p50 1.009-1.013 ≤ 1.12).

**What would make it wrong.** The deletion claim is measured on one genesis family
(monodisperse touching lattice, fill 0.7, β ≤ 0.09, thermal) across n = 400-12800;
a genesis that sustains a driven oscillation (checker2's coherent-fleet wall-ram,
Fano₁ 10-129) sits outside it. The 25600 octave (the checker's optional second
step, ~40 min/arm here) is extrapolated by the instrument, not flown — predicted:
extinction by t ≈ 18-30k post-burn, F64_late 1-3. If a checker flies it and
F64_late leaves that band, the scale-free steady state dies with this dossier.
Also: onset-vs-side grew 1.7-2.5× over one octave — three octaves out the safe
horizon rule may need re-measuring, though it stays O(side).

**Record-hygiene note.** Mid-run polling of the streaming arms produced outputs
that do not match the completed files' immutable prefix; the record here uses only
completed-file analysis, verified three ways (bit-identity with the checker's
committed arm through tick 9216, hand-recomputed block 4, identity F64 = mean64·m²
at every truncation). `regen.sh` regenerates everything from a clean tree.

**Cost of adoption.** Zero code. One scale-free measurement rule: judge steady-state
rate modulation by late-window F64 from a window ≥ ~2× the ringdown onset, never by
raw Fano or whole-run m. One deleted fear, octave flown: no N-dependent
batch-shaping margin for thermal dense scenes at any n measured (400-12800).

**Fit with PRINCIPLES.** "The cheapest compute is compute not done": the ringdown
extinguishes itself and the steady state is flat — paying steady-state machinery
against it is work for no reason. "A test that cannot fail is a control": P1/P4
carried kill lines stated before the runs; P4's expectation missed and is reported
as the instrument lesson rather than buried. "Fat tails: judge behaviours over
many seeds and look at the worst cases": three seeds, worst (latest-crossing) seed
quoted first. "Rough first": the octave flight is the refinement the checker
priced; nothing here polishes a scene family the ladder may replace.

**The lens (second author).** What this run may have missed: extinction is claimed
for the box's acoustic ringdown only — the checker's other half (sustained
coherent-fleet bunching) remains unpriced, and F64_late is now the right tool for
it. The super-linear onset hint (1.7-2.5× vs 1.41× side) is one octave of three
seeds — if real, the genesis batch cost at 10⁹ scales worse than √n, and the
allocator cares about the startup transient more than the steady state this run
certified flat.
