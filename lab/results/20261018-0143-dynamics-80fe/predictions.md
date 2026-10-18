# Predictions — 20261018-0143-dynamics-80fe (frozen before the decisive runs)

The experiment (chaos-shadowing open direction 2, the successor e846's gold names in its lens
note): the encounter-parity certificate as a **rate/survival process**. Same ensemble as e846
(144 ICs = 12 synodic angles 15°..345° × du ∈ {±0.35…±1.45}·band, band = √(8μ/3)), horizon 512 P.
Truth: the judge's full-model integrator (rtol 1e-12), **disk-entry events** found by the shipped
`until_crossing` (resolved, never a grid). Plane: shipped plane, step 7 (kick cadence P/64), kills
= any Lost branch (e846's census). μ ∈ {1e-3 (JUPITER, control), 1e-2 (unrun)}. The statistic:
first-event survival S(t) and event rate per P, ensemble level, bootstrap over ICs.

Prior state (e846, μ=1e-3, 512 P): plane kills 47/144; truths crossing the disk at all: 39/144
(19 dead-IC + 20 kept-IC); horizon 512 P.

- **P1 (the layer thickens):** the fraction of ICs whose truth enters the disk at least once in
  512 P rises from ~27% at μ=1e-3 to **≥ 50% at μ=1e-2** (Hill radius ×2.15, thicker transport
  channel).
- **P2 (parity at the control):** at μ=1e-3 the plane's first-event (kill) count and the truth's
  first-entry count agree within counting noise: ratio ∈ **[0.8, 1.4]** (47 kills against 39
  first-entries prior; the survival curves cross inside the bootstrap bands).
- **P3 (parity tightens at μ=1e-2):** conjunction dwell inside the fixed disk scales as
  μ^(−1/2) through Kepler shear (Δv ∝ Ω·Δa, du in band units ⇒ Δv ∝ μ^(1/2)), ×3.2 longer at
  μ=1e-2, so kick-cadence detection improves: first-event ratio plane/truth ∈ **[0.7, 1.3]** at
  μ=1e-2, and the plane's kill fraction of the ensemble at 512 P reaches **≥ 60%**.
- **P4 (the hazard is a mixture, not a constant):** the truth's first-entry hazard declines over
  the horizon: h(t < 128 P) / h(128–512 P) ≥ **2** — the encounter-prone sub-ensemble (low
  osculating q, e846's dead-set q_min/S 15.6 against 138) is depleted early, so a single rate is
  NOT the certificate's form; it needs the conditioning.
- **P5 (the instrument holds at the ensemble level):** the rtol 1e-13 rerun of the events arm
  reproduces the 1e-12 first-entry count within ±5 ICs and the survival curve inside the bands;
  per-IC entry epochs scramble (the shadowing clause — expected, that is why the statistic is the
  curve, not the epoch).
- **P6 (the driver check, free):** this tree's μ=1e-3 plane dead set matches e846's 47 exactly
  (same crates/xtask code at this HEAD, deterministic engine), and therefore still differs from
  b9be's 48 in the same 3 ICs at φ = 105°.

Kill criteria: events-arm give-ups above 10% of ICs (instrument), plane arm failing to complete
the ensemble (VOID, report), or the plane refusing at build on a large fraction at μ=1e-2 (a
domain wall worth reporting, not a parity number).

Honest prior: P2's direction is genuinely open — e846's class evidence (kills are real-class
crossings) and the 20 missed kept-crossers pull opposite ways at the count level.
