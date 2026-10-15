topic: n9-ledger
status: open
closed-by:
valid-while:
updated: 20261015-2041-fermi-99b5

# The 10⁹ ledger: cadence, re-mints, and the record stack at a billion bodies

*(Checker-corrected: the run's headline law was refuted; the page now records what
stands. See check.md — three independent lines of evidence, two of them the checker's
own flights.)*

## Current best

**Nothing in this run's ledger survives as new.** The belt's cadence stands where
3294's census and cf45 left it — median fire interval 28,141.5 s = 3.55e-5 kicks per
belt body per game-second, confirmed twice before this run (3294 census on the
nladder scene, f82a re-check; cf45's flat-in-a interval) and now a third time by
N-scaling (20261015-2041-fermi-99b5's checker, unthrottled flights at rtf 900:
per-body depth-differenced rate 1.54e-3 / 1.93e-4 / 5.69e-5 at 10³/10⁴/10⁵ — the
signature of ~328 fixed near-Home locals at λ≈4.8–5.7e-3/game-s diluted by the belt,
not an N-flat law; 3294: those locals take 81% of all fires). The 10⁹ composition at
that cadence: kicks 1.53 cores (c01c 43 µs), re-mints **0.131 cores cap'd ≈ 0757's
"~0.15" — 0757 was right** — 1.67 uncapped (12.7 reads/dem), CPU 1.66 cores = 0.21×
the M1 (not CPU-bound), and memory the record stack 0.98–1.32 TB = 163× the ~6 GB
budget, binding ~780× harder than every CPU term — which is already on record
(760f "the wall is the record stack", quant-0619's 1.4 TB knee, d6ba's checker "the
record stack is the term"). The run's shipped-code memory anchors do reproduce
(birth 2,347–2,465 B/body RSS, dashboard 1,352–1,437, catalogue N+76, equal to
8b89's ctl; depth-invariant at 10⁴) — confirmations, not new measurements.

**Instrument note (the run's one durable lesson, already implicit in 3294's
parenthetical "the ladder's own counter agrees: 1.902e-4 over all bodies incl.
near-Home"):** a per-body average over a scene with a fixed local population is not
a per-body law. Read cadence from a kick-site census (3294's census.rs) or from
N-scaling across at least two unthrottled rungs; a single rung's all-bodies counter
cannot separate them (the 10⁴ mix coincides with the birth-window rate to within
10%, which is what misled this run).

**Domain.** The standard nladder scene (seed 1, coast), rungs 10³–10⁵, cuts to
~45k game-s, one Linux box, rtf 900–3000. Not tested: burn at depth, the 10⁶ rung
(over this box's budget), 10⁹ itself.

## Refuted

- **"The belt's shipped kick cadence is 1.9×10⁻⁴ per body per game-second, 5.4× the
  doll-interval law" (20261015-2041-fermi-99b5):** that is the 10⁴ *scene average*,
  ~82% locals. Refuted by 3294's census (belt median 28,141.5 s; locals 81% of
  fires), by the checker's unthrottled N-scaling (1.54e-3 → 1.93e-4 → 5.69e-5 at
  10³/10⁴/10⁵), and by the run's own 10⁵ shallow arm (1.715e-5, belt silent =
  locals alone). cf45's interval law stands unscoped-wrong; the "two interval laws"
  contradiction was an artifact.
- **"Every paced 10⁵-and-up coast flight measures the 12 ms budget" (same run):**
  at rtf 900 the 10⁵ rung runs unthrottled (p50 2.3–3.3 ms, ≤7 frames over) and
  delivers the true cadence (5.69e-5); the rtf-3000 arm delivered ~90–100% of it,
  not 14–26%. The "predicted 17%" was the wrong law times the scoreboard's 75 µs;
  at c01c's 43 µs no throttle was predicted. ladder.txt's 10⁵ 1.9e-5 is a 20-s
  window artifact (first belt wave at 13,051–14,534 game-s). The dossier also
  mis-cites ladder.txt's 10³ row as 1.86e-4; it reads 1.86e-3, locals-dominated.
- **"0757's ~0.15 cores re-mint at 10⁹ understates 4.8–60×" (same run):** inverted —
  at the belt cadence the steady bill is 0.131 cores cap'd; 0757's number was
  accurate.
- **"CPU today 9.0 cores = 1.13× the M1" (same run):** at the belt cadence 1.66
  cores = 0.21×; the 10⁹ ledger is memory-only, as effb/cf45/quant-0619/d6ba already
  had it.

## Open directions

1. **Shrink the per-body record** — unchanged from 760f/quant-0619/d6ba: the
   0.98–1.32 TB record stack is the only 10⁹ term over budget; compact-store
   promotion (shipmem's 21–40 bits, unwired).
2. **Cadence split leverage, priced at the true law:** an 8× cut takes kicks
   1.53→0.19 cores (cap'd re-mints 0.13→0.02) — compute was never the 10⁹ wall at
   coast; the split matters for the burn and the frame, not this ledger.

## Contradictions

- None standing: the run's "measured law vs cf45's interval" contradiction is
  dissolved (locals contamination). The effb→cf45 lineage governs.

## Runs

- 20261015-2041-fermi-99b5 (lead): the 10⁴ scene average (1.9e-4) mistaken for the
  belt's cadence; throttle story, 0757 correction and CPU-bound composition all
  refuted by 3294's census + N-scaling; memory anchors reproduce (8b89
  confirmation), record-stack conclusion already known.
