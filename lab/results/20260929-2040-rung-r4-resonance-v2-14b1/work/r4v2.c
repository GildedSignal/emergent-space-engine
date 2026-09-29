/* Rung r4 v2: arc-integrated kicks vs averaging, mean-motion resonance 2:1.
 *
 * System (restricted 3-body, coplanar, G=1): primary M=1; inner test particle
 * m1=0; perturber m2=3e-3 on a circular orbit. Truth: barycentric N-body RK4,
 * fixed step h = P1/steps_per_orbit (float64). Law: elements frozen between
 * window ends; kick = first-order Gauss-Picard integral of the full direct+
 * indirect perturbing acceleration along the unperturbed arc, applied at the
 * window end (delta r and delta v). Windows: arc = between conjunctions
 * (lambda1 = lambda2 mod 2pi); archalf = every alignment mod pi (two per
 * synodic period); avg = once per inner orbit, perturber frozen at the window
 * midpoint; none = no perturbation.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define PI 3.14159265358979323846264338327950288

static const double MU   = 1.0;    /* G*M for the inner orbit about the primary */
static const double M2   = 3.0e-3; /* perturber mass ratio */
static const double A1   = 1.0;
static const double W1   = 0.0;    /* varpi_1(0) */
static const double M10  = 0.0;    /* inner mean anomaly at t=0 (pericentre) */
static const double W2   = 0.0;    /* varpi_2 */
static const int    NSYN = 200;    /* duration in synodic periods */
static const double DTS  = (2.0*PI/25.0); /* sample cadence: 25 per inner orbit */

static double E1_INIT = 0.01;     /* inner eccentricity at t=0 (calibratable) */
static double E2_INIT = 0.0;      /* perturber eccentricity (0 = circular) */

typedef struct { double a, e, w, M; } El;   /* M at the epoch owned by caller */

typedef struct { const char *name; double ratio, lam20; } Case;
static const Case CASES[5] = {
    {"res-2to1",       2.00, 0.0},
    {"res-2to1-shift", 2.00, 4.0},
    {"ctrl-r5.00",     5.00, 0.0},
    {"ctrl-r2.55",     2.55, 0.0},
    {"ctrl-r2.15",     2.15, 0.0},
};

/* ---------------- Gauss-Legendre ---------------- */
static void legendre(int n, double z, double *p, double *dp) {
    double pm1 = 1.0, pv = z;
    if (n == 0) { *p = 1.0; *dp = 0.0; return; }
    for (int j = 2; j <= n; j++) {
        double q = ((2*j-1)*z*pv - (j-1)*pm1)/j;
        pm1 = pv; pv = q;
    }
    *p = pv; *dp = n*(z*pv - pm1)/(z*z - 1.0);
}
static void gl_nodes(int n, double *x, double *w) {
    for (int i = 0; i <= (n-1)/2; i++) {
        double z = cos(PI*(i + 0.75)/(n + 0.5)), p, dp;
        for (int it = 0; it < 200; it++) {
            legendre(n, z, &p, &dp);
            double dz = -p/dp; z += dz;
            if (fabs(dz) < 1e-16) break;
        }
        legendre(n, z, &p, &dp);
        x[i] = z; x[n-1-i] = -z;
        double wi = 2.0/((1.0 - z*z)*dp*dp);
        w[i] = wi; w[n-1-i] = wi;
    }
}

/* ---------------- Kepler ---------------- */
static double kepler_E(double M, double e) {
    double E = M + e*sin(M);
    double lo = M - e - 1e-12, hi = M + e + 1e-12;   /* root bracket: |E-M| <= e */
    for (int it = 0; it < 200; it++) {
        double f = E - e*sin(E) - M, fp = 1.0 - e*cos(E), d = f/fp;
        E -= d;
        if (E < lo) E = lo; else if (E > hi) E = hi;
        if (fabs(d) < 1e-16) break;
    }
    return E;
}
static void el_rv(const El *el, double mu, double te, double t, double *r, double *v) {
    double a = el->a, e = el->e;
    double n = sqrt(mu/(a*a*a));
    double M = el->M + n*(t - te);
    double E = kepler_E(M, e);
    double xo = a*(cos(E) - e), yo = a*sqrt(1-e*e)*sin(E);
    double den = 1.0 - e*cos(E);
    double vxo = -a*n*sin(E)/den, vyo = a*n*sqrt(1-e*e)*cos(E)/den;
    double cw = cos(el->w), sw = sin(el->w);
    r[0] = xo*cw - yo*sw; r[1] = xo*sw + yo*cw;
    v[0] = vxo*cw - vyo*sw; v[1] = vxo*sw + vyo*cw;
}
static void rv_el(const double *r, const double *v, double mu, El *el) {
    double R = hypot(r[0], r[1]);
    double v2 = v[0]*v[0] + v[1]*v[1];
    double vr = (r[0]*v[0] + r[1]*v[1])/R;
    double a = 1.0/(2.0/R - v2/mu);
    double f1 = v2/mu - 1.0/R;
    double ex = f1*r[0] - vr*R*v[0]/mu, ey = f1*r[1] - vr*R*v[1]/mu;
    double e = hypot(ex, ey);
    double w, M;
    if (e > 1e-13) {
        w = atan2(ey, ex);
        double cosE = (1.0 - R/a)/e, sinE = vr*R/(e*sqrt(mu*a));
        double E = atan2(sinE, cosE);
        M = E - e*sin(E);
    } else { w = atan2(r[1], r[0]); M = w; e = 0.0; }
    el->a = a; el->e = e; el->w = w; el->M = M;
}
/* continuous true longitude (branch-safe for unwrapped M) */
static double lam_of(const El *el, double mu, double te, double t) {
    double n = sqrt(mu/(el->a*el->a*el->a));
    double M = el->M + n*(t - te);
    double beta = el->e/(1.0 + sqrt(1.0 - el->e*el->e));
    double f = M + 2.0*atan2(beta*sin(M), 1.0 - beta*cos(M));
    return el->w + f;
}
/* wrapped true longitude from wrapped M (sampling only) */
static double lam_wrap(const El *el) {
    double beta = el->e/(1.0 + sqrt(1.0 - el->e*el->e));
    double f = el->M + 2.0*atan2(beta*sin(el->M), 1.0 - beta*cos(el->M));
    double l = el->w + f;
    l = fmod(l, 2.0*PI); if (l < 0) l += 2.0*PI;
    return l;
}

/* ---------------- perturber + disturbing acceleration ---------------- */
typedef struct { El e2; double T; } Setup;      /* perturber on a fixed ellipse */
static Setup setup_of(const Case *c) {
    Setup s;
    double ratio = c->ratio;
    if (getenv("RATIO")) ratio = atof(getenv("RATIO"));  /* calibration only */
    if (getenv("E2")) E2_INIT = atof(getenv("E2"));      /* calibration only */
    double n2 = 1.0/ratio;                     /* n1 = 1 (a1=1, mu=1) */
    s.e2.a = cbrt((1.0 + M2)/(n2*n2));         /* exact two-body about primary */
    s.e2.e = E2_INIT;
    s.e2.w = c->lam20;                         /* w2 */
    s.e2.M = 0.0;
    s.T = NSYN * 2.0*PI/(1.0 - n2);
    return s;
}
static void pert_rv(const Setup *s, double t, double *r2) {
    double v2[2];
    el_rv(&s->e2, 1.0 + M2, 0.0, t, r2, v2);
}
/* continuous mean longitude of the perturber */
static double lam2_of(const Setup *s, double t) {
    return lam_of(&s->e2, 1.0 + M2, 0.0, t);
}
/* full direct + indirect perturbing acceleration on the inner body */
static void a_pert(const Setup *s, double t, const double *r, double *a) {
    double r2[2]; pert_rv(s, t, r2);
    double dx = r2[0]-r[0], dy = r2[1]-r[1];
    double d3 = pow(dx*dx+dy*dy, 1.5);
    double r2n = pow(r2[0]*r2[0] + r2[1]*r2[1], 1.5);
    a[0] = M2*(dx/d3 - r2[0]/r2n);
    a[1] = M2*(dy/d3 - r2[1]/r2n);
}
/* the same with the perturber frozen at time tf (for the averaged config) */
static void a_pert_frozen(const Setup *s, const double *r, double *a, double tf) {
    double r2[2]; pert_rv(s, tf, r2);
    double dx = r2[0]-r[0], dy = r2[1]-r[1];
    double d3 = pow(dx*dx+dy*dy, 1.5);
    double r2n = pow(r2[0]*r2[0] + r2[1]*r2[1], 1.5);
    a[0] = M2*(dx/d3 - r2[0]/r2n);
    a[1] = M2*(dy/d3 - r2[1]/r2n);
}

/* ---------------- series writer ---------------- */
typedef struct { FILE *f; long n; double se, ce; double maxe; } Series;
static void ser_emit(Series *s, double t, double e, double phi) {
    double p = fmod(phi, 2.0*PI); if (p < 0) p += 2.0*PI;
    fprintf(s->f, "%.9f %.9f %.9f\n", t, e, p);
    s->n++;
    s->se += sin(p); s->ce += cos(p);
    if (e > s->maxe) s->maxe = e;
}

/* ---------------- the law ---------------- */
/* mode 0: arc (windows at conjunctions); 1: archalf (alignments mod pi);
 * mode 2: avg (one window per inner orbit, frozen perturber); 3: none */
static long law_run(const Case *c, int mode, int nodes, const char *path,
                    double *out_conc, double *out_maxe, long *out_samples) {
    Setup s = setup_of(c);
    El el = { A1, E1_INIT, W1, M10 };
    double te = 0.0;
    Series ser; ser.f = fopen(path, "w"); ser.n = 0; ser.se = ser.ce = 0.0; ser.maxe = 0.0;
    double gx[64], gw[64];
    if (mode <= 2) gl_nodes(nodes, gx, gw);
    double q = (mode == 0) ? 2.0*PI : PI;
    long windows = 0;
    double t = 0.0, next_sample = DTS;
    int guard = 0;
    while (t < s.T) {
        double t1;
        if (mode == 2) {
            t1 = t + 2.0*PI*sqrt(el.a*el.a*el.a/MU);
            if (t1 > s.T) t1 = s.T + 1.0;
        } else if (mode == 3) {
            t1 = s.T + 1.0;
        } else {
            double Dnow = lam_of(&el, MU, te, t) - lam2_of(&s, t);
            double target = (floor(Dnow/q) + 1.0)*q;
            while (target < Dnow + q*1e-9) target += q;
            double tb = t + q/0.05;
            while (lam_of(&el, MU, te, tb) - lam2_of(&s, tb) < target) tb += q/0.05;
            double lo = t, hi = tb;
            for (int it = 0; it < 200; it++) {
                double mid = 0.5*(lo + hi);
                double Dm = lam_of(&el, MU, te, mid) - lam2_of(&s, mid);
                if (Dm < target) lo = mid; else hi = mid;
            }
            t1 = 0.5*(lo + hi);
        }
        /* emit uniform samples inside this window with frozen elements */
        double t_end_sample = (t1 < s.T ? t1 : s.T);
        for (; next_sample <= t_end_sample + 1e-9; next_sample += DTS) {
            double lam1 = lam_of(&el, MU, te, next_sample);
            double lam2v = lam2_of(&s, next_sample);
            ser_emit(&ser, next_sample, el.e, 2.0*lam2v - lam1 - el.w);
        }
        /* kick at the window end: Gauss-Picard on the invariants.
         * d(alpha) = integral of the Gauss planetary rates along the
         * unperturbed arc, by Gauss-Legendre quadrature. Element space:
         * no dense dynamics steps, no state refit. */
        if (mode <= 2 && t1 <= s.T) {
            double W = t1 - t, half = 0.5*(t + t1);
            double Da = 0, De = 0, Dw = 0, DM = 0;
            double n0 = sqrt(MU/(el.a*el.a*el.a));
            for (int k = 0; k < nodes; k++) {
                double tk = half + 0.5*W*gx[k];
                double r[2], v[2];
                El tmp = el;
                el_rv(&tmp, MU, te, tk, r, v);
                double a[2];
                if (mode == 2) a_pert_frozen(&s, r, a, half);   /* perturber frozen */
                else           a_pert(&s, tk, r, a);
                double R = hypot(r[0], r[1]);
                double urx = r[0]/R, ury = r[1]/R;
                double Rc = urx*a[0] + ury*a[1];            /* radial component */
                double Sc = -ury*a[0] + urx*a[1];           /* transverse component */
                double Mk = el.M + n0*(tk - te);
                double E = kepler_E(Mk, el.e);
                double f = 2.0*atan2(sqrt(1.0+el.e)*sin(0.5*E), sqrt(1.0-el.e)*cos(0.5*E));
                double cf = cos(f), sf = sin(f);
                double sq = sqrt(1.0 - el.e*el.e);
                double da = 2.0/(n0*sq)*(el.e*sf*Rc + (1.0 + el.e*cf)*Sc);
                double de = sq/(n0*el.a)*(sf*Rc + (cf + cos(E))*Sc);
                double dw = sq/(n0*el.a*el.e)*(-cf*Rc + (1.0 + 1.0/(1.0+el.e*cf))*sf*Sc);
                double dM = -(2.0/(n0*el.a))*(R/el.a)*Rc - sq*dw;
                double wk = 0.5*W*gw[k];
                Da += wk*da; De += wk*de; Dw += wk*dw; DM += wk*dM;
            }
            el.M += n0*W;          /* unperturbed mean-anomaly drift to the window end */
            el.a += Da; el.e += De; el.w += Dw; el.M += DM;
            if (getenv("KICKDUMP") && windows <= 8)
                fprintf(stderr, "W%03ld t=%.6f a=%.6f e=%.6f w=%.6f Da=%.3e De=%.3e Dw=%.3e DM=%.3e\n",
                        windows, t1, el.a, el.e, el.w, Da, De, Dw, DM);
            te = t1; windows++;
            if (el.e > 0.95 || el.e < 1e-6 || el.a <= 0.2 || el.a >= 4.0) { guard = 1; break; }
        }
        t = t1;
        if (guard) break;
    }
    fclose(ser.f);
    *out_conc = hypot(ser.se, ser.ce)/(double)ser.n;
    *out_maxe = ser.maxe;
    *out_samples = ser.n;
    return windows;
}

/* ---------------- truth: barycentric N-body RK4 ---------------- */
static void nb_accel(const double *y, double *dydt) {
    const double ms[3] = { 1.0, M2, 0.0 };
    double acc[6] = {0,0,0,0,0,0};
    for (int i = 0; i < 3; i++)
        for (int j = i+1; j < 3; j++) {
            double rx = y[2*j] - y[2*i], ry = y[2*j+1] - y[2*i+1];
            double r3 = pow(rx*rx + ry*ry, 1.5);
            acc[2*i]   += ms[j]*rx/r3; acc[2*i+1] += ms[j]*ry/r3;
            acc[2*j]   -= ms[i]*rx/r3; acc[2*j+1] -= ms[i]*ry/r3;
        }
    for (int i = 0; i < 3; i++) {
        dydt[2*i]   = y[6+2*i];
        dydt[2*i+1] = y[6+2*i+1];
        dydt[6+2*i] = acc[2*i];
        dydt[6+2*i+1] = acc[2*i+1];
    }
}
static void truth_run(const Case *c, int steps, const char *path,
                      double *out_conc, double *out_maxe, long *out_samples, long *out_steps) {
    Setup s = setup_of(c);
    double h = 2.0*PI/(double)steps;
    double y[12], k1[12], k2[12], k3[12], k4[12], yt[12];
    /* primary at origin at rest; perturber on its exact fixed ellipse */
    double r2[2], v2[2];
    el_rv(&s.e2, 1.0 + M2, 0.0, 0.0, r2, v2);
    y[0]=0; y[1]=0; y[2]=r2[0]; y[3]=r2[1];
    y[6]=0; y[7]=0; y[8]=v2[0]; y[9]=v2[1];
    /* particle heliocentric start */
    El el0 = { A1, E1_INIT, W1, M10 };
    double r1[2], v1[2];
    el_rv(&el0, MU, 0.0, 0.0, r1, v1);
    y[4]=r1[0]; y[5]=r1[1]; y[10]=v1[0]; y[11]=v1[1];

    Series ser; ser.f = fopen(path, "w"); ser.n = 0; ser.se = ser.ce = 0.0; ser.maxe = 0.0;
    double t = 0.0, next_sample = DTS;
    long nsteps = 0;
    while (t < s.T - 1e-12) {
        double hh = (t + h <= s.T) ? h : s.T - t;
        nb_accel(y, k1);
        for (int i = 0; i < 12; i++) yt[i] = y[i] + 0.5*hh*k1[i];
        nb_accel(yt, k2);
        for (int i = 0; i < 12; i++) yt[i] = y[i] + 0.5*hh*k2[i];
        nb_accel(yt, k3);
        for (int i = 0; i < 12; i++) yt[i] = y[i] + hh*k3[i];
        nb_accel(yt, k4);
        for (int i = 0; i < 12; i++) y[i] += hh/6.0*(k1[i] + 2*k2[i] + 2*k3[i] + k4[i]);
        t += hh; nsteps++;
        while (next_sample <= t + 1e-12) {
            double rp[2] = { y[4]-y[0], y[5]-y[1] }, vp[2] = { y[10]-y[6], y[11]-y[7] };
            double rq[2] = { y[2]-y[0], y[3]-y[1] }, vq[2] = { y[8]-y[6],  y[9]-y[7] };
            El e1, e2;
            rv_el(rp, vp, MU, &e1);
            rv_el(rq, vq, 1.0 + M2, &e2);
            double lam1 = lam_wrap(&e1), lam2 = lam_wrap(&e2);
            ser_emit(&ser, next_sample, e1.e, 2.0*lam2 - lam1 - e1.w);
            next_sample += DTS;
        }
    }
    fclose(ser.f);
    *out_conc = hypot(ser.se, ser.ce)/(double)ser.n;
    *out_maxe = ser.maxe;
    *out_samples = ser.n;
    *out_steps = nsteps;
}

/* ---------------- self-test: osculating round-trip ---------------- */
static double selftest(void) {
    double worst = 0.0;
    int shown = 0;
    for (double a = 0.3; a <= 3.0; a *= 1.3)
        for (double e = 1e-3; e <= 0.9; e *= 1.7)
            for (double M = -PI; M <= PI; M += 0.37)
                for (double w = -PI; w <= PI; w += 0.9) {
                    El el = { a, e, w, M };
                    double r[2], v[2];
                    el_rv(&el, MU, 0.0, 0.0, r, v);
                    El el2;
                    rv_el(r, v, MU, &el2);
                    double r2[2], v2[2];
                    el_rv(&el2, MU, 0.0, 0.0, r2, v2);
                    double err = hypot(r2[0]-r[0], r2[1]-r[1]) + hypot(v2[0]-v[0], v2[1]-v[1]);
                    if (err > 1e-12 && shown < 8) {
                        printf("rt-fail a=%.3f e=%.5f M=%.4f w=%.3f err=%.3e (el2 a=%.4f e=%.5f w=%.3f M=%.4f)\n",
                               a, e, M, w, err, el2.a, el2.e, el2.w, el2.M);
                        shown++;
                    }
                    if (err > worst) worst = err;
                }
    return worst;
}

int main(int argc, char **argv) {
    if (argc < 2 || (argc < 3 && strcmp(argv[1], "selftest"))) {
        fprintf(stderr, "usage: r4v2 selftest | truth <case> <steps> <file> [e1]"
                        " | arc|archalf <case> <nodes> <file> [e1] | avg|none <case> <file> [e1]\n");
        return 2;
    }
    if (!strcmp(argv[1], "selftest")) {
        printf("{\"roundtrip_max\": %.3e}\n", selftest());
        return 0;
    }
    const char *mode = argv[1];
    int ci = atoi(argv[2]);
    if (ci < 0 || ci > 4) { fprintf(stderr, "bad case\n"); return 2; }
    double conc, maxe; long samples, windows = 0, steps = 0;
    const char *cfg, *path;
    if (!strcmp(mode, "truth")) {
        int st = atoi(argv[3]); path = argv[4];
        if (argc > 5) E1_INIT = atof(argv[5]);
        truth_run(&CASES[ci], st, path, &conc, &maxe, &samples, &steps);
        cfg = (st == 600) ? "truth-600" : (st == 1200) ? "truth-1200" : "truth-2400";
        printf("{\"config\": \"%s\", \"case\": \"%s\", \"max_e\": %.6f, \"conc\": %.6f, "
               "\"windows\": 0, \"dense_steps\": %ld, \"samples\": %ld, \"quad_nodes\": 0, "
               "\"kicks_per_orbit\": 0.0}\n",
               cfg, CASES[ci].name, maxe, conc, steps, samples);
        return 0;
    }
    int nodes = 0, argpath;
    if (!strcmp(mode, "arc") || !strcmp(mode, "archalf")) {
        nodes = atoi(argv[3]); path = argv[4]; argpath = 4;
    } else if (!strcmp(mode, "avg")) {
        nodes = 64; path = argv[3]; argpath = 3;
    } else if (!strcmp(mode, "none")) {
        nodes = 0; path = argv[3]; argpath = 3;
    } else { fprintf(stderr, "bad mode\n"); return 2; }
    if (argc > argpath + 1) E1_INIT = atof(argv[argpath + 1]);
    int m = !strcmp(mode, "arc") ? 0 : !strcmp(mode, "archalf") ? 1 : !strcmp(mode, "avg") ? 2 : 3;
    windows = law_run(&CASES[ci], m, nodes, path, &conc, &maxe, &samples);
    Setup s = setup_of(&CASES[ci]);
    double kpo = (double)windows/(s.T/(2.0*PI));
    printf("{\"config\": \"%s\", \"case\": \"%s\", \"max_e\": %.6f, \"conc\": %.6f, "
           "\"windows\": %ld, \"dense_steps\": 0, \"samples\": %ld, \"quad_nodes\": %d, "
           "\"kicks_per_orbit\": %.6f}\n",
           mode, CASES[ci].name, maxe, conc, windows, samples, nodes, kpo);
    return 0;
}
