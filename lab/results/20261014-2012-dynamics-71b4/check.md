Grade: gold

**Abstract.** 524e-vs-54d9 is resolved against 524e: the impulse-quantum trigger
walks in a bounded kernel. In 54d9's scene (32 bodies, second-order midpoint
kernel, clock control bounded at slope ≤ 0.013), the trigger walks (slope
0.89–0.92 at 400 parent orbits, D 11–13× the clock at matched rate), and
524e's contrary record is a machine artifact: its held-at-close clock compounds
too (slope 0.82, replicated). All decisive rows reproduced **bit-exact** from
the shipped scripts. Checker probes strengthen the kill: fresh seed 777
(trigger 0.51, clock 0.00), horizon 800 (0.67 vs clock 0.02), and the author's
own named escape — a sigma-delta remainder variant — still walks (0.94 / 0.31).
Gain: deletes the trigger from the adoption path, closes the wiki's named
contradiction. Adoption cost: zero (a kill); fold the page.

**Reasons.**

1. *Reproduction.* Cold rerun in a clean tree (/tmp, shipped `harness2.py`,
   exact `regen.sh` commands): A_K16, A_K32, Q_q0.0005, C_th0.5 regenerate
   **bit-exact** (`dser` max diff 0.0 against the stored npz), including the
   clock rows that predate the author's 20:28 harness2.py edit — that edit
   changed nothing on those paths. `held_A8` slope 0.818 replicates (machine 1:
   the clock itself compounds in 524e-style held kernels — the artifact claim,
   anchored independently by the wiki's stored 524e checker numbers, clock
   T-doubling ×2.27). The convergence claim "3.1–7.3 per rate doubling"
   regenerates from fresh conv runs (3.13/3.61/7.34); an apparent mismatch was
   my own mixing of median conventions on 8-body samples.
2. *Predictions.* `predictions.md` mtime 20:26:58 precedes the decisive batch
   (first file 20:27:11, last 20:36:52); calibration pilots (8-body) predate
   it. P1–P5 and P7 held; P6 (the author's kill criterion) honestly reported
   as not fired.
3. *Adversarial (mine).* (a) **Seed 777** — outside the author's single tested
   draw: trigger walks (slope med 0.511, D 7.1e-3) while the clock stays
   bounded (0.000). (b) **Horizon 800** — double the author's range: trigger
   0.668 over orbits 400–800 with D growing to 1.9e-2; clock control 0.024.
   (c) **Sigma-delta remainder variant** (carry −= q at fire) — the dossier's
   own named "what would make it wrong": walks at both sensor rates (WS=128:
   0.935, D 1.07e-2; WS=512: 0.308, D 4.3e-3) — the decorrelation escape does
   not exist in this kernel. Three probes, all confirming; none found a
   bounded trigger.
4. *Novelty.* The live kick-cadence page names this exact experiment ("One
   experiment decides: run 52[4e's D and 54d9's C in one machine]") and open
   direction 4 prices the trigger "as shipped" with belt savings 2.6–2.9×. Not
   a repetition: it closes contradiction #3 and deletes the standing exception.
5. *Controls on both sides.* Positive: the clock bounded at every rate
   (slope ≤ 0.013 med, p90 ≤ 0.16, second-order convergence). Negative: the
   gate replicates 54d9's walk (0.65–0.88). Both behave; the verdict is not
   VOID, and the walk is not an instrument artifact (post-hoc series rebuilt
   from the fire log on the actual kicked trajectory).
6. *Goal fit.* PRINCIPLES 13: "basically we don't want errors that can compound
   that's the goal" — the trigger compounds. Principle 9: the kill deletes a
   configuration, never the method; the cadence lever stays
   precomputed-from-constants (54d9's surviving scheme). Zero adoption cost;
   B12-register requirement sharpened (expose the walk slope for every
   event-triggered cadence).

**Page corrections made** (in `wiki/kick-cadence.md`): restored the prior
"regime-aware and coarse" summary paragraph (it carried the branch-sweep note
and the three off-page runs aa78/ef10/76d6, which the fold had dropped), and
restored 524e's Runs line to its original append-only text — the Runs section
is append-only; the refutation is already carried in Refuted and
Contradictions. The new paragraph itself matches the evidence number for
number.

**What the author missed.**

- `regen.sh`'s `[ -f ]` guards make the runner's regen a cache hit: a checker
  must delete `runs/` to truly regenerate. Harmless here (bit-exact), but the
  "60 s cached" phrasing invites stale-data grading.
- The 20:28:07 `harness2.py` edit postdates the stored A_K controls
  (20:27:11–33) — undisclosed; the rows do regenerate, but the dossier should
  say which stored data predates the final harness.
- The sigma-delta probe (mine): the author's named untested variant is now
   measured and walks — open direction 4's "decorrelating trigger" hope is
   strictly narrower than the page implies; a future author should start from
   that negative.
- "State feedback of any kind walks" is one kernel, one μ, planar, tide-only;
   my probes widen it (new seed, 2× horizon, remainder variant) but it remains
   a single-machine statement — the page says so, keep it said.
