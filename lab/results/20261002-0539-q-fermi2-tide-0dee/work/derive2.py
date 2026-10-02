"""Stage 2: boosted tetrad, C in that frame, rotation rate omega, parallel frame, eigenvalues."""
import sympy as sp
exec(open('work/derive.py').read())   # gives Rdown, Gam, gfun, conventions verified

G = sp.symbols('G', positive=True)   # G = sqrt(E^2 - eps f) = E*beta
lam = (1, 1/f, r**2, r**2)           # diagonal g at equator (sin=1)

# --- tetrad, coordinate components ---
u   = [E/f, rd, 0, L/r**2]
l1  = [0, 0, 1/r, 0]
l2p = [0, L*f/(r*G), 0, -rd/(r*G)]
l3p = [G/f, rd*E/G, 0, L*E/(r**2*G)]

# relations: rd^2 = E^2 - f(eps + L^2/r^2);  G^2 = E^2 - eps f
rel = lambda e: sp.together(sp.expand(e))
def red(e):
    e = e.subs(rd**2, E**2 - f*(eps + L**2/r**2)).subs(G**2, E**2 - eps*f)
    return sp.simplify(sp.simplify(e).subs(rd**2, E**2 - f*(eps + L**2/r**2)).subs(G**2, E**2 - eps*f))

def ip(a, b):
    return sp.simplify(red(sum(lam[i]*a[i]*b[i] for i in range(4))))

print("--- orthonormality checks ---")
print("u.u       =", ip(u, u), "  (want -eps)")
print("l1.l1     =", ip(l1, l1))
print("l2p.l2p   =", ip(l2p, l2p))
print("l3p.l3p   =", ip(l3p, l3p))
print("u.l1..l3p =", ip(u, l1), ip(u, l2p), ip(u, l3p))
print("l2p.l3p   =", ip(l2p, l3p), "  (want 0)")

def Cc(a, b):
    s = sp.S.Zero
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    t = Rdown[i][j][k][l]*u[i]*a[j]*u[k]*b[l]
                    if t != 0: s += t
    return red(s)

print("\n--- boosted-frame tidal tensor C^B_{ab} = R_{a 0 b 0} ---")
B11 = Cc(l1, l1); B22 = Cc(l2p, l2p); B33 = Cc(l3p, l3p); B23 = Cc(l2p, l3p)
B12 = Cc(l1, l2p); B13 = Cc(l1, l3p)
for nm, v in [('B11', B11), ('B22', B22), ('B33', B33), ('B23', B23), ('B12', B12), ('B13', B13)]:
    print(nm, "=", sp.factor(sp.simplify(v)))
print("trace:", sp.simplify(B11 + B22 + B33), " (want 0)")

print("\n--- rotation rate omega23 = g(grad_u l2p, l3p) ---")
f_ = sp.simplify(f)
fp = sp.diff(f_, r)                       # f' = 2M/r^2
drd2dr = -fp*(eps + L**2/r**2) + 2*f_*L**2/r**3
dG2dr = -eps*fp
def dtau(v):
    """total dr/dtau derivative of a component expr(r, rd, G)"""
    return sp.simplify(sp.diff(v, r) + sp.diff(v, rd)*drd2dr/(2*rd) + sp.diff(v, G)*dG2dr/(2*G))

def Gamma(i, j, k):
    return sp.simplify(Gam[i][j][k].subs({sn: 1, cs: 0}))

def grad_u(v):
    out = []
    for nu in range(4):
        e = dtau(v[nu])
        for mu in range(4):
            if u[mu] != 0:
                for al in range(4):
                    if v[al] != 0:
                        e += Gamma(nu, mu, al)*u[mu]*v[al]
        out.append(sp.simplify(e))
    return out

gl2 = grad_u(l2p)
omega23 = sp.simplify(red(sum(lam[i]*gl2[i]*l3p[i] for i in range(4))))
print("omega23 =", sp.factor(sp.simplify(sp.radsimp(omega23))))
# orthogonality sanity of the transport
gl3 = grad_u(l3p)
print("g(grad_u l2p, l2p) =", red(sum(lam[i]*gl2[i]*l2p[i] for i in range(4))), " (want 0)")
print("g(grad_u l2p, l1)  =", red(sum(lam[i]*gl2[i]*l1[i] for i in range(4))), " (want 0)")
print("g(grad_u l2p, u)   =", red(sum(lam[i]*gl2[i]*u[i] for i in range(4))), " (want 0)")

print("\n--- parallel frame pieces (Phi' = -omega23) ---")
halfsum  = sp.simplify((B22 + B33)/2)
halfdif  = sp.simplify((B22 - B33)/2)
print("C11 (theta axis) =", sp.factor(sp.simplify(B11)))
print("(B22+B33)/2     =", sp.factor(halfsum))
print("(B22-B33)/2     =", sp.factor(halfdif))
print("B23             =", sp.factor(sp.simplify(B23)))

print("\n--- in-plane eigenvalues: discriminant perfect square? ---")
disc = sp.simplify(halfdif**2 + B23**2)
sq = sp.sqrt(disc)
sq_simpl = sp.radsimp(sp.simplify(sq))
print("disc =", sp.factor(disc))
print("sqrt(disc) =", sq_simpl)
print("eigen in-plane: ", sp.factor(sp.simplify(halfsum + sq_simpl)), " , ", sp.factor(sp.simplify(halfsum - sq_simpl)))
