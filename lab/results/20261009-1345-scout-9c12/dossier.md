# dossier.md — 20261009-1345-scout-9c12 (scout lens)

## Claim

Julien's bet that the player's influence series converges ("a series that
converges i bet", OC) is measured for the first time: it holds at belt scale
with today's certificate floors (0 births in 100 orbits from 8 scarred ships)
and fails structurally — super-linear scar growth — wherever any of four
conditions holds (planet-crossing flybys, floors at q ≲ 1e-9 relative,
compounding error, co-orbital fleets), and the failure lands in **bytes, not
compute**: scars change encounter outcomes, never encounter rates.

## Bottleneck

The growing light cone (HANDOFF "Risks to attack first", OC#50; the only live
risk with no queue owner). The question restated: does the set of
player-caused distinctions stay bounded as play age grows? Expected gain:
deletes the fear "we cannot handle the universe anymore" as a compute
question and replaces it with one measurable budget line — scar-birth rate vs
idle-time program re-fit rate (shipmem). Orders of magnitude: at play scale
(one hour at 100×: 3–11 orbits) the live frontier is ≤ ~10² bodies in every
configuration except a fleet; at qualification scale (1e10 yr) the frontier
saturates any N, so the entire question moves to reabsorption.

## The candidate found (scout deliverable)

The structure "a disturbance that branches through interactions, decays
multiplicatively, and dies below a quantum" is a **branching random walk with
an absorbing barrier** (log ε walks by log f per encounter; absorbed below
log q). Source, verified: Hu & Shi, "The critical random barrier for the
survival of branching random walk", arXiv:0911.2227 (also Ann. IHP B 48(4),
2012). Mechanism mapped to our engine: ε = a scar (shipmem's exact difference
from a population program); encounters are the branching events (r8's 1.1 per
body per orbit); the barrier q is the certificate floor; sub-barrier mass is
**accumulated** (PRINCIPLES 6) in cell pools; saturation of a finite N is SIR
burn-out. The same lens is the garbage collector's generational hypothesis
("most objects die young", verified: Python Language Summit 2026 post on
generational GC): scars are objects, the player is the root set, idle-time
recompression is collection. UNVERIFIED analogies I did not source-check:
Kermack–McKendrick final size, percolation of epidemic waves.

Known failure mode of the candidate (from the probe, not the literature):
barriers do not stay put — a single amplifier (a planet flyby, f_p ∈ [139,
634] at B13's 1.5–3.2 R_p) refills the high-ε cloud through the ε cap, so
the effective growth exponent is NOT the flyby rate but the Malthusian rate
of the joint process (measured 0.0716/orbit at ν_p = 0.01/orbit, 7× my
prediction).

## Evidence

Machine: shared Linux x86 runner, load average 3.9–4.1 at start, 8 vCPU.
Timings are wall seconds; orders of magnitude only.

    cd lab/results/20261009-1345-scout-9c12 && python3 probe.py   # 27 s total

Model (predictions.md, derived before any run): encounter impulse
I = 2Gm/(b·v); a partner's position error ε maps to child error
ε·f(b)·|cos θ|, f = 2Gmτ_drift/(b²·v_rel). Belt: m = 1e12 kg, v = 5 km/s,
τ = 1e7 s ⇒ f ∈ [3.9e-6, 0.267] over b ∈ [1 km, mutual Hill 2.6e5 m]; rate
1.1/orbit (r8's belt); N = 1e6; ε₀ = 8e-4 (a 30 m/s burn drifted half an
orbit); live = ε ≥ q; below q, transfers accumulate and can cross later.

| run | n_live(100) | births/orbit early→late | verdict vs prediction |
|---|---|---|---|
| base (q=1e-6) | 8 | 0 → 0 | P1 ✓ (0 ∈ [0,4] births; dusted 838, 942 ∈ [700,1100]) |
| q=1e-8 | 160 | 1.6 → 1.4 | bracketing point |
| q=1e-9 | 719 | 7.3 → 6.8 | P3 ✓ ([500,2000]; [6,12]) |
| crossers ν_p=1e-2/orbit | 10,373 | 2.9 → 526.6 | supercritical ✓; exponent 0.0716 vs predicted ≈ ν_p = 0.01 ✗ (7×) |
| crossers ν_p=1e-1/orbit | 600,000 (cap) | 30.3M births total | supercritical ✓ (saturated the live cap mid-run) |
| chaos λ=0.1/orbit | 845 | 0.1 → 11.6 | P4 ✓ (×116 ≥ ×5; [100,1e4]) |
| fleet 1e4 @ 20/orbit | 172,875 | 495 → 1,832 | P5 ✗ magnitude (predicted 2e4–5e4, 316±30%): direction ✓, 3.5–5× over |

Play scale (one hour at 100× = 3 belt orbits, 11 inner orbits): n_live(3) =
8 (base), 32 (q=1e-9), 9 (crossers 1e-2), 8 (chaos), 10,949 (fleet). The
frontier is invisible at play scale in every case but the fleet.
Qualification scale (1e10 yr): every super-linear case saturates N; even the
linear q=1e-9 pump (7.1/orbit from 8 ships) saturates 1e6 in 1.4e5 orbits;
the base belt's rate is 0, so it never saturates. Geometric cone (analytic,
not simulated): one play-hour at 100× sweeps radius 3.6e5 light-s ≈ 72 AU —
the star system; cone-area costs saturate with the system, then with the
galaxy doll.

Reproduction: seeds fixed (0; base also seed 7), outputs `out-*.json` in
this folder, per-run wall times 0.1–23 s. One instrument bug was found and
fixed mid-run (asteroid births silently dropped; flyby branch unaffected);
the fix is in `work/`-visible history and all numbers above are from the
fixed instrument, rerun end to end.

## Predictions

See [predictions.md](predictions.md), written before any run. Held: the
central bet at belt scale (P1: subcritical, 0 births), the fine-floor
behaviour (P3: linear, constant rate, children near the floor), the chaos
acceleration (P4). Missed, twice, the same mechanism: amplifiers couple back
into the weak channel through the ε cap — flyby children sit at the cap
(0.5) where nearly every encounter births, so the growth exponent is the
Malthusian rate of the loop, not the flyby rate (P2: 7×; P5: 3.5–5×). This
miss is itself the finding: **the barrier is refilled by the amplifiers it
shields**, so no single-channel R₀ is safe; the engine must measure the joint
rate.

## What would make it wrong

The transfer model is linearized impulse scattering; at f ≫ 1 (deep flybys,
B13's chaotic-scattering domain) it is order-of-magnitude only — the
supercritical verdicts there are robust (any f > q/ε births), but the
exponents are not. Scalar ε drops vector phase (resonant kicks could channel
error faster). Dust→dust propagation is ignored, which under-counts births
(biased in favour of the bet). r8's 1.1/orbit is borrowed, not re-measured
here. If the real engine's re-fit (program recompression) cannot absorb
scars at the measured birth rates, the byte conclusion flips from "bounded"
to "unbounded" — that is the named next experiment, on the real belt (B18b,
b-belt-wire), not this toy.

## Cost of adopting, and fit

Adoption is a criterion, not code: track two dimensionless numbers per
region — birth condition ε·f/q per channel, and saturation budget
(birth rate)·T vs N — and schedule program re-fit so it outruns the measured
birth rate (it is the convergence mechanism, PRINCIPLES' "idle time goes to
recompression" made load-bearing). Cost: one counter per population plus a
re-fit cadence rule; no new component. Deletions it enables: any per-body
sub-quantum bookkeeping (cell pools suffice), and the open-ended fear line
in HANDOFF becomes two numbers with thresholds.

PRINCIPLES fit: "Compute only surprises… influences below one quantum
accumulate" (3, 6) — the barrier and the pools are exactly this; "regimes are
chosen by dimensionless numbers" (4) — the criterion is dimensionless; "The
player is the only wildcard, and their influence travels at c" (5) — the
frontier is the wildcard's residue, and the measurement shows c-bound
propagation is not the threat, branching is.

## The lens

The scout searched for the best foreign frame and found one (branching walk
with absorption), but the frame arrived with a blind spot I then hit myself:
single-channel reasoning (my R₀ = ν_p prediction) is wrong when barriers
refill. The lens also under-serves the engine's side: reabsorption (program
re-fit) was modelled as absent, so all byte conclusions are lower bounds on
pressure, not forecasts. And this run measures a toy calibrated by hand;
b-h-live (queued) measures the real belt's distinction rate and will
supersede these numbers.
