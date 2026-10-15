# regen.sh — regenerates every number in dossier.md
# Run from lab/results/20261015-1747-redteam-de98/. Runtime ≈ 15 s.
# Requirements: python3 with numpy, scipy (present on the runner).
set -e
cd "$(dirname "$0")"
python3 eob_doll.py 2>/dev/null | tee regen-output.txt
echo "---"
echo "Key rows (grep from regen-output.txt):"
grep -E "C1 doll|C1b|P1|PLUNGE|P5|census" regen-output.txt || true
