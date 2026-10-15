#!/bin/sh
# regen.sh — regenerates every number in dossier.md from shipped code and this run's
# scripts. The runner applies work/patch.diff (empty: no tree edits) before this runs.
# Wall: build ~10 s + bench ~2.5 min + mpmath corner check ~5 s. No network needed
# after `cargo build` has the two crates.io deps cached (num-bigint, num-traits).
set -e
cd "$(dirname "$0")"

echo "== build (standalone crate; path-depends on shipped crates/space; x86-64-v3) =="
(cd native && cargo build --release)
BIN="${CARGO_TARGET_DIR:-$HOME/lab-target-0}/release/promo-bench"

echo "== full bench: value checks, wider grid, three timing arms =="
"$BIN" | tee bench-output.txt

echo "== kernel reference checks (Carlson's published values + mpmath 30 dps) =="
"$BIN" --rj
python3 - <<'EOF'
from mpmath import mp, elliprj
mp.dps = 30
for args in [(2, 3, 4, 5), (1e-6, 1, 1, 1.2666666666666666), (1e-6, 1.5714285714285714, 1, 1.2666666666666666)]:
    print("mpmath rj", args, "=", elliprj(*args))
EOF

echo "== strong-q corner: closed form exact at 40 dps (dossier's 3e-41 line) =="
python3 - <<'EOF'
from mpmath import mp, mpf, sqrt as msqrt, sin as msin, cos as mcos, elliprf, elliprj, quad
mp.dps = 40
k = mpf(2)/3; q = mpf(1)/7; u = mpf(1.5697963267948966)
eta = 1-k; n3 = 2*eta
A = 1-2*q*(4*k-1); m = 4*q*(1-k)/A; mg = -m/(1-m); n4 = 2*q*n3/(1-2*q)
tnum = msqrt(k*(1-2*q)*(1+2*q*(1-2*k)))
s = msin(u); c = mcos(u); s2 = s*s; c2 = c*c; s3 = s2*s
W2 = 1-mg*s2; W = msqrt(W2)
F = s*elliprf(c2, W2, 1)
Pi = lambda nn: F + (nn/3)*s3*elliprj(c2, W2, 1, 1-nn*s2)
E = F - (mg/3)*s3*elliprj(c2, W2, 1, 1)
def solve(M, b):
    n = len(b); M = [row[:] + [b[i]] for i, row in enumerate(M)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[piv] = M[piv], M[col]
        for r in range(n):
            if r != col and M[r][col]:
                f = M[r][col]/M[col][col]
                for j in range(col, n+1): M[r][j] -= f*M[col][j]
    return [M[i][n]/M[i][i] for i in range(n)]
n = -n3
q0, q1, c1, kap = solve([[1,0,1,1],[2*n,1,n,-n-2-2*mg],[n*n,2*n,0,3*mg],[0,n*n,0,mg*n]], [1,0,0,0])
aa, bb2, gg = solve([[1,1,1],[n4-n3,n4,-2*n3],[-n3*n4,0,n3*n3]], [1,0,0])
I2 = q0*F + q1*(F-E)/mg + c1*Pi(n3) + kap*s*c*W/(1-n3*s2)
t = tnum*(2/msqrt(A*(1-m)))/(1-2*q)*(aa*Pi(n3)+bb2*I2+gg*Pi(-n4))
f_t = lambda th: tnum/(msqrt(1-q*(6*k+2*eta*mcos(th)))*(k+eta*mcos(th))**2*(1-2*q*(k+eta*mcos(th))))
t_true = quad(f_t, [0, 2*u])
print("closed t (40dps) =", t)
print("quad   t (40dps) =", t_true)
print("rel diff         =", abs(t-t_true)/abs(t_true))
EOF
echo "== done =="
