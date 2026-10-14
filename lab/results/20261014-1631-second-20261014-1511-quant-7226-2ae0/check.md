Grade: silver

**Abstract.** The checker-named experiment holds: the guarded AB-IQI policy (`ES_FP=3`) passes the frozen tail rule — worst 10–18 probes vs ≤ 30 (mean 10.6–11.1 vs bisection's 29.4), probes −62…−64 % at every arm — and digests are bit-identical everywhere, including the OFF arm re-verified by me against a pristine build (flying s3/7/11/42, battle m400). Composed with the warm start: readouts −78…−83 %, flying leaver −43…−47 %, savings add. Held by me outside the author's domain: seeds 42/99 at both paces, a 16 s horizon, rtf 10, composition at new seeds, `ES_FP` edge values. Silver, not gold: the pre-registered P2 battle-median cut (≥ 15 %) measured ~0 % — a miss by the author's own counting rule — and the end-to-end gain is ~1.9× on the flying kick, under the 10× bar. Adoption: flip two env defaults.

## Reasons

**1. Reproduced, from my own build.** I applied `work/patch.diff` to a clean tree, rebuilt, and re-ran the regen arms: every count and digest matches `regen.log` exactly (s3 fly OFF 802/23,552/32 → P3 802/8,589/14, digests `36637e67`/`f282c907`; ladder 35,621/57, 9,810/13, 8,709/11; battle 91,323→34,318, worst 28→12; suite 11/11). Wall columns sit inside the dossier's stated wobble. The prior run's secant kill row regenerates exactly (P4).

**2. OFF = shipped, verified against a pristine build, not just the prior checker's word.** The patch carries one unconditional edit (0b85's Crash-retain removal in `rebind`) plus the `next_impact` restructure, so I reverse-applied the patch and built pristine: digests identical at flying s3/s7/s11/s42 (`36637e67`, `cf58ac6e`, `164d6547`, `b089fe3a`) and at battle m400 (`ce552bb4`, 0 searches — the m4000 battle scene exists only through the patch's `ES_MEMBERS` bench unlock, so its OFF reference is necessarily patch-internal; the dossier claims pristine verification only for the three flying digests, which is honest). Identity of the ON path is structural (integer predicate on a monotone bracket, probes strictly interior) and empirically total: ~30 arms across author/regen/me, zero digest differences, refused 0.

**3. Held-out predictions: four of five held; P2 half-failed, honestly.** P1 held (worst ≤ 18 everywhere, incl. my new arms' ≤ 15, vs promised ≤ 20; mean ≤ 11.13 vs ≤ 15). P3, P4, P5 held everywhere, P5 including my composition arms at seeds 42/99 (warm+P3 < warm alone < P3 alone < shipped; worst 32→10–12). P2 held at flying (−34…−39 % ≥ 25 %) and failed at battle: predicted ≥ 15 %, measured −0.1…−0.2 % at the median. The author pre-registered "count it as a miss against the gold condition if < 25 %" and reported it as a miss — that binds. The offered mechanism (the battle median leaver carries no search; the descents sit in the 2,064-of-3,096 dipping minority; the saving lands at all-kick p99) is credible arithmetic and my data shows its signature (battle medians flat to 0.1 µs while p99 falls), but it is counter arithmetic, not a per-kick trace (the author says so in The lens). Timing: predictions.md (16:47:28) sits between the tuning arm (16:46:32) and the held-out arms (16:47:36+); the composition arms (16:53) are after. The wrongly-predicted battle result is itself evidence of pre-registration.

**4. Attack (my own cases, three outside the author's domain).**
- New seeds 42/99, flying: 25,243→9,028 (−64 %), 29,875→10,868 (−64 %), worst 30→12 / 33→15, leaver 203.6→133.7 (−34 %) / 183.7→111.8 (−39 %), digests identical.
- New seeds 42/99, battle: 87,175→32,891 and 87,682→33,027 (−62 %), worst 28→12, digests identical, medians flat as claimed.
- 16 s horizon (2× searches): worst stays 14, probes −64 %, digest `558b40b3` identical — the tail does not grow with run length.
- Untested pace rtf 10: 7 searches, 145→51 probes, worst 27→9, digest identical.
- Env semantics: `ES_FP=""` and `=0` are OFF exactly; `=5` (undefined rung) behaves as policy 2, digest identical, no panic; `=abc` silently means policy 1 (secant, the killed row), digest still identical.
- Composition at new seeds: s42 fly 4,399 probes (−83 % vs shipped), worst 10; s99 fly warm-only 5,690 → warm+P3 5,032, worst 32→12; digests identical.

**5. Novelty.** The frame-cost page's Open direction 1 (from the prior run's checker) names exactly this experiment: AB/inverse-quadratic with a tail guard, then the warm-start composition. Not a repetition — it supersedes the prior run's "naive policies killed" with the surviving, now-guarded policy and regenerates its kill table from the patch. No other wiki page or H entry claims it.

**6. The page.** Faithful in substance; I corrected three overstatements in place: the composed readouts/search range (battle is 6.5–6.6, not ≤ 6.3), the battle p99 cut (−1…−18 % across runs, the wobbliest column, not a stable −13…−14 %), and "off = shipped verbatim" (now records the pristine re-verification, the patch-internal m4000 reference, and the unconditional retain removal).

**7. Goal fit.** Board line 3 (the kick vs the ~50 ns floor), PRINCIPLES #1 "the cheapest compute is compute not done" and #13 "errors never compound" (the integer predicate decides every step; digests identical by construction and measurement). The search's ~29.4 readouts fall to ~4.9–6.6; the remaining kick is the bind half, correctly left untouched and named as the next term.

**Why not gold.** (a) One pre-registered held-out prediction failed, by the author's own counting rule; the 1-October precedent (one failed prediction, honestly reported → silver, adopted) applies exactly. (b) The moved quantity is ~6× on the search term and ~1.9× on the flying leaver kick (199→105 µs; battle median ~0) — real and adoptable, but under the 10×/component-deletion/premise-refuted bar; the prior run had itself already named AB as the probable survivor, so no standing premise falls.

## The one experiment to gold

Per-kick probe attribution at battle pace: instrument the bench to attach each search's probe count to its kick sample, and show the median battle leaver carries 0 probes (the criterion-artifact reading made a measurement instead of counter arithmetic). With that clause corrected on evidence, every pre-registered claim holds at every arm — or the integrator adjudicates the both-pace median clause as an instrument artifact now, on the r2/r3 precedent, and the record stands.

## What the author missed

- The battle-median mechanism was never traced to individual kicks (self-admitted); the p99 claim rests on the wobbliest instrument column with no machine-state guard on the comparison.
- `ES_FP` with an unparseable value silently selects policy 1 (secant, the killed row) via `unwrap_or(1)` — a new footgun of the family the last checker's note closed; it should mean OFF or error. Harmless to correctness (digest identical), misleading to a re-measurer.
- The m4000 battle scene has no pristine reference by construction (shipped clamps `--members` to 400); the dossier could have said so instead of leaving the reader to discover which digests the pristine claim covers.
- The equality test still covers only the plane's handed-out ships and two surfaces; the `next_exit` fast path (Illinois + vertex quadratic) remains inherited and unexercised (0 searches in every arm, mine included).
- The "~4.9–6.3 readouts/search" range understated the battle arm (6.5–6.6) — corrected on the page.
