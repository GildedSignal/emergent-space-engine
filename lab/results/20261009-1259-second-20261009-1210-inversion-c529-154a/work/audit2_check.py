#!/usr/bin/env python3
"""Independent audit of the G1c worst watch-miss pair (run ...-154a).
Bodies dumped from refresh-b.jsonl (worst event, truncated to the digits shown).
Independent Kepler solver (Newton on E); no crate code.
Checks: (1) the encounter is real (min distance < rho=1e-4), (2) it recurs at
near-fixed phase, (3) at contact the mean-longitude gap is ~6 spacings (the
watch miss) while true longitudes nearly coincide (EoC cancellation), and the
gap is near-frozen (the two periods differ by ~5e-6 relative).
"""
import json, math

TAU = 2 * math.pi

def bodies():
    for line in open("refresh-b.jsonl"):
        o = json.loads(line)
        if o["scene"] == "G1c-goldfleet-e10x":
            return o["rho"], o["worst"][0]

def state(a, e, pom, lam0, n, t):
    # mean longitude is linear: lam = lam0 + n*t ; M = lam - pom
    M = (lam0 + n * t - pom + math.pi) % TAU - math.pi
    E = M
    for _ in range(60):
        f = E - e * math.sin(E) - M
        fp = 1 - e * math.cos(E)
        d = f / fp
        E -= d
        if abs(d) < 1e-15:
            break
    x = a * (math.cos(E) - e)
    y = a * math.sin(E) * math.sqrt(1 - e * e)
    ca, sa = math.cos(pom), math.sin(pom)
    lam_true = math.atan2(y, x)
    return (ca * x - sa * y, sa * x + ca * y), lam_true

rho, w = bodies()
a_i, e_i, pom_i, lam_i = w["a_i"], w["e_i"], w["pom_i"], w["lam0_i"]
a_j, e_j, pom_j, lam_j = w["a_j"], w["e_j"], w["pom_j"], w["lam0_j"]
# mean motions from Kepler's third law (n = 2*pi/period, period = a^1.5)
n_i, n_j = 1 / a_i**1.5, 1 / a_j**1.5  # crate: n = TAU*TICKS/period = a^-1.5 rad/time-unit

horizon = 100 * TAU
STEP = 4e-4
t = 0.0
# local minima of the pair distance (coarse scan at 2e-4, ~500 samples per contact)
prev = prev2 = None
minima = []
while t < horizon:
    (xi, yi), _ = state(a_i, e_i, pom_i, lam_i, n_i, t)
    (xj, yj), _ = state(a_j, e_j, pom_j, lam_j, n_j, t)
    d = math.hypot(xi - xj, yi - yj)
    if prev2 is not None and prev < prev2 and prev <= d and prev < 10 * rho:
        minima.append((t - STEP, prev))
    prev2, prev = prev, d
    t += STEP

sub = [m for m in minima if m[1] < rho]
dmin = min((d for _, d in minima), default=float("inf"))
spacing = TAU / 300
t0 = sub[0][0] if sub else minima[0][0]
gli = (lam_i + n_i * t0) % TAU
glj = (lam_j + n_j * t0) % TAU
gap = min((gli - glj) % TAU, (glj - gli) % TAU)
gap_spacings = gap / spacing
# true-ANOMALY separation at the same instant (perifocal atan2); at contact the true
# LONGITUDES coincide by construction (d < rho), so f_i - f_j ~= -(pom_i - pom_j).
(_, lti) = state(a_i, e_i, pom_i, lam_i, n_i, t0)
(_, ltj) = state(a_j, e_j, pom_j, lam_j, n_j, t0)
tsep = min((lti - ltj) % TAU, (ltj - lti) % TAU)
# gap drift over the horizon (nearly frozen?)
gap_end = min(((lam_i + n_i * horizon) - (lam_j + n_j * horizon)) % TAU,
              ((lam_j + n_j * horizon) - (lam_i + n_i * horizon)) % TAU)
print(json.dumps({
    "pair": [w["i"], w["j"]],
    "rho": rho,
    "sub_rho_minima": len(sub),
    "d_min": dmin,
    "rust_d_at_event": w["d"],
    "rust_rank_lam": w["rank_lam"],
    "mean_lam_gap_at_contact_spacings": round(gap_spacings, 2),
    "true_anomaly_sep_at_contact_rad": tsep, "pom_diff_rad": (pom_i - pom_j) % TAU,
    "gap_drift_over_100_orbits_spacings": round(abs(gap_end - gap) / spacing, 3),
    "period_ratio_minus_1": a_j**1.5 / a_i**1.5 - 1,
}, indent=1))
