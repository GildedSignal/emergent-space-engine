#!/usr/bin/env python3
"""Secular-shadow twin: the checker's named gold experiment for run 20261007-1032-taleb-ab03.

Question (check.md): propagate the SAME birth state under the averaged field alone and measure
the residual scar bits vs the full run at 5 and 20 yr, belt proper + resonant minority
separately. Decides whether belt H_live is ~0 (program absorbs; 8 GB safe) or ~100 bits
(irreducible; the belt needs a secular program in the store).

Twin = the exact double-averaged field of the Giant (an eccentric ring: the time-average of its
instantaneous Newtonian acceleration over uniform mean longitude = the field the law's
orbit-averaged kick layer carries), on a (r, phi) table (256-node trapezoid, 1080x2048 bilinear)
applied by the SAME drift-kick integrator, SAME one-orbit windows, SAME floors as hlive_probe2.
Birth states are drawn with the identical rng consumption (all 69,632 bodies), then sliced to
the belt, so the full-field belt columns regenerate the shipped record exactly.

Domain (pre-registered): double-averaging is valid only for non-crossing orbits. Secular domain
= belt bodies with birth apocenter Q0 = a0(1+e0) < 4.64 AU (0.05 AU below the Giant's pericentre
4.69). Crossing bodies (Q0 >= 4.64) are the encounter regime: counted separately, no twin claim.

Companions for interpreting the twin's residual:
  (B) full field, window = the body's synodic period (2*pi/|n - nJ|): is the E/L column
      leftover synodic oscillation (deterministic machinery: f(birth, shared ephemeris, t))
      rather than secular drift?
  (C) clone test: birth lambda0 + 2*pi/2^32 (the tube's u32 quantum) and a0 + 1e-9 AU on an
      8,192-body subset; divergence of the full-run mean columns = the birth->now map's
      sensitivity at store resolution (smooth => recompute-from-birth viable; amplified =>
      the birth program must evaluate extra precision).
  (N) twin-noise controls: ring at dt/2 and a 128-node table: the twin's own numerical floor,
      so residual bits are read against it; variance-explained is the scale-free version.
"""
import numpy as np, json, time, os

TAU = 2 * np.pi
GM = 4 * np.pi ** 2
MU = 2.0 ** -10
AJ, EJ = 4.94, 0.05
NJ = np.sqrt(GM * (1 + MU) / AJ ** 3)

rng = np.random.default_rng(20261007)
N_BELT, N_CROSS = 65536, 4096
N = N_BELT + N_CROSS

a0 = np.concatenate([2.0 + 1.5 * rng.random(N_BELT), 5.5 + 1.0 * rng.random(N_CROSS)])
e0 = np.clip(np.sqrt(-2 * 0.1 ** 2 * np.log(1 - rng.random(N))), 1e-6, 0.45)
w0 = rng.random(N) * TAU
lam0 = rng.random(N) * TAU
n0 = np.sqrt(GM / a0 ** 3)

A0, E0, W0, L0, N0 = a0[:N_BELT], e0[:N_BELT], w0[:N_BELT], lam0[:N_BELT], n0[:N_BELT]
NB = N_BELT
SEC = A0 * (1 + E0) < 4.64          # secular domain: orbit does not cross the Giant's annulus
CROSS = ~SEC

qE = 2.0 ** 48 / abs(GM / 4.0 - GM / 7.0)
qL = 2.0 ** 32 / (np.sqrt(GM * A0 * (1 - E0 ** 2)).max() - np.sqrt(GM * A0 * (1 - E0 ** 2)).min())
qW = 2.0 ** 32 / TAU

def kepler_E(M, e):
    E = M + e * np.sin(M)
    for _ in range(8):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E

def elem_to_cart(a, e, w, lam):
    n = np.sqrt(GM / a ** 3)
    E = kepler_E((lam - w) % TAU, e)
    c, s = np.cos(E), np.sin(E)
    den = 1 - e * c
    xo, yo = a * (c - e), a * np.sqrt(1 - e * e) * s
    vxo, vyo = -a * n * s / den, a * n * np.sqrt(1 - e * e) * c / den
    cw, sw = np.cos(w), np.sin(w)
    return (cw * xo - sw * yo, sw * xo + cw * yo, cw * vxo - sw * vyo, sw * vxo + cw * vyo)

def cart_to_elem(x, y, vx, vy):
    r = np.hypot(x, y); v2 = vx * vx + vy * vy; rv = x * vx + y * vy
    a = 1.0 / np.maximum(2.0 / r - v2 / GM, 1e-12)
    ex = (v2 / GM - 1.0 / r) * x - (rv / GM) * vx
    ey = (v2 / GM - 1.0 / r) * y - (rv / GM) * vy
    e = np.clip(np.hypot(ex, ey), 1e-9, None)
    w = np.arctan2(ey, ex)
    E = np.arctan2(np.clip(rv / (e * np.sqrt(GM * a)), -1, 1),
                   np.clip((1 - r / a) / e, -1, 1))
    lam = w + E - e * np.sin(E)
    return a, e, w, lam % TAU

def giant_xy(t):
    gx, gy, _, _ = elem_to_cart(np.array([AJ]), np.array([EJ]), np.array([0.7]),
                                np.array([(0.3 + NJ * t) % TAU]))
    return gx[0], gy[0]

# ---------------- averaged (ring) field table ----------------
R_MIN, R_MAX, NR, NPHI, NNODE = 1.0, 5.3, 1080, 2048, 256
RS = np.linspace(R_MIN, R_MAX, NR)
DR = RS[1] - RS[0]
DPHI = TAU / NPHI
NEAR_BAND = 4.55          # quadrature accuracy is reported for r < NEAR_BAND (secular domain)

def build_ring_table(nodes):
    """Time-average of the Giant's direct acceleration over uniform mean longitude."""
    lamJ = np.arange(nodes) * TAU / nodes
    gx, gy, _, _ = elem_to_cart(np.full(nodes, AJ), np.full(nodes, EJ),
                                np.full(nodes, 0.7), lamJ)
    phis = np.arange(NPHI) * TAU / NPHI
    CX, CY = np.cos(phis), np.sin(phis)
    wgt = 1.0 / nodes
    AX = np.zeros((NR, NPHI)); AY = np.zeros((NR, NPHI))
    for k in range(nodes):
        dxk = gx[k] - RS[:, None] * CX[None, :]
        dyk = gy[k] - RS[:, None] * CY[None, :]
        d3 = (dxk * dxk + dyk * dyk) ** 1.5
        AX += dxk / d3 * wgt
        AY += dyk / d3 * wgt
    return AX, AY

t0 = time.time()
AX, AY = build_ring_table(NNODE)
AXc, AYc = build_ring_table(128)
band = RS < NEAR_BAND
CONV = float(max(np.abs(AX - AXc)[band].max(), np.abs(AY - AYc)[band].max())
             / max(np.abs(AX)[band].max(), np.abs(AY)[band].max()))
print(f"[{time.time()-t0:6.1f}s] ring tables built; quadrature conv 256-vs-128 rel (r<{NEAR_BAND}) {CONV:.2e}")

def ring_accel(x, y, AX_=AX, AY_=AY):
    """bilinear interpolation of the averaged acceleration (per unit GM*mu)."""
    r = np.hypot(x, y)
    ir = np.clip((r - R_MIN) / DR, 0, NR - 1.000001)
    i0 = ir.astype(np.int64); i1 = np.minimum(i0 + 1, NR - 1); fr = ir - i0
    ip = (np.arctan2(y, x) % TAU) / DPHI
    j0 = ip.astype(np.int64) % NPHI; j1 = (j0 + 1) % NPHI; fp = ip - ip.astype(np.int64)
    def bil(T):
        return (T[i0, j0] * (1 - fr) * (1 - fp) + T[i1, j0] * fr * (1 - fp)
                + T[i0, j1] * (1 - fr) * fp + T[i1, j1] * fr * fp)
    return bil(AX_), bil(AY_)

# ---------------- integrator (same structure as hlive_probe2.run, belt only) ----------------
def run(a_, e_, w_, lam_, field, dt, T, epochs, window, AX_=AX, AY_=AY, mask=None):
    a, e, w, lam = a_.copy(), e_.copy(), w_.copy(), lam_.copy()
    n_b = np.sqrt(GM / a ** 3)
    Pw = (TAU / np.abs(n_b - NJ)) if window == "syn" else (TAU / n_b)
    hyper = np.zeros(NB, bool)
    acc = {t_: dict(sa=np.zeros(NB), saa=np.zeros(NB), se=np.zeros(NB), see=np.zeros(NB),
                    cw=np.zeros(NB, complex), cl=np.zeros(NB, complex), cnt=np.zeros(NB))
           for t_ in epochs}
    if mask is None:
        mask = np.ones(NB, bool)
    steps, t = int(round(T / dt)), 0.0
    for _ in range(steps):
        lam = lam + np.sqrt(GM / np.maximum(a, 1e-6) ** 3) * dt
        x, y, vx, vy = elem_to_cart(a, e, w, lam)
        if field == "full":
            gx, gy = giant_xy(t + 0.5 * dt)
            dx, dy = gx - x, gy - y
            d = np.hypot(dx, dy)
            rJ = np.hypot(gx, gy)
            k = GM * MU * dt
            vx = vx + k * (dx / d ** 3 - gx / rJ ** 3)
            vy = vy + k * (dy / d ** 3 - gy / rJ ** 3)
        elif field == "ring":
            axr, ayr = ring_accel(x, y, AX_, AY_)
            vx = vx + np.where(mask, GM * MU * dt * axr, 0.0)
            vy = vy + np.where(mask, GM * MU * dt * ayr, 0.0)
        na, ne, nw, nlam = cart_to_elem(x, y, vx, vy)
        a, e, w, lam = na, ne, nw, nlam
        hyper |= (a <= 0) | (e > 0.99) | ~np.isfinite(a) | ~np.isfinite(e)
        t += dt
        for t_ in acc:
            m = (~hyper) & mask & (t <= t_) & (t >= t_ - Pw)
            if m.any():
                A = acc[t_]
                A["sa"] += np.where(m, a, 0); A["saa"] += np.where(m, a * a, 0)
                A["se"] += np.where(m, e, 0); A["see"] += np.where(m, e * e, 0)
                A["cw"] += np.where(m, np.exp(1j * (w - W0)), 0)
                A["cl"] += np.where(m, np.exp(1j * (lam - L0 - N0 * t)), 0)
                A["cnt"] += m
    out = {}
    for t_, A in acc.items():
        c = np.maximum(A["cnt"], 1)
        ma = A["sa"] / c
        var = np.maximum(A["saa"] / c - ma * ma, 0)
        out[t_] = dict(t=t_, ma=ma, me=A["se"] / c, msd_a=np.sqrt(var),
                       mdw=np.angle(A["cw"] / c), mdl=np.angle(A["cl"] / c),
                       cover=A["cnt"] / (Pw / dt), cnt=A["cnt"], hyper=hyper)
    return out

def bits(dq, lsb, width):
    q = np.abs(dq) / lsb
    return np.where(q >= 1, 1 + np.log2(np.clip(q, 1, 2.0 ** width)), 0.0)

WIDTH = dict(E=48, L=32, w=32, M=32)

def cols_of(s):
    dE = -GM / (2 * s["ma"]) + GM / (2 * A0)
    dL = np.sqrt(GM * s["ma"] * (1 - s["me"] ** 2)) - np.sqrt(GM * A0 * (1 - E0 ** 2))
    return dict(E=dE, L=dL, w=s["mdw"].copy(), M=s["mdl"].copy())

CTRL = run(A0, E0, W0, L0, "none", 0.0625, 1.2, [1.0], "orbit")[1.0]
ctrl_dE = -GM / (2 * CTRL["ma"]) + GM / (2 * A0)
ctrl_dL = np.sqrt(GM * CTRL["ma"] * (1 - CTRL["me"] ** 2)) - np.sqrt(GM * A0 * (1 - E0 ** 2))
floor = dict(
    E=max(1 / qE, 2 * np.abs(ctrl_dE).max()),
    L=max(1 / qL, 2 * np.abs(ctrl_dL).max()),
    w=max(1 / qW, 2 * np.abs(CTRL["mdw"]).max()),
    M=max(1 / qW, 2 * np.abs(CTRL["mdl"]).max()))
print(f"[{time.time()-t0:6.1f}s] mu=0 control done; belt n={NB}, secular={int(SEC.sum())}, crossing={int(CROSS.sum())}")

EP = [1.0, 5.0, 20.0]
FULL = run(A0, E0, W0, L0, "full", 0.0625, 20.0, EP, "orbit")
print(f"[{time.time()-t0:6.1f}s] full/orbit done")
SYN = run(A0, E0, W0, L0, "full", 0.0625, 20.0, EP, "syn")
print(f"[{time.time()-t0:6.1f}s] full/synodic-window done")
RING = run(A0, E0, W0, L0, "ring", 0.0625, 20.0, EP, "orbit", mask=SEC)
print(f"[{time.time()-t0:6.1f}s] ring/orbit (secular twin) done")
RING2 = run(A0, E0, W0, L0, "ring", 0.03125, 20.0, [20.0], "orbit", mask=SEC)
print(f"[{time.time()-t0:6.1f}s] ring dt/2 noise control done")
RINGQ = run(A0, E0, W0, L0, "ring", 0.0625, 20.0, [20.0], "orbit", AX_=AXc, AY_=AYc, mask=SEC)
print(f"[{time.time()-t0:6.1f}s] ring 128-node quadrature noise control done")

# clone tests on the full field (all belt bodies; sensitivity is a property of the map)
NS = 8192
sel = np.random.default_rng(7).choice(NB, NS, replace=False)
dlam = TAU / 2.0 ** 32                    # the tube's u32 angle quantum
L0p = L0.copy(); L0p[sel] += dlam
CL = run(A0, E0, W0, L0p, "full", 0.0625, 20.0, EP, "orbit")
print(f"[{time.time()-t0:6.1f}s] clone dlambda done")
A0p = A0.copy(); A0p[sel] += 1e-9
CA = run(A0p, E0, W0, L0, "full", 0.0625, 20.0, EP, "orbit")
print(f"[{time.time()-t0:6.1f}s] clone da done")

RES = np.array([2.501, 2.824, 2.958, 3.117])
rd = np.abs(A0[:, None] - RES[None, :]).min(1)
resmask = rd < 0.05

def bitsrow(dc, sub=None):
    idx = slice(None) if sub is None else sub
    return {k: bits(dc[k][idx], floor[k], WIDTH[k]) for k in dc}

def stats(b, hyper=None):
    tot = b["E"] + b["L"] + b["w"] + b["M"]
    if hyper is not None:
        tot = np.where(hyper, 144.0, tot)
    return dict(mean=float(tot.mean()), p50=float(np.median(tot)),
                p99=float(np.percentile(tot, 99)), max=float(tot.max()),
                col={k: float(v.mean()) for k, v in b.items()})

def varexpl(d_resid, d_full, sub):
    return {k: float(1.0 - np.var(d_resid[k][sub]) / np.var(d_full[k][sub])) for k in d_resid}

rows = {}
for t_ in EP:
    f, s, g, cl, ca = FULL[t_], SYN[t_], RING[t_], CL[t_], CA[t_]
    cf, cs, cg = cols_of(f), cols_of(s), cols_of(g)
    ccl, cca = cols_of(cl), cols_of(ca)
    b_frozen = bitsrow(cf)                       # regeneration: frozen-program bits (belt, sec)
    b_res = bitsrow({k: cf[k] - cg[k] for k in cf})      # (A) full - secular twin
    b_twin = bitsrow(cg)                         # twin's own scar vs birth program
    b_syn = bitsrow(cs)                          # (B) synodic window vs birth
    b_cl = bitsrow({k: ccl[k] - cf[k] for k in cf}, sel)  # (C) clone divergence
    b_ca = bitsrow({k: cca[k] - cf[k] for k in cf}, sel)
    proper = SEC & ~resmask & ~f["hyper"]
    resonant = SEC & resmask & ~f["hyper"]
    alive = SEC & ~f["hyper"]
    rows[t_] = dict(
        cover_orbit=float(f["cover"][SEC].mean()), cover_syn=float(s["cover"][SEC].mean()),
        belt_hyper_sec=int((f["hyper"] & SEC).sum()), belt_cross=int(CROSS.sum()),
        frozen=stats(b_frozen, f["hyper"]), resid_full_minus_twin=stats(bitsrow({k: cf[k] - cg[k] for k in cf}, alive)),
        twin_vs_birth=stats(bitsrow(cg, alive)), synwin_vs_birth=stats(bitsrow(cs, alive)),
        var_explained=varexpl({k: cf[k] - cg[k] for k in cf}, cf, alive),
        clone_dlam=stats(b_cl), clone_da=stats(b_ca),
        clone_dlam_col={k: float(v.mean()) for k, v in b_cl.items()},
        clone_da_col={k: float(v.mean()) for k, v in b_ca.items()},
        proper=dict(n=int(proper.sum()), frozen=stats(bitsrow(cf, proper)),
                    resid=stats(bitsrow({k: cf[k] - cg[k] for k in cf}, proper)),
                    synwin=stats(bitsrow(cs, proper)),
                    clone_dlam=stats({k: v[proper[sel]] for k, v in b_cl.items()})),
        resonant=dict(n=int(resonant.sum()), frozen=stats(bitsrow(cf, resonant)),
                      resid=stats(bitsrow({k: cf[k] - cg[k] for k in cf}, resonant)),
                      synwin=stats(bitsrow(cs, resonant)),
                      clone_dlam=stats({k: v[resonant[sel]] for k, v in b_cl.items()})))

# twin-noise rows at 20 yr (secular domain only)
g2, gq, cg0 = cols_of(RING2[20.0]), cols_of(RINGQ[20.0]), cols_of(RING[20.0])
noise = dict(
    dt_half_col={k: float(v.mean()) for k, v in bitsrow({k: cg0[k] - g2[k] for k in cg0}, SEC).items()},
    quad128_col={k: float(v.mean()) for k, v in bitsrow({k: cg0[k] - gq[k] for k in cg0}, SEC).items()})

rep = dict(floor_rel=dict(E=floor["E"] * qE, L=floor["L"] * qL, w=floor["w"] * qW, M=floor["M"] * qW),
           table=dict(NR=NR, NPHI=NPHI, nodes=NNODE, conv_rel_band=CONV, band=NEAR_BAND),
           n_belt=NB, n_sec=int(SEC.sum()), n_cross=int(CROSS.sum()),
           dlam=dlam, da=1e-9, twin_noise_20yr=noise, wall_s=time.time() - t0, rows=rows)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "twin.json")
with open(out, "w") as fh:
    json.dump(rep, fh, indent=1, default=float)

for t_ in EP:
    r = rows[t_]
    print(f"\n== t={t_}yr  cover orbit {r['cover_orbit']:.2f} syn {r['cover_syn']:.2f} hyper(sec) {r['belt_hyper_sec']}")
    for nm in ("frozen", "resid_full_minus_twin", "twin_vs_birth", "synwin_vs_birth"):
        s = r[nm]
        print(f"  {nm:22s} mean {s['mean']:7.2f} p50 {s['p50']:7.2f} p99 {s['p99']:7.2f} "
              f"max {s['max']:7.1f} cols {({k: round(v,1) for k,v in s['col'].items()})}")
    print(f"  var explained by twin  {({k: round(v,3) for k,v in r['var_explained'].items()})}")
    print(f"  clone dlambda        mean {r['clone_dlam']['mean']:7.3f} p99 {r['clone_dlam']['p99']:7.2f} cols {({k: round(v,2) for k,v in r['clone_dlam_col'].items()})}")
    print(f"  clone da=1e-9AU      mean {r['clone_da']['mean']:7.3f} p99 {r['clone_da']['p99']:7.2f} cols {({k: round(v,2) for k,v in r['clone_da_col'].items()})}")
    rr, pp = r["resonant"], r["proper"]
    print(f"  sec-resonant (n={rr['n']}): frozen {rr['frozen']['mean']:.1f} resid {rr['resid']['mean']:.1f} "
          f"synwin {rr['synwin']['mean']:.1f} clone {rr['clone_dlam']['mean']:.2f}")
    print(f"  sec-proper   (n={pp['n']}): frozen {pp['frozen']['mean']:.1f} resid {pp['resid']['mean']:.1f} "
          f"synwin {pp['synwin']['mean']:.1f} clone {pp['clone_dlam']['mean']:.2f}")
print(f"\ntwin noise @20yr cols: dt/2 {({k: round(v,2) for k,v in noise['dt_half_col'].items()})}, "
      f"quad128 {({k: round(v,2) for k,v in noise['quad128_col'].items()})}")
print(f"wall {time.time()-t0:.1f}s")
