# Dossier — 20261011-1600-constraint-2094 (lens: the constraint)

**Claim.** On the plane as flown, the frame's constraint is the view gather — an unbudgeted,
perfectly linear **15.4 µs per emitter per frame** (1.98 readouts/emitter, already at Newton's
floor) — while the engine is already protected by its 5 ms budget; per-body gathering is 2–7
orders of magnitude short of the goal's N, so the next representation to change is the view's
(doll-level gather), not the engine's.

**Bottleneck.** The board's live order says "kicks dominate the engine's cost" — true inside the
engine, but the frame (what the player feels; the plane is judged on smoothness) is owned by the
gather at every scale measured: **65–70% of every frame**, engine 17–22%, json+wire 13%. The gain
from a hierarchical (doll-level) gather is the difference between O(visible bodies) and
O(visible dolls + significant bodies): at 10⁹ bodies per-body gathering is 4.3 hours per frame —
seven orders over. It also deletes the only unbounded synchronous claim left in the frame loop
(plane.md foundation 7 names it: "…or a gather").

**Evidence** (all commands ≤ 60 s unless noted; Linux 8 vCPU shared box, 1 thread, machine_state
recorded in the JSONs — most fields unavailable on Linux; orders of magnitude only):

1. The plane, as the player runs it (`cargo run --release -p xtask -- universe --bench --rtf 100
   --seconds 30`; work/bench-rtf100-t1.json): frame p50 4.22 ms, p99 10.77 ms, no hitches;
   `where_the_time_goes_ms`: **gather 69.5% / engine 17.4% / json 9.2% / wire 3.8%**; engine p50
   0.24 ms inside a 5 ms budget; rtf median 100.0, lowest 1% 9.9; 53 overflow frames.
2. Members 480 and 4800 (work/bench-rtf100-m480.json, -m4800.json): the scene **saturates at 428
   bodies / ~214 alive** — the fleet dial is not a body-count dial beyond ~400 (the battle's
   collision frontier, not the member count, sets the hand-out rate; a finding for future N-work:
   the plane has no body-count dial that scales). At 428 bodies: gather p50 6.6 ms, **first
   hitches above 16.7 ms: 120/hour**, worst 17.7 ms (≈ gather max 9.7 + engine max 8.7); player
   item 3.35–3.59 ms = **68–72% of the engine's whole frame budget in one item**; overflow frames
   356–408, rtf lowest 1% = 0.0 — the engine starves gracefully (defers), the frame's worst
   tracks the gather's max.
3. The gather alone at the extremes (B15's stream scene, bare tubes so the engine is ~0;
   `cargo run --release -p emergent-universe --example gather_scaling`, work/gather-scaling.txt;
   probe added at crates/universe/examples/gather_scaling.rs, 60 frames at rtf 100, warm cache):

   | emitters | gather p50 | µs/emitter | readouts/emitter |
   |---|---|---|---|
   | 100 | 1.49 ms | 14.9 | 1.98 |
   | 1 000 | 15.0 ms | 15.0 | 1.98 |
   | 10 000 | 154 ms | 15.4 | 1.98 |
   | 50 000 | 770 ms | 15.4 | 1.98 |
   | 100 000 | 1 540 ms | 15.4 | 1.98 |

   Dead linear over three decades; 1.98 readouts per emitter is the floor for a verified integer
   crossing (the cache extrapolates by arrival rate and lands within ~1 tick), so the cost is the
   readout itself (exact integer doll-chain math) — **there is nothing left to exploit**.
4. Frame-budget arithmetic: at 60 Hz the frame is 16.7 ms; engine 5 ms (protected), json+wire
   ~1 ms ⇒ the gather fits in ~10 ms ⇒ **~650 emitters per frame** is the view's ceiling on this
   class of machine. The first flight (76 bodies) sits at 1/8 of it; 428 bodies already hitch.
5. Gates: `behave --law plane` — B12 FAIL (statistic known miscalibrated, redesign in flight),
   B13 FAIL 60/64 (known marginal), B14 FAIL 60.1 s over the 60 s limit (this box, marginal).
   The G/B7/B9–B11 "FAIL" lines under `--law plane` are an invocation artifact: the plane law
   answers None outside B12–B14 (xtask/src/behave/plane.rs's `impl Law`); G1–G6 belong to
   `--law space` (confirmed separately, work/behave-space-g.txt). No new breakage; the state
   matches HANDOFF (6 October).

**Goldratt reading.** Exploit: nothing — the gather is at its algorithmic floor; micro-optimising
the readout buys ≤ 5× (ceiling ~650 → ~3 000 emitters), not the goal's scale. Subordinate: the
engine already does (budget, defer, rtf dip); two things do not — the player's item carries the
exact O(N)-in-doll neighbourhood scan (`PlayerNeighbourhood`, 1.33 → 3.4–3.6 ms/item as alive
bodies went 50 → 214; fleet, player and every handed-out member share Home's doll, so it grows
with the doll's population), and view_json+wire is linear in what's seen. Elevate: gather dolls,
not bodies — a doll whose members sit below the player's perception floor is ONE emitter (a
multipole of the view); this is the goal's own law ("the zoom level is the minimap", OC#30;
principle 33's symmetric reading: an observer resolves only what is significant at its scale).
The perception floor is Julien's to set ("the floor is what the player can differentiate").
**Where the constraint moves next:** with a hierarchical gather, the frame's next constraint is
the engine's event rate (1 058 events/s at 428 bodies, ~100 µs per ship item — the kicks cadence,
the board's top question), then the player's O(N) scan (the encounter skin). The board's order is
confirmed; the missing piece was that the view, not the engine, owns today's frame.

**Predictions** (predictions.md, written before the sweep): the linear gather and its dominance
held exactly (15.4 µs/emitter over three decades; 65–70% share at every scale; hitches at ~430
bodies; the budget protects the frame — worst frame tracks the gather, engine defers). Two
magnitudes were off, both reported as held-miss: the player item grew 2.5× (not 5–10×; half the
handed-out members are refused, so ~214 alive, not 428) and ship µs/item fell to 97–106 µs (not
within 2× of 280; the item mix changed — haulers' eccentric orbits vs handed-out members) — in
both cases the prediction's substance (an O(N) term in the player's item, none in a ship's) held.
The "~4 800 bodies" case was untestable: the scene saturates at ~430 (itself a finding).

**What would make it wrong.** The M1's per-emitter cost being materially cheaper (the readout is
exact integer math, not SIMD-bound — the order should hold; the integrator re-measures); the
first flight staying under ~600 emitters forever (the belt B18b and any fleet-scale content blow
through it; the goal says billions); the encounter skin landing before the player's scan bites
(it bites near ~10³ bodies in one doll). Also unexamined: whether what the gather computes is the
right physics — 7 of 101 emitters at the first-light edge returned no crossing (a completeness
question for B15, noted, not judged here).

**Cost of adoption.** A doll-level gather is a view-layer change (view.rs) judged by B15 (frozen);
it must not change what the player can differentiate. Until the perception floor is set, a cheap
interim exists that changes no outcome: budget the gather like the engine (nearest-arrival first,
overflow = a smooth dip), which plane.md foundation 7 already demands of it.

**Fit with PRINCIPLES.** Principle 3: "Nothing is evolved that can be derived when looked at
(clocks, redshift, views)" — the gather derives correctly, but at per-body cost, which violates
the same principle's economy at scale; principle 33: "a body resolves only the influences that
are significant at its own scale" — symmetrically, an observer resolves only emitters significant
at its scale; OC#30: "the zoom level is the minimap". plane.md foundation 7's own letter: nothing
takes an unbounded synchronous claim on the frame "whether a cycle compile, a rebinding burst, a
decompression or a gather" — the gather as built is exactly that claim.

**The lens.** The constraint lens measures the machine, not the law: it may have missed that the
right fix is a law question (the perception floor is Julien's), and it judged nothing about the
gather's physics correctness (B15's domain). Single machine, single thread (the plane as flown is
1 thread; the gather is serial regardless, so threads do not move this constraint).
