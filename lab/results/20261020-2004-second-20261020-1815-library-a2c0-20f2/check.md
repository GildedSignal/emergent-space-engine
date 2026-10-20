Grade: gold

**Abstract.** a2c0's checker named the gold experiment; this run flies it, and it lands. My own regen (patch applied at base 6db15364): F1 digest `8eecf1fa…` byte-identical to 23a6's committed e3, all 41 (t,tests,skip_bnd) triples equal. δ pinned per-answer: 0.053–0.399, drifting (28/40 in a2c0's fitted band; 28 recounted by hand); the invalidation is slack-margin crossing, not kick-Poisson; c_check 27.4 ns kills the ≥40.5-ns corner; ALL-walk durations corrected from each leg's own ladder line (c2 56,035 gs, 3e5 legs 40.2–40.7k — verified raw), so capture = 2.15–6.02 h/era at 1e9, ledger 16.1–20.0 h/era. My four held-out arms (seed 2, ES_BOUND_VERIFY at 1e5, coast, 45k-gs cut) confirm the mechanism and scope the letter. Adoption cost: none — corrected numbers plus the rule that no 1e9 warm-answer quote rides without its cadence's check bill.

## Reproduction

- `git apply work/patch.diff` clean at base 6db15364; my own `./regen.sh` (48.7 s): exit 0, every count-level line identical to `regen.log`; digest byte-identical to the committed e3; F1 counts identical across three independent draws (author's, runner's, mine). Wall-µs lines differ under load exactly as disclosed (my live c_check draws 32–57 ns while my own flights load the box; counts invariant).
- Independent recomputation, not the author's script: the 41 belt-wide rows read raw — cold 88,873/99,715 = 89.13%; gaps 165.27/330.54 gs (2^25/2^26 ticks × TICK_SECONDS, verified at view.rs:23); miss 0.044%→0.333% over the 18 constant-gap legs (7.5×), peak 0.488%, end 0.142%; δ_eff 0.053–0.399 with 28/40 inside [0.065,0.266] (I recounted the 28 by hand); c_check row-by-row (27.5–36.2 ns); duration corrections verified against each leg's own `game … s after` line (c2 56,035; a1 40,231; w3 40,724; b1 56,043); ledger arithmetic (12.75 + 2.15–6.02 + 1.19 = 16.1–20.0 h; 830–1,030×; shares) recomputed exact; a31c/8365 constants verified verbatim on the live page (12.75 h, 69.75 s, era 27.9k).

## Predictions

The one record defect: `predictions.md` claims mtime 20:15:55, "14 s before the first F1 flight"; the file's actual mtime is 20:24:43 — after F1 (~20:16), so the pre-registration state is unverifiable (edits happened; the F1 outputs were also overwritten by disclosed re-flights). Substance survives: the registered bands MISSED where a post-hoc writer would not have — D1's top 0.32 breached by 0.399, D7's total landed 16.1–20.0 below the registered 18–21.5, D3's spike-at-doubling withdrawn as unidentifiable — and F1's counts are deterministic (identical in every re-flight), so nothing measured could be retrofitted. R1, D2, D4, D5, D6 held; no kill bar fired. Disclosed non-blindness (the committed artifacts were read first) was honest and is inherent to the "log read" experiment the checker itself named.

## Adversarial cases (four, all flown; artifacts in work/flights/chk_*)

1. **Seed 2 (held out):** 41 belt-wide answers, cold 89.1%, δ_eff 0.055–0.359 — the letter holds on a fresh seed, δ=1 excluded, and the constant-cadence growth reproduces (6.5×). The claim generalizes across seeds within the window.
2. **Exactness at 1e5 (never flown above 3e3):** `ES_BOUND_VERIFY=1` on the full F1 protocol — zero false skips across all 1,876 answers (~1.87M bound decisions). The bound whose invalidation is being priced is exact at this rung.
3. **Coast (other regime):** zero ALL captures, no belt-wide answers at all — the answer channel is approach-driven, as the slack mechanism requires.
4. **45k-gs cut (outside the tested 30k window):** the miss decays to tests = 0 for ELEVEN consecutive belt-wide answers (~2k kicked bodies per gap — kick-Poisson with any λ(t) > 0 is dead outright, cleaner than the author's growth argument), then a late re-approach reads 2.95–4.47% per answer, δ_eff ≈ 2.2. So δ<0.5 and the δ=1 exclusion are window facts, not scene constants — the run's mechanism sentence generalizes, its numbers do not (the lens conceded this; the page now says so). The 45k leg's ALL rate is 77.7/era, just above the 1e5 band top, inside the 1e5–3e5 envelope; the capture band's edges (7.74/21.68 µs/body/era) are untouched.

## Novelty

`docs/HISTORY.md` holds no invalidation-rate, c_check, or walk-count work; the wiki's line was a2c0's fitted band on assumed uniform gaps with c_check unmeasured — this run replaces a two-point fit with the measured per-answer series, identifies the mechanism, measures c_check, and corrects the capture N-scaling that a2c0's own checker flagged (N^0.74) as the ledger's live risk. Executing the named experiment is the lab's designed silver→gold path, not a repetition.

## Goal fit

Board #1 (bodies 28 → 10⁹). It shows two premises wrong by measurement (δ as a law-band constant; kick-Poisson invalidation — my zero-plateau is decisive), kills the 41-s-at-era-cadence sentence's last surviving corner by counts alone, and corrects a pending 1e9 inference before it hardens (capture 7.1–13.4 → 2.15–6.02 h; answers 0.08–0.49 → 1.19 h), holding the adopt order. PRINCIPLES 3: "Compute only surprises. Cost follows change and entropy" — the answer bill is now priced at its true driver (slack, the geometry of who-could-have-reached-whom), not a fitted kick ratio; and H0183's "a failed expectation is not automatically a failed method: diagnose which one broke" — a2c0's conclusion held, its constant did not.

## Why gold

Reproduced byte-identical from shipped code + patch; the checker-named experiment done with every number regenerable in ~45 s; two premises dead by measurement at near-zero adoption cost; my four independent held-out arms confirm the mechanism and add the exactness control the author never flew at 1e5. The 1e9 rows stay honestly [INFERENCE]-tagged, resting on N-flat counts measured only to 3e5 — the one soft edge, disclosed, and every direction of its breaking strengthens the surviving ordering.

## What the author missed

1. The pre-registration mtime evidence is gone (file touched 20:24:43, post-F1) — the record cannot prove the ordering it claims; only the bands' misses and F1's determinism carry it.
2. `ES_BOUND_VERIFY` at 1e5: the exactness control for the very memo being priced sat one env var away and was not flown (23a6 ran it only at 3e3).
3. The zero-miss plateau past the window: one longer cut (40 s more of wall time) would have shown tests = 0 for 11 consecutive belt-wide answers — the cleanest possible kill of kick-Poisson, stronger than the 7.5×-growth argument, which still admits a drifting-λ(t) confound.
4. The page carried one non-regenerating number (era-answer band "1,683–4,082 s = 24–59×" vs the regenerable committed-draw 1,648–3,998 = 24–57×) — corrected in place, with my held-out scope note appended to the page.
5. The dossier's §A "the flight's own kick rate 5.051e-5" is the committed e3's rate; re-flights read 5.049e-5 (−0.04%, digest unaffected) — the wording blurs which draw is quoted.
