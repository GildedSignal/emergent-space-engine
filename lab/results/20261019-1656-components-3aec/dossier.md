# Dossier — 20261019-1656-components-3aec (components lens)

**Claim.** After 73b5 killed the churn row's wholesale arm, the 10⁹ CPU ledger is
**91–97% one component, the kick/event stream** — and that row is **rate-bound at its
floor**: at a765's ~6 µs arithmetic floor the shipped cadence alone costs 24 M1 cores
(6× the 4-core budget), so closure *requires* the cadence cut (split 8 × survival, 4.92×)
*and* a cost ≤ ~5 µs/event — both levers the board already owns, neither optional; with
today's measured cost (82.5 µs/kick-item x86, this run, flat in N) the post-73b5 total is
**40.5–43.4 cores = 10–11× budget**, and cd3b's "1.3–2.1×, not a physics gap" reads
2–4× optimistic against the measured constant.

**Bottleneck.** The board's #1-adjacent question ("bodies in the flyable engine", via the
interlocking CPU ledger) and the lens's own: the stream component's floor and idiot index.
Floor ladder at the measured fired rate λ = 4×10⁻⁵/body/game-s (0659), 10⁹ bodies, rtf 100
→ 4×10⁶ events/wall-s: **write floor 50 ns → 0.20 cores; arithmetic floor 6 µs → 24;
cd6e's composed kick (8–19 µs) split8 → 6.5–15.4; 262f's native 4 µs → 3.3; shipped
cadence, today's cost → 193; today's cost split8 → 39.3.** Idiot index today: 39.3/4 ≈
10× over budget after the welded rate lever; 193/0.2 ≈ 10³× shipped. What it deletes:
any plan that closes 10⁹ with a cost lever alone (Carlson adoption without the cadence
octave leaves 15.4/4 ≈ 4×; the cadence octave alone at today's cost leaves 9.8×).

**Evidence** (all commands ≤ 60 s; Linux x86, 8 vCPU shared, load recorded in work/):
- `nladder 10000/100000 coast 10` (probes.log): anchors reproduce 097e same-day —
  b/body 2458/2348 (097e 2464/2348), p50 engine 0.043/0.049 ms, kicks 1920 = 1920
  across the decade (**the belt is inert over 10 s wall: the flown stream is the
  player's and the locals'**, first belt item p50 14,071 game-s = 141 wall-s away).
- `belt_first 10000`: belt first-item p50 **14,071 game-s, locals 661 — cd3b's anchors
  to the digit** (P5 held).
- Prof build, 540 frames (prof1e5.log, prof1e4.log): **item: kick 82.5 µs/call**
  (286.8 µs/frame ÷ 3.48), boundary 18.4, apply 7.6, root walk 7.0; **N-flat**
  (82.4 at 10⁴); the frame is idle-cheap (p50 0.046 ms) and the stream hides in event
  frames (p99 5.3 ms, events/frame p50 2 → max 212) — a flat frame ladder does not
  certify the 10⁹ stream.
- `python3 ledger.py` (~1 s): the full composition above, every constant cited;
  corrected post-73b5 totals: today-cost 40.5–43.4 cores (10.1–10.9×), cd3b-letter-cost
  6.5–12.5 (1.6–3.1×), arithmetic-floor closure 4.9 + churn 0.35–1.4 + mint 0–1.9 +
  view 0.1 + frame 0.72 ≈ **4.4–9.0 cores = 1.1–2.3×** — the ledger's honest floor.
- **A 2× I cannot derive and flag for the checker:** cd3b's letter composes 208 shipped
  → 8.4 with only split 8 × survival (÷4.92 → 42.3, or ÷26 as their letter implies);
  my composition from their own published constants gives 23.8 at their 29.3 µs cost.
  The direction of every conclusion is unchanged by the 2×.

**Predictions.** predictions.md, written before the decisive runs: P1 held (anchors,
belt inert), P2 held (82.5 µs in the predicted 45–90 high side; main carries no 5ade
carry), P3 held (letter-cost total 6.5–12.5 vs predicted 6.5–12.4), P4 held — the
decisive one: arithmetic floor at shipped cadence = 24 cores ≥ 10, so the cadence octave
is mandatory and the row is rate-bound, P5 held to the digit. No kill branch fired.

**What would make it wrong.** (1) The 82.5 µs is the locals'/player's kick (planet-class
keys, the dearest population; a765's 63–75 µs plane rebinds corroborate); the belt's own
wave is 59–76 µs/kick (b30b, x86) — same class, but if the 10⁹ belt's fired items are
materially cheaper (weak-branch compiles at 4.4 µs, the attendants share smaller), the
shipped row falls toward cd3b's 117–208 and the composed row toward 8–16: the
rate-bound conclusion survives (it uses no cost). (2) λ is 0659's clock-path measurement
(doll tides, no belt–belt channel); a stirred belt re-opens it (budget-1e9 od 3).
(3) The x86→M1 conversion rides cd3b's 208/355. Cost of adopting: none — no engine code
changed except the nladder Linux footprint stub (work/patch.diff); the numbers feed the
integrator's ledger and the closure bar (≤ 4.9 µs/event at split8+survival) for
b-readout-cost. **Fit with PRINCIPLES:** "no work for no reason, so no ticks" (#14) —
the stream's cost is cadence, not arithmetic, exactly the principle's cut; "the right
question, then the representation" (#18): the row's question is *how many events*,
not *how dear*; "errors never compound" untouched (no law change).

**The lens.** First-principle one component: the floor ladder is the deliverable. What
the lens may have missed: the neighbours — the mint (0–1.9) and churn (0.35–1.4) rows
are composed, not re-measured; and the 10⁹ belt's own fired-item cost was never flown
(needs a 141+ wall-s flight or a stirred belt — the named next run on both counts).
