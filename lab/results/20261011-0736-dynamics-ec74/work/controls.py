"""Controls: (a) K=6 neighbour pruning vs brute-force O(N^2) pair check;
(b) sample-rate halving S=128 vs S=256. Run after the sweep."""
import numpy as np, sys
sys.path.insert(0, '.')
import swarm
from swarm import Swarm, TWO_PI, kepler_states

# --- control (a): brute force ---
def step_brute(sw, t, dt):
    a, e, varpi, M0 = sw.a, sw.e, sw.varpi, sw.M0
    x1, y1, vx1, vy1 = kepler_states(a, e, varpi, M0, t - dt)
    x2, y2, vx2, vy2 = kepler_states(a, e, varpi, M0, t)
    n = sw.N
    hits = 0
    b_H = 3.0 * (sw.mu_g / 3.0) ** (1/3)
    for i in range(n):
        px0 = x1 - x1[i]; py0 = y1 - y1[i]; ux0 = vx1 - vx1[i]; uy0 = vy1 - vy1[i]
        px = x2 - x2[i]; py = y2 - y2[i]; ux = vx2 - vx2[i]; uy = vy2 - vy2[i]
        s0 = px0 * ux0 + py0 * uy0
        s1 = px * ux + py * uy
        cross = (s0 < 0) & (s1 >= 0)
        cross[i] = False
        u = np.hypot(ux, uy)
        b = np.abs(px * uy - py * ux) / np.maximum(u, 1e-14)
        sel = cross & (b < b_H)
        for j in np.nonzero(sel)[0]:
            if j < i:
                continue
            hits += 1
    return hits

psi = 3e-4
N, W, SE, S = 150, 0.04, 0.04, 128
T_orb = 30
A = Swarm(N=N, w=W, sigma_e=SE, m=psi*SE**3/2, seed=3)
B = Swarm(N=N, w=W, sigma_e=SE, m=psi*SE**3/2, seed=3)
dt = TWO_PI / S
ha = hb = 0
t = 0.0
for step in range(T_orb * S):
    t += dt
    ha += A.step_all(t, dt, K=6)
    hb += step_brute(B, t, dt)
print(f"control (a) neighbour K=6 vs brute force over {T_orb} orbits: "
      f"{ha} vs {hb} impulses ({100*ha/max(hb,1):.1f}%)")

# --- control (b): sample rate ---
from swarm import run_swarm
for S in [128, 256]:
    sw, res = run_swarm(3e-4, N=200, w=W, sigma_e=SE, T_orbits=60, S=S, K=6, seed=0)
    chi = np.array([l[3] for l in res["log"]])
    strong = (chi >= 0.3).sum()
    print(f"control (b) S={S}: impulses={len(res['log'])} strong={strong} "
          f"rate={strong/200/60:.2e} sig_e {res['sig_e'][0]:.4f}->{res['sig_e'][-1]:.4f} "
          f"sig_a {res['sig_a'][0]:.4f}->{res['sig_a'][-1]:.4f}")
