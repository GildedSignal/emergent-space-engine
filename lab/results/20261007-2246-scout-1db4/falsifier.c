/* Cadence falsifier: planar elliptical restricted 3-body.
 * Drift = exact Kepler about the central body (the compiled tube stand-in);
 * kicks = perturber tide (direct + indirect), DKD at 1/n of the body's CURRENT radial period.
 * Usage: falsifier name mu_pert n_pert a_body e0 horizon_orbits mu_central seeds
 * Output CSV: name,n_kick,seed,orbit,t,a,e,w(lambda of periapsis),lambda(polar angle)
 * escape marker: orbit=-1, a=-1.
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

typedef struct { double x, y, vx, vy; } State;
typedef struct { double a, e, w, M; } Elems;
static double PI;

static State elems_to_state(Elems el, double mu) {
    double E = el.M;
    for (int i = 0; i < 80; i++) {
        double f = E - el.e * sin(E) - el.M;
        double fp = 1.0 - el.e * cos(E);
        double d = f / fp; E -= d;
        if (fabs(d) < 1e-15) break;
    }
    double b = el.a * sqrt(1.0 - el.e * el.e);
    double n = sqrt(mu / (el.a * el.a * el.a));
    double cE = cos(E), sE = sin(E);
    double px = el.a * (cE - el.e), py = b * sE;
    double vpx = -el.a * n * sE / (1.0 - el.e * cE), vpy = b * n * cE / (1.0 - el.e * cE);
    double cw = cos(el.w), sw = sin(el.w);
    State s;
    s.x = px * cw - py * sw; s.y = px * sw + py * cw;
    s.vx = vpx * cw - vpy * sw; s.vy = vpx * sw + vpy * cw;
    return s;
}

static Elems state_to_elems(State s, double mu) {
    double r = hypot(s.x, s.y), v2 = s.vx * s.vx + s.vy * s.vy;
    double rv = s.x * s.vx + s.y * s.vy;
    double a = 1.0 / (2.0 / r - v2 / mu);
    double ex = ((v2 - mu / r) * s.x - rv * s.vx) / mu;
    double ey = ((v2 - mu / r) * s.y - rv * s.vy) / mu;
    double e = hypot(ex, ey);
    Elems el; el.a = a; el.e = e;
    el.w = (e > 1e-12) ? atan2(ey, ex) : 0.0;
    el.M = 0;
    if (a > 0 && e < 0.9995) {
        double ee = (e > 1e-12) ? e : 1e-12;
        double cosE = (1.0 - r / a) / ee;
        double sinE = rv / (ee * sqrt(mu * a));
        double E = atan2(sinE, cosE);
        el.M = E - e * sin(E);
        while (el.M < 0) el.M += 2 * PI;
        while (el.M >= 2 * PI) el.M -= 2 * PI;
    }
    return el;
}

int main(int argc, char **argv) {
    PI = acos(-1.0);
    if (argc < 9) { fprintf(stderr, "args: name mu_pert n_pert a_body e0 horizon mu_c seeds\n"); return 2; }
    const char *name = argv[1];
    double mu_p = atof(argv[2]), n_p = atof(argv[3]);
    double a0 = atof(argv[4]), e0 = atof(argv[5]);
    long horizon = atol(argv[6]);
    double mu_c = atof(argv[7]);
    int seeds = atoi(argv[8]);
    int nvals[] = {1, 2, 4, 8, 16, 32, 64, 128, 256, 512};
    int nn = sizeof(nvals) / sizeof(nvals[0]);

    unsigned long rng = 88172645463325252ULL ^ (unsigned long)(a0 * 1e9) ^ ((unsigned long)(e0 * 1e7) << 17);
    for (int s = 0; s < seeds; s++) {
        for (int vi = 0; vi < nn; vi++) {
            int n_kick = nvals[vi];
            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
            double lam0 = (rng % 1000000) / 1e6 * 2 * PI;
            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
            double w0 = (rng % 1000000) / 1e6 * 2 * PI;
            double M0 = lam0 - w0;
            while (M0 < 0) M0 += 2 * PI;
            Elems el = { a0, e0, w0, M0 };
            double t = 0;
            long orbits_out = 0;
            int escaped = 0;
            printf("%s,%d,%d,0,%.17g,%.17g,%.17g,%.17g,%.17g\n", name, n_kick, s, t, el.a, el.e, el.w, lam0);
            for (long it = 0; it < (long)horizon * n_kick && !escaped; it++) {
                double P = 2 * PI * sqrt(el.a * el.a * el.a / mu_c);
                double h = P / n_kick;
                double n_mean = sqrt(mu_c / (el.a * el.a * el.a));
                el.M = fmod(el.M + n_mean * h / 2, 2 * PI);
                t += h / 2;
                State st = elems_to_state(el, mu_c);
                double Rx = cos(n_p * t), Ry = sin(n_p * t);
                double dx = Rx - st.x, dy = Ry - st.y;
                double d3 = pow(dx * dx + dy * dy, 1.5);
                st.vx += mu_p * (dx / d3 - Rx) * h;
                st.vy += mu_p * (dy / d3 - Ry) * h;
                el = state_to_elems(st, mu_c);
                if (el.a <= 0 || el.e >= 0.9995 || el.a > 3 * a0) { escaped = 1; break; }
                n_mean = sqrt(mu_c / (el.a * el.a * el.a));
                el.M = fmod(el.M + n_mean * h / 2, 2 * PI);
                t += h / 2;
                if ((it + 1) % n_kick == 0) {
                    orbits_out++;
                    State st2 = elems_to_state(el, mu_c);
                    printf("%s,%d,%d,%ld,%.17g,%.17g,%.17g,%.17g,%.17g\n", name, n_kick, s,
                           orbits_out, t, el.a, el.e, el.w, atan2(st2.y, st2.x));
                    if (orbits_out >= horizon) break;
                }
            }
            if (escaped) printf("%s,%d,%d,-1,%.17g,-1,-1,-1,-1\n", name, n_kick, s, t);
        }
    }
    return 0;
}
