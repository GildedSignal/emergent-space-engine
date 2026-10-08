# Dossier — run 20261008-0458-system-5a2c (lens: the whole system)

## Claim

The distinctions that decide whether 10⁹ bodies fit in 8 GB are minted by the **memo key's shear**, not
by the grain: a belt's birth program dies within ~10² orbits (every body takes a new 12-bit key every
~50–100 orbits), records shared at the key width split by a broad, power-law shear (not chaos), so the
population program and the kick layer must be **one mechanism** — a reband (re-program) loop that
re-absorbs the smooth secular flow — and H_live on the dashboard must count the reband residue, not
scars against a static program (which saturates to N and measures nothing).

## Bottleneck

Board: "fitting 10⁹ in 8 GB … decided by distinctions created per game-second" (HANDOFF: "not measured
yet"; risk list). Expected gain: turns an unmeasured, design-blocking question into a measured rate
(~10⁻² splits/body/orbit at belt scale) and deletes the wrong instrument before `b-belt-wire`/`b-h-live`
land: without a reband loop the belt bills 16 B/body (16 GB at 10⁹: the goal fails on tube bytes alone);
with rebands every ~50 orbits it bills ~0.5–2 GB.

## Evidence (all commands ≤ 60 s, Linux/x86 cloud — orders of magnitude only)

Scene: 6,143 belt bodies (a ∈ [2.1, 3.3] AU, e Rayleigh 0.07) + 1 M☉ star + Jupiter (μ = 9.55×10⁻⁴,
a = 5.204, e = 0.049), heliocentric leapfrog at 775 steps/P_Jupiter (≈ 290/belt orbit; integrator noise
±0.5 key quantum, 0.027 crossings/orbit floor, measured by a no-Jupiter control). Keys = the law's memo
quantization (`crates/space/src/orbit.rs`: MEMO_SHAPE_BITS = MEMO_SCALE_BITS = 12, relative):
scale = round(log₂ r_p · 2¹²), shape = round(log₂(1−e) · 2¹²). Twins: same elements, r_p offset by 0.4
and 0.1 quantum — bodies sharing (or bordering) one memo cell; their separation is common-mode-immune
to integrator noise.

```
cd lab/results/20261008-0458-system-5a2c
python3 hlive_belt.py dtest                        # ~10 s: dt PJ/150 vs PJ/300 agree (flux integral)
python3 - <<'EOF'                                  # ~2 s: no-Jupiter control (noise floor)
import numpy as np, hlive_belt as H
H.MU_J=0.0
r=H.run(6143,100.0,775,seed=9,checkpoints=[0,int(100/(H.PJ/775))],extras=False)[0][-1]
print(r['frac_off'], r['cross_per_body'])
EOF
python3 - <<'EOF' > main775.log 2>&1               # ~44 s: the decisive run (see main775.log)
import hlive_belt as H
H.run(6143, 2400.0, 775)
EOF
```

Measured (541 belt orbits, full log in `main775.log`):

1. **The birth program is a transient.** 99.4 % of bodies are off their birth key within 2 orbits
   (osculating short-period jitter ≈ 2–3 quanta amplitude; the engine's orbit-averaged billing sees the
   mean-element drift instead). Steady state: 0.018 key crossings/body/orbit (noise floor 0.027; the
   twin separations give the clean mean rate: median record moves ~6 quanta per 541 orbits, p90 ~34).
   Every belt body takes a new memo key every ~50–100 orbits. A static `shipmem` program (Form P frozen
   at birth) scars the whole belt within ~10² orbits of game time; H_live measured against it saturates
   to N and stays there.
2. **Records shared at the key width split by shear, not chaos.** Same-cell twin pairs: 50 % split by
   ~104 orbits (0.4-quantum offset), 89 % by 541; at 0.1-quantum offset 55 % by 541. Separation grows as
   orbits^0.5–0.6 (diffusive power law, not exponential), broad across the belt (70–99 % in every
   a-band, weakest at the inner edge farthest from Jupiter — tracks the forcing strength, not the
   resonance map: 2:1, 3:1, 5:2 bands are not special). Mechanism: within-cell δa → δn → conjunction-phase
   slip; the key trajectory is **not a function of the key**, so per-key kick sharing (the natural
   extension of the cycle memo, ~10⁷ occupied cells ⇒ ~80 bodies/key at 10⁹) is wrong at 12 bits beyond
   ~10² orbits.
3. **Flux is cadence-invariant.** dt and dt/2 give the same splits and crossings (dtest) — the flux is
   an integral, so the queued q-cadence/averaging levers buy CPU only. The memory lever is elsewhere:
   reband cadence and stored widths.

## Predictions

`predictions.md` was written before the decisive run. Held: (1) fast program death — stronger than
predicted (99 % within 2 orbits, not 60); (3) dt-invariance. **Failed, reported as held-out: (2) "twins
mostly stay together, <20 % split" — the smooth flow is NOT re-absorbable *per key* at the 12-bit width**
(89 % split). My mechanism model was wrong: I expected the shared flow to carry whole cells; instead
within-cell offsets shear apart through the conjunction phase. Prediction (4) (sublinear occupancy) was
an artifact: in-scene N is too small (occupancy ≈ 1 at 2×10³ bodies); the ~10⁷-cell / ~80-per-key figure
at 10⁹ is analytic (belt extent in (log₂ r_p, log₂(1−e)) at 12 bits), flagged as inference.

## What would make it wrong

- A second perturber or the belt's own grain (excluded here; r8 measured 427 real encounters per 20
  orbits on belt 0 — a per-body rate ~10⁻⁶/orbit, negligible against 10⁻²) could add splits; that only
  strengthens the finding. Weaker Jupiter (or a shorter game) stretches the ~50–100-orbit scale
  linearly with the forcing but cannot remove the shear.
- The engine's integer Carry rounds sub-quantum kicks by truncation; if its accumulator suppressed
  within-cell shear (it cannot — the shear is a differential secular drift, far above the carry), splits
  would be slower. A rung should re-measure the split rate on the integer law (see cost below).
- My floats measured element drift; positions/residuals on the integer grid could differ in the constant,
  not the scaling (r2's lesson: widths set by behaviour).

## Cost of adoption, and fit with PRINCIPLES

Adoption: (a) `b-h-live` must define H_live as **reband residue** (splits not re-absorbed + grain), else
it reports a saturated, meaningless number on the first belt; (b) `shipmem`'s `seal`/repack becomes a
scheduled doll operation (reband every ~50 orbits at belt scale, cost O(occupied cells) ≈ 10⁷ writes —
7 % of even the averaged kick rate 0.3/body/orbit: memory maintenance is not a CPU risk); (c) per-key
kick sharing is dead at 12 bits over ≥10² orbits — do not build it; (d) phase columns stored at the
view's floor width, not 96 bits, or rebands cannot pay. Fit: principle 3 ("Compute only surprises" — the
shear is not a surprise, the reband loop is its readout), principle 32 ("Symmetry is found, not given" —
the shear-free frame is the reband grid), representation.md line 89 ("orbits indistinguishable at the
stored width become one record" — measured: such records share for only ~10² orbits), plane.md's own
definition of H_live ("against what reabsorption removes" — the removal mechanism is the finding).

## The lens

The whole-system lens found two mechanisms secretly one: the population program and the kick layer are
the same object at two timescales, and the seam between them (`shipmem` Form P frozen at birth) is where
the 8 GB goal currently leaks. What it may have missed (named case that could break this): **dense
scenes** — fleets, battles, rings — where the grain (real encounters at ~1/cell/light-crossing) mints
distinctions faster than any reband can absorb; there H_live is honestly per-body and the dense order's
entropy floor (~4 bits/collision, H0173), not the secular shear, decides the bytes. This run measured
the belt regime only; the fleet regime needs its own probe before the dashboard number is trusted there.
