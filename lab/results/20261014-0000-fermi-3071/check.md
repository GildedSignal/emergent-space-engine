Grade: silver

**Abstract.** Claim: the nladder conflict dissolves — ea91's Gini 0.72–0.74 and 7497's flat per-orbit bulk are one stream, the tail manufactured (natives = compiled period ladder, members = birth-burst-then-death, head = driver), so rule 2 dies as a ladder rule and the certificate is birth-constant arithmetic. Reproduced: ho1 digest bit-identical (`aca905ad…`); every table regenerates; independent recomputation matches. Checker attacks beyond the author's domain: rtf 300 window (ladder bodies ×2.99–3.00 exactly, G_all 0.764 still rising toward the native ceiling), m4 member floor (native items bit-identical to m400's), probe digest-neutrality re-verified. Two held-out misses on B, one inside the pre-registered kill list — disclosed, mechanism confirmed by the checker, but overridden post-hoc. Adopt: merge the resolved wiki page. Gold needs the member/driver half as a formula.

## Reproduction

- Clean tree, patch applied by me; `analyze.py` regenerates every table in `regen.log` exactly.
- ho1rep digest `aca905ad7792…` == ea91's stored `census-ho1.json` digest, `cut_tick` equal, census item vectors equal — the bit-identical reproduction claim holds on this box.
- Independent recomputation (my own Gini/Zipf/Spearman, own code): roster ladder 0.0484 max, 12 of 28 above 3×10⁻³/s ✓; roster Gini 0.759 ✓; ρ 0.940–0.958 ✓; native counts identical across seeds 3/7/11 and m48/120/400 ✓; kicks 266 = 2·133, items 533 = 2·267−1 ✓; player 417 → 350 ✓; A: G_all 0.721, G(nat) 0.736, dead 0.47, h2 median 2 (5/5) ✓; B: G_all 0.753 (rose), zipf −1.59 ✓.

## Adversarial cases (mine; two outside the author's tested range)

1. **rtf 300, seed 3, m400 (T ≈ 16,500 game-s — one decade beyond the doubled window).** Ladder bodies scale ×2.99 (items) / ×3.00 (kicks) exactly; G_all 0.764, continuing the rise 0.737 → 0.753 → 0.764 toward the native-only ceiling — the author's miss mechanism (dead-member bursts freeze while ladder bodies grow ∝T) is the real behaviour and generalises. Player 682 = 1.64× (not 3×): schedule-bound again, worse for any measured rank. ρ 0.973.
2. **m4, seed 3 (member floor; neither author ran it).** Native items **bit-identical** to m400's (267,267 / 134,134,134 / 34,34 / player 417); G_all → 0.729 ≈ G(nat) 0.736 as members vanish. The decomposition is clean at the floor; "live fraction set at generation" is confirmed at both ends.
3. **Probe digest-neutrality.** Same scene with `ES_SURPRISE` off: digest identical to the probe-on run. Independently re-established here.

## Predictions record

`predictions.md` predates the author's runs (mtimes: predictions 7 m; the author's census `.err` files 6 m; the model inputs, the two prior runs' data, 11 m). A held 5/5. B held the structural discriminator exactly (2× per ladder body, roster Gini T-invariant, zipf) but missed two point predictions: G(nat) 0.713 vs band [0.716, 0.756] (by 0.003, the player), and G_all rose instead of falling. Prediction 5's failed clause sits inside the pre-registered kill list ("any of 1–5 failing its band → rule 2's measured-rank reading revives"); the author replaced that consequence with a post-hoc mechanism instead of following it. My rtf-300 run shows the override is *scientifically right* — the player's count is schedule-bound and ever further from any body-intrinsic rate, which undermines a measured rank further — but a pre-registered decision rule was overridden after the fact. That, and the failed G_all direction, keep this off the gold letter.

## Novelty

The constant-certificate verdict is 7497's (its wiki side already said "knowable from body constants at birth"). New here: (a) the adjudication — both runs measured one stream, so the flagged wiki conflict dissolves instead of being decided; (b) exact determinism (census counts *identical* across seeds and member counts — stronger than 7497's ±5 % per-orbit) and exact kT window scaling, a new measurement; (c) the roster model reproducing G_all and the Zipf slope; (d) the resolved page (five merge conflicts → one text). No HISTORY entry adjudicates this; the wiki held the open conflict. Not a repetition: ea91's numbers are cited and one digest control is rerun, not re-measured.

## Goal fit

Board focus 1's flagged conflict (`nladder: open, conflict to resolve`). It deletes the census-instrumentation design path before it is built — "The cheapest compute is compute not done" — and closes a second convention beside the cadence law (#19: "a fix signals the wrong representation; one law at every scale" — the cadence law *is* the promotion law). Honest about being a decision, not a 10× compute claim.

## Page

Faithful after two corrections I made in place: "within ±0.013" → 0.017 (worst case, tune: model 0.748 vs measured 0.730 — the dossier's ±0.013 is wrong for tune), and the garbled "(266 = 2·133−1)" → the correct arithmetic (kicks 266 = 2·133 exactly; 133 = 2·67−1, 33 = 2·17−1), "2× per body" → "per ladder body".

## The one experiment for gold

Make the member/driver half arithmetic: a birth-burst-then-death formula for members and the player's item count derived from the shipped decision schedule (canonical ticks), so the whole census is a zero-free-parameter function of birth constants plus the decision log. Pre-register G_all, G(nat) and the player's count on fresh windows/scenes (rtf 300 and m4 are now spent by this check; use e.g. rtf 50, seed 5, m200). If held, the manufacture claim has no measured half left and the kill-criterion question disappears.

## What the author missed

- The model-accuracy claim "within ±0.013" is false for tune (0.017).
- "1,613:1" divides by 3×10⁻⁵, but the roster's minimum nonzero rate is 2.5×10⁻⁵ (≈1,936:1) and two planets sit at exactly 0 — the roster prediction includes two zero-rate bodies.
- The G_all model is half-circular (members copied from the measured data, disclosed in the lens); the "Zipf slope is manufactured" demonstration inherits that circularity.
- The measured G(nat) is *not* T-invariant: 0.736 → 0.713 → 0.717 at 1×/2×/3× windows, drifting down as the player's schedule-bound share shrinks. Only the ladder bodies' Gini is invariant; the dossier's "and so is the measured one" holds to ±0.02 and degrades with window length.
- The pre-registered kill consequence should have been followed or the criteria registered channel-scoped (bands on ladder bodies only) in the first place; an override needs independent confirmation to stand — this one got it (my rtf 300), the next one may not.
- The alive-member quiescence reading ("1–3 items per half-run") is window-dependent: the h2 median grows to 7 at rtf 300.
