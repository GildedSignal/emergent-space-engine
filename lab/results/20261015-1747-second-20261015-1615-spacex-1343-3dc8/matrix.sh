#!/bin/sh
# The decisive matrix: digest identity + the bill, ctl vs seam vs variant,
# on the standard ladder and the mixed-peri comet stream. One file per arm.
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

# The standard ladder (e0f9's arms): ctl digest must equal e0f9's published one.
for scene in "1000 coast 20000 1 1000" "10000 coast 20000 1 1000" "10000 burn 20000 1 1000"; do
  s=$(echo "$scene" | cut -d' ' -f1-2 | tr ' ' '_')
  arm "ctl_$s"    "$scene" ES_LAZY_ENTRY=0
  arm "seam_$s"   "$scene" ES_LAZY_ENTRY=1
  arm "variant_$s" "$scene" ES_LAZY_ENTRY=1 ES_LAZY_PASSAGES=1
done

# The comet stream at player pace: 1.2 AU, star-grazing, mixed-peri.
for scene in "500 comet 1200 1 100" "500 stargraze 1200 1 100" "1000 mixed 1200 1 100"; do
  s=$(echo "$scene" | cut -d' ' -f1-2 | tr ' ' '_')
  arm "ctl_$s"    "$scene" ES_LAZY_ENTRY=0
  arm "seam_$s"   "$scene" ES_LAZY_ENTRY=1
  arm "variant_$s" "$scene" ES_LAZY_ENTRY=1 ES_LAZY_PASSAGES=1
done

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
    out.append(f"{scene}: {'IDENTITY' if same else 'MISMATCH'} {arms.get('ctl','?')[:16]} ctl/seam/variant: {arms.get('ctl','?')[:12]}/{arms.get('seam','?')[:12]}/{arms.get('variant','?')[:12]}")
print("\n".join(out))
print("VERDICT:", "ALL IDENTITY" if ok else "MISMATCH SOMEWHERE")
EOF
