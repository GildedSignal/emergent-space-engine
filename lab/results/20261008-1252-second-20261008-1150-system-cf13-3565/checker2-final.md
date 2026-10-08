Working...
**Grade: silver** — written to `check2.md`.

**Reproduction:** complete. Every row of `scenes.jsonl` and `boundary.jsonl` — all six scenes × four configs, the W_SAFETY boundary runs, both kick scenes and the exit policy — reproduced with identical counts (pairs, evals, checks, sections, renewals, half_win, missed, false, matched); only wall times differ on the shared runner. All dossier ratios recompute from the rows. `work/patch.diff` is empty; the experiment is self-contained. Predictions predate the record by file times, with the smoke-run disclosure intact; P1–P5 held as claimed.

**Attack — one real break, two holds:**
- **QUIET** (station-keeping fleet, e~10⁻⁶ vs ρ/r=10⁻⁴): the band certificate **misses 21,764 of 81,985 encounters (26.5%)**; the cone finds all. Root cause: the meeting bound is |Δλ| ≤ 2(e_i+e_j) **+ ρ/r**, but `w_enc = 2.5·2·e_hi` covers the chord term only multiplicatively — exact while e_hi ≳ ρ/r, vanishing as e_hi→0. The comment "2.5 covers ρ/r" is wrong in exactly that way, and every recorded scene sits at e_hi/ρ ≥ 40. Formations are the phase tier's motivating workload, so this regime matters. `W_SAFETY=4` (≈ the missing term) restores 0 missed at 13,867/19,900 pairs — the fix is one additive term.
- **ECC60** (e=0.6, just below 5e<π self-destruction): 0 missed; numeric bound 2·max|ν−M| = 2.52 < 3.0 — the center-equation margin holds to the threshold, as disclosed.
- **DRIFTC** (clusters drifting together at t≈0.95·t_end, renewals clamped to 64): 0 missed — the renewal union bound holds at the horizon edge.

**Why not gold:** the exactness claim is load-bearing under the lab's zero-miss standard and carries a silent validity condition that a legitimate scene breaks by a quarter of all encounters. One experiment separates it from gold: add ρ/r to `w_enc` and rerun the scenes plus a quiet-formation family sweeping e_hi/ρ. Adversarial work ran from a scratch copy (`/tmp/check2/exp-adv`); the run folder holds only `check2.md`.
