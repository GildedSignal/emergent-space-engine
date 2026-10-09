/* Compiled-form readout cost: same algorithm as plunge_readout.py's make_reader
 * (bisect bracket + 3 Newton-in-psi iterations with GL4 local quadrature, exact
 * analytic dtau/dpsi), translated mechanically. Times per-sample cost; verifies
 * three probe readouts against Python-computed expected values (semantic check).
 * Build: cc -O2 -o plunge_readout_c plunge_readout_c.c -lm
 */
#include <math.h>
#include <stdio.h>
#include <time.h>

static const double GX[4] = {-0.8611363115940526, -0.3399810435848563,
                             0.3399810435848563, 0.8611363115940526};
static const double GW[4] = {0.3478548451374538, 0.6521451548625461,
                             0.6521451548625461, 0.3478548451374538};

#define BODY_C 1
#include "tube_C.h"
#define BODY_K7 1
#include "tube_k7.h"

static inline double dtau(double p, double u1, double rho, double a, double bb,
                          double L, double s2r) {
    double s = sin(p), u = u1 + rho * s * s;
    double Q = (u - a) * (u - a) + bb * bb;
    return s2r / L * cos(p) / (u * u * sqrt(Q));
}

static inline double dphi(double p, double u1, double rho, double a, double bb, double s2r) {
    double u = u1 + rho * sin(p) * sin(p);
    return s2r * cos(p) / sqrt((u - a) * (u - a) + bb * bb);
}

static inline double dv(double p, double u1, double rho, double a, double bb,
                        double L, double E, double s2r) {
    double s = sin(p), u = u1 + rho * s * s;
    double Q = (u - a) * (u - a) + bb * bb, sqQ = sqrt(Q);
    double dt = s2r / L * cos(p) / (u * u * sqQ);
    return (1.0 + L * L * u * u) / (E + L * sqrt(2.0 * (u - u1) * Q)) * dt;
}

static inline double gl4d(double p0, double p, double u1, double rho, double a,
                          double bb, double L, double s2r) {
    double m = 0.5 * (p0 + p), h = 0.5 * (p - p0), s = 0.0;
    for (int i = 0; i < 4; i++) {
        double q = m + h * GX[i];
        s += GW[i] * dtau(q, u1, rho, a, bb, L, s2r);
    }
    return h * s;
}

static void read3(double t, const double *psi, const double *tau, const double *phi,
                  const double *vv, double u1, double rho, double a, double bb,
                  double L, double E, double s2r, double *out) {
    int lo = 0, hi = 513;              /* bisect bracket on tau */
    while (hi - lo > 1) {
        int mid = (lo + hi) / 2;
        if (tau[mid] <= t) lo = mid; else hi = mid;
    }
    int j = lo;
    if (j >= 512) j = 511;
    double p0 = psi[j], p1 = psi[j + 1], T0 = tau[j], T1 = tau[j + 1];
    double p = p0 + (t - T0) / (T1 - T0) * (p1 - p0);
    if (!(p0 < p && p < p1)) p = 0.5 * (p0 + p1);
    for (int it = 0; it < 3; it++) {
        double f = T0 + gl4d(p0, p, u1, rho, a, bb, L, s2r) - t;
        p -= f / dtau(p, u1, rho, a, bb, L, s2r);
        if (p < p0) p = p0; else if (p > p1) p = p1;
    }
    out[0] = u1 + rho * sin(p) * sin(p);
    /* local GL4 for phi and v */
    double m = 0.5 * (p0 + p), h = 0.5 * (p - p0), sph = 0.0, sv = 0.0;
    for (int i = 0; i < 4; i++) {
        double q = m + h * GX[i];
        sph += GW[i] * dphi(q, u1, rho, a, bb, s2r);
        sv += GW[i] * dv(q, u1, rho, a, bb, L, E, s2r);
    }
    out[1] = phi[j] + h * sph;
    out[2] = vv[j] + h * sv;
}

static double now_s(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + 1e-9 * ts.tv_nsec;
}

int main(void) {
    unsigned long seed = 0x9e3779b97f4a7c15UL;
    double out[3];
    const int N = 2000000;

    /* semantic check against Python probes */
    FILE *f = fopen("probe_C.txt", "r");
    double t, eu, eph, ev;
    printf("probe checks (C vs Python), case C:\n");
    while (fscanf(f, "%lf %lf %lf %lf", &t, &eu, &eph, &ev) == 4) {
        read3(t, P_psi_C, P_tau_C, P_phi_C, P_vv_C, P_u1_C, P_rho_C, P_a_C,
              P_bb_C, P_L_C, P_E_C, P_s2r_C, out);
        printf("  u %.3e  dphi %.3e  dv %.3e (abs diffs)\n",
               fabs(out[0] - eu), fabs(out[1] - eph), fabs(out[2] - ev));
    }
    fclose(f);

    /* cost: case C */
    for (int w = 0; w < 3; w++) {                       /* warmup */
        seed = seed * 6364136223846793005UL + 1442695040888963407UL;
        double t = P_tau_C[1] + ((seed >> 11) * (1.0 / 9007199254740992.0)) *
                   (P_tau_C[512] - P_tau_C[1]);
        read3(t, P_psi_C, P_tau_C, P_phi_C, P_vv_C, P_u1_C, P_rho_C, P_a_C,
              P_bb_C, P_L_C, P_E_C, P_s2r_C, out);
    }
    double acc = 0.0, t0 = now_s();
    for (int i = 0; i < N; i++) {
        seed = seed * 6364136223846793005UL + 1442695040888963407UL;
        double t = P_tau_C[1] + ((seed >> 11) * (1.0 / 9007199254740992.0)) *
                   (P_tau_C[512] - P_tau_C[1]);
        read3(t, P_psi_C, P_tau_C, P_phi_C, P_vv_C, P_u1_C, P_rho_C, P_a_C,
              P_bb_C, P_L_C, P_E_C, P_s2r_C, out);
        acc += out[0];
    }
    double dt = now_s() - t0;
    printf("case C: %.1f ns/sample over %d readouts (chk %.6f)\n", dt / N * 1e9, N, acc);

    /* cost: sweep k=7 (worst winding) */
    t0 = now_s();
    for (int i = 0; i < N; i++) {
        seed = seed * 6364136223846793005UL + 1442695040888963407UL;
        double t = P_tau_k7[1] + ((seed >> 11) * (1.0 / 9007199254740992.0)) *
                   (P_tau_k7[512] - P_tau_k7[1]);
        read3(t, P_psi_k7, P_tau_k7, P_phi_k7, P_vv_k7, P_u1_k7, P_rho_k7, P_a_k7,
              P_bb_k7, P_L_k7, P_E_k7, P_s2r_k7, out);
        acc += out[0];
    }
    dt = now_s() - t0;
    printf("sweep k=7: %.1f ns/sample over %d readouts (chk %.6f)\n", dt / N * 1e9, N, acc);
    return 0;
}
