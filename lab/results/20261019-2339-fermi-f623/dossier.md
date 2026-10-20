# Dossier — 20261019-2339-fermi-f623

**Claim.** The 10⁹ ledger's two never-priced floors — the mint stream's allocator throughput and
memory-bandwidth traffic — are now measured per fired kick on the shipped ladder, and both CLOSE:
allocator 0.4–1.7 cores and marginal byte traffic 6–28 GB/s (11–48% of the M1's ~60 GB/s) at the
shipped cadence, 3–6% after split8; **no machine floor forces the kick-mint deletion beyond the
record's memory-ratchet + item-cost case**, and the per-kick churn law is measured: ~18 allocs +
~16 frees per kick (naive), of which only ~11–13 allocs and **1.4–3.3 KB ride the marginal kick**
— the rest is an N-flat flight base, 64% of it in >2 KB scratch — with a per-kick heap-call family
{88, 240, 304, 352, 384², 704, 832} B that is NOT 9edc's mint anatomy {192, 208, 288}.

**Bottleneck.** budget-1e9's composition (3aec + checkers) closes CPU only with split8 + Carlson;
PRINCIPLES #12 names the allocator; the ledger has no allocator or bandwidth row. Expected gain:
none in cores (the rows close) — the value is a measured kill: nobody should build a pooling
subsystem or delete the mint "because the machine demands it". Cost of adopting: zero (no engine
code changed; print-only probe, shipped `nladder` scene untouched).

**Evidence** (Linux/x86 8 vCPU, load 0.31, orders of magnitude per the lab rule; exact commands in
`regen.sh`, ~2 min):

- Instrument: `crates/universe/examples/alloc_probe.rs` — new binary, a counting `GlobalAlloc`
  wrapping `System` (the engine sets none) + per-wall-second probe lines next to the engine's own
  kick deltas + an exact size histogram to 2 KiB. Shipped code otherwise untouched (the patch is
  the new example only).
- K = 10⁴ (10,028 bodies) coast rtf 2000, 48,803 game-s, 96,108 kicks, 184,628 events:
  naive **17.6 allocs + 16.5 frees + 4.4 reallocs per kick, 12.66 KB allocated and 12.11 KB freed
  per kick, net live +53 MB = 0.55 KB/kick retained** (the ratchet; 88e9's 2.1 KB/binding RSS is
  the same law with allocator slack). Window OLS (25 windows, kicks as regressor): **marginal
  3.32 KB/kick and 12.9 allocs/kick; base churn 18 KB/game-s**.
- K = 3×10⁴ (30,028) coast, 36,404 gs, 87,380 kicks: naive 19.3/15.8 calls, 12.28 KB; marginal
  **1.40 KB/kick**, base 26 KB/gs — **N-flat within ~20% (P5 held)**, so the per-kick constants
  carry to the priced reaches.
- Histogram (10⁴): family **{88, 240, 304, 352, 384, 704, 832} B at 8.7 calls/kick total = 76% of
  ≤2 KiB bytes** (10.1 calls/kick, 79% at 3×10⁴); **>2 KiB scratch is 64% of ALL allocated bytes**
  at 0.56 calls/kick ≈ 15 KB average; 192/208/288 are absent from the top 16 — the mint's heap
  calls are not its struct sizes (9edc's anatomy is `size_of`, the heap path allocates other cuts).
- Allocator floor (`bench_malloc.rs`, this box, glibc tcache): **11.6 ns per alloc+touch+free pair
  at 192–288 B = 86 M pairs/s/core** (12.2 ns at 48 B, 24.9 ns at 4 KiB).
- Composition at 10⁹, rtf 100, λ ∈ {4×10⁻⁵, 8.4×10⁻⁵} (0659/3aec band; f80a's 8.4×10⁻⁵ at 3×10⁴):
  **allocator 0.60–1.25 cores marginal (0.81–1.71 naive)**; **byte traffic 13.6–28.5 GB/s marginal
  = 23–48% of 60 GB/s (naive 52–109 GB/s = 86–181% in wave windows)**; split8 → 0.05–0.2 cores and
  1.7–3.6 GB/s (3–6%). The full after-lever table (every row cited) is `compose.py`'s output,
  `compose_out.txt`.

**Predictions** (`predictions.md`, written before any flight):
- P1 calls/kick ∈ [4,24]: **FAILED high** — 34 naive, ~26 marginal. The mint drags more call
  machinery than the anatomy suggests.
- P2 bytes/kick ∈ [0.8, 5] KB: **half-held** — marginal 1.4–3.3 KB holds; naive 12.3–12.7 KB
  fails, and my own kill criterion (>10 KB → investigate) fired on the naive reading: the
  investigation IS the result — the OLS split shows 64%+ of the churn is flight-base scratch,
  not per-kick mint.
- P3 ≥50% of bytes at {192,208,288}×{1,2}: **FAILED** — the family is real (76–79% of ≤2 KiB
  bytes) but the sizes are {88,240,304,352,384²,704,832}: 9edc's mint anatomy does not describe
  the heap calls. Prior art corrected, not overturned (the retained objects are still theirs).
- P4 allocator ≤2 cores (held: 0.4–1.7) and bandwidth ≤50% of 60 GB/s (**held on the marginal
  attribution 23–48%; failed on the naive wave-average 86–181%**). The decision half did NOT
  fire: no floor forces the mint deletion.
- P5 N-flat within 2×: **held** (within 20% on every constant).
- Bench anchor 20–100 ns/pair: **failed low** — 11.6 ns; the allocator floor is cheaper than
  assumed, which strengthens the closure.

**What would make it wrong.** The x86 glibc allocator is not the M1's (order-of-magnitude rule;
if the M1's malloc is ≥5× dearer under contention the allocator row reopens at 8 threads);
marginal-vs-naive attribution assumes the flight base is N-flat, checked only across two rungs
(10⁴, 3×10⁴) on one seed, coast only — a burn arm (the player's item, the wave) may shift bytes
into the marginal term; the >2 KiB scratch's 15 KB average is derived from total bytes minus the
binned histogram, not logged per call. Cost of adopting: none — it is a priced non-adoption (the
deletion case stays where 225d left it). Fit with PRINCIPLES: "the best part is no part" (#17) —
the cheapest pooling subsystem is the one nobody builds; and "Measure before claiming" (#10) —
the naive Fermi headline ("bandwidth forces the deletion") was measured into a narrower truth.

**The lens.** The Fermi estimate alone would have published the wrong headline: my pre-registered
bands were built on the retained-object anatomy and came out wrong on three of six predictions;
the window regression, not the estimate, found the base/marginal split. Missed by this lens: the
burn arm (the wave-window naive reading says the transient traffic is ~1× the whole machine's
bandwidth at the shipped cadence — cc9d's freeze and this traffic likely share the read set);
scratch-size logging above 2 KiB; more than two rungs and one seed.

## Reproduce

`./regen.sh` (≈2 min): builds the probe, runs the malloc bench, flies both arms, composes.
