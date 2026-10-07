# Run 20261007-2057-spacex-de6a — H_live, the first measurement

## Claim

On the plane's scene the sparse order (dolls and tubes) gains **5.5–11.4 bits of live distinguishing information per game-second, 0.07–0.16 bits per body per game-second** (seeds 1/2/7, rtf 100, 800 game-s; rtf 1000, 5,000 game-s: 5.5 bits/s), and **99.7 % of the scene's events (≈426 of 427 s⁻¹) are the fleet battle's dense order, whose bits this probe does not reach** — so at the measured rates even a uniformly *quiet* billion breaks the 8 GB budget in one game-hour (≈57 GB of accumulated distinctions), and the memory question is decided by the active fraction and by reabsorption, exactly as the outside review claimed.

## Bottleneck

Board focus "fitting 10⁹ in 8 GB … decided by distinctions created per game-second"; HANDOFF's risk list: "H_live … not measured yet". Idiot-index form: measured memory is 5,310 bytes/body (dashboard) against a measured distinction rate of ~0.1 bits/body/game-second — the memory cost is dominated by plumbing, not information. The number was missing; without it B18's "≤ 2× floor + 2 bytes" has no numerator for the floor's dynamic part.

## What was built

Read-only instrumentation (patch: `crates/universe/src/universe.rs` +150 lines, `xtask/src/universe/mod.rs` +11; `work/patch.diff`): at the single funnel `Universe::apply`, the integer deltas of the canonical words — tube key, wrapping periapsis angle, periapsis time, the two sub-quantum velocity carries — are histogrammed per (event kind, body, field); `h_live` block added to `xtask universe --bench` JSON. Operational definition (a proposal for the directed build `b-h-live`, which owns the final one): a body's first event is a birth (the program's job); an all-zero-delta event stores nothing; otherwise the bits added are the empirical conditional entropy of the deltas given (kind, body). Decisions counted at `take`.

## Evidence

Commands (each < 60 s, Linux x86, orders of magnitude only):

```
cargo build --release -p xtask
for s in 1 2 7; do xtask universe --bench --rtf 100 --seconds 8 --unpaced --seed $s > bench-s$s.json; done
xtask universe --bench --rtf 1000 --seconds 5 --unpaced --seed 1 > bench-rtf1000.json
```

JSONs in this folder. Machine: 8 vCPU shared runner, idle-ish, `machine_before/after` in each JSON.

| run | game-s | body events | bits/s | bits/body/s | kick bits/event |
|---|---|---|---|---|---|
| seed 1, rtf 100 | 800 | 1,176 | 8.97 | 0.126 | 12.0 |
| seed 2, rtf 100 | 800 | 784 | 5.81 | 0.083 | 11.7 |
| seed 7, rtf 100 | 800 | 1,464 | 11.45 | 0.164 | 12.5 |
| seed 1, rtf 1000 | 5,000 | 3,034 | 5.49 | 0.072 | 18.0 |

`cargo test --release -p emergent-universe`: 10 + 6 + 1 unit tests pass on the patched tree (doctests interrupted by my own 60 s timeout, not a failure).
Findings that matter:

1. **The kick's information is in the carries.** Per kick: carry0+carry1 ≈ 9.3 of 12.0 bits (77 %); angle 1.5; time 1.3; **the (E, L) memo key changes on 0 of 594 kicks** — the quantized orbit is stable, the sigma–delta remainder in 2⁻¹⁶ of the velocity quantum is the scar. Each carry occupies only ~2⁴·⁶ distinct values.
2. **Boundary crossings store nothing:** 560/560 all-zero-delta (seed 1) — "compute only surprises" measured: 49.3 % of funnel events do zero distinguishing work.
3. **Rate falls with horizon:** bits/s drops 8.97→5.49 from 800 to 5,000 game-s (kick bits/event rises to 18 as the histogram spreads, but events/s falls faster). The per-game-second rate is not a constant; report it with the horizon.
4. **The dense order owns the event budget:** funnel 1.47 events/s vs dashboard 427.3 events/s → the fleet battle (48 of ~119 entities, 40 %) generates ≈99.7 % of events (≈8.9 events/member/game-second). Its bits (lattice contact carries) are unmeasured; at even 2 bits/event the battle would exceed the sparse order's whole rate by ~100×. Distinction mass concentrates where bodies interact.
5. **Digest unchanged:** seed 1 digest `29f440d6…` identical to the clean build's at the same seed/rtf/cut (run before patching); frame CPU p50 1.017 ms vs 1.003 ms clean (~1.5 % instrumentation cost).

## Extrapolation to the goal (the number the integrator asked for)

- Quiet universe: 10⁹ bodies × 0.126 bits/body/game-second × 3,600 s = 4.5×10¹¹ bits ≈ **57 GB per game-hour — 7× over 8 GB** with no reabsorption. Even the sparse order alone needs an active fraction < ~14 % (or scar compaction) to fit.
- Battle-like universe: if members distinguish at ≥2 bits per contact event (8.9 events/member/s), a 0.1 % active fraction (10⁶ bodies) already adds ≥1.8 GB/hour. The allocator must shed or fold battle scars, not tube scars.
- Repack arithmetic (encouraging): a belt body at ~0.3 kicks/orbit × 12 bits ≈ 3.6 bits/orbit; 2²³ bodies on 5×10³ s orbits ≈ 3 kbit/s of new scar — idle-time repacking is nowhere near saturated by quiet populations. The pressure is entirely in the dense order.

## Predictions (predictions.md, written before the run)

- P1 held: kick bits/event 11.7–12.5 ≤ 12 (marginal; 18.0 at rtf 1000, so it holds only at the bench's native horizon — the estimator's support grows with samples, stated as a caveat, not hidden).
- P2 failed as written: kicks are 0 % zero-delta (every kick moves a carry); boundaries are 100 % zero. Overall 49.3 % vs the predicted ≥50 % for ship events. The interesting structure (which kind is predictable) was not in the prediction.
- P3 not testable from this output (no per-body rates emitted; the directed build should add them).
- P4 failed for the sparse order alone (8.97 < the 10² floor) and is untestable for the scene total (dense order unmeasured). My Fermi estimate wrongly put all bodies at 6 events/s; the sparse order runs at 1.5 events/s and the battle at 426.
- P5 held in direction, not magnitude: uniformly quiet 10⁹ gives 7× over budget (not ≥100×); ≥100× needs the battle regime.
- P6 held trivially: nothing heals scars; removals (17–28 bodies) are the only reabsorption.

## What would make it wrong

The conditional-entropy proxy measures statistical predictability given (kind, body, last state) — a real program (launch grid, formation lattice) predicts far more structure (e.g. correlated carry sequences), so the proxy **overstates** the true floor; conversely it misses the dense order entirely, so it **understates** the scene total. The two errors are on different populations; the 57 GB/hour figure is an upper bound for quiet bodies, and the battle term is a lower bound of unknown size. If `b-h-live`'s precise definition (from the engine's own state, with reabsorption) lands within 3× of these numbers on the sparse order, the probe did its job.

## Cost of adopting

Small: the patch is read-only instrumentation behind one funnel, digest-verified identical, ~1.5 % frame cost in the bench path (could be compiled out of the page). Fit with PRINCIPLES: "Compute only surprises" (§3) — now measured: half the sparse order's events store zero bits; "The memory floor is information" (§24) — the first dynamic numerator; "Measure before claiming" (§10). The lens may have missed: the fleet battle is the actual memory story and this lens (delete/idiot-index) spent its time on the part it could reach cheaply.

## Grade suggested

Silver: real, measured, digest-safe, on a named bottleneck — one experiment away from gold (instrument the dense order's contact carries, which hold ~99.7 % of the events, and add per-body rates). The directed build `b-h-live` (queued last) should pick that up; this patch gives it the sparse-order half and the definition to argue with.
