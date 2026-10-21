# Dossier — 20261021-1346-library-1fd7 (library lens)

**Claim.** The desynchronised grid at cbe6's measured belt floor deletes the kick-comb row
of the 1e9 single-doll era ledger (658× → 0.39–0.58× of the 69.75-s era budget), it is the
last cadence lever on that row (4/conjunction FAILS B12), and its adoption hangs on two
now-frozen distributional bars the census flight must record: f_fine ≤ 1.6–3.3% (B13's
encounter class at 256/orbit) and a governing synodic period ≥ 3.4 yr — at 77-d-class
forcing the row stays 15× over even at the floor.

**Bottleneck.** The board's top macro row (kicks per body, ~10³ at stake; HANDOFF's
"Real bodies" row through CPU = bodies × kick rate × kick cost). Measured multiplier:
kick rate ÷1,144–1,689 (two measured anchors compose). What it deletes: the doll-wide Δs
as a policy (one `kicks_log2` per class replaces it; ext.rs:146 — the clock constants are
already computed per body), and with it the kick row as a 1e9 term. What it does NOT
delete: the scan channel (walks 111–311× + answers 61×, cadence-invariant — the tier's
row, b57f), memory (the plateau b30b is steady-state per body), the fleet row, the wave.

**Evidence** (zero flights; composition on page-cited measured constants, cf2a/6793
precedent; commands < 1 s each, full regen ~5 s):
- `python3 compose_desync.py` — the whole composition. Inputs: λ_ship 4.889e-5 kicks/B/gs
  (nladder: 0a46/8365/9ed1), kick payload 45.5 µs (8365), kick comb 12.75 h/era = 658× the
  69.75-s era budget, walks 2.15–6.02 h, answers 1.19 h (a2c0/20f2/a31c), cbe6's floor
  (8/conjunction PASS, 4 FAIL; belt 2–3 AU, Jupiter-class forcing: belt orbit 3.95 yr,
  S 5.93 yr), board anchor ~9,000 kicks/belt-orbit, B13's 256/orbit (7076).
  Outputs: R = 1,144 (rate anchor) / 1,689 (board anchor); kick row → 0.575×/0.390×;
  f_fine ≤ 1.57%/3.33%; S_bar = 1.077e8 gs = 3.41 yr; 77-d forcing R = 44 → 15× over;
  post-desync ledger 173–373× (from 830–1,030×; ÷2.8–4.8 total).
- `python3 verify_quotes.py` — 5/5 byte-identical against the fresh cache (L4 a
  contiguous span; L1/L2/L3/L5 full highlights); cache = 4,590 highlights (fetch_readwise.py).
- Shipped-code citation (grep): `crates/universe/src/ext.rs:146`
  `constants(ctx, d, t, except, kicks_log2)` — per-body clock constants behind one global
  dial; `step.rs:558` `step_for(&self.rec.b, …)`. The desync is a policy change, not an
  algorithm.

**Predictions** (predictions.md, written before both scripts ran): P1 headroom
[1.0e3, 1.8e3] — HELD (1,144/1,689). P2 kick row ≤ 0.6× — HELD (0.575/0.390). P3 census
band [1.5%, 3.5%] — HELD (1.57–3.33%). P4 S_bar ∈ [3.0, 4.0] yr and 77-d row ≥ 10× —
HELD (3.41 yr; 15×). P5 ledger lands ~170–370×, wall to the scan channel — HELD
(173–373×). P6 quotes 5/5 — HELD. P7 wt/cadence's 4/Cinder-period sits at ≤ 4/conjunction
(2/conjunction if the period base holds 2 conjunctions), at/below cbe6's FAILING point —
HELD as a check to run, not a verdict (wt/cadence's population may not be the belt).

**What would make it wrong.** (a) Payload constancy: the composition scales the kick row
linearly in cadence at fixed 45.5 µs payload — measured flat at ÷8 (98cb), unmeasured at
÷10³; a coarser Δs that changes the refit cost breaks the 0.4–0.6× landing (not the
direction of the closure, only its margin). (b) Scene transfer: cbe6's 8/conjunction was
measured on a Jupiter-class forcing scene; the plane's belt must be censused for its
governing S — a close-in forcing keeps the row open (15× at 77-d). (c) The census bars
assume the fine class pays 256/orbit uniformly; a fine class that is also the class the
scan channel walks (passages) couples the two rows. Adoption cost: one policy change
(per-class kicks_log2) + one legality flight (B12/B13/B14/B17 at per-class Δs) + the
census flight (f_fine, S_gov, resonance fraction as three fields) + the payload arm at
deep splits. Fit with PRINCIPLES: "you don't advance a ship tick by tick you just map
where it wants to go" (CL 09-27) — the conjunction is where the ship wants to go; the
doll grid is the tick. And "a lever under 2× on its row is not worth a run" (board) —
this one is ~10³ on its row, but only ÷3–5 on the composed ledger, so it must land WITH
the tier, not instead of it.

**The lens.** A library run composes; it does not fly. The two bars and the payload
assumption are exactly what a flight run (components/system on cbe6's harness) must now
measure; this run's numbers are only as good as the page constants they cite (all
checker-reproduced), and the rtf/unit conventions of two ledgers (the era ledger here,
the 686f/ef63 s/s ledger) were kept strictly separate — the add-back (0.548 s/s, time-
barred, cadence-independent) belongs to the second and is untouched by the desync.
