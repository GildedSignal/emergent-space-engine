# Dossier — H_live measured by estimate: bounded iff the generator is re-fit

Run 20261011-0006-fermi-2a9d, Fermi lens. Machine: GitHub Actions linux runner, 8 vCPU,
idle. Scripts: `h_live.py` (Monte Carlo, 7 min, <1 GB), `sweep.py` (falsification
sweep + no-jump control, 4.5 min), `budget.py` (the 10⁹ budget table, <1 s). Raw points
in `results.json` and `sweep.json`. All under 60 s per reproduction step except the two
Monte Carlos, which are ≤ 7 min each.

## Claim

H_live — the live distinguishing information per body — is bounded in steady play **iff
the population's generator is re-fit to the kicked ensemble** (a mechanism `shipmem` does
not implement: its reabsorption is return-to-base only, measure-zero under diffusion).
Measured at N = 2²⁰ with r8-belt encounter rates: a frozen birth program loses every body
to a full scar record within ~350 orbits (50–62 bits/body; 7.75–16 GB at 10⁹); generator
re-fit holds the element state at a measured table-resolution floor of 4.3–6.1 bits/body
(knot-count-controlled, `sweep.py`), leaving the **label permutation** — ½·log₂t per
walking column plus a measured constant 4.29 bits, i.e. 16 bits at ~1.2×10⁷ orbits — as
the only growing term. At 10⁹ bodies memory, not compute, breaks first: 16 GB naive
(2× over) against 0.5 GB (re-fit floor) to 4.3 GB (re-fit + 3-column labels at t = 8×10³
orbits).

## Bottleneck

Board risk "**Distinctions created per game-second (H_live): they, not the body count,
decide whether 10⁹ fit in 8 GB; not measured yet**"; bottleneck 5. This run measures it
by estimate ahead of the queued `b-h-live` build and hands that build held-out numbers.

Gains, in orders of magnitude:

- **Steady-state memory**: 50–128 bits/body un-reabsorbed → 4.3–6.1 bits re-fit floor
  (+ labels). ~1.3–1.5 orders; the difference between 16 GB (broken) and ~0.5 GB.
- **Accounting**: law.md's "+62 bits per kick" is an un-reabsorbed *record* cost (B18b
  derives 50 = 9+11+15+15; a scar row adds the Elias–Fano rank); the true information
  birth per kick is the delta's differential entropy — measured 2.10 bits at σ = 1 cell
  (5.37 at σ = 10, both matching the formula log₂(4.13σ) to 0.05 bits). The "−60 per
  reabsorption" has no mechanism in the tree.
- **Law choice**: phasors (memo R2) vs today's 64 kicks/orbit moves the information
  *birth rate* by ~10⁴× (64×3 bits vs 2.1×10⁻³×8.7 bits per body-orbit).

## Evidence

### The 10⁹ budget table (`python3 budget.py`, <1 s)

Quiet smooth belt at a = 2.7 AU (P = 4.4 yr), N = 10⁹, rtf 100, M1 constants from
`docs/HANDOFF.md` §"The machine"; every rate traceable in the script header:

| term | value | verdict |
|---|---|---|
| kick compute, today (64/orbit × 24 µs) | 1.11 P-cores | fits (tight) |
| kick compute, averaged (0.3/orbit, H0190) | 0.005 cores | free |
| encounter certification (r8, 786 work/encounter) | 0.0000053 cores | free |
| tube-write bandwidth | 0.001 GB/s vs ~60 | free |
| memory, naive 16-byte tube (law.md) | **16.0 GB** | **breaks (2×)** |
| memory, belt program (gold 98bc, 0.126 bits) | 0.016 GB | fits |
| memory, program + re-fit floor (measured) | 0.53 GB | fits |
| memory, + 3-column labels at t = 8×10³ orbits (measured) | 4.34 GB | fits (tight) |
| memory, un-reabsorbed encounter records (62 bits, ~all hit by t ≈ 10⁴) | **7.75 GB** | **breaks** |

**Memory breaks first**; compute never binds at rtf 100 in a quiet belt (encounters are
certificate-tier, adopted q-candidate-degree; 2.1×10⁻³/body/orbit at fixed density).

### The Monte Carlo (`python3 h_live.py`; N = 2²⁰, one trajectory, two store policies)

Dynamics: diffusion s cells/orbit + close-encounter jumps at r = 2.135×10⁻³/body/orbit
(r8 v2 belt 0: 427 encounters / 10⁴ bodies / 20 orbits), J = 100 cells. Store policies
are codes for the same state; the dynamics never read them. Main run (s = 1, λ = 1
body/cell, J = 100, T = 8192): ever_hit = 100%; H(δ) = 2.10 bits/orbit (jump alone 8.69).

| t (orbits) | frozen scar (bits/body) | re-fit residual (m=256) | label permutation |
|---|---|---|---|
| 1 | 2.14 | 2.25 | 1.76 |
| 8 | 3.80 | 3.27 | 3.77 |
| 64 | 5.97 | 4.43 | 6.01 |
| 512 | 8.61 | 5.37 | 8.62 |
| 4096 | 10.29 | 6.07 | 10.28 |
| 8192 | 10.79 | 6.32 | 10.79 |

- Both frozen scar and label permutation grow at **+0.51 bits per doubling** (½·log₂t),
  and coincide (rank and cell displacement carry the same variance at λ = 1).
- The label entropy is exactly modelled as ½·log₂t + log₂(4.13·λ√(2s² + rJ²)):
  constant measured 4.29 against 4.31 modelled. **16 bits at t = 1.2×10⁷ orbits** with
  r8-belt jump rates (J = 100 cells); the no-jump control pushes it to ~10⁸.
- Held-out runs (s = 0.1, s = 10, λ = 32, J = 10) in `results.json`: same slope
  everywhere; H(δ) = 5.37 at s = 10 against log₂(4.13·10) = 5.36 predicted.

### The falsification sweep (`python3 sweep.py`)

Is the re-fit residual's growth information or table resolution? m-knot budget swept on
the jumped trajectory (s = 1, J = 100, T = 4096):

| m | residual (bits/body) | program (32m/N) | total |
|---|---|---|---|
| 256 | 6.08 | 0.008 | 6.09 |
| 1024 | 5.64 | 0.031 | 5.67 |
| 4096 | 4.76 | 0.125 | 4.89 |
| 16384 | 3.76 | 0.500 | 4.26 |

It is resolution, not information: the floor falls monotonically with m and the program
cost stays negligible to m = 16384. But it does **not** reach ≤ 2 bits at any measured m:
the honest floor for this program class at this spread is ~3.5–4.5 bits/body, and m
should be sized from the measured spread (B18b's dyadic quantile tables are the
scale-free way to spend knots in the tails; uniform-in-rank knots are what I measured).
No-jump control (s = 1, r = 0, T = 8192): frozen = 8.60 bits against 8.55 predicted,
label = 8.60 against 9.05 — my pure-diffusion constants were right; the main run's early
crossings came from the encounter-jump variance I folded into prediction 4 but omitted
from predictions 1 and 3.

### What is implemented vs what the law's budget line needs

- `crates/shipmem/src/program.rs:284`: "all-zero rows are reabsorbed" — return-to-base
  only; under diffusion P(return to the exact base) ≈ 0.
- `crates/shipmem/src/shelf.rs:820`: `compact()` repacks into **fresh dense blocks** —
  bounds cost at the dense store, deletes no distinctions.
- `docs/law.md` line 13: "about +62 bits per kick and −60 per reabsorption". The +62 is
  the right order for a scar *record* (B18b's 50-bit derivation plus the EF rank); the
  −60 needs generator re-fit: re-emit the population as a bijection over the *current*
  ensemble (quantile table + sorted matching, O(N log N) per epoch, the same order as
  `compact()`'s repack), legitimate because the dynamics are exchangeable (kicks iid
  across bodies given the shared field) and identity is provenance.
- B18b charges churn as permanent 50-bit replacement kicks at 1%/epoch — the
  un-reabsorbed picture, ~2 orders gentler than today's kick law's actual churn (100%
  per 1/64 orbit; the memo's coupling point).

## Predictions

`predictions.md` was written before the run; one arithmetic slip corrected at 00:16
before any output existed, disclosed there. Outcome:

1. **Frozen-scar form held** (+0.51 bits/doubling), **crossing constant failed ~10×**:
   measured crossing of 8 bits at t ≈ 350 against 3.8×10³ predicted — I folded the
   encounter-jump variance into prediction 4 but not into this constant. The no-jump
   control (8.60 vs 8.55 predicted) proves the diffusion constant was right; the jumps
   make it worse, which strengthens the claim.
2. **Failed as stated** (≤ 2 bits): the measured floor is 4.3–6.1 bits depending on m,
   and the sweep shows the growth is table resolution, not information (above). The
   claim's substance survives at a worse constant, with m a measured design knob.
3. **Form held exactly** (constant 4.29 vs 4.31 modelled with jumps), **crossing failed
   ~10× early** (1.2×10⁷ orbits, not 2.5×10⁸): same omitted-jump slip, same diagnosis.
4. **Held**: H(δ) = 2.10 measured against 2.05 predicted at s = 1; 5.37 against 5.36 at
   s = 10. The +62-bit line is record cost, not information.
5. **Held**: ever_hit = 100%; the re-fit absorbs the jump news in the element columns
   (6.32 bits against the frozen 10.79 at t = 8192, and ~3.8 with adequate knots).

Two of five constants failed with one diagnosed cause (encounter-jump variance omitted
from two constants while correctly included in a third). Nothing was retuned after the
fact; the corrected formulas are stated, not refit.

## What would make it wrong

- **Resonant/multi-modal marginals.** Diffusion keeps the marginal smooth, so quantile
  programs fit it. A resonance-sculpted belt (Kirkwood gaps) or fleet formation
  structure is multi-modal: residual grows with the marginal's *structure*, and the
  program class must widen (mixtures, joint (U,V,W) tables). The honest kill case for
  the floor, and what the B18 red-team's tail tests guard at birth — not after churn.
- **Correlated kicks** (shared tide, one perturber): the shared part is smooth and
  program-absorbable — makes re-fit stronger, not weaker. Breaks independence only via
  resonance, covered above.
- **Joint 3-column matching**: my matching is 1D-optimal (sorting). Per-column matching
  composes only while columns are independent (true at birth; encounter jumps correlate
  U and e). Joint structure can multiply the floor by up to the column count.
- **The label permutation is real state** under "identity is provenance": re-fit cannot
  delete it, only a canonical-relabelling rule for *unobserved* bodies can — a law
  decision (identity-through-time) that belongs to Julien. Measured deadline: 16 bits/
  column at ~1.2×10⁷ orbits at r8-belt rates, so 3 columns ≈ 40+ bits/body ≈ 5 GB at
  10⁹ near t = 10⁷–10⁸ orbits — inside the 10¹⁰-year universe goal, not inside any
  session. The decision is not urgent; it is not optional forever.
- **The engine's own kick magnitudes** (my s and J in cells) were not measured; the time
  axis scales with √(2s² + rJ²). Measuring them is `b-h-live`'s first number.

## Cost of adopting

One idle-time pass in `crates/shipmem` (generator re-fit: quantile build + sorted
match, O(N log N) per epoch, cheaper than the repack it usually replaces), with m sized
from the population's measured spread, plus one dashboard counter. No gate edits: B18/B18b
judge the store; this changes which store form wins, and the gate already reports (not
gates) bytes at 10⁹. The law's budget line should be re-derived as: "+ ~2–5 bits per
kick (true birth, log₂(4.13σ)); re-fit holds the steady state at the table floor
(~4 bits measured) + the label permutation (½log₂t + 4.3 at belt rates); 50–62 bits is
the no-reabsorption record cost".

## Fit with PRINCIPLES

- **6. Store the generator, not the generated.** The generator must be re-emitted as the
  ensemble drifts, or it stops being the generator — the whole content of this run.
- **24. The memory floor is information.** The floor is the re-fit residual (measured),
  not the scar record; the law's line currently budgets the record.
- **3. Compute only surprises.** An exchangeable kick is not a surprise; only the label
  permutation and player-pinned distinctions are.
- **1. Less is more.** Re-fit deletes the per-body scar store at 10⁹ — the cheapest
  compute is the record never written.

## The lens (what Fermi may have missed)

Orders of magnitude, one element column, iid diffusion with one jump size. Missed,
knowingly: observation pinning (the player's light cone bounds it, unmodelled — it
converts label entropy into player-visible identity); the e-columns' deterministic shear
under phasors (favorable: program-computable, zero bits); multi-modal marginals (the
main kill case); a jump-size distribution instead of one J (real encounters are a power
law in impact parameter — a heavy jump tail fattens the marginal faster than my J = 100,
and the label constant grows like ½log of its second moment); and the engine's real kick
sizes in cells, which set the clock. The m-sweep's uniform knots also understate B18b's
dyadic tables, which are the scale-free version of the same knob — a builder should
re-measure the floor with them before freezing any number.
