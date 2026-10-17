# Dossier — 20261017-1240-quant-ceb2 (Quant)

**Claim.** The kick's byte bill is measured for the first time — 12.2–18.8 KB of allocation
traffic and 16.5–16.7 allocs per fired kick on shipped code — and it acquits the von-Neumann
bottleneck for the event path: the bandwidth floor is 0.18–1.1 µs/event, 45–900× under the
kick's compute bill (≤1% of the shipped kick, 2–11% of a ~10 µs post-Carlson kick), so **the
event stream is compute-bound at every N; at 10⁹ the memory wall is capacity (bytes stored),
never bandwidth (bytes moved)**. Second, the readout's cold-cache tax (+3.0–3.9 µs, 103–167%
of its hot 2.9–3.3 µs) is **~75–85% shared footprint (code/statics), only 0.5–1.6 µs the
per-key knot table** — the assumed culprit is innocent, the record's in-situ read prices
(~4 µs at 10⁵, 5ade) are already the cold-data prices, and no table-layout lever hides there.

**Bottleneck.** The board's kick program (75–160 µs vs a "~50 ns floor"; a765 corrected the
floor to ~6 µs arithmetic). PRINCIPLES 17 ("deeply aware of von-neumann bottleneck") had
never been priced on the event path: every timing in the record is cache-hot, and nobody had
counted bytes per event. If bytes/event × event rate could reach the M1's ~68 GB/s roof, the
lever ranking would invert (layout/compression above arithmetic). It cannot, by ~2 orders.

**Evidence** (Linux/x86 runner, 8 vCPU, single thread; alloc counts bit-identical across
three executions; wall numbers wobble ±25% with box load; orders of magnitude only, per the
lab rules):

1. **Sizes and write bill (exact, allocator-counted).** `Knot` = 88 B, `OrbitShape` 224,
   `Orbit` 200. `Orbit::compile` at p = 1.2×10⁹ M: e 0.01 → 6 knots (528 B table), e 0.90 →
   69 (6.1 KB), e 0.99 → 124 (10.9 KB); **allocation traffic per compile 1.4–24.5 KB — the
   Vec-growth churn writes ~2.2× the table it keeps** (e ≥ 0.90: 24.5 KB allocated for a
   6–10.9 KB table).
2. **The wave (shipped `plane_extra` flight through the first-kick wave, counting allocator
   live).** N=3000: 34,537 kicks, **577,535 allocs / 650,057,850 bytes = 16.7 allocs and
   18,822 B per kick** (0.11–0.14 GB/s of flight). Held-out N=10000: 41,537 kicks, **16.5
   allocs and 12,205 B per kick** — flat in N; the byte difference is mix (N=3000 is
   locals-heavy, 11.5 kicks/body vs 4.2, and locals carry bigger tables).
3. **Hot/cold micro (interleaved 3×, evictor = 128 MB every-64 B pass at a measured 14.7–17.6
   GB/s, subtraction control timed; the first version's evictor was CSE'd by LLVM and its
   numbers are excluded; two full runs).** Read `signed_state`: hot 2.9–3.3 µs at every e
   (e 0.01→0.99), cold 6.0–7.2 µs — **delta +3.0–3.9 µs, flat in knots (6→124)**. Split arm
   (evict, warm the code path once on another key, then time): read drops to 3.5–4.8 µs →
   **data-only delta 0.5–1.6 µs (0.2–0.6 µs at p=7); the rest, ~2.4–2.9 µs, is the shared
   footprint** (code + tiny statics: `W`/`X` are 2 elements; `EDGE`/`ATAN` 17×16 B — the
   quadrature tables total under 1 KB). Compile: hot 3.6–3.7 / 11.2–12.2 / 22.5–25.0 /
   46.8–52.2 / 85.0–92.8 µs (e 0.01→0.99, the record's e-monotone band), cold delta
   +3.4–7.3 µs, 109%→5% of hot as compute grows — the same shared tax, amortized by compute.
4. **Roofline.** Machine balance: ~17 GB/s per core measured here (stream calibration);
   M1 ≈ 68 GB/s / 4 P-cores. Event needs: 12.2–18.8 KB moved per 50–165 µs of compute =
   0.07–0.5 GB/s per core — **a bandwidth floor of 0.18–1.1 µs/event, 45–900× under the
   compute bill. Bandwidth binds only if per-event compute falls below ~0.4 µs, below
   a765's ~6 µs arithmetic floor — unreachable on this representation.** The record's
   bandwidth-shaped walls are elsewhere: the per-body walks (calendar's rescans, 21.9–23.2
   ns/body, latency-bound random access) — there, not in the event path, is where PRINCIPLES
   17 bites.

**Predictions** (predictions.md, written after the sizes pilot, before micro/wave):
prediction 1 (read cold delta < 20% of hot) **killed as written** — the kill rule (≥50%)
fired at every key (103–167%); the diagnosis is the mechanism above: the tax exists but rides
the shared footprint, which stays warm in-situ (the record's prices were already paying the
data part — 5ade's ~4 µs in-situ reads = my hot + data-only delta). Prediction 2 (compile
delta ≤ 5%) killed at low e (109% at e 0.01), held at e ≥ 0.6 (23%→5%) — same shared tax.
Prediction 3 held: 15–35 KB/kick predicted, 12.2–18.8 measured, flat in N, flight under
0.5 GB/s. Prediction 4 held (the roofline acquittal).

**What would make it wrong.** The counting allocator sees allocation traffic, not every read
touch: reads of *standing* tables (the 98–224 reads per generation, 4ea0) are not counted —
bounded above by the split arm's data-only delta (~0.5–1.6 µs/read) and by the in-situ
reconciliation with 5ade. x86, not the M1 (orders of magnitude; the integrator re-measures).
If a future representation cut per-event compute below ~0.4 µs, or batched events lost the
compute padding, the roofline flips — the number to watch is bytes/event ÷ ns/event vs
17 GB/s/core.

**Cost of adopting: none** (measurement only; the example `bwfloor.rs` is print-only, engine
untouched, flights unmodified). **Fit with PRINCIPLES:** "we need to be deeply aware of
von-neumann bottleneck and memory" (17) — answered where it bites; "Less is more" (1) — the
churn (16.7 allocs/kick, 2.2× the table in Vec growth) and any table-layout rework are now
priced as non-levers on the kick's wall (≤0.5–1.1 µs of 75–160 µs), so the deletion budget
stays on the compute program (kick-jet open 1, the Carlson wiring).

**The lens (what it may have missed).** One box, one thread, no hardware counters
(paranoid=4): the hot/cold split replaces cachegrind, and the shared-footprint attribution
(code vs statics vs allocator) is by elimination, not by counter. The wave arm flew the
belt/locals mix only, not the strong-e plane population; the 12.2–18.8 KB/kick range is that
mix's range. The player is absent (no view, no scan) — d959's census says that half is flat
in N, so the roofline verdict stands, but the scan's own cold-cost was not re-measured here.

## Reproduce

`regen.sh` (≈1 min): builds and runs `bwfloor sizes`, `bwfloor micro`, `bwfloor wave 3000
20000`, `bwfloor wave 10000 20000` on the patched tree (the patch adds only the example),
then prints the roofline arithmetic.
