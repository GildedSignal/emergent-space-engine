Grade: lead

**Abstract.** The primitive half reproduces: cos 43.4 ns at its single-chain ISA floor (author 41.6), unrolled control equal, cos4 1.51× isolated, 2M-lane fuzz bit-identical, suite green, plane digests exact. But the headline — 0% at the compile, interleave dead — is an artifact: the A/B grid (p ≥ 2²⁰) and the plane settle never execute the patched `fast_quad`, because compactness = 1/periapsis clamps to zero at weak field and `quad()` dispatches e>0 keys to the **unpatched** `weak_quad` first. A coarse cos4 sabotage leaves all 28 grid keys and both plane digests (settle 1e10, 4e10) bit-identical — both arms ran identical code. On keys that do execute cos4 (p 2⁴–2¹⁶), a balanced A/B measures **+2.9% (2.3–3.4%)** per compile (null keys −0.1%). The primitive floor stands; the direction-closure falls.

## Reproduction (clean tree + work/patch.diff, all regen steps)

- Primitives (`cos_variants`, fuzz 2M lane-wise): shipped 43.4 ns | tuned 42.8 | cos4 lane 28.9 | isqrt ref 57.8 (author 41.6/41.2/27.6/56.0; runner 43.7/43.2/29.8/58.8 — same epoch family, ~4% box drift; ratio 1.50× vs claimed 1.51×). Fuzz asserts passed.
- Compile A/B, one binary, pinned core, epochs interleaved: B 24.2/24.9/24.8 µs vs I 25.0/24.5/24.6 µs in matched epochs — reproduces the reported "no difference" (author 25.1±0.2 vs 25.3±0.3; runner 25.4 vs 25.5). First pair straddled an epoch drift (B 18.8, I 24.3); a solo epoch measured 18.2 µs — the author's 30%-drift warning is real and their interleaved protocol is sound.
- Plane digest both arms `0c306185…cada2c` (settle 1e10) — exact; also 4e10 `d8a1847c…`. Suite with patch live: green (70 passed, 1 ignored).
- `predictions.md` (13:02) predates the patched artifacts (13:09–13:10); pre-registration verified. Band 1 (−4–12%) missed; the author reported the miss honestly — but attributed it to prediction 5 (OoO overlap), which the evidence below does not support.

## The artifact (adversarial case 1: sabotage census — outside the author's tested range)

A coarse sabotage of `cos4` (one lane's output += 2⁶⁰, far above any flooring resolution) with `COS4=1`:
- **All 28 of the author's grid keys: compiled Orbit checksum unchanged.** All 40 keys of my extended grid (p 2⁴–2³² × e 0–0.999): only the 16 keys with p ≤ 2¹⁶ and e > 0 change; every p ≥ 2²⁰ key and every e=0 key is unchanged. `COS4=0` + sabotage: 0/40 changed (the switch itself works both ways).
- **Plane digests unchanged under sabotage at settle 1e10 and 4e10** — the plane never executes `fast_quad`/`cos4` either. The dossier's "digest identical both arms" is true but vacuous.
- Mechanism, read off the shipped source: `compactness = periapsis.reciprocal()` (orbit.rs:104), so at p = 2²⁰, q = 2⁻²⁰ ≤ 2⁻¹⁸ (`WEAK_EXPONENT`) and `ShapeKey::for_orbit` clamps it to ZERO (orbit.rs:149); `quad()` then dispatches to `weak_quad` (orbit.rs:310) **before** the `fast` check — and the patch touches only `fast_quad` (orbit.rs:361). `predictions.md` states "fast_quad **and weak_quad** evaluate their four cos per panel through interleaved cos4" — weak_quad was never patched. The author's grid and the plane measure identical code in both arms; the 0% is by construction, and the mechanism claim ("the OoO window already overlaps those chains inside fast_quad") was asserted, never measured.

## The sign is positive where the patch executes (adversarial case 2: next decades of the swept numbers)

Keys that genuinely run `cos4` (p 2⁴–2¹⁶, e 0.5–0.999 — decades below the grid's p floor), balanced protocol (6 blocks of B-I-I-B, 12 runs/arm, per-key medians): **+2.9% median saving per compile, every key positive (min +2.3, max +3.4)**; the p ≥ 2²⁰ keys — identical code — sit at −0.1% (−0.5/+0.3) as a clean null. So the interleave **partially** survives the node: "0%", "does not survive the node", "dead on any deep-OoO core" are all wrong. The plane-relevant question (weak_quad, the actual hot path) remains untested.

## Novelty

Genuine: the wiki's open direction 1 named the interleave "(untested)"; no HISTORY entry or doc tests it; the primitive-floor measurement and the 77 ns correction are new. 7d2b's 24%-of-node ≈ 77 ns was a per-node attribution (4 cos), not per-cos; calling it "1.9× inflated" is defensible only under the per-cos reading — an interpretation, not a 7d2b error.

## Page (corrected in place)

The proposed page enshrined the false refutation (Refuted line, Current-best paragraph "the interleave idea with it", open direction 1b "closed") and its conflict resolution silently dropped main's 1a (9384's checker arms) while keeping the now-stale "(untested)" in direction 1. I corrected all four in `wiki/kick-jet.md`, marked as checker corrections, restored 1a, and kept the author's true content (primitive floor, epoch-drift protocol lesson — which I reproduced).

## Goal fit

Right bottleneck (`kick-jet`/frame-cost: the compile is ~half a kick's wall) and the primitive half obeys "Measure before claiming". But the compile half violates the lab's own 5 October lesson: "agreement between runs is not independence when they share harness bugs. Check that the measured events are distinct before counting hits" — here **zero** cos4 executions were counted as a measurement of cos4. A registered-risk diagnosis (OoO overlap) cannot substitute for a sabotage/control probe that the patched code actually runs.

## What the author missed

- A control that the A/B arms differ: any perturbation probe on `cos4` would have exposed the vacuous comparison in minutes. The interleave protocol (epochs) was well designed; the path liveness was never checked.
- The dispatch order in `quad()` and the compactness clamp at 2⁻¹⁸ — the "weak field, the fast path" premise of the grid is exactly backwards: weak field is the **weak_quad** path.
- `predictions.md` misdescribes the patch (weak_quad claimed patched).
- The experiment that would make this gold: patch `weak_quad`'s four cos (the plane's quadrature), rerun the balanced one-binary A/B with a sabotage liveness check, and price it against the kick (compile ≈ 49–62% of a leaver kick). If it holds ≥3% there it is a real, cheap, bit-identical lever; if 0%, the direction closes with evidence that executes.
