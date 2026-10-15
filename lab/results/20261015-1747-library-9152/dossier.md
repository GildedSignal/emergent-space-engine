# Dossier — 20261015-1747-library-9152 (library lens)

## Claim

Julien's library, read against the nladder record, orders the ladder's open decisions — delete the
scan's read before caching it, optimize the mint factory rather than the retention warehouse, gate
caches on maximum reuse distance, ship the ruin fence by damage — and the shipped record class is
measured at **2,333 B/body marginal, flat in N** (2.33 TB extrapolated at 10⁹ against the 8 GB
machine; **292× over** the ≤ 8 B/body budget), so only the zero-marginal-cost program class reaches
10⁹.

## Bottleneck

Board's first: **bodies in the flyable engine, 28 against 10⁹** (nladder). The page's live fight —
the retention-cap family (five days of arms: FIFO ring, ONCE admission, knee pricing, defaults) —
ended in "no bounded cap serves burn; price the re-mints or delete the reads." This run does not add
a cap arm; it prices the class the ladder is climbing with (shipped whole-process marginal cost) and
orders the next decisions from practitioner structures in Julien's own library (lessons.md).

## Evidence

Machine: GitHub Linux runner, 8 vCPU, 15 GB, load 0.71 (idle), 2 GB in use. Shipped code + this
run's one tree edit (nladder.rs `footprint()` ported to Linux: `/proc/self/status` VmRSS/VmHWM; the
macOS branch unchanged — the example was macOS-only before). Flights: `nladder N coast 10 100 12`,
fresh process per rung (each ≤ 9 s wall; `work/flights.txt`):

| bodies | peak MB (build) | B/body (end) | view ms/gather |
|---|---|---|---|
| 28 | 4 | — | 0.5 |
| 1,028 | 6 | 3,523 | 9.1 |
| 10,028 | 27 | 2,459 | 93.2 |
| 100,028 | 237 | 2,348 | 937.1 |

- **Marginal cost: 2,333 B/body at 10³→10⁴ and 10⁴→10⁵** (build-peak slope; run-to-run 237 vs 238
  MB, ~1%). Flat in N — the record class does not amortize.
- Extrapolation: 2,333 B × 10⁹ = **2.33 TB**; the 8 GB machine allows < 8 B/body all-in:
  **292× over budget**. Even the seam's 962 B standing store (0.96 TB) and the knots alone
  (672 B → 0.67 TB) do not fit; the birth program (0.126 bits/body, 98bc) plus a bounded live set
  does, with ~10⁵ live bodies at the measured 2.3 kB costing ~0.25 GB.
- The 2.3 kB is 2.4× the seam's standing store and 3.5× the knots: the machinery around the record
  (bindings, catalogue entries, allocator slack) costs more than the record's own knots — deleting
  *machinery*, not compressing knots, is where bytes are.
- Incidental, and it prices an open direction: **the view gather is linear, 9.38 µs/body** (0.5 →
  9.1 → 93 → 937 ms): 9.4 s per gather at 10⁶, 2.6 h at 10⁹. Confirms the view page's finding (the
  membership rescan must become a birth/death feed) with a shipped-code slope.
- Reproduce: `sh regen.sh` (build 15 s + 4 flights ≈ 25 s + parse). Quote base: `work/readwise.json`
  (770 docs, 4,580 highlights, fetched via the export API this run).

## Predictions

`predictions.md`, written before the flights. **P1 wrong**: predicted 300–1000 B/body, measured
2,333 — the Fermi priced knots + records but not the surrounding machinery; reported as wrong, no
re-fit. **P2 direction right, magnitude wrong**: predicted 0.3–1 TB and 40–125× over budget;
measured 2.33 TB and 292× — the claim is stronger than registered. **P3 held**: slope flat in N
(2,333 at both intervals, against the >3× drop that would have weakened the class-change claim).
No kill criterion fired (marginal ≫ 8 B/body).

## What would make it wrong

- VmHWM under-reports (swapped/compressed pages) — but the box was idle (13.9 GB available) and the
  end-footprint B/body column agrees with the peak slope.
- Coast-only: burn compiles more (passage/plunge windows), so burn's marginal cost is ≥ coast's —
  the extrapolation is conservative, not optimistic.
- The 10⁹ population being belt-like (it is, by design: `plane_extra` puts the mass in the belt).
- The five lessons are analogies, not physics: they stand only while their named decisions are open;
  when the neighbourhood read deletes the capture and the mint stays exact, lessons 1–3 collapse
  into "done" — which is their success condition, not a refutation.

## Cost of adoption

Zero code for lessons 1, 4, 5 (ordering + gate instrumentation + a rung metric: the marginal form is
two flights' difference, `work/marginal.py`). Lesson 2's test is the page's own named gold step (the
two-line demote-passages variant, one flight + one mixed-peri comet stream). Lesson 3's test is one
arm (retention-deleted coast) on the existing patch line.

## Fit with PRINCIPLES

"The cheapest compute is compute not done. Delete before optimizing" (#1 — the cap family
accelerated a read whose requirement was unexamined); "Store the generator, not the generated" (#6 —
2.3 kB/body is generated state; the program class is the generator); "not making mistakes matters
more than doing things efficiently, don't multiply by zero" (#25 — the fence ships by damage, and no
default ships whose knee is 1.4 TB); "we want to guess in a way that is perfect how the simulation
will run to bypass it" (bottleneck 0 — the mint factory). The record itself converged here first:
0619/f55d's "price or delete, no cap ships" is lesson 1's measured form.

## The lens

The library has no systems-programming text (no Denning, no buffer-pool or scan-resistance
literature, no Forth); the structures those practitioners solved with named algorithms are mapped
here through Musk/Feynman/Taleb/Naval/Waitzkin quotes instead — the mapping orders decisions, it
adds no physics. Readwise (770 docs) ≠ the full shelf (611 goodreads rows): books read without
highlights are invisible to this method, and every quote not in `work/readwise.json` would have had
to be marked UNVERIFIED (none were needed). Blind spot of the run: coast-only flights at N ≤ 10⁵ on
a shared box — orders of magnitude only; the integrator re-measures on the M1.
