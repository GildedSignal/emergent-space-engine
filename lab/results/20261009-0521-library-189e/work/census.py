#!/usr/bin/env python3
"""Belt census: sharp convergents vs envelope disjointness vs chi regimes.
N=500 orbits, a ~ U[0.95,1.05], e ~ U[0,0.05]. Writes census.json. ~0.6 s."""
import math, random, json

rng = random.Random(20261009)
N = 500
a = [rng.uniform(0.95, 1.05) for _ in range(N)]
e = [rng.uniform(0, 0.05) for _ in range(N)]
n = [x ** -1.5 for x in a]

def convergents(x, qmax):
    out = []
    p2, p1, q2, q1 = 1, 0, 0, 1
    r = x - math.floor(x)
    for _ in range(30):
        if r < 1e-12:
            break
        ai = int(1 / r)
        if ai > 10 ** 9:
            break
        r = 1 / r - ai
        p = ai * p1 + p2
        q = ai * q1 + q2
        if q > qmax:
            break
        for m in range(1, ai + 1):
            out.append((m * p1 + p2, m * q1 + q2))
        p2, p1, q2, q1 = p1, p, q1, q
    return [(pp, qq) for pp, qq in out if 0 < qq <= qmax]

tot = adj = sharp = adj_sharp = disj = neither = clean = 0
for i in range(N):
    for j in range(i + 1, N):
        dn = n[i] - n[j]
        tot += 1
        adjpair = abs(a[i] - a[j]) < 0.02
        adj += adjpair
        w = (n[i] / dn) % 1.0 if abs(dn) > 1e-12 else 0.5
        sh = any(abs(w - p / q) < 1 / (2 * q * q) for (p, q) in convergents(w, 13))
        sharp += sh
        adj_sharp += (adjpair and sh)
        d = abs(a[i] - a[j]) > a[i] * e[j] + a[j] * e[i]
        disj += d
        neither += (not sh and not d)
        clean += (2 * max(e[i], e[j]) / abs(dn) < 0.5)

res = {"N": N, "pairs": tot, "adjacent_pairs": adj,
       "frac_sharp_convergent_q13": sharp / tot, "frac_adjacent_sharp": adj_sharp / adj,
       "frac_envelope_disjoint": disj / tot, "frac_neither_skin": neither / tot,
       "frac_clean_chi<0.5": clean / tot}
open("census.json", "w").write(json.dumps({**res, "counts": {
    "sharp": sharp, "adj_sharp": adj_sharp, "disj": disj, "neither": neither,
    "clean": clean}}, indent=1))
print(json.dumps(res, indent=1))
