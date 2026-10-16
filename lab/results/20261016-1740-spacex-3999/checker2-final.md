Grade: gold**Grade: gold.** Written to `check2.md` (and `checker2-final.md`); the author's wiki page corrected in place at two overstatements.

What I did, and found:

**Reproduction** — regen.sh (runner, exit 0) plus my own runs of the built probe. Every deterministic cell bit-exact across author/regen/my runs: fallback=true in-band at 10³/10⁴/10⁵ both seeds, pass = N−314 (714 / 9,714 / 99,714), zero encounters, Home control kept 8 pass 7, empty belt kept 1, huge-h falls back, sweep band [1.75, 3.0) AU at 10⁵. Timings on the loaded machine (9.9/8 vCPU): per-read 3.96–6.0 µs, inside the author's and cdf0's bands. The probe's loops verified line-by-line against the shipped path (`radial.rs:254` rule, `encounter.rs:162-198`/`:130-154`, `universe.rs:762-773` frame-path capture); belt generator is Rayleigh σ_e = 0.07 ≤ 0.4 as claimed.

**Attack** — three adversarial cases: (1) **N = 10⁶, seed 3**, a decade past the author's range: every law extends — fallback in-band, pass = 999,714 = N−314, per-read flat at 4.17 µs (no cache term), capture 92 ms, 0 encounters; (2) seed 3 at 10³/10⁴: identical; (3) the anomaly margin from a Kepler solve: 0.1401 at e = 0.07 exact, and the exact max runs *above* 2e — the repricing is conservative.

**Predictions** — pre-dated the probe by file times; P2–P5 held, the refuted P1 is disclosed as the result with the claim's own pre-registered kill criteria all passing.

**Novelty** — closes the page's named unmeasured regime; refutes cdf0's "not a belt-scale one" scoping and the cure's "~tens of µs" price. No prior HISTORY entry.

**Page corrections (mine)** — the fallback band's edges move with N (at 10⁶ the inner release is 2.0 AU, and the 1.75-AU window then keeps 170,188 bodies short of the rule — the tail windows are expensive even outside it); "max|ν−M| = 2e" is first-order, not exact.

**Noted for the integrator**: `ENGINE_BUDGET_MS` isn't a symbol in the tree (examples default 12 ms; b = 5 ms is 69f3's frozen bar — verdicts survive either); the 10³ latch margin is thin (2.8–4.3 ms vs 2.5 bar); the probe's answer timing includes a float replica the shipped loop lacks (inflation favours the claim, bounded by cdf0's band). My 10⁶ probe peaked at 2.54 GB RSS — my overrun, not the author's.
