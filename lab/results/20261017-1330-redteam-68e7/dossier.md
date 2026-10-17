# Dossier — 20261017-1330-redteam-68e7 (lens: premise red-team)

**Claim.** The recorded blocker "r5 remains uncreated and cannot be created in this lab …
an M1-side run owns it" (wiki representation-premises, 20261017-1018-redteam-13c6) is a
category error: the dense order is "CPU, or Metal on the GPU" (law.md L50), its CPU arm
(`Chronon`) is portable, and r5 — created and frozen here before its execution — **PASSES
on this Linux box**: sparse ≡ dense bit-identity holds 20/20 (10 scenes × threads {1,4},
116,874 contacts, kicks and live carries in every scene), the both-shifted positive
control agrees 10/10, the one-order-late negative breaks 10/10, verdict PASS.

**Bottleneck.** Not a compute bottleneck: a false dependency. The premise census left the
design's §3 premise "two evaluation orders … with identical bits" unguarded and its rung
(r5) blocked on the M1; this run deletes the blocker (any box can run the CPU arm) and
unblocks the falsifier ladder's r5. Expected gain: none in speed; a dead wait removed and
a premise moved from "unguarded" to "guarded and passing". Bonus, orders of magnitude
only (shared x86, release): the sparse event core beats lockstep 28× at 2500 bodies
(0.27 s vs 7.54 s) and 13× at 3000 (0.84 s vs 10.80 s), equal only on the epoch-1 storm
scene (7.75 s vs 7.70 s) — the design's §3 split (sparse where events are rare) is
already the right call at battle scale on CPU.

**Evidence.** All numbers regenerate with `regen.sh` (≈9 min: identity suite debug
~7 min + rung release ~1 min + verdict).

1. The blocker's letter is false on shipped code, unmodified:
   `cargo test -p emergent-engine --test identity` → **9 passed, 0 failed, 435.76 s**
   (debug, shared box; per-scene tests, each one scene). The suite is `Chronon`
   (lockstep, dense) vs `EventCore` (sparse) over the frozen 8-scene ladder, with thread
   sweeps and its own planted negative — and it carries no `target_os` gate. Only
   `metal_identity.rs` / `metal_cost.rs` (the GPU arm) are `#![cfg(target_os = "macos")]`,
   and `lattice-metal`'s Linux stub is exactly that arm.
2. The rung, frozen at `r5-dense-order.md` before execution
   (`crates/engine/tests/r5_dense_order.rs`, the harness; `metrics.py`, the assembler):
   `R5_OUT=… cargo test --release -p emergent-engine --test r5_dense_order` → **10 passed,
   42.44 s**, rows in `rows/r5-*.json`, then
   `python3 lab/verdict.py r5-dense-order.md metrics.json` →
   **PASS; cpu-pair passed every criterion** (candidate 1.0/1.0, positive pass, negative
   `fail ident`). Cases: the frozen s0–s7 ladder verbatim plus two held-out draws
   (h1: 2500 bodies, q 512, seed 11, scattered, div 32, k 12; h2: 3000 bodies, q 2048,
   seed 12, formation, div 8, k 14). Coverage is real: contacts 82–51,464 per scene,
   epochs 17–4097, a live carry in every scene (tide kicks are being felt and rounded).
   The negative (kick one chronon late in one order) changed the world digest on every
   scene (e.g. h1 `ca1a44203f8a` → `032cb31c81ce`), and shifting both orders restored
   agreement 10/10 — the equality is about the order, not a law frozen out. And the
   equality is not coincidence: a second full execution of the harness wrote
   byte-identical rows (world digests, contacts, epochs, flags) — only the wall-clock
   fields moved.

**Predictions** (`predictions.md`, written before the run): P1 suite 9/9 on Linux — held;
P2 held-out h1/h2 identity — held; P3 negative breaks all, both-shifted restores all —
held; P4 no speedup claim — held (and inverted: sparse is the faster order here); P5 GPU
arm stays Mac-only — held (it is the stub, and the rung names it an M1 extension, not a
config).

**What would make it wrong.** The rung judges `Outcome` equality (world+log+tide digests)
on the CPU arm at battle scale; it does not touch the GPU arm (Mac-only), budget-starved
schedules (the sparse queue under load — the suite's steppers are single-threaded; only
the kick pass sweeps threads), or the field's libm channel (replay-gate: corpus
redifferentiation is an oracle-float disease; none of these digests pass through floats).
A later M1 run executing the GPU extension with different bits would kill the premise
proper, not this run's letter. Cost of adopting: one file (`r5-dense-order.md` into
`lab/rungs/`, the harness already lives behind the patch — the integrator may commit it
beside `identity.rs`); zero law changes; regen needs only cargo. Fit with PRINCIPLES:
measure before claiming (the blocker was claimed without running the ungated suite —
principle 10); "a test that cannot fail is a control" — the negative breaks 10/10, so
this one can fail (evidence §2); and the census's own lesson, "agreement between runs is
not independence": 13c6's blocker was the same misreading this page's standing record
made nowhere else — the dense order was conflated with its GPU implementation.

**The ranked attacks after this run** (the lens's deliverable; each with the rung that
should have caught it, or "none"):

1. **Kicks/derivatives "multiply-add" (L67, L114) — dead twice over**: cost (34.8–203 µs
   vs "~50 ns", 12db; 75.6 µs gold b063) and correctness (the jet's one-signed phase
   error, three golds, law.md L36). **No rung exists for per-kick cost** — B9/B10 gate
   counts and exponents only. The integrator's doc amendment (open direction 1) is the
   remaining fix.
2. **View at the past light cone — letter dead, r6 now guards cost/presence** (13c6);
   physics holes stand: multi-image (6eae), no time-transfer law (5977, gold), rotating-
   doll deflection key (8be2, gold). r6's criteria catch cost regressions; **no rung
   guards the time-transfer law** — a candidate r8-view-physics for a later run.
3. **Dense ≡ sparse (L70) — guarded and PASSING as of this run** (r5, CPU arm; the
   criterion `ident` catches any order divergence, and the negative proves it fails when
   it must). GPU arm: no Linux rung can exist; M1 extension specified in the rung file.
4. **Binet cells (L32) — superseded by the Darwin compilation** (law.md L20; r1v2
   executed, 79ed/cec1). Guarded by r1; remaining: m8 period tail, near-separatrix rows
   at m16/m32.
5. **Two-body doll 1PN (L37) — survives** (r3 v3, B11); the sub-p̄≈12M merger flank wants
   an NR-calibrated EOB (too heavy for a 60-minute run; left to the integrator's queue).
6. **Undisturbed ≈ 0 (L113) — survives by rate, not cost** (a4ed; 3294's one rebind per
   doll interval); the per-rebind cost is the frame-cost page's territory, not this
   lens's.

A premise that survived: the doc's §3 order split itself — sparse wins at battle scale on
CPU (28×/13× above), exactly where the doc claims ticks waste nothing only when
everything changes (the epoch-1 storm, where the two orders tie).

**The lens.** A red-team overweighting exotic cases would have chased the EOB flank or
the separatrix; the failure found here is administrative (a false blocker recorded as
fact on the page every author reads first), which the lens's "rank by what the player
sees" rule almost hid — the player sees nothing of r5, but the lab loses a rung's worth
of guarding per window while the blocker stands. What this lens may still have missed:
the budget-starved sparse schedule (slack order under load, not tested here) and the GPU
arm's own bits — both named in the rung as extensions.
