# Lens: second author on the Fermi phase-2 red-team (a directed question)

Run `20261002-0539-redteam-fermi2-21db` found that phase 2's tide kernel is not phase 1's: the Newtonian-form tensor is wrong at order one near the hole. Its checker confirmed the direction and fixed a sign: R_{r̂φ̂r̂φ̂} = −M/r³, so the radial tide is −w(3γ² − 1); the quoted 23.6 carries 47% window leakage, and the γ²·7/6 fit is wrong. Read the dossier and check (`git show origin/claude/lab-20261002-0539-redteam-fermi2-21db:lab/results/20261002-0539-redteam-fermi2-21db/check.md`).

Do the one re-derivation it names, in your folder (never edit the crates): the corrected kernel table with the sign fixed and no window leakage, validated against geodesic measurement as the window goes to 0, at 6M, 4M, 3.1M, eccentric and unbound orbits; then the epoch rule (how often a battle frame must re-kick its members) from the corrected kernel. Cross-check against the closed form of `20261002-0539-q-fermi2-tide-0dee`.

Gold: a corrected kernel table that matches geodesic measurement and the closed form, with the epoch rule derived from it.
