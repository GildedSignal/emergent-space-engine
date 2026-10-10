#!/usr/bin/env python3
"""The memory curve: a B12 statistic that separates state-only error from memory.

Lab run 20261010-1947-quant-9c2f. Input: the law's own per-sample observables dumped by
xtask's ignored `dump_b12_streams` test (no reference integration is read here). Ten f64
columns per row: t, x, y, vx, vy, C_J, a, n_enc, d_RH, judged.

The instrument: pairs of samples matched in the state coordinate a (semimajor axis) at
increasing encounter separations. |e(t2) - e(t1)| extrapolated to zero a-separation is the
memory estimate M(dn). An error that is a function of the current state returns the same
value at the same a: M flat. A walk in the encounter count does not: M rises as sqrt(dn).
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
STREAMS = HERE / "streams"
SAMPLES = 1601
COLS = 10
HILL_OVER_SEP = (1e-3 / 3.0) ** (1.0 / 3.0)  # R_H/sep of the JUPITER scene
BOUNCED = 1e-7 / HILL_OVER_SEP  # the plant's coefficient, in relative-C_J units per sep

# --------------------------------------------------------------------------------------
# deterministic integer randomness (SplitMix64), so every number here regenerates anywhere
class Rng:
    MASK = np.uint64(0xFFFFFFFFFFFFFFFF)

    def __init__(self, seed: int):
        self.s = np.uint64(seed)

    def next(self) -> int:
        self.s = np.uint64((self.s + np.uint64(0x9E3779B97F4A7C15)) & Rng.MASK)
        z = self.s
        z = np.uint64((z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)) & Rng.MASK
        z = np.uint64((z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)) & Rng.MASK
        return int(z ^ (z >> np.uint64(31)))

    def unit(self) -> float:
        return (self.next() >> 11) * 2.0**-53


def load(name: str, judged_only: bool = True) -> list[dict]:
    raw = np.fromfile(STREAMS / f"{name}.f64", dtype="<f8")
    assert raw.size % (COLS * SAMPLES) == 0, f"{name}: {raw.size}"
    ships = raw.reshape(-1, SAMPLES, COLS)
    out = []
    for s in ships:
        if judged_only and s[0, 9] < 0.5:
            continue
        cj0 = s[0, 5]
        out.append(
            {
                "t": s[:, 0],
                "cj": s[:, 5],
                "e": (s[:, 5] - cj0) / abs(cj0),
                "a": s[:, 6],
                "n": s[:, 7],
                "d": s[:, 8],
            }
        )
    return out


# --------------------------------------------------------------------------------------
# the memory curve
DN_BINS = [(1, 2), (2, 4), (4, 8), (8, 16), (16, 32), (32, 64), (64, 1 << 20)]
SUBS = 8
MIN_PAIRS = 60


def ship_curve(ship: dict) -> list[tuple[float, int, float]]:
    """(dn_center, pairs, M) per encounter-separation bin; M = median |de| extrapolated to da=0."""
    e, a, n = ship["e"], ship["a"], ship["n"]
    i, j = np.triu_indices(len(e), k=1)
    dn = n[j] - n[i]
    keep = dn > 0
    i, j, dn = i[keep], j[keep], dn[keep]
    da = np.abs(a[j] - a[i])
    de = np.abs(e[j] - e[i])
    rows = []
    for lo, hi in DN_BINS:
        m = (dn >= lo) & (dn < hi)
        if m.sum() < MIN_PAIRS:
            continue
        da_m, de_m, dn_m = da[m], de[m], dn[m]
        order = np.argsort(da_m)
        da_s, de_s = da_m[order], de_m[order]
        cuts = np.linspace(0, len(da_s), SUBS + 1).astype(int)
        xs, ys = [], []
        for k in range(SUBS):
            seg_a, seg_e = da_s[cuts[k] : cuts[k + 1]], de_s[cuts[k] : cuts[k + 1]]
            xs.append(float(np.median(seg_a)))
            ys.append(float(np.median(seg_e)))
        xs, ys = np.array(xs), np.array(ys)
        A = np.vstack([np.ones_like(xs), xs]).T
        coef, *_ = np.linalg.lstsq(A, ys, rcond=None)
        rows.append((float(np.median(dn_m)), int(m.sum()), max(float(coef[0]), 0.0)))
    return rows


def law_curve(ships: list[dict]) -> list[tuple[float, int, float]]:
    """Per-bin median across ships of the per-bin M (bins unioned by nearest center)."""
    per = {}
    for ship in ships:
        for center, pairs, mem in ship_curve(ship):
            per.setdefault(round(center), []).append(mem)
    out = []
    for center in sorted(per):
        out.append((float(center), len(per[center]), float(np.median(per[center]))))
    return out


def slope(curve: list[tuple[float, int, float]]) -> float:
    pts = [(np.log(c), np.log(m)) for c, _, m in curve if m > 0]
    if len(pts) < 3:
        return float("nan")
    x, y = zip(*pts)
    return float(np.polyfit(x, y, 1)[0])


def flag(curve) -> str:
    """Verdict with the thresholds pre-registered in predictions.md (no fitting)."""
    s = slope(curve)
    if not np.isfinite(s):
        return "no-data"
    top = max(m for _, _, m in curve)
    bot = min(m for _, _, m in curve if m > 0)
    growth = top / bot if bot > 0 else float("inf")
    if s >= 0.25 and growth >= 2:
        return "LEAK"
    if s <= 0.15:
        return "state-only"
    return f"grey (slope {s:.3f}, growth {growth:.1f})"


# --------------------------------------------------------------------------------------
# the classic alternative: variance ratio on the error levels (unit-root view)
def vr(ship: dict, k: int) -> float:
    e = ship["e"]
    var1 = np.var(e[1:] - e[:-1], ddof=1)
    if var1 <= 0:
        return float("nan")
    vark = np.var(e[k:] - e[:-k], ddof=1)
    return float(vark / (k * var1))


# --------------------------------------------------------------------------------------
# synthetic controls, added to echo's streams (the analysis never sees the reference)
def walk(stream: list[dict], delta: float, seed0: int) -> list[dict]:
    """A random walk in the encounter count, unit-variance uniform steps (the plant's rule)."""
    out = []
    for si, ship in enumerate(stream):
        rng = Rng(seed0 + 0x9E37 * si + 1)
        n = ship["n"].astype(int)
        steps = {k: (rng.unit() - 0.5) * np.sqrt(12.0) for k in range(1, int(n[-1]) + 1)}
        w, s = [], 0.0
        prev = 0
        for k in n:
            for q in range(prev, int(k)):  # encounters passed since the last sample
                s += steps.get(q + 1, 0.0)
            prev = int(k)
            w.append(s)
        out.append({**ship, "e": ship["e"] + delta * np.array(w)})
    return out


def ar1(stream: list[dict], phi: float, sigma: float, seed0: int) -> list[dict]:
    out = []
    for si, ship in enumerate(stream):
        rng = Rng(seed0 + 0x85EB * si + 1)
        x, acc = [], 0.0
        for _ in range(len(ship["e"])):
            acc = phi * acc + sigma * (rng.unit() - 0.5) * np.sqrt(12.0)
            x.append(acc)
        out.append({**ship, "e": ship["e"] + np.array(x)})
    return out


def state2d(stream: list[dict], coef: float) -> list[dict]:
    """A state-only error in two coordinates: a and the planet distance d (both dumped)."""
    out = []
    for ship in stream:
        a0, d0 = ship["a"][0], ship["d"][0]
        out.append({**ship, "e": ship["e"] + coef * ((ship["a"] - a0) + 0.5 * (ship["d"] - d0))})
    return out


# --------------------------------------------------------------------------------------
def main():
    echo = load("echo")
    bounded = load("planted-bounded")
    compound = load("planted-compound")
    n_med = float(np.median([s["n"][-1] for s in echo]))
    n_max = float(max(s["n"][-1] for s in echo))
    dstar = 1e-4 / np.sqrt(n_med)

    report = {"n_enc_med": n_med, "n_enc_max": n_max, "dstar": dstar, "laws": {}, "vr": {}, "ladder": []}

    print(f"encounters per ship: median {n_med:.0f}, max {n_max:.0f};  "
          f"requirement threshold delta* = 1e-4/sqrt(n_med) = {dstar:.3e}")
    print(f"{'stream':34} {'slope':>7} {'verdict':24} top M      curve (dn: M)")
    for name, ships in [
        ("echo", echo),
        ("planted-bounded", bounded),
        ("planted-compound", compound),
        ("leak 16 delta*", walk(echo, 16 * dstar, 0xA)),
        ("leak 4 delta*", walk(echo, 4 * dstar, 0xB)),
        ("leak delta* (requirement)", walk(echo, dstar, 0xC)),
        ("leak delta*/4", walk(echo, dstar / 4, 0xD)),
        ("AR(1) 0.9 sigma 1e-8", ar1(echo, 0.9, 1e-8, 0xE)),
        ("state-only a+d", state2d(echo, BOUNCED)),
        ("state-error + leak delta*", walk(state2d(echo, BOUNCED), dstar, 0x11)),
        ("state-error + leak delta*/4", walk(state2d(echo, BOUNCED), dstar / 4, 0xF)),
        ("state-error + leak delta*/16", walk(state2d(echo, BOUNCED), dstar / 16, 0x10)),
    ]:
        curve = law_curve(ships)
        s = slope(curve)
        top = max((m for _, _, m in curve), default=float("nan"))
        cres = " ".join(f"{c:.0f}:{m:.1e}" for c, _, m in curve)
        print(f"{name:34} {s:7.3f} {flag(curve):24} {top:.2e}   {cres}")
        report["laws"][name] = {"slope": s, "verdict": flag(curve), "curve": curve}
        report["vr"][name] = {
            k: float(np.median([vr(ship, k) for ship in ships])) for k in (8, 64, 512)
        }

    # P6: no convergence filter — all dumped ships, not just the judged ones
    for name in ("planted-bounded", "planted-compound"):
        allc = law_curve(load(name, judged_only=False))
        report[f"all16_{name}"] = {"slope": slope(allc), "verdict": flag(allc), "curve": allc}
        print(f"all-16 ships, {name:20} {slope(allc):7.3f} {flag(allc)}")

    print("\nvariance ratio VR(k) on error levels (medians):")
    for name, vals in report["vr"].items():
        print(f"  {name:34} " + "  ".join(f"k={k}: {v:.2f}" for k, v in vals.items()))

    (HERE / "memory_curve.json").write_text(json.dumps(report, indent=1, default=float))
    print("wrote memory_curve.json")


if __name__ == "__main__":
    main()
