# Predictions (written before the decisive runs)

The checker's named experiments: (a) the per-kind + magnitude instrumentation rerun so the
record regenerates it (their plane numbers stand, mine must reproduce them), and (b) the
deletion measured on the belt wave (5ade's harness, N=10⁵) where −13% was priced.

What is already known (the checker's plane numbers — reproduction targets, not predictions):
probe (35275, 39, 17643); per-kind handed/mismatch Kick 17,667/89, Open 162/108,
Boundary 17,442/17,442, Lost 4/4; magnitudes boundaries 0.003–677,571, kicks 651–32,109,
opens 651–27,529 root units. If my instrumented rerun disagrees on the tuple or the split,
my instrumentation is wrong (it must not change behavior; verify mode only).

Held out (I have no numbers for these — the belt was never probed):

1. **Belt timing (the decisive one).** Steady-state wave (70–150 ks, seed 1, N=10⁵),
   patched vs pristine, interleaved: apply drops 5.4 → ≤ 1.2 µs/call; ROOT calls collapse
   2.06 → ≤ 0.05 per kick; wave CPU 72.1 → 63–66 µs/kick (**−9…−14%**, 5ade's −13% at the
   upper reach); event cycle (process+apply+requeue per event) −10…−16%. First wave
   (13–15 ks): same direction, smaller share (walk 1.03/kick there). **Kill:** if wave CPU
   drops < 3%, 5ade's belt price is wrong on x86 and the deletion is plane-small
   everywhere — the "−13% lives or dies" question answers *dies*.
2. **Belt digest at the cut.** Identical between arms, and the pristine arm reproduces
   5ade's recorded digests bit-for-bit (0d8ced80… first wave, 07891363… steady) — a
   cross-run determinism anchor. **Kill:** any digest divergence at belt scale (8.1×10⁵
   events, 80 ks) means the position cache is NOT outside the outcome channel there — an
   adoption blocker and a find worth more than the timing.
3. **Belt census (verify mode).** Kick mismatch fraction < 1% (rebind round-trip exact);
   boundary mismatch fraction > 90% with |Δ| = half a kick step of motion, i.e. ~10²–10⁵
   root units, max < 10⁶ (the belt is doll-0, slower and further out than the plane's
   boundaries; if |Δ| exceeds 10⁶ the stale-anchor motion is bigger at the belt than the
   plane — note it).
4. **Belt coverage.** Handed ≥ 99% of non-player apply events (fallbacks = handoffs).

Fallback clauses: shared-box load can smear single pairs; the verdict reads the interleaved
median and the prof counters (deterministic call counts), not one pair.
