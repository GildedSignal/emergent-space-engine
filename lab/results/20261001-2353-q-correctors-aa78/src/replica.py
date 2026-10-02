"""Float replica of the plane's motion law (docs/law.md "Perturbed motion", step.rs).

The plane: drift = exact Kepler (tube, zero work) around the doll's dominant mass;
kicks = sibling secondaries' direct pulls + the parent's full differential tide,
1 kick of weight H at the midpoint of [T, T+H], H = P_radial / 2^7 (Config::default).

Schemes tested (all compositions of the SAME free drift D and kick K):
  dkd    : D(h/2) K(h) D(h/2)                        — 1 kick/step (the plane today)
  saba2/3/4: Laskar & Robutel (2001), coefficients as in REBOUND integrator_saba.c
  whc3   : Wisdom-Holman-Touma (1996) 3rd-order corrector (REBOUND whfast a1/b31),
           applied per step as a conjugation: C(+) dkd C(-)     — 5 kicks/step
  whc5   : 5th-order corrector (a1,a2,b51,b52)                  — 9 kicks/step
  whc3b  : the same 3rd-order corrector applied ONCE at each end of the whole run
           (conjugations telescope: (C M C^-1)^N = C M^N C^-1)  — 1 kick/step
  whc5b  : 5th-order, boundary-only                             — 1 kick/step

Newtonian Kepler drift by osculating elements (the tube's float stand-in), exact
closed form; elliptic and hyperbolic branches, vectorized over bodies/seeds.
"""
import numpy as np

TWOPI = 2.0 * np.pi

# ---------------------------------------------------------------- Kepler drift

def elements(x, y, vx, vy, gm):
    """Osculating (a, e, varpi, nu) from a state. a<0 if hyperbolic."""
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    en = 0.5 * v2 - gm / r                      # specific energy
    a = -gm / (2.0 * en)
    # eccentricity vector: ((v^2 - gm/r) x - (x.v) v)/gm
    rv = x * vx + y * vy
    ex = ((v2 - gm / r) * x - rv * vx) / gm
    ey = ((v2 - gm / r) * y - rv * vy) / gm
    e = np.hypot(ex, ey)
    tiny = e < 1e-13
    varpi = np.where(tiny, np.arctan2(y, x), np.arctan2(ey, ex))
    nu = np.where(tiny, np.arctan2(y, x),
                  np.arctan2(y, x) - varpi)      # may need 2pi fix
    # true anomaly measured from periapsis:
    nu = np.arctan2(np.sin(np.arctan2(y, x) - varpi), np.cos(np.arctan2(y, x) - varpi))
    return a, e, varpi, nu


def kepler_drift(st, dt, gm):
    """Advance states st (..., 4) by dt exactly along Kepler orbits of gm."""
    x, y, vx, vy = st[..., 0], st[..., 1], st[..., 2], st[..., 3]
    a, e, varpi, nu = elements(x, y, vx, vy, gm)
    ell = a > 0
    # eccentric anomaly from nu (F for hyperbolic: tanh(F/2)=sqrt((e-1)/(e+1)) tan(nu/2))
    q = np.sqrt(np.maximum((e - 1.0) / (e + 1.0), 0.0)) * np.tan(0.5 * nu)
    E = np.where(ell,
                 2.0 * np.arctan2(np.sqrt(np.abs((1 - e) / (1 + e))) * np.sin(0.5 * nu), np.cos(0.5 * nu)),
                 2.0 * np.arctanh(np.clip(q, -0.9999999999, 0.9999999999)))
    M = np.where(ell, E - e * np.sin(E), e * np.sinh(E) - E)
    # advance mean anomaly
    n = np.sqrt(gm / np.abs(a) ** 3)
    M2 = M + n * dt
    # solve Kepler's equation (vectorized Newton)
    if np.any(ell):
        Ei = M2.copy()
        for _ in range(12):
            f = Ei - e * np.sin(Ei) - M2
            fp = 1.0 - e * np.cos(Ei)
            Ei = Ei - f / fp
        E2 = Ei
    if np.any(~ell):
        # hyperbolic: e sinh F - F = M ; start from decent guess
        Mi = np.where(M2 >= 0, np.log(2 * np.abs(M2) / e + 1.8), -np.log(2 * np.abs(M2) / e + 1.8))
        Fi = np.where(np.isfinite(Mi), Mi, 0.0)
        for _ in range(30):
            f = e * np.sinh(Fi) - Fi - M2
            fp = e * np.cosh(Fi) - 1.0
            step = f / fp
            Fi = Fi - np.clip(step, -5.0, 5.0)
        E2h = Fi
    E2 = np.where(ell, E2 if np.any(ell) else M2, E2h if np.any(~ell) else M2)
    # back to state
    if np.any(ell):
        cE, sE = np.cos(E2), np.sin(E2)
        r = a * (1.0 - e * cE)
        # true anomaly from E
        nu2 = np.arctan2(np.sqrt(np.abs(1 - e * e)) * sE, cE - e)
        xo = np.where(np.abs(r) > 0, a * (cE - e), a * (cE - e))
        yo = a * np.sqrt(np.abs(1 - e * e)) * sE
        vf = np.sqrt(gm / np.abs(a)) / np.maximum(np.abs(1 - e * cE), 1e-300)
        vxo = -vf * sE * np.sqrt(1.0)  # placeholder, replaced below
        # velocities:  dx/dE = -a sinE, dy/dE = b cosE, dE/dt = n/(1-e cosE)
        b = a * np.sqrt(np.abs(1 - e * e))
        dEdt = n / (1.0 - e * cE)
        vxo = -a * sE * dEdt
        vyo = b * cE * dEdt
        cv, sv = np.cos(varpi), np.sin(varpi)
        xr = xo * cv - yo * sv
        yr = xo * sv + yo * cv
        vxr = vxo * cv - vyo * sv
        vyr = vxo * sv + vyo * cv
    if np.any(~ell):
        cF, sF = np.cosh(E2), np.sinh(E2)
        A, B = -a * (e - cF), -a * np.sqrt(e * e - 1.0) * sF
        dFdt = n / (e * cF - 1.0)
        vxA = a * sF * dFdt
        vyA = -a * np.sqrt(e * e - 1.0) * cF * dFdt
        cv, sv = np.cos(varpi), np.sin(varpi)
        xrh = A * cv - B * sv
        yrh = A * sv + B * cv
        vxrh = vxA * cv - vyA * sv
        vyrh = vxA * sv + vyA * cv
    if np.all(ell):
        return np.stack([xr, yr, vxr, vyr], -1)
    if not np.any(ell):
        return np.stack([xrh, yrh, vxrh, vyrh], -1)
    return np.stack([np.where(ell, xr, xrh), np.where(ell, yr, yrh),
                     np.where(ell, vxr, vxrh), np.where(ell, vyr, vyrh)], -1)


# ---------------------------------------------------------------- schemes

SABA_C = {2: [0.2113248654051871177454256097490212721762, 0.5773502691896257645091487805019574556476],
          3: [0.1127016653792583114820734600217600389167, 0.3872983346207416885179265399782399610833],
          4: [0.06943184420297371238802675555359524745214, 0.2605776340045981552106403648947824089476,
              0.3399810435848562648026657591032446872006]}
SABA_D = {2: [0.5],
          3: [0.2777777777777777777777777777777777777778, 0.4444444444444444444444444444444444444444],
          4: [0.1739274225687269286865319746109997036177, 0.3260725774312730713134680253890002963823]}
# WHFast corrector coefficients (REBOUND integrator_whfast.c = WHT96)
A1, A2 = 0.41833001326703777398908601289259374469640768464934, 0.83666002653407554797817202578518748939281536929867
B31 = -0.024900596027799867499350357910273437184309981229127
B51 = -0.0083001986759332891664501193034244790614366604097090
B52 = 0.041500993379666445832250596517122395307183302048545

KICKS_PER_STEP = {"dkd": 1, "saba2": 2, "saba3": 3, "saba4": 4,
                  "whc3": 5, "whc5": 9, "whc3b": 1, "whc5b": 1}


class Integrator:
    """Synchronized multi-body split. accel(st, t) -> (n,2) kick accelerations
    (the plane's kick: siblings' pulls + parent tide). gm array = per-body drift GM."""

    def __init__(self, scheme, gm, accel, t0=0.0):
        self.scheme, self.gm, self.accel, self.t = scheme, np.asarray(gm), accel, t0
        self.nkick = 0

    def D(self, st, dt, t):
        return kepler_drift(st, dt, self.gm)

    def K(self, st, w, t):
        self.nkick += st.shape[0]
        a = self.accel(st, t)
        st = st.copy()
        st[..., 2] += w * a[:, 0]
        st[..., 3] += w * a[:, 1]
        return st

    def Z(self, st, a_c, b_c, tau, t):
        """WHT96 corrector operator Z(a,b) = D(a) K(-b) D(-2a) K(b) D(a)."""
        st = self.D(st, a_c * tau, t)
        st = self.K(st, -b_c * tau, t)
        st = self.D(st, -2 * a_c * tau, t)
        st = self.K(st, b_c * tau, t)
        return self.D(st, a_c * tau, t)

    def corrector(self, st, inv, order, tau, t):
        if order == 3:
            st = self.Z(st, A1, -inv * B31, tau, t)
            st = self.Z(st, -A1, inv * B31, tau, t)
        else:
            st = self.Z(st, -A2, -inv * B51, tau, t)
            st = self.Z(st, -A1, -inv * B52, tau, t)
            st = self.Z(st, A1, inv * B52, tau, t)
            st = self.Z(st, A2, inv * B51, tau, t)
        return st

    def kernel(self, st, tau, t):
        s = self.scheme
        if s == "dkd" or s.startswith("whc"):
            st = self.D(st, 0.5 * tau, t)
            st = self.K(st, tau, t + 0.5 * tau)
            return self.D(st, 0.5 * tau, t + tau)
        if s.startswith("saba"):
            n = int(s[4])
            tt = t
            for op, c in saba_sequence(n):
                if op == "D":
                    st = self.D(st, c * tau, tt)
                    tt += c * tau
                else:
                    st = self.K(st, c * tau, tt)
            return st
        raise ValueError(s)

    def step(self, st, tau):
        s = self.scheme
        if s in ("whc3", "whc5"):
            order = 3 if s == "whc3" else 5
            st = self.corrector(st, 1.0, order, tau, self.t)
            st = self.kernel(st, tau, self.t)
            st = self.corrector(st, -1.0, order, tau, self.t + tau)
        else:
            st = self.kernel(st, tau, self.t)
        self.t += tau
        return st

    def run(self, st, nsteps, tau, out_every):
        """Return (nsteps//out_every + 1, n, 4) trajectory samples."""
        s = self.scheme
        if s in ("whc3b", "whc5b"):          # corrector only at the two ends
            order = 3 if s == "whc3b" else 5
            st = self.corrector(st, 1.0, order, tau, self.t)
        outs = [st.copy()]
        for i in range(nsteps):
            st = self.step(st, tau)
            if (i + 1) % out_every == 0:
                outs.append(st.copy())
        if s in ("whc3b", "whc5b"):
            st = self.corrector(st, -1.0, order, tau, self.t)
            outs[-1] = st.copy()
        self.final = st
        return np.array(outs)


def saba_sequence(n):
    """Explicit (drift, kick) list for SABAn, mirroring REBOUND's loop."""
    c, d = SABA_C[n], SABA_D[n]
    seq = [("D", c[0])]
    for i in range(n):
        j = min(i, n - 1 - i)                      # kicks mirror
        w = d[j if j < len(d) else -1]
        seq.append(("K", w))
        if i < n - 1:
            seq.append(("D", c[min(i + 1, n - 1 - i)]))
    seq.append(("D", c[0]))
    return seq


# ---------------------------------------------------------------- helpers

def state_from_elements(gm, a, e, varpi, nu0):
    """State at true anomaly nu0 on a conic (a, e, varpi). Handles e >= 1."""
    ell = e < 1.0
    if np.any(ell):
        ta2 = np.sqrt((1 - e) / (1 + e))
        E = 2.0 * np.arctan2(ta2 * np.sin(0.5 * nu0), np.cos(0.5 * nu0))
        xo = a * (np.cos(E) - e)
        yo = a * np.sqrt(1 - e * e) * np.sin(E)
        n = np.sqrt(gm / a ** 3)
        dEdt = n / (1 - e * np.cos(E))
        vxo = -a * np.sin(E) * dEdt
        vyo = a * np.sqrt(1 - e * e) * np.cos(E) * dEdt
    if not np.all(ell):
        den = 1 + e * np.cos(nu0)
        ch = (e + np.cos(nu0)) / den
        sh = np.sqrt(e * e - 1.0) * np.sin(nu0) / den
        xo = a * (ch - e)                       # a < 0
        yo = -a * np.sqrt(e * e - 1.0) * sh
        n = np.sqrt(gm / np.abs(a) ** 3)
        dFdt = n / (e * ch - 1.0)
        vxo = a * sh * dFdt
        vyo = -a * np.sqrt(e * e - 1.0) * ch * dFdt
    if np.all(ell):
        xo, yo, vxo, vyo = xo, yo, vxo, vyo
    else:
        xo = np.where(ell, xo, xo); yo = np.where(ell, yo, yo)
        vxo = np.where(ell, vxo, vxo); vyo = np.where(ell, vyo, vyo)
    cv, sv = np.cos(varpi), np.sin(varpi)
    return np.stack([xo * cv - yo * sv, xo * sv + yo * cv,
                     vxo * cv - vyo * sv, vxo * sv + vyo * cv], -1)


def ellipse_xv(a, e, varpi, M, gm=1.0):
    """Position on a fixed ellipse at mean anomaly M (closed form)."""
    E = M.copy()
    for _ in range(12):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    xo = a * (np.cos(E) - e); yo = a * np.sqrt(1 - e * e) * np.sin(E)
    n = np.sqrt(gm / a ** 3)
    dEdt = n / (1 - e * np.cos(E))
    vxo = -a * np.sin(E) * dEdt; vyo = a * np.sqrt(1 - e * e) * np.cos(E) * dEdt
    cv, sv = np.cos(varpi), np.sin(varpi)
    return np.stack([xo * cv - yo * sv, xo * sv + yo * cv], -1), \
           np.stack([vxo * cv - vyo * sv, vxo * sv + vyo * cv], -1)


def unwrap(a):
    return np.mod(a + np.pi, TWOPI) - np.pi
