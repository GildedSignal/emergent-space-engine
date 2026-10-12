Grade: silver

**Abstract.** Claim: the skin must trigger on accumulated element drift ("provable" zero-miss at `W_SLACK ≤ R_ENC/2`), not on kick arrival; 3.4×–10.9× less work per encounter. Reproduction is perfect (both probes bit-identical, 38 s, 39 MB; quotes verbatim; predictions pre-registered). But the proof is wrong by a factor of 2 and the zero-miss evidence cannot fail: measured window coverage shows the implemented rule misses real encounters (2–18 per seed on plain belts, 6% under concentration, 23/246 in the tail). The corrected rule (window `R_ENC + 2·W_SLACK`) is zero-miss on 8/8 runs at honest gains 2.57× (λ=32), 8.25× (λ=0.5). The 28% eccentric width leak and the gain dial are real. Trigger-on-accumulation is q-skin's already-queued Verlet rule.

## Reproduction

`python3 probe_skin.py` and `probe_skin_smalkick.py` in a clean tree: outputs **bit-identical** to the stored JSONs (37.7 s / 37.4 s, 39 MB RSS — matches "38 s, < 300 MB"). Every dossier table number matches. `work/patch.diff` is empty (no repo edits — everything self-contained in the run folder, as claimed). All five library quotes found verbatim in the cached `library.json`. `predictions.md` mtime precedes both probe outputs — pre-registration order holds. The formation E-setup/B-live = 106× and the 37× smalkick gain both reproduce.

## The central claim is false as implemented (measured)

The docstring's own condition for zero-miss is `|da_i| + |da_j| ≤ W_SLACK` with window radius `WIN = R_ENC + W_SLACK`. Per-body triggers at `W_SLACK` bound each body's drift by `< W_SLACK`, so the **sum** reaches `2·W_SLACK`. Coverage needs `WIN ≥ R_ENC + 2·W_SLACK` (or triggers at `W_SLACK/2`, keeping `WIN` — exactly the rule `predictions.md` line 6 stated before the probe silently doubled the trigger). Standard molecular-dynamics Verlet lists use precisely that: rebuild at `s/2`, list radius `r_c + s`.

The probe never measures coverage: `width_miss` tests current `|Δa| > WIN`, which for circular truth pairs is unreachable (`|Δa| ≤ √2·R_ENC < 1.5·R_ENC = WIN`). "Zero trigger misses everywhere" is unmeasured — a control that cannot fail (the heuristics file's own rule).

I measured coverage (track each body's last window-build checkpoint and its `a` then; a pair is covered iff inside either owner's window at build time; same seeded worlds, three of four cases the author's exact populations):

| workload | encounters | miss B (author) | miss B-fix2 | gain B (author) | gain B-fix2 |
|---|---|---|---|---|---|
| belt20k λ32 (author's seed 1, enc 257 = theirs) | 257 | **7** | 0 | 3.39× | 2.57× |
| belt20k seeds 11–14 | 197–249 | **2–18** | 0 | 3.39× | 2.57× |
| formation 5k (their seed + 2 more) | 46–49 | **2–3 (≈6%)** | 0 | 3.38× | 2.57× |
| belt20k+tail (beyond the 95 width fails) | 246 | **23 (9%)** | 0 | 3.39× | 2.56× |
| belt20k λ0.5 (their exact world) | 97 | 0 | 0 | 10.92× | 8.25× |

A (per-kick) is zero-miss in every run. Fixes: trigger at `W/2` (predictions' rule) — zero misses on circular workloads, 10 residual tail misses (eccentric geometry needs the wider window too), gain 2.07×/2.77×; window `R_ENC + 2·W_SLACK` at trigger `W` — zero misses everywhere, gain 2.57×/8.25×.

## Other defects

- **The "27.6 measured vs 25 formula" validation is not reproducible.** Direct count on the author's own stream: 37.2 kicks/crossing (640,471 kicks / 17,200 crossings). The formula underpredicts by ~1.4–1.5× at both σ (renewal overshoot plus finite-horizon truncation: at σ=5e-6 a cycle needs ~117 of the 150 checkpoints; only 1.77 of 2.55 total drift gets absorbed). The 37× gain itself is correct — it is this 37.2, not 27.6.
- **Prediction-to-probe swap, partly undisclosed.** `predictions.md`'s A is a *global* trigger (all bodies rebuild when any body moves; the mechanism of lesson 1's Taleb maximum quote) and its prediction 2 (A grows with N) refers to that A. The probe's A is per-kick. The dossier reports predictions 2/3 as "half failed"/"failed" without saying the structure that failed differs from the one predicted. C was dropped (disclosed).
- The certificate's second half (predicted conjunction deadlines) is entirely unmodeled: `pair_evals` rounds to 0 in every row. The initial window build is uncounted for both A and B (at λ=0.5 it is comparable to B's entire counted work, so B's 10.9×/8.25× is an overstatement of net work).

## Novelty

Trigger-on-accumulation is not new here: `q-skin.md` posed it verbatim ("set a pair up again only when the kicks accumulated since its setup exceed s", molecular dynamics' Verlet list), and board gold `components-4643` named the skin the 12.6× lever. The corrected rule is the textbook Verlet rule. Genuinely new and reproduced: (a) the gain-as-dial formula `W_SLACK/(0.8σ)` with its upstream implication (kick-size cuts amortize the skin — though it underpredicts by ~1.4×, and the corrected constant is 2.57×, not 3.4×); (b) the 28% eccentric `|Δa|`-window leak (95/341 reproduced), which correctly redirects to radial-range windows; (c) the formation tier blowup (106×, independently confirming taleb-09b5's 135×).

## Goal fit

Aimed at the board's top scaling risk (candidate work tracking real encounters); the skin build is queued in both lanes (`lab/queue.txt` b-encounter-skin), so a corrected trigger rule is adoptable within one step. PRINCIPLES #6 applies literally ("influences below one quantum accumulate") and #14 ("we only care about changes"). The reporting failure is against #2 in spirit: "error type over error size" was claimed as a proven bound that was not proven.

## The one experiment that would make it gold

Rerun with the corrected bound (`WIN = R_ENC + 2·W_SLACK`, or triggers at `W/2`) with **coverage** as the miss metric and the initial build counted — my numbers already show it holds (0 misses, 8/8 runs, 2.57×/8.25×) — ideally on `crates/encounters`' Binet cone rather than the 1-D `a`-window toy, where the certificate's deadline half also exists. Then the dossier's constants and the "provable" claim are honest, and the rule is adoptable as written.

## What the author missed

1. The factor-2 in their own proof — their docstring states the right condition and their `predictions.md` the right rule; the code implements neither.
2. Coverage was never measured; the `width_miss` test cannot fail on circular workloads. One instrumented run would have caught both.
3. The finite-horizon truncation behind kicks-per-crossing, and an unverifiable 27.6.
4. The deadline half of the certificate is unmodeled; initial builds uncounted (both flatter B's sparse-λ case).
5. The Taleb maximum quote in lesson 1 argues for the global-vs-local comparison that was predicted but never run; as measured, lesson 1 is lesson 2's amortization point restated.
6. The self-declared lens blind spot (Taleb-heaviness) is real, but the actual misses were arithmetic and instrumentation hygiene, not lens bias.

*Checker probes: `/tmp/check-aa2f/probe_check.py` (coverage + fixes; 14 s, 61 MB) — self-contained, imports the author's `probe_skin.py` unchanged; identical seeded worlds.*
