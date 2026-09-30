"""Aggregate belts.json + scaling.json into metrics.json and picture.svg."""
import json
import numpy as np

CONFIGS = ["element-sort", "shear-grid", "oracle", "ring-cells"]

def main():
    belts = json.load(open('belts.json'))
    sc = json.load(open('scaling.json'))
    metrics = {}
    for cfg in CONFIGS:
        missed = sum(b[cfg]['missed'] for b in belts)
        false = sum(b[cfg]['false'] for b in belts)
        ref = sum(b['ref_encounters'] for b in belts)
        wpe = float(np.median([b[cfg]['events'] / b['ref_encounters'] for b in belts]))
        epbo = float(np.median([b[cfg]['events'] / (b['N'] * 20.0) for b in belts]))
        metrics[cfg] = {
            "missed_fraction": missed / ref,
            "false_fraction": false / ref,
            "work_per_encounter": wpe,
            "events_per_body_orbit": epbo,
            "scale_exponent": sc['scale_exponent'][cfg],
        }
    with open('metrics.json', 'w') as f:
        json.dump(metrics, f, indent=1)
    print(json.dumps(metrics, indent=1))

    # ---------------- picture: work per orbit vs true encounter rate per orbit
    W, H, M = 760, 560, 70
    xs = np.array([b['rate'] for b in belts])
    allpts = []
    for ci, cfg in enumerate(CONFIGS):
        ys = np.array([b[cfg]['events'] / (b['N'] * 20.0) for b in belts])
        allpts.append((xs, ys))
    lo = min(min(x) for x, _ in allpts) / 3
    hi = max(max(x) for x, _ in allpts) * 3
    loy = min(min(y) for _, y in allpts) / 3
    hiy = max(max(y) for _, y in allpts) * 3
    lo = min(lo, loy); hi = max(hi, hiy); loy, hiy = lo, hi
    def px(x): return M + (np.log10(x) - np.log10(lo)) / (np.log10(hi) - np.log10(lo)) * (W - 2 * M)
    def py(y): return H - M - (np.log10(y) - np.log10(loy)) / (np.log10(hiy) - np.log10(loy)) * (H - 2 * M)
    cols = {"element-sort": "#1f77b4", "shear-grid": "#d62728", "oracle": "#2ca02c", "ring-cells": "#7f7f7f"}
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Helvetica,Arial,sans-serif">']
    s.append(f'<rect width="{W}" height="{H}" fill="white"/>')
    # grid + ticks
    for dec in range(int(np.floor(np.log10(lo))), int(np.ceil(np.log10(hi))) + 1):
        for m in (1, 2, 5):
            v = m * 10 ** dec
            if not (lo <= v <= hi):
                continue
            X = px(v)
            s.append(f'<line x1="{X:.1f}" y1="{M}" x2="{X:.1f}" y2="{H-M}" stroke="#e8e8e8" stroke-width="1"/>')
            s.append(f'<line x1="{M}" y1="{py(v):.1f}" x2="{W-M}" y2="{py(v):.1f}" stroke="#e8e8e8" stroke-width="1"/>')
            if m == 1:
                s.append(f'<text x="{X:.1f}" y="{H-M+18}" font-size="12" text-anchor="middle" fill="#444">1e{dec}</text>')
                s.append(f'<text x="{M-10}" y="{py(v)+4:.1f}" font-size="12" text-anchor="end" fill="#444">1e{dec}</text>')
    s.append(f'<line x1="{M}" y1="{H-M}" x2="{W-M}" y2="{M}" stroke="#999" stroke-dasharray="6,5" stroke-width="1.5"/>')
    s.append(f'<text x="{px(np.sqrt(lo*hi)):.0f}" y="{py(np.sqrt(lo*hi))+22:.0f}" font-size="12" fill="#666" transform="rotate(-34 {px(np.sqrt(lo*hi)):.0f} {py(np.sqrt(lo*hi))+22:.0f})">y = x (work = encounters)</text>')
    for cfg, (xs, ys) in zip(CONFIGS, allpts):
        c = cols[cfg]
        for x, y in zip(xs, ys):
            s.append(f'<circle cx="{px(x):.1f}" cy="{py(y):.1f}" r="4" fill="{c}" fill-opacity="0.75"/>')
    s.append(f'<line x1="{M}" y1="{H-M}" x2="{W-M}" y2="{H-M}" stroke="black"/>')
    s.append(f'<line x1="{M}" y1="{M}" x2="{M}" y2="{H-M}" stroke="black"/>')
    s.append(f'<text x="{W/2}" y="{H-18}" font-size="14" text-anchor="middle">true encounter rate per body per orbit</text>')
    s.append(f'<text x="24" y="{H/2}" font-size="14" text-anchor="middle" transform="rotate(-90 24 {H/2})">work per body per orbit (events)</text>')
    lx = M + 12
    for cfg in CONFIGS:
        s.append(f'<circle cx="{lx}" cy="{M-22}" r="5" fill="{cols[cfg]}"/>')
        s.append(f'<text x="{lx+10}" y="{M-18}" font-size="13">{cfg}</text>')
        lx += 20 + 9 * len(cfg)
    s.append(f'<text x="{W-M}" y="{H-M-8}" font-size="11" text-anchor="end" fill="#888">16 belts, N=1e4, 20 periods each</text>')
    s.append('</svg>')
    open('picture.svg', 'w').write('\n'.join(s))
    print("picture.svg written")

if __name__ == '__main__':
    main()
