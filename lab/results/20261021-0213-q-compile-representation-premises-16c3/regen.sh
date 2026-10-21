#!/usr/bin/env bash
# Regenerates every number in dossier.md. Runtime: ~2 s. No network, no build.
# Runs from anywhere; resolves the repo root relative to this script.
set -euo pipefail
RUN="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$RUN/../../.." && pwd)"
cd "$ROOT"

echo "== 1. budgets / runs / grades / number survival (check_compile.py) =="
python3 "$RUN/check_compile.py"

echo
echo "== 2. run-id union across the page's whole git history (no run lost mid-history) =="
for c in $(git log --format='%h' -- lab/wiki/representation-premises.md); do
  git show "$c":lab/wiki/representation-premises.md 2>/dev/null
done | grep -oP '(?<=^- )\d{8}-\d{4}-[a-z0-9-]+' | sort -u > /tmp/regen-allruns.txt
grep -oP '(?<=^- )\d{8}-\d{4}-[a-z0-9-]+' "$RUN/wiki/representation-premises.md" | sort -u > /tmp/regen-newruns.txt
echo "distinct-ever $(wc -l < /tmp/regen-allruns.txt) vs new page $(wc -l < /tmp/regen-newruns.txt) (must be equal)"
diff /tmp/regen-allruns.txt /tmp/regen-newruns.txt && echo "union: identical"

echo
echo "== 3. the real index tool on a scratch copy (no tree mutation) =="
rm -rf /tmp/regen-wiki && mkdir -p /tmp/regen-wiki/lab
cp -r lab/wiki /tmp/regen-wiki/lab/
cp lab/wiki.py /tmp/regen-wiki/
cp "$RUN/wiki/representation-premises.md" /tmp/regen-wiki/lab/wiki/
( cd /tmp/regen-wiki && python3 wiki.py index )
grep 'representation-premises' /tmp/regen-wiki/lab/wiki/index.md | cut -c1-140

echo
echo "== 4. grades straight from the run branches (7 gold / 10 silver) =="
g=0; o=0
while read -r r; do
  gr=$(git log -1 --format=%s "origin/claude/lab-$r" | grep -oP 'Grade: \K\w+' || echo unknown)
  if [ "$gr" = gold ]; then g=$((g+1)); else o=$((o+1)); fi
done < /tmp/regen-newruns.txt
echo "gold $g / other $o (branch subjects; matches the page's run lines)"
[ "$g" -eq 7 ] && [ "$o" -eq 10 ]

echo
echo "== 5. negative control: the no-loss check fails when it should =="
sed -e 's|L59/L116 strike|L59 strike|' -e 's|"~1800× floor"|"~1,800× floor"|g' \
  "$RUN/wiki/representation-premises.md" > /tmp/regen-broken.md
python3 - "$ROOT" <<'EOF'
import re, sys, unicodedata
def norm(s):
    return unicodedata.normalize("NFKC", s.replace("\u2212", "-").replace("\u207a", "+"))
def tokens(text):
    out = set()
    for m in re.finditer(r"\d+(?:\.\d+)?(?:e-?\d+)?", norm(text), re.I):
        s = m.group(0).lower()
        s = re.sub(r"^(\d+)", lambda g: g.group(1).lstrip("0") or "0", s)
        out.add(s)
    return out
old = open(sys.argv[1] + "/lab/wiki/representation-premises.md", encoding="utf-8").read()
broken = open("/tmp/regen-broken.md", encoding="utf-8").read()
missing = sorted(tokens(old) - tokens(broken))
print("broken-copy missing tokens:", missing)
assert missing == ["116", "1800"], "negative control broken"
print("negative control: FAIL reproduced as designed")
EOF
echo "REGEN: all dossier numbers reproduced"
