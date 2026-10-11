# Predictions (written before the decisive run)

The probe drives one body's kicks directly (`step::process` on a cloned record, frozen universe
snapshot) and shadows each kick with the jet alternative: keep the tube frozen at the last
recompile, carry every fired kick exactly as a velocity correction plus its free-flight position
response, and recompile only when the shadow's position error crosses a bound.

Cases (from `scenario::plane`, seed 1, none tuned):
- Orbiter 3 (`ships[14]`): low orbit about Home, tide + moon, the WH-split kick path.
- Hauler 1 (`ships[1]`) and Hauler 6 (`ships[6]`): 0.5–8 AU about the star, kicked by three
  planets, the fictitious-clock kick path (the motion law v2).

Predictions:

1. **Rebind rate.** On all three bodies, ≥ 80% of kicks fire (`dvq != 0`) and rebind —
   consistent with the five-run "recompiles on ~99% of kicks".
2. **Jet interval (the held-out number).** Between recompiles the shadow's relative position
   error grows roughly quadratically in elapsed kicks (C·drift², the red-team's law), so the
   kicks-between-recompiles at a 10⁻⁶ relative bound is ≥ 50 on the quiet bodies. On the
   Orbiters (a stronger tide) the interval is shorter than on the Haulers, by between 3× and 30×.
3. **No secular leak.** Within every recompile interval the error resets to ~0; the distribution
   of per-interval *maximum* error stays at the bound (bounded error type, not a walk): the
   median interval max is within 3× of the bound chosen.
4. **The degenerate case** (named, not run): a deep flyby's kicks are larger than any bound, so
   the jet recompiles per kick and degenerates to today's cost — no loss where kicks are rare,
   the win is on the quiet majority of body-time.
5. **Cost.** With from_state at ~17.5 µs of a ~36 µs kick (measured on this machine before these
   cases), a recompile rate of 1/R per kick puts the jet's kick at ≤ 20 µs whenever R ≥ 5
   (i.e. a ≥ 1.7× per-kick speedup on the quiet bodies).

What would kill the claim: intervals of ~1 kick at a 10⁻⁶ bound on the quiet bodies (the jet
buys nothing), or an error that keeps growing across recompiles (the carry leaks).
