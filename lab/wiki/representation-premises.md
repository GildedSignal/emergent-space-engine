topic: representation-premises
status: open
closed-by:
valid-while:
updated: 20261018-1433-redteam-915d

# The premises of docs/representation.md: a census against the record


**NEW (915d, premise red-team): the additive-attitude premise is dead at the game's own
speeds — thesis 3 ("its change is an addition") and L50 ("thrust grows the rapidity linearly
in proper time"), as shipped in `thrust.rs`'s `owed` accumulator ("The heading turns by
±turn·Δτ"), cannot store the non-abelian part of SO(2,1): the frame rotates by exactly
(γ−1)·ψ for a constant-γ turn through ψ — certified at every grid point to 0.02° over
β 0.05–0.99 (γ to 7.09), with the two-boost Wigner angle matching its closed form
2·atan(tanh²(φ/2)) to 3e-14 and both controls (collinear, pure turn) reading exactly 0
(20261018-1433-redteam-915d, exact SO(2,1) exponentials vs the shipped law replicated
verbatim in the flat limit; the only modeled difference is where the thrust direction comes
from). The seen sky (`view.rs` L309 aberrates with velocity only, "the heading axis is the
page's") and the thrust direction both miss it, and it feeds back into the trajectory at the
record's own flights: off45 burn from γ 2 — nose 12.1° off, position 6.6% of path; off135
brake from γ 2 — nose 55.8° off, final speed off 0.27 c, position 22.3%; an open-loop turn
to reversal at γ 2 — nose 73.2° off, velocity direction 133.4° off, position 48.2%. A 180°
reversal at γ 2 rotates the whole starfield by 180°; one holding loop at β 0.6 by 90°.
Predictions 9/10 held (P6 missed honestly: the off45 brake turns the sky only 18° over its
whole flight, not >30° before 90° of velocity turn — the big angles belong to real turns).
No rung, gate or criterion sees any of it (§7 has no attitude/thrust rung; the bar to freeze:
a turning flight at γ ≥ 1.1 must carry (γ−1)ψ in sky and nose; negative control = the
accumulator, missing by exactly (γ−1)ψ). The cure is the doc's own §1 L40 (unit
split-quaternions: one multiply per burn) plus principle 6 (a held burn is a one-parameter
subgroup — a generator, closed-form and cheaper than the per-flush composition it replaces);
same disease as e8f7's doll keys ("compose boosts, not sum shears") — this run is the owner
its "Wigner axis error… owned by the spatial turn machinery if anyone's" asked for: the
machinery is the player's own flight.**


**NEW (1885, premise red-team): the aggregate readout premise is dead at high γ and its
failure is a closed form in the rapidity dispersion — "Aggregates are one sample each…
about one sample per pixel" (L59, L116) with "beaming k⁴, which in log form are
additions… a type × log k table gives the sprite" (L58) is refuted in the flagship
regime and safe only where nothing relativistic flies (20261018-1126-redteam-1885,
exact-SR float; the fleet model is exact, not a toy: for approach k = e^φ, so a LOS
velocity dispersion σ_β is a rapidity dispersion s = σ_φ = γ²σ_β and ln k is exactly
normal — every arm lognormal by construction, per-arm analytic assertion passed 12/12).
At β 0.9 with σ_β 0.03: one-sample sprite error median 40% (p90 86%), frame-to-frame
strobe 58%/frame, samples for a 5% flux bar 196; at β 0.9/σ_β 0.05: 63% median,
strobe 2.6×/frame (94%/frame), 799 samples, colour band off 28% median; at β 0.99/σ_β 0.01:
**the top 1% of members carry 37.2% of the fleet's seen flux** (top 0.1%: 13.6%) —
principle 20's crushed tail made physical — and the 5% bar needs 1.7×10⁴ samples.
Closed forms (checker2: CV and log-word exact for the lognormal arms, per-arm assertion
<0.02; strobe ≈ 4s itself a loose coefficient — exact half-normal median 3.82s — and
verified within 6–10% at s ≥ 0.25): CV(k⁴)=√(e^{16s²}−1), log-word miss e^{8s²}, strobe ≈ 4s,
visibility boundary s* ≈ 0.005 ⇔ σ_β* = 0.005/γ² (0.095% of c at β 0.9). The player's
own motion alone breaks it with ZERO internal dispersion: β_O 0.5, a static formation
spanning ±0.05 rad at 90° — 7% error, 9%/frame strobe, 88% of frames above 2%
contrast; β_O 0.9 same crowd: 12% (p90 30%)/16% (gone dead ahead, exactly d ln k/dθ). Controls:
Newtonian k=1 under-reports the β 0.9 fleet 628×; the belt control (β 10⁻⁵, σ_β 10⁻⁵)
reads all zeros — the premise is safe exactly where B18 tests it, i.e. the belt rung's
regime hides the failure (predictions 9/10 held, the miss conservative). No rung judges
a seen value (r6 gates per-emitter cost/presence; B18 gates storage at β ≈ 0; 2fa4's
"no gate judges a seen value" extended to the aggregate readout with magnitudes).**
**Checker (independent, additions only): the refutation is parameterization-robust and
the table's numbers are lower bounds — a velocity-Gaussian fleet at the same σ_β is
worse than the rapidity-Gaussian model (measured s runs 17–40% above γ²σ_β, artanh
curvature; CV(k⁴) 165–609 where the closed form gives 0.9–2.3; top-1% share 98–100% at
β 0.9/σ_β 0.05), the boundary collapses beyond the swept grid (σ_β* = 1.0×10⁻⁵ c at
γ 22.4, 1.0×10⁻⁶ at γ 70.7, held-out direct-β draws; β 0.999/σ_β 0.0003 already sits
at s 0.18), and the "samples for 5%/2%" columns are a 1σ scale — a p99-within-5% bar
(the criterion proposed below) needs ×6.6 more (5,422 at s 0.263, 600 trials). Strobe
figures are median |Δ ln F|: "58%/frame" is ×1.79 linear, "5.7×" already linear.**
**Checker2 (independent): reproduced bit-exact (regen.sh; every table number matches
results.json). Confirmed outside the swept range (γ 22.4, β 0.999): s = γ²σ_β holds to the
digit (σ_β 10⁻⁴ c → s 0.050, 14% one-sample; 3×10⁻⁴ → 38%), receding mirrors approach
(40.3% at s 0.158), a bounded uniform-rapidity crowd fails as hard (72.5% at s 0.263), and
a two-squadron bimodal formation with ZERO internal dispersion still errs 41% median
(square-wave strobe: the median-|Δln F| statistic reads 0 for bimodal crowds — use the
>2%-visible fraction there). One domain limit on the observer arm: its σ_θ is the whole
crowd's span, valid when the crowd is one aggregate (the letter's own reading); if
aggregates were re-clipped per pixel, σ_θ per aggregate is bounded by the pixel FOV
(~1.5 mrad) and the pure-angular observer arm falls to 0.4–0.7% at β_O 0.9 — the
LOS-dispersion fleet arms are untouched by that clipping (velocity dispersion survives
pixel subdivision). Dossier nit: the boundary at β 0.5 is 0.4% of c, not 0.7%.**

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
6. **Undisturbed ≈ 0 (L113): SURVIVES by rate, not by cost** (a4ed gold: belts pass 10⁹ at
   10× real time; but fire rate 1.000, one rebind per doll interval, 20261015-0724-system-3294).

## Refuted
- **"Every quantity is kept in the form in which its change is an addition" + "thrust grows
  the rapidity linearly in proper time" as the attitude law** (representation.md thesis 3,
  L50; shipped as `thrust.rs`'s heading accumulator): boosts do not commute
  ([K_x,K_y] = −J), the missed commutator is the Thomas/Wigner rotation, exactly (γ−1)·ψ
  per constant-γ turn through ψ, and it corrupts the seen sky, the nose and (through the
  burn direction) the trajectory — 12–74° nose error, up to 0.27 c and 48% of path inside
  single maneuvers at β ≥ 0.866; the cure (unit split-quaternion per thrusting body, a
  generator per held burn) is the doc's own §1 algebra and cheaper than what it replaces
  (20261018-1433-redteam-915d).

- **"§2's observable set is the view's physics" (representation.md L53–59, the list
  every view run inherited): opacity is missing — no capture rule, no occluder test —
  and the player sees through black holes and planets at measured rates (16.7% of the
  sky at a 2-radii planet approach; 25.0% inside the shadow arc at r_o = 6 M)
  (20261017-2142-redteam-e59e; the shipped gather is straight light, `view.rs` L15).**
- **"Aggregates are one sample each… ~1 sample per pixel" + "beaming k⁴… in log form
  additions… a type × log k table gives the sprite" as the aggregate readout law**
  (representation.md L58–59, L116): a point k cannot express a crowd's k⁴-moment; at
  β 0.9/σ_β 0.03 the one-sample sprite errs 40% median and strobes 58%/frame, the
  shared log-word under-reports by e^{8s²}, and at β 0.99/σ_β 0.01 the top 1% of
  members carry 37% of the seen flux; safe only at s = γ²σ_β ≲ 10⁻⁴ (the belt regime
  B18 tests) — the visibility boundary is σ_β* = 0.005/γ²
  (20261018-1126-redteam-1885; closed forms, exact-SR instrument, controls both sides).
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
  document).**
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
6. **A seen-flux rung for aggregates (1885's freeze-ready criterion), and the moment
   representation beside the sample:** at β_bulk 0.9, σ_β 0.03, an aggregate drawn from
   10⁶ members must match Σk_i⁴ within 5% at p99 over 60 frames with |Δ ln F| < 2% at
   95%; negative controls: the one-sample readout (must strobe ~58%/frame) and the
   shared-log-word readout (must sit at −18%); observer-motion arm: β_O 0.9, a static
   crowd at ±0.05 rad must hold 2% (one-sample fails at 16%/frame). The design's own
   cure for smooth programs is derivation (the belt program's k-moments in closed form —
   "nothing is evolved that can be derived when looked at"); for real crowds the readout
   law must be s-aware (sample count ∝ CV(k⁴)², or tracked observer-dependent moments —
   unpriced, deserves its own run). Amend L58/L59/L116 with it when the integrator next
   touches the doc (folds into direction 1).

## Contradictions

None. The doc's provisional status ("DRAFT … supersedes nothing until the falsifiers in §7
have run") is kept beside the census: the letter is refuted, the status line was honest
about it; both stand. e59e's opacity entry in Refuted targets the observable-set reading
(the list every view run treated as complete), while the doc never asserts completeness
in so many words — the gap is against Julien's conversation, not against a written
falsehood; the nuance is recorded here, the entry stands.

## Runs
- 20261016-1207-redteam-12db (silver): premise census; kick cost 34.8 µs vs the doc's
- 20261017-1018-redteam-13c6 (silver): r6 created, frozen and executed — PASS for the
- 20261017-1330-redteam-68e7 (awaiting grade): r5 created and PASSES on Linux — dense≡sparse 20/20, the "uncreatable here" blocker refuted; GPU arm stays M1-side
- 20261017-1447-second-20261017-1330-redteam-68e7-506c (awaiting grade): r5-starve frozen and executed — dense≡sparse holds under starvation and load, 11/11 + 27 allocator cells, allocator arm first for EventCore
- 20261017-2142-redteam-e59e (awaiting grade): opacity missing from the view's premises — stars through planets (16.7% of sky at 2R) and black holes (25% at r_o 6M); no rung sees it
- 20261018-0035-redteam-22d1 (silver, checker-corrected): the occlusion cure measured —
- 20261018-0143-second-20261018-0035-redteam-22d1-9ffc (awaiting grade): instrument fixed in the run's own script; every corrected number regenerates, closed-form certified per row (0 mismatches, onsets to 1e-12 s); the W2 deficit is the 1/γ arc exactly
- 20261018-1126-redteam-1885 (awaiting grade): the aggregate one-sample readout refuted
- 20261018-1433-redteam-915d (awaiting grade): additive attitude refuted — the Thomas
