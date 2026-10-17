# Predictions — 20261017-1829-taleb-75d6 (written before the decisive runs)

**The question.** ed3a's birth stagger (`ES_STAGGER`, verbatim patch) is the measured cure for the belt's
first-kick wave (17× at the window, the birth at 10⁹ costs the steady stream instead of ~2,000 cores). Its
adoption is blocked on one unmeasured gate (birth-stagger page, open direction 2): does the per-body
first-kick phase offset change the law's error CLASS on belt bodies — a new systematic ensemble bias or a
compounding term — or does it only redistribute the bounded per-body sampling offset the shipped cadence
already has (ad35: the tide error is a systematic offset ~0.5·n^-2.1, bounded, not noise)?

**Instrument.** `examples/stagger_legality.rs`: lean scene (star + the three planets + n=128 belt ships of the
ladder's own draw, k in [128, 256) of extra=256, seed 1; seed 2 held out), settled (canonical cut) to
t_wave_end + {1, 2}·P_min. Arms: off (shipped), on (`ES_STAGGER=1`), ref (shipped at step_log2 8: 2× the
kicks, the converged same-law truth). Per body: the tube's exact key — k48 (mantissa of 1/(1+e), integer),
periapsis angle (Q32, integer), periapsis (exact dyadic, printed at f64 precision) — and alive/refusals.
Errors ε = (arm − ref) per body per horizon on a = p/(1−e), e, and the apsidal angle.

**Controls (must hold or the run is VOID):**
- C1: birth keys (horizon 0) identical across arms, per body (same `ladder_ship` draw; the stagger moves
  only the first kick's tick, visible as `first_kick`).
- C2: the three planets' keys bit-identical off vs on at h=1 (the stagger touches only root-doll ships).
- C3: the off arm on the patched build is bit-identical to the pristine build (`frame_digest`, both arms
  byte-identical), re-verified by regen.sh.

**Pre-registered kill criteria (the stagger is ILLEGAL as a birth default if any holds):**
- K1 (bias): |mean(ε_on − ε_off)| > 5·(std/√n) on ln a or e at any horizon, either seed — a real ensemble
  bias the shipped cadence does not have.
- K2 (class): median|ε_on| > 3·median|ε_off| at h=1 (seed 1) — the staggered arm's error against the
  converged truth is a worse class, not a reshuffle.
- K3 (compounding): the ensemble-median per-body growth exponent of |ε| from h=1 to h=2 (error vs orbits
  completed, log-log) exceeds the off arm's by more than 0.3 — an error that compounds where the shipped
  one stays bounded.
- K4 (tail): any body with |ε_on| > 10·p99|ε_off| (seed 1, h=2) — a fat tail: a few bodies ruined.

**Pass (legal):** C1–C3 hold and no K fires. Then the stagger is a reshuffle of the same bounded offset
class, and the adoption blocker moves to the B13/B14-class gates themselves (a different instrument).

**My Fermi expectations (falsifiable, before running):**
- P1: ε_off (median, ln a, h=1) ≈ 0.5·n_orb^-2.1 with n_orb ≈ P_body/Δs ≈ 2,000-5,000 kicks/orbit →
  |Δa/a| ~ 1e-8-1e-7 per orbit; the stagger moves each body within that same envelope: median|ε_on|
  within 2× of median|ε_off|. PASS expected on K2.
- P2: mean(ε_on − ε_off) consistent with 0 (|z| < 3): the offsets are id-decorrelated. PASS on K1.
- P3: both arms' |ε| grow sublinearly with orbits completed (exponent < 0.7, bounded-offset class); the
  arm difference does not grow. PASS on K3.
- P4: the risk I actually fear (Taleb): the first interval is asymmetric by construction — the kick's
  weight stays Δs while its time moves by up to one step, so the FIRST step's split is off-centre by
  up to Δs/2 per body, once. If that one-time asymmetry dominates (it is O(Δs) local, the largest single
  term either arm pays), the staggered arm's per-orbit error could sit ABOVE the off arm's at h=1 but
  NOT grow with horizon (one-time, not per-orbit): that would fail K2 while passing K3. I predict it does
  not (the drift is exact and the kick evaluates the field at the shifted tick — the sampler stays
  midpoint-class for every later step), but this is the prediction I am least sure of.
- P5: refusals 0, dead 0, all bodies alive in both arms (periapsis > 1.2 AU, no crossings).
- P6: seed 2 (held out) agrees with seed 1 on every criterion.

**What would make the run VOID:** any control failing; a refusal; a dead body; fewer than 120 of 128
bodies readable at every horizon.
