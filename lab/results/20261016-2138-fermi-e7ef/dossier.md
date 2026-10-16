# Dossier — 20261016-2138-fermi-e7ef

**Claim.** The 10⁹ CPU ledger closes on measured levers alone — closure is the single
product kick-cost ÷ cadence-cut ≤ 1.13 µs at 10⁹ rtf 100, so a 9–23 µs kick suffices in
every measured-lever configuration and the 42–56 ns floor is not on the 10⁹ critical
path; the terms that do NOT close at 10⁹ are the encounter tier on graded levers
(62–571 cores) and memory (every generic floor busts 6 GB; only the measured
phase-locked program class fits).

**Bottleneck.** The board's framing question ("bodies 28→10⁹", with the kick row at
10³·³ as a co-equal gap). Expected gain: a re-ranking of the four live questions —
the kick row demoted from 10⁹ blocker to 10⁶-flyability lever, and the 10⁹ critical
path named as two wiring items (compact store, encounter routing's grade). Deletes:
any 10⁹-motivated push toward the 50-ns kick (a 10³·³ programme bought where 2–5×
suffices), and the double-count in the scoreboard's "gaps interlock" identity.

**Evidence** (regenerate with `./regen.sh`, < 5 min, no tree edits — `work/patch.diff`
is empty by construction):

- *Anchor, shipped code, this box* (`cargo run --release -p emergent-universe
  --example belt_first`, 14.5 s): belt first-kick p50 **14,072 game-s** (spread
  13,051–14,534) → interval = 28,144 s against the recorded 28,141.5 (3294/4093);
  rate×interval = **1.0004** kicks/body/interval — the metronome identity holds as
  "one kick per body per doll-grid interval". Source-derived: P_D(Cinder) = 3.602e6 s
  = **0.468 ×** Cinder's SI Kepler period 7.700e6 s (a = 35.6e6/0.9 ru, AU =
  1.013e8, TICK_SECONDS = 4.9255e-6); the law's doll-clock factor f'(c) ≈ 2.14
  [inference from ext.rs's Δs law, not read in code].
- *The stream* (`python3 ledger.py`, 0.05 s; constants each cited in the script):
  10⁹ rtf 100 = 177 cores (x86 50 µs) / 104 (M1 29.3) — reproducing 4093's 120–190;
  ÷8× split (7f97) = 22.2; ÷8× and −38.5% delete (1a46 frozen) = 13.7; ÷8× and −61%
  (widened) = 8.65; + secular 15× (5030, extrapolated) = 0.58. **Required kick cost
  to fit 4 cores: 1.1 µs (shipped cadence), 9.0 µs (8×), 23.1 µs (8× + 61%) — 23–472×
  above the floor.** At the 49 ns floor, shipped cadence = **0.17 cores** (fits).
- *The crest*: t = N·C/0.72 gives 10⁶ → 69.4 s (4093 measured 69 s), 3×10⁵ → 21 s,
  10⁹ → 69,444 s x86 / 40,694 s M1 — ≥19.3 h stands, and it is cured by the measured
  genesis stagger (ed3a/f82a), not by kick cost.
- *Encounters at 10⁹* (arithmetic from the pages): cube 1.65–8.2×10³ cores (1738);
  + gate (277d silver) leaves **62–571** (recomputed 69–586) — does not close; only
  f0a2's birth-constant routing (awaiting grade) closes it, 0.03–0.6 cores.
- *Memory at 10⁹* (6-GB / 48-bit budget): phase-locked compact store 21–40 bits →
  **2.6–5.0 GB, the only class that fits**; 3-field floor 62 bits → 7.7 GB; 4-field
  126 → 15.7; driven-belt worst 126.4 → 15.8; shipped plateau 4.85–5.06 kB/B → 4.9–5.1
  TB = **808×** the budget; and 6–8 GB ÷ plateau = **1.19–1.65×10⁶ bodies — the
  ladder's measured memory wall exactly**, i.e. the wall IS the plateau, no physics
  in it.

**Predictions** (`predictions.md`, written before the run): P1 belt clause HELD
(14,072 ∈ 14,100±700); P1 locals clause FAILED (p50 661 s against my ≤300 — Home's
doll clock ~21× faster than guessed; no effect on the ledger, reported as failed);
P2 HELD (0.4678 ∈ 0.468±0.02); P3 HELD (22.19 cores; required 9.0 µs = 184×);
P4 HELD (0.17 cores); P5 HELD (69.4 vs 69 s); P6 HELD (both non-closing terms
confirmed). 

**What would make it wrong.** (i) The rate 3.55e-5/B/game-s or the 50 µs cost being
mis-framed (rtf, per-body accounting) — but the same constants reproduce 4093's
independent flights (120–190 cores; the 69-s crest to the second digit). (ii) The 8×
split's legality not extending to the 10⁹ belt bulk (7f97 measured it on the plane's
populations; B17's 16-per-perturber-period is the mechanism) — but closure holds even
at 8× with NO delete if the kick reaches 9 µs, and holds at 1.1 µs with no cadence
change at all; the redundancy is the claim, not any single lever. (iii) A fourth CPU
term I left out (the view is free after the birth/death feed, view page; H_live 21
bits/s, memory-h-live; the hot set 90–186 MB, a11b/ba64). **Cost of adopting:** zero
code; a re-ranking of the board (demote the kick row for 10⁹, name the two wiring
blockers). **PRINCIPLES fit:** #1 "the cheapest compute is compute not done" — do
not buy a 10³·³ kick programme when 2–5× closes; #18 "the right question, then the
representation" — the ledger's question is the product, not four independent gaps;
#10 "measure before claiming" — the wall is the plateau, measured.

**The lens.** Fermi: I re-derived the newest ledger's anchors instead of measuring
new ones, so I inherit the pages' constants — a shared-harness risk the lab itself
flags; my two independent checks (belt_first on this box; the wall = budget ÷ plateau
identity) are the firewall. The lens also biases toward assembly over probe: I did
not fly the crest's cure or the delete at 10⁹-scale; those remain 4093's/1a46's
measurements, cited not re-measured. What the lens may have missed: whether the
"player pace = rtf 100" frame is Julien's actual play pace (if he flies at rtf 10,
every CPU row gains 10× slack and memory alone remains); and the locals' storm at
plane scale, where my failed P1 clause shows my doll-clock intuition is 21× off.
