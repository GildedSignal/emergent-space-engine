#!/usr/bin/env python3
"""Cross-check the Rust key-window port (keydump) against the original run's
store_probe.py formulas (key_cells + widened_u), on identical body inputs."""
import subprocess, sys
import numpy as np

SCALE_BITS = 12
SHAPE_BITS = 12
R = 5e-4  # dense scene rho

BIN = sys.argv[1] if len(sys.argv) > 1 else None
scene = "dense"
out = subprocess.run([BIN, "keydump", scene], capture_output=True, text=True, check=True).stdout.splitlines()
header = out[0]
rows = [list(map(float, l.split())) for l in out[1:]]
a = np.array([r[1] for r in rows]); e = np.array([r[2] for r in rows])
u_lo_rust = np.array([r[3] for r in rows]); u_hi_rust = np.array([r[4] for r in rows])

# store_probe.py key_cells + widened_u (verbatim math)
p = a * (1 - e * e)
g = (1 - e) / (1 + e)
m, ex = np.frexp(p)
mq = np.round(m * (1 << SCALE_BITS))
gq = np.clip(np.round(g * (1 << SHAPE_BITS)), 1, 1 << SHAPE_BITS)
p_q = mq * 2.0 ** (ex - SCALE_BITS)
g_q = gq / (1 << SHAPE_BITS)
k_q = (1 + g_q) / 2
r_peri = p_q * k_q
r_apo = p_q * k_q / g_q
qp = 2.0 ** -SCALE_BITS
gg = r_peri / r_apo
pad = r_apo * (qp + qp / gg) + r_peri * qp
lo_r, hi_r = r_peri - pad - R, r_apo + pad + R
u_lo_py, u_hi_py = 1.0 / hi_r, 1.0 / lo_r

dlo = np.abs(u_lo_rust - u_lo_py) / np.abs(u_lo_py)
dhi = np.abs(u_hi_rust - u_hi_py) / np.abs(u_hi_py)
print(f"header: {header}")
print(f"n_checked: {len(rows)}  max_rel_diff u_lo: {dlo.max():.3e}  u_hi: {dhi.max():.3e}")
ok = dlo.max() < 1e-12 and dhi.max() < 1e-12
print("PORT MATCHES" if ok else "PORT MISMATCH")
