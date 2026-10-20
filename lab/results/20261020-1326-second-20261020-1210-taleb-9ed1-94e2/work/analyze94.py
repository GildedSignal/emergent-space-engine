#!/usr/bin/env python3
"""Analysis for 20261020-1326-second-...-94e2 (second author on 9ed1).

Reads the esans answer trace (ES_ANS_TRACE) and the escsv frame trace (8365's
instrument, carried by 9ed1's patch) and prints, per arm: the worst frames, the
answer-path anatomy (candidates, doll, interval, wall, encounters, the exact
linear bound's skip fraction), the per-body constant when the answer bites, and
import sys, re, importlib.util, os

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "analyze9.py")  # 9ed1's loader, kept beside this script
if not os.path.exists(src):
    src = "/tmp/analyze-9ed1.py"
spec = importlib.util.spec_from_file_location("a9", src)
a9 = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(a9)
except Exception:
    a9 = None

TICK = None  # filled from the csv (gs column vs ticks) if needed

def load_ans(path):
    rows = []
    for line in open(path):
        if not line.startswith("esans"):
            continue
        d = dict(t.split("=", 1) for t in line.split()[1:] if "=" in t)
        rows.append({
            "t": int(d["t"]), "h_gs": float(d["h_gs"]), "cand": int(d["cand"]),
            "near": None if d["near"] == "-" else int(d["near"]), "doll": int(d["doll"]),
            "en": int(d["en"]), "ns": int(d["ns"]), "skipb": int(d["skipb"]), "innow": int(d["innow"]),
        })
    return rows

def frames(csv):
    if a9 is None:
        raise SystemExit("need analyze9.py")
    return a9.load(csv)

def main(err, csv, label):
    ans = load_ans(err)
    fr = frames(csv)
    print(f"== {label}: {len(ans)} answers, {len(fr)} frames")
    top = sorted(ans, key=lambda a: -a["ns"])[:4]
    for a in top:
        us_body = a["ns"] / 1e3 / max(a["doll"], 1)
        print(f"   biggest: cand {a['cand']:>6} near {a['near']} doll {a['doll']} h_gs {a['h_gs']:.0f} "
              f"en {a['en']:>3} ns {a['ns']/1e6:8.1f}ms  {a['ns']/1e3/max(a['cand'],1):6.2f} us/cand  "
              f"{us_body:5.2f} us/body  skipb {a['skipb']/max(a['cand'],1):.2f}")
    big = [a for a in ans if a["cand"] > 50]
    if big:
        tot = sum(a["cand"] for a in big)
        sk = sum(a["skipb"] for a in big)
        print(f"   answers cand>50: {len(big)}, en sum {sum(a['en'] for a in big)}, "
              f"skipb frac {sk/tot:.3f}, total answer wall {sum(a['ns'] for a in big)/1e9:.2f} s")
    h = sorted({a["h_gs"] for a in ans})
    print(f"   intervals h_gs: min {h[0]:.0f} max {h[-1]:.0f} top {h[-4:]}")
    worst = sorted(fr, key=lambda r: -r["ms"])[:4]
    print("   worst frames:", ", ".join(f"f{r['f']} {r['ms']:.0f}ms ev{r['ev']} en{r['en']} held{r['held']} gs{r['gs']:.0f}" for r in worst))
    # chunk arms: for each big answer (ns or cand), find the frame that logged its en (en>0 with gs near t·TICK)
    enb = [r for r in fr if r["en"] > 0]
    if enb:
        print(f"   frames with en>0: {len(enb)}, max en {max(r['en'] for r in enb)}, sum en {sum(r['en'] for r in enb)}")
    held = max((r["held"] for r in fr), default=0)
    rss = max((r["rss"] for r in fr), default=0)
    print(f"   held_max {held}, peak rss {rss:.0f} MB, frames over 12ms {sum(1 for r in fr if r['ms']>12)}")

if __name__ == "__main__":
    main(sys.argv[2], sys.argv[1], sys.argv[3] if len(sys.argv) > 3 else sys.argv[1])
