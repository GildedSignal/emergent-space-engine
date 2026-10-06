# Dossier — 20261006-0916-fermi-bf90

**Claim.** At 10⁹ bodies the M1's binding terms are not the kicks: the board's "190 cores" pairs the B9 *ceiling* cadence (512/orbit) with the *cheap* event cost (2 µs) — an inconsistent pairing that lands within 10% of today's honest bill (172–549 cores) only by cancellation — and under the law's designed point (0.3 kicks/orbit) the kick bill is 0.1 core while the **encounter candidate setup** (2.5–24 µs per pair per element change, k ≈ 4) becomes the largest per-body term (0.7–2.7 cores), the **O(N) view gather** is dead by ≥ 2 orders even at 1 ns/item (only aggregation + incrementality passes), and **scar reabsorption ≥ 0.9 MB/s** is required or every long session dies at 3.2 GB/h regardless of N.

**Bottleneck.** Board #3 ("cost at a billion… about 190 cores… need 10–100× less") and the 5 October scaling risk. The estimate shows the 10–100× is already banked between cadence (107×, adopted H0190) and kick-cost work (2–7×, in flight), and re-ranks what is actually left: per-body arithmetic is a non-problem (measured floor 24 ns vs the 2 µs target = 80× headroom), so the next 10× must come from the O(N) terms and reabsorption, not from kicks.

**Evidence.** All commands run in this tree; each ≤ 60 s (x86 cloud, orders of magnitude only).

1. *Today's real kick cost, the plane's own bench* (`xtask universe --kick-bench`, seeded scene, deterministic replay, distinct pending kicks at 60 Hz snapshots):
   `cargo build --release -j4 -p xtask && $CARGO_TARGET_DIR/release/xtask universe --kick-bench --seconds 10 --rtf 100` → `kick-bench-rtf100.txt`
   - made bodies: median **35 µs**, p99 56 (137 samples); fleet members: median **88–91 µs**, p99 **392–478** (682 samples).
   - `cycle_rebinds` 663 of 682 samples: **97% of distinct kicks rebind**; exact-key memo hit rate **0.0** (confirms the 5 Oct artifact lesson on distinct kicks).
   - M1 anchor unchanged in OoM (29 µs, 15 of them rebinding; HANDOFF).
2. *The designed kick's arithmetic floor* (`rustc -O -o kick_floor kick_floor.rs && ./kick_floor`): i128 fixed-point ΔE/ΔL from the doll's shared moments, J2 term, 12+12-bit cycle-memo probe, tube advance by additions — **24 ns/kick**, identical hot and streaming 67 MB (compute-bound, not bandwidth-bound). The 2 µs event target sits **80× above** the arithmetic floor: cost/kick is a compiler problem, never a physics bound.
3. *The budget model* (`python3 model.py > model-out.json`), every anchor measured, nothing tuned. Headline rows (10⁹ bodies, all on 90-min orbits, RTF 1, 4 cores):

   | pairing | cores | verdict |
   |---|---|---|
   | 512/orbit × 2 µs (the headline's arithmetic) | **190** | dead ×47 |
   | 32/orbit × 29 µs (today, honest) | **172** (x86 members: 549) | dead ×43 |
   | 0.3/orbit × 29 µs | 1.6 | pass, 2.5× margin |
   | 0.3/orbit × 2 µs (designed) | **0.11** | pass ×36 |
   | 0.3/orbit × 24 ns (floor) | 0.0013 | pass ×3000 |
   | + re-anchor jet 0.05 × compile(1–30 µs) | +0.08 | pass |
   | + encounter setup k=4 × 12 µs (today) | **+2.7** | pass only 1.4× |
   | + encounter setup k=4 × 2 µs | +0.44 | pass ×13 |

   - **Memory:** stored tubes 16 GB (dead ×3.2); population programs 16 MB; programs+scars pass to a kicked fraction of 10% (2.4 GB); scar cap ≈ 2.1×10⁸ live distinctions in 5 GB.
   - **Bandwidth:** ≤ 12 GB/s even at the ceiling cadence ×128 B — never binding (5× headroom worst case, 10⁴× designed).
   - **Gather:** O(N) per item dead ×3.6×10⁷ today, ×2×10⁵ at 1 µs, **×200 even at 1 ns**; aggregated-every-frame passes only at ≤ 10⁶ visible × 1 ns; **incremental** (933 changed visible per frame × 1 µs = 0.9 ms) passes. "The zoom level is the minimap" is a hard requirement, not a nicety.
   - **H_live:** 5.6×10⁴ kicks/s × 128 b ≈ **0.9 MB/s** of distinction bits → **3.2 GB/h** if never reabsorbed. Reclamation must match the distinction rate (B18's floor rule is the guard).
   - **Scene mix:** goal-shaped (10⁷ in 90-min fleets, rest on ≥ year orbits) pays 0.001 core in kicks; the 190-core scene is the adversarial corner, not the goal.

**Predictions** (`predictions.md`, written before the runs): P1 ✓ (median in 10–60 µs; rebind share ≥ 40% — measured 97% of kicks, 52% of M1 cost); P2 **missed low**: floor measured 24 ns against a predicted 50–500 ns (conclusion strengthened, bound missed by 2×); P3 ✓ (190 = 512 × 2 µs ÷ 5400 s; today honest 172); P4 ✓ (tubes dead ×3.2; gather dead ≥ ×200 even at 1 ns; encounter setup, not kicks, binds the designed scene); P5 ✓ (0.001 core goal-shaped).

**What would make it wrong.** (a) If fleet-member kicks on the M1 are not ≤ 29 µs-class (my x86 88–91 µs median may reflect the older core; the M1 re-measure decides the "today honest" row, not the designed rows). (b) If averaged kicks usually leave the quantized (E, L) key unchanged, the encounter setup bill collapses (the model charges every kick a full element change — conservative); if they *always* cross a quantum, cadence gains erode too. (c) k = 4 is taleb-09b5's formation case; sparse high-e belts may need larger k (r8 v2's candidate sets). (d) The 24 ns floor is my model of the designed kick (always-memo-hit, no carry law), not shipped code — it bounds arithmetic, not semantics. (e) Medians hide tails: p99 kicks are 4–5× the median, and OC#36 prices p95/99, so the core bill above is the *mean* bill; the allocator must absorb the tails.

**Cost of adoption.** None in code — this re-ranks work: (1) the encounter setup cost (2.5–24 µs) is the un-banked per-body lever and should join Sol's kick work (same rebind-dominated float path); (2) the view gather must be measured for aggregation+incrementality before any pixel polish (a per-emitter cache is queued — the estimate says it is mandatory, worth 10⁵×); (3) scar reabsorption becomes a B18-adjacent requirement with a number (≥ 0.9 MB/s adversarial).

**Fit with PRINCIPLES.** "Compute only surprises… Nothing is evolved that can be derived" (3): the two mandatory terms are exactly the surprise-driven ones (incremental gather, scar reabsorption); "the algorithm that allocates the work to prevent those heavy tails" (12): the p99 column is where the margin actually lives; "Measure before claiming" (10): two of the board's standing numbers (190 cores, 10–100×) now have their arithmetic exposed and reconciled. "A failed expectation is not automatically a failed method" (H0183): P2's miss is the floor being *better* than estimated.

**The lens.** Fermi arithmetic sees means, not tails (the p99 kick is the real smoothness question), treats the scene as one orbit class until forced otherwise, and cannot see scheduling structure (slack ordering, GPU offload of the dense order) at all. The reconciliation's power came from exposing *which* two numbers the headline multiplied; a different lens might have accepted 190 as "about right" and moved on — the cancellation makes it right today for the wrong reason, which is exactly the kind of agreement that hides drift.

## Reproduce
```
cargo build --release -j4 -p xtask && $CARGO_TARGET_DIR/release/xtask universe --kick-bench --seconds 10 --rtf 100
rustc -O -o kick_floor kick_floor.rs && ./kick_floor
python3 model.py > model-out.json
```
Files: `kick_floor.rs`, `kick-bench-rtf100.txt`, `model.py`, `model-out.json`, `predictions.md`.
