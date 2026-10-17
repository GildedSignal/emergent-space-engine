#!/bin/sh
# Regenerates every dossier number: probes on shipped code (patch applied by the runner),
# then the ledger composition. ~1 minute.
set -e
cd "$(dirname "$0")/../../.."
cargo build --release -p emergent-universe --example nladder --example belt_first
RUN=lab/results/20261017-0552-fermi-4e2d
{
  cargo run --release -p emergent-universe --example belt_first -- 10000
  cargo run --release -p emergent-universe --example nladder -- 10000 coast 46 900
} > $RUN/probe.txt
python3 $RUN/ledger.py > $RUN/ledger-out.txt
cat $RUN/ledger-out.txt
