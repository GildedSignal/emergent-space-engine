Working...
**Grade: silver** — written to `check2.md`, with the author's wiki page corrected in place. Tree restored clean (only `lab/results/` untracked, as the runner left it).

**What held under reproduction and attack:**
- `regen.sh` from a clean tree: `seam2.json` **byte-identical**; every dossier number recomputed with independent code and confirmed (record 3.677 radii, circles radius-exact 144/144, |Δw| max 0.357, 76 fixed points with 51 w-wobbling, μ paired 84%/71%, strong-walker saturation 1.03). The probe's shipped-API claims (`raw(φ,3)` = 8φ slip, μ ∈ [1,2) doll domain, bind.rs mirrors) all check against source.
- Depth 512 (next decade): 0 refusals, envelope still 3.68. μ at 1.0001/1.6/1.999: benign, 0 refusals — μ covered across [1,2). My variant was validated first: on the default grid it reproduces the author's 864-chain record field-for-field.

**What didn't hold — the silver reason:** at even phases (1/4, 1/2, 3/4 turns — outside the author's odd-eighth grid) the mid-walk refusal class the dossier calls "not a measured class" *is* measured: 5/648 chains refuse past step 64 (`fit:Range` steps 87–175, `cartesian:Range` 161), record 3.98 radii. The dossier's explanation ("their probe's word handling differed") is wrong — it's a phase-class effect. Retrograde starts add 10/864 entry refusals. Plus two record defects: μ is 1.28 exactly (not "1.2846") and the census "294" sums to 304.

**Path to gold** (named in check2.md): fold the per-class refusal budget into the corrected census — a one-line grid change, under 2 minutes of runs. The physics conclusion (anchor w+t before demote-at-commit) survives every attack; the record just claimed slightly more than the grid showed.
