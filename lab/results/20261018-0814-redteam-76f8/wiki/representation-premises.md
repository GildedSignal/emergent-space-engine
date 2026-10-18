topic: representation-premises
status: open
closed-by:
valid-while:
updated: 20261018-0814-redteam-76f8

# The premises of docs/representation.md: a census against the record

## Current best
**The design doc teaches three dead letters and one unmeasured cost, and its perturbation
premise is refuted ~700× by shipped code, deterministically: the kick resolver costs a
median 34.8 µs (p99 53–63 over three runs) for plane bodies and 203.3–203.7 µs (p99
399–408) for handed-out members against the doc's "~50 ns each" (L114), and the memo the
cheap path needs hits 0.0% exactly (2262 rebinds, 2262 distinct keys) while the only
repeating key (the quantized 12+12-bit memo, 98.0% here) is the one law.md refuses (it
re-rounds every kick, a random walk) (20261016-1207-redteam-12db, `xtask universe
--kick-bench`, runs digest-identical, shared x86 — orders of magnitude; the M1 record:
43–52.8 µs c01c/0c44, 75–160 µs on the board, and the same refutation at gold grade:
**75.6 µs vs a 42–56 ns floor, ~1,800×, exact memo 0%** — 20261011-1729-components-b063,
the closest prior, measured six days before this census; leaver medians are
pace-dependent, 162–365 µs across the checker's arms — seeds 7/42, rtf 100–3000: 14,219
rebinds, zero exact reuse, made 34.6–35.4 µs, refused 0).** The premise is squeezed from
both sides: exact keys never repeat, the repeating key is not the law — so "a kick
updates the cycle by a multiply-add" (L67) has no shipped fast path and cannot get one
from memoization ("derivative prediction never substitutes for authoritative rebinding",
crates/space/ENVELOPE.md; the jet retired by three golds, law.md L36).

**NEW (76f8, premise red-team): the two-orders boundary (L70–76) is measured for the
first time — the premise survives but its constant is an order wrong and its example is
on the wrong side (20261018-0814-redteam-76f8, `crates/engine/tests/xdense.rs` on
shipped code, `Chronon` vs `EventCore`, digests asserted equal in every cell, 43–50 s,
shared x86, load 1.4–1.5).** Density-swept scenes (q = 1024, radius q/2 so the touching
floor is exact; c = 1 quantum/chronon, so a q²-cell's light crossing is one chronon):
lockstep first becomes cheaper than the sparse core at **ρ\* ≈ 0.15–0.2 contacts per
body per chronon = K ≈ 0.06–0.11 events per q²-cell per chronon — not the letter's
"near 1"** (crossover rows: 1.06× at ρ 0.129 → 0.85× at 0.204, v = q/4; 1.03× → 0.84×,
v = q/2; 1.36× → 0.84×, v = q/8), robust in N (400/1600/6400 → 1.25×/1.09×/1.09× at
fixed density) and stable in load (0.71–0.76 across two passes; ops bit-identical).
The domain it carves: a **confined grind at near-touching packing only** (spacing ≤
1.5q; max lockstep win 1.7× at touching, v = q/4, K 0.306). No battle-shaped scene the
author tested reaches it: the densest slam (1.5q) rides ρ = 0.041–0.045, **3.3–3.7×
short** (2.31–2.50× sparse-side; formation 1.71×), and the shipped battle scene's 5q
density is ~40× short (5.9× sparse-side here, consistent with r5's 28× with its empty
tail). Checker's domain facts (20261018-0814 check): the slam at touching packing
(s = 1.0q inside each fleet, denser than any author cell) still stays sparse-side —
ρ 0.080/0.083, lock/sparse 1.57×/1.12× — so the claim holds at the envelope, but the
margin there is **~1.8–2.4× short**, not 3.3×; N = 25600 at s = 1.5q gives 1.12×
(no flip 4× beyond the author's max), v = q/16 at touching lands exactly on the band
(ρ 0.172 → 1.02× par, confirming ρ as the governing variable below the author's
slowest speed), and T = 1600 shows the grind does not cool (ρ 0.129 → 0.121, 0.204 →
0.193; ratios 1.07 → 1.12, 0.84 → 0.88). At the game's
dominant density the certificate is overwhelming: an empty flight of 1600 bodies over
2080 chronons costs the sparse core 0.0002 s against lockstep's 1.037 s (**4,275×**;
the checker's regen: 4,382×, ops bit-identical; lockstep re-bins and sorts every body
every chronon, Ω(n log n · T), the sparse
calendar sits idle). Sparse's ops at the grind are 2.8× lockstep's (45.8M vs 16.5M) —
it does more, cheaper ops; lockstep wins on wall only inside the grind. Unmeasured and
named: the letter's own target hardware ("the GPU and NEON") — a vectorized lockstep
gaining 8–16× would push ρ\* toward ≈0.02–0.06 [inference], inside the densest battle
shapes; that is the M1-side run. Bonus domain: r5's digest property extended to 21
walled worlds (the r5 scenes are unwalled).

**NEW (e59e, premise red-team): the doc's observable set for the view is incomplete —
opacity is missing entirely, and the size of what the player sees wrong is measured
(20261017-2142-redteam-e59e, float falsifier, exact Schwarzschild null geodesics).**
§2 L53–59 lists the view's physics (clock, colour, aberration, lensing crossings,
blackbody, "Nothing bounces") with no capture rule and no occluder test; the shipped
gather is straight light (`view.rs` L15 "(no lensing yet)", verified). Exact shadow arc
(Synge α_sh = asin(√27·√(1−2/r_o)/r_o), verified against RK4 bisection to ≤4.2e-5 and
r1/B4's four capture cases 4/4): **1.64% of the 2-D sky at r_o = 100 M, 7.93% at 20 M,
exactly 25.0% at 6 M, 46.6% at 3.2 M** — fabricated rows inside it at N = 10⁴ sky
emitters: **164 / 793 / 2,500 / 4,662**. Opaque bodies: an occluder at 10 radii blocks
3.19% of the sky (319 of 10⁴ emitters drawn through it), at 2 radii (every planet
approach) 16.7% (1,667). The rim is not a perturbation: exact deflection 2.08 rad at
b = 1.1·b_c, 4.23 at 1.01, 6.51 at 1.001 (the analytic −ln(b/b_c−1)+ln[216(7−4√3)]−π),
so "memoized deflection(b)" (L57) has a domain ending at the rim and the letter is
silent on b ≤ b_c rows — either wiring (keep-straight / drop-on-None, the shipped
`deflection` returns None) fails eclipse parity. No rung, gate or criterion sees any of
it (r6's presence bar requires the rows occlusion must remove); Julien's conversation
names occlusion six times, including "eclipse status unchanged" as an invariant and
"check whether that null segment intersects the worldtube of an occluding planet"
(original-conversation.md L984/4283/4864/4872/5032/6450/7375) — dropped in the pivot's
rewrite without a recorded decision (it survived in September's approved-build-plan G6).

**NEW (22d1, premise red-team): the occlusion cure this page proposed — "static occlusion
is one interval test per row" — is the wrong law at the game's own velocities, in both
natural wirings (20261018-0035-redteam-22d1, exact 2-D flat geometry, e59e's scene).**
The snapshot test (occluder at frame time) mis-times every eclipse by the full light time
d/c — −2/−10/−100 s at d = 2/10/100 planet radii, speed-independent — and once
β·d/R ≳ 2 its occluded arc is a disjoint sky patch (Jaccard 0.000 at β 0.5–0.9 beyond 10R;
a planet at 2R passed at β 0.5 already sits at β·d/R = 1, Jaccard 0.401). The
render-consistent sprite wiring (everything drawn retarded, exact quadratic retarded time)
is **not** parity either, but through the arc, not the timing: the sprite sits at retarded
distance γd, so its occluded arc is the true arc shrunk by exactly 1/γ — centres coincide
(sprite direction atan(βγ) = true centre asin β) — arc Jaccard 0.855–0.875 at β0.5 and
0.42–0.45 at β0.9 (the 1/γ = 0.866/0.436 row deficit, plus edge asymmetry at close
approach), while its timing error is bounded O(R/β): onset +0.24…+0.62 s, rim +0.28…+0.44 s
across 2–100R. **The record now regenerates and the corrected physics is exact
(9ffc, second author): the onset instrument is fixed in the run's own script
(retarded-time quadratic on the worldline, not the current distance), every corrected
number reproduces, and each wiring is certified per row by closed forms — 0 mismatched
rows of 10⁴ in all 11 cells; onsets to ≤ 3.6e-12 s of W1 = −R/β, W3 = d − R√(1+β²)/β,
W2 = √(d²+R²) − R/β (error → (R/β)(√(1+β²)−1) ≈ Rβ/2), W2p = d − R/β; the true arc is
the static arc translated to −asin β (roots sinψ = [−β(d²−R²) ± R√(d²−β²(d²−R²))]/d²),
the sprite's is |sin(ψ+asin β)| < R/(γd) — Jaccard → √(1−β²) exactly; the run's
+1.25…+125.13 s onset column is confirmed dead as an instrument artifact (the tell —
two wirings converging — resolves: fixed +0.3855/+0.3809 s), P2 re-graded held-in-form;
W2p is killed under either reading of its letter (arc Jaccard 0.000 at 100R, or onsets
+15/+125 s if the offset uses the current distance); oblique W2 now measured
(Jaccard 0.9971/0.9341 at 45°, d 10R) and the oblique W3 predicate anchors at the
frame-time distance, not the perpendicular foot.** The naive per-row
offset (d·cosψ) is worse at speed: the
encounter retarded time carries the sweep factor (1+β²)⁻¹ (at β0.5: 0.784 vs the
sprite's 0.855 at 2R, 0.307 vs 0.865 at 10R, 0.000 at 100R). Only the exact per-row
segment-vs-worldtube test is the law — and it prices at **69–79 ns/row** (10⁵ rows ≈ 7–8 ms,
under the screen cap): the price premise was right, the geometry was wrong (principle 19).
Observer arm: the occluded half-arc appears at 17.58°/49.77° at β_O 0.5 (reproduces
check2's 17.6°/49.8° independently; −41%/+66% of static), while row parity itself is
frame-consistent (2/10⁴) — the failing observable is the seen arc size, so the parity gate
judges in the observer's frame at player β. Strong field: the sprite-consistent
differential Shapiro delay at r_o 20M, b 10.26M is 0.782 s = 19.6% of a β0.5 transit
(invisible at planet β); the naive no-cancel 8.66 s delay is not the observable. No rung
or gate sees any of it; the rung spec is below (direction 2).

The census, ranked by player visibility (the rest of this page's standing record):

1. **Kicks/derivatives (L67, L114): REFUTED** (above; no rung exists for per-kick cost —
   B9/B10 gate counts and exponents, the §7 ladder has no kick-cost falsifier).
2. **View at the past light cone (L56-59): letter dead, physics holes open — NOW GUARDED
   IN COST AND PRESENCE by r6, created and executed (20261017-1018-redteam-13c6):
   PASS for the shipped memo-carrying gather (rows 38400/38400, median 2.0
   readouts/emitter, p99 2.92 on stream content at β 0.5–0.9999, observers β 0–0.9,
   60 Hz rtf 100); the no-memo cold path KILLED (median 3.66, p99 6.0, 12/38400
   emitters silently dropped — checker's correction: the drops are root_state read
   failures at ticks the from-the-present walk probes (emitters 32/33 at frames
   118–119; an independent bisection fails the same rows; warm resolves them), not
   64-iteration exhaustion on racing crossings);
   "any cache, however stale or foreign" KILLED as a cost claim (poisoned caches:
   same rows, p99 5.13); the amnesiac-memo negative fails as required. The historical
   1.5 clamp (4570) does not separate — at 60 Hz × rtf 100 a 0.999c closing stream
   races through its approach inside one frame (dt_e/dT = 10³): physics kills that
   negative. Checker's correction:
   r6's named hole closed by the checker at the frozen scale itself: an independent
   bisection oracle agrees with warm's ticks on 23,170/23,170 post-light rows
   (bracket violations 0.07% at eps 1e-3; at ~10⁶ root units 35,578/35,578, 0.13%)
   — the author's "40% of identically-correct rows fail from ±1–2 ticks of f64
   noise" was the pre-light tick-0 fallback fraction (15,230/38,400 = 39.7%), a
   semantics bug in the withdrawn oracle, not a noise floor: tick exactness is
   freezable at game scale now. Checker's domain facts: at rtf 10 nothing
   separates (cold passes every bar; the amnesiac negative passes → VOID);
   at rtf 1000 warm itself drops 20.9% of rows; on a 360-frame window at the same
   cadence warm fails its own presence bar (0.986, drops from frame 178); at
   β 0.6 cold/amnesiac still fail (separation is not confined to β ≳ 0.9); warm
   holds at β 0.99999 and N=512. Cold-seed weakness prior: 0fe0 (12 Oct) already
   had "cold seeds leave the bracket at β ≥ 0.9".**
   100% of azimuths at r_o 100–3.2 M, 20261011-1234-redteam-6eae); no time-transfer law
   (flat light-time off 2–176° within ~50 M, 20261011-0924-redteam-5977, gold);
   deflection key broken for rotating dolls (20261010-2052-redteam-8be2, gold);
   **and opacity/capture absent from the premises entirely (e59e, above) — the one
   hole in this list with no shipped half and no rung, at measured 16.7% of the sky
   on an ordinary planet approach.**
3. **Binet cells "the primary in-cell solution" (L32): replaced 30 September by the Darwin
   compilation** (law.md L20: the band map's tangents carry a first-order slope error in
   every turning cell); research rehabilitation partial with four broken instrument
   channels (→ binet-cells).
4. **Two-body doll 1PN, ν only in the energy map (L37): SURVIVES** (r3 v3: precession
   1024/1024, periods 632/632, assists 64/64; B11) — licensed domain now measured:
   p̄ ≳ 65M at ν ≤ 0.25 (→ handoff, 97b0).
5. **Dense ≡ sparse (L70): SURVIVES in the lab** (tie rule 20261005-0543-redteam-6254,
   batch rule, locality licence, B8) — unguarded in the field (→ replay-gate); **NOW
   GUARDED BY AN EXECUTED RUNG ON LINUX: r5 created, frozen and PASSES
   (20261017-1330-redteam-68e7) — the dense order is not only Metal: its CPU arm
   (`Chronon`) is portable, the shipped `engine/tests/identity.rs` suite runs 9/9 on
   this Linux box (435.76 s, debug), and the r5 rung (frozen at
   `lab/results/20261017-1330-redteam-68e7/r5-dense-order.md`) holds 20/20 identical
   Outcomes (10 scenes × threads 1, 4; the frozen s0–s7 ladder plus two held-out
   draws: 2500 and 3000 bodies; 116,874 contacts, kicks and live carries in every
   scene), the both-shifted positive control agrees 10/10, and the one-order-late
   negative breaks 10/10. Only the GPU arm (`MetalChronon`, macOS-gated) stays with
   an M1-side run. Bonus, orders of magnitude only (shared box, release): the sparse
   event core beats lockstep 0.27 s vs 7.54 s at 2500 bodies and 0.84 s vs 10.80 s at
   3000, equal only on the epoch-1 storm scene.**
   Checker's domain facts (20261017-1330 check): identity holds beyond the rung's frozen
   domain — 4000 bodies (27,957 contacts, epochs 513), horizon 8192 (epochs 1025), a
   q 256 / div 4 / k 9 near-storm (epochs 2049, 7085 contacts), and cross-thread pairing
   the rung never gated (lockstep t1 ≡ sparse t4 and t4 ≡ t1, lockstep t1 ≡ sparse t8 at
   all three scenes); the epoch shift changes each order's outcome, so the negative is a
   law change, not a no-op. The checker's full regen reproduced metrics byte-identically
   (identity 1.0/1.0, late 0.0, contacts 116,874; suite 9/9 at 463 s debug).
   **Budget axis guarded (20261017-1447-second-20261017-1330-redteam-68e7-506c, the
   check's named gold experiment, rung r5-starve frozen then executed: PASS):** every
   schedule, budget and thread count pops the same sequence — starved sparse (budget 1
   and seeded 1..=97, up to 1.2×10⁷ advance calls in one battle) ≡ unbounded lockstep,
   starved lockstep ≡ unbounded sparse, cross-thread starved t4 ≡ t1, and the same
   seeded stream under 3 spinning hogs ≡ unloaded (11/11 scenes, incl. held-out 3500
   bodies; slow 1.2–1.7×, so the load was real; 10/10 world digests equal the
   checker-verified 68e7 rows). The allocator hosting `EventCore` regions under its own
   least-slack schedule with one-event budgets, sabotage and 1/8 workers (27 cells;
   rollbacks racy at 8 workers, identity either way) merges to exactly one `Chronon` per
   scene. Scheduler metadata (units/merges) is wall-fed by design under calibrated budgets
   and worker races — digests never move; no rung should gate on it. Both-shifted starved
   agrees 11/11; one-order-late breaks 11/11. Coverage is per config now (the check's
   note 3). Remaining unguarded: only the GPU arm (M1-side).**
   Checker's domain facts (20261017-1447 check): identity holds beyond the rung's frozen
   domain — 4000 bodies starved (both orders, 27,957 contacts), budget spans 997 and
   65535 (rung span 97), budget 1 + 3 hogs + 4 threads combined (the dossier's named
   untested case), an alternate budget-stream seed on the 3000-body formation, and the
   allocator's `heavy_tail` scene class (giant gas region + 16 islands; budget 1,
   sabotage, 8 workers, plus fixed-budget-1 under 3 hogs — 2,581 contacts, every cell
   one `Chronon`). Full clean-tree regen: PASS, battle rows byte-identical across three
   executions, 0 digest flips; slow_min 1.11–1.33 across executions (the quoted 1.2–1.7
   band is per-execution wall variance, as the dossier itself says).
   Second check (20261017-1447 check2), independent arms: identity holds at horizon 8192
   under starvation (h3deep 31,499 contacts, 27.2M budget-1 calls; s7deep 93,659 contacts,
   epochs 8193), with both orders starved at mismatched threads (lockstep-f1-t4 ≡
   sparse-rand-t8), and in 12/12 allocator cells at odd workers {3,5}, fixed budgets {3,7}
   and a different sabotage seed. Domain fact: `Chronon` floors the budget axis at one
   chronon (starved calls = horizon exactly, whatever the budget) — the dense order's
   budget clause is satisfied at its granularity floor, so the budget attack surface is
   the sparse queue and the allocator, which are where the slicing was measured.
   **Cost half now measured too (76f8, above): the CPU-arm crossover sits at ρ\* ≈
   0.15–0.2 contacts/body/chronon (K ≈ 0.1, not the letter's "near 1"); battles ride
   1.8–40× below it (checker's touching-slam arm at the near edge); empty flight is
   4,275× sparse-side. The GPU/NEON arm's crossover
   is the open M1-side question.**
6. **Undisturbed ≈ 0 (L113): SURVIVES by rate, not by cost** (a4ed gold: belts pass 10⁹ at
   10× real time; but fire rate 1.000, one rebind per doll interval, 20261015-0724-system-3294).

## Refuted

- **"Dense: where that number is near 1" (L72), as the engagement rule for the CPU arm, and
  battles as its example ("the normal case of many necessary interactions in a short
  time")**: the measured crossover is K ≈ 0.06–0.11 events per q²-cell per chronon
  (ρ\* ≈ 0.15–0.2 contacts/body/chronon) — an order below "near 1" on the q² reading
  (a q²-cell's light crossing is exactly one chronon at c = 1 quantum/chronon); on the
  Chronon's own adaptive cell (~2q at v = q/2) the boundary is K ≈ 0.2–0.4, ~3× below
  "near 1" — either way below the letter, whichever cell it meant. No battle-shaped
  scene reaches it: densest author slam ρ = 0.045, 3.3× short; the checker's
  touching-packing slam (s = 1.0q per fleet) ρ = 0.083, ~1.8–2.4× short, still
  sparse-side (1.12–1.57×); the shipped battle scene ~40×
  short. Inside the physical range only a confined grind at near-touching packing
  (spacing ≤ 1.5q) crosses; engaging lockstep below ρ\* costs 1.06–28× more than the
  sparse core (20261018-0814-redteam-76f8). The two-orders premise itself survives —
  see Current best; what dies is the constant and the example.**
- **"§2's observable set is the view's physics" (representation.md L53–59, the list
  every view run inherited): opacity is missing — no capture rule, no occluder test —
  and the player sees through black holes and planets at measured rates (16.7% of the
  sky at a 2-radii planet approach; 25.0% inside the shadow arc at r_o = 6 M)
  (20261017-2142-redteam-e59e; the shipped gather is straight light, `view.rs` L15).**
- **"Static occlusion is one interval test per row" as the occlusion law** (this page's
  direction 5 as stated, and any snapshot or sprite wiring of it): the snapshot errs by
  the light time d/c (2–100 s) and goes arc-disjoint at β·d/R ≳ 2; the exact sprite's
  arc is the true arc shrunk by 1/γ (Jaccard 0.42–0.88 at β 0.5–0.9) with timing error
  bounded O(R/β) (checker-corrected; the run's "+125 s, unbounded in d" onset column was
  an instrument artifact, not physics); the law is the per-row worldtube test, 69–81 ns/row
- **"A kick updates the cycle by a multiply-add" as a cost claim** (representation.md L67 +
  L114): three golds killed the jet (20261006-1249-redteam-4978,
  20261008-1757-second-…-0ccd-b33f, 20261012-1227-second-…-4808-d617, via law.md L36), and
  **the same refutation was already measured at gold grade: 75.6 µs vs a 42–56 ns floor,
  ~1,800×, exact memo 0% (20261011-1729-components-b063)**; the census run regenerates it on
  shipped code (34.8 µs median, exact memo 0.0%) — the doc still teaches it.
- **"The Hashlife memo premise as an operating fast path"** ("identical invariants share one
  memoized cycle"): exact_hit_rate 0.0 at 2262 rebinds, digest-stable (the census run;
  checker's held-out arms seeds 7/42, rtf 100–3000: 14,219 rebinds, zero reuse), after 0/203,017
  (20261010-1544-system-97ce) and 0/3,225 (20261013-2005-quant-7055); the quantized
  alternative is a refused law change (law.md L36; taste log 5 Oct).
- **"Each visible tube crosses the observer's past light cone once"** (6eae, silver):
  2–4 images near masses.
- **"The cold no-memo gather as a row-complete fallback"** ("every crossing found from
  scratch", view.rs): 12/38400 emitters dropped at β 0.999–0.9999 Toward, deterministic —
  checker: root_state read failures at ticks the from-the-present walk probes (an independent
  bisection fails the same rows; warm resolves them), not budget exhaustion; killed by r6
  (20261017-1018-redteam-13c6).
- **"Any cache, however stale or foreign" as a cost claim** (view.rs doc, representation.md
  §2 "shortcuts… add speed, never error"): true for the view's rows, false for its cost —
  stale/foreign caches pay p99 5.13 vs the kept cache's 2.92 (20261017-1018-redteam-13c6).
- **"r5 remains uncreated and cannot be created in this lab … `lattice-metal`'s dense order
  is `#[cfg(target_os = \"macos\")]` and compiles to a stub on Linux — an M1-side run owns
  it"** (13c6's blocker, this page before this run): a category error — the dense order is
  "CPU, or Metal on the GPU" (law.md L50), and the CPU arm (`Chronon`) is portable; the
  shipped identity suite runs 9/9 on Linux and the created r5 rung PASSES 20/20 with its
  negative breaking 10/10 (20261017-1330-redteam-68e7). What is Mac-only is the GPU arm.

## Open directions
1. **The integrator's one-pass amendment of representation.md** (no code): strike L67/L114
   for the recorded 43–160 µs and rebind-per-kick; relabel Binet cells as research;
   annotate "crosses once" (the "mark r5 uncreatable off-Mac" clause is dead — see
   Refuted); **new (e59e): add opacity to §2's observable list — capture arcs (Synge's
  closed form, valid r_o ≥ 3 M: inside the photon sphere the blocked fraction is the
  complement, 62% of the sky at 2.5 M — checker bisection) and occluder worldtubes —
  and fix L28's spoke count (N = 2πm/ln2 = 145 at m = 16, not 128). Until then every
  new reader is seeded with refuted premises (principles 10 and 19, applied to the
  document).** **New (76f8): correct L72's engagement constant — "near 1" → K ≈ 0.1
  events per q²-cell per chronon (ρ\* ≈ 0.15–0.2 contacts/body/chronon, CPU arm) —
  and move the letter's dense-regime example from battles to confined grinds at
  near-touching packing (battles ride 3.3–40× below the line).**
2. **Commit r6** (`lab/results/20261017-1018-redteam-13c6/r6-view.md`, frozen hash
   recorded, checker silver): the view's cost and presence are now guardable mechanically
   at rtf 100; the next rung is exactness, and the checker's bisection oracle already
   certifies warm's ticks 23,170/23,170 at the frozen scale — no smaller scene needed —
   **new (e59e): the rung that does not exist is eclipse parity — rows whose retarded
   null segment meets an occluder's worldtube must be absent, emitters near the rim
   present via their true deflected images; negative control = the shipped straight
   gather (must fabricate at e59e's measured rates). The wiring decision (keep-straight
   vs drop-on-None at b ≤ b_c) must be frozen before lensing lands: both fail parity.**
   **22d1's frozen form, bars now exact (9ffc): the occlusion predicate is the per-row
   worldtube test (the snapshot and sprite wirings are the negative controls — the
   snapshot must mis-time by d/c − (R/β)(√(1+β²)−1) and go arc-disjoint at β·d/R ≳ 2;
   the sprite must show onset error exactly (√(d²+R²) − d) + (R/β)(√(1+β²)−1) and arc
   Jaccard √(1−β²) at d ≥ 10R — transverse cells only, checker2's sweep: the per-row
   predicates stay exact over 20–135° at β 0.5–0.9 (0 mismatches), while oblique
   Jaccards run higher away from transverse (0.46–0.99, meeting the transverse
   √(1−β²) at 90°) and are judged
   by the per-row predicate; the per-row offset must fail on the arc, Jaccard ≤ 0.31
   at 10R β0.5 → 0 at 100R, whichever distance its letter uses); judged in the
   observer's frame at player β (arc sizes 17.6°/49.8°, not 30°), plus onset/egress
   times within one frame at β·d/R ≤ 1 and a duration-distortion bar ≤ 5% at the
   strong-field scene.**
   ("no lensing yet") — freeze the absence half now, the rim-presence half with the
   lensing memo.
3. **Adopt r5 and r5-starve into `lab/rungs/`** (`lab/results/20261017-1330-redteam-68e7/r5-dense-order.md`
   and `…-506c/r5-starve.md`, both frozen before execution, both PASS): the CPU arm is
   guarded on every axis this lab can reach — orders, threads, budgets, sabotage and
   competing load; what remains M1-side is only the GPU extension (`MetalChronon`
   configs and `metal_identity.rs`'s scenes, same criteria, starved wrapper included).
   **New (76f8): the cost half is now one freeze away — `xdense.rs` is the instrument
   (criterion shape: the crossover row must sit at ρ ∈ [0.1, 0.3] with the slam and
   miss controls on their named sides, ≥ 2× each); the M1 run that matters is the same
   sweep on the NEON/Metal arm, whose crossover an 8–16× vector gain could move inside
   the battle shapes [inference].**
4. The EOB strong-field flank: closed by 97b0's oracle (→ handoff); the merger scene's
   licence below p̄ ≈ 12M still wants an NR-calibrated EOB.
5. **~~Price the moving-occluder eclipse~~ MEASURED (22d1): the price premise was right
   (69–79 ns/row, ≈7–8 ms at 10⁵ rows — not the bill) and the geometry was wrong.** The
   occlusion law is the per-row segment-vs-worldtube test; delay(b) (5977's missing memo)
   enters as the sprite-consistent differential (0.782 s, 19.6% of a β0.5 transit at
   r_o 20M — a duration-distortion bar for the rung), not as the naive 8.66 s delay.
   Check2's aberrated arcs (17.6°/49.8° at β_O 0.5) reproduce independently (17.58°/
   49.77°); row parity is frame-consistent — the gate judges the seen arc size and the
   onset/egress times, in the observer's frame at player β. Unmeasured: occluder and
   observer moving together, extended occluders (fleet dolls), aggregate emitters
   (partial dimming, not row drops).
6. **[New, 76f8] The mixed-world question the crossover opens:** the boundary's use is per
   region (a grind inside a sparse world), which is the allocator's call — a world that
   holds both a grind region and empty flight pays the 4,275×-side and the 1.7×-side at
   once. The allocator's region-splitting at ρ\* is unmeasured, and is where this
   premise meets the board's allocator bottleneck.

## Contradictions

None. The doc's provisional status ("DRAFT … supersedes nothing until the falsifiers in §7
have run") is kept beside the census: the letter is refuted, the status line was honest
about it; both stand. e59e's opacity entry in Refuted targets the observable-set reading
(the list every view run treated as complete), while the doc never asserts completeness
in so many words — the gap is against Julien's conversation, not against a written
falsehood; the nuance is recorded here, the entry stands. 76f8's L72 entry kills the
constant and the example, not the two-orders premise; both are recorded side by side
(the premise survives with a measured domain, per Current best).

## Runs
- 20261016-1207-redteam-12db (silver): premise census; kick cost 34.8 µs vs the doc's
- 20261017-1018-redteam-13c6 (silver): r6 created, frozen and executed — PASS for the
- 20261017-1330-redteam-68e7 (awaiting grade): r5 created and PASSES on Linux — dense≡sparse 20/20, the "uncreatable here" blocker refuted; GPU arm stays M1-side
- 20261017-1447-second-20261017-1330-redteam-68e7-506c (awaiting grade): r5-starve frozen and executed — dense≡sparse holds under starvation and load, 11/11 + 27 allocator cells, allocator arm first for EventCore
- 20261017-2142-redteam-e59e (awaiting grade): opacity missing from the view's premises — stars through planets (16.7% of sky at 2R) and black holes (25% at r_o 6M); no rung sees it
- 20261018-0035-redteam-22d1 (silver, checker-corrected): the occlusion cure measured —
- 20261018-0143-second-20261018-0035-redteam-22d1-9ffc (awaiting grade): instrument fixed in the run's own script; every corrected number regenerates, closed-form certified per row (0 mismatches, onsets to 1e-12 s); the W2 deficit is the 1/γ arc exactly
- 20261018-0814-redteam-76f8 (awaiting grade): the two-orders crossover measured on the
  CPU arm — ρ\* ≈ 0.15–0.2 contacts/body/ch (K ≈ 0.1, not "near 1"); battles 3.3–40×
  short of it, confined grinds only; empty flight 4,275× sparse-side; all five
  pre-registered predictions held
