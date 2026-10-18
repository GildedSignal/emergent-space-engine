# Dossier — 20261018-0814-library-6faa (library lens)

**Claim.** The kick bottleneck's decision table, composed from measured constants, splits by
population: the Carlson wiring is a 3.3–9.4× lever on the plane rebind and a 3.1–11.0% lever
at 10⁹ — so the plane and memory close on the wiring, the 10⁹ CPU row closes on the cadence
split, and five verbatim library lessons (5/5 byte-identical) hold that ordering.

**Bottleneck.** The board's #3: the kick, 75–160 µs against a ~6 µs arithmetic floor (a765;
the 42–56 ns write floor never binds — e7ef: at it, even shipped cadence fits, 0.17 cores).
Gain: plane kick path 3.3–9.4×, flyable N 3.97× (the knot table is 75% of the live plateau),
10⁹ CPU ~zero from the wiring. What it deletes: the knot/crossing table (7–16 KB/body), the
walk-polishing program behind 71 kick-jet runs, and the scoreboard's independent kick row
(double-counts cost×cadence, e7ef).

**Evidence.** Cache: `work/readwise.json` (4,590 highlights, 770 books, fetched fresh this
run via the export API, all pages). Reproduce every number (≤ 5 s):

```
cd lab/results/20261018-0814-library-6faa && ./regen.sh
# quotes: 5/5 byte-identical (work/quotes.py, exact substring of one highlight)
# P2 wiring CPU, belt/10⁹ : save 1.55-5.55 us of 50.4 = 3.1-11.0%
# P2 wiring CPU, plane    : compile 52.8-65.3 of 62.6-75.4 us rebind = 86% share
# P2 compile term 18-23x; whole rebind -> 8-19 us = 3.3-9.4x
# P3 belt kick composed: 32.1-36.1 us vs req 23 -> 1.40-1.57x over
# P4 knot table 3784 B of 5060 B plateau = 75%; wall 1.19-1.58M -> 4.70-6.27M live = 3.97x
```

All inputs page-cited: 3570 (belt kick 50.4 µs), c4d3 (belt compile 4.45 µs), de99 (kernels
≤2.9 µs all-three), a765 (plane rebind/compile shares, 6 µs floor), cd6e (composed kick
8–19 µs), 5ade (−17%), 9c67/d65c (−9…−11%), e7ef (23 µs requirement, redundancy), b30b
(5,060 B plateau), HANDOFF scoreboard (43 knots × 88 B), 6793 (wall 6–8 GB).

## The five lessons (all quotes byte-identical, `work/quotes.py`)

1. **"So I got a great reputation for doing integrals, only because my box of tools was
   different from everybody else's, and they had tried all their tools on it before giving
   the problem to me."** — Feynman, *Surely You're Joking, Mr. Feynman!*
   Mechanism: the same integral is a quadrature walk or one closed evaluation — a tool
   choice, not a law; 71 runs polished the walk because it was the tool at hand.
   Change: wire the Carlson kernels into `Rebinding::from_state` (kick-jet open 1):
   compile term 18–23×, whole rebind 62.6–75.4 → 8–19 µs; the walk keeps oracle status.
   Test: resolver-level digest identity (a765's harness + frame_digest's 8 schedules).
2. **"Tools and leverage create this disconnection between inputs and outputs."** — Naval,
   *The Almanack of Naval Ravikant*. Mechanism: per-event µs is an input; the ledger is
   rate × cost — redundant levers (e7ef). Change: the wiring is 3.1–11.0% at 10⁹ but 86% of
   the plane rebind and 75% of the plateau (3.97× flyable N); 10⁹ closes on the split
   (S* ≈ 20×), never on kick µs; delete the scoreboard's independent kick row.
   Test: arithmetic (this run's ledger.py).
3. **"It's not the product that leads to success. It's the ability to make the product
   efficiently. It's about building the machine that builds the machine."** — Musk via
   Isaacson, *Elon Musk*.
   Mechanism: on the belt the product (the compiled cycle, 4.45 µs) is cheap; the factory
   (bind/refit walks, sources, decodes — 84–93%) is the bill; hand the value over, never
   re-walk it (5ade's tau pair, 9c67's apply walk are the template).
   Change: the ≤23 µs requirement's lever list is walks/sources (read-stream open 1's
   per-drain sources rebuild 19%, observe's per-event reads 66%) — not the compile, not the
   retired search. Test: one stage-census flight on a post-adoption build (5ade's harness).
4. **"A man who has committed a mistake and doesn't correct it, is committing another
   mistake."** — Confucius via Bevelin, *Seeking Wisdom*.
   Mechanism: five kick-side wins are measured, digest-identical and unadopted (b583's
   retired search −46…−48% leaver; 2ae0's warm+AB-IQI −78…−83% readouts; 5ade's tau carry;
   9c67's apply walk; the Carlson wiring) — every unbilled event repeats the mistake.
   Change: one adoption window clears the class — b583's regen fix (build xtask per arm,
   interleave, restore the two deleted kick-bench fields), 2ae0's gate flip, the wiring.
   Test: the regen fix itself, a script edit.
5. **"We abandoned the appearance of power to preserve the essence of it."** — Asimov,
   *Foundation's Edge*.
   Mechanism: f64 exactness to r = 10⁻¹⁵ is appearance; the law's quantum (Q30, integers
   decide) is essence; open 3's ulp-level key kills judge by appearance.
   Change: port the kernels to integer inside the wiring (one adoption, open 5), verified
   per channel against the walk at the quantum; keep the exact bisection key — a 3% prize
   never justifies a law change.
   Test: one kernel (RF) at Q30 vs de99's f64 oracle on the 29-key grid.

**Predictions** ([predictions.md](predictions.md)). P1 held (5/5 byte-identical). P2
half-held: the belt clause (≤5%) holds only at the compile-only bound (3.1%; honest band
3.1–11.0% — the 11% end assumes the read composes at parity, which cd6e's checker bounded
warm-only); the plane share (≥80%) held at 86%, the "≥8× rebind" holds only at the top edge
(3.3–9.4×). P3 held as a band: 1.40–1.57× over 23 µs (the ≥1.5 clause holds at the
compile-only end, marginally missed at the upper end). P4 held (75% ≥ 70%; 3.97× ≥ 3×).
P5 missed on "exactly three": five unadopted wins exist (the three named plus 5ade's and
9c67's deletions); the blocker-class claim (bookkeeping/identity debt, not physics) held.

**What would make it wrong.** The 8–19 µs composed-kick band is cd6e's f64 instrument, not
a wired measurement; if the resolver wiring fails digest identity, or prices like 262f's
batched promotion (a 2.9× regression at belt keys), the plane multiple collapses toward the
compile-only bound. The 10⁹-side shares inherit b30b's/3570's shared-box wall anchors.
Cost of adopting: the integrator's one named step (open 1) plus one adoption window (L4);
the integer port rides the same adoption (L5).
**Fit with PRINCIPLES.** "we just need to have the right representation so that math is
trivial" (L1 is that principle in Feynman's mouth); "'Exact' means deterministic and
reproducible, not equal to reality. Exact physics is the oracle, not the implementation"
(the walk demoted to oracle, L1/L5); "The cheapest compute is compute not done" (L3/L4).

**The lens.** A lessons run prices and orders but wires nothing; every number here
inherits the cited pages' instruments (one upstream stage-share error would reorder L1–L3);
and it cannot see the one gate that kills L1 — whether digest identity survives the
composition. The library over-represents business texts; the compute-starved practitioner
voices it holds (Feynman, Musk, Simons) are thin — Simons' two transcript highlights were
unusable (garbled ASR spacing).
