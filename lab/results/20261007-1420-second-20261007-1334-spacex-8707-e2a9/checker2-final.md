Grade: goldCheck complete. **Grade: gold** — written to `check2.md` (full report) and `checker2-final.md` (grade + abstract) in the run folder; nothing else in the run folder was touched, and `check.md` was never read.

**What I verified:**

- **Reproduction, bit-level.** The port (`hlive2.py --sampler orig`) regenerates the silver's `conv_dt10.json` bit-for-bit on every original key; my full-scale reruns of both decisive scenes (b17/b16, seed 7, N=30000, 1000 yr) are **bit-identical** to the stored JSONs; the null reproduces exactly (4.05e-12). `orig/` is md5-identical to the `claude/lab-20261007-1334-spacex-8707` branch — the record the relabels come from was not doctored.
- **Premise against the repo.** `belt.rs` SPEC matches the dossier's sampler exactly; `scenario.rs` AU/STAR_RADIUS match the scale derivation to 0.014%; darwin is Q16 doll-relative with the 8192 cap, so the placement is genuinely unfrozen (HANDOFF still queues the wiring with Sol) and k∈{16,17} are the only between-planets power-of-two placements.
- **Predictions.** mtime 14:32:42, before null (14:34) and decisive outputs (14:38–39); 6/7 held, the one miss (b16 exponent 0.013) in the cheaper direction, honestly reported.
- **Attack.** Held-out seed 10: every headline holds (rate 1.0e-3/9.91e-4, exponent 0.612, T*=5). 3×-Giant: long-run rate unchanged, T* only 5→2 yr. My b16 dt=0.05 probe (the convergence case the author never ran — only ~15 kicks/orbit at the inner edge) confirms the plateau and T*=20. Pre-registered kill criterion nowhere near triggered.

**Nits recorded** (none load-bearing): the 0.23% session-lag median hides seed 7's 3.1%; "nobody crosses q=3e-3" is 0.1% on seed 8; the dv-min bin is the inner edge, not "band-centre"; post-refit regrowth is inferred, not directly measured.
