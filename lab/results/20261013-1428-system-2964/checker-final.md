Working...
Check complete. **Grade: silver** — written to `lab/results/20261013-1428-system-2964/check.md`.

**Reproduction** (regen exit 0 + my own runs): end |v|/c to 6 digits on every flight, refusal counts exact, coast digests identical across arms, ship≡unset equivalence verified; wall-dependent counts (pitems, lag) within a few percent. Applied `work/patch.diff` myself (clean, 10 s build), then restored the tree to zero changes.

**Adversarial cases** (3, one outside the author's range):
- **32 s flights** (next duration decade): claim's structure holds — items collapse (2,233→15 at L8), lag(off)=0.038 s everywhere, refusals grow to 151, all faults still the velocity word. Two new behaviors the author missed: retrograde off lands **47.8% low** (the 8→16 s improvement 6.6%→0.5% is not a trend), and pburst(off)=11–14 off-prograde (P1's "burst=1" is prograde-only at longer durations). Both *strengthen* the deletion-is-broken half; folded into the page.
- **Seed 7**: counts and 6-digit end speeds identical to seeds 1/3 — level-set confirmed.
- **f8 16 s** (the arm regen never re-ran): **digests bit-identical** to the author's held-out run.

**Novelty**: the carry lever was already on the page (174d/0f2a); new here is the measured answer to the page's own open question (the word-margin does *not* survive readout — deletion refuses), the refine alternative dead (lag invariant to sampling; ~1% error stands at any cadence), and the priced contract. Mechanism verified in code: step.rs:51 comment, :402 refusal site, `thrust::owed` closed-form.

**Page corrections** (in place): "27–230×"→19–204× (7–71× retrograde/turn; the original had no anchor in the tables), "4–8×"→4–14×, envelope corrected to 4.2e-2 at 16 s, "7–10% low"→single point ~7%, plus the 32 s non-monotonicity note.

**Why not gold**: the contract's central clause — the word can *step* its exponent instead of refusing — was testable as a one-arm spike in the same probe and wasn't run, and no frozen gate was consulted on the ~1% error or the envelope (PRINCIPLES 34). The 19–204× gain is priced, not demonstrated. That spike is the one named experiment to gold.
