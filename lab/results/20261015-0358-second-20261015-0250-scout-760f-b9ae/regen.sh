#!/bin/sh
# Regenerates every number in dossier.md. Eight flights + certificate ≈ 3 minutes, Linux.
#
# INSTRUMENT PROVENANCE (disclosed in dossier.md §Regenerability): the runner's patch
# capture returned work/patch.diff as 0 bytes, so the seam + examples/lazy.rs source is
# not in this record. The author's final instrument build survived at
# /home/glmlab/lab-target-0/release/examples/lazy (sha256 below; its control arms
# reproduce the scout's bit-identical digests, which anchors its flight to shipped
# dynamics). We build from source if a future tree provides it, else use that binary.
set -e
cd "$(dirname "$0")/../../.." || exit 1  # the repo root
OUT=lab/results/20261015-0358-second-20261015-0250-scout-760f-b9ae/out
mkdir -p "$OUT"

BIN=target/release/examples/lazy
cargo build --release -p emergent-universe --example lazy 2>/dev/null || true
[ -x "$BIN" ] || BIN=/home/glmlab/lab-target-0/release/examples/lazy
if [ ! -x "$BIN" ]; then
  echo "FATAL: no lazy instrument (source absent from this record and prebuilt binary gone)" >&2
  exit 1
fi
echo "instrument: $BIN  sha256 $(sha256sum "$BIN" | cut -d' ' -f1)"

# every arm is control (lazy 0) then lazy (1): N flight wall rtf lazy seed
for arm in "10000 coast 8 6000 0 1" "10000 coast 8 6000 1 1" \
           "10000 burn 8 6000 0 1" "10000 burn 8 6000 1 1" \
           "100000 coast 8 6000 0 1" "100000 coast 8 6000 1 1" \
           "10000 coast 8 6000 0 7" "10000 coast 8 6000 1 7"; do
  "$BIN" $arm
done > "$OUT/runs.txt" 2>&1

# the certificate: control digest == lazy digest per arm, and the three scout baselines hold
python3 - "$OUT/runs.txt" <<'PY'
import sys
rows = {}
for line in open(sys.argv[1]):
    if line.startswith("lazy: n="):
        d = {t.split("=", 1)[0]: t.split("=", 1)[1] for t in line.split() if "=" in t}
        rows.setdefault((d["n"], d["flight"], d["seed"]), {})[d["lazy"]] = d
ok = True
for key, arms in sorted(rows.items()):
    same = "0" in arms and "1" in arms and arms["0"]["digest"] == arms["1"]["digest"]
    ok &= same
    print(f"arm N={key[0]} {key[1]} seed={key[2]}: control digest == lazy digest -> {same} ({arms['1']['digest'][:16]}...)")
baselines = {
    ("100000", "coast", "1"): "2109a2e0d2918c0b0b4f4f9eba0b242dba5de6e2d6f7af48f98b81e2d722c1e7",
    ("10000", "coast", "1"): "f8b528554776ddceb9b9273bbef24da913bb6ff19183ad127467c4fd01ca8795",
    ("10000", "burn", "1"): "44d6a9b529b7bb9f8e93343d4b1b941e961f7d389667823b0377c1718219f9d0",
}
for key, dg in baselines.items():
    got = rows.get(key, {}).get("0", {}).get("digest")
    ok &= got == dg
    print(f"scout baseline {key}: seam-off reproduces it -> {got == dg}")
print("CERTIFICATE:", "PASS" if ok else "FAIL")
PY
cat "$OUT/runs.txt"
