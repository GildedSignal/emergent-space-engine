topic: memory-h-live
status: open
closed-by:
valid-while:
updated: 20261017-1330-library-7bd9

# Memory at 10⁹ in 8 GB: live information per body (H_live), scars, the standing representation

## Current best

**The FLOW's growing path is attributed, and the wall's load-path pin is priced: the accumulator is the
held-scans queue, and the fence is one constant.** A 13-s flight pair on shipped code (counting GlobalAlloc
+ the two standing queue counters, `flow_attr` example; 400 members, coast, rtf 100, 3,600 frames): quiet
flat (live 14.6 MB, held_scans 0), under 6-way pinned load live_B grows 24.0→96.4 MB monotone at
**13.1 kB/gs (470f's rate)** with **held_scans 10→433 in lockstep and handouts 0 throughout** —
171 kB + 73 live allocations pinned per held scan (the capture is the candidates Vec, encounter.rs:174-195,
≈400 B/candidate by measurement — the 216 B tuple guess does not close: 428 bodies × 216 B = 92 kB — the
whole doll when the radial filter bails; the pin declines to ~90 kB/scan as the fleet dissolves:
146→88 across the record log itself, checker), so `SCAN_BACKLOG = 2048`'s force-answer is
470f's "one bulk drop of ~78k" (latch ETA 26,629 nominal gs; in presented game-s, which the load arm
undershoots ~1.3×, ≈21,000 gs at the 0.096 scans/gs two checker flights reproduce — against their
~20,000-gs drop) and the latch's bound at this scene is **2048 × 171 kB ≈ 0.35 GB** (worst, early
flight; ~0.18 GB late) — ~1.5 GB at 604c's formation candidate counts, and **not a safe fence at scale**
[checker, outside the author's 400-only range: at 1,600 members with births mid-flight the pin reaches
~2 MB/scan (93 scans, 225 MB in 1,200 frames, no same-CPU spinners) — a multi-GB count-latch bound;
`prune()` is unconditional (universe.rs:1082): 470f's prune-starvation
lead is dead; `held_scans()` (universe.rs:299) existed unread — smoothness runs track its max, no memory
instrument read the standing count. Growth is per-scan × capture, NOT per-body: at ladder scenes the
candidates are the player's doll (c439's near set, O(1) in N), so the 10⁶ headline survives with a bounded
~0.1–0.2 GB pin — a quiet-machine claim until flown under load (20261017-1330-library-7bd9, library;
one flight per arm on top of 470f's 37, quotes 5/5 byte-identical, predictions half-held as stated in
its dossier).**

**The play-time FLOW is bimodal and wall-path-dependent: peak memory is not a canonical
outcome.** At 400 fleet members the same flight (same seed, args, binary, quiet machine) either
peaks at ~44 MB or grows **~11 kB of live Rust allocations per game-second to 220.9 MB / 83,768
live allocations by 20,000 game-s, frees ~78k allocations in one bulk drop, and leaves peak RSS
at 206 MB forever** (allocator retention) — 5 of 15 quiet-machine seed-1 coast flights took the
growing path; the split is machine-load-dependent, not a coin [checker, same run: 9/9 flights
grew under 9-way concurrent load (seeds 1 and 5), 0/3 alone; second checker: 8/8 under 8-way
load, 8/8 with the counting allocator removed — not an instrument artifact — and 2/4 quiet];
every other arm was flat in
every run (both burn arms, seed-2 coast, the shipped
48-member plane over 40,000 game-s, the 3,000-body belt). Every shipped counter is flat
throughout (bodies, catalogue_live, bytes_per_body at a constant 5.9 kB/body, the stats ledger,
slices frozen; settle +0 kB; mapping count constant — the growth is live allocations in the
main heap, seen only by a counting GlobalAlloc). The trigger is the wall-budget path, not the
game state. d3fe's clean ruin rate is otherwise dead on main: fleets dissolve by ~3,000 game-s
at every size flown, the fleet-slice bill is one-time (events 17.6→~2/gs at dissolution), and
the long-lived-battle case is unreachable by growing the fleet
(20261017-0238-inversion-470f, inversion; probe `ruin_probe.rs`, the player's own loop unpaced
at rtf 100, seeds 1–3, the bench's burn script as an arm; not an 8 GB ruin at this scene — a
4.7× path-dependent multiplier on any single-run memory-wall measurement, counter-invisible
until fenced). Not 400-specific [checker]: N=100 grows ~3.9 kB/gs, N=800 ~29 kB/gs to 183 MB
RSS by 6,000 gs under load, N=1600 ~54 kB/gs to 327 MB [second checker: growth ∝ N]; the flat
path is stable flat to 60,000 gs. What reopens the clean
refutation: a checker whose fresh runs never grow.

**The standing catalogue is a cache pretending to be state, and its duplication is now measured
with controls: 99.6% under co-orbital concentration, 0.4% on the belt** (20261017-0005-system-efd4,
gold: the intern was flown by the checker — 513→2 standing on the formation, digests bit-identical).
A 512-ship formation on one orbit stands 513 entries for 2 distinct intern keys (the
duplicates are byte-identical: `Orbit::compile`/`Passage::compile` are pure in `(Unit, OrbitKey,
sense, passage edge)` — the edge is a real input, and the intern key must carry it); a
512-distinct-orbit scatter stands 513/513, and the flown plane with a 2,000-ship ladder belt stands
2,044/2,036 after 2,550 kicks. Nobody queries the plane's `Catalogue` (`get` has zero callers;
every reader holds the `Arc<Entry>`), the digest leaves slot ids out (ties.rs), and `crates/space`'s
own catalogue already interns by `(OrbitKey, bool, Option<Scalar>)` — the plane's fork kept the
free list and dropped the intern. So one structure (intern + refcount, then eviction) deletes the
per-binding mint, the creation compile (16.4 µs/ship measured) for program births on shared
orbits — the intern alone does not remove it: the mint must consult the key before fitting, which
is not yet flown — and the dead-body entries; the scattered belt's stock needs the eviction half
(5465's regenerable 58%), not the intern. The kick-CPU memo stays dead (memo.rs: exact keys never
recur on distinct kicks).

**The rate is small, measured, and not the problem.** At 10⁹ bodies H_live ≈ 21 bits/s
total: rebinds through the secondary's SOI (10.2 bits/s) co-dominant with the player
(~10 bits/s), contacts 0.9 bits/s, at Γ_SOI = 1.31×10⁻² transits/body/orbit
(20261012-1621-second-20261012-1524-fermi-4b55-09a1, gold). Ship-to-ship gravity
creates exactly zero scar bits at any belt density to 10⁹ (every ship–ship kick ≥ 9
orders below the (E,L) quantum); the only growing channels are contacts, massive-body
encounters and decisions (20261011-1600-fermi-13ad, gold), and mutual-encounter
inertia holds across instruments: δv/v ≈ (4/3)μ/b² per conjunction, so the parent
term depends only on total embedded perturber mass (20261007-0621-second-…-5e74;
20261007-0528-fermi-aab3: f_ind ≤ 0.375 at 6 GB is the gate, not the encounter
stream). On the plane itself, fired kicks run 3.55–3.64×10⁻⁵/body/game-s, invariant
in seed and N (20261008-2113-components-a9d7, gold); the integer ledger's creation
rate decays 14.8 → 0.036 bits/game-s, ~0.2 GB of scars per hour at plane density
(20261007-2344-spacex-dbf9; record repaired to regenerate by
20261008-0041-second-…-57e8, gold). The exact-vs-quantized gap is the one live
rate risk: at exact Q48 a ship writes 0.076–0.136 bits/s (40–61 GB/h at 10⁹) against
~0.0013–0.0015 at the 24-bit memo key (20261010-1947-spacex-19bc) — and holding even
the coarse side costs a measured 0.6–1.1% of a core in reabsorption duty, while the
exact side dies on CPU as well as bandwidth (0.3–1.3 cores;
20261010-2052-second-20261010-1947-spacex-19bc-d205) — and at the
tube's 32-bit angle quantum a belt writes 180.6 GB/h — the quantum must be coarser
than ~2×10⁻⁷ rad (20261012-0616-components-0e9c). The write rate itself is
geometry-split: fc22's ≤ ~1 MB per 300 h holds in 3-D only (18 KB/game); planar
belt writes run ~209 MB/game at 10⁹ at the dossier's own parameters
(20261007-0933-second-20261007-0842-fermi-fc22-a7d0, gold).

**The stock saturates by promotion level; the census, not the rate, decides 10⁹.**
Per body on the shipped store: program member 17.3–29.6 bits, first scar +70.7–76.7,
individual 149.7–196.6, re-kicks ≈ 0 — so at 4 GiB the ceiling is 9.5–12.9%
individuals (24% scarred), and the promoters are contacts and embedded masses, never
rock–rock gravity (20261008-2031-fermi-9d49, gold). A kicked body costs ~50 bits once
plus ~2 bits per further doubling (49.9 → 68.3 bits at K = 1 → 1024); the shipped
shelf stays 0.8–7 bits above that floor with bit-exact repacks; a fully-mixed
population (63 bits/body) is ≈ 7.9 GB — the first wall (20261007-0800-fermi-a91f,
gold). One chaotic scar is a stock of 40.2 bits = the analytic 2·log₂(σ/q)+4.1,
independent of kick count — law.md's "+62/−60" flow model is dead (20261007-0621-scout-6e10),
and real Jupiter-flyby kicks are chaotic for every bounded event program (0.0–4.8% of
the kick's bits recaptured; every body kicked every epoch;
20261007-0711-second-20261007-0621-scout-6e10-ab9d, gold). On the plane each
rebounded binding costs 234–252 bits and even a quiescent belt leaves 173.5–175.1
bits/binding, so the +62 is ~3× low and the −60 has no mechanism (20261009-1754-spacex-c6d8,
headline ~2.2× low, corrected by 20261009-1858-second-20261009-1754-spacex-c6d8-71bd);
the bound is the current binding, not history — a kick stream revisits its own programs
82–97%, ~15–25 bits entropy-coded (20261010-1706-fermi-2914). The scar constant is
magnitude-dependent: S = Elias–Fano ~7 b + Σ(b_c+2), 61.2 → 172.5 bits from the
shipped kick to the supra-family stress rung (20261011-0517-second-…-b3e7, gold),
giving the admission rule bits/body ≈ 1 + S·f_cum with break-even f* = 33.4/S ∈
[0.19, 0.55] (20261011-0324-fermi-c211; corrected by b3e7).

**The floor, and what busts it.** The 3-field sorted floor at 10⁹ is 61.6–62.1
bits/body = 7.70–7.77 GB — the board's "~62 bits" — but every exact non-replay
encoding must also carry the phase (t_p, 64 bits per radial cycle, uniform by
construction at 63.96 bits/sample), so the 4-field floor is 125.5–126.1 bits/body =
15.7–15.8 GB, ≈ 2× over budget; the scar form is near-optimal (+0.9 bits after the
first pass), so the wall is the tube's own quanta (20261010-1544-second-…-0820,
gold). A driven belt pays it at once: one Jovian pass scars every body, 126.4
bits/body within one orbit (20261010-1407-fermi-fc48); the plane's belt carries a
one-time ~146 bits/body (exact quanta) / ~69 (memo cell) of orientation-coupled
synodic scatter, flat after — the generator needs first-order epicyclic terms
(20261011-0517-spacex-d0ea, gold) — and no secular program absorbs it either: the
exact double-averaged twin leaves residual 108.71 of 108.77 frozen bits at 20 yr
(20261007-1106-second-20261007-1032-taleb-ab03-0263, gold); the real engine's kicked belt scars every member
within half an orbit and never reabsorbs, ~130 bits/member ≈ 16 B at law widths, and
shipmem's Form P dies as a family representation the moment a member is kicked
(20261007-1646-quant-b30e, gold). The escape is measured: re-fit the generator AND
canonically relabel unobserved bodies — re-fit alone bounds nothing (42/42
checkpoints; label cost → 0) — giving a law-robust floor of 1.80–1.83 bits/column at
2.6×10⁵ knots, 4.26–4.30 bits/body at lab N (20261011-0134-second-…-fdfc;
20261011-0006-fermi-2a9d); a re-programmed synthetic belt is statistically
indistinguishable from the true one (KS(a) 0.031, p = 0.29; 20261008-0041-fermi-8072,
gold), which reconciles b30e (no re-programming: ~130 bits/member busts) with 8072
(legal re-programming: tens of MB). Self-stirred belts never get there: escape needs
a median 158–420 sub-quantum kicks (98–100% multi-kick) under real conjunction
geometry, t_sat ≈ (Q/σ_s)² orbits, so a real 10⁹ belt never scars and stands at
1.7–2.4 B/live-body, inside B18 (20261012-0616-second-…-07b4, gold;
20261012-0616-scout-d0a9); and at the law's own quanta no recompilation cadence
rescues the driven belt — 45–76 bits/body residual against the 34.4 budget at every
cadence and program class, restored only by per-population quanta 256× coarser
(2,560 km → 33.2 bits; 6759's "1 km" quantum was in fact 10 km;
20261012-0358-second-20261012-0311-scout-6759-0ae6, gold); the growth that does exist is diffusive, σ ∝ t^0.55,
flat in N at fixed belt mass, and the storage quantum is the lever (−13 bits per
decade of coarsening; 20261010-1544-components-986b, gold) — the ½·log₂ family
(20261008-1337-fermi-ab86; 20261009-1556-fermi-8fb8: ½ per identity-tied column, ¼
interchangeable, f_tie the knob; 20261008-1150-components-4b84: the periapsis-time
axis, ~1.5·log₂t; 20261010-0814-dynamics-740f: ~3 bits per kick doubling;
20261010-1152-fermi-e9a5: ~1 bit per time-octave; 20261010-1302-second-…-a9c4, gold:
a cold belt stands at 41.7 bits = 5.2 GB at 2 dof, only concentrated 3-dof regions
break; 20261011-0006-second-…-2b8e, gold: a synodic-aware program absorbs all but
0.55 events/ship/P_p, mature footprint 20.7–22.1 bits/ship).

**The standing representation is the shipped-code villain.** On the shipped plane the
live stock is 1,245–1,277 B per belt body (4,665 B/body flown): `Catalogue::insert`
never dedups compiled trajectories — 2,000 ships on one orbit hold 2,000 entries —
plus a 448 B record and a mandatory 192 B history segment; even at the law's floor
widths a billion individual records are 14–18 GB, so the billion must be population
programs (20261007-0711-spacex-cae7, gold). A median ship stands at ~1.46 KB = 90×
the law's 16-byte tube (448 B `BodyRec` + ~530–970 B of resident compiled
quadrature); 10⁹ costs ~1.4 TB ≈ 175× over — evictable shared shapes and out-of-line
records, not a better prune (20261009-0401-spacex-4a62, gold). Scene spread: 9,846
B/body stored with compiled shapes (20261007-1106-fermi-443e), ~7 KB/body = 428–446×
the tube, the biggest lever on the board (20261009-2212-fermi-a11b), 2.3 KB/orbiter
and 5.0 KB/battle member with whales = re-minted generators, retained segments,
never-freed corpses (20261010-0306-quant-4985), commit path 660 B per ~60-bit kick
(88×; 20261008-0148-components-df14), packed live state itself only 448–454 bits =
56.0–56.8 B vs 672 B stored (20261009-2348-components-42e6) — a 75–615× spread over
the 16 B tube. One doll body stands at 5,186 B = 324× the tube, 58% of it compiled
knots proven regenerable bit-identically from the exact key (a cache, not state) and
29% the view's retired history (20261012-0311-components-5465). At 4,000 members the
plane's 845 MB is unpruned rebind history — ~10 kB per ship kick, `settle` bypassing
the every-64-frames prune — on a true construction marginal of ~19 kB per handed-out
body (~33 kB/body post-prune steady; the dashboard under-reports ~20×;
20261012-1019-spacex-3463, decomposed by
20261012-1117-second-20261012-1019-spacex-3463-c304, gold). The event queue needs no
container (a counting scan at 8 B/body against the heap's 16 B + slack;
20261011-2028-components-6a0e), and the encounters crate's second per-body copy
(~96 GB at 10⁹) deletes onto the tube store itself (20261011-2028-system-3b42).
The one unbounded grower is the compiled-cycle catalogue, and it is a
churn leak (one entry per ship ever created; 20261011-2235-second-…-e4cc, gold;
20261011-2132-spacex-91a0), with H_live itself saturating despite continuous kicks
(fleet 17.8–22.3 bits/member, ships 45.5–49.9 bits/ship, second-half slopes ≈ 0).
A reachable ruin state was claimed: peak RSS grows ~0.2 kB per surviving member per
game-second through any battle that stays live, and both instruments were blind to
it (20261006-0030-taleb-d3fe, silver) [re-measured 20261017-0238-inversion-470f: the rate as
stated is dead at shipped size, but a stochastic wall-path-dependent growth of the same kind
survives at 400 members — see Current best].

**What binds at 10⁹ is regime-dependent, and both gold verdicts stand.** The hot
side is two per-body terms: 6.9 KB live per hot body with N_hot ≈ 1.3–2.7×10⁴ at
rtf 100, cold populations free by horizon (20261009-2257-second-20261009-2212-fermi-a11b-ba64,
gold; the board's 190 cores re-derives as 175). At the
short-orbit corner (90-min orbits, 32.5 kicks/orbit) compute binds first: 153 cores
averaged at RTF 100, S_live capped at 5.2×10⁷ by compute vs 5.4×10⁸ by memory
(20261006-1354-fermi-c9fa, gold — frame-cost topic). At belt scale memory capacity
binds: the tube store plus any per-body event queue is already 3.2× over the usable
5 GB while compute clears by 3–5 orders once the two measured levers (kick-setup
12.5×, tide averaging 114×) are applied (20261011-1917-fermi-b946, gold). The
ordering compute (short-orbit) ≫ memory (admission at f_cum ≥ 0.19–0.55) ≫ H_live ≫
bandwidth is measured at the 81-min corner (20261011-0517-second-…-b3e7, gold;
20261010-0448-fermi-71b2: the wall is regime-dependent, not N; 20261010-0352-spacex-2dca
and 20261010-1152-fermi-e9a5: at the 1× belt, churn/CPU, four orders of margin) —
first seen as compute ≫ H_live ≫ bandwidth with the affordable hot fraction 5–10%
at rtf 1 (0.05–0.1% at rtf 100) and reabsorption ≥ 37–292 MB/game-s at 10⁹
(20261007-1843-fermi-1feb). The contact channel is the exception that can ruin a
close-in belt: 4 GiB in 9–18
play-hours for immortal ships unless contacts are terminal or herds re-program
(20261011-1600-fermi-13ad, gold).

**Domain.** 2D belts (B18b-family geometry), plane scenes 28–2,112 ships, exact-Kepler
toy engines to 10⁶ bodies, settles to 512 orbits and horizons to 71 kyr; rates are
seed- and N-checked where stated. NOT tested: k > 1 secondaries (rebind rate scales
×k), inclined belts (lower density — rates here are upper bounds), gameplay that
holds ships inside SOIs, contact recycling at real rates, 3D, and the dense order
beyond the plane's battle. The 128 bits/rebind and ~10 bits/s player are stated
assumptions, not measurements; they bound H_live between roughly 11 and 100 bits/s
at the measured Γ_SOI. Both cross-instruments for Γ_SOI are cold-belt-only; only the
brute-force counter carries it across regimes (checker, 12 October). m_crit is now
measured at three quanta: c7eb's ≈ 8×10⁻¹⁹ M☉ (500-m rock, (E,L) quantum) was
corrected 16× up to ≈ 1.3×10⁻¹⁷ M☉ (1.3-km rock) by its checker
(20261009-1345-second-20261009-1259-fermi-c7eb-46a6, gold), which also finds no mass
threshold protects tp-identity — but a phase tick is 1.9×10⁷ per player pixel, so
consumers, not belt self-evolution, set H_live (~0.2 distinctions/s at 10⁹ over
1.7×10⁴ orbits); mutual-encounter distinctions begin only above μ_b ≈ 1.7×10⁻¹⁸ M☉
(~1-km rock; 20261010-1816-components-6273); ≈ 4.3×10¹⁸ kg at the scar quantum
(√2-corrected from 4b55's 3.0×10¹⁸ by 20261012-1621-second-…-09a1). All make ship-mass mutual encounters inert. The mixed-population entropy after repopulation (0.126 → ~30
bits/body, ceiling ~3.75 GB) is still a bracket, not a measurement — `b-h-live`'s
job; repopulation is load-bearing: scattered singletons saturate the store in
1/Γ_SOI ≈ 76 orbits ≈ 400 game-years and never re-smooth on their own
(20261012-1621-second-…-09a1).

## Refuted

- **470f's "prune starvation" mechanism lead, and universe.rs:77's "about 10 KB each" for a held scan**:
  prune is unconditional (universe.rs:1082); the accumulator is the held-scans queue, and the measured pin
  is 171 kB/scan on the 400-member plane (capture ≈ population × ~400 B by measurement — the 216 B tuple
  guess does not close — declining to ~90 kB as the fleet dissolves; 20261017-1330-library-7bd9, checker).
- **"The growth is counter-invisible" as a missing counter**: `held_scans()` existed (universe.rs:299);
  no memory instrument or stats line read it — an instrumentation gap, closed by one print
  (20261017-1330-library-7bd9).
- "A reachable ruin state: peak RSS grows ~0.2 kB per surviving member per game-second
  through any battle that stays live" (d3fe, silver): at shipped size (48 members) and on the
  belt plane, dead on main at 4–7× the flown horizon — fleets dissolve by ~3,000 game-s, the
  slice bill is one-time, RSS +0.001 kB/gs over 40,000 game-s in every flat run. NOT refuted as
  a class: 5-of-15 runs at 400 members grow ~11 kB/gs of live allocations to a 221 MB peak
  (bulk-freed at 20,000 gs, peak RSS retained) with every shipped counter flat, trigger
  wall-path, un-isolated (20261017-0238-inversion-470f).

- "H_live at 10⁹ ≈ 5×10³ bits/s with rebinds 36.5/s and the player nil" — a 10³
  text slip on a 2.2× sign-flipped-Newton bug; truth 0.0798 rebinds/s, player
  co-dominant (20261012-1621-second-20261012-1524-fermi-4b55-09a1).
- Per-ship scarring by mutual encounters at ship mass: δv per encounter ~10⁻¹⁷ v_K
  against q_v = 10⁻⁵, twelve orders of margin (20261012-1524-fermi-4b55, P4,
  reproduced by its checker); exactly zero gravitational scar bits to 10⁹ density
  (20261011-1600-fermi-13ad, gold).
- Counting encounter-certificate events as H_live: overstates by ~5 orders
  (20261012-1524-fermi-4b55, decomposition).
- law.md's "+62 bits per kick, −60 per reabsorption" as a flow: a scar is a bounded
  stock (40.2 bits = 2·log₂(σ/q)+4.1, independent of kick count, 33× overcount at 24
  kicks; 20261007-0621-scout-6e10; ~2× optimistic on the plane,
  20261009-1754-spacex-c6d8).
- "Distinctions per game-second ≈ event rate": the ~6×10⁴ kicks/game-second create
  ≈ 0 bits; re-kicks are free (20261008-2031-fermi-9d49, gold;
  20261008-2113-components-a9d7, gold).
- The uniform-tube memory plan: fully-mixed ≈ 7.9 GB at 63 bits/body
  (20261007-0800-fermi-a91f); the flat 16-B tube store alone is 14.9 GiB = 1.9× over
  (20261009-1259-fermi-c7eb); the exact 4-field floor 15.7 GB ≈ 2× over
  (20261010-1544-second-…-0820, gold).
- "History is never reabsorbed; live state grows ~4 B/body/game-second and fills
  8 GB in ~2 game-s" (20261008-2206-spacex-d031, lead): the plane's light-cone prune
  reaches steady state, creation = reabsorption (20261007-0711-spacex-cae7;
  20261009-0401-spacex-4a62; 20261011-2235-second-…-e4cc, golds).
- fc22's "H_live writes ≤ ~1 MB per 300 h" for planar belts — every belt the
  engine ships: ~209 MB/game at 10⁹, ~200× (holds in 3-D at 18 KB/game;
  20261007-0933-second-20261007-0842-fermi-fc22-a7d0, gold).
- 6759's "~67 bits after one orbit at 1 km quanta": the quantum was 10 km
  (Q_A = 6.6846×10⁻⁸ AU); the headline was 10× optimistic
  (20261012-0358-second-…-0ae6, gold).
- d80d's "99.9% of a weak-drive resonance belt is program-regenerable": a horizon
  artifact; 1.8% depart permanently at ~40 bits each
  (20261012-1438-second-…-b2fd).
- 3463's "marginal memory ~330 kB per handed-out body, growing with body count":
  unpruned rebind history (~10 kB/ship-kick) on a ~19 kB construction marginal
  (20261012-1117-second-…-c304, gold).
- "The secular program absorbs the belt's drift": the exact double-averaged twin
  explains none of it (residual 108.71 of 108.77 bits at 20 yr;
  20261007-1106-second-…-0263, gold).
- Return-based scar reabsorption as the balancer: 10⁻⁶ of creation; the layer grows
  only log in t (20261006-1029-components-21c3).

## Open directions

1. **Shrink and share the standing record** — the measured 75–615× lever on shipped
   code: catalogue dedup, evictable/shared compiled shapes, out-of-line records,
   free the whales (20261007-0711-spacex-cae7; 20261009-0401-spacex-4a62;
   20261009-2212-fermi-a11b; 20261010-0306-quant-4985; 20261009-2348-components-42e6;
   20261011-2235-second-…-e4cc; 20261012-0311-components-5465: 58% is a regenerable
   cache; 20261012-1117-second-…-c304: prune the rebind history `settle` bypasses;
   20261011-2028-components-6a0e: queue at 8 B/body, no container;
   20261011-2028-system-3b42: delete the encounters copy). Would change: 10⁹ fits
   with no law change.
2. **The requantization law, phase anchored, plus epicyclic generator terms** —
   deletes the 64-bit/radial-cycle phase dof and the one-time 146-bit synodic
   scatter; sets q_v ≳ 10⁻⁶ v_K and the angle quantum ≥ ~2×10⁻⁷ rad
   (20261010-1544-second-…-0820; 20261011-0517-spacex-d0ea; 20261007-0842-fermi-fc22;
   20261012-0616-components-0e9c; 20261010-0306-spacex-acb2;
   20261010-1544-components-986b; 20261012-0358-second-…-0ae6: per-population quanta
   256× coarser restore the budget). Would change: the 4-field floor 15.7 GB → under
   budget.
3. **Wire the promotion census and the admission rule** — f_cum/promotion counters,
   S by kick magnitude, f* ∈ [0.19, 0.55], re-fit + canonical relabelling
   (20261008-2031-fermi-9d49; 20261011-0324-fermi-c211;
   20261011-0517-second-…-b3e7; 20261011-0134-second-…-fdfc;
   20261008-0041-fermi-8072). Would change: 10⁹ becomes a budget identity; the
   `b-h-live` dashboard gets its counters.
4. **The mixed-population entropy after repopulation** (0.126 → ~30 bits/body): the
   only 8 GB-scale term; `b-h-live` is queued for it
   (20261012-1621-second-…-09a1; 20261004-1525-components-98bc for the 0.126 anchor).
5. **The secondary census** (k, μ distribution): sets the rebind prefactor and the
   rebind/player balance; unmeasured (20261012-1621-second-…-09a1).
6. **m_crit transition and contact recycling:** map ~10¹²–10¹⁸ kg by quantum — two
   interior points now measured, μ_b ≈ 1.7×10⁻¹⁸ M☉ (~1 km; 20261010-1816-components-6273)
   and ≈ 1.3×10⁻¹⁷ M☉ (~1.3 km, c7eb corrected; 20261009-1345-second-…-46a6, gold)
   — plus the tp channel (no mass threshold; 20261009-1345-second-…-46a6);
   make contacts terminal or
   herd-re-programming legal before a close-in belt's 9–18 h ruin
   (20261011-1600-fermi-13ad, gold; 20261008-2031-fermi-9d49, gold).

## Contradictions

None open among graded runs. The apparent conflicts resolve by regime or drive, each
in the record: compute-bound (20261006-1354-fermi-c9fa, 90-min corner) vs
memory-bound (20261011-1917-fermi-b946, belt scale) — the ordering is measured in
20261011-0517-second-…-b3e7; self-stirred never scars
(20261012-0616-second-…-07b4) vs giant-driven scars ~100% once
(20261007-1646-quant-b30e; 20261010-1407-fermi-fc48; 20261007-1334-quant-7334);
no-re-programming busts at ~130 bits/member (20261007-1646-quant-b30e) vs legal
re-programming holds (20261008-0041-fermi-8072). The 4b55 silver's three mutually
inconsistent headline values (42,462 / 4.7×10³ / 4.7 bits/s) were reconciled to one
code path (`soi_truth.py`, 21.1 bits/s; 20261012-1621-second-…-09a1).

## Runs
- 20261012-1524-fermi-4b55 (silver): H_live term decomposition — rebinds,
- 20261012-1621-second-20261012-1524-fermi-4b55-09a1 (this run): named
- 20261006-0030-taleb-d3fe (silver): plane RSS grows ~0.2 kB per surviving member per game-second through a live battle; ruin reachable, instruments blind.
- 20261006-0437-fermi-c26d (silver): belt floor is a heating trajectory, ~92 bits/body by 10 Gyr; the phase column pins ~20 bits within 1.3×10⁴ orbits.
- 20261006-1029-components-21c3 (silver): scar layer grows only log in t; return-based reabsorption dead (10⁻⁶); two-tier store 5.6 bits/body.
- 20261006-1101-scout-183b (silver): a scar saturates at ~one key word per body; floor 0.13 + f_x×35 bits/body.
- 20261006-1354-dynamics-04d7 (silver): the birth program dies under its own stirring; program+scars cross 16 bits/body within 11–12 orbits.
- 20261007-0128-b-h-live-1599 (missing): the b-h-live build run; its checker died on a 429, ungraded.
- 20261007-0528-fermi-aab3 (silver): 8 GB gated by individualized fraction (f_ind ≤ 0.375), not the encounter stream; ship/rock encounters ~0 bits.
- 20261007-0621-scout-6e10 (silver): law.md's +62/−60 is a flow model of a stock; one chaotic scar = 40.2 bits, kick-count-independent.
- 20261007-0621-second-20261007-0528-fermi-aab3-5e74 (silver): per-conjunction kick δv/v ≈ (4/3)μ/b²; parent H_live term depends only on M_pert.
- 20261007-0711-spacex-cae7 (gold): live stock 1,245–1,277 B/body; Catalogue::insert never dedups compiled trajectories.
- 20261007-0800-fermi-a91f (gold): kicked body ~50 bits once + ~2 per doubling; shelf near floor; fully-mixed wall ≈ 7.9 GB.
- 20261007-0842-fermi-fc22 (silver): H_live writes ≤ ~1 MB per 300 h; the breaker is uniform tube precision (2.35 TB measured).
- 20261007-0933-scout-23c8 (silver): secular scars saturate ~6 bits/body within 2 orbits, then ~0 creation; resonant and encounter regimes burstier.
- 20261007-1032-taleb-ab03 (silver): belt proper ~100 bits/body upper bound by the first averaging window; the fat tail is Giant-crossers.
- 20261007-1106-fermi-443e (silver): each binding change ~104 near-incompressible bits; stored representation 9,846 B/body.
- 20261007-1234-second-20261007-1106-fermi-443e-d57e (gold): doll binding injects 25.6–27.2 bits; handoff re-reference ~50 bits; reabsorption 1.04–1.08.
- 20261007-1334-quant-7334 (silver): Jupiter scars 100% of bodies within one orbit; scar field 22–38 bits/body, creation ~0 bits/s.
- 20261007-1334-spacex-8707 (silver): secular H_live ~10⁻³ scars/body/yr at q = 10⁻³, saturating in 5–7 sim-yr; cannot force 8 GB.
- 20261007-1420-second-20261007-1334-spacex-8707-e2a9 (gold): holds on the plane's frozen B18b sampler; refit cadence T* = 5–20 game-yr.
- 20261007-1646-quant-b30e (gold): real-engine kicked belt scars every member in half an orbit, never reabsorbs; ~130 bits/member.
- 20261007-1918-second-20261007-1843-fermi-1feb-ece4 (silver): plane kicks cost 39–56 scar bits each on the shipped Shelf; Key::darwin column space killed.
- 20261007-2002-spacex-3b99 (silver): saturation at the belt's element entropy, 39/51/63 bits/body by scar width; split by identity class.
- 20261007-2057-library-26cb (silver): quiescent belt writes 0.27 L-key changes/orbit, zero E-key; ~1.3 B/s at 10⁹.
- 20261007-2057-spacex-de6a (silver): sparse order gains 5.5–11.4 bits/s, 77% in velocity carries; a quiet 10⁹ breaks 8 GB in a game-hour.
- 20261007-2155-fermi-ef1d (silver): a cold 10⁹ belt creates zero live distinctions for 2.6×10⁷ yr; distinctions come from chaos.
- 20261007-2155-second-20261007-2057-spacex-de6a-3ce2 (gold): dense order instrumented at both funnels; record regenerates; H_live horizon-invariant.
- 20261007-2344-spacex-dbf9 (silver): integer ledger creation falls 14.8 → 0.036 bits/game-s; ~0.2 GB of scars per hour at 10⁹.
- 20261008-0041-fermi-8072 (gold): belt live information saturates; re-programmed synthetic belt statistically indistinguishable (KS 0.031).
- 20261008-0041-second-20261007-2344-spacex-dbf9-57e8 (gold): repairs dbf9's record; the live-ledger patch regenerates it from shipped code.
- 20261008-0148-components-df14 (silver): the commit path carries ~60 live bits per kick and writes 660 B (88× floor).
- 20261008-0458-system-5a2c (silver): Jupiter-driven shear of the key mints distinctions; birth programs die in ~10² orbits at 12-bit memo.
- 20261008-0615-second-20261008-0458-system-5a2c-af34 (silver): the reband loop converges at 3.5–4.5 bits/body; the 10⁹ belt bills ≤ 0.6 GB.
- 20261008-0945-spacex-5964 (silver): the scar's grid, not body count, decides H_live.
- 20261008-1150-components-4b84 (silver): the periapsis-time axis sets the floor, ~1.5·log₂t bits/body; refold holds 0.2–3.1 GB.
- 20261008-1252-spacex-d4e7 (silver): secular memory is a step, not a rate: naive scars ~84 bits/body; a closed-form generator holds ~0.
- 20261008-1337-fermi-ab86 (silver): distinctions grow ½·log₂(play decades); catalogue-quantum ceiling 28–38 b/b inside the 36 b/b budget.
- 20261008-1757-system-72ef (silver): perturbed-belt scar stock saturates ~64 bits/body at q = 10⁻⁶; 10⁹ needs 7.2–8.2 GB.
- 20261008-2031-fermi-9d49 (gold): H_live saturates per level; 10⁹ decided by the promotion census (≤9.5–12.9% individual at 4 GiB).
- 20261008-2113-components-a9d7 (gold): fired kicks 3.55–3.64×10⁻⁵/body/game-s, seed- and N-invariant; the rate is trivially affordable.
- 20261008-2206-spacex-d031 (lead): claimed history never reabsorbed (~4 B/body/game-s); contradicted by measured plane steady states.
- 20261009-0401-spacex-4a62 (gold): creation reabsorbed; a median ship stands at ~1.46 KB = 90× the tube; evictable shared shapes needed.
- 20261009-1210-fermi-e7a9 (silver): a carrying body holds 70–90 bits steady with 82–97% reabsorption; memory is representation width (~600×).
- 20261009-1259-fermi-c7eb (silver): the flat 16-B tube store (14.9 GiB) binds; belt encounters inert below m_crit ≈ 8×10⁻¹⁹ M☉.
- 20261009-1345-components-0e4d (silver): the cycle memo, not the bodies, busts 8 GB at the strong branch (0.44–2.0 GB at 2²⁰).
- 20261009-1345-scout-9c12 (silver): the player-influence cascade is a branching random walk absorbed at the certificate floor; bytes, not compute.
- 20261009-1504-fermi-9d3b (silver): kicked-belt distinctions saturate ≈ 61 bits/scarred body (7.6 GB at 10⁹); the lever is the residual quantum.
- 20261009-1556-fermi-8fb8 (silver): bits grow ½·log₂k identity-tied, ≈ ¼ interchangeable; the tie fraction is the knob.
- 20261009-1649-components-6b55 (silver): belt encounter rate 0.04/body/orbit, N-independent at fixed density; heavy belt scars 100%.
- 20261009-1754-spacex-c6d8 (silver): the plane creates 0.8–1.5 bits/ship/game-s (98–121 per rebounded binding); law.md's ledger ~2× optimistic.
- 20261009-2212-fermi-a11b (silver): ~7 KB live per body (428–446× the 16-B tube) is the biggest lever; cold populations free by horizon.
- 20261009-2348-components-42e6 (silver): live ship state packs to 448–454 bits (56 B) vs 672 B stored (11.8×).
- 20261010-0306-quant-4985 (silver): ledger saturates at ~2.3 KB per orbiter, ~5.0 KB per battle member; whales: re-minted generators, segments, corpses.
- 20261010-0306-spacex-acb2 (silver): the distinction rate is set by mass and velocity quantum; 10⁹ fits iff q_v ≳ 10⁻⁶ v_K.
- 20261010-0352-spacex-2dca (silver): 1.98×10⁻³ distinctions/body/orbit at the 1× belt; four orders of margin; CPU is the wall.
- 20261010-0448-fermi-71b2 (silver): the M1's wall is regime-dependent, not a body count; bench 1,203 B/body standing.
- 20261010-0814-dynamics-740f (silver): the scar layer is a logarithmic crawl (~3 bits per kick doubling); re-anchoring unneeded at play horizons.
- 20261010-1152-fermi-e9a5 (silver): the live store is log-bounded (~1 bit per time-octave); churn, not memory, binds.
- 20261010-1407-fermi-fc48 (silver): one Jovian pass scars every body: 126.4 bits/body within one orbit, then 2.95 bits/doubling.
- 20261010-1544-components-986b (gold): H_live grows diffusively (σ ∝ t^0.55, flat in N); the storage quantum, not encounter rate, is the lever.
- 20261010-1544-second-20261010-1407-fermi-fc48-0820 (gold): the exact 4-field floor is 125.5–126.1 bits/body = 15.7 GB at 10⁹ (≈2× over); phase irreducible.
- 20261010-1947-spacex-19bc (silver): 0.076–0.136 bits/s per ship at exact Q48 (40–61 GB/h at 10⁹) vs ~0.0013 quantized.
- 20261010-2314-taleb-6baf (silver): a frozen birth-key program dies in ≤ 0.4 P_p at ≥ 8 bits/axis; churn 10–14 events/ship/P_p.
- 20261011-0006-fermi-2a9d (silver): H_live bounded iff the generator is re-fit; true birth ~2 bits against the 62-bit record cost.
- 20261011-0134-second-20261011-0006-fermi-2a9d-fdfc (silver): bounded iff re-fit AND canonical relabelling; floor 1.8 bits/column, law-robust.
- 20261011-0134-components-a122 (lead): the scar layer charges ~130 bits/body for common-mode secular drift; the drift must be derived.
- 20261011-0224-spacex-e46b (lead): live information partitions by resonance distance; scarred fraction ∝ μ^(2/3); ~7+5 bits/body.
- 20261011-0324-fermi-c211 (silver): memory is an admission rule, bits/body ≈ 1 + 61·f_cum, break-even f ≈ 0.55.
- 20261011-0517-second-20261011-0324-fermi-c211-b3e7 (gold): the scar constant is magnitude-dependent (61.2 → 172.5 bits); f* ∈ [0.19, 0.55].
- 20261011-0517-spacex-d0ea (gold): one-time ~146 bits/body (exact) in the first orbit, then flat; program+scars cannot hold at current quanta.
- 20261011-1332-dynamics-8269 (silver): off resonance the proper-a is bounded; a 12.2% resonance minority carries the scar flux.
- 20261011-1600-fermi-13ad (gold): ship-to-ship gravity creates exactly zero scar bits; contacts are the only growing channel (4 GiB in 9–18 h).
- 20261011-1917-fermi-b946 (gold): at belt scale memory capacity binds (tubes + queue 3.2× over 5 GB); compute clears with measured levers.
- 20261011-2132-spacex-91a0 (silver): H_live saturates on the flying plane; the compiled-cycle catalogue is the one unbounded grower.
- 20261011-2235-second-20261011-2132-spacex-91a0-e4cc (gold): saturation holds despite continuous kicks; store-bound (≥370× over floor); the catalogue is churn.
- 20261012-0311-scout-6759 (silver): Jupiter-kicked stock ~67 bits after one orbit at 1 km quanta, ~2× the 34.4 bits/body budget.
- 20261012-0358-scout-cdac (silver): live memory follows the surprise rate; MB/h sub-linear in Γ; belt self-encounters are no risk.
- 20261012-0616-components-0e9c (silver): at the tube's 32-bit quantum a 10⁹ belt writes 180.6 GB/h; the quantum must beat ~2×10⁻⁷ rad.
- 20261012-0616-scout-d0a9 (silver): first-passage law t_sat ≈ (Q/σ_s)² orbits; a real 10⁹ belt never scars (~16 MB of programs).
- 20261012-0616-second-20261012-0358-scout-cdac-07b4 (gold): real Kepler geometry is 3–9× safer per kick; saturated belt store 1.7–2.4 B/live-body.
- 20261012-1340-scout-d80d (silver): H_live is a rate class; at weak drive 99.9% of a resonance belt is program-regenerable.
- 20261012-1524-fermi-4b55 (silver): H_live term decomposition: rebinds, contacts and the player create; mutual encounters inert at ship mass.
- 20261012-1621-second-20261012-1524-fermi-4b55-09a1 (gold): corrected the silver's broken record; Γ_SOI = 1.31×10⁻²; H_live ≈ 21 bits/s at 10⁹.
- 20261007-0711-second-20261007-0621-scout-6e10-ab9d (gold): real Jupiter-flyby kicks are chaotic for every bounded program (≤4.8% recaptured); every body kicked every epoch.
- 20261007-0933-second-20261007-0842-fermi-fc22-a7d0 (gold): fc22's ≤1 MB holds in 3-D only; planar belts (all shipped ones) write ~209 MB/game at 10⁹.
- 20261007-1106-second-20261007-1032-taleb-ab03-0263 (gold): the secular-shadow twin refutes program-absorption for the belt: residual 108.71 of 108.77 bits at 20 yr.
- 20261007-1843-fermi-1feb (silver): ordering: compute first, H_live second, bandwidth third; hot fraction 5–10% at rtf 1; reabsorption ≥37–292 MB/game-s.
- 20261007-2057-second-20261007-2002-spacex-3b99-be63 (gold): the element-entropy ceiling stands; the identity split is forced by embedded massive bodies, not the mutual walk (4.3×10¹² orbits).
- 20261009-1345-second-20261009-1259-fermi-c7eb-46a6 (gold): m_crit corrected 16× up to ≈1.3×10⁻¹⁷ M☉ (1.3-km rock); no mass threshold protects tp-identity; consumers set H_live.
- 20261009-1858-second-20261009-1754-spacex-c6d8-71bd (silver): the plane creates 234–252 bits per rebounded binding; a quiescent belt still leaves 173.5–175.1 bits/binding; +62/−60 dead.
- 20261009-2257-second-20261009-2212-fermi-a11b-ba64 (gold): 6.9 KB live per hot body; N_hot ≈ 1.3–2.7×10⁴ at rtf 100; cold populations free by horizon; 190→175 cores.
- 20261010-0352-second-20261010-0306-spacex-acb2-7b82 (silver): Λ = 0.525 ± 0.069 with error bars; q_v* = 3.8×10⁻⁷ v_K (2.8× below shipped); q=10⁻⁶ certified marginal.
- 20261010-1302-second-20261010-1152-fermi-e9a5-a9c4 (gold): log-bounded, regenerating record; cold belt 41.7 bits (5.2 GB, 2 dof); only concentrated 3-dof regions break.
- 20261010-1706-fermi-2914 (silver): ~20 bits per kick; H_live bounded by the current binding (~15–25 bits); raw residual storage ~8× over 4 GiB.
- 20261010-1816-components-6273 (silver): store cost is rate × kernel; mutual-encounter distinctions start only above a ~1-km-rock crossover mass.
- 20261010-2052-second-20261010-1947-spacex-19bc-d205 (silver): reabsorption duty measured: 0.6–1.1% of a core at the memo key; exact Q48 costs 0.3–1.3 cores — CPU death.
- 20261011-0006-second-20261010-2314-taleb-6baf-2b8e (gold): synodic-aware programs absorb all but 0.55 events/ship/P_p; mature footprint 20.7–22.1 bits/ship.
- 20261011-2028-components-6a0e (silver): the event queue needs no container: a per-frame counting scan owns 8 B/body against the heap's 16 B.
- 20261011-2028-system-3b42 (silver): the tube store sorted by (key, phase) is already the encounter index; the ~96 GB per-body copy deletes.
- 20261012-0358-second-20261012-0311-scout-6759-0ae6 (gold): no recompilation cadence saves the belt at law's quanta (45–76 bits vs 34.4); 6759's quantum was 10 km.
- 20261012-0311-components-5465 (silver): one doll body stands at 5,186 B = 324× the tube: 58% regenerable compiled knots, 29% retired view history.
- 20261012-1019-spacex-3463 (silver): marginal memory ~330 kB per handed-out body, growing with N; the dashboard under-reports ~40×.
- 20261012-1117-second-20261012-1019-spacex-3463-c304 (gold): the 845 MB at 4,000 members is unpruned rebind history (~10 kB/ship-kick; settle bypasses the prune) plus 19 kB/handout.
- 20261012-1438-second-20261012-1340-scout-d80d-b2fd (silver): twin-rates predict sealed-scar memory, not traffic; 1.8% depart permanently at ~40 bits each.
- 20261017-0005-system-efd4 (gold): standing catalogue duplication measured with controls — 99.6% co-orbital, 0.4% belt; intern+eviction is one structure; intern flown by the checker (digests bit-identical).
- 20261017-0238-inversion-470f (this run): peak memory is wall-path-dependent, not canonical: 5-of-15 flights at 400 members grow ~11 kB/gs of live allocs to a 221 MB peak (bulk-freed at 20,000 gs, RSS retained) with every shipped counter flat; shipped size and belt flat; fleets dissolve by ~3,000 gs; slices one-time.
- checker (20261017-0238-inversion-470f): reproduced 3× (regen flipped arms: 40k flat, r1+r4 grew); load is the knob — 9/9 grew under load (N=100/400/800, seeds 1/5), 0/3 alone; long-run rate 9.0 kB/gs (the ~11 is the first-6,000-gs window); prune-starvation is the open mechanism lead.
- second-checker (20261017-0238-inversion-470f): 20 of 22 fresh flights grew (8/8 under 8-way
7. **The held-scan fence (the FLOW's structural cure, one constant)**: bound the scan backlog by
   BYTES (the force-answer at 2,048 already proves answering early changes no outcome — order-preserving by
   construction), add the held_scans stats line, and freeze no wall number without the load arm
   (20261017-1330-library-7bd9; the 16-s flight pair is the cheapest load-axis instrument). At fleet scenes
   the latch bound is ~1.5 GB — this rung precedes the diet there.
- 20261017-1330-library-7bd9 (library): FLOW attributed — the held-scans queue is the accumulator (171 kB/scan, latch = the bulk drop, bound 0.35 GB here / ~1.5 GB at formations); growth is per-scan, not per-body.
