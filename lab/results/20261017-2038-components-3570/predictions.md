# Predictions (written before the decisive run)

Decisive run: `BOUND_PROBE=1 nladder 10000 coast 10 100` (the kick-cadence page's own
scale: one comb window at 10⁴), plus a held-out arm `30000 coast 8 100` if time allows.

The component under test: the **boundary event** (`What::Boundary`, step.rs:805 — readout +
two point certificates + `plan_interval`). Floor claim under test: its outcome is a function
of the binding the previous kick already compiled (r(t) ∈ [periapsis, apoapsis] of the cycle;
the plan repeats on the aligned grid), so a steady body's boundary carries no news.

Cases I did NOT tune on (the smoke was N=2000, 3 s):

- **P1 (news census):** ≥ 95% of boundary events on the belt bulk end `Resolved::Boundary`
  with `iv == iv0` and `st == st0` (the replan reproduces the previous interval and step
  exactly), no death, no handoff. If instead > 5% change the interval or step, the boundary
  carries real re-planning news and the "zero bits" reading dies.
- **P2 (margins):** belt-body boundaries sit far from the checks they duplicate — I expect
  `me ≤ -4` (r under 1/16 of the doll edge) for ≥ 95% of non-root dolls. The surface margin
  `ms` I expect bimodal: deep (≥ 4× surface) for most, with a thin population near 1-2×
  (the doll-normalized units make this scale-free; the smoke showed ms=1 rows, so I may be
  wrong here — if ≥ 10% sit at ms ≤ 1, the surface certificate is NOT margin-derivable and
  the key-range test must be exact, not margin-based).
- **P3 (cost parity):** the boundary's wall ns is within ~2× of the kick's wall ns on my
  box (both dominated by the readout/compile machinery), i.e. the same order as
  kick-cadence's 51-54 µs vs 12.6-13.2 µs ratio ≈ 4×; I predict kick/boundary ns ratio
  in 2-8×.
- **P4 (event parity):** boundary events ≈ kick events within 20% (the two combs).
- **P5 (fail mode):** if boundaries turn out to be mostly on the clock path (ext set,
  root doll) rather than the split path, the census splits by doll and the deletable class
  is the planet-doll (non-clock) one; I predict ≥ 90% of boundary events are non-clock
  (the belt is the bulk).

Kill criterion for the design (pre-registered): if P1 fails (> 5% of boundaries change the
plan) the "boundary carries no news" premise is killed and the dossier reports it.
