# Dossier — 20261020-1002-fermi-8994 (fermi)

**Claim.** The allocation wave's bytes are marginal, not base — attributed inside the fired
item's own scope, 91% of the naive per-kick traffic is item work — and the "naive vs marginal"
gap f623 could not resolve is a third thing: the player item's doll-proportional scratch
(490 B/body per player item, doubling chains to one ~352-B entry per body), which no per-kick
constant can price.

**Bottleneck.** budget-1e9 od 6 (the checker's named deciding instrument: "attribute bytes
inside the fired item's own scope, not through budget-coupled windows; log scratch sizes above
2 KiB per call"). Decides whether pooling is machine-mandated and which scratch it must pool.
Gain: the 10⁹ bandwidth row's marginal constant measured directly (11.35 KB/kick coast, not the
OLS 1.4–3.3), and the pooling lever re-aimed from a generic frame-scratch pool at the player
item's one belt-sized Vec.

**Instrument.** `alloc_scope` (work/patch.diff): an env-gated TLS marker in `advance()`
around each top-level item (`ES_ALLOC_SCOPE=1`; outermost class wins, nested items stay inside),
plus a counting `GlobalAlloc` (`crates/universe/examples/alloc_scope.rs`) that attributes every
alloc/free/realloc (old and new sizes) to the scope it happens in — 0 = frame base, 3 = ship
item, 4 = player item, 5 = fleet/hand-out — with a power-of-two size census per scope and a
per-frame CSV. Flight otherwise shipped (`nladder` args verbatim: seed 1, rtf 2000, 12 ms).
Off = shipped bits (env gate; the marker early-returns).

**Evidence** (this box, load ~0.3, all runs ≤ 35 s wall, peak RSS 87 MB ≪ 2 GB; x86 → M1 orders
only — bytes/kick is schedule-dependent, not machine-dependent):

Anchors reproduced: naive coast **12.42 KB/kick** (f623: 12.3–12.7), naive burn **21.33**
(f623's checker: 21.5), to <2%. Neutrality: instrumented kicks 12,353/12,353/12,353 on a fixed
5-s arm vs shipped `nladder` 12,321/12,353/12,353 — inside the shipped rerun spread.

| arm | game-s | kicks | items (ship/player) | item-scope KB/kick | = % of naive | base KB/game-s |
|---|---|---|---|---|---|---|
| D1 coast K=10⁴ | 57,338 | 108,383 | 42,422 / 219 | **11.35** | **91.4%** | 2.03 |
| D2 burn K=10⁴ | 56,297 | 105,911 | 152,113 / 1,646 | **15.19** | **71.2%** | 11.53 |
| D3 coast K=3×10⁴ | 51,726 | 139,795 | 92,978 / 136 | **9.12** | **91.8%** | 2.20 |

- **P1 (the fork) fired its kill bar**: item-scope ≥ 8 KB on D1 — f623's OLS window marginal
  (1.4–3.3 KB/kick) is refuted as an *attribution*; the naive reading was ~right all along. The
  base (frame scope) is the minority: 8.6% of bytes coast, 28.8% burn.
- **The item term is two laws, not one.** D1: ship scope 156.6 MB / 42,422 items = **3.7 KB per
  ship item** (~1.6 KB/kick at 2.27 kicks/item) — the stream's own marginal, scaling with kicks.
  Player scope: 1,073.6 MB / 219 items = **4.90 MB per player item = 490 B per body** of the
  10,028-body doll — 87% of all item traffic from 0.5% of the items, scaling with the doll, not
  with kicks. In burn the player scratch grows by **doubling realloc chains** (56 KiB → 3.5 MiB,
  129 full chains; census means exactly 57,344 / 114,688 / 229,376 / 458,752 / 917,504 /
  1,835,008 / 3,670,016 B) ending at **3,670,016 B = one ~352–366 B entry per body** — the
  root-doll read set cc9d named for the freeze, now priced in allocator bytes. A chain costs ~2×
  its final size in realloc traffic; `with_capacity` halves the player term and deletes its
  realloc calls.
- **The arrival waves are item-carried** (per-frame CSV, contiguous hot clusters): D1
  [356,426]: item 2.2× ebb, base 0.8×; D2 [401,431]: item 8.0×, base 0.5×; D3's wave [858,908]:
  base 1.2×; item KB/kick at the waves 2.2–13.3 (ebb 11.7–18.8: arrival kicks are *cheap* ship
  items; the ebb's sparse kicks ride the player's buffers). The one base-carried wave is the
  burn's late tail [1651,1720]: base 5.4× ebb, item 1.4× — the held-scan era, 7b6f's TTL-fence
  finding now confirmed in bytes.
- **>2 KiB census** (the checker's ask): coast — item scope's calls sit at exact multiples
  (means 2,549 / 5,637 / 11,267 / 22,528 / 57,344 B: arrays of the {352, 384, 704} heap
  family), 55% of all bytes; base's >2 KiB is 2.9% of traffic but holds the only ≥256 KiB calls
  (16 of them, 20.3 MB, build-growth leftovers). Burn adds 51k fresh base blocks at 2–32 KiB
  (means 2,944 / 5,919 / 11,679 / 22,566 / 38,467 B) = the burn base's 5.7× rise.
- **10⁹ composition** (rtf 100; λ = 4 / 8.4 ×10⁻⁵ → 4 / 8.4 ×10⁶ events/wall-s): the stream's
  own marginal (ship term, 1.6 KB/kick) = **6.4 / 13.4 GB/s = 11% / 22% of 60 GB/s — closes,
  no pooling subsystem is machine-mandated for the stream** (f623's sentence stands for the
  stream, now measured at the scope instead of an OLS slope). The mixture (11.35 KB/kick) =
  45.4 / 95.3 GB/s = 76% / 159% — but its excess is the player item's 490 B/body term: at 10⁹
  one player item allocates ~490 GB (8 s of bus) — O(doll), cc9d's unclosable root-doll row,
  not a per-kick pooling question. Pooling the player buffer buys ~2× there; the fix is the
  read set.

**Predictions** (predictions.md, written after two disclosed pre-wave calibrations, before D1–D3):
P1 held (kill bar fired), P2 held (87% ≥ 50%; realloc 80% ≥ 60%; base >2 KiB 2.9% ≤ 25%), P4
held (burn/coast 1.34 ∈ [1,2]), P5 held on its number (76% ∈ [53,133]) and inverted on its
reading (the closable term is 11%, not 76% — re-attributed), P6 held (D3/D1 = 0.80 ∈
[0.7,1.5]). P3 half-held: the wave is item-carried (base 0.5–1.2× at every arrival wave, the
letter's essence) but D1's rise is 2.2×, not ≥3× (the rtf-2000 ebb is itself item-heavy);
D2's 8× held the letter. Neither kill criterion fired: no arm moved counters with the gate off
(unrunnable by construction — the example asserts the env — neutrality shown instead by rerun
spread), and freed < bytes only through realloc's hidden old-block frees (disclosed here;
traffic = alloc + realloc new sizes).

**What would make it wrong.** The scope marker brackets the top-level item only; anything the
frame does between items (rekey, take_due, drain_scans, deferred requeue) reads as base by
definition — if the "player item" traffic were actually minted by drain_scans answering held
scans (idle time, outside items), the 490 B/body term moves from the player item to the base
without changing the totals. The census cannot tell which function inside the player's item
owns the 352-B-entry Vec (pull_ships vs the neighbourhood scan); only a backtrace instrument
would. One seed, one box, K ≤ 3×10⁴: the 490 B/body and 3.7 KB/ship-item constants are
orders-of-magnitude at 10⁹, and both inherit the schedule elasticity of every wall-budget
flight (±few % here, more under load).

**Cost of adopting.** Nothing to adopt in the engine: the row closes with measured constants.
The named cheap fix (one line of intent, not built here): `with_capacity(doll)` for the
player-scratch Vec — halves the player term's traffic and deletes ~0.3–1.2 M realloc calls per
flight; the real fix is cc9d's read-set row. Fit with PRINCIPLES: "the best part is no part"
(measured, no pooling subsystem is mandated for the stream); "compute only surprises" (the
steady ebb, not the wave, carries 90% of the traffic — the stream is always-on marginal work).

**The lens.** The Fermi estimate that the OLS slope was trustworthy (a rate × count argument)
was itself the error the instrument killed: windows cannot separate two terms with different
scaling (per-kick vs per-doll) that share a frame budget. What the lens may have missed: the
view's gather and the dashboard run in this same process (base scope, one cold gather at
flight end — its ~30 µs/body read is outside the census window by construction, disclosed).
