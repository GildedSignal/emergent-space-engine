"""Binary metrics for rung r3 v3, all four configurations.

Ingestion (frozen by gate B11, "given their 1PN invariants", and by
schwarzschild_from_invariants' own comment: "Matching invariants avoids
equating harmonic and Schwarzschild radial coordinates"):
  each seed (p, e, nu) -> 1PN invariants (H, J) = eih_invariants(p, e, nu),
  and every doll consumes invariants, never the raw harmonic (p, e).

  eob-doll: E_eff = 1 + H + (nu/2) H^2  (the exact inverse of the frozen energy
    map E_real = M*sqrt(1+2 nu (E_eff-1)) with E_real = M(1+nu H)), L_eff = J,
    exact Schwarzschild geodesic with those invariants (Darwin p_eff, e_eff),
    T_law = T_eff * (1+nu H)  [the map's frequency rescaling; the square root
    equals 1+nu H identically by the inversion].
  test-mass: nu ignored, lighter body on a fixed m1 = M(1+sqrt(1-4 nu))/2, no
    invariant matching (the naive reading of "orbits a fixed M = m1").
  newton-doll: Kepler orbit with the same (H, J): a = -1/(2H), T = 2 pi a^1.5.

Truncation rule (rung v3, "the relative size of the next post-Newtonian term"):
  period: next-term estimate 5/a^2 with a = p/(1-e^2) (the integrator's own B11
    precedent), excluded above half the 0.1% tolerance, i.e. judged iff a >= 100.
  nu: the nu-term is itself a 1PN correction; its next term is 5/a^2 of the
    period = 5/a of the nu-term, excluded above half the 10% tolerance: a >= 100.
  precession: rung-defined band (0.01 + 2*8/p), all seeds judged.
"""
import json
import math

from common import (bound_constants, schw_advance, schw_period_t, oracle_1pn,
                    sample_cases)


def eih_invariants_safe(p, e, nu):
    from common import eih_invariants
    if e > 1e-12:
        return eih_invariants(p, e, nu)
    j0 = math.sqrt(p)  # e -> 0 limit of dj (0/0 in the frozen formula)
    dcorr = ((1.0 - 3.0 * nu) * j0 ** 4 / (2.0 * p ** 5)
             + 3.0 * (3.0 + nu) * j0 * j0 / (2.0 * p ** 4) - 1.0 / p ** 3)
    dj = dcorr * p ** 3 / (2.0 * j0)
    vt = (j0 + dj) / p * (1.0 - 0.5 * (1.0 - 3.0 * nu) * j0 * j0 / (p * p) - (3.0 + nu) / p)
    v2 = vt * vt
    energy = (0.5 * v2 - 1.0 / p + 0.375 * (1.0 - 3.0 * nu) * v2 * v2
              + 0.5 / p * ((3.0 + nu) * v2 + 1.0 / p))
    angular = p * vt * (1.0 + 0.5 * (1.0 - 3.0 * nu) * v2 + (3.0 + nu) / p)
    return p, vt, energy, angular


def oracle_safe(p, e, nu):
    _, _, energy, angular = eih_invariants_safe(p, e, nu)
    q = -2.0 * energy
    n = q ** 1.5 * (1.0 + q * (-15.0 + nu) / 8.0)
    return 6.0 * math.pi / (angular * angular), 2.0 * math.pi / n


def schw_from_invariants(binding, angular, p_guess):
    """Port of schwarzschild_from_invariants (stable outer bound root)."""
    l2 = angular * angular
    e2 = (1.0 + binding) ** 2
    p = p_guess
    for _ in range(60):
        f = (l2 + 4.0) / p - 8.0 * l2 / (p * p) + 16.0 * l2 / p ** 3 - e2
        df = -(l2 + 4.0) / (p * p) + 16.0 * l2 / p ** 3 - 48.0 * l2 / p ** 4
        step = f / df
        p -= step
        if abs(step) < 2e-14 * p:
            break
    return p, math.sqrt(max(p - 3.0 - p * p / l2, 0.0))


def eob_doll(p, e, nu, cache={}):
    key = (p, e, nu)
    if key in cache:
        return cache[key]
    _, _, H, J = eih_invariants_safe(p, e, nu)
    E_eff = 1.0 + H + 0.5 * nu * H * H
    pef, eef = schw_from_invariants(E_eff - 1.0, J, p)
    adv = schw_advance(pef, eef)
    T = schw_period_t(pef, eef) * (1.0 + nu * H)
    cache[key] = (adv, T, pef, eef)
    return cache[key]


def main():
    binaries, b_assist = sample_cases()

    rows = []
    for (p, e, nu) in binaries:
        a = p / (1.0 - e * e)
        adv_or, T_or = oracle_safe(p, e, nu)
        _, T_or0 = oracle_safe(p, e, 0.0)
        d_or = T_or / T_or0 - 1.0
        judged_period = (5.0 / (a * a)) <= 5.0e-4
        judged_nu = (5.0 / a) <= 0.05 and nu >= 0.05

        adv_eob, T_eob, pef, eef = eob_doll(p, e, nu)
        _, T_eob0, _, _ = eob_doll(p, e, 0.0)
        d_eob = T_eob / T_eob0 - 1.0

        f1 = 0.5 * (1.0 + math.sqrt(1.0 - 4.0 * nu))  # m1/M, nu ignored
        adv_tm = schw_advance(p / f1, e)
        T_tm = f1 * schw_period_t(p / f1, e)
        _, _, H0, J0 = eih_invariants_safe(p, e, nu)
        d_tm = T_tm / schw_period_t(p, e) - 1.0

        adv_nw = 0.0
        T_nw = 2.0 * math.pi * (-1.0 / (2.0 * H0)) ** 1.5  # Kepler from invariants
        d_nw = 0.0

        rows.append(dict(p=p, e=e, nu=nu, a=a, adv_or=adv_or, T_or=T_or, d_or=d_or,
                         judged_period=judged_period, judged_nu=judged_nu,
                         adv_eob=adv_eob, T_eob=T_eob, d_eob=d_eob, p_eff=pef,
                         adv_tm=adv_tm, T_tm=T_tm, d_tm=d_tm,
                         adv_nw=adv_nw, T_nw=T_nw, d_nw=d_nw))

    with open("binaries.json", "w") as f:
        json.dump(rows, f)

    def fractions(adv, T, d):
        prec = sum(abs(adv[i] - rows[i]["adv_or"]) <= (0.01 + 16.0 / rows[i]["p"]) * abs(rows[i]["adv_or"])
                   for i in range(len(rows))) / len(rows)
        jp = [i for i, r in enumerate(rows) if r["judged_period"]]
        per = sum(abs(T[i] - rows[i]["T_or"]) <= 1e-3 * abs(rows[i]["T_or"]) for i in jp) / len(jp)
        jn = [i for i, r in enumerate(rows) if r["judged_nu"]]
        nu_pass = sum(1 for i in jn
                      if (d[i] > 0) == (rows[i]["d_or"] > 0)
                      and abs(d[i] - rows[i]["d_or"]) <= 0.1 * abs(rows[i]["d_or"]))
        return prec, per, nu_pass / len(jn), len(jp), len(jn)

    n_period = sum(1 for r in rows if r["judged_period"])
    n_nu = sum(1 for r in rows if r["judged_nu"])
    out = {}
    for name, adv, T, d in [
        ("eob-doll", [r["adv_eob"] for r in rows], [r["T_eob"] for r in rows], [r["d_eob"] for r in rows]),
        ("oracle", [r["adv_or"] for r in rows], [r["T_or"] for r in rows], [r["d_or"] for r in rows]),
        ("test-mass", [r["adv_tm"] for r in rows], [r["T_tm"] for r in rows], [r["d_tm"] for r in rows]),
        ("newton-doll", [r["adv_nw"] for r in rows], [r["T_nw"] for r in rows], [r["d_nw"] for r in rows]),
    ]:
        prec, per, nup, jp, jn = fractions(adv, T, d)
        out[name] = dict(precession_pass_fraction=prec, period_pass_fraction=per,
                         nu_effect_pass_fraction=nup, min_judged_seeds=min(n_period, n_nu))
        print(f"{name:12s} prec={prec:.4f} period={per:.4f} nu={nup:.4f} "
              f"(judged period {jp}, nu {jn})")
    with open("binaries_summary.json", "w") as f:
        json.dump(out, f, indent=1)

    jn = [i for i, r in enumerate(rows) if r["judged_nu"]]
    fails = [(rows[i]["p"], rows[i]["e"], rows[i]["nu"], rows[i]["d_or"], rows[i]["d_eob"])
             for i in jn if not ((rows[i]["d_eob"] > 0) == (rows[i]["d_or"] > 0)
                                 and abs(rows[i]["d_eob"] - rows[i]["d_or"]) <= 0.1 * abs(rows[i]["d_or"]))]
    print(f"nu fails: {len(fails)} of {len(jn)}; worst few:")
    for f_ in sorted(fails, key=lambda t: -abs(t[4] / t[3] if t[3] else 9))[:6]:
        print(f"   p={f_[0]:.0f} e={f_[1]:.2f} nu={f_[2]:.3f} d_or={f_[3]:+.3e} d_law={f_[4]:+.3e}")


if __name__ == "__main__":
    main()
