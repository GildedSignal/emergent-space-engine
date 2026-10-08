Grade: lead

**Abstract.** The author claims per-chronon contacts stay Poisson only at small scale, with Fano growing with N (gas 1.2→30.5 at fill 0.2; stock battle 1.7→40.2) — a missing smoothness gate. Every number reproduces bit-for-bit, but the two falsifiers the author named and did not run kill the headline: a grid-free, rejection-sampled gas at matched density gives Fano 0.93 flat (n=4096/16384, vs 6.4/30.5 on the lattice), so the gas growth is the generator's crystal start; the battle growth is the synchronized crossing transient inside a nonstationary window (second-half Fano 1.2–3.2, not growing; 4× velocity scatter → 7.7), while the allocator's own quantities stay thin (ops p99/p50 ≤ 2.8, max/p50 shrinking 29→13). The law is Poisson-smooth where it flies; no gate is missing. Energy non-drift verified (equal-mass cradles exact to 10⁶ ticks) but its instrument is not in the patch.

## Reproduction record

Applied `work/patch.diff` to a clean tree; `cargo test --release -p emergent-lattice-event` builds in 8 s.

- `gas_packing`: all 13 rows identical to the dossier (Fano 0.98/1.10/1.14 at fill 0.05; 1.20/6.44/30.53 at 0.2; 12.35 at 0.4/4096; p99/p50 1.17–2.05). 28 s, 32 MB.
- `battle_front_scaling`: identical (Fano 1.72/3.54/13.58/40.22; p99/p50 2.79→1.31; contacts/body 4.7/9.2/18/27). 7 s.
- `instrument_control`: flat 0–10 ops/tick, max_batch 0. Passes.
- `inst_check`: EventCore ≡ Chronon, same digest and fired count at ticks 300–1700; Chronon pays 5.8× the ops. The identity control is real.
- The author's `fleets()` is a line-faithful copy of `engine/src/scenes.rs::battle` (formation=false); I diffed them by eye. The "engine's own scene" framing is honest.

## Adversarial cases (mine, each < 35 s)

1. **Grid artifact — the author's named falsifier, unrun by them.** Same box, radius, speeds, walls and nominal fill 0.2, but uniform rejection-sampled placement instead of `worlds::gas`'s grid (which at fill 0.2 is a *perfect* lattice: cell 3, jitter 0, local packing π/9): **Fano 0.93 at n=4096 and 0.93 at n=16384** (grid: 6.44/30.53). No growth with N whatsoever. The gas half of the claim is a generator artifact, not dynamics.
2. **Finite size.** n=65,536 at fill 0.2: Fano 49.0 — still growing but the exponent is collapsing (0.84 per 4× in N up to 16k, 0.35 after). Moot given (1).
3. **Battle nonstationarity.** n=25,600 stock, window split: all-window Fano 40.2 (reproduces), **first half 30.5, second half 3.2**; at n=1600/6400 the second halves are 1.6/1.2 — the post-front process is Poisson at every N. With 4× velocity scatter (front de-synchronized): all-window 7.7, halves 6.2/8.6. The "Fano 40.2" is quiet-approach + burst + dispersal mixed in one window: a statistic-of-window choice, not a frame tail.
4. **The allocator's actual quantities** (OC#36's p99): ops p99/p50 ≤ 2.79 at every N and *max*/p50 shrinks (29→18→14→13). The absolute crossing spike grows ≈ N^0.5 but so does the median. Nothing here eats a frame.
5. **Energy** (the dossier's numbers are regenerable by no shipped code — the instrument is in neither patch nor tree): my throwaway reproduces the claims qualitatively: gas(1024, 0.05), 3600 chronons, E/E0 = 0.99988 (Newtonian), 0.99676 (Relativistic), 0.99577 (V1); equal-mass cradle to 10⁶ ticks exact (1.000000, all three laws); unequal 1-vs-4 bounded, same sign pattern (+0.3%/−5.5%/−4.4% vs the author's +1.4%/−8.9%). No runaway. But per the taste log (5 October: "results that the shipped code could not regenerate"), these numbers cannot carry a grade.
6. `max_batch` (pairs, not connected components — the author flags this) does grow ≈ N^0.75 (34→122→407) and survives 4× scatter (351). If a future connected-component probe shows one indivisible cluster at the front, that is the surviving kernel; today it is unmeasured.

## Predictions

`predictions.md` predates the dossier (mtime 9 min earlier vs written-now dossier) and the scorecard is honest: P1 failed at fill 0.2, the Fano growth in battles was *not* predicted ("I predicted thin tails at all n"), P3 declared not-run and no claim made. Prediction discipline: good. But the honest scorecard already said the central result was unpredicted; my controls then remove it.

## Novelty

No H entry measures contact-rate tails, Fano or per-chronon smoothness on the lattice-event core (215 entries scanned; nearest are the event-core premise lines in `crates/lattice-event/src/lib.rs:38,64` — "a stale slot only costs a spurious wake-up"). The measurement is novel; the conclusion inverts.

## Goal fit

Board #4 (smoothness, OC#36). The run does settle the question it posed, in the collapse direction the author themselves priced in: "this collapses to 'the contact law is Poisson-smooth everywhere reachable' — a premise confirmation, still worth one line in the board." My controls (1) and (3) force exactly that collapse. A premise confirmation with a control-solid instrument is a lead, kept: the next smoothness run should start from the grid-free control and the second-half window, not from the grid gas.

## What the author missed

- The two falsifiers named under "What would make it wrong" were one `cargo test` away each; running them before the dossier would have inverted the headline claim in the author's own hands. Naming a kill test is not running it.
- `worlds::gas`'s fill is nominal only: integer cell division makes fill 0.2 a zero-jitter crystal at local packing 0.35, and fills ≥ 0.4 collapse to packing 0.785. The disclosed "genesis degeneracy at fill ≥ 0.4" is the mild end of a quantization that also taints the 0.2 rows the claim rests on.
- The energy instrument was left unshipped after the 5 October taste-log entry made that exact failure mode a named grade-killer.
- The battle window is nonstationary by construction; an all-window Fano on it cannot measure a steady-state tail.
