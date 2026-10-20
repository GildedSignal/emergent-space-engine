# Dossier — 20261020-0036-components-6b9a (components lens)

**Claim.** The live plane's scheduling apparatus — five per-body `Calendar`s plus the
deadline position cache — is 156 B/body of schedule-only state at the shipped
`body_cap` sizing (two of the five containers hold the whole population at every
census, and the same next-tick fact sits in both), no row of the 10⁹ ledger prices it,
so the "wired store 0.2–2.0×" memory closure holds only if the calendars are deleted
or live-sized: unresized, the scheduler alone is 156 GB ≈ 20× the 8 GB machine at 10⁹,
while live-population sizing (λ·τ·N ≈ 1.74×10⁶ slots) costs 0.27 GB — a ×574 flip on
a sizing policy, with the CPU neighbour measured three orders under the event stream.

**Bottleneck.** Memory at 10⁹ (the board's fourth bullet; PRINCIPLES #24 "why do you
need so many bytes per entity?"). Expected gain: names the missing per-body term the
wired composition must delete (156 B/body → ~0.27 B/body), correcting the ledger's
memory row. It deletes nothing by itself; it prices a deletion that is already
designed (25ce's class-major cursors) but never carried as a wired-plane cost.

## Evidence (all numbers regenerate via `regen.sh`, ~2 min, this box, load 1.36–2.49)

*Shipped bytes (instrument: `crates/space/examples/schedbytes.rs`, a counting global
allocator around the shipped `Calendar::new` — no engine change):*
- `Scalar` key = 16 B, heap slot `(Scalar, u32)` = 24 B, `pos` row = 16 B.
- `Calendar::new(n)` allocates **exactly 28.00 B/slot, N-flat at n = 10⁴/10⁵/10⁶**
  (2 allocations: heap 24n + pos 4n). Capacity is reserved once at `body_cap`
  (universe.rs:481–490 — all five calendars; pos at :479).
- Apparatus capacity = 5×28 + 16 = **156 B/body** → **156.0 GB at 10⁹ ≈ 19.5× an
  8 GB machine**; live-population sizing (L = λ·τ·N = 4×10⁻⁵ × 43.6 × 10⁹ =
  1.744×10⁶, λ and τ cited from 0659) = **0.272 B/body → 0.272 GB ≈ 3.4%** of the
  machine. Same shipped `Calendar` code; only the capacity policy differs.

*Occupancy (instrument: `crates/universe/examples/schedcensus.rs` on the nladder
driver — `plane_extra`, `frame_to`, 12 ms budget, rtf 1000; a print-only
`sched_census` getter is the run's only engine edit, disclosed in `work/patch.diff`):*
- K = 10⁴ (10,028 bodies, 25 s wall) and K = 3×10⁴ (30,028, 12 s): **`ship_ticks` =
  1.000–1.002×N and `waiting` = 1.000–1.002×N at every census** (identical counts,
  e.g. 30,043/30,043 — the same next-tick fact in two whole-population containers);
  `child_ticks` = 311–333 and `prunable` = 105–108 **absolute** (the locals' scale,
  N-independent); `queue` = 5–6 (the always-queued few); `pos` = N.
- Live slot content ≈ (1.002+1.002)×28 + 16 ≈ **72.5 B/body** — but RSS pays capacity
  (156), and at 10⁹ both are ruinous (72.5 GB vs 156 GB) beside the 0.27 GB floor-arm.
- Kicks fire throughout (≈3,000/census window), so the census is steady state, not a
  cold start; waiting never drains (belt step ~27.6k game-s ≫ frame).

*CPU neighbour (lens blind spot — the apparatus is bytes, not CPU):* shipped heap ops
at n = 10⁶: fill 30.8 ns/slot, update 37.6 ns/slot, full drain 364 ns/pop — ≥120×
under the fired item's 44.7–82.5 µs (3aec), so no cost is being moved onto CPU by
deleting bytes here.

*Composition hole (grep-checked):* `budget-1e9.md`'s memory terms are "build
2,348–2,464 B/body; wired store 1.7–2.4 B/live-body [07b4]" — the wired row is a
store-only number; no page prices the scheduler's bytes (the only queue-byte entries
in the record are 6a0e's single-calendar 16→8 B scan and 25ce's cursor design; the
calendar page's own refuted line already says the *queue* "closes at ≤ MB of cursors"
— one queue, not the five-container apparatus). HANDOFF's memory identity ("bodies ×
bits + live bodies × ~1.3 KB") carries no scheduler term. The scheduler's state is
schedule-only by the engine's own contract: universe.rs's header ("The queue's own
order … is only a schedule: nothing it breaks a tie by reaches an outcome"),
observe.rs:8–9 ("deadlines … never an outcome"), and 9c67/d65c's digest-indifference
proof for the position cache.

## Predictions

`predictions.md` was written before the census. **P1, P2, P3, P6, P7 held** (two
whole-population containers; queue sparse; heap ops ns-scale; the ×574 flip).
**P4 and P5 failed**: `child_ticks` is the Home/Moon locals (~331 absolute), not the
belt, and `prunable` holds ~105–108 slots, not →N — both are locals-scale, which
*strengthens* the headline (the whole-population term is exactly the two redundant
containers) and is reported as failed. Kill criterion (P2 and P4 both failing) did
not fire.

## What would make it wrong

- The wired 10⁹ plan sizing the calendars by the live population (nothing in the
  record or code says so: universe.rs:481–490 sizes at `body_cap`; if the integrator's
  wiring already assumes live-sized calendars, the 156 collapses to 0.27 GB and the
  finding becomes a bookkeeping note).
- A belt at 10⁹ living entirely in `shipmem` and never entering `Universe` bodies —
  but then the wake problem is exactly 25ce's cursors and my capacity claim applies to
  whatever `body_cap` is; today the belt demonstrably enters the calendars (census).
- The census is coast-only, one scene family (`plane_extra`), rtf 1000, x86: under
  burn, a kick wave could transiently drain `waiting` (the always-queued rule keeps
  `queue` small, so capacity — the number the composition uses — is unaffected).

**Cost of adoption:** the capacity flip is a sizing-policy change (allocate by live
cap with growth; the promotion machinery already exists); the container deletion is
25ce's cursor design plus re-deriving `rekey`'s wake walk; `waiting`'s duplication of
`ship_ticks` is a separate candidate (one key-range read replaces it) that this run
names but does not build.

**Fit with PRINCIPLES.** #24 "The memory floor is information … why do you need so
many bytes per entity?" — the next-due word is already carried in the compact row
(calendar page, od 4: drift 6×10⁻⁵/fire), so the non-due body's scheduler floor is
~0 B; #17 "the best part is no part"; #14 owns the component itself (the deadline
queue IS the no-tick scheduler — required; its per-body form is not); #13 is not at
stake (schedule state, no outcome channel).

**The lens.** First-principles-by-component sees bytes and floors; it may miss that
the integrator's cursor design (25ce) already answers the 10⁹ form — this run's
contribution is the shipped-code measurement, the two-container redundancy, and the
missing ledger row, not a new design. A dynamics lens would fly the burn arm.
