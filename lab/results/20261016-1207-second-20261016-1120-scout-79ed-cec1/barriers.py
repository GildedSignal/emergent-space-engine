#!/usr/bin/env python3
"""The model's capture barriers, bisected (both arms, m=16 and m=32, vs GR).

GR: matter E=1 critical L = 4 exactly; photon critical b = 3*sqrt(3) = 5.1962.
Model: the piecewise band law's own thresholds (turning possible only where the
per-band equilibrium up(c) < c, i.e. 3c^2 - c + invL2 > 0)."""
import math, json, sys
import importlib.util
spec = importlib.util.spec_from_file_location("b", __file__.rsplit('/', 1)[0] + "/binet_r1v2.py")
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)

def matter_absorbed(L, m, arm):
    invL2 = 1.0 / (L * L); u0 = 0.01
    v0 = math.sqrt(max(2.0 * u0 / (L * L) - u0 * u0 + 2 * u0 ** 3, 0.0))
    try:
        cs = b.consts_scatter(u0, v0, m, invL2, 1.0, L, arm, u_esc=1e-6)
        r = b.walk_scatter(u0, v0, m, invL2, 1.0, L, consts=cs, u_esc=1e-6)
        return r['absorbed']
    except b.Plunge:
        return True

def photon_absorbed(bb, m, arm):
    u0 = 1e-4
    v0 = math.sqrt(1.0 / (bb * bb) - u0 * u0 + 2 * u0 ** 3)
    try:
        cs = b.consts_scatter(u0, v0, m, 0.0, 1.0, bb, arm, u_esc=u0)
        r = b.walk_scatter(u0, v0, m, 0.0, 1.0, bb, consts=cs, u_esc=u0)
        return r['absorbed']
    except b.Plunge:
        return True

def bisect(f, lo, hi, tol=1e-3):
    # f(lo) True (absorbed), f(hi) False (escaped)
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if f(mid):
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)

out = {"gr": {"matter_L": 4.0, "photon_b": 3.0 * math.sqrt(3.0)}}
for m in (16, 32):
    for arm in ('centre', 'refit'):
        Lh = bisect(lambda L: matter_absorbed(L, m, arm), 3.5, 4.5)
        bh = bisect(lambda x: photon_absorbed(x, m, arm), 4.0, 9.0)
        out[f"m{m}-{arm}"] = {"matter_L_hat": Lh, "photon_b_hat": bh}
        print(f"m={m} {arm}: matter L_hat = {Lh:.4f} (GR 4.0) | photon b_hat = {bh:.4f} (GR {3*math.sqrt(3):.4f}; sqrt(54)={math.sqrt(54):.4f})", flush=True)
# theory: photon threshold -> sqrt(54) as m -> inf; at finite m the deepest rotation band top
for m in (8, 16, 32):
    c = 2.0 ** (-math.ceil(m * math.log2(6.0)) / m)  # centre just below 1/6
    while 1.0 - 6 * c > 0:
        c *= 2.0 ** (1.0 / m)
    u_hi = c * 2.0 ** (1.0 / (2.0 * m))  # top of the deepest rotation band
    bth = 1.0 / math.sqrt(u_hi * u_hi * (1.0 - 2.0 * u_hi))
    out[f"m{m}-rotation-top-threshold"] = bth
    print(f"m={m}: deepest-rotation-band top u_hi={u_hi:.5f} -> barrier {bth:.4f}")
with open(sys.argv[1] if len(sys.argv) > 1 else 'barriers.json', 'w') as f:
    json.dump(out, f, indent=1)
