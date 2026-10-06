# dossier.md — run 20261006-0220-scout-4ea2 (lens: scout)

## Claim (one sentence)

The plane's four B13 failures are a representation gap, now measured end to end: a flyby must be
an **event entered by analytic detection at ≥ 1.5·SOI** (the two conics already know the
encounter), after which the plane's own in-doll rule (exact planetocentric Kepler drift + tide
kicks at 1/64 of the passage) holds B13's 1% gate on the near-parabolic corner — **15/15, worst
2.4×10⁻³, ~65–120 events per encounter, independent of e_h** — where the star-doll cadence rule
passes **0/60 anywhere** and the pure Öpik one-event map (no interior) passes **≤ 7/41**: adopt
the encounter event (crates/encounters detection wired as the doll door), not the patched-conic
leg.

## Bottleneck

Board focus 1/2 (kicks dominate; the lever is cadence) and the live gate failure
"B13 60/64 (the 4 failures are near-parabolic: the cadence starves them)". The cadence
starvation is structural: the star-doll step is `2^k` of the tube's radial period, and a
near-parabolic heliocentric passage has a radial period → ∞ (or undefined, E_h ≥ 0), so no
constant in the rule can see a flyby that lasts SOI/v∞. Expected gain: B13 fixed at ~10² events
per encounter where the plane's passing ships already spend 161–644 events (measured trace), and
the star-doll cadence stops being a correctness dependency for flyby scenes at all ("no work for
no reason, so no ticks"). What it deletes: the per-passage cadence as the flyby's clock.

## Evidence (all commands ≤ 60 s, Linux box, load ~2–8 shared)

**1. The plane, reproduced with its own trace** (build: `cargo build --release -p xtask -j2`,
~60 s; `CARGO_TARGET_DIR=/home/glmlab/lab-target-2`):

```
PLANE_TRACE=1 $CARGO_TARGET_DIR/release/xtask behave --law plane --gates B13   # 3.2 s
# B13 FAIL assists: 60/64 judged ... worst ΔE 1.26e0 ΔL 1.00e0; 9 draws replaced ...
```

The trace separates the failure classes: 62 ships answer with `handoffs=1–2, kicks 89–427,
events 161–644`; the failing-class ships answer with `kicks=2 handoffs=0 boundaries=0` and
`kicks=113 handoffs=0 opens=6` — **the flyby happens inside a star-doll kick interval, the doll
door never opens**. This is the entry, not the interior.

**2. The float falsifier** (`cd lab/results/20261006-0220-scout-4ea2/work && python3
flyby_event.py`, ~26 s; writes `flyby_event.json`). Scene and protocol transcribed exactly from
`xtask/src/behave/{restricted,assist}.rs` (μ=1e-3, sep=5.27e8, R_p=4.84e4, SOI=sep·μ^0.4,
start 1.5·SOI inbound; ΔE_h, ΔL_h at the truth's t_exit; 1% gate; truth DOP853 1e-12 checked
against 1e-13 at the gate's own 1e-4 rule). Kepler library: universal variables, forward vs
DOP853 worst 6.5e-12 over 60 conics including e = 1±10⁻³ (m-meso-motion's NaN corner). 72 seeds
(48 matched to B13's distribution; 16 near-parabolic, smallest |e_h−1| ≤ 9.1e-6; 8 fast+deep),
60 judged, 12 excluded inside-planet (my stream has no prefix-stable replacement; > 10%, reported).

| law | A (41) | B (15, |e−1|≤9.1e-6) | C (4) | worst | events |
|---|---|---|---|---|---|
| L1 star-doll cadence alone | 0 | 0 | 0 | 9.5e2 | 6–334 |
| L2 Öpik one event, patch SOI | 7 | 0 | 1 | 3.6e-1 | 1 |
| L2 Öpik one event, patch 1.5·SOI | 0 | 0 | 0 | 1.6e1 | 1 |
| L3 event + interior, door SOI | 34 | 13 | 4 | 3.4e-1 | 76–129 |
| **L3 event + interior, door 1.5·SOI** | **40** | **15** | **4** | **2.4e-3** | **65–120** |

- L1 = the star-doll rule (`H = 2^round(log2(T_pass/64))`) judged alone: 0/60. The encounter
  channel is load-bearing for *every* flyby; near-parabolic is where its absence becomes
  starvation (T_pass/T_enc ≈ 8–10 measured on set B; the plane's failing ship had 2 kicks in the
  whole window).
- L3@1.5: 59/60; the one miss is worst 1.4e-2 (a set-A deep case, 40% above the gate). Set B
  errors 7.3e-7…2.4e-3 — three orders below the gate. Interior resolution is *not* the cost:
  on a probe seed the error is flat from 91 to 5796 kicks (the drift is exact Kepler; the kick
  carries only the smooth star tide).
- The **door radius is load-bearing** for deep encounters (q down to 1.2 R_p = 1.6×10⁻³ SOI):
  entering at the SOI instead of 1.5·SOI drops A to 34/41. Mechanism: the planet's neglected
  pull outside the door shifts the incoming impact parameter by ~SOI·γ_tail ≳ q when q/SOI is
  small — a *geometry* error (wrong encounter), not an error-size one (principle 2's error type).

**3. Prior-art ranking** (fit to our requirements, not popularity):

1. **Öpik–Valsecchi b-plane / patched conics** (planetary defense, gravity-assist tour design;
   Öpik 1951, Valsecchi et al. 2003 — cited via m-meso-motion's dossier; production use in
   JPL/ESA impact monitoring UNVERIFIED at source today): right *detection and geometry* form
   (the encounter as one b-plane event, zero work between), wrong *leg* at our gate (L2's 1
   event: ≤ 7/41). Steal the door, not the room.
2. **The comet Kepler map** (near-parabolic motion as one event per perihelion, phase-conjugate;
   the Chirikov-school comet-diffusion literature — UNVERIFIED at source today): the correct
   skeleton for e→1 passages — work per event, no cadence; instantiated here as the entry event.
3. **WH/SyMBA with exact Kepler legs** (the plane itself; Wisdom–Holman 1991, Duncan–Levison–Lee
   via law.md): measured sufficient at the plane's own 1/64-passage rule (resolution-flat).
4. **Adaptive steps (Sundman / log-H)**: dead by probe 1 and the 29-September prior-art scout
   (Calvo–Sanz-Serna); not re-tested.

## Predictions (predictions.md, written before the decisive run)

- P1 (L1 starves only near e→1): **failed, stronger than predicted** — L1 fails 0/60
  everywhere; the encounter channel is always load-bearing.
- P2 (one-event passes fast, fails slow): **failed** — the one-event form fails at all speeds
  here (b-amplification SOI/q dominates; mechanism found, see L2/L3 door comparison).
- P3 (event+interior ≥ 90% at ~≤70 events): **held** — 59/60 (98%) at 65–120 events (median ~94;
  my "~70" was the 1/64 rule's nominal, powers of two land higher).
- P4 (L3 insensitive to patch radius): **refuted, mechanism found** — the door must be ≥ 1.5·SOI
  for deep encounters; this is the run's second finding.
- P5 (≤ 10% excluded): **failed in letter** — 12/72 (17%) inside-planet; my stream replaces
  nothing (the gate's is prefix-stable). Judged set still 60.

## What would make it wrong; adoption cost; PRINCIPLES fit

Wrong if: the integer plane's changeover cannot compose with an event-triggered entry at
1.5·SOI (its shells engage on separation, and the ship's position between star-doll boundaries
comes from the same conics — so the risk is low but unmeasured); or the near-parabolic root-doll
*tube compilation* (not the cadence) is what the trace's `refused/lost` hides; or rebind cost
makes ~10² events/encounter expensive in integers (the passing ships already pay 161–644).
Adoption (one step): wire `crates/encounters`' Binet-cone/conjunction detection as the doll-door
event for tubes whose star-doll step exceeds the encounter duration (near-parabolic passages),
opening at ≥ 1.5·SOI; the interior is unchanged; judge by `behave --law plane --gates B13`.
Fit: "no work for no reason, so no ticks … you don't advance a ship tick by tick you just map
where it wants to go" (CL 09-29); "a fix signals the wrong representation" (CL 09-29 — resizing
the cadence is that fix); principle 33 (each scale resolves only what matters at that scale:
the star-doll must not resolve encounters, the event does); principle 26 (steal from skin in
the game — and the honest half: what the hazard community stole for screening is not enough for
our gate).

## The lens (what it may have missed)

The scout lens stopped at one float falsifier on a 2-D CRTBP: it did not wire the event into
the integer plane (the adoption step's real test), did not test 3-D inclination (Öpik's sphere,
detection in 3-D Binet space), and the relativistic encounter is out of scope here (v∞/c ≤
6.7×10⁻⁵). Two mid-run harness bugs (a frame-mixing subtraction — barycentric planet from
heliocentric ship, ~1.6% of SOI, exactly the deep-encounter scale — and a signed-time Kepler
branch) were found by convergence probes and fixed *before* the reported numbers; the first
run's tables are void, and the checker should reproduce the final `flyby_event.py` (rng seed
20261006 in `seeds()`; fresh draws are the held-out check). Cloud timings are orders of
magnitude only.
