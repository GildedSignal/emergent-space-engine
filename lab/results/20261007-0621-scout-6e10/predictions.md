# Predictions — run 20261007-0621-scout-6e10 (written before the decisive experiment)

Question: what is H_live (live distinguishing bits per body per unit of play) on the plane's
workloads, and does its steady state fit 10⁹ bodies in 8 GB? The ledger in law.md assumes
"+62 bits per kick, −60 per reabsorption" as a **flow**; the store holds a **stock** (each
scarred body holds one scar = its current offset from its program). These differ.

## Cases I have not tuned on, and what I expect

The replica: belt = B18b's scene (banded p, Rayleigh e, uniform angles) under Laplace–Lagrange
secular evolution from a Jupiter, quantized to the law's grid at each epoch; battle = a fleet
born on one orbit (0 bits/member) scattered by Poisson contact kicks. Entropies are empirical
integer-delta entropies at quantum 2⁻²⁴ of each column's range (2⁻¹⁶ and 2⁻³² as brackets).
Controls: a belt with no perturber must show exactly 0 scars; a battle with 0 kicks must show
≈0 residual bits. If a control fails, the instrument is broken and everything below is VOID.

- **P1 (belt, secular + grid only).** The secular flow keeps the family smooth: every body
  leaves its birth lattice (scarred fraction → 1 within a few epochs), but the scar is a
  *differential precession* offset whose entropy grows diffusively (log-like), not linearly:
  ≤ 2 bits/member/epoch at 2⁻²⁴, and a program that carries t (a time-dependent generator)
  predicts it to ≈0 bits. Falsifier: if measured scar entropy ≥ 10 bits/member/epoch at 2⁻²⁴,
  secular drift alone fills memory and the "orbit is a good behaviour" premise (Julien, 30 Sep)
  is wrong at the grid.
- **P2 (belt + encounters).** At belt encounter rates (r8 v2's belt: ~10⁻²/body/orbit,
  UNVERIFIED N≈2×10³, 427 encounters / 20 orbits), scarred-by-encounter bodies accumulate
  irreversibly (a scattered body never exactly returns): steady-state contribution
  < 0.5 bits/body after 1000 orbits; 10⁹-belt extrapolation < 100 MB.
- **P3 (battle — the load-bearing one).** Post-battle, a best-fit program (shared drift +
  slot-indexed component) recaptures only the shared part; chaotic scattering decorrelates
  slots: residual ≥ 90 bits/member (≥ 70% of a bare 128-bit tube), i.e. a fought-over fleet
  becomes per-member state ≈ tubes at ~16 B each. If residual < 50 bits, memory is elastic
  and there is no war cap — my central claim dies.
- **P4 (stock ≠ flow).** A body kicked K times stores one scar whose entropy ≈
  log₂(σ√K / quantum) + O(1) — sub-linear in K. The +62-bits/kick flow model overcounts the
  steady-state stock by roughly K/5. Consequence: H_live's budget line should be written in
  bits of *stock per scarred body* and *bodies scarred per second*, not bits per kick.

## Kill criteria

- P1 ≥ 10 bits/member/epoch → belts are not free; the memory question is much harder than
  the board assumes.
- P3 < 50 bits/member → war recapture works; no tube cap; delete the war-cap claim.
- Either control failing → VOID, rerun with a fixed instrument.

## What the numbers feed

The 8 GB ledger: births (program bits, measured by the gold belt run) + secular stock (P1,
≈0 if programs carry t) + encounter stock (P2) + war stock (P3, the only term that can fill
8 GB: it caps simultaneous war-distinguished bodies at ≈ free_bytes/16 B ≈ 2–3×10⁸).
