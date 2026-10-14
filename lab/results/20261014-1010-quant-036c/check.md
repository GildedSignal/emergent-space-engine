Grade: silver

**Abstract.** Built and certified: threading the prior tube's found impact through `rebind` as a guess for `next_impact`'s bisection (`ES_IMPACT_GUESS`, ~20 lines, default off) is bit-identical everywhere — every arm pair, my fresh seeds 11 and 5, 8,000 and 16,000 members, and a per-call equivalence probe (5,875 guess-carrying calls, zero answer changes) — and halves the crash search itself (−38…−60% µs/call). But the priced win does not land: made kicks move −4…−5% at the battle arm, firing the run's own frozen kill rule; leaver kicks fall −35…−40% at flying pace only (~0 at battle pace — the dossier's −30% cell rode a load-inflated off arm). Adoption: ~20 lines, no measured downside on any arm; roughly half of quant-1845's priced −45%/kick.

## Reasons

1. **Reproduction (complete on the load-independent claims).** The runner's regen and the fixer's verify regen both exit 0 with identical structure; I reproduced by hand from `work/patch.diff` in a pristine tree: digests (canonical and replay) bit-identical on/off at every pair, search µs/call 106–115 → 41–70 across arms, guess shares 0.42–0.71, `refused 0` everywhere, plain build = prof-off digest. Suite green with the guess forced on.

2. **Adversarial cases, past every edge the author tested.** (a) Held-out seed 11 at m4000/rtf1: identical digests, search 111→67, share 0.45. (b) Held-out seed 5 at m400/rtf100 (flying): identical, leaver 193.5→115.2 (−40%), share 0.71. (c) 8,000 and 16,000 members (2× and 4× the author's max, matching quant-1845's checker extreme): identical, search −40%, share 0.45. (d) The strongest probe: a build that recomputes the plain bisection beside **every** guess-carrying call and asserts equality — 2,064 + 3,811 calls, zero mismatches, probe-build digests equal the off arms'. This closes the hole the digests cannot (a crash tick past the cut would not surface in them). The known edge (a turning orbit inside the star) is in the suite, green twice with the guess on.

3. **Why not gold: the run's own frozen criteria fired against it.** Prediction 3 failed outright (hit rate 0.42–0.69 vs ≥60%; 0.45 at m4000). Prediction 2's kill clause — "if the [made] median moves <10% at m4000/s3, the built lever fails its own price: kill" — fired: −3.6…−5.4% in the author's run and both clean regens. The author disclosed both honestly but reframed instead of taking the kill; the pre-registration exists precisely so the price is not re-derived after seeing the data. The physics stands; the priced configuration at the battle arm is dead by its own rule.

4. **Two dossier numbers the log contradicts, corrected on the page.** The m4000 off arms were load-inflated in the author's run (search 151 µs and leaver 531 µs vs 112 and 364 in both regens and all my runs), so the claimed −29.7% battle-pace leaver win is not real — at battle pace even dipping leavers move ~0, because the search is a small share of their 364 µs. And the suite line "26 passed, 1 ignored" is the first six test targets of its own log; the full `--tests` run is 77 passed / 0 failed / 3 ignored. Cloud timings are orders of magnitude only, but a −30% cell presented as a pair delta needs a load control the author did not run.

5. **Novelty.** quant-1845 priced the warm-start bracket (−45%/kick) without building it; this run builds it, certifies identity, and refutes the price's premise (near-total settlement; measured 42–69%). A real increment on the board's third bottleneck (the kick), not a repetition. The page folded the result in faithfully after my corrections; the topic stays open (one gold at most here, and this is silver).

6. **Goal fit.** PRINCIPLES #1 "The cheapest compute is compute not done" — the crossing is derived from the tube the body just had; #2 "Exact means deterministic and reproducible" — bit-identical, per call; #13 "Errors never compound" — no error introduced at all. Follows the codebase's own certified-guess precedent (`next_exit_with`, with its guess-vs-reference test at step.rs:941).

## The one experiment to gold

Kill the miss tail: the ~67–74 µs the 55–58% of misses still pay at battle pace. Either the float-screened predicate (cheap proxy readouts, exact only near the crossing) or the compiled orbit's analytic crossing as the guess (`next_exit_with`'s pattern fed by the anomaly), frozen with criteria on the battle-arm made-kick median (≥30%) and hit rate (≥90%) — the priced win landing at the arm where this run's kill rule fired.

## What the author missed

- **The hit rate was priceable before the arms.** One histogram of the crossing drift |new − prior| per rebind predicts the two-readout settlement share directly, is the tolerance the next guess must survive, and costs one instrumented pass. The lens section says this; the run did not do it.
- **No load control on pair deltas.** Off/on medians compared across a shared box without interleaving or a repeated off arm produced the two artifact cells; the regen caught them, not the author.
- **The prior could survive a chain.** `prior_impact.take()` consumes the immediately-prior tube's crossing on the first `plan_terminal`; an older, still-certified prior (or the last *found* crossing, not the last tube's) might settle more of the misses — unmeasured.
- The suite count slip (26 vs 77): small, but it is a number the log contradicts, and the lab grades on those.
