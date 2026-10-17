#!/usr/bin/env python3
"""stagger_legality analysis (lab run 20261017-1829-taleb-75d6).

Reads the probe CSVs (off/on/ref x seeds), checks the controls C1/C2 and the
pre-registered kill criteria K1-K4 of predictions.md, and prints the numbers the
dossier quotes. Pure statistics on exact-integer key parts (k48, angle32) and the
17-digit periapsis; no engine state is touched.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(arm: str, seed: int):
    rows = {}
    planets = None
    for line in (HERE / f"{arm}_s{seed}.csv").read_text().splitlines():
        if line.startswith("# planet"):
            planets = line
        if line.startswith("#") or line.startswith("arm,"):
            continue
        f = line.split(",")
        if len(f) != 16:
            continue
        r = dict(
            body=int(f[2]), h=int(f[3]), tick=int(f[4]), alive=int(f[5]), refus=int(f[6]),
            events=int(f[7]), first=int(f[9]), period=float(f[10]), peri=float(f[11]),
            k48=int(f[12]), kexp=int(f[13]), ang=int(f[14]),
        )
        assert r["kexp"] == 0, f"k_exponent {r['kexp']} (not a periodic key)"
        rows[(r["body"], r["h"])] = r
    return rows, planets


def elem(r):
    e = (1 << 48) / r["k48"] - 1.0  # 1/(1+e) = k48 * 2^-48
    a = r["peri"] / (1.0 - e)
    om = r["ang"] / 2**32 * 2 * math.pi
    return a, e, om


def dangle(x, y):
    d = (x - y) % (2 * math.pi)
    return d - 2 * math.pi if d > math.pi else d


def med(v):
    s = sorted(v)
    return s[len(s) // 2] if s else float("nan")


def pct(v, p):
    s = sorted(v)
    return s[min(len(s) - 1, int(p * (len(s) - 1)))]


def mean_std(v):
    n = len(v)
    m = sum(v) / n
    var = sum((x - m) ** 2 for x in v) / (n - 1) if n > 1 else 0.0
    return m, math.sqrt(var)


def main():
    out = {}
    arms = {a: {} for a in ("off", "on", "ref")}
    for a in ("off", "on", "ref"):
        for s in (1, 2):
            try:
                arms[a][s], pl = load(a, s)
                if pl:
                    out[f"planets_{a}_s{s}"] = pl
            except FileNotFoundError:
                arms[a][s] = None

    # ---- controls -------------------------------------------------------------
    bodies = sorted(b for (b, h) in arms["off"][1] if h == 0)
    for s in (1, 2):
        if not arms["on"][s]:
            continue
        bad = [
            b for b in bodies
            if (arms["off"][s][(b, 0)]["k48"], arms["off"][s][(b, 0)]["ang"], arms["off"][s][(b, 0)]["peri"])
            != (arms["on"][s][(b, 0)]["k48"], arms["on"][s][(b, 0)]["ang"], arms["on"][s][(b, 0)]["peri"])
        ]
        out[f"C1_birth_keys_identical_s{s}"] = {"mismatches": len(bad), "n": len(bodies)}
    out["C2_planets_off_vs_on_s1"] = out.get("planets_off_s1") == out.get("planets_on_s1")
    alive = all(
        arms[a][s][(b, h)]["alive"] == 1 and arms[a][s][(b, h)]["refus"] == 0
        for a in ("off", "on") for s in (1, 2) if arms[a][s]
        for (b, h) in arms[a][s]
    )
    out["P5_alive_no_refusals"] = alive

    # ---- errors vs ref (seed 1) ----------------------------------------------
    for s in (1, 2):
        if not arms["ref"][s]:
            continue
        hs = sorted({h for (_, h) in arms["ref"][s]} - {0})
        for h in hs:
            ea = {}
            for a in ("off", "on"):
                rows = []
                for b in bodies:
                    if (b, h) not in arms[a][s] or (b, h) not in arms["ref"][s]:
                        continue
                    ao, eo, oo = elem(arms[a][s][(b, h)])
                    ar, er, orr = elem(arms["ref"][s][(b, h)])
                    rows.append((b, math.log(ao / ar), eo - er, dangle(oo, orr)))
                ea[a] = rows
            for i, x in enumerate(("lna", "e", "om")):
                for a in ("off", "on"):
                    v = [abs(r[1 + i]) for r in ea[a]]
                    out[f"s{s}_h{h}_{a}_{x}"] = {
                        "med": med(v), "p90": pct(v, 0.9), "max": max(v),
                    }
            # K1 bias (the ref cancels: mean of on-off)
            for i, x in enumerate(("lna", "e", "om")):
                d = [r_on[1 + i] - r_off[1 + i] for r_on, r_off in zip(ea["on"], ea["off"])]
                m, sd = mean_std(d)
                out[f"s{s}_h{h}_bias_{x}"] = {"mean": m, "std": sd, "n": len(d), "z": m / (sd / math.sqrt(len(d)))}
            # K2 class
            if s == 1 and h == 1:
                for i, x in enumerate(("lna", "e", "om")):
                    mo = med([abs(r[1 + i]) for r in ea["on"]])
                    mf = med([abs(r[1 + i]) for r in ea["off"]])
                    out[f"K2_ratio_med_{x}"] = mo / mf
            # K4 tail
            if s == 1:
                for i, x in enumerate(("lna", "e", "om")):
                    vo = sorted(abs(r[1 + i]) for r in ea["on"])
                    vf = pct([abs(r[1 + i]) for r in ea["off"]], 0.99)
                    out[f"s1_h{h}_tail_{x}"] = {"max_on": max(vo), "p99_off_x10": 10 * vf}
            # K3 growth per body (h>=2 vs h=1) — needs both horizons vs the same ref
        if len(hs) >= 2:
            slopes = {}
            for a in ("off", "on"):
                sl = []
                for b in bodies:
                    try:
                        r1a, r1r = arms[a][s][(b, 1)], arms["ref"][s][(b, 1)]
                        r2a, r2r = arms[a][s][(b, 2)], arms["ref"][s][(b, 2)]
                    except KeyError:
                        continue
                    a1, e1, o1 = elem(r1a); ar1, er1, or1 = elem(r1r)
                    a2, e2, o2 = elem(r2a); ar2, er2, or2 = elem(r2r)
                    d1 = abs(math.log(a1 / ar1)); d2 = abs(math.log(a2 / ar2))
                    orb1 = max((r1a["tick"] - r1a["first"]) / r1a["period"], 1e-9)
                    orb2 = max((r2a["tick"] - r2a["first"]) / r2a["period"], 1e-9)
                    if d1 > 0 and d2 > 0:
                        sl.append((math.log(d2) - math.log(d1)) / (math.log(orb2) - math.log(orb1)))
                slopes[a] = sl
            for a in ("off", "on"):
                out[f"K3_s{s}_growth_slope_{a}"] = {"med": med(slopes[a]), "n": len(slopes[a])}
            out[f"K3_s{s}_delta"] = med(slopes["on"]) - med(slopes["off"])

    # ---- differential growth on-off (no ref needed), both seeds ---------------
    for s in (1, 2):
        if not arms["on"][s] or not arms["off"][s]:
            continue
        hs = sorted({h for (_, h) in arms["on"][s]} - {0})
        if len(hs) < 2:
            continue
        r1 = []
        for b in bodies:
            try:
                on1, of1 = arms["on"][s][(b, hs[0])], arms["off"][s][(b, hs[0])]
                on2, of2 = arms["on"][s][(b, hs[-1])], arms["off"][s][(b, hs[-1])]
            except KeyError:
                continue
            d1 = abs(math.log(elem(on1)[0] / elem(of1)[0]))
            d2 = abs(math.log(elem(on2)[0] / elem(of2)[0]))
            r1.append(d2 / d1 if d1 > 0 else float("inf"))
        out[f"s{s}_differential_growth_ratio_h{hs[-1]}_over_h{hs[0]}"] = {
            "med": med(r1), "p90": pct(r1, 0.9),
        }

    # ---- e-tail decile (seed 1, h=1): where a new error would hide first -----
    if arms["ref"][1]:
        es = sorted(((elem(arms["off"][1][(b, 0)])[1], b) for b in bodies), reverse=True)
        top = {b for _, b in es[: len(es) // 10]}
        for a in ("off", "on"):
            v_top, v_rest = [], []
            for b in bodies:
                if (b, 1) not in arms[a][1]:
                    continue
                aa, ee, _ = elem(arms[a][1][(b, 1)])
                ar, er, _ = elem(arms["ref"][1][(b, 1)])
                (v_top if b in top else v_rest).append(abs(math.log(aa / ar)))
            out[f"s1_etail_{a}"] = {"top_decile_med": med(v_top), "rest_med": med(v_rest)}

    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    sys.exit(main())
