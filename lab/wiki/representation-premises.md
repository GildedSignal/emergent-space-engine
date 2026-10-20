topic: representation-premises
status: open
closed-by:
valid-while:
updated: 20261020-1002-second-20261020-0440-redteam-9c08-870b

# The premises of docs/representation.md: a census against the record

**NEW (9c08, premise red-team): the one-sample aggregate is dead on its THIRD channel — the
observer's own γ, with a perfectly cold sky (zero velocity dispersion, exactly where 1885's and
7bcf's channels read zero): one shift per sky cell errs the forward (headlight) sky's k⁴
brightness by E(γ·θ_f) alone — measured 1.09%/p99 7.2% at γ 50, 18.3%/27.2% at γ 125 (the
plane's own playability red measured a burn at γ≈120), 48% at γ 250, saturating at 68.8% (mean
k), 141% (seen-weighted, 2.4× over-bright) and 91% (any colour-true single k) once the whole
sky compresses into one cell; the cell's k-span halves at exactly γ·θ_f = 1 (125.00 stock,
1000.0 fine, solved); 100.0% of the error sits inside θ′ < 2/γ on cells carrying 97–100% of
the seen flux; colour drifts to 0.86 octaves (a ⅛-octave sprite table fully blown) — one
number cannot serve brightness and colour. The fine floor reproduces the stock curve shifted
×8 to machine noise (18.3122% vs 18.3132% at γθ_f = 1): the law is the product alone. The view
record's own domain (e6c9/959a flown to β 0.65 = γ 1.3) reads 0.0025% p99 — control passes;
the engine's own gates fly γ to 10⁶ (C1) — the letter's readout is licensed nowhere in
between. The cure is one already-computed quantity: a running sum Σ(lum·k⁴) per cell at the
due events the record already pays (the shipped per-body path computes k per event,
`view.rs` L308–319) — one extra FMA, exact brightness; colour from the letter's own type ×
log k table (L58), B = 4–64 equal-ln-k bins at γθ_f = 1…8000 (B ≈ 4·log₂(γθ_f), O(1) per
cell). This also deletes the adaptive-cell cure (narrowing as 1/γ, ~γ² cells). No rung sees
it (r6 per-emitter cost/presence; r11 occlusion; r12 formation flux); freeze-ready arm
r13-sky-shift in the dossier (one-shift negative fails bright p99 0.18–0.69, colour 0.10–0.86
oct; γ 1 and 1.33 controls must read 0). Cold-sky numbers are a floor: 1885/7bcf's
dispersion channels add on top. (20261020-0440-redteam-9c08; predictions 4/7 held, three
misses all on one side — the small-angle constant was 4× aggressive — each sharpening the
law: the γθ_f collapse, halving at γθ_f = 1, B ≈ 4 log₂(γθ_f).)**

**Checker (independent; regen exact, every number reproduced; the saturation row verified
against the closed-form full-sky moments ⟨k⁴⟩/⟨k⟩⁴ = 3.2 → 68.75%, Σk⁵/Σk⁴ → 141.07%,
e^{⟨ln k⟩} → 90.86%): the law extends beyond the author's sweep — the E(γθ_f) collapse
holds at a third, coarser floor (3.2e-2: 18.33% at γθ_f = 1, 48.14% at 2, saturation),
γ = 10⁷ and 10⁸ sit exactly at the saturated values, and fresh seeds move 18.3122% by
≤0.03pp. ONE CORRECTION, the lens's own blind spot: the falsifier samples a 3D isotropic
sky, but the plane's sky is a CIRCLE (the record's 786 cells = 2π/θ_f) with members
uniform in θ_s, not in cosθ_s. In 2D (exact quadrature) the law and the kill stand with
shifted constants: 16.76% (not 18.31%) at γθ_f = 1, 44.67% at 2, saturation 77.14%
(analytic (4.375−1)/4.375 — WORSE than 3D's 68.8%), colour-true k 98.6%, p99 5%
crossing at γ ≈ 42; the γθ_f collapse holds in 2D too (16.7599% vs 16.7608% at the two
floors). Quote 2D numbers for the game. Nit: P1's "oracle errs brightness" clause was
unachievable as written — the brightness-oracle k̄ = ⟨k⁴⟩^{1/4} errs brightness ≡ 0 by
construction (the script proves it); the binding bracket is R4 + the gap, as the dossier
table correctly reports.**
**NEW (7bcf, premise red-team): the dispersion channel's rung exists, frozen (r12-seen-flux,
sha256 a6335a29…89ce) and executed PASS, and the channel's location is found — the γ²
amplification in 1885's CV law belongs to OBSERVER-frame dispersion (a swarm), not to a
formation: with comoving v′ composed by exact velocity addition, the addition compresses
the longitudinal dispersion by exactly the γ² that k amplifies at the mean
(d ln k⁴/dv′∥ = 4·(1+O(v′))), so CV(k⁴) ≈ 4σ_comoving independent of γ — measured 0.120
= 4×0.03 identically at β 0.5/0.9/0.99 and 0.420 = 4×(0.15/√2) for a fast ring. The
observer-frame diagnostic reads CV 4.05 at n=400 at 1885's own headline point (β 0.9,
σ 0.03, head-on) where the linearized law reads 0.70: the published law is the small-s
limit and understates the tail by ≥ 6× (k's convexity explodes near u→1; checker below:
the understatement is unbounded). The letter's
"aggregates are one sample each" is dead on the flux channel in every convention —
one-sample p99 0.21–1.11, worst at PLAYER speed (β 0.5, σ 0.10: 1.109), not exotic γ.
The cure is licensed: squad-Gaussian + formation-shape readout by quadrature over the
full nonlinear k, p99 ≤ 0.033 at N=400 (that residual is the truth's own CV/√N sampling
floor; against a 10⁶-member truth the readout error is 1.2×10⁻⁴–3.8×10⁻⁴, ring 8.9×10⁻¹⁶
spectral), ~4.3×10³ ops per fleet per frame CONSTANT in N (per-ship exact: 1.7×10⁷ at
N=10⁶). Sharper than expected: for formations the shape barely matters — the BULK readout
errs only e^{8σ²}−1 ≈ 1.6% at σ 0.03 and a single Gaussian moment reads the fast ring
(β_rot 0.15) to 0.23% p99; the letter's failure is specifically sampling one member, not
missing moments. Predictions 3/7 held; all four misses share the one convention
diagnosis (disclosed in the dossier). Awaiting the integrator: commit r12 to lab/rungs/;
v2-freeze sentence in the dossier (squads/formations carry their velocity description;
observer-frame swarms are the γ² regime).**

**Checker (independent; regen byte-identical, PASS from my own metrics-check.json, freeze
hash holds; fresh-code cross-validation reproduces the author's c2 exactly — one-sample
0.2771, bulk 0.01572, CV 0.1203): the slope identity is confirmed to 6 decimals (4.000000
at v′=0 for β 0.5/0.9/0.99/0.999; 4/(1−v′²) away from it — the comoving cancellation is
exact, any β). The claim extends beyond the author's domain: at N=10⁶ (c2-like, full
path, fresh seed) mix-quad p99 5.7×10⁻⁵ with one-sample still dead at 0.195, and at
β 0.99/σ 0.10 (next decade of σ at high γ) mix-quad 6.0×10⁻⁴, one-sample 0.473; the
frozen N=400 bar is seed-robust (8 fresh seeds on c7: 0.013–0.043, all ≤ 0.05) and no
quadrature node ever crosses c in the frozen layouts (ksafe never fires — no silent
bias). Two sharpenings for the freeze sentence: (1) the observer-frame swarm's CV is
n-DIVERGENT, not a constant — sample CV reads 8.9/4.7/30/952 at n=400/10⁴/10⁵/10⁶
(second seed: 704), the top 1% of members carries 98.3% of seen flux, one-sample p99
0.80: no moment description of a swarm's seen flux exists, so swarms need per-member
treatment at the bright end or their comoving description; (2) the 4σ law is
LONGITUDINAL — a transverse-dispersed squad (σ⊥ 0.10, σ∥ 0.001) has CV 0.028 (second
order), and a wrongly-isotropic scalar-σ description of it errs 8.5% p99: the dispersion
TENSOR the rung letter already names is load-bearing, not optional.**

**Checker 2 (blind to the first check; regen byte-identical, PASS re-derived; k verified
against the exact identity √((1+u)/(1−u)) to 5×10⁻¹³; the slope-4 cancellation re-derived
by hand — the γ₀⁻² composition derivative cancels the 4γ₀² observer-frame slope exactly):
the domain extends a decade in γ (β 0.999: mix-quad 0.0103 at σ 0.03, 0.0201 at σ 0.06,
CV = 4σ holds; one-sample dead) and to relativistic squad separation (±0.60: mix-quad
0.0041, bulk readout dead at 1.42). Three edges the freeze sentence must carry: (1) the
frozen N=400 license bar saturates on the truth's own CV/√N floor by σ ≈ 0.12–0.15 — at
σ 0.15 mix-quad reads 0.0555 against its N=400 truth (bar FAIL) while the readout itself
is 4.9×10⁻⁴ against a 10⁶ truth; at σ 0.2 the Gaussian squad model itself draws
superluminal internal velocities (members() has no rejection; compose then yields
garbage/NaN); (2) ops are LINEAR in squad count — 10 squads at the σ 0.03 sizing already
cost 21,600 counted ops, past the 20,000 fence the frozen cases (≤ 2 squads) never reach:
"constant in N" holds per fixed description granularity; a many-squad fleet needs squad
aggregation or per-squad caching; (3) cosmetic: the "1885-law" diagnostic prints 0.000
for squad cases (σ undefined there).**

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
it fails at β = 0 with a perfectly uniform fleet — exactly the regime where 1885's belt
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

**NEW (4ff1, second author on c78d — the silver's named experiment done): the rung
exists, frozen before its run (r11-eclipse-aggregate.md, sha256 de53f498…0506) and
executed: PASS. The corrected bars hold, measured on two independent code paths
(quadratic light-cone root vs monotone bisection; clip vs case-split predicate —
outcomes identical, metrics agree to solver noise). Per-pixel aggregate occlusion (the
letter's own second clause) is licensed at player β 0.5, both orientations, at BOTH
pitches: h = R_p/2 → p99 flux error 1.6% at 113 samples; h = R_p → 4.1% at 29 samples
(the record's 145-sample cure was conservative: at p99 semantics the >5% spikes at
h = R_p are <1% of the path). Domain condition: the frozen truth fleet and the pixel
weights are both UNIFORM — a non-uniform core breaks the uniform-weight readout
(checker3: Gaussian σ = R_f/2 errs p99 0.21–0.23), so the license is for uniform-density
aggregates or pixels weighted by the density moment (direction 3's profile). The
one-sample negative fails three bars (p99 0.84,
fmin dev 0.80, false-blink fraction 0.058 — an error of type, fabricated total
eclipse); the overlap closed form passes as the positive control (p99 0.0018). The
page's cap-as-function is exact: samples/(π(R_f/h)²) = 0.998–1.000 at R_f = 3/10/30·R_p
while the error falls 0.024 → 0.0027 → 0.0004 (the cure gets cheaper per unit flux as
fleets grow); the cure survives β 0.9 (p99 0.027 transit / 0.016 sky). The game's own
shape answers "which readout wins where": the 400-ship arc needs the pitch to resolve
its thinnest dimension, not its span — 3 samples err 0.63, 41 err 0.083, 168 (h = 0.075)
err 0.038 at 2.4× fewer predicates than per-ship; a sub-pixel or sparser aggregate pays
exact per-ship sums (one law over a representative set — cost = min(N, support pixels
at the resolving pitch)). INSTRUMENT CORRECTION (disclosed, both paths here fixed):
c78d's β arm weighted k⁴ = 1/(γ(1+β²·px/q)) — the doppler's β counted twice; exact SR
is 1/(γ(1+β·px/q)), moving the β-arm minima ~1pp (sky 0.815 → 0.800, transit
0.535 → 0.523): every c78d conclusion is geometric and stands, but both checkers had
"reproduced" the typo exactly from the description — agreement is not independence,
again.**
**Checker3 (blind, independent; fresh seeds 777/888, 16 s): regen exact in a clean tree —
decisive configs, check path, diagnostics and the c78d base all bit/byte-identical; verdict
PASS reproduced from my own metrics; the doppler typo confirmed in c78d's code (cosang is
v·n, then multiplied by β again). The cure extends beyond the author's sweep: β 0.99
(γ 7.1) p99 0.024/0.017 with zero false blink; grazing impact 2.8 = 0.7(R_p+R_f) p99
0.015. The missing axis is DENSITY: a Gaussian-core fleet (253 uniform pixels at the
frozen pitch) errs p99 0.229/0.210 with fmin dev 0.21/0.19, a two-clump fleet 0.14/0.36 —
uniform pixel weights misprice a core 4–5× past the bar; density-weighted pixels cost the
same (one arm for the next freeze). Sub-planet R_f = 0.5·R_p: h = R_p/2 pays 5 samples at
p99 0.22, h = R_p/4 pays 13 at 0.11 — the min(N, pixels) crossover sits near 80 pixels ≈
N, as the domain line says.**
**Checker4 (blind second checker of 4ff1; fresh code, third solver — Newton on the light
cone — seeds 777xxx): regen total (author metrics, check path to 1e-12, verdict PASS,
diagnostics, c78d base all identical); pixel counts 113/29/3/41/168 re-derived. Cure
holds outside the author's range: impact 1.0/2.0/2.8 at β 0.5 (p99 ≤ 0.017, zero
blink), β 0.99 (0.022/0.013), 10× truth N (0.015), 5× path steps (no aliasing). The
doppler typo re-confirmed by re-committing it from the same description (0.8135 ≈ the
stored 0.815) before fixing (fresh delta 0.5273 vs 0.5206). The density axis decomposes
as WEIGHT, not pitch: Gaussian core σ = R_f/2, uniform pixels err p99 0.226/0.205 at
3σ support (253 samples — checker3's 0.229/0.210 reproduced) and refining pitch never
restores 5% (h = R_p/4 uniform: 0.072/0.110), while density-weighted pixels at the SAME
pitch and cost give 0.009/0.028; the magnitude is support-convention-dependent (2σ
support: 0.077/0.103, 13.5% of mass outside) — the aggregate must carry its support
radius AND density profile as moments. The hash-frozen domain line carries neither
clause: r11 as frozen passes uniform pixels that err 20% on cored fleets, and the
game's formations are not uniform discs — the v2 re-freeze's one sentence.**

**NEW (870b, second author on 9c08): the rung exists and is flown, and the checker's named hinge
cuts the other way — the shipped record is EXEMPT from 9c08's brightness kill.** The cell struct
read on the record's own branch (959a `work/patch.diff`: `CellSums { n, lum, lc[3], ls, sh,
kinds[8] }`, `e.lum += row.luminosity` with `row.luminosity = lum·shift⁴`, served as
`luminosity: lum`) shows the record stores the exact per-member seen-flux sum — 9c08's proposed
cure (a running sum Σ lum·k⁴, "one extra FMA") is the record's own field at zero extra cost, and
its one-shift model (brightness k̄⁴·n) is a readout the record never serves; its own
"what would make it wrong" clause (1) fired on the struct read. The letter L59 stays dead as a
RULE, now rung-guarded: **r13-sky-shift frozen (sha256 ed91f4c0…) and executed — PASS** — on the
game's 2D circle sky (786 cells = 2π/θ_f; 9c08's 3D numbers were the idealisation): the record's
representation (`exact-sum` = CellSums + the letter's L58 log-k table, B = 128) reads brightness
0.0 exactly and colour ≤ 0.036 oct at γθ_f ≤ 8000 (γ to 8·10⁶, both floors); the one-shift
collapse (`one-shift` negative, the letter read literally) fails brightness p99 0.77 and colour
0.96 oct; both read 0 at the record's flown γ ≤ 1.33 (`flat-gamma` positive); +4 ops/event for
the table (the Σ lum·k⁴ term is shipped). The E(γ·θ_f) law holds for the continuum forward
error (quadrature identical to 6 digits) and the 3D p99 (0.630141/0.630142 across floors;
γθ_f=1 → 27.2% 3D p99, saturation 68.8%); in 2D the stock p99 reads 27.8% at γθ_f=1 and
saturates at 77.2% — but the 2D p99 does NOT collapse across floors: at γθ_f=4 the fine floor
reads 0.708 vs stock 0.629 (1.13×, systematic over seeds — the p99 tail at fine floors picks
just-off-axis cells whose k-span depends on γ and θ_f separately; checker 870b). The topic's
three channels (dispersion r12, occlusion r11-era predicates, observer-γ r13) are now all
rung-guarded. Colour: the record's `lc/lum` flux-weighted
per-member blackbody mix needs no k (no γ-aggregate error; it exists identically at γ = 1), but
it is not an exact identity for the shipped palette — `blackbody()` max-normalizes and
gamma-encodes per member before the mix, erring ≤ ~0.5 oct on mixed temperatures, a
display-palette approximation shared with the per-body render path (checker 870b); the L58 table
(B=128, 0.036 oct at γθ_f=8000, B ≈ 4·log₂(γθ_f) confirmed) serves only a sprite-table colour-k.
Unflown: r13 against the merged Rust serve path in flight (the metric definitions here are the
contract), and
staleness between due events stays e3a4's tier (identical for sums and any cure).
(20261020-1002-second-20261020-0440-redteam-9c08-870b; predictions 6/8 held — P5's miss disclosed,
P7 misreported as held: the 2D p99 does NOT collapse across floors at γθ_f 1 and 4, corrected
above; the max-over-cells colour metric picks a sparse off-axis cell above the forward cell's 0.83.)

**Prior standing record, unchanged (compiled from the runs below), plus 9c08's observer-γ
half:**

9c08 — the one-sample aggregate is dead on the observer's-γ channel with a cold sky:
brightness error E(γ·θ_f) alone (18.3% at γθ_f = 1, saturating 69–141%), k-halving at
γ·θ_f = 1 exactly, 100% of the error on the forward cells that carry the flux; the view
record's license needs the γ clause (flown to γ 1.3 = 0.0025%; the gates fly to 10⁶);
cure = Σ(lum·k⁴) running sum (1 FMA/event, exact) + the letter's own log-k table
(B = 4–64 bins); deletes the 1/γ adaptive-cell branch. [870b: r13 now frozen and executed —
PASS; and the struct read shows the record already stores that sum, so the kill and the cure
apply to the letter's one-shift readout, not the shipped record.]

915d — the additive-attitude premise is dead at the game's own speeds: the frame rotates
by exactly (γ−1)·ψ per constant-γ turn through ψ (SO(2,1) non-commutativity; 12–74° nose
error, 0.27 c and 48% of path inside single maneuvers at β ≥ 0.866); no rung sees it.

1885 — the aggregate one-sample readout is dead at high γ on the DISPERSION channel:
CV(k⁴)=√(e^{16s²}−1) with s = γ²σ_β; 40% median sprite error at β 0.9/σ_β 0.03, top 1% of
members carrying 37% of seen flux at β 0.99; boundary σ_β* = 0.005/γ². (c78d's occlusion
channel is the orthogonal half.) [7bcf refines the constant's domain: the law is the
small-s limit of the OBSERVER-frame convention; exact CV there is 4.05 at its own
headline point; under the comoving formation convention CV = 4σ, γ-free. 9c08 adds the
geometric half: dispersion σ = 0 still errs E(γθ_f) from the cell's own angular width.]

e59e — opacity is missing from §2's observable list: 16.7% of the sky fabricated at a
2-radii planet approach, 25.0% inside the shadow arc at r_o = 6 M.
22d1/9ffc — the occlusion law is the per-row worldtube test (69–79 ns/row); snapshot and
sprite wirings are the negative controls; judged in the observer's frame at player β.

12db — the kick cost premise ("~50 ns each"): 34.8 µs median shipped (75.6 µs at gold
grade, ~1,800× over floor; exact memo 0.0%); the multiply-add cycle update has no shipped
fast path.

Census, ranked by player visibility (standing): 1. kicks/derivatives REFUTED (12db; no
kick-cost rung). 2. view at the past light cone — letter dead, guarded in cost/presence
by r6 (13c6); the aggregate readout is now dead on ALL THREE channels: occlusion (r11,
executed PASS), formation seen-flux (r12, executed PASS — 7bcf) and the observer's own γ
across a sky cell (9c08, no rung yet); the shipped per-body gather is the exact control
(view.rs L308–319). 3. Binet cells replaced by the Darwin (r1v2 executed; band-constant
rule settled). 4. two-body doll 1PN SURVIVES (r3 v3; licensed p̄ ≳ 65M at ν ≤ 0.25; below
12M wants NR-calibrated EOB). 5. dense ≡ sparse SURVIVES, guarded by r5 + r5-starve on
Linux (68e7, 506c; GPU arm M1-side). 6. undisturbed ≈ 0 SURVIVES by rate, not cost
(a4ed; fire rate 1.000).

## Refuted
- **"Aggregates are one sample each" on the observer's-γ channel too (9c08): with a cold
  sky (zero dispersion — where 1885's and 7bcf's channels read zero) one shift per sky
  cell errs the forward sky's brightness by E(γ·θ_f) alone — 18% at γ 125 stock (the
  plane's own burn red is at γ≈120), saturating 69–141%; k-halving at γ·θ_f = 1 exactly;
  colour to 0.86 octaves; cure = Σ(lum·k⁴) running sum (1 FMA/event) + log-k table
  (4–64 bins); the record's license needs the γ clause (flown only to γ 1.3). [870b: the letter
  is dead as a rule, rung-guarded (r13 PASS, 2D numbers 27.8% p99 at γθ_f=1, saturation 77.2%);
  but the record itself is exempt — it serves the exact seen-flux sum, so the one-shift kill
  never touched it.]**
- **"Aggregates are one sample each" on the flux channel too (7bcf, r12 executed): p99
  one-sample error 0.21–1.11 across comoving formations at β 0.5–0.99, worst at player
  speed with σ 0.10; dead in every convention; the cure (moments/formation quadrature,
  constant ops) licensed and rung-guarded.**
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
   cap) with c78d's numbers, or replace both with the derivable-overlap law; 7bcf adds
   the flux half's replacement sentence (moments/formation quadrature, 7bcf's numbers);
   9c08 adds the sky-cell sentence: per-cell seen-flux running sum (Σ lum·k⁴, exact, one
   FMA per due event) + type × log k table for colour; the single-shift aggregate is
   licensed nowhere above γ ≈ 0.6/θ_f at the 5% bar (p99 bar: γ ≈ 44 stock).
2. [executed aggregate half, 4ff1] The eclipse-parity rung's aggregate arm is r11:
   frozen (hash in the run), executed, PASS, on the corrected bars — 5% p99 vs exact
   Σk⁴ at player β both orientations; fmin within 5% of the arm's exact minimum;
   false-blink type bar; samples ≤ 150 pinned at R_f = 3·R_p plus the scale-aware
   ratio ≤ 1.1 (measured 0.998–1.000 to R_f = 30·R_p). Awaiting the integrator: commit
   r11 to lab/rungs/, then the absence half (22d1's per-row law). Shape clause for the
   freeze: the pitch resolves the thinnest support dimension (the arc at h = 0.075,
   168 samples, errs 0.038; h = R_p errs 0.63); sub-pixel/sparse aggregates pay exact
   per-ship sums — cost = min(N, support pixels at the resolving pitch).
3. [flux half executed, 7bcf] Commit r12-seen-flux to lab/rungs/ (frozen hash in the
   run; executed PASS). Remaining named arms: heterogeneous member luminance (weighted
   moments); the sprite TYPE table (binned log k — 1885's 40% median was reported there;
   bin-boundary interaction with dispersion is unmeasured); moment drift under stirring
   (how often σ must be re-estimated — kick-cadence territory). EOB strong-field flank
   (NR oracle) still standing. The moment representation now has both halves measured:
   spatial (c78d/4ff1: support radius + density profile) and velocity (7bcf: squads +
   formation shape; the γ² channel is the observer-frame swarm's).
4. [sky-cell half, 9c08] Freeze r13-sky-shift (criterion in the run's dossier: one-shift
   negative vs seen-flux-sum candidate at γθ_f ∈ {1, 4, 8000}; γ 1 and 1.33 controls must
   read 0). Named arms beyond it: the record's own cell struct on its branch (read once:
   confirm the stored shift is not already a seen-flux sum — then only the colour channel
   stands); the cold-sky floor plus real dispersion (additive in quadrature with
   1885/7bcf); clustered skies (more members in the worst cells).
5. [standing tails] Occluder+observer comoving; extended occluders (fleet dolls);
   strong-field occlusion near the photon sphere (e59e's rim domain) — unmeasured.

## Contradictions

None. c78d's transit-plane occluded fraction (46% at β 0.5) and its sky-plane one (17%)
are two orientations of one cone geometry, not a conflict — the rung judges both. 7bcf's
CV=4σ (comoving) and 1885's CV law (observer-frame) are two conventions of one channel,
bracketed by the rung's frozen comoving cases and the observer-frame diagnostic — the
v2-freeze sentence names both. 9c08's geometric channel composes with both dispersion
channels (it is the σ = 0 floor; real dispersion adds on top).

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
- 20261016-1207-redteam-12db (silver): premise census; kick cost 34.8 µs vs the doc's 50 ns
- 20261017-1330-redteam-68e7 (awaiting grade): r5 created and PASSES on Linux
- 20261017-1447-second-20261017-1330-redteam-68e7-506c (awaiting grade): r5-starve PASSES
- 20261017-2142-redteam-e59e (awaiting grade): opacity missing — 16.7% of sky at 2R
- 20261018-0035-redteam-22d1 (silver, checker-corrected): the occlusion law measured
- 20261018-0143-second-20261018-0035-redteam-22d1-9ffc (awaiting grade): 22d1 regenerates
- 20261018-1126-redteam-1885 (awaiting grade): aggregate readout refuted on dispersion
- 20261018-1433-redteam-915d (awaiting grade): additive attitude refuted — Thomas rotation
- 20261019-0141-redteam-c78d (this run, awaiting grade): aggregate readout refuted on
- 20261019-0141-redteam-c78d (silver; gold blocked on the rung freeze, done by 4ff1): aggregate readout refuted on occlusion — 89–99% fleet blinks; cure priced
- 20261019-0325-second-20261019-0141-redteam-c78d-4ff1 (this run): r11 aggregate arm frozen + executed — PASS; one-sample negative fails 3 bars; cure licensed at 29–113 samples; c78d's β-arm doppler typo corrected (~1pp, conclusions stand)
- 20261019-2339-redteam-7bcf (this run): r12 seen-flux frozen + executed — PASS; one-sample dead on flux (0.21–1.11 p99, worst at player speed); moment/formation readout licensed (≤3.8e-4 vs 1e6 truth, constant ops); the γ² channel located: observer-frame swarms (exact CV 4.05 vs the linear law's 0.70 at its own headline point), comoving formations CV = 4σ
- 20261019-0141-redteam-c78d (awaiting grade): aggregate readout refuted on
- 20261019-0325-second-20261019-0141-redteam-c78d-4ff1 (awaiting grade): r11 aggregate arm frozen + executed — PASS; one-sample negative fails 3 bars; cure licensed at 29–113 samples; c78d's β-arm doppler typo corrected (~1pp, conclusions stand)
- 20261019-2339-redteam-7bcf (awaiting grade): r12 seen-flux frozen + executed — PASS; one-sample dead on flux (0.21–1.11 p99, worst at player speed); moment/formation readout licensed (≤3.8e-4 vs 1e6 truth, constant ops); the γ² channel located: observer-frame swarms (exact CV 4.05 vs the linear law's 0.70 at its own headline point), comoving formations CV = 4σ
- 20261020-0440-redteam-9c08 (this run): one-sample dead on the observer's own γ (cold sky): E(γθ_f) alone, 18% at γ 125 stock, halving at γθ_f = 1 exact, saturates 69–141%; cure = seen-flux running sum (1 FMA) + log-k table; record's license needs the γ clause; no rung sees it
- 20261020-1002-second-20261020-0440-redteam-9c08-870b (awaiting grade): r13-sky-shift frozen and executed PASS; struct read: the record stores Σ lum·k⁴ already (9c08's cure = the shipped field); letter L59 dead as a rule; 2D law at p99 confirmed
