Grade: gold

**Abstract.** Claim: the belt crest is a period-halved two-comb cycle — a kick comb and a
boundary comb, each ≈1.00 events per belt body per 28,141.5-game-s interval — so the freeze
recurs per interval; idle-time compute-ahead fits at 3×10⁵/10⁶ (10.8×/3.2× headroom) but is
~308× short at 10⁹, and every kick-counted 10⁹ ledger undercounts belt CPU by ~26 %.
Reproduced: regen clean; window-1 masses agree to ≤1 event across rtf 300/1800
(310,224/310,225) and my rtf 3600 (310,250); recurrence holds to 4.3 intervals (3×10⁵) and
8.2 (10⁵); seed 2 keeps the phases and the 1.00+1.00 identity. Wording corrected on the
page: "forever" → the phase structure shears into merged per-interval spells after ~6
intervals; decay ratios are delivery-dependent. Adoption cost: zero (a reading); it
reprices e7ef/98cb's 10⁹ closure and passes promotion's direction-3 gate.

## Reasons

**Reproduction.** `regen.sh` exit 0 on this box (8 vCPU, load 1.9–2.1). Every deterministic
number reproduces: window-1 masses 310,225 kicks/10,138 bnd (rtf 1800) vs the dossier's
310,224 at rtf 300 — and my rtf-3600 arm reads 310,250, a third rtf within 26 events of
310k (0.008 %). Crest table reproduces within the stated few % (crest 1: 300,081 vs
299,808; spell 21.8 s; Ĉ 51.6; 9e75's 298,465/20.9 s/49.9 µs reproduced +0.5 %/+4 %/+3 %).
C's idle claim verified from the trace: p50 0.863 ms/frame, p50 1 event/frame (dossier:
0.903). Patch read line by line: print-only (Linux /proc footprint, wider rows, spell
table, ES_TRACE, wall cap) — no law or schedule change. The `work/patch.diff` header hashes
match the tree at base 9d71a890.

**Mechanism verified in code.** `kick_clock` plans `What::Boundary` at `t + full/2` and the
next `Kick` at `t + full` (step.rs:717-718); `boundary_clock`'s doc (step.rs:723-725) is
quoted verbatim by the dossier. Two events per doll interval per clock body is law-native,
so a phase-locked belt must carry both combs.

**Adversarial cases (mine, all beyond the author's grid).**
1. *rtf 3600, 3×10⁵, 150 s → 4.3 intervals (9 crests).* Recurrence holds beyond the
   author's 3.7; kick-comb spell E flat-to-rising (311.6k→322.5k), boundary 307.8k→300.8k,
   window masses 1.034/1.031/1.023/1.007 per body. The spells clamp at the law (ratios
   1.01–1.08; one boundary spell 1.19). This arm *contradicts* the "−2.5 %/interval decay"
   as a comb property: at this rtf the kick comb does not decay at all, and later window
   masses move up to 2 % with rtf — the quoted decay ratios are a delivery artifact mix,
   not rtf-free comb constants. Only window 1 is bit-invariant.
2. *Seed 2 (`plane_extra` seed arg), 10⁵, rtf 3600.* The two-comb structure reproduces:
   kick combs centered ~15k/43k, boundary combs ~29k/57k — same game-time phases as seed 1
   — and after the locals' comb (seed-dependent, ~12.5k/window vs seed 1's ~10.2k) the belt
   fires ~0.99 kicks + ~1.00 boundaries per body per interval. The reading is seed-robust,
   closing the one-seed caveat.
3. *Seed 1, 10⁵, 150 s → 8.2 intervals (14 crests) — the next decade of the swept number.*
   The half-interval alternation holds ~5–6 intervals; comb widths grow steadily
   (6.6k→13.2k→26.4k game-s) until adjacent combs merge into per-interval spells (crests
   12/13: E/N 2.37/2.47, one 16–18-s clamp covering both combs). Boundary comb decays
   96.7k→82.4k (0.946–0.98) while kick stays 110k–126k. The between-comb background grows
   3.1→4.9 ev/game-s (also in the author's own arm A trace: 3.13→3.24→4.20→5.11) — mass
   migrates off the combs. So: "recurs every half-interval forever" is wrong as stated;
   what is horizon-robust is the *per-interval bill* (~2 events/body, every interval flown)
   and recurrence itself — exactly what the compute-ahead ledger and the +26 % correction
   need. The author's own P3 named this plateau risk but stopped before reaching it.

**Predictions.** `predictions.md` predates the flights (file times: 29 min into the session
vs flights/logs later; the log order is consistent). Honest scoring: P1 held in substance
with the epoch miss disclosed and explained (the discovery); P4 failed for 2 of 7 boundary
spells and the author applied their own pre-registered rule (timing void, counts stand);
P6 refuted — reported as the finding. No kill criterion fired; K3's 1.00/comb identity
confirmed by my seed-2 arm.

**Novelty.** No "boundary comb"/"two-comb"/"second spell printed" anywhere in
docs/HISTORY.md, lab/wiki/kick-cadence.md (the page the run started from), or
lab/wiki/promotion.md. The prior record (9e75-checker2) saw a "second deep clamp at
≈42.2 k game-s" — that is the kick comb's *second* occurrence; the boundary comb at
~28.4k is new. The run answers promotion.md's open direction 3 verbatim ("the stagger's
recurrence gate (≥ 3 intervals, the unprinted second spell) before idle-time
compute-ahead is considered at all") and corrects the metronome identity's reading —
a premise correction that propagates into e7ef/98cb's composed 10⁹ ledger (+~26 % belt
CPU at shipped cadence, conditional on `BELT_SPLIT` stretching boundaries with kicks,
which the page keeps as open direction 1).

**The page.** Faithful to the evidence; two overstatements corrected in place: (a)
"recurs every half-interval forever" → bounded to the flown horizon with my 8.2-interval
merge finding; (b) "rtf-free and BIT-IDENTICAL" scoped to window 1 (later windows drift
≤2 % with delivery). A checker clause with my three arms added to Current best. Topic
stays open (this is the first gold on it; no three-gold agreement).

**Goal fit.** Board #1/#3 via the named recurrence gate; PRINCIPLES #17 — "Use idle time
to compute ahead — yes this is a whole important idea of this project" — the cycle is the
predictable demand that idle exists to serve; #12 — "the algorithm that allocates the work
to prevent those heavy tails, it's the most important one" — the heavy tail is now
measured as a periodic comb with law-native due times, i.e. schedulable a half-interval
ahead for free. Measurement only; nothing adopted into law; floats decided nothing
canonical (all load-bearing numbers are deterministic counts).

## What the author missed

- The background's growth (3.1→4.9 ev/game-s, in their own trace) is unreported; it is the
  honest mechanism of both the "decay" and the eventual smear, and it bounds how long the
  combs stay phase-sharp (~6 intervals at 10⁵).
- The decay ratios are presented as comb properties; they are delivery-dependent (my rtf
  3600 inverts the kick comb's sign). Only window 1 is a rtf-free count.
- The run stopped at 3.7 intervals, one interval short of watching the combs merge — the
  very plateau P3 pre-registered as the spike model's kill.
- Still unflown (admitted): the burn arm, the de-phased arms (stagger/chain), and the
  `BELT_SPLIT` boundary-stretch question — the latter is the one experiment that prices
  the +26 % against the composed arm, and it is named as open direction 1.
- Timing numbers are shared-box (this check included; load 1.9–2.1, 8 vCPU); the M1
  re-measures. Orders of magnitude only, per the lab rule.
