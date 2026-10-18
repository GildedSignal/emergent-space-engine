# Predictions (written before the corrected-instrument run)

Context: be13 (silver) shipped "COM centring is worse at every grid"; the checker
found a third instrument bug (com_program radial extent `hi = gal.R_MAX` instead of
`np.log(gal.R_MAX)` — a 1.6× coarser log grid filling ~62% of rings, visible as
cells_used 148599 vs 221937) and claims the inversion: COM is better at every grid
on matched bins. The checker's probes (not on a shipped record): clustered scene
passes at 256×1024; 3 fresh seeds pass; m ≤ 4 at 256×1024 fails p90; inner annulus
p90 over the bar. My instrument is an independent re-implementation of the fix with
controls C1–C5. Cases I have not tuned on, and what I expect there:

1. **The inversion reproduces on matched bins (decisive).** COM med < geom med at
   EVERY grid on BOTH scenes, and at 256×1024 smooth COM passes med AND p90
   (~0.0009/0.0030 vs geom 0.0028/0.0062). If instead geom still wins on truly
   matched bins, the checker's correction is itself wrong and this dossier refutes
   it — that outcome would be reported, not buried.
2. **C2 fires on the old bug.** With the cell-count control, be13's shipped COM
   numbers cannot regenerate: the assert `g_used == c_used` fails on the unpatched
   extent. (I will not re-run the bugged grid; the control's mechanism is that any
   binning mismatch is now structural, not silent.)
3. **COM convergence order (never measured, genuinely held out).** Checker's
   corrected meds 0.0372 → 0.0087 → 0.00094 give ratios 4.3×, 9.3× per halving —
   superquadratic, consistent with ~h³ (dipole removed; quadrupole remainder).
   I predict the 512×2048 point continues ≥ 6× per halving (med ≤ ~1.5×10⁻⁴),
   while geom stays ~h² (ratio ~4×, med ~6–7×10⁻⁴).
4. **Clustered fine grid.** 128×512 med passes but p90 sits at/over the bar
   (~0.010, marginal); 256×1024 passes med AND p90 with MORE headroom than smooth
   (~0.0014/0.0031). The near-ring (Barnes–Hut) fallback stays unnecessary for
   field fidelity at N = 10⁶.
5. **Fresh seeds.** Both fresh seeds pass at 256×1024 (geom and COM), med within
   ±25% of the shipped 0.0028 — the pass is not a seed artifact.
6. **m-truncation at the passing grid.** m ≤ 4: med near the bar (~0.008, ≤ 10%
   either side) but p90 ≈ 2× the bar → NOT a pass; m ≤ 8 passes med and p90.
   COM centring does not rescue m ≤ 4's p90 (truncation error and centring error
   are different channels). be13's "m* ≈ 2–4" clause stays dead; the priced
   program is the full-azimuth grid.
7. **Annuli.** Inner 0.02–0.2: med passes (~6×10⁻⁴) but p90 goes OVER the bar
   (~0.013); outer 4.8–5.0 marginal (p90 ~0.008). The shipped test window was the
   easy middle; the pass clause is p90-bounded to R ≳ 0.2.
8. **Softening coupling survives the fix.** At 256×1024, ε 0.05 → 0.02 → 0.01
   raises the error monotonically ~10× per halving of ε (geom ~0.003 → ~0.018 →
   ~0.05; COM ~0.001 → ~0.009 → ~0.029): a finer aggregate quantum demands finer
   cells; with the corrected instrument the constants land on the checker's, not
   be13's (0.0041/0.027/0.054).

Kill criterion for the corrected claim (pre-registered): if COM does NOT beat geom
on matched bins at every grid, or if the clustered scene fails p90 at 256×1024,
then the corrected adoptable sentence ("COM-centred monopole cells on a log-polar
grid") does not hold as stated, and the dossier reports which half broke.

## What happened (confirm2.out, 6:44 wall, 1.23 GB peak RSS; every control held)
1. **HELD (decisive).** COM beats geom at EVERY grid on BOTH scenes: smooth med
   0.03720/0.00871/0.00094/0.00012 vs geom 0.03888/0.01147/0.00279/0.00138
   (64×256→512×2048); clusters 0.00949/0.00178/0.00020 vs 0.01144/0.00412/0.00135.
   256×1024 smooth COM 0.00094/0.00303 — PASS med AND p90, the checker's numbers.
   My geom row regenerates be13's shipped PASS (0.00279/0.00621) exactly.
2. **HELD mechanically.** bugdemo.out reproduces the shipped counts (148599 bugged
   vs 221937 fixed/geom at 256×1024) from be13's own binning line; in the corrected
   run C2 never fired silently-different — counts identical at every grid.
3. **HELD.** COM per-halving ratios 4.27×, 9.27×, 7.79× — superquadratic (~h³),
   512×2048 med 1.2×10⁻⁴ ≤ my 1.5×10⁻⁴ bound. One sub-miss: geom's finest point
   came in at 0.00138 (2.0× ratio), not my 6–7×10⁻⁴ — at 550790 nonzero cells for
   10⁶ bodies (~1.8 bodies/cell) geom's quadrature floors on cell granularity (the
   lumps channel), while COM keeps improving: with ~2 bodies per cell the COM is
   nearly the bodies themselves. Mechanism identified, direction as predicted.
4. **HELD.** Clusters 128×512 geom 0.00412/0.01008 (p90 marginal over bar,
   checker's 0.0101); 256×1024 geom 0.00135/0.00314 PASS (checker-identical).
   NEW: COM passes clusters at 128×512 OUTRIGHT (0.00178/0.00679) — the clustered
   scene's passing grid halves under COM.
5. **HELD.** Seeds 118/219: geom 0.00280/0.00699 and 0.00264/0.00683 (PASS, med
   within ±25% of 0.0028); COM 0.00090/0.00324, 0.00096/0.00305 (PASS).
6. **HALF.** m≤4: med 0.00763 (4.6% headroom), p90 0.01475 ≈ 1.8× bar; COM does
   not rescue it (0.00742/0.01396) — as predicted. WRONG on m≤8: 0.00722/0.01441,
   p90 still 1.8× the bar (I said it would pass). The azimuthal tail above any m*
   is white-noise-like (m≤4 vs m≤8 barely differ), so no cheap m-truncation passes
   p90; the priced program keeps the full azimuth. m* ≈ 2–4 stays dead.
7. **HELD for geom, SUPERSEDED for COM.** Inner annulus geom 0.00063/0.00807 (p90
   over bar, as predicted), outer 0.00381/0.00818 (marginal). But COM: inner
   0.00011/0.00100 PASS, outer 0.00070/0.00354 PASS — the annulus caveat was
   geometric centring's artifact (near the disc centre, intra-cell mass
   displacement is a large relative error): the corrected program passes med AND
   p90 over the whole sampled disc [0.02, 5.0].
8. **HELD.** geom 0.01793/0.04914, COM 0.00902/0.02852 at ε 0.02/0.01 — the
   checker's constants land exactly; monotone, ~3–6× per ε halving at fixed grid.

Kill criterion: did NOT fire. The corrected claim holds on the shipped record.

