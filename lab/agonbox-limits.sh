#!/usr/bin/env bash
# Keep agonbox healthy under GLM: an experiment that runs out of memory is killed alone, never the runner or the box.
# (5 October: one GLM experiment reached 15 GB plus 4 GB of swap and the OOM killer stopped the whole runner service.)
# Run on agonbox, once, after the runner service is installed:  sudo bash agonbox-limits.sh
set -euo pipefail
u=$(systemctl list-units --all --plain --no-legend 'actions.runner.*' | awk '{print $1}' | head -1)
[ -n "$u" ] || { echo "no runner service found"; exit 2; }
mkdir -p "/etc/systemd/system/$u.d"
cat > "/etc/systemd/system/$u.d/limits.conf" <<'C'
[Service]
MemoryMax=12G
MemorySwapMax=2G
OOMPolicy=continue
C
pkill -u glmlab -x omp 2>/dev/null || true
systemctl daemon-reload
systemctl restart "$u"
systemctl is-active "$u" && systemctl show "$u" -p MemoryMax -p OOMPolicy
