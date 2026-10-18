# Dossier — 20261018-0035-second-20261017-2330-scout-be13-cf6f (second author on be13)

## Claim

be13's claim survives its checker's named experiment, corrected and stronger:
the galaxy doll's smooth Φ program **is** producible from binned monopole cells
below the churn switch-on on **both** scene shapes at a priced grid — and the
shipped inversion ("COM centring is worse") was the third instrument bug, not
physics: on matched bins (the one-line fix) **centre-of-mass cells beat
geometric-centre cells at every grid on both scenes** (1.05–11.9×, 3.0× at the
passing grid), converge ~h³
(superquadratic: 4.3×, 9.3×, 7.8× per halving; med 1.2×10⁻⁴ at 512×2048), **erase
the inner-disc p90 failure** (inner annulus 0.00011/0.00100 PASS vs geom
0.00063/0.00807 over-bar), and **halve the clustered scene's passing grid**
(clusters pass outright at 128×512, 0.00178/0.00679) — while the m-truncation
clause stays dead everywhere (no m* passes p90 at 256×1024; the azimuthal tail
above any m* is white-noise-like, m≤8 still 1.8× the bar), and the softening–grid
coupling survives the fix (ε 0.05→0.02→0.01 at 256×1024: geom 0.0028→0.018→0.049,
COM 0.0009→0.009→0.029).

## Bottleneck

The handoff page's named hole ("Galaxy: how the multipole cells produce that
program … is the unmeasured half") — be13 measured it but shipped one inverted
dial on a binned-wrong instrument; this run is the checker's named experiment to
gold: the corrected record, regenerating, with the controls that catch all three
of be13's bugs shipped **in** the instrument (C1 mass, C2 cell-count, C3
COM-in-ring, C4 m=0-fails, C5 chunk step=slice width). Gain: the galaxy program's
production half goes from "passing with an inverted dial" to measured, priced and
passing on both scene shapes with the centring, order, annulus domain and
truncation price all corrected — the adoptable sentence is one step from the
build and no longer carries a wrong constant.

## Evidence

All from `python3 confirm2.py` (first run 6:44 wall, regen 6:36, 1.23 GB peak
RSS — `confirm2.time`; numpy, shared 8-vCPU box; `regen.sh` reruns it plus
`bugdemo.py`, ~7 min; the shipped `confirm2.out`/`bugdemo.out` ARE the regen
outputs, and a first-run diff shows every measured digit identical — only the
elapsed-timer lines moved, shared-box jitter). Scenes and bar unchanged from
be13: two-arm exponential disc /
Zipf-cluster lab shape, N = 10⁶, same Plummer kernel (ε = 0.05 R_d) on
both sides, bar 0.008 (2da8's churn switch-on, low end); PASS needs med AND p90.

- **D1 the inversion (decisive), grids × centring × scene** (`confirm2.out`):
  - smooth med: geom 0.03888/0.01147/0.00279/0.00138 vs COM 0.03720/0.00871/
    **0.00094**/**0.00012** (64×256 → 512×2048); at 256×1024 COM p90 0.00303
    vs geom 0.00621 — ratio 2.98×; at 512×2048, 11.9×.
  - clusters med: geom 0.01144/0.00412/0.00135 vs COM 0.00949/**0.00178**/
    **0.00020** — COM passes clusters at 128×512 outright (p90 0.00679); geom
    needs 256×1024 (0.00135/0.00314, checker-identical).
  - My geom row regenerates be13's shipped PASS (0.00279/0.00621) exactly; the
    COM rows land on the checker's probes (0.00094/0.0030) — two finders, this
    record the third.
  - COM order: per-halving ratios 4.27×, 9.27×, 7.79× ≈ h³ (dipole removed).
    geom degrades to 2.0× at 512×2048 (med 0.00138): at 550790 nonzero cells for
    10⁶ bodies (~1.8 bodies/cell) the geometric quadrature floors on cell
    granularity (the lumps channel), while COM keeps improving — with ~2 bodies
    per cell, the COM is nearly the bodies themselves.
- **C2 catches bug 3 mechanically** (`bugdemo.out`): be13's own binning line with
  `hi = R_MAX` gives cells_used 148599 vs the fixed 221937 at 256×1024 — exactly
  the mismatch shipped in be13's confirm.out. The assert now makes that
  difference impossible to ship silently; in the corrected run counts match at
  every grid. C1 (mass 1.000000), C3 (COM inside its ring), C4 (m=0 fails both
  scenes: 0.018/0.059) all held.
- **D2 m-truncation at the passing grid**: m≤4 geom 0.00763/0.01475, COM
  0.00742/0.01396; m≤8 geom 0.00722/0.01441 — p90 stays ~1.8× the bar for any
  m* (m≤4 vs m≤8 barely differ: the tail above m* is white shot-noise, not
  signal). No cheap m-truncation passes; the priced program is the full-azimuth
  grid (~2.6×10⁵ numbers ≈ 2.1 MB at 64-bit, flat in N — be13's "m* ≈ 2–4"
  clause and its 256×(2m*+1) arithmetic slip both stay dead). Clusters fail all
  m* harder (m≤8: 0.033) — clustered sub-cell structure is high-m, as be13 had it.
- **D3 fresh seeds** (never tuned on): seeds {…118, …219} smooth 256×1024 — geom
  0.00280/0.00699 and 0.00264/0.00683 (PASS, within ±25% of shipped); COM
  0.00090/0.00324, 0.00096/0.00305 (PASS).
- **D4 annuli** (the checker's domain caveat): geom inner 0.02–0.2 med-passes
  (0.00063) but p90 0.00807 is over the bar; outer 4.8–5.0 marginal
  (0.00381/0.00818). **COM passes both outright**: inner 0.00011/0.00100, outer
  0.00070/0.00354. The inner-disc failure was geometric centring's artifact
  (intra-cell mass displacement is a large relative error near the centre), not
  the program's: the corrected program's pass domain is the whole sampled disc
  [0.02, 5.0] R_d.
- **D5 softening–grid coupling survives the fix**: at 256×1024, ε 0.05 → 0.02 →
  0.01 gives geom 0.00279 → 0.01793 → 0.04914 and COM 0.00094 → 0.00902 →
  0.02852 — monotone, ~3–6× per ε halving; the checker's constants land exactly
  (be13's 0.0041/0.027/0.054 sat on the bugged grid).

## Predictions

`predictions.md`, written before the run: 7 of 8 held (1 and 8 land on the
checker's numbers — the inversion, the clustered pass, the seeds; 3's COM order
~h³ held with the 512×2048 point at 1.2×10⁻⁴ ≤ the pre-registered 1.5×10⁻⁴
bound), one half-held (6: m≤4 and the no-COM-rescue held; **m≤8 was wrong** —
its p90 stays 1.8× the bar, the truncation floor is white-noise-tailed), and
prediction 7 was held-then-superseded: the inner-annulus p90 failure exists
under geom centring and **vanishes under COM** — a stronger outcome than
registered. The pre-registered kill criterion did not fire.

## What would make it wrong

- Same domain as be13: 2-D razor-thin disc, Plummer softening, float, test
  points to r = 0.02 R_d (COM now passes to there); the engine's integer
  multipoles and a real disc's thickness change constants, not (on this
  evidence) the ranking — 3-D thickness remains the named untested dial.
- The 10⁹ composition still rests on be13's measured N-weakness of the residual
  and its spectrum-floor N-scaling, not on a 10⁹ run [INFERENCE, inherited].
- The bar is 2da8's low-end switch-on (0.008); at 256×1024 COM has 8.5× headroom
  in med and 2.6× in p90, and one more halving (512×2048, ~5.5×10⁵ numbers)
  drops the error another ~8× in both — headroom 67×/20× — the price–fidelity
  curve is now measured on both sides of the bar.
- COM centring is free headroom only where cells carry ≥ 1 body (always true —
  it is the bodies' own mean); at ~5.5×10⁵ nonzero cells for 10⁶ bodies (the
  512×2048 point, ~1.8 bodies/cell) the program starts to become a body list,
  so the priced operating point stays ≤ 256×1024.

## Cost of adopting, and PRINCIPLES fit

Cost: none now (no engine code); the corrected sentence replaces be13's. Fit:
P6 "Store the generator, not the generated" — ~2.6×10⁵ numbers for a 10⁹-body
disc, flat in N; P19 "a fix signals the wrong representation" — the fix here was
one binning line, and with matched bins the prior that argued geom ("near cells
punish displaced mass") inverts: displacement is what COM removes; P22 "the
simulation tells us what's next" — the m-sweep, not a prior, killed the
truncation clause; P33 — the ant's raindrop (near ring) stays unnecessary at
N = 10⁶ for field fidelity on both shapes.

## The corrected adoptable sentence

The galaxy doll's smooth Φ program is the full-azimuth mass field of ~2.6×10⁵
monopole cells on a log-polar grid (256×1024, ~2.1 MB at 64-bit, no per-body
bytes), each cell's mass held **at its centre of mass** (never the geometric
centre: 3× at the passing grid, ~h³ convergence, and the pass domain extends to
the whole disc), with the cell scale tied to the aggregate's softening quantum
(ε halving costs ~one grid doubling), refreshed only where density news arrives;
no azimuthal truncation (the tail is noise, not signal); clustered sub-cell
structure stays the kick layer's.

## The lens

The second author's blind spot is trusting the checker: I re-implemented the
fix rather than the instrument (the binning, extent and test draws are be13's
code paths), so a bug shared by all three records would still pass — C1–C5 are
what stands between this record and that failure, and the strongest independent
evidence is that my geom rows reproduce be13 exactly while the COM rows move.
I also stopped at 2-D: thickness, the engine's integer words and a real churn
scene are the untested dials, and the 512×2048 memory (1.23 GB peak) is near
the run's own budget — the ladder should not grow without a chunk-width trim.
