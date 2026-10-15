# predictions — 20261015-1615-scout-ee30 (written before the decisive run)

Question: what must the view's missing engine half — the birth/death feed for the row-set
deletion (view page, open 1: "the p99 owner") — cost, and does it delete the 240-frame
rescan (3.5 µs/body, 2df1's checker) at the ladder's N?

Instrument: float replica of the ladder scene's own birth law (scenario.rs:333-344:
belt a ∈ [2,3) AU, e Rayleigh 0.07 redrawn > 0.4, uniform angles, prograde) with the
shipped client's map criterion verbatim (page.html drawMap: square window in the star's
frame centered on the observer's current position, half-width W, testing each body's
retarded offset; fitted W from fitLog ≈ 7× the nearest local's distance). Observer:
circular at 1 AU (Home's neighborhood). Retarded positions by fixed-point (2 passes).
Kepler propagation exact to < 1e-12 (Newton on E). Costs composed at r_event = 2 µs
(277d measured 480–700 ns/conjunction on x86, + margin for the row-form recompute;
UNVERIFIED for this certificate's exact shape).

Arms: coast-belt (W = 750 ls, long horizon), coast-fitted (W = 3.5 ls), burn (β to 0.05
radial over 600 s), zoom (W 3.5 → 750 ls at ~1.5 dex/s, the wheel's pace), controls.

Pre-registered expectations, each with its kill:

- **P1 (steady flux, belt zoom):** entries+exits < 0.01 per game-second at N = 1e5 —
  the set changes slower than once per 100 s (orbital periods are years; ~2 boundary
  crossings per orbit per in-window body). KILL the feed's adoption case if ≥ 1/s: the
  scan pays ~0.875 ms per game-second at 1e5 (3.5 µs × 1e5 / 400 game-s between scans at
  flying pace), so a ≥ 1/s flux at 2 µs/event is < 10⁴× and the rescan's replacement is
  not the claimed deletion class.
- **P2 (fitted zoom):** zero belt events over the whole horizon, and the belt's minimum
  distance to the window > 100×W (the group envelope — annulus vs box — is disjoint for
  a whole session; the 73-row set is arithmetic, not luck). KILL if any belt row enters:
  then per-body certificates are needed even at fitted zoom.
- **P3 (burn):** a 0.05c radial burn over 600 s adds < 1e3 entries at N = 1e5 (swept
  area × belt density), worst feed frame < 1 ms of certificate work. KILL if the burn
  alone re-imposes a per-frame Θ(N) term.
- **P4 (zoom burst):** the exponential wheel sweep concentrates entries in its final
  frames (swept annulus ∝ W² at constant dex/s): worst frame ≥ 1e3 events at N = 1e5,
  and at N = 1e6 the worst frame crosses 16.7 ms of certificate work at 2 µs/event —
  the drain (the 4487 budgeted-drain pattern) is REQUIRED for zooms, not optional.
  KILL the "feed is free" framing if the burst is flat instead (then the zoom is cheap
  and the drain claim is wrong).
- **P5 (controls):** belt-out window + moving observer: 0 events (specificity);
  belt-straddling window: > 0 events (sensitivity). Either failing voids the instrument.
- **P6 (composition, arithmetic):** at 1e9 the steady-state feed composes to < 1e-3
  cores while the rescan composes to ~8.75 cores (3.5 µs × 1e9 / 400 game-s): the scan
  alone would eat the whole 4-core budget; the feed must not.

Lens disclosure (scout): the cross-field mapping (kinetic data structures' certificate
scheduling; incremental view maintenance's delta rule; netcode interest management) was
chosen for fit to the engine's own event/certificate method, and may under-weight
client-side draw costs — out of scope here, named on the view page already.
