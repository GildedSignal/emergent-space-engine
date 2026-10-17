#!/usr/bin/env python3
"""stagger_legality v2 analysis (lab run 20261017-1918-second-20261017-1829-taleb-75d6-d5c3).

Reads the v2 probe CSVs (off/on/sym/ref8/ref9 x seeds 1,2, every arm read at the SAME absolute
ticks), checks the controls C1-C4 + P5/P8 and the pre-registered criteria K1-K5 of predictions.md,
and prints the numbers the dossier quotes. Pure statistics on exact-integer key parts (k48, angle32)
and the 17-digit periapsis; no engine state is touched.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARMS = ("off", "on", "sym", "ref8", "ref9")
STAG = ("off", "on", "sym")


def load(arm: str, seed: int):
    rows = {}
    planets = None
    hdr = {}
    for line in (HERE / f"{arm}_s{seed}.csv").read_text().splitlines():
        if line.startswith("# planet"):
            planets = line
        if line.startswith("#"):
            for k in ("width", "p_min_ticks", "horizon_base"):
                if k in line:
                    v = line.split(f"{k}=")[1]
                    hdr[k] = v
            continue
        if line.startswith("arm,"):
            continue
        f = line.split(",")
        if len(f) != 17:
            continue
        r = dict(
            body=int(f[2]), h=int(f[3]), tick=int(f[4]), alive=int(f[5]), refus=int(f[6]),
            events=int(f[7]), step=int(f[8]), first=int(f[9]), period=float(f[10]), peri=float(f[11]),
            k48=int(f[12]), kexp=int(f[13]), ang=int(f[14]), lead=int(f[16]),
        )
        assert r["kexp"] == 0, f"k_exponent {r['kexp']} (not a periodic key)"
        rows[(r["body"], r["h"])] = r
    return rows, planets, hdr


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


def ranks(v):
    idx = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(idx):
        j = i
        while j + 1 < len(idx) and v[idx[j + 1]] == v[idx[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[idx[k]] = avg
        i = j + 1
    return r


def spearman(x, y):
    rx, ry = ranks(x), ranks(y)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else float("nan")


def err_rows(arm_rows, ref_rows, bodies, h):
    """Per body (ln a, e, omega) errors of arm vs ref at horizon h (the common tick)."""
    out = []
    for b in bodies:
        if (b, h) not in arm_rows or (b, h) not in ref_rows:
            continue
        a, e, o = elem(arm_rows[(b, h)])
        ar, er, orr = elem(ref_rows[(b, h)])
        out.append((b, math.log(a / ar), e - er, dangle(o, orr)))
    return out


def main():
    out = {}
    data = {a: {} for a in ARMS}
    for a in ARMS:
        for s in (1, 2):
            try:
                data[a][s], pl, hdr = load(a, s)
                if pl:
                    out[f"planets_{a}_s{s}"] = pl
                if hdr.get("width"):
                    out.setdefault("wave_width_ticks", {})[f"{a}_s{s}"] = hdr["width"]
            except FileNotFoundError:
                data[a][s] = None

    # ---- controls -------------------------------------------------------------
    bodies = sorted(b for (b, h) in data["off"][1] if h == 0)
    for s in (1, 2):
        for a in ("on", "sym"):
            if not data[a][s]:
                continue
            bad = [
                b for b in bodies
                if (data["off"][s][(b, 0)]["k48"], data["off"][s][(b, 0)]["ang"], data["off"][s][(b, 0)]["peri"])
                != (data[a][s][(b, 0)]["k48"], data[a][s][(b, 0)]["ang"], data[a][s][(b, 0)]["peri"])
            ]
            out[f"C1_birth_keys_identical_{a}_s{s}"] = {"mismatches": len(bad), "n": len(bodies)}
    # P8: the grids. first_kick(on) - first_kick(off) in [0, birth step); |fk_sym - fk_on| tiny.
    for s in (1, 2):
        if data["on"][s] and data["off"][s]:
            offs = [data["on"][s][(b, 1)]["first"] - data["off"][s][(b, 1)]["first"] for b in bodies]
            out.setdefault("P8_offset_ticks", {})[f"s{s}"] = {
                "min": min(offs), "max": max(offs),
                "in_birth_step": all(0 <= o < data["off"][s][(b, 0)]["step"] for o, b in zip(offs, bodies)),
            }
        if data["sym"][s] and data["on"][s]:
            d = [abs(data["sym"][s][(b, 1)]["first"] - data["on"][s][(b, 1)]["first"]) for b in bodies]
            out.setdefault("P8_fk_sym_minus_on", {})[f"s{s}"] = {"max_abs": max(d)}
    out["C2_planets_off_vs_on_s1"] = out.get("planets_off_s1") == out.get("planets_on_s1")
    out["C2_planets_off_vs_sym_s1"] = out.get("planets_off_s1") == out.get("planets_sym_s1")
    alive = all(
        data[a][s][(b, h)]["alive"] == 1 and data[a][s][(b, h)]["refus"] == 0
        for a in ARMS for s in (1, 2) if data[a][s]
        for (b, h) in data[a][s]
    )
    out["P5_alive_no_refusals"] = alive

    # C4: the first-rebind lead (mechanics), from the mech CSVs taken just past each arm's wave.
    for a, tickfile in (("off", "mech_off.csv"), ("on", "mech_on.csv"), ("sym", "mech_sym.csv")):
        p = HERE / tickfile
        if not p.exists():
            continue
        rows = [dict(body=int(f[2]), first=int(f[9]), lead=int(f[16]))
                for f in (l.split(",") for l in p.read_text().splitlines())
                if len(f) == 17 and f[0] == a and f[3] == "1"]
        if a in ("off", "on"):
            out[f"C4_lead_equals_first_kick_{a}"] = sum(1 for r in rows if r["lead"] == r["first"])
        else:
            # sym: lead must equal the OFF arm's first kick (its own half) to within the step re-derivation.
            offk = {r["body"]: r["first"] for r in
                    [dict(body=int(f[2]), first=int(f[9]))
                     for f in (l.split(",") for l in (HERE / "mech_off.csv").read_text().splitlines())
                     if len(f) == 17 and f[0] == "off" and f[3] == "1"]}
            d = [abs(r["lead"] - offk[r["body"]]) for r in rows if r["body"] in offk]
            steps = [r for r in rows]
            out["C4_sym_lead_minus_off_half"] = {"max_abs": max(d) if d else None, "n": len(d)}

    # Descriptive (not a criterion): the checker's failed monotone fit, redone at the common tick —
    # |on - off| against the offset itself. A phase-reshuffle term predicts rho ~ 0.
    for s in (1, 2):
        if data["on"][s] and data["off"][s]:
            offs = [data["on"][s][(b, 1)]["first"] - data["off"][s][(b, 1)]["first"] for b in bodies]
            da, do = [], []
            for o, b in zip(offs, bodies):
                if (b, 1) in data["on"][s] and (b, 1) in data["off"][s]:
                    da.append(abs(math.log(elem(data["on"][s][(b, 1)])[0] / elem(data["off"][s][(b, 1)])[0])))
                    do.append(o)
            out[f"descr_rho_absonoff_vs_offset_s{s}"] = spearman(do, da)

    # ---- errors vs the finest ladder (ref9); ref8 kept for the ladder line --------------------
    ref = 9
    for s in (1, 2):
        if not data[f"ref{ref}"][s]:
            continue
        hs = sorted({h for (_, h) in data[f"ref{ref}"][s]} - {0})
        ea = {}
        for h in hs:
            for a in STAG:
                ea[(a, h)] = err_rows(data[a][s], data[f"ref{ref}"][s], bodies, h)
            for i, x in enumerate(("lna", "e", "om")):
                for a in STAG:
                    v = [abs(r[1 + i]) for r in ea[(a, h)]]
                    out[f"s{s}_h{h}_{a}_{x}_vs_ref{ref}"] = {"med": med(v), "p90": pct(v, 0.9), "max": max(v)}
            # K1 bias (the ref cancels: mean of X - off)
            for i, x in enumerate(("lna", "e", "om")):
                for a in ("on", "sym"):
                    d = [r_a[1 + i] - r_o[1 + i] for r_a, r_o in zip(ea[(a, h)], ea[("off", h)])]
                    m, sd = mean_std(d)
                    out[f"s{s}_h{h}_bias_{a}_{x}"] = {"mean": m, "std": sd, "n": len(d), "z": m / (sd / math.sqrt(len(d)))}
            # K2 class (s1 h1): against the finest ladder, the corrected headline
            if s == 1 and h == 1:
                for i, x in enumerate(("lna", "e", "om")):
                    mf = med([abs(r[1 + i]) for r in ea[("off", h)]])
                    for a in ("on", "sym"):
                        out[f"K2_ratio_{a}_vs_ref{ref}_{x}"] = med([abs(r[1 + i]) for r in ea[(a, h)]]) / mf
            # vs ref8 for the anchoring line: the same data read against the coarser, tick-0-anchored ladder
            if data["ref8"][s] and h == 1:
                for i, x in enumerate(("lna", "e", "om")):
                    for a in STAG:
                        rows8 = err_rows(data[a][s], data["ref8"][s], bodies, h)
                        out[f"s{s}_h{h}_{a}_{x}_vs_ref8_med"] = med([abs(r[1 + i]) for r in rows8])
            # K4 tail (s1, h2)
            if s == 1:
                for i, x in enumerate(("lna", "e", "om")):
                    vf = pct([abs(r[1 + i]) for r in ea[("off", h)]], 0.99)
                    for a in ("on", "sym"):
                        vo = [abs(r[1 + i]) for r in ea[(a, h)]]
                        out[f"s1_h{h}_tail_{a}_{x}"] = {"max": max(vo), "p99_off_x10": 10 * vf}
        # K3 growth per body (h2 vs h1) vs the same ref
        if len(hs) >= 2:
            slopes = {}
            for a in STAG:
                sl = []
                for b in bodies:
                    try:
                        r1a, r1r = data[a][s][(b, 1)], data[f"ref{ref}"][s][(b, 1)]
                        r2a, r2r = data[a][s][(b, 2)], data[f"ref{ref}"][s][(b, 2)]
                    except KeyError:
                        continue
                    d1 = abs(math.log(elem(r1a)[0] / elem(r1r)[0]))
                    d2 = abs(math.log(elem(r2a)[0] / elem(r2r)[0]))
                    orb1 = max((r1a["tick"] - r1a["first"]) / r1a["period"], 1e-9)
                    orb2 = max((r2a["tick"] - r2a["first"]) / r2a["period"], 1e-9)
                    if d1 > 0 and d2 > 0:
                        sl.append((math.log(d2) - math.log(d1)) / (math.log(orb2) - math.log(orb1)))
                slopes[a] = sl
            for a in STAG:
                out[f"K3_s{s}_growth_slope_{a}"] = {"med": med(slopes[a]), "n": len(slopes[a])}
            for a in ("on", "sym"):
                out[f"K3_s{s}_delta_{a}"] = med(slopes[a]) - med(slopes["off"])

    # ---- the ladder (s1): off-ref8, off-ref9, ref8-ref9 (the anchoring correlation) ------------
    if data["ref8"][1] and data["ref9"][1]:
        for h in (1, 2):
            for i, x in enumerate(("lna", "e", "om")):
                pairs = {
                    "off_ref8": err_rows(data["off"][1], data["ref8"][1], bodies, h),
                    "off_ref9": err_rows(data["off"][1], data["ref9"][1], bodies, h),
                    "ref8_ref9": err_rows(data["ref8"][1], data["ref9"][1], bodies, h),
                }
                for k, rows in pairs.items():
                    out[f"ladder_s1_h{h}_{k}_{x}_med"] = med([abs(r[1 + i]) for r in rows])

    # ---- ref-free same-tick differentials (no ladder involved) --------------------------------
    for s in (1, 2):
        hs = sorted({h for (_, h) in data["on"][s]} - {0}) if data["on"][s] else []
        for h in hs:
            for a in ("on", "sym"):
                rows = err_rows(data[a][s], data["off"][s], bodies, h)  # arm vs OFF, same tick, no ref
                for i, x in enumerate(("lna", "e", "om")):
                    v = [abs(r[1 + i]) for r in rows]
                    out[f"s{s}_h{h}_same_tick_diff_{a}_{x}"] = {"med": med(v), "std": (lambda vv: mean_std(vv)[1])(v), "max": max(v)}
        if len(hs) >= 2:
            for a in ("on", "sym"):
                r1 = err_rows(data[a][s], data["off"][s], bodies, hs[0])
                r2 = err_rows(data[a][s], data["off"][s], bodies, hs[-1])
                ratios = []
                for ra, rb in zip(r1, r2):
                    d1 = abs(ra[1])
                    d2 = abs(rb[1])
                    if d1 > 0:
                        ratios.append(d2 / d1)
                out[f"s{s}_differential_growth_ratio_{a}"] = {"med": med(ratios), "p90": pct(ratios, 0.9)}

    # ---- K5: the mechanism decomposition -------------------------------------------------------
    for s in (1, 2):
        if not (data["sym"][s] and data["on"][s] and data["ref9"][s]):
            continue
        for h in (1, 2):
            if (bodies[0], h) not in data["ref9"][s]:
                continue
            e_on = err_rows(data["on"][s], data["ref9"][s], bodies, h)
            e_sym = err_rows(data["sym"][s], data["ref9"][s], bodies, h)
            e_off = err_rows(data["off"][s], data["ref9"][s], bodies, h)
            if not (len(e_on) == len(e_sym) == len(e_off)):
                continue
            for i, x in enumerate(("lna", "e", "om")):
                d_on = [a[1 + i] - o[1 + i] for a, o in zip(e_on, e_off)]
                d_sym = [a[1 + i] - o[1 + i] for a, o in zip(e_sym, e_off)]
                out[f"K5_s{s}_h{h}_rho_on_off_vs_sym_off_{x}"] = spearman(d_on, d_sym)

    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    sys.exit(main())
