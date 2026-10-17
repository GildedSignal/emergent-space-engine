# Dossier — 20261017-2142-redteam-e59e (lens: premise red-team)

**Claim.** `docs/representation.md` §2's observable set for the view (L53–59) omits
opacity entirely — no capture rule, no occluder test — so as specified and as shipped
(`crates/universe/src/view.rs`, "Light is straight in the root frame (no lensing
yet)"), the player sees stars **through black holes and through planets**: at r_o = 6 M
a quarter of the sky is fabricated (2,500 of 10⁴ rows), and at two planet radii on
approach 16.7% of the sky shines through the ground (1,667 of 10⁴) — a load-bearing
observable Julien's own conversation names six times, dropped by the design, gated by
no rung (r6's presence criterion *requires* the rows occlusion must remove).

**Bottleneck.** Not a speed bottleneck: a premise gap on the view (board item "the
view", the engine's knowledge half). The doc's §2 list is the specification every
view run (45 runs on view.md) inherited; none measured opacity because the premise
says it does not exist. Adopting it deletes nothing and costs one interval test per
occluder per row plus one closed-form asin per black-hole doll (Synge), so its
absence is not a cost tradeoff — it is an omission.

## Evidence (all numbers from `python3 falsifier.py`, 0.2 s, this folder)

Truth: exact Schwarzschild null geodesics, M = 1, backward-traced from a static
observer (RK4 on u″ = −u + 3u²); capture iff b < b_c = 3√3 (the exact predicate r1/B4
use). Scheme: the doc's §2 gather and the shipped view (straight crossing, every
emitter present, no opacity test — verified by reading `view.rs` and by search).

- **Instrument validity, both sides (P1):** r1/B4's own photon-capture cases classify
  4/4 (b/b_c ∈ {0.9, 0.97} capture; {1.03, 1.1} escape).
- **The shadow arc (P2, P3):** α_sh = asin(√27·√(1−2/r_o)/r_o) (Synge) matches the
  numerically bisected capture boundary to ≤ 4.2×10⁻⁵ relative at r_o ∈ {100, 20, 6,
  3.2} M (6eae's own radii). 2-D sky, fraction = α_sh/π: **1.64% at 100 M, 7.93% at
  20 M, exactly 25.0% at 6 M, 46.6% at 3.2 M** — inside that arc *no arrival
  direction exists*; the shipped gather returns every emitter whose straight path
  lands there: **164 / 793 / 2,500 / 4,662 fabricated rows at N = 10⁴** uniform sky
  emitters.
- **The rim is not a perturbation (P5):** exact deflection 0.556 rad at b = 2 b_c
  (weak-field series 0.532, fine), but **2.08 rad at 1.1 b_c (series −38%), 4.23 rad
  at 1.01 b_c (−65%), 6.51 rad at 1.001 b_c** — the last equals the analytic
  strong-deflection law −ln(b/b_c−1) + ln[216(7−4√3)] − π to three digits. The doc's
  "memoized deflection(b)" (L57) has a domain that *ends at the shadow rim* (the
  shipped `space::kerr::deflection` returns None for captured b); the letter is
  silent on rows whose straight b ≤ b_c: keep-straight → fabricated in-shadow rows;
  drop-on-None → the emitter vanishes, though exact GR shows its images outside the
  rim at 100% of azimuths (6eae). Either wiring fails eclipse parity.
- **Opaque bodies, flat geometry (P6):** an occluder of radius R at distance d blocks
  an arc asin(R/d): at d = 10 R, 3.19% of the sky (**319 of 10⁴ emitters drawn
  through it**); at d = 2 R (every planet approach), 16.7% (**1,667**).
- **The gap is total (P7):** search of `lab/rungs/*.md`, `docs/representation.md`,
  `docs/law.md` — ray-side capture is gated (r1 `photon-capture`, B3/B4), view-side
  opacity appears nowhere; r6 (per the census) gates readouts/emitter, presence and
  cost, with the amnesiac cache as negative — its presence bar counts in-arc rows as
  correct. Julien's conversation required it: "occlusion" in the render list
  (original-conversation.md L984, L6450, L7375), "check whether that null segment
  intersects the worldtube of an occluding planet … a spacetime visibility problem"
  (L4872), "**eclipse status unchanged**" as an invariant (L5032), "a shadow from a
  circular body can often be treated analytically" (L4283), "observation: … sensor
  sensitivity and **occlusion**" (L4864).

**Reproduce:** `cd lab/results/20261017-2142-redteam-e59e && python3 falsifier.py`
(JSON to stdout; `evidence.json` is the saved run). Full regen: `./regen.sh`
(< 1 s; no tree edits outside this folder — `work/patch.diff` is empty).

**Predictions:** `predictions.md`, written before the run — **all seven held**
(P3's 25.0% at 6 M exact, P4's four fabricated-row counts, P5's >3 rad at 1.01 b_c,
P6's ~320/~1,700). The one mid-run event: the P5 integrator's initial sign was
wrong (returned −1.72 rad); fixed before any number was read, disclosed here.

## The ranked attacks (the lens's deliverable)

1. **Opacity/capture missing from the view's premises** — this falsifier. Player
   visibility: any planet approach (16.7% of sky) or black hole on screen (1.6% at
   100 M, 25% at 6 M). Rung that should catch it: **none does**; the missing
   criterion is *eclipse parity* (rows whose retarded null segment meets an
   occluder's worldtube must be absent; emitters near the rim present via their true
   deflected images; negative = the shipped straight gather, which must fabricate at
   the measured rates).
2. **deflection(b) as the lensing readout is a perturbation whose domain ends at the
   rim** (same falsifier, P5); the doc's wiring choice at b ≤ b_c decides between
   fabricated stars and lost ones — both wrong.
3. **The fleet doll freezes under sustained thrust** (representation.md L23 "the
   free-fall frame of its centre of mass" + L50 decisions-as-kinks): measured by
   56cd (escape burn: 56 refused anchors, origin 3,174 dr off, shape 32%), no rung
   sees it — reported, not re-measured here.
4. **Letter bug, trivial:** L28 "N ≈ 2πm/ln 2 spokes (m = 16, N = 128)" — 2π·16/ln2
   = 145, not 128 (cells 13% off square); N = 128 belongs to m ≈ 14.
5. **Premises that survive** (reported, per the lens): the two-body doll (licensed
   p̄ ≳ 65 M at ν ≤ 0.25, 97b0); dense ≡ sparse (guarded by r5 + r5-starve on every
   axis this lab can reach); undisturbed ≈ 0 by rate (a4ed); Binet cells already
   replaced by the Darwin compilation (the doc's DRAFT still teaches it — the
   census's amendment, unchanged).

**What would make it wrong.** The client compositing occlusion for free (no: the
view is "physics, not visuals", the same gather feeds perception and instruments,
and a black hole's shadow has no surface to depth-sort against); or no game scene
ever putting an occluder on the sky (false: every planet approach, every black
hole); or the 2-D sky assumption misreading the game (it is 2+1 D; N = 10⁴ is
illustrative — 649c measured ~10⁵ rows in flight).

**Cost of adopting.** One interval test per occluder per row against the retarded
segment (analytic for circular bodies, per Julien's conversation), one closed-form
asin per black-hole doll; local, no new state, no broadcast — it composes with the
missing delay(b) memo (5977), which the moving-occluder eclipse timing ("eclipse
status unchanged") will need anyway.

**Fit with PRINCIPLES.** Principle 30: "what really matters is navigation, knowledge
and dynamics those need to be perfect" — knowledge is this gather; and the doc's own
L56 "Light is gathered at the observer, never broadcast" makes opacity a per-row
predicate, the cheapest possible form — its absence is not "less is more" but a lost
law.

**The lens's blind spot.** A premise red-team weighs what the *document* says; the
deeper risk is the documents nobody wrote — occlusion survived in September's
approved-build-plan (G6 "the observatory provides … occlusion") and vanished in the
pivot's rewrite without a decision recorded against it. Also unmeasured here: the
moving-occluder eclipse timing (needs delay(b)) and occlusion at γ → 1 closing
speeds — exotic, deliberately not ranked first.
