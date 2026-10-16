Grade: gold

**Abstract.** Every step of the repaired record regenerates: I applied `work/patch.diff` to a
clean tree at c9657cd1 myself and reproduced steps 1–7 bit for bit (crossings vector, 14/14
judged with B12 false, #57 at 7016 kicks / 24.37109375 / 8.409466703853747e-8, census 14/11/8
and musl 15/16, ulp-stability 5423/5424, freeze control c84f5787 bit-identical, crcheck +0 ulp;
`echo_is_linear` fails solo under load exactly as corrected). The named experiment holds: my own
independent mpmath recompute (dps 80, own code, Rust's exact op order) matches all 16×12 CR-table
fields, glibc 0 ulp from CR on r/v/cos/sin for all 16 ships, CR corpus = the 14/16 red corpus,
j_run(#57) = 8.409e-8 on CR bits. My probe routing only the walk's per-step `sin_cos`/`hypot`
through musl (seeds held glibc) rewrites the corpus (judged 14→11/16, #85 inside at 0.012 Rp):
the walk channel, inferred by the author, is now measured. Cost to adopt: none to the engine;
the integrator's fix menu collapses to freeze-the-fields or CR-walk.

**Reasons.**

1. **Reproduction, my own execution, clean tree.** `git apply` of the delivered patch (no
   workspace member; libm only as xtask dev-dependency), then each step's command run by hand
   with my own log (/tmp/checker2-regen.log): all non-empty, all numbers identical to the
   parent's dossier and this run's claims. The runner's own regen (exit 0, log delivered) is a
   third independent execution. The one deviation I found anywhere: none.
2. **Predictions.** predictions.md (18:43) precedes the decisive artifacts (regen-full.log
   19:03, dossier 19:04). PG1/PG2 held (steps non-empty; bit-identical). PC1 held (the probe's
   k/α bit assertions passed for all 16). PC2 held stronger than predicted (0 ulp everywhere,
   not ≤1–2). PC3 held in its central branch and sharpened: the CR corpus equals the current red
   corpus exactly — the strongest form of "CR seeds ≠ frozen 16/16"; the kill criterion did not
   fire. PC4 held (#57 at 8.409e-8, inside the predicted scatter; no directional call was owed).
3. **The central new claim independently confirmed.** I recomputed the CR table from scratch
   (own script, dps 80, replicating Rust's evaluation order including `to_radians` =
   x·CR(PI_f64/180) and per-op rounding): all 16 ships × 12 fields match `cr_seeds.txt`
   (sha256 e370148d… verified first), and glibc's `cbrt`/`powf`/`cos`/`sin` seed chain sits 0 ulp
   from CR on every component of every ship. "The CR corpus is this box's corpus" is therefore
   exactly true, and "CR seeds alone repair the corpus" is refuted on this box with no
   instrument gap. The logic that seeds alone cannot repair both machines stands a fortiori
   after my walk probe: even bit-identical seeds leave the corpus walk-conditional.
4. **Attacks (three, one outside the author's domain).**
   - *Independent CR recompute* (above): matched; no tie sensitivity at dps 60 vs 80.
   - *Musl-walk probe* (outside: the author varied seeds only, and named the walk as unmeasured):
     `WALK_MUSL=1` swaps only the per-step `sin_cos`/`hypot` on the assess path; control without
     the flag reproduces the pristine census exactly. With the flag: judged 14→11/16, kept[0]
     closest 59.530→45.450 Rp, #57 crossings 14→6 at 7.476 Rp, #85 inside at 0.012 Rp. The
     author's conclusion "the machine channel is the walk" is confirmed by measurement — I
     folded this into the page as a [checker 2] note.
   - *Single-bit flips of #57* (8 cases): x−1 → 3.697e-8 pass (exactly the page's checker
     number), vy+1 → 2.644e-8 pass, the other six fail. The page's disclosure that a non-CR
     seed libm can still flip the "portable red" is accurate and, if anything, understated in
     frequency (2 of 8).
5. **Novelty.** Neither docs/HISTORY.md nor the published replay-gate page holds any CR-seed
   measurement; the parent proposed the CR fix, and this run prices out its seed leg. The
   load-class correction of the parent (echo_is_linear fails even solo under this window's load)
   also reproduced.
6. **Page.** Faithful: every number on the proposed page checks against evidence I regenerated;
   the portability claim carries both disclosed caveats (machines that build the CR seed bits;
   the scene's `powf` in `period()`/`omega()`). I corrected nothing that overstated and added
   the [checker 2] measurement note. Not three golds on this topic's best — the page stays open.
7. **Goal fit.** PRINCIPLES: "Canonical outcomes are exact and independent of cache, partition,
   observation, schedule and hardware. Floats never decide them." With this run (and my probe),
   the last ambiguity in *where* the floats decide the B12 corpus is gone: seeds measured
   innocent on glibc, walk measured guilty, and the failing observable made deterministic on CR
   bits. It shows a premise wrong (CR-seeds repair) and closes the parent's record hole; the
   integrator's one-step adoption is the fix choice itself.

**What the author missed.** The walk channel was inferred, not measured (now measured here, in
the author's favour); the M1/macOS leg remains unmeasurable from this box (disclosed); the full
202/9/21 suite count was not re-run by me (out of window; the deterministic core and the solo
load behaviour were verified); the new page paragraph sits below the "standing record unchanged"
marker, a small ordering quirk, not an overstatement.
