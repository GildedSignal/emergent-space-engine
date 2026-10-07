Working...
**Grade: silver** — written to `lab/results/20261007-1032-spacex-3d04/check.md`. Tree restored to `cae700a` (patch reverted, only untracked `lab/results/`).

**What I did (30 min):**
- **Reproduced** every dossier command in a clean tree, then with `work/patch.diff` applied. All digests bit-exact: `6ce636fa` (rtf 100, paced = unpaced, pre- and post-patch — bit-neutrality confirmed), `d0a37c3f` (rtf 10⁴, engine-ms 5 = 50, deferral 132→0), `99d27789`/`64255c32`/`225ee461` (burn/coast/coast-10⁵). Events/s within 1% of the author at every rung (61/92/337/551/2678 vs 61/93/338/552/2679). The 10⁷ game-s coast fails to settle in 100 s (exit 124, 0-byte report) as claimed.
- **Pre-registration verified by mtime**: predictions 10:36:14 < first bench 10:36:56; the two misses are reported as misses.
- **Five adversarial cases**: paced 10³ (p99 12.1 ms, 0 hitches, same digest — kill criterion survives one rung past the author's check); rtf 300 flat; seed 2 coast survives; `--level 3` on the patched binary **errors** (the patch silently deletes `--level` while `--help` still documents it); rtf 10⁵ default **aborted with no report on the first try** — the author's reported instrument hole, reproduced.
- **Novelty**: nothing in HISTORY maps the plane's rtf envelope; the HANDOFF "100× and more" claim was unmeasured before this.

**Why silver, not gold**: measurement + instrument work — no bottleneck moves 10× yet, and two headline constants are box-conditioned (coast ceiling 8.5×10³ on my runs vs 3–4×10³ stated; the fleet-dead 3.36×10⁴ row aborted here). The gold experiment is named: re-run this envelope with the slack skin; ≥10× ceiling movement is that gold, with this run as the frozen baseline — after restoring `--level` and making player loss degrade instead of abort.
