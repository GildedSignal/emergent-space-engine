#!/usr/bin/env python3
"""Print every dossier number from out/taul.json + out/hlive2.json in one shot."""
import json, math
import numpy as np

m = json.load(open("out/taul.json"))
mm = next(r for r in m if r["cfg"] == "measured")
half = next(r for r in m if r["cfg"] == "dt_half")
ch = np.array(mm["chaotic"]); a0 = np.array(mm["a0"]); tau = np.array(mm["tau_orb"])
print("=== measure_taul (8192 bodies, 1e4 yr) ===")
print(f"chaotic_frac={mm['chaotic_frac']:.5f}  (dt_half: {half['chaotic_frac']:.5f})")
if ch.any():
    print(f"tau_orb chaotic: median={np.median(tau[ch]):.0f} p10={np.percentile(tau[ch],10):.0f} p90={np.percentile(tau[ch],90):.0f}")
    print(f"tau_yr chaotic median={mm['tau_yr_chaotic_median']:.0f}")
print(f"bounded_rms_AU_regular={mm['bounded_rms_AU_regular']:.3g}")
brms = mm["bounded_rms_AU_regular"]
qv = 1.18e-3  # m/s at 2.25 AU
dv = (19856.0/2)*(brms/2.25)
print(f"  -> bounded dv={dv:.3g} m/s = {dv/qv:.3f} quanta")
print(f"e_exceed_cap={mm['e_exceed_cap']:.5f} a_out_of_band={mm['a_out_of_band']:.5f} drift={mm['massive_energy_drift']:.1e}")
print("chaotic fraction by 0.05-AU bin:",
      [f"{2.0+0.05*i:.2f}:{ch[(a0>=2.0+0.05*i)&(a0<2.05+0.05*i)].mean():.3f}" for i in range(10)])

print("=== hlive2 ===")
h = json.load(open("out/hlive2.json"))
print(f"f_chaos={h['measured_scene']['f_chaos']:.5f}")
for r in h["rows"]:
    if r["orbits"] == 2000:
        print(f"{r['cfg']:>16}: scarred={r['scarred_frac']:.5f} bits/body={r['total_bits_per_body']:.4f} tubes={r['tubes']} sigma_q={r['sigma_quanta']:.2f}")
s = h["stock_1e4yr"]
print(f"STOCK measured @1e4yr: scarred={s['scarred_frac_measured']:.6f} bits/scarred={s['bits_per_scarred']:.2f} bits/body={s['total_bits_per_body']:.5f} median_rms={s['rms_quanta_median']:.4f}q p99={s['rms_quanta_p99']:.4f}q tubes={s['tubes']}")
# headline conversions at 1e9
for cfg in ("measured", "assumed300"):
    r = next(x for x in h["rows"] if x["cfg"] == cfg and x["orbits"] == 2000)
    print(f"{cfg}: {r['total_bits_per_body']:.4f} bits/body -> {r['total_bits_per_body']*1e9/8/1e9:.4f} GB at 1e9; tubes {r['tubes']} -> {r['tubes']*(1e9/2**20)*16/1e9:.3f} GB of 16B tubes")
