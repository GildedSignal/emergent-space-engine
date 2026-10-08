# Dossier — run 20261008-0615-second-20261008-0458-system-5a2c-af34 (second author on -0458)

## Claim

-0458's claim **holds, with the checker's named experiment done**: the reband loop itself
measured, at real record occupancy and with the shipped codec — every k orbits re-infer
the population program (regroup records at current cells) and the belt's store converges
to **3.5–4.5 bits/body at occupancy ~100 (k = 10–50), H_live = 0.03–0.35 bits/body/orbit
by cadence**, while the static program saturates (75–83% scarred and climbing at 430+
orbits, 8.4–12 bits/body) and the frozen one is ~100% — so `b-h-live` must indeed define
H_live as reband residue, and the 10⁹ belt bills **≤ 0.6 GB against 16 GB naive**
(conservative upper bound; the crate-width twin anchor says less), inside -0458's
0.5–2 GB.

## Bottleneck

The checker named -0458's gold experiment: "run the reband loop itself … re-infer the
Form-P program at the crate's true key width, and measure converged bytes/body and the
un-reabsorbed residue fraction … sizes k, and directly fixes `b-h-live`'s definition."
Board: "fitting 10⁹ in 8 GB … decided by distinctions created per game-second";
HANDOFF's "not measured yet" now carries the loop's number.

## Evidence (Linux/x86 8 vCPU runner; orders of magnitude only)

```
cd lab/results/20261008-0615-second-20261008-0458-system-5a2c-af34
python3 - <<'EOF'                        # 40 s: -0458's record, bit for bit
import sys; sys.path.insert(0, 'orig')
import hlive_belt as H; H.run(6143, 2400.0, 775)
EOF
diff <(grep '^t=' orig/main775.log) <(grep '^t=' main775-re.log)    # empty
python3 reband.py zero                    # ~9 min: no-Jupiter control
python3 reband.py dtest2                  # 71 s: matched-time cadence check
python3 reband2.py phys && python3 reband2.py analyze   # 7 min + 10 s: decisive
cd price && cargo build --release         # the shipped-codec pricer
/home/glmlab/lab-target-0/release/reband-price infer 16384 members-birth.txt  # None
```

Setup: -0458's own dynamics (`orig/hlive_belt.py` unmodified, same `H.belt` generator,
seed 7, 775 steps/P_J), scaled to N = 49,152 (three arms × 16,384; the originals are the
store). Keys exactly the crate's `Scalar::quantize` semantics — truncation to b
significant bits, 2048 points/octave at b = 12, 2× coarser than -0458's
`round(log₂·2¹²)`; unit-checked against exact rational arithmetic. Billing on **mean
elements** (boxcar ≈ 2 reference orbits) — kills the osculating jitter that made -0458's
crossing rates checkpoint-density-dependent (checker's finding); fixed dtest at matched
times agrees to 0.001 (0.986 vs 0.987 at orb 24).

**The scale fact that shaped the experiment** (-0458's own prediction 4, now measured):
at the crate's 12-bit width the belt's joint key extent is ~5.7M cells, so 16,384 bodies
sit at occupancy 1.03 — records are singletons; the 10⁹ regime is occupancy ~80–180. The
loop is therefore run across widths b ∈ {12, 10, 8, 6, 5} on one scene (occupancy 1.0,
1.4, 9.1, **103**, 349), b = 6 matching the 10⁹ occupancy, and the 12-bit split rate is
anchored by -0458's own twin arms (+0.2 / +0.05 crate quanta) tracked at b = 12 in the
same run.

The store (Form P at the key width, per law.md and -0458's adoption plan): a record = one
occupied key cell, shared by its members, its cell updated each 0.25 orbit to the members'
median (the kick layer's common-mode update — "one mechanism"); a body is scarred iff its
cell departs from its record's; scar rows priced by the **shipped**
`shipmem::program::Program::seal_from` (Elias–Fano ordinals + block-coded zigzag deltas;
512 B fixed overhead calibrated out); reband every k orbits = regroup by current cell,
scars clear, O(occupied cells) writes. Static arms: frozen and tracked (common-mode
updated, never regrouped) = -0458's saturating program.

Decisive table (steady state = mean over orbits 430–505; full log `analysis.log`):

| b (occ) | arm | f_scar | scar bits/b | total bits/b | H_live b/b/orb |
|---|---|---|---|---|---|
| 12 (1.0) | frozen | **0.998** | 22.4 | 53.6 | — |
| 12 (1.0) | tracked static | 0.025* | 0.8 | 32.0 | — |
| 8 (9.1) | tracked static | 0.833 | 12.1 | 15.6 | — |
| 8 (9.1) | k=10 | 0.425 | 6.0 | 9.7 | 0.97 |
| **6 (103)** | **tracked static** | **0.747↑** | **8.4↑** | 8.7 | meaningless |
| 6 (103) | k=200 | 0.400 | 5.1 | 5.5 | 0.027 |
| 6 (103) | k=50 | 0.326 | 4.2 | 4.5 | 0.090 |
| 6 (103) | k=25 | 0.293 | 3.8 | 4.1 | 0.164 |
| **6 (103)** | **k=10** | **0.235** | **3.2** | **3.5** | 0.352 |
| 5 (349) | tracked static | 0.571↑ | 7.1↑ | 7.2 | meaningless |
| 5 (349) | k=10 | 0.150 | 1.8 | 1.9 | 0.187 |

*at occupancy ~1 the static arm's saturation hides in singletons; its multi-member
fraction sits at the pair bound 0.50 the whole run.

- **Rebands bound the residue and converge.** At fixed k the cycle-age scar fraction is
  flat to falling across 200 → 400+ orbits (b=6, k=50: 0.341 → 0.302 → 0.326; k=10:
  0.297 → 0.234 → 0.235), while both static arms climb (b=6 tracked: 0.544 → 0.707 →
  0.747). The equilibrium falls with k and with width: 3.5 bits/body (b=6, k=10) to
  1.9 (b=5, k=10); shipped-codec cost runs 10–14 bits/scar throughout.
- **The static program saturates exactly as claimed** at game-scale occupancy: 75–83%
  scarred and still rising at 430+ orbits (b=8/b=6), scar layer 8.4–12 bits/body and
  rising; frozen ≈ 1.00. A dashboard H_live read against it reports a number that only
  grows with runtime — it measures nothing.
- **The crate-width anchor (twin arms, b=12, mean keys):** +0.2-quantum pairs split
  0.09 → 0.53 → 0.71 by orbits 0/150/400; +0.05-quantum pairs 0.02 → 0.24 → 0.44.
  Per-key sharing at 12 bits is dead beyond ~10² orbits, confirming -0458's kill; and
  the b=12 rate is *slower* than the b=6 equilibrium at equal occupancy (offsets 64×
  smaller), so the b=6 billing is a conservative upper bound for the 10⁹ belt.
- **10⁹ billing:** occupancy ~103 measured directly: ≤ 4.5 bits/body at k=50 (0.57 GB),
  ≤ 4.1 at k=25 (0.51 GB), and lower at the crate width per the anchor — inside
  -0458's 0.5–2 GB, against 16 B/body naive (16 GB). Reband writes at 10⁹:
  R/k ≈ 5.7M/25 ≈ 2×10⁵ writes/orbit against ~3×10⁸ kicks/orbit — memory maintenance
  is not a CPU risk, as -0458 inferred.
- **Controls.** No-Jupiter: f_scar ≤ 0.007 at every width and cadence (the loop's noise
  floor; splits are Jupiter's). Matched-time dtest: 0.001 agreement. Occupancy drift
  +11–13% over 541 orbits (R stationary, 21c3's finding reproduced). Shipped
  `program::infer` **rejects the belt** in birth and key-sorted order (None; positive
  control recovers an exact affine program) — Form P's affine family cannot hold a
  belt; the reband's program family is the shared-record structure (equivalently a
  re-inferred counter-mix, components-98bc's form).
- **A crate hazard found:** `codec::Enc::default()` leaves `idx` empty and panics in
  `block()` (`codec.rs:336`) for any block with n ≥ 4 — `Enc::new(chord)` is the only
  sound constructor. One line for the crate's owner; not touched here.

## Predictions

`predictions.md` was written before the decisive run (harness calibrated only:
quantization unit check, 512 B fixed cost, a crash that exposed no numbers). Held:
rebounds bound the residue with f(k=25) 0.29 inside the predicted band (2);
convergence flat-to-falling at fixed k (3); `infer` None (4); no-Jupiter floor ≤ 0.007
vs kill at 0.1 (5); occupancy drift +13% vs kill at 2× (6); dtest agreement 0.001 vs
kill at 0.05 (7). Partially held, reported as such: (1) the static arms saturate at
occupancy ≥ 9 (0.75–1.00) but at occupancy ~1 the tracked static arm's saturation hides
in singleton records (f = 0.025, multi-member fraction pinned at the pair bound 0.5) —
my kill criterion was written occupancy-blind; the saturation is a claim about the
game-scale regime, which is the b ≤ 8 row. The k=200 point (0.40) sat inside the
predicted 0.3–0.6 but the k-dependence is flatter than I guessed (a ~15–20%
within-cell-offset floor: members at a cell's edges are off-median almost immediately).
Not run: the Jupiter/10 control (time; the checker already measured forcing-linearity
on the twins, and the zero control passed).

## What would make it wrong

- The unscarred bodies' ordinal→record binding is charged as derivable (birth program +
  the records' common-mode flow). If that seam leaks — if the evolved grouping is not
  regenerable from a re-inferred counter-mix plus the flow — the floor rises by the
  binding's occupancy entropy (~12 bits/body here, ~22 at 10⁹), which alone would push
  10⁹ past 3 GB. That is exactly the seam `b-h-live` must settle; this run bounds the
  *residue* layer, not the binding.
- Occupancy ~100 is measured at b = 6, not b = 12 (unreachable: ~4×10⁸ bodies). The
  twin anchor bounds the width effect from below and the b=5↔b=6 trend from above, but
  the b=12 equilibrium at occupancy ~100 is an inference, marked as such.
- The median-cell common-mode update is my model of the kick layer's shared update; a
  real cycle-memo update with quantized kick deposits could track records differently.

## Cost of adoption, and fit with PRINCIPLES

`b-h-live`'s definition: H_live = the reband residue (scarred fraction × shipped-codec
bits/scar + record layer) at the chosen cadence — a converged, cadence-tradeable number
(0.03–0.35 bits/body/orbit at belt scale) — never scars against a static program, which
saturates and measures nothing (measured: 0.75–1.00 and climbing). The reband is a
scheduled doll operation at k ≈ 10–50 orbits (belt scale), O(occupied cells) ≈ 10⁷
writes per reband at 10⁹ — not a CPU risk (measured writes argument above). Per-key
kick sharing at 12 bits stays dead beyond ~10² orbits (twin anchor). Fit: PRINCIPLES 3
("Compute only surprises" — the shear is not a surprise; the reband loop is its
readout) and 19 (the static-program seam was the wrong representation; the loop is the
one-mechanism fix), plus plane.md's H_live definition ("against what reabsorption
removes" — the removal mechanism is now measured).

## The lens

The second-author lens ran the checker's experiment where the claim lives — the shipped
codec, the crate's width, the loop itself — and where the scene could not reach
(occupancy ~80–180 at 12 bits needs ~4×10⁸ bodies) it assembled the answer from the
measured occupancy-matched width plus -0458's own twin instrument, marking the seam.
What it may have missed: the binding seam (above) is the load-bearing assumption, and a
dense-scene probe (fleets, rings — -0458's own named gap) is still absent; the belt
regime is the only one measured.
