Grade: silver

**Abstract.** Second author on be13 (the checker's named experiment, gold-path). Reproduced digit-for-digit in a clean rerun (6:44, 1.24 GB peak): COM-centred cells beat geometric-centre cells on matched bins at every grid ≥ 128×512 on both scenes (3.0× at 256×1024: 0.00094/0.00303 PASS), converge ~h³, erase the inner-disc p90 failure, and halve the clustered passing grid (128×512 outright). My attacks confirm the core: passes at N = 10⁷ and on a new bulge+disc scene. But D2's "no m-truncation passes / white-noise tail" is refuted at m* = 64 (COM passes p90 on 3 seeds and at N = 10⁷), and "every grid" flips under seed noise at 64×256. Adopt: the corrected sentence (page fixed); no engine code.

**Reasons.**

1. **Reproduction: exact.** My clean rerun of `python3 confirm2.py` and `bugdemo.py` (fresh process, ~7 min, peak RSS 1.24 GB, under the 2 GB cap) matches the shipped `confirm2.out`/`bugdemo.out` digit-for-digit on every measured number; the runner's `regen.log` and the shipped file agree too — three records, same digits, elapsed lines only differ. be13's geom PASS row (0.00279/0.00621) regenerates exactly, and bugdemo regenerates be13's 148599-vs-221937 mismatch from be13's own binning line. C1–C5 are real and active in the code.

2. **Predictions: substantively held, pre-registration unverifiable.** 7/8 held, one honest miss (m ≤ 8), exactly as the dossier reports (every quoted number checked against the output). But `predictions.md`'s only mtime (00:46:52) is 97 s **after** the timed decisive run finished (`confirm2.time`, 00:45:15); `run.log` is empty, so "written before the run" cannot be confirmed — the file mixes predictions and a results section, consistent with an append, and the honest m ≤ 8 miss argues genuineness. Most predictions concerned the first checker's already-known probe numbers (disclosed); the genuinely blind ones (h³ order with the 1.5×10⁻⁴ bound; m ≤ 8) behaved as real predictions.

3. **Adversarial (mine, all on the author's instrument, extensions only):**
   - **A4/B1 — the m-truncation clause is wrong.** Extended the sweep past the author's m ≤ 8: truncation error decays monotonically (COM p90 at 256×1024: m≤8 0.0134, m≤16 0.0117, m≤32 0.0102, m≤64 0.0064–0.0076, m≤96 0.0053). **COM m ≤ 64 passes med AND p90 on 3 seeds and at N = 10⁷; even geom passes at m ≈ 96.** "No m* passes p90" and "the tail is white shot-noise" are false as stated (white noise would decay far slower than measured); the measured decay is signal. The be13 kill of m* ≈ 2–4 stands.
   - **A2/B2 — "every grid" overstates.** 6 fresh seeds: geom wins 1/6 at 64×256 (med ratio 0.96×); at N = 10⁷ geom also wins 64×256 (0.0374 vs 0.0386). The coarsest-grid margin (~1.05×) is within seed noise. COM wins every seed at ≥ 128×512 (1.14–1.39×).
   - **A3 — generalizes to a new scene shape** (35% Gaussian bulge σ = 0.12 + two-arm disc, never tested by be13 or cf6f): mid and inner both PASS under COM; inner p90 COM 0.00061 vs geom 0.00498. Supports the claim.
   - **B2 — outside the tested N (10⁷, next decade toward 10⁹):** 256×1024 PASS under both centring, COM still better (0.00126/0.00324 vs 0.00155/0.00427). Supports.
   - **A5 — page's outside-grid sentence confirmed** (r ∈ [5.5, 11]: med ≤ 2×10⁻⁶).

4. **Novelty.** The live `lab/wiki/handoff.md` already held the inversion and the corrected numbers (folded from be13's checker before this run). This run's own new measured deltas: the ~h³ order with the 512×2048 point, geom's cell-granularity floor at 512×2048, the m ≤ 8 kill (now extended by me), the clusters-128×512 outright pass, controls C1–C5 shipped in the instrument, and bugdemo. Real, but confirmation-with-instrumentation rather than a 10×, delete, or novel premise kill — "a repetition is not gold, however well done."

5. **The page.** The author's fold was faithful to its own evidence except the two overstatements I corrected in place: the "every grid" claim (seed-noise qualifier at 64×256) and the "no m-truncation passes / white tail" clause (replaced with the measured decay and the m ≤ 64 pass). I also folded in the N = 10⁷ and bulge+disc confirmations. Not three-agreeing-gold on this topic; the page stays open.

6. **Goal fit.** P6 "Store the generator, not the generated" — ~2.6×10⁵ numbers flat in N is exactly that, and my N = 10⁷ run supports the direction. P19 "a fix signals the wrong representation" — the inversion came from one binning line, correctly diagnosed. The miss is P22 "the simulation tells us what's next, not us": the white-noise prior, not a measurement, closed the m-sweep at 8. The memory board gains a concrete open lever (below).

**The experiment that would make it gold.** Price the azimuthal half from a coefficient-native store: evaluate ring-harmonic forces directly from per-ring Fourier coefficients (no irfft back to the 1024-point grid), and find the smallest m* passing med AND p90 across ≥ 5 seeds, both scenes, and N = 10⁷. My probes show m* ≈ 64–96 passes as-implemented — if the native read holds, the program drops from ~2.6×10⁵ numbers (2.1 MB) to ~3–5×10⁴ (~5–8× on the galaxy program's bytes, a memory-bottleneck deletion); if it cannot be read cheaply, the full-azimuth grid is a proven floor and the sentence closes. Either outcome is adoptable in one step.

**What the author missed.**
- The m-sweep stopped at 8 and then asserted "any m*" and "white noise" — two more decades of m* were one loop iteration away and refute both.
- No error bars on the seed-dependent claims at the coarse grids; a 1.05× margin from one seed was shipped as "every grid".
- Pre-registration discipline: the predictions file's only mtime is post-run; save the pre-run copy or its hash next time.
- C3's assert checks only the ring's outer edge while the docstring claims the COM "cannot leave its own ring"; the inner edge is unchecked (practically safe at 2π/1024 azimuth span, but the control is weaker than stated).
- Stopped at one N decade and 2-D (disclosed honestly; thickness remains the named untested dial).
