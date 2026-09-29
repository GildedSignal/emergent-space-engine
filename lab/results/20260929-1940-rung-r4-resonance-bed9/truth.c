/* Rung r4 truth: dense float64 N-body (star + massless inner + perturber),
 * planar, velocity Verlet, fixed step. G=1, M*=1, a1=1 units.
 * Usage: truth a1 e1 w1 lam1 a2 e2 w2 lam2 m2 T_end steps_per_orbit mode out
 *   mode = full    -> 4096 uniform samples: t a1 e1 lam1 varpi1 a2 e2 lam2 varpi2
 *   mode = summary -> one JSON line: {"maxe1":..,"conc":..,"dE":..}
 * conc = |mean(exp(i*psi))| over uniform samples, psi = 2*lam2 - lam1 - varpi1.
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define NS 4096

static double KE(double M, double e) { /* solve E - e sinE = M, Newton */
    double E = M, d;
    for (int i = 0; i < 100; i++) {
        d = (E - e * sin(E) - M) / (1.0 - e * cos(E));
        E -= d;
        if (fabs(d) < 1e-14) break;
    }
    return E;
}

/* elements (a,e,varpi,lam) about unit mass -> heliocentric r,v */
static void rv_from_el(double a, double e, double w, double lam,
                       double *x, double *y, double *vx, double *vy) {
    double M = lam - w, E = KE(M, e);
    double cE = cos(E), sE = sin(E), r = a * (1.0 - e * cE);
    double n = 1.0 / (a * sqrt(a));
    double xo = a * (cE - e), yo = a * sqrt(1.0 - e * e) * sE;
    double vf = n * a * a / r;
    double cw = cos(w), sw = sin(w);
    *x = xo * cw - yo * sw; *y = xo * sw + yo * cw;
    *vx = vf * (-sE * cw - sqrt(1 - e * e) * cE * sw);
    *vy = vf * (-sE * sw + sqrt(1 - e * e) * cE * cw);
}

static void el_from_rv(double x, double y, double vx, double vy,
                       double *a, double *e, double *w, double *lam) {
    double r2 = x * x + y * y, r = sqrt(r2), v2 = vx * vx + vy * vy, rv = x * vx + y * vy;
    *a = 1.0 / (2.0 / r - v2);
    double ex = (v2 - 1.0 / r) * x - rv * vx, ey = (v2 - 1.0 / r) * y - rv * vy;
    *e = sqrt(ex * ex + ey * ey);
    *w = atan2(ey, ex);
    double h = x * vy - y * vx;
    double cnu = (*e > 0) ? ((ex * x + ey * y) / (*e * r)) : 1.0;
    if (cnu > 1) cnu = 1; if (cnu < -1) cnu = -1;
    double nu = acos(cnu);
    if (rv < 0) nu = -nu;
    *lam = *w + nu;
}

int main(int argc, char **argv) {
    if (argc != 14) { fprintf(stderr, "args\n"); return 2; }
    double a1 = atof(argv[1]), e1 = atof(argv[2]), w1 = atof(argv[3]), l1 = atof(argv[4]);
    double a2 = atof(argv[5]), e2 = atof(argv[6]), w2 = atof(argv[7]), l2 = atof(argv[8]);
    double m2 = atof(argv[9]), T = atof(argv[10]);
    int spO = atoi(argv[11]);
    const char *mode = argv[12], *out = argv[13];

    double m[3] = {1.0, 0.0, m2}, x[3], y[3], vx[3], vy[3], ax[3], ay[3];
    double x1, y1, vx1, vy1, x2, y2, vx2, vy2;
    rv_from_el(a1, e1, w1, l1, &x1, &y1, &vx1, &vy1);
    rv_from_el(a2, e2, w2, l2, &x2, &y2, &vx2, &vy2);
    x[0] = 0; y[0] = 0; vx[0] = 0; vy[0] = 0;      /* star at rest at origin */
    x[1] = x1; y[1] = y1; vx[1] = vx1; vy[1] = vy1;
    x[2] = x2; y[2] = y2; vx[2] = vx2; vy[2] = vy2;

    double dt = 2.0 * M_PI / spO;
    long ns = (long)(T / dt);
    double E0 = 0;
    /* accelerations */
    #define ACC do { \
        for (int i = 0; i < 3; i++) { ax[i] = 0; ay[i] = 0; } \
        for (int i = 0; i < 3; i++) for (int j = i + 1; j < 3; j++) { \
            double dx = x[j] - x[i], dy = y[j] - y[i]; \
            double r = sqrt(dx * dx + dy * dy), f = 1.0 / (r * r * r); \
            ax[i] += m[j] * dx * f; ay[i] += m[j] * dy * f; \
            ax[j] -= m[i] * dx * f; ay[j] -= m[i] * dy * f; } } while (0)
    ACC;
    for (int i = 0; i < 3; i++) E0 += 0.5 * m[i] * (vx[i] * vx[i] + vy[i] * vy[i]);
    for (int i = 0; i < 3; i++) for (int j = i + 1; j < 3; j++) {
        double dx = x[j] - x[i], dy = y[j] - y[i];
        E0 -= m[i] * m[j] / sqrt(dx * dx + dy * dy); }

    FILE *fo = (mode[0] == 'f') ? fopen(out, "w") : NULL;
    double maxe = 0, sr = 0, si = 0;
    long next_s = 0;
    for (long s = 0; s <= ns; s++) {
        double t = s * dt;
        while (next_s <= NS - 1 && t >= next_s * T / NS - 1e-12) {
            double A, E, W, L, A2, E2, W2, L2;
            el_from_rv(x[1] - x[0], y[1] - y[0], vx[1] - vx[0], vy[1] - vy[0], &A, &E, &W, &L);
            el_from_rv(x[2] - x[0], y[2] - y[0], vx[2] - vx[0], vy[2] - vy[0], &A2, &E2, &W2, &L2);
            if (E > maxe) maxe = E;
            double psi = 2.0 * L2 - L - W;
            sr += cos(psi); si += sin(psi);
            if (fo) fprintf(fo, "%.10g %.10g %.10g %.10g %.10g %.10g %.10g %.10g %.10g\n",
                            next_s * T / NS, A, E, L, W, A2, E2, L2, W2);
            next_s++;
        }
        if (s < ns) {
            for (int i = 0; i < 3; i++) { vx[i] += 0.5 * dt * ax[i]; vy[i] += 0.5 * dt * ay[i]; }
            for (int i = 0; i < 3; i++) { x[i] += dt * vx[i]; y[i] += dt * vy[i]; }
            ACC;
            for (int i = 0; i < 3; i++) { vx[i] += 0.5 * dt * ax[i]; vy[i] += 0.5 * dt * ay[i]; }
        }
    }
    double conc = sqrt(sr * sr + si * si) / NS;
    double E1 = 0;
    for (int i = 0; i < 3; i++) E1 += 0.5 * m[i] * (vx[i] * vx[i] + vy[i] * vy[i]);
    for (int i = 0; i < 3; i++) for (int j = i + 1; j < 3; j++) {
        double dx = x[j] - x[i], dy = y[j] - y[i];
        E1 -= m[i] * m[j] / sqrt(dx * dx + dy * dy); }
    if (fo) { fclose(fo); }
    printf("{\"maxe1\":%.8g,\"conc\":%.8g,\"dE\":%.3e,\"nsamp\":%ld}\n", maxe, conc, fabs(E1 - E0), next_s);
    return 0;
}
