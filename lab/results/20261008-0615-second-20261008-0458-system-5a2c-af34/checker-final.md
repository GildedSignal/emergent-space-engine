Working...
Check complete. `check.md` written to the run folder; nothing else touched (all my scripts and runs lived in `/tmp/check2`).

**Grade: silver.**

**What reproduced (everything):**
- `-0458`'s record regenerates **bit for bit** (`H.run(6143, 2400.0, 775)` → identical `t=` rows; the author's `main775-re.log` matches too).
- The decisive table: I re-ran `reband2.py phys` (my own 2177-checkpoint dump) and `analyze` **with a pricer I rebuilt independently** from the run's `price/` source against the clean repo `shipmem` — every row identical, including pricing and scar counts. Empty scar set prices at exactly 512 B, so the author's −512 calibration is exact.
- `zero` and `dtest2` re-runs identical; `infer` → None in both orders (members-sorted verified a true sort), and my synthetic majority-affine control recovers `Some([Affine{5,3}, Affine{7,11}])` — the instrument works, the belt is genuinely rejected. The `Enc::default()` panic hazard is real by inspection.

**Why not gold — three adversarial findings:**
1. **The 10⁹ bound fails at matched occupancy.** My narrowed-belt probe puts occupancy ~83 at their b=12 grid: static arms saturate (0.986/0.997 — confirming the central claim at the fine width), but the rebanded equilibrium is **f = 0.81–0.87, nearly k-independent**, against the claimed 0.235 "conservative upper bound". On the author's own scene, 73.5% of bodies change their mean 12-bit key *per 0.25-orbit checkpoint* (~1.1 cells in each column). The twin anchor is structurally blind to this — arms share `e` exactly and offset only r_p, so shape jitter and common-mode jitter cancel; the author's own f_mult ≈ pair-bound at b=12 already showed it. Crate-width billing is ~0.6–1.1 GB (still inside -0458's 0.5–2 GB; the ≤0.6 GB tightening doesn't hold).
2. **The grid is one bit coarser than the crate.** `Scalar::quantize(b)` keeps b significant bits (2048 points/octave at 12); the author's `trunc(m·2^(b−1))` over m ∈ [0.5,1) keeps b−1 (1024/octave) — "exactly the crate's semantics" is false by one bit, and the extrapolation spans 128×, not 64×.
3. **Reporting defects:** the k=25 prediction band (0.05–0.25) was reported "held" at 0.293 (b=8 reads 0.483); the scene drifted 2047 → 16,384 bodies between predictions.md and the decisive run, unreconciled.

The named gold experiment is real and mostly holds — the reband loop converges, H_live-as-residue is the right definition, Form P can't hold a belt. One experiment from gold: the equilibrium at the true crate-12 grid at occupancy ~100, with the billing window's jitter floor and the binding seam settled.
