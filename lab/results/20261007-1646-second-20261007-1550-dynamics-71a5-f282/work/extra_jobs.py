#!/usr/bin/env python3
import json, os, time
from cert import TAU, body, pair_minima
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "truth")
nn = lambda a: a ** -1.5
G6 = (body(1.0, 0.30, 0.3, nn(1.0)), body(0.8, 0.30, 1.03, nn(0.8)))
PH12 = [k * TAU / 12 for k in range(12)]
import sys
i, n = int(sys.argv[1]), int(sys.argv[2])
J = []
for k in [1,2,4,5,7,8,10,11]:
    for j in range(1, 92):
        J.append((f"g6P_p{k}_d{j}", dict(G6[0], pom=G6[0]["pom"] + 0.05*j), dict(G6[1], M0=PH12[k]), 1500.0, 1<<21))
mine = [(idx, j) for idx, j in enumerate(J) if idx % n == i]
t0=time.time()
for idx, (key, bi, bj, T, N) in mine:
    path = os.path.join(OUT, key + ".json")
    if os.path.exists(path): continue
    mins = pair_minima(bi, bj, T, N, 0.05)
    tmp = path + ".tmp"
    with open(tmp, "w") as f: json.dump(dict(key=key, T=T, N=N, mins=[[t,d] for t,d in mins]), f)
    os.replace(tmp, path)
print(f"extra shard {i}/{n}: {len(mine)} jobs in {time.time()-t0:.0f}s")

