# Predictions (written before the decisive run)

Question: `plan_clock` (crates/universe/src/step.rs) reads the body's own synchronised state
at the same tick `t` up to three times per plan — line ~629 inside the `ext.is_none()` block
(for `pt_exp`), inside `project(t)` (line ~612), and again at line ~635. Belt bodies (doll 0,
`on_clock()`) all pay this at birth in `Universe::start`'s tick-0 replan pass, the term the
nladder page prices at 32.8–33.9 µs/body shipped (d31c) and 76–78% of the 42–44 µs/body birth
rail (404b). One readout can serve all three reads (nothing mutates the binding between them).

Arms: `ES_ONE_READ=0` (shipped verbatim path) vs `=1` (one shared readout), one binary,
`pass_bench` at belt N ∈ {10⁴, 3×10⁴, 10⁵} × seed ∈ {1, 7} (7 held out; d31c flew 1/7/11,
404b held out 7 and 3).

Cases I have NOT tuned on, and what I expect there:

- **P1 (identity):** the universe digest after `start` is byte-identical between arms at every
  (N, seed) flown. The ON arm reads the same value once instead of three times and changes no
  arithmetic; any digest difference kills the run.
- **P2 (the cut, seed 1, 10⁴/10⁵):** the replan pass falls by the price of two `readout`s per
  clock body. d31c measured two own-state readouts at 6.9 µs/body on the ON-pass
  decomposition; I predict an absolute cut of 6–8 µs/body on the belt bodies' pass share,
  i.e. the whole-pass µs/body (over all bodies incl. the ~300 locals and the plane's own)
  falls 15–22% at 10⁴–10⁵.
- **P3 (flat in N, held-out seed 7):** the absolute cut per belt body is the same at 3×10⁴,
  10⁵ and seed 7 as at 10⁴ seed 1 (a per-body redundancy, not a cache effect); cut within
  ±15% of the seed-1 value. If the cut shrinks with N, the readouts were cache-warm artifacts
  and the adoption case weakens.
- **P4 (untouched terms):** the requeue/rekey/alloc terms 404b priced at ≤ 0.1 µs/body stay
  ≤ 0.1 µs/body in both arms (the hoist touches no queue code); the locals' (non-clock)
  bodies are untouched — their contribution to the pass is identical between arms.

Kill criterion: P1 fails (any digest differs), or the cut at 10⁵ is under 3 µs/body (the
redundancy is not worth a patch line; the run reports a lead, not a lever).
