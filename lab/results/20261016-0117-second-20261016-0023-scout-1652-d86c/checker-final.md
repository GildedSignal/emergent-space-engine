Working...
Check complete. **Grade: silver** — written to `check.md`, page corrected in place, tree restored clean at base `d8e7176`.

**What held (reproduced exactly):**
- Applied `work/patch.diff` myself; all six dossier flights re-flown. My deterministic digest tables hash **identical to the runner's regen** (coast `27d90a6c…`, burn `bd2b4d90…`), floor-on = floor-off in both — third independent execution of the record.
- Every dossier number verified in the logs: 16.0× coast (1.053→0.066), 3.3× burn at 60k, IN_WINDOW 100%, dead_with 20→0, view misses 6 vs 21,206, warm serves 175 vs 10,052/gather, engine serves identical per interval, **zero engine misses anywhere**.
- Code paths real (`ext.rs:134` refusal → `view.rs:293` `t_read = event_time` fallback confirmed in shipped code); the instrument fixes both defects the scout's checker named.

**Adversarial (4 arms, 3 beyond the author's domain):**
- **150k coast** (2.5× the horizon): digests still identical, but the run's own registered D2 bound **breaks** — 6 emitters past their own discs at 90k, 228 at 150k (~60 m scale, zero vanish). Per the author's own pre-registered rule: a blocker at depth.
- **150k burn**: digests identical, but the standing cut **decays 3.3× → 1.6×** (floor-off residue 100% in-window, growing 0.43→1.57). The invariant win is the ~1.0 segs/body dead pin, not the ratio; "equals that need exactly" was a 60k snapshot.
- **N=5×10⁴**: clean (digests identical, 1.011→0.013, zero over-disc).
- **Fresh wall re-flight**: observer-fallback mode recurs, no emitter lost — but the dossier's wall numbers (−6.94×10⁶ m, "spread ~60 m") **don't regenerate**: the rerun shows −9.19×10⁶ m with ~60 km spread (rigid only to ~0.7%), and the original logs were overwritten by regen.

**The named gold experiment:** fly the deletion to depth (≥150k) with the far class — the infalling comet class, the page's own Open direction 6 — and the view cap wired; restate the standing-store law floor-off (dead pin deleted vs in-window growth). Novelty confirmed: this was the scout-checker's named experiment, not a repetition; no HISTORY entry covers it.
