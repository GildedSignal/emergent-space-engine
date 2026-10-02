"""Stage 3: rotation rate omega23, built as one scalar then simplified once."""
import sympy as sp
exec(open('work/derive.py').read())

G = sp.symbols('G', positive=True)
lamg = (-f, 1/f, r**2, r**2)
u   = [E/f, rd, 0, L/r**2]
l2p = [0, L*f/(r*G), 0, -rd/(r*G)]
l3p = [G/f, rd*E/G, 0, L*E/(r**2*G)]
rd2 = E**2 - f*(1 + L**2/r**2)
G2  = E**2 - f

def red(e):
    e = sp.expand(e)
    for _ in range(5):
        e = sp.expand(e.subs({rd**2: rd2, G**2: G2, rd**4: rd2**2, G**4: G2**2, rd**6: rd2**3, G**6: G2**3}))
    return sp.cancel(sp.simplify(e))

# equatorial Christoffel table (only nonzero)
GamE = {(0,0,1): M/(r**2*f), (0,1,0): M/(r**2*f),
        (1,0,0): M*f/r**2, (1,2,2): -r*f, (1,3,3): -r*f,
        (2,1,2): 1/r, (2,2,1): 1/r, (3,1,3): 1/r, (3,3,1): 1/r}

fp = sp.diff(f, r)
drd2dr = -fp*(1 + L**2/r**2) + 2*f*L**2/r**3
dG2dr = -fp
def dtau_raw(v):
    return sp.diff(v, r) + sp.diff(v, rd)*drd2dr/(2*rd) + sp.diff(v, G)*dG2dr/(2*G)

expr = sp.S.Zero
for nu in range(4):
    expr += lamg[nu]*dtau_raw(l2p[nu])*l3p[nu]
for (nu, mu, al), c in GamE.items():
    expr += lamg[nu]*c*u[mu]*l2p[al]*l3p[nu]
w23 = red(expr)
print("omega23 = dPhi_parallel_relation: grad_u l2p = omega23 * l3p")
print("omega23          =", sp.factor(w23))
print()
dPhidtau = sp.simplify(-w23)
print("dPhi/dtau (Phi = angle of parallel frame vs boosted) =", sp.factor(dPhidtau))
print()
dPhidphi = sp.cancel(sp.simplify(dPhidtau*r**2/L))
print("dPhi/dphi =", sp.factor(dPhidphi))
print()
# circular check: rd=0, L^2=Mr^2/(r-3M): expect dPhi/dtau = -(L/r^2)(1 - sqrt(1-3M/r))
Lc = sp.sqrt(M*r**2/(r-3*M))
sub = {rd: 0, L: Lc, E: (r-2*M)/sp.sqrt(r*(r-3*M))}
val = sp.simplify(dPhidtau.subs(sub))
print("circular dPhi/dtau      =", sp.simplify(val))
print("expected -(L/r^2)(1-sqrt(1-3M/r)) =", sp.simplify(-Lc/r**2*(1 - sp.sqrt(1 - 3*M/r))))
print("match:", sp.simplify(val + Lc/r**2*(1 - sp.sqrt(1 - 3*M/r))) == 0)
