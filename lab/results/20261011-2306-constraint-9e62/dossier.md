# Dossier — 20261011-2306-constraint-9e62 (lens: the constraint)

**Claim.** On main today, the plane's frame at the flight setting (rtf 100) is bound by the view gather, not the engine: 64.6% of frame CPU is the gather, 99% of the gather is the `state_rate` light-cone readouts of the non-fleet bodies (2.88 of 3.75 ms/frame paced), the engine spends 0.28 ms p50 — and the gather is the one unbudgeted, emitter-linear claim on the frame.

**Bottleneck.** Not on the board's ranked list: the board ranks bottlenecks *inside* the engine (kicks, changeover, encounters), and inside the engine kicks still dominate (fleet 62 µs/item, ship 237, player 1,279; kick-bench median 60.3 µs with a 0.0% exact-memo hit, 23/23 distinct shapes). But the frame the player runs is 65% gather. Expected gain from the cuts below: ≥ 10× on the gather (to ~0.3 ms/frame at the flight setting), which deletes the gather as the frame's constraint up to ~10× the emitter count and lets the engine's 5 ms budget become the binding surface it was designed to be. It also unblocks any emitter-dense scene (fleets, belts) before a single engine change.

**Evidence** (Linux/x86, 8 vCPU, orders of magnitude only; raw JSONs in this folder; every command ≤ 60 s after a 36 s `cargo build --release -p xtask`):

| run (all `universe --bench`, seed 1) | emitters | gather p50 | engine p50/p99 | frame p50 | readouts/body/frame | overflow frames |
|---|---|---|---|---|---|---|
| rtf 100 paced (flight setting), 10 s | 76 | **3.75 ms (64.6% share)** | 0.28 / 5.39 ms | 4.68 ms | 2.61 | 34/600 |
| rtf 100 unpaced, 10 s | 76 | 0.75 ms | 0.05 / — ms | 1.10 ms | 2.60 | — |
| rtf 100 paced, `--members 400`, 5 s | ~394 | 4.38 ms (52.5%) | 2.81 / 5.75 ms | — | **12.0** | **126/300** |
| rtf 1 paced, 10 s | 76 | 2.36 ms (70.8%) | 0.14 ms | 3.27 ms | 1.64 | 0 |

- The gather's own split (600 frames, flight setting, from `view_split` in the run's patch): bodies loop 1,791.8 ms total, of which `state_rate` readouts 1,729.8 ms (**97%**); fleet setup 26.8, `f.motions` 1.0, member float work 5.1 ms (**0.2%**). Unpaced the same split is 450/435 ms — the readout path is **4.0× more expensive paced than unpaced** (per-readout 40.8 µs cold vs 10.3 µs warm): pointer-chasing through binding histories, descheduled between frames. This is the player's number; the warm number is a mirage.
- Per readout ≈ 10 µs warm against ~50 flops of physics: the readout walks the doll chain and `credit`/`partial` in i128 `Scalar` arithmetic with `binding_at` history walks per Newton step.
- Members sweep (unpaced, 5 s each): gather p50 0.48 / 0.79 / 3.57 ms at 4 / 48 / 400 members — linear, ≈ 9.5 µs per member and ≈ 15 µs per body warm; extrapolated to 10⁴ emitters the gather alone is ≥ 90 ms/frame warm. Members cap at ~366 (the lattice's own size).
- Determinism held across the instrumentation: the flight-setting digest `09e4085904c780e5…` at cut 203,025,447 is bit-identical before and after the patch (the patch only measures; `bench-flight-paced.json` vs the first pre-patch run).

Commands:
```
cargo build --release -p xtask                                       # 36 s
/home/glmlab/lab-target-1/release/xtask universe --bench --seconds 10 --rtf 100            # flight setting, paced
/home/glmlab/lab-target-1/release/xtask universe --bench --seconds 10 --rtf 100 --unpaced  # warm control
/home/glmlab/lab-target-1/release/xtask universe --bench --seconds 5  --rtf 100 --members 400
/home/glmlab/lab-target-1/release/xtask universe --bench --seconds 10                     # rtf 1
/home/glmlab/lab-target-1/release/xtask universe --kick-bench --seconds 10
```

**Predictions** ([predictions.md](predictions.md)): 4 of 5 held. Bodies dominate (50% + 49% eval = 99% of the split); `f.motions` is a cheap copy (0.03%); cold inflation is pointer-chasing-bound (4.0× on `eval`, the integer/history path, vs 3.6× on the float members); scaling linear with emitters. **Miss:** readouts are 2.61 per body per frame at the flight setting — above my 1.2–2.0 band — and **12.0 at 400 members** (handed-out fleet members get fresh, badly-guessed crossings: the ViewCache slot is per body id and a handed-out member is a new body). The kill criterion (readouts ≥ 4 warm) fires only in the 400-member case for the handed-out members, so the constraint naming holds at the flight setting and the guess quality is a second, measured defect at scale.

**Exploit, subordinate, elevate (the cheapest changes first, none built here):**
1. *Exploit the readout count:* seed a handed-out member's ViewCache slot from the fleet's last member state (it is the same ship; the id changes, the worldline does not). Measured ceiling at scale: 12.0 → ~2.6 readouts, a 4.6× cut on those bodies, one local change in the gather.
2. *Exploit the readout cost:* the same (body, tick) is read 2+ times per crossing (Newton convergence); a one-entry readout memo per body per frame is pure-function caching, no law change. Ceiling ~2×.
3. *Elevate (new mechanism, only after 1–2):* refresh quanta for the view — recompute an emitter only when its displayed quantities could cross a display quantum (direction, colour, age), per #28 "real vs displayed is not the same thing". This is the ≥ 10× cut and the one that scales to 10⁴ emitters.
4. *Subordinate:* the gather should sit under the frame's budget discipline like the engine (plane.md foundation 7: "Nothing takes an unbounded synchronous claim on the frame" — today the gather is exactly that claim, emitter-linear and unbudgeted).

**Where the constraint moves next:** at ~400 emitters paced the engine already overflows its 5 ms budget on 42% of frames (p99 5.75 ms; rtf lowest 1% 9.7 at the flight setting). Once the gather is cut, the frame's constraint moves to the engine's kick/rebind path — the board's known top item (60 µs/kick, 0% exact-memo hits, every kick a fresh cycle compile) — and past that to memory (1,203 bytes/body on a 16-byte tube) at billions of bodies.

**What would make it wrong.** The gather's share is measured on Linux/x86 with 8 vCPU; on the M1 (unified memory, different cache behaviour) the 4.0× cold inflation and the 65% share could shrink — the integrator re-measures. If the emitter count the player actually faces stays ≤ ~10², the gather never binds and the engine's kicks remain the only constraint that matters; my extrapolation to 10⁴ emitters assumes fleet/belt scenes, which is the goal, not the current scene. The rtf-1 paced gather (2.36 ms, 70.8%) shows the cost is per-frame, not per-game-second: it does not vanish by flying slower.

**Cost of adopting.** Cut 1 is ~10 lines in `view.rs` (seed the cache slot at handoff); cut 3 is a display-side refresh policy behind the existing `ViewCache`, touching no engine code and no outcomes (the gather stays a pure read; the crossing search stays exact when it runs). No gate is sized against it; B-series gates are untouched.

**Fit with PRINCIPLES.** #3: "Nothing is evolved that can be derived when looked at (clocks, redshift, views)" — the view is the named example, and the gather today re-derives every emitter's crossing every frame. #28: "real vs displayed is not the same thing" licenses display quanta. #12: "minimize spike compute and average compute usage" — an unbudgeted, emitter-linear gather is the opposite. #1: the cheapest compute is compute not done.

**The lens.** Goldratt's lens measured the plane's frame loop and stopped there: it did not run `behave --law plane` (which gate fails) nor the galaxy engine (`crates/space`, a different frame loop), so "the gather is the constraint" is a claim about the plane only. It also buys the dashboard's own category "engine vs view" uncritically: if observation itself were budgeted as engine work (the light cone as a consumer in the slack queue), the split would read differently, though the physics cost would be the same.
