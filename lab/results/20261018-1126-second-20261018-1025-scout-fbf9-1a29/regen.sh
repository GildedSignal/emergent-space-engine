#!/bin/sh
# Regenerates every number in dossier.md: builds the flight crate against the
# SHIPPED crates/encounters (no repo edits) and runs it (~70 s single-threaded,
# < 100 MB). Deterministic fields are byte-identical across runs; only
# us_per_eval / wall_s (timings) vary.
set -e
cd "$(dirname "$0")"
cargo build --release --manifest-path flight/Cargo.toml --quiet
BIN="${CARGO_TARGET_DIR:-flight/target}/release/flight"
[ -x "$BIN" ] || BIN="$(cargo metadata --manifest-path flight/Cargo.toml --format-version 1 | python3 -c 'import json,sys; print(json.load(sys.stdin)["target_directory"])')/release/flight"
"$BIN" | tee regen.out
echo "regen: deterministic fields diff vs stored flight.out (expect only timing):"
python3 - <<'EOF'
import json

def load(p):
    out = []
    for ln in open(p):
        ln = ln.strip()
        if ln.startswith("{"):
            d = json.loads(ln)
            for k in ("us_per_eval", "wall_s"):
                d.pop(k, None)
            out.append(json.dumps(d, sort_keys=True))
    return out

a, b = load("flight.out"), load("regen.out")
print("IDENTICAL" if a == b else "DIFFERS: %d vs %d lines" % (len(a), len(b)))
EOF
