#!/bin/sh
# The decisive matrix: digest identity + census + the bill, ctl / seam / variant / all.
# Arms: ctl (shipped), seam (ES_LAZY_ENTRY=1: kick-settled cycles), variant (+ES_LAZY_PASSAGES=1),
# all (+ES_LAZY_ALL=1: every keyed entry demotes — births and no-kick settles included).
# Scenes: the standard ladder (e0f9's anchors), the pre-wave cut (birth arcs standing),
# the mixed-peri comet stream (3dc8's anchor), and the dive (peri inside the star).
# Usage: matrix.sh <run-folder-abs-path> <binary-abs-path>
set -e
R="$1"; B="$2"
mkdir -p "$R/flights"; : > "$R/flights.txt"

arm() { # name scene-args env...
  name="$1"; shift
  scene="$1"; shift
  echo "== $name: $scene ==" | tee -a "$R/flights.txt"
  env "$@" timeout 420 "$B" $scene 2>/dev/null | tee "$R/flights/$name.txt" | tee -a "$R/flights.txt" | grep -E "^arm|^digest|^kicks|census |^bodies" || echo "TIMEOUT/FAIL $name" | tee -a "$R/flights.txt"
}

# The standard ladder (e0f9's arms): ctl digests must equal e0f9/3dc8's published ones.
for scene in "1000 coast 20000 1 1000" "10000 coast 20000 1 1000" "10000 burn 20000 1 1000"; do
  s=$(echo "$scene" | cut -d' ' -f1-2 | tr ' ' '_')
  arm "ctl_$s"     "$scene" ES_LAZY_ENTRY=0
  arm "seam_$s"    "$scene" ES_LAZY_ENTRY=1
  arm "all_$s"     "$scene" ES_LAZY_ENTRY=1 ES_LAZY_ALL=1
done

# The pre-wave cut: the belt's birth arcs are still standing in ctl/seam (no kick yet).
arm "ctl_10000_prewave"    "10000 coast 10000 1 1000" ES_LAZY_ENTRY=0
arm "all_10000_prewave"    "10000 coast 10000 1 1000" ES_LAZY_ENTRY=1 ES_LAZY_ALL=1

# The mixed-peri comet stream (3dc8's scene): ctl and variant anchor to 3dc8's digests.
arm "ctl_1000_mixed"    "1000 mixed 1200 1 100" ES_LAZY_ENTRY=0
arm "variant_1000_mixed" "1000 mixed 1200 1 100" ES_LAZY_ENTRY=1 ES_LAZY_PASSAGES=1
arm "all_1000_mixed"    "1000 mixed 1200 1 100" ES_LAZY_ENTRY=1 ES_LAZY_ALL=1

# The dive: peri 0.001 AU, inside the star. Bound as passages; dead at the surface.
arm "ctl_200_dive"   "200 dive 1200 1 100" ES_LAZY_ENTRY=0
arm "all_200_dive"   "200 dive 1200 1 100" ES_LAZY_ENTRY=1 ES_LAZY_ALL=1
arm "ctl_200_dive_deep" "200 dive 6000 1 300" ES_LAZY_ENTRY=0
arm "all_200_dive_deep" "200 dive 6000 1 300" ES_LAZY_ENTRY=1 ES_LAZY_ALL=1

# The identity verdict, machine-readable.
python3 - "$R" <<'EOF'
import sys, re, glob, os
R = sys.argv[1]
rows = {}
for f in sorted(glob.glob(os.path.join(R, "flights", "*.txt"))):
    name = os.path.basename(f)[:-4]
    txt = open(f).read()
    d = re.search(r"^digest ([0-9a-f]{64})$", txt, re.M)
    rows[name] = d.group(1) if d else "NONE"
scenes = {}
for name, dg in rows.items():
    scene = name.split("_", 1)[1]
    scenes.setdefault(scene, {})[name.split("_", 1)[0]] = dg
ok = True
out = []
for scene, arms in sorted(scenes.items()):
    same = len(set(arms.values())) == 1 and "NONE" not in arms.values()
    ok &= same
    out.append(f"{scene}: {'IDENTITY' if same else 'MISMATCH'} " + " ".join(f"{a}:{d[:12]}" for a, d in sorted(arms.items())))
print("\n".join(out))
print("VERDICT:", "ALL IDENTITY" if ok else "MISMATCH SOMEWHERE")
EOF
