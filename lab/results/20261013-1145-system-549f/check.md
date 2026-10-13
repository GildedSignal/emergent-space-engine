Grade: silver

Abstract: Claim: one stored acceleration word per binding — written free where the kick already computes `f.accel` (step.rs:669–671) — replaces the per-read re-derivation in `observe::partial` and prices the news payload's `a` slot and the burn generator's second-order piece. Reproduced bit-identically (regen.sh): err median 2.8×10⁻¹⁰ vs shipped term max 2.0×10⁻⁴ on plain scenes; dive err max 1.0×10⁻⁸ at Δa/a ≤ 3.0×10⁻²; light-window staleness 10⁻³ plain, 0.40 on the dive. My attacks hold it (seed 7/400 members, 16 s dive to β 0.49, fwd L15). But the 81%-of-readout gain is cited from 51bf, not re-measured; the word is priced, not wired. Adoption: one store at the kick, one read rule, delete `partial`'s `step()` closure; strong field and the word's width unpriced.

## Reproduction

`regen.sh` exit 0, re-run by me: every census number bit-identical (all three flights, all stats, worst-read tables). Code facts verified in the shipped tree: `step.rs:669–671` computes `f = force::field(...)`, uses `f.potential` for the weight and `f.accel` for the impulse, discards the acceleration; `observe.rs:145` re-derives the same doll-chain field per read inside `partial`'s ~10-line `step()` closure; `observe.rs:41–101` (`credit`) ramps the stored quantized `kick.dv` with no field evaluation — the structural finding (two mechanisms, one storing, one re-deriving) is real. My re-implementation control (env-parameterized copy of the probe) reproduces the rev flight exactly (6,101 reads, identical stats).

## Predictions

`predictions.md` mtime precedes the probe and dossier by 7–8 minutes; cases genuinely not tuned. P1 held. P2 failed the interesting way (the predicted read-window break never came — max Δa/a 3.0×10⁻²) and is honestly reported. P3 failed in magnitude (predicted ≤10⁻⁶, measured 6.3×10⁻⁴ median, 0.40 dive). P4 verified. Two failures against the author's own guesses are strong evidence the predictions were held out — but by the letter, the held-out predictions did not all hold, which alone bars gold.

## Attacks (one outside the author's range)

1. **Seed 7, 400 members, rev L15** (8× bodies, new seed — outside the range): the term itself grows 37× (p99 5.8×10⁻³, max 7.6×10⁻³ doll units) — the term is no longer plainly invisible, so keep-vs-delete is live inside the plane, not only in strong-field dolls — yet the word still tracks it 4+ orders below (err max 3.7×10⁻⁷, Δa/a max 3.0×10⁻², 0% over 1). Claim holds.
2. **Rev L15 held to 16 s** (the next decade of duration; 174d checker2's territory): dive deepens to β 0.49, r 1.02×10⁸. Read windows still safe (err max 2.4×10⁻⁸ vs term max 8.1×10⁻⁴, Δa/a max 1.5×10⁻¹, 0% over 1). But the light-window staleness grows 0.40 → **0.80** — the author's "0.4 at the handoff" is not the regime's ceiling; a slightly deeper dive crosses 1. The refresh-at-rebinds rule is confirmed and sharpened.
3. **Fwd L15, 16 s** (author tested forward only at L8): β 0.49 the other way; Δa/a max 2.8×10⁻², err max 2.4×10⁻⁸. Holds.

## Novelty

Not a repetition. 7b86 (itself pending) named the three-consumer convergence and priced *pure deletion* (the term's own invisibility); this run prices the *stored word* — the substitution error (new), the light-window freshness constraint for r-news (new; 7ab4's open direction 1 gets a design rule it did not have: the carried word cannot be ridden across a light window on a dive), the free write (new code fact), and the `credit`/`partial` unification (new). The old "stored-a" line (H0115–H0119) is the pre-pivot `emergent-coupled-response` overlay — a different representation; citing it, the idea's *shape* has prior art but not on the tube/doll representation.

## Page

Faithful to the evidence; two corrections made in place: the light-window 4.0×10⁻¹ is depth-growing, not a ceiling (checker 0.80 at β 0.49, 16 s), and the deletable scope is the ~10-line `step()` closure, not ~35 lines (the gates and base resolution stay for the word read; the ~35 was inherited from 7b86's phrasing).

## Goal fit

Moves the shared slot of three named board bottlenecks (view, gravity-news, frame-cost) and is exactly PRINCIPLES 6 ("Store the generator, not the generated") and 3 ("Nothing is evolved that can be derived when looked at" — here the converse: nothing re-derived that the law already computes). But it moves no gate, deletes no component yet, and its headline gain is borrowed: not gold.

## The one experiment for gold

Wire the word: store `f.accel` (quantized like `kick.dv`) on the binding at `kick_clock`, read `Δx = a·τ²/2` in `partial`, delete the `step()` closure — then measure the readout/frame gain on the shipped bench (7b86/51bf's 81% says ~2× the frame) and digest identity, plus the strong-field standalone probe (r ≲ 20M, 7ab4's oracle) pricing the refresh cadence against one-word-per-read.

## What the author missed

- **The free write is half a step staler than the census's word.** The kick computes `f.accel` at the kick tick `t`, but the next window's boundary is `t + full/2` (step.rs:704); the census prices `a(B)`, the freshest possible word. The buildable free word is `a(B − len/2)`, so the real err is up to ~2–3× the census's — margins survive (4+ orders plain, 7+ vs the quantum on the dive), but the wired build should re-derive the price. Writing at `boundary_clock` instead would cost one field eval per step (it runs none today).
- **The light-window staleness is a trend, not a value**: 0.40 (8 s, β 0.25) → 0.80 (16 s, β 0.49) on the same flight; the page now says so.
- **The term is already visible at another seed** (37× at seed 7/400 members): the strong-field caveat understates that the keep-the-term rationale is live within the plane itself.
- **The multiplicity consumer** (named in the lens) stays unpriced: many reads between a body's kicks all get the same word; no census of reads-per-kick per body.
