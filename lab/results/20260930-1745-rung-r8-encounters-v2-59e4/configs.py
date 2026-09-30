"""The five configurations of rung r8 v2.

Every configuration reports encounters found and a count of events it
processes. Exact per-pair checks use the same Kepler machinery as the
reference, so a configuration that checks every candidate conjunction
(element-sort, hier-bounds) reproduces the truth list exactly.

Event accounting (favourable-to-config choices documented in the dossier):
- element-sort: one event per swap of kinetic-list neighbours; each
  candidate pair is counted once (dedup across bins); bin width = rho.
- shear-grid: events = cell changes. Radial path per orbit is exactly 4ae
  (Kepler), phi_shear path measured on the body's own sheared longitude
  (smoothed: bin-jump discontinuities not charged). Cells are rho x rho so
  that any pair within rho is in the same or an adjacent cell. Detection =
  a cell change of either body inside the d<rho interval, or the initial
  occupancy sweep.
- hier-bounds: events = group-pair certificates (+ renewals) + splits +
  member-pair interval tests + exact per-pair examinations. Overlapping
  group pairs are split once, then member-examined; an exact examination
  settles a pair for the whole run (Kepler elements never change).
- oracle (positive): reads the true list; cost = number of true encounters.
- ring-cells (negative): 128 rings x 16 spokes, checks occupants of the new
  cell only; detection = pair in the same fixed cell during the d<rho
  interval (a generous reading).
"""
import numpy as np
from belt import TWOPI, kepler_states, rel_state

T_MAX = [0.0]   # run duration of the current belt, set by the runner
def element_sort(ref):
    """Swaps = conjunctions of candidate pairs; checks are exact, done at
    the swap itself (no extra charge). Reports = the reference list."""
    return dict(events=int(ref["C"].sum()), detected=len(ref["encounters"][0]),
                missed=0, false=0)


def shear_grid_events(B, T, smp=256):
    """Cell changes with cells rho x rho in (r, phi - n_own t)."""
    orbits = T * B.n / TWOPI
    radial = 4.0 * B.a * B.e / B.rho * orbits
    # phi_shear path over one orbit, sampled
    idx = np.arange(B.N)
    ts = np.linspace(0.0, TWOPI / B.n, smp)   # one orbit, per body
    path = np.zeros(B.N)
    x_prev = y_prev = None
    for k in range(smp):
        x, y = kepler_states(ts[k], idx, B, with_v=False)
        th = np.arctan2(y, x) - B.n * ts[k]
        if k > 0:
            path += np.abs(np.mod(th - th_prev + np.pi, TWOPI) - np.pi)
        th_prev = th
    dphi = B.rho / B.a                        # cell arc = rho
    azim = path * orbits / dphi
    return radial + azim


def shear_grid_detection(B, ref, smp=2048):
    """For each true encounter: did a cell change of either body fall inside
    its d<rho interval (or did the initial sweep catch it)?"""
    ei, ej, t, d = ref["encounters"]
    K = len(ei)
    if K == 0:
        return 0, 0
    r0 = B.rlo.min() - B.rho
    det = np.zeros(K, bool)
    for k in range(K):
        i = int(ei[k]); j = int(ej[k])
        a = max(ref["t_in"][k], 0.0); b = min(ref["t_out"][k], T_MAX[0])
        if a > b:
            det[k] = True   # clipped: only visible at t=0 sweep
            continue
        ts = np.linspace(a, b, min(smp, max(int((b - a) / 1e-6) + 3, 5)))
        changed = False
        for bidx in (i, j):
            ii = np.full(len(ts), bidx)
            x, y = kepler_states(ts, ii, B, with_v=False)
            r = np.hypot(x, y)
            th = np.arctan2(y, x) - B.n[bidx] * ts
            nph = int(round(TWOPI / (B.rho / B.a[bidx])))
            cell = np.floor((r - r0) / B.rho).astype(np.int64) * (2 * nph) \
                 + np.mod(np.floor(th / (B.rho / B.a[bidx])).astype(np.int64), nph)
            changed |= bool((np.diff(cell) != 0).any())
        det[k] = changed
    return int(det.sum()), K


def hier_bounds(B, ref, T):
    """Groups in adjacent a; certificates from radial envelopes.
    A group pair whose certificate expires too often (renewals > REN_MAX)
    is split (the wider group halves); at the floor (<= 4 bodies or width
    <= 2 rho) member pairs are interval-tested and exact-examined."""
    order = np.argsort(B.a, kind="stable")
    ae = B.a * B.e
    rlo_s = B.rlo[order]; rhi_s = B.rhi[order]; ae_s = ae[order]
    a_s = B.a[order]
    Wbar = 2.0 * ae.mean() + B.rho
    wg = max(2.0 * Wbar / 3.0, 4.0 * B.rho)
    starts = []; ends = []
    s = 0
    for k in range(1, B.N + 1):
        if k == B.N or a_s[k] - a_s[s] > wg:
            starts.append(s); ends.append(k); s = k
    G = len(starts)
    env = {}
    def envelope(p, q):
        key = (p, q)
        if key not in env:
            env[key] = (rlo_s[p:q].min(), rhi_s[p:q].max(),
                        ae_s[p:q].max(), a_s[p:q].max(), a_s[p:q].min(),
                        float(q - p), a_s[p:q])
        return env[key]
    REN_MAX = 64
    cert = renew_tot = splits = member = exact = 0
    stack = [(starts[p], ends[p], starts[q], ends[q], False)
             for p in range(G) for q in range(p + 1, G)]
    stack += [(starts[p], ends[p], starts[p], ends[p], True) for p in range(G)]
    # only pairs whose envelopes can ever interact matter
    out = []
    for it in stack:
        sp, ep, sq, eq, intra = it
        lop, hip, aep, ahp, alp, szp, _ = envelope(sp, ep)
        loq, hiq, aeq, ahq, alq, szq, _ = envelope(sq, eq)
        if intra:
            out.append(it)
            continue
        gap = max(lop - hiq, loq - hip)
        if gap <= 1.5 * (aep + aeq) + B.rho:
            out.append(it)
    stack = out
    while stack:
        sp, ep, sq, eq, intra = stack.pop()
        lop, hip, aep, ahp, alp, szp, _ = envelope(sp, ep)
        loq, hiq, aeq, ahq, alq, szq, _ = envelope(sq, eq)
        gap = max(lop - hiq, loq - hip)
        vclose = alp ** (-1.5) * aep + alq ** (-1.5) * aeq + 1e-300
        tau = max(gap - B.rho, 0.0) / vclose
        rens = int(np.ceil(T / tau)) if tau > 0 else 0
        wp = a_s[ep - 1] - a_s[sp]; wq = a_s[eq - 1] - a_s[sq]
        splittable = max(wp, wq) > 2 * B.rho and min(szp, szq) > 4
        if not intra and tau > 0 and rens <= REN_MAX:
            cert += 1; renew_tot += rens      # settled: members can never meet
            continue
        if splittable:
            splits += 1
            if intra:
                m = (sp + ep) // 2
                stack.append((sp, m, sp, m, True))
                stack.append((sp, m, m, ep, False))
                stack.append((m, ep, m, ep, True))
            elif wp >= wq:
                m = (sp + ep) // 2
                stack.append((sp, m, sq, eq, False))
                stack.append((m, ep, sq, eq, False))
            else:
                m = (sq + eq) // 2
                stack.append((sp, ep, sq, m, False))
                stack.append((sp, ep, m, eq, False))
            continue
        # floor: member interval tests settle pairs forever (frozen elements);
        # overlapping ones are examined exactly
        ii = np.arange(sp, ep); jj = np.arange(sq, eq)
        ok = (rlo_s[ii, None] <= rhi_s[None, jj] + B.rho) & \
             (rlo_s[None, jj] <= rhi_s[ii, None] + B.rho)
        if intra:
            iu, ju = np.triu_indices(len(ii), 1)
            member += len(iu)
            exact += int(ok[iu, ju].sum())
        else:
            member += len(ii) * len(jj)
            exact += int(ok.sum())
    events = int(cert + renew_tot + splits + member + exact)
    return dict(events=events, detected=len(ref["encounters"][0]), missed=0,
                false=0, parts=dict(cert=cert, renew=renew_tot, splits=splits,
                                    member=member, exact=exact))


def ring_cells_events(B, T):
    """128 rings x 16 spokes; body checks occupants of each new cell."""
    Nr, Ns = 128, 16
    dr = (B.rhi.max() - B.rlo.min()) / Nr
    dphi = TWOPI / Ns
    orbits = T * B.n / TWOPI
    radial = 4.0 * B.a * B.e / dr * orbits
    idx = np.arange(B.N)
    smp = 64
    path = np.zeros(B.N)
    th_prev = None
    for k in range(smp):
        ts = (k / smp) * TWOPI / B.n
        x, y = kepler_states(np.full(B.N, ts) if np.isscalar(ts) else ts, idx, B, with_v=False)
        th = np.arctan2(y, x)
        if k > 0:
            path += np.abs(np.mod(th - th_prev + np.pi, TWOPI) - np.pi)
        th_prev = th
    azim = path * orbits / dphi
    return radial + azim, dr, dphi


def ring_cells_detection(B, ref, dr, dphi, smp=4096):
    """Per the rung: a body checks the occupants of the new cell at its own
    cell crossings. Detected iff either body changes cell inside the
    d<rho interval (the other is then within rho and co-resident, cells
    being much wider than rho), or the initial sweep catches it."""
    ei, ej, t, d = ref["encounters"]
    K = len(ei)
    if K == 0:
        return 0, 0
    det = np.zeros(K, bool)
    for k in range(K):
        i = int(ei[k]); j = int(ej[k])
        a = max(ref["t_in"][k], 0.0); b = min(ref["t_out"][k], T_MAX[0])
        if a > b:
            det[k] = True
            continue
        changed = False
        for bidx in (i, j):
            ii = np.full(smp, bidx)
            ts = np.linspace(a, b, smp)
            x, y = kepler_states(ts, ii, B, with_v=False)
            cell = np.floor(np.hypot(x, y) / dr).astype(np.int64) * N_SPOKES[0] \
                 + np.mod(np.floor(np.arctan2(y, x) / dphi).astype(np.int64),
                          N_SPOKES[0])
            changed |= bool((np.diff(cell) != 0).any())
        det[k] = changed
    return int(det.sum()), K


N_SPOKES = [16]


def oracle(ref):
    K = len(ref["encounters"][0])
    return dict(events=K, detected=K, missed=0, false=0)
