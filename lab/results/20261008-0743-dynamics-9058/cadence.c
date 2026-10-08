/* Kick-cadence dynamics for the orbital kick layer (docs/law.md "Perturbed motion").
 *
 * Scene: CR3BP, Sun (1-mu) + Jupiter (mu) on a circular barycentric orbit, massless particle.
 * Units: GM_total = 1, n_J = 1, a_J = 1, so Jupiter's period is 2*pi.
 *
 * Truth: barycentric Cartesian RK4 at fine fixed step (structure independent of the model).
 * Model: heliocentric Wisdom-Holman split. Drift = exact Kepler about GM = 1-mu
 * (universal-variable propagator). Kick = Jupiter's pull + the indirect term (law.md line 36):
 *   a_kick(r,t) = -mu[ (r - r_Jh)/|r - r_Jh|^3 + r_Jh ],  r_Jh = (cos t, sin t), |r_Jh| = 1.
 * Cadence: metronome tau = T_p/K fixed from t=0. Flavors:
 *   F  frozen-at-centre: dv = tau * a_kick(kepler state at window centre), split half/half
 *      (the shipped Fermi-frame flavor, crates/engine frame.rs "the tide frozen at the
 *      centre of its interval").
 *   W  window integral: dv = int_window a_kick(r_kep(s), s) ds by 8-pt Gauss-Legendre,
 *      split half/half (H0190's averaging flavor).
 * Readout mid-window: position = Kepler drift of the post-half-kick state; velocity = linear
 * ramp between pre-kick and post-kick velocity (law.md line 33's second-order ramp).
 *
 * Usage: cadence <a> <e0> <flavor F|W> <kpo> <mode locked|golden> <n_jup_orbits> [thj0]
 * Prints CSV header + rows: t_jup, cj_err, e_err, pom_err, arel_err, rotdist, cj_truth_drift
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#ifndef MUO
#define MUO (1.0 / 1047.35)
#endif
static const double MU = MUO;
static const double GMS = 1.0 - MU;
static double THJ0 = 0.4;

typedef struct { double x, y, vx, vy; } St;

static void sun(double t, double *xs, double *ys, double *vxs, double *vys) {
    double cc = cos(t + THJ0), ss = sin(t + THJ0);
    *xs = -MU * cc; *ys = -MU * ss; *vxs = MU * ss; *vys = -MU * cc;
}

static void acc_bar(double t, const St *s, double *ax, double *ay) {
    double cc = cos(t + THJ0), ss = sin(t + THJ0);
    double dxs = s->x + MU * cc, dys = s->y + MU * ss, rs3 = pow(dxs * dxs + dys * dys, 1.5);
    double dxj = s->x - (1 - MU) * cc, dyj = s->y - (1 - MU) * ss, rj3 = pow(dxj * dxj + dyj * dyj, 1.5);
    *ax = -GMS * dxs / rs3 - MU * dxj / rj3;
    *ay = -GMS * dys / rs3 - MU * dyj / rj3;
}

static St rk4_step(double t, St s, double h) {
    double y[4] = { s.x, s.y, s.vx, s.vy }, k1[4], k2[4], k3[4], k4[4], yy[4];
    St st;
    k1[0] = y[2]; k1[1] = y[3]; acc_bar(t, &s, &k1[2], &k1[3]);
    for (int i = 0; i < 4; i++) yy[i] = y[i] + 0.5 * h * k1[i];
    st.x = yy[0]; st.y = yy[1]; st.vx = yy[2]; st.vy = yy[3];
    k2[0] = yy[2]; k2[1] = yy[3]; acc_bar(t + 0.5 * h, &st, &k2[2], &k2[3]);
    for (int i = 0; i < 4; i++) yy[i] = y[i] + 0.5 * h * k2[i];
    st.x = yy[0]; st.y = yy[1]; st.vx = yy[2]; st.vy = yy[3];
    k3[0] = yy[2]; k3[1] = yy[3]; acc_bar(t + 0.5 * h, &st, &k3[2], &k3[3]);
    for (int i = 0; i < 4; i++) yy[i] = y[i] + h * k3[i];
    st.x = yy[0]; st.y = yy[1]; st.vx = yy[2]; st.vy = yy[3];
    k4[0] = yy[2]; k4[1] = yy[3]; acc_bar(t + h, &st, &k4[2], &k4[3]);
    St out;
    out.x = y[0] + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]);
    out.y = y[1] + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]);
    out.vx = y[2] + h / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]);
    out.vy = y[3] + h / 6 * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3]);
    return out;
}

static void stumpff(double z, double *C, double *S) {
    if (z > 1e-8) { double sz = sqrt(z); *C = (1 - cos(sz)) / z; *S = (sz - sin(sz)) / (z * sz); }
    else if (z < -1e-8) { double sz = sqrt(-z); *S = (sinh(sz) - sz) / pow(-z, 1.5); *C = (cosh(sz) - 1) / (-z); }
    else { *C = 0.5 - z / 24.0 + z * z / 720.0; *S = 1.0 / 6.0 - z / 120.0 + z * z / 5040.0; }
}

static void kepler(St *s, double dt) {
    if (dt == 0) return;
    double r0 = hypot(s->x, s->y), v2 = s->vx * s->vx + s->vy * s->vy;
    double rdv = s->x * s->vx + s->y * s->vy, alpha = 2.0 / r0 - v2 / GMS;
    double X = sqrt(GMS) * fabs(alpha) * dt;
    if (X == 0) X = 1e-12;
    for (int it = 0; it < 100; it++) {
        double z = alpha * X * X, C, S; stumpff(z, &C, &S);
        double F = (1 - alpha * r0) * X * X * X * S + rdv / sqrt(GMS) * X * X * C + r0 * X - sqrt(GMS) * dt;
        double dF = (1 - alpha * r0) * X * X * C + rdv / sqrt(GMS) * X * (1 - z * S) + r0;
        double dX = F / dF; X -= dX;
        if (fabs(dX) < 1e-14 * (1 + fabs(X))) break;
    }
    double z = alpha * X * X, C, S; stumpff(z, &C, &S);
    double f = 1 - X * X / r0 * C, g = dt - X * X * X / sqrt(GMS) * S;
    double xn = f * s->x + g * s->vx, yn = f * s->y + g * s->vy;
    double rn = hypot(xn, yn);
    double fd = sqrt(GMS) / (rn * r0) * X * (z * S - 1);
    double gd = 1 - X * X / rn * C;
    double vxn = fd * s->x + gd * s->vx, vyn = fd * s->y + gd * s->vy;
    s->x = xn; s->y = yn; s->vx = vxn; s->vy = vyn;
}

static void akick(double t, double x, double y, double *ax, double *ay) {
    double xj = cos(t + THJ0), yj = sin(t + THJ0);
    double dx = x - xj, dy = y - yj, r3 = pow(dx * dx + dy * dy, 1.5);
    *ax = -MU * (dx / r3 + xj);
    *ay = -MU * (dy / r3 + yj);
}

static const double GLX[8] = { 0.019855071751231856, 0.10166676129356630, 0.23723379504183558,
    0.40828267875217510, 0.59171732124782490, 0.76276620495816442, 0.89833323870643370, 0.98014492824876814 };
static const double GLW[8] = { 0.050614268145193569, 0.11119051722668728, 0.15685332293894362,
    0.18134189168918099, 0.18134189168918099, 0.15685332293894362, 0.11119051722668728, 0.050614268145193569 };

static double jacobi(double t, const St *bar) {
    double th = t + THJ0, c = cos(th), s = sin(th);
    double xi = c * bar->x + s * bar->y, eta = -s * bar->x + c * bar->y;
    double vrx0 = bar->vx + bar->y, vry0 = bar->vy - bar->x;
    double vrx = c * vrx0 + s * vry0, vry = -s * vrx0 + c * vry0;
    double dS = hypot(xi + MU, eta), dJ = hypot(xi - 1 + MU, eta);
    double U = GMS / dS + MU / dJ + 0.5 * (xi * xi + eta * eta);
    return 2 * U - (vrx * vrx + vry * vry);
}

static void elems(const St *h, double *a, double *e, double *pom) {
    double r = hypot(h->x, h->y), v2 = h->vx * h->vx + h->vy * h->vy;
    double rv = h->x * h->vx + h->y * h->vy;
    double ex = (v2 / GMS - 1 / r) * h->x - rv / GMS * h->vx;
    double ey = (v2 / GMS - 1 / r) * h->y - rv / GMS * h->vy;
    *e = hypot(ex, ey); *pom = atan2(ey, ex); *a = 1.0 / (2.0 / r - v2 / GMS);
}

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage: %s a e0 F|W kpo locked|golden norbits [thj0]\n", argv[0]); return 1; }
    double a0 = atof(argv[1]), e0 = atof(argv[2]);
    char flavor = argv[3][0];
    double K = atof(argv[4]);
    int golden = (argv[5][0] == 'g');
    double norb = atof(argv[6]);
    if (argc > 7) THJ0 = atof(argv[7]);
    double Tend = 2 * M_PI * norb;

    double pom0 = 0.3, f0 = 1.1, p = a0 * (1 - e0 * e0);
    double rr = p / (1 + e0 * cos(f0));
    St hel = { rr * (cos(pom0) * cos(f0) - sin(pom0) * sin(f0)),
               rr * (sin(pom0) * cos(f0) + cos(pom0) * sin(f0)),
               -sqrt(GMS / p) * (sin(pom0 + f0) + e0 * sin(pom0)),
                sqrt(GMS / p) * (cos(pom0 + f0) - e0 * cos(pom0)) };

    double Tp = 2 * M_PI / sqrt(GMS / (a0 * a0 * a0));
    double PHI = 0.5 * (1 + sqrt(5.0));
    double tau = Tp / (golden ? K * PHI : K);

    double xs, ys, vxs, vys; sun(0, &xs, &ys, &vxs, &vys);
    St tru = { hel.x + xs, hel.y + ys, hel.vx + vxs, hel.vy + vys };
    double cj0t = jacobi(0, &tru);

    St m = hel;
    St b0 = { m.x + xs, m.y + ys, m.vx + vxs, m.vy + vys };
    double cj0m = jacobi(0, &b0);

    double hstep = 2 * M_PI / 8192.0;
    double tt = 0, tcheck = 2 * M_PI, tnext = 0, vprex = 0, vprey = 0, dvx_last = 0, dvy_last = 0;
    int inwin = 0;
    printf("t_jup,cj_err,e_err,pom_err,arel_err,rotdist,cj_truth_drift\n");
    while (tcheck <= Tend + 1e-9) {
        /* march model windows; read out inside the window that holds the checkpoint */
        St rd = m; int have_rd = 0;
        while (tnext < tcheck - 1e-12) {
            double dvx, dvy;
            if (flavor == 'F') {
                St mid = m; kepler(&mid, 0.5 * tau);
                double ax, ay; akick(tnext + 0.5 * tau, mid.x, mid.y, &ax, &ay);
                dvx = tau * ax; dvy = tau * ay;
            } else {
                dvx = dvy = 0;
                for (int q = 0; q < 8; q++) {
                    St pt = m; kepler(&pt, GLX[q] * tau);
                    double ax, ay; akick(tnext + GLX[q] * tau, pt.x, pt.y, &ax, &ay);
                    dvx += GLW[q] * tau * ax; dvy += GLW[q] * tau * ay;
                }
            }
            m.vx += 0.5 * dvx; m.vy += 0.5 * dvy;   /* first half kick at window start */
            if (tnext + tau <= tcheck + 1e-12) {
                kepler(&m, tau);                     /* whole window before the checkpoint */
                m.vx += 0.5 * dvx; m.vy += 0.5 * dvy;
                tnext += tau;
            } else {                                 /* checkpoint inside this window */
                double s = (tcheck - tnext) / tau;
                rd = m; kepler(&rd, s * tau);       /* position and Kepler velocity at s */
                rd.vx += (s - 0.5) * dvx; rd.vy += (s - 0.5) * dvy; /* kick applied linearly */
                have_rd = 1;
                break;
            }
        }
        if (!have_rd) rd = m;                        /* checkpoint exactly at a window end */
        /* truth to the checkpoint */
        while (tt < tcheck - 1e-12) {
            double hh = fmin(hstep, tcheck - tt);
            tru = rk4_step(tt, tru, hh); tt += hh;
        }
        double cjt = jacobi(tt, &tru);
        double xs2, ys2, vxs2, vys2; sun(tt, &xs2, &ys2, &vxs2, &vys2);
        St bm = { rd.x + xs2, rd.y + ys2, rd.vx + vxs2, rd.vy + vys2 };
        double cjm = jacobi(tt, &bm);
        St ht = tru; double xs3, ys3, vxs3, vys3; sun(tt, &xs3, &ys3, &vxs3, &vys3);
        ht.x -= xs3; ht.y -= ys3; ht.vx -= vxs3; ht.vy -= vys3;
        double at, et, pt_, am, em, pm;
        elems(&ht, &at, &et, &pt_); elems(&rd, &am, &em, &pm);
        double dp = pm - pt_; while (dp > M_PI) dp -= 2 * M_PI; while (dp < -M_PI) dp += 2 * M_PI;
        double th = tt + THJ0, cth = cos(th), sth = sin(th);
        double dxi = (bm.x - tru.x) * cth + (bm.y - tru.y) * sth;
        double deta = -(bm.x - tru.x) * sth + (bm.y - tru.y) * cth;
        printf("%.6f,%.3e,%.3e,%.3e,%.3e,%.3e,%.3e\n",
            tt / (2 * M_PI), fabs(cjm - cj0m) + 1e-300, fabs(em - et), dp,
            fabs(am - at) / at, hypot(dxi, deta), fabs(cjt - cj0t) + 1e-300);
        tcheck += 2 * M_PI;
        if (tcheck > Tend + 1e-9) break;
    }
    return 0;
}
