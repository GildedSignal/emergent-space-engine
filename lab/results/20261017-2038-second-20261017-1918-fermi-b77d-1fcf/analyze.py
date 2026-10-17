#!/usr/bin/env python3
"""Analyze flowcrowd logs: the held-scan pin in real bytes (counting GlobalAlloc).

Pin = least-squares slope of live_b vs held over the growing window (frozen arms),
reported over the whole growth AND over its first 40 held increments (the early-flight
phase, comparable across arms however long the flight ran — the checker's K=2,400 window).
"""
import itertools
import re
import sys
import math
from pathlib import Path


def parse(path):
    arm = {"probes": [], "name": path.stem, "loadavg": ""}
    for line in path.read_text().splitlines():
        if line.startswith("machine:"):
            arm["loadavg"] = line.split('"')[1] if '"' in line else ""
        if line.startswith("flowcrowd "):
            for kv in re.findall(r"(\w+)=([-\d.]+)", line):
                arm.setdefault(kv[0], kv[1])
        m = re.match(
            r"probe f=(\d+) gs=([\d.]+) held=(\d+) live_b=(\d+) live_a=(\d+) "
            r"rss_mb=([\d.]+) cat=(\d+) ev=(\d+) engine_ms=([\d.]+) gather_ms=([\d.]+) seen=(\d+)",
            line,
        )
        if m:
            f, gs, held, lb, la, rss, cat, ev, ems, gms, seen = m.groups()
            arm["probes"].append(dict(f=int(f), gs=float(gs), held=int(held), lb=int(lb),
                                      la=int(la), rss=float(rss), cat=int(cat),
                                      ems=float(ems), gms=float(gms), seen=int(seen)))
        if line.startswith("summary "):
            for kv in re.findall(r"(\w+)=([\w.]+)", line):
                arm["summary_" + kv[0]] = kv[1]
    return arm


def slope(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return None
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    syy = sum((y - my) ** 2 for y in ys)
    r2 = (sum((x - mx) * (y - my) for x, y in zip(xs, ys)) ** 2) / (sxx * syy) if syy else 0
    return b, r2


def window_pin(w, first=None):
    if first:
        h0 = w[0]["held"]
        w = list(itertools.takewhile(lambda q: q["held"] <= h0 + first, w))
    xs = [q["held"] for q in w]
    if len(set(xs)) < 3:
        return None
    sb = slope(xs, [q["lb"] for q in w])
    sa = slope(xs, [q["la"] for q in w])
    sr = slope(xs, [q["rss"] * 1e6 for q in w])
    if not sb:
        return None
    cat = sum(q["cat"] for q in w) / len(w)
    return dict(pin_kb=sb[0] / 1e3, r2=sb[1], allocs=sa[0] if sa else 0, cat=cat,
                b_per_entry=sb[0] / max(1, cat), held1=xs[-1],
                rss_kb=sr[0] / 1e3 if sr else 0)


def analyze(arm):
    p = arm["probes"]
    out = {"name": arm["name"], "loadavg": arm.get("loadavg", "?")}
    out["build_live_mb"] = float(arm.get("build_live_mb", 0))
    out["cat_build"] = int(arm.get("cat", 0))
    if not p:
        return out
    out["held_max"] = max(q["held"] for q in p)
    out["gs_end"] = p[-1]["gs"]
    out["frames"] = len(p)
    grown = [i for i, q in enumerate(p) if q["held"] > 0]
    out["frozen"] = bool(grown) and all(
        p[i]["held"] >= p[i - 1]["held"] for i in range(grown[0] + 1, len(p)))
    out["drained_end"] = p[-1]["held"]
    if grown and out["held_max"] >= 3:
        w = p[grown[0]:]
        wp = window_pin(w)
        we = window_pin(w, first=40)
        if wp:
            out.update(pin_kb=wp["pin_kb"], pin_r2=wp["r2"], allocs_per_scan=wp["allocs"],
                       cat_mean=wp["cat"], pin_b_per_entry=wp["b_per_entry"],
                       rss_slope_kb=wp["rss_kb"], live_mb_end=w[-1]["lb"] / 1e6)
            out["arr_per_gs"] = (w[-1]["held"] - w[0]["held"]) / max(1e-9, w[-1]["gs"] - w[0]["gs"])
        if we:
            out["early"] = we
    g = sorted(q["gms"] for q in p)
    e = sorted(q["ems"] for q in p)
    out["gather_p50_ms"] = g[len(g) // 2] if g else 0
    out["engine_p50_ms"] = e[len(e) // 2] if e else 0
    out["seen_max"] = max(q["seen"] for q in p)
    out["cat_end"] = p[-1]["cat"]
    return out


def main(flight_dir):
    rows = []
    for path in sorted(Path(flight_dir).glob("K*.log")):
        r = analyze(parse(path))
        if r.get("frames"):
            rows.append(r)
    print(("{:<8} {:>14} {:>4} {:>8} {:>6} {:>11} {:>5} {:>9} {:>8} {:>7} {:>10} {:>8} "
           "{:>7} {:>8} {:>5} {:>6} {:>6}").format(
        "arm", "load", "catE", "held_max", "froz", "pin kB/scan", "r2", "B/entry",
        "cat_mean", "arr/gs", "live MB end", "rss kB/s", "eng50", "gat50", "seen", "fram", "gs"))
    for r in rows:
        d = {**{k: 0 for k in ("pin_kb", "pin_r2", "pin_b_per_entry", "cat_mean",
                               "arr_per_gs", "live_mb_end", "rss_slope_kb",
                               "engine_p50_ms", "gather_p50_ms", "seen_max", "cat_end")},
             **r}
        print(("{name:<8} {loadavg:>14} {cat_end:>4.0f} {held_max:>8} {frozen!s:>6} "
               "{pin_kb:>11.0f} {pin_r2:>5.2f} {pin_b_per_entry:>9.0f} {cat_mean:>8.0f} "
               "{arr_per_gs:>7.4f} {live_mb_end:>10.1f} {rss_slope_kb:>8.0f} "
               "{engine_p50_ms:>7.2f} {gather_p50_ms:>5.1f} {seen_max:>6} {frames:>6} "
               "{gs_end:>6.0f}").format(**d))
    print("\nearly-flight pins (first 40 held increments — the checker's window):")
    print(("{:<8} {:>12} {:>5} {:>9} {:>9} {:>9} {:>12}").format(
        "arm", "pin kB/scan", "r2", "B/entry", "cat_mean", "allocs", "rss kB/scan"))
    early = []
    for r in rows:
        e = r.get("early")
        if e:
            early.append((r["name"], e))
            print(f"{r['name']:<8} {e['pin_kb']:>12.0f} {e['r2']:>5.2f} {e['b_per_entry']:>9.0f} "
                  f"{e['cat']:>9.0f} {e['allocs']:>9.0f} {e['rss_kb']:>12.0f}")
    # the law across K on the early window (phase-matched)
    law = [(e["cat"], e["pin_kb"], e["b_per_entry"]) for _, e in early if e["r2"] > 0.9]
    if len(law) >= 3:
        law.sort()
        print("\nearly-window pin law over catalogue entries:")
        ex = slope([math.log10(c) for c, _, _ in law], [math.log10(k) for _, k, _ in law])
        ee = slope([math.log10(c) for c, _, _ in law], [math.log10(b) for _, _, b in law])
        for c, k, b in law:
            print(f"  cat={c:7.0f}  pin={k:10.0f} kB/scan  {b:8.0f} B/entry")
        if ex:
            print(f"  pin/scan exponent vs cat: {ex[0]:.2f} (r2 {ex[1]:.3f}); "
                  f"per-entry exponent: {ee[0]:.2f} (r2 {ee[1]:.3f})")
        for gb in (0.97, 8.0):
            need = gb * 1e9 / 2048
            below = [c for c, k, _ in law if k * 1e3 <= need]
            above = [c for c, k, _ in law if k * 1e3 >= need]
            print(f"  2048-count fence crosses {gb} GB at pin {need/1e6:.2f} MB/scan "
                  f"(between cat {max(below) if below else '-'} and {min(above) if above else '-'})")
    print("\nper-arm summaries (verbatim):")
    for path in sorted(Path(flight_dir).glob("K*.log")):
        for line in path.read_text().splitlines():
            if line.startswith("summary "):
                print(f"  {path.stem}: {line[len('summary '):]}")



def phase_windows(flight_dir):
    import re as _re
    print("\nphase windows (40 held each — the pin declines as the crowd dissolves):")
    for path in sorted(Path(flight_dir).glob("K*.log")):
        rows = []
        for l in path.read_text().splitlines():
            m = _re.match(r"probe f=\d+ gs=([\d.]+) held=(\d+) live_b=(\d+).*cat=(\d+)", l)
            if m:
                rows.append(tuple(float(x) for x in m.groups()))
        grown = [i for i, q in enumerate(rows) if q[1] > 0]
        if not grown or max(q[1] for q in rows) < 41:
            continue
        w = rows[grown[0]:]
        h0 = w[0][1]
        print(f"  {path.stem}:")
        while h0 + 40 <= w[-1][1]:
            win = [q for q in w if h0 < q[1] <= h0 + 40]
            if len(win) >= 5:
                dh = win[-1][1] - win[0][1]
                db = win[-1][2] - win[0][2]
                cat = sum(x[3] for x in win) / len(win)
                print(f"    held {int(h0)}->{int(h0+40)}: {db/dh/1e3:8.0f} kB/scan  cat~{cat:.0f}  "
                      f"{db/dh/max(1,cat):6.0f} B/entry  gs {win[0][0]:.0f}-{win[-1][0]:.0f}")
            h0 += 40
    print("\nK10000u per-held-scan deltas (the first includes birth churn; 2nd/3rd are the pin):")
    for path in sorted(Path(flight_dir).glob("K10000u.log")):
        prev = None
        for l in path.read_text().splitlines():
            m = _re.match(r"probe f=\d+ gs=[\d.]+ held=(\d+) live_b=(\d+) live_a=\d+ rss_mb=[\d.]+ cat=(\d+)", l)
            if not m:
                continue
            held, lb, cat = int(m.group(1)), float(m.group(2)), int(m.group(3))
            if prev is not None and held > prev[0]:
                d = (lb - prev[1]) / 1e6
                print(f"  held {prev[0]}->{held}: +{d:.1f} MB  cat={cat}  ({d*1e3/max(1,cat):.1f} kB/entry)")
            prev = (held, lb, cat)




def transition_pins(flight_dir):
    """The capture's own pin: live_b delta across frames where held +1 (churn excluded).

    The estimator the window slopes cannot be: births and dissolution are collinear with
    held growth at a fixed arrival rate, so window slopes alias them into the pin (b8e2's
    named trap); the per-transition delta sees only what the capture itself allocated.
    """
    import re as _re
    import statistics as _st
    print("\nper-transition pins (live_b delta on held +1 — the capture's own allocation):")
    print(f"{'arm':<8} {'n':>5} {'median kB':>10} {'p25':>7} {'p75':>7} {'B/entry':>8} {'allocs':>7}")
    law = []
    for path in sorted(Path(flight_dir).glob("K*.log")):
        rows = []
        for l in path.read_text().splitlines():
            m = _re.match(r"probe f=\d+ gs=[\d.]+ held=(\d+) live_b=(\d+) live_a=(\d+) rss_mb=[\d.]+ cat=(\d+)", l)
            if m:
                rows.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))
        ds, als, cats = [], [], []
        for p, r in zip(rows, rows[1:]):
            if r[0] == p[0] + 1:
                ds.append((r[1] - p[1]) / 1e3)
                als.append(r[2] - p[2])
                cats.append(r[3])
        if len(ds) >= 3:
            s = sorted(ds)
            med = _st.median(ds)
            print(f"{path.stem:<8} {len(ds):>5} {med:>10.0f} {s[len(s)//4]:>7.0f} "
                  f"{s[3*len(s)//4]:>7.0f} {med*1e3/max(1,_st.median(cats)):>8.0f} "
                  f"{_st.median(als):>7.0f}")
            if path.stem.endswith(("l", "q", "u")) and path.stem != "K1000q":
                law.append((_st.median(cats), med))
    if len(law) >= 3:
        law.sort()
        print("  -> capture pin vs window candidates (the floor term of the fence):")
        for c, k in law:
            print(f"     cat={c:6.0f}  {k:8.0f} kB/scan  {k*1e3/c:6.0f} B/entry")
        lin = slope([c for c, _ in law], [k for _, k in law])
        if lin:
            b, r2 = lin
            print(f"     linear fit: pin = {b*1e3:.0f} B x candidates  (r2 {r2:.3f})")


def _round(x):
    return x


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).parent / "flights")
    main(d)
    phase_windows(d)
    transition_pins(d)
