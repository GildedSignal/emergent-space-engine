# Dossier — 20261018-1025-scout-fbf9

**Claim.** The encounter row's missing constant is answered by mechanism: after a
belt-quantum kick, the pairs that must be re-checked are the near-horizon time-window
band — **0.034 arm-evals per body per kick at cells of 10⁴ (law n·W·(H+2)·⟨|Δa|⟩/T̄_syn,
i.e. ∝ n² at fixed density: 0.0034 at 10³, 0.034 at 10⁴, 0.34 at 10⁵), not fe6b's
0.034·n = 346** — so the churn term falls ~6 orders (≈197 cores → ≈2×10⁻⁴ cores at
10⁹, 1 µs/arm, 1 kick/body/interval) and the row's CPU closes on cd3b's stream terms
alone; the price is that the *event list's miss-distance content* is kick-fragile
(~50–70% of an 8-interval armed list re-lotteries per quantum kick), so armed lists
must be slack in miss space and re-decided at the due, never stored exact across kicks.

**Bottleneck.** Encounter work at 10⁹ (board row 2): cd3b priced the event flow
(≤1.9 cores worst-case mint) and left "pairs re-checked per kick at 10⁹-scale
occupancy" as the row's whole unknown ("if n is the cell's 10⁴ bodies it is ~10¹–10²
cores after split 8"). This run kills that term: nothing near 10¹–10² cores is forced
by the physics; what re-checks remain are O(1)-per-body. Deletes: any per-kick
wholesale re-arm of cell-mates; any design that stores exact armed lists across kicks.

**Evidence** (all from `toy.py`, ~10 s, `sh regen.sh`; planar 2-body Kepler, shipped
scenario constants: belt a∈[2,3) AU, e Rayleigh 0.07, reach B = 5×10⁵ m, interval =
P(2.5 AU)/4.43, horizon 8 intervals; kicks dv/v = 2⁻²³ at a random anomaly, pre/post
compared at the same anomaly):

- **A, dilute cells at fixed 10⁹ density** (6.37×10⁷/AU² annulus; W = n/(ρ·2πa)):
  wholesale candidates/kick = n−1 (99/999/9999, slope 1 — the fe6b structure
  reproduced; fe6b's own 0.0346 constant not expected to match, its X and anchor are
  not in the record here). **Armed pairs and flips per kick: 0 at every n and dv**
  (upper bound 1.5×10⁻³ flips/kick/body at n=10⁴ over 200 kicks; intra-cell armed
  probability is ~10⁻¹¹ — cell-mates at 10⁹ density are co-orbital to 10⁻⁵ AU, T_syn
  ≈ 7.4×10⁵ intervals). Near-horizon band (first-meeting due < H+2): **0 / ~0 / 0.030–0.035
  per body at n = 10²/10³/10⁴** — the analytic law n·(H+2)·⟨|Δa|⟩/T̄_syn gives 0.034 at
  n=10⁴ (match to the digit), 3.4×10⁻³ at 10³ (consistent with 0 counts, expected 0.7);
  seeds 777/424242: band 0.050/0.065, flips 0 — seed-stable.
- **Due-walk geometry (P3):** per-kick due-move is multiplicative, δdue ≈ due·(δn_i/Δn_pair):
  median cell-mate walks 10⁵–4×10⁶ intervals per kick (huge far out — slack bookkeeping
  in due-space is worthless intra-cell), while in-horizon partners walk 1.5×10⁻⁵ intervals
  (wide-band, ×6.1 at dv×8, ×9.9 at dv×64 — linear in dv) and 0.7 intervals for
  near-co-orbital in-horizon pairs — the walk is small exactly where arming is decided,
  which is what makes the band test sound.
- **A2, live anchor** (partners sampled at true density over ±0.35 AU, ×7000
  extrapolation): armed ≈ 525–1050 per body per 8-interval horizon (Poisson-limited) —
  same order as cd3b's flow (their n₂D = N/25 vs this N/15.7 explains the residual
  ~1.6×). **Flips at the bare-B certificate: 0.5–0.7× armed per quantum kick** (saturating
  to ~2×armed = decorrelation at dv = 2⁻¹⁷): the miss-distance, not the time window,
  churns (a 2⁻²³ kick moves r(θ) by ~0.2 B). In a due-queue design this costs no CPU
  (the event is re-decided once at its due) but it forbids storing exact armed lists.
- **Controls.** B (soundness): closed-form arming is a strict superset of a 9,000-step
  brute-force conjunction scan on a live wide band (reach amplified to 0.02 AU so
  events exist at N=80): 11/11 events covered, 0 missed. C (negative): a no-margin
  schedule (horizon = rebuild window, no mid-window re-arm) loses 2 events/100 kicks
  at dv=2⁻¹⁷ and 5 at 2⁻¹⁴ — the instrument can fail. D (concentration, fleet-class
  shared-(a,e,ω) ring, σ_λ = 5×10⁻⁶ rad): **standing 543.2 per body** (Θ(n): the
  predicted 0.27·2000 = 540, the taleb-09b5 ruin class), flips 33 on / 344 off per kick
  (dissolution-dominated; the binary toy has no dwell, so off-flips are an upper bound —
  b509's 16.8 newly-armed/kick at F=10⁴ is the same class, UNVERIFIED constant, different
  scene).

**Predictions.** `predictions.md` was written (and amended once, disclosed in-file,
before any run): P1 held (slope-1 baseline); P2 held in substance (flips ≤ 0.1:
measured 0; band 0.034 ≤ 0.1 at 10⁴) with the amended n²-at-fixed-density letter
confirmed by the analytic-constant match; P3's amended multiplicative law held
(in-horizon wide partners 1.5×10⁻⁵ ≪ 0.1; near-co-orbital in-horizon pairs exceed the
0.1 letter at 0.7 — disclosed); P4 held (standing 543 ≥ 1, flips ≥ 0.1); P5 held
(0 missed; negative control loses events; second seed stable).

**What would make it wrong.** The toy is 2-body mean-longitude Kepler with an r(λ)
radial model — no mutual perturbations, no GR, no e > 0.4; the near-band constant
inherits that geometry. The composition to cores assumes 1 kick/body/interval, 1 µs
per arm eval (b509's measured 1.02–1.16 µs), and cells that are U-bins of the belt's
own density; a different cell geometry (angle-sliced) changes the band law's constant,
not its n² shape. The kill test for the whole claim: fly the near-band rule on the
shipped tier at 10⁴ occupancy and measure re-arms/kick — if they are Θ(n), the toy's
window model missed a churn channel (the standing class D suggests where to look:
dwell). Cost of adopting: the tier's per-kick path becomes a due-band test instead of
a candidate re-arm sweep (a wiring change on `tier::arm_pair`'s callers), plus the
miss-space slack rule for stored armed lists. Fit: PRINCIPLES 3 ("nothing is evolved
that can be derived when looked at" — dues derive, only the band re-arms), 14 ("no
work for no reason"), 15 (local laws), 22 ("the simulation tells us what is next").

**The lens.** The scout searched MD (Verlet skin: LAMMPS rebuild-on-displacement) and
kinetic data structures (Basch–Guibas: flight-plan updates recompute certificate
failure times, verified in the KDS survey literature) — both map cleanly, and the run
is their mechanism priced. What the lens may have missed: fields where the certificate
is the *miss distance* rather than the time window (event-driven MD's time-of-impact
ordering — contact-speed's page just closed that door for contacts); and the lab's own
b509 slack machinery already implies half of this — the new content is the dilute-cell
constant, its n² cell law, the multiplicative due-walk, and the miss-space fragility.

**Grade suggested:** silver — one flight on the shipped tier (re-arms/kick at 10⁴
occupancy, the dossier's kill test) away from gold.
