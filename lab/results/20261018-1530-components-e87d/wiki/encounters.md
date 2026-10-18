topic: encounters
status: open
closed-by:
valid-while:
updated: 20261018-1530-components-e87d

# Finding encounters: the pairwise tier, the slack skin, the Binet cone

## Current best
**[20261018-1530-components-e87d] Open directions 1 and 2 are measured dead at the design
reach, by one law: a single belt-quantum kick FULLY decorrelates the section rotation's due
at every horizon — flips of [k_first ≤ KH] equal armed·(1−armed)·(0.88–0.97) at KH ∈
{10³,10⁴,10⁵,10⁶}, dv-independent across 2⁻²³/2⁻¹⁷/2⁻¹⁴ (components lens; exact integer
replica of the shipped tier: `arm_sections` + `arm_pair`'s integer setup + `dioph::first_hit`
on a `make_belt` cell at ρ = B = 3.34×10⁻⁶ AU, 2,000 bodies, a-window 10⁻⁴/10⁻⁵ AU, seeds
20261018/777; dv=0 bit-identical, 0/240,000 pairs).** The beat-resident record (od 1) dies
on the slack: at L ≤ 10⁴ passages the slack is vacuous (p50 ≈ pi/5, the rotation has not
approached the window); at the first meaningful horizon L = 10⁵ it is p50 **2.7 window
widths** and one quantum kick drifts it by **2.0 widths** (drift/slack p50 0.8) — the
identity behind both classes: δd p50 = 2.4×10⁴ ticks per quantum kick = 0.44·w in this
fat-window class, ~10³·w in the thin class (1a29's w ≈ 23). The leak-gated skip (od 2) dies
with it: certified-safe-then-kicked pairs leak at ~2×10⁻³ per kick-set flat in 1/8/64 kicks
(≈ 2× the re-roll rate, no accumulation structure), so a 10⁻⁶ budget buys ~0 skipping.
**What survives a kick, measured: the float window w (δw p50 < 1 tick on Cross sections —
checker: tail max ≈ 0.14·w per quantum kick in the same belt class, so tail soundness of a
cached w is unmeasured), the section shape (0 changes), the candidate set (c9c7). What that
buys: the shipped 1,394 ns
eval (1a29's 1.13–1.42 µs reproduced) is 72% float section reconstruction, all of it
kick-stable — cache the section per pair, maintain (c0, d, pi) by the kick's exact integer
deltas, decide with `first_hit`: 416 ns/pair/kick measured, a 3.4× cut (355 → ~105 cores in
1a29's units), exactness-preserving (same integers, same decision). The row's floor this
establishes: one integer re-decision per candidate pair per kick is information-forced (the
re-roll is total), so below ~100 ns/pair/kick the row is a candidate-density question
(pairs ∝ ρ·density), not a certificate question. Next constant lever, named and unpriced:
`first_hit`'s u128 arithmetic (all section values < 2⁶³ — a u64 port). The Full-section
corner (nearly identical orbits — keys fleets; 0/100,000 in the author's mix) was measured
by the checker on a one-orbit formation (identical a, e, ϖ; uniform λ): the kill extends
there, stronger — the pre-kick due is "never" for every pair (d = 0, armed 0/240,000) and
one quantum kick flips 2.27×10⁻¹ of pairs on at KH = 10⁶ (δd = a full random residue), so
no beat record exists to store at all; but the cache lever does NOT extend: δw p50
2.1×10⁴ = 0.32·w per kick, and 26% of pairs change section shape at 2⁻¹⁷.**
*[Checker 2, 20261018 (blind): regen bit-identical on all physics modes (timing 1,365–1,372 ns,
within clock noise of the 1,394 quoted). Two corrections to the letter, kill unaffected: (1) the
"~10³·w thin class" is 1a29's unit arithmetic, not an in-crate class — c₀ ≤ v bounds w ≥ ρ/v,
so the design-reach floor is ~2–4×10⁴ ticks; measured at the thinnest corner I could build
(a = 1, σ_e 0.3, 10⁻³ cell): w p50 3.8×10⁴, δd/w ≈ 0.19, re-roll ratio 0.99–1.03, drift/slack
1.17, leak 0.18 at L = 10⁵ — the kill holds there by measurement. (2) the Full-corner flip
constant is formation-dependent: my formation (e 0.05) flips 4.5×10⁻¹ at KH = 10⁶ with δw p50
0.39·w — same verdict (nothing to store; no cache). Wide sections: 0 even at σ_e 0.3 — P6's
branch stays unpopulated at the design reach.]*


**[20261018-1126-second-20261018-1025-scout-fbf9-1a29] The silver's kill test is flown
on the shipped tier and it KILLS the due-band rule: at the design reach
(B = 5×10⁵ m) the shipped due is a deep-beat Diophantine draw that re-rolls under any
kick — window w ≈ ρ/c₀ ≈ 23 ticks against rotation step d ≈ |Δp| ≈ 3×10⁵ ticks at a
cell's typical |Δn|, beat depth k ~ 10⁶ — so after a belt-quantum kick (2⁻²³) silent
cell-mates flip armed at 5–7×10⁻⁶ per candidate per kick (0.0017/0.055/0.72
silent→armed flips per body per kick at n = 10³/10⁴/10⁵; the toy's own kill line
"flips/kick > 0.1" crossed at 0.1075), dv-INDEPENDENTLY (0.108/0.165/0.175 across
2⁻²³/2⁻¹⁷/2⁻¹⁴ — a re-roll, not the toy's multiplicative walk, which holds only for
the k = 0 conjunction), with EVERY flip-on outside the band (their stored dues sit
2.7–4.3×10⁶ intervals out; |Δn| at the cell's typical value, so no Δn cut separates
them) and ~14% carrying real exact-machinery events — the band rule loses encounters
at ~10⁻⁶ per candidate per kick.** Sound per-kick re-arm on this representation is
wholesale: 355 cores per 10⁴-cell occupancy at 1 µs/eval, 1 kick/body/interval
(checker clock 28141.5 s; 0.35 on SI) — the row does NOT close on the stream terms
via a due band. The regime boundary reconciles this with quant-c9c7: the re-roll
exists while w ≪ d (ρ ≪ ρ\* = c₀·d/TICKS ≈ 4.4×10⁻⁵ AU; design B = 3.3×10⁻⁶ AU
is ~13× below [checker: the dossier's "3.3×10⁻⁹" / "10⁴×" is a units slip]),
while quant's ρ = 1e-4 replica sits above ρ\* in the smooth walk regime — their 0
slack violations do not transfer to the design reach, where the leak is the measured
~10⁻⁶ events/candidate/kick. What survives of the toy: the conjunction-band constant
reproduces on shipped elements (0.0525/0.0575/3.95 per body per kick at 10⁴/seed
777/10⁵ vs toy–checker 0.034–0.065/3.4–4.67 — the n² law), wholesale is n−1 with
tier-1 bit-stable under quantum kicks (0 candidacy flips everywhere), standing/dwell
co-tick pairs are clean (2–9, 0 armed, 0 flips — the kill test's named suspect
acquitted; the channel is the beat re-roll), arm evals 1.13–1.42 µs (b509's
1.02–1.16), and never-store-exact strengthens (anchor churn 1.1× armed per kick at
bare B; anchor flip fraction 3.6×10⁻⁴ at 2⁻²³ → 3.4×10⁻² at 2⁻¹⁷, walk-scaled).
Instrument: shipped Phase-A (`Sorted` scan → `is_candidate` → `tier::arm_pair`
safety 1.1) on the toy's scene constants; armed covers exact truth 68/68 and 78/78
at amplified reach; regen byte-identical (second run, flight/ + regen.sh, 70 s).
**[Checker, 20261018: regen IDENTICAL again; n = 3×10⁵ (one decade out) gives
3.5 flips/kick, viol2_on = flips_on 65/65, 4 more real events, violators at
1.3–1.7× the candidate |Δn| median (no Δn cut separates); a reach sweep
collapses the violator dues 1.3×10⁶ → 23 intervals between ρ = 10⁻⁵ and
4.4×10⁻⁵ AU (the boundary is real and brackets ρ\*; B sits ~13× below it);
7/7 dumped leak events re-derived as within-reach minima by an independent
Kepler solve. The violating pairs' dues (~10⁶ passages) imply effective
windows of ~10⁵ ticks (the Wide passage-overlap class, w/d ~ 0.3–1), not the
23-tick cross window; the re-roll stands on the measured decorrelation, and
the margin to ρ\* is thin — a factor in the leak-gated-slack design.]**
**[Checker 2, 20261018 (blind): reproduced bit-identically in an isolated build. My
adversarials: n = 10⁶ (two decades out) → 6.6×10⁻⁶ flips-on/candidate/kick, 79/79
outside the band, 6 real events, violators' |Δn| tracking the cell width (Θ(n) and
the leak extend); fresh 10⁵ seed and cold σ_e = 0.01 belt reproduce (5.5×10⁻⁶/cand,
all outside); my own reach probes bracket ρ* (1×10⁻⁵ AU: dues 3.9×10⁶ intervals,
re-roll; 6×10⁻⁵ > ρ*: quantum flips collapse to 2/100, dues ~4×10², and 2⁻¹⁷ → 138
flips — the dv-dependent walk regime); all 3 leaked events at 10⁴ re-derived REAL by
an independent Kepler solver (1.411/1.481/1.976×10⁻⁶ AU < reach 3.342×10⁻⁶). One
qualification: at dv = 2⁻²⁶ (below the belt quantum) the channel dies (0 flips in
200 kicks, ~11 expected) — "re-rolls under any kick" holds only for kicks ≳ the
quantum; and the leak fraction spans 7–24% across configs, "~14%" is the 10⁴/10⁵
headline.]**


**[20261018-1025-quant-c9c7] The row's one missing constant is measured and it inverts the closure reading:
pairs re-checked per kick on the shipped U-scan tier is 0.484·N at the belt's own mix — the
window is SATURATED (the scan is the whole band at every N, 10⁴→10⁶, exponent 0.999; the
Rayleigh e-tail's e_max/p ≈ 0.19 exceeds the band's whole U-span 1/2−1/3 = 0.167), so the
count is linear in N and NOT O(1) even at fixed density, and cells cannot bound it (reach
spans ~10⁵ cells of 10⁴).** fe6b's 0.0346·n is the *unsaturated* regime: reproduced at its
own spec (0.0824→0.0843·N at 10⁴→10⁶ = 0.0346·N·(1+X)/(2(X−1)) with X = 1.52 ≈ 1.5), while
the belt mix carries 5.7× more candidates (σ_R 0.07 vs 0.01). Composed at 10⁹ rtf 100:
candidate rescans are 10⁷–10⁹ cores — the rescan framing of the row is dead by 5–7
orders. The closure is measured the same run on the flow/slack side: at the belt quantum
(2⁻²³) the candidate set is bit-stable (gained+lost ≈ 0 of ~10⁵–5×10⁵ pairs per kick),
92.3–92.5% of pairs are slack-skippable with 0 violations (changed 1.3%; armed pairs
0.85% of candidates; n = 10⁴ and 3×10⁴, seeds 20261050 and 777), and stored slack dies
at 10⁻⁵-class kicks (4.5% skippable; 0.04% at 10⁻³) — churn reduces to cd3b's mint flow
(≤1.9 cores) plus burn-priced re-arm. Replica element tier (Binet cone, ρ = 1e-4;
measured N ≤ 10⁶, extrapolated 10³× structurally; instrument `examples/churn.rs` +
the parameterized shipped `kick`, `regen.sh`). **[Checker, 20261018: reproduced
bit-identically; σ 0.2 → 0.849·N, σ 0.4 → 0.940·N (stirring worsens the rescan
verdict); n = 3×10⁶ → 0.519·N; fe6b's law at a second X ([1,2]: 0.0511 vs 0.0519);
10×-wider band [2,12] → 0.15–0.154·N; the named 10⁶-pair slack probe: 0.9219
skippable, 0 violations.]** *[20261018-1126 note: the slack side's 0 violations were
measured at ρ = 1e-4 ≫ ρ\* — in the smooth regime; at the design reach the same skip
leaks ~10⁻⁶ real events per candidate per kick (this page, top entry).]*

**[20261018-1025-scout-fbf9, refuted in its central rule by the top entry's flight;
constants and churn findings retained]** The toy measured: intra-cell armed
probability ~10⁻¹¹, flips 0 at every occupancy, near-horizon band 0.030–0.065 across
seeds at n = 10⁴ against the analytic 0.034 (∝ n² at fixed density, checker-measured
4.67 at 10⁵), the due-walk multiplicative (median cell-mates 10⁵–4×10⁶ intervals per
kick — refuting its own first, due-space-slack model), live-anchor armed 525–1050
per body per horizon (cd3b's flow order), bare-B miss churn 0.5–0.75× armed per
quantum kick (saturating at 2⁻¹⁷), controls sound (superset 11/11, no-margin loses
events, concentration standing 543/body = taleb-09b5's ruin class). **The rule these
supported — re-check iff first due < H+2 — is dead on the shipped tier: the shipped
due is the k ~ 10⁶ first-hit, not the k = 0 conjunction the walk law describes
(20261018-1126-second-…-1a29).**

**[20261018-0932-fermi-cd3b] The belt row's EVENT FLOW at 10⁹ is derived on the shipped
geometry and it is cheap and small: ~0.22 contacts/game-s and ~1.1×10³ b≤5×10⁵-m
conjunctions/game-s (2-D Poisson sweep on scenario.rs's own constants — planar a∈[2,3) AU,
49-m ships, n₂D = N/25 AU², v_rel 1.8 km/s; anchor `belt_first 10000` reproduces 14,071
to the digit), so the whole flow costs ≤1.9 M1 cores at rtf 100 even if every conjunction
re-mints a key at the measured 16.4 µs (0.068 cores at 277d's exact-eval cost; with efd4's
intern only distinct pairs pay). The 62–571-core row span is therefore 100% certificate
churn, and churn scales with KICKS — one dial with the belt stream, which itself
composes to 5.3–8.4 M1 cores on this week's levers.** Cross-checks: model rate ∝
density vs ec74's λ ∝ Ψ^0.95 (silver; 1b1f's 0.105–0.247/body/orbit at N=800 implies
their b was 2.7×10⁸ m; contacts 0.22/s × ~4 bits ≈ 09a1's gold 0.9 bits/s contacts
term (fermi; ledger.py arithmetic + shipped `belt_first`, predictions pre-registered,
one honest miss: the mint term). Consequence for the goal: at 10⁹ real bodies the
shipped belt *grinds* — one contact every ~4.5 game-s is the fragmentation/combat
feed, information 0.2–1 bits/s, CPU noise; the board's "cut encounter work by 10³"
is a certificate-scheduling question, not an event-volume question. *[20261018-1025
note: the singular number this paragraph owed was measured twice — 0.034/kick
proposed by the toy (20261018-1025-scout-fbf9), then killed on the shipped tier:
the sound per-kick term is wholesale Θ(n), 355 cores per 10⁴-cell occupancy
(20261018-1126-second-…-1a29); the row's closure stays on the slack/stream side or
a beat-storing representation.]*

*[Prior best retained below — the fleet row, the calendar, the sweep baseline, the
belt anchors: unchanged by these runs, which measured the dilute belt's per-kick tier
work only. See git history of this page for their full text.]*
## Refuted

- **"After a belt-quantum kick the pairs that must be re-checked are the
  near-horizon time-window band (0.034 arm-evals/body/kick at 10⁴, ∝n²)"** — the
  shipped-tier flight: silent→armed flips at 5–7×10⁻⁶ per candidate per kick,
  dv-independent, every flip-on outside the band, ~14% with real events
  (20261018-1126-second-20261018-1025-scout-fbf9-1a29). The band constant itself is
  real (conjunction dues reproduce it) — it is just not the re-check set.
- **"A beat-resident pair record could certify 'no early hit post-kick' without paying
  first_hit" (od 1 as stated, and every margin/slack form of it)**: the slack the record
  would live in does not exist — at L = 10⁵ passages it is p50 2.7 window widths and one
  quantum kick drifts it by 2.0 (drift/slack 0.8; the identity δd = 0.44·w fat-class,
  ~10³·w thin-class); at L ≤ 10⁴ it is vacuous (pi/5 — no window approach). The due itself
  fully decorrelates: flips = armed·(1−armed)·0.88–0.97 at every horizon, dv-independent
  over 64× (20261018-1530-components-e87d).
- **"Leak-gated slack between kicks" (od 2 re-scoped, quant-c9c7's branch at design reach)**:
  the leak of a certified-safe pair under quantum kicks is ~2×10⁻³ per kick-set, flat in
  1/8/64 kicks — the leak *is* the re-roll rate, so no budget above the news rate buys any
  skipping; the sound re-decision per pair per kick is forced (20261018-1530-components-e87d).
- **"The churn term falls ~4 orders and the row's CPU closes on cd3b's stream terms
  alone"** (same run): sound per-kick re-arm on the shipped representation is
  wholesale Θ(n−1) — 355 cores per 10⁴-cell occupancy at the checker's clock; the
  stream terms do not carry the row alone (20261018-1126-second-…-1a29).
- **"Stored slack with 0 violations transfers to the design reach"**
  (quant-c9c7's slack side, measured at ρ = 1e-4): above ρ\* ≈ 4.4×10⁻⁵ AU the
  window swallows the rotation step and the beat is smooth; at B = 3.3×10⁻⁶ AU the
  same skip leaks ~10⁻⁶ real events per candidate per kick
  (20261018-1126-second-…-1a29). The bit-stability finding stands; the soundness
  domain is reach-dependent.
- **"Pairs re-checked per kick at 10⁹-scale occupancy is the row's biggest unknown,
  plausibly ~10¹–10² cores"** (cd3b's own hedge on fe6b's 0.0346·n): measured on the
  shipped geometry's dilute cells — the sound term is wholesale n−1, the toy's band
  counter-proposal is now killed too (20261018-1025-scout-fbf9 toy;
  20261018-1126-second-…-1a29 flight).
- **"Slack bookkeeping in due-space makes intra-cell re-arms deferrable for ~10⁶
  kicks"** (the toy's own first model, killed inside the run): the due-walk is
  multiplicative — median cell-mates walk 10⁵–4×10⁶ intervals *per kick*
  (20261018-1025-scout-fbf9).
- **"The armed list can be stored across kicks"**: bare-B churn 0.5–0.75× armed per
  2⁻²³ kick (toy), 1.1× on shipped windows at the anchor
  (20261018-1126-second-…-1a29); stored lists need miss-space slack and a
  re-decision at the due (20261018-1025-scout-fbf9).

## Open directions
1. ~~**A representation that stores the beat**~~ **Measured dead** (20261018-1530-components-e87d,
   see Refuted): the slack the record needs does not exist (2.7 window widths at the first
   meaningful horizon, drift 2.0 widths per quantum kick), and the due fully decorrelates per
   kick (flips = armed·(1−armed) at every horizon). What replaces it, measured the same run:
   the float section (72% of the 1,394 ns eval) is kick-stable on Cross (δw p50 < 1 tick,
   shape 0/240,000; checker: tail δw ≤ 0.14·w, Full formations δw p50 0.32·w — Cross-class
   lever, tail soundness unmeasured)
   — **cache the section per pair, maintain (c0, d, pi) by exact integer deltas, decide with
   `first_hit`: 416 ns/pair/kick, 3.4× (355 → ~105 cores)**; then the u64 `first_hit` port
   (all section values < 2⁶³), unpriced. Below ~100 ns/pair/kick the row is a
   candidate-density question (pairs ∝ ρ·density), not a certificate question.
2. ~~**Leak-gated slack between kicks**~~ **Measured dead** (20261018-1530-components-e87d):
   the leak of a certified-safe pair IS the re-roll rate (~2×10⁻³/kick-set, flat in 1/8/64
   kicks), so no event-loss budget above the news rate buys skipping; the per-kick re-decision
   is forced. The Full-section corner (keys fleets, 0/100,000 in the measured cell) was
   measured by the checker (one-orbit formation): the kill extends — pre-kick due "never"
   for all pairs, one quantum kick flips 2.27×10⁻¹ at KH = 10⁶. The corner is closed.
3. **The mint term's semantics**: does every b≤5×10⁵-m conjunction re-mint a key
   (1.87 cores at rtf 100), or does efd4's intern hold it near zero? One flight
   with a mint counter on the live anchor decides.
4. **The conjunction calendar as the shipped fleet arm** — standing contacts as
   stored state, the due-queue as the only waker; the miss-space fragility
   (0.5–1.1× churn per kick) and now the beat re-roll both feed its slack design.
5. (prior) The belt-anchor dispute f0a2 vs 2b89; the refused-train (da ≥ 4e-4) tier;
   cross-group fleet×belt routing (`7532`).

## Contradictions

Resolved 20261018-1126: fe6b's 0.0346·n, quant-c9c7's 0.484·N saturation, and the
toy's 0.034 band read three different quantities — tier-1 scan sweeps (Θ(N),
e-dispersion-saturated), per-kick wholesale arm evals (n−1 in-cell), and the
conjunction-due band (real constant, not the re-check set). The churn regime is set
by w vs d: ρ ≫ ρ\* ≈ 4.4×10⁻⁵ AU is the smooth walk world (quant's replica,
slack sound there); ρ ≪ ρ\* is the deep-beat re-roll world (the design's B, no due
band sound). cd3b's flow (1.1×10³ conjunctions/s) and the anchors' armed counts
(~10³/body/horizon) still differ by convention (n₂D N/25 vs N/15.7, game-s vs s);
flip *fractions*, not absolute armed counts, carry the churn findings.

## Runs
- 20261006-0220-scout-4ea2 (gold): B13 flybys are an entry gap: analytic detection at ≥1.5·SOI as the doll door holds the gate; cadence rules fail.
- 20261006-0346-inversion-8cee (silver): shipped fixed-k check misses 5–7% at e 0.6–0.95; make_belt caps e at 0.5, so frozen verification never looked there.
- 20261006-0437-components-2222 (silver): cone certificates cost 93× the scan at n=10; per-pair sections re-paid per check — the skin framing is right.
- 20261006-0437-dynamics-43d5 (silver): no steady state: stirring keeps a kick floor; certificate re-setup churn 15–50× real encounters; fragmentation can run supercritical.
- 20261006-0737-components-4643 (gold): deferral killed: 92% of per-kick evals are window setup; ceiling 1.1–1.2×; analytic windows over-fire 427×.
- 20261006-1029-dynamics-6875 (silver): endogenous kicks hold work at 2.3–3.6×10⁵ evals per real encounter (control 2.2×10³); the steady state does not exist.
- 20261006-1135-spacex-317c (gold): skin windows as ρ-level sets at ρ_eff = ρ+1.5·s·r²max: exact at s=4·eps_u; setups/kick 14.95 vs 188.6; economy boundary measured.
- 20261006-1249-library-8f99 (silver): skin width must follow per-pair precession; the 55× resonance-split headline is confounded; the "hard floor" walks.
- 20261006-1436-autoresearch-cdf8 (lead): both claims die, but a real engine bug: hit()'s cross·cross overflows i128, reporting phantom encounters (19/19 plane contacts).
- 20261006-1436-scout-eab7 (silver): element-space skin makes setup track churn (8× at 16 epochs, horizon-limited); envelope unsound in churn at κ 1e-3.
- 20261006-1545-second-20261006-1436-scout-eab7-73f0 (gold): the cut equals mean cache lifetime τ = slack·eps_u·32/((e/p)·g); slack-0.5/widen-2 unsound at strong rotation.
- 20261006-2240-b-encounter-skin-8bfa (silver): slack skin built in crates/encounters: 0/0 vs independent truth; setups/kick 142.3→17.1; total evals still rise 1.5×.
- 20261007-0341-second-20261006-2240-b-encounter-skin-8bfa-57c1 (silver): the setups cut converts: fleet total evals 3.6×, wall 3.0–3.7×, p95/p99 down 3–4×; max-age refresh unimplemented.
- 20261007-0621-autoresearch-f521 (silver): hoisting j's arc grid plus dropping unused acceleration terms cuts setup 1.39×, bit-identical certificates; ~20 lines.
- 20261007-0711-taleb-2e81 (gold): fleet engagement is a second ruin: Θ(n_A·n_B) store (~144 TB at 10⁶×10⁶); trigger and node guard blind; tier exactly sound.
- 20261007-1032-quant-7578 (silver): the certificate's cost is a burst, not a load: degree/body ∝ N at ρ=1/N; re-pay p99 20–80 ms at 10⁴–10⁵.
- 20261007-1234-dynamics-da90 (lead): replay completeness measured on a self-selected minority; 70–98% of unscheduled encounters are silent on the author's own stream.
- 20261007-1550-dynamics-71a5 (gold): differential precession kills the "never" certificate at t_tang = travel/Δϖ̇ (12/12); sections belong in the co-precessing frame.
- 20261007-1801-dynamics-532c (silver): coplanar pairs split by χ_t = Δa/(e₁a₁+e₂a₂); conjunction-anchored checks miss 40–97% of deep crossings; CF pays only sparse.
- 20261007-1843-dynamics-1b1f (silver): the 0.1-encounters/body/orbit attractor is dead: rate 0.105→0.247 still climbing at 800 orbits; static budgets wrong ×2.5.
- 20261007-2002-library-b2d5 (silver): practitioner lessons plus a candidate-cost law (fixed-extent slope 1.0); the dilution headline is confounded by per-band density growth.
- 20261007-2246-system-969a (silver): the law's 12+12-bit Catalogue key is a candidate tier: zero misses on 8 scenes; 2.7× median cut vs O(N).
- 20261007-2344-second-20261007-2246-system-969a-5d90 (gold): timing tier on the key window: recall 1.0, tier-2 work bit-identical; sound domain ends at e≈0.969 (206/289 missed beyond).
- 20261008-0338-redteam-4e7c (lead): GR-doll apsidal advance breaks the rotation timing and the cone; record doctored — the GR domain is untested, direction only.
- 20261008-0945-taleb-48e5 (silver): radial concentration does not break the cone: cpe ≈ 1.2·a^2.6/ρ; degree tails ≤ 3.9; the ρ-adoption mechanism falsified.
- 20261008-1058-second-20261008-0945-taleb-48e5-abd7 (gold): cpe decomposes exactly as a^1.5 local clock × a^1.0 relative-ρ: ρ∝a plus per-doll clocks makes it radius-flat.
- 20261008-2031-dynamics-87da (lead): the pair-timing rotation identity is real (2.7e-10) but the 95–98% "never" tables are uniform-sampling artifacts.
- 20261008-2113-scout-6652 (silver): the Wide window's closed-form h(λ) replacement misses zero, but its unmargined 17-sample routing falsely kills 3/6 high-e sections.
- 20261009-0401-second-20261009-0208-fermi-fe6b-90fb (gold): cascade anchored at 10⁶: pairs/kick = 0.0346·n·(1+X)/(2(X−1)); skin 0.077 cores/cell; U-index 16 GB at 10⁹.
- 20261009-0521-library-189e (gold): the CF/Diophantine conjunction calendar killed at belt scale: median rank 0.48 ≈ random; conjunctions cluster when 2e·n > |Δn|.
- 20261009-1345-second-20261009-1259-fermi-c7eb-46a6 (gold): contact impulse validated (median 0.998 over 1091 RK4); m_crit ≈ 1.3×10⁻¹⁷ M☉; 50-m rocks never cross a tick.
- 20261009-1345-system-136a (silver): quantized (periapsis,k) buckets are a conservative cone index (zero misses, superset ×1.02–1.49); Δϖ-band caches amortize ×43–312.
- 20261009-1504-second-20261009-1345-system-136a-ca96 (gold): the Δϖ-band cache refuted as zero-miss: tolerance ≈1e-5 rad, 9.3% silent miss; the arc geometry θ_c binds.
- 20261009-1649-system-aa29 (silver): the kick resonance gate and the CF pass read one synodic rotation; the standalone detector is deletable; recall 46–92%.
- 20261009-1858-library-c716 (silver): time-priority τ book: static keys miss 99%; τ frac≤4 is 0.6–0.8; the O(N·k) gain is asserted, not measured.
- 20261009-1936-system-8716 (silver): the cone ∧ wrap(Δλ₀) rule unifies the tiers, recall 1.0 — but its ΔU-linearized index misses 66/495 on bimodal-e belts.
- 20261009-2043-second-20261009-1936-system-8716-88ee (gold): occupants' exact mean-motion extremes make the unified index emit the naive rule: 0/0 on 23 scenes; trigger deletable.
- 20261009-2120-library-30a7 (silver): naive CF/beat next-conjunction prediction misses ~90% (fA 0.067); the "≥3× skin" prescription falsified; corroborates the calendar kill.
- 20261009-2212-dynamics-79ef (silver): stirred-belt rate decays λ∝t^-0.25, collapsing to λ=0.345·e^-0.215; mildly self-exciting (b≈0.35, subcritical); tails 1.8× Poisson.
- 20261010-0541-dynamics-6565 (silver): belt encounters do not avalanche: corrected branching 1.01–1.11× baseline; the elastic runaway is real; τ=2 rows mislabelled.
- 20261010-1029-taleb-5c01 (gold): silent misses are a horizon-edge hole: 20.2% of true encounters; two unconditional edge checks catch every observed miss.
- 20261010-1920-autoresearch-ccc6 (silver): setup cut 1.4–2.1× and a dual-guard skin cuts kick re-cert 7377→851 µs/kick at ε1e-9, zero violations; 10–15× undelivered.
- 20261010-1947-second-20261010-1920-spacex-cb3f-f79a (gold): the same-doll pre-filter is priced out: airtight bound rejects 0.07%; exact tier ~4 µs/pair linear — do-not-spend.
- 20261011-0517-quant-d7bd (silver): PlayerNeighbourhood::find is an exact O(N) scan at 1.5–1.9 µs/body: one player event crosses the frame at ≈10⁴ bodies.
- 20261011-0736-dynamics-ec74 (silver): impulsive conjunctions valid only inside b ≲ 3 r_H; swarms a Poisson gas (λ ∝ Ψ^0.95); game swarms deletable.
- 20261011-0924-library-9834 (silver): synodic strobe: a frozen pair's indicator is a rotation-hitting sequence; three numbers per pair; 78–91% deletable — frozen only.
- 20261011-1102-second-20261011-0924-library-9834-5c16 (gold): the three-number record inverts under real kicks: amortized work 1.1–20× scanning; 43k–3.97M evals/encounter vs 38k.
- 20261011-1234-taleb-62f7 (gold): crossing packets make contacts Θ(n_A·n_B) (exponent 1.94): events are the workload; per-ship flux replaces enumeration, 0.87–1.04 of truth.
- 20261011-2132-autoresearch-a85a (silver): caching j's τ-grid and k=32→16 cuts per-kick re-certification 1.6–2.1× with identical events, zero misses everywhere.
- 20261011-2132-second-20261011-2028-system-3b42-214f (gold): the same-key straggler tier freezes as a closure-scaled arc window (cand/enc 5.3–5.6 in n); U(L)|E never turns bound.
- 20261012-1340-quant-e49d (silver): one kick's wake is O(N) (6.8 ms at 10⁴) but 98% defers by deadline; the skin cannot absorb player burns.
- 20261009-0401-second-20261009-0208-fermi-fe6b-90fb (gold): cascade anchored at 10⁶: pairs/kick = 0.0346·n·(1+X)/(2(X−1)); skin 0.077 cores/cell; U-index 16 GB at 10⁹. *[20261014-1137: the per-cell label corrected — 0.966/0.077 is the partitioned total; the law, anchor and verify controls all stand.]*
- 20261014-1137-fermi-1738 (awaiting grade): the 10⁹ encounter ledger audited: 90fb's per-cell constant is the partitioned total (max-rtf 5,216 reproduced), effb's ×10⁵ double-bills; the honest cube spans 0.077 to 3×10⁷ cores on cadence/topology/skin; the remaining engine lever is the contiguous belt's candidate count.
- 20261014-1221-scout-0b81 (silver): the quantum gate measured — one Q48 of E against each pair's strongest conjunction; author model: 99.96% deleted, ledger 0.5–3.1 cores; checker: the miss model is 6×10²–9×10³× too large at Δa ≤ 0.05 (Kepler-true misses quasi-periodic), corrected 95.5–97.8% and 37–369 cores — mechanism and controls stand, the budget claim does not; phase-free group certificates vacuous (1/K→0); the mass spectrum is the content dial.
- 20261014-1511-scout-f0a2 (awaiting grade): the exact tier empties at the shipped key's own Q48 (gate deletes 1.00000, survivors ≥34-km partners); the affordable gate is a birth-constant route (D* = 1.3 km, wake cut 129×, 10⁹ → 0.03–0.6 cores of routing); the one-bit floor unsound (aligned conjunctions 1.9×10⁻⁶·v_k) — pair-geometry floor + phase tier; the anchor dispute with 0b81 opened.
- 20261006-1029-dynamics-6875 (silver): endogenous kicks hold work at 2.3–3.6×10⁵ evals per real encounter; the steady state does not exist.
- 20261006-1135-spacex-317c (gold): skin windows as ρ-level sets at ρ_eff = ρ+1.5·s·r²max: exact at s=4·eps_u; setups/kick 14.95 vs 188.6.
- 20261006-1249-library-8f99 (silver): skin width must follow per-pair precession; the 55× resonance-split headline is confounded.
- 20261006-1436-autoresearch-cdf8 (lead): both claims die, but a real engine bug: hit()'s cross·cross overflows i128.
- 20261006-1436-scout-eab7 (silver): element-space skin makes setup track churn; envelope unsound in churn at κ 1e-3.
- 20261007-0621-autoresearch-f521 (silver): hoisting j's arc grid plus dropping unused acceleration terms cuts setup 1.39×, bit-identical certificates.
- 20261007-0711-taleb-2e81 (gold): fleet engagement is a second ruin: Θ(n_A·n_B) store (~144 TB at 10⁶×10⁶); trigger and node guard blind.
- 20261007-1234-dynamics-da90 (lead): replay completeness measured on a self-selected minority; 70–98% of unscheduled encounters are silent.
- 20261007-1550-dynamics-71a5 (gold): differential precession kills the "never" certificate at t_tang = travel/Δϖ̇; sections belong in the co-precessing frame.
- 20261007-1801-dynamics-532c (silver): coplanar pairs split by χ_t = Δa/(e₁a₁+e₂a₂); conjunction-anchored checks miss 40–97% of deep crossings.
- 20261007-1843-dynamics-1b1f (silver): the 0.1-encounters/body/orbit attractor is dead: rate 0.105→0.247 still climbing at 800 orbits.
- 20261007-2002-library-b2d5 (silver): practitioner lessons plus a candidate-cost law (fixed-extent slope 1.0); the dilution headline is confounded.
- 20261007-2344-second-20261007-2246-system-969a-5d90 (gold): timing tier on the key window: recall 1.0, tier-2 work bit-identical; sound domain ends at e≈0.969.
- 20261008-0338-redteam-4e7c (lead): GR-doll apsidal advance breaks the rotation timing and the cone; record doctored — the GR domain is untested.
- 20261008-0945-taleb-48e5 (silver): radial concentration does not break the cone: cpe ≈ 1.2·a^2.6/ρ; degree tails ≤ 3.9.
- 20261008-1058-second-20261008-0945-taleb-48e5-abd7 (gold): cpe decomposes exactly as a^1.5 local clock × a^1.0 relative-ρ.
- 20261008-2031-dynamics-87da (lead): the pair-timing rotation identity is real but the 95–98% "never" tables are uniform-sampling artifacts.
- 20261009-0521-library-189e (gold): the CF/Diophantine conjunction calendar killed at belt scale: median rank 0.48 ≈ random.
- 20261009-1345-second-20261009-1259-fermi-c7eb-46a6 (gold): contact impulse validated (median 0.998 over 1091 RK4); m_crit ≈ 1.3×10⁻¹⁷ M☉.
- 20261009-1345-system-136a (silver): quantized (periapsis,k) buckets are a conservative cone index; Δϖ-band caches amortize ×43–312.
- 20261009-1504-second-20261009-1345-system-136a-ca96 (gold): the Δϖ-band cache refuted as zero-miss: 9.3% silent miss.
- 20261009-1649-system-aa29 (silver): the kick resonance gate and the CF pass read one synodic rotation; the standalone detector is deletable.
- 20261009-1858-library-c716 (silver): time-priority τ book: static keys miss 99%; τ frac≤4 is 0.6–0.8.
- 20261009-2043-second-20261009-1936-system-8716-88ee (gold): occupants' exact mean-motion extremes make the unified index emit the naive rule: 0/0 on 23 scenes.
- 20261009-2120-library-30a7 (silver): naive CF/beat next-conjunction prediction misses ~90%; corroborates the calendar kill.
- 20261009-2212-dynamics-79ef (silver): stirred-belt rate decays λ∝t^-0.25, collapsing to λ=0.345·e^-0.215; mildly self-exciting.
- 20261010-0541-dynamics-6565 (silver): belt encounters do not avalanche: corrected branching 1.01–1.11× baseline.
- 20261010-1920-autoresearch-ccc6 (silver): dual-guard skin cuts kick re-cert 7377→851 µs/kick at ε1e-9, zero violations.
- 20261010-1947-second-20261010-1920-spacex-cb3f-f79a (gold): the same-doll pre-filter is priced out: rejects 0.07%; exact tier ~4 µs/pair linear.
- 20261011-0517-quant-d7bd (silver): PlayerNeighbourhood::find is an exact O(N) scan at 1.5–1.9 µs/body.
- 20261011-0736-dynamics-ec74 (silver): impulsive conjunctions valid only inside b ≲ 3 r_H; swarms a Poisson gas.
- 20261011-0924-library-9834 (silver): synodic strobe: a frozen pair's indicator is a rotation-hitting sequence; 78–91% deletable — frozen only.
- 20261011-1102-second-20261011-0924-library-9834-5c16 (gold): the three-number record inverts under real kicks: amortized work 1.1–20× scanning.
- 20261011-1234-taleb-62f7 (gold): crossing packets make contacts Θ(n_A·n_B) (exponent 1.94): per-ship flux replaces enumeration, 0.87–1.04 of truth.
- 20261011-2132-autoresearch-a85a (silver): caching j's τ-grid and k=32→16 cuts per-kick re-certification 1.6–2.1× with identical events.
- 20261011-2132-second-20261011-2028-system-3b42-214f (gold): the same-key straggler tier freezes as a closure-scaled arc window.
- 20261009-0401-second-20261009-0208-fermi-fe6b-90fb (gold): *[20261014-1137: the per-cell label corrected — 0.966/0.077 is the partitioned total; the law, anchor and verify controls all stand.]*
- 20261014-1137-fermi-1738 (awaiting grade): the 10⁹ encounter ledger audited: the honest cube spans 0.077 to 3×10⁷ cores; the remaining engine lever is the contiguous belt's candidate count.
- 20261014-1221-scout-0b81 (silver): the quantum gate measured — author model 99.96% deleted / 0.5–3.1 cores; checker: the uniform miss model is 10²–10⁴× too large, corrected 95.5–97.8% and 37–369 cores; phase-free group certificates vacuous (1/K→0).
- 20261014-1511-second-20261014-1221-scout-0b81-277d (silver, this run): the checker's gold experiment done exactly — Kepler-true yield 95.5–98.0% (validated +0.02% vs brute), r_event 480–700 ns x86, f_r 0.017–0.025 event-scheduled vs 5–7 per-refresh (killed), ledger 62–571 cores: ceiling 14–24×, flux split mandatory; all-10-km control 0.003; real-mass ×52 → 0.377.
- 20261014-1221-scout-0b81 (silver): the quantum gate measured — one Q48 of E against each pair's strongest conjunction; mechanism and controls stand; phase-free group certificates vacuous (1/K→0); the mass spectrum is the content dial.
- 20261014-1511-scout-f0a2 (awaiting grade): the exact tier empties at the shipped key's own Q48 (legacy E anchor); the affordable gate is a birth-constant route (D* = 1.3 km, wake cut 129×, 10⁹ → 0.03–0.6 cores of routing); the one-bit floor unsound. *[Live-path anchor measured 20261017: the shipped binding stores no E — see this run's Refuted.]*
- 20261014-1511-second-20261014-1221-scout-0b81-277d (silver): the checker's gold experiment done exactly — Kepler-true yield 95.5–98.0% (validated +0.02% vs brute), r_event 480–700 ns x86, f_r 0.017–0.025 event-scheduled vs 5–7 per-refresh (killed), ledger 62–571 cores: ceiling 14–24×, flux split mandatory; all-10-km control 0.003; real-mass ×52 → 0.377.
- 20261017-0839-fermi-2b89 (fermi, this run): the live anchor measured — ev = −73, quantum 3.17e-14 m/s, every Dohnanyi conjunction fires and mints a key from 2¹¹–2¹² quanta; the exact tier is full on the live path; 10⁹ closes on the flux accumulator at every width; the anchor is a word-width dial (5–15 bits between 277d's and f0a2's worlds).
- 20261017-0839-inversion-2373 (inversion, silver): the phase certificate's k priced — quadratic in F for every fleet with shape dispersion, 36–4,500 cores at 10⁹ fleets; the composed ledger's encounter row is population-dependent and missing.
- 20261017-1018-second-20261017-0839-inversion-2373-b509 (second, pending grade): the
- 20261018-0543-library-5567 (library): the fleet row dies by representation — the shipped Fermi-frame fleet carries F=10⁵×10⁴ at ≤ ~1 core (0.89 µs/member/game-s measured, member-flat slices, scale-free epoch composition); dissolution at spread > r_p/32 measured; three wiring debts named.
- 20261018-0932-fermi-cd3b (fermi): the belt row's event flow at 10⁹ is cheap and small (0.22 contacts/s, 1.1e3 conjunctions/s, ≤1.9 cores worst-case mint) — the row is 100% certificate churn riding the kick cadence; the stream composes to 5.3–8.4 M1 cores.
- 20261018-1025-quant-c9c7 (quant): the churn constant measured — 0.484·N candidates/kick at the belt mix, window saturated by the e-tail (fe6b's 0.0346·n is the unsaturated regime, X ≈ 1.5); rescans 10⁷–10⁹ cores at 10⁹; slack 92.5% skippable, 0 violations at the quantum.
- 20261017-0839-inversion-2373 (inversion): the formation regime's cure is quadratic in fleet size; the phase certificate's paid occupancy law k̄ = F·(4·e_max + 0.75·da·TAU·H)/TAU verified to 3 digits.
- 20261017-1018-second-…-b509 (silver): the calendar measured: arm 1.02–1.16 µs/pair vs 57.7–414.7 exact; sound 0/0; the armed set is ρ-driven; a standing pair re-evaluated per interval costs 31 ms — store it.
- 20261018-0543-library-5567 (silver): the fleet row dead by representation: the Fermi-frame fleet carries F = 10⁵ × 10⁴ at ≤ ~1 core; checkers extended to m = 6,144 and priced the all-battle bound.
- 20261018-1025-scout-fbf9 (silver, self-suggested): the churn constant answered — 0.034 re-arms/body/kick at n = 10⁴ (∝ n² at fixed density), not 0.034·n; the term falls ~4 orders in arm-evals (checker-corrected; the author's ~6-orders headline does not reproduce); armed lists are miss-space fragile (0.5–0.75×/kick at bare B); kill test = one shipped-tier flight.
- 20261014-1511-scout-f0a2 (awaiting grade): the exact tier empties at the shipped key's own Q48 (gate deletes 1.00000, survivors ≥34-km partners); the affordable gate is a birth-constant route (D* = 1.3 km, wake cut 129×, 10⁹ → 0.03–0.6 cores of routing); the one-bit floor unsound (aligned conjunctions 1.9×10⁻⁶·v_k) — pair-geometry floor + phase tier; the anchor dispute with 0b81 opened. *[Live-path anchor measured 20261017: the shipped binding stores no E — see this run's Refuted.]*
- 20261017-0839-fermi-2b89 (fermi): the live anchor measured — ev = −73, quantum 3.17e-14 m/s, every Dohnanyi conjunction fires and mints a key from 2¹¹–2¹² quanta; the exact tier is full on the live path; 10⁹ closes on the flux accumulator at every width; the anchor is a word-width dial (5–15 bits between 277d's and f0a2's worlds).
- 20261017-1018-second-20261017-0839-inversion-2373-b509 (silver): the calendar measured: arm 1.02–1.16 µs/pair vs 57.7–414.7 exact; sound 0/0; the armed set is ρ-driven; a standing pair re-evaluated per interval costs 31 ms — store it.
- 20261018-0543-library-5567 (silver): the fleet row dead by representation: the Fermi-frame fleet carries F = 10⁵ × 10⁴ at ≤ ~1 core (0.89 µs/member/game-s measured, member-flat slices, scale-free epoch composition); dissolution at spread > r_p/32 measured; three wiring debts named.
- 20261018-1025-quant-c9c7 (quant): the churn constant measured — 0.484·N candidates/kick at the belt mix, window saturated by the e-tail (fe6b's 0.0346·n is the unsaturated regime, X ≈ 1.5); rescans 10⁷–10⁹ cores at 10⁹; slack 92.5% skippable, 0 violations at the quantum (smooth-regime ρ; see 1a29 for the design-reach leak).
- 20261018-1126-second-20261018-1025-scout-fbf9-1a29 (second, this run): the kill test flown on the shipped tier — the due-band rule KILLED: silent→armed flips 5–7×10⁻⁶/candidate/kick at the quantum, dv-independent (deep-beat re-roll, w ≈ 23 ticks ≪ d ≈ 3×10⁵), all flip-ons outside the band, ~14% with real events; sound per-kick re-arm is wholesale Θ(n−1) (355 cores/10⁴-cell at the checker clock); toy's conjunction-band constant, n−1 wholesale, bit-stability, clean dwell, 1.2 µs/arm all confirmed; regime boundary ρ\* ≈ 4.4×10⁻⁵ AU reconciles quant-c9c7 (ρ ≫ ρ\*, smooth) with the design reach (ρ ≪ ρ\*, re-roll).
- 20261018-1530-components-e87d (components, awaiting grade): od 1 and od 2 measured dead — the due fully decorrelates per quantum kick (flips = armed·(1−armed)·0.88–0.97, dv-independent 64×, 1a29's regime reproduced), slack 2.7w vs drift 2.0w at L=10⁵, stale-record leak ~2×10⁻³/kick flat; survives: δw < 1 tick and shape 0/240,000 → the 72% float section is cacheable, 1,394 → 416 ns/pair/kick (3.4×, 355 → ~105 cores), then the u64 first_hit port; below that the row is candidate density.
