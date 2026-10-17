Working...
Check complete. `check.md` written — **Grade: silver** — and the author's wiki page corrected in place.

**What reproduced** (clean tree, patch applied, rebuilt):
- Core mechanism: starved arms grow held scans and RSS together (m100: 89–100 kB/scan regen); digests identical across every wall budget (`2713edb5…`, plus the cap arms' `a35637d9…`) — law innocent, wall path only.
- The bimodality at the shipped default, made deterministic: my forced-load run (ms 5.0, 6 spinners) grew held 4→38 while the quiet/ambient pass stays flat, same digest.
- Mid-knob ms 2.0 (outside the author's sweep) also grows — the cliff sits between 5.0 and 2.0, as the drain condition predicts.
- The settle spike's load dependence: the runner's regen pass (box at load 17.7) reproduced END RSS 45.8/159.8/160.0 MB vs the author's quiet 24.0/44.9/46.1, digests equal.
- Code claims all verified: `room ≥ 2·max(scan_ns, 750 µs)` at universe.rs:1190, `SCAN_BACKLOG = 2048` behind the "about 10 KB each" comment (:77), `Held::capture` pinning one `Binding` per window candidate, `prune` only in `frame_to` (:1082) so `settle` bypasses it.

**What broke** (why not gold):
- The m800 arm is void: `--members` clamps at 400 (xtask mod.rs:40; `--members 800 --describe` prints "1 fleet(s) of 400 members", byte-identical). The "window saturation (400 = 800)" reading — P4's disclosed outcome — is an artifact of the CLI, not a measurement.
- My unclamped m200 arm gives 112 kB/scan vs 89–100 at m100: the pin is **sub-linear**, not ∝ N; P4 fails independently of the clamp.
- 69f3 (scan-queue) already recorded the drain condition at belt/burn scale — uncited; the run's genuine novelty is naming the held scans as 470f's growing structure, the knob/load control, and the 8–10× comment correction.
- "220.9 MB = the cap, not a leak" stays consistent arithmetic (11 kB/gs × 20,000 gs ≈ 2048 × pin; 78k-alloc bulk drop ≈ 38/scan) — the cap was never observed engaged (held ≤ 172 anywhere).

**Gold experiment named:** re-fly scaling off the clamped harness and run one arm until `SCAN_BACKLOG` engages — held pinned at 2,048, RSS plateauing at 2048 × pin. Page corrections: clamp fact folded into Current best, cap marked arithmetic, 69f3 cited, Refuted entry fixed. Tree restored (patch reverted, no stray spinners).
