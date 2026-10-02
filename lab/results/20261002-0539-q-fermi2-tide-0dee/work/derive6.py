"""Stage 5: omega23 with explicit sqrt expressions (rd and G as real radicals)."""
import sympy as sp
exec(open('work/derive.py').read())

lamg = (-f, 1/f, r**2, r**2)
rdx = sp.sqrt(E**2 - f*(1 + L**2/r**2))       # rdot (outward positive)
Gx  = sp.sqrt(E**2 - f)
u   = [E/f, rdx, 0, L/r**2]
l2p = [0, L*f/(r*Gx), 0, -rdx/(r*Gx)]
l3p = [Gx/f, rdx*E/Gx, 0, L*E/(r**2*Gx)]

expr = sp.S.Zero
for nu in range(4):
    expr += lamg[nu]*sp.diff(l2p[nu], r)*rdx*l3p[nu]     # d/dtau = rdot * d/dr
GamE = {(0,0,1): M/(r**2*f), (0,1,0): M/(r**2*f),
        (1,0,0): M*f/r**2, (1,2,2): -r*f, (1,3,3): -r*f,
        (2,1,2): 1/r, (2,2,1): 1/r, (3,1,3): 1/r, (3,3,1): 1/r}
for (nu, mu, al), c in GamE.items():
    expr += lamg[nu]*c*u[mu]*l2p[al]*l3p[nu]

w23 = sp.simplify(sp.radsimp(sp.together(expr)))
print("omega23 =", sp.factor(w23))
print()
# circular anchor
sub = {L: sp.sqrt(M*r**2/(r-3*M)), E: (r-2*M)/sp.sqrt(r*(r-3*M))}
val = sp.simplify(w23.subs(sub))
print("circular omega23 - sqrt(M/r^3) =", sp.simplify(val - sp.sqrt(M/r**3)))
print()
print("dPhi/dphi =", sp.factor(sp.simplify(-w23*r**2/L)))
print("L=0:", sp.simplify(w23.subs(L, 0)))
with open('work/omega_expr.txt', 'w') as fh:
    fh.write(sp.sstr(w23))
