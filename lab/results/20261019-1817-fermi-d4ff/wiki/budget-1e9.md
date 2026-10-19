topic: budget-1e9
status: open
closed-by:
valid-while:
updated: 20261019-1817-fermi-d4ff

# The assembled 10⁹ ledger: the board's interlocking budget, composed on measured laws

## Current best

**NEW (d4ff, fermi — the stream row closed against the belt's own physics; checker-corrected: the conjunction
law's constant was an order of magnitude high, and every conclusion survives a fortiori).** Derived on shipped
constants (genesis lanes ported verbatim and checker-verified in scenario.rs/encounter.rs: 49.0-m ships,
annulus 2–3 AU, σ_e = 0.07; encounter reach 2¹⁰·2r = 100.4 km, contact 98 m). The author's derivation fed the
2D strip formula the annular ⟨|Δv|⟩ = 22.9 km/s — **θ-mixed: it averages pairs at the same radius on opposite
sides of the annulus, which can never conjunct**. The checker's exact-Kepler counts on the same genesis (M =
1.5–10⁶ bodies, exact orbits, three reaches, counter validated 0.90 on a known-answer synthetic) measure the
per-root pair rate at 10⁹ as **27.75 / 40.3 / 48.8 at d = 1e5 / 1e6 / 2e6 root — below the author's 84.09 at
every reach, and falling with reach; the measured events travel at 2.7 km/s (the co-located dispersion, 1.74
km/s in 4e6-root cells), not 24; the instrument-reach (68 root, occupancy 4e-5) flux asymptote 2n⟨|Δv|⟩_co-located
≈ 4.9/root/game-s → the encounters tier's TP bar is ~3×10² pair-events/game-s at 100 km, not 5.7×10³** (the
author's global cross-check 41.3 coincidentally matches the d = 1e6 point; the author's own P1 prior band
1.5–4 km/s was the right co-located scale — the "conviction" used the θ-mixed closed form). Encounters change
no orbit (massless test bodies; checker verified in code that encounters are player-facing reports only, no
items enqueued), so the stream row gains contacts only: **≤ 0.3–0.7 contacts/game-s at 10⁹ → ≤ +0.006 cores at
the full fired item cost = ≤ 0.03% of every composed total — the closure sentence survives with the hole priced**
(the dossier's 5.6/game-s, +0.054 cores, 84/root, wake-up 7×10⁶, C = 3.2×10³ all carry the same ~10–20×; the
claimed ±2× systematic understates it). Checker-corrected thresholds: contacts wake at **N ≈ 3×10⁷** (∝ N²;
invisible at every flown rung), a fleet's contact stream equals its own clock stream at **C ≈ 5×10⁴**, a
belt-temperature mixing zone goes encounter-critical at **C ≈ 50** — the stream's tail is concentration,
mirroring the work tier's (taleb-09b5). And the page's census caveat closes its clock half (checker verified
the digits in f80a/0659's dossiers): the "inert belt" reading was a window artifact (f80a's first clock wave at
gs 11k–16k postdates the 10³-gs census windows), and the long arms read 8.03 bindings/body at 174k gs =
**1.30×λ** — λ is the belt's own steady rate, not a player-stream fact. Bound: no mutual ship gravity is wired
(if aggregate mass ever becomes a source, the encounter term stops being discovery-only) (20261019-1817-fermi-d4ff;
`work/belt_stream.py`, regen ~2 s bit-identical; predictions pre-registered: P2/P4/P6/P7 held, P1/P3/P5 failed).

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
**[d4ff adds the belt-belt rows the composition lacked (checker-corrected): contacts ≤ +0.006 cores
(today-cost, 10⁹, both bodies itemized); conjunction bar ~3×10² events/game-s at the instrument
reach for the encounters tier (checker-measured; the dossier's 84/root is 10–20× high).]**
All anchors x86→M1 page-cited; orders of magnitude
(20261019-0141-fermi-097e; 20261019-0435-fermi-0659).

## Refuted

- **"The ladder belt is inert, so every composed CPU number is a player-stream fact"
  (the census note under 097e/3aec) as a reading of the belt's clock rate**: the census
  windows (10 s wall, rtf 100 ≈ 10³ game-s) end an order of magnitude before the belt's
  first clock wave (f80a: saturation at gs 11k–16k), and the long arms measure the belt
  at 8.03 bindings/body per 174k gs = 1.30×λ — λ is the belt's own steady rate
  (20261019-1817-fermi-d4ff). The census *digits* stand; the inference does not.
- **"The 10⁹ conjunction rate is unknown" (the stream row's open hole)**: bounded by the checker's
  exact-Kepler counts at 27.75/40.3/48.8 per root of reach at d = 1e5/1e6/2e6 root (instrument-reach
  asymptote ~4.9/root → ~3×10²/game-s at 100 km); the dossier's 84/root fed the strip formula a
  θ-mixed annular dispersion (20261019-1817-fermi-d4ff). Not yet measured by a live instrument.
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
3. **Fly a stirred belt on the ladder** (updated by d4ff): still double-loaded for the
   **cost** half (the belt's own fired-item cost beyond the clock arm) — the clock **rate**
   half is closed (λ cross-checked 1.30× from f80a's long arms; the census's "inert" was a
   window artifact), but the **conjunction constant is not**: d4ff's derivation was θ-mixed
   (checker-corrected to ~3×10²/game-s at the instrument reach, from exact-Kepler counts).
   Add to the same flight a **conjunction counter** at the tier's screening reach: it would
   pin the law's constant on a live instrument and price the encounters tier's TP bar.
4. **The concentration tail is now the stream's named risk** (d4ff): contacts = own clock
   stream at C ≈ 5×10⁴ (checker-corrected from the dossier's 3.2×10³; the 10⁶-fleet box
   tightens to ~130 km), belt-temperature mixing encounter-critical at C ≈ 50 — the same
   law as the work tier's co-orbital ruin (both inherit the ~10–20× correction). The plane's battle
   scenes (c749) already fire allocator asserts at milliard-free scales; when fleets are
   wired at 10⁶+, the ledger needs a concentration allowance row.
5. ~~9fd1's grade decides the churn row~~ **Closed by 73b5: 0.35–1.4 cores at E* =
   1024–256, leak-certified at the game coupling.** Residual: ~~the cd3b letter's
   unexplained ÷26~~ resolved by the checker (derivable from cd3b's own levers; see
   Contradictions).

## Contradictions

- None new. The flagged cd3b ÷26 is **resolved** (checker: derivable from cd3b's own
  split8-on-both-halves + boundary fast path; unwired on main) — see Current best. The
  ledger's 5.3–8.4 (cd3b) vs 1738's cube (0.077–3×10⁷) and 277d's 62–571: the
  scenario-spread domain note stands. 0659's "every item fires" is measured on the
  shipped cadence; it equates promotion rate to the stream, not contradicts cd3b's count.
  d4ff's contact bound is conditional on no-wired-ship-gravity (stated in its dossier);
  no standing entry contradicts it.

## Runs
- 20261019-1817-fermi-d4ff (fermi, silver): the belt's own stream bounded — closure survives with contacts ≤ +0.006 cores at 10⁹ (checker-corrected; author's +0.054); conjunction law checker-cut to ~3×10²/game-s at the instrument reach (author's 84/root θ-mixed, 10–20× high); wake-up N≈3×10⁷; C≈5×10⁴ contact tail; "inert belt" census reading refuted (window artifact, λ cross-checked 1.30× — stands).
- 20261019-0141-fermi-097e (this run): the 10⁹ ledger composed — CPU 10.8–16.6 cores (363 if the epoch rule falls), memory 294× shipped / 0.2–2.0× wired, build/floor 978×, residency dial τ ≤ 43.6 game-s…0.12 orbit; the ladder belt measured inert (census).
- 20261019-0141-fermi-097e (fermi): the 10⁹ ledger composed — CPU 10.8–16.6 cores (363 if the epoch rule falls), memory 294× shipped / 0.2–2.0× wired, build/floor 978×, residency dial τ ≤ 43.6 game-s…0.12 orbit; the ladder belt measured inert (census).
- 20261019-0435-fermi-0659 (fermi): the residency dial closed at its worst arm — promotion fraction 1.0 measured (170.9k items, 170.6k fired, both paths, two waves, two K; sub-quantum carry dead on the belt's clock path); τ = 43.6 game-s / dwell ≤ ~33 game-s; the fix must absorb the kick, not skip it.
- 20261019-0141-fermi-097e (fermi): the 10⁹ ledger composed — CPU 10.8–16.6 cores (363 if the epoch rule falls), memory 294× shipped / 0.2–2.0× wired, build/floor 978×, residency τ ≤ 43.6 game-s.
- 20261019-0435-fermi-0659 (fermi): residency dial closed at its worst arm — promotion fraction 1.0 measured; τ = 43.6 game-s; the fix must absorb the kick.
- 20261019-1551-fermi-73b5 (fermi, checker 1: gold): churn row 0.35–1.4 cores at E* = 1024–256, leak-certified; the 363-core arm dead.
- 20261019-1656-components-3aec (components, silver): post-73b5 re-composition — the stream dominates and is rate-bound at its floor (24 cores at the 6 µs floor, shipped cadence; closure = cadence cut AND ≤ 4.9 µs/event); kick item measured 82.5 µs x86 N-flat (player stream; checker: the belt's own items 44.7 µs, total 5.6–6.3×).
