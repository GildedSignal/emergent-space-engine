# Dossier — 20261011-1102-scout-4c5b (lens: scout)

**Machine:** GitHub Actions linux, 8 vCPU, 15 GB, load 1–4, all processes < 100 MB. Wall for the
whole falsifier: 40 s. Everything regenerates from `python3 inspiral.py` in this folder
(writes `inspiral-out.json`; log in `inspiral-log.txt`).

## Claim

The inspiral generator the law already names on paper ("Inspiral is not a jet: Peters' a(t) is
its generator", law.md; named and unclaimed by b-news-gravity-e300) is **adoptable, and the run
fixes its three design constants plus one wiring rule**: (1) the handoff is the **exact
Schwarzschild separatrix** in (E, L) — the same boundary where the plunge-tube compiler
(scout-a1a4) takes over — and inside B11's domain (ν ≤ 0.25, p ≥ 20M) **eccentric binaries
circularize before plunge**: the plunge tube receives a near-circular orbit at a\* ∈ [6.1, 9.1]M,
with residual eccentricity at plunge growing as ν falls (0.00 at ν = 0.01 → 0.47 at ν = 10⁻³,
e₀ = 0.9 — the EMRI signature); (2) the generator is **free outside the strong field** (0.005
re-keys/orbit; 555 re-keys over ~10⁶ orbits from 1000M at the 1% bar, each one calendar event
with slack = ε_bar·P/|dṖ/P|), but the re-key wall (≥ 1 recompile/orbit) sits at **25M (1% bar) /
63M (0.1% bar) for ν = 0.25**, leaving a bounded one-off chirp regime of **53 / 583 orbits**
before the separatrix; at ν ≤ 10⁻³ the 1% wall essentially coincides with the separatrix
(6.3M, 3 orbits inside); (3) the Newtonian flux alone **misses a 1% merger-time bar everywhere
in B11's strong-field domain** (net deficit vs the 1PN-corrected generator: +1.8% at a₀ = 100M,
−9.7% at 20M; flux-only +4.1% at 100M, +0.9% at 600M → the 1% bar breaks at a₀ ≈ 150M net,
≈ 500M flux-only), and the two-flux Newtonian drift on the exact tube is **inconsistent for
circular births** (spurious e grows to 0.81 over the inspiral): L must be projected onto the
exact circular family.

## Bottleneck

HANDOFF "Headed next" #4, third item — "inspiral (Peters' generator)", Julien: "i like both".
The only item of the headed-next list with **no owner**: b-kerr, b-fermi-phase2, b-plunge-tubes,
b-handoff-surface, b-energy-register, b-news-gravity all ran; nothing claims radiation reaction
(b-news-gravity-e300: "both named, neither claimed here"). Expected gain: not a speedup but a
**deletion plus a contract** — it deletes inspiral-as-kicks permanently (df81 killed the jet:
1.1×10⁻² drift/orbit at a = 20M) and hands the motion-law v2 finishers a measured generator:
the drift's event rate (the queue's own slack key), the handoff surface (one predicate already
implicit in the tube's cubic), and the accuracy contract (where 1PN terms are mandatory).
Falsifier on the law's own representation: the exact Schwarzschild tube from (E, L), fluxes
evaluated on the exact turning-point elements (a, e).

## Evidence

`cd lab/results/20261011-1102-scout-4c5b && python3 inspiral.py` (40 s; numpy only; M = G = c =
1; the binary is one doll, M = 1, reduced mass ν). Wiring controls: **W1** the Peters–Mathews
flux factor f(e) re-derived numerically from the quadrupole formula (STF tensor including the
zz = −r²/3 component, exact η-space chain-rule time derivatives): relerr ≤ 1.4×10⁻¹⁵ at e ∈
{0, .1, .3, .5, .7, .9} — the flux is verified at source, independently of the closed form.
**W2** circular generator vs Peters' closed form a(t): 8×10⁻⁸ (endpoint discretization, not
wiring: a 4× step change moves it 2×, not 256×). **P3** the circular family map round-trips
r → E → r to 10⁻⁴ M at r = 6.001 and hits 6.000 at the ISCO.

**M — the generator on the exact tube** (a₀ = 100M, ν = 0.25 unless stated; walls at ε_bar =
1% / 0.1% = the bars of B1-style behaviour / B2 periods):

| birth | orbits to plunge | a\*, e\* at handoff | wall 1% | wall 0.1% | orbits inside 1% / 0.1% | re-keys from 1000M (1%) |
|---|---|---|---|---|---|---|
| circ ν=.25 | 1929 | 6.00, 0 | 25.4M | 62.6M | 53 / 583 | 690 |
| e₀=.3 ν=.25 | 1468 | 6.3, .088 | 24.7M | 67.2M | 49 / 637 | 555 |
| e₀=.6 ν=.25 | 545 | 6.8, .000 | 26.1M | 100M (at start) | 53 / 545 | 547 |
| e₀=.9 ν=.25 | 18 | 7.2, .277 | 100M (at start) | at start | 18 / 18 | 345 |
| circ ν=.01 | 48230 | 6.00, 0 | 8.5M | 18.0M | 23 / 488 | 749 (e₀=.3) |
| e₀=.9 ν=.01 | 453 | 9.1, .000 | at start | at start | 453 / 453 | 345 |
| circ ν=10⁻³ (a₀=30M) | 21088 | 6.00, 0 | 6.3M | 8.5M | 3 / 233 | 0 |
| e₀=.9 ν=10⁻³ (a₀=30M) | 974 | 8.9, .469 | **no wall** | 31.9M | 0 / 974 | 0 |

Read off: eccentricity never grows (max e = e₀ in every run); the circularization-vs-shrink race
is decided by ν (residual e\* at plunge: 0.00, 0.00, 0.28, 0.00, 0.47 as ν falls / e₀ rises);
the handoff band is narrow and near-circular for ν ≥ 0.01; the total re-keys from 1000M are
O(10²–10³) over 10⁵–10⁶ orbits (0.005/orbit — the generator is a calendar event, not a cost).
The wall closed form (wiring-checked against the circular run: 62.6M measured vs 62M analytic):
a_wall^{5/2} = (384π/5)·ν·F̃(e)·(1/(2ε_bar))·… — i.e. the wall is a property of (ν, e, ε_bar),
so the engine can precompute it per binary family.

**PN — the 1% bar vs the Newtonian flux** (circular, ν = 0.25, t_merge from a₀ to 6M):

| a₀ | flux 1PN+tail (Newtonian family) | geometry (exact family) | both |
|---|---|---|---|
| 20M | +8.2% | −16.7% | −9.7% |
| 100M | +4.1% | −2.2% | +1.8% |
| 600M | +0.9% | −0.3% | +0.5% |

The 4πv³ tail partially cancels the 1PN term at small a (flux multiplier 0.92 at 20M, 1.11 at
6M). Net: pure Peters holds 1% only for a₀ ≳ 150M; the flux-only correction holds it to ~500M.

**P9 — the wiring rule**: drifting both (E, L) by Peters' two fluxes from a circular birth on
the exact tube pumps a spurious e = 0.81 by the end (the Newtonian dL/dt against the exact
family's dL/dE). The circular generator must project L onto the exact family (L(a) = √(a/(a−3)));
the eccentric path (both fluxes on exact elements) is internally consistent at Newtonian order.

## Predictions

[predictions.md](predictions.md), written before the run. **Held (P1: 1.4×10⁻¹⁵ ≤ 10⁻⁵; P3:
6.000; P7: 555 ∈ [300, 900]; P5 circular-half: 62.6M vs ≈62M; P8 at 100M: +4.1% ∈ [4, 8] and
1%-crossover ~500M flux-only ∈ [400, 700]).** **Failed, both reported as held-out misses with
diagnosed causes: P4** — I predicted wide-apastron plunge (a\* 15–150M at e₀ = 0.6–0.9);
measured 6.1–9.1M: Peters' de/dt circularizes faster than da/dt shrinks the orbit, so the
separatrix is met near-circular (the miss makes adoption simpler, not harder). **P9** —
predicted spurious e ∈ [10⁻⁴, 10⁻²], measured 0.81: the two-flux wiring is inconsistent, hence
the projection rule. **Partially failed: P2** (8×10⁻⁸ vs 10⁻⁹, endpoint effect, disclosed),
**P5 e₀=0.9** (wall ≥ 1068M by the corrected algebra — the run starts deep inside it; my range
[300, 900] was low), **P6** (wall/separatrix = 4.2 at the 1% bar, not ≤ 2 — but the honest
quantity is orbits inside the wall: 53 at 1%, 583 at 0.1%, bounded), **P8 at 20M** (+8.2% vs my
20–35%: the tail cancellation).

## The candidate, its source, and the scan (the lens's deliverable)

**Best candidate: adiabatic flux balance on the exact geodesic** — the orbit is the compiled
tube (zero work); radiation reaction is the orbit-averaged quadrupole flux balance drifting
(E, L); re-key events fire when the memo key is crossed; the separatrix hands off to the plunge
tube. Sources: **Peters (1964)** and **Peters & Mathews (1963)** — the flux factor **verified at
source** here by independent numerical derivation (W1); the merger-time closed form **verified**
(W2). Practitioners with skin in the game: LISA EMRI waveform models (adiabatic evolution of
eccentric geodesics; the lineage Gair–Bond–Hobbs 2011 "osculating geodesics", cited from
scout-a1a4's verified-title scan — **UNVERIFIED at source this run**) and population-synthesis
codes that integrate Peters for millions of binaries per run. Ranked alternatives: **TaylorT2/T4
PN phasing** (LIGO matched filtering — the same generator in (v, Φ), proof it scales to
10⁶ templates/s; **UNVERIFIED**); **osculating geodesics / self-force** (the fallback where
adiabaticity breaks — my walls say where the engine would need it: only if the bar is finer
than 1% in the last 50–600 orbits, or high-e EMRIs at 0.1%; **UNVERIFIED**); **Ori–Thorne
transition regime** (a few slow orbits through the homoclinic orbit before plunge — inside the
handoff, the plunge tube's business; **UNVERIFIED**). Rejected: numerical relativity (cost),
full EOB (no layer for it in the plane), 2.5PN force stepping (df81 already killed
inspiral-as-kicks; steps at 512/orbit contradict B9).

**Mapping onto the law:** state = the binary doll's tube (E, L) (law.md §State, 16 bytes); the
drift is one calendar event with slack = ε_bar·P/|dP/dt| (the min-plus queue's own key);
re-key = one cycle recompile (≈ 38 crossings at m = 16); the handoff predicate = the cubic's
bound root pair merging (u_p → u_3) — the **same surface** a1a4's plunge compile handles, so
plunge and inspiral-end are one boundary, not two; the chirp as news reaches the player at c
through the existing past-cone gather. Error type: staleness resets at each re-key — bounded,
never compounding (PRINCIPLES 13); no jet, no derivative store (df81's C·drift² avoided by
construction).

## What would make it wrong

- The **1PN+tail flux coefficients are from memory** (Blanchet 2014-style series; two web
  searches failed to surface the formula; nothing in the repo). A wrong coefficient moves the
  1%-crossover (150–500M) by ±2× but not the conclusion: the **geometry** term (−2.2% at 100M,
  exact-family algebra, round-trip-verified) alone breaks 1% inside ~200M.
- The exact family is the **test-mass** (ν → 0) family; the comparable-mass 1PN family (the EOB
  energy map, B11) differs at O(ν) — for ν = 0.25 the "geometry" column carries that error. The
  consistent EOB-mapped generator is the follow-up.
- **No independent full-GR oracle was integrated** (no 2.5PN osculating run, no Teukolsky
  fluxes): the adiabatic approximation error itself is unmeasured here; the literature puts it
  at O(few orbits) near the separatrix (Ori–Thorne) — inside our handoff.
- Eccentric strong-field accuracy is Newtonian ±(5–10)% (no eccentric 1PN fluxes — the
  Junker–Schäfer class is the adoption cost for eccentric binaries inside ~100M).
- P = 2πa^{3/2} is used for eccentric periods (the radial period differs by the precession,
  O(M/a)); the walls inherit that proxy. ε_bar is swept as a proxy because the memo key's actual
  (E, L) quantum width is not pinned in the docs — the real design derives ε_bar from the key
  width.
- Cost of adopting: one flux module + one calendar event type + the separatrix predicate
  (already implicit in the tube) + the 1PN circular coefficient; a B-gate on merger time (1% vs
  the 1PN-corrected generator, a₀ ≥ 20M), chirp shape, and residual e\*(ν) at plunge.

## PRINCIPLES fit

#3 "Compute only surprises… Nothing is evolved that can be derived when looked at" (zero work
between re-keys; 0.005 events/orbit); #6 "Store the generator, not the generated" (Peters' a(t)
analytic, the tube recompiled only at key crossings); #13 "Errors never compound" (staleness
resets each re-key; the generator recomputes, no jet); #22 "The simulation decides; heuristics
schedule" (the separatrix, not a heuristic ISCO, ends the inspiral); #33 "Each scale resolves
only what matters at that scale" (ν chooses the regime: adiabatic to the plunge at ν ≤ 10⁻³ vs
a 50–600-orbit chirp regime at comparable mass); #30 "we need to build towards GR" (the exact
tube is the geometry; radiation reaction rides on it, not inside it).

## The lens may have made me miss

The scout imports from a field whose requirement is waveform phase accuracy over 10⁵ cycles, not
game cost — that bias over-specifies (1PN fluxes) where a game may only need the chirp's shape,
and under-weights what the plane already owns (the memo quantum width should set ε_bar, not a
gate's bar). The scout also stopped at the separatrix: the merger/ringdown is the plunge tube's
business (a1a4), untested here, and the view side (the chirp as c-borne news through the gather)
was asserted, not measured. Nothing here touches the Kerr case (B19): eccentric inspiral into a
rotating hole has a different separatrix (χ enters), and that is the next rung up.
