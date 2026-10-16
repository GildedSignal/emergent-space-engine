#!/usr/bin/env bash
# One-time setup of agonbox (Julien's headless Linux machine; he authorized it for the GLM lab on 5 October) as the lab's
# self-hosted runner. GLM runs as the user glmlab: no sudo, no access to Julien's files (his home is 750), no GPU, and
# no route to the home network or the tailnet; it reaches the internet only. Publishing stays on GitHub's machines,
# so this machine never holds a credential that can write to the repo.
# Run on agonbox, once:  sudo bash agonbox-setup.sh
set -euo pipefail
U=glmlab
id "$U" >/dev/null 2>&1 || adduser --disabled-password --gecos "GLM lab runner" "$U"
chmod 750 /home/julien
apt-get -o DPkg::Lock::Timeout=1200 update -y   # waits while unattended-upgrades holds the lock
apt-get -o DPkg::Lock::Timeout=1200 install -y build-essential pkg-config git curl jq python3-pip python3-venv \
  python3-numpy python3-scipy python3-sympy python3-mpmath python3-matplotlib

# The firewall: glmlab may not reach private, link-local, CGNAT (tailnet) or the home IPv6 prefix.
cat > /usr/local/sbin/glmlab-firewall <<'F'
#!/bin/sh
set -e
for c in iptables ip6tables; do
  $c -D OUTPUT -m owner --uid-owner glmlab -j GLMLAB 2>/dev/null || true
  $c -F GLMLAB 2>/dev/null || true; $c -X GLMLAB 2>/dev/null || true; $c -N GLMLAB
done
for n in 10.0.0.0/8 172.16.0.0/12 192.168.0.0/16 100.64.0.0/10 169.254.0.0/16; do iptables -A GLMLAB -d "$n" -j REJECT; done
for n in fc00::/7 fe80::/10 $(ip -o -6 addr show scope global | awk '$2 !~ /tailscale/ {print $4}'); do ip6tables -A GLMLAB -d "$n" -j REJECT; done
iptables -I OUTPUT 1 -m owner --uid-owner glmlab -j GLMLAB
ip6tables -I OUTPUT 1 -m owner --uid-owner glmlab -j GLMLAB
F
chmod 755 /usr/local/sbin/glmlab-firewall
cat > /etc/systemd/system/glmlab-firewall.service <<'S'
[Unit]
Description=GLM lab: the glmlab user reaches the internet only (not the home network, not the tailnet)
After=network-online.target ufw.service tailscaled.service
Wants=network-online.target
[Service]
Type=oneshot
ExecStart=/usr/local/sbin/glmlab-firewall
RemainAfterExit=yes
[Install]
WantedBy=multi-user.target
S
systemctl daemon-reload && systemctl enable --now glmlab-firewall.service

# Rust and GitHub's runner, for glmlab only (a file, because sudo -i flattens a multi-line command).
cat > /tmp/glmlab-user-setup.sh <<'G'
set -e
cd "$HOME"
command -v cargo >/dev/null || [ -x "$HOME/.cargo/bin/cargo" ] || curl --proto "=https" --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal
python3 -m pip config set global.break-system-packages true
mkdir -p "$HOME/actions-runner" && cd "$HOME/actions-runner"
if [ ! -x ./config.sh ]; then
  v=$(curl -s https://api.github.com/repos/actions/runner/releases/latest | jq -r .tag_name | tr -d v)
  curl -sSL -o r.tgz "https://github.com/actions/runner/releases/download/v$v/actions-runner-linux-x64-$v.tar.gz"
  tar xzf r.tgz && rm r.tgz
fi
echo "glmlab: rust $("$HOME/.cargo/bin/rustc" --version | cut -d' ' -f2), runner $(./config.sh --version 2>/dev/null || echo installed)"
G
chmod 644 /tmp/glmlab-user-setup.sh
sudo -u "$U" -H bash /tmp/glmlab-user-setup.sh
rm -f /tmp/glmlab-user-setup.sh

# The isolation check, as glmlab: the router must be unreachable, GitHub reachable.
if sudo -u "$U" curl -s --max-time 4 -o /dev/null http://192.168.1.1; then echo "FAIL: glmlab reaches the home network"; exit 2; fi
sudo -u "$U" curl -s --max-time 8 -o /dev/null https://api.github.com && echo "OK: glmlab reaches GitHub, not the home network"
echo
echo "Last step (the token is yours): GitHub, the repo, Settings, Actions, Runners, New self-hosted runner, Linux, x64."
echo "Copy only the token from its ./config.sh line, then run here:"
echo "  sudo -iu glmlab bash -c 'cd ~/actions-runner && ./config.sh --url https://github.com/GildedSignal/emergent-space-engine --labels glm --name agonbox --unattended --token PASTE_TOKEN'"
echo "  sudo bash -c 'cd /home/glmlab/actions-runner && ./svc.sh install glmlab && ./svc.sh start'"
