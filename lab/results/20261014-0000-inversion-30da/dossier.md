# Dossier — 20261014-0000-inversion-30da (inversion lens)

## Claim

The merge gate `universe --replay-all` (merged 13 October) silently stops checking flights
as play accumulates: a fixed 55 s budget is shared over an append-only corpus, flights it
cannot reach are skipped with **exit code 0**, and at the only recorded real-play density
the whole budget holds ~19 minutes of total play — less than one budgeted session.

## Bottleneck

Not a board physics bottleneck; this is failure mode 5 of the lens's list (a process that
eats the builders' trust) wearing failure mode 4 (state that grows with play). The gate
guards every merge — all physics work — so its silent decay taxes everything downstream.
Expected gain: not orders of magnitude of compute, but the restoration of a binary
guarantee ("every committed flight replays, or the merge stops"); what it deletes is the
*illusion* of coverage. The corpus's replay cost grows without bound (nothing prunes
`artifacts/flights/`), while the budget is frozen.

## Evidence

All on shipped code (`main` @ f687ec25 + this run's patch, Linux/x86, 8 vCPU, orders of
magnitude only; the M1 re-measures). Commands in `regen.sh`; rows also in
`work/growth.json`.

1. **Mechanism (code, not inference).** `xtask/src/universe/replay.rs::replay_all`:
   `ALL_SECONDS = 55.0`, each flight capped at `budget/2 = 27.5` s, and
   `Err(Stop::Deadline)` → `skipped += 1` with the process exit code staying 0 unless a
   *reached* flight regresses.
2. **Today, full coverage.** The three committed flights replay in 2.3 s in all
   (`--replay-all`, measured). Per-flight: 1.4 s / 0.2 s / 0.5 s.
3. **Real-play replay density.** Committed flight 20261013T143859Z: 1,205 coordinate-s
   (tick 244,668,019 × TICK_SECONDS 4.9255 µs), 6 inputs, replay 1.4 s → **~8.6×10²
   coordinate-s per replay second**. The other two: 2.0×10³ and 4.4×10³.
4. **Growth model (flown, not simulated).** Sessions flown through the shipped
   `Session`/recorder at 48 members (as the committed flights), scripts in coordinate
   time with real decision density (asserted ≥ 5 inputs):
   500 / 5.5k / 29.5k / 59.5k coordinate-s → 0.13 / 1.98 / 2.48 / 3.64 s replay. Cost is
   event-driven and front-loaded: the burn-dense opening runs at ~2.8×10³ coordinate-s/s,
   the coasting tail at ~3.3×10⁴; a 130k coordinate-s burn-dense flight (105,826 events,
   259 inputs) replays in 5.9 s (~2.2×10⁴ coordinate-s/s, ~1.8×10⁴ events/s).
5. **The corpus demonstration (the probe, run as pre-registered).** Ten legal flights,
   each replayable alone in ~6 s (far under the per-flight cap), plus the three
   committed ones: solo replays 54.1 s + 2.1 s > 55 s. `replay_all` on that directory
   reached 11 of 13 and **skipped the longest committed real flight**
   (`20261013T143859Z`, "not replayed within 1 s") — and still printed
   `0 regression(s)` and **exited 0**. Ten flights ≈ 1.3×10⁶ coordinate-s ≈ 8.7 hours
   of rtf-100-equivalent play; at the committed flights' real density the same budget is
   gone after ~19 minutes of play. Coverage is longest-first, so what the gate abandons
   first is exactly the richest flights.

## Predictions


- **P1 partially wrong:** throughput is not one R; it spans 0.9–22×10³ coordinate-s/s by
  play style (8× spread, all measured). Front-loaded: openings cost ~6× their tail.
- **P2 wrong in magnitude, right in shape:** the 6×10⁴ flight replayed in 3.6 s, under
  the predicted 5–40 s window; a single *scripted* flight outliving the 27.5 s cap needs
  ~6×10⁵ coordinate-s. But at real-play density (evidence 3) the cap is crossed at
  ~2.4×10⁴ coordinate-s ≈ 10 minutes of play.
- **P3 held:** corpus reach 55 s × R = 4.7×10⁴–1.2×10⁶ coordinate-s ≈ 19 min–8 h of
  play; the demonstration sits at the top of that band, the committed flights at the
  bottom.
- **P4 held:** control passed — 3/3 committed flights reached today; and the skip path
  was demonstrated directly (exit 0), not inferred.
- **P5 held at real density:** one budgeted hour ≈ 174 s of replay at the only recorded
  real density; ~7 s at scripted-cheap density. The claim "a budgeted session can never
  be checked" is density-dependent, not universal — the honest form is evidence 6.

## What would make it wrong

- If flight-time replay throughput on the M1 is ≥ 4×10⁵ coordinate-s/s for real play
  (none of the three recorded flights is within 100× of that), the corpus holds months
  of play and the decay is theoretical. The three real samples say otherwise.
- If flights are meant to be pruned (a retention rule I did not find — the recorder is
  append-only and `--replay-all` reads the whole directory), corpus growth stops and the
  budget suffices.
- If the integrator treats the printed `skipped` line as a failure by discipline (it is
  one line among many, and the exit code says success — the HANDOFF line "0 regressions
  now" does not mention coverage), the gate is already honest enough for its owner.

## Cost of adoption, and fit

The fix is not the law; it is the gate's contract, one small patch: (a) `skipped > 0`
must exit non-zero (a gate that cannot fail is a control — PRINCIPLES, test-ladder
inverted), and (b) replay the corpus in parallel (replays are independent and exact;
~8× reach on this box, more on the M1's 4P+4E). Optionally raise `ALL_SECONDS`. Cost:
minutes of build, a possibly slower (but honest) merge check as the corpus grows;
benefit: the recorder's promise ("his flights are the regression suite", HANDOFF item 2)
stays true past the first day of play. PRINCIPLES: "Measure before claiming" — the merge
check now claims coverage it does not have; "Errors never compound" — uncovered
regressions compound silently in the recorded corpus; "no busywork" — a green gate that
checked nothing is busywork.

## The lens

Inversion asked what the most recent merge silently assumes; the recorder assumed its
gate's budget scales with the corpus it is given. What this lens may have missed: the
physics bottlenecks (the N ladder, encounters, the kick) moved not at all this hour —
this is process insurance, and the integrator may rightly rank it below a physics merge.
The event-cost front-loading (evidence 4) is a physics observation this lens reports but
did not chase: why the opening 5.5k coordinate-s costs ~2 s while the next 54k costs 1.7 s
(compilation? first bindings? γ growth?) is a frame-cost question, left to that page.
