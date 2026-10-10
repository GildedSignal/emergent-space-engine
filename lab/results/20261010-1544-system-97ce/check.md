Grade: silver

**Abstract.** Claim: on the engine's belt path (default cadence 2⁷) the cycle memo would hit 0 of 203,017 kicks — every kick fires, rebinds and rekeys (1.000/kick, ~22 µs per bind). Reproduced bit-for-bit; extended adversarially: all 101,519 keys are globally distinct (zero revisits — even an unbounded memo misses every kick), and Saturn (2⁻¹², 9.58 AU) also saturates at 1.0000. But `bind()` is only 43.7 % of wall (2.22/5.08 s), so the designed re-anchor (0.05 compiles/kick) buys ≈1.7× belt wall, not 20× — the 20× is the compile-count reduction alone. Belt compute at 10⁹ ≈ 3.4 % of one core; the 8 GB risk is the record format, not the kick stream. Silver: held-out predictions failed, and the gain is a priced target, not a wired lever.

## Reproduction (clean tree, `git apply work/patch.diff`)

`cargo test -p emergent-universe --release --test hlive -- --nocapture`:

- 2⁷: events 406,220 (kicks 203,017, opens 385, boundaries 202,818), rebinds 203,017 (1.000/kick), rekeys 203,017 (100 %), 25.9 µs/event (author: 23–25, shared box), 196.7 events/body/ship-orbit, 4.41-yr ship orbit. Identical counts to the dossier.
- 2⁴: events 50,939, rekeys 25,401 (100 %); work ratio 7.98× for 8× cadence — "work ∝ cadence, cost per event flat" confirmed.
- Control: 397 kicks, 397 rekeys; `dv != 0` = 0 everywhere — and code reading confirms why: `kick_clock` writes `dv: [0; 2]` (step.rs:638); only the non-clock `kick()` populates it (step.rs:388). The first probe was indeed blind; the author's disclosure is accurate.
- Sizes 176/192/448 B ✓. Extrapolation arithmetic checks: 406,220/(7.485e8 s·384) = 1.41e-6 events/s/body → ~1.4k events/s at 10⁹ → ~34 ms CPU/s ≈ 3.4 % of a core; 16 B × 10⁹ = 16 GB.
- Documentary: law.md:35 carries the re-anchor text with "≈ 0.05 compiles per kick" ✓; HANDOFF.md:70 "H_live … not measured yet" ✓; `Config::default().step_log2 = 7`, so 2⁷ is the engine's own cadence ✓; `Catalogue::insert` (bind.rs:44) has no dedup — no memo exists in shipped code, so "memo hits 0" correctly means *would-be* hits, via key equality.

## Adversarial cases (three, plus determinism)

1. **Key revisits.** Consecutive-key-change counting overstates memo misses if keys oscillate (a 2-entry memo would then hit). Instrumented every fired kick's new key: 101,519 keys over 384 bodies, **all globally distinct (100.0 %)**; per-body distinct equals per-body kicks (258–301). Every key is new — the 0 % claim holds for a memo of any size.
2. **Weaker perturber.** Saturn analog (2⁻¹² at 9.58 AU, ~8× weaker tide at ~2× the distance): kicks 89,507, rebinds and rekeys 89,507 (1.0000/kick). Saturation is not a Jupiter artifact; it generalizes across the weak field.
3. **Cost attribution** (the dossier's own open question, one counter away). Timed `bind()` inside `rebind`: 21.9 µs/call, 2.22 s of 5.08 s wall = **43.7 %**. The compile is the largest single component but not "the belt's whole engine cost": at 0.05 compiles/kick the belt's wall drops ≈1.7×, and the remaining ~56 % (readout, field, ext.time, planning) needs the secular-kick build. The "20×" is real as compiles/kick vs the design's 0.05, not as wall time.

## Novelty

HISTORY.md (September, pre-pivot) has nothing on belt memos/rekeys. The taste log (5 October) already knows the plane recompiles ~99 % of kicks, the exact memo hits 0 % on distinct kicks, and the quantized cell hit 94.5 % there. This run's delta is the weak-field population: the quantized (E, L) key flips on **every** belt kick (the plane's 94.5 % collapses to 0 % here), keys never revisit, a second perturber strength saturates too, the 10⁹ belt prices at 3.4 % of a core, and the memory risk moves to the record format. Real and new, but the phenomenon class (per-kick recompile) was known and the fix was already designed and queued for wiring.

## Predictions

`predictions.md` mtime precedes dossier and patch; run.log is empty, so log-order proof is absent — mtimes are consistent but weak. Content: predictions 1 and 2 failed (the distinction rate tracks cadence exactly — the author's own kill criterion for the "one scalar, two faces" notion fired), 3 was untestable (blind instrument), 4/5/6 held (boundaries ≈ kicks; memory is the record; ns/event flat). All disclosed honestly, and the failures were converted into the result. By the lab's precedent (1 October law red-team: one failed held-out prediction → silver despite adoption), gold's "held-out predictions held" is not met.

## What would make it gold

Wire the re-anchor on the belt path (recompile only when the accumulated offset reaches √(floor/C), per law.md) and measure: compiles/kick against the 0.05 target, the belt's wall (my attribution predicts ≈1.7×), and behaviour (B9/B12-class invariants on the same belt, many seeds). That converts a priced target into an adopted lever and settles the wall gain.

## What the author missed

- The `bind()` share was one counter away and bounds the headline: 43.7 % of wall, so the re-anchor alone buys ~1.7×, not 20×; "the belt's whole engine cost" overstates.
- No revisit analysis (done here: zero revisits — the claim is stronger than stated).
- One perturber strength only (done here: Saturn also saturates).
- H_live at behaviour scale remains unmeasured: the surviving distinction proxy is the word-scale key flip, which saturates by construction; the record-format question is posed, not measured (today's 448 B BodyRec × 10⁹ = 448 GB vs the 16 B tube floor is the number worth tabulating).
- run.log empty — the pre-registration evidence rests on mtimes alone.
