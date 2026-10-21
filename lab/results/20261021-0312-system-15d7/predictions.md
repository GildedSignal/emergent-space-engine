# Predictions (written before the decisive run)

Question: does the BOUNDARY comb ever *do* work on the belt's own stream, or is its payload
(surface / leave / handoff certificates) already implied by state the body holds (the energy
register and the tube's key)? The nladder page prices the comb (5.9–8.6 µs, ~50% of the belt's
stream, -50% deletion buys 1.2×) but has never counted fires.

Cases I have not tuned on, and what I expect there:

- **P1 (belt, coast, 3×10⁴ bodies, ~2 eras):** boundary combs ≈ 1 per belt body per era
  (~50% of the event stream, matching the page's 49.7/50.7% split), and **fires = 0**
  (no crash, no leave, no handoff). Belt bodies are clock-stepped in the root doll, and
  `boundary_clock` has no handoff arm at all — so handoff fires are structurally 0 there.
- **P2 (belt, the phase of the kick):** if the belt's kicks sit at periapsis (birth wave at
  one Δs), the boundary's surface check happens at apoapsis — the *maximum* of r — where it
  cannot fire before the kick's own surface check (kick_clock checks the surface at every
  kick). So crash fires 0 is expected *by mechanism*, not by luck.
- **P3 (control, plunge scenes):** the instrument must be able to see a fire. On the shipped
  plunge tests I expect boundary crash fires to be **0 as well** (plunges are ended by the
  kick's surface check or the planned `What::Crash` item, not the boundary), which would mean
  the boundary's crash arm fires only for apoapsis-phased kicks — a narrower domain than its
  cost suggests. If fires > 0 there, the wiring is proven and P3 reports where the arm lives.
- **P4 (leave is derived-when-looked-at):** every belt body's energy register stays negative
  through the flight (bound ⇒ finite apoapsis far under `leave_log2`), so the leave
  certificate is one comparison on state the body already holds — no readout needed.

Kill criterion for the claim: belt fires > 0 at a rate above ~1e-3 per comb kills the
"certificates already implied" reading for the belt, and the run reports the firing bodies.
