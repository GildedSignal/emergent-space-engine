Working...
Check complete. **Grade: silver** — written to `lab/results/20261014-1010-quant-036c/check.md`.

**What I did:**
- **Reproduced** from `work/patch.diff` in a pristine tree: digests bit-identical on/off at every arm, search −38…−60% µs/call, suite green with the guess forced on. The runner's and fixer's regens agree.
- **Attacked past every author edge:** held-out seeds 11 and 5, 8,000 and 16,000 members (2–4× the author's max) — all identical, search −40%, `refused 0`. Plus a per-call equivalence probe (a build asserting guess-answer == plain-bisection-answer on every call): 5,875 calls, **zero mismatches** — closing the hole where a differing crash tick past the digest cut would hide.
- **Found what the log contradicts:** the m4000 off arms were load-inflated in the author's run (search 151 vs 112 µs, leaver 531 vs 364 µs), so the claimed −29.7% battle-pace leaver win is not real — at battle pace even dipping leavers move ~0; and the suite is 77/0/3, not "26 passed, 1 ignored" (the first six targets only). Corrected both on the page, added a checker paragraph.
- **Why silver, not gold:** the run's own frozen kill rule — made-kick median <10% at m4000/s3 kills — fired (−3.6…−5.4%), and the hit-rate prediction (≥60%) failed at 0.45; the author disclosed honestly but reframed instead of taking the kill. The lever itself is real, certified, cheap, with no measured downside anywhere — worth about half of quant-1845's priced −45%/kick, and only where kicks pay the search.
- **Path to gold:** kill the miss tail (float-screened predicate or the compiled orbit's analytic crossing as the guess), frozen on the battle-arm made-kick median and hit rate.

Tree restored pristine; `work/patch.diff` untouched; nothing else in the run folder changed beyond `check.md` and the page corrections.
