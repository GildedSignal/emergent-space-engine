#!/usr/bin/env python3
"""Truth jobs for the second-author run (20261007-1646-...-f282).

Computes brute-force pair minima (the run's truth instrument, unchanged from cert.py) for a
fixed list of (key, body_i, body_j, T, N) specs, one JSON per job under truth/. Sharded:
    python3 jobs.py --shard i/n
Nothing here is tuned on results; all specs follow predictions.md.
"""
import argparse
import json
import os
import time

from cert import TAU, body, pair_minima

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "truth")

nn = lambda a: a ** -1.5

# geometries, exactly as the author defined them
G2 = (body(1.0, 0.30, 0.3, nn(1.0)), body(0.85, 0.40, 1.2, nn(0.85)))
G6 = (body(1.0, 0.30, 0.3, nn(1.0)), body(0.8, 0.30, 1.03, nn(0.8)))
G4N = (body(1.0, 0.30, 0.3, nn(1.0)), body(0.8, 0.30, 1.00, nn(0.8)))

TL, NL = 1500.0, 1 << 21   # light jobs (matches cert2's A2/B2-dT instrument)
TH, NH = 3000.0, 1 << 22   # heavy jobs (matches the author's results3 B2 grid)
DMAX = 0.05

PH12 = [k * TAU / 12 for k in range(12)]      # author's A2 phase grid
SUB4 = [0, 3, 6, 9]                            # 4 of the 12 phases for the theta-sweeps


def jobs():
    J = []  # (key, bi, bj, T, N)

    # --- A/B/C: G6 ensemble, frozen lists + true at 5 rates (scaling fit) ---
    for k, p in enumerate(PH12):
        J.append((f"g6f_p{k}", G6[0], dict(G6[1], M0=p), TL, NL))
    for omc in (1, 2, 3, 5, 10):
        for k, p in enumerate(PH12):
            J.append((f"g6r{omc}_p{k}", dict(G6[0], Om=omc * 1e-3),
                      dict(G6[1], M0=p), TL, NL))

    # --- D/E: G2 deep-crossing, 4 phases, frozen + true at om=3e-3 (fix test) ---
    for k in SUB4:
        J.append((f"g2f_p{k}", G2[0], dict(G2[1], M0=PH12[k]), TL, NL))
        J.append((f"g2r_p{k}", dict(G2[0], Om=3e-3), dict(G2[1], M0=PH12[k]), TL, NL))

    # --- F: rigid-rotation control on G2 (equal absolute Om both bodies) ---
    J.append(("g2rig_p0", dict(G2[0], Om=0.05), dict(G2[1], M0=0.0, Om=0.05), TL, NL))

    # --- G/H: G4n never-pair, 6 phases x 4 rates, T=3000 (safety-vs-realization) ---
    for omc in (1, 2, 3, 5):
        for k in range(6):
            J.append((f"g4r{omc}_p{k}", G4N[0],
                      dict(G4N[1], Om=-omc * 1e-3, M0=k * TAU / 6), TH, NH))
    J.append(("g4f", G4N[0], G4N[1], TH, NH))

    # --- I: G6 staleness grid: P(delta) = pair with pom_i shifted by delta, frozen ---
    for k in SUB4:
        for j in range(1, 92):
            J.append((f"g6P_p{k}_d{j}", dict(G6[0], pom=G6[0]["pom"] + 0.05 * j),
                      dict(G6[1], M0=PH12[k]), TL, NL))

    # --- J: G2 staleness grid ---
    for k in SUB4:
        for j in range(1, 92):
            J.append((f"g2P_p{k}_d{j}", dict(G2[0], pom=G2[0]["pom"] + 0.05 * j),
                      dict(G2[1], M0=PH12[k]), TL, NL))

    # --- K: regen of the author's results3 grid (verification, bit-identity) ---
    for om, tag in ((5e-4, "0.0005"), (1e-3, "0.001"), (2e-3, "0.002")):
        for k in range(4):
            J.append((f"regen_{tag}_k{k}", G4N[0],
                      dict(G4N[1], Om=-om, M0=k * TAU / 4), TH, NH))

    # --- L: G4n fix grid at theta=0.2, phase 0 (pom_j steps of 0.2, run direction) ---
    for j in range(1, 15):
        J.append((f"g4fix_d{j}", G4N[0],
                  dict(G4N[1], pom=G4N[1]["pom"] - 0.2 * j, M0=0.0), TH, NH))
    return J


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shard", default="0/1")
    a = ap.parse_args()
    i, n = (int(v) for v in a.shard.split("/"))
    os.makedirs(OUT, exist_ok=True)
    J = jobs()
    mine = [(idx, j) for idx, j in enumerate(J) if idx % n == i]
    print(f"shard {i}/{n}: {len(mine)} of {len(J)} jobs", flush=True)
    t0 = time.time()
    for done, (idx, (key, bi, bj, T, N)) in enumerate(mine):
        path = os.path.join(OUT, key + ".json")
        if os.path.exists(path):
            continue
        mins = pair_minima(bi, bj, T, N, DMAX)
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(dict(key=key, T=T, N=N, mins=[[t, d] for (t, d) in mins]), f)
        os.replace(tmp, path)
        print(f"[{time.time()-t0:7.1f}s] {key}: {len(mins)} minima", flush=True)
    print(f"shard {i}/{n} done in {time.time()-t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
