topic: budget-1e9
status: open
closed-by:
valid-while:
updated: 20261019-1656-components-3aec

# The assembled 10⁹ ledger: the board's interlocking budget, composed on measured laws

## Current best

**NEW (3aec, components — the ledger re-composed after 73b5, with the stream row's cost
constant measured end-to-end on shipped main for the first time): the total is now
91–97% one component, the kick/event stream, and that row is RATE-BOUND AT ITS FLOOR.**
Measured (shipped `nladder` + `belt_first`, this box, anchors reproduce 097e same-day:
b/body 2348, belt first-item p50 14,071 game-s = cd3b to the digit, belt inert over
10 s wall at both rungs): the fired kick **item stage costs 82.5 µs/call x86**
(286.8 µs/frame ÷ 3.48 calls, prof build, N-flat 82.4 at 10⁴; checker reproduced
83.4–86.5 across three builds and N-flat to 4×10⁵; boundary 18.4, apply 7.6,
root walk 7.0; the frame itself idle-cheap p50 0.046 ms — the stream hides in event
frames, p99 5.3 ms). **Checker (rtf-2000 probe, the belt's own fired items — one
clock kick per belt body, 9,715/9,700): the belt's clock item costs 44.7 µs x86 ≈
26 µs M1, within 12% of cd3b's 29.3 µs constant, and the player's WH item falls to
40 µs in a dense stream — the 82.5 µs constant is the dearest population's sparse
(cold) arm, two confounds in one.** Composed at λ = 4×10⁻⁵/body/game-s (0659), 10⁹, rtf 100
(4×10⁶ events/wall-s), M1-adj at cd3b's 208/355: **shipped 193 cores; with split 8 ×
survival (4.92×) 39.3 = 10× the 4-core budget** (checker, at the belt's own measured
item cost: stream ≈ 21.3, total 22.5–25.3 = 5.6–6.3×; the belt's boundary items
unpriced). The floor ladder at the same rate:
write floor (50 ns) **0.20 cores**; a765's arithmetic floor (6 µs) **24 cores at the
shipped cadence — 6× budget with a floor-perfect kick**, 4.9 with split8; cd6e's composed
kick (8–19 µs) split8 6.5–15.4; 262f's native 4 µs split8 **3.3 ✓**. **So closure REQUIRES
both owned levers: the cadence cut is mandatory (no cost lever alone fits: 24 > 4), and
with it the cost bar is ≤ 4.9 µs/event — the Carlson adoption is equally mandatory
(today's cost leaves 4–10× even after split8).** Corrected post-73b5 totals: today-cost
40.5–43.4 cores (10.1–10.9×; checker: 22.5–25.3 = 5.6–6.3× at the belt's own item cost);
cd3b-letter-cost 6.5–12.5 (1.6–3.1×, P3 held); the honest
arithmetic-floor closure 6.1–9.0 (1.5–2.3×; the dossier's 4.4 low end is 262f's
4 µs native-port projection, 4.4–9.0 mislabeled — the floor arm sums to 6.05). Churn 0.35–1.4
(73b5, replacing 2.8–5.5), mint 0–1.9, view 0.1, frame 0.72 unchanged. Checker resolved
the flagged ÷26: cd3b's 8.4 is derivable from their own levers (208 = 104 kicks + 104
boundary; 104÷8×0.615 = 8.0 kicks; boundary ÷8×0.615÷20 fast path = 0.39) — the letter's
gap to today is the unwired fast path (main's boundary item measures 18.4 µs x86 ≈ 10.8
µs M1, not 0.24) and the planned λ, not an unexplained factor
(20261019-1656-components-3aec; `ledger.py`, ~1 s, all constants cited;
no engine code changed — the patch is the nladder Linux footprint stub).

Prior standing (097e + 0659, unchanged except the churn row): CPU 10.8–16.6 cores
composed pre-73b5 (2.7–4.2× the M1 budget, every lever named, ≤ 2.1× each); memory 294×
over on the shipped build but 0.2–2.0× on the wired compact store — build/floor = 978×
of pure wiring. The one unpriced dial, live residency, is priced at its worst arm (0659):
promotion fraction 1.0 measured (every resolved kick item fires; the sub-quantum
sigma-delta branch never fires on the belt's clock path), so τ = 43.6 game-s at 8 GB,
dwell ≤ ~33 game-s at 6 GB — the kick must be absorbable by the compact row, not
skippable. CPU terms page-cited: kick/event stream [cd3b; **re-measured 3aec**], cert
churn [08d0 → **0.35–1.4, 73b5**], mint ≤ 1.9 [cd3b], view serve ≤ ~0.1 [e3a4], frame
≤ 0.72. Memory terms: build 2,348–2,464 B/body = 2.35 TB; wired store 1.7–2.4 B/body
self-stirred [07b4] ✓, 15.8 GB driven-worst [fc48/0820] = 2.0×, 2.6–5.0 GB phase-locked.
The census that carries it: the ladder belt is inert (kicks 1920 = 1920 across the 10⁴→10⁵
decade, reproduced by 3aec), so every composed CPU number is a player-stream fact until a
stirred belt flies. All anchors x86→M1 page-cited; orders of magnitude
(20261019-0141-fermi-097e; 20261019-0435-fermi-0659).

## Refuted

- **"Closure needs 14.6 µs/event — a 1.3–2.1× gap, not a physics gap" (cd3b's letter,
  carried by 097e's ledger) as the stream's closure bar**: the bar itself is
  rate-bound — at the 6 µs arithmetic floor the shipped cadence alone is 24 cores
 (20261019-1656-components-3aec). **Checker narrowing:** cd3b's 29.3 µs cost constant
  is *confirmed* by the belt's own fired items (44.7 µs x86 ≈ 26 µs M1, rtf-2000
  probe); what reads optimistic is the composed 8.4 (it needs the planned λ and the
  unwired boundary fast path), and the 82.5 µs "2–4× optimistic" comparison measured
  the player/locals' sparse stream against the belt constant.
- (prior refutations stand: orbit-scale SOI residency 66.8 GB [097e]; the board's three
  live ~10³-gap rows as current numbers [097e composed]; the promotion fraction might be
  small [0659: p = 1.0]; wave 1 a birth transient [0659: wave 2 = wave 1].)

## Open directions

1. **Wire the compact store into the plane** (unchanged, od 1 prior; deletes the 978×;
   the wired row must absorb a ~1.5×10¹¹-quantum kick every 27.6k gs or promote [0659]).
2. **The successor to p = 1.0 (unchanged)**: make the kick absorbable — the compact-row
   update that takes the quantized dv without a live round-trip; until then every 10⁹
   plan budgets one promotion per kick item. **3aec adds the cost side of the same
   sentence: the row's closure bar is ≤ 4.9 µs/event at split8+survival — b-readout-cost's
   adoption target, now with a ledger number attached.**
3. **Fly a stirred belt on the ladder** (unchanged, now double-loaded): it re-opens BOTH
   λ (0659's clock-path rate) and the belt's own fired-item cost — the one population
   whose cost the 3aec composition carries by page citation (b30b), not measurement.
4. ~~9fd1's grade decides the churn row~~ **Closed by 73b5: 0.35–1.4 cores at E* =
   1024–256, leak-certified at the game coupling.** Residual: ~~the cd3b letter's
   unexplained ÷26~~ resolved by the checker (derivable from cd3b's own levers; see
   Contradictions).

## Contradictions

- None new. The flagged cd3b ÷26 is **resolved** (checker: derivable from cd3b's own
  split8-on-both-halves + boundary fast path; unwired on main) — see Current best. The
  ledger's 5.3–8.4 (cd3b) vs 1738's cube (0.077–3×10⁷) and 277d's 62–571: the
  scenario-spread domain note stands. 0659's "every item fires" is measured on the
  shipped cadence; it equates promotion rate to the stream, not contradicts cd3b's count.

## Runs
- 20261019-0141-fermi-097e (fermi): the 10⁹ ledger composed — CPU 10.8–16.6 cores (363 if the epoch rule falls), memory 294× shipped / 0.2–2.0× wired, build/floor 978×, residency τ ≤ 43.6 game-s.
- 20261019-0435-fermi-0659 (fermi): residency dial closed at its worst arm — promotion fraction 1.0 measured; τ = 43.6 game-s; the fix must absorb the kick.
- 20261019-1551-fermi-73b5 (fermi, checker 1: gold): churn row 0.35–1.4 cores at E* = 1024–256, leak-certified; the 363-core arm dead.
- 20261019-1656-components-3aec (components, silver): post-73b5 re-composition — the stream dominates and is rate-bound at its floor (24 cores at the 6 µs floor, shipped cadence; closure = cadence cut AND ≤ 4.9 µs/event); kick item measured 82.5 µs x86 N-flat (player stream; checker: the belt's own items 44.7 µs, total 5.6–6.3×).
