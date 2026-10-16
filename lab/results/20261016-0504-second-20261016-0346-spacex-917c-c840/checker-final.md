Working...
Check complete. **Grade: gold** — `check.md` written.

**What I established:**

1. **The dossier's headline reproduces exactly on my own fresh build** from `work/patch.diff` on a clean tree: B13 off `60/64, worst 2.12e-2` (bit-matched to HANDOFF's baselined red) vs armed `0/64, worst 4.65e0`. Engagement verified: PLANE_TRACE kick counts (305→213, matching the author's traces seed-for-seed), all 13 armed digests changed, off bit-identical to pristine, moon-probe rates exact.

2. **The runner's own regen.log contradicted the dossier (armed = off, 60/64) — I found the root cause:** regen.sh's build line (`cargo build -p xtask -p emergent-universe --example …`) is target-filtered and **never builds xtask** (proved: deleted xtask, ran the exact line, finished clean with xtask absent). The regen's gate runs used a leftover pre-stagger binary from the author's session. The author's engagement-verify discipline was right; their "env-drop" mechanism attribution was wrong — corrected the wiki page in place.

3. **Adversarial, outside the author's range:** the bounded stagger they named but never flew — offset ÷64 gives `40/64, worst 1.17e-1`. Monotone damage (60→40→0 passing as shift grows 0→1%→57% of a step): the kill extends to bounded post-hoc staggers as a class, strengthening the birth-time-lawful conclusion.

4. Predictions were pre-registered (file times precede the decisive runs); P1/P5 failed as written but the pre-registered kill criterion fired, honestly reported. Novel: no HISTORY/wiki prior. Faithful page fold-in. Goal fit: PRINCIPLES #9 — a killed configuration, one decision from adoption, killed cheaply before wiring.

Required with adoption: regen.sh must build xtask explicitly, or its decisive armed number silently regenerates as the off number on any box with a stale target dir.
