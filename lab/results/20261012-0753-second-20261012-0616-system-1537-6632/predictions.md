# Predictions (written before the fixed-patch runs)

The prior run's checker named the gold experiment: complete the fleet side of the tick deletion and show
three-schedule digest identity at flat quiet frames. Reproduced first (this session, my binary, clean tree):

- Baseline (unpatched): quiet 219/975/5,683/36,128 µs per frame at n = 1k/4k/16k/64k, events=0; digest
  A=B=C=`645d0367d54b951b4f165ec1ea638a56fb4f650eb4592d7b6b2beac1e8c99204` at cut 9e10
  (kicks 73,316, slices 104/98/106, bodies 36) and A=B=C=`ca3a52509b3f1b0206f378cc4f2a8fab369fd31c459ecfce4fadb5b57c93ec71`
  at cut 6e10; restricted R=R2=`d3dffd24aa54709519c73394802109dd7a6b4a43c9bb331b7ad548532c06a421`.
- Author's patch (`work/patch.diff`, universe.rs only): digest A/B/C = `e1078737…`/`ebaa6ae7…`/`6931638f…`,
  bit-for-bit the checker's values; per-body dumps show **items past the cut resolved** (body 0 event_time
  107.4e9 > cut 90e9; moon 93.4e9), and a backtrace proves the over-cut resolutions come from the top-level
  pop of a **stale `due` entry**: an entity resolved through a pull is requeued into the calendar by the
  patch's own `requeue`, but its old `due` entry survives and later pops, resolving the entity at its
  *current* key, past the frame's target. The checker's "under-resolution" (B: 1 slice, C: 3 slices vs 104)
  is the same disease on the budget path: entities drained into `due` but unresolved at the budget break are
  dropped from the calendar forever (the unpatched code requeued its `deferred` list).

## The fix (one mechanism, three sites)

`due` entries carry the tick they were admitted at; a pop resolves only if `key_of(e)` still equals that
admitted key (lazy deletion — the calendar slot is the single admission authority). Leftovers at the budget
break go back into the calendar. `resolve_fleet`'s early return requeues. The fleet cap takes its
"next entity in line" from both sides (the due heap's min deadline and the calendar's nearest future item,
a lower bound for every calendar deadline), floored at the fleet's own admitted tick — the floor restores
the unpatched invariant (the popped fleet was the deadline minimum, so its cap was never below its tick)
and kills the no-op spin.

## Held-out cases and expectations

1. **Cross-schedule identity, cut 9e10.** A = B = C after the fix. Primary expectation: all three equal the
   unpatched `645d0367…` — the over-cut resolutions were the only source of divergence, and the baseline
   itself proves the fleet's bits are slice-independent (its three schedules agree with slice counts
   104/98/106). If they agree on a *new* value instead, cross-schedule identity still holds but the digest
   is re-frozen (law.md "Ties" keys the queue by `(time, id)`; the shipped deadline key already disagrees
   with the law) — I report that as a law-visible change, not silently.
2. **Alternate cut 6e10** (held out from tuning): same outcome — A = B = C, expected `ca3a5250…`.
3. **Quiet frames stay collapsed.** The fix adds no per-entity per-frame work (the drain touches only
   entities with an item inside the frame): 0.1–0.5 µs/frame, flat within 2× from 1k to 256k bodies,
   events=0, rss under 2 GB.
4. **The fleet-free control.** R = R2 = `d3dffd24…`, unchanged (no fleet, no handouts; the lazy-deletion
   path alone must not disturb it).
5. **The fleet's committed state converges.** Stats at cut 9e10: slices within a small factor of the
   baseline's 104 across A/B/C, leavers=8, dissolved=1, bodies=36, pending_handouts=0 — the battle no
   longer freezes under budget schedules (B/C slices were 1/3 on the broken patch).

Kill criteria: any schedule disagreeing with another at either cut, or the quiet frame regrowing with N,
kills the fix as written and the finding stands as a diagnosis (the tick is real; the deletion needs the
`due`-entry invariant above, not just requeues).
