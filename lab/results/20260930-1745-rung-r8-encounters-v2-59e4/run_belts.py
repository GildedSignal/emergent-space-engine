"""Run the 16 frozen belts (N = 1e4, 20 periods at a = 1) and record, per
configuration, events and detection outcome against the reference."""
import json
import random
import sys
import time

import numpy as np

from belt import make_belt, belt_params
import reference as R
import configs as C
from configs import T_MAX

NBELT = 16
N_BODIES = 10_000
PERIODS = 20          # orbital periods at a = 1 (T = 40 pi, mu = 1)
T = PERIODS * 2.0 * np.pi

def main(out_path):
    rng = random.Random(20261008)
    recs = []
    for b in range(NBELT):
        t0 = time.time()
        sigma_e, rho = belt_params(rng)
        B = make_belt(rng, N_BODIES, sigma_e, rho)
        T_MAX[0] = T
        pi, pj = R.candidate_pairs(B)
        ref = R.reference_encounters(B, T, pi, pj)
        K = len(ref["encounters"][0])
        ev_sg = C.shear_grid_events(B, T)
        det_sg, _ = C.shear_grid_detection(B, ref)
        ev_rc, dr, dphi = C.ring_cells_events(B, T)
        det_rc, _ = C.ring_cells_detection(B, ref, dr, dphi)
        rec = dict(
            belt=b, sigma_e=sigma_e, rho=rho, truth=K,
            cand_pairs=int(len(pi)),
            conj=int(ref["C"].sum()),
            element_sort=dict(events=int(ref["C"].sum()), detected=K),
            shear_grid=dict(events=int(ev_sg.sum()), detected=int(det_sg)),
            hier_bounds=C.hier_bounds(B, ref, T),
            ring_cells=dict(events=int(ev_rc.sum()), detected=int(det_rc)),
            oracle=dict(events=K, detected=K),
        )
        recs.append(rec)
        print(f"belt {b:2d}  sig_e={sigma_e:.4f} rho={rho:.2e}  cand={len(pi):8d}"
              f"  conj={rec['conj']:9d}  truth={K:6d}"
              f"  es={rec['element_sort']['events']:9d}"
              f"  sg={rec['shear_grid']['events']:11d} detsg={det_sg}"
              f"  hb={rec['hier_bounds']['events']:10d}"
              f"  rc={rec['ring_cells']['events']:10d} detrc={det_rc}"
              f"  ({time.time()-t0:.1f}s)", flush=True)
    with open(out_path, "w") as f:
        json.dump(recs, f)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "belts.json")
