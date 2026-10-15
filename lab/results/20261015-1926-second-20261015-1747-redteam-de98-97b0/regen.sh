#!/usr/bin/env bash
# Regenerates every number in dossier.md from the shipped scripts.
# work/patch.diff is empty for this run (no tree edits outside the run folder).
set -e
cd "$(dirname "$0")"
if [ -s work/patch.diff ]; then
  echo "work/patch.diff is non-empty but regen runs from the run folder's own scripts; nothing to apply." >&2
fi
python3 oracle.py > run-record.txt 2>/dev/null
echo "=== validations ==="
grep -E "^V[0-9]" run-record.txt
echo "=== adjudication (conv_tp) ==="
grep -A4 "Adjudication" run-record.txt
echo "=== P5/P7 ==="
grep -E "^P[57] " run-record.txt
echo "=== dossier table numbers (from oracle_data.json) ==="
python3 - <<'EOF'
import json
d = json.load(open('oracle_data.json'))
for r in d['sweep']:
    if r['conv'] == 'de98' and r['e'] == 0.6 and r['nu'] == 0.25 and r['pbar'] in (20, 30, 50):
        print(f"de98-conv pbar={r['pbar']}: ek2={r['ek_eob2']*100:+.2f}% "
              f"ek3={r['ek_eob3']*100:+.2f}% ek4={r['ek_eob4']*100:+.2f}% "
              f"ek_djs={r['ek_djs']*100:+.2f}%")
for r in d['sweep']:
    if r['conv'] == 'doll' and r['e'] == 0.6 and r['nu'] == 0.25 and r['pbar'] == 20:
        print(f"doll-conv pbar=20: ek3={r['ek_eob3']*100:+.2f}% eT3={r['eT_eob3']*100:+.2f}%")
EOF
