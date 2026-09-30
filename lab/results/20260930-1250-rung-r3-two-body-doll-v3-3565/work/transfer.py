"""The transfer: 2:1 interior resonant chain, ship apoapsis r_apo = 1.0044 AU,
started at apoapsis 0.004 rad behind the planet. Conjunctions recur each
planet period (two handoffs per conjunction); 100 handoffs = 50 conjunctions.

Outputs transfer.json: law crossings (t, E_helio, entering), reference samples
at the same times, path samples in the rotating frame, exponent, convergence.
"""
import json
import math

from common import MU_PLANET, R_SOI
from nbary import (helio_energy, helio_state, law_ship, planet_state,
                   run_law_transfer, run_reference)

R_APO = 1.0044
THETA_A = -0.0040
A_S = 2.0 ** (-2.0 / 3.0)


def initial_state():
    r_apo = R_APO
    v_apo = math.sqrt(2.0 / r_apo - 1.0 / A_S)
    r0 = (r_apo * math.cos(THETA_A), r_apo * math.sin(THETA_A))
    v0 = (v_apo * -math.sin(THETA_A), v_apo * math.cos(THETA_A))
    y0 = (0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, r0[0], r0[1], v0[0], v0[1])
    return y0, r0, v0


def main():
    y0, r0, v0 = initial_state()
    print("law: propagating patched dolls to 100 handoffs...", flush=True)
    crossings, path, _tf = run_law_transfer(r0, v0, n_cross=100, win=0.01, sample_dt=0.08, t_max=400)
    t_end = crossings[-1][0]
    print(f"  100 handoffs by t={t_end:.2f} ({t_end/(2*math.pi):.1f} planet periods)",
          flush=True)
    times = [c[0] for c in crossings]

    print("reference: base run...", flush=True)
    yf, samples = run_reference(y0, t_end, targets=times, h_bg=3.75e-4, c_enc=500.0)
    print("reference: half-step rerun...", flush=True)
    yf2, _ = run_reference(y0, t_end, targets=times, h_bg=1.875e-4, c_enc=707.0)

    (rx, ry), _ = helio_state(yf)
    (rx2, ry2), _ = helio_state(yf2)
    rel_final = math.hypot(rx - rx2, ry - ry2) / math.hypot(rx, ry)
    print(f"  final-position agreement base vs half-step: {rel_final:.3e}")

    err = []
    for (t, E_law, entering), (tq, y) in zip(crossings, samples):
        E_ref = helio_energy(y)
        err.append(abs(E_law - E_ref))
    ks = list(range(1, len(err) + 1))
    lx = [math.log(k) for k in ks]
    ly = [math.log(max(e, 1e-300)) for e in err]
    n = len(ks)
    mx, my = sum(lx) / n, sum(ly) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(lx, ly))
    sxx = sum((a - mx) ** 2 for a in lx)
    exponent = sxy / sxx
    print(f"  handoff energy-error growth exponent: {exponent:.4f}")
    print(f"  err[0]={err[0]:.3e} err[49]={err[49]:.3e} err[-1]={err[-1]:.3e}")

    rot = []
    for (t, x, y, _q) in path[::3]:
        c, s = math.cos(-t), math.sin(-t)
        rot.append((t, x * c - y * s, x * s + y * c))
    ref_rot = []
    for (t, y) in samples:
        (x, yy), _ = helio_state(y)
        c, s = math.cos(-t), math.sin(-t)
        ref_rot.append((t, x * c - yy * s, x * s + yy * c))
    out = dict(
        crossings=[(c[0], c[1], c[2]) for c in crossings],
        err=err, exponent=exponent, rel_final=rel_final, t_end=t_end,
        law_path_rot=rot, ref_path_rot=ref_rot,
    )
    with open("transfer.json", "w") as f:
        json.dump(out, f)


if __name__ == "__main__":
    main()
