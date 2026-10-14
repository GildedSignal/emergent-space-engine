# Dossier — 20261014-1221-system-b8fc (lens: the whole system)

**Claim.** The compiled cycle's **knot table** is one structure behind the plane's three measured
walls — the kick's bind, the kick's search, and the memory after the first kick — and the census
shows it is a cache that costs more than what it caches: **per compiled table of 77–92 knots, only
7.1–7.6 bracket cells are ever read (≤10%), while every readout still re-integrates ~13 integrand
point-evals of Newton quadrature; both sides of the event cost pay the same quadrature over the
same integrand that the certified Carlson closed forms evaluate in O(1).**

**Bottleneck.** The board's three ~10³ gaps "one kick 75–300 µs vs ~50 ns", "memory ~5,100 B/body
vs ≤6 B", "bodies 10⁶ vs 10⁹" share this structure. Deletion, not tuning: the table's only
irreplaceable content is (a) cumulative-time anchors and (b) the cycle increments — (b) is already
certified to the table's own 2⁻³⁰ quantum by Carlson kernels (kick-jet page), (a) and the readout
are the fenced incomplete forms. This census prices that replacement: it deletes the build walk
(4×334k–4×1.44M point-evals per 8 game-s), the read re-integration (2.8 quads + 1.9 rate evals per
readout), and the standing 77–92 knots × 88 B per live binding — one adoption, three bottlenecks.

**Evidence** (shipped `plane` scene, single thread, additive counters only — `crates/space/census.rs`,
hooks in `orbit.rs`; the digest proves no bit moved; commands in `regen.sh`, each run < 6 s):

| arm (seed 3, 8 game-s) | compiles | knots/table | readouts | cells read/table | build pts | read pts |
|---|---|---|---|---|---|---|
| 400 members, rtf 100 | 4,348 | 76.9 | 224,233 (60/table) | **7.6 (9.9%)** | 1.34 M (31%) | 2.98 M (69%) |
| 1,500 members, rtf 100 | 15,553 | 92.3 | 825,221 (55/table) | **7.1 (7.7%)** | 5.74 M (34%) | 10.96 M (66%) |

- Read anatomy (both arms): per time→state readout, 5.4–5.7 bracket **probes** (cheap compares on
  stored sums) then 2.8–2.9 partial-panel **quads** + 1.9 Newton **rate** evals ≈ 13.4 integrand
  point-evals — the 4.6 µs/readout the frame-cost page measured is re-integrated quadrature, not
  table lookup. The table brackets; it does not serve.
- Digest identity (schedule independence, B8): 400/rtf100/8 s gives `b1feb4bf1157db6958091a41aa140903`
  under unlimited budget **and** under a biting 3 ms wall budget (kicks 4,004 both; the settle
  reaches the same canonical cut). Counters change no bits.
- Prof on the 400 arm reproduces the frame-cost page's structure: kick item 188.8 µs (fit 77.7 µs
  inside), hand-out 501 µs (bind 358). The census attributes the fit's walk and the search's
  readouts to the same integrand family.

**Predictions** (`predictions.md`, written before the run): P1 held exactly (7.6/76.9 and 7.1/92.3
against bounds ≤10%/≤60%). P5 held. P2 held at 13.4 point-evals (predicted ≥15 — close, honest
miss). **P3/P4 failed as stated and the failure is the finding**: I predicted the build would
dominate integrand work on quiet arms; measured, the **read side dominates everywhere (66–69%)** —
the table is built 77–92 knots wide per event and then *re-derived* by quadrature at every read
because only ~7 cells are consumed. The unification survives, inverted: the replacement must take
the readout path first, not the compile.

**What would make it wrong.** If the incomplete Carlson forms' integer port cannot hold the readout's
2⁻³⁰-in-ψ contract (fenced, unpriced — the kick-jet page's standing objection), the read side stays
panel-based and the deletion halves. The census is orbit.rs-only (bound Darwin cycles; Kerr, light,
plunge walks uncounted), single-thread, two scenes, 8 game-s; `at_radius` (the passage guess) is
17,929 calls on the 1,500 arm — a 2% path. Table identity is by allocation address (Arc reuse can
only undercount distinct cells read — the 7.1–7.6 is an upper bound of consumption, strengthening
the claim).

**Cost of adoption / fit.** One representation change at the Entry: closed-form increments plus
incomplete-form readout, fence from the kick-jet page (Carlson 1994 forms, already verified against
the walk to its own quantum on the complete channels). PRINCIPLES: "we just need to have the right
representation so that math is trivial" (18); "the best part is no part" (17) — this deletes a
per-event table, not a constant. Not a law change: same bits required only at the readout contract
level (the closed form must reproduce the walk's certified quantum, as it already does for the
increments).

**The lens.** Whole-system: I almost shipped the compile-side story (P3/P4) because the frame-cost
page frames the bind as the kick's cost; measuring both sides showed the read side is the larger
half — the per-page framing had hidden the shared structure. Missed here: the view's readouts are
inside the 224k–825k (I did not split reader by consumer); the wiki's `view` page (93–99.9% far-row
tax) suggests most of those reads buy zero pixels — the same deletion pays there too.
