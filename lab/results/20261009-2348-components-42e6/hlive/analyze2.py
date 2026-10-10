#!/usr/bin/env python3
"""H_live, corrected: quantized-entropy bounds (sample-size safe), per-kind packed live widths,
belt-like vs fleet rates, zero-dv rebind census. Inputs: kS1.jsonl kS7.jsonl."""
import json, math, collections

FIELDS = ["i","t","rk","kind","doll","key","ang","tperi","dv0","dv1","len","level",
          "clock","boundary","lead","rp0","rp1","rv0","rv1","ta","tb","et","c0","c1","new"]

def load(path):
    out = []
    for line in open(path):
        vals=[]
        for x in line.rstrip("\n").split("\t"):
            try: vals.append(int(x))
            except ValueError: vals.append(x)
        out.append(dict(zip(FIELDS, vals)))
    return out

def H0(vals):
    n = len(vals)
    if n == 0: return 0.0
    c = collections.Counter(vals)
    return -sum((k/n)*math.log2(k/n) for k in c.values())

def bounds(vals):
    """Tightest [lower, upper] entropy bound by scale-quantization: X=Y*2^s+Z.
    upper = H0(Y)+s minimized over s; lower = H0(Y) at that s (coarsest sensible)."""
    best = None
    for s in range(0, 49):
        h = H0([v >> s for v in vals])
        u = h + s
        if best is None or u < best[1]:
            best = (s, u, h)
    s, u, h = best
    return {"scale": s, "upper_bits": round(u, 2), "lower_bits": round(h, 2)}

def w(v):
    return max(1, int(abs(v)).bit_length() + (1 if v < 0 else 0))

LIVE = ["ang","tperi_rel","dv0","dv1","rp0","rp1","rv0","rv1","ta","tb","c0","c1","len","level","et_rel"]
DELTA = ["ang_d","tperi_d","dv0","dv1","rp0","rp1","rv0","rv1","ta_d","tb_d","dc0","dc1"]

def run(path, gs, tag, made_n=28):
    recs = load(path)
    for r in recs:
        r["tperi_rel"] = r["tperi"] - r["et"]
        r["et_rel"] = r["et"]
    bodies = collections.defaultdict(list)
    for r in recs:
        bodies[r["i"]].append(r)
    for i in bodies:
        bodies[i].sort(key=lambda r: r["t"])
        prev = None
        for r in bodies[i]:
            if prev is None:
                r["ang_d"], r["tperi_d"], r["ta_d"], r["tb_d"], r["dc0"], r["dc1"] = r["ang"], r["tperi"], r["ta"], r["tb"], r["c0"], r["c1"]
            else:
                r["ang_d"] = ((r["ang"] - prev["ang"] + (1 << 31)) & 0xFFFFFFFF) - (1 << 31)
                r["tperi_d"] = r["tperi"] - prev["tperi"]
                r["ta_d"], r["tb_d"] = r["ta"] - prev["ta"], r["tb"] - prev["tb"]
                r["dc0"], r["dc1"] = r["c0"] - prev["c0"], r["c1"] - prev["c1"]
            prev = r
    made_ships = {i for i in bodies if i < made_n and recs and any(r["kind"] == 0 for r in bodies[i])}
    fleet = {i for i in bodies if i >= made_n}
    def rate(ids, kind=0):
        ks = [r for i in ids if i in bodies for r in bodies[i] if r["kind"] == kind]
        return len(ks), (len(ks) / len(ids) / gs if ids else 0)
    mk, mr = rate(made_ships); fk, fr = rate(fleet)
    zero_dv = [r for r in recs if r["dv0"] == 0 and r["dv1"] == 0]
    res = {"tag": tag, "records": len(recs), "bodies": len(bodies),
           "made_ship_bodies": len(made_ships), "fleet_bodies": len(fleet),
           "made_kicks": mk, "made_kicks_per_body_game_s": round(mr, 6),
           "fleet_kicks": fk, "fleet_kicks_per_body_game_s": round(fr, 4),
           "zero_dv_kicks": len(zero_dv), "zero_dv_share": round(len(zero_dv) / len(recs), 3),
           "zero_dv_new_entry_share": round(sum(r["new"] for r in zero_dv) / max(1, len(zero_dv)), 3)}
    # per-kind packed live widths (static bitfields, exact) and entropy bounds
    kinds = {0: "ship", 2: "planet", 3: "moon"}
    pk = {}
    for kd, kn in kinds.items():
        kr = [r for r in recs if r["kind"] == kd]
        if not kr: continue
        widths = {f: max(w(r[f]) for r in kr) for f in LIVE}
        packed = sum(widths.values())
        fl = {f: bounds([r[f] for r in kr]) for f in LIVE}
        pk[kn] = {"packed_bits": packed, "packed_bytes": round(packed / 8, 1),
                  "floor_upper_bits": round(sum(v["upper_bits"] for v in fl.values()), 1),
                  "floor_lower_bits": round(sum(v["lower_bits"] for v in fl.values()), 1),
                  "widths": widths, "bounds": {f: fl[f] for f in ["ang","tperi_rel","dv0","rp0","rv0","ta","tb"]}}
    res["live_state_per_kind"] = pk
    # replay/scar stream: per-body delta coding, all ship kicks
    sr = [r for i in bodies for r in bodies[i] if r["kind"] == 0 and len(bodies[i]) > 1]
    stream = {f: [r[f] for r in sr] for f in DELTA}
    res["scar_stream"] = {f: bounds(v) for f, v in stream.items()}
    res["scar_bits_per_kick_upper"] = round(sum(v["upper_bits"] for v in res["scar_stream"].values()), 1)
    # belt verdict at 1e9 bodies, 8 GB (or the approved 4 GiB store budget)
    bits_kick = res["scar_bits_per_kick_upper"]
    res["verdict"] = {
        "belt_like_rate_per_game_s": round(mr, 6),
        "belt_bits_per_body_game_s": round(bits_kick * mr, 4),
        "GB_per_1e9_at_packed_ship_bits": round(pk["ship"]["packed_bits"] * 1e9 / 8 / 1e9, 1),
        "game_s_to_spend_8_bytes_per_body_belt": round(8 * 8 / max(1e-9, bits_kick * mr), 0),
        "game_s_to_spend_8B_at_fleet_rate": round(8 * 8 / max(1e-9, bits_kick * fr), 1),
    }
    return res

out = [run("kS1.jsonl", 6000.0, "seed1_rtf300_6000gs"), run("kS7.jsonl", 6000.0, "seed7_rtf300_6000gs")]
json.dump(out, open("analysis2.json", "w"), indent=1)
for o in out:
    print(json.dumps({k: v for k, v in o.items() if k not in ("live_state_per_kind", "scar_stream")}, indent=1))
    for kn, kv in o["live_state_per_kind"].items():
        print(kn, "packed", kv["packed_bits"], "b =", kv["packed_bytes"], "B | floor in [", kv["floor_lower_bits"], ",", kv["floor_upper_bits"], "] bits")
    print("scar stream upper", o["scar_bits_per_kick_upper"], "bits/kick; verdict", o["verdict"])
