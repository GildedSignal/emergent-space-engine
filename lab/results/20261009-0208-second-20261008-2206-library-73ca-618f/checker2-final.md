Working...
Check complete. `check2.md` written: **Grade: silver**.

**What held (reproduced exactly):**
- `analyse` over the shipped series regenerates `b12_alpha.json` byte-identically; full `law sym-sched` and `select --candidates 60` reruns regenerate `seeds.json` and both series **bit-for-bit** — the record is fully regenerable on this machine.
- All dossier table numbers match the logs; predictions.md predates the decisive artifacts; all four predictions held. Bounded plants verified genuinely bounded (mean error 7.35e-6 → 7.37e-6 across 10⁴ orbits).
- α-profile separation as claimed: 0.00–0.01 (32/32 bounded) vs 0.94–1.22 (32/32 compounding).

**Why not gold — the strawman:** the headline "B12 v1 false-kills 21/32 bounded seeds" was measured against an invented "[1,10⁴] running-max window" statistic. The shipped gate (`xtask/src/behave/fit.rs`) drops the first 10% and uses per-window maxima; my faithful port on the author's **own series** reads 0/32 false kills and convicts 32/32 compounding — the shipped v1 separates these plants as well as the α-profile does. v1's real documented failure (state-dependent bounded error reading 0.3–0.6, probe P2) is a plant type this run never contains.

**Adversarial findings:** a bounded law with its dt/4→dt switch at orbit 3000 instead of 300 (final 2.4e-5, passes the level bar) is **falsely convicted** at α_top +1.06 — "conviction is safe" is falsified; delayed-onset leaks need true α ≳ 0.4 to convict (stated floor 0.1 understates ~4×); a 0.15/decade creep escapes both type and level.

**Gold experiment named:** plant the state-dependent bounded error that actually breaks the shipped `fit::growth_exponent` and show the amended α-profile acquits it where the real v1 convicts.
