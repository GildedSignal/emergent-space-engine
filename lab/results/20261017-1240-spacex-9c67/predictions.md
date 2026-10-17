# Predictions (written before the decisive runs)

The change: `apply`'s post-event `root_state_raw` walk is replaced, for every event whose
resolver read or built the body's state at the item tick, by that handed-over state (same
arithmetic, doll chain still walked). 5ade priced the walk at 5.0 µs × 2.06 per kick (−13%
of the event cycle) but never built it.

Cases I have NOT tuned on, and what I expect there:

1. **Bit identity (ES_POS_VERIFY=1, cost_split settle + a flown bench flight):** the handed
   state equals the fresh binding's `readout` at its anchor exactly, because the fit
   decomposes into (decoded, residual) as integers and `readout` re-adds the residual.
   Prediction: **POS_MISMATCH = 0** over ≥ 10⁵ events. If the fit ever truncates, mismatches
   appear first on high-e clock-stepped bodies (the deepest word offsets) — I have not
   checked the fit's word discipline.
2. **Coverage:** POS_HANDED/(POS_HANDED+POS_WALKED) ≥ 95%. The fallbacks should be first
   plans (`replan`), handoffs (capture/release), and terminal crashes that never read.
3. **Digest identity:** kick-bench's `replay_digest` identical trivially (pure resolver
   untouched); the game `digest` identical only if resolution order (which the position
   cache feeds through deadlines) does not change any recorded state. Positions are
   documented as "never an outcome". Prediction: **identical**; if not, the run reports the
   divergence and the deletion is not free (a law-visible ordering channel — itself a find).
4. **Timing (interleaved, same box):** the whole-universe µs/event in cost_split drops by
   ~8–15% (5ade's −13% ± load noise); the pure-resolver kick µs unchanged (control); the
   `--bench` ROOT bucket ("position walk") collapses toward zero. If the drop is < 3%, the
   walk was not 5 µs on this scene/population mix (cost_split's plane is 32-body, not the
   belt) — the claim then restates on the bench arm only.
5. **Held-out:** a second seed and a burn flight (player input) must hold 1–4; the burn arm
   exercises `decide`'s hand-off, which no default settle run touches.

Kill criterion: any POS_MISMATCH > 0, or a changed game digest, kills the "exact duplicate"
claim (5ade's letter) for the affected arm; timing is secondary to identity.
