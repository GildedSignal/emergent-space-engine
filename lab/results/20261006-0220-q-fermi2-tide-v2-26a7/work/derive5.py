"""omega23 derivation (v2, true derivation of record).

g(grad_u l2', l3') for the boosted pair
    l2' = [0, L f/(r G), 0, -rd/(r G)],   l3' = [G/f, rd E/G, 0, L E/(r^2 G)],
    u = [E/f, rd, 0, L/r^2],  f = 1-2M/r,  rd^2 = E^2 - f(1+L^2/r^2),  G^2 = E^2 - f,
computed symbolically with the CORRECT chain rule
    d/dtau = rd * d/dr + (d(rd^2)/dr / 2) * d/d(rd) + (d(G^2)/dr * rd/(2G)) * d/dG
and the COMPLETE equatorial Christoffel set (Gamma^r_{rr} = -M/(r^2 f)
included -- the shipped derive5 omitted it, and so did derive6; the shipped
omega was right because the numeric measurement caught it, but no script
regenerated it until now).

Reduction: numerator/denominator as polynomials in (rd, G), exponents reduced
mod 2 via rd^2 -> E^2-f(1+L^2/r^2), G^2 -> E^2-f (exact algebraic reduction;
the old subs-loop left un-cancelled sqrt(r^3 rd^2) terms and printed a monster).

Emits work/omega_expr2.txt; run from the run folder root:
    python3 work/derive5.py
"""
import sympy as sp
exec(open('work/derive.py').read())   # conventions + asserted static Riemann

G = sp.symbols('G', positive=True)
lamg = (-f, 1/f, r**2, r**2)
u   = [E/f, rd, 0, L/r**2]
l2p = [0, L*f/(r*G), 0, -rd/(r*G)]
l3p = [G/f, rd*E/G, 0, L*E/(r**2*G)]
rd2 = E**2 - f*(1 + L**2/r**2)
G2  = E**2 - f

fp = sp.diff(f, r)
drd2dr = -fp*(1 + L**2/r**2) + 2*f*L**2/r**3
dG2dr = -fp
def dtau(v):
    return sp.diff(v, r)*rd + sp.diff(v, rd)*drd2dr/2 + sp.diff(v, G)*dG2dr*rd/(2*G)

expr = sp.S.Zero
for nu in range(4):
    expr += lamg[nu]*sp.expand(dtau(l2p[nu]))*l3p[nu]
GamE = {(0,0,1): M/(r**2*f), (0,1,0): M/(r**2*f), (1,0,0): M*f/r**2,
        (1,1,1): -M/(r**2*f), (1,2,2): -r*f, (1,3,3): -r*f,
        (2,1,2): 1/r, (2,2,1): 1/r, (3,1,3): 1/r, (3,3,1): 1/r}
for (nu, mu, al), c in GamE.items():
    expr += lamg[nu]*c*u[mu]*l2p[al]*l3p[nu]

def mod_sq(e):
    """exact reduction in Q(E,L,M,r)[rd,G] / (rd^2-rd2, G^2-G2)."""
    num, den = sp.fraction(sp.together(e))
    def red(P):
        acc = sp.S.Zero
        for (i, j), c in sp.Poly(P, rd, G).terms():
            acc += c*rd**(i % 2)*G**(j % 2)*rd2**(i//2)*G2**(j//2)
        return sp.expand(acc)
    return sp.cancel(red(num)/red(den))

w23 = mod_sq(expr)
with open('work/omega_expr2.txt', 'w') as fh:
    fh.write(sp.sstr(sp.factor(w23)))
print("omega23 =", sp.factor(w23))
print()
print("dPhi/dtau = -omega23 =", sp.factor(-w23))
print()
dpp = sp.cancel(-w23*r**2/L)
print("dPhi/dphi =", sp.factor(dpp), "   E=1 ->", sp.factor(dpp.subs(E, 1)))
print()
# anchors
Lc = sp.sqrt(M*r**2/(r-3*M)); Ec = (r-2*M)/sp.sqrt(r*(r-3*M))
val = sp.simplify(w23.subs({rd: 0, L: Lc, E: Ec}))
print("circular omega23 - sqrt(M/r^3) =", sp.radsimp(sp.simplify(val - sp.sqrt(M/r**3))))
print("L=0 omega23 =", sp.simplify(w23.subs(L, 0)))
