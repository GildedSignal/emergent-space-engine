#!/usr/bin/env python3
"""P1 — Integer multiresolution moments (dyadic quadtree) for the kick field.

Claim under test: a doll's mass field, held as integer moments on a dyadic tree,
gives (a) an epsilon-controlled field error from a *dimensionless, per-scale*
criterion (own detail below threshold at own scale), (b) sparse reads on smooth
scenes, (c) per-level coefficient ranges that fit a shared exponent (32-bit
packets), (d) bit-identical sums under any visit order.

Kernel: 2D gravity potential Phi = sum m*log|q-p| (the game is 2D).
Criterion C1 (dipole only): accept node iff S <= d(query, node box) and
  |Dx|+|Dy| <= eps*M*S                      (all integer comparisons)
Criterion C2: additionally Q/S^2 <= eps*M    (Q = sum m*|offset|^2, node units)
Control: Barnes-Hut theta in {0.5, 0.75, 1.0}, monopole at COM (float).
Oracle: direct float64 sum over all bodies.

Notes on arithmetic: the bulk sweep uses int64 with per-level normalization
(Dx,Dy <= 2^49, M <= 2^30, Q>>2*(20-level) <= 2^30: all exact); the determinism
checksum runs the same criterion on a Python-int path. eps is dyadic,
eps = eps_num / 2^12.
"""
import json
import numpy as np

rng = np.random.default_rng(20261005)

GRID = 1 << 20
EPS_BITS = 12
MAXDEPTH = 10
LOG2GRID = 20

# ---------------- scenes ----------------
def make_belt(n, r0=0.30, r1=0.50):
    th = rng.uniform(0, 2*np.pi, n)
    r = np.sqrt(rng.uniform(r0**2, r1**2, n))
    return 0.5 + r*np.cos(th), 0.5 + r*np.sin(th)

def make_galaxy(n):
    arm = rng.integers(0, 2, n)
    t = rng.uniform(0.0, 2.6, n)
    r = np.clip(0.06*np.exp(0.75*t), 0.02, 0.46)
    th = t*2.0 + arm*np.pi + rng.normal(0, 0.15, n)
    return np.clip(0.5 + r*np.cos(th), 0.001, 0.999), np.clip(0.5 + r*np.sin(th), 0.001, 0.999)

def masses_zipf(n, heavy=1 << 18, tail=1 << 6):
    rank = np.arange(1, n+1)
    m = np.maximum((heavy / rank**1.1).astype(np.int64), tail)
    rng.shuffle(m)
    return m

# ---------------- flat tree ----------------
class Tree:
    """Flat arrays per node: cx, cy, size, M, Dx, Dy, qn(=Q>>2*(20-level)),
    level, first_child, n_children, leaf flag; leaf nodes index into body lists."""

def build(xi, yi, m, depth=MAXDEPTH):
    T = Tree()
    # Morticode: node id = level-major ordering built by BFS
    cells = {}
    for x, y in zip(xi, yi):
        k = (int(x) >> depth, int(y) >> depth)
        cells.setdefault(k, []).append(len(cells))
    # simpler: build node lists level by level using dictionaries
    cx_l, cy_l, size_l, M_l, Dx_l, Dy_l, qn_l, lev_l, kids_l, bodies_l = \
        [], [], [], [], [], [], [], [], [], []
    body_cell = np.empty(len(xi), dtype=np.int64)
    cellmap = {}
    for i, (x, y) in enumerate(zip(xi, yi)):
        k = (int(x) >> depth, int(y) >> depth)
        if k not in cellmap:
            cellmap[k] = []
        cellmap[k].append(i)
    def make(level, lx, ly):
        size = GRID >> level
        cx, cy = lx*size + size//2, ly*size + size//2
        if level == depth:
            idxs = cellmap.get((lx, ly), [])
            if not idxs:
                return None
            M = np.int64(0); Dx = np.int64(0); Dy = np.int64(0); Q = 0
            for i in idxs:
                mm = int(m[i])
                M += mm
                Dx += mm*(int(xi[i])-cx); Dy += mm*(int(yi[i])-cy)
                Q += mm*((int(xi[i])-cx)**2 + (int(yi[i])-cy)**2)
                body_cell[i] = len(M_l)
            cx_l.append(cx); cy_l.append(cy); size_l.append(size)
            M_l.append(np.int64(M)); Dx_l.append(np.int64(Dx)); Dy_l.append(np.int64(Dy))
            qn_l.append(np.int64(Q >> (2*(LOG2GRID-level))))
            lev_l.append(level); kids_l.append(None); bodies_l.append(np.array(idxs, dtype=np.int64))
            return len(M_l) - 1
        kids = []
        for a in (0, 1):
            for b in (0, 1):
                k = make(level+1, 2*lx+a, 2*ly+b)
                if k is not None:
                    kids.append(k)
        if not kids and not (level == 0):
            return None
        M = np.int64(0); Dx = np.int64(0); Dy = np.int64(0); Q = 0
        for k in kids:
            M += M_l[k]
            Dx += Dx_l[k] + M_l[k]*(cx_l[k]-cx)
            Dy += Dy_l[k] + M_l[k]*(cy_l[k]-cy)
            s = size_l[k]
            Q += (qn_l[k] << (2*(LOG2GRID-level-1))) \
                 + 2*(Dx_l[k]*(cx_l[k]-cx) + Dy_l[k]*(cy_l[k]-cy)) + M_l[k]*((cx_l[k]-cx)**2 + (cy_l[k]-cy)**2)
        cx_l.append(cx); cy_l.append(cy); size_l.append(size)
        M_l.append(np.int64(M)); Dx_l.append(np.int64(Dx)); Dy_l.append(np.int64(Dy))
        qn_l.append(np.int64(Q >> (2*(LOG2GRID-level))))
        lev_l.append(level); kids_l.append(np.array(kids, dtype=np.int64) if kids else None)
        bodies_l.append(None)
        return len(M_l) - 1

    root = make(0, 0, 0)
    T.cx = np.array(cx_l, dtype=np.int64); T.cy = np.array(cy_l, dtype=np.int64)
    T.size = np.array(size_l, dtype=np.int64); T.M = np.array(M_l, dtype=np.int64)
    T.Dx = np.array(Dx_l, dtype=np.int64); T.Dy = np.array(Dy_l, dtype=np.int64)
    T.qn = np.array(qn_l, dtype=np.int64); T.lev = np.array(lev_l, dtype=np.int64)
    T.kids = kids_l; T.bodies = bodies_l; T.root = root; T.body_cell = body_cell
    return T

def traverse(T, px, py, eps_num, criterion, bh_theta=None):
    """Vectorized level-by-level traversal. Returns (accepted_ids, leaf_ids).
    criterion=1: dipole test; 2: dipole+quadrupole; bh_theta set: Barnes-Hut."""
    accepted, leaves = [], []
    frontier = np.array([T.root], dtype=np.int64)
    while frontier.size:
        cx = T.cx[frontier]; cy = T.cy[frontier]; S = T.size[frontier]
        dx = np.maximum(np.abs(px - cx) - (S >> 1), 0)
        dy = np.maximum(np.abs(py - cy) - (S >> 1), 0)
        d2 = dx*dx + dy*dy
        M = T.M[frontier]
        contains = (np.abs(px - cx) <= (S >> 1)) & (np.abs(py - cy) <= (S >> 1))
        if bh_theta is not None:
            d = np.sqrt(d2.astype(np.float64))
            ok = (~contains) & (M > 0) & (S <= bh_theta*np.maximum(d, 1e-9))
        else:
            ok = (~contains) & (M > 0) & (S.astype(np.int64)*S <= d2)
            if criterion == 1:      # dipole channel: negative control (wrong for COM)
                dip = np.abs(T.Dx[frontier]) + np.abs(T.Dy[frontier])
                thr = (np.int64(eps_num)*M*S) >> EPS_BITS
                ok &= dip <= thr
            if criterion == 2:      # quadrupole channel: own-scale concentration
                thr2 = (np.int64(eps_num)*M) >> EPS_BITS
                ok &= T.qn[frontier] <= thr2
            if criterion == 3:      # concentration x distance: error of THIS node <= eps
                # Q/(M d^2) <= eps   <=>   qn*S^2 <= eps_num*d^2*M / 2^12
                lhs = T.qn[frontier]*(S*S)
                rhs = ((np.int64(eps_num)*M) >> EPS_BITS)*d2
                ok &= lhs <= rhs
        acc = frontier[ok]
        accepted.append(acc)
        rest = frontier[~ok]
        # leaves among rest: nodes with no children
        has_kids = np.array([T.kids[i] is not None and len(T.kids[i]) > 0 for i in rest],
                            dtype=bool) if rest.size else np.zeros(0, dtype=bool)
        leaves.append(rest[~has_kids])
        nxt = [T.kids[int(i)] for i in rest[has_kids]]
        frontier = np.concatenate(nxt) if nxt else np.zeros(0, dtype=np.int64)
    return np.concatenate(accepted) if accepted else np.zeros(0, dtype=np.int64), \
           np.concatenate(leaves) if leaves else np.zeros(0, dtype=np.int64)

def phi_terms(T, acc, leaf_ids, px, py, xi, yi, m, skip_idx):
    phi = 0.0; terms = 0
    if acc.size:
        M = T.M[acc].astype(np.float64)
        comx = (T.cx[acc]*T.M[acc] + T.Dx[acc]).astype(np.float64)/M
        comy = (T.cy[acc]*T.M[acc] + T.Dy[acc]).astype(np.float64)/M
        r2 = np.maximum((comx-px)**2 + (comy-py)**2, 1.0)
        phi += float(np.sum(M*0.5*np.log(r2))); terms += acc.size
    for L in leaf_ids:
        for i in T.bodies[L]:
            if i == skip_idx: continue
            r2 = (xi[i]-px)**2 + (yi[i]-py)**2
            if r2 == 0: continue
            phi += float(m[i])*0.5*np.log(r2); terms += 1
    return phi, terms

def direct_phi(px, py, xi, yi, m, skip_idx):
    r2 = np.maximum((xi-px)**2 + (yi-py)**2, 1)
    mm = m.astype(np.float64).copy()
    if skip_idx is not None: mm[skip_idx] = 0.0
    return float(np.sum(mm*0.5*np.log(r2)))

def run_scene(name, x, y, m, nq=128):
    xi = np.clip((x*GRID).astype(np.int64), 0, GRID-1)
    yi = np.clip((y*GRID).astype(np.int64), 0, GRID-1)
    T = build(xi, yi, m)
    qidx = rng.choice(len(xi), size=min(nq, len(xi)), replace=False)
    xif, yif = xi.astype(np.float64), yi.astype(np.float64)
    oracle = np.array([direct_phi(xi[i], yi[i], xif, yif, m, i) for i in qidx])
    res = {'scene': name, 'N': int(len(xi)), 'direct_terms': int(len(xi))}
    for criterion, esweep in ((1, (16,)), (2, (256, 64,)), (3, (256, 64, 16, 4))):
        for e in esweep:
            errs, terms_l = [], []
            for j, qi in enumerate(qidx):
                acc, lv = traverse(T, xi[qi], yi[qi], e, criterion)
                phi, terms = phi_terms(T, acc, lv, xi[qi], yi[qi], xi, yi, m, qi)
                errs.append(abs(phi - oracle[j])); terms_l.append(terms)
            rel = np.array(errs)/np.abs(oracle)
            res[f'C{criterion}_eps_{e}_over_{1<<EPS_BITS}'] = {
                'max_rel': float(np.max(rel)), 'rms_rel': float(np.sqrt(np.mean(rel**2))),
                'mean_terms': float(np.mean(terms_l)), 'p99_terms': float(np.percentile(terms_l, 99))}
    for theta in (0.5, 0.75, 1.0):
        errs, terms_l = [], []
        for j, qi in enumerate(qidx):
            acc, lv = traverse(T, xi[qi], yi[qi], 0, 0, bh_theta=theta)
            phi, terms = phi_terms(T, acc, lv, xi[qi], yi[qi], xi, yi, m, qi)
            errs.append(abs(phi - oracle[j])); terms_l.append(terms)
        rel = np.array(errs)/np.abs(oracle)
        res[f'BH_theta_{theta}'] = {
            'max_rel': float(np.max(rel)), 'rms_rel': float(np.sqrt(np.mean(rel**2))),
            'mean_terms': float(np.mean(terms_l)), 'p99_terms': float(np.percentile(terms_l, 99))}
    # determinism: same criterion on Python-int path, two child orders
    def tally(seed):
        import random
        rnd = random.Random(seed)
        stack = [T.root]
        h = 0
        h2 = 0
        while stack:
            nd = int(stack.pop())
            cx, cy, S, M = int(T.cx[nd]), int(T.cy[nd]), int(T.size[nd]), int(T.M[nd])
            dx = max(abs(int(xi[qidx[0]])-cx) - S//2, 0); dy = max(abs(int(yi[qidx[0]])-cy) - S//2, 0)
            contains = abs(int(xi[qidx[0]])-cx) <= S//2 and abs(int(yi[qidx[0]])-cy) <= S//2
            kids = T.kids[nd]
            has_kids = kids is not None and len(kids) > 0
            ok = (not contains) and M > 0 and S*S <= dx*dx + dy*dy \
                 and int(T.qn[nd]) <= (16*M) >> EPS_BITS
            if ok or not has_kids:
                v = (M*1000003 + int(T.Dx[nd])) if ok else (-nd-1)
                h = (h + v) & 0xFFFFFFFFFFFFFFFF
                h2 = (h2*3 + v) & 0xFFFFFFFFFFFFFFFF
                continue
            kids = list(kids); rnd.shuffle(kids); stack.extend(kids)
        return h
    res['determinism_int_identical'] = bool(tally(1) == tally(2))
    # float control: accepted-monopole float sums in opposite orders
    def floatsum(seed):
        acc, lv = traverse(T, xi[qidx[0]], yi[qidx[0]], 16, 2)
        M = T.M[acc].astype(np.float64)
        comx = (T.cx[acc]*T.M[acc] + T.Dx[acc]).astype(np.float64)/M
        comy = (T.cy[acc]*T.M[acc] + T.Dy[acc]).astype(np.float64)/M
        vals = list(M*0.5*np.log(np.maximum((comx-xi[qidx[0]])**2 + (comy-yi[qidx[0]])**2, 1.0)))
        if seed:
            import random as _r
            _r.Random(seed).shuffle(vals)
        s = 0.0
        for v in vals: s += v
        return s
    res['float_control_identical'] = bool(floatsum(0) == floatsum(1))
    # per-level detail spread: log2((|Dx|+|Dy|)/(M*S))
    inner = np.arange(len(T.M))
    inner = inner[(T.M > 0) & (T.lev < MAXDEPTH)]
    ratio = (np.abs(T.Dx[inner]) + np.abs(T.Dy[inner])).astype(np.float64) / (T.M[inner]*T.size[inner]).astype(np.float64)
    lv = T.lev[inner]
    res['detail_bits_per_level'] = {}
    for l in range(MAXDEPTH):
        msk = lv == l
        if msk.sum() > 8:
            v = np.log2(np.maximum(ratio[msk], 1e-30))
            res['detail_bits_per_level'][str(l)] = {
                'p1': float(np.percentile(v, 1)), 'p99': float(np.percentile(v, 99)),
                'spread_bits': float(np.percentile(v, 99) - np.percentile(v, 1))}
    return res

def main():
    out = []
    n = 4096
    x, y = make_belt(n); m = masses_zipf(n)
    out.append(run_scene('belt', x, y, m))
    x, y = make_galaxy(n); m = masses_zipf(n)
    out.append(run_scene('galaxy', x, y, m))
    xb, yb = make_belt(n-256)
    xc = np.clip(0.42 + rng.normal(0, 0.008, 256), 0.001, 0.999)
    yc = np.clip(0.58 + rng.normal(0, 0.008, 256), 0.001, 0.999)
    x = np.concatenate([xb, xc]); y = np.concatenate([yb, yc])
    m = np.concatenate([masses_zipf(n-256), np.full(256, 1 << 14, dtype=np.int64)])
    out.append(run_scene('belt+battle', x, y, m))
    with open('probe1_out.json', 'w') as f:
        json.dump(out, f, indent=1)
    for r in out:
        print(f"== {r['scene']} (N={r['N']}, direct terms/query = {r['N']})")
        for k, v in r.items():
            if isinstance(v, dict) and 'max_rel' in v:
                print(f"  {k:28s} max_rel={v['max_rel']:.2e} rms={v['rms_rel']:.2e} "
                      f"terms mean={v['mean_terms']:7.0f} p99={v['p99_terms']:7.0f}")
        print(f"  determinism int identical: {r['determinism_int_identical']}; "
              f"float control identical: {r['float_control_identical']}")
        sp = max(v['spread_bits'] for v in r['detail_bits_per_level'].values())
        print(f"  worst per-level detail spread: {sp:.1f} bits")

if __name__ == '__main__':
    main()
