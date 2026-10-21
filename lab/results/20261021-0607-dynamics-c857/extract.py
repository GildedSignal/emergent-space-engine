#!/usr/bin/env python3
"""Extracts every dossier number from the run's own artifacts (flights + dumps + analysis)."""
import struct, math, sys
from pathlib import Path

R = Path(sys.argv[1] if len(sys.argv) > 1 else ".")


def load(p):
    data = open(p, "rb").read()
    out, o = {}, 0
    while o + 16 <= len(data):
        g, n, mn = struct.unpack_from("<IIq", data, o)
        o += 16
        gen = []
        for _ in range(n):
            i, off = struct.unpack_from("<Hq", data, o)
            o += 10
            gen.append((i, mn + off))
        out[g] = gen
    return out


for seed in (1, 2):
    rows = {}
    for ln in open(R / f"work/flight_s{seed}.txt"):
        if ln.startswith(("g=", "flight ")):
            parts = ln.split()
            if ln.startswith("flight "):
                print(f"seed {seed}: {ln.strip()}")
                continue
            if parts[0].startswith("g="):
                keys = ["g", "n", "span", "maxmu64", "floor64", "f10_64", "f90_64", "excess64", "c50", "maxmu32", "maxmu128", "maxmu1k", "drift_abs", "drift_sign", "var_due"]
                d = dict(zip(keys, parts))
                rows[int(d["g"][2:])] = d
    full = [g for g, d in rows.items() if int(float(d["n"])) == 2700]
    lo, hi = min(full), max(full)
    mm = [float(rows[g]["maxmu64"]) for g in full]
    ex = [float(rows[g]["excess64"]) for g in full]
    c5 = [float(rows[g]["c50"]) for g in full]
    vd = [(g, float(rows[g]["var_due"])) for g in full if g >= 8]
    beta = math.log(vd[-1][1] / vd[0][1]) / math.log(vd[-1][0] / vd[0][0])
    dr = [float(rows[g]["drift_abs"]) for g in full if rows[g]["drift_abs"] != "-" and float(rows[g]["drift_abs"]) > 1e-9]
    ds = [float(rows[g]["drift_sign"]) for g in full if rows[g]["drift_sign"] != "-" and abs(float(rows[g]["drift_sign"])) > 1e-9]
    print(f"  matched n=2700: g={lo}..{hi}; maxmu64 {mm[0]:.2f}→{mm[-1]:.2f} (min {min(mm):.2f} max {max(mm):.2f}); excess {min(ex):+.2f}..{max(ex):+.2f}; c50 {min(c5):.3f}..{max(c5):.3f}; Var(due)/step^2 g^beta with beta={beta:.3f} (g={vd[0][0]}→{vd[-1][0]}, {vd[0][1]:.2e}→{vd[-1][1]:.2e}); drift_abs(change-fires) {min(dr):.1e}..{max(dr):.1e}, signed {min(ds):.1e}..{max(ds):.1e}")

    gens = load(R / f"work/dues_s{seed}.bin")
    gs = sorted(gens)
    seq = {}
    for g in gs:
        for i, d in gens[g]:
            seq.setdefault(i, {})[g] = d
    med, allsteps = {}, []
    for i, s in seq.items():
        kk = sorted(s)
        iv = sorted(s[kk[a + 1]] - s[kk[a]] for a in range(len(kk) - 1))
        med[i] = iv[len(iv) // 2]
        allsteps += iv
    step_mean = sum(allsteps) / len(allsteps)
    spread = (max(allsteps) - min(allsteps)) / step_mean

    def prof64(vals):
        mn, mx = min(vals), max(vals)
        span = mx - mn
        c = [0] * 64
        for v in vals:
            c[min(int((v - mn) * 64 / span), 63)] += 1
        return c

    g = max(x for x in gs if len(gens[x]) == 2700)
    c1 = prof64([d for _, d in gens[g]])
    c2 = prof64([v - min(med.values()) for v in med.values()])
    n1 = [x / sum(c1) for x in c1]
    n2 = [x / sum(c2) for x in c2]
    m1, m2 = sum(n1) / 64, sum(n2) / 64
    r = sum((a - m1) * (b - m2) for a, b in zip(n1, n2)) / 64 / (math.sqrt(sum((a - m1) ** 2 for a in n1) / 64) * math.sqrt(sum((b - m2) ** 2 for b in n2) / 64))
    print(f"  steps: {len(set(allsteps))} distinct over {len(allsteps)} intervals, spread (max-min)/mean = {spread:.3f}; profile g={g} vs step profile r = {r:.3f}")
print("--- analysis.txt ---")
print((R / "work/analysis.txt").read_text())
