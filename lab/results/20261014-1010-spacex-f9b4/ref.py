#!/usr/bin/env python3
"""Independent mpmath reference for the three increments, and the certificate check.

Channels (from the shipped walk's own arithmetic, orbit.rs node()/fast_quad, and the
Darwin (p, e) parametrization of envelope.rs's reference):
  advance = 2 * Int_0^pi (g - 1) dpsi
  period  = 2 * (p k)^{3/2} * sqrt(k(1-2q)(1+2q(1-2k))) * l / (k^2 p^2 en) * Int_0^pi (en/l) g/(u^2 (1-2u)) dpsi
  proper  = 2 * (p k)^{3/2} * sqrt(k - q(3k^2 + eta^2)) * l / (k^2 p^2) * Int_0^pi g/(l u^2) dpsi
with k = 1/(1+e), q = 1/(p k), u = (1 + e cos psi)/p, g = 1/sqrt(1 - q(6k + 2(1-k) cos psi)),
l = p/sqrt(p-3-e^2), en = sqrt(((p-2)^2 - 4 e^2)/(p (p-3-e^2))).
The ladder arm's error vs this reference is the control: it must reproduce the record's
~1e-9 band at p >= 20 (5a3b's oracle validation), which validates the scaling formulas.
"""
import csv
import sys

import mpmath as mp

mp.mp.dps = 50
BAR = mp.mpf(2) ** -30  # the compile's verified certificate


def reference(p, e):
    p, e = mp.mpf(p), mp.mpf(e)
    k = 1 / (1 + e)
    q = 1 / (p * k)
    eta = 1 - k
    l = p / mp.sqrt(p - 3 - e * e)
    en = mp.sqrt(((p - 2) ** 2 - 4 * e * e) / (p * (p - 3 - e * e)))
    tn = mp.sqrt(k * (1 - 2 * q) * (1 + 2 * q * (1 - 2 * k)))
    taun = mp.sqrt(k - q * (3 * k * k + eta * eta))

    def g(s):
        return 1 / mp.sqrt(1 - q * (6 * k + 2 * (1 - k) * mp.cos(s)))

    def u(s):
        return (1 + e * mp.cos(s)) / p

    r0 = mp.quad(lambda s: g(s) - 1, [0, mp.pi])
    r1 = mp.quad(lambda s: (en / l) * g(s) / (u(s) ** 2 * (1 - 2 * u(s))), [0, mp.pi])
    r2 = mp.quad(lambda s: g(s) / (l * u(s) ** 2), [0, mp.pi])
    ts = (p * k) ** mp.mpf("1.5")
    return [
        2 * r0,
        2 * ts * tn * l / (k * k * p * p * en) * r1,
        2 * ts * taun * l / (k * k * p * p) * r2,
    ]


def main(paths):
    rows = []
    for path in paths:
        with open(path) as fh:
            for line in fh:
                parts = line.strip().split(",")
                if parts[0] != "ROW":
                    continue
                rows.append(parts)
    by_key = {}
    for parts in rows:
        p, e, arm = parts[1], parts[2], parts[3] or "ladder"
        if parts[4] == "ERR":
            continue
        by_key.setdefault((p, e), {})[arm] = {
            "panels": int(parts[4]),
            "cross": int(parts[5]),
            "inc": [float(x) for x in parts[6:9]],
            "ns": int(parts[9]),
        }
    out = csv.writer(sys.stdout)
    out.writerow(["p", "e", "arm", "panels", "err_adv", "err_t", "err_tau",
                  "max_err", "cert(2^-30)", "vs_ladder", "ns"])
    worst = {}
    for (p, e), arms in sorted(by_key.items(), key=lambda kv: (float(kv[0][0]), float(kv[0][1]))):
        ref = reference(p, e)
        ladder = arms.get("ladder")
        for arm, d in sorted(arms.items()):
            errs = [abs(mp.mpf(v) - r) / abs(r) for v, r in zip(d["inc"], ref)]
            mx = max(errs)
            cert = "PASS" if mx <= BAR else "FAIL"
            if ladder and arm != "ladder":
                rel = "thin<=lad" if mx <= max(abs(mp.mpf(v) - r) / abs(r) for v, r in zip(ladder["inc"], ref)) * 2 else "thin>2xlad"
            else:
                rel = "-"
            out.writerow([p, e, arm, d["panels"],
                          mp.nstr(errs[0], 3), mp.nstr(errs[1], 3), mp.nstr(errs[2], 3),
                          mp.nstr(mx, 3), cert, rel, d["ns"]])
            worst.setdefault(arm, []).append((mx, p, e))
    print("\n# summary per arm (max_err over keys):")
    for arm, ws in worst.items():
        m, p, e = max(ws)
        n_pass = sum(1 for x, *_ in ws if x <= BAR)
        print(f"# {arm}: keys={len(ws)} pass={n_pass} worst={mp.nstr(m, 3)} at p={p} e={e}")


if __name__ == "__main__":
    main(sys.argv[1:])
