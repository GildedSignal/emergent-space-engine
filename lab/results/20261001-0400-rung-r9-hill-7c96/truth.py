"""truth: direct integration of the circular restricted three-body problem
(DOP853, rtol=atol=1e-12), the same reference as behave B14. Also runs the
chaos probe: a re-run with a scaled by 1+1e-6; a seed is chaotic when its
bound/escaped class flips.
"""
import json
import numpy as np
from scipy.integrate import solve_ivp
from multiprocessing import Pool
from common import (MU, RH, T_END, DT, make_seeds, init_state, cr3bp,
                    rot_to_inert, osc)

T_EVAL = np.arange(0.0, T_END + DT / 2, DT)


def run_seed(args):
    seed, mode = args
    ascale = 1.0 + 1e-6 if mode == "chaos" else 1.0
    s0 = init_state(seed, ascale)
    sol = solve_ivp(cr3bp, (0.0, T_END), s0, method="DOP853",
                    rtol=1e-12, atol=1e-12, t_eval=T_EVAL)
    if not sol.success:
        return dict(i=seed["i"], fail=sol.message)
    y = sol.y
    u_rot = (y[0] - (1 - MU)) + 1j * y[1]
    v_rot = y[2] + 1j * y[3]
    t = sol.t
    uin, vin = rot_to_inert(u_rot, v_rot, t)
    a_os, e_os, z = osc(uin, vin)
    # class from the final state: escaped iff unbound or far outside the Hill sphere
    r_fin = np.abs(u_rot[-1])
    escaped = bool(a_os[-1] <= 0.0 or r_fin > 2.0 * RH)
    if mode == "chaos":
        return dict(i=seed["i"], escaped_b=escaped)
    return dict(i=seed["i"], escaped_a=escaped, nfev=int(sol.nfev),
                z=z.astype(np.complex64), u=u_rot.astype(np.complex64),
                a_os=float(a_os[-1]), e_os=float(e_os[-1]),
                esc_win=bool(np.max(np.abs(u_rot[:int(40 * np.pi / DT)])) > 1.5 * RH))


def main():
    seeds = make_seeds()
    jobs = [(s, "main") for s in seeds] + [(s, "chaos") for s in seeds]
    with Pool(4) as p:
        outs = p.map(run_seed, jobs)
    main_o = {o["i"]: o for o in outs if "escaped_a" in o}
    chaos_o = {o["i"]: o for o in outs if "escaped_b" in o}
    truth = []
    for i in sorted(main_o):
        a, b = main_o[i], chaos_o[i]
        truth.append(dict(i=i, aRH=seeds[i]["aRH"], retro=seeds[i]["retro"],
                          w0=seeds[i]["w0"], e0=seeds[i]["e0"],
                          tau=2.0 / 3.0 * (seeds[i]["aRH"] * (1 + seeds[i]["e0"])) ** 3,
                          escaped=a["escaped_a"], chaotic=bool(a["escaped_a"] != b["escaped_b"]),
                          esc_win=a["esc_win"], nfev=a["nfev"],
                          a_os=a["a_os"], e_os=a["e_os"]))
    with open("truth.json", "w") as f:
        json.dump(truth, f, indent=1)
    # shards of the time series (u on the fine grid, z on every 4th sample)
    ts = T_EVAL[::4]
    for k in range(4):
        idx = range(k * 64, (k + 1) * 64)
        np.savez_compressed(f"truth_shard{k}.npz", t=ts,
                            **{f"z{i}": main_o[i]["z"][::4] for i in idx},
                            **{f"u{i}": main_o[i]["u"] for i in idx})
    tot = sum(r["nfev"] for r in truth)
    print(f"truth: {len(truth)} seeds, chaotic {sum(r['chaotic'] for r in truth)}, "
          f"escaped {sum(r['escaped'] for r in truth)}, nfev total {tot} "
          f"(~{tot // 12} steps)")


if __name__ == "__main__":
    main()
