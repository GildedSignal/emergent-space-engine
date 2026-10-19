# Predictions — run 20261019-1817-system-c7a6 (system lens)

Question: the burn-mode memory ratchet's fuel is the retention law `keep = 2·light_distance + 2²⁶`
(universe.rs:1247). Who actually reads history that deep? The demand side has never been measured;
today's runs (4447, e181, 527a, b911, f80a) all attacked the supply side.

Instrument: print-only census inside `PlainBodies::binding_at` (body.rs) — every call classified
as current-binding (t ≥ event_time) or history (t < event_time), the history look-back
`now − t` in ticks, three call sites tagged (VIEW = the past-light-cone gather, SCAN =
Held::capture, OTHER = everything else: credit walk-backs, rebind reads, handoffs, clock sources).
Env-gated (`READ_CENSUS`); off = shipped bits, no counting. Supply read as `probe_keep_ticks` =
the exact `keep` expression for sampled bodies. 1 game-s = 1 tick × TICK_SECONDS (4.9255 µs);
the doll interval is 28,141.5 game-s (checked against the record).

Arms (shipped `nladder` example, seed 1, 12 ms, guard cap lifted to 100 s via `LADDER_CAP_S`):
- A (the ratchet scene): `30000 burn 100 2000` — no view gather in flight (the shipped loop
  gathers only at the end, if it fits; disabled here by the cap so the arm is purely headless).
- B (the view runs): A + `LADDER_VIEW_EVERY=900` (a warm gather every 15 s of wall time).
- C (control): `30000 coast 100 2000`.

Predictions, written before the first flight:

- **P1 (the headless demand is shallow and flat).** On A, ≥ 99% of `binding_at` calls hit the
  current binding, and the deepest history look-back at every probe from 30k game-s on stays
  ≤ 8×10⁴ game-s (≈ 3 doll intervals; the bound is `credit`'s walk-back, ≤ 2 whole-step windows),
  and does not grow with play time (lb_max past 150k within 2× of lb_max at 30k), while the
  supply `keep` for belt bodies passes 3×10⁵ game-s — keep/lb_max ≥ 4× at 150k and rising
  without bound (keep grows ~2β·t, the demand does not grow).
- **P2 (the view is the one deep reader, at exactly one leg).** On B, VIEW-site history reads
  appear with look-back ≈ the gather's own max emitter age (within one interval), and the max
  look-back over all sites never exceeds one light leg + one interval: lb_max < ld_max + 8×10⁴
  game-s at every probe. The second light leg of `keep` is read by nobody, on any arm.
- **P3 (demand is phase-independent).** A vs C at matched probes: history-read rate per body and
  lb_max within 2× — the demand side is the same in coast and burn; only the supply (the
  observer's recession) differs.
- **P4 (the stock is unread).** On A past 100k game-s, history reads run < 0.01 per body per
  game-s while the retained stock is ≥ 8 segments per body — over any window as long as one
  kick interval, ≥ 99% of retained segments are never read.

What would kill the reading: a history reader with look-back that tracks `keep` (the demand
genuinely covers the interval — then the ratchet is the price of a real reader and the fix must
move that reader, not the retention law); or VIEW reads beyond one leg (the 2× is load-bearing).
