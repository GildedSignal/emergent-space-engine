#!/usr/bin/env python3
"""End-to-end float check of the phase-2 law against E9's geodesic-pair oracle, plus
the closed-form ansatz for the Fermi rotation angle sigma(chi)."""
import numpy as np
TAU = 2*np.pi
exec(open('proto.py').read().split('def main')[0])  # oracle machinery (System, initial, rk4_step, period_lambda)

# ---------- E9 oracle, verbatim logic (pairs + parallel axes + projections) ----------
def inv_diff(r, d, power):
    b = r + d
    s = sum(r**j * b**(power-1-j) for j in range(power))
    return -d * s / (r**power * b**power)

class Pair:  # de, dl
    def __init__(s, de, dl): s.de, s.dl = de, dl

class Sys(sys_system := object):  # extend the reference geodesic with pairs
    pass

def make_oracle(a, e, offsets, scale):
    p = (1+e)/a
    energy = np.sqrt(((p-2)**2-4*e*e)/(p*(p-3-e*e)))
    angular = np.sqrt((1+e)/(1-(3+e*e)*a/(1+e)))
    f = 1-2*a
    u = np.array([energy/f, 0.0, angular])
    axes = [np.array([0.0, f**0.5, 0.0]), np.array([a*angular/f**0.5, 0.0, energy/f**0.5])]
    def displaced(x, v):
        y = np.zeros(9); y[1] = 1.0
        for c in range(3):
            y[3+c] = x[0]*axes[0][c] + x[1]*axes[1][c]
            y[6+c] = u[c] + v[0]*axes[0][c] + v[1]*axes[1][c]
        rescale = (-1.0/(a*metric(a,1.0,y[6:9],y[6:9])))**0.5
        y[6:9] *= rescale
        for _ in range(16):
            def drhs(z):
                dz = np.zeros(9); dz[:3] = z[3:6]
                eta = z[3:6]; gg = connection(a, z[1], eta, eta); gu = connection(a, z[1], eta, z[6:9])
                for c in range(3):
                    dz[3+c] = -gg[c]; dz[6+c] = -gu[c]
                return dz
            y = rk4_step(y, 1/16, drhs)
        return y[0:3], y[6:9]
    # reference geodesic + 2 axes + pairs: y = [r, dr, t, phi, ax1(3), ax2(3), pairs(4 each)]
    y = [1.0, 0.0, 0.0, 0.0]
    y += list(axes[0]); y += list(axes[1])
    pairs = []
    for (x, v) in offsets:
        for sign in (scale, -scale):
            z, vel = displaced(x*sign, v*sign)
            r = z[1]
            pairs.append(Pair((1-2*a/r)*vel[0]-energy, r*r*vel[2]-angular))
            y += [r-1.0, vel[1], z[0], z[2]]
    y = np.array(y)
    # rhs for the combined system
    def rhs(yy):
        r, w = yy[0], yy[1]
        dy = np.zeros_like(yy)
        f_ = 1-2*a/r
        dy[0] = w
        dy[1] = -1/r**2 + angular**2/r**3 - 3*a*angular**2/r**4
        u0 = energy/f_; u2 = angular/r**2
        dy[2] = u0; dy[3] = u2
        uu = np.array([u0, w, u2])
        for start in (4, 7):
            g = connection(a, r, uu, yy[start:start+3])
            dy[start:start+3] = -g
        for i, pr in enumerate(pairs):
            j = 10+4*i
            d = yy[j]; b = r+d
            fb = 1-2*a/b
            dl2 = pr.dl*(2*angular+pr.dl)
            dy[j] = yy[j+1]
            dy[j+1] = -inv_diff(r,d,2) + dl2/b**3 + angular**2*inv_diff(r,d,3) - 3*a*(dl2/b**4 + angular**2*inv_diff(r,d,4))
            dy[j+2] = pr.de/fb - energy*2*a*d/(r*b*f_*fb)
            dy[j+3] = pr.dl/b**2 + angular*inv_diff(r,d,2)
        return dy
    class S: pass
    s = S(); s.rhs = rhs; s.energy = energy; s.angular = angular; s.pairs = pairs; s.y0 = y
    return s

def oracle_samples(a, e, offsets, dt, steps, scale, samples=401):
    s = make_oracle(a, e, offsets, scale)
    y = s.y0.copy()
    out = []
    for j in range(samples+1):
        axes = [y[4:7], y[7:10]]
        members = []
        for i in range(len(offsets)):
            plus = 10+8*i; minus = plus+4
            delta = np.array([(y[plus+2]-y[minus+2])/(2*scale), (y[plus]-y[minus])/(2*scale), (y[plus+3]-y[minus+3])/(2*scale)])
            pos = [metric(a, y[0], delta, axis) for axis in axes]
            members.append(np.array(pos)); members.append(-np.array(pos))
        out.append(members)
        if j < samples:
            for _ in range(steps):
                y = rk4_step(y, dt/steps, s.rhs)
    return out

# ---------- my phase-2 law ----------
def phase2_members(a, e, offsets, dt, substeps, scale, samples=401):
    """Propagate members under xi'' = -C_F(tau) xi with exact rotation, per proper time (lambda units)."""
    p = (1+e)/a
    E = np.sqrt(((p-2)**2-4*e*e)/(p*(p-3-e*e)))
    Lm = np.sqrt((1+e)/(1-(3+e*e)*a/(1+e)))*np.sqrt(1.0/a)  # L in M units
    # state: r, dr (M units), phi, sigma, and member states. Integrate geodesic by RK4 in lambda with M-unit conversion:
    # dtau_M = dlambda / a^1.5, dr_M = rho, drdot_M = lam_dot * sqrt(a)  (derived earlier)
    def derivs(rM, wM):
        return -1/rM**2 + Lm**2/rM**3 - 3*Lm**2/rM**4
    rM = 1.0/a; wM = 0.0; phi = 0.0; sigma = 0.0
    h = dt/substeps
    # member state in Fermi axes: xi (2), dxi/dlambda (2). Initial: offsets x along (e_r, E_phi'),
    # velocities v along the same (matching E9's displaced convention as closely as possible:
    # their axes[0] = e_r, axes[1] ~ tangential; we use orthonormal (e_r, E_phi')).
    mem = []
    for (x, v) in offsets:
        for sign in (1.0, -1.0):
            mem.append((np.array(x)*sign, np.array(v)*sign))
    def C_at(rM, wM, phi, sigma):
        f = 1-2/rM
        gam = E/f**0.5
        bp = (Lm/rM)/gam; br = (wM/f**0.5)/gam
        g2 = gam**2; gr2 = 1+g2*br**2
        mu = 1.0/rM**3
        c_rr = -mu*(2+bp**2)/(1-bp**2)
        c_pp = mu*(gr2 - (g2**2*br**2/gr2)*(1+2*bp**2))
        c_rp = mu*3*g2*gam*br*bp/gr2
        # angle of E_r axis in Fermi axes: theta = -(sigma) - tilt? e1 = cos(sig')E_r + sin(sig')E_phi with sig' = -sigma
        gr2t = gr2
        tilt = np.arctan2(g2*br*bp, gr2t)  # = atan(g^2 br bp / gr^2)
        th = tilt - sigma  # angle of E_r measured from e1 (validated)
        # C in Fermi axes = R(th) C_comov R(th)^T where R rotates comov->fermi... careful:
        # vector with Fermi coords Xf corresponds to comoving coords Xc = R(-th) Xf?? Let's derive:
        # e_r_hat (comoving axis 1) = cos(th) e1 + sin(th) e2. So X = Xc1*Ec1 + Xc2*Ec2 and Xf = R(th)^T Xc:
        # Xf1 = Xc1 cos th + Xc2 sin th; Xf2 = -Xc1 sin th + Xc2 cos th  => Xc = R(-th) Xf with R(-th) = [[c, s],[-s, c]]
        c_, s_ = np.cos(th), np.sin(th)
        Cf11 = c_**2*c_rr + 2*c_*s_*c_rp + s_**2*c_pp
        Cf12 = c_*s_*(c_rr-c_pp) + (c_**2-s_**2)*c_rp
        Cf22 = s_**2*c_rr - 2*c_*s_*c_rp + c_**2*c_pp
        return np.array([[Cf11, Cf12],[Cf12, Cf22]])
    out = []
    dl_dtauM = a**-1.5  # dtau_M/dlambda
    for j in range(samples+1):
        out.append([(xi.copy()) for (xi, vi) in mem])
        if j == samples: break
        for _ in range(substeps):
            f = 1-2/rM
            gam = E/f**0.5
            bp = (Lm/rM)/gam; br = (wM/f**0.5)/gam
            # sigma advance per lambda
            w_rot = bp/(1-bp**2)*(rM-3)/(rM**2*f**0.5)
            # member ODE per lambda: d2xi/dl2 = (dl/dtau)^2 * (-C xi), dtau_M/dl = a^-1.5
            k = a**-1.5
            for i, (xi, vi) in enumerate(mem):
                acc = -k**2 * C_at(rM, wM, phi, sigma) @ xi
                xi = xi + h*vi + 0.5*h*h*acc
                mem[i] = (xi, vi + h*acc)
            sigma += w_rot * k * h
            # geodesic RK4 in lambda (rho units -> M units)
            def geo(lam_state):
                rho, wr = lam_state
                rM_ = rho/a; wM_ = wr*np.sqrt(a)
                return (wr, derivs(rM_, wM_)*a**1.5/np.sqrt(a))  # d2rho/dl2 = d2rM/dtauM^2 * (dtauM/dl)^2 * a (rho=a rM)
            st = np.array([rM*a, wM/np.sqrt(a)])
            k1 = geo(st); k2 = geo(st+0.5*h*k1); k3 = geo(st+0.5*h*k2); k4 = geo(st+h*k3)
            st = st + h/6*(k1+2*k2+2*k3+k4)
            rM, wM = st[0]/a, st[1]*np.sqrt(a)
    # scale positions from M units to rp units? E9 truth is in rp units: multiply by rp_M? offsets given in rp units.
    rp_M = 1.0/a
    return [[xi*rp_M for xi in row] for row in out]

def errors(got, truth, offsets):
    pe = 0.0; se = 0.0
    for g, t in zip(got, truth):
        mass = sum((1+i//2) for i in range(len(t)))
        cg = np.array([sum(p[c]*(1+i//2)/mass for i,p in enumerate(g)) for c in range(2)])
        ct = np.array([sum(p[c]*(1+i//2)/mass for i,p in enumerate(t)) for c in range(2)])
        spread = max(np.linalg.norm(p-ct) for p in t) or 1.0
        for i in range(len(t)):
            d = max(np.linalg.norm(t[i]), np.linalg.norm(offsets[i//2][0]), 1.0)
            pe = max(pe, np.linalg.norm(g[i]-t[i])/d)
            se = max(se, np.linalg.norm((g[i]-cg)-(t[i]-ct))/spread)
    return pe, se

def fixtures_offsets(scale_pos=1e-5, R=1<<40):
    offsets = []
    for px, py in [(1.0,0.0),(0.35,0.8),(-0.7,0.45)]:
        x = np.array([px, py])*scale_pos*R
        v = np.array([-py, px])*scale_pos*R*0  # placeholder, replaced below
        offsets.append((x/R, v))
    return offsets

def main():
    # E9 fixtures: n = Q/(R sqrt(ratio)); member initial: x = p*eps*R (lattice), k = (-n x_y, -n x_x)?? read E9:
    # k = [(-n*x[1]).round(), (-n*x[0]).round()] -- NOTE: k1 = -n*x1, k2 = -n*x0 (the second is x0!)
    # offsets velocity: k.map(c => c/(n R)) => v = (-x1, -x0)*n/(nR) = (-x1/R, -x0/R)
    eps = 1e-5
    for ratio in [1e6, 1e4, 1e3, 100.0, 30.0, 10.0]:
        a = 1.0/ratio
        for e in [0.0, 0.3, 0.6]:
            offsets = []
            for px, py in [(1.0,0.0),(0.35,0.8),(-0.7,0.45)]:
                x = np.array([px*eps, py*eps])  # in rp units
                v = np.array([-py*eps, -px*eps])  # from E9's k = (-n x1, -n x0) / (n R) => (-x1, -x0)/R, x in rp units
                offsets.append((x, v))
            # NOTE: E9's k = [-n*x[1], -n*x[0]] is (co-rotation?) v_phi = -n x_r? and v_r = -n x_phi?? looks like a
            # rigid rotation by -90 deg. We mirror it exactly.
            P = period_lambda(a, e)
            # dt per sample: stride*n in lambda units; n = Q/(R sqrt(ratio)) with Q=2^20, R=2^40 (rad/chronon);
            # in lambda-per-chronon = n (their convention). stride = round(P/(40n)) -> dt = stride*n ~ P/40.
            dt = P/40
            truth = oracle_samples(a, e, offsets, dt, 256, 1/16)
            got = phase2_members(a, e, offsets, dt, 512, 1/16)
            pe, se = errors(got, truth, offsets)
            print("ratio=%8.1f e=%.1f  position=%.4f shape=%.4f  %s" % (ratio, e, pe, se, "PASS" if pe<=0.01 and se<=0.01 else "FAIL"))

if __name__ == "__main__":
    main()
