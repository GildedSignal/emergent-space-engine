# Dossier — 20261017-0552-inversion-604c (inversion lens)

**Claim.** The scan's "bounded near set" is an artifact of the ladder scenario's population, not a
property of the law: on shipped main the radial filter bails on **100% of the plane's own coast
scans** (28 bodies, no formation added), a fleet formation on the player's circle adds **1.00
candidates per ship**, and 1,000 ships there put the frame's p99 at **52.5 ms** (68/600 frames over
the 12-ms budget) with single scan answers at **4.5 ms** — the observer half of the read stream is
crowd-proportional, and the filter's on/off is decided by populations in other dolls.

**Bottleneck.** The board's top item (bodies in the flyable engine: 28 vs 10⁹) and the promotion
page's standing census ("read demand O(1) in N … the player's scan reads a bounded near set (70.0
candidates at burn, 184 at coast)"), whose own open direction 2 names the unflown scene: "a
co-orbital formation swells it". Inverted: fly the scene the O(1) verdict excluded. The verdict does
not survive it — and it was already dead on the census's own plane, unseen, because the verdict's
flights (N = 10⁴, 10⁵) sit on the protected side of the filter's bail threshold.

**Evidence** (all from `regen.sh`, Linux/x86, 8 vCPU shared, load 1.7; each flight ≤ 10 s wall;
instrument = print-only atomic counters in `radial::candidates` and `PlayerNeighbourhood::capture`
(`radial::scanstat`), census bit-identical across 3 reruns; the shipped `prof` stages time the
scan path; raw in `raw/`):

*The filter is dead on the plane itself.* At form=0, extra=0 (the shipped plane, 28 bodies + fleet
handouts): 87/87 scans bail (`hit + unbounded > bodies/4 + 64`), every capture walks the whole
universe (mean 70.6 bodies, 55.7 `binding_at` a scan). Mechanism, from the window terms: at coast
the scan interval is `h = 1.1e12` doll units and the doll's registered speed cap `9.76e-3`, so the
window half-width `reach ≈ (v + v_cap)·h = 1.11e10 ≈ 9×r` — the window floors at the `1e-30` clamp
and covers **every radius from zero** (2,108 bins ≈ 128 octaves). The numerator `hit` counts
**bin-entries, not bodies**: 1,947 mean against 71 registered (the handouts' wide tubes span
hundreds of bins each), so `hit ≫ bodies/4 + 64` whenever the universe is small — the filter
self-destructs exactly where the player lives.

*Why the census never saw it.* At extra=10⁴ and 10⁵ (the census's flights): zero bails, and the near
set is 201.1 / 199.5 candidates (186.2 / 187.1 after the doll filter) — the census's own numbers
reproduce to the digit on my binary. The bail's denominator (`self.bodies`) counts **every doll's**
registrations: the belt's 10⁴-10⁵ bodies inflate it past the numerator, so the filter stays on. The
O(1) verdict was measured entirely on that side; it is a property of the population, not the filter
— and it inverts with scale: the same plane that bails at 28 bodies passes at 10⁴.

*The formation (the game's own scene), 1:1.* Formation ships on the player's own circle (4,740 ru,
±2%, e ≤ 0.05, drawn from the seed like the ladder's): candidates/scan = 37.7 + 1.00·K — 87.7 at
K=50, 148.7 at 111, 237.7 at 200, 1,037.9 at 1,000 (max 1,044); the walk covers the whole universe
at every K (the bail never turns off at extra=0). Each candidate is a `binding_at` (capture: 382 µs
a scan at K=1,000 ≈ 0.36 µs a body) plus, in the answer, a `cartesian` + exact predicate
(**4.53 ms a scan** = 4.4 µs a candidate, `prof` "held scans answered" ns/call).

*The composition tier.* form=200 beside extra=10⁴: the formation pushes `hit` (2,594 mean) over the
belt-inflated threshold (10,271/4+64 = 2,632) — a **marginal** crossing, so the bail count wall-varies
(78/84 to 81/87 across invocations on the shared machine) but the tier is robust when it crosses:
**a 200-ship fleet switches the universe's scans back to full walks: ~9,550 `binding_at` a scan (51×
the census's 186), mean candidates 525.** At form=3,000: 100% bail, 13,056 `binding_at` and 3,338
candidates a scan, p99 **152-160 ms**, 85 frames over budget, held scans piling to 71 — the observer
alone ruins the frame at 13,028 bodies, a population the ladder flies smoothly at spread radii.

*The frame.* p99 at extra=0: 2.2 ms (K=0) → 11.7 (200, 1 frame over) → **52.5 ms (1,000, 68
frames over, worst 60.7, and the flight loses 23% of its game time)**. Two measured channels: the
scan (4.5 ms answers) and the comb — 1,000 ships born on one tick at one period fire 128 events a
frame (item kicks 2.67 ms + boundaries 1.32 ms a frame; 71,026 events vs the ladder's spread-10³
class ~7.7k, 9×) — the nladder comb at fleet scale, unregistered before this run (noted as an
observation, not a pre-registered claim).

*The 10⁹ arithmetic (orders only, from the measured constants).* A 10⁶-ship faction fleet in one
radial band: capture ≈ 0.36 s and one answer ≈ 4.4 s a scan, ~1.1 scans/game-s → at rtf 100 the
observer alone needs ~500 s of work a wall second. The promotion page's "~7.7×10³ observer reads/s
at 10⁹" becomes ~10⁷ reads/s at a 10⁵ fleet (1.1×10³× over), and each held scan pins
candidates × 216 B (216 MB at 10⁶). "Pin the ~70-body near set" pins nothing on this scene.

*Controls.* The belt controls (form=0) reproduce the census bit-class at 10⁴ and 10⁵ (above). The
census instrument is stable (3 reruns, identical `scan:` lines). Honest limits: digests are
wall-paced at rtf (flights end at different ticks), so run-to-run digest identity is not the
neutrality test; neutrality is by construction — the patch adds atomic counters only, no control
flow, no float read into logic (the diff is inspectable; `regen.sh` applies it). Flights are
pre-wave (≤ 900 game-s), coast, seed 1, 1 thread, Linux; the M1 re-measures.

**Predictions** (`predictions.md`, written before the runs): P1 (∝K, ~K+5-8) — held in effect,
wrong in mechanism: the near set grows through the bail's full walk (slope 1.0006), not a window
cut, and the intercept is ~38 (the doll's own population), not 5-8. P2 (bail first at K≈111) —
wrong in letter, right in kind: the bail is always on at extra=0 (the double-counted numerator),
and the interesting threshold is the belt-side one (K=200 re-kills it at extra=10⁴). P3 (the belt
controls O(1), no bail) — held exactly. P5's "frame stays smooth at coast" — **failed**: p99 52.5 ms
at K=1,000 (the off-critical-path design holds only while answers fit idle time's 750 µs margin; a
4.5 ms answer does not, and SCAN_BACKLOG then forces it into a frame). The kill criterion for my
own claim (candidates ≤ ~200 at K=1,000) did not fire.

**What would make it wrong.** The census numbers at 10⁴/10⁵ could be a different code path (they
are not — same binary, same counters); the window terms could be a Linux artifact (the caps and
intervals are integer-derived and machine-independent, and the census's own 70/184 split is the
same window physics: burn's small `h` narrows it); the formation scenario could be ungame-like
(it is the game's stated premise — "faction-based … billions of ships" — and the nladder page's own
direction names it). The p99 attribution between scan and comb is measured only in aggregate
(stage means + per-call costs), not per-worst-frame decomposed.

**Cost of adoption, and fit.** Nothing to adopt: this kills a premise ("the observer half is
free"; "pin the near set") and re-ranks the fix. The cheap fixes to price next: (a) the bail's
numerator should count bodies (dedup `hit`) and its threshold should be entries-in-window vs
window-population, not `bodies/4` of the whole universe — a nonlocal coupling today (the belt in
doll 0 switches Home's scan on/off), against PRINCIPLES 15 ("local laws"); (b) the filter needs a
phase axis — the same concentration invariant as the encounters gold (taleb-09b5: real encounters
lie within partner rank 4 along the orbit), which is the representation that makes co-orbital
crowds cheap for the observer too; (c) the comb channel belongs to kick-cadence's page. Fit:
PRINCIPLES 26 ("steal what works") and 19 (a fix signals the wrong representation — a filter whose
viability depends on other dolls' populations is the wrong representation); the inversion lens did
its job ("invert a success: find the scene where the assumption breaks and run it").

**The lens.** Inversion sees what concentration breaks; it may under-weight that the census was
explicitly scoped ("on the ladder's flights") and honest about its domain — the failure was the
domain's quiet dependence on a scenario cap (`ladder_locals ≤ 300`, none in the player's band) and
a bail threshold crossed only off-scene. A builder lens would now build the phase axis; check that
against the cadence page's plans first (the comb is theirs).
