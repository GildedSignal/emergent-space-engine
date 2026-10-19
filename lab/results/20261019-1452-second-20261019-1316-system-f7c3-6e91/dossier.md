# Dossier — the gold rung flown: the gates kill the 11+11 wiring; the belt's rebind CPU was never the wall

## Claim

**The checker's named experiment is done and it refutes f7c3's adoption half: with the served
rebind wired (`ES_QMEMO=1`, 9eeb's `Orbit::from_shared`, exact key carried), B13 fails —
46/64 flybys within 1e-2 against the exact arm's 60/64, worst ΔE 5.93e-1 (28× the exact arm,
59× the band), deterministic across solo, loaded and strong-branch-guarded runs — so the
quantized cell at 11+11 is **not** adoptable as the plane's law; and the measured serve
constants replace the composition: the belt's own exact compile is 4.95 µs (not the cited
104 µs plane-FIT figure), the served hit 0.641 µs (7.8×), so at 10⁹ the belt's rebind stream
is 0.15–0.17 cores compiled → 0.019–0.022 cores served — the CPU row was overstated ~25×, and
the O(1) standing memory (f7c3, unchanged) — not CPU — is the adoption case.**

## Bottleneck

The cell-rebind gold rung as pre-registered by 9eeb's and f7c3's checkers: "wire
`Orbit::from_shared` in the rebind, re-judge B12/B13/B17, recalibrate the 0.9 guard" plus
"the 0.40 µs serve is a composition, not a measurement". All three items are flown here on
shipped code (both prior patches applied verbatim; my additions are a wall-clock counter
around `served()` — identical on both arms, so the OFF arm times the exact compile — and a
`servetime` microbench on the belt's own 99,699 genesis keys).

## Evidence

Commands and full log: `regen.sh` (~12 min; every number below regenerates). Machine: the
lab's shared 8-vCPU Linux box, load 2–4 during the arms.

**The gates (B13 decisive; B12 broken instrument, B17 un-runnable here).**

| arm | B13 verdict |
|---|---|
| exact (shipped law, patches inert) | FAIL 60/64 within 1e-2, worst ΔE 2.12e-2 |
| **clean tree (patches stashed)** | **FAIL 60/64, worst 2.12e-2 — bit-identical** |
| served (`ES_QMEMO=1`) | **FAIL 46/64, worst ΔE 5.93e-1** |
| served + strong-branch exact guard (`ES_QWEAK=1`, od 4) | FAIL 47/64, worst 5.92e-1 |

- The exact arm's red is pre-existing on this box (B12's documented libm disease, a8cd: the
  corpus fails for the exact law itself), and my patches are float-inert in it (clean-tree
  control identical). B12 reads text-identical `worst err inf` on both arms (its corpus
  assessment never reaches the law); B17 times out at the frozen 60 s limit on both arms,
  solo — no signal from either. B13 is the one gate that discriminates, and it discriminates
  against serving: −14 draws, worst ×28, reproduced three times including solo.
- **Mechanism (per-draw diagnostic):** 20 draws outside 1%, spread across q = 2.3–44.5 R_p —
  far, weak flybys as much as close ones — every draw `alive, refused 0, lost 0`, and
  **ΔE ≡ ΔL to 3 digits on nearly every draw**: a common-mode phase offset through the
  encounter window, not a dynamics error. The serve's ≤2⁻¹¹ period shift accumulates along
  the ~300–800-kick approach and moves where the ship meets the planet. The strong-branch
  guard does not help: the failing keys are weak-branch (the guard changed nothing).

**The belt stream under serving (10⁴ and 10⁵, seed 1): serving does not move it.**

| arm | belt recurrence | belt cells | kicks (10⁴) |
|---|---|---|---|
| 10⁴ exact / served | 0.9510 / 0.9509 | 1,425 / 1,429 | 167,262 / 167,262 (identical) |
| 10⁵ exact / served | 0.9913 / 0.9917 | 1,731 / 1,736 | 296,470 / 318,259 (wall-limited arms) |

**The measured constants (the composition replaced).**

| quantity | exact | served |
|---|---|---|
| belt keys, microbench (99,699) | 4.95 µs/compile | 0.641 µs/hit (1,732 cells) |
| live mixed stream 10⁴ | 4.87 µs/call | 0.759 µs/call (hits 99.1%) |
| live mixed stream 10⁵ | 5.71 µs/call | 0.769 µs/call (hits 99.6%) |

- Belt rebind rate measured: 3.04–3.36×10⁻⁵ rebinds/(body·game-s) (10⁴–10⁵, both arms) —
  consistent with 0659's cited 3.6–4.3.
- **10⁹ row, measured constants:** 30–34k rebinds/game-s × 4.95 µs = **0.15–0.17 cores
  compiled**; × 0.641 µs = **0.019–0.022 cores served** (+ 1.6–1.8k one-time builds, the
  birth cells, amortized to ~0). f7c3's
  "3.7–4.5 compiled cores" priced the belt's stream at the plane scene's 104 µs FIT compile;
  the belt's own compile is 20× cheaper, so the CPU deletion is 7.8×, not ~100×.

**The guard.** Served-plane recurrence 0.898 (9eeb's figure, reproduced); served-belt
0.95–0.99 (above). `memo.rs`'s 0.9 guard recalibrated to **0.85** (comment in the patch: the
guard catches write-back, not cell count) — passes on both arms; `qmemo.rs` untouched and green.

## Predictions

Written before the decisive arms (`predictions.md`). **P1 refuted — the kill criterion fired:
any gate FAIL = not adoptable at this width.** My "all three PASS" prediction was wrong: the
error band ("within 3× of OFF") was violated 28× on B13's worst draw, and B12/B17 yielded no
signal (broken / un-runnable instrument here — the prediction assumed a working instrument).
P2: cells ±3% held (+0.3%), fire rate within 15% held (−5%), but the recurrence point (≥0.97)
read 0.9509 — the miss is the exact arm's own value (serving delta −0.0001). P3: serve ≤2.5 µs
held (0.641–0.77); the compile band (60–140 µs) and ratio (≥30×) **missed — and the miss is
the finding**: 4.95 µs, 7.8×. P4 held (0.85 both arms green). Three substantive misses, each
reported as a correction, none tuned around.

## What would make it wrong

- B13's exact-arm red is this box's libm (4 draws outside); on the M1 both arms may sit
  lower, but the ON−OFF delta (−14 draws, ×28 worst) is deterministic and law-caused, not
  machine noise — the same corpus, the same 9 replaced draws, both arms.
- If the width ladder's error scaling is linear in cell width, B13's band needs ~6 more
  fraction bits (11→17) at the plane; if the encounter amplification is superlinear near
  grazing draws, no width fixes it. Unmeasured — the successor experiment.
- The serve-cost constants are Linux/x86 orders of magnitude (PRINCIPLES: cloud timings);
  the 7.8× ratio is instrument-internal (same timer both arms) and should transfer.

## Adoption cost and fit

The belt-scoped memory claim (f7c3's core, the O(1) standing set) survives untouched: the
served belt stream is the exact arm's stream (recurrence, cells, 10⁴ kicks identical).
What dies is plane-wide adoption at 11+11. Cheapest surviving shape: serve the belt's keys
only (a population the B13 scene never flies), or step the ladder and re-fly B13 first.
PRINCIPLES 19 ("a fix signals the wrong representation"): the assist's 59× amplification of
a 2⁻¹¹ phase shift says the *encounter*, not the cycle, owns the width — the same reading as
the page's resonance-guard open direction. PRINCIPLES 2 ("behaviours matter, not continuum
fidelity: error type over error size") cuts the other way for the plane gates: the band is
the frozen law, and it fails.

## The lens

The whole-system read: the rung's three named items were one question — does the wiring fly?
— and its answer rearranges the value: the CPU half of the headline was priced on the wrong
scene's constant (20×), the memory half stands, and the gate that works says the cell's width
is set by encounters, not by cycles. My blind spot: I predicted the gates green from 9eeb's
weak-cycle error figures and did not weight that an assist is a phase amplifier; the
pre-registered kill criterion is what kept the miss honest.
