# Dossier — the belt crest is a two-comb limit cycle; compute-ahead is priced

**Run:** 20261017-0005-dynamics-8ffc (dynamics lens). **Claim:** the belt's freeze crest is a
stable, period-halved two-comb limit cycle — one kick comb at phase ≈ interval/2 (51.6–53.8 µs
an event) and one boundary comb at phase ≈ interval (12.6–13.2 µs), each exactly ≈ 1.0 event
per belt body per 28,141.5-game-s doll interval, both decaying only −2.5 %/interval over 3.7
intervals — so the freeze recurs every half-interval forever at shipped cadence, idle-time
compute-ahead fits the whole cycle at the player's pace with 10.8× (3×10⁵) and 3.2× (10⁶)
headroom but is 308× short at 10⁹, and every kick-counted 10⁹ stream ledger undercounts the
belt by the boundary comb's ~+26 % CPU.

## Bottleneck

Board #1 (bodies in the flyable engine) and #3 (the kick/stream cost), through the named
recurrence gate: promotion.md direction 3 ("the stagger's recurrence gate (≥ 3 intervals, the
unprinted second spell, 9e75-checker2) before idle-time compute-ahead is considered at all")
and kick-cadence's checker2 note ("a full second spell not yet printed"). 4093/9e75's
"≥ 19.3 h of clamped delivery per interval at 10⁹" assumed per-interval recurrence; nobody
had printed past crest 2. What it deletes or unlocks: the compute-ahead certificate
(PRINCIPLES #17, "Use idle time to compute ahead — yes this is a whole important idea"), and
a missing term in the 10⁹ CPU ledger.

## Evidence (shipped `nladder` coast; patch = print-only instrument: 9e75's Linux footprint,
per-spell table, per-frame trace, wall cap raised — no law, no schedule change)

Flights (sequential, load 0.12–0.38, 14 GB free; peak RSS 1.45 GB):

- **A (decisive):** `300000 coast 150 1800` — 104.4 s wall, 9,000 frames, presented to
  ~103k game-s = 3.7 intervals, **7 crests**.
- **B (N-control):** `100000 coast 60 3600` — 48 s wall, 7 crests, same structure.
- **C (near-player pace):** `300000 coast 100 300` — 46 s wall, crest 1 + the idle between.

**The crest table (A; spell = merged clamp run ≥ 60 frames):**

| crest | mid (game-s) | Δmid | events | kicks % | spell wall | µs/ev | law ratio |
|---|---|---|---|---|---|---|---|
| 1 | 14,741 | — | 299,808 | 98.7 | 21.8 s | 51.6 | 1.01 |
| 2 | 28,804 | 14,064 | 265,785 | 1.2 | 4.8 s | 12.6 | 1.03 |
| 3 | 43,390 | 14,586 | 295,725 | 98.4 | 21.8 s | 52.3 | 1.01 |
| 4 | 57,236 | 13,845 | 249,302 | 1.6 | 5.0 s | 13.2 | 1.09 |
| 5 | 70,917 | 13,681 | 297,510 | 97.6 | 22.7 s | 53.8 | 1.02 |
| 6 | 85,435 | 14,518 | 226,639 | 1.9 | 4.3 s | 12.8 | 1.07 |
| 7 | 100,372 | 14,936 | 292,119 | 97.3 | 21.7 s | 52.2 | 1.02 |

**Two interleaved combs, one per half-interval** (spacing 14,072 = interval/2, alternating
composition). Per comb, spacing = the full interval (kicks: 28,650/27,527/29,454; boundaries:
28,431/28,200; interval 28,141.5).

**Delivery-independent comb masses** (game-time windows, `combs.txt`; immune to clamp-window
artifacts — the spell table undercounts the cheap boundary crests by 10–24 %):

- A (3×10⁵): kick comb 1.034 / 1.027 / 1.005 / 0.982 kicks per body per interval (decay
  0.993, 0.980, 0.975); boundary comb 1.035 / 1.022 / 0.990 (decay 0.987, 0.969). The
  locals' fixed comb is 10,138–10,276 events/window at BOTH N — subtracting it, each belt
  body fires **exactly 1.00 kicks + 1.00 boundaries per interval**.
- B (10⁵, rtf 3600): identical structure (kick 1.102/1.095/1.073 incl. the locals' 0.101;
  boundary 1.104/1.090/1.062; decay ≈ 0.98/interval). Crest 7 truncated mid-drain by the
  flight's end (excluded from decay).
- **C = A bit for bit:** kick window 1 [11.8k, 18.5k] game-s reads **310,224 kicks /
  10,138 boundaries at rtf 300 AND at rtf 1800** — the game-time demand is rtf-invariant to
  the digit (the determinism control).
- Fine structure (kick crest 3, drained under clamp): one unimodal pulse — 90 % of the kick
  mass within ~1,635 game-s, the q25–q75 core ~900 game-s, no doll-octave sub-peaks; phase
  interval/2 + 1.2k ± 0.7k game-s.
- Between combs: 3.13 ev/game-s background (both arms, same digits), and at rtf 300 the
  engine idles at **p50 0.903 ms of the 12 ms budget** (events/frame p50 1) while crest 1
  still clamps 16.7 s (E 232,972 in-spell, Ĉ 51.0, law 1.011). Arm A's p50 at rtf 1800 is
  11.9 ms — at 18× pace the baseline stream itself saturates; the combs are what the player's
  pace feels.
- Positive controls: crest 1 at 3×10⁵ rtf 1800 reproduces 9e75 (E 299,808 vs 298,465,
  +0.5 %; spell 21.8 vs 20.9 s; Ĉ 51.6 vs 49.9); a 10⁵ smoke reproduced 7.0 s / 97,554 vs
  their 7.1 s / 96,995. Law ratio (spell wall vs E·Ĉ/0.72): kick crests 1.01–1.05 everywhere
  ✓; boundary crests 1.03–1.17 — two of seven (B's 1.121/1.174) outside the pre-registered
  ±10 % band, so those spells' timing is flagged; their counts (deterministic) stand.
- refusals 0, dead 0, player alive on every arm; E/N identities hold after the locals'
  subtraction (K3 did not fire: 1.00 per comb).

**The mechanism is law-native:** `boundary_clock` (`crates/universe/src/step.rs:725`) is
documented as "the synchronised output of the split, in the middle between two kicks" — the
doll step's two halves. A phase-locked belt (genesis at tick 0) therefore carries one kick
comb and one midpoint boundary comb per interval, by construction. The metronome identity
(kick-cadence: "2^step_log2 events per P_D per body") was read off the kick half; the belt's
true stream is **2 events/body/interval**.

**The compute-ahead ledger** (per interval at the player's rtf 100: whole-engine budget
0.72 s/s × 281.4 s = 202.6 s; bill = 1.00 × 51.6 µs + 1.00 × 12.9 µs per body):

| N | comb bill per interval | vs budget | verdict |
|---|---|---|---|
| 3×10⁵ | 18.8 s | 10.8× headroom | fits |
| 10⁶ | 62.5 s | 3.2× | fits — the 69–73 s 10⁶ spell (9e75, derived) is schedulable |
| 10⁹ | 62,503 s | 308× over | capacity-bound: no scheduling cure |

Between combs the budget sits ~92 % idle at the player's pace (C's p50 0.9 ms; checker2's
p50 2.0 ms at rtf 450/100) — the idle exists exactly when the combs' bill must be
pre-computed. At 10⁹ the clamped delivery per interval is bill/0.72 ≈ 24 h (9e75's 19.3 h
was kicks-only; the boundary comb adds ~25 %), and recurrence means every interval.

## Predictions (predictions.md, written before the flights)

- **P1 (recurrence): held in substance** — every crest ≥ 0.75 × E₁, spacing = one interval
  per comb; **formally wrong on epochs**: I predicted crests at 14,072 + k×28,141.5; the
  cycle is period-halved (crests at k×14,072, alternating composition — crest 2 measured at
  28.8k, predicted 42.2k). The miss is the discovery: the second comb.
- **P2:** held — kick comb ±1.3 % in-spell (±2.5 % by window mass); boundary −1.3 to −3.1 %
  per interval (window mass), not the −9 % the spell table suggested.
- **P3:** held — widths 1.1–8.3k game-s; kick widths 3,036→5,630→5,537 (×1.8 then flat);
  note width is partly a delivery-window property (the same crest reads 1,134 at rtf 300).
- **P4:** held for all kick crests (1.01–1.05); failed for 2 of 7 boundary crests (1.12,
  1.17 at 10⁵ rtf 3600) — flagged, counts unaffected.
- **P5:** half-held — structure N-invariant, epochs identical; E/N 0.99 (3×10⁵) vs 1.08
  (10⁵) in-spell, reconciled exactly by the locals' fixed comb (0.101/body at 10⁵) in the
  window masses.
- **P6:** refuted for half the cycle — kick crests are 92–99 % kicks, but the even crests
  are 94–99 % boundaries. The pre-registration missed the boundary comb.
- **P7:** held exactly — 10.8× / 3.2× / 0.003× at 3×10⁵ / 10⁶ / 10⁹.

No kill criterion fired: K1 (crest 2 < 0.1 × E₁) — crest 2 is 0.89 × E₁ by window mass;
K2 (spacing ≠ interval) — spacing is the interval per comb; K3 (E/body outside [0.5, 2.0])
— 1.00 per comb.

Regen note: the rerun (`regen.sh`) reproduces every deterministic number — window masses
to ≤ 1 event in 310,224–310,225, spacings, phases, composition — and the timing-side
numbers (spell E, walls, µs/ev) to a few percent (e.g. B crest 1: 108,426 vs 108,035; the
clamp-window membership is the only moving part).

## What would make it wrong

- The comb masses are deterministic counts on one scene (`plane_extra`, seed 1) — a
  different belt birth law (the staggered genesis, f82a) de-phases the combs by design; the
  cycle measured here is the SHIPPED genesis's. The stagger does not delete the combs' mass,
  only their phase-locking — the bill per interval is unchanged, so the ledger stands for
  any de-phase that keeps cadence (and a de-phased crest is its own compute-ahead).
- The 10⁶ row is arithmetic on measured per-body constants (1.00 × 51.6 µs + 1.00 ×
  12.9 µs), not a flight (10⁶ build is 2.34 GB > this lab's 2 GB cap); 9e75's independent
  10⁶ spell derivation (69–73 s) agrees with bill/0.72 = 86.8 s to 20 %.
- Ĉ is x86 here (Linux cloud box); the M1 re-measures (lab rule: orders of magnitude).
- The +26 % ledger correction assumes `BELT_SPLIT` stretches the boundary comb with the
  kicks (its code position — "the middle between two kicks" — says yes); if it does not,
  the composed ledger's miss is larger. One flight of the composed arm with this instrument
  decides it (the named next experiment).
- Wall and µs numbers are shared-box timings (state in `work/state-a.txt`); every
  load-bearing number (window masses, spacings, phases, composition) is a deterministic
  count, reproduced bit-identically across rtf 300/1800.

## Cost of adopting, and fit with PRINCIPLES

Adopting the reading costs nothing (it is a measurement); acting on it has two prices.
Compute-ahead is a scheduler change the integrator owns: pre-compute each comb during the
idle half-interval before it is due (the combs' due times are known — they are the metronome
itself), then the crest costs ~nothing at presentation; the certificate question is whether
anything observes a body between its event's due time and its early application (scans,
views, encounters) — unmeasured here. The ledger correction (+26 % belt stream CPU at 10⁹
at shipped cadence) reprices e7ef/98cb's closure arithmetic. Fit: "Use idle time to compute
ahead — yes this is a whole important idea of this project" (CL 09-25, PRINCIPLES #17) —
the cycle is the predictable demand that idle time exists to serve; "the algorithm that
allocates the work to prevent those heavy tails, it's the most important one" (CL 09-25) —
the heavy tail is now measured as a periodic, predictable comb, not a stochastic spike.

## The lens

The dynamics lens looked for the attractor and found a limit cycle; what it may have made
me miss: (a) the burn arm (9e75 measured no freeze there — the crest overruns instead), so
this cycle is coast-only; (b) the de-phased arms (stagger, chain) — their crest profile is
qualitatively different and my ledger prices only the shipped phase-lock; (c) one seed, one
scene — the combs' phase stability across seeds is untested (the mechanism says it is
genesis-locked, f82a's train result agrees).

## Reproduce

`regen.sh` (≈ 4 min warm): applies `work/patch.diff`, builds, flies A/B/C, runs `crest.py`
and the window-mass script (`combs.txt`). Every number above is in `work/arm{A,B,C}.log`,
`crest.txt`, `combs.txt`.
