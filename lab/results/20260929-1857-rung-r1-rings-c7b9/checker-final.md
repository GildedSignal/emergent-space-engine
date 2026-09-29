Working...
Check complete. Deliverables in place: `metrics-check.json` (my reproduced numbers), `check.md` (report), `work/` restored to the author's original file set, nothing committed or pushed.

**Verdict: VOID** — the author's session hit its deadline mid-run (no dossier, no predictions, no metrics.json, no picture). No configuration passes or dies on this run.

**What I verified:**
- **Reproduction:** recompiled `work/rung_r1.c` unmodified → `river-m32` metrics reproduce **byte-identically**; `river-m16` and `tiltonly` also ran (both fail every criterion). `binet-m8/16/32` and `square` exceed 400 s without producing metrics.
- **Oracle:** all ports match `xtask/src/gr_oracle.rs` / `gr_oracle_extended.rs` line-for-line; selftest values cross-checked by hand (periapsis, null turning, tail, capture separatrices). Correct.
- **Seeds:** regenerated from the frozen sampler — match.

**Three implementation defects against the frozen spec:**
1. **Binet band index inverted on outward crossings** (`EV_OUT` does `k--` where the u-band geometry requires `k++`). Traced on seed 0: after the first crossing the orbit lands in a band that doesn't contain u and oscillates there — 0 crossings/cycle, advance 30–75 % off GR. The centerpiece's numbers are invalid; this also explains the >400 s timeouts (`EV_STALL` path bypasses the φ-cap check).
2. **River `dt` integrand is γ× too large** — code returns g²/(ob²S); correct is g/(ob·S) (flat-space check fails 4/√3 vs 2/√3). River periods measure the bug, not the model.
3. **Median fabrication** — `cross_counts[130]` when most seeds fail; `crossings_per_cycle = 1.0` is an artifact.

**Adversarial:** my independent spec-literal river reimplementation confirms the river model *genuinely* fails at m ≤ 32 (advance +0.26 vs GR +1.23 at p=20; retrograde at p=84; 562 rad/cycle chatter at p=10/e=0.7) — so a corrected rerun would still kill river, but on honest numbers. `tiltonly` fails as a negative should; `square` times out, so it says nothing.

Next run needs: the one-character Binet fix, the dt fix, a real median, bounded loops — then all seven configs.
