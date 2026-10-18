# Dossier — 20261018-0932-fermi-cd3b (Fermi lens)

**Claim.** On the shipped belt geometry the 10⁹ encounter row's *event flow* is measured-Fermi
and cheap — ~0.22 **contacts**/game-s and ~1.1×10³ Dohnanyi-class conjunctions/game-s at
N=10⁹, i.e. ≤ ~1.9 M1 cores even if every conjunction mints a key at the measured 16.4 µs
and ~0 for everything else — so the row's 62–571-core span is **100% certificate churn,
which rides the kick cadence** (one dial with the stream), while the stream itself composes
to **5.3–8.4 M1 cores** on this week's measured levers (split 8, secular survival, boundary
fast path) against the 4-core budget: a 1.3–2.1× gap, not a physics gap.

**Bottleneck.** The board's #2 row ("encounter work at 10⁹: ~10³–10⁴ cores; what cuts it by
10³") and #3 ("the kick: 10³·³"). This run says: the 10³ cut already exists for the *flow*
(it was never the flow); what is left is (a) the churn constant — pairs re-checked per kick
at 10⁹-scale occupancy, unmeasured on the live anchor — and (b) 1.3–2.1× of stream glue.
Expected gain: retires the kick row's 10³·³ as a 10⁹ lever (confirming e7ef on 18-Oct
constants) and names the one number the next encounter run must measure.

**Evidence** (all from `python3 lab/results/20261018-0932-fermi-cd3b/ledger.py`, ~1 s, plus
`cargo run --release -p emergent-universe --example belt_first -- 10000`, ~10 s; Linux x86,
8 vCPU, load 1.8, 13 GB free; full JSON in `ledger-out.json`):

*Anchor (P1, held to the digit):* `belt_first 10000` → belt first-item p50 **14,071 game-s**
(3294's 28,141.5-s interval ÷ 2), locals p50 661 — the 2-events/body/interval identity the
ledger stands on.

*Event flow (2-D Poisson sweep on scenario.rs's own constants: planar belt a∈[2,3) AU,
e Rayleigh 0.07 (redrawn >0.4), ship radius 34·2⁻¹⁰ ru = 49 m with 1 ru = 1,477 m from the
Moon's 1,176-ru radius — game AU = 1.4962×10¹¹ m ≈ SI AU to 0.1%; n₂D = N/25 AU²,
v_rel = 1.8 km/s, own period 12,480 intervals = 3.52×10⁸ game-s):*
- contacts (b ≤ 98 m) at 10⁹: **0.224/game-s** = 7.9×10⁷ per own orbit (P2 held:
  predicted 0.1–1.5). One contact somewhere every ~4.5 game-s — at 10⁹ real bodies the
  shipped belt *grinds*; this is the fragmentation/combat feed, and it matches 09a1's gold
  contacts term (0.9 bits/s ≈ 0.22 ev/s × ~4 bits) in order.
- conjunctions at b ≤ 5×10⁵ m (2b89's key-mint scale): **1,140/game-s** (P3 held);
  at b ≤ 10⁷ m: 2.3×10⁴/game-s.
- CPU of the flow at rtf 100: exact evals 0.068 cores (277d's 0.6 µs), contacts 2×10⁻⁵
  cores, key minting **1.87 cores if every conjunction re-mints** at 5567/efd4's 16.4 µs
  (P3's "≤0.1 cores" FAILED on this term — honest miss); with efd4's intern (513→2 standing,
  gold) repeats hit the intern and only distinct-pair formations pay, so the mint term is
  0–1.9 cores and must be measured, not assumed.
- Cross-checks, no >10× disagreement (P5 did not fire): rate ∝ density exactly vs ec74's
  gold λ ∝ Ψ^0.95; 1b1f's 0.105–0.247 encounters/body/orbit at N=800 implies their b was
  2.7×10⁸ m (P4 held) — contact-scale would have failed it.

*Stream composition at 10⁹, rtf 100 (P6 held):* shipped 208 M1 cores (2 ev/body/interval ×
10⁹ × 100 × 29.3 µs; x86 355). Composed: split 8 (de7b, welded) × survival 0.615 (1a46)
→ kicks 8.0 M1 + boundary **0.40** with 16ec/49e9's fast path (clock path 4.4–5.6 µs →
0.21–0.27 µs; bulk is a ns-class digest-neutral skip) = **8.4 M1 cores**; with RES survival
0.385 = **5.3**. 4e2d's 10.3 reproduced within 20% (they carry the pre-fast-path +25%
boundary). Closure needs 14.6 µs/event (vs today's 29.3; e7ef said 23) or one more cadence
octave beyond split 8 (S* = 1.3–2.1 further): **1.3–2.1×, not 10×**. At the 42-ns floor
even shipped cadence is 0.30 cores — the kick-cost scoreboard row stays retired as a 10⁹
lever.

**Predictions.** `predictions.md`, written before either command ran: P1, P2, P4, P6 held;
P3 held on rate and exact-eval cost but **failed on the mint term** (1.9 cores, predicted
≤0.1 — the 16.4 µs creation cost times 1,140 mints/s at rtf 100); P5 (kill criterion) did
not fire.

**What would make it wrong.** The flow model's three ±: A_eff (25 AU², ±2× → contacts
0.1–0.5/s), v_rel (±30%), and the mint-per-conjunction semantics (0–1.9 cores). If 2b89's
live-anchor tier must *exactly evaluate* candidates at a rate scaling with occupancy rather
than with conjunctions (fe6b's pairs/kick = 0.0346·n·…, n = cell occupancy), the churn term —
not modelled here, deliberately — dominates and the row keeps its 62–571-core span: that is
the one number to measure on the live word. Cost of adopting: none (arithmetic + one shipped
example; no code changed — `work/patch.diff` is empty and regen needs no patch).

**Fit with PRINCIPLES.** "Compute only surprises" (#3): at 10⁹ the surprises are 0.22
contacts/s — the row's cost is all certificate, i.e. scheduling, and "the simulation decides,
heuristics schedule" (#22) says price the churn per kick, which it does. "The memory floor
is information" (#24) — the flow's information is 0.2–1 bits/s, matching 09a1.

**The lens.** Fermi estimates delete; this one deletes the board's "cut encounters by 10³"
as a *flow* problem. What the lens may have missed: the churn term's occupancy scaling
(fe6b's law at 10⁴-body cells could be ~10¹–10² cores after split 8 — if so the row is still
the CPU ledger's biggest unknown, and my "one dial" framing is optimistic); and the game
could deliberately run belts 10-100× denser than the shipped geometry, rescaling the flow
linearly.

## Machine state
Linux 6.8.0-111, 8 vCPU, 15 GB (13 free), load 1.81/1.10/0.54 at 09:42, shared runner,
no thermal control. Cloud x86: orders of magnitude only (per lab README); the M1 anchors
(29.3 µs) are page-cited, not re-measured here.
