# Predictions — second author on 20261019-1551-dynamics-e3b7

Written before any decisive flight below. Calibration already done (not tuned on):
baseline C0 s1 H=16384 thermal=0 reproduces the author's digest `e8a69ff7…`
bit-for-bit in this tree; nothing else flown yet.

The checker's named experiment is folded in as this run's own result, plus the one
link neither the author nor the checker flew: the eccentricity ladder on isolated
orbits (the corrected mechanism — "contact-TRIGGERED, tide-FED … pericenter pump on
contact-eccentricized orbits" — has never been tested at e > 3×10⁻⁵).

## Arms

- **A1–A3 (the named experiment): `--pass` controls** (contacts recorded, velocities
  untouched — belt and fleet bodies created `Response::Pass`, one knob, default off).
  - A1: C0 s1 H=32768 thermal=0 `--pass` — must reproduce the checker's digest
    `b73b06dc…` **bit-for-bit** (my record independently regenerating an independent
    flight; a mismatch means my knob is not their knob).
  - A2: C0 s1 H=49152 thermal=0 `--pass` (1.5× the checker's horizon, 3× the
    Bounce onset ~12–16k).
  - A3: thermal cold control C s1 H=49152 (±q/256) `--pass`.
- **A4 (cadence, checker's variant folded in):** C0 s1 H=16384 thermal=0 `--every 4`
  (kick every 4th chronon at 4× magnitude).
- **A5 (the eccentricity ladder; new).** Single body, same shipped Chronon +
  RelativisticV1 + same integer field, `gravityorbit` example, H=98304 (14 orbits at
  a=70q), placed at apocenter with exact vis-viva velocity, integer-rounded:
  - circular a=36q, a=70q (folds the checker's isolated flights into the record);
  - a=70q, e ∈ {0.01, 0.06 (one contact's worth), 0.2, 0.5, 0.8, 0.97, 0.99};
  - a=36q, e=0.5 (r_p = 18q, the grinder remnant's own scale);
  - a=70q circular +1-quantum tangential (the belt's rounding scale, e ≈ 3×10⁻⁵).

## Predictions (kill branches named)

- **P1 (A1):** digest matches `b73b06dc…`; belt flat: maxk drift < 1%, esc = 0,
  rms radius constant within 1%. If the digest differs, my `--pass` is not their
  Pass and A1 is VOID until the variant is found.
- **P2 (A2, kill branch):** flat to H=49152 (maxk drift < 2%, esc = 0). If the tide
  alone destroys the belt by 49k, the checker's correction itself fails — that is a
  clean refutation and this run reports it as the result.
- **P3 (A3):** thermal ±q/256 under Pass is flat too (contacts are its only decay
  channel); maxk drift < 2%, esc = 0.
- **P4 (A4):** first-escape onset in [10k, 15k] ch (checker: 12236 vs Bounce 13022);
  digest `e98306bb…` if my every-phase/rounding variant coincides with theirs, else
  report my variant's digest and onset and say the variant differs.
- **P5 (A5, the mechanism discriminator; three branches):**
  - (i) bounded: every arm with r_p ≳ 5q keeps r_max drift < 2% over 14 orbits
    (prior: the rounded tide's per-chronon torque noise walks e by ≤ 10⁻³/orbit, far
    below contact impulses ~0.02–0.06 per hit);
  - (ii) cap-pump: arms whose pericenter enters the clamp region (r ≲ 2.2q:
    e ≥ 0.97 at a=70q) show a measurable walk — r_max or e drift > 5%, sign-varying
    per passage (the clamp is the only O(1)-relative error source in the field);
  - (iii) belt-e pump: some arm with 0.06 ≤ e ≤ 0.8 walks r_max > 5% — then the
    corrected claim "the kicks alone hold it" is FALSE at contact-seeded
    eccentricities, the checker's redirect ("pericenter pump on contact-eccentricized
    orbits") is confirmed in a stronger form than they flew, and the gate must
    forbid those e, not the contacts.
  Prior: (i) + (ii). Branch (iii) at e ≤ 0.8, or (ii) failing to walk at e = 0.99,
  each overturns a half of the corrected mechanism — either is reportable gold-grade
  content, not a VOID.

## What would make this run wrong

`--pass`/`--every` changing the default path (it must not: belt digests regenerate);
single-body genesis differing from belt-body dynamics (same World/Chronon/kick calls,
radius q, mass 1 — checked against A1's belt behaviour for consistency); reading
boundedness off floats (all boundedness verdicts read integer r_max/r_min columns
only; floats print as readouts).
