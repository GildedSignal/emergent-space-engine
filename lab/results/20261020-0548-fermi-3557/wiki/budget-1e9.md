topic: budget-1e9
status: open
closed-by:
valid-while:
updated: 20261020-0548-fermi-3557

# The assembled 10⁹ ledger: the board's interlocking budget, composed on measured laws

## Current best

**NEW (3557, fermi — od 6 closed by the instrument its checker demanded: the marginal-vs-base
split is now directly counted, and the marginal kick is a flat 2.5 KB law; the burn wave's extra
bytes are 99.7% frame-base, so the pooling target moves off the mint).** `ITEM_SCOPE`
(AtomicU8, print-only, set around the item resolution in `advance`, nested wave kicks included)
read by a counting `GlobalAlloc` (new `scoped_alloc` example; neutrality control: shipped
nladder counters identical with/without the probe; the patch carries the nladder Linux footprint
stub). Five arms, coast/burn × {1e4, 3e4} × {24k, 48k} gs, quiet box, seed 1, threads 1:
**item-scoped 2,477–2,621 B allocated per kick (10.6–10.9 calls/kick, spread ±3% across every
axis — a counted constant where the OLS slope spanned −1.1 to +5.3 KB), share 0.51–0.78 of all
allocated bytes; base N-flat at 1e4→3e4 (2,132 B/gs coast, 4,934–4,935 burn; coast
byte-identical, burn within 1 B/gs — the wave-scratch count wanders ±1 call), ~7
allocs/frame.** The burn's extra traffic is **99.7% base-scoped: 1.02 extra >2 KiB calls per
wave-era frame at 5.7 KB average — one frame-path buffer, not the fired item's own** — so
pooling the mint's objects cannot touch wave traffic (the target is the frame path, and only if
wave windows bind again after the stagger). Composed at 10⁹, rtf 100: **marginal 10–22 GB/s =
17–37% of 60 GB/s at λ ∈ {4, 8.4}×10⁻⁵ (2.0–4.5 GB/s = 3–7% after split8); allocator 0.51–1.06
cores (0.10–0.22 split8, at f623's 11.6 ns floor); base 0.49 MB/s — nil at any N.** Both of
f623's machine-floor rows re-close, tighter. **Conflict disclosed:** at the window-matched arm
(47.9k gs, 94,735 kicks vs f623's 48.8k/96,108 — same scene, rate to 1%) this probe reads naive
3,588 B/kick, 13.2 allocs, 0.30 reallocs against their 12.3–12.7 KB / 17.6–19.3 / 4.4–4.9; the
engine is git-identical since before their run, so it is a probe-accounting or machine-state
(FLOW backlog) difference, unresolved — the marginal/base decision is internal to one instrument
and regenerates deterministically (20261020-0548-fermi-3557; regen ~1.5 min; predictions v2
pre-registered: P2/P4 held — the kill bar never fired; P3 half-failed into the re-scoping; P1
failed on the letter, the conflict above).**

**NEW (f623, fermi — the ledger's two unpriced floors are now measured and both CLOSE: no machine
floor forces the kick-mint deletion; and the mint's per-kick churn law is measured, splitting
naive vs marginal for the first time).** Print-only counting-`GlobalAlloc` probe (new
`alloc_probe` binary on the shipped `nladder` scene; shipped code untouched), coast arms
K = 10⁴ (48,803 gs, 96,108 kicks) and 3×10⁴ (36,404 gs, 87,380), this box, load 0.3:
**naive 17.6–19.3 allocs + 16 frees + 4.4–4.9 reallocs and 12.3–12.7 KB allocated per fired kick
(12.1 KB freed — the engine already pools by immediate free; net live 0.55–1.6 KB/kick = the
known ratchet), but window OLS attributes only ~11–13 allocs and 1.4–3.3 KB to the MARGINAL
kick** — the rest is a flight base (checker: NOT N-flat — 18→27→53 KB/game-s at 10⁴/3×10⁴/10⁵),
64% of all allocated
bytes sitting in >2 KiB scratch at 0.56 calls/kick (~15 KB avg). The heap-call family is
**{88, 240, 304, 352, 384², 704, 832} B at ~9–10 calls/kick = 76–79% of ≤2 KiB bytes — NOT the
mint anatomy {192, 208, 288}** (9edc's sizes are `size_of`, not the heap cuts). Malloc floor
measured: 11.6 ns per alloc+touch+free pair (86 M/s/core). **Composed at 10⁹, rtf 100, λ ∈
{4, 8.4}×10⁻⁵: allocator 0.6–1.7 cores; byte traffic 13.6–28.5 GB/s marginal = 23–48% of the
M1's ~60 GB/s (naive wave windows 52–109 GB/s = 86–181%, transiently ~1× the machine — cc9d's
wave, likely the same read set); after split8: 0.05–0.2 cores, 1.7–3.6 GB/s (3–6%).** So the
closure sentence survives with both new rows closed: **the mint deletion's case stays memory
(the ratchet) + CPU (its share of the 82.5 µs item) — no pooling subsystem is machine-mandated**
("the best part is no part"); the after-lever table's only unclosable row remains the player's
root-doll item (cc9d). Predictions: P4/P5 held (P4's bandwidth half holds on the marginal
(20261019-2339-fermi-f623; regen ~2 min; coast only, one seed, x86→M1 orders only; burn arm named
below). **[Checker, silver: the decision survives every attack — naive constants (10.5–13.5 KB,
17–21 calls/kick) and the heap family reproduce at 10⁵, seed 7 and burn, and even the worst
attribution (burn-naive 21.5 KB/kick) closes under the already-mandatory split8 (≈37% of 60 GB/s
at λ = 8.4×10⁻⁵) — but the marginal split is NOT yet a law: the OLS slope across arms spans
−1.1 to +5.3 KB/kick (author 3.32/1.40; regen 3.32/0.98; checker seed-7 +5.34, 10⁵ coast −1.08,
burn −0.06; sign flips — the 12-ms frame budget cuts non-kick work when kicks spike, coupling
regressor and bytes), so 23–48% is one draw, not a measured row.]**


**NEW (f876, second author on d4ff — the conjunction constant is now MEASURED at the ladder's
checkable decade, checker-extended flat to 2×10⁵ root, and the checker's anchor table falls with it).** Exact Kepler propagation
of the shipped genesis (M = 10⁵ bodies, per-pair debounced threshold crossings, burn-in excluded,
1,182 events, four configs; checker: 596 more events at 10⁵ read 6.27, 2,264 at 2×10⁵ read 5.96) measures the belt's pair-event rate at **Γ = 6.21 per root of reach per
game-s (band 5.4–7.0), FLAT in reach across d = 10⁴–10⁵ root (falling ~5% by 2×10⁵)** — the kinetic flux regime, reached six
mean-spacings down and carried to the instrument reaches by its own flatness (no physics scale between
10⁴ root and the ship radius) — the carry below 10⁴ is theory plus bookends, not a measurement. At the priced reaches: **TP bar ≈ 422 pair-events/game-s at 100 km**
(selectivity 8×10⁻¹⁶ of 5×10¹⁷ pairs), **contacts 0.41/game-s → +0.0040 cores today-cost = ≤ 0.03% of
every composed total**, wake-up N = 2.6×10⁷, C_contact = 4.3×10⁴ (10⁶-fleet box ≥ 142,000 km),
belt-temperature C = 42. The author's 84.09/root is REPRODUCED as an artifact (the kinetic theorem on
shell-random pairs — θ-mixed — gives 83.3: their construction, their number), and the checker's
corrected constants all stand to ~30% (their 4.9 vs measured 6.21). But the checker's three-reach
anchor table (27.75/40.3/48.8 per root at d = 10⁵/10⁶/2×10⁶) is **itself 4–8× high as a pair-event
rate**: a second, independent instrument (steady-state pair MC: conjunctions at |Δn|/2π, miss = impact
parameter at the angular crossing) reads 6.1–6.8 at 10⁵ and 4.6/3.9 falling at 10⁶/2×10⁶ — their
rising-with-reach signature is presence-flavoured counting (their occupancy 1.3–5.3 at the upper
reaches), not pair events. The MC's own straight-line miss overcounts the slow tail (|Δv| ≲ Ω|Δr|:
orbital shear closes the window before the radial offset does) — +10% at 10⁵ root, dominant below 10⁴
(full/safe at 68 root: 13.8/10.8, bookends only, OUTSIDE the adopted band 5.4–7.0 — the priced-reach
constant carries that one-sided risk, unmeasured below 10⁴; every ledger conclusion survives a 2× rise);
the propagation anchors the flat law instead (checker's independent KDTree counter: 5.65 at 3×10⁴).
(20261019-1906-second-20261019-1817-fermi-d4ff-f876; `regen.sh` ~11 min: parallel propagation + pair MC + kinetic theorem + ledger; predictions
pre-registered: P1 flatness, P3 artifact-reproduction, P4 speeds, P5 downstream, P6 all held; P2's
shear-safe-cut plan failed at 68 root — kill criterion fired, adopted constant is the
propagation-anchored flat law. Bound unchanged: no mutual ship gravity wired.)

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
**[f623 adds the two machine-floor rows the composition lacked, both closed: allocator
0.6–1.7 cores today-cost, byte traffic 23–48% of 60 GB/s marginal (86–181% naive in
waves), 3–6% after split8 — no pooling subsystem is machine-mandated.]**
All anchors x86→M1 page-cited; orders of magnitude
(20261019-0141-fermi-097e; 20261019-0435-fermi-0659).

## Refuted

- **"The mint's heap-call anatomy is Binding 192 + Segment 208 + Entry 288" (9edc's
  `size_of` reading) as a description of the allocation stream**: the measured per-kick
  family is {88, 240, 304, 352, 384², 704, 832} B at ~9–10 calls/kick (76–79% of ≤2 KiB
  bytes), those three sizes absent from the top 16; the retained objects are still
  9edc's, the heap cuts are not (20261019-2339-fermi-f623).
- **"The allocator and memory bandwidth are unpriced risks at 10⁹" (this page's own
  gap, and PRINCIPLES #12's worry)**: measured 0.6–1.7 cores and 23–48% of 60 GB/s
  marginal at the shipped cadence (3–6% after split8) — both close; the naive per-kick
  average (12.3–12.7 KB, 86–181% of bandwidth in waves) over-attributes an N-flat
  flight base, 64% of it >2 KiB scratch, to the mint (20261019-2339-fermi-f623).
- **"The ladder belt is inert, so every composed CPU number is a player-stream fact"
  (the census note under 097e/3aec) as a reading of the belt's clock rate**: the census
  windows (10 s wall, rtf 100 ≈ 10³ game-s) end an order of magnitude before the belt's
  first clock wave (f80a: saturation at gs 11k–16k), and the long arms measure the belt
  at 8.03 bindings/body per 174k gs = 1.30×λ — λ is the belt's own steady rate
  (20261019-1817-fermi-d4ff). The census *digits* stand; the inference does not.
- **"The 10⁹ conjunction rate is unknown" (the stream row's open hole)**: now MEASURED flat at
  Γ = 6.21/root/game-s (band 5.4–7.0) by exact propagation at d = 10⁴–10⁵ root and carried to the
  instrument reaches (TP bar ≈ 422/game-s at 100 km; f876). The dossier's 84/root was a θ-mixed
  shell-pair artifact (reproduced at 83.3; d4ff).
- **The checker's three-reach anchor table (27.75/40.3/48.8 per root) as a pair-event rate**
  (d4ff's check.md): two independent instruments — exact propagation (6.19 at 10⁵) and the
  steady-state pair MC (6.83 at 10⁵, falling per root above) — both sit 4–8× below it; the table's
  rising-with-reach shape matches presence counting, not debounced pair events. Checker f876-review
  confirms by rerun and by a third, differently-structured counter (596 events at 10⁵ → 6.27;
  2,264 at 2×10⁵ → 5.96, falling; KDTree counter 5.65 at 3×10⁴). The checker's
  downstream constants survive (~30%) because their asymptote and bands absorbed it (f876).
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
   Add to the same flight a **conjunction counter** at the tier's screening reach: the constant is now pinned off-engine
   (Γ = 6.21 flat, f876 — propagation at 10⁴–10⁵ root + kinetic flatness to 68 root); the flight
   instrument remains to confirm it inside the shipped loop (the propagation is the belt's own
   law, not the engine's scan).
4. **The concentration tail is now the stream's named risk** (d4ff): contacts = own clock
   stream at C ≈ 4.3×10⁴ (measured Γ = 6.21; f876; checker 5×10⁴; dossier 3.2×10³; 10⁶-fleet
   box ~142,000 km), belt-temperature mixing encounter-critical at C ≈ 42 (f876; checker 50) — the
   same law as the work tier's co-orbital ruin. The plane's battle
   scenes (c749) already fire allocator asserts at milliard-free scales; when fleets are
   wired at 10⁶+, the ledger needs a concentration allowance row.
5. ~~9fd1's grade decides the churn row~~ **Closed by 73b5: 0.35–1.4 cores at E* =
   1024–256, leak-certified at the game coupling.** Residual: ~~the cd3b letter's
   unexplained ÷26~~ resolved by the checker (derivable from cd3b's own levers; see
   Contradictions).
6. ~~**The burn arm of the allocation law (f623)**~~ **Closed by 3557's scoped probe:** the
   marginal/base split is counted directly (od 6's named instrument) — marginal 2.5 KB/kick
   flat, burn-wave extra bytes 99.7% base (a ~5.7 KB/frame wave-era buffer), naive 3.6 KB/kick
   on this harness vs f623's 12.3–12.7 (probe-accounting conflict disclosed, unresolved).
   Residual: one loaded-box flight (FLOW backlog engaged) to test whether the split moves;
   the free-path traffic (2× alloc bytes) is uncounted.

## Contradictions

- None new. The flagged cd3b ÷26 is **resolved** (checker: derivable from cd3b's own
  split8-on-both-halves + boundary fast path; unwired on main) — see Current best. The
  ledger's 5.3–8.4 (cd3b) vs 1738's cube (0.077–3×10⁷) and 277d's 62–571: the
  scenario-spread domain note stands. 0659's "every item fires" is measured on the
  shipped cadence; it equates promotion rate to the stream, not contradicts cd3b's count.
  d4ff's contact bound is conditional on no-wired-ship-gravity (stated in its dossier);
  no standing entry contradicts it. f623's naive-vs-marginal split is an attribution
  choice, disclosed both ways; no standing entry depends on the naive reading.

## Runs
- 20261019-0141-fermi-097e (this run): the 10⁹ ledger composed — CPU 10.8–16.6 cores (363 if the epoch rule falls), memory 294× shipped / 0.2–2.0× wired, build/floor 978×, residency dial τ ≤ 43.6 game-s…0.12 orbit; the ladder belt measured inert (census).
- 20261019-0141-fermi-097e (fermi): the 10⁹ ledger composed — CPU 10.8–16.6 cores (363 if the epoch rule falls), memory 294× shipped / 0.2–2.0× wired, build/floor 978×, residency dial τ ≤ 43.6 game-s…0.12 orbit; the ladder belt measured inert (census).
- 20261019-0435-fermi-0659 (fermi): the residency dial closed at its worst arm — promotion fraction 1.0 measured (170.9k items, 170.6k fired, both paths, two waves, two K; sub-quantum carry dead on the belt's clock path); τ = 43.6 game-s / dwell ≤ ~33 game-s; the fix must absorb the kick, not skip it.
- 20261019-0141-fermi-097e (fermi): the 10⁹ ledger composed — CPU 10.8–16.6 cores (363 if the epoch rule falls), memory 294× shipped / 0.2–2.0× wired, build/floor 978×, residency τ ≤ 43.6 game-s.
- 20261019-0435-fermi-0659 (fermi): residency dial closed at its worst arm — promotion fraction 1.0 measured; τ = 43.6 game-s; the fix must absorb the kick.
- 20261019-1551-fermi-73b5 (fermi, checker 1: gold): churn row 0.35–1.4 cores at E* = 1024–256, leak-certified; the 363-core arm dead.
- 20261019-1656-components-3aec (components, silver): post-73b5 re-composition — the stream dominates and is rate-bound at its floor (24 cores at the 6 µs floor, shipped cadence; closure = cadence cut AND ≤ 4.9 µs/event); kick item measured 82.5 µs x86 N-flat (player stream; checker: the belt's own items 44.7 µs, total 5.6–6.3×).
- 20261019-1817-fermi-d4ff (fermi, silver): the belt's own stream bounded — closure survives with contacts ≤ +0.006 cores at 10⁹ (checker-corrected; author's +0.054); conjunction law checker-cut to ~3×10²/game-s at the instrument reach (author's 84/root θ-mixed, 10–20× high); wake-up N≈3×10⁷; C≈5×10⁴ contact tail; "inert belt" census reading refuted (window artifact, λ cross-checked 1.30× — stands).
- 20261019-1906-second-20261019-1817-fermi-d4ff-f876 (second, on d4ff): the conjunction constant measured where it is paid — Γ = 6.21/root/game-s flat (propagation, 1,182 events, d = 10⁴–10⁵), TP bar 422/game-s, contacts 0.41/s, +0.0040 cores; author's 84.09 reproduced as θ-mixing (83.3); checker's anchor table 4–8× high as pair events, their downstream constants stand to ~30%.
- 20261019-2339-fermi-f623 (fermi, silver): the two unpriced floors measured and closed — allocator 0.6–1.7 cores, bytes 23–48% of 60 GB/s marginal (86–181% naive in waves; 3–6% split8); per-kick churn law 17.6–19.3 allocs + 12.3–12.7 KB naive vs 1.4–3.3 KB marginal, family {88,240,304,352,384²,704,832}, 64% >2 KiB scratch; no machine floor forces the mint deletion. Checker: naive law + family reproduce at 10⁵/seed-7/burn and the closure survives the worst attribution (burn-naive 21.5 KB/kick ≈ 37% under mandatory split8), but the marginal/base OLS split is unstable (−1.1 to +5.3 KB/kick) — not yet a law.
- 20261020-0548-fermi-3557 (fermi): od 6 closed by the scoped counting allocator — marginal 2,477–2,621 B/kick flat (share 0.51–0.78), base N-flat (2,132/~4,934 B/gs coast/burn), burn-wave extra 99.7% base (a 5.7 KB/frame buffer); composed 17–37% of 60 GB/s shipped cadence, 3–7% split8, allocator 0.51–1.06 cores; naive conflict with f623 disclosed (3.6 vs 12.3 KB/kick at a window-matched arm, engine git-identical).
