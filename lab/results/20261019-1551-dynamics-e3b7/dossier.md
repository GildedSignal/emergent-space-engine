# Dossier — 20261019-1551-dynamics-e3b7 (dynamics lens)

## Claim (one sentence)

The only gravity wiring available to the shipped lattice (per-body, per-chronon rounded
1/r² kicks through `Kickable::kick`) is **unstable at belt scale**: a contact-free cold
belt self-heats and self-destructs by t ≈ 10–25k chronons (maxk 99k → 727k at 0.02–5
contacts/ch; the thermal cold control reaches 72.9M contacts and 449/800 evicted by
49k, both seeds), so e56b's leftover — the plateau's lifetime under gravity — is
**unanswerable on this wiring**, and the fleet season that does stand (83–86% eviction
of the belt in one crossing, the 140–250q shell emptied) hands over to the *same*
self-generated grinder the cold belt reaches alone.

## Bottleneck

chaos-shadowing open direction 2's named leftover ("the gravity-held belt — confined
without walls — the plateau's lifetime there"), through the board's smoothness line:
what standing contact load does the game's belt geometry put on the scheduler. The
answer found is upstream of the question: the representation available today cannot
hold a belt, and the missing gate (a cold gravity-held belt with bounded eccentricity
at long horizon) is now measured, with its onset time and its seed robustness.

## Evidence

Shipped `Chronon` + `Law::RelativisticV1`, Q = 2^20, MU = 70·2^52 (v_circ(70q) = q/16),
belt = 800 bodies on rings 36–102q, ±q/2 position jitter, v_circ ± thermal, fleet =
800-body coherent stream at 0.25 q/ch (1.9–3.6× v_esc), field = integer kicks
dk = −round(MU·x/r³) (sub-quantum and zero beyond r ≈ 757q; clamp ±q/16 below r ≈ 2.2q).
Regenerate everything: `regen.sh` (~8 min). Digests rerun-identical; `--slim` (no kept
events) verified digest-identical on a 512-ch pair (`37cfa9f0…`).

1. **The wiring's own instability (the P1 kill branch, fired honestly).**
   - C0 (cold, thermal = 0, contacts 0.02/ch for 8k ch): maxk 99,194 → 151,731 →
     379,827 → 726,985 across the four 4k-ch blocks; rms radius *grows* 77.7q → 91.8q;
     escapers begin at t ≈ 12k. Orbit diffusion with essentially zero contacts: the
     pump is the tide representation, not contact noise (digest `e8a69ff7…`).
   - C s1/s2 (cold, thermal ±q/256, H 49152/16384): calm through t ≈ 4–8k (0.26–2.26
     contacts/ch, esc ≤ 5), then self-destruction: 262 → 930 → … → 2871 contacts/ch,
     449/800 evicted, endpoint n_in 309, rms 37q, maxk 686,460 = v_esc(1q) (s2 tracks:
     446 → 1271/ch by 12–16k). digests `634d9918…` / in `work/`.
   - Mechanism (read off the C0 ladder): per-component rounding makes the kick not
     exactly central (torque noise), and one kick per chronon samples the 1/r² field
     too coarsely near pericenter — the classical discretization eccentricity pump.
2. **Walls arm (GW, box ±150q, H 24576):** esc = 0 always (walls contain even the
   self-destruction debris), n_in *grows* 1189 → 1360 (recycled fallback), rms radius
   arrested at 72–90q (no contraction), while contacts climb 403 → 5732/ch (totals: 78.3M contacts;
   digest `79b89629…`). Wall hits total 14 896 (mean 0.61/ch, per-block rate FALLING
   0.88 → 0.31/ch: the box, unlike free space, re-absorbs the debris until contacts
   take over as the cost).
   Containment converts the tide's slow leak into a standing dense soup of the full
   1600 bodies — e56b's "persistence is the confinement's" reproduces here in the
   contaminated sense: with a leaking tide, walls do not rescue the belt, they recycle
   its debris at growing rate.
3. **The fleet season stands in the clean window (t ≤ 8192, cold control esc ≤ 5
   there).** G s1/s2: the crossing evicts 83% of all bodies by t = 4096 (esc 1327/1600)
   and 86% at saturation (1376; s2 1374); the 140–250q shell is *empty* from t ≈ 4k
   (every body either inside 140q or beyond 250q — there is no bound halo, no
   wall-free plateau of any kind); the bound remnant is ~200 bodies at rms 46q.
   esc crosses 50% of n at t = 2211 (s1) / 2222 (s2). Season peak 64-ch window 183 685
   ≈ 2276× the cold mean window in the same window of the control (P2 far exceeded).
4. **The late grinder is the wiring's attractor, not the fleet's bequest.** G s1
   49152: remnant contracts rms 46.2q → 15–21q while contacts rise 1431 → 2771/ch
   (ke_in flat 8.6e11 → 7.4e11: compaction, not heating; late rattle 0.63). The cold
   control *alone* reaches the same object (2871/ch, n_in 309, rms 37q at 49k). P3's
   branch (b) "grinder" was registered as a fleet outcome; the measurement reassigns
   its cause to the wiring — the fleet only buys earlier entry (~2k vs ~10k ch).
   P5 held everywhere (maxk constant after first contacts *within the fleet window*;
   ke_all monotone down after the season peak) — but the C0 arm overrides P5's
   "no injection" reading at long horizon: the injection is real, slow, and contactless.
## Predictions

Written before the ladder (`predictions.md`). P1's kill branch FIRED (cold control
fails past t ≈ 8k; my 2048-ch smoke calibration was blind to it — the instrument
lesson, same class as ded5's fixed-window lesson). P2 held (season ≫ 20× cold). P3
resolved to branch (b) grinder, but its cause is reattributed by the C0 discriminator
(not available to my prior). P4's letter (esc ≈ 0) held; its "≥10× cold" held trivially
for the wrong reason (the tide leaks on its own). P5 held in the fleet window and was
overridden at long horizon by C0.

## What would make it wrong

- C0's contacts are not exactly zero (0.02–5/ch late): a contact-mediated amplifier
  could ride on a weaker field-driven seed. The discriminator bounds it: the maxk
  ladder is established by t = 12k when cumulative contacts are ≈ 20k ≪ the thermal
  control's 73M.
- MU is 70·2^52 and the belt sits at 36–102q: the pericenter sampling error scales
  with (v·Δt/r)² — a colder/denser field or a coarser kick cadence (per-cell tide)
  changes the onset time. The onset (≈10k ch at this scale) is a parameter of this
  scene, not a constant; the *mechanism* claim is the transferable part.
- Not tested: self-gravity, warmer belts, a tide cadence ≠ 1/chronon, kick symmetric
  rounding (round-to-nearest-even on the pair jointly, or a rotation-exact scheme),
  horizon > 49k.

## Cost of adopting / fit with PRINCIPLES

Nothing to adopt into the engine; one gate to add before any belt wiring: **a cold
gravity-held belt must hold bounded eccentricity for ≥ 5× the belt's own dynamical
time at the shipped tide cadence** (here: onset 10k ch vs orbit period 7k ch — it
fails its own gate by a little, and monotonically after). This is Julien's "a fix
signals the wrong representation" (P19) measured at the law's own surface, and the
lens brief's "an instability … a gate we lack". It costs one rung-shaped harness
(`gravitybelt.rs`, kept in this run's patch) and no crate change; `main` untouched.

## The lens

The dynamics lens trusted its mechanism prior (quench by ejection drain) against its
own control discipline; the control won, which is the system working. Remaining lens
bias: "grinder" language implies a persistent object — the horizon ends mid-growth,
and the C0 mechanism says the object is the tide's error flow, not a self-organized
attractor of bodies; a better integrator would delete it (check: rerun C0 with kicks
every 4th chronon at 4× magnitude — predicted onset moves by < 4×, since the error is
pericenter-sampling-dominated, not cadence-dominated).
