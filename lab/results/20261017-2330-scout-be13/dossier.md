# Dossier — 20261017-2330-scout-be13 (scout)

## Claim

The galaxy doll's smooth Φ program **is** producible from binned monopole cells below
the measured disc-churn switch-on, at a priced grid: a 256×1024 log-polar cell program
(≈ 2.6×10⁵ numbers ≈ 2.1 MB, flat in N) holds the field to **med 0.0028 / p90 0.0062**
against 2da8's eps_eff ≈ 0.008 bar, converging ~h² in cell size — while the multipole
order is not the lever on smooth scenes (m ≥ 2 is flat), dipole centring is *worse* at
every grid, the softening couples to the grid (a finer aggregate quantum demands finer
cells), and the clustered scene still fails at every swept grid ≤ 64×256 — and my own
first decisive run had killed the same claim with an instrument artifact (a grid mask
dropping 2–5% of the mass, caught by a mass-conservation control now shipped in the
script).

## Bottleneck

The handoff page's own named hole — "Galaxy: a *given* smooth Φ(r) — how the multipole
cells produce that program … is the unmeasured half" (lab/wiki/handoff.md, Domain;
Headed next 6, the galaxy phase). Gain: the production half goes from unmeasured to
**priced and passing** at game scale (one design sentence to adopt), with the failure
boundary located (clustered sub-cell structure + the ε–grid coupling) instead of a
build attempted blind. It deletes the "the program's cost/fidelity at galactic scale is
unknown" risk before the galaxy phase spends a window on it.

## Evidence (this run's scripts; numpy 1.26, shared 8-vCPU box, peak RSS < 0.5 GB,
## every number regenerated at least twice with identical digits after the fixes)

Commands, in `lab/results/20261017-2330-scout-be13/` (outputs shipped as
`galprogram.out`, `confirm.out`; `regen.sh` reruns both, ~3 min):

- `python3 galprogram.py` (71 s) — the sweep. Scenes: a two-arm exponential disc
  (arm contrast 0.3) and the lab galaxy-scene shape (Zipf clusters on the arms); N ∈
  {10⁵, 10⁶}; program = polar log-grid density (8–64 radial × 256 azimuthal cells),
  truncated at |m| ≤ {0,2,4,8,16,32,all}; truth = the same bodies' field, identical
  Plummer softening (ε = 0.05 R_d) on both sides, so the error isolates the program.
  400 test points, R ∈ [0.2, 4.8] R_d. Bar = 0.008 (2da8's churn switch-on, low end).
  A mass-conservation control prints `grid carries 1.000000 of the mass` per arm.
  - **m-flatness (smooth):** N = 10⁶ at 64×256: m = 2 → 0.0392, flat to m = 128 →
    0.0389; m = 0 fails at 0.0443 (the control that can fail, fails).
  - **m pays (clusters):** N = 10⁶ at 64×256: m = 0 → 0.0620, m = 2 → 0.0539,
    m = 128 → 0.0114 — still failing the bar; clustered sub-cell structure is high-m
    and sampling-limited (arm power/noise 2.7× at 10⁵, 3.8× at 10⁶).
  - **Lumps (bodies vs the coarse program):** smooth 0.0409 → 0.0389, clusters
    0.0136 → 0.0114 (10⁵ → 10⁶): N-weak — the cell's continuum quadrature error,
    not sampling noise.
- `python3 confirm.py` (109 s) — the pass and the dials. Smooth scene, N = 10⁶, all
  modes, geometric (monopole-at-centre) cells:
  - 64×256 → 0.0389/0.083 (med/p90), 128×512 → 0.0115/0.025,
    **256×1024 → 0.00279/0.0062 = PASS** (h² convergence: 3.4×, 4.1× per halving).
  - Centre-of-mass (dipole) centring is **worse at every grid**:
    0.0532/0.0267/0.0041 — near cells punish displaced mass; the monopole at the
    geometric centre wins; at 256×1024 COM's p90 (0.0110) is over the bar.
  - Softening scan at 256×1024 (COM): ε 0.05 → 0.02 → 0.01 gives 0.0041 → 0.0268 →
    0.0536 — the aggregate's quantum and the grid must move together.
  - Program numbers at the passing grid: 256×(2·m*+1) with m* ≈ 2–4 → ~2.6×10⁵
    numbers ≈ 2.1 MB at 64-bit (≈ 0.4 MB at the engine's word widths) — no per-body
    bytes.

## Predictions

See `predictions.md` (written before the decisive run; the "what happened" section
includes the instrument-artifact record). Of the four held-out predictions: 1 is
wrong for the smooth scene (m* ≈ 2, flat) and right-shaped only for the clustered
one; 2 is the lever (h² convergence, once my mask bug was fixed); 3 is wrong (the
residual is binning bias, N-weak, not √N sampling); 4 is right (2.1 MB). The
pre-registered kill criterion did **not** fire after the instrument fix. The first
run's kill ("N-invariant 1.8% floor at every resolution") was manufactured by my own
grid dropping r < 0.02 bodies (2–5% of the mass) — caught by a mass-conservation
check, not by the sweep it corrupted; a second bug (summation chunk step ≠ slice
width) briefly quadrupled all forces and was caught by magnitude. Both controls are
now in the shipped scripts.

## The candidate (scout deliverable), ranked

Requirements as numbers: 10⁹ bodies in a disc; program ≪ bytes/body (P6 "store the
generator", P24 memory floor); fidelity below eps_eff ≈ 0.008–0.025 (2da8's measured
churn switch-on); integer aggregation, deterministic (P2). Candidates:

1. **Polar log-grid monopole cells (grid Poisson / PIC deposit class), measured
   here: PASSES at 256×1024** on the smooth scene — 2.1 MB, m ≤ 4, h² convergence,
   geometric centring. This is the practitioner shape (density on a grid, force from
   the grid) at the engine's own cell vocabulary.
2. **Barnes–Hut/FMM opening** (Barnes & Hut 1986; Greengard & Rokhlin 1987;
   UNVERIFIED at the source this run): the measured facts point at it for the
   *clustered* scene — its high-m, sampling-limited sub-cell structure is exactly
   what opening near cells solves; the near ring joins the kick layer (P33's
   raindrop line: the ant's raindrop is a ring of cells, not a body).
3. **Biorthogonal SCF basis** (Clutton-Brock 1973; Hernquist & Ostriker 1992;
   UNVERIFIED at the source this run): buys bytes, not fidelity — the smooth scene
   is already m-flat; it cannot help where the binding axis is spatial.
4. **Timing-wheel / MVCC incremental update** — orthogonal (the news side,
   gravity-news's page); unaffected.

Adoptable sentence for the galaxy phase: the smooth Φ program is 2–4 azimuthal
moments on a log-polar grid of ~2.6×10⁵ monopole cells (mass at the geometric
centre, never the COM), refreshed only where density news arrives, with the cell
scale tied to the aggregate's quantum; clustered structure is the kick layer's
(near ring), not the program's.

## What would make it wrong

- The pass is measured **only on the smooth two-arm scene**; the clustered
  (lab-scene-shaped) scene fails at every grid the sweep reached (≤ 64×256) and its
  fine-grid behaviour is the one named experiment left — if 256×1024 still fails
  there at N = 10⁶, the program needs the near ring (candidate 2) or 10⁹-style
  sampling before it clears the bar.
- 2-D razor-thin disc with Plummer softening, float, no vertical structure: the
  engine's integer multipoles and a real disc's thickness both change the constants,
  not (on this evidence) the ranking. The bar itself is 2da8's low-end switch-on;
  at the 0.025 end the pass has 9× headroom, at 0.008 it has 2.9×.
- The 10⁹ composition rests on the measured N-weakness of the residual and the
  measured N-scaling of the spectrum floor (2.0×10⁻⁶ → 2.2×10⁻⁷ per decade), not on
  a 10⁹ run [INFERENCE].

## Cost of adopting, and PRINCIPLES fit

Cost: none now (no engine code); the design sentence plus two probes (clustered
fine-grid; 3-D thickness) precede any build. Fit: P6 "Store the generator, not the
generated" — the program is the generator, ~2×10⁵ numbers for 10⁹ bodies; P22 "the
simulation tells us what's next, not us" — the m-flatness picked the lever; P33 "an
ant cares about a raindrop but the lion does not" — the measured separation is
spatial (near ring vs program), not spectral; P2/P13 — the artifact confession keeps
the error type of the *instrument* on the record, which is what let the kill invert
instead of shipping a wrong floor.

## The lens's blind spot

The scout reads other fields' requirements as ours: astronomers accept %-level
systematics because collisionless evolution is their question; this run's bar is a
gameplay-fidelity bar (2da8) — and the same sensitivity is why the instrument had to
be controlled twice before its numbers meant anything. I also did not test the
engine's actual galaxy scene constants (the handoff page's rtf-2e10 disc), and I
accepted 2-D: thickness is the most likely place the constants move.
