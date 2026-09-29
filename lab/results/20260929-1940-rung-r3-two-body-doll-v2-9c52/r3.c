// Rung r3 v2: two-body doll (EOB), handoffs, gravity assist.
// Oracle parts ported verbatim from xtask/src/gr_oracle_extended.rs (checker-verified).
// Units: binaries in G = M_total = c = 1; transfer/flyby in G = M_sun = 1, time yr/2pi.
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const double PI = 3.14159265358979323846;

// ---------- Gauss-Legendre nodes (n points, computed once) ----------
static double GLX[64], GLW[64];
static void gl_nodes(int n) {
    for (int i = 0; i < n; i++) {
        double x = cos(PI*(i + 0.75)/(n + 0.5));
        for (int it = 0; it < 100; it++) {
            double p0 = 1.0, p1 = x;
            for (int k = 2; k <= n; k++) { double p2 = ((2*k-1)*x*p1 - (k-1)*p0)/k; p0 = p1; p1 = p2; }
            double dp = n*(x*p1 - p0)/(x*x - 1.0);
            double dx = p1/dp; x -= dx;
            if (fabs(dx) < 1e-16) break;
        }
        double p0 = 1.0, p1 = x;
        for (int k = 2; k <= n; k++) { double p2 = ((2*k-1)*x*p1 - (k-1)*p0)/k; p0 = p1; p1 = p2; }
        double dp = n*(x*p1 - p0)/(x*x - 1.0);
        GLX[i] = x; GLW[i] = 2.0/((1 - x*x)*dp*dp);
    }
}
typedef double (*F1)(double, void*);
static double integrate_gl(double lo, double hi, long pieces, int n, F1 f, void* ctx) {
    double h = (hi - lo)/pieces, s = 0;
    for (long i = 0; i < pieces; i++) {
        double a = lo + i*h, m = 0;
        for (int j = 0; j < n; j++) m += GLW[j]*f(a + (1 + GLX[j])*h*0.5, ctx);
        s += m*h*0.5;
    }
    return s;
}

// ---------- Oracle: exact Schwarzschild Darwin orbit (ported) ----------
static void bound_constants(double p, double e, double* E, double* L) {
    *E = sqrt(((p - 2.0)*(p - 2.0) - 4.0*e*e)/(p*(p - 3.0 - e*e)));
    *L = p/sqrt(p - 3.0 - e*e);
}
typedef struct { double p, e, E, L; } QuadCtx;
static double f_dphi(double chi, void* v) { QuadCtx* q = v; return sqrt(q->p/(q->p - 6.0 - 2.0*q->e*cos(chi))); }
static double f_dt(double chi, void* v) {
    QuadCtx* q = v; double c = cos(chi), r = q->p/(1.0 + q->e*c);
    return sqrt(q->p/(q->p - 6.0 - 2.0*q->e*c))*r*r/q->L*q->E/(1.0 - 2.0/r);
}
static double refine(F1 f, void* ctx) {
    long pieces = 16; double v = integrate_gl(0, 2*PI, pieces, 32, f, ctx);
    while (pieces < 1L << 14) {
        pieces *= 2; double w = integrate_gl(0, 2*PI, pieces, 32, f, ctx);
        int done = fabs(w - v) <= 1e-14*fabs(w); v = w; if (done) break;
    }
    return v;
}
// ---------- Oracle: 1PN EIH invariants + Damour-Deruelle (ported) ----------
static double corrf(double r, double nu, double j0) {
    return -(1.0 - 3.0*nu)*pow(j0,4)/(8.0*pow(r,4)) - (3.0 + nu)*j0*j0/(2.0*pow(r,3)) + 1.0/(2.0*r*r);
}
static void eih_invariants(double p, double e, double nu, double* rp, double* vt, double* energy, double* angular) {
    double rp_ = p/(1.0 + e), ra_ = p/(1.0 - e), j0 = sqrt(p);
    double dj = -(corrf(rp_, nu, j0) - corrf(ra_, nu, j0))/(j0*(1.0/(rp_*rp_) - 1.0/(ra_*ra_)));
    double vt_ = (j0 + dj)/rp_*(1.0 - 0.5*(1.0 - 3.0*nu)*j0*j0/(rp_*rp_) - (3.0 + nu)/rp_);
    double v2 = vt_*vt_;
    *rp = rp_; *vt = vt_;
    *energy = 0.5*v2 - 1.0/rp_ + 0.375*(1.0 - 3.0*nu)*v2*v2 + 0.5/rp_*((3.0 + nu)*v2 + 1.0/rp_);
    *angular = rp_*vt_*(1.0 + 0.5*(1.0 - 3.0*nu)*v2 + (3.0 + nu)/rp_);
}
static void damour_deruelle(double energy, double angular, double nu, double* adv, double* per) {
    double q = -2.0*energy;
    double n = pow(q, 1.5)*(1.0 + q*(-15.0 + nu)/8.0);
    *adv = 6.0*PI/(angular*angular);
    *per = 2.0*PI/n;
}
static void schwarzschild_from_invariants(double binding, double angular, double p_guess, double* p, double* e) {
    double l2 = angular*angular, e2 = pow(1.0 + binding, 2), p_ = p_guess;
    for (int i = 0; i < 30; i++) {
        double f = (l2 + 4.0)/p_ - 8.0*l2/(p_*p_) + 16.0*l2/pow(p_,3) - e2;
        double df = -(l2 + 4.0)/(p_*p_) + 16.0*l2/pow(p_,3) - 48.0*l2/pow(p_,4);
        double step = f/df; p_ -= step;
        if (fabs(step) < 2e-14*p_) break;
    }
    *p = p_; *e = sqrt(p_ - 3.0 - p_*p_/l2);
}

// ---------- Dolls (binaries) ----------
// eob-doll: relative motion as exact Schwarzschild test body with M = m1+m2;
// the EOB energy map fixes the constants, and dt_real = (H_real/M) dt_eff rescales the period.
static void doll_eob(double p, double e, double nu, double* adv, double* per) {
    double rp, vt, eps, J; eih_invariants(p, e, nu, &rp, &vt, &eps, &J);
    double hrat = 1.0 + nu*eps;                        // H_real/M
    double Etest = (nu > 1e-12) ? 1.0 + (hrat*hrat - 1.0)/(2.0*nu) : 1.0 + eps;
    double pg, eg; schwarzschild_from_invariants(Etest - 1.0, J, p, &pg, &eg);
    QuadCtx q; bound_constants(pg, eg, &q.E, &q.L); q.p = pg; q.e = eg;
    *adv = refine(f_dphi, &q) - 2*PI;
    *per = hrat*refine(f_dt, &q);
}
// test-mass (negative): the lighter body is a test body around a fixed m1, same turning radii.
static void doll_test(double p, double e, double nu, double* adv, double* per) {
    double m1 = 0.5*(1.0 + sqrt(1.0 - 4.0*nu));
    QuadCtx q; q.p = p/m1; q.e = e; bound_constants(q.p, e, &q.E, &q.L);
    *adv = refine(f_dphi, &q) - 2*PI;
    *per = m1*refine(f_dt, &q);                        // time unit scales with the mass unit
}
// newton-doll (negative): Kepler, M = m1+m2.
static void doll_newton(double p, double e, double nu, double* adv, double* per) {
    double a = p/(1.0 - e*e);
    *adv = 0.0; *per = 2.0*PI*pow(a, 1.5);
}

// ---------- Transfer / flyby ----------
// Units: G = M_sun = 1, AU, time yr/2pi. star + planet + ship (test mass).
static const double MS = 1.0 - 3e-6, MP = 3e-6, MT = 1.0;
static const double CL = 10065.9;                      // c [AU/(yr/2pi)]
static const double RSOI = 0.01;                       // a (m_p / 3 m_s)^{1/3} = 0.01 AU
static const double RP_EARTH = 4.25875e-5;             // AU
static int LAW;                                        // 0 newton, 1 eob, 2 test-mass
static int OWNER;                                      // 0 star doll, 1 planet doll

// relative 1PN harmonic acceleration, total mass M, symmetric ratio nu (eih_ode form)
static void acc_1pn(double M, double nu, double x, double y, double vx, double vy, double* ax, double* ay) {
    double r = sqrt(x*x + y*y), rd = (x*vx + y*vy)/r, v2 = vx*vx + vy*vy;
    double A = -M/(r*r) + (M/(r*r*CL*CL))*((4.0 + 2.0*nu)*M/r - (1.0 + 3.0*nu)*v2 + 1.5*nu*rd*rd);
    double B = (M/(r*r*CL*CL))*(4.0 - 2.0*nu)*rd;
    *ax = A*x/r + B*vx; *ay = A*y/r + B*vy;
}
static void star_state(const double* y, double* x, double* yy, double* vx, double* vy) {
    if (LAW == 2) { *x = 0; *yy = 0; *vx = 0; *vy = 0; }
    else { *x = -MP/MT*y[0]; *yy = -MP/MT*y[1]; *vx = -MP/MT*y[2]; *vy = -MP/MT*y[3]; }
}
static void planet_state(const double* y, double* x, double* yy, double* vx, double* vy) {
    if (LAW == 2) { *x = y[0]; *yy = y[1]; *vx = y[2]; *vy = y[3]; }
    else { *x = MS/MT*y[0]; *yy = MS/MT*y[1]; *vx = MS/MT*y[2]; *vy = MS/MT*y[3]; }
}
static void binary_acc(double x, double y, double vx, double vy, double* ax, double* ay) {
    if (LAW == 0) { double r = sqrt(x*x + y*y); *ax = -MT*x/(r*r*r); *ay = -MT*y/(r*r*r); }
    else if (LAW == 1) acc_1pn(MT, MS*MP/(MT*MT), x, y, vx, vy, ax, ay);
    else acc_1pn(MS, 0.0, x, y, vx, vy, ax, ay);
}
static void deriv_doll(const double* y, double* dy) {
    binary_acc(y[0], y[1], y[2], y[3], &dy[2], &dy[3]);
    dy[0] = y[2]; dy[1] = y[3]; dy[4] = y[6]; dy[5] = y[7];
    double ox, oy, ovx, ovy, M;
    if (OWNER == 0) { star_state(y, &ox, &oy, &ovx, &ovy); M = MS; }
    else { planet_state(y, &ox, &oy, &ovx, &ovy); M = MP; }
    double rx = y[4] - ox, ry = y[5] - oy, r = sqrt(rx*rx + ry*ry);
    if (LAW == 0) { dy[6] = -M*rx/(r*r*r); dy[7] = -M*ry/(r*r*r); }
    else acc_1pn(M, 0.0, rx, ry, y[6] - ovx, y[7] - ovy, &dy[6], &dy[7]);
}
// reference: monolithic N-body under the config's law. The ship feels both bodies
// (Newtonian sum + per-body 1PN test terms; EIH cross terms are < 1e-11 of the signal).
static void deriv_ref(const double* y, double* dy) {
    binary_acc(y[0], y[1], y[2], y[3], &dy[2], &dy[3]);
    dy[0] = y[2]; dy[1] = y[3]; dy[4] = y[6]; dy[5] = y[7];
    double px[2], py[2], vx[2], vy[2];
    star_state(y, &px[0], &py[0], &vx[0], &vy[0]);
    planet_state(y, &px[1], &py[1], &vx[1], &vy[1]);
    double m[2] = {MS, MP}, ax = 0, ay = 0;
    for (int b = 0; b < 2; b++) {
        double rx = y[4] - px[b], ry = y[5] - py[b], r = sqrt(rx*rx + ry*ry);
        ax += -m[b]*rx/(r*r*r); ay += -m[b]*ry/(r*r*r);
        if (LAW != 0) { double qx, qy;
            acc_1pn(m[b], 0.0, rx, ry, y[6] - vx[b], y[7] - vy[b], &qx, &qy);
            ax += qx + m[b]*rx/(r*r*r); ay += qy + m[b]*ry/(r*r*r); }
    }
    dy[6] = ax; dy[7] = ay;
}
typedef void (*Accel)(const double*, double*);
static void rk4(double* y, double h, Accel f) {
    double k1[8], k2[8], k3[8], k4[8], t[8];
    f(y, k1);
    for (int i = 0; i < 8; i++) t[i] = y[i] + 0.5*h*k1[i];
    f(t, k2);
    for (int i = 0; i < 8; i++) t[i] = y[i] + 0.5*h*k2[i];
    f(t, k3);
    for (int i = 0; i < 8; i++) t[i] = y[i] + h*k3[i];
    f(t, k4);
    for (int i = 0; i < 8; i++) y[i] += h/6.0*(k1[i] + 2*k2[i] + 2*k3[i] + k4[i]);
}
static double g_soi(const double* y) {
    double px, py, vx, vy; planet_state(y, &px, &py, &vx, &vy);
    double dx = y[4] - px, dy = y[5] - py;
    return sqrt(dx*dx + dy*dy) - RSOI;
}
static double e_helio(const double* y) {
    double sx, sy, svx, svy; star_state(y, &sx, &sy, &svx, &svy);
    double rx = y[4] - sx, ry = y[5] - sy;
    return 0.5*((y[6]-svx)*(y[6]-svx) + (y[7]-svy)*(y[7]-svy)) - MS/sqrt(rx*rx + ry*ry);
}
static double ATOL = 1e-13, RTOL = 1e-11, HNEXT;
static long NSTEP;
typedef void (*EvCb)(double, const double*, void*);
typedef int (*StopCb)(double, const double*, void*);
static long NCROSS;
static void (*HANDOFF_HOOK)(double, const double*);
static void propagate(double* y, double tmax, int doll, double h0, EvCb ev, void* ctx, StopCb stop) {
    double t = 0, h = h0; NSTEP = 0;
    while (t < tmax) {
        if (t + h > tmax) h = tmax - t;
        double y1[8];
        for (int try_ = 0; try_ < 80; try_++) {
            double y2[8];
            memcpy(y1, y, sizeof(y1)); memcpy(y2, y, sizeof(y2));
            rk4(y1, h, doll ? deriv_doll : deriv_ref);
            rk4(y2, h*0.5, doll ? deriv_doll : deriv_ref); rk4(y2, h*0.5, doll ? deriv_doll : deriv_ref);
            double err = 0;
            for (int i = 0; i < 8; i++) { double e = fabs(y1[i] - y2[i])/(ATOL + RTOL*fabs(y2[i])); if (e > err) err = e; }
            if (err <= 1.0 || h < 1e-13) {
                HNEXT = (err > 1e-28) ? h*fmin(2.2, fmax(0.2, 0.9*pow(err, -0.2))) : h*2.2;
                break;
            }
            h *= fmax(0.1, 0.9*pow(err, -0.25));
        }
        double hb = h;
        if (doll && g_soi(y)*g_soi(y1) < 0) {          // handoff: land exactly on the SOI boundary
            double lo = 0, hi = h, yb[8], g0 = g_soi(y);
            for (int i = 0; i < 70; i++) {
                double mid = 0.5*(lo + hi);
                memcpy(yb, y, sizeof(yb)); rk4(yb, mid, doll ? deriv_doll : deriv_ref);
                if (g0*g_soi(yb) < 0) hi = mid; else lo = mid;
            }
            hb = 0.5*(lo + hi);
            memcpy(y1, y, sizeof(y1)); rk4(y1, hb, doll ? deriv_doll : deriv_ref);
            OWNER = !OWNER; HNEXT = 1e-4; NCROSS++;
            if (HANDOFF_HOOK) HANDOFF_HOOK(t + hb, y1);
        }
        memcpy(y, y1, sizeof(y1)); t += hb; NSTEP++;
        if (ev) ev(t, y, ctx);
        if (stop && stop(t, y, ctx)) return;
        h = HNEXT;
        if (NSTEP > 30000000L) return;
    }
}
// Co-orbital (1:1) initial state: ship at longitude phi, radius 1 - h, on a
// circular orbit of its own radius. Amplitude h near the horseshoe limit makes
// the ship and planet repeat their close encounters, crossing the SOI each time.
static void init_transfer(double phi_deg, double h, double* y) {
    y[0] = 1.0; y[1] = 0.0; y[2] = 0.0; y[3] = 1.0;    // planet rel star, circular
    double rx, ry, vx, vy;
    if (h == -1.0) {
        // figure-eight transfer: 2:1 resonance, e = 0.5, crossing r = 1 AU on the
        // descending leg at longitude phi; phi tunes the first conjunction geometry
        double phi = phi_deg*PI/180.0;
        double a = pow(2.0, 2.0/3.0), ptr = a*0.75;
        double v2 = 2.0 - 1.0/a, vt = sqrt(ptr), vr = -sqrt(v2 - ptr);
        double cx = cos(phi), sx = sin(phi);
        rx = cx; ry = sx; vx = vr*cx - vt*sx; vy = vr*sx + vt*cx;
    } else {
        double phi = phi_deg*PI/180.0, r = 1.0 - h, vt = sqrt(1.0/r);
        double cx = cos(phi), sx = sin(phi);
        rx = r*cx; ry = r*sx; vx = -vt*sx; vy = vt*cx;
    }
    if (LAW == 2) { y[4] = rx; y[5] = ry; y[6] = vx; y[7] = vy; }
    else { y[4] = rx - MP/MT; y[5] = ry; y[6] = vx - MP/MT*y[2]; y[7] = vy - MP/MT*y[3]; }
}
typedef struct { double tlast; FILE* out; const char* tag; double dt; } TrCtx;
static void tr_ev(double t, const double* y, void* v) {
    TrCtx* c = v;
    if (t - c->tlast >= c->dt) {
        double sx, sy, svx, svy; star_state(y, &sx, &sy, &svx, &svy);
        fprintf(c->out, "%s %.9f %.9f %.9f\n", c->tag, t, y[4] - sx, y[5] - sy);
        c->tlast = t;
    }
}
static double EV_T[8192], EV_E[8192]; static int NEV;
static void handoff_hook(double t, const double* y) {
    if (NEV < 8192) { EV_T[NEV] = t; EV_E[NEV] = e_helio(y); NEV++; }
}
static double *REF_T, *REF_E; static long NREF, CREF;
static FILE* RR_OUT; static double RR_LAST;
static void ref_ev(double t, const double* y, void* ctx) {
    (void)ctx;
    if (NREF < CREF) { REF_T[NREF] = t; REF_E[NREF] = e_helio(y); NREF++; }
    if (RR_OUT && t - RR_LAST >= 0.5) {
        double sx, sy, svx, svy; star_state(y, &sx, &sy, &svx, &svy);
        fprintf(RR_OUT, "TRR %.9f %.9f %.9f\n", t, y[4] - sx, y[5] - sy);
        RR_LAST = t;
    }
}
static double interp_ref(double t) {
    long lo = 0, hi = NREF - 1;
    while (hi - lo > 1) { long mid = (lo + hi)/2; if (REF_T[mid] <= t) lo = mid; else hi = mid; }
    double w = (t - REF_T[lo])/(REF_T[hi] - REF_T[lo]);
    return REF_E[lo] + w*(REF_E[hi] - REF_E[lo]);
}
static int mode_transfer(int law, double phi_deg, double h, double tmax, int check) {
    LAW = law; OWNER = 0; NCROSS = 0; NEV = 0; HANDOFF_HOOK = handoff_hook;
    double y[8]; init_transfer(phi_deg, h, y);
    FILE* fd = fopen("tr_doll.txt", "w");
    TrCtx cd = {0, fd, "TRD", 0.5};
    propagate(y, tmax, 1, 1e-4, tr_ev, &cd, NULL);
    fclose(fd);
    long ndoll = NCROSS, nstepd = NSTEP;
    double y2[8]; init_transfer(phi_deg, h, y2);
    CREF = 40000000; REF_T = malloc(CREF*sizeof(double)); REF_E = malloc(CREF*sizeof(double)); NREF = 0;
    RR_OUT = fopen("tr_ref.txt", "w"); RR_LAST = 0;
    propagate(y2, tmax, 0, 1e-4, ref_ev, NULL, NULL);
    fclose(RR_OUT); RR_OUT = NULL;
    double yfinal_ref[8]; memcpy(yfinal_ref, y2, sizeof(yfinal_ref));
    double t_ref_end = REF_T[NREF-1];
    double hs_err = -1;
    if (check) {
        double y3[8]; init_transfer(phi_deg, h, y3);
        double a0 = ATOL, r0 = RTOL; ATOL = a0/8; RTOL = r0/8;
        propagate(y3, tmax, 0, 1e-4, NULL, NULL, NULL);
        ATOL = a0; RTOL = r0;
        hs_err = 0;
        for (int i = 0; i < 8; i++) { double e = fabs(y3[i] - yfinal_ref[i])/(1e-9 + fabs(yfinal_ref[i])); if (e > hs_err) hs_err = e; }
    }
    printf("SUMMARY law %d phi %.4f h %.6f tmax %.4f crossings %ld handoffs %d steps_doll %ld steps_ref %ld t_ref_end %.6f halfstep %.3e\n",
           law, phi_deg, h, tmax, ndoll, NEV, nstepd, NSTEP, t_ref_end, hs_err);
    for (int k = 0; k < NEV; k++)
        printf("EV %d %.9f %.15e %.15e\n", k + 1, EV_T[k], EV_E[k], interp_ref(EV_T[k]));
    // doll final state energy for reference
    printf("EEND %.15e\n", e_helio(y));
    free(REF_T); free(REF_E);
    return 0;
}
static double FB_D = 0.012, FB_VINF = 0.503683;     // 15 km/s; start just outside the SOI
static double MIND;
static void fb_track(double t, const double* y, void* ctx) {
    (void)t; (void)ctx;
    double px, py, vx, vy; planet_state(y, &px, &py, &vx, &vy);
    double d = sqrt((y[4]-px)*(y[4]-px) + (y[5]-py)*(y[5]-py));
    if (d < MIND) MIND = d;
}
static int fb_stop(double t, const double* y, void* ctx) {
    (void)ctx;
    if (t < 0.05) return 0;                           // approach takes ~0.07 units
    double px, py, vx, vy; planet_state(y, &px, &py, &vx, &vy);
    double d = sqrt((y[4]-px)*(y[4]-px) + (y[5]-py)*(y[5]-py));
    return d >= FB_D;
}
// Aim: start D=FB_D from the planet, velocity v_inf toward the planet's position
// led by the meeting time (circular motion), with a lateral offset s that a
// bisection on the reference sets so the realized closest approach equals b.
static double AIM_S;
static void init_flyby(double b_unused, double* y) {
    (void)b_unused;
    y[0] = 1.0; y[1] = 0.0; y[2] = 0.0; y[3] = 1.0;    // planet rel star, circular
    // planet position/velocity at t=0 (frame origin handled per law below)
    // overtaking geometry: ship D ahead along the orbit (planet at (1,0) moving +y),
    // lateral offset AIM_S; the planet overtakes the ship, so the planet-frame
    // incoming v_inf is (0, -v_inf). A bisection on AIM_S fixes the realized b.
    if (LAW == 2) {
        y[4] = 1.0 + AIM_S; y[5] = FB_D; y[6] = 0.0; y[7] = 1.0 - FB_VINF;
    } else {
        y[4] = MS/MT + AIM_S; y[5] = FB_D;
        y[6] = -MP/MT*y[2]; y[7] = MS/MT - FB_VINF;
    }
}
static int mode_flyby(int law, double b_rp, int check) {
    LAW = law;
    double b_au = b_rp*RP_EARTH;
    double dmin = -1;
    // noaim mode: analytic offset aim = -1.05 b (bisection-verified near-identity);
    // the realized closest approach is recorded and the metric compares doll vs
    // reference on identical initial conditions.
    if (getenv("NOAIM")) { AIM_S = -1.05*b_au; dmin = -1; }
    else {
    double slo = -0.002, shi = 0.002;
    for (int it = 0; it < 22; it++) {
        AIM_S = 0.5*(slo + shi);
        double yt[8]; OWNER = 0; NCROSS = 0; MIND = 1e9; LAW = law;
        init_flyby(b_au, yt);
        propagate(yt, 0.8, 0, 1e-5, fb_track, NULL, fb_stop);
        dmin = MIND;
        if (dmin > b_au) slo = AIM_S; else shi = AIM_S;
    }
    }
    OWNER = 0; NCROSS = 0; NEV = 0; HANDOFF_HOOK = handoff_hook; MIND = 1e9;
    double y[8], y0[8]; init_flyby(b_au, y); memcpy(y0, y, sizeof(y0));
    propagate(y, 3.0, 1, 1e-5, fb_track, NULL, fb_stop);
    double dvx = y[6] - y0[6], dvy = y[7] - y0[7];
    long cs = NCROSS; double mind_d = MIND;
    double y2[8]; init_flyby(b_au, y2); memcpy(y0, y2, sizeof(y0));
    MIND = 1e9; propagate(y2, 3.0, 0, 1e-5, fb_track, NULL, fb_stop);
    double dvx2 = y2[6] - y0[6], dvy2 = y2[7] - y0[7];
    double hs_err = -1;
    if (check) {
        double y3[8]; init_flyby(b_au, y3);
        double a0 = ATOL, r0 = RTOL; ATOL = a0/8; RTOL = r0/8;
        propagate(y3, 3.0, 0, 1e-5, NULL, NULL, fb_stop);
        ATOL = a0; RTOL = r0;
        hs_err = sqrt(pow(y3[6]-y2[6],2) + pow(y3[7]-y2[7],2));
    }
    printf("FB law %d b_rp %.6f aim %.8e dmin_aim %.8e mind_doll %.8e mind_ref %.8e crossings %ld dv_doll %.12e %.12e dv_ref %.12e %.12e halfstep_v %.3e\n",
           law, b_rp, AIM_S, dmin, mind_d, MIND, cs, dvx, dvy, dvx2, dvy2, hs_err);
    return 0;
}
int main(int argc, char** argv) {
    gl_nodes(32);
    if (argc >= 2 && !strcmp(argv[1], "bin")) {
        printf("p,e,nu,Aor,Por,Por0,Aeob,Peob,Aeob0,Peob0,Atm,Ptm,Anw,Pnw,epsp,epsT,epsn\n");
        double p, e, nu;
        while (scanf("%lf %lf %lf", &p, &e, &nu) == 3) {
            double rp, vt, eps, J; eih_invariants(p, e, nu, &rp, &vt, &eps, &J);
            double Aor, Por; damour_deruelle(eps, J, nu, &Aor, &Por);
            double rp0, vt0, eps0, J0; eih_invariants(p, e, 0.0, &rp0, &vt0, &eps0, &J0);
            double Aor0, Por0; damour_deruelle(eps0, J0, 0.0, &Aor0, &Por0);
            double Ae, Pe, Ae0, Pe0, At, Pt, An, Pn;
            doll_eob(p, e, nu, &Ae, &Pe);
            doll_eob(p, e, 0.0, &Ae0, &Pe0);
            doll_test(p, e, nu, &At, &Pt);
            doll_newton(p, e, nu, &An, &Pn);
            // Truncation estimates (config-independent), derived in dossier.md:
            // prec: 1PN oracle advance vs exact test-mass solution in the oracle's own
            //   harmonic convention: (7.5 + e^2 + 5nu)/p  [measured family]
            // period: next-PN content of the coordinate period: (4 + 2nu)/a^2, a = p/(1-e^2)
            // nu: consecutive-PN ratio on the DD nu-sector: 4|E_eih|
            double epsp = (7.5 + e*e + 5.0*nu)/p;
            double aa = p/(1.0 - e*e);
            double epsT = (4.0 + 2.0*nu)/(aa*aa);
            double epsn = -4.0*eps;
            printf("%.12g,%.12g,%.12g,%.15g,%.15g,%.15g,%.15g,%.15g,%.15g,%.15g,%.15g,%.15g,%.15g,%.15g,%.10g,%.10g,%.10g\n",
                   p, e, nu, Aor, Por, Por0, Ae, Pe, Ae0, Pe0, At, Pt, An, Pn, epsp, epsT, epsn);
        }
        return 0;
    }
    if (argc >= 6 && !strcmp(argv[1], "transfer")) {
        int law = atoi(argv[2]); double phi = atof(argv[3]), h = atof(argv[4]), tmax = atof(argv[5]);
        int check = (argc >= 7 && !strcmp(argv[6], "check"));
        return mode_transfer(law, phi, h, tmax, check);
    }
    if (argc >= 4 && !strcmp(argv[1], "flyby")) {
        int law = atoi(argv[2]); double b = atof(argv[3]);
        int check = (argc >= 5 && !strcmp(argv[4], "check"));
        return mode_flyby(law, b, check);
    }
    fprintf(stderr, "usage: r3 bin | r3 transfer <law 0|1|2> <phi0_deg> <tmax> [check] | r3 flyby <law> <b_Rp> [check]\n");
    return 1;
}
