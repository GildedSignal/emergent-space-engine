#!/usr/bin/env python3
"""Analysis for the second-author run: prints every number the dossier quotes,
from control.json / mapcheck.json / flyby.json / flyby2.json / conv.json
(regenerable).  The second-order channel reads err = k*u (u = xi0/rp); k is
reported as the median of err/u over u in [1e-3, 3e-2] with its spread."""
import json
import numpy as np

ANG = {0.0: "rad", np.pi / 8: "pi/8", np.pi / 4: "pi/4", 3 * np.pi / 8: "3pi/8",
       np.pi / 2: "along", "z": "z"}
CH_ORDER = ["rad", "pi/8", "pi/4", "3pi/8", "along", "z"]
US = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2]


def angname(a):
    return ANG[a] if a in ANG else (a if a == "z" else "%.3f" % a)


def exit_map(runres):
    return {(angname(r[0]), r[1]): r[2] for r in runres["exit"]}


def kread(runres, ch, us=US):
    ex = exit_map(runres)
    q = [(u, ex[(ch, u)]) for u in us if (ch, u) in ex]
    ks = [v / u for u, v in q]
    return float(np.median(ks)), (max(ks) - min(ks)) / float(np.median(ks))


def main():
    ctrl = json.load(open("control.json"))
    mc = json.load(open("mapcheck.json"))
    fly = json.load(open("flyby.json"))["flyby"]
    fly2 = json.load(open("flyby2.json"))["flyby2"]
    conv = json.load(open("conv.json"))["conv"]

    print("=" * 72)
    print("CONTROLS")
    print("=" * 72)
    print("rhs_check (vectorized vs loop member RHS): %.1e" % ctrl["rhs_check"])
    for r in ctrl["eigen_control"]:
        print("eig rp%-4g b%-5g dev=%.1e udrift=%.1e orth=%.1e"
              % (r["rp"], r["beta"], r["eig_dev"], r["u_drift"], r["orthonorm"]))
    for s in ctrl["sign_control"]:
        xs_ = sorted(s["udrift0_max_by_xi"], key=float)
        print("sign rp%-4g b%-5g udrift0<= %.1e | vrel0_fd %s | rtrip0 %s"
              % (s["rp"], s["beta"], max(s["udrift0_max_by_xi"].values()),
                 " ".join("%.1e" % s["vrel0_fd_max_by_xi"][x] for x in xs_),
                 " ".join("%.1e" % s["roundtrip0_max_by_xi"][x] for x in xs_)))
    print("\nmap check (residual vs exact exponential map, old vs dual):")
    for r in mc["map_check"]:
        print("  rp%-4g b%-4g %-5s xi=%-6g old=%.2e dual=%.2e  ratio=%.0fx"
              % (r["rp"], r["beta"], angname(r["alpha"]), r["xi"],
                 r["resid_old"], r["resid_dual"], r["resid_old"] / r["resid_dual"]))

    print("\n" + "=" * 72)
    print("EXIT TABLES, truncated IC (err := |xi_true - xi_ODE|/xi0)")
    print("=" * 72)
    for runres in fly:
        ex = exit_map(runres)
        print("\nrp=%g beta=%g  (drift %.1e, orth %.1e, member drift %.1e)"
              % (runres["rp"], runres["beta"], runres["u_drift"],
                 runres["orthonorm"], runres["member_u_drift_exit"]))
        print("%-6s" % "chan" + "".join("%11s" % x for x in ("1e-4", "3e-4", "1e-3", "3e-3", "1e-2", "3e-2"))
              + "   k=err/u    spread")
        for ch in CH_ORDER:
            vals = [ex.get((ch, u), np.nan) for u in US]
            k, sp = kread(runres, ch)
            print("%-6s" % ch + "".join("%11.3e" % v for v in vals)
                  + "   %9.4g  %5.1f%%" % (k, 100 * sp))

    print("\n" + "=" * 72)
    print("K TABLE (median err/u over u in [1e-3,3e-2]) and ratios")
    print("=" * 72)
    by = {(r["rp"], r["beta"]): r for r in fly}
    by2 = {(r["rp"], r["beta"]): r for r in fly2}
    print("%-6s" % "chan" + "".join("rp%gb%-4g      " % (rp, b) for rp in (18, 100) for b in (0.5, 0.9, 0.95)))
    for ch in CH_ORDER:
        row = "%-6s" % ch
        for rp in (18, 100):
            for b in (0.5, 0.9, 0.95):
                k, _ = kread(by[(rp, b)], ch)
                row += "%-13.4g" % k
        print(row)
    print("\nk_exact/k_trunc per channel (IC-convention split):")
    for ch in CH_ORDER:
        row = "%-6s" % ch
        for rp in (18, 100):
            for b in (0.5, 0.9, 0.95):
                kt, _ = kread(by[(rp, b)], ch)
                ke, _ = kread(by2[(rp, b)], ch)
                row += " %6.2f" % (ke / kt)
        print(row, "  (rp18 b.5/.9/.95, rp100 b.5/.9/.95)")
    print("\nk with EXACT ICs (physical channel):")
    for ch in CH_ORDER:
        row = "%-6s" % ch
        for rp in (18, 100):
            for b in (0.5, 0.9, 0.95):
                ke, spe = kread(by2[(rp, b)], ch)
                row += " %6.2g(%2.0f%%)" % (ke, 100 * spe)
        print(row)
    print("\nrp100/rp18 k ratio (exact ICs):")
    for ch in CH_ORDER:
        rs = [kread(by2[(100, b)], ch)[0] / kread(by2[(18, b)], ch)[0] for b in (0.5, 0.9, 0.95)]
        print("  %-6s %s" % (ch, " ".join("%.3f" % v for v in rs)))
    print("beta ratios (0.9/0.5, 0.95/0.9), exact ICs, rp18 | rp100:")
    for ch in CH_ORDER:
        r18 = (kread(by2[(18, 0.9)], ch)[0] / kread(by2[(18, 0.5)], ch)[0],
               kread(by2[(18, 0.95)], ch)[0] / kread(by2[(18, 0.9)], ch)[0])
        r100 = (kread(by2[(100, 0.9)], ch)[0] / kread(by2[(100, 0.5)], ch)[0],
                kread(by2[(100, 0.95)], ch)[0] / kread(by2[(100, 0.9)], ch)[0])
        print("  %-6s %5.2f %5.2f | %5.2f %5.2f" % (ch, r18[0], r18[1], r100[0], r100[1]))
    print("\nexact-IC vrel0_fd (should be xi^2: compare across xi) for rp18:")
    for b in (0.5, 0.9, 0.95):
        r2 = by2[(18, b)]
        d = r2["tau0"]
        for xi in (1e-4, 1e-3, 1e-2, 3e-2):
            vs = [v for v, m in zip(r2["vrel0_fd"], d) if m["xi"] == xi]
            if vs:
                print("  b%-4g xi=%-6g vrel0_fd max %.2e" % (b, xi, max(vs)))

    print("\n" + "=" * 72)
    print("TAU-GROWTH (fraction of exit err; truncated ICs, rp18)")
    print("=" * 72)
    for runres in fly:
        if runres["rp"] != 18:
            continue
        print("\nrp=18 beta=%g   r/rp: %s" % (runres["beta"],
              " ".join("%s:%.2f" % (k, v) for k, v in sorted(runres["r_over_rp"].items(),
                                                             key=lambda kv: float(kv[0])))))
        frs = sorted(runres["snaps"], key=float)
        print("%-6s" % "chan" + "".join("%9s" % f for f in frs))
        for ch in CH_ORDER:
            exrow = {angname(r[0]): (r[1], r[2]) for r in runres["snaps"][frs[-1]]}
            xi0 = exrow[ch][1]
            line = "%-6s" % ch
            for f in frs:
                row = {angname(r[0]): (r[1], r[2]) for r in runres["snaps"][f]}
                line += "%9.3f" % (row[ch][1] / xi0)
            print(line)

    print("\n" + "=" * 72)
    print("CONVERGENCE + REPRO")
    print("=" * 72)
    ref = json.load(open("ref-451f-flyby.json"))["flyby"][1]["checkpoints"]
    ref = {"z|0.0001": ref["z|0.0001"]["3999"], "z|0.03": ref["z|0.03"]["3999"]}
    for c in conv:
        if c["cfg"] == "repro451f":
            for xi in (1e-4, 3e-2):
                mine = [r[2] for r in c["exit"] if r[0] == "z" and r[1] == xi][0]
                key = "z|0.0001" if xi == 1e-4 else "z|0.03"
                print("repro451f %-9s mine=%.4e 451f=%.4e  rel=%.2e"
                      % (key, mine, ref[key], abs(mine - ref[key]) / ref[key]))
        else:
            row = "nsteps %6d: " % c["nsteps"]
            for ch in ("rad", "z"):
                for xi in (1e-4, 3e-2):
                    e = [r[2] for r in c["exit"] if angname(r[0]) == ch and r[1] == xi][0]
                    row += "%s@%g=%.3e  " % (ch, xi, e)
            print(row, " drift=%.1e" % c["u_drift"])


if __name__ == "__main__":
    main()
