import json, math, random, time
from concurrent.futures import ProcessPoolExecutor
import r10 as R

def watch(args):
    side, k, alpha, rtol = args
    sc = R.Scene(1e-3)
    s0 = R.b12_ship(sc, side, k, alpha)
    times = [j * sc.period / 256 for j in range(200 * 256 + 1)]
    out = R.truth_states(sc, s0, times, rtol)
    if out is None:
        return None
    states, nfev = out
    inside, crossings, cj = None, 0, []
    for t, s in zip(times, states):
        now = sc.planet_distance(t, s) < sc.soi
        if inside is not None and now != inside:
            crossings += 1
        inside = now
        if abs((t / sc.period) * 8.0 - round((t / sc.period) * 8.0)) < 1e-9:
            cj.append(sc.jacobi(t, s))
    return crossings, cj, nfev

if __name__ == "__main__":
    t0 = time.time()
    rng = random.Random(20261011)
    cands = R.b12_candidates(rng, 12)   # the rung's own sampler, first 12 draws
    with ProcessPoolExecutor(2) as ex:
        bases = [ex.submit(watch, (*c, 1e-12)) for c in cands]
        res = [f.result() for f in bases]
    kept = []
    for c, r in zip(cands, res):
        if r is not None:
            kept.append({"idx": cands.index(c), "sk": list(c), "crossings": r[0],
                         "cj": r[1], "nfev": r[2], "converged": None})
    kept.sort(key=lambda s: -s["crossings"])
    kept = kept[:6]
    json.dump({"kept": kept, "tried": 12, "excluded": 12 - len(kept),
               "note": "rung sampler Random(20261011) first 12 draws; ships whose 1e-12 "
                       "reference completed, six with the most SOI crossings; the gate's frozen "
                       "SplitMix64 ships all failed or did not converge under this barycentric "
                       "reference within the budget; no ship reached 20 crossings"},
              open("b12_sel.json", "w"))
    print("kept", [(s["crossings"], [round(v, 3) for v in s["sk"]]) for s in kept],
          f"{time.time()-t0:.0f}s", flush=True)
