Working...
Check complete: **Grade: gold**, written to `lab/results/20261017-1829-spacex-d399/check.md`; the author's wiki page corrected in place; tree restored to pristine.

**What I verified (all from a clean tree, patch applied by me):**
- **Premise**: pristine main reproduces all five N=3000 digests bit for bit — the inert patch is digest-neutral.
- **Identity**: delete arm identical on every case (runner's regen), and my own arms extend it out of the author's domain — all eight N=100/N=1000 cases, wave and belt-crossing regimes, 4 schedules each.
- **Probe (the run's own flagged risk)**: instrumented `decoded_event()` — 0 errors on the three heaviest N=3000 cases; the only corner where the arm could bind-where-shipped-refused never fires.
- **Structure by reading**: `bind_in` consumes only `trajectory/periapsis_angle/periapsis_time/clockwise`; universe has zero `Rebinding::reconstruct` calls; the residual's real consumer is space's `TubeEvent::bind`, unfown by the plane.
- **Timing**: fit ns/call −17.1% (regen) vs −18.6% (author); engine process −6.6% vs −8.2%. The −18.3% engine-p50 headline does **not** reproduce (−6.8% here) — single-pass wall noise; corrected on the page.

**Adversarial find the author missed**: `ending_at` early-returns `from_state`'s fit, so the arm also strips the residual for surface binds (creation/kicks/handoffs) — still dead, but the adoption API split must route that path; noted on the page.

Gold because: reproduced, predictions held, deletes a full Newton solve + cartesian readout per bind (bit-identity as the certificate, ~10-line adoption), refutes the page's direction-2 premise (`at_radius` 1.1 µs, 4%), and re-prices compile at 49% — the next lever's map.
