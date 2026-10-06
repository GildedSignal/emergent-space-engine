# Dossier — 20261006-1354-fermi-c9fa (lens: Fermi)

## Claim

At 10⁹ bodies the 8 GB M1 budget is bounded by **compute, not memory**: the
programs-plus-scars store absorbs encounter distinctions for **1–9 days with zero
reabsorption** (90-min orbits), while tide kicks at the plane's RTF 100 need
**153 cores today** (19× over) — and one number, the live set S_live (bodies off
program form), is capped by kicks at **5.2×10⁷** where memory would tolerate
5.4×10⁸. "Fitting 10⁹ in 8 GB" is decided in the ALU, not the RAM.

## Bottleneck

Board focus item "fitting 10⁹ in 8 GB … decided by distinctions created per
game-second" and plane.md's H_live line (the 5 October outside review). Gain:
not a speedup — a sizing law that deletes the memory-first framing and fixes the
independent variable (S_live, not N) for B10/B18-at-10⁹ and the encounters
design. It also quantifies bottleneck 3 ("10–100× less") exactly: **20×** on
kick cost at RTF 100.

## Evidence (all from `budget.py`, 0.07 s; anchors in `anchors.json`)

Reproduce: `python3 lab/results/20261006-1354-fermi-c9fa/budget.py` (cwd = repo
root; full output in `budget-out.txt`). Anchors are measured, not assumed:

- **Memory holds for days.** Generator floor 15 MiB (0.126 bit/body, gold
  components-98bc); encounter scars at the measured hits rate (5.9×10⁻³ per body
  per orbit, steady.jsonl converged over 10⁵ orbits; sweep rate 2.0×10⁻²) × 64
  bits fill the frozen 4 GiB cap in **5.7 d / 1.7 d** at 90-min orbits, **92 d /
  27 d** at 24-h orbits. shipmem already reabsorbs (return-to-program) and
  repacks (shelf.rs `compact`), so this is a floor, not a requirement.
- **Compute binds first.** Kicks: 32.5/orbit (H0190) × 29 µs (H0210) at 10⁹,
  90-min orbits → **175 cores at RTF 1 unaveraged** (tide averaging is
  load-bearing even at RTF 1, not polish), **153 cores at RTF 100 averaged**
  (19× over the 8-core M1); RTF 10 averaged = 15 cores (2× over). A 20× kick cut
  (29 → 1.4 µs, Sol's kick job + cadence) makes RTF 100 fit inside one core-budget.
- **The unified variable.** S_live ≤ 5.2×10⁷ (compute, RTF 100, 29 µs) vs
  5.4×10⁸ (memory). Feed rate 1086–3704 scars/s → **reabsorption deadline 4–13 h**
  to hold the compute cap — compatible with idle-time compaction. With 1.4 µs
  kicks the compute cap lifts above the whole population (108%).
- **P5, a design law:** any *resident* per-body encounter store breaks memory:
  16 B/body = 3.7× the 4 GiB cap; the killed r8 tiers measured 575–51,587 B/body
  (134–11,700× over). Certificates must be program-derived (a smooth belt's
  phase neighbours are ordinal neighbours, ~0 bytes) plus per-scar entries.
- **Cross-checks.** My independent reconstruction of the board's "~190 cores"
  line gives 175 (−8%); H0190's own averaged rate (0.01 core per 10⁶) gives 10
  cores at 10⁹ RTF 1 vs my 1.5 — same order, probe kick heavier. Bandwidth at
  RTF 100: 0.3–36% of 60 GB/s for 32 B–4 KB touched per kick (locality matters,
  not binding).

## Predictions (predictions.md, written before the run)

- Held: P1 (153 ∈ [100, 200]), P2 (175 ∈ [140, 220]), P4 (caps 5.2×10⁷ and
  5.4×10⁸; compute binds 10× first), P5 (5.8–14.9× over at 25–64 B/body), P7
  (175 vs 190, within 30%).
- Partially held: P3 — fill time 5.7 d ∈ [2, 10] at the steady rate, but the
  sweep's higher hits rate gives 1.68 d, 16% below my predicted lower bound.
- **Failed, instructively:** P6 — hits/body/orbit is NOT ∝ ρ across the scale
  sweep; the sweep holds ρ·N fixed and hits are N-invariant (±6%) at 0.020,
  while at fixed n hits ∝ ρ (steady vs sweep at n=3000: 3.34× ρ → 3.34× hits).
  Both rates are carried; the invariant to quote is "fixed physical
  neighbourhood ⇒ ~0.02 encounters per body per orbit".

## What would make it wrong

- A scene where encounters are 100× denser than the measured belts (war zones,
  dense rings): fill time drops to ~hours and the reabsorption deadline to
  minutes. Battles are bounded scenes by design (plane.md), but a dense-ring
  universe would flip memory back to first place.
- Secular chaos that is not program-formable: resonant belts (H0203: resonance
  kills averaging) may individualize bodies without encounters; the belt gold
  covers smooth belts only.
- Kick cost falling anyway (Sol's job) makes the 20× number stale — that is the
  intended fate of this result.
- RTF at 10⁹ being 1–10 rather than 100: then only a 2× kick cut is needed and
  this dossier overstates the urgency (Julien's "compared to real time" does not
  fix the target).

## Cost of adoption, fit with PRINCIPLES

No code. Three sizing laws to carry into B10/B18-at-10⁹ and the encounters
design: (1) report S_live, not N, as the independent variable; (2) certificates
program-derived, never resident per body; (3) reabsorption cadence ≥ hourly at
90-min-orbit populations. PRINCIPLES 24 ("the memory floor is information"):
confirmed — the floor is 15 MiB and the live-information budget is compute-bound.
PRINCIPLES 12 (smoothness): the kick deficit is 2.55 core-seconds per 16.7 ms
frame at RTF 100 — no allocator can schedule around it; the kick cut is
load-bearing. PRINCIPLES 21 (rough first): orders of magnitude only, anchored on
frozen evidence.

## The lens (what Fermi may have missed)

Orders of magnitude hide constants I did not measure: the orbit mix of a real
10⁹ universe (mostly outer orbits → everything relaxes: 24-h orbits give 27–92 d
fill and 63–214 h deadlines); the true scar width distribution (multi-column
deltas at wide quanta could double bits); and the cost of a *scarred* body's
kicks (I charged the plane's 29 µs; a recompiled cycle kick may differ either
way). I also could not measure anything on the M1 — all costs are quoted from
M1-measured evidence (H0190, H0210) and this box only did arithmetic.
