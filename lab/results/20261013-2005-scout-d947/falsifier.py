#!/usr/bin/env python3
"""Falsifier: what must a gravity-news version carry — (x,v), (x,v,a) or (x,v,a,j)?

Toy = Carlip's Lorentz-invariant scalar retarded gravity (gr-qc/9909087 §3, eq. 3.1):
  F = (gamma*M / r_inv^2) * [ v_R - ((1-v_R^2)/(1-n.v_R)) * n ]
  r_inv = gamma*R*(1 - n.v_R),  n = (x_c - x_s(t_r))/R,  R = |x_c - x_s(t_r)|,
  t_r solved from t - t_r = |x_c(t) - x_s(t_r)| (true trajectory, all arms common).
Source: analytic thrust program x(t) = (a0*t^2/2 + j*t^3/6, 0). Consumer: circular
orbit at beta_c. Versions every T; arm reconstructs the source's retarded state from
the newest version (t_v = T*floor(t_r/T)) by Taylor order 1/2/3. Oracle arm uses the
exact retarded state. 'now1' arm = order-1 reconstruction read as-if-current (the
no-retardation tube readout). Scar per rebind = |E_arm - E_oracle| growth per window.
Units G=M=c=1. Pure stdlib. Deterministic.
"""
import json, math, sys

def run(beta, T_frac, a0, jerk, order, h_frac=1024.0, t_run_P=1.0, readout="ret"):
    r0 = 1.0 / beta**2                 # circular radius
    v0 = beta                          # circular speed
    P = 2.0 * math.pi / beta**3        # period
    T = T_frac * P
    h = P / h_frac
    n_steps = int(round(t_run_P * P / h))
    L = r0                             # nominal light delay

    def src(t):                        # analytic source state
        return ((0.5*a0*t*t + jerk*t*t*t/6.0, 0.0),
                (a0*t + 0.5*jerk*t*t, 0.0),
                (a0 + jerk*t, 0.0))

    def retarded_t(t, xc):
        tr = t - math.hypot(xc[0], xc[1])
        for _ in range(6):
            xs, _, _ = src(tr)
            tr = t - math.hypot(xc[0]-xs[0], xc[1]-xs[1])
        return tr

    def field(t, xc, order, readout):
        # versions live on the light cone: t_r is solved on the true trajectory
        # (common to all arms); "now" = newest ARRIVED version read as-if-current
        # (the no-retardation tube readout), so its staleness is >= the light delay.
        tr = retarded_t(t, xc)
        tv = T*math.floor(tr/T)
        d = (t - tv) if readout == "now" else (tr - tv)
        xv, vv, av = src(tv)
        if order >= 2:
            xr = (xv[0]+vv[0]*d+0.5*av[0]*d*d, xv[1]+vv[1]*d+0.5*av[1]*d*d)
            vr = (vv[0]+av[0]*d, vv[1]+av[1]*d)
        else:
            xr = (xv[0]+vv[0]*d, xv[1]+vv[1]*d); vr = vv
        if order >= 3:
            jx, jy = jerk, 0.0            # thrust program is along +x
            xr = (xr[0]+jx*d*d*d/6.0, xr[1]+jy*d*d*d/6.0)
            vr = (vr[0]+0.5*jx*d*d, vr[1]+0.5*jy*d*d)
        if readout == "oracle":
            xr, vr, _ = src(tr)
        R = math.hypot(xc[0]-xr[0], xc[1]-xr[1])
        nx, ny = (xc[0]-xr[0])/R, (xc[1]-xr[1])/R
        v2 = vr[0]*vr[0]+vr[1]*vr[1]
        if v2 > 0.25: return None       # out of toy domain
        g = 1.0/math.sqrt(1.0-v2)
        ndv = nx*vr[0]+ny*vr[1]
        rinv = g*R*(1.0-ndv)
        c = g/(rinv*rinv)
        k = (1.0-v2)/(1.0-ndv)
        return (c*(vr[0]-k*nx), c*(vr[1]-k*ny))

    def deriv(t, s, order, readout):
        f = field(t, (s[0], s[1]), order, readout)
        return (s[2], s[3], f[0], f[1])

    def rk4(s, t, order, readout):
        k1 = deriv(t, s, order, readout)
        s2 = [s[i]+0.5*h*k1[i] for i in range(4)]
        k2 = deriv(t+0.5*h, s2, order, readout)
        s3 = [s[i]+0.5*h*k2[i] for i in range(4)]
        k3 = deriv(t+0.5*h, s3, order, readout)
        s4 = [s[i]+h*k3[i] for i in range(4)]
        k4 = deriv(t+h, s4, order, readout)
        return [s[i]+h/6.0*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(4)]

    def energy(t, s):
        xs, _, _ = src(t)
        return 0.5*(s[2]**2+s[3]**2) - 1.0/math.hypot(s[0]-xs[0], s[1]-xs[1])

    s_or = [r0, 0.0, 0.0, v0]
    s_ar = list(s_or)
    dE_marks = []
    n_win = int(t_run_P*P/T)
    for i in range(n_steps):
        t = i*h
        s_or = rk4(s_or, t, 0, "oracle")
        s_ar = rk4(s_ar, t, order, readout)
        if (i+1) % max(1, n_steps//max(1, n_win)) == 0:
            dE_marks.append(energy(t+h, s_ar)-energy(t+h, s_or))
    # per-rebind scar: mean |dE| growth per window (second half, past transient)
    half = dE_marks[len(dE_marks)//2:] or dE_marks
    growth = [abs(half[i+1]-half[i]) for i in range(len(half)-1)]
    per_rebind = (sum(growth)/len(growth)) if growth else abs(dE_marks[-1])
    # velocity/position remainders at mid-window for the channel bookkeeping
    d_mid = T/2.0
    dv = a0*d_mid + 0.5*jerk*d_mid*d_mid if order < 2 else 0.5*jerk*d_mid*d_mid
    dx = 0.5*a0*d_mid*d_mid + jerk*d_mid**3/6.0 if order < 2 else jerk*d_mid**3/6.0
    return dict(beta=beta, Tf=T_frac, a0=a0, jerk=jerk, order=order,
                readout=readout, per_rebind=per_rebind,
                max_dE=max(abs(e) for e in dE_marks),
                dv_mid=dv, dx_mid=dx, ToverL=T/L)

def main():
    out = []
    betas = [0.003, 0.03, 0.3]
    Ts = [1/256.0, 1/128.0, 1/64.0, 1/32.0, 1/16.0, 1/8.0]
    for beta in betas:
        P = 2.0*math.pi/beta**3
        v0 = beta
        A0 = 0.01*v0/P          # burn: 1% of orbital speed per period
        J0 = A0*4.0/P           # jerk: thrust doubles in a quarter period
        cases = [("A_const_burn", A0, 0.0), ("B_burn+jerk", A0, J0), ("C_pure_jerk", 0.0, J0)]
        for cname, a0, jk in cases:
            for Tf in Ts:
                for order, rn in [(1, "ret"), (2, "ret"), (3, "ret"), (1, "now")]:
                    r = run(beta, Tf, a0, jk, order, readout=rn)
                    r.update(case=cname); out.append(r)
        # controls: free fall (no thrust) and amplitudes
        r = run(beta, 1/64.0, 0.0, 0.0, 1, readout="ret"); r.update(case="F_freefall"); out.append(r)
        for fac in (0.5, 2.0):
            r = run(beta, 1/64.0, fac*A0, 0.0, 1); r.update(case="A_x%g"%fac); out.append(r)
            r = run(beta, 1/64.0, 0.0, fac*J0, 2); r.update(case="C_x%g"%fac); out.append(r)
            r = run(beta, 1/64.0, 0.0, -J0, 2); r.update(case="C_neg"); out.append(r)
    # step-size control at the tuning anchor
    for hf in (1024.0, 4096.0):
        r = run(0.03, 1/64.0, 0.01*0.03/(2*math.pi/0.03**3), 0.0, 1, h_frac=hf)
        r.update(case="conv_h%d"%int(hf)); out.append(r)
    json.dump(out, open(sys.argv[1] if len(sys.argv)>1 else "results.json", "w"), indent=1)
    print("runs:", len(out))

if __name__ == "__main__":
    main()
