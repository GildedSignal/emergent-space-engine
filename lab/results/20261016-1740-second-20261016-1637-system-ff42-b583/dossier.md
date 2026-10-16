# Dossier — 20261016-1740-second-20261016-1637-system-ff42-b583 (second author on 20261016-1637-system-ff42)

## Claim

The checker's named gold experiment, done: with the guess mirrored around the **unrounded**
periapsis epoch and verified over a **window sized by the residual offset's reach over the
closed-form fall speed** (both from the binding, ~30 lines over ff42's block), the crash
search's fallback goes to **zero everywhere** — author grid 29/29, held-out battery 52/52,
and **2,723 fires with 0 fallbacks across three flown seeds** — at **2.2–2.4 readouts per
search** (the bisection class: ~11 grid, 29.4 flying), tick-exact on all 155 synthetic cases
and **bit-identical flight digests**, while the flying leaver kick **halves**: 211→113,
205→110, 201→104 µs (interleaved arms, one load). The crash search retires behind its
inverse, as the exit search did; the bisection and any policy on it (warm start, AB-IQI)
become pure insurance.

## Bottleneck

The per-kick cost on crash-course bindings (frame-cost's census: the search was 45% of a
flying kick). The search's term collapses to one exact inverse plus two verifications:
measured −46…−48% on the whole leaver kick, matching the census's share. What it deletes:
the probe-policy layer's domain (its fallback path never runs on any measured scene), and
the future need to tune any probe policy for the crash search.

## Evidence (all from `regen.sh`, ~7 min; deterministic counts, wall = orders of magnitude)

- **Bench, author grid (36 cases)**: `bench.txt` — 31 answered, 0 mismatches (bench exits
  on any), **fired 29/29, 0 fallbacks**, mean readouts 10.92 → **1.67**, mean per call
  56.4 → 16.2 µs (**3.49×**; ff42's uncured block: 2.0×). Stats come from statics inside
  `step::next_impact` (`IMPACT_GUESS_FIRES/FALLBACKS/WINDOW_READOUTS`) — no replication of
  the patch's arithmetic, the defect that misinstrumented ff42.
- **Held-out battery (89 cases, `adv.txt`)**: `after` ∈ {bracket-start, mid-outbound,
  pre-cross, next-cycle, +3 periods, mid-fall, already-inside} × 3 bindings; e 0.1–0.97 ×
  two periapsis fractions × both senses; grazing f 0.995–0.9999; μ = 3/2 non-unity dolls;
  30 seeded-random phase/course draws. **89/89 answered, 0 mismatches, 52/52 fired, 0
  fallbacks**; every fire spent exactly 2 window readouts. (ff42's predictions promised
  this set and never ran it; the checker ran it against the ±1 window and found ~half
  firing — the window was the whole difference.)
- **Why the window law is right (`diag.txt` + pre-run diag2)**: the readout radius equals
  the tube radius at the crossing to 6 decimals (the offset projects below display range);
  the miss is `‖offset‖·quantum / |dr/dt|` ticks — predicted 0.98/1.59, measured 1 tick,
  on the only two grid cases that missed under ±1. The window is `ceil(that) + 1`, capped
  at 8 (a grazing fall dearer than the bisection it saves falls back; no case in any
  battery reached the cap).
- **Flights (`flights.txt`)**: kick-bench, seeds 3/7/11, flying (rtf 100, 8 s) and battle
  (rtf 1, m4000), **pristine/patched binaries interleaved under one load**: digests SAME
  on all six arms; flying leaver median 210.7→113.1, 205.0→110.3, 201.3→104.3 µs;
  fires 791/1215/717, **fallbacks 0**, window readouts/fire 2.20/2.29/2.36. Battle arms:
  digests SAME; no crash searches occur in the 8 s window on shipped main (0 leaver
  samples), so identity holds trivially there.
- **frame_digest** (`digest-pristine.txt` = `digest-patched.txt`): `6a0c3cf7…`,
  `2373bdb3…`, 4 schedules agree per flight, bit-identical — the adoption gate ff42 left
  unflown and the checker flew for the ±1 version, now flown for the windowed one.
- **Crate suite**: `cargo test --release -p emergent-universe --lib` — 10/10.
- **Composition with the warm start + AB-IQI stack (2ae0)**: not runnable — its patch no
  longer applies to today's main even standalone (`step.rs:283`, `kick_bench.rs:103`
  conflict; its base predates 12–14 Oct merges). Answered by measurement instead: 2,723
  fires, 0 fallbacks on every scene shipped main can run, so the policy layer would never
  execute there; where a fallback did occur it remains orthogonal insurance (it optimizes
  the bisection this patch keeps as fallback). The stateless guess alone matches what
  2ae0's composed stack measured on the flying leaver (199→105 µs on their arm; 201→104
  here) without env gates, retained state, or a policy.

## Predictions (predictions.md, written before bench/flights)

All five held: 0 mismatches everywhere (1); 100% window-verified on every held-out regime
including flights (2); 2.2–2.4 readouts/search (3); digests bit-identical, leaver kick
toward the bind-only floor (4); composition: subsumption measured, stack itself unappliable
(5). The kill criteria (any mismatch, any digest change, >5% fallback at mid fractions)
never fired. One instrument lesson, honestly: my first patched-vs-pristine kick comparison
was taken minutes apart on the shared box and showed *no* movement (155.9 vs 155.0 µs);
interleaving the two binaries under one load recovered the true −46%. Single-arm wall
comparisons on this box mislead by up to ±45% — arms must interleave.

## What would make it wrong

- A binding whose readout radius differs from the tube's by more than the L1 reach + 8
  quanta at the crossing (the turn is within two quanta of the rotation; `inside`'s sqrt
  rounds at 2⁻⁶²): then the window can miss and fall back — safe, but the win shrinks. No
  such case appeared in 155 synthetic + 2,723 flight searches.
- A non-monotone fall branch would break the bisection too (the shipped premise); the
  guess only ever agrees with the bisection's own answer.
- The counters are `Relaxed` statics: benign under the bench's single-threaded resolver;
  a threaded future re-reads them per-call as now or drops them (they never decide
  anything).

## Cost of adopting, and fit

Production delta over ff42: `periapsis_epoch` extracted (next_periapsis now ceils it — one
body, no duplication), the mirrored guess around it, `crossing_window` (L1 reach ÷ fall
speed, cap 8), the ±k walk, three counters; `at_radius` made `pub`. The bench (`levelbench`)
and the kick-bench print are instrumentation. PRINCIPLES 18/19: the bisection over ticks
was the fix; the compiled cycle's inverse was the representation — with the window sized by
the offset's own law, the search retires and the fix goes. 32: the symmetry (Darwin mirror
+ the offset's reach) was found in the representation, not paid in probes. What remains for
the integrator: replay arms (`--replay-all`) and the M1 re-measure — the same gates 2ae0's
stack still owes.

## The lens (what this run may have missed)

The second-author lens trusts the checker's named experiment and ran it whole; what it did
not do: the battle arm shows no searches on shipped main, so the claim "retires the search"
is proven on the flying arm only (the census's dipping hand-out half lives in scenes main's
battle bench no longer reaches — `ES_MEMBERS` was 2ae0's unlock, not adoptable here). The
`next_exit` Cycle branch (ff42's own note) still bisects untouched. And the window cap of 8
is a chosen constant: a scene with grazing falls that dip by less than the cap's reach in
ticks would fall back there by design — one battery row short of infinite grazing was
tested.
