Grade: gold

**Abstract.** The named gold experiment is flown and reproduces exactly: on a fresh build of `work/patch.diff` (clean tree, `cargo build -p xtask`), B13 armed fails 0/64 (worst ΔE/ΔL 4.65e0) vs off 60/64 (2.12e-2, bit-matched to HANDOFF's baseline), engagement verified (PLANE_TRACE kicks 305→213, same per-seed counts as the author's trace). All 13 armed `ladder_digest` digests change; off is bit-identical to pristine — the first checker's armed-identity was an artifact. Root cause proven here: regen.sh's target-filtered build line never rebuilds xtask, so the runner's own regen.log ran a stale pre-stagger binary and printed armed == off. Adversarial beyond the author's range: stagger ÷64 → 40/64, worst 1.17e-1 — damage monotone in the shift, so bounded post-hoc staggers fail too. The adoption direction is killed cheaply; the cure routes to the birth program. Adopt the kill; fix regen.sh (build xtask explicitly).

**Reasons.**

1. **Reproduction (my own hands, clean tree + `git apply work/patch.diff`).**
   - B13 off: `60/64, worst ΔE 2.12e-2 ΔL 2.12e-2` — identical to HANDOFF's baselined red ("B13 60/64 (baselined red)", docs/HANDOFF.md).
   - B13 armed: `0/64, worst ΔE 4.65e0 ΔL 4.65e0` — the dossier's headline, exact.
   - Engagement: `PLANE_TRACE=1 ES_STAGGER=1` gives per-seed kicks 213/214/101/270…, matching the author's armed trace line-for-line; off gives 305/275/130/310… — the encounter is sampled materially differently, as claimed.
   - Digest record (runner's regen, whose example binaries were genuinely rebuilt by the pristine dance): OFF bit-identical to pristine; ARMED 13/13 case digests changed, 4 with changed kick counts (`N=1000 coast through the wave` 32,537 → 31,973) — dossier exact.
   - Moon probe (regen's rerun): seed 4 rates 0.8906/0.8880/0.8712, seed 1 −0.0325/−0.0314/−0.0389, seed 5 −0.1385/−0.1379/−0.1488; escape class identical across off/armed/reference (3/3/3) — dossier exact.
   - B14 armed on my fresh staggered binary: `B14 FAIL timeout` — P3 confirmed on clean provenance (the regen's B14 lines ran the stale binary, but the off-arm timeout is HANDOFF-known and the armed arm is a fortiori).

2. **The regen.log anomaly is explained and the dossier survives it.** regen.log printed "B13 armed: 60/64" (identical to off). I proved the mechanism: `cargo build --release -p xtask -p emergent-universe --example ladder_digest --example stagger_probe` is target-filtered and **never builds xtask** (deleted xtask, ran the exact line: Finished clean, xtask absent). The regen's gate invocations therefore ran a leftover pre-stagger xtask from the author's session. The author's mitigation (engagement-verify every armed number) was right; their mechanism attribution ("env-drop") was wrong — I corrected the wiki page's mechanism sentence in place. This is a real, recurring hazard for every armed/off experiment in the lab: **build the gate binary explicitly and engagement-verify it, not just the examples.**

3. **Adversarial cases (three, one outside the author's tested range).**
   - *Bounded stagger (outside the range; the author's own named-but-unflown falsifier):* offset ÷64 (0.5666 → 0.00885 of a step) → B13 `40/64, worst 1.17e-1`. Monotone: 0 shift → 60/64 @ 2.12e-2; ÷64 → 40/64 @ 1.17e-1; full → 0/64 @ 4.65e0. Damage is continuous and nonzero at ~1% of a step — the kill extends to bounded post-hoc staggers, strengthening the birth-time-lawful conclusion beyond what the dossier claimed.
   - *Binary-provenance control:* fresh `cargo build -p xtask` from a clean patched tree reproduces armed 0/64 — the damage is the kick-time shift itself, not any armed-build pathology.
   - *Engagement outside the gate path:* armed digests change 13/13 while off is bit-identical to pristine — the off arm is a clean no-op, the armed arm is visibly engaged.

4. **Predictions.** `predictions.md` predates the decisive runs (file times: predictions 05:09 < probes 05:17 < traces 05:32). P2, P3 held; P4 held on class with the band honestly missed (2.9e-2 vs 1e-2, still 3.4× inside the gate's own 10%); P1 and P5 failed as written — and the pre-registered kill criterion ("armed B13 below ~56/64 kills the adopt-as-birth-default direction") fired. The failures are reported as failures, with diagnosis, and the answer went against the author's expectation — the opposite of tuned. This is the shape H0183 protects: the failed expectation is the finding.

5. **Novelty.** No stagger or spacex-917c entry in docs/HISTORY.md; the wiki fold-in (current best, refuted line, runs line) is new against `lab/wiki/nladder.md`. The parent's run was silver with this exact experiment named as its gold step; this run flies it and kills the configuration. The first checker's contrary "armed digest identity 13/13" finding is refuted with a proven mechanism.

6. **Goal fit.** Board focus 1 (bodies: 28 → 10⁹; the nladder). A configuration one integrator decision from adoption is killed before wiring, and the wave's cure is redirected to the birth program (B18's domain), where single-birth scenes stay untouched. PRINCIPLES #9: "A failed experiment kills that configuration, never the method"; #22: "the simulation decides" — the stagger moved when the first surprise lands for our bookkeeping, and the assist gate felt it. Nothing to adopt except the kill and the instrument fix.

**Required with adoption (one line):** regen.sh must build the gate binary itself (`cargo build --release -p xtask` as its own line) — as shipped, its decisive armed number silently regenerates as the off number on any box with a stale target dir. The dossier's named command (`xtask behave --law plane --gates B13` armed) regenerates the number exactly on any fresh build, which I did.

**What the author missed.**
- The regen.sh provenance hole itself: their diagnosis ("env-drop", `VAR=1 cmd > file` form) names the wrong mechanism — env vars propagate fine; what silently disarms an armed run is a stale xtask binary that the regen's target-filtered build line never rebuilds. Their own regen.log fell into it on the runner; a future run could too, in the other direction.
- The bounded variant was left unflown (their own named next falsifier). Flown here: 40/64 @ 1.17e-1 — the failure is graded in the shift fraction and does not vanish at 1% of a step, so "a bounded variant is the natural next falsifier" is answered: it fails too, and the kill should be stated for post-hoc first-kick movers as a class.
- The instrumented trace build ("STAGGER engages" print) was not shipped in patch.diff, so the trace evidence was not regenerable from the record; PLANE_TRACE's kick counts re-derive it on shipped code (done here).
- regen.log's B14 armed line also ran the stale binary; re-run clean here (timeout, as claimed).
