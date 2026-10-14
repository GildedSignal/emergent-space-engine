/* r_event: the wired gate's unit cost - evaluate one conjunction's miss and
   impulse vs the quantum (two Kepler solves + distance + compare), scalar loop.
   cc -O2 -o bench_r bench_r.c && ./bench_r */
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

static void kepler_state(double a, double e, double w, double M0, double t,
                         double *x, double *y, double *u, double *v) {
    double n = pow(a, -1.5);
    double M = fmod(M0 + n * t + M_PI, 2 * M_PI) - M_PI;
    if (M < -M_PI) M += 2 * M_PI;
    double E = M + e * sin(M);
    for (int i = 0; i < 5; i++)
        E -= (E - e * sin(E) - M) / (1 - e * cos(E));
    double cE = cos(E), sE = sin(E);
    double b = a * sqrt(1 - e * e);
    double ox = a * (cE - e), oy = b * sE;
    double dodE = n / (1 - e * cE);
    double vox = -a * sE * dodE, voy = b * cE * dodE;
    double cw = cos(w), sw = sin(w);
    *x = cw * ox - sw * oy; *y = sw * ox + cw * oy;
    *u = cw * vox - sw * voy; *v = sw * vox + cw * voy;
}

int main(int argc, char **argv) {
    long iters = argc > 1 ? atol(argv[1]) : 2000000;
    /* representative belt pair */
    double a1 = 1.0, e1 = 0.05, w1 = 1.0, M1 = 0.3, mu1 = 1e-18;
    double a2 = 1.03, e2 = 0.07, w2 = 2.5, M2 = 4.0, mu2 = 1e-17;
    double Q48 = ldexp(1.0, -48);
    volatile double sink = 0;
    long deleted = 0;
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    for (long k = 0; k < iters; k++) {
        double t = (double)(k % 6283);
        double x1, y1, u1, v1, x2, y2, u2, v2;
        kepler_state(a1, e1, w1, M1, t, &x1, &y1, &u1, &v1);
        kepler_state(a2, e2, w2, M2, t, &x2, &y2, &u2, &v2);
        double dx = x1 - x2, dy = y1 - y2, ux = u1 - u2, uy = v1 - v2;
        double d = hypot(dx, dy), vr = hypot(ux, uy);
        double z = d * vr;
        double dEi = 4 * mu2 / (pow(a1, -0.5) * z);
        double dEj = 4 * mu1 / (pow(a2, -0.5) * z);
        int del = (dEi < Q48) && (dEj < Q48);
        deleted += del;
        sink += d;
    }
    clock_gettime(CLOCK_MONOTONIC, &t1);
    double dt = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);
    printf("r_event: %.1f ns/conjunction-eval over %ld iters (deleted %ld, sink %.3f)\n",
           dt * 1e9 / iters, iters, deleted, (double)sink);
    return 0;
}
