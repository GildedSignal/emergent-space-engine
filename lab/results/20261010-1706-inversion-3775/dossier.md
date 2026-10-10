# Dossier — run 20261010-1706-inversion-3775 (lens: inversion)

**Claim.** The co-orbital certificate's premise (gold 20261006-0346: concentration = a formation;
"every real encounter within partner rank 4 along the orbit"; fix = phase-neighbour certificate at
O(n·k), triggered by a dimensionless concentration number) fails on the **breakup cloud** — the
concentration the game itself mass-produces (every death, collision, wreck): the cloud is a *null
plane* in Binet space, the cone filter retains 100% of its pairs (~37 TB of candidate state at
10⁶ fragments, permanently), its phase neighbours churn so a per-orbit-cadence rank-4 certificate
misses 46% of real encounters at N=4000 (97% in the compact-blob phase), and 14–39% of its
encounters live at per-pair second foci no shared-focus certificate can see; an **epoch-stream
sort at the shared focus** covers the main stream exactly at 3–4 checks per encounter, flat in N.

**Bottleneck.** The board's top scaling risk (5 October): candidate pairs per body grow with N;
candidate work must track real encounters. The gold answered it for formations; this run shows the
answer's domain excludes the scene one breakup event creates. Expected gain of adopting the
correction: deletes the quadratic tier's 100%-retention blow-up for plane populations (one
O(N log N) sort per fraction of an orbit replaces O(N²) pair state), and it re-routes the queued
build `b-coorbital-cert` before it ships rank-4 + an element trigger that cannot work here.

**Evidence** (`python3 breakup.py`, 11.6 s, deterministic seeds; floats explore, integer counts
decide; machine in results.json: Xeon-class 8-vCPU runner, load recorded; cloud timings are
orders of magnitude only, per the rules):

| measurement | number |
|---|---|
| cloud cone retention (N=4000, σv/v0=1e-3) | 7,997,999 / 7,998,000 pairs = **99.99999%** |
| null-plane fit ‖U+V−1‖∞ (θP=0) | **3.3e-16** (exact) |
| belt control retention (a∈[0.8,1.2], Rayleigh e 0.02) | **16.8%** (a tighter e-first belt gave 55% — both reported) |
| formation control (lattice train, N=1000) | 67,796 encounters, **0 misses**, max rank 2 (gold reproduced) |
| phase cert at per-orbit cadence, mixed age (256 orbits) | misses **3.2%** (N=300), **24%** (N=1000), **46%** (N=4000) |
| same, compact-blob age (0.25 orbit) | **96.6% missed** (N=1000) |
| partner circular rank *at conjunction* | median 1, max 6 at every N (adjacency is real) |
| partner still within rank 4 after Δ | N=4000: 99% at T/8, 91% at T/4, **35% at T/2** → ≥4 re-sorts/orbit |
| epoch-stream cert at P (window 3b/v0) | **0 misses** at every N; window pairs / encounter = 3.0 / 3.0 / 3.0 / 4.1 / 2.9 (N=300…4000) — flat |
| at-P encounter rate scaling | 0.97 / 12.7 / 257 per orbit at N=300/1000/4000 (∝N², ratios 13.1 and 20.2 vs 11.1 and 16) |
| second-focus (Q_ij) encounters vs at-P | **14%** (N=300), 27% (age 0.25), 60% (age 4), 37% (N=1000, age 256), **39%±14** (N=4000) |
| element spreads (σa/a, ē, ϖ resultant) | cloud 0.0020/0.0020/**0.013**; belt 0.116/0.025/0.036; formation 0/0.05/**1.0** |
| cone-probe (16 random others inside one's cone) | cloud **1.0**, formation 1.0, belt 0.17 |
| pairwise tier on one 10⁶-fragment breakup | 5×10¹¹ pairs → 1.25–12×10⁶ core-s setup (14.5–139 core-days), 37 TiB at 80 B/pair |
| truth validation (P7): windowed analytic d_min vs full Kepler | max rel err **0.4%** (n=30 sampled true encounters) |

Mechanism (derived, then measured): orbits through a common point P satisfy
r0·(U+V cosθP+W sinθP)=1 — a plane whose normal is *null* in the cone metric, so by Cauchy–Schwarz
every pair on it crosses; the cone condition is literally the crossing condition, so the filter
cannot remove anything. The formation is the degenerate point on the same plane. Miss distance at
a shared-focus co-passage is v0·|Δt| (both bodies transit the point at orbital speed), so the
timing window is universal (b/v0): one sorted epoch stream per focus finds all of them. Element
statistics cannot see the plane (a/e tight like a formation, ϖ uniform like a belt); the
cone-probe can.

**Predictions** (predictions.md, written before the run, v2 corrected pre-run when the exact
two-crossing truth machinery revealed two errors in v1's physics): P2 ✓, P4 ✓ (flat work, zero
misses, universal window), P3'' ✓ (adjacency real), formation control ✓. Missed, honestly:
P1's belt bound (16.8% vs <10%), P3's magnitude at mixed age (46% at N=4000, not >80%; the blob
phase did hit 97%), P5's "cloud spread belt-like" (it is 13–57× tighter in a,e, uniform in ϖ),
P6's "at-Q within ×2 of at-P" (measured 0.14–0.39×; the conclusion it supported — per-pair work
stays Ω(N²) — survives: even 14% on per-pair foci keeps the pairwise tier quadratic). Kill
criteria did not trigger.

**What would make it wrong.** (i) The engine never materializes candidate pairs (the cone filter
stays implicit and lazy) — then the 100% retention costs nothing until a kick re-set walks it;
the churn and Q-stream misses stand regardless. (ii) Real breakups are far more eccentric than
σv/v0=1e-3 around circular — the plane and its null normal are exact for any breakup at one point,
but the epoch-stream window and the 14–39% Q-share were measured in the near-circular regime only.
(iii) Ship-scale play means clouds of N≈10²–10³: at N=300 the per-orbit cadence misses only 3%, so
the phase certificate nearly works there — the failure is a fleet-scale statement. Cost of
adopting: the certificate becomes "sort passage epochs through each detected focus" (O(N log N)
per sort, ≥4 sorts/orbit at N=4000) plus the cone-probe trigger; the at-Q residue and the 100%
plane retention under kick re-sets remain open — the honest endpoint is that plane populations
want their *generator* (one breakup event = birth point + epoch + dispersion, the shipmem program
form), not N² pair state.

Fit with PRINCIPLES: principle 32 ("under the right representation many symmetries can appear") —
the symmetry is the null plane, found by changing the question from "who is near whom" to "what do
all these orbits share"; principle 33 ("a body resolves only the influences significant at its own
scale") — the cloud resolves at its focus, not in pairwise space; "invert, always invert" — the
scene is the one the engine's own success (fleets die) guarantees.

**The lens.** Inversion found what the gold's own frame hid: the gold asked "how do we find
formation encounters cheaply" and answered with the formation's invariant (static neighbours);
asking "how does this certificate guarantee failure" found the scene where the invariant churns.
What this lens may have missed: I did not test eccentric or inclined breakups (the plane is exact,
the numbers are near-circular), nor the interplay with the slack skin, and the at-Q stream's
structure (θ_Q = 2·atan2(ΔW,ΔV) depends only on the Binet difference direction — possibly itself
concentrated for breakup clouds) was measured but not exploited.

Commands: `cd lab/results/20261010-1706-inversion-3775 && python3 breakup.py` (≈12 s, <200 MB);
outputs `results.json` (all integers exact, seeds fixed).
