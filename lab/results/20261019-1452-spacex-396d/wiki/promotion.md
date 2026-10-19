topic: promotion
status: open
closed-by:
valid-while:
updated: 20261019-1452-spacex-396d

# The compact↔live promotion: what the boundary costs, in bytes and in µs

## Current best
**NEW (396d, spacex — the player-seam flight, promotion od 1's unflown arm, flown at K = 10⁴ and 3×10⁴):**
crossing the belt turns **every** player scan inside the belt's *registered radial hull* into a
full-universe walk, the hull is ~2.5× wider than the density band (walks r = 1.62 → 5.17 AU over
gs 45,247 → 103,580, against the band's 2–3 AU: the e-smeared `[rmin, rmax]` registration, not the
window's width, sets the zone — every belt body registers ~10–20 bins, so any window touching the
hull sums ~N bin-entries against the global `bodies/4 + 64` and the filter bails), `cands` = 9,715 /
29,715 (= N − locals, every doll-0 body), capture 0.9–2.0 ms / 4.3–9.1 ms ⇒ **167 → 214 ns per walked
body** (c439's binding_at law, on the walk), **and no frame goes over from the seam at these rungs**
(the over frames of both flights, 74/80 of 297,840/160,380, cluster at gs ≈ 140–150k outside the walk
zone — the root doll's boundary wave; the worst frame 42.36 ms is 4447's known burn tail 42.5, the
instrument's control match; the walk zone itself has zero over frames: the 9,715-candidate answers
drain into idle room at p50 0.024 ms) — while the memory ratchet walks to its guard (1,400/1,300 MB)
with a **K-independent** late slope of 2.23 / 2.07 MB per held scan, which **excludes the walk
candidates as the ratchet's bytes** (3× the candidates at 3×10⁴, the same slope; 4447's held↔RSS
coupling confirmed, their open byte attribution now narrowed past the scan-answer channel).
Home's doll: 2,095 scans, zero walks — the negative control. A 1-D radial index cannot cut a
population at its own band once e > 0 smears the registration: the cheap fix direction is the second
axis this page keeps arriving at (the phase/along-orbit compare), not a better radial threshold
(20261019-1452-spacex-396d, spacex; shipped flight + print-only env-gated `ES_SEAM_CENSUS`
(off = shipped path: 0 census lines, kicks bit-identical 5,651/5,651, events within the same-arm
load spread 17,686–17,727), two flights ≤ 90 s wall, regen ~4 min; predictions pre-registered:
P1 held and extended to the hull, P2 held, P3 wrong on frames, P4 wrong, P5 half-held — the run's
kill criterion, walk = 0 through the crossing, did not fire. Frame verdict is a these-rungs verdict:
at 10⁶ one in-band answer is ~4 s at 604c's µs/candidate class — do not quote "no over frames" past
3×10⁴.)
[checker, one decade up (K = 10⁵, flown): the cost law extends exactly — in-band walks 42, cands
= 99,715 = N − 313, 214 ns a body, in-band capture p50 21.4 ms over the 12 ms budget, so at 10⁵ the
seam owns over frames as scoped; but the 1.5 GB guard fires at frame ≈ 21k mid-hull with a slope
≈ 5.8 MB a held scan (~22× faster per frame than 10⁴) — the K-independent slope is a
10⁴–3×10⁴ fact, and at 10⁵ memory breaks before the seam does; the exclusion must not be quoted
past 3×10⁴ (at 99,715 cands × 216 B ≈ 21.5 MB a held scan, the guard's mid-hull firing is what
pinned candidates would cause). Also: the generator caps apoapsis at 3·(1+0.4) = 4.2 AU, so the
zone's last AU (4.2→5.17) is window reach, not registration, and the median belt body (e ≈ 0.07)
registers ~3–4 bins, not 10–20 — the summed bin-entries, not any per-body count, are what fires
the bail. Coast control, whole flight: 290 scans, zero walks.]

**[20261018-0722-second-…-5f36] The tier is re-derived against the exact `law::hit` (approaching
conjunct in) and flown on the shipped binary (`rigidring` probe: a rigid keys ring, one compiled
key, e = 2^-48, beside the shipped plane): the read list on a rigid keys fleet IS the phase window
at the scan's own interval (flown 32 at (K=10⁴, ρ=1e-5) and 32 again at (K=10⁵, ρ=1e-6); at
larger intervals the segment read list grows past it — 2.2e4/2.5e4 at intervals 2¹²/2²⁴, K=10⁵,
32.6, candidates = 1.00·K + background, the engine's answers agreeing member-for-member with an exact
integer replica of `Scan::compute` — but the shipped ANSWER is neither empty nor law-decided: it
is a quantization-signed residual (a scene-dependent fraction of the window at the scan tick —
47–53% on the author's rings, 19% at K=3·10⁴, checker2 — swinging 15→31→12 across quarter-period
decode points on a time-constant window — the approaching sign at the edge is grid noise, and
the same-orbit relative motion is ⊥ to 1.3e-9 at large h). So the exact tier reads the window
(~353 at K=10⁶, ρ=1e-6), never ~0. The selector is sound at 0 misses over 48 cells (e ≤ 0.5,
σ_a ≤ 1e-3, h ∈ {P/10, 9}, clustered) ONLY as a 2D capability curve C(δ, Δa) (2¹⁴ × 9 Δa-bins,
one-cell/one-bin widening) [checker2: still 0 misses on 15 cells beyond the swept axes — h = 90
and 0.05, σ_a = 3e-3 (bins widened), ρ = 1e-5, σ_φ 0.005–0.05; reads/hits up to 68× at (0.5, 1e-3,
h = 90)]: the 1D curve misses up to 9% of hits at e = 0.1–0.2 (near apsides
the same-orbit d·w is O(δ²), so a linear-in-Δa shear flips the approaching sign ≈1.5·near
outside the window), and the UNwidened curve misses 69–84% of hits (the hit set is one-sided
under the approaching conjunct). Store-grounded price: the window lookup at K=10⁶ is 3.2 µs
(`searchsorted` on the δ-sorted class-major store — O(log K), the 19.2 ns/member figure
retired; unsorted packed sweep 0.32 ms), exact reads at the flown 1.9 µs/cand (3.8 µs at
e = 0.1 — the flown eccentric arm, `e_q48 = 2^48/10`, not 0.05 as the dossier says; 604c's 4.4 µs
class): the ρ=1e-6 closure at K=10⁶ is 0.67 ms/scan flown-rate
(1.56 ms at 604c's) against 1.9–4.4 s shipped — ~3×10³×, and the observer term closes under
one frame budget (the "≈1×" letter, flown end to end).**

**[20261018-0431-scout-b083] The scan's phase axis is corrected to the answer tier, and it
is measured on the shipped predicate: no horizon can cut a circular formation's candidates
(the coast window ≈ 9r contains the ring and every member's radial range is the player's
own — 604c's 1.00·K law is structural, not a dial), but on a shared circular orbit
d·w = 0 exactly (3.6e-15), so the per-member read list collapses to one compare on a
stored phase offset — 2r·sin(δ/2) ≤ 2¹⁰·ρ·r, horizon-independent (no closure on a rigid
ring: these answers carry slack, not urgency) — at 19.2 ns vectorised / ~10 ns
native against the measured 4.4 µs per-candidate read (7.1 µs with capture's binding_at):
the 10⁶-ship formation scan falls 4.4 s → ~10–20 ms plus 353 exact reads (~2× order on
the instrument, load-dependent — the regen 200× assert fails at 79× on a loaded box,
checker), closing 604c's ~500×-over answer term to ≈1×. [Checker: the shipped law::hit
additionally requires *approaching* (d·w < 0, law.rs every branch), which the replica
dropped; on a rigid ring d·w ≡ 0 (identically on the integer lattice), so the shipped
encounter *answer* there is empty — the 37/353/3,204 near set is the exact tier's read
list (a sound superset: law::hit ⊆ seg-dist ⊆ the window), not the shipped answer set;
the price holds a fortiori, the answer needs the approaching conjunct.] [0722, flown: the
answer is the quantization-signed residual — ≈ half the window, unstable across decode
points; the selector needs the 2D curve; see Current best.]** The near set
is a pure phase
window (37/353/3,204 per 10⁶ at ρ = 1e-7/1e-6/1e-5; ∝1/σ_φ under clustering to 4.1k/40.6k/
391k — the clustered tail is the standing-contact class, encounters od 1's group
certificate, not per-member reads). The failure modes are priced: the naive circular chord
degrades to 0.8–3.0% membership error at e = 0.2–0.5 (the per-orbit-class capability curve
C(δ, ν_p) is grid-limited, not e-limited: 0.8% at 2¹⁴ samples, sound with one-cell
widening; build ~29 ms per ν-bin per class amortized ~1e-3 s/s — circular formations, the
measured ruin class, need no curve); the phase-only tier is sound for σ_a ≤ 1e-5·a (0
misses/40k at h=P/10; onset of unsoundness at σ_a ≈ 1e-3 against the predicted
1.5·n·σ_a·h ≈ near at 1.09e-3; keys fleets are σ_a = 0 by birth) [checker: the onset is
horizon-dependent — at the coast horizon h ≈ 9 (the ruin case) σ* ≈ 7.6e-5, first
misses measured at 7.6e-5 and 5 at 1e-4; the sound class σ_a ≤ 1e-5 has 0 misses at
both horizons; and at ρ = 1e-4 under clustering the near set is 100% of the fleet —
the tier is net-negative one decade past the swept range]; and 99.97% of the shipped
reads on a uniform fleet buy ≤ 0.001 bits (the boundary comb's no-op machine, at the
observer). Float replica of the shipped predicate's segment distance (encounter.rs::
Scan::compute, radial.rs window; the approaching conjunct d·w < 0 of law::hit was
dropped — see the bracket above),
r=1 units, controls both sides (e=0 exactness 2.2e-16; shuffled-table 47.7% disagreement);
Linux/x86 orders of magnitude. Mechanism = PRINCIPLES 32 (the crowd's symmetry is the one
compiled key the engine already mints per keys-fleet) and bottleneck 0's own store shape
(bodies as offsets in the cell's frame); prior art fit-ranked: Clohessy–Wiltshire/Hill and
the shearing sheet (first-order-only, the standing rule), constellation phase-slot tables,
taleb-09b5's rank axis at the observer tier.

**The formation frame's tail is decomposed per frame, and the fix ranking inverts: the over-budget
frames at fleet scale in-phase are comb-owned (91.7-99.7% item pipeline: kicks, boundaries, fits),
not scan-owned — at K=1,000, 0.6-1.0% scan / 97.7-98.5% comb in the 68 over frames on both seeds
and two passes, the six p99 frames 98.0-98.7% comb, the worst frames the wave frames (`ev=1002`;
comb 43.9-65.4 ms against scan 0.24-0.33; at 3,000+10⁴ the worst is 137.26 ms = 1.47 scan /
134.23 comb, `ev=3002`; at 10⁴, p99 452.8-463.5 ms, 98.4% comb) — so the frame's first fix is the
comb's cadence (de-phase the births; kick-cadence's), and the observer's phase axis is second: the
scan channel rides idle room below 69f3's latch (72-95% of its ns inside under-budget frames
[checker: 95/95 author-regen, 88 seed 3, 72 seed 5 — the placement is seed/load-dependent; the
tail ownership is not], 3-10% of mean frame wall at K ≤ 1,000 (seed 5: 2.9), answers ~3.9-4.4
ms one at a time (seed 5: 4.41), held_max ≤ 54 of 2,048 across five seeds, ≤ 71 at any K),
freezes above
it (zero answers in flight at K ≥ 3,000 — 69f3's `S < b/2` with S ∝ K, the crowd law setting S)
and then pins 51 MB (3,000+10⁴: 71 held × 3,338 × 216 B) to 93 MB (10⁴) [checker2, one decade
beyond: 2×10⁴ pins 43 × 20,039 × 216 B ≈ 186 MB — the pin ∝ K; there the over frames stay 0.7%
scan / 95.1% comb, worst frame ev=20,002, comb 923 ms, hwm 932 MB]. 0552's P5 mechanism is
corrected: SCAN_BACKLOG (2,048) never fires in any flight (held_max ≤ 71); below the latch the
answers drain into quiet frames, above it they stop, not pile into a frame
(20261017-0739-second-20261017-0552-inversion-604c-2e42, per-frame top-level prof channels closed
against wall to 98.4-99.6%, both seeds, coast, rtf 100, regen.sh; seed-1 K=1,000 digest identical
to 0552's). What stands from 0552: both channels' own bills are crowd-proportional, so at 10⁹ the
observer fix alone buys a smooth mean on a ruined frame — the two fixes are ranked, not
alternatives.**


**The observer half's "bounded near set" is measured on the game's own crowd and it is crowd-proportional:
the radial filter bails on 100% of the plane's own coast scans (28 bodies, no formation: 87/87, the window
at coast covers every radius from zero — reach ≈ 9·r from h = 1.1e12 doll units × speed_cap 9.76e-3, and
the bail's numerator counts bin-entries, 1,947 mean against 71 registered, so `hit ≫ bodies/4 + 64` at
plane scale), a fleet formation on the player's circle adds 1.00 candidates a ship (37.7 + 1.00·K:
87.7 at 50, 1,037.9 at 1,000; capture 382 µs and one answer 4.53 ms a scan at K=1,000, 4.4 µs a
candidate), 1,000 ships put the p99 at 52.5 ms (68/600 frames over the 12-ms budget, 23% of game time
lost; beside the comb: 128 events a frame, 9× the spread-10³ class), and 200 ships beside a 10⁴ belt
switch the whole universe's scans back to full walks (78/84 bailed, 9,549 binding_at a scan, 51× the
census's 186) — the filter's on/off decided by other dolls' populations (the belt inflates `self.bodies`,
the bail's denominator), a nonlocal coupling against PRINCIPLES 15 (20261017-0552-inversion-604c,
inversion; coast, rtf 100, seed 1, print-only `radial::scanstat` census bit-stable across reruns,
`prof` stages, regen.sh; at 10⁹ a 10⁶-ship fleet ≈ 0.36 s capture + 4.4 s answer a scan ≈ ~500× over
at rtf 100, and a held scan pins candidates × 216 B).** The census's own numbers reproduce on the same
binary at form=0 (201.1 / 199.5 candidates at 10⁴ / 10⁵, zero bails): the O(1) verdict is a property of
the ladder's population (locals capped at 300, none in the player's band, the belt in another doll), not
of the filter. [20261017-0739: the tier beside a 10⁵ belt is off (0 bails, 387 candidates) — the "200
ships" crossing is population-pair-dependent, as 0552's checker measured.] [396d: the seam flight — the
player itself inside the belt's band — is now flown; see Current best. The 0552 crossing (200 ships
beside a belt switching the scans to walks) and the seam are the same law read from two sides: the
registration's width defeats the 1-D filter at the population's own band.] Fixes to price: the bail's
numerator in bodies (dedup) and its threshold local to the window's population; a phase axis for
co-orbital crowds (taleb-09b5's rank-along-orbit invariant, the encounters gold, applied to the
observer); the comb channel is kick-cadence's.

Provenance (checker): the plane-scale fallback and the `bodies/4 + 64` mechanism are scan-queue's
priors (cdf0 20261016-1120: Home's doll trips the N-relative rule exactly at the plane's flown N,
95% of coast captures; 3999: the belt-band every-N disease) — this run's new content is the
co-orbital formation itself (the page's named unflown direction), the 1.00/ship crowd law, the
coast window covering every radius with a bin-entry numerator, so the bail never turns off under
concentration (100% still at 10⁴ in-band bodies, checker — cdf0's "small-N disease" scoping
corrected), the c439 inversion, and the frame cost. [20261017-0739 adds the per-frame channel
decomposition and the ranking.]

Prior best retained: **the read stream is censused on shipped code and the 10⁹ premise is corrected: the engine's
read demand is O(1) in N on the ladder's flights — every reader's absolute count identical
at N=1e4 and 1e5 (scan candidates 148,996 at both; totals 188,181 vs 188,227) — the player's
scan reads a bounded near set (70.0 candidates a scan at burn, 184 at coast's wider window;
the radial apsidal filter cuts the belt), and the only N-linear reads ride the kick cadence
at 2.9–4.3 reads an event (state_of 0.9–1.6 + root_state_raw 1.4–1.8 + rec 0.6–0.9;
misses 0, history hits ≤4.3%) (20261017-0428-quant-c439, `prof::reads` census behind the
prof feature, digest-identical plain vs prof `d1822b88…`, regen.sh).** So the "~6 cores of
pure hit-path ε (lock+clone)" never materializes as an observer demand: at 10⁹ rtf 100 the
observer reads are ~7.7×10³/s and the event-riding reads between ~4×10³/s and ~10⁷/s
(≤ ~1 core at the measured 67–129 ns a `binding_at`, 192 B; rec 114–167 ns, 464 B) — a
term of the kick bill (kick-cadence's, ladder break 1), not a separate knee. The ~7×10⁶/s
figure is the wave-window per-body extrapolation (checker2: events themselves are O(1) in
N over 20 s windows — 16,212/16,215/16,215 at 1e4/1e5/1e6 — and grow only ~2.4× a decade
through the wave, 65,154→155,092 events 1e4→1e5, so no per-body × 10⁹ term exists on
these flights; checker2's wave arm at 1e5: 4.70 reads an event). 8792's b = 11.48
reads/body/20k gs
reconciles as the kicks' own mint-path reads (~3.9 kicks/body in that window × ~4.3), which
an N-linear counter records when a mint counts as a read. The dwell cliff's hot set is,
as an inference (never flown together: the census runs on main, the cliff on 8792's
retention patch), the scan's near set (~70 bodies read at ~1.1 scans/gs at burn, 88 on
seed 2 — checker; 144 on seed 3 at coast and 70.2 at N=1e6, O(1) a decade up — checker2;
clustered in bursts): a pin of the near set is the proposed deletion
of the cliff's observer half, unflown, and the set's size is realisation-dependent.
Domain: the ladder's
flights (player near Home / the root doll at 1 AU, seed 1, 1 thread); a flight into the
belt at density (radial returns None, the player seam) and the page's per-frame O(N) view
gather are outside it. [396d: the seam is inside it now — flown, see Current best.]

Prior best retained: the standalone mint+demote measured on the flown store — 3.7–5.3 µs
p50 (mint = the compile: 3.7–4.7 on seam/retain/100/1000, 5.2–5.6 on the re-mint-storm arm
dwell-17 burn 10⁵; demote = the Arc drop, 0.04–0.08), across coast and burn, four dwell
classes and two N — the ledger's CPU half holds with ≥4.4× margin against the 23.1 µs
4-core budget at 10⁹ rtf 100 (composed ÷8+delete = 0.78–0.85 cores; ÷8 alone = 2.0–2.2, so
cadence alone meets the mint budget), and its 44 µs bind/refit pricing is corrected: the
settle hands the promotion an exact key, so the promotion never refits — b29a's 21 µs
`from_state` is the kick's own settle bill, already inside the kick Ĉ (b063). The memory
half is coast-scoped: the dwell dial (`ES_RETAIN_DWELL`) collapses coast's standing resident
100,819→288–329 at +1% re-mints, N-independent — but on burn it fails at 10⁹ as stated
below (8792; 24 flights, one frozen binary, digests bit for bit; anchors regenerate
exactly: 131,053/763,888/100,788,130,187). The re-ranking stands, sharpened: diet = 10⁶
lever; ÷8 = the mint-budget lever; delete = the event-stream lever; burn-10⁹ memory = the
kick cadence's mint bill plus bytes/body, no separate read-stream term.

## Refuted
- **"The shipped answer on a rigid keys fleet is empty" (b083's checker's idealization, and
  b083's caveat iii read hopefully)**: flown, the answer is a residual (a scene-dependent
  fraction of the window — 47–53% on the author's rings, 19% at K=3·10⁴, 50% at e = 0.3,
  checker2) and the residual is not stable — 15→31→12 across quarter-period decode points on a
  constant window of 32 (10→32→0 at e = 0.3, 18→66→12 at K=3·10⁴); the exact tier reads
  the window, never ~0 (20261018-0722-second-…-5f36).
- **"The per-orbit-class capability curve C(δ) + shear drift is a sound selector"** (b083's
  e > 0 form): misses up to 9% of hits at e = 0.1–0.2, σ_a ≥ 1e-5 — the approaching conjunct's
  window edge moves under the Δa-shear near apsides; the sound form is the 2D curve C(δ, Δa),
  0 misses over the full sweep (20261018-0722-second-…-5f36).
- **"The observer half is free / pin the ~70-body near set" (this page's own open direction 1, and
  the census's c439 reading)**: on the game's own crowd the near set is crowd-proportional (1.00
  candidates a ship), the filter bails on 100% of the plane's own scans, and at K=1,000 one answer
  is 4.53 ms — the observer alone is ~500× over at rtf 100 for a 10⁶-ship fleet
  (20261017-0552-inversion-604c). [20261017-0739: the observer's own bill stands, but the frame's
  ruin is not its — the over-budget frames are 98.5% comb on both seeds; see Current best.]
- **"The radial apsidal filter cuts the belt" (c439's letter, as a property of the filter)**: at
  coast the window covers every radius from zero (reach ≈ 9·r); what cuts the belt is the doll
  partition, and the filter's own viability hangs on the belt inflating the bail's denominator —
  at plane scale it bails always (20261017-0552-inversion-604c). [396d, stronger and flown: at
  the population's own band the filter bails on every scan for the belt's whole registered hull —
  the e-smear, not the window's width, sets the zone (20261019-1452-spacex-396d).]
- **"The burn read stream is an N-linear observer demand at 10⁹"** (8792's open direction 1
  as stated, "~6 cores of hit-path ε"): on shipped main the engine's read demand is O(1) in
  N on the ladder's flights — identical absolute counts 1e4↔1e5, 70 candidates a scan — and
  the N-linear reads are the kicks' own (4.3 an event through the wave), i.e. the mint bill
  the cadence owns (20261017-0428-quant-c439).
- **"The seam's cost lands on the frame at ladder K" (396d's own pre-registered P3/P4)**: at
  10⁴ and 3×10⁴ the walk zone's frames stay inside the 12 ms budget (answers drain into idle
  room at p50 0.024 ms); the over frames are the root's boundary wave, and the ratchet's
  MB/held slope is K-independent (2.23/2.07 MB) where the walk candidates differ 3× — the
  seam is a these-rungs per-item tax (167–214 ns × N per player item) and a 10⁶-frame
  extrapolation must price the answer channel (~4.4 µs × N), not the observed frames
  (20261019-1452-spacex-396d).
- **"The smallest promotion is a byte question"** (the board's framing under nladder):
  bytes only buy dwell headroom; the binding terms are dwell (memory) and mint cost
  (CPU) (20261016-2327-library-cbc5).
- **"The record diet moves 10⁹"**: it moves the 10⁶ ladder wall (its 75–615× is real
  there); at 10⁹ the diet only lifts dwell* — CPU is unchanged, and CPU is the bind
  (20261016-2327-library-cbc5).
- **"Mint+demote = 84% of kick cost (44 µs)"** — the ledger's pricing: the promotion on
  the flown store never refits (the settle's key is exact), so mint+demote = compile + Arc
  drop = 3.7–5.3 µs measured; the refit is inside the kick bill, and pricing it again
  on the promotion side double-counts (20261017-0005-…-8792).
- **"Dwell is the memory dial at 10⁹"** as stated: coast-true, burn-false — the miss cliff
  (73%→14% between dwell 17 and 100) is real but its owner is now named: the scan's ~70-body
  near set read in bursts (the observer half) plus the kick mints (the cadence half); with
  the near set pinned, what's left of the cliff is the cadence's
  (20261017-0005-…-8792; c439). [20261017-0552: the "near set pinned" clause is
  crowd-scoped — under a formation the set is K-sized, not 70.]
- **"A phase/along-orbit axis makes fleet scenes cheap for the scan" (this page's od 1b,
  the candidate-side reading): measured wrong at coast and unnecessary — the window
  contains the ring and the radial representation is degenerate on it (candidates =
  1.00·K at every horizon for circular formations; eccentric rings are cut only at
  burn-class windows, 0.15% at e = 0.5); the cheap answer is the offset compare, not a
  shorter candidate list (20261018-0431-scout-b083).**
- **"The observer's crowd bill needs a new index" (any candidate-side structure): the
  shipped predicate's own geometry (d ⊥ w on a shared circular orbit) already carries the
  read list per member in one compare on the stored phase word (the answer adds the
  approaching conjunct d·w < 0 — empty on a rigid ring, checker); the index is the store's
  existing class-major layout (calendar od 3) (20261018-0431-scout-b083).**

## Open directions
1. **The scan's representation under concentration** (this run's handback): price (a) the bail made
   local (numerator in bodies — dedup the bin-entries — and threshold against the window's own
   population, not the universe's `bodies/4`), and (b) a phase/along-orbit axis for co-orbital
   crowds (taleb-09b5's invariant on the observer's side), which is the only representation that
   makes fleet scenes cheap for the scan; measure both against this run's matrix (regen.sh). The
   old "pin the near set" is refuted above; the player-seam flight (into the belt at density,
   radial None) stays unflown. [20261017-0739 ranks it: the phase axis is the observer's own bill
   (mean share ~10% at K ≤ 1,000, the pin 51-93 MB above the latch), second to the comb's cadence
   for the frame's tail.] [396d: the seam is flown — see Current best; the flight prices (a) as
   insufficient at the band (the hull's bin-entries are ~N at ANY local threshold once e smears
   the registration: the zone's bail is honest work for a 1-D index, and the fix is (b), the
   phase compare, or an e-graded registration that bins by periapsis-class rather than the hull).
   Unflown now: the seam's answer channel at 10⁵-10⁶ (frame ruin by arithmetic, ~4.4 µs × N a
   scan), and the seam under a cold (e ≈ 0) population, where the zone should collapse to the
   band.]
2. The comb channel of the formation scene (1,000 ships at one period: 128 events a frame, p99
   52.5 ms) is kick-cadence's page, not this one; the formation matrix is the ready instrument.
   [20261017-0739: the comb owns the over-budget frames (91.7-99.7% at K = 200-10⁴, and 95.1% at
   2×10⁴ — checker2) — the cadence fix (de-phased births) is the frame's first; the interaction
   (de-phased waves moving work into the quiet frames where the answers drain) is unmeasured.
   Checker2: rtf 25 does not de-phase the wave — the worst frame still resolves all ev=1002 in
   one frame (comb 54.1 ms) and only the over count drops (68→21), so the de-phasing must come
   from the births'/cadence phase, not from the time knob.]
3. Cliff position, seed stability and N-linearity are flown (checkers: cliff between 80
and 100 gs with miss 72–75% flat from dwell 5 through 80; seed 2 within 6% and seed 3 at
14.0% on the cliff's right side, digest-identical to its own ctl; reads linear at 2×10⁵
to 0.13%). The coast dial saturates at ~N beyond ~2000 gs (dwell 10000: standing
115,276 ≈ N, re-mints exactly 1.00× retain's — checker2). Remaining: the formation scene's
dwell behaviour (the burst scale the cliff hangs on is now measured crowd-proportional, so
the cliff's observer half is a fleet term — unflown together) and the sub-frame dwell class.
4. ES_SECULAR's promotion-skip coverage (1a46) prices the event stream only — its effect
   on the read stream is unmeasured.
5. The stagger's recurrence gate (≥3 intervals, the unprinted second spell,
   9e75-checker2) before idle-time compute-ahead is considered at all.

## Contradictions
Resolved by 8792: 0619's burn knee vs the ledger's λ×dwell identity (different
instruments; the standing resident is burst-structured, not λ×dwell). Reconciled by c439:
8792's b = 11.48 reads/body/20k gs is the mint-path reads riding ~3.9 kicks/body, not
observer re-reads — their N-linearity and the census's O(1) observers measure the same
flight's two halves. Standing watch: the ledger's P6 cell (diet at shipped rate binds
memory for dwell ∈ (2,808, 28,141] gs) is coast-only. New, named: c439's "70 candidates a
scan" and this run's "crowd-proportional, bail always at plane scale" measure the same
filter on different populations — reconciled above (the cap and the belt's denominator), no
live conflict. Resolved by 20261017-0739: 0552's P5 mechanism (a 4.5-ms answer forced into a
frame by SCAN_BACKLOG) against the measurement — SCAN_BACKLOG never fires (held_max ≤ 71
of 2,048); below 69f3's latch the answers drain into quiet frames' idle room, above it they
freeze and pin. The frame's over-budget tail is comb-owned on both seeds. New (396d), carried
as a domain note, not a conflict: 0552's "200 ships beside a 10⁴ belt switch the scans to
full walks" and 396d's "no over frames from the seam's own walks at 10⁴-3×10⁴" measure
different channels of the same bail (0552: the candidate/answer bill in a formation's tight
frames; 396d: the capture bill in a burn's idle-rich frames) — the bail's cost is
frame-context-dependent, the bail itself is not.

## Runs
- 20261014-0450-scout-b29a (silver, prior art on nladder, uncited by the ledger):
- 20261015-0250-scout-760f (silver, prior art, uncited): promotion = one 4.6 µs
- 20261015-1926-quant-c4d3 (silver, prior art, uncited): shipped `add_body` promotion
- 20261015-1338-quant-1d52 … 0757, and 20261015-1615-quant-0619 (prior art, uncited):
- 20261016-2327-library-cbc5 (library, this run): promotion ledger — dwell is the memory
- 20261014-0450-scout-b29a (silver, prior art on nladder): the smallest promotion
- 20261015-0250-scout-760f (silver): promotion = one 4.6 µs compile, bit-identical
- 20261015-1926-quant-c4d3 (silver): shipped `add_body` promotion path 9.2 µs p50, flat
- 20261015-1338-quant-1d52 … 0757, and 20261015-1615-quant-0619: demotion/retention built
- 20261016-2327-library-cbc5 (library, silver): promotion ledger — dwell is the memory
- 20261017-0005-second-20261016-2327-library-cbc5-8792 (second author, this run): the
- 20261017-0428-quant-c439 (this run): the read census — read demand O(1) in N (counts
- 20261017-0552-inversion-604c (this run): the formation scene flown — the filter bails on
- 20261017-0739-second-20261017-0552-inversion-604c-2e42 (this run, second author): the
- 20261018-0431-scout-b083 (scout, awaiting grade): the phase axis lands on the answer
- 20261018-0722-second-20261018-0431-scout-b083-5f36 (second author): the tier
- 20261019-1452-spacex-396d (spacex, awaiting grade): the player-seam flown — walks = N over the
  belt's registered hull (1.6-5.2 AU, the e-smear), 167-214 ns a walked body, no seam-owned over
  frames at 10⁴-3×10⁴, the ratchet's MB/held slope K-independent (candidates excluded).
