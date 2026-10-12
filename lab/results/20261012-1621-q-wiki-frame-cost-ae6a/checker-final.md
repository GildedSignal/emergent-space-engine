Working...
Check complete. **Grade: gold** — written to `lab/results/20261012-1621-q-wiki-frame-cost-ae6a/check.md`; the author's wiki page needed no correction (no overstatement found in 20+ sampled numbers).

**What I verified:**

- **Reproduction:** `verify.py` passes independently (partition 68 = 30+34+3+1; tally gold 15 / silver 50 / lead 2 / missing 1). The probe's four digests are bit-identical across three independent passes (author's, runner's regen, mine at 1600/3200); hitches wobble with shared-box load exactly as disclosed.
- **Branch truths, checked directly:** the b7a4 grade drift is real (branch says gold, cluster list silver; kick-cadence, correctly off this page); a342 truly has a dossier and no check.md; the canon leak is live on main (`session.rs` `input(now, keys)` at the presented tick; no `decision_tick` test).
- **Adversarial, outside the author's domain** (seed 1 only, ≤6,400): seed 2 at 6,400 → 129.9 ms worst hitch; 9,600 members → 106.1 ms, RSS 2.6 GB (~271 KB/member, corroborating 3cfc's memory ceiling). No ≥0.6 s stall anywhere through 9,600 — the 3cfc/ba35 contradiction resolution holds beyond the tested range. 12,800 is memory-blocked on this box (~3.5 GB), matching the author's disclosure that it went unmeasured.
- **Novelty:** `lab/wiki/frame-cost.md` was the integrator's empty stub; this run is the designated first compiler.

**The one defect (named in check.md, one-line fix at adoption):** `regen.sh`'s patch-apply step uses a repo-root-relative path, so from a clean checkout it never applies `patch.diff` and the probe silently benches four identical 400-member scenes — I proved the silent clamp on a clean build (`--members 400` ≡ `1024`, both digest `11ad8fb9…`). The archived numbers are genuine (I reproduced them with the patch applied, per the dossier's stated precondition), but a future clean-tree regen would wrong-pass at exit 0.

Topic stays open, as the author judged: closure would block open directions 1–7, which are the board's live question.
