# regen.sh — regenerates every number in the dossier from falsifier.py
# (no tree edits needed; the instrument is standalone float Python).
# Runtime: ~2.5 min on the lab box (8 vCPU; single-threaded Python).
set -e
cd "$(dirname "$0")"
python3 falsifier.py --heldout | tee run-output.txt
echo "--- summary ---"
python3 - <<'EOF'
import re
txt = open('run-output.txt').read()
cf = [float(x) for x in re.findall(r"\|CF-QD\|=\s*([0-9.e+-]+)", txt)]
rk = [float(x) for x in re.findall(r"\|RK-QD\|=\s*([0-9.e+-]+)", txt)
      if "e+30" not in x and float(x) < 1.0]
print(f"rows: {len(re.findall(r'^\[', txt, re.M))};  CF-vs-QD comparisons: {len(cf)},"
      f" worst {max(cf):.2e};  RK-vs-QD (excl. degenerate equatorial/a=0 polar skips):"
      f" {len(rk)}, worst {max(rk):.2e}")
EOF
