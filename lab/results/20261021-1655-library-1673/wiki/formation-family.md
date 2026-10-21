topic: formation-family
status: open
closed-by:
valid-while: crates/universe@00696555 + 20261021-1551-scout-033c's patch (family_hill.rs, standalone f64 instrument; no engine change)
updated: 20261021-1655-library-1673

# The formation family: one orbit, one integer kick stream, one binding

## Current best
**NEW (1673, library — composed from page-cited constants, no flight [checker-corrected]): the family's population is the fleet/driven belt, never the phase-locked belt; locals/GEO dead domain (11.6–17.3× the 15,000 kill radius).
Bytes (B+F·w)/F floors at w = 8–32 B: misses the ≤6 B row at every F, loses the phase-locked belt to compact 1.6× (8.12 vs 5.0 B), beats compact driven 1.44× (10.93 vs 15.75 B), cuts the fleet population 113–245× off the 5,060 B plateau; blended 10⁹ row closes iff driven share ≤32.1% (family) / ≤9.3% (compact driven).
Events: LEO cadence 1.56e4× the belt's floor rate; 1–10% fleet share swings the 10⁹ kick row 0.69×→6.87× (floor-belt convention) or 1.7×→7.8× (the ledger's own λ=4e-5) [checker: dominance robust under both, the absolutes are convention-bound]; fire collapse 44.6× at the plane's F=48.
Fork bill (od 3) 0.216–0.230% of the stream saving, the fleet's own 0.05–0.25% [checker] — immaterial. Certificates: belt 130× over T*; fleet 2.07–10.2× a session horizon (1.2e5 gs) but 0.03× e29c's 8e6-gs flown fence — the fleet fork recurs ~30–130× per T*, so the claim is "never a session event", not store-lifetime [checker].
Adoption: the calendar-item change first (digest-neutral, b560), then w11, then the od-1 gates scoped to belt+fleet. P1–P5 held (P4 against a misidentified horizon baseline [checker]); quotes 5/5 on a fresh 4,590-highlight export (compose_family.py, 0.1 s).**


**Standing (033c, scout — od 4 measured: no crossover in child dolls; the tube-family dies at GEO scale, and at the fleet lattice radius itself the kill is not shown [checker-corrected]).** The w11 family certificate inside Home's doll, on the shipped kick formulas' structure at the plane's real constants: at the fleet lattice radius r = 4,740 root the word's Xi saturates at ~1.9e-4 (dx beyond ~3e4 wraps the ring — the tide across the whole fleet ring is the bound), first fork 682–716 kicks (h = P/16) — but that integer is a common-mode wrap straddle: the checker's Moon-phase sweep moves it 682–3,367 at fixed dx 1e4, and the run's own disagree_frac (0.16% at 4,740/dx1e4 vs 4.5% for the 1 AU control at dx1e4) says the fleet-lattice stream is 99.84% shared, ~28× st…

**Prior standing (b560, components — od 2 executed engine-side: the intern key exists in the engine, and the belt's clock cannot reach it).** Two same-orbit planets at δx = 10⁶ root (the doll split's aligned grid, step.rs:19) **co-fire at ONE calendar key through 383 fires (25,525/25,525 censuses, identical steps 2³⁵; r = 2 AU: 25,526/25,526, 2³⁷)** — only a step change by a factor of 2 forks it. Checker extensions, all confirming: F = 16 families (δx 10³ and 10⁶) co-fire 41,328/41,328 through 1,513 fires; e = 1/20 and synodic drift (planet 1 AU, family 1.3 AU) change nothing; 6,303 fires (16× the horizon) still no fork; and a cross-r pair (1.00/1.15 AU, different orbits) co-fires 99.80% of censuses until its H change forks it at fire ~1,485 — **the sharing class is th…**

**Prior standing (a877 — the word half, off-engine): certificate Ξ = h·H·δx/(2⁻¹¹·v)** (H the sources' tidal tensor; on `force::acceleration` + `step.rs::quantize` verbatim). The 61-bit word splits every family on every kick; at 11 fraction bits the root doll shares over measured horizons (0 forks to δx 10⁶ at 1 AU, ring included) but not forever (checker: first fork at kick 14,030/57,638 — the truncation straddle forks any δx > 0 at a certified rate). D(t) bounded at every radius; the Fermi fleet doll keeps the planet-doll regime; the tube-family is the root-doll form.

## Refuted

- **NEW — "where the crossover is (a tube-family at what ρ beats the Fermi frame's lattice
  cost) is unmeasured" (the page's od-4 premise): measured — there is no crossover inside the
  doll at any dx where the family word still holds (the lattice's linear-tide residue is
  1.4–210× below the family differential at every child-doll dx; checker: it is exceeded at
  star-doll dx ≥ 5e5, so "at every arm" is false), and the family word dies within ~10² kicks
  above ~1.5×10⁴ root radius (69 at 15,000; 3–5 at 47,400; the r²·H cadence law), so the Fermi
  lattice owns child dolls above that radius and the tube-family is a belt/LEO/root-doll object
  (20261021-1551-scout-033c + checker; at 4,740 itself the steady rate favours the family — see
  Current best — so the LEO kill is unproven).**
- **"same-key members fire at the same tick and keep one intern key in the shipped
  calendar, as the construction (shared step size and anchoring) implies" (the page's od-2
  premise): refuted for the shipped clock — root-doll ships share neither step nor anchor nor
  key at any δx > 0 from birth (16 distinct dues at every census, both radii); the intern key
  holds only on the doll split's aligned grid, which ships do not run
  (20261021-0607-components-b560).**
- **"One kick per ship erases the sharing" as a property of the physics (225d's reading):**
  refuted — it is a property of the 61-bit word; at the family width the stream is shared
  (0 forks, 30 synodic periods, 1 AU ring included) (20261020-2158-m2-meso-motion-a877).
- **A position offset at equal velocity as a "formation":** refuted — that is a different
  orbit; Kepler shear separates it at ~n·δx (the family is the same orbit at a phase
  offset) (a877).
- **"Ξ < 2⁻¹⁶ ⇒ bit-identical forever" (a877's own certificate line):** refuted by the checker
  at 10× the horizon — the truncation straddle forks any δx > 0 at a certified rate; the rate
  is certified, the zero is not (a877 + checker).

## Open directions

1. **The gates at the family word** (the adoption question): B13's encounter-phase sensitivity
   vs a bounded 2⁻¹¹·v error; B12/B17/B18 on a w11-family plane. One named experiment — the
   gold experiment. Now sharpened: the plane needs BOTH w11 (the dv) and a family-anchored
   grid (the key) — b560 prices the second alone at F× slots and F×
   fires. **Sharpened by 033c (checker-corrected): the belt's sharing horizon at dx 1e4–1e5 is
   554–13,512 kicks ≈ 35–845 belt orbits across the three arms (h = P/16; 4:1 alone gives
160–845), so the gate's fork budget per plane session is ~10¹–10³ forks per belt family,
   not one.**
   **Scoped by 1673's ledger: the gates' memory payoff is the fleet/driven row (the
   phase-locked belt is the compact store's, 2.6–5 B vs the family's w-floor 8–32 B; the
   locals and GEO are dead domain), and the adoption order is the calendar-item change
   first, w11 second, gates last.**
2. ~~The engine-side key census~~ **Executed (b560): the answer is no for ships, yes for doll
   bodies — see Current best.** The unflown half: `fleet.rs`'s members are doll bodies; do real
   fleet dolls already co-fire on the aligned grid (free interning today)? Checker (code read):
   the queue's keys cannot merge OR share — `key_of` returns (tick, id) and the queue keys by
   deadline + moved, so every body is its own entry; a shared fire needs a calendar-item change.
3. ~~The fork handler as H_live~~ **Closed at the belt by composition (1673): worst
   recurring cadence (1 fork/35 orbits/member, the 3:1 anchor) at the dearest handler
   (58 µs full rebind) bills 1.66 µs/B/orbit against a stream saving of 721–768 µs/B/orbit
   = 0.216–0.230% at F = 16–2,700 — immaterial; the belt certificate is a store-lifetime
   event (130× over the ledger's own T* horizon). Checker: the 0.3% bound is
   convention-fragile (0.46% if boundary combs were free — still immaterial), and the
   fleet's own bill (fork every 43–210 LEO orbits, 58 µs, saving 16×35.1 µs/orbit) is
   0.05–0.25% — od 3 closes for the fleet too. The unflown half is od 4's steady belt
   disagree rate (the fleet's is 0.16%): it prices the handler only if it is re-bind-class
   AND ≫ the fleet's rate.**
4. ~~Child-doll families~~ **Executed (033c, checker-corrected): dead above ~1.5×10⁴ root
   radius (69 kicks at 15,000; 3–5 at GEO scale; the r²·H cadence law, checker-confirmed at
   the untested 15,000) — no crossover with the Fermi lattice at any child-doll dx. At the
   fleet lattice radius itself (4,740) the kill is NOT shown: the 682–716 first fork is a
   phase-lottery straddle (Moon-phase sweep 682–3,367) and the steady disagreement rate there
   (0.16%) beats the 1 AU control's (4.5%). Next experiment, rate-based: phase-ensemble
   steady re-sync rates for family vs lattice at 4,740 and the belt, plus the lattice's own
   span certificate above GEO scale — at what radius does the *lattice* need per-member
   refinement, and does the shipped fleet doll refresh rather than carry a word?**

## Contradictions

None open. a877's word barrier and b560's clock barrier compose (the word gates the dv, the
grid gates the key; neither alone shares the event). cell-rebind's B13 kill remains the nearest
gate neighbour: its error accumulated per kick; the family word's is sigma-delta-bounded —
different error type, same gate. 033c's control fork at dx 1e6 (653 vs a877's 14,030) is
conjunction-geometry sensitivity of the first-fork integer, not a conflict: both arms' H_eff
and Xi laws agree (the 1 AU domain is Home-conjunction-driven either way).

## Runs
- 20261020-2158-m2-meso-motion-a877 (silver): the family certificate measured — w61 splits at
- 20261021-0607-components-b560 (silver): od 2 engine-side — the aligned grid interns
- 20261021-1551-scout-033c (silver): od 4 measured — no crossover in child dolls; tube-family dead above ~1.5e4 root radius (r²·H law, checker-confirmed at 15,000); belt sharing 35–845 orbits at dx 1e4–1e5; first-fork integers are phase-lottery order markers, at 4,740 the steady rate favours the family over the 1 AU control (checker).
- 20261021-1655-library-1673 (library, silver): the ledger composed — family = fleet/driven population (113–245× bytes there, 44.6× fires at F=48, the 10⁹ kick row swings 0.69–6.87× on fleet share; checker: 1.7–7.8× on the ledger's own λ); phase-locked belt stays compact's; locals/GEO dead domain (11.6–17.3× beyond kill); od 3 closed by composition (fork bill ≤0.23%; fleet's own 0.05–0.25%).
