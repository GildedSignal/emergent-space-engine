"""The reband loop on run -0458's belt scene, measured across memo widths.

The checker's gold experiment: run the reband loop itself (re-infer the population
program every k orbits), measure converged bytes/body and the un-reabsorbed residue
(H_live), with the SHIPPED emergent-shipmem codec pricing the scar layer.

Scale fact (measured below, predicted by -0458's prediction 4): at the crate's 12-bit
width the belt's joint key extent is ~5.7M cells, so any simulable N sits at occupancy
~1 (records are singletons; the loop has nothing to share). The 10^9 regime has
occupancy ~80-180. So the equilibrium is measured at coarser widths b in {5, 6} where
occupancy is 12-47 at N=16,384 originals, and the age-rescale law to b=12 is fitted
from the sweep (linear shear predicts split age scales as 2^(12-b)); the 12-bit anchor
is -0458's own twin arms (offsets +0.2/+0.05 crate quanta), tracked directly.

Instrument fixes vs -0458 (checker's findings):
  - keys at the crate's quantize semantics: truncation to b significant bits
    (2048 points/octave at b=12, 2x coarser than -0458's round(log2*2^12) grid);
  - billing on mean elements (boxcar 2 reference orbits), not osculating: kills the
    short-period jitter that made crossing rates checkpoint-density-dependent;
  - cadence check at matched end times.

Store model (Form P at the key width, faithful to law.md / the -0458 claim):
  - a record = one occupied key cell; members share it; the record's cell is updated
    each checkpoint to the members' median cell (the kick layer's common-mode update:
    "the population program and the kick layer are one mechanism");
  - a body is scarred iff its cell differs from its record's cell (rows priced by the
    shipped Program::seal_from: Elias-Fano ordinals + block-coded zigzag deltas);
  - reband every k orbits: regroup by current cell (re-infer), scars clear,
    cost O(occupied cells) writes;
  - static arms: frozen (record cell never updated) and tracked (common-mode updated,
    membership never regrouped) = the claim's saturating program.

Run:  python3 reband.py sim    -> decisive scene, all widths and cadences (~7 min)
      python3 reband.py zero   -> no-Jupiter control (loop noise floor)
      python3 reband.py weak   -> Jupiter/10 control (forcing scaling)
      python3 reband.py dtest2 -> matched-time cadence check
"""
import math
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "orig"))
import hlive_belt as H  # the run's own dynamics, unmodified

REF_ORBIT = 2 * np.pi * 2.7 ** 1.5 / np.sqrt(H.GM)  # 4.441 yr, -0458's orbit unit
CP_ORBITS = 0.25                                    # checkpoint spacing in orbits
SMOOTH_N = 8                                        # boxcar = 2 reference orbits
EMIN_S, EMIN_H = -4, -6                             # octave offsets for integer cell ids
N_ALL = 49152                                       # 3 arms x 16384 (H.belt, seed 7)
N_ORIG = N_ALL // 3                                 # originals arm: the population store
BIN = "/home/glmlab/lab-target-0/release/reband-price"

WIDTHS = [12, 10, 8, 6, 5]                          # memo bits per column
KS = [math.inf, "frozen", 200, 100, 50, 25, 10]     # cadences in orbits
LOG_EVERY = 25                                      # orbits between log rows


def cells(a, ecc, bits):
    """Crate memo-key cell ids (Scalar::quantize semantics) as monotone integers.

    scale = r_p = a(1-e), shape = (1-e)/(1+e); frexp is exact for floats; i_b =
    floor(m * 2^(b-1)) truncates to b significant bits (2^(b-1) points per octave).
    """
    lo = 1 << (bits - 1)
    stride = 1 << bits
    ms, es = np.frexp(a * (1.0 - ecc))
    mh, eh = np.frexp((1.0 - ecc) / (1.0 + ecc))
    i_s = (ms * lo).astype(np.int64)
    i_h = (mh * lo).astype(np.int64)
    return i_s + (es - EMIN_S) * stride, i_h + (eh - EMIN_H) * stride


def group_medians(gid, gid_order, val):
    """Per-group lower-median of val, evaluated for every body in gid_order order."""
    g = gid[gid_order]
    v = val[gid_order]
    bounds = np.flatnonzero(np.r_[True, g[1:] != g[:-1]])
    counts = np.diff(np.r_[bounds, g.size])
    med_pos = bounds + (counts - 1) // 2
    return v[med_pos][g]


class Store:
    """One Form-P store at one memo width: records, common-mode tracking, rebands."""

    def __init__(self, js, jh, mode):
        self.mode = mode  # reband cadence in orbits, or inf (tracked) or "frozen"
        self.rebands = 0
        self.writes = 0
        self.regroup(js, jh)

    def regroup(self, js, jh):
        key = js * (1 << 18) + jh
        self.gid = np.unique(key, return_inverse=True)[1]
        self.R = int(self.gid.max()) + 1
        self.rec_s, self.rec_h = js.copy(), jh.copy()
        self.rebands += 1
        self.writes += self.R

    def step(self, js, jh):
        """Common-mode update + scar readout. Returns (scarred, |d|, multi)."""
        if self.mode != "frozen":
            order = np.lexsort((js, self.gid))
            ginv = np.empty_like(order)
            ginv[order] = np.arange(order.size)
            self.rec_s = group_medians(self.gid, order, js)[ginv]
            self.rec_h = group_medians(self.gid, order, jh)[ginv]
        d = np.abs(js - self.rec_s) + np.abs(jh - self.rec_h)
        counts = np.bincount(self.gid, minlength=self.R)
        return d != 0, d, counts[self.gid] >= 2

    def maybe_reband(self, js, jh, orbits_since):
        if self.mode in (math.inf, "frozen"):
            return False
        if orbits_since >= self.mode - 1e-9:
            self.regroup(js, jh)
            return True
        return False


def simulate(T, steps_per_PJ, muj=H.MU_J, seed=7):
    """H.belt scene (3 arms); yields (orbit, originals' mean cells per width, twin splits)."""
    H.MU_J = muj
    rng = np.random.default_rng(seed)
    a0, e0, lam, varpi, m = H.belt(N_ALL, rng)
    s = H.state(a0, e0, lam, varpi)
    dt = H.PJ / steps_per_PJ
    nst = int(round(T / dt))
    cp_step = max(1, round(REF_ORBIT * CP_ORBITS / dt))
    ring_a = np.zeros((SMOOTH_N, N_ALL))
    ring_e = np.zeros((SMOOTH_N, N_ALL))
    ri = 0
    t = 0.0
    cp = 0
    for step in range(nst + 1):
        if step % cp_step == 0:
            a, e = H.elements(s[0], s[1], s[2], s[3])
            ring_a[ri], ring_e[ri] = a, e
            ri = (ri + 1) % SMOOTH_N
            filled = min(cp + 1, SMOOTH_N)
            ma, me = ring_a[:filled].mean(0), ring_e[:filled].mean(0)
            out = {b: cells(ma[:m], me[:m], b) for b in WIDTHS}
            # twin anchor at b=12: arms 2/3 sit at +0.4/+0.1 quanta of -0458's grid
            # = +0.2/+0.05 of the crate grid; split = cells no longer equal
            kA = out[12][0] * (1 << 18) + out[12][1]
            kB = cells(ma[m:2 * m], me[m:2 * m], 12)
            kC = cells(ma[2 * m:], me[2 * m:], 12)
            f4 = float((kB[0] * (1 << 18) + kB[1] != kA).mean())
            f1 = float((kC[0] * (1 << 18) + kC[1] != kA).mean())
            yield t / REF_ORBIT, out, (f4, f1)
            cp += 1
        if step == nst:
            break
        xj, yj = H.jup(t + dt / 2)
        s[0] += s[2] * dt / 2
        s[1] += s[3] * dt / 2
        ax, ay = H.accel(s[0], s[1], xj, yj)
        s[2] += ax * dt
        s[3] += ay * dt
        s[0] += s[2] * dt / 2
        s[1] += s[3] * dt / 2
        t += dt


def price(rows, n):
    """Shipped shipmem pricing of scar rows [(ordinal, ds, dh)] -> marginal bits."""
    if not rows:
        return 0.0, 0
    path = os.path.join(os.path.dirname(__file__), "scars.tmp")
    with open(path, "w") as f:
        for o, ds, dh in rows:
            f.write(f"{o} {ds} {dh}\n")
    out = subprocess.run([BIN, "price", str(n), path],
                         capture_output=True, text=True, check=True).stdout
    parts = dict(zip(out.split()[::2], out.split()[1::2]))
    return (int(parts["bytes"]) - 512) * 8.0, int(parts["scars"])


def main(tag, muj, T=2400.0, price_all=True):
    stores = {}       # (bits, k) -> Store
    last_orb = {}
    log = []          # rows every LOG_EVERY orbits
    samples = {}      # (bits, k) -> list of scar-row lists
    twins = []        # (orbit, split0.4, split0.1) at b=12
    for orb, out, (f4, f1) in simulate(T, 775, muj=muj):
        twins.append((orb, f4, f1))
        for b in WIDTHS:
            js, jh = out[b]
            for k in KS:
                key = (b, k)
                if key not in stores:
                    stores[key] = Store(js, jh, k)
                    last_orb[key] = 0.0
                st = stores[key]
                scarred, d, multi = st.step(js, jh)
                if st.maybe_reband(js, jh, orb - last_orb[key]):
                    last_orb[key] = orb
                if abs(orb % LOG_EVERY) < CP_ORBITS / 2:
                    row = log_row(log, orb, b, k)
                    row.update(f=float(scarred.mean()),
                               fm=float(scarred[multi].mean()) if multi.any() else 0.0,
                               med=float(np.median(d[scarred])) if scarred.any() else 0.0,
                               p90=float(np.percentile(d[scarred], 90)) if scarred.any() else 0.0,
                               R=st.R)
                # price scar sets near the end: rebanded ks at two cycle ages,
                # static arms once
                near_end = orb >= T / REF_ORBIT - 120
                want = (isinstance(k, (int, float)) and k != math.inf and near_end
                        and len(samples.get(key, [])) < 6
                        and (abs(orb % k - k / 2) <= 0.2 or abs(orb % k - (k - CP_ORBITS)) <= 0.2))
                want_static = (price_all and k in (math.inf, "frozen")
                               and orb >= T / REF_ORBIT - 30 and len(samples.get(key, [])) < 1)
                if price_all and (want or want_static):
                    idx = np.flatnonzero(scarred)
                    ds = js - st.rec_s
                    dh = jh - st.rec_h
                    samples.setdefault(key, []).append(
                        [(int(i), int(ds[i]), int(dh[i])) for i in idx])
    print(f"=== {tag}")
    print(f"{'b':>3} {'k':>6} {'occ':>5} {'f_scar':>7} {'f_mult':>7} {'med|d|':>6} "
          f"{'p90':>5} {'R':>6} {'scb/b':>6} {'rcb/b':>7} {'tot':>7} {'H_live':>8}")
    for b in WIDTHS:
        for k in KS:
            rows = [r for r in log if r["b"] == b and r["k"] == k and r["orb"] >= 430]
            if not rows:
                continue
            f = np.mean([r["f"] for r in rows])
            fm = np.mean([r["fm"] for r in rows])
            med = np.mean([r["med"] for r in rows])
            p90 = np.mean([r["p90"] for r in rows])
            R = int(np.mean([r["R"] for r in rows]))
            occ = N_ORIG / R
            name = k if k != math.inf else "inf"
            bits = [price(s, N_ORIG)[0] / N_ORIG for s in samples.get((b, k), [])]
            sb = float(np.mean(bits)) if bits else float("nan")
            rb = R * 32.0 / N_ORIG
            kk = k if isinstance(k, (int, float)) and k != math.inf else 541
            print(f"{b:3d} {str(name):>6} {occ:5.1f} {f:7.3f} {fm:7.3f} {med:6.1f} {p90:5.1f} "
                  f"{R:6d} {sb:6.2f} {rb:7.2f} {sb + rb:7.2f} {(sb + rb) / kk:8.4f}")
    print("--- twin anchor b=12 (orbit, split@+0.2q, split@+0.05q):")
    for orb, f4, f1 in twins:
        if abs(orb % 50) < CP_ORBITS / 2:
            print(f"  {orb:6.1f}  {f4:.3f}  {f1:.3f}")
    print("--- convergence trace b=6 (f per k in KS order):")
    for r in log:
        if r["b"] == 6 and abs(r["orb"] % 50) < CP_ORBITS / 2:
            same = [r2 for r2 in log if r2["b"] == 6 and r2["orb"] == r["orb"]]
            same.sort(key=lambda r2: KS.index(r2["k"]))
            print(f"  {r['orb']:6.1f}  " + "  ".join(f"{x['f']:.3f}" for x in same))


def log_row(log, orb, b, k):
    for r in log:
        if r["orb"] == orb and r["b"] == b and r["k"] == k:
            return r
    r = dict(orb=orb, b=b, k=k)
    log.append(r)
    return r

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "sim"
    if mode == "sim":
        main("decisive (MU_J=9.55e-4)", H.MU_J)
    elif mode == "zero":
        main("no-Jupiter control", 0.0, price_all=False)
    elif mode == "weak":
        main("Jupiter/10 control", H.MU_J / 10, price_all=False)
    elif mode == "dtest2":
        # matched-time cadence check on the mean-key instrument (fixed dtest)
        for spj in (775, 1550):
            birth = None
            off = []
            for orb, out, _ in simulate(120.0, spj):
                js, jh = out[12]
                if birth is None:
                    birth = js * (1 << 18) + jh
                if abs(orb % 24) < CP_ORBITS / 2:
                    off.append((orb, float((js * (1 << 18) + jh != birth).mean())))
            print(f"steps/PJ={spj}: " + "  ".join(f"{o:.0f}:{f:.3f}" for o, f in off))
