# Predictions (written before the decisive runs)

Question: what is the burn read stream FOR? (promotion.md, open direction 1.)
Instrument: `readstat`, a `#[track_caller]` census of `Binding::readout` by call site,
print-only, armed after the build (patch = bind.rs + nladder.rs; no arithmetic touched).
Runs: `nladder <N> <coast|burn> 20 100` (2,000 game-s target, rtf 100, seed 1), the
ladder's own harness. The burn enters the star's doll (where every belt body lives) at
frame 947 (15.8 s of page time), so each 20-s flight holds ~4 s of page time inside the
root doll.

Tuned on: N=1000 coast 5 s (the pilot, above).

## Pre-registered, on the cases not run yet

P1 (burn 10^5, 20 s): `encounter.rs:137` (the scan's pair test) is the top site, and the
scan family (encounter.rs:133/137/168/180) holds >= 60% of all readouts.

P2 (N-scaling, burn): the scan sites grow ~10x from 10^4 to 10^5 (N-linear, per-body
flat), while the resolver's own sites (step.rs:407/478, the kick and settle reads) stay
within 2x of flat (their bodies are the ~300 locals and the player, not the belt).

P3 (coast vs burn, 10^5): coast's scan share is far smaller (< 30%): the coasting player
never enters the root doll, so its scan reads only Home's ~300 locals; the top coast site
is the view/observation family (observe.rs) or the scan of the locals.

P4 (held-out from the tuning run's family): at N=10^3 burn the per-body scan rate (scan
reads / body / gs, counting only page time in the root doll) matches the 10^5 rate within
2x (the belt's density is N-independent, so the scan reads each candidate the same number
of times; only the candidate count grows).

P5 (the deletion it names): if P1 and P2 hold, the read stream is not the kicks' settle
(the kick sites are flat in N): the representation that deletes it is the scan's own
(candidates the player cannot touch this window never get a pair test), i.e. the
encounters tier's certificate, not a smaller binding.

## What would make each wrong
- P1 wrong => the read stream belongs to the resolver or the view; the deletion moves there.
- P2 wrong (scan sub-linear) => the scan already prunes by density; the knee's cause moves
  to whatever site carries the growth.
- P4 wrong => the scan's per-candidate read count depends on N (a window effect), and the
  per-body flatness claim in promotion.md needs re-deriving.
