Working...
Check complete. `check.md` written to the run folder; tree restored (only `check.md` added; no commits made).

**Grade: silver.**

What I did and found:

**Reproduction (exact).** Applied `work/patch.diff` in the clean tree, ran the dump (67.8 s) — all 126 CSVs bit-identical to the author's — then `quick.py` (24 s): every dossier number reproduced (bounded exp 0.353/ρ 0.300, compound 0.416/0.677, drift 1.355/0.724, leaks ρ 0.29, S2 flags 10/12/14/13/12/13, max |z| 6.26, floors 1.0e-18/P and 5.2e-9/P, exponent port faithful to `fit::growth_exponent`).

**Defects found.**
- The shipped patch writes invalid `scene.json` (`"ships":0,1,…`, no brackets); the documented reproduce command crashes until hand-repaired exactly as the author silently did.
- Prediction 3's thresholds (≥15/12/10 of 16 same-signed) all missed — 8/14 on every leak — yet reported "held"; prediction 6 silently dropped (the calibration ladder is flat 35.7% at every rate: it never crosses a floor, so it cannot show tracking).
- Bounded control sits at 10–11 of 14 ships against the fail threshold 12 — one ship of margin, and the threshold was derived for 16 judged ships; at 14, S1's ≥14/16 rule can never fire, so the "pair" is S2 alone here.
- The core recurrence-matching idea is the unchecked prior run `20261006-1545-q-b12-design-9242` ("arrow of time at a fixed state"), uncited in the dossier.

**Attacks (6, on the reproduced series).** A fast-phase state-only error (plausible handoff-geometry error) passes — no false positive; a pure walk at 1e-9 amplitude flagged 14/14 by S2 but *not* S1 (the disjunction is load-bearing); a walk reaching 1e-6 on top of the real bounded error flagged 14/14; memory 1000× below the bounded error and bounded+1e-11/P leak stay invisible, matching the derived floor; the shipped exponent-ranking test fails on this machine, independently confirming the cross-machine flip (my dump's direct medians prove it regardless of which assert tripped).

**The gold experiment:** finer state matching (|Δ(E,L)| bands or 9242-style nearest match with drift adjustment) dropping bounded to the echo confound while holding the memory flags, at the real judged-ship count, with the permutation cost measured inside a 60 s gate and a patch whose output parses.
