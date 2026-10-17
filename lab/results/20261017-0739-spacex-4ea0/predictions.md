# Predictions (written before the decisive census runs)

Question: kick-jet open direction 2 — compile-on-read for the fired kick. The unmeasured
quantity is **shape reads per binding generation** (and who the readers are). It decides:
(a) if a large share of generations is never read, deferring the compile DELETES those
compiles; (b) if the view dominates reads, eviction (knots→0 standing) multiplies compiles
by reads/gen (CPU ruin) and the deferral only MOVES the compile onto the per-frame path;
(c) if engine reads dominate and are few, the deferral is nearly free CPU-wise.

Instrument: print-only census (patch `work/patch.diff`): compiles counted/timed at
`OrbitShape` build + `Passage::compile`; reads counted at `Binding` decode, per Entry
generation, attributed by caller file (view/observe/ctx-secondaries/step/dash/chain/birth).

Cases (held out — not tuned on; my Fermi before any run):
- **P1 (reader mix):** on `universe --bench` (48-member plane, view in the loop) the view
  owns the plurality of attributed reads; I predict view ≥ 40% of attributed reads, with
  `step` (the body's own event reads) and `secondaries` (sources) sharing most of the rest.
- **P2 (never-read generations):** rebind generations are read at least once by the engine
  (the successor event reads the binding it lives on), so never_read(rebind) < 10%; spec
  (birth) generations are the planets/sources, read constantly. If never_read(rebind) ≥ 30%
  instead, compile-on-read deletes that share of compiles outright.
- **P3 (reads per generation):** p50 reads/gen over read generations lands between 2 and
  50; the 48-member plane's bodies are all emitters read ~1×/frame by the view, so I expect
  the mean to be view-dominated and LARGE (> 20) on the default plane, and the fleet leavers
  (passages) to sit at the bottom (1–3, engine-only).
- **P4 (the decision):** if p50 reads/gen > 20 with view dominance, then eviction-style
  compile-on-read (b9ae's knots→0 standing) pays ≥ ×20 compiles on the read path and is
  CPU-ruin at bench scale; retention-style deferral (compile at first read, keep until
  rebind) is CPU-neutral and memory-neutral, so NEITHER form of direction 2 deletes the
  kick's compile term — the lever stays direction 1 (a cheaper compile). If p50 reads/gen
  ≤ 3 with never_read small, retention-deferral moves the kick's 84–87% compile share off
  the event path at ~zero bill and direction 2 wins before the closed form is wired.
- **P5 (compile mix):** passage compiles are a minority of compiles but a large share of
  compile wall on this scene (the leaver ladder: 318–356 µs of 365–381 µs, ec9d); orbit
  (cycle) builds dominate the count.

Kill criteria: the census is VOID if the patched binary's bench digest differs from the
pristine one (kick-bench digest comparison), or if attributed reads exceed the space-side
shape-read total (instrument inconsistency).
