# Predictions (written before the decisive run)

Run: 20261004-0555-taleb-b41e, `memo_probe`, decisive config `members=1024 frames=1800`
(smoke was `256 60`; its numbers are in brackets and were tuned on, so they are not evidence).

The question: law.md's state says the cycle memo is "keyed by quantized (E, L) … shared by every
tube with the same key". The plane's Catalogue is a keyless arena, so every kick rebinds and
compiles a fresh trajectory. What would key-sharing actually buy, and is exactness kept?

1. **Key churn.** Distinct exact keys per rebind stays ≥ 0.95 (each rebind compiles a trajectory
   no other body can reuse). [smoke: 767/782 = 0.98]
2. **Memo hit rate.** Distinct 12-bit memo keys / rebinds falls with run length as the scene's
   key cells saturate; in-stream hit rate (a keyed catalogue hits when this rebind's memo cell
   was already visited) rises above the smoke value. Predict ≥ 0.75 at 1800 frames. [smoke: 0.69]
3. **Exactness control.** `from_state_memo` reconstructions are bit-identical to the bound state
   for 100% of sampled rebind states; residual ≤ ~60 bits (comfortably inside the 65-bit residual
   word the space crate documents). [smoke: 30/30, 52 bits]
4. **Cost split.** On this cloud box, `Orbit::compile` alone is a minority of `from_state`
   (compile ~2–4 µs of ~10 µs; the fit dominates), so a keyed memo removes
   `hit_rate × compile` per kick: a ~10–25% kick-cost cut here. The integrator's M1 measurement
   (15 of 29 µs in "rebinding fit and compile") implies ~35% there — inference, cloud timings are
   orders of magnitude only.
5. **Memory.** One compiled entry is ~0.6–1 KB deep. Unshared (today's plane), each decorrelated
   body carries its own entry: ~10⁹ bodies ⇒ ~10¹² B-class overshoot vs the 8 GB budget — entry
   sharing is not an optimization but a requirement of bottleneck 5; sharing caps live entries at
   distinct live keys, which for correlated fleets is per-family, not per-ship. [smoke: 848 B/entry]
6. **Fleet members are lattice bodies** and never appear as tube rebinds; rebinds come from ships,
   doll centres and leavers only. [smoke: 28 tube bodies at members=256]

What would make the memo idea wrong (falsifiers, pre-registered):
- memo hit rate ≤ ~0.3 at 1800 frames ⇒ sharing buys nothing under the plane's own kicks;
- any reconstruct failure ⇒ the residual does not carry the quantization (premise dead);
- memo quantize errors > 0 on real states ⇒ the 12-bit key is not representable for this scene;
- residual > 65 bits ⇒ words overflow (the documented per-component bound).

Commands (≤ 60 s): `cargo build --release -p emergent-universe --example memo_probe`
then `./target/release/examples/memo_probe 1024 1800`.
