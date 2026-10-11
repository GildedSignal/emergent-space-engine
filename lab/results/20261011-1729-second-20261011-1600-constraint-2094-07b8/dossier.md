# Dossier — 20261011-1729 (second author on 20261011-1600-constraint-2094, lens: the constraint)

**Claim.** The checker's named experiment is done — the `--members` clamp raised, the sweep run at
true 480 and 4800 members — and the original claim **holds at true N with three corrections**: the
view gather is still the frame's constraint at every scale measured (63.1% of a collapsed 58.9 ms
frame at 4305 bodies, the engine deferring 900/900 frames, the player's O(N) item at 25.8 ms —
5× the engine's whole budget), but (1) the "scene saturates at 428 bodies" finding is retracted —
it was the CLI clamp, and the scene reaches 4305 bodies in 15 s; (2) "1.98 readouts/emitter is the
floor" is wrong — the plane as flown runs at 1.00–1.29 readouts per body (H0213's 1.2 confirmed;
the shipped `view_rel` shows 1.00–1.63 by geometry; the floor for a cached crossing is 1); (3) the
"15.4 µs per emitter, nothing left to exploit" law is the stream geometry's number — the plane's
own hot marginal is ~11 µs per body, and the first flight's 69% gather share is inflated ~4× by a
~2.8 ms per-frame cold-restart that is an artifact of pacing on this co-tenanted box (unpaced, the
identical flight gathers in 0.72–0.98 ms). The ~650-emitter ceiling survives re-derivation from
the plane's own marginals: ~700 bodies all-in.

**Bottleneck.** The board's question behind the run: does the frame's constraint move with true N?
Answer: no — the gather owns it at 4305 bodies as at 76, and the next constraint after it is the
player's O(N) neighbourhood item, exactly as the author ordered them. The gain of the doll-level
gather is unchanged (O(visible bodies) → O(visible dolls)); what this run adds for the integrator
is the corrected per-emitter arithmetic the next design step needs: ~1.0 readout per body per
frame (the memo is at its floor), ~8–9 µs per readout once the working set leaves cache (the cost
is memory, not Newton — principle 17's von-Neumann bottleneck, so the lever is the tubes' memory
layout, not the arithmetic), json+wire ≈ +5 µs per body, ceiling ≈ 700 bodies at 60 Hz with the
engine's 5 ms protected.

**Evidence** (Linux 8 vCPU shared box — the window's other omp runs were resident, load ~1.1;
peak RSS of the largest run 1.14 GB; machine_state in the JSONs, most fields unavailable on
Linux; orders of magnitude only, the M1 re-measures). All from this tree with the author's probe
patch applied and ONE line changed: `--members` clamp `clamp(4, 400)` → `clamp(4, 40_000)`
(xtask/src/universe/mod.rs:32). Both edits are in `work/patch.diff`; the tree is restored after
the run. Commands (each ≤ 60 s unless noted; `X=/home/glmlab/lab-target-0/release`):

1. **The record regenerates.** `cargo build --release -p xtask && $X/xtask universe --bench
   --rtf 100 --seconds 30` → digest `41343a14…728b2`, bit-identical to the author's and the
   checker's baseline (work/bench-rtf100-default.json): frame p50 4.22 ms, gather p50 3.45 ms /
   68.9%, engine 0.243 ms, 0 hitches, rtf median 100.
2. **True 480 members** (`… --members 480 --seconds 30`, work/bench-rtf100-m480-true.json,
   digest `c4e03c80…`, distinct from the clamped runs' identical `3db02d3d…`): **508 bodies —
   all 480 members handed out; there was no saturation and no collision-frontier mechanism.**
   Gather p50 3.52 ms / 58.3%, frame p50 5.22 ms, **zero hitches above 16.7 ms (worst 13.5 ms)**
   — the author's clamped-run "120 hitches/hour, gather 6.6 ms at 428 bodies" did not reproduce
   on today's box (contention-inflated then); player 2 174 µs/item (the O(N) scan, 1.7× baseline),
   ship 61 µs/item, rtf lowest 1% 0.00 with 274 engine-overflow frames.
3. **True 4800 members** (`… --members 4800 --seconds 15`, wall 53.8 s, work/
   bench-rtf100-m4800-true.json, digest `577a2568…`): **4305 bodies, all alive, climbing.** The
   frame collapses exactly as the checker's 10 s probe showed: frame p50 58.92 ms, **gather p50
   36.95 ms / 63.1%**, json 12.23 / 20.5%, wire 2.47 / 4.2%; engine p50 5.118 ms — pinned at its
   budget, deferring every frame (overflow 900/900, rtf median 0.0); **player item 25 844 µs —
   5× the engine's whole 5 ms budget** (the author's prediction 2, which the clamp cost them,
   holds at true N); hitches above 50 ms 43 518/hour; worst frame 114.6 ms ≈ gather max 60.7 +
   engine max 51.8 (one frame where the engine itself blew its budget — the only observed crack
   in "the engine is protected"; the median is protected).
4. **The ramp instrument** (new probe `plane_readouts`, in work/patch.diff; the bench's frame
   loop, scripted decisions identical, per-frame alive/gather/readouts; `$X/examples/
   plane_readouts <members> <frames> <rtf> <paced>`; outputs in work/plane-readouts-*.txt):
   - **Readouts per body in the plane as flown: 1.00–1.29** (m4800 ramp 1.00–1.15; m480 steady
     state 1.03–1.05; m48 1.22 — its alive mix is ~40% native planets/moons vs ~8% at m480; the
     mix dependence is a hypothesis, not measured). The accounting floor is (alive−1)/alive ≈
     0.997 (the player is never crossed), so steady state ≈ 97% of bodies cross in ONE readout.
     H0213's 1.2 is the plane's own number; the author's 1.98 was the stream geometry (dist 5e7)
     alone.
   - **Hot marginal: ~10.5–11 µs per body** (m480 bins at 250–300 alive: 10.5–11.0 stable over
     25 s; m48: (0.73 ms − ~0.15 fixed)/54 ≈ 11; m4800 rising 8.2 → 11.3 µs as alive goes ~560
     → 2980 — the working set leaving cache). Per readout ≈ 8–9 µs established — the same as the
     stream probe's 15.4/1.98 = 7.8 µs at 100k emitters (DRAM-bound): **the per-readout cost is
     set by the memory hierarchy, not by Newton's iterations.**
   - **The true alive dynamics at members 480:** alive peaks at 404 (~9 s) then falls to ~250 by
     30 s (257 lost) — the real "frontier" is the battle's loss rate balancing hand-outs, a
     dynamic, not a clamp and not a fixed ceiling.
5. **The readout floor across geometries** (shipped, unmodified): `$X/examples/view_rel 100 100`
   → reads/emitter 1.00 (slow across) to 1.63 (observer 0.9c, toward); H0213's 1.2 = the 0.9c
   toward/away cases. The author's stream law reproduces from the patch (`$X/examples/
   gather_scaling`, ~150 s, over the 60 s rule, noted): 15.0–15.8 µs/emitter this box, dead
   linear 100→100k, 1.98 readouts — one law across three boxes (author 14.9–15.4, checker
   15.0–15.5; work/gather-scaling.txt).
6. **The first flight's 69% share decomposed.** The same m48 flight, unpaced (probe, decisions
   identical): gather 0.72–0.98 ms. Paced at 60 Hz: the bench's 3.45 ms — a ~2.8 ms per-frame
   cold-restart. It persists when pinned to one core (3.7–3.9 ms), it is compute not
   descheduling (the bench's frame_cpu_ms ≈ frame_ms), and the box carries the window's other
   omp runs: after each frame's sleep a co-tenant has thrashed the shared cache. **On the M1,
   alone, this term should shrink; the cloud number overstates the first flight's intrinsic
   gather cost ~4×. The integrator re-measures.** (work/plane-readouts-m48-paced.txt and
   -m48-scripted.txt.)
7. **The ceiling, re-derived from the plane's own marginals** (all hot, the regime at a full
   frame where there is no sleep): gather ~11 + json ~4.2 + wire ~0.9 ≈ 16 µs per body →
   (16.7 − 5 − ~0.3)/16 µs ≈ **700 bodies**. The author's ~650 stands — their derivation used
   the stream's 15.4 µs for the gather alone and ignored json+wire; the errors cancelled.

**Predictions** (predictions.md, written before the sweep; the checker's 10 s m4800 probe was
known to me and is not counted): P4 and P5 HELD (the 4800 collapse, its numbers, the ceiling
moving < 2×); P2 HELD (view_rel 1.00–1.63, the plane at 1.00–1.29); P1 HALF-WRONG in the
instructive way — the 2.8 ms "fixed" cost is not intrinsic to the gather but the paced
cold-restart on this box (unpaced fixed ≈ 0.15 ms), and the marginal came in 10.5–11 not 8–10;
**P3 FAILED** — true 480 shows gather 3.52 ms (not 7–9) and zero hitches (not hundreds/hour):
the alive peak is 404 and falls, and the hot marginal is 11 µs, not the 30–50 I derived from
the author's contention-inflated clamped run. My kill criteria did not trigger (gather share
never under 50%; marginal never ≥ 15; plane readouts never ≈ 1.98). The 1.05 readout floor
criterion triggered marginally at 1.03; investigated: the true accounting floor is ≈ 0.997, so
1.03 is valid (above), not an accounting error.

**What would make it wrong.** The M1 measuring materially differently on the two artifact-laden
numbers (the cold-restart term, which should shrink on an idle single-tenant machine, and the
per-readout cost, which is cache-hierarchy-bound); the first flight staying under ~600 emitters
forever (the goal says billions; the belt and any fleet content blow through it); a doll-level
gather that cannot preserve what the player can differentiate (B15's domain, not measured here).
Unexamined here: the gather's physics completeness (7 of 101 emitters returning no crossing,
noted by the author, still open); the engine's one 51.8 ms overrun at 4305 bodies (one frame —
worth one look by the engine's owner, it is the only crack in "the budget protects the frame").

**Cost of adoption.** Nothing to build in the engine; the corrections are to the record the next
design step reads: use ~1.0 readout/body, ~8–9 µs/readout (memory-bound), json+wire ≈ +5
µs/body, ceiling ≈ 700 at 60 Hz — and treat the memory layout of tubes (causal-order layout,
principle 17) as the lever the "nothing left to exploit" conclusion hid. The interim the author
named (budget the gather like the engine) remains the cheap view-layer change; the doll-level
gather remains the real one, pending Julien's perception floor.

**Fit with PRINCIPLES.** Unchanged from the author's reading — principle 3 ("Nothing is evolved
that can be derived when looked at (clocks, redshift, views)"): the gather derives correctly but
at per-body cost; principle 33's symmetric reading (an observer resolves only what is
significant at its scale); OC#30 ("the zoom level is the minimap"). This run adds principle 17
to the finding's letter: "we need to be deeply aware of von-neumann bottleneck and memory" —
the readout's cost is memory, so the next 10× is a layout change, not an arithmetic one.

**The lens.** The constraint lens measures the machine; corrections 2 and 3 came from adding the
two instruments it lacked (per-frame readout counts in the plane's own scene, and the
paced/unpaced pair that separates intrinsic cost from box artifacts). What it still does not
judge: whether what the gather computes is the right physics (B15), and whether 700 emitters is
the right ceiling to design against — that is Julien's perception floor, not a measurement.
