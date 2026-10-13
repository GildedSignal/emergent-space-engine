#!/bin/sh
# Regenerates every number in dossier.md for run 20261013-2005-second-20261013-1915-system-81ca-6701.
# work/patch.diff (applied by the runner before this runs) adds crates/space/tests/carlson_compile_probe.rs.
set -e
RUN_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$RUN_DIR/../../.."   # repo root (lab/results/<id> -> root)
cargo test --release -p emergent-space --test carlson_compile_probe -- --nocapture 2>&1 | tee "$RUN_DIR/probe-out.txt"
# Independent 50-dps mpmath cross-check of the dumped closed-form channels (advance,
# t_half, tau_half) from the raw (k, q) fields: catches any algebra/port drift that
# the in-probe quadrature arm could share.
python3 -c "import mpmath" 2>/dev/null || pip install mpmath --quiet
python3 - "$RUN_DIR/probe-out.txt" << 'EOF'
import re, sys
import mpmath as mp
mp.mp.dps = 50
PI = mp.pi
text = open(sys.argv[1]).read()
rows = re.findall(r"MPK p=(\S+) e=(\S+) k=(\S+) q=(\S+) ts=(\S+) adv=(\S+) t_half=(\S+) tau_half=(\S+)", text)
assert rows, "no MPK dump lines found"
def channels(k, q):
    # A-frame characteristics (probe header algebra), evaluated by mpmath quadrature
    # of the raw psi-integrands: fully independent of the Rust code paths.
    m = 4*q*(1-k)/(1-q*(8*k-2))
    tn = k*(1-2*q)*(1+2*q*(1-2*k))
    d  = k - q*(3*k*k + (1-k)**2)
    f = lambda psi: 1/mp.sqrt(1 - q*(6*k + 2*(1-k)*mp.cos(psi)))
    x = lambda psi: k + (1-k)*mp.cos(psi)
    adv = 2*(mp.quad(f, [0, PI]) - PI)
    t_half = mp.sqrt(tn)*mp.quad(lambda p: f(p)/(x(p)**2*(1-2*q*x(p))), [0, PI])
    tau_half = mp.sqrt(d)*mp.quad(lambda p: f(p)/x(p)**2, [0, PI])
    return adv, t_half, tau_half
worst = 0.0
for (p, e, ks, qs, ts, adv, th, tauh) in rows:
    k, q = mp.mpf(ks), mp.mpf(qs)
    a, t, tau = channels(k, q)
    for mine, want, name in [(adv, a, "adv"), (th, t, "t"), (tauh, tau, "tau")]:
        rel = abs(mp.mpf(mine) - want)/abs(want)
        worst = max(worst, float(rel))
        assert rel < mp.mpf("1e-12"), f"{name} p={p} e={e}: {mine} vs {want} rel {rel}"
    print(f"MPMATH-CHECK p={p} e={e}: all three channels rel < 1e-12")
print(f"MPMATH-CHECK worst rel over {len(rows)} keys x 3 channels = {worst:.2e} (< 1e-12)")
EOF
echo "Done. Numbers are in probe-out.txt plus the MPMATH-CHECK lines above."
