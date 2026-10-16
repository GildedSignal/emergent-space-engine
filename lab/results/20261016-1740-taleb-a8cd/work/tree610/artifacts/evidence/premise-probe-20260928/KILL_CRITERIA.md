# Premise probe: kill criteria, frozen before any run (28 September 2026)

This is a float lab probe: non-canonical, 64-bit floats, orders of magnitude only. Scene: point masses at physical scale (Sun, Earth, Moon), a ship in low Earth orbit, and a velocity quantum of 0.27 mm/s (Q = 2^40). Each premise dies if its criterion is met:

- **K1: the parent formula.** It dies if, with the formula as a Kepler conic about Earth and the Moon and Sun tides as kicks, a ship in low orbit takes more than 10^3 kicks per orbit. The estimate is about 30.
- **K2: averaging known tides.** It dies if first-order averaging of the Moon and Sun quadrupole, with short-period terms included, cuts kicks by less than 10× against K1. The claim is about 500×.
- **K3: an oblate parent.** It dies if J2 = 1.08·10⁻³, placed in the formula as the equatorial 1/r³ term, still leaves more than 10× K1's kicks.
- **K4: handoff.** In an Earth-to-Moon transfer across the Hill sphere, with hysteresis and error-feedback re-anchoring, it dies if the E and L carries grow secularly over 100 handoffs (a fitted growth exponent of at least 0.8).
- **K5: binaries.** For a planet around a star pair with mass ratio 0.8, report kicks per orbit when the parent is the dominant star. Above 10^3, binaries need a two-body formula as parent. This is expected, and it is recorded, not a kill.
- **Also report:** `position` calls per second per body from kicks and re-anchors, for a million ships in low orbit.
