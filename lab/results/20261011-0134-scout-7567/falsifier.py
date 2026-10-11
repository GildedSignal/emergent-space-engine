#!/usr/bin/env python3
"""Falsifier: can ANY statistic separate bounded from compounding error on chaotic ships?

Faithful synthetic port of xtask/src/behave/laws.rs (B12's planted faults) onto B12's exact
sample geometry (xtask/src/behave/handoff.rs): 16 ships, 200 planet periods, one sample per
P/8 => 1601 samples, ~40 planet encounters (entries into 3 R_H), chaotic semimajor-axis
diffusion clipped by the C_J level set (zero-velocity cap). Horizons 1x (the gate's) and 10x
(law-only; the oracle is not needed: C_J is computable from the law's own states).

Laws (error series per ship, relative to |C0|):
  echo     |N(0,1e-13)|                       float noise, below the gate's 1e-12 floor
  const    3e-8 + noise                       positive control (bounded, no structure)
  bounded  1e-7 * (a(t)-a0)/(R_H/sep) + noise Fault::Bounded (BOUNDED=1e-7), state-only
  compound 1e-7 * cumsum(unit steps/encounter) Fault::Compound, walk in encounter count
  drift    1e-13 * j^1.1 * wobble             Fault::Drift (reference DP rtol 1e-12); shape UNVERIFIED
  kick     (1+1e-3)^n_enc - 1                 Fault::Kick (KICK=1e-3 per SOI entry, compounding)
  leak[e]  bounded + e*cumsum(unit steps)     the discriminating case: leak under bounded noise

Statistics:
  exp      exact port of fit::growth_exponent + B12's shipped rule
  allan    overlapping Allan-deviation slope (white <= 0, walk +1/2, drift +1)
  rank     one-sided Mann-Whitney halves growth score z_g = -z per ship, panel k >= 3/16
  horizon  law-only 10x run: derived-cap + max-err growth ratio
           (cap = 1e-7 * A_CAP, the accessible state range on the C_J level set;
            PASS iff median ratio <= 2 and worst max err <= 1.05 * cap)
"""
import json
import numpy as np

RNG_MASTER = np.random.default_rng(20261011)
NSHIPS, PERIODS, COARSE = 16, 200, 8
FLOOR, ERR_MAX, GROWTH_MAX = 1e-12, 1e-4, 0.2
A_CAP = 5.0            # accessible |a-a0| on the C_J level set, in R_H/sep units
NENC = 40              # entries into 3 R_H over the 1x horizon
CAP = 1e-7 * A_CAP     # derived cap for the bounded-mechanism class (BOUNDED=1e-7)


def ship_error_models(n_samples: int, n_enc: int, seed: int):
    """Per-ship latent processes, shared across laws (the same chaotic ship for every law)."""
    rng = np.random.default_rng(seed)
    enc = np.sort(rng.choice(np.arange(1, n_samples), size=n_enc, replace=False))
    is_enc = np.zeros(n_samples, bool)
    is_enc[enc] = True
    a = np.empty(n_samples)                      # chaotic diffusion of a, clipped by the level set
    x = 0.0
    for j in range(n_samples):
        x += rng.standard_normal() * (0.3 if is_enc[j] else 0.02)
        x = np.clip(x, -A_CAP, A_CAP)
        a[j] = x
    noise = np.abs(rng.standard_normal(n_samples)) * 1e-13
    steps = np.where(is_enc, rng.standard_normal(n_samples), 0.0)
    return a, noise, np.cumsum(steps), np.cumsum(is_enc.astype(float))


def law(name: str, e: float, a, noise, walk, nkick):
    n = len(a)
    j = np.arange(n, dtype=float)
    if name == "echo":
        return noise.copy()
    if name == "const":
        return 3e-8 + noise
    if name == "bounded":
        return np.abs(1e-7 * a) + noise
    if name == "compound":
        return 1e-7 * np.abs(walk) + noise
    if name == "drift":
        return 1e-13 * np.power(j + 1.0, 1.1) * (0.8 + 0.2 * np.sin(0.05 * j)) + noise
    if name == "kick":
        return np.power(1.0 + 1e-3, nkick) - 1.0
    if name == "leak":
        return np.abs(1e-7 * a) + e * np.abs(walk) + noise
    raise ValueError(name)


def growth_exponent(err):
    """Exact port of xtask/src/behave/fit.rs."""
    err = np.asarray(err, float)
    n = err.size
    first = max(n // 10, 1)
    if n <= first or not np.isfinite(err).all():
        return float("nan")
    windows, used, pts = 16, 0, []
    for w in range(windows):
        a_idx = int(round(first * (n / first) ** (w / windows)))
        b = n if w == windows else int(round(first * (n / first) ** ((w + 1) / windows)))
        if b <= a_idx:
            continue
        used += 1
        top = np.abs(err[a_idx:b]).max()
        if top > 0.0:
            pts.append((np.log(np.sqrt(a_idx * (b - 1))), np.log(top)))
    if used < windows // 2 or len(pts) < 3:
        return 0.0 if not pts else float("nan")
    p = np.array(pts)
    return float(np.polyfit(p[:, 0], p[:, 1], 1)[0])


def allan_slope(err):
    x = np.asarray(err, float)
    n = x.size
    taus, sig = [], []
    for m in range(1, n // 8):
        d = x[2 * m:] - 2 * x[m:n - m] + x[:n - 2 * m]
        s = np.sqrt((d ** 2).sum() / (2.0 * (n - 2 * m)))
        if s > 0:
            taus.append(m)
            sig.append(s)
    t, s = np.log(np.array(taus, float)), np.log(np.array(sig))
    return float(np.polyfit(t, s, 1)[0])


def mw_halves_z(x):
    """Mann-Whitney z of first half vs second half (positive: first half larger)."""
    x = np.asarray(x, float)
    h = x.size // 2
    a, b = x[:h], x[h:]
    allv = np.concatenate([a, b])
    order = allv.argsort(kind="mergesort")
    ranks = np.empty_like(order, float)
    ranks[order] = np.arange(1, allv.size + 1)
    sv = allv[order]
    i = 0
    while i < sv.size:
        j2 = i
        while j2 + 1 < sv.size and sv[j2 + 1] == sv[i]:
            j2 += 1
        if j2 > i:
            ranks[order[i:j2 + 1]] = (i + j2 + 2) / 2.0
        i = j2 + 1
    u = ranks[:h].sum() - h * (h + 1) / 2.0
    n1, n2 = h, x.size - h
    _, counts = np.unique(allv, return_counts=True)
    tie = (counts ** 3 - counts).sum()
    var = n1 * n2 / 12.0 * ((x.size + 1) - tie / (x.size * (x.size - 1)))
    return float((u - n1 * n2 / 2.0) / np.sqrt(var))


def b12_gate(ships):
    exps, maxe = [], 0.0
    for err in ships:
        maxe = max(maxe, float(np.abs(err).max()))
        if np.abs(err).max() > FLOOR:
            exps.append(growth_exponent(err))
    med = float(np.median(exps)) if exps else 0.0
    return ("PASS" if med <= GROWTH_MAX and maxe <= ERR_MAX else "FAIL"), med, maxe


def allan_gate(ships):
    slopes = [allan_slope(e) for e in ships]
    med = float(np.median(slopes))
    maxe = max(float(np.abs(e).max()) for e in ships)
    return ("PASS" if med < 0.25 and maxe <= ERR_MAX else "FAIL"), med, maxe


def rank_gate(ships):
    """z_g = -MW_z(|err|): positive means the second half is stochastically larger."""
    zs = [-mw_halves_z(np.abs(e)) for e in ships]
    k = sum(z > 1.96 for z in zs)
    return ("FAIL" if k >= 3 else "PASS"), float(np.median(zs)), k


def horizon_gate(ships, maxima_1x):
    ratios = [float(np.abs(e).max()) / max(m, 1e-300) for e, m in zip(ships, maxima_1x)]
    med = float(np.median(ratios))
    worst = max(float(np.abs(e).max()) for e in ships)
    return ("PASS" if med <= 2.0 and worst <= 1.05 * CAP else "FAIL"), med, worst


LAWS_1X = [("echo", 0), ("const", 0), ("bounded", 0), ("compound", 0), ("drift", 0),
           ("kick", 0), ("leak", 1e-9), ("leak", 3e-9), ("leak", 1e-8), ("leak", 3e-8),
           ("leak", 1e-7)]
LAWS_10X = [("echo", 0), ("const", 0), ("bounded", 0), ("compound", 0), ("drift", 0),
            ("kick", 0), ("leak", 1e-9), ("leak", 1e-8), ("leak", 3e-8), ("leak", 1e-7)]


def run(laws, horizon_mult, maxima_1x=None):
    n_samples = PERIODS * COARSE * horizon_mult + 1
    seeds = RNG_MASTER.integers(1, 2 ** 31, size=NSHIPS)  # same latent ships at both horizons
    latents = [ship_error_models(n_samples, NENC * horizon_mult, int(s)) for s in seeds]
    maxima_1x = maxima_1x or {}
    out = {}
    for name, e in laws:
        key = f"{name}:{e:g}"
        ships = [law(name, e, *lat) for lat in latents]
        v1, med_e, maxe = b12_gate(ships)
        v2, med_a, _ = allan_gate(ships)
        v3, med_z, k = rank_gate(ships)
        entry = {
            "exp": {"verdict": v1, "median_exponent": round(med_e, 3), "max_err": maxe},
            "allan": {"verdict": v2, "median_slope": round(med_a, 3)},
            "rank": {"verdict": v3, "median_z": round(med_z, 2), "ships_flagged": k},
        }
        if horizon_mult > 1:
            v4, med_r, worst = horizon_gate(ships, [maxima_1x[key]] * len(ships))
            entry["horizon"] = {"verdict": v4, "median_ratio": round(med_r, 2), "max_err": worst}
        else:
            entry["horizon"] = {"max_err": maxe}
        out[f"{name}" + (f"[{e:g}]" if name == "leak" else "")] = entry
    return out


def main():
    base = run(LAWS_1X, 1)
    m1 = {f"{n}:{e:g}": d["horizon"]["max_err"] for (n, e), d in zip(LAWS_1X, base.values())}
    p10 = run(LAWS_10X, 10, m1)
    result = {"horizon_1x": base, "horizon_10x": p10}
    with open(__file__.replace(".py", "-out.json"), "w") as f:
        json.dump(result, f, indent=1)
    contract = {"echo": "PASS", "const": "PASS", "bounded": "PASS", "compound": "FAIL",
                "drift": "FAIL", "kick": "FAIL", "leak": "FAIL(leak)"}
    for hz in ("horizon_1x", "horizon_10x"):
        print(f"== {hz} ==")
        print(f"{'law':>14} | {'exp':>4} {':med':>6} | {'allan':>5} {':slope':>6} | "
              f"{'rank':>4} {':zg':>6} k | {'cap+ratio':>9} {':r':>5} | contract")
        for name, d in result[hz].items():
            c = contract[name.split("[")[0]]
            h = d["horizon"]
            hv = f"{h.get('verdict', '--'):>9} {str(h.get('median_ratio', '--')):>5}" if "verdict" in h \
                else f"{'--':>9} {'--':>5}"
            print(f"{name:>14} | {d['exp']['verdict']:>4} {d['exp']['median_exponent']:>6} | "
                  f"{d['allan']['verdict']:>5} {d['allan']['median_slope']:>6} | "
                  f"{d['rank']['verdict']:>4} {d['rank']['median_z']:>6} {d['rank']['ships_flagged']} | "
                  f"{hv} | {c}")


if __name__ == "__main__":
    main()
