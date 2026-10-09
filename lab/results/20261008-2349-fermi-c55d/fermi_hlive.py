#!/usr/bin/env python3
# Fermi audit of H_live (distinctions per game-second) for the 10^9-bodies-in-8GB goal.
# Deterministic (seeded), stdlib only, < 60 s. Units: belt units, GM_sun = a0 = v_K(a0) = 1.
# Run: python3 fermi_hlive.py            (prints tables; writes fermi_hlive.json)
import math, random, json

RNG = random.Random(20261008)

# ---------------------------------------------------------------- A. exact scattering
def dv_impulse(b, b90, vrel):
    """Exact |delta-v| of a two-body flyby (hyperbola): tan(Theta/2) = b90/b."""
    return 2.0 * vrel * b90 / math.sqrt(b * b + b90 * b90)

# ---------------------------------------------------------------- B. control (positive)
def elements_from_state(r, v, GM=1.0):
    r0 = math.hypot(*r); v2 = v[0]*v[0] + v[1]*v[1]
    E = v2/2 - GM/r0
    a = -GM/(2*E)
    h = r[0]*v[1] - r[1]*v[0]
    e = math.sqrt(max(0.0, 1 + 2*E*h*h/(GM*GM)))
    return a, e

def control_impulse_to_elements(n=200):
    """Linearized da/a = 2 dv_t/vK vs exact Kepler elements after an impulse."""
    worst = 0.0
    for _ in range(n):
        a0, vK = 1.0, 1.0
        th = RNG.random() * 2 * math.pi
        r = (a0 * math.cos(th), a0 * math.sin(th))
        t_hat = (-math.sin(th), math.cos(th))
        v = (-vK * math.sin(th), vK * math.cos(th))
        ang = RNG.random() * 2 * math.pi
        mag = 10.0 ** (RNG.uniform(-9, -4)) * vK
        dv = (mag * math.cos(ang), mag * math.sin(ang))
        dv_t = dv[0]*t_hat[0] + dv[1]*t_hat[1]
        lin = 2.0 * dv_t / vK
        a1, _ = elements_from_state(r, (v[0]+dv[0], v[1]+dv[1]))
        exact = (a1 - a0) / a0
        scale = max(abs(lin), abs(exact), 1e-300)
        worst = max(worst, abs(lin - exact) / scale if scale > 0 else 0.0)
    return worst

# ---------------------------------------------------------------- C. scar random walk
def sigma_step(mratio, rho, vrel):
    """RMS |da/a| step of the zero-mean walk: exact E[dv^2] over p(b)=2b/rho^2
    and uniform impulse direction (E[cos^2]=1/2), times 2 dv_t/vK."""
    b90 = mratio / (vrel * vrel)
    e_dv2 = (4.0 * vrel*vrel * b90*b90 / (rho*rho)) * math.log((rho*rho + b90*b90) / (b90*b90))
    return math.sqrt(e_dv2)              # sqrt(E[(2 dv cos)^2]) = sqrt(4 * 1/2 * E[dv^2])

def scar_horizon(mratio, rho, vrel, q, rate):
    """Mean orbits until |cumulative da/a| first crosses quantum q.
    First passage of a zero-mean walk: E[T_steps] = (q/sigma)^2, clamped at >= 1 step."""
    s = sigma_step(mratio, rho, vrel)
    if s == 0.0:
        return math.inf
    return max(1.0, (q / s) ** 2) / rate

def scar_horizon_mc(mratio, rho, vrel, q, rate, nsteps_cap=2_000_000, nsamp=48):
    """Capped Monte-Carlo control (median)."""
    b90 = mratio / (vrel * vrel)
    def step():
        b = rho * math.sqrt(RNG.random())
        return 2.0 * dv_impulse(b, b90, vrel) * math.cos(RNG.random() * math.pi)
    out = []
    for _ in range(nsamp):
        x, n = 0.0, 0
        while n < nsteps_cap:
            n += 1
            x += step()
            if abs(x) > q:
                break
        out.append(n / rate if abs(x) > q else math.inf)
    out.sort()
    return out[len(out)//2]

# ---------------------------------------------------------------- D. rates
# Truth rates measured by the repo's own instrument on this checkout:
# cargo run --release -p emergent-encounters --bin encounters -- verify a / d
TRUTH = {  # belt -> (truth_enc, n, orbits, sigma_e, rho)
    "s1e-3-r1e-4": (35, 1000, 200, 1e-3, 1e-4),
    "s3e-3-r1e-4": (68, 1000, 100, 3e-3, 1e-4),
    "s1e-2-r1e-4": (189, 1000, 100, 1e-2, 1e-4),
    "s3e-2-r1e-4": (248, 1000, 50, 3e-2, 1e-4),
    "n3000-r3e-4": (1042, 3000, 20, 1e-2, 3e-4),
}
TRUTH_RATE = {k: e / (n * t) for k, (e, n, t, _, _) in TRUTH.items()}

def analytic_rate(N, sigma_e, rho, a_lo=1.0, a_hi=1.5):
    """2-D flat-belt swept-tube estimate: linear density of band-crossing neighbours
    along the path, x tube width 2 rho, x epicyclic crossing speed, x local period."""
    a_bar = 0.5 * (a_lo + a_hi)
    e_rms = sigma_e * math.sqrt(2.0)
    n_a = N / (a_hi - a_lo)
    band = 2.0 * a_bar * e_rms
    neigh = n_a * 2 * band
    lam = neigh / (2.0 * math.pi * a_bar)
    vrel = math.sqrt(2.0) * e_rms
    T = 2.0 * math.pi / (a_bar ** -1.5)  # local period T = 2 pi a^{3/2}
    return lam * (2.0 * rho) * vrel * T

# ---------------------------------------------------------------- E. the 10^9 budget
def budget(r_enc, mratio_ship=1e-27, mratio_ceres=1e-12):
    out = {}
    out["program_bits_per_body"] = 0.126            # lab gold components-98bc
    out["programs_MB_at_1e9"] = 0.126 * 1e9 / 8 / 1e6
    out["tubes_if_all_MB_at_1e9"] = 16e9 / 1e6      # 16-byte tube each
    out["max_exception_fraction_4GiB"] = 4 * 1024**3 / 16e9
    vrel = 0.02
    for tag, mr in (("ship", mratio_ship), ("ceres", mratio_ceres)):
        b90 = mr / vrel**2
        d = sorted(2 * dv_impulse(1e-4 * math.sqrt(RNG.random()), b90, vrel) for _ in range(4096))
        out[f"da_over_a_median_{tag}"] = d[len(d)//2]
        out[f"da_over_a_p99_{tag}"] = d[int(0.99*len(d))]
    P_s = 3.156e7                                   # game-seconds per 1-AU orbit
    kicks_per_gs = 1e9 * 32 / P_s
    out["kicks_per_game_second_1e9_1AU"] = kicks_per_gs
    out["kick_cores_rtf100_at_300ns"] = kicks_per_gs * 100 * 300e-9
    # Two density scenarios at 1e9 (rate per body ∝ linear density along the path):
    out["enc_per_gs_fixed_density"] = 1e9 * r_enc / P_s * 100          # belt widens with N
    out["enc_per_gs_fixed_extent"] = 1e9 * r_enc * 1e6 / P_s * 100     # 1e9 in the same belt
    out["enc_cores_fixed_extent_unamortized"] = out["enc_per_gs_fixed_extent"] * 4200 * 50e-9
    out["enc_cores_fixed_density_amortized"] = out["enc_per_gs_fixed_density"] * 1.2 * 50e-9
    rho_phys = 1.0 / 1.496e11                       # 1 m at 1 AU
    r_contact = r_enc * (rho_phys / 1e-4) ** 2
    out["ship_contact_perbody_orbit"] = r_contact
    out["ship_contacts_per_gs_1e9_rtf100"] = 1e9 * r_contact / P_s * 100
    out["player_bits_per_game_second_rtf100"] = 100 * 10 / 100
    return out

def main():
    res = {}
    res["control_impulse_vs_exact_worst_relerr"] = control_impulse_to_elements()
    for N, se, rho, tag in ((1000, 1e-2, 1e-4, "s1e-2-r1e-4"), (1000, 1e-3, 1e-4, "s1e-3-r1e-4"), (3000, 1e-2, 3e-4, "n3000-r3e-4")):
        res[f"analytic_rate_{tag}"] = analytic_rate(N, se, rho)
        res[f"truth_rate_{tag}"] = TRUTH_RATE[tag]
    base_rate = TRUTH_RATE["s1e-2-r1e-4"]
    res["base_rate_per_body_orbit"] = base_rate
    for mr in (1e-27, 1e-21, 1e-15, 1e-12, 1e-10, 1e-8):
        res[f"sigma_step_m{mr:.0e}"] = sigma_step(mr, 1e-4, 0.02)
        res[f"scar_horizon_orbits_m{mr:.0e}_q1e-9"] = scar_horizon(mr, 1e-4, 0.02, 1e-9, base_rate)
        res[f"scar_horizon_orbits_m{mr:.0e}_q1e-12"] = scar_horizon(mr, 1e-4, 0.02, 1e-12, base_rate)
    res["scar_mc_control_m1e-12_q1e-12"] = scar_horizon_mc(1e-12, 1e-4, 0.02, 1e-12, base_rate)
    res["scar_analytic_m1e-12_q1e-12"] = scar_horizon(1e-12, 1e-4, 0.02, 1e-12, base_rate)
    res["budget"] = budget(base_rate)
    print(json.dumps(res, indent=1, default=str))
    with open("fermi_hlive.json", "w") as f:
        json.dump(res, f, indent=1, default=str)

if __name__ == "__main__":
    main()
