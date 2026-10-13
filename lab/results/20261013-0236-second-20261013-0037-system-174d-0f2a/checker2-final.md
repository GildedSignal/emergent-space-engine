Working...
Check complete. `check2.md` written, the author's page corrected in place, tree restored to base (`941f6941`), nothing else touched, no commits.

**Grade: gold** — `lab/results/20261013-0236-second-20261013-0037-system-174d-0f2a/check2.md`

**What I did:**
- **Reproduced**: applied `work/patch.diff` to the clean tree, ran `regen.sh` (19 s, exit 0). Decisive table exact (636→6, 897→23, 1,085→24, 404→5, 377→1; law-bound 0 everywhere); my run printed the fixed-granularity 31,286 verbatim; demand worst frames 42/579/1,036 digit for digit; L15 n_law = 24 in all four batteries.
- **Independent arithmetic**: recomputed n_law, window budgets, ratio medians and the plunge decomposition from the raw kick logs with my own parser — all match, including 149 deep kicks = 100.0% of 1.558×10¹³ quanta = 0.019 of 24 events, and the 1.517×10⁻⁴ tail at both seeds.
- **Instrument**: `clock_full` verified as `plan_interval`'s want before the thrust clamp (step.rs:551–556, 718–727); coast prints step==clock; env-gated counters only, tests pass.
- **Predictions**: mtime order verified; all five held as written.
- **Four attacks**: seed 3 (pattern identical); 16 s flights — outside the author's domain, envelope 0–24 still holds (L8 707→24, brake 1,454→19, win ≥29×); reverse L15 — untested brake-at-high-level and the most expensive burst ever measured (2,219 kicks) → 23 events (96×); rtf 20 — L15's 24 is pace-invariant.
- **One correction to the page**: the count is dive-set at L12/L15 but duration-set at L8 (6→24 from 8→16 s) — "set by the dive, not the throttle level" was incomplete; folded in with the domain extension, plus a stale `(this run)` label fix.
- **Novelty**: the silver explicitly left this cadence underived ("which this run does not derive"); this run derives it from shipped law and shows the fixed-granularity inversion was the divisor's artifact — premise correction plus the adoptable 45–377× event-cut price for the carry-the-burn lever.
