# Predictions — 20261006-1135-autoresearch-eb29

Written before the decisive (held-out) run. Tuned-on case: seed 1, `universe --kick-bench
--rtf 100 --seconds 30` (the bench the handoff uses). Held out: seeds 2 and 3, same command,
never measured during tuning except as the baseline digests below.

Baseline (instrumented build, Linux x86 cloud box, rtf 100, 30 s):
- seed 1: replay 27fd0a4427a67d31…, made median 36.6 µs, p99 51.4, leavers median 103.9, n=1158
- seed 2: replay 6ce6c53f3f27703f…, made median 36.5 µs, p99 60.6, leavers median 84.8, n=980
- seed 3: replay 5e121398caba0b5d…, made median 36.7 µs, p99 56.5, leavers median 100.5, n=1059

Anatomy measured on seed 1 (per sampled kick, means): rebind 82 µs (of which compile 60 µs,
fit 4.2, remainder 5.3, decode 4.0), secondaries+tide 7.2, readout 3.9, acceleration 1.1.
Compile = ~85% append/quad; ~55 bands, ~63 knots, ~130 quad panels (≈520 `num::cos` ≈ 48 ns
each, ~20% in `div_word` ≈ 18 ns each) per compile; 1125/1158 full-bound, 33 passages, 0
circle fast paths; exact memo hit rate 0% (confirms the 5 October correction), quantized 95.5%.

## Predictions

1. **Bit identity.** R1 (skip the discarded `Residual::between(decoded_event)` inside the
   *universe* bind path) and R2 (hoist loop-invariant shape constants in `weak_quad`,
   pre-size the knot vectors) change no output: the replay digest and state digest on seeds
   1, 2, 3 are exactly the baselines above. The events layer (`crates/space/src/events`),
   which does consume the residual, keeps the residual path.
2. **Gain.** R1 removes one full decode+cartesian per rebind (~3–5 µs of a ~60 µs mean
   rebind): made median −5–10%, leaver median −3–6% (leavers' tail is compile-bound, which
   R1 does not touch), p99 −4–8%. R2 gains a further 1–4% (hoisting saves ~2 of ~90 i128
   ops per node; with_capacity removes ~7 reallocations per compile).
3. **Round decay.** A third micro round (node-path Scalar trimming) gains < 2%: cos and
   div_word are already within ~1.5× of the u64-multiply hardware floor (measured 47.7 and
   18.0 ns), so the loop stops at three rounds per the lens rule.
4. **Ceiling.** Even a perfect bit-identical micro rewrite of the whole quad path cannot
   beat ~−25% on the mean kick: 520 cos + 520 div_word per compile ≈ 34 µs of the 60 µs
   mean compile is irreducible arithmetic at the measured primitive rates.
5. **Held out.** On seeds 2 and 3 the digest stays bit-identical and the median gain lands
   within the seed-1 range (5–10%). If any digest differs, the change is reverted regardless
   of speed.
