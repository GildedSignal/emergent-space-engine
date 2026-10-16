Working...
Check complete. `check.md` written to the run folder with `Grade: silver`, and the author's wiki page extended in place with the checker's held-out rows.

**What I did and found:**

**Reproduction — exact.** `regen.sh` in a clean temp tree (11 s): every number in the dossier, `run_console.txt`, and `report.json` matches line for line. `work/patch.diff` is empty (script-only run). The oracle ports are faithful in form to the shipped `gr_oracle.rs`/`gr_oracle_extended.rs`, and the frozen arm reproduces fe85's published calibration (1.83e-4 median, 255/256 at m=16).

**Held-out attacks (author's unmodified module, ~32 s):**
- **Fresh 1024-seed draw, different RNG (outside tested range):** the GEO win is draw-independent — m=16 gives 1024/1024 on precession *and* period (frozen 1018/1024), median −24%; m=8 precession 0.999 vs frozen 0.955, but period 0.976 < 0.99, so m=8 stays unlicensed exactly as the dossier says.
- **Near-circular family (the refit's target, the author's broken channel):** GEO worst advance error 1.66e-8 at e=1e-4 vs frozen 3.0e-2 — six orders; family 96/96 vs 61/96. This supplies the e→0 limit of the undecided kill-bar row. New caveat the author missed: at e≈0.03 (straddle) GEO is mildly *worse* than frozen (3.1e-3 vs 2.2e-3), both inside bars.
- **Moderate strong-field rows (u_apo < 1/6, outside the NaN set):** no GEO regression. **Fixed-point audit (352 seeds):** converges in 3–5 rounds, zero cap hits, bit-stable. **m=64:** pattern continues (9.9e-6 vs 1.1e-5).

**Why silver, not gold:** the author's own decisive channel never ran — the pre-registered kill bar is undecided, and four of seven instrument channels are broken in the run's walker; the graded path is the r1 rung, which has still never been graded, and adoption needs a canon reset plus an r1 re-freeze naming the band-constant rule, with the integer form unpriced. The one experiment to gold is named in `check.md`. Novelty is clean: this is exactly the "one measured row" fe85's wiki page asked for, and it deletes the "m=32 minimum" premise through the precession channel.
