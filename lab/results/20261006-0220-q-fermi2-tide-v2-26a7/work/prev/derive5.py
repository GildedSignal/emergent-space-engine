"""Stage 4: omega23 in coordinates, fast: no per-term simplify."""
import sympy as sp
exec(open('work/derive.py').read())

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
def dtau_raw(v):
    return sp.diff(v, r) + sp.diff(v, rd)*drd2dr/(2*rd) + sp.diff(v, G)*dG2dr/(2*G)

expr = sp.S.Zero
for nu in range(4):
    expr += lamg[nu]*sp.expand(dtau_raw(l2p[nu]))*l3p[nu]
GamE = {(0,0,1): M/(r**2*f), (0,1,0): M/(r**2*f),
        (1,0,0): M*f/r**2, (1,2,2): -r*f, (1,3,3): -r*f,
        (2,1,2): 1/r, (2,2,1): 1/r, (3,1,3): 1/r, (3,3,1): 1/r}
for (nu, mu, al), c in GamE.items():
    expr += lamg[nu]*c*u[mu]*l2p[al]*l3p[nu]

def red(e):
    e = sp.expand(e)
    for _ in range(6):
        e = sp.expand(e.subs({rd**2: rd2, G**2: G2, rd**4: rd2**2, G**4: G2**2,
                              rd**6: rd2**3, G**6: G2**3}))
    return sp.cancel(sp.together(e))

w23 = red(expr)
print("omega23 =", sp.factor(w23))
print()
print("dPhi/dtau = -omega23 =", sp.factor(-w23))
print()
dpp = sp.cancel(-w23*r**2/L)
print("dPhi/dphi =", sp.factor(dpp))
print()
# circular anchor
Lc = sp.sqrt(M*r**2/(r-3*M)); Ec = (r-2*M)/sp.sqrt(r*(r-3*M))
val = sp.simplify(w23.subs({rd: 0, L: Lc, E: Ec}))
print("circular omega23 =", sp.radsimp(val), "   sqrt(M/r^3) =", sp.sqrt(M/r**3))
print("circular match:", sp.radsimp(sp.simplify(val - sp.sqrt(M/r**3))) == 0)
# radial anchor: L=0 -> 0
print("L=0 omega23 =", sp.simplify(w23.subs(L, 0)))
