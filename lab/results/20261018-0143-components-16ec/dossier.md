# Dossier — the boundary's key-range fast path, flown

## Claim

The clock path's boundary certificates are decidable at O(1) from the tube's own key — a
bound cycle's radius never leaves `[periapsis, apoapsis]` widened by the readout's slack —
so the no-op boundary's readout walk is deleted **exactly**: on the belt (the 10⁹
population) 100.0% of boundaries skip at 202 ns against 4,077 ns shipped (20.3×), with the
canonical digest bit-identical at the same cut on every coast arm flown — and the burn arm,
flown held-out, diverges (the kill criterion fired; mechanism unresolved in this window).

## Bottleneck

The board's belt stream: 2 events per body per interval (kick + boundary), the boundary half
measured by components-3570 as "27.8% of the kick+boundary resolver CPU buys 0 bits"
(99.88% no news). This run is 3570's named gold experiment ("the kick-time key-range test
flown"), taken as a **digest-neutral deletion instead of a rescheduling**: the boundary keeps
its tick and its anchor write; only the provably certificate-free readout walk is deleted.

**Requirement (PRINCIPLES):** "Compute only surprises … Nothing is evolved that can be
derived when looked at" (3) and "no work for no reason, so no ticks … we only care about
changes" (14): a boundary whose two certificates (surface, leave) are decidable from the
tube's key alone is work for no reason.

**Floor:** the no-op boundary's output is one anchor write; its input need is the range
test — two Scalar reads off the binding (key already in the `Arc<Entry>`), one divide, one
unit conversion, one residual-norm add, two compares: O(10 ns). Shipped: 4,077 ns mean
(census, this box). **Idiot index ≈ 400×** on the clock path; after the fast path, 202 ns
(census timer and atomics included; the test itself is ~tens of ns) — within ~10× of the
floor, the residue being the census instrument and the still-scheduled event.

## Evidence (Linux/x86, orders of magnitude; every number from `regen.sh`)

**The bound is exact (`bound_probe`, `work/probe.txt`).** 1,200 bound-cycle bindings built
the way the engine builds them (exact doll-unit states off compiled cycles via the same
`cartesian`-after-`to_doll` readout as `decode`, perturbed up to 2²⁰ velocity quanta so the
fit carries residuals; periapsis 2⁴–2²⁰ M, e to 0.99, unit mantissas 1 and 1.5), swept over
three full cycles each (96 samples + turning points): **worst relative excursion beyond the
widened range 0.000e0** — the readout radius never left `[periapsis, apoapsis] ⊕ (|res|₁ +
4 quanta)`. 4 unbound states compiled to passages and were all refused (`None`), the
conservative direction. The containment makes skip-safety immediate: skip fires only when
the whole widened range sits strictly inside `(surface, leave)`, and equality at either end
refuses (matching the shipped `<`/`>` senses).

**The flights (`nladder 10000 … 60 1800`, canonical cut pinned at 1.2×10¹⁰ ticks via
`ES_LIMIT`; two stability controls first — unpinned cuts drift with load and their digests
are incomparable, which is why the cut is pinned):**

| arm | digest (16 hex) | clock boundaries | fast | ns/event | deaths |
|---|---|---|---|---|---|
| coast ctl | a725217f1dcd9f2a | 19,423 | 0 | 4,077 | 0 |
| coast ctl (rerun) | a725217f1dcd9f2a | 19,423 | 0 | 4,098 | 0 |
| coast fast | **a725217f1dcd9f2a** | 19,423 | **19,423 (100.0%)** | **202** | 0 |
| seed-7 ctl | c57f15a04e8f657c | 19,426 | 0 | 4,228 | 0 |
| seed-7 fast | **c57f15a04e8f657c** | 19,426 | **19,426 (100.0%)** | **219** | 0 |
| burn ctl | 08b6399c4898a671 | 19,761 | 0 | 4,368 | 0 |
| burn fast | **0096b634a7c18339 — DIVERGES** | 19,761 | 19,423; 338 passage | 9,319 (slow) / 202 (fast) | 0 |

Coast: digest bit-identical across control, rerun and fast arm, at 100.0% skip, 20.3× per
event (79.2 ms → 3.9 ms of resolver CPU on the clock-boundary term). Seed 7 (held-out):
identical. Burn (held-out): **the digest diverges and the event stream with it** (by the
cut: kicks 107,681 vs 107,771, boundaries 105,402 vs 105,422; refusals 0/0, deaths 0/0 — so
neither the refusal ledger nor a missed kill is the channel; 338 boundaries took the passage
branch and were read out in both arms). The mechanism is unidentified in this window; the
named next probe is an item-tick bisect of the two event streams at the first diverging
kick.

**A decomposition correction to 3570's census.** On this flight the total boundary mass is
189,996–190,000 items, of which only 19,423 (10.2%) ride the clock path — the belt; the
other ~84.6% is the WH-split `boundary()` of the locals and planets (~330 bodies,
N-independent, with the dear per-event cost: 3570's shared-box p50 25.2 µs mixes both
paths). The clock-path boundary — the term that scales to 10⁹ — measures **4.1–4.4 µs mean
here, not 25 µs**; the fast path takes it to 0.20 µs. The WH path's no-op boundary is a
separate question (its bodies are edge-capped by `next_exit`, not certificate-checked
only) and is untouched by this test.

**10⁹ ledger arithmetic (this box, order of magnitude):** belt boundaries at 10⁹ bodies × 1
per 28,141 game-s interval × 4.1 µs ≈ 0.15 cores continuous; with the fast path ≈ 0.007
cores. The deletion is exact, so it composes with any cadence split (the boundary can still
be unscheduled later — the stronger 3570 form, which moves the digest by design).

## Predictions

Written before the flights (`predictions.md`). P1 held on coast and seed-7, **failed on the
burn arm** (digest divergence, exactly the held-out case P5 named: "any digest divergence
between arms at the same cut … kills the fast path as built"). P2 held and overshot (100.0%
≥ 99%; zero slow-cycle, zero passage on coast). P3 held (202 ns < 1 µs; 20.3× per event;
the belt's clock-boundary CPU term −95%). P4 held (zero excursions; passages refused). P5's
burn failure fires: **the fast path as built is not adoptable on thrusting populations
until the divergence is understood**; on the coasting belt (the 10⁹ bulk) it is exact.

## What would make it wrong

The containment slack (component rounding √2, the turn's "two quanta", the residual's L1)
is my reading of `bind.rs`/`lorentz.rs`; the probe's dense sweeps found zero excursion, but
a pathologically large residual (near the 65-bit i128 bound) is not swept — the belt's
kick-minted residuals are thousands of quanta at most. The burn divergence is unexplained:
if it turns out the fast arm *correctly* skipped a boundary whose shipped readout silently
corrupted state, the shipped path is the bug, not the fast path; if the fast arm skipped a
boundary that should have fired, the bound's slack term is wrong somewhere — the bisect
decides. The digest comparison itself relies on the pinned cut (`ES_LIMIT`); unpinned
flights are incomparable (measured: two controls at 40 s diverged by cut alone).

## Cost of adopting, fit with PRINCIPLES

One flag-gated branch in `boundary_clock` (`step.rs`, +70 lines with census; the decision
is ~10 lines) plus a Linux footprint shim and print-only instrumentation in `nladder` —
zero cost off (the flag path is one atomic load), zero bytes of new state (the range is
recomputed from the binding each time; no cache). Fit: PRINCIPLES 1 (cheapest compute is
compute not done), 3 and 14 as quoted above; it deletes rather than adds (the alternative
3570 form — unscheduling — is strictly stronger but moves the digest by design and needs
the B-gate re-freeze; this form needs none, on the coasting belt). Not adoptable while the
burn divergence stands.

## The lens

First principles, one component (the boundary event). What the lens may have made me miss:
I scoped to the clock path (the 10⁹ bulk) and measured the WH path only as a decomposition
line — its no-op boundary mass at plane scale is 8× the clock path's and remains unprobed;
and I treated the burn divergence as out of budget rather than chasing the bisect, which a
dynamics lens would have run first. The census timer (202 ns fast) includes its own
overhead — the true test cost is tens of ns.
