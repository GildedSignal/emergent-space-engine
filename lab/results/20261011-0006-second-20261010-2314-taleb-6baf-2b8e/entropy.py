#!/usr/bin/env python3
"""k-NN (Kozachenko-Leonenko) differential entropy of (a, L) samples from the
hlive2 dumps (N=4000) — the estimator that scales with N (no log2(N) pin)."""
import glob, json, math
import numpy as np
from scipy.spatial import cKDTree
from scipy.special import digamma


def knn_h(a, L, ks=(1, 4, 8, 16)):
    X = np.column_stack([a, L]).astype(float)
    N = X.shape[0]
    tree = cKDTree(X)
    out = {}
    for k in ks:
        d, _ = tree.query(X, k=k + 1)
        r = d[:, k]
        r = r[r > 0]
        out[f"k{k}"] = float((digamma(N) - digamma(k)) / math.log(2) + math.log2(math.pi)
                            + 2.0 * np.mean(np.log2(r)))
    return out


rows = {}
for f in sorted(glob.glob("*.2.json")):
    d = json.load(open(f))
    if "dumps" not in d:
        continue
    tag = d["tag"]
    rows[tag] = {}
    for mark, smp in d["dumps"].items():
        act = np.array(smp["active"], bool)
        a = np.array(smp["a"], float)[act]
        L = np.array(smp["L"], float)[act]
        rows[tag][mark] = {"n": int(act.sum()), "h_bits": knn_h(a, L)}
        print(tag, mark, rows[tag][mark]["n"], {k: round(v, 3) for k, v in rows[tag][mark]["h_bits"].items()})

# iid thin-ridge null at N=4000 for the legacy plug-in pin (checker's null, our scale)
rng = np.random.default_rng(7)
for Nn in (4000, 40000, 1000000):
    a = 2.0 + 1.5 * rng.random(Nn)
    e = rng.rayleigh(0.02, Nn)
    L = np.sqrt(a * (1.0 - e * e))
    if Nn <= 40000:
        rows[f"null{Nn}"] = {"birth": {"n": Nn, "h_bits": knn_h(a, L)}}

json.dump(rows, open("entropy.json", "w"), indent=1)
print("wrote entropy.json")
