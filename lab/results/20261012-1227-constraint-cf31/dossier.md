# Dossier — 20261012-1227-constraint-cf31 (constraint lens)

**Claim.** Measured whole, the flying plane's constraint is not the engine but the view gather: re-deriving every emitter from exact integers every frame costs 61–74% of every frame's CPU at every real-time factor, and deleting the light-cone search alone (which leaves the digest bit-identical) cuts the frame 2–3.5× at rtf ≥ 100 — the engine is 5–24%, so the board's engine questions govern a fifth of the frame, not the product.

**Bottleneck.** Not on the board's list: the board's live questions (kicks per orbit, changeover, encounters, memory) are all engine-interior. The measured whole says the constraint of the system as the player runs it is `gather_cached` (crates/universe/src/view.rs): an unbudgeted, O(N_bodies) per-frame loop that for each alive body runs a Newton light-cone search whose every evaluation is a full doll-chain readout (`state_rate` → `binding_at` + `partial`'s map-run + `force::field`), ~14–58 µs per body per frame (Linux/x86, orders of magnitude; the run-to-run swing on this shared box is 4×, so the stable probe floor 18–22 µs is the honest number). Expected gain of the named exploitation: 2–5× on the gather, 2–3.5× on the whole frame at rtf ≥ 100; it deletes the per-frame Newton search as a component. At 10⁶ engine bodies the loop as written is ~20 s/frame — the O(N) unbudgeted scan is a wall long before the engine's own scaling risk (candidate pairs) bites.

**Evidence** (seed 1, paced 60 Hz, Linux/x86 8 vCPU, load 0.5–1.8; all JSONs and DIAG traces in this folder; `analyze.py` recomputes the table):

| rtf | gather p50 intact → no-crossing probe | frame CPU p50 intact → probe | shares intact (engine/gather/json/wire) | digest |
|---|---|---|---|---|
| 1 | 2.36 → 1.26 ms (1.9×) | 3.30 → 1.96 ms | 0.05 / 0.74 / 0.15 / 0.07 | n/a (different cut) |
| 100 | 3.60 → 1.13 ms (3.2×) | 4.59 → 1.62 ms | 0.20 / 0.67 / 0.09 / 0.04 | identical |
| 1000 | 5.95 → 1.12 ms (5.3×) | 7.25 → 2.05 ms | 0.24 / 0.69 / 0.05 / 0.02 | identical |

- The probe (`ES_PROBE_NO_CROSSING=1`, patch in `work/`) replaces the per-body Newton search with one read at the presented tick: engine digest bit-identical at rtf 100/1000 — the view is a pure read, so the frame budget can be spent on it with zero physics risk.
- Even with no search at all, the gather floor is 1.1–1.3 ms for 48–76 bodies (18–22 µs per body per frame, stable across runs): the mandatory full re-derivation, not the search, is the deeper half.
- The same file holds the cheap representation: fleet members are read at 2.6 µs each (extrapolated from the stepper's committed tick, no crossing, no doll-chain solve) — 6–20× cheaper per body than the bodies loop.
- The engine's own budget holds: 5 ms wall, causal-deadline order, overflow 4–92 frames at rtf 1–1000 with no hitch in CPU time (hitch counts 0 above 16.7 ms in every run).
- Gates on this tree match HANDOFF (B12's statistic broken as known, B13 60/64, B14 timeout 60.1 s; G1/G2/G5 PASS under `--law space`; the G-failures under `--law plane` are the adapter's honest "does not answer" per its module doc).

Commands (each ≤ 60 s):
```
cargo build --release -p xtask
/home/glmlab/lab-target-1/release/xtask universe --bench --seconds 30             # rtf 1, intact
/home/glmlab/lab-target-1/release/xtask universe --bench --seconds 20 --rtf 100   # intact
/home/glmlab/lab-target-1/release/xtask universe --bench --seconds 20 --rtf 1000  # intact
ES_PROBE_NO_CROSSING=1 …/xtask universe --bench --seconds 20 --rtf 100            # probe (patched tree)
python3 analyze.py .                                                              # the table above
/home/glmlab/lab-target-1/release/xtask behave --law plane; … behave --law space --gates G1,G2,G5
```

**Predictions** (predictions.md, written before the probe): 5 held (digest identical, engine unaffected), 6 held at the top edge (floor 18–22 µs/body vs predicted 3–15). 1–3 partially failed, honestly: I predicted the search was ≥ 80% of the gather; it is 45–80% (1.9× at rtf 1, not 5×+), because the mandatory per-body read is ~15 µs by itself. 4 held at rtf = 1000 only (engine becomes the top share 0.36 only there; the gather floor still leads at rtf ≤ 100). The refinement — constraint = per-emitter re-derivation as such, search included — is the corrected claim above.

**What would make it wrong.** (a) If the frame's real budget is the engine at scale: at N where events/frame × ~50 µs exceeds ~5 ms the engine reclaims the constraint — on this scene that is rtf ≳ 10⁴, at larger N sooner; the claim is about the plane as it flies today. (b) If the M1's gather/wire costs differ in kind, not just degree (the integrator re-measures). (c) If emitters must be re-solved every frame for correctness — no: the memo already guarantees staleness-independence (`ViewCache` doc: any cache gives the same view), so cadence is free to choose. Adoption cost: small and local — a crossing cadence policy in `gather_with` plus a surprise gate (re-solve when the body's binding changed: its `event_time` moved), the fleet path as the template; nothing in the engine, the laws, or the gates moves (digest proves it). Fit with PRINCIPLES: #3 "Nothing is evolved that can be derived when looked at (clocks, redshift, views)" — the view is correctly derived, but #14 "we only care about changes" is what the gather violates: it re-derives unchanged emitters at full exact-integer price every frame; #12's smoothness budget applies to the view exactly as to the engine, and today the view has none.

**Goldratt steps.** Exploit: advance each emitter's crossing by its memoised arrival window (one addition) and read the tube once at that tick — no Newton, no bracket; re-solve exactly on binding change or every k-th frame; the digest cannot tell. Subordinate: the view needs the engine's discipline (a budget, causal order, overflow accounting) before the body count grows — it is the only unbudgeted per-frame O(N) loop in the frame. Elevate (only after): read emitters from changes (tube events, observer crossings), the fleet member path as the existence proof. When the constraint moves: to the engine at high rtf/large N (already share 0.36 at rtf 1000 in the probe) — then the board's #1 (fewer kicks per orbit) governs, then encounters at N; at rtf 1 with a cheap view the frame becomes JSON/wire-bound (~0.7 ms), i.e. smoothness headroom, not physics, is the product there.

**The lens.** The constraint lens measured the machine and found the constraint outside the engine the board optimises; what it may have missed: (a) taste — the view's exactness is why the game *feels* relativistic (redshift, lag, aberration are computed, not faked); any cadence policy must keep what the player can differentiate (PRINCIPLES #28, the view is an instrument), which is a behaviour question, not a cost question, and needs its own rung; (b) the wire/JSON 15% share is a browser-age artifact the same way, and the browser render cost is outside this bench entirely; (c) per the lab rules these are Linux/x86 numbers — orders of magnitude only, M1 to be re-measured by the integrator.
