Grade: gold

**Abstract.** f82a closes 3294's named gaps and refutes the tail third of its "one dial": the belt's fired impulse is 2⁻²³ of body speed (p01 2⁻²⁴, p99 2⁻²⁰, n = 99,712; identical at 10⁴), so at the 2–8 kicks/orbit floor a kick carries 2¹⁶–2¹⁸ word units — the quantum gate cannot bind anywhere the behaviour gates pass. A genesis hash-stagger (~15 lines, env-gated, bit-identical off) flattens the fire train to uniform (246.6 → 13,904.8 s = 0.49·I; rate 1.000, distributions unchanged) and deletes the 10⁵ tail (over → 0, held 154 → 1, lag → 0; my 10⁵-burn re-flight: worst frame 820 → 35.5 ms, 23×). Everything deterministic reproduces to the digit. Adoption: one M1 step — the B-gate delta flight.

## Reproduction

Runner's `regen.sh` (exit 0) plus my own flights (commands below). Every deterministic number in the dossier regenerates exactly:

- Baseline = 3294 to the digit: 29,143/29,143 fired, all dv ≥ 2⁷; interval median 28,142.3 s (3294: 28,141.5); wave-1 246.6/1,101.7 s (3294: 246/1,099); 10⁵ 99,712/99,712; burn census = coast.
- Dimensionless: ship/root median 2⁻²³, p01 2⁻²⁴, p99 2⁻²⁰ at 10⁴ and 10⁵; ship/child 2⁻²⁶/p99 2⁻¹⁴; moon 2⁻¹³; player 2⁻²⁹. Exactly as claimed; word unit ≈ 2⁻³⁰ of speed.
- Stagger: rate 1.000 in **seven** independent arm-runs (mine included: 23,178/23,178; 66,217/66,217 at 10⁵; 51,607/51,607 at 2× horizon), all dv ≥ 2⁷, dv/dim buckets match baseline, dead 0, refusals 0, catalogue 10,076 = bodies + 48 everywhere. Wave-1 13,904.8 s = 0.494·I, wave-2 same.
- Digests: coast baseline ×3 identical `d5bc72b7…`, coast staggered ×2 identical `5f3e8b42…`, different across arms — the author's hashes exactly.

## Numbers that differ (all recorded)

1. **Stagger total fires are wall-horizon-dependent**: author 22,995–23,205; my regen 21,854 coast / 23,100 burn; my re-flights 23,178 / 66,217 / 51,607. Per-interval rate 1.000 in every run — covered by the author's horizon-edge disclosure (fires/body 2.4 vs 3.0 checks out arithmetically against a 2.8–2.9-interval horizon).
2. **Burn digests were stable in my regen** (bb1 = bb2 = `1f2b1d89…`; bs1 = bs2 = `c3686195…`, the author's own leftover `bs2.txt` agreeing) — the "run-unstable" disclosure is over-conservative, in the strengthening direction.
3. **10⁴ coast tail flips sign with load**: under load 2.8 the regen gave stag max 19.32 ms / over 13 vs base 11.95 / 0; my quiet re-run (load ≈ 1.1) reproduces the author (p99 11.92 → 9.94, max 11.97 → 11.59, over 0/0, held 112 → 9). The 10⁴ max/over comparison is noise on this shared host both ways; `held_max` and the 10⁵ numbers are the robust carriers — all disclosed in the dossier ("three baseline batches bracket them").
4. **"9–11 octaves" is mislabeled arithmetic**: per-kick units ≈ 2⁷·(4428/n), so binding (<1 unit) needs n > 2⁷·4428 ≈ 566k/orbit — 2⁷× finer than the grid, **16–18 octaves finer than the floor** (the author's 9–11 is the floor-kick/grid-kick ratio). Substance unchanged and understated; I corrected the page line in place.

## Adversarial cases (mine; three, one beyond the author's domain)

Commands: `nladder 10000 coast 55 1500` ×2 (repeat), `nladder 100000 burn 55 600` ×2, `nladder 10000 coast 110 1500` ×2, `DIGEST_AT=76000 nladder 10000 coast 55 1500` ×3; base vs `STAGGER_GENESIS=1`; then `waves.py` with the belt filter widened to ≤8 fires.

- **A, quiet-load 10⁴ coast repeat**: base p99 11.92 / max 11.97 / held 112 → stag 9.94 / 11.59 / held 9. Claim stands off the loaded batch.
- **B, 10⁵ burn (author never ran it)**: held 1043 → 1039, over 99 → 87 — the held pile is indeed the player's doll's, not the belt's (confirms the author's decomposition at 10× the scale); but **max_ms 820.3 → 35.5 ms (23×)** — the catastrophic worst frame at 10⁵ burn *was* the wave×burn crossing. The tail-deletion claim extends to the worst frame at the scale that matters. Rate 1.000 both arms.
- **C, 2× horizon (110 s)**: baseline train shears 246.6 → 2,677.5 s across waves 1–6 (3×/wave, 3294's law); staggered holds 0.49–0.50·I through wave 5 (n ≈ 9,715). Frame tails hold (held 112 → 9).
- **D, over-flown digests**: three flights all refuse the digest and end at wall-dependent ticks (16,518,777,775 / 16,498,475,231 / 16,518,777,775) — the non-canonicality mechanism observed directly; the guard works.

## Predictions

`predictions.md` (13:49) precedes the decisive flights (author's `bs2.txt` 14:00, `regen.sh` 14:04, dossier 14:07); only N=10³ smoke flights ran before it. Prediction 2 held exactly (0.494·I is a sharp number that held to three digits), 3 held (counters, digests), 4 held in direction. Prediction 1 **failed by one octave in size** (h = 23 vs predicted [24,34]) and was reported as failed — in the claim-strengthening direction (floor kicks bigger than predicted); no adopted sentence rests on h's exact value. The kill criteria were pre-written and none fired. This is genuine pre-registration: a post-hoc author would not have predicted the wrong octave.

## Novelty and the page

The live page's open direction 8 (3294's own closing line) names exactly these two experiments; f82a ran both, plus the canonical-cut digest protocol and 3294's arithmetic corrections (10× floor cores; scar rate at P = 1.25×10⁸ s). Not a repetition — the refuted list gains a line (the dial's tail third), and the current best changes. HISTORY/docs hold no prior stagger/genesis-phase result for the fire train. The proposed page is faithful to the evidence (every new number checked against regen/my flights); I corrected one line in place (the octave arithmetic, noted inline). No closure: 3294 itself is still awaiting its second check, so no three-gold agreement exists on this result.

## Goal fit

Board bottleneck 4 (smoothness: worst frame, p99, allocator): at 10⁵ the stagger takes the coast arm into budget (over 3 → 0, held 154 → 1, lag 9.3 → 0.0) and the burn arm's worst frame down 23×. And it shows a premise wrong — the tail third of a gold-record unification claim. PRINCIPLES: "minimize spike compute and average compute usage so that you get a bigger simulation that runs smoothly" (OC#36); the stagger is a constants-only genesis choice — no state feedback, so it respects every killed per-body cadence rule on this page (54d9/0713/71b4); "the cheapest compute is compute not done" — the phase-lock was manufactured synchrony, not information.

**Why gold:** reproduced to the digit where deterministic and in direction everywhere load-bound; the held-out structural predictions held; a premise is shown wrong by direct intervention (the strongest form); the worst-frame metric moves 23× at 10⁵ burn and held 154 → 1 at 10⁵ coast; adoptable within one step (env-gated, bit-identical off) — the remaining step (B-gate delta on the M1) cannot run in this lab and is the integrator's by rule.

## What the author missed

- The 10⁵ burn arm (I ran it) is the strongest adoption number: it separates the two tail mechanisms at scale and shows 23× on the worst frame — better evidence than the load-noisy 10⁴ pairs.
- The octave arithmetic slip (9–11 vs 16–18), corrected on the page.
- `dim.py`'s p01 prints a 2⁻⁴⁸ fallback artifact at n ≤ 2 (planet/root rows) — never quoted, but the instrument should guard tiny n.
- `waves.py`'s belt classifier (≤4 fires) is horizon-coupled: at 2× horizon it silently excludes the whole belt. The census counters are the honest path (the author says so for counts, but the script itself degrades without warning).
- The stagger's first kick lands at up to 1.5× the nominal impulse; aggregate dv buckets are unchanged, but the per-body first-kick tail was not shown — near-resonant belts stay the named unsafe edge, and the page already says no cadence certifies there.

*(Checker scratch files were removed from this folder; every adversarial number above regenerates from the commands in "Adversarial cases".)*
