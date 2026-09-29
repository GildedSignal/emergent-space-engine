/* rung3_ships.c — rung r3 ships: continuous 3-body reference, doll segments (Kepler or
 * exact Schwarzschild geodesic legs with SOI-crossing handoffs), and flyby assists.
 * Units: AU, yr, Msun, G = 4 pi^2. Star 1 Msun, planet 3e-6 Msun at 1 AU circular.
 * Reference: adaptive RK4 with step-doubling, half-step agreement < 1e-9 (rung spec).
 *
 * Modes:
 *   ref3 <t_end>              stdin: "xs ys vxs vys" (ship heliocentric). Prints
 *                             CROSS lines at refined SOI crossings, then DONE.
 *   dollseg <cfg> <kind>      cfg: kepler|schw, kind: star|planet.
 *                             stdin: "t xs ys vxs vxs" (heliocentric ship + time).
 *                             Propagates the doll until the next SOI crossing
 *                             (star: heliocentric leg w/ moving planet SOI event;
 *                              planet: planet-frame leg w/ |xi|=SOI event).
 *                             Prints SEG <t_cross> <state helio> <state frame>.
 *   flyby <cfg> <tol>         stdin: b list (planet radii, one per line).
 *                             Prints FLY <b> <t_end> <dv_doll..> <dv_ref..> <rperi>.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

static const double G = 39.478417604357434;
static const double MSTAR = 1.0, MPL = 3.0e-6;
static const double AP = 1.0, WP = 6.283185307179586;
static const double RP_AU = 6371.0/1.495978707e8;
static const double C_AUYR = 299792.458/(1.495978707e8/3.15576e7);
static const double SOI = 0.006178008505674118;  /* (3e-6)^(2/5) */
static const double MU_P = 0.0001184352528130723;

static void planet_eph(double t, double pos[2], double vel[2]) {
    double c = cos(WP*t), s = sin(WP*t);
    pos[0] = AP*c; pos[1] = AP*s;
    vel[0] = -AP*WP*s; vel[1] = AP*WP*c;
}

/* ---------- adaptive RK4 + step doubling + Richardson ---------- */
typedef void (*deriv_t)(double, const double*, double*);

static void rk4(double t, const double *y, double h, int n, deriv_t f, double *out) {
    static double k1[12], k2[12], k3[12], k4[12], tmp[12];
    int i;
    f(t, y, k1);
    for (i = 0; i < n; i++) tmp[i] = y[i] + 0.5*h*k1[i];
    f(t + 0.5*h, tmp, k2);
    for (i = 0; i < n; i++) tmp[i] = y[i] + 0.5*h*k2[i];
    f(t + 0.5*h, tmp, k3);
    for (i = 0; i < n; i++) tmp[i] = y[i] + h*k3[i];
    f(t + h, tmp, k4);
    for (i = 0; i < n; i++) out[i] = y[i] + h*(k1[i] + 2*k2[i] + 2*k3[i] + k4[i])/6.0;
}

/* advance one accepted step; returns scaled error estimate */
static double step_adaptive(double t, double *y, double *h, int n, deriv_t f, double tol) {
    double y1[12], ya[12], yb[12], err;
    int i;
    for (;;) {
        rk4(t, y, *h, n, f, y1);
        rk4(t, y, *h*0.5, n, f, ya);
        rk4(t + *h*0.5, ya, *h*0.5, n, f, yb);
        err = 0.0;
        for (i = 0; i < n; i++) {
            double e = fabs(yb[i]-y1[i])/(1.0+fabs(yb[i]));
            if (e > err) err = e;
        }
        if (err <= tol || *h < 1e-13) break;
        *h *= 0.5;
    }
    for (i = 0; i < n; i++) y[i] = yb[i] + (yb[i]-y1[i])/15.0;
    double fac = err > 0 ? 0.9*pow(tol/err, 0.25) : 2.0;
    if (fac > 2.0) fac = 2.0;
    if (fac < 0.3) fac = 0.3;
    double hacc = *h;
    *h = hacc*fac;
    return hacc;   /* accepted step length */
}

/* integrate with event g(t,y) (crossing when sign changes), or to t_end if g==NULL */
typedef double (*event_t)(double, const double*);

static double integrate_event(double t0, const double *y0, int n, deriv_t f, event_t g,
                              double t_end, double tol, double *y_out, int *crossed) {
    double y[12], h, t = t0;
    memcpy(y, y0, sizeof(double)*n);
    h = 1e-5;
    *crossed = 0;
    double gprev = g ? g(t, y) : 0.0;
    while (t < t_end - 1e-15) {
        if (t + h > t_end) h = t_end - t;
        double yprev[12], tprev = t;
        memcpy(yprev, y, sizeof(double)*n);
        double used = step_adaptive(t, y, &h, n, f, tol);
        t += used;
        if (used < 1e-16) break;
        if (g) {
            double gnow = g(t, y);
            if (gprev == 0.0) gprev = 1e-30;
            if (gnow*gprev < 0.0) {
                /* bisect between tprev and t by re-stepping */
                double lo = tprev, hi = t, mid, yl[12], gm[12];
                memcpy(yl, yprev, sizeof(double)*n);
                for (int it = 0; it < 80; it++) {
                    mid = 0.5*(lo+hi);
                    double hh = mid - tprev;
                    double ym[12];
                    rk4(tprev, yprev, hh, n, f, ym);
                    memcpy(gm, ym, sizeof(double)*n);
                    double gmval = g(mid, gm);
                    if (gmval*gprev < 0.0) hi = mid; else { lo = mid; memcpy(yl, gm, sizeof(double)*n); }
                }
                double hh = hi - tprev;
                rk4(tprev, yprev, hh, n, f, y);
                memcpy(y_out, y, sizeof(double)*n);
                *crossed = 1;
                return hi;
            }
            gprev = gnow;
        }
    }
    memcpy(y_out, y, sizeof(double)*n);
    return t;
}

/* ---------- 3-body reference (star+planet mutual, ship test particle) ---------- */
typedef struct { double m[3]; } masses_t;
static masses_t MS = {{1.0, 3.0e-6, 0.0}};

static void ref3_deriv(double t, const double *y, double *dy) {
    /* y = [star(2), planet(2), ship(2)] x [pos, vel] */
    const double *p[3] = { y, y+4, y+8 };
    double a[3][2] = {{0,0},{0,0},{0,0}};
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (i == j || MS.m[j] == 0.0) continue;
            double dx = p[j][0]-p[i][0], dy_ = p[j][1]-p[i][1];
            double r = sqrt(dx*dx+dy_*dy_);
            double f = G*MS.m[j]/(r*r*r);
            a[i][0] += f*dx; a[i][1] += f*dy_;
        }
    }
    for (int i = 0; i < 3; i++) {
        dy[4*i+0] = y[4*i+2]; dy[4*i+1] = y[4*i+3];
        dy[4*i+2] = a[i][0];  dy[4*i+3] = a[i][1];
    }
}

static double ship_planet_dist(double t, const double *y) {
    double dx = y[8]-y[4], dy = y[9]-y[5];
    return sqrt(dx*dx+dy*dy) - SOI;
}

/* ---------- Kepler (universal variables) ---------- */
static double stumpc(double z) {
    if (z > 1e-8) { double s = sqrt(z); return (1-cos(s))/z; }
    if (z < -1e-8) { double s = sqrt(-z); return (cosh(s)-1)/(-z); }
    return 0.5 - z/24.0 + z*z/720.0;
}
static double stumps(double z) {
    if (z > 1e-8) { double s = sqrt(z); return (s-sin(s))/(s*s*s); }
    if (z < -1e-8) { double s = sqrt(-z); return (sinh(s)-s)/(s*s*s); }
    return 1.0/6.0 - z/120.0 + z*z/5040.0;
}
static void kepler_prop(double mu, const double s0[4], double dt, double s[4]) {
    double x = s0[0], y = s0[1], vx = s0[2], vy = s0[3];
    double r0 = hypot(x, y), v2 = vx*vx+vy*vy, rv = x*vx+y*vy;
    double alpha = 2.0/r0 - v2/mu, sq = sqrt(mu);
    double chi = (alpha > 1e-12) ? sq*dt*alpha : sq*dt/r0;
    if (dt < 0) chi = -fabs(chi);
    for (int it = 0; it < 200; it++) {
        double z = alpha*chi*chi, C = stumpc(z), S = stumps(z);
        double F = (r0*rv/sq)*chi*chi*C + (1.0-alpha*r0)*chi*chi*chi*S + r0*chi - sq*dt;
        double dF = (r0*rv/sq)*chi*(1.0-z*S) + (1.0-alpha*r0)*chi*chi*C + r0;
        double d = F/dF;
        chi -= d;
        if (fabs(d) < 1e-14*fabs(chi)+1e-16) break;
    }
    double z = alpha*chi*chi, C = stumpc(z), S = stumps(z);
    double f = 1.0 - chi*chi*C/r0, g = dt - chi*chi*chi*S/sq;
    double xn = f*x+g*vx, yn = f*y+g*vy;
    double rn = hypot(xn, yn);
    double fd = sq/(rn*r0)*(z*chi*S - chi), gd = 1.0 - chi*chi*C/rn;
    s[0] = xn; s[1] = yn; s[2] = fd*x+gd*vx; s[3] = fd*y+gd*vy;
}

/* ---------- exact Schwarzschild geodesic leg (super-Hamiltonian, tau flow) ---------- */
typedef struct { double m; } geo_t;
static geo_t GEO;

static void geo_deriv(double tau, const double *y, double *dy) {
    /* y = [t_geo, x, y, pt, px, py]; g^{ij} = delta_ij + (A-1) x_i x_j / r^2;
       H = 0.5 (-pt^2/A + p^2 + (A-1) (p.x)^2/r^2), static so pt conserved. */
    double X = y[1], Y = y[2], pt = y[3], px = y[4], py = y[5];
    double r2 = X*X+Y*Y, r = sqrt(r2), m = GEO.m;
    double A = 1.0 - 2.0*m/r, B = A - 1.0;
    double w = px*X + py*Y, p2 = px*px + py*py, W = w*w/r2;
    double dAdx = 2.0*m*X/(r2*r), dAdy = 2.0*m*Y/(r2*r);
    double dWdx = 2.0*w*px/r2 - 2.0*w*w*X/(r2*r2);
    double dWdy = 2.0*w*py/r2 - 2.0*w*w*Y/(r2*r2);
    dy[0] = -pt/A;
    dy[1] = px + 2.0*B*w*X/r2;
    dy[2] = py + 2.0*B*w*Y/r2;
    dy[3] = 0.0;
    dy[4] = -0.5*(pt*pt*dAdx/(A*A) + dAdx*W + B*dWdx);
    dy[5] = -0.5*(pt*pt*dAdy/(A*A) + dAdy*W + B*dWdy);
}

static void geo_init(const double pos[2], const double vel_in[2], double *y) {
    /* internal geometric units: length AU, time AU/c (so c=1 inside the metric) */
    double vx = vel_in[0]/C_AUYR, vy = vel_in[1]/C_AUYR;
    double X = pos[0], Y = pos[1];
    double r2 = X*X+Y*Y, r = sqrt(r2), m = GEO.m;
    double A = 1.0 - 2.0*m/r;
    double rv = X*vx + Y*vy;
    double Q = vx*vx + vy*vy + (1.0/A - 1.0)*rv*rv/r2;   /* g_ij v^i v^j */
    double ut = sqrt(1.0/(A - Q));
    y[0] = 0.0; y[1] = X; y[2] = Y;
    y[3] = -A*ut;
    y[4] = (vx + (1.0/A - 1.0)*rv*X/r2)*ut;
    y[5] = (vy + (1.0/A - 1.0)*rv*Y/r2)*ut;
}

static void geo_readout(const double *y, double pos[2], double vel[2]) {
    pos[0] = y[1]; pos[1] = y[2];
    double X = y[1], Y = y[2], pt = y[3], px = y[4], py = y[5];
    double r2 = X*X+Y*Y, r = sqrt(r2), m = GEO.m;
    double A = 1.0 - 2.0*m/r, D = 1.0/A - A;
    double w = px*X + py*Y;
    double vxd = A*px + 2.0*D*w*X/r2;   /* dx/dtau */
    double vyd = A*py + 2.0*D*w*Y/r2;
    double tdot = -pt/A;                /* d(t_geo)/dtau; t_geo in AU/c */
    vel[0] = vxd/tdot*C_AUYR; vel[1] = vyd/tdot*C_AUYR;
}


/* star-doll geodesic propagation from heliocentric state s at time t0, to exact time
   t_target (clamped steps, no overshoot). Output heliocentric state. */
static void geo_star_to(const double s[4], double t0, double t_target, double out[4]) {
    GEO.m = G*MSTAR/(C_AUYR*C_AUYR);
    double y[6];
    geo_init(s, s+2, y);
    y[0] = t0*C_AUYR;
    double hh = 1e-6;
    while (y[0]/C_AUYR < t_target - 1e-15) {
        double rem = (t_target - y[0]/C_AUYR)*C_AUYR;
        if (hh > rem) hh = rem;
        double used = step_adaptive(0.0, y, &hh, 6, geo_deriv, 1e-12);
        if (used <= 0.0) break;
    }
    double pos[2], vel[2];
    geo_readout(y, pos, vel);
    out[0] = pos[0]; out[1] = pos[1]; out[2] = vel[0]; out[3] = vel[1];
}

/* doll leg propagators with SOI-crossing events, config law */
static int CFG_KEPLER = 1;

static double helio_event(double tgeo, const double *y) { /* geodesic state; t_geo = c*t */
    double pp[2], pv[2];
    double t = tgeo/C_AUYR;
    (void)t; planet_eph(t, pp, pv);
    double dx = y[1]-pp[0], dy = y[2]-pp[1];
    return sqrt(dx*dx+dy*dy) - SOI;
}
static double frame_event(double tau, const double *y) {
    double dx = y[1], dy = y[2];
    return sqrt(dx*dx+dy*dy) - SOI;
}

/* propagate a heliocentric state under the star-doll until next SOI entry.
   Returns t_cross; outputs heliocentric ship state. */
static double star_leg(double t0, const double s0[4], double tol, double s_out[4]) {
    double pp[2], pv[2], s[4];
    if (CFG_KEPLER) {
        double dt = 2e-5, t = t0, lo = t0, hi = t0;
        planet_eph(t0, pp, pv);
        { double dx = s0[0]-pp[0], dy = s0[1]-pp[1];
          double g = sqrt(dx*dx+dy*dy)-SOI; (void)g; }
        for (int k = 0; k < 400000; k++) {
            t += dt;
            kepler_prop(G*MSTAR, s0, t - t0, s);
            planet_eph(t, pp, pv);
            double dx = s[0]-pp[0], dy = s[1]-pp[1];
            if (sqrt(dx*dx+dy*dy) <= SOI) { hi = t; break; }
            lo = t;
            if (t - t0 > 3.0) break;
        }
        if (hi <= lo) { memcpy(s_out, s0, sizeof(double)*4); return t; }
        for (int it = 0; it < 80; it++) {
            double mid = 0.5*(lo+hi);
            kepler_prop(G*MSTAR, s0, mid - t0, s);
            planet_eph(mid, pp, pv);
            double dx = s[0]-pp[0], dy = s[1]-pp[1];
            if (sqrt(dx*dx+dy*dy) <= SOI) hi = mid; else lo = mid;
        }
        kepler_prop(G*MSTAR, s0, hi - t0, s_out);
        return hi;
    }
    GEO.m = G*MSTAR/(C_AUYR*C_AUYR);
    double y[6];
    geo_init(s0, s0+2, y);
    y[0] = t0*C_AUYR;
    double h = 1e-6;
    double gprev = helio_event(y[0], y);
    if (gprev < 0) gprev = 1e-30;
    while (y[0]/C_AUYR < t0 + 3.0) {
        double yprev[6], tauprev = 0.0;
        memcpy(yprev, y, sizeof(double)*6);
        double used = step_adaptive(tauprev, y, &h, 6, geo_deriv, tol);
        if (used < 1e-18) break;
        double gnow = helio_event(y[0], y);
        if (gnow <= 0.0) {
            /* bisect on tau between tauprev(=0 each iter is wrong for later steps) */
            /* recompute proper bracket: integrate from yprev for fraction of used */
            double lotau = 0.0, hitau = used;
            for (int it = 0; it < 80; it++) {
                double mid = 0.5*(lotau+hitau), ym[6];
                rk4(0.0, yprev, mid, 6, geo_deriv, ym);
                if (helio_event(ym[0], ym) <= 0.0) hitau = mid; else lotau = mid;
            }
            double ym[6];
            rk4(0.0, yprev, hitau, 6, geo_deriv, ym);
            memcpy(y, ym, sizeof(double)*6);
            break;
        }
        gprev = gnow;
    }
    double pos[2], vel[2];
    geo_readout(y, pos, vel);
    s_out[0] = pos[0]; s_out[1] = pos[1]; s_out[2] = vel[0]; s_out[3] = vel[1];
    return y[0]/C_AUYR;
}

static void twobody_deriv(double t, const double *y, double *dy) {
    double r = hypot(y[0], y[1]);
    double f = -MU_P/(r*r*r);
    dy[0] = y[2]; dy[1] = y[3];
    dy[2] = f*y[0]; dy[3] = f*y[1];
}

static double xi_dist_event(double t, const double *y) {
    return hypot(y[0], y[1]) - SOI;
}

/* propagate a planet-frame state under the planet-doll until |xi|=SOI outward */
static double planet_leg(double t0, const double xi0[4], double tol, double xi_out[4]) {
    if (CFG_KEPLER) {
        double y[4] = {xi0[0], xi0[1], xi0[2], xi0[3]};
        double h = 1e-7, t = 0.0;
        while (t < 1.0) {
            double yprev[4], tprev = t;
            memcpy(yprev, y, sizeof(double)*4);
            double used = step_adaptive(t, y, &h, 4, twobody_deriv, tol);
            t += used;
            if (xi_dist_event(t, y) >= 0.0) {
                double lo = tprev, hi = t;
                for (int it = 0; it < 80; it++) {
                    double mid = 0.5*(lo+hi), ym[4];
                    rk4(tprev, yprev, mid-tprev, 4, twobody_deriv, ym);
                    if (xi_dist_event(mid, ym) >= 0.0) hi = mid; else lo = mid;
                }
                rk4(tprev, yprev, hi-tprev, 4, twobody_deriv, y);
                memcpy(xi_out, y, sizeof(double)*4);
                return t0 + hi;
            }
        }
        memcpy(xi_out, y, sizeof(double)*4);
        return t0 + t;
    } else {
        GEO.m = G*MPL/(C_AUYR*C_AUYR);
        double y[6];
        geo_init(xi0, xi0+2, y);
        y[0] = 0.0;
        double h = 1e-7;
        while (y[0]/C_AUYR < 1.0) {
            double yprev[6];
            memcpy(yprev, y, sizeof(double)*6);
            double used = step_adaptive(0.0, y, &h, 6, geo_deriv, tol);
            if (used < 1e-18) break;
            if (frame_event(0.0, y) > 0.0) {
                double lotau = 0.0, hitau = used;
                for (int it = 0; it < 80; it++) {
                    double mid = 0.5*(lotau+hitau), ym[6];
                    rk4(0.0, yprev, mid, 6, geo_deriv, ym);
                    if (frame_event(0.0, ym) > 0.0) hitau = mid; else lotau = mid;
                }
                double ym[6];
                rk4(0.0, yprev, hitau, 6, geo_deriv, ym);
                memcpy(y, ym, sizeof(double)*6);
                break;
            }
        }
        double pos[2], vel[2];
        geo_readout(y, pos, vel);
        xi_out[0] = pos[0]; xi_out[1] = pos[1]; xi_out[2] = vel[0]; xi_out[3] = vel[1];
        return t0 + y[0]/C_AUYR;
    }
}

static double e_helio(const double pos[2], const double vel[2]) {
    return 0.5*(vel[0]*vel[0]+vel[1]*vel[1]) - G*MSTAR/hypot(pos[0], pos[1]);
}

/* full 3-body reference from ship heliocentric state, printing crossings */
static void run_ref3(double t_end, double tol) {
    double y[12] = {0};
    double xs, ys, vxs, vys;
    if (scanf("%lf %lf %lf %lf", &xs, &ys, &vxs, &vys) != 4) { fprintf(stderr, "bad stdin\n"); exit(1); }
    /* star at origin at rest, planet circular, ship given */
    y[4] = AP; y[5] = 0.0; y[6] = 0.0; y[7] = AP*WP;
    y[8] = xs; y[9] = ys; y[10] = vxs; y[11] = vys;
    double t = 0.0, h = 1e-5;
    int nc = 0;
    double gprev = ship_planet_dist(0.0, y);
    double e0 = e_helio(y+8, y+10);
    while (t < t_end) {
        double yprev[12], tprev = t;
        memcpy(yprev, y, sizeof(double)*12);
        double used = step_adaptive(t, y, &h, 12, ref3_deriv, tol);
        t += used;
        double gnow = ship_planet_dist(t, y);
        if (gnow*gprev < 0.0) {
            double lo = tprev, hi = t;
            for (int it = 0; it < 80; it++) {
                double mid = 0.5*(lo+hi), ym[12];
                rk4(tprev, yprev, mid-tprev, 12, ref3_deriv, ym);
                if (ship_planet_dist(mid, ym)*gprev < 0.0) hi = mid; else lo = mid;
            }
            double ym[12];
            rk4(tprev, yprev, hi-tprev, 12, ref3_deriv, ym);
            memcpy(y, ym, sizeof(double)*12);
            t = hi;
            nc++;
            int dir = gprev < 0.0 ? 1 : -1; /* entering SOI */
            printf("CROSS %d %.15f %d %.15f %.15f %.15f %.15f %.15f %.15f %.15f %.15f\n",
                   nc, t, dir, y[8], y[9], y[10], y[11], y[4], y[5], y[6], y[7]);
            fflush(stdout);
            gprev = ship_planet_dist(t, y);
            /* continue from refined state */
            h = 1e-6;
        } else gprev = gnow;
    }
    printf("DONE %d %.12f Eerr %.3e %.15f %.15f %.15f %.15f %.15f %.15f %.15f %.15f\n", nc, t, fabs(e_helio(y+8, y+10)-e0), y[8], y[9], y[10], y[11], y[4], y[5], y[6], y[7]);
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "mode?\n"); return 1; }
    if (!strcmp(argv[1], "ref3")) {
        double t_end = atof(argv[2]);
        double tol = argc > 3 ? atof(argv[3]) : 1e-9;
        run_ref3(t_end, tol);
        return 0;
    }
    if (!strcmp(argv[1], "ref3state")) {
        /* stdin: t xs ys vxs vys (ship helio) + argv[2]=t_end: propagate 3-body to
           exactly t_end (no event stops) and print final states */
        double t0, xs, ys, vxs, vys, t_end = atof(argv[2]);
        if (scanf("%lf %lf %lf %lf %lf", &t0, &xs, &ys, &vxs, &vys) != 5) return 1;
        double y[12] = {0};
        y[4] = AP; y[6] = 0.0; y[7] = AP*WP;
        y[8] = xs; y[9] = ys; y[10] = vxs; y[11] = vys;
        double e0s[4] = {xs, ys, vxs, vys};
        double t = t0, h = 1e-6;
        /* rotate planet to t0 phase */
        {
            double pp[2], pv[2];
            planet_eph(t0, pp, pv);
            y[4] = pp[0]; y[5] = pp[1]; y[6] = pv[0]; y[7] = pv[1];
        }
        while (t < t_end - 1e-14) {
            if (t + h > t_end) h = t_end - t;
            double used = step_adaptive(t, y, &h, 12, ref3_deriv, 1e-9);
            t += used;
        }
        printf("R3S %.15f %.15f %.15f %.15f %.15f %.15f %.15f %.15f %.15f\n",
               t, y[8], y[9], y[10], y[11], y[4], y[5], y[6], y[7]);
        (void)e0s;
        return 0;
    }
    if (!strcmp(argv[1], "dollseg")) {
        CFG_KEPLER = !strcmp(argv[2], "kepler");
        const char *kind = argv[3];
        double t, xs, ys, vxs, vys;
        if (scanf("%lf %lf %lf %lf %lf", &t, &xs, &ys, &vxs, &vys) != 5) return 1;
        double s_out[4], tc;
        if (!strcmp(kind, "star")) {
            double s0[4] = {xs, ys, vxs, vys};
            tc = star_leg(t, s0, 1e-12, s_out);
        } else {
            double pp[2], pv[2];
            planet_eph(t, pp, pv);
            double xi0[4] = {xs-pp[0], ys-pp[1], vxs-pv[0], vys-pv[1]};
            double xio[4];
            tc = planet_leg(t, xi0, 1e-12, xio);
            planet_eph(tc, pp, pv);
            s_out[0] = pp[0]+xio[0]; s_out[1] = pp[1]+xio[1];
            s_out[2] = pv[0]+xio[2]; s_out[3] = pv[1]+xio[3];
            printf("SEG %.15f %.15f %.15f %.15f %.15f %.15f %.15f %.15f %.15f\n",
                   tc, s_out[0], s_out[1], s_out[2], s_out[3],
                   xio[0], xio[1], xio[2], xio[3]);
            return 0;
        }
        printf("SEG %.15f %.15f %.15f %.15f %.15f %.15f %.15f %.15f %.15f\n",
               tc, s_out[0], s_out[1], s_out[2], s_out[3],
               s_out[0], s_out[1], s_out[2], s_out[3]);
        return 0;
    }
    if (!strcmp(argv[1], "flyby")) {
        CFG_KEPLER = !strcmp(argv[2], "kepler");
        double u = 6.0/(1.495978707e8/3.15576e7);
        double b, D = 2.0*SOI;
        while (scanf("%lf", &b) == 1) {
            double rp = b*RP_AU;
            double bi = rp*sqrt(1.0 + 2.0*MU_P/(rp*u*u));
            /* planet-frame initial state at |xi|=D, incoming along +x */
            double xi0[4] = {-D, bi, u, 0.0};
            double pp[2], pv[2];
            planet_eph(0.0, pp, pv);
            double s0[4] = {pp[0]-D, pp[1]+bi, pv[0]+u, pv[1]};
            /* doll: star leg to SOI entry, planet leg to exit, star leg to |xi|=D again */
            double s1[4], xio[4], s2[4];
            double t1 = star_leg(0.0, s0, 1e-12, s1);
            planet_eph(t1, pp, pv);
            double xi1[4] = {s1[0]-pp[0], s1[1]-pp[1], s1[2]-pv[0], s1[3]-pv[1]};
            double t2 = planet_leg(t1, xi1, 1e-12, xio);
            planet_eph(t2, pp, pv);
            double s2h[4] = {pp[0]+xio[0], pp[1]+xio[1], pv[0]+xio[2], pv[1]+xio[3]};
            /* star leg until |xi| = D again: propagate until ship-planet dist = D */
            double lo = t2, hi = t2, s[4], dt = 1e-4;
            memcpy(s, s2h, sizeof(double)*4);
            while (1) {
                hi = lo + dt;
                double sm[4];
                if (CFG_KEPLER) kepler_prop(G*MSTAR, s2h, hi-t2, sm);
                else geo_star_to(s2h, t2, hi, sm);
                planet_eph(hi, pp, pv);
                double dx = sm[0]-pp[0], dy = sm[1]-pp[1];
                if (sqrt(dx*dx+dy*dy) >= D) { memcpy(s, sm, sizeof(double)*4); break; }
                lo = hi; dt *= 1.3;
                if (hi - t2 > 2.0) break;
            }
            /* refine to D-sphere crossing */
            double lo2 = lo, hi2 = hi;
            for (int it = 0; it < 80; it++) {
                double mid = 0.5*(lo2+hi2), sm[4];
                if (CFG_KEPLER) kepler_prop(G*MSTAR, s2h, mid-t2, sm);
                else {
                    geo_star_to(s2h, t2, mid, sm);
                }
                planet_eph(mid, pp, pv);
                double dx = sm[0]-pp[0], dy = sm[1]-pp[1];
                if (sqrt(dx*dx+dy*dy) >= D) hi2 = mid; else lo2 = mid;
            }
            double sm[4];
            if (CFG_KEPLER) kepler_prop(G*MSTAR, s2h, hi2-t2, sm);
            else geo_star_to(s2h, t2, hi2, sm);
            double dvdx = sm[2]-s0[2], dvdy = sm[3]-s0[3];
            /* reference to the same t_end */
            double y[12] = {0};
            y[4] = AP; y[6] = 0.0; y[7] = AP*WP;
            y[8] = s0[0]; y[9] = s0[1]; y[10] = s0[2]; y[11] = s0[3];
            double hh = 1e-5, tc3 = 0.0;
            while (tc3 < hi2 - 1e-15) {
                if (hh > hi2 - tc3) hh = hi2 - tc3;
                double used3 = step_adaptive(tc3, y, &hh, 12, ref3_deriv, 1e-9);
                if (used3 <= 0.0) break;
                tc3 += used3;
            }
            double dvrx = y[10]-s0[2], dvry = y[11]-s0[3];
            printf("FLY %.6f %.9f %.12e %.12e %.12e %.12e %.12f\n",
                   b, hi2, dvdx, dvdy, dvrx, dvry, rp);
            fflush(stdout);
        }
        return 0;
    }
    if (!strcmp(argv[1], "geotest")) {
        double xs, ys, vxs, vys, dur;
        scanf("%lf %lf %lf %lf %lf", &xs, &ys, &vxs, &vys, &dur);
        GEO.m = G*MSTAR/(C_AUYR*C_AUYR);
        double y[6];
        geo_init((double[2]){xs, ys}, (double[2]){vxs, vys}, y);
        y[0] = 0.0;
        double H0 = 0.0;
        {
            double X = y[1], Y = y[2], pt = y[3], px = y[4], py = y[5];
            double r2 = X*X+Y*Y, r = sqrt(r2), A = 1.0-2.0*GEO.m/r;
            double w = px*X+py*Y;
            H0 = 0.5*(-pt*pt/A + (px*px+py*py) + (A-1.0)*w*w/r2);
        }
        double h = 1e-6;
        while (y[0]/C_AUYR < dur) step_adaptive(0.0, y, &h, 6, geo_deriv, 1e-12);
        double pos[2], vel[2];
        geo_readout(y, pos, vel);
        double X = y[1], Y = y[2], pt = y[3], px = y[4], py = y[5];
        double r2 = X*X+Y*Y, r = sqrt(r2), A = 1.0-2.0*GEO.m/r, D = 1.0/A-A;
        double w = px*X+py*Y;
        double H1 = 0.5*(-pt*pt/A + (px*px+py*py) + (A-1.0)*w*w/r2);
        printf("GEOTEST t=%.6f pos=(%.9f,%.9f) r=%.9f vel=(%.9f,%.9f) Hdrift=%.3e\n",
               y[0]/C_AUYR, pos[0], pos[1], hypot(pos[0], pos[1]), vel[0], vel[1], H1-H0);
        return 0;
    }
    fprintf(stderr, "unknown mode\n");
    return 1;
}
