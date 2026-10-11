# Dossier — 20261011-0324-second-20261011-0224-taleb-236b-55a8

**Claim.** The taleb-236b record now regenerates end to end and every gap the
first checker named is closed, and the claim survives with one material
amendment: rank-k in mean anomaly is indeed not a certificate in e-dispersed
co-orbital families (confirmed against the corrected conjunction record, the
capture-bias-free truth, and differential precession), but the right fix is
not per-pair crossing-offset windows — it is ordering by **mean longitude**,
where every contact lies within a first-order universal offset
|Δλ| ≤ 2(e_i+e_j), so a one-window-per-body certificate sized by the
tangential (Binet dT) e-vector dispersion is zero-miss: k=32 for the realistic
formation, k=8 at the trigger boundary, k=128 for a full collision family —
and it does not drift under differential precession at any rate tested.

**Bottleneck.** The board's top scaling risk ("candidate work must track real
encounters") and the queued build `b-coorbital-cert` (two lanes). This closes
the pre-freeze probe: the M-ordering certificate is dead as taleb-236b
claimed; the offset-window fix it proposed is superseded by a cheaper
λ-window with no per-pair geometry; what is genuinely quadratic is only the
multi-clump bulk interception (S2), where both fleets coincide in phase by
construction — the encounter-skin problem, not candidate discovery.

**Evidence** (seed 20261011; each command ≤ 60 s, all in this folder):

- **Regeneration.** `python3 probe.py 1e-4` → metrics bit-identical to the
  published `work/orig/metrics-R1e-04.json` except timing (25 s).
- **Conjunction record** (`python3 probe2.py conj`, 4 s → `probe2-conj-*.json`):
  10,077 S4 pairs whose ΔM crosses 0 in 24 orbits, exact misses 1.04e-4–0.540 —
  the checker's numbers exactly; **0 pairs below R=1e-4, 4 below 3e-4**, so
  "conjunctions are non-encounters" is R-relative, not absolute. The author's
  "59 conjunction pairs, misses 0.02–0.33" is unreproducible under any natural
  reading (contact∩conjunction = 262 pairs, 131 with misses in [0.02,0.33];
  8,831 conjunction pairs in that range). Tail attribution: the 3.4% rank≤4
  tail is the degenerate co-elliptic branch (|Δϖ| ≤ 0.012, bottom ~2% of the
  pair distribution, crossing offsets |ΔM*| ≤ 0.010) — on the crossing branch
  proper the M-drop is ~100%.
- **Dense truth** (`python3 probe2.py dense`, 21 s): 929 contacts (checker 1's
  independent finder: 928); the author's finder undercounts 58 (6.2%).
  Mechanism: **all 58 missed pairs have 4–23 coarse approaches** (slow
  epicyclic neighbours) and the one-approach-per-pair refinement picks the
  wrong dip — not the stated capture condition: **max v_rel at contacts is
  0.0092**, 3× below the 0.03 that condition requires (refutes my PD2 and
  checker 1's stated condition alike). frac 0.0344 / median 73, unchanged.
- **The ordering is the representation** (`python3 circ.py`, 32 s; `python3
  lam.py`, 35 s; `s2-cross-lam.json`). At a contact, ΔM* ≈ −Δϖ (first order)
  but Δλ* = 2(e_j sin ν_j − e_i sin ν_i) (second order) — the opposite sign to
  checker 1's point-4 formula. Measured: S1 max circular λ-rank 110 against
  the bound-predicted 107; S2 cross-group |Δλ| = 0.170 ≤ 2(e_i+e_j) = 0.2.
  Zero-miss λ-windows: **S4 k=32 (max 18), S5 boundary k=8 (max 8, 97% at
  k=4), S1 k=128 (max 110)**; in M no finite window (S4: k=64 catches 45%).
  The boundary case S5 (cone 0.65, e pinned) — where the failure "persists
  mid-cone" in M — is a λ-non-failure: **the gate is the e-vector dispersion
  dT, not the cone fraction.** S2's cross contacts sit at |Δλ|=0.170 with
  ~400 bodies inside (two clumps side-by-side in λ): k ~ n/2 in any ordering.
- **Precession — the missing experiment** (`python3 probe2.py prec`, 13 s, and
  the circular-λ pass, 12 s → `probe2-prec-*.json`, `prec-circL.json`):
  differential apsidal precession σκ ∈ {1e-3, 1e-2, 5e-2} rad/orbit (churn up
  to 1.7 rad ≫ σΔϖ) plus a rigid control. M-rank-4 fails identically at every
  κ (frac 3.3–3.7%, median 65–74); crossing offsets drift with slope **−0.97**
  against Δκ·t — the ΔM* ≈ −Δϖ law, so M-offset windows must refresh at the
  element-change rate; the rigid control is bit-identical to κ=0. The
  encounter rate grows only 871 → 1125 (0.121 → 0.156 per body per orbit):
  precession sweeps pairs through alignment, but each alignment yields a
  contact only when passages coincide (~1% timing dilution). The λ-certificate
  is precession-robust: **circular-λ zero-miss at k=16 at every κ** (max rank
  15–17), caught fraction at k=4 rising 0.62 → 0.87.
- **Frozen lists:** t=0-frozen rank-4 catches the same ~3% as live in S4's
  tight formation but only 27% vs 100% live in the S0 shear control — refresh
  cadence is drift/spacing in every ordering (the element-change rate).

**Predictions** (`predictions.md`, written before any probe2 run; the only
prior execution was the base regeneration). Held: PA1/PA2 **exactly** (10,077;
1.04e-4/0.540), PA3, PC (tail co-elliptic), PD1 (929 ∈ [900,950]), PD3
(v_rel ≤ 0.01), PE (boundary 4.6%/49 in M), PF1 (rigid identical), PF3
(structure survives all κ), PF4 (slope −0.97), PF6 (λ ≥ M everywhere). Missed,
disclosed: **PD2 refuted** — the finder's misses are multi-dip pairs, not fast
pairs; **PF2 wrong by 30–80×** (predicted 30–90k events at σκ=5e-2, measured
1125 — I missed the simultaneous-passage dilution); PB — my range (150–700)
held but no reading yields the author's 59: that number is simply wrong;
PF5 — held for S4, but S0's frozen catch is 27% against my ≤20% bound.

**What would make it wrong.** The λ-bound is first order in e: e ≳ 0.3 is
untested (largest here: S1, e ≤ 0.11, where the bound is tight, 110 vs 107).
λ needs each body's ϖ — the same e-vector state the cone fraction uses, so no
new information. The offset during approach (contact not exactly at the
crossing) is measured negligible (median |ΔM−ΔM*| = 4.8e-5). **Cost of
adopting:** the build lane replaces "rank 4, gate on cone fraction" with
"circular mean-longitude ordering, window k ≈ 4·dT/λ-spacing, ordering
refreshed at the element-change rate" — one window per body, no per-pair
crossing geometry, no offset drift under precession; O(n·k) preserved with k
measured 8–128. Multi-clump interceptions stay O(n·clump) in every
representation — by construction, not by representation failure. Fit with
PRINCIPLES: "we just need to have the right representation so that math is
trivial" (18) — λ is the along-orbit coordinate in which crossing offsets
collapse to second order; "a fix signals the wrong representation" (19) — the
M-offset windows were a fix on the wrong ordering; "under the right
representation many symmetries can appear" (32); "the simplest, most powerful
form" (35).

**The lens** (second author): I repaired the record first and let the
instruments talk; the blind spots: all measurements again share one harness
(my Kepler, my rank) — a checker should re-derive the λ bound on an
independent propagator, as checker 1 did for the original claim; the λ-window
k is local-density-dependent, so a 10⁶-ship hierarchical fleet needs a
per-region k (the same machinery as the dyadic sheets), untested here; and
the precession is imposed per-ship apsidal drift, not the design's own
GR/secular field — the 1:1 drift law and λ-robustness should survive, but the
~1% timing dilution that sets the encounter rate belongs to the motion-law
lane.
