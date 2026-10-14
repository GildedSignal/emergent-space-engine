#!/bin/sh
# Regenenerates every dossier number from shipped code + work/patch.diff (already applied).
# Total: one release build (~1 min) + one bench run (~15 s).
set -e
cd "$(git rev-parse --show-toplevel)"
cargo run --release -p emergent-shipmem --example promo_floor > "$(dirname "$0")/run.log" 2>/dev/null
grep -E "SCAR|WIDEGRADE|REL|BYTES|IDENT|COLIDENT|SCALE|STAT|PERIOD|STATE|N=" "$(dirname "$0")/run.log"
