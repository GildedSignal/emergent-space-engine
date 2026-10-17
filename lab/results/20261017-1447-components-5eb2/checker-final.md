Working...
Check complete. **Grade: silver** — written to `lab/results/20261017-1447-components-5eb2/check.md`, with the author's wiki page corrected in place where it overstated by omission.

**What I did:**

1. **Reproduced** — the runner's `regen.sh` exited 0 (parity bit-identical on `ladder_digest`); my own fresh `git apply` + re-flights matched every headline number: kick 44.0-45.2 µs (claimed 46.3), FIT 45%, census 84,254/31,652 to the digit, bind bench 17.3 µs, `div_word` 2.8 vs wide 22.3 ns, compile 4.4 µs belt. The FIT stage and the standalone bind bench agree — the decomposition's strongest internal check.

2. **Three adversarial cases, all strengthening, none breaking:**
   - **N=10⁵** (outside the author's range): census concentration grows to **27.9×** (98.6% shared); FIT/kick 47%. Side finding: the clock comb doesn't fire in-window there.
   - **rtf 100** (below the tested range): **24×** (99.2%).
   - **The run's own named unknown — cache invalidation**: I built a content-hash probe over the returned `Vec<Secondary>` per normalized `(doll, tick, except)` key: **0 of 292,864 calls** across three arms had changed content at a repeated key. The proposed cache would have been bit-identical everywhere flown. (Print-only, prof-gated; tree restored clean.)

3. **Why not gold**: the census is genuinely new (it answers d959's named "unflown" question), but the headline "priced from the inside for the first time" does not survive the record — **5ade** decomposed the wave kick yesterday (fit 41%/sources 23%) **and killed a source memo on the spread belt (0.029)**, a regime this run never flew and never engages; **c4d3** already timed the compile at true belt keys at the same 4.4-4.5 µs; **a765** measured the rebind at 84-87%. No 10× moved; the b063/a765 tension is opened, not resolved.

4. **Gold experiment named**: fly the `except`-normalized `(doll, tick)` cache digest-identically on *both* regimes — plane steady arm and the wave/birth-crest belt. One flight decides whether direction 1 lives for the 10⁹ ledger or is plane-steady-only.

Also flagged for the author: the cache key must normalize `except` (planet-self events), and the "re-runs move timings ≤5%" claim fails on the held-out arm's FIT (30.4→25.6 µs).
