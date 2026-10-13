# Predictions (written before the decisive run)

Topic: the in-flight E→1 crossing (the page's named hole: the acceptance sweep covered E→1 at
periapsis exactly, vr = 0; a burn crosses off-periapsis). Probe: `crates/universe/examples/crossing.rs`,
plane seed 1, 48 members, 1 thread. Modes: A<level> hold-forward to the first Passage (Home escape),
cut, coast; B (level 8) hold through the star-escape flip, cut, coast, then reverse-hold to the capture
flip back to Cycle, cut, coast. Levels A: 2, 5, 8, 11, 15.

1. **No level lands parabolic.** The burn steps E in finite quanta (one rebind per 1/64 of |v|), so the
   first Passage state has E−1 > 0 bounded away from the fit's cancellation band. I predict E−1 ≥ 10⁻⁶
   at every level, growing with level (bigger steps: roughly ∝ v²/64 at the crossing).
2. **The clock does not spike at the seam.** Worst |dt/dτ/u^t − 1| over the bracket [flip/4, 4·flip]
   stays ≤ 10⁻⁵ at every level, in line with the merge's 4×10⁻¹²…5.6×10⁻⁶ elsewhere — i.e. the family
   flip is not a new error wall. If it spikes > 10⁻³ anywhere, that is the result.
3. **Refusals stay zero** through every flip (the parabolic edge compiled at every periapsis in the
   sweep). Genuinely uncertain: the off-periapsis parabolic edge is exactly what the sweep did not
   cover; I would not be surprised by a small refusal count at one level. If refusals appear, the page
   gains a named hole in `from_state`, not in the key.
4. **The capture (downward crossing) compiles** at level 8: the kind returns to Cycle with k > 1/2,
   apoapsis ≈ the braking radius, ship alive, clock ≤ 10⁻⁶ after the flip. The pump finding (held brake
   below γ ≈ 1.2 pumps back up) is a near-rest regime; braking from hyperbolic far out should cross
   cleanly. Risk: it lands near parabolic from above and the captured orbit's apoapsis passes the leave
   → silent death (`fault=None`), which would tie the capture seam to the standing leave finding.
5. **The gentle levels do not reach the star crossing** in the window (A2, maybe A5 stay star-bound
   after the Home escape; only a held burn at L8+ crosses the star's E=1 in-window) — consistent with
   the L2-escape leave death being the generic fate of gentle escapes: they never leave, they wander
   out and the window ends.

What would make the crossing matter (the inversion): any of — a refusal or loss at a flip, a clock
relerr > 10⁻³ localized at the flip, a capture that dies silently, or an E−1 < 10⁻⁶ landing (inside
the fit's cancellation band, where the far-field arithmetic is known to refuse).
