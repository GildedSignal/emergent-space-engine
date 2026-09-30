"""Run the 16 frozen belts (N=1e4, sampler random.Random(20261008)) and the
scaling runs; write belts.json, scaling.json, validation notes."""
import json, random, time
import numpy as np
from multiprocessing import Pool
from common import *

def run_one(args):
    b, sigma_e, rho = args
    rng = random.Random(20261008)
    for _ in range(b):          # burn the b first belt-param draws
        draw_belt_params(rng)
    a, e, varpi, lam0 = sample_belt(rng, 10000, sigma_e)
    Ws = None
    t0 = time.time()
    res = analyse_belt(a, e, varpi, lam0, rho, Ws=Ws)
    res.pop('_dips', None); res.pop('_pairs', None)
    res['sigma_e'] = sigma_e
    res['seconds'] = round(time.time() - t0, 1)
    res['belt'] = b
    return res

def main():
    rng = random.Random(20261008)
    params = [draw_belt_params(rng) for _ in range(16)]
    with Pool(4) as pool:
        results = pool.map(run_one, [(b, p[0], p[1]) for b, p in enumerate(params)])
    with open('belts.json', 'w') as f:
        json.dump(results, f, indent=1)
    print("belt  sigma_e   rho      ref   es_found es_miss  es_events   sh_events   rc_events  s")
    for r in results:
        print(f"{r['belt']:4d}  {r['sigma_e']:.2e}  {r['rho']:.2e}  {r['ref_encounters']:5d} "
              f"{r['element-sort']['found']:6d} {r['element-sort']['missed']:6d} "
              f"{r['element-sort']['events']:10.0f} {r['shear-grid']['events']:11.3e} "
              f"{r['ring-cells']['events']:10.3e}  {r['seconds']}")

if __name__ == '__main__':
    main()
