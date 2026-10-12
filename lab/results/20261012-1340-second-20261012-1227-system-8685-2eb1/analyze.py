#!/usr/bin/env python3
"""Analyze the second-author record: orbit-anchored (p) vs tick-anchored (seg) vs
uniform (u) vs window-only (w) kick schedules, belt scene, 64 seeds vs u2048 truth.
Also: W-sweep tables and the encounter 64-seed inversion check."""
import csv, math, os, statistics as st

W = os.path.join(os.path.dirname(os.path.abspath(__file__)), "work")

def load(name):
    path = os.path.join(W, name)
    if not os.path.exists(path): return None
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            rows.append({k: (r[k] if k in ("config","variant") else
                             (int(float(v)) if k in ("seed","kicks","solves","ejected_at_sample","nfit") else float(v)))
                         for k, v in r.items()})
    return rows

def med(x): return st.median(x) if x else float("nan")
def mad(x):
    if not x: return float("nan")
    m = med(x)
    return med([abs(v - m) for v in x])

BODY_ORBITS = {"encounter": 1000 * 1.25**1.5, "resonant": 1000 * 1.5874**1.5,
               "belt": 500 * 5.2**1.5}

# ---------- belt 64-seed grid ----------
truth = load("belt-truth64.csv")
tv = [r["varpi_rate"] for r in truth if r["nfit"] > 0]
te = [r["e_rate"] for r in truth if r["nfit"] > 0]
tj = [r["jacobi_max"] for r in truth]
Mv, Me = mad(tv), mad(te)
tmed_v, tmed_e = med(tv), med(te)
floor = None
print("=== BELT, 64 seeds, truth u2048 ===")
print(f"truth: med wpidot={tmed_v:.4e} MAD={Mv:.3e}  med edot={tmed_e:.4e} MAD={Me:.3e}  "
      f"eject={sum(1 for r in truth if r['ejected_at_sample']>=0)}/64  medJacMax={med(tj):.3e}")
tf = load("belt-truthfine64.csv")
if tf:
    fv = [r["varpi_rate"] for r in tf if r["nfit"] > 0]
    fe = [r["e_rate"] for r in tf if r["nfit"] > 0]
    print(f"truth check u4096 ({len(tf)} seeds): dmed(wpidot)={abs(med(fv)-tmed_v)/Mv:.2f} MADs, "
          f"dmed(edot)={abs(med(fe)-tmed_e)/Me:.2f} MADs")
print(f"{'variant':<12} {'k/orb':>6} {'sol/orb':>7} {'d_wpidot':>9} {'rel%':>8} {'d_edot':>8} {'Dej':>4} {'medJac':>9} {'x_floor':>8}")
order = ["u64","u32","u16","u8","w0.5","w0.5seg4","w0.5seg8","w0.5seg16",
         "w0.5seg8m","w0.5seg8n","w0.5seg8mn","w0.5p2","w0.5p4","w0.5p8","w0.5p16","w0.5p32"]
for v in order:
    rows = load(f"belt64-{v}.csv")
    if not rows: continue
    kv = [r["varpi_rate"] for r in rows if r["nfit"] > 0]
    ke = [r["e_rate"] for r in rows if r["nfit"] > 0]
    kj = [r["jacobi_max"] for r in rows]
    kpo = sum(r["kicks"] for r in rows) / len(rows) / BODY_ORBITS["belt"]
    spo = sum(r["solves"] for r in rows) / len(rows) / BODY_ORBITS["belt"]
    eject = sum(1 for r in rows if r["ejected_at_sample"] >= 0)
    dw = abs(med(kv) - tmed_v) / Mv
    de = abs(med(ke) - tmed_e) / Me
    rel = (med(kv) / tmed_v - 1) * 100
    if v == "u64": floor = med(kj)
    xf = med(kj) / floor if floor else float("nan")
    print(f"{v:<12} {kpo:>6.2f} {spo:>7.2f} {dw:>9.2f} {rel:>+8.2f} {de:>8.2f} {eject:>4} {med(kj):>9.3e} {xf:>8.1f}")

# ---------- belt W-sweep, 16 seeds ----------
print("\n=== BELT W-sweep (16 seeds): window-only vs window+orbit-anchored p8 ===")
print(f"{'W':>7} | {'w-only rel%':>11} {'w d_edot':>9} | {'p8 rel%':>8} {'p8 d_edot':>9} {'p8 x_floor':>10}")
for Wv in ["0.125","0.25","0.5","1.0","2.5"]:
    a = load(f"belt-w{Wv}-sweep2.csv"); b = load(f"belt-w{Wv}p8-sweep.csv")
    ra = abs(med([r["varpi_rate"] for r in a if r["nfit"]>0]) / tmed_v - 1) * 100 if a else float("nan")
    da = abs(med([r["e_rate"] for r in a if r["nfit"]>0]) - tmed_e) / Me if a else float("nan")
    rb = abs(med([r["varpi_rate"] for r in b if r["nfit"]>0]) / tmed_v - 1) * 100 if b else float("nan")
    db = abs(med([r["e_rate"] for r in b if r["nfit"]>0]) - tmed_e) / Me if b else float("nan")
    xf = med([r["jacobi_max"] for r in b]) / floor if (b and floor) else float("nan")
    print(f"{Wv:>7} | {ra:>+11.1f} {da:>9.2f} | {rb:>+8.2f} {db:>9.2f} {xf:>10.1f}")

# ---------- encounter 64-seed inversion ----------
enc = load("enc-truth64.csv")
if enc:
    print("\n=== ENCOUNTER, 64 seeds, truth u4096 (16) ===")
    ev = [r["varpi_rate"] for r in enc if r["nfit"] > 0]
    ee = [r["e_rate"] for r in enc if r["nfit"] > 0]
    Mve, Mee = mad(ev), mad(ee)
    print(f"truth u2048(64): med wpidot={med(ev):.3e} MAD={Mve:.2e}  med edot={med(ee):.3e} MAD={Mee:.2e}")
    ef = load("enc-truthfine64.csv")
    if ef:
        efv = [r["varpi_rate"] for r in ef if r["nfit"] > 0]
        efe = [r["e_rate"] for r in ef if r["nfit"] > 0]
        print(f"truth u4096(16): dmed(wpidot)={abs(med(efv)-med(ev))/Mve:.2f} MADs, dmed(edot)={abs(med(efe)-med(ee))/Mee:.2f} MADs")
        tv2, te2 = med(efe), med(efe) and med(efe)
        tmed_ev, tmed_ee = med(efv), med(efe)
    print(f"{'variant':<8} {'k/orb':>6} {'d_wpidot':>9} {'d_edot':>8} {'Dej':>4}")
    for v in ["u64","u32","u16","u8","w0.25","w0.5","w1.0"]:
        rows = load(f"enc64-{v}.csv")
        if not rows: continue
        kv = [r["varpi_rate"] for r in rows if r["nfit"] > 0]
        ke = [r["e_rate"] for r in rows if r["nfit"] > 0]
        kpo = sum(r["kicks"] for r in rows) / len(rows) / BODY_ORBITS["encounter"]
        eject = sum(1 for r in rows if r["ejected_at_sample"] >= 0)
        dw = abs(med(kv) - tmed_ev) / mad(efv)
        de = abs(med(ke) - tmed_ee) / mad(efe)
        print(f"{v:<8} {kpo:>6.2f} {dw:>9.2f} {de:>8.2f} {eject:>4}")
