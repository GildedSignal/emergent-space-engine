"""Continue the symmetric 2:1 periodic family from the distant branch toward
apoapsis-at-conjunction (x0 -> 1), warm-starting Newton at each step."""
import math

from common import MU_PLANET, R_SOI
from periodic import integrate, solve


def main():
    # distant branch solution (from periodic.py run at d_r = 0.002)
    x0, vy0 = 0.874564123, 0.836345952
    u = [x0, vy0]
    best = None
    x_target = 0.9972
    step = 0.01
    while x0 < x_target:
        x_next = min(x0 + step, x_target)
        guess = (x_next, u[1])
        un, nrm, it = solve(guess, tol=1e-11, iters=14)
        if nrm > 1e-9 or it < 0:
            step *= 0.5
            if step < 2e-4:
                print(f"family stops at x0={x0:.6f}")
                break
            continue
        u = list(un)
        x0 = u[0]
        y, min_d = integrate(u)
        print(f"x0={u[0]:.6f} vy0={u[1]:.6f} |r|={nrm:.1e} it={it} "
              f"min_d={min_d:.5f} ({min_d/R_SOI:.2f} R_SOI)")
        best = (u[0], u[1], min_d)
    print("best:", best)


if __name__ == "__main__":
    main()
