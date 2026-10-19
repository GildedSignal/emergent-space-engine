# Predictions (written before the decisive run)

The carried form of the law's quantized cell: `Rebinding::from_state` serves its cycle from
`QuantizedMemo` (the law's 11+11-bit cell, ENVELOPE.md's measured width) with the **exact key
carried** (`Orbit::from_shared(exact_key, cell_shape)`), env-gated `ES_QMEMO=1`; off = shipped
verbatim. The exact integer state and the residual channel (`turn·decode + offset`) are untouched,
so the state channel never absorbs the cell's rounding — the write-back form law.md killed
("re-rounds at every kick, a random walk") is not this form.

Cases not tuned on (the plane scene's real distinct-kick stream, 900 frames, seed 1, 48 bodies,
the same harness as the standing `memo.rs` test):

- **P1 (the hit rate, served):** the cell recurs on > 90% of distinct kicks (memo.rs's standing
  measurement, now actually served): shape builds / rebind < 0.15.
- **P2 (B2 re-judged, the tightest):** max |period(served)/period(exact compile) − 1| over all
  distinct kicks < 1e-3 (B2's frozen 0.1% band; memo.rs's doc bounds the cell's period error by
  2^-11 ≈ 4.9e-4 — only 2× of margin).
- **P3 (B1 re-judged):** max |advance(served)/advance(exact) − 1| < 1e-2 (B1's frozen 1% band).
- **P4 (B9 re-judged):** the cell's knot count within a few of the exact compile's (same band
  structure; no knot explosion).
- **P5 (determinism):** the served law is a pure function of the exact key, so two full runs of
  the same stream give identical readout hashes; and with `ES_QMEMO` unset every printed number
  and the game digest are the shipped law's, bit for bit (the patch is inert when off).
- **P6 (the state channel stays exact):** the exact keys of the kicks' new orbits still never
  recur (< 5% recurrence) — the orbit carries the exact invariants, not the cell's.
- **P7 (the CPU deletion):** the harness's wall time (and the FIT stage when the prof feature is
  on) drops by ≥ 3× with the cell serving (the compile is 84–87% of a kick, hits ~90%+ → expect
  4–8×).
- **P8 (the memory bound):** standing shapes at the end of the stream, deduped by allocation,
  are bounded by distinct cells (< a few hundred), not by bodies.

**Kill criteria:** P1 fails (no hit rate to serve); or P2 fails at the shipped cell width AND P7's
saving is < 2× (then the width and the win do not trade); or P5 fails (the served path is not a
pure function of the key — determinism broken); or P6 fails (the exact key is being snapped — we
have re-built the killed write-back form and the idea is dead as designed).

What I expect could break (named before the run): P2 is the one with only 2× of margin; if it
fails while P7 holds, the result is a width report (one more fraction bit halves the error and
quarters... doubles the cells), not a kill of the mechanism. The oracle here is the law's own
exact compile (the same judge `behave` uses for B1/B2-class statistics on this crate), not a
float truth — no trajectory identity is demanded anywhere.
