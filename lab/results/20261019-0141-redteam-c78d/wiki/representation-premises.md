topic: representation-premises
status: open
closed-by:
valid-while:
updated: 20261019-0141-redteam-c78d

# The premises of docs/representation.md: a census against the record

**NEW (c78d, premise red-team): the aggregate-readout letter's occlusion half is refuted —
"Aggregates are one sample each, and the screen caps the work at about one sample per
pixel" (L59; the same row at L116) makes every fleet-scale eclipse all-or-nothing: one
sample = one occlusion predicate, so a fleet larger than the planet it passes behind is
shown TOTALLY GONE for the sample's eclipse window while its flux stays visible —
measured mid-transit error 89.1% at R_f = 3·R_p (exactly 1 − (R_p/R_f)²) and 99.0% at
10·R_p, error > 80% for exactly the sample's eclipse width 2·R_p inside an 8·R_p transit,
f_true never below 0.889/0.989, 67% of the transit above 5% error; the blink survives the
exact retarded-time + 3D segment-vs-disc predicate with k⁴ beaming at β 0.5 (f₁ = 0 while
53.5% (transit-plane; deeper ships sit deeper in the shadow cone, 46% truly occluded) and
81.5% (sky-plane, peak 0.835) of the seen flux is visible); R_f = R_p peaks 60.5% at the
limb step; the artifact is sample-choice-invariant (random member: whole-fleet blink at a
random phase, path peak 0.305). The channel is ORTHOGONAL to 1885's dispersion refutation:
it fails at β = 0 with a perfectly uniform fleet — the exact regime where 1885's belt
control read all zeros; the two refutations bracket the one-sample rule from both sides.
The cure is the same line's second clause, priced: per-pixel sampling at R_p/2 → 145
samples, peak 3.0%; R_p/8 → 1957, 0.46%; or zero extra samples via the circle–circle
overlap closed form (max deviation 0.003 against a 10⁵-ship exact MC — the occluded
fraction of a uniform-disc aggregate is derivable, principle 3). Safe domain: R_f ≲ 0.1·R_p
in DURATION (1% of transit above 5%) but never in peak (a limb-crossing flash of
~0.5·fleet-flux for ~2R_f/v exists at every size); grazing impacts (0.7·(R_p+R_f)) show a
missed eclipse instead (true 6.7% dimming, one-sample none) — the blink needs impact <
R_p, i.e. the common central transit. No rung sees it (verified: no file in lab/rungs/
mentions occlusion or eclipse; r6 gates per-emitter cost/presence); freeze-ready
criterion in the dossier, folding into direction 2's eclipse-parity rung as its aggregate
arm — direction 5's "aggregate emitters (partial dimming, not row drops)" tail is hereby
measured (20261019-0141-redteam-c78d; predictions 6 of 10 held, every miss sharpened the
domain: P2 peak, P5 peak band, P6 sample-choice, P10 grazing form; one disclosed
instrument fix — the β arm's first window missed the seen transit's light-time shift).**

**Checker (independent; regen byte-identical, adversarial arms 8 s, and a
reimplementation of the β arm reproduces f_true_min = 0.535 exactly):
the refutation extends beyond the author's sweep — taleb-09b5's own fleet shape (a
400-ship arc formation, r = 3·R_p, 60°) errs 1.000 (centroid behind, every ship
visible), as does a ring annulus (peak 1.000); the next decade R_f = 30·R_p reads
0.9991 (law 0.9989); at β 0.9 the blink persists in both orientations (peaks
0.695/0.856, f₁ = 0 while f_true > 0.5). The CURE's domain is narrower than the
dossier's "cheapest cure" phrasing: the circle–overlap closed form assumes a uniform
disc at β → 0 — it errs 11.1pp on the ring, 24.1pp on the arc, and 10.4–31.3pp at
β 0.9 (transit/sky) against the exact Σk⁴ truth, so at player β the licensed cure is
per-pixel exact predicates (the criterion's "within 5% of exact Σk⁴ at player β"
already enforces this). The 690× compression is density-dependent: a 400-ship
formation pays more per-pixel samples (145–1957) than per-ship predicates (400).**
**Checker2 (independent, fresh-code arms, seeds 4242/999, no reuse of the author's
functions): regen byte-identical (13.7 s), every dossier number matches results.json, and
the refutation holds everywhere tested beyond the sweep — R_f = 30 and 100·R_p read
0.9989/0.9999 (the closed form to the next decades) with the err>80% window still
2.00 R_p, i.e. the blink window is the sample's own eclipse width at every size; β 0.9
blinks in both orientations (peaks 0.702/0.861, f₁ = 0, freshly reimplemented retarded
predicate); and a convoy column (σ_x = 10 R_p, σ_y = 0.3 R_p) peaks 0.925 with f_true_mid
0.924 — anisotropic fleets blink too and have no disc radius for the overlap cure at all,
so the shape-general licensed cure is per-pixel exact predicates. The failure covers
25/33 of the impact band (every impact < R_p errs 0.89; >5% out to impact ≈ 3), not just
central transits. Cure floor: h = R_p pays 45 samples at 7.7% peak — the 5% bar needs
h = R_p/2 exactly (145 samples), so the criterion's cap has no slack.**

## Current best
**Prior standing record, unchanged (compiled from the runs below):**

915d — the additive-attitude premise is dead at the game's own speeds: the frame rotates
by exactly (γ−1)·ψ per constant-γ turn through ψ (SO(2,1) non-commutativity; 12–74° nose
error, 0.27 c and 48% of path inside single maneuvers at β ≥ 0.866); no rung sees it.

1885 — the aggregate one-sample readout is dead at high γ on the DISPERSION channel:
CV(k⁴)=√(e^{16s²}−1) with s = γ²σ_β; 40% median sprite error at β 0.9/σ_β 0.03, top 1% of
members carrying 37% of seen flux at β 0.99; boundary σ_β* = 0.005/γ². (c78d's occlusion
channel is the orthogonal half.)

e59e — opacity is missing from §2's observable list: 16.7% of the sky fabricated at a
2-radii planet approach, 25.0% inside the shadow arc at r_o = 6 M.
22d1/9ffc — the occlusion law is the per-row worldtube test (69–79 ns/row); snapshot and
sprite wirings are the negative controls; judged in the observer's frame at player β.

12db — the kick cost premise ("~50 ns each"): 34.8 µs median shipped (75.6 µs at gold
grade, ~1,800× over floor; exact memo 0.0%); the multiply-add cycle update has no shipped
fast path.

Census, ranked by player visibility (standing): 1. kicks/derivatives REFUTED (12db; no
kick-cost rung). 2. view at the past light cone — letter dead, guarded in cost/presence by
r6 (13c6), tick-exactness freezable; opacity now half-measured (c78d's aggregate arm;
eclipse-parity rung still uncreated). 3. Binet cells replaced by the Darwin compilation
(r1v2 executed; band-constant rule settled). 4. two-body doll 1PN SURVIVES (r3 v3;
licensed p̄ ≳ 65M at ν ≤ 0.25; below 12M wants NR-calibrated EOB). 5. dense ≡ sparse
SURVIVES, guarded by r5 + r5-starve on Linux (68e7, 506c; GPU arm M1-side). 6. undisturbed
≈ 0 SURVIVES by rate, not cost (a4ed; fire rate 1.000).

## Refuted

- **"Aggregates are one sample each" on the occlusion channel (representation.md L59/L116):
  all-or-nothing fleet eclipses — 89.1%/99.0% mid-transit flux error at R_f = 3/10·R_p
  with total blinks while ≥ 89% of flux is visible; survives exact retardation and k⁴
  beaming at β 0.5 (checker: β 0.9 peaks 0.695/0.856; the 400-ship arc formation
  errs 1.000 — the record's own fleet shape); orthogonal to the dispersion channel
  (fails at β = 0, uniform); cure = per-pixel exact predicates (145 samples → 3.0%;
  density-dependent compression) or the overlap closed form, licensed to uniform
  discs at β → 0 only (checker: 11–31pp outside) (20261019-0141-redteam-c78d).**
- [standing] The additive-attitude premise (915d); the aggregate readout on dispersion
  (1885); opacity absent (e59e); snapshot/sprite occlusion (22d1); the kick multiply-add
  cost (12db, b063); the Hashlife memo fast path (12db); "crosses once" (6eae); the cold
  no-memo fallback and any-cache cost (13c6); "r5 uncreatable off-Mac" (68e7).

## Open directions

1. [standing] The integrator's one-pass amendment of representation.md — now also strike
   L59's first clause ("aggregates are one sample each") and keep the second (the pixel
   cap) with c78d's numbers, or replace both with the derivable-overlap law.
2. [standing, extended] The eclipse-parity rung (absence half freeze-ready per 22d1):
   its aggregate arm is now specified and priced (c78d's criterion — N ≥ 100 fleet at
   R_f ≥ 3·R_p, impact 0, ≤ 5% p99 vs exact Σk⁴-occluded; negative must blink > 80%;
   ≤ 150 samples; both fleet orientations at player β). Freeze fixes (checker): the
   ≤ 150-sample cap is R_f = 3-specific (at R_f = 30·R_p the same h = R_p/2 pays
   11,677 — cap as ~(R_f/h)²·π/4 or pin R_f); "f_true_min ≥ 0.88" cannot survive its
   own "judged at player β" clause (exact minima are 0.535/0.815 at β 0.5) — bar it as
   within 5% of each arm's exact f_true_min.
3. [standing] Adopt r5/r5-starve into lab/rungs/; EOB strong-field flank (NR oracle);
   seen-flux rung for the dispersion channel (1885) and the moment representation —
   c78d adds the spatial-extent moment (centre, radius, density profile) as the same
   design's cure for its channel.
4. [standing tails] Occluder+observer comoving; extended occluders (fleet dolls);
   strong-field occlusion near the photon sphere (e59e's rim domain) — unmeasured.

## Contradictions

None. c78d's transit-plane occluded fraction (46% at β 0.5) and its sky-plane one (17%)
are two orientations of one cone geometry, not a conflict — the rung judges both.

## Runs

- 20261016-1207-redteam-12db (silver): premise census; kick cost 34.8 µs vs the doc's 50 ns
- 20261017-1018-redteam-13c6 (silver): r6 created, frozen and executed — PASS for the
  shipped gather; cold path and any-cache KILLED
- 20261017-1330-redteam-68e7 (awaiting grade): r5 created and PASSES on Linux
- 20261017-1447-second-20261017-1330-redteam-68e7-506c (awaiting grade): r5-starve PASSES
- 20261017-2142-redteam-e59e (awaiting grade): opacity missing — 16.7% of sky at 2R
- 20261018-0035-redteam-22d1 (silver, checker-corrected): the occlusion law measured
- 20261018-0143-second-20261018-0035-redteam-22d1-9ffc (awaiting grade): 22d1 regenerates
- 20261018-1126-redteam-1885 (awaiting grade): aggregate readout refuted on dispersion
- 20261018-1433-redteam-915d (awaiting grade): additive attitude refuted — Thomas rotation
- 20261019-0141-redteam-c78d (this run, awaiting grade): aggregate readout refuted on
  occlusion — fleet eclipses are all-or-nothing blinks, 89–99% flux error; cure priced
