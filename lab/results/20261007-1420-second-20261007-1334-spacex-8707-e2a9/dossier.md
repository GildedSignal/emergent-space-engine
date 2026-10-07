# Dossier — second author on 20261007-1334-spacex-8707: the B18b sampler experiment done, and the claim holds with corrected labels

## Claim

Run 20261007-1334's claim, restated after the named experiment: **on the plane's own frozen
B18b belt sampler** (banded Darwin p, Rayleigh e sigma 0.07 capped 0.6 — tails kept — uniform
angles), at the same N = 30000, 1000 yr, dt = 0.1, seeds {7,8,9} and the same Giant, the
secular live-distinction rate after one program refit is ~1e-3 scars/body/yr long-run at
q = 1e-3 at **both** plausible star-doll placements of the band (quiet [1.33, 1.66] AU and
resonance-loaded [2.65, 3.31] AU) — the loaded placement is within 1.22x of the original
scene's rate at every decisive quantum, far inside the checker's 5x pure-2:1 bound — so
planetary secular dynamics cannot force the 8 GB ceiling at session scale on the plane's
own sampler: a program refit every 5–20 sim-yr keeps the scar store <= 25% ~ 4 GB at 1e9,
and the session-scale memory question stays with encounters and the player. With the
checker's three labeling slips fixed: per-body median first-cross is 10 yr (q=1e-3) / 50 yr
(q=3e-3), not 6.2/21.7; 4 GB fills in ~6.8 game-yr at the early peak rate (3.7e-2/body/yr)
and ~250 game-yr at the long-run rate (1e-3/body/yr) — the honest un-refit margin is T*
itself; the outer-edge |dv| multiple is 24x, not 19x.

## Bottleneck

The same one the silver run answered (board: "distinctions created per game-second at 1e9,
decided by B18's belt wiring"), minus the silver's one gap: the scene was the author's
invented uniform belt, not the plane's frozen sampler. This run closes it; nothing new is
proposed for the engine, and B18's "reported at 1e9" line and the refit cadence now have a
sampler-independent basis.

## Evidence

All commands from this folder; each belt run ~290 s wall for all six in parallel (shared
8-vCPU runner, load ~4 during runs, memory ~0.5 GB/process).

- **The port regenerates the shipped record bit-identically.** `hlive2.py` is the original
  `hlive.py` (fetched from `origin/claude/lab-20261007-1334-spacex-8707`) plus a `--sampler`
  switch, scene-parameterized analysis constants, one new output key (`frac_crossed_vs_t`),
  and per-scene Kepler-solver iteration counts. Proof:
  `python3 hlive2.py --scene belt --sampler orig --N 4000 --years 300 --dt 0.1 --seed 7
  --out port_conv_dt10.json` (8 s) matches the stored `conv_dt10.json` on **every original
  key, bit for bit** (deep compare; only NaN != NaN entries differ, identical NaNs in
  both). The original scene pins 4 Newton iterations; the B18b scenes use 7 because the
  tail reaches e = 0.6 (extra iterations are not bit-level no-ops once converged — found by
  the first verification attempt failing on last ulps, fixed by pinning per scene).
- **Null control on the B18b sampler** (`--scene null --sampler b17 --N 30000 --years 1000`,
  194 s): max |da|/a = 4.1e-12, max |de| = 1.6e-13. The e-tail does not break the
  generators.
- **The frozen sampler.** `xtask/src/behave/belt.rs:SPEC`: Darwin p uniform over
  [2048, 2560) at 2^16, e Rayleigh sigma 0.07 capped at 0.6 (644245094/2^30), omega and t_p
  uniform — "banded p, tails kept". In the harness: p uniform over the band, a = p/(1-e^2).
  Placement: the plane's root unit is GM_star/c^2 (STAR_RADIUS 471,000 = R_sun/(GM_sun/c^2);
  Home's periapsis 99.3e6 root at e 0.02 fixes 1 AU = 1.0129e8 root), so the band is
  [2048, 2560) x 2^k root: **b16 = [1.3252, 1.6564) AU (quiet, no Jovian MMR inside), b17 =
  [2.6503, 3.3129) AU (5:2, 7:3 and 2:1 inside)**. The wiring is not frozen anywhere in the
  repo (Sol's queued build, HANDOFF after 9 October), and these two are the only power-of-two
  scales that put the band between the planets — they bracket wherever it lands.
- **Decisive runs** (290 s wall, six concurrent):
  `python3 hlive2.py --scene belt --sampler {b16,b17} --N 30000 --years 1000 --dt 0.1
  --seed {7,8,9} --keep-sub 6000 --out b1{6,7}_s{7,8,9}.json`, then
  `python3 aggregate2.py` -> `aggregate2.json`:
  - **b17 (loaded):** reabsorbed-e-residual RMS grows as t^0.637 (median seed); out-of-sample
    crossings at q = 1e-3 reach 99.9% by 50 yr (long-run rate 1.0e-3/body/yr — saturated);
    at q = 3e-3, 99.4% cross by 1000 yr (rate 9.94e-4 vs the original scene's
    8.15e-4: **1.22x**). T* (frac = 25% at q = 1e-3) = 5 yr (5, 5, 10 by seed); early
    peak rate 5.0e-2/body/yr over the first 20 yr; session lag 0.23% crossed at 2 yr.
    |dv| fingerprint: the 2:1-edge bin (3.30–3.35) is 16.6x the band-centre bin — the same
    sculpting tail the silver run found, now inside the plane's own band.
  - **b16 (quiet):** the residual *saturates* (growth exponent 0.013 over 50–1000 yr; RMS
    plateaus at 1.4–1.7e-3); everyone crosses q = 1e-3 by 20 yr (T* = 20 yr) and **nobody
    crosses q = 3e-3 in 1000 yr** — the quiet placement is strictly cheaper than the
    silver run's scene.
  - **Fit-noise control:** in-sample/out-of-sample rate ratio 1.000 at both placements.
  - **Memory verdict at 1e9 (16 B/scars), honest labels:** peak 25.3 B/game-s (2.5 KB/real-s
    at rtf 100) -> 4 GB in 5.0 game-yr unattended; long-run 0.507 B/game-s -> 250 game-yr;
    refit every T* = 5 (b17) / 20 (b16) game-yr keeps the store <= 25% ~ 4 GB. The refit's
    own cost at that point is one streaming pass over ~2.5e8 scars (~4 GB read) every
    ~1.6e6 real-s at rtf 100 — ~3 KB/s, noise (the checker's missed line, now stated).
- **Relabels, read straight off the shipped record** (`orig/`, no rerun): per-body median
  first-cross 10/10/20 yr at q = 1e-3 and 50/50/50 yr at q = 3e-3 (the 6.2/21.7 in the
  silver dossier were the aggregate's RMS-reaches-q times); fill arithmetic as above
  (6.8/250 game-yr, not "200 game-years" at the peak rate); |dv| max/min bin multiple 24.3x
  (seed 7). **q-insensitivity, the checker's missed point, is on the record:** without any
  refit the raw crossed fractions at 1000 yr are 1.0 at q = 1e-5 and 1e-4, 0.999 at 1e-3 —
  no quantum choice rescues the un-refit store; only the refit does.

## Predictions

`predictions.md` (written 14:32, before the decisive runs; smoke was N <= 6000, <= 200 yr;
decisive outputs 14:38–14:39). **6 of 7 held:** null 4.1e-12 (predicted <= 1e-11) OK; b16
rate <= 2e-3 OK (1e-3); b17 rate in [1, 5]x original OK (1.22x at q = 3e-3, equal at 1e-3);
T* in [5, 60] (b16) and [3, 40] (b17) OK (20 and 5 yr); b17 exponent 0.637 in [0.4, 0.8] OK;
b17 edge dominance >= 15x OK (16.6x); fit-noise <= 30% OK (1.000). **One failed, in the safe
direction:** b16's growth exponent is 0.013, below my [0.4, 0.8] band — the quiet belt's
residual saturates instead of growing (my exponent band was tuned on resonance-dominated
smokes; the saturated case is cheaper for memory, not dearer).

## What would make it wrong, cost, fit

Wrong if: the plane's belt is wired at a scale other than 2^16/2^17 root units per darwin
(k = 15 puts the band at Home's orbit, k = 18 beyond the Giant — both unphysical for a
belt, but the wiring is Sol's to freeze); a second giant or the belt's self-gravity raises
the floor; or the plane's kick cadence differs enough from this midpoint-slab map that the
residual field decorrelates. What this run does *not* cover: the `shipmem`/`behave --law
plane` path itself has no belt to run (the law's `belt_birth` returns the in-judge reference
belt; the plane scene wires no belt) — the cheapest decisive part of the named experiment is
what was run: the frozen sampler's distribution through the same kick-map architecture and
measurement. Adoption cost: none beyond the silver run's (one number for B18's
reported-at-1e9 line, one cadence); the placement question goes to Sol's belt wiring, where
2^17 is the recommendation (all three planets fit the law's darwin-8192 cap with 2x margin,
and the band then brackets the Kirkwood structure the engine must eventually respect).
PRINCIPLES #6, "Store the generator, not the generated": measured on the plane's own
sampler, the secular generator (two smooth fields F(a), g(a) plus a clock, refit every
5–20 sim-yr) still suffices between refits — at the quiet placement even the q = 3e-3 store
never grows. #21, "rough first, refine when a certificate could break": the refit is the
refinement, and T* is when it must fire.

## The lens

The second-author lens took the checker's words literally and ran the missing experiment at
both defensible placements instead of one; what it may have missed: (a) it inherits the
silver harness's one-planet, 2-D, secular-refit assumptions and the checker-verified +1.2%
causality control rather than re-deriving them; (b) the g(a) fit still zero-weights
|free0| <= 1e-4 bodies (conservative, unstated in the silver, stated now); (c) the
secular-encounter conversion the checker flagged (a stronger perturber turns churn into
ejections) remains unmeasured on the B18b sampler — at sigma_e = 0.07 with the cap at 0.6
the frozen sampler ships *more* deep-e bodies than the silver's scene, so that boundary,
not the secular side, is where the 8 GB question should be re-asked next.
