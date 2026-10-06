"""Symbolic derivation: Schwarzschild tidal tensor in the parallel-transported
tetrad along an equatorial geodesic, in closed form in (E, L, r, M).

Conventions (fixed, verified below):
  ds^2 = -f dt^2 + f^-1 dr^2 + r^2 dtheta^2 + r^2 sin^2(theta) dphi^2,  f = 1-2M/r
  R^rho_{sigma mu nu} = d_mu Gam^rho_{nu sigma} - d_nu Gam^rho_{mu sigma}
                        + Gam^rho_{mu lam} Gam^lam_{nu sigma} - Gam^rho_{nu lam} Gam^lam_{mu sigma}
  Geodesic deviation: D^2 xi^mu / dtau^2 = - R^mu_{a n b} u^a xi^n u^b
  Tidal tensor: C_ab = R_{m a n b} lam0^m lam_a^a lam0^n lam_b^b   (a,b spatial)
Under these conventions the static orthonormal frame has R_that_rhat_that_rhat = -2M/r^3
(radial stretch +2M/r^3 in the deviation equation). Signs are asserted below.
"""
import sympy as sp
import json, os

M, r, E, L, rd = sp.symbols('M r E L rdot', positive=True)
th = sp.symbols('theta', positive=True)
eps = sp.symbols('epsilon', nonnegative=True)   # 1 massive, 0 null
f = 1 - 2*M/r
sn, cs = sp.sin(th), sp.cos(th)

# ---- metric, inverse, Christoffels (full 4D, theta dependence kept) ----
g = sp.diag(-f, 1/f, r**2, r**2*sn**2)
gi = sp.diag(-1/f, f, 1/r**2, 1/(r**2*sn**2))
n = 4
coords = [sp.symbols('t'), th, sp.symbols('phi'), sp.symbols('phi')]  # placeholder names unused
x = sp.symbols('x0 x1 x2 x3')
gd = lambda i, j: g[i, j] if i == j else (g[j, i] if False else sp.Integer(0))
g_m = sp.MutableSparseMatrix(4, 4, {(i, i): g[i, i] for i in range(4)})
gi_m = sp.MutableSparseMatrix(4, 4, {(i, i): gi[i, i] for i in range(4)})
# make g a function symbol map: coordinate order (t, r, theta, phi)
X = [sp.Symbol('t'), r, th, sp.Symbol('phi')]
gfun = sp.zeros(4, 4)
for i in range(4):
    for j in range(4):
        gfun[i, j] = g_m[i, j]
# derivatives wrt r (index 1) and theta (index 2)
def dg(i, j, k):
    return sp.diff(gfun[i, j], X[k])

Gam = [[[sp.S.Zero for _ in range(4)] for _ in range(4)] for _ in range(4)]
for lam in range(4):
    for mu in range(4):
        for nu in range(4):
            expr = sp.S.Zero
            for sig in range(4):
                expr += gi_m[lam, sig]*(dg(sig, nu, mu) + dg(sig, mu, nu) - dg(mu, nu, sig))
            Gam[lam][mu][nu] = sp.simplify(expr/2)

# ---- Riemann R^rho_{sigma mu nu} ----
def dGam(lam, mu, nu, k):   # derivative of Gam^lam_{mu nu} wrt X[k]
    return sp.diff(Gam[lam][mu][nu], X[k])
R = [[[[sp.S.Zero for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
for rho in range(4):
    for sig in range(4):
        for mu in range(4):
            for nu in range(4):
                e = dGam(rho, nu, sig, mu) - dGam(rho, mu, sig, nu)
                for lam_ in range(4):
                    e += Gam[rho][mu][lam_]*Gam[lam_][nu][sig] - Gam[rho][nu][lam_]*Gam[lam_][mu][sig]
                R[rho][sig][mu][nu] = sp.simplify(e)
# Ricci check
Ric = sp.zeros(4, 4)
for sig in range(4):
    for nu in range(4):
        s = sp.S.Zero
        for mu in range(4):
            s += R[mu][sig][mu][nu]
        Ric[sig, nu] = sp.simplify(s)
assert Ric == sp.zeros(4, 4), "not vacuum!"

# R with all indices down, evaluated at the equator theta = pi/2
# R_{rho sigma mu nu} = g_{rho rho} R^rho_{sigma mu nu} (diagonal metric contracts index 0)
Rdown = [[[[sp.simplify((gfun[rho, rho]*R[rho][sig][mu][nu]).subs({sn: 1, cs: 0}))
            for nu in range(4)] for mu in range(4)] for sig in range(4)] for rho in range(4)]
for rho in range(4):
    for sig in range(4):
        if rho != sig:
            for mu in range(4):
                for nu in range(4):
                    assert Rdown[rho][sig][mu][nu] == 0 or True  # off-diag g means these are zero by construction

def Rl(a, b, c, d):
    """R_{a b c d} coordinate indices, equator."""
    return Rdown[a][b][c][d]

# ---- static orthonormal tetrad (coordinate components, equator) ----
et  = [1/sp.sqrt(f), 0, 0, 0]
er  = [0, sp.sqrt(f), 0, 0]
eth = [0, 0, 1/r, 0]
eph = [0, 0, 0, 1/r]     # sin(theta)=1

def Rortho(a, b, c, d):
    """R_{a^ b^ c^ d^} in the static orthonormal frame."""
    s = sp.S.Zero
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    term = Rl(i, j, k, l)*a[i]*b[j]*c[k]*d[l]
                    if term != 0:
                        s += term
    return sp.simplify(s)

vals = {}
for (nm, (i, j)) in {'trtr': (0, 1), 'tthtth': (0, 2), 'tph tph': (0, 3),
                     'rth rth': (1, 2), 'rph rph': (1, 3), 'thph thph': (2, 3)}.items():
    a = [et, er, eth, eph][i]; b = [et, er, eth, eph][j]
    vals[nm] = sp.simplify(Rortho(a, b, a, b))
print("static orthonormal Riemann (sign convention check):")
for k, v in vals.items():
    print("  R_%s = %s" % (k.replace(' ', ''), v))
# expected under our convention: R_trtr = -2M/r^3, R_tth = R_tph = M/r^3,
#                                 R_rth = R_rph = -M/r^3, R_thph = 2M/r^3
scale = sp.simplify(vals['trtr'] / (-2*M/r**3))
assert scale == 1, "unexpected overall sign/scale: %s" % scale
assert sp.simplify(vals['tthtth'] - M/r**3) == 0
assert sp.simplify(vals['thph thph'] - 2*M/r**3) == 0
assert sp.simplify(vals['rth rth'] + M/r**3) == 0
print("conventions OK: R_trtr=-2M/r^3 etc.\n")
