"""Stage 2 (clean): timelike eps=1. Boosted tetrad, tidal tensor, rotation rate, parallel frame, eigenvalues."""
import sympy as sp
exec(open('work/derive.py').read())

G = sp.symbols('G', positive=True)
lamg = (-f, 1/f, r**2, r**2)

u   = [E/f, rd, 0, L/r**2]
l1  = [0, 0, 1/r, 0]
l2p = [0, L*f/(r*G), 0, -rd/(r*G)]
l3p = [G/f, rd*E/G, 0, L*E/(r**2*G)]

rd2 = E**2 - f*(1 + L**2/r**2)
G2  = E**2 - f
def red(e):
    e = sp.expand(e)
    for _ in range(4):
        e = sp.expand(e.subs({rd**2: rd2, G**2: G2, rd**4: rd2**2, G**4: G2**2, rd**6: rd2**3, G**6: G2**3}))
    return sp.simplify(e)

def ip(a, b):
    return red(sum(lamg[i]*a[i]*b[i] for i in range(4)))

print("--- orthonormality ---")
for nm, val in [("u.u", ip(u, u)), ("l1.l1", ip(l1, l1)), ("l2p.l2p", ip(l2p, l2p)),
                ("l3p.l3p", ip(l3p, l3p)), ("u.l1", ip(u, l1)), ("u.l2p", ip(u, l2p)),
                ("u.l3p", ip(u, l3p)), ("l2p.l3p", ip(l2p, l3p))]:
    print(" ", nm, "=", val)

def Cc(a, b):
    s = sp.S.Zero
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    t = Rdown[i][j][k][l]*u[i]*a[j]*u[k]*b[l]
                    if t != 0: s += t
    return red(s)

print("\n--- boosted tidal tensor B ---")
B11 = Cc(l1, l1); B22 = Cc(l2p, l2p); B33 = Cc(l3p, l3p); B23 = Cc(l2p, l3p)
B12 = Cc(l1, l2p); B13 = Cc(l1, l3p)
for nm, v in [('B11', B11), ('B22', B22), ('B33', B33), ('B23', B23), ('B12', B12), ('B13', B13)]:
    print(nm, "=", sp.factor(sp.cancel(sp.simplify(v))))
print("trace =", sp.simplify(B11 + B22 + B33))

print("\n--- transport / rotation rate ---")
fp = sp.diff(f, r)
drd2dr = -fp*(1 + L**2/r**2) + 2*f*L**2/r**3
dG2dr = -fp
def dtau(v):
    return sp.simplify(sp.diff(v, r) + sp.diff(v, rd)*drd2dr/(2*rd) + sp.diff(v, G)*dG2dr/(2*G))
def GamE(i, j, k):
    return sp.simplify(Gam[i][j][k].subs({sn: 1, cs: 0}))
def grad_u(v):
    out = []
    for nu in range(4):
        e = dtau(v[nu])
        for mu in range(4):
            if u[mu] != 0:
                for al in range(4):
                    if v[al] != 0:
                        e += GamE(nu, mu, al)*u[mu]*v[al]
        out.append(sp.simplify(e))
    return out
gl2 = grad_u(l2p); gl3 = grad_u(l3p)
w23   = red(sum(lamg[i]*gl2[i]*l3p[i] for i in range(4)))
print("omega23            =", sp.factor(sp.cancel(w23)))
print("g(grad l2p, l2p)   =", red(sum(lamg[i]*gl2[i]*l2p[i] for i in range(4))))
print("g(grad l2p, l1)    =", red(sum(lamg[i]*gl2[i]*l1[i] for i in range(4))))
print("g(grad l2p, u)     =", red(sum(lamg[i]*gl2[i]*u[i] for i in range(4))))
print("g(grad l3p, l3p)   =", red(sum(lamg[i]*gl3[i]*l3p[i] for i in range(4))))
w31 = red(sum(lamg[i]*gl3[i]*l2p[i] for i in range(4)))
print("g(grad l3p, l2p)   =", w31, "  (want -omega23)")

print("\n--- parallel-frame pieces: C11, halfsum, Q, and Marck angle ---")
halfsum = sp.cancel(sp.simplify((B22 + B33)/2))
halfdif = sp.cancel(sp.simplify((B22 - B33)/2))
Q2 = sp.simplify(halfdif**2 + B23**2)
print("C11          =", sp.factor(B11))
print("halfsum      =", sp.factor(halfsum))
print("halfdif      =", sp.factor(halfdif))
print("halfdif^2+B23^2 =", sp.factor(sp.cancel(Q2)))
print("sqrt -> Q    =", sp.factor(sp.cancel(sp.sqrt(sp.simplify(Q2)))))

print("\n--- dPhi/dphi ---")
dPhidtau = sp.cancel(sp.simplify(-w23))
print("dPhi/dtau =", sp.factor(dPhidtau))
print("dPhi/dphi =", sp.factor(sp.cancel(sp.simplify(dPhidtau * r**2/L))))
