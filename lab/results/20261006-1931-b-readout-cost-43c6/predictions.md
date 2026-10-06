# Predictions (written before the decisive run)

The change: the partial step's force, today evaluated at read time (the sources decoded and the
field summed per readout), is read from the kicks' own samples instead. `kick_clock` stores the
acceleration it already computed (velocity quanta per tick, in the binding's `Kick.dv`, which the
clock law leaves at `[0, 0]` today), and `observe::partial` completes the tube with a force linear
in time through the base binding's sample and the one before it. No source is decoded and no field
is evaluated at read time; the readout becomes one tube decode plus integer arithmetic.

Cases I have not tuned on, and what I expect there:

1. **The readout-vs-map ratio** (`the_readout_between_kicks_reads_the_boundarys_error`, gate ≤ 3,
   today 1.11×): the ramp's force error is the extrapolation of a linear fit over one step,
   `O(ä·h²)`, against the map's own `O(h²)`; at 128 kicks per orbit in the far field
   `(h/T)² ≈ 6×10⁻⁵` of the raw tube's pending half kick (4×10⁻⁴), i.e. ~2×10⁻⁸ against a map
   error of 1×10⁻⁶. I predict the worst ratio stays under **1.5×** (the ramp adds almost nothing
   to the readout's error budget in the far field; near passes the clock's own step shrinks
   faster than the force varies).
2. **The jump tests** (`the_readout_at_a_boundary...`): the ramp is anchored on the *base*
   binding, which does not change across a kick inside a step, so the readout is continuous
   across kicks by construction (today 3.3×10⁻⁹ of the velocity, gate 1×10⁻⁷); across a boundary
   the correction tends to zero with τ, and the jump is the ramp's error at the far end of the
   step, `O(ä·h³)` — I predict under **3×10⁻⁵** of the velocity (gate 1×10⁻⁴, today 1.1×10⁻⁵) and
   under 2×10⁻⁷ of the radius (gate 5×10⁻⁷, today 5.7×10⁻⁸).
3. **The second-order test** (`the_readout_error_falls_as_the_step_squared`): the ramp's error is
   `O(ä·h³)` in the impulse (one order below the map's `O(h²)` read at boundaries), so the
   readout should keep falling with the map output at the same 16× between 2⁻⁶ and 2⁻⁸. I predict
   every judged ship still passes (ramp ratio ≥ 0.5× the map's fall, ≥ 8× where the map falls 16×).
4. **Purity** (same test, clause 2): the ramp reads the base binding and its predecessor; both are
   in the history any settled-to-t universe holds (the shipped held branch already reads one back;
   the prune margin is 2·light-distance + 2²⁶). I predict the bit-identity assert holds. If the
   predecessor is pruned in one universe and not the other, this is where it breaks — the fallback
   would then be a state-dependent zero-slope, and I would see it here.
5. **Cost** (`readout_cost`, `universe --bench`): the pieces measured 9.9 µs sources + 3.3 µs mid
   decode + 1.7 µs field + 3.3 µs endpoint decode against a 3.2 µs raw tube (Linux x86, shared).
   Deleting the first three predicts the ramped readout at **≤ 1.3× the raw tube** (~4 µs here;
   on the M1, ~3 µs against 2.6 µs), and the bench's `view_gather` p50 back to **≤ 1.2 ms**
   (today 1.47 with 12 ships near the star; 1.13 before the partial step landed), with
   `frame_cpu_ms` p50/p99 holding or improving.
6. **B13** (assists): the flybys' energy and angular momentum are decided by the kicks, not the
   readout; the readout only feeds the view and the clocks. I predict **60/64 unchanged** (the
   same marginal failures as the baseline, the same ships).
7. **The first step after a decision or a handoff** (no sample yet, `dv = [0, 0]`): the readout
   falls back to the exact partial step there, so I predict no accuracy change where samples are
   missing — visible only as a one-step cost blip, never in an outcome.

Kill criterion: if prediction 1 or 3 fails (the ramp's error is not one order below the map's),
the linear-force ramp is the wrong completion for this law and the run reports the measured
failure; if only prediction 2's boundary clause fails, the anchor moves one sample forward and the
kick-continuity is re-measured before any conclusion.
