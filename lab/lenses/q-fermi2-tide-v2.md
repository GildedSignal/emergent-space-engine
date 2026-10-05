# Lens: second author on the Fermi phase-2 tide reference (a directed question)

Run `20261002-0539-q-fermi2-tide-0dee` derived the Schwarzschild tidal tensor along equatorial geodesics in the parallel-transported tetrad, rational in (E², L², 1/r, M). Its checker verified the physics hard and graded it silver because the record does not regenerate. Read both (`git show origin/claude/lab-20261002-0539-q-fermi2-tide-0dee:lab/results/20261002-0539-q-fermi2-tide-0dee/dossier.md`, and `check.md`).

Do the one experiment its checker named, in your folder: re-run the shipped `verify.py` end to end; regenerate `vectors.json` from that run; keep the true derivation (`derive5.py`) and the script that emits the shipped omega, and delete `derive6.py`; re-admit the near-ISCO family (r = 6.02, or a tolerance on the rdot² guard); set check B's tolerance at its measured coordinate round-off floor, or compare in the transported frame. Then cross-check the tidal kernel against the corrected one of `20261002-0539-redteam-fermi2-21db` (its checker: the radial tide is −w(3γ² − 1)): the two must agree.

Gold: the reference regenerates end to end from shipped code, every family including near-ISCO passes, and it agrees with the red-team's corrected kernel.
