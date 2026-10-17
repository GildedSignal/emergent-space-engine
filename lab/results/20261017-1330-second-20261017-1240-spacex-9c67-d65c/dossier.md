# Dossier — 20261017-1330-second-20261017-1240-spacex-9c67-d65c

**Claim.** The checker's two named experiments are done and the adoption's record is complete:
the per-kind + magnitude census reproduces the checker's numbers exactly and now regenerates
from shipped code, and the deletion measured on the belt wave (N=10⁵, 5ade's own harness) is
**real but −9…−11% of wave CPU, not 5ade's −13%** — the hand-off deletes only the body's own
tube walk; the belt ships sit in planet dolls, so the centre-chain walk stays — with digests
identical at both cuts (5ade's pristine anchors reproduced bit-for-bit) and the stale-anchor
mismatch censused at 41× the plane's events (boundaries 100%, |Δx| to 6.8×10⁵ root units,
kicks 0.04%), the outcome channel blind to all 720,562 divergences.

**Bottleneck.** The kick/event cycle (board #3). 9c67 built 5ade's third "exact duplicate"
(`Update::own` hands the resolver's state to `apply`, deleting the post-event
`root_state_raw` walk) and the checker held it at silver for exactly two gaps: a census that
did not regenerate, and the gain unmeasured on the belt scene the adoption targets. This run
closes both. Expected gain: none new — this prices an already-built deletion (−9…−11% of the
wave's event cycle, ~6.5–7.6 µs/kick at N=10⁵ on x86) and finishes the outcome-channel
evidence that "positions are never an outcome" (§28) stands at belt scale.

**Evidence** (Linux/x86 shared runner, 8 vCPU, orders of magnitude; every number regenerates
by `regen.sh`, ~12 min: two builds, the plane census, 9 belt runs, `work/analyze.py`):

- **The census regenerates** (checker's numbers stand, now from shipped code +
  `work/patch.diff`): plane probe `(35275, 39, 17643)`; per-kind handed/mismatch **Kick
  17,667/89, Open 162/108, Boundary 17,442/17,442, Lost 4/4** — identical to the checker to
  the event; magnitudes (Euclidean norm, root units) boundaries 0.0033–682,078, kicks
  685–34,727, opens 685–29,774 — the checker's component-wise ranges (0.003–677,571 /
  651–32,109 / 651–27,529) to within the metric difference. Instrumentation is verify-mode
  only (`ES_POS_VERIFY`); behaviour is 9c67's deletion unchanged — and the patched binary's
  digests equal the pristine's, which is the no-behavior-change proof.
- **The belt wave, measured** (steady 70–150 ks, 389,200 kicks + 420,419 boundaries, seed 1,
  `waveprobe` = 5ade's harness with the source census stripped; 3 interleaved pristine/patched
  pairs): **apply 5.6–5.9 → 2.2–2.6 µs/event (−55…−62%)**, the ROOT bucket 4.7 → 1.2 µs/call
  (−72…−76%) with **calls unchanged at 2.06/kick** — the proof of the mechanism's price
  split: the body's own tube walk is gone, the planet-doll centre chain remains (~1.2 µs).
  Stage arithmetic: 3.1–3.6 µs/event saved × 2.08 events/kick = **6.5–7.6 µs/kick ≈ −9…−10%**
  of the 75 µs wave CPU. Wall-clock pairs are load-void raw (the untouched resolver drifted
  +0.6/+7.1/+21.9% across pairs); control-normalized (wave_cpu per process-ns) the drop is
  **−7.8/−10.5/−11.1%, median −10.5%**. First wave (13–15 ks): apply 5.15 → 1.72 µs (−67%),
  wave CPU 53.9 → 50.7 (−6.0%, back-to-back pair).
- **5ade's −13% answered: it over-priced by ~30%.** They priced the whole 5.0 µs walk ×
  2.06/kick; the built hand-off keeps the doll chain above the body, and the true belt
  deletion is the tube walk only (~3.4 µs × 2.06). The "lives or dies" question answers:
  lives, at −9…−11%.
- **Digests, belt scale:** identical between arms in both windows (7 runs), and the pristine
  arm reproduces 5ade's recorded anchors **bit-for-bit** (`07891363…` steady, `0d8ced80…`
  first wave) — a cross-run, cross-day determinism anchor for the whole harness.
- **Belt census** (`ES_POS_VERIFY=1`, patched arm, 1.45 M handed events): **Boundary
  719,845/719,845 (100%) mismatched, |Δx| 0.0014–682,078 root units — the same ceiling as the
  32-body plane**; Kick 283/725,976 (0.04%); Open 404/561 (72%); Lost 30/30. Coverage
  1,446,412/1,446,512 = **99.99% of steady events** (the 100,091 walk fallbacks are the belt's
  birth replans at build, not handoffs — a correction to my own prediction). The game digest
  is blind to 720,562 position divergences at belt scale (80 ks window, 8.1×10⁵ events).
- Commands: `regen.sh` (everything); the decisive arms are
  `waveprobe-{pristine,patched} 100000 70000 150000` and
  `ES_POS_VERIFY=1 waveprobe-patched 100000 70000 150000`, all in `work/belt-*.txt`,
  summarised by `work/analyze.py` into `work/belt-analysis.txt`.

**Predictions** (`predictions.md`, written before the decisive runs): digest identity **held**
(both windows, both anchors); belt census **held** (kick mismatch 0.04% < 1%, boundary 100% >
90%, magnitudes 10²–10⁵ with max 6.8×10⁵, inside the "note if > 10⁶" clause); coverage
**held on the number, missed on the attribution** (99.99% steady, but the fallbacks are birth
replans, not handoffs — handoffs are ~0 in this window); timing **held on the control-normalized
median** (−10.5%, in the −9…−14% band) and **missed on the raw median** (+1.2% — the
pre-registered fallback clause fired: single pairs are load-smeared, the verdict reads the
normalized statistic and the prof counters). 5ade's exact −13% upper reach did not survive;
−9…−11% did.

**What would make it wrong.** The timing is one shared x86 box with a 3-pair interleaved
design and a pre-registered control (the resolver's own stage) carrying the normalization —
a quieter box could shift −9…−11% by a point either way, and the M1 re-measures (5ade's
note: the M1's fit is cheaper, so the walks' share there is *larger*). The census and the
digests are deterministic and bit-reproduced across days and boxes. The remaining unmeasured
surface is the horizon: the belt window is 80 ks and the plane's 1,200 frames; a
deadline-order flip at longer horizons (the cache's only consumer is `light_distance`) would
not show in either — that open question is now the only one left on this lever. **Cost of
adopting:** 9c67's +83/−7 plus ~40 lines of verify-mode instrumentation; no law change.
**Fit with PRINCIPLES:** "The cheapest compute is compute not done. Delete before
optimizing" (§1); "real vs displayed is not the same thing" (§28) — the position cache is
display-adjacent state, and the digest's blindness to 7.2×10⁵ divergences at belt scale is
that principle measured, not asserted.

**The lens (second author).** The lens's discipline here was to run exactly the checker's
named experiments from the run's own scripts and nothing else — and the one judgement call
(the control normalization) was pre-registered in `predictions.md`'s fallback clause before
the pairs ran, because the raw pairs were visibly load-smeared (p3's resolver +22%). The
lens may have missed: a second belt seed (the harness fixes seed 1; a seed change needs
`plane_extra`'s parameter exposed, not done), and the first-wave timing rests on a single
back-to-back pair.

**Grade proposed: gold** — the checker's named experiments are done, the record regenerates
from shipped code, the claim (deletion real, digest-identical, mechanism = the walk's stale
anchor clock) now holds with the belt measurement and the corrected price folded in, and the
one number that died (−13%) died with its cause named (the kept centre chain).
