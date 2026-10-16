# Predictions (written before the decisive runs; smoke-tuned only at N=2000, window 13-15 ks, both arms)

Probe: `cargo run --release --features prof -p emergent-universe --example waveprobe -- <N> <pre game s> <post game s>`,
single-threaded, unlimited budget (settle), Linux/x86 shared box. Arms: `ES_TAU_CARRY` unset (off = shipped
bits) vs `=1` (the two exact tau carries). Decisive runs: N=1e5, window 13,000-15,000 game s (the belt's
first-kick wave) and window 70,000-150,000 (the second and third waves), plus `frame_digest` at both arms.

1. **Bit-identity.** `Universe::digest()` at each cut is identical between arms, and `frame_digest`'s
   digests (the plane's flights, no extras) are identical between arms. If not: VOID, instrument or
   carry is wrong.
2. **The tau pair is a duplicate walk.** Off-arm, per fired kick: `W_TAUT` = 1.0 and `W_TAU0` = 1.0 calls
   (~3.4 us each on this box). On-arm in the first-wave window: `W_TAUT` -> 0.0 (the kick's own decode is
   handed to the rebind), `W_TAU0` -> ~1 call per body (its first kick: the birth binding has no cached
   anchor), so the first wave saves one walk per kick, ~8% of the kick item.
3. **In the second/third-wave window** every binding has its anchor cached: `W_TAUT` = 0, `W_TAU0` = 0,
   and the kick item falls by two walks (~13 us of ~85 us item+apply cycle on this box), ~15%.
4. **The belt kick's interior is walks + fit, ≥ 80% of the item**: ~5 own decode walks (own, bind, tau x2,
   boundary amortized) + ~3 source walks (one per planet read through `ctx::state_of`), ~3.4 us each, and
   `fit: bind_surface` ~16-20 us/call on this box (the M1's compile-only anchor is 4.4 us; this box is
   slower and `bind_surface` is fit+compile+word, not compile alone).
5. **Source reads repeat**: at N=1e5 the (body, tick) source-read census shows repeat share >= 0.6
   (smoke: 0.614 at N=2000, worst multiplicity 255): a shared-key memo would delete that share exactly.
6. **The third exact duplicate is apply's position walk** (`root_state_raw`, ~6 us/event, 1.0 per event):
   named and priced here, not built.

Kill criteria: any digest divergence (VOID); `W_TAUT` not exactly 0 on-arm (instrument wrong); the kick
item not falling by the deleted walks' ns within noise (the walks are not what I think they are).
