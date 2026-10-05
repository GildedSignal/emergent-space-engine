#!/usr/bin/env bash
# One-time setup of the GLM lab's own cloud machine (Oracle Cloud Always Free, Ubuntu 24.04 on Ampere aarch64),
# which runs the lab's GLM job as a GitHub self-hosted runner (labels: self-hosted, glm). Never on Julien's Mac.
# Julien runs this once on the machine, then registers the runner from GitHub's page himself (the token is his).
# Publishing stays on GitHub's own machines, so this machine never holds a credential that can write to the repo.
set -euo pipefail
sudo apt-get update -y
sudo apt-get install -y build-essential pkg-config git curl jq python3 python3-pip python3-venv \
  python3-numpy python3-scipy python3-sympy python3-mpmath python3-matplotlib
python3 -m pip config set global.break-system-packages true   # GLM installs what it needs; a throwaway machine
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal
grep -q cargo/env ~/.bashrc || echo 'source "$HOME/.cargo/env"' >> ~/.bashrc
echo "Ready. Now register the runner: GitHub, the repo, Settings, Actions, Runners, New self-hosted runner, Linux, ARM64."
echo "Run its commands, adding to ./config.sh:  --labels glm --name glm-oracle --unattended"
echo "Then, instead of ./run.sh:  sudo ./svc.sh install && sudo ./svc.sh start"
