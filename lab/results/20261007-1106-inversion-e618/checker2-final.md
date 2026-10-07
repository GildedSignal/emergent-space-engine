Working...
Check complete. `check2.md` written; tree restored to HEAD; no commits.

**Grade: gold** — blind second checker, all criteria met:

**Reproduced** (clean tree, `git apply work/patch.diff`):
- `invert smoke`: 232 encounters (gold: 233), dist-rank ≤ 2, lon-rank ≤ 3, `val_miss: 0` against the full O(nc²) scan — matches the dossier exactly.
- Headline row (nc=3200, σ_e=0.001, σ_λ=0.01, seed 7): identical in every field to `sweep2.log` (lon>4 = 0.661, occ 20.9/50, enc 59030).
- Predictions genuinely held out: mtimes 11:16 (predictions) < 11:18 (first sweep) < 11:51 (decisive sweep) < 11:56 (dossier).

**Adversarial (5 cases of my own)**:
- Seeds 8/9 at the cliff config: lon>4 = 0.674/0.664 (predicted ±0.15; actual spread 0.013).
- Isotropic apsides: lon>4 = 0.695 while **distance-rank — the gold's own evidence metric — shows max rank 4**. The gold's instrument looks perfect exactly where the certificate misses 70% of contacts.
- nc=6400: lon>4 = 0.818, occ 40.5 — occupancy doubles per nc doubling (20.9 → 40.5 → 79.7).
- Independent occupancy probe at fleet scale: nc=12800 → 79.7 (bit-identical to the scan's average via a different code path), nc=10⁶ bunched → **6190** (≈ 446 GB of sections at 72 B — the ruin arithmetic now measured, not extrapolated), uniform → 36.0 (claimed ≈35), σ_λ halved → 12223.
- Verified `Section` = 72 B and the gold's code measured distance-rank while certifying a phase order.

**Novelty/goal fit**: no prior occupancy critique in the record; moves the board's top scaling risk by showing an adopted gold's premise (constant k=4) is wrong at its target scale. PRINCIPLES #19 (wrong representation), #4 (occupancy is the dimensionless number), "measure before claiming".

**Noted misses** (in check2.md, none blocking): the gold's nc=800 point was uniform-λ, so its bunched evidence was only nc=200 — the inversion is *stronger* than the dossier claims (8.6% miss already at nc=800 bunched); true-longitude rank is a conservative floor for a mean-longitude order; table rows mix 1/2-orbit horizons.
