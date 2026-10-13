Working...
Check complete — `lab/results/20261013-1145-system-549f/check.md` written, grade **silver**.

**What I did:**

1. **Reproduced** — re-ran `regen.sh`: every census number bit-identical across all three flights (coast/fwd/rev, 5,760/5,760/6,101 reads, all stats and worst-read tables). All four cited code facts verified in the shipped tree: `step.rs:669–671` (kick computes and discards `f.accel`), `observe.rs:145` (per-read re-derivation), `credit` (observe.rs:41–101) ramps the stored `kick.dv` with zero field evals — the structural unification finding is real.

2. **Predictions** — `predictions.md` predates the probe/dossier by 7–8 min; P1 held, P2 and P3 failed against the author's own guesses (honestly reported) — genuine held-out work, but by the letter not all held.

3. **Attacks** (one outside the author's range, via an env-parameterized copy of the probe):
   - **Seed 7, 400 members, rev L15**: term grows 37× (p99 5.8×10⁻³) — keep-vs-delete is live inside the plane — yet the word still tracks it 4+ orders below.
   - **16 s dive** (β 0.49): read windows still safe (err max 2.4×10⁻⁸), but light-window staleness grows 0.40 → **0.80** — the author's handoff number is not the ceiling.
   - **Fwd L15 16 s** (author tested fwd only at L8): holds (Δa/a max 2.8×10⁻²).

4. **Why silver, not gold**: reproduced and novel (prices the word's substitution error, the light-window freshness rule for r-news, the free write — 7b86 priced only pure deletion and named the convergence), but the 81%-of-readout gain is cited from 51bf, the word is priced rather than wired, and the strong field is unmeasured. The one experiment: wire the word (store at `kick_clock`, read `Δx = a·τ²/2` in `partial`, delete the `step()` closure), measure frame gain + digest identity.

5. **Page corrections** (in place): light-window staleness marked depth-growing with my 0.80 measurement; the "~35 lines deleted" narrowed to the ~10-line `step()` closure (gates stay). Also caught in the check: the *free* write lands at the kick tick, half a step before the boundary B the census prices — real err up to ~2–3× the census's, margins survive.

My probe variant was removed; the tree carries only `regen.sh`'s own `a_word.rs`.
