#!/usr/bin/env python3
"""H_live analysis, v2: differential entropies on the integer lattice (exact moments).

A kick's or a body's deviation value is an integer pair on a fine lattice (values essentially
never repeat), so the honest bits-per-value is the differential entropy of the empirical
distribution, log2(2*pi*e*sx*sy) bits (2-D, Gaussian-shaped bulk; checked against a coarse
exact histogram). Entropies of saturated unique-value counts are NOT entropy.
"""
import csv, json, lzma, math, sys
from collections import Counter, defaultdict

TICK_S = 4.925_490_947e-6
LOG2_2PIE = math.log2(2 * math.pi * math.e)

def load_kicks(run):
    files = [f"{run}-kicks2.csv.xz"]
    if not __import__("os").path.exists(files[0]):
        files = [f"{run}-kicks2a.csv.xz", f"{run}-kicks2b.csv.xz"]
    with lzma.open(files[0], "rt") as f:
        reader = csv.DictReader(f)
        rows, last_t = [], {}
        _consume(reader, rows, last_t)
    for fn in files[1:]:
        with lzma.open(fn, "rt") as f:
            _consume(csv.DictReader(f), rows, last_t)
    return rows

def _consume(reader, rows, last_t):
    for r in reader:
        b = int(r["body"])
        t = last_t.get(b, 0) + int(r["dtick"])
        last_t[b] = t
        rows.append((b, t, int(r["dvx"]), int(r["dvy"]), int(r["nexp"]),
                     int(r["carry0"]), int(r["carry1"])))

def load_states(run):
    with open(f"{run}-states.csv") as f:
        return [(int(r["sample"]), int(r["body"]), int(r["tick"]), int(r["events"]),
                 int(r["carry0"]), int(r["carry1"])) for r in csv.DictReader(f)]

def load_summary(run):
    import re
    txt = open(f"{run}-summary.txt").read()
    return dict(re.findall(r"(\w+)=(\S+)", txt))

def sigma(v):
    n = len(v)
    m = sum(v) / n
    return math.sqrt(sum((x - m) ** 2 for x in v) / n)

def diff_entropy(xs, ys):
    """Bits per value of an integer-lattice 2-D distribution (Gaussian-bulk estimate)."""
    return LOG2_2PIE + math.log2(sigma(xs)) + math.log2(sigma(ys))

def coarse_entropy(xs, ys, step):
    """Exact discrete entropy after lattice quantization at `step` (a control on the estimate)."""
    c = Counter((x // step, y // step) for x, y in zip(xs, ys))
    tot = sum(c.values())
    return -sum(k / tot * math.log2(k / tot) for k in c.values()) + 2 * math.log2(step)

def analyze(run):
    kicks = load_kicks(run)
    states = load_states(run)
    summ = load_summary(run)
    seconds = float(summ["game_s"])
    bodies = sorted({k[0] for k in kicks})
    n = len(bodies)
    E0 = min(k[4] for k in kicks)

    # ---- gross stream (per fired kick) --------------------------------------
    rate = len(kicks) / n / seconds
    dx = [k[2] << (k[4] - E0) for k in kicks]
    dy = [k[3] << (k[4] - E0) for k in kicks]
    h_dv = diff_entropy(dx, dy)
    h_dv_coarse = coarse_entropy(dx, dy, 1 << max(0, int(math.log2(sigma(dx))) - 3))
    mag = Counter(max(abs(a), abs(b)).bit_length() for a, b in zip(dx, dy))
    tot = sum(mag.values())
    h_mag = -sum(c / tot * math.log2(c / tot) for c in mag.values())
    # physical scale of one kick, in c (velocities are in doll units, c = 1)
    dv_c = sigma(dx) * 2.0 ** E0, sigma(dy) * 2.0 ** E0

    # ---- net deviation D_i(t) = sum dv (velocity quanta from the program) ----
    cum = defaultdict(lambda: [0, 0])
    net_at = defaultdict(dict)
    ki = 0
    for (sample, body, tick, events, c0, c1) in states:
        while ki < len(kicks) and kicks[ki][1] <= tick:
            b, _, a, b2, nexp, _, _ = kicks[ki]
            s = nexp - E0
            cum[b][0] += a << s
            cum[b][1] += b2 << s
            ki += 1
        net_at[sample][body] = tuple(cum[body])
    tick_of = {}
    carry_last = {}
    for (sample, body, tick, events, c0, c1) in states:
        tick_of[sample] = tick
        carry_last[body] = (c0, c1)
    series = []
    for sample in sorted(net_at):
        vals = list(net_at[sample].values())
        sx, sy = sigma([v[0] for v in vals]), sigma([v[1] for v in vals])
        zero = sum(1 for v in vals if v == (0, 0))
        series.append(dict(sample=sample, t_s=tick_of[sample] * TICK_S,
                           bits=round(LOG2_2PIE + math.log2(max(sx, 1)) + math.log2(max(sy, 1)), 2),
                           sigma_x=sx, sigma_y=sy, exact_zero=zero / len(vals)))
    first, last = series[2], series[-1]
    # growth of net bits with log time (random walk: +1 bit per doubling)
    slope = ((last["bits"] - first["bits"]) / (math.log2(last["t_s"]) - math.log2(first["t_s"]))
             if math.log2(last["t_s"]) != math.log2(first["t_s"]) else 0.0)

    cx = [v[0] for v in carry_last.values()]
    cy = [v[1] for v in carry_last.values()]
    h_carry = diff_entropy(cx, cy)

    return dict(
        run=run, n=n, seconds=seconds, fired_kicks=len(kicks),
        kick_rate_per_body_s=rate,
        h_dv_bits_per_kick=round(h_dv, 2), h_dv_coarse_control=round(h_dv_coarse, 2),
        h_dv_magnitude_bits=round(h_mag, 2),
        sigma_dv_in_c=[dv_c[0], dv_c[1]],
        gross_bits_per_body_s=rate * h_dv,
        gross_bits_s_at_1e9_bodies_GBps=rate * h_dv * 1e9 / 8 / 1e9,
        h_carry_bits=round(h_carry, 2),
        carry_range=[[min(cx), max(cx)], [min(cy), max(cy)]],
        net_series=[{**s, "sigma_x": round(s["sigma_x"], 1), "sigma_y": round(s["sigma_y"], 1)}
                    for s in series],
        net_bits_last=last["bits"], net_bits_growth_per_log2_t=round(slope, 3),
        exact_zero_last=last["exact_zero"],
        bytes_per_body_now=float(summ["bytes_per_body"]),
        stray_over_captured=(float(summ["stray_items"]) / max(1, float(summ["captured_items"]))),
        digest=summ.get("digest"),
    )

if __name__ == "__main__":
    for r in sys.argv[1:]:
        print(json.dumps(analyze(r)))
