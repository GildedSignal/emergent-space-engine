# Predictions (written before the decisive grid)

Grid: 16 nose angles (22.5° steps) × levels {0,2,4,6,8,10,12,15}, held forward burn, settle-based,
burn horizon 2^36 ticks, wall cap 10 s/flight, plane seed 1, 48 members, probe turn_log2 = −26
(11.25°/flush; the burn and scene are shipped config). Cases tuned so far: 8 angles × level 6 only
(that smoke showed a clean half/half split at L6 with boundary between rel_v −1° and +41°).

- **P1 (contiguous cone).** At every level the CRASH outcomes occupy one contiguous arc in nose-vs-v̂
  angle (`rel_v`), the escape/bound outcomes the complementary arc: exactly two boundary angles per
  level, no interleaving at 22.5° resolution. Kill: an isolated CRASH between two ESCAPE neighbours
  (or vice versa) at adjacent grid points.
- **P2 (level shrinks the cone).** The crash arc is widest at L0–L2 and shrinks monotonically as the
  level grows (a strong retro burn reverses the velocity and escapes); by L12–L15 the crash arc is
  empty or a sliver. Kill: a level where the arc is wider than at the level below.
- **P3 (the radial channel is faster, not separate).** Noses with a strong inward-radial component
  (|rel_rout| > 90°) die sooner (smaller t_end) than retro-tangential noses at the same level, but
  they lie inside the same contiguous crash arc — no third boundary. Kill: an escape island in the
  inward-radial sector while both tangential sides crash.
- **P4 (silence).** Every CRASH row reports fault = None and refusals = 0, with γ_max ≈ orbital
  (≤ 10⁻³): no warning channel exists in the record for any death, and crash vs leave cannot be
  told apart by the fault tag. Kill: any refusal or fault tag preceding a crash.
- **P5 (the leave is silent too).** At high levels some prograde flights end as LEAVE (r > 2^39,
  dead or alive past the leave) or alive-in-Passage at the horizon, again with fault = None,
  refusals = 0.

What I expect to be wrong about: P2's monotonicity near the L4/L5 retro boundary (prior runs put
the retro threshold between L4 and L5 — my P2 implies the arc is already small at L5); and P3's
"no third boundary" (the handout to the root doll on the escape side could interact with the
inward-radial sector's geometry after the first orbit).
