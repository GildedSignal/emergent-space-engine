- **Claim:** The birth plan pass is not an irreducible exact search: 30% of it is the planets' exact states re-derived once per body, deleted digest-identically by a birth-only hoist (33→23 µs/body), and the bulk of the rest is the per-body clock derivation — measured from Julien's own library lessons, one of them flown.
- **Bottleneck:** The board's first: live bodies 28 against 10⁹. The birth rail's plan pass (404b: 32.5–33.5 µs/body, 76–78% of the 42–44 µs rail), interior unattributed — the wiki's open direction #1 ("irreducible exact search or deletable bookkeeping").

## Evidence (lab box, Linux/x86-4790, orders of magnitude)

The probe: `ES_BIRTH_SPLIT` counters around the start pass (`crates/universe/src/universe.rs`), `Ctx::secondaries`, `project`, `plan_terminal`; `ES_SEC_HOIST` a (doll, tick, except→normalised) memo armed only inside `Universe::start`, where no binding changes. Commands (each ≤ 60 s):

```
cargo build --release -p emergent-universe --example sec_probe
for n in 10000 100000; do for s in 1 7; do for h in 0 1; do
  ES_BIRTH_SPLIT=1 ES_SEC_HOIST=$h /home/glmlab/lab-target-2/release/examples/sec_probe $n $s
done; done; done
```
(Regeneration note: run.sh's patch capture returned an empty `work/patch.diff`, so the probe travels
inside `regen.sh` as `work/probe.patch` — applied, built, flown on the same 8-arm grid, tree restored.
Re-run: ~30 s, every number above regenerates: pass 33.6–34.1 µs/body, secondaries 30.3–30.5%,
hoist 22.8–23.8, terminal 0.05, project 15.6–16.1, `sec_calls` = n+28, 7 memo keys, digests identical.)

| n | seed | pass µs/body (hoist off) | secondaries µs/body | share | pass (hoist on) | digest |
|---|---|---|---|---|---|---|
| 10⁴ | 1 | 32.95 | 9.92 | 30.1% | 22.84 | identical |
| 10⁴ | 7 | 32.63 | 9.85 | 30.2% | 22.87 | identical |
| 10⁵ | 1 | 33.42 | 10.12 | 30.3% | 23.14 | identical |
| 10⁵ | 7 | 33.49 | 10.23 | 30.6% | 23.16 | identical |

- The pass reproduces 404b's 32.5–33.5 flat in N, seed-stable. `plan_terminal` (the bisection search) is 0.03 µs/body (0.1%). `project` incl. its secondaries read: 15.4–16.0 µs/body. `sec_calls` = n + 28 → exactly one secondaries read per body; hoisted, 7 distinct keys serve 10⁵ bodies.
- The planets are re-derived a **second** time per body through `ext::constants`' `source(ctx,j,t)` (crates/universe/src/ext.rs:153), not covered by the memo: the unattributed remainder (~17 µs) minus per-body clock math holds another ~10 µs of the same reads. One shared "planets at t" readout serving both paths is the named next rung.
- At 10⁹, the hoisted pass alone deletes ~10⁻⁵ s × 10⁹ ≈ 2.8 core-hours of the ~6 404b priced for the plan pass (order of magnitude, lab box).

## Predictions (predictions.md, written before the flight)

Held-out seed 7 and N=10⁵ were never tuned on. **Failed:** (1) secondaries >50% of replan — it is 30%; the biggest term is the clock derivation (`constants`+`project`). **Partially held:** (2) hoist <18 µs/body — got 22.8–23.2 (the `source` reread is a second path). **Held:** (3) terminal search <10% (0.1%); (4) one secondaries call per body exactly; (5) share flat in N and seed.

## What would make it wrong

The memo is exact only because no binding changes inside the birth loop (verified by code read and digest identity on 8 flights); a runtime version needs the apply-loop's invalidation. The remainder attribution (~17 µs: constants' `source` vs kepler/field scalar chains) is arithmetic, not a direct timer — the next rung perf-instruments it.

## Cost of adopting; fit with PRINCIPLES

Birth-only hoist: ~60 lines, no behaviour change, deletes compute ("the cheapest compute is compute not done"; "Compute only surprises" — a body's birth re-derives what its own tick already knows). The deeper adoption (shared readouts at every wave, and `source`+`secondaries` as one read) is the same law, one representation change. Grade-candidate: silver — one named experiment from gold (the shared-readout flight covering both paths, digest-identical, priced at 10⁵).

## The lens (library, mined verbatim — every quote retrieved from the Readwise API, work/library.json)

Top-board structure: how the compute-starved made per-item setup vanish. Five lessons, each changing a decision:

1. **"It is easy to deduce something you already know."** — Isaac Asimov, *Foundation and Earth*. Mechanism: per-body recomputation of per-tick shared state is a deduction repeated, not new information. Change: hoist the planets' readouts across both read paths (measured here: −29.5% of the pass, digest-identical; the same structure repeats at every wave-front pass). Test: flown above; the adoption flight is the same knob in a canonical-cut flight.
2. **"Amortization is the process of spreading the cost of a resource investment over the estimated useful life of that investment."** — Josh Kaufman, *The Personal MBA*. Mechanism: the first plan is billed 100% at tick 0 for an interval that lives 2.8×10⁴ s; unamortized birth is the wave's ruin basin (315–1,213 ms frames, 6138/4487). Change: bill the clock derivation at the first reader/first boundary, not at start — and never promote-then-plan (404b's consequence 2). Test: lazy-first-plan arm at 10⁵ burn, max-frame meter, digest at canonical cuts.
3. **"Redundancy is ambiguous because it seems like a waste if nothing unusual happens. Except that something unusual happens—usually."** — Nassim Taleb, *Antifragile*. Mechanism: the belt is 98.4% past the keep window at steady cuts but 91.2% in-window just past a wave — the unusual is periodic, so a fixed cap pays the waste both ways (0619: no fixed cap ships burn). Change: retention sized by the tail's frequency (wave-synced keep), not by N. Test: 398f's adoption flight (ALL+retention ≥48k on the belt and one infalling class).
4. **"Fortunes require leverage. Business leverage comes from capital, people, and products with no marginal cost of replication (code and media)."** — Eric Jorgenson, *The Almanack of Naval Ravikant*. Mechanism: a compiled arc is inventory (8–26 kB sticky); a record is code (113 B, re-mint bit-identical, 3dc8) — the ladder's whole seam family is this axis. Change: apply the no-marginal-cost test to the birth state (the belt is already a bijective program, 98bc: 0.126 bits/body) and price promotions per distinct reader, not per body. Test: count distinct readers per promotion on the belt arm (f55d's cap-invariant read stream says it is ~1).
5. **"You would think that 3D printers would have solved the scarcity problem. In fact, the technology had just moved the bottleneck."** — Dennis Taylor, *We Are Legion* (Bobiverse). Mechanism: every seam fix so far moved the constraint (retention → promotion bill → history stack → the view's walk); optimising the pre-fix bottleneck is polishing a solved one. Change: re-measure the pass after this hoist before any deeper store work — the new candidate is the bignum scalar chains of the clock derivation, not representation. Test: perf the 23 µs remainder (`constants`' `source` reads vs kepler/field), one rung.

**Blind spot:** a library of decision books maps cleanly onto cost structure but not onto GR-native representation; lessons 1 and 5 were flown because they were the only two whose cheapest test fit this window. Analogies are cheap — the other three are ranked by how directly they change a named rung.
