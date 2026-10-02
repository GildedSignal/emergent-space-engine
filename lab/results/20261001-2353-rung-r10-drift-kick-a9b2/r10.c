// Rung r10: the compiled drift plus kicks, with a smooth changeover.
// Configurations: symba (exact Kepler drift about the dominant body, planet kicks at a fixed step
// in the drift's phase, DLL98-style smooth changeover in the separation with recursive sub-steps),
// wh-fixed (Wisdom-Holman, fixed step, no changeover), soi-switch (events3: a hard, state-selected
// switch of the drift's dominant body at the sphere of influence), truth (the judge's own
// reference: adaptive Dormand-Prince 5(4) with steps clipped to the asked times, ported from
// xtask/src/behave/restricted.rs). Units G = M_star + M_planet = 1.
// Build: gcc -O2 -o r10 r10.c -lm
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const double TAU = 6.283185307179586;
static const double PI = 3.141592653589793;

// ---------------------------------------------------------------- SplitMix64 (sample.rs)
typedef struct { uint64_t s; } Rng;
static uint64_t rng_next(Rng *r) {
    r->s += 0x9E3779B97F4A7C15ULL;
    uint64_t z = r->s;
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}
static double rng_unit(Rng *r) { return (double)(rng_next(r) >> 11) / 9007199254740992.0; }

#define HANDOFF_SEED 20261002ULL
#define HILL_SEED 20261004ULL
#define ECCENTRIC_SEED 20261007ULL
static const int HANDOFF_KEPT[16] = {1, 2, 12, 14, 15, 19, 22, 23, 25, 30, 31, 32, 35, 39, 45, 46};
static const int PIC_SHIPS[3] = {0, 5, 10};   // frozen choice for the picture

typedef struct { double side, k, alpha; } Handoff;
static void handoffs(int n, Handoff *out) {
    Rng r = { HANDOFF_SEED };
    for (int i = 0; i < n; i++) {
        double side = (rng_next(&r) >> 63) == 1 ? 1.0 : -1.0;
        out[i] = (Handoff){ side, 1.5 + 1.5 * rng_unit(&r), (30.0 + 300.0 * rng_unit(&r)) * (PI / 180.0) };
    }
}

// ---------------------------------------------------------------- Scene (restricted.rs)
typedef struct { double hi, lo; } dd;
typedef struct { double mu, sep, planet_radius; dd omega_dd; } Scene;
static Scene JUPITER;

static void two_sum(double a, double b, double *hi, double *lo) {
    double s = a + b, v = s - a;
    *hi = s; *lo = (a - (s - v)) + (b - v);
}
static void two_prod(double a, double b, double *hi, double *lo) {
    double p = a * b; *hi = p; *lo = fma(a, b, -p);
}
static dd dd_mul(dd a, dd b) {
    double p, e, s, r, h2, l2;
    two_prod(a.hi, b.hi, &p, &e);
    two_sum(p, e + (a.hi * b.lo + a.lo * b.hi), &s, &r);
    two_sum(s, r, &h2, &l2);
    return (dd){ h2, l2 };
}
static dd omega_dd_of(double sep) {
    double root = sqrt(sep), sq, sqe, h, l, h2, l2;
    two_prod(root, root, &sq, &sqe);
    two_sum(root, ((sep - sq) - sqe) / (2.0 * root), &h, &l);
    dd cube = dd_mul((dd){ sep, 0.0 }, (dd){ h, l });
    double q = 1.0 / cube.hi;
    dd back = dd_mul(cube, (dd){ q, 0.0 });
    two_sum(1.0, -back.hi, &h, &l);
    two_sum(q, q * (h + l - back.lo), &h2, &l2);
    return (dd){ h2, l2 };
}
static double phase_of(dd omega, double t) {
    dd p = dd_mul(omega, (dd){ t, 0.0 });
    double n = round(p.hi / TAU), nh, nl, d, e;
    two_prod(n, TAU, &nh, &nl);
    two_sum(p.hi, -nh, &d, &e);
    return d + (e - nl - n * 2.4492935982947064e-16 + p.lo);
}
static void scene_init(Scene *s, double mu, double sep, double planet_radius) {
    s->mu = mu; s->sep = sep; s->planet_radius = planet_radius;
    s->omega_dd = omega_dd_of(sep);
}
static double sc_omega(Scene *s) { return pow(s->sep, -1.5); }
static double sc_phase(Scene *s, double t) { return phase_of(s->omega_dd, t); }
static double sc_period(Scene *s) { return TAU * pow(s->sep, 1.5); }
static double sc_hill(Scene *s) { return s->sep * cbrt(s->mu / 3.0); }
static double sc_soi(Scene *s) { return s->sep * pow(s->mu, 0.4); }
static void sc_planet(Scene *s, double t, double p[2], double v[2]) {
    double th = sc_phase(s, t), sn = sin(th), cs = cos(th);
    double r = s->sep * (1.0 - s->mu), vv = s->sep * (1.0 - s->mu) * sc_omega(s);
    p[0] = r * cs; p[1] = r * sn; v[0] = -vv * sn; v[1] = vv * cs;
}
static void sc_star(Scene *s, double t, double p[2], double v[2]) {
    double th = sc_phase(s, t), sn = sin(th), cs = cos(th);
    double r = s->sep * s->mu, vv = s->sep * s->mu * sc_omega(s);
    p[0] = -r * cs; p[1] = -r * sn; v[0] = vv * sn; v[1] = -vv * cs;
}
static double sc_planet_distance(Scene *s, double t, const double ship[4]) {
    double p[2], v[2]; sc_planet(s, t, p, v);
    return hypot(ship[0] - p[0], ship[1] - p[1]);
}
static double sc_jacobi(Scene *s, double t, const double ship[4]) {
    double sp[2], sv[2]; sc_star(s, t, sp, sv);
    return 2.0 * (1.0 - s->mu) / hypot(ship[0] - sp[0], ship[1] - sp[1])
         + 2.0 * s->mu / sc_planet_distance(s, t, ship)
         + 2.0 * sc_omega(s) * (ship[0] * ship[3] - ship[1] * ship[2])
         - (ship[2] * ship[2] + ship[3] * ship[3]);
}
static void sc_barycentric(Scene *s, double t, const double rel[4], double out[4]) {
    double p[2], v[2]; sc_planet(s, t, p, v);
    out[0] = rel[0] + p[0]; out[1] = rel[1] + p[1]; out[2] = rel[2] + v[0]; out[3] = rel[3] + v[1];
}
static void sc_relative(Scene *s, double t, const double ship[4], double out[4]) {
    double p[2], v[2]; sc_planet(s, t, p, v);
    out[0] = ship[0] - p[0]; out[1] = ship[1] - p[1]; out[2] = ship[2] - v[0]; out[3] = ship[3] - v[1];
}
static double norm2(double a, double b) { return sqrt(a * a + b * b); }

// ---------------------------------------------------------------- Reference (DP 5(4), restricted.rs)
typedef struct {
    Scene *scene; double rtol, t, h; double rel[4], k1[4]; int has_k1, gave_up;
    uint64_t steps, evals;
} Ref;

static void ref_deriv(Ref *r, double t, const double w[4], double out[4]) {
    Scene *s = r->scene;
    r->evals++;
    double r2 = w[0] * w[0] + w[1] * w[1];
    double pull = r2 < s->planet_radius * s->planet_radius
        ? s->mu / (s->planet_radius * s->planet_radius * s->planet_radius)
        : s->mu / (r2 * sqrt(r2));
    double ax = -pull * w[0], ay = -pull * w[1];
    double th = sc_phase(s, t), sn = sin(th), cs = cos(th);
    double dx = s->sep * cs, dy = s->sep * sn;
    double q = (w[0] * (2.0 * dx + w[0]) + w[1] * (2.0 * dy + w[1])) / (s->sep * s->sep);
    double u = 1.0 + q, u32 = u * sqrt(u);
    double f = q * (3.0 + q * (3.0 + q)) / (1.0 + u32);
    double k = (1.0 - s->mu) / (s->sep * s->sep * s->sep * u32);
    ax -= k * (w[0] - f * dx); ay -= k * (w[1] - f * dy);
    out[0] = w[2]; out[1] = w[3]; out[2] = ax; out[3] = ay;
}
static void ref_lin(const double y[4], const double *const ks[], const double *as, int n, double h, double out[4]) {
    for (int i = 0; i < 4; i++) {
        double sum = 0.0;
        for (int j = 0; j < n; j++) sum += as[j] * ks[j][i];
        out[i] = y[i] + h * sum;
    }
}
static void ref_rk(Ref *r, double t, const double y[4], const double k1[4], double h,
                   double y5[4], double err[4], double k7[4]) {
    double tmp[4], k2[4], k3[4], k4[4], k5[4], k6[4];
    ref_lin(y, &k1, (double[]){ 1.0 / 5.0 }, 1, h, tmp); ref_deriv(r, t + h / 5.0, tmp, k2);
    { const double *ks[2] = { k1, k2 }; double a[2] = { 3.0 / 40.0, 9.0 / 40.0 };
      ref_lin(y, ks, a, 2, h, tmp); ref_deriv(r, t + 3.0 * h / 10.0, tmp, k3); }
    { const double *ks[3] = { k1, k2, k3 }; double a[3] = { 44.0 / 45.0, -56.0 / 15.0, 32.0 / 9.0 };
      ref_lin(y, ks, a, 3, h, tmp); ref_deriv(r, t + 4.0 * h / 5.0, tmp, k4); }
    { const double *ks[4] = { k1, k2, k3, k4 };
      double a[4] = { 19372.0 / 6561.0, -25360.0 / 2187.0, 64448.0 / 6561.0, -212.0 / 729.0 };
      ref_lin(y, ks, a, 4, h, tmp); ref_deriv(r, t + 8.0 * h / 9.0, tmp, k5); }
    { const double *ks[5] = { k1, k2, k3, k4, k5 };
      double a[5] = { 9017.0 / 3168.0, -355.0 / 33.0, 46732.0 / 5247.0, 49.0 / 176.0, -5103.0 / 18656.0 };
      ref_lin(y, ks, a, 5, h, tmp); ref_deriv(r, t + h, tmp, k6); }
    { const double *ks[5] = { k1, k3, k4, k5, k6 };
      double a[5] = { 35.0 / 384.0, 500.0 / 1113.0, 125.0 / 192.0, -2187.0 / 6784.0, 11.0 / 84.0 };
      ref_lin(y, ks, a, 5, h, y5); }
    ref_deriv(r, t + h, y5, k7);
    for (int i = 0; i < 4; i++)
        err[i] = h * (71.0 / 57600.0 * k1[i] - 71.0 / 16695.0 * k3[i] + 71.0 / 1920.0 * k4[i]
                    - 17253.0 / 339200.0 * k5[i] + 22.0 / 525.0 * k6[i] - 1.0 / 40.0 * k7[i]);
}
static double ref_scaled_error(Ref *r, const double y[4], const double y5[4], const double err[4]) {
    double sp = r->rtol * fmax(norm2(y[0], y[1]), norm2(y5[0], y5[1]));
    double sv = r->rtol * fmax(norm2(y[2], y[3]), norm2(y5[2], y5[3]));
    return fmax(fmax(fabs(err[0]), fabs(err[1])) / sp, fmax(fabs(err[2]), fabs(err[3])) / sv);
}
static int ref_step(Ref *r, double limit) {
    double k1[4];
    if (r->has_k1) memcpy(k1, r->k1, sizeof k1); else ref_deriv(r, r->t, r->rel, k1);
    for (;;) {
        if (r->steps > 40000000ULL || !(r->h > 1e-15 * fmax(fabs(r->t), 1.0))) { r->gave_up = 1; return 0; }
        double left = limit - r->t;
        int clipped = r->h >= left;
        double hs = clipped ? left : r->h;
        double y5[4], err[4], k7[4];
        ref_rk(r, r->t, r->rel, k1, hs, y5, err, k7);
        double e = ref_scaled_error(r, r->rel, y5, err);
        double fac = e > 0.0 ? fmin(5.0, fmax(0.2, 0.9 * pow(e, -0.2))) : 5.0;
        if (e <= 1.0) {
            r->steps++;
            r->t = clipped ? limit : r->t + hs;
            memcpy(r->rel, y5, sizeof y5);
            memcpy(r->k1, k7, sizeof k7); r->has_k1 = 1;
            r->h = (clipped && fac > 1.0) ? fmax(r->h, hs * fac) : hs * fac;
            return 1;
        }
        r->h = hs * fac;
    }
}
static void ref_init(Ref *r, Scene *s, double rtol, const double ship[4]) {
    memset(r, 0, sizeof *r);
    r->scene = s; r->rtol = rtol;
    sc_relative(s, 0.0, ship, r->rel);
    r->h = 1e-3 * norm2(r->rel[0], r->rel[1]) / fmax(norm2(r->rel[2], r->rel[3]), 2.2250738585072014e-308);
}
static int ref_advance(Ref *r, double to, double out[4]) {
    while (r->t < to) if (!ref_step(r, to)) return 0;
    sc_barycentric(r->scene, r->t, r->rel, out);
    return 1;
}

// ---------------------------------------------------------------- Universal Kepler drift
static void stumpff(double z, double *C, double *S) {
    if (z > 0.1) { double sq = sqrt(z); *C = (1.0 - cos(sq)) / z; *S = (sq - sin(sq)) / (sq * z); }
    else if (z < -0.1) { double sq = sqrt(-z); *C = (cosh(sq) - 1) / (-z); *S = (sinh(sq) - sq) / ((-z) * sq); }
    else { double z2 = z * z, z3 = z2 * z;
        *C = 0.5 - z / 24.0 + z2 / 720.0 - z3 / 40320.0;
        *S = 1.0 / 6.0 - z / 120.0 + z2 / 5040.0 - z3 / 362880.0; }
}
static double kep_F(double c0, double c1, double r0, double sq, double dt, double alpha, double x) {
    double z = alpha * x * x, C, S;
    stumpff(z, &C, &S);
    return c0 * x * x * C + c1 * x * x * x * S + r0 * x - sq * dt;
}
static void kepler(double gm, double p[2], double v[2], double dt) {
    if (dt == 0.0) return;
    double r0 = norm2(p[0], p[1]), v2 = v[0] * v[0] + v[1] * v[1];
    if (!(r0 > 0.0) || !isfinite(v2)) return;
    double vr = (p[0] * v[0] + p[1] * v[1]) / r0;
    double alpha = 2.0 / r0 - v2 / gm;
    double sq = sqrt(gm);
    if (alpha > 0.0) {   // elliptic: the flow is periodic, reduce dt mod the period (exact)
        double T = TAU / (sq * alpha * sqrt(alpha));
        if (fabs(dt) > 0.5 * T) dt -= round(dt / T) * T;
    }
    double x;
    if (alpha > 0.0) x = sq * dt * alpha;
    else if (alpha < 0.0) x = (dt > 0 ? 1.0 : -1.0) / sqrt(-alpha) * log1p(2.0 * sq * pow(-alpha, 1.5) * fabs(dt));
    else x = sq * dt / r0;
    double c0 = r0 * vr / sq, c1 = 1.0 - alpha * r0, tol = 1e-10 * fmax(1.0, fabs(sq * dt));
    for (int it = 0; it < 60; it++) {
        double F = kep_F(c0, c1, r0, sq, dt, alpha, x);
        if (fabs(F) <= tol) break;
        double eps = 1e-7 * fmax(1.0, fabs(x));
        double dF = (kep_F(c0, c1, r0, sq, dt, alpha, x + eps) - F) / eps;
        if (!isfinite(dF) || dF == 0.0) break;
        double dx = -F / dF, cap = 2.0 * fabs(x) + 1.0;
        if (dx > cap) dx = cap;
        if (dx < -cap) dx = -cap;
        x += dx;
    }
    if (!(fabs(kep_F(c0, c1, r0, sq, dt, alpha, x)) <= 1e-6 * fmax(1.0, fabs(sq * dt)))) {
        // The residual is monotone in x: bracket by doubling, then bisect.
        double lo = fmin(0.0, x), hi = fmax(0.0, x);
        int ok = kep_F(c0, c1, r0, sq, dt, alpha, lo) <= 0 && kep_F(c0, c1, r0, sq, dt, alpha, hi) >= 0;
        for (int k = 0; k < 120 && !ok; k++) {
            if (lo == 0.0 && hi == 0.0) { lo = -1.0; hi = 1.0; }
            else { if (lo != 0.0) lo *= 2.0; if (hi != 0.0) hi *= 2.0; if (lo == 0.0) lo = -1.0; if (hi == 0.0) hi = 1.0; }
            if (!isfinite(lo) || !isfinite(hi)) break;
            ok = kep_F(c0, c1, r0, sq, dt, alpha, lo) <= 0 && kep_F(c0, c1, r0, sq, dt, alpha, hi) >= 0;
        }
        if (ok && isfinite(lo) && isfinite(hi)) {
            for (int k = 0; k < 200; k++) {
                double mid = 0.5 * (lo + hi);
                if (kep_F(c0, c1, r0, sq, dt, alpha, mid) <= 0) lo = mid; else hi = mid;
            }
            x = 0.5 * (lo + hi);
        }
    }
    double z = alpha * x * x, C, S;
    stumpff(z, &C, &S);
    double f = 1.0 - x * x / r0 * C, g = dt - x * x * x / sq * S;
    double rn0 = f * p[0] + g * v[0], rn1 = f * p[1] + g * v[1], rnew = norm2(rn0, rn1);
    double fdot = sq / (r0 * rnew) * x * (alpha * x * x * S - 1.0), gdot = 1.0 - x * x / rnew * C;
    double vn0 = fdot * p[0] + gdot * v[0], vn1 = fdot * p[1] + gdot * v[1];
    p[0] = rn0; p[1] = rn1; v[0] = vn0; v[1] = vn1;
}

// ---------------------------------------------------------------- Candidates
// Star-centric state (rho, v): relative to the star, axes inertial. With d the planet's position
// from the star and s = rho - d:
//   A = -(1-mu) rho/|rho|^3                     star, carried exactly by the star-Kepler drift
//   B = -mu s/|s|^3 - mu d/sep^3                planet direct + indirect, kicked (windowed)
//   C = -(1-mu)(s+d)/|s+d|^3 + (1-mu) d/sep^3   star direct + indirect, kicked in the planet frame
// A + B = (-mu s/|s|^3 + C) - d/sep^3, so the two decompositions describe the same motion, and the
// changeover windows the split between them: far, phi = 1 (B kicked, A drifted); near, phi = 0
// (C kicked, the planet's Kepler drifted); between, both, with the double-counted direct term
// removed by the -phi*B part of the near kick.
typedef struct { double rho[2], v[2], t; uint64_t evals; } Cand;
typedef enum { C_SYMBA, C_WH, C_SOI } Cfg;

// Design constants, fixed before any graded run.
static double CO_R0_HILL = 1.3;  // changeover outer edge, Hill radii (covers apoapsis 1.17 of the 0.9/e0.3 births)
static const double CO_RIN_DIV = 3.0;  // fully planet-dominated inside R0/3
static const int SUB_RES = 40;         // sub-divide while the local planet period < SUB_RES sub-steps
static const int LMAX = 9;             // deepest recursion: h/3^9

static void cand_planet_d(Scene *s, double t, double d[2], double dd_[2]) {
    double th = sc_phase(s, t), sn = sin(th), cs = cos(th), vv = s->sep * sc_omega(s);
    d[0] = s->sep * cs; d[1] = s->sep * sn;
    dd_[0] = -vv * sn; dd_[1] = vv * cs;
}
static double cand_sep(Scene *s, Cand *c) {
    double d[2], dd_[2]; cand_planet_d(s, c->t, d, dd_);
    return norm2(c->rho[0] - d[0], c->rho[1] - d[1]);
}
static void force_B(Scene *s, Cand *c, double w, double out[2]) {
    double d[2], dd_[2]; cand_planet_d(s, c->t, d, dd_);
    double sx = c->rho[0] - d[0], sy = c->rho[1] - d[1], r2 = sx * sx + sy * sy;
    double pull = r2 < s->planet_radius * s->planet_radius
        ? s->mu / (s->planet_radius * s->planet_radius * s->planet_radius)
        : s->mu / (r2 * sqrt(r2));
    out[0] = w * (-pull * sx - s->mu * d[0] / (s->sep * s->sep * s->sep));
    out[1] = w * (-pull * sy - s->mu * d[1] / (s->sep * s->sep * s->sep));
}
static void force_C(Scene *s, Cand *c, double out[2]) {
    double d[2], dd_[2]; cand_planet_d(s, c->t, d, dd_);
    double sx = c->rho[0] - d[0], sy = c->rho[1] - d[1];
    double px = sx + d[0], py = sy + d[1], r = norm2(px, py);
    double k = (1.0 - s->mu) / (r * r * r);
    out[0] = -k * px + (1.0 - s->mu) * d[0] / (s->sep * s->sep * s->sep);
    out[1] = -k * py + (1.0 - s->mu) * d[1] / (s->sep * s->sep * s->sep);
}
static double window(double sep, double r0, double rin) {
    if (sep >= r0) return 1.0;
    if (sep <= rin) return 0.0;
    double u = (sep - rin) / (r0 - rin);
    return u * u * u * (10.0 + u * (-15.0 + 6.0 * u));
}
// One planet-centric DKD sub-step of duration tau. wfix < 0: recompute the window each kick
// (symba); wfix = 0: no anti-kick, the kick is C alone (soi-switch inside).
static void cand_sub_step(Scene *s, Cand *c, double tau, double r0, double rin, double wfix) {
    double d[2], dd_[2], p[2], v[2];
    cand_planet_d(s, c->t, d, dd_);
    p[0] = c->rho[0] - d[0]; p[1] = c->rho[1] - d[1];
    v[0] = c->v[0] - dd_[0]; v[1] = c->v[1] - dd_[1];
    kepler(s->mu, p, v, tau / 2.0);
    c->t += tau / 2.0;
    cand_planet_d(s, c->t, d, dd_);
    c->rho[0] = p[0] + d[0]; c->rho[1] = p[1] + d[1];
    c->v[0] = v[0] + dd_[0]; c->v[1] = v[1] + dd_[1];
    double w = wfix >= 0.0 ? wfix : window(cand_sep(s, c), r0, rin);
    double cb[2], cc[2];
    force_B(s, c, w, cb); force_C(s, c, cc);
    c->v[0] += (cc[0] - cb[0]) * tau; c->v[1] += (cc[1] - cb[1]) * tau;
    c->evals++;
    cand_planet_d(s, c->t, d, dd_);
    p[0] = c->rho[0] - d[0]; p[1] = c->rho[1] - d[1];
    v[0] = c->v[0] - dd_[0]; v[1] = c->v[1] - dd_[1];
    kepler(s->mu, p, v, tau / 2.0);
    c->t += tau / 2.0;
    cand_planet_d(s, c->t, d, dd_);
    c->rho[0] = p[0] + d[0]; c->rho[1] = p[1] + d[1];
    c->v[0] = v[0] + dd_[0]; c->v[1] = v[1] + dd_[1];
}
static void cand_middle(Scene *s, Cand *c, double tau, int depth, double r0, double rin) {
    double sep = cand_sep(s, c);
    double tloc = TAU * sqrt(sep * sep * sep / s->mu);
    if (depth < LMAX && tloc < (double)SUB_RES * tau) {
        for (int i = 0; i < 3; i++) cand_middle(s, c, tau / 3.0, depth + 1, r0, rin);
    } else {
        cand_sub_step(s, c, tau, r0, rin, -1.0);
    }
}
static void cand_step(Scene *s, Cand *c, double h, Cfg cfg) {
    double hill = sc_hill(s), r0 = CO_R0_HILL * hill, rin = r0 / CO_RIN_DIV;
    double sep = cand_sep(s, c);
    if (cfg == C_WH) {
        // Wisdom-Holman: star-Kepler drift, full planet kick B at the centre, star-Kepler drift.
        double p[2] = { c->rho[0], c->rho[1] }, v[2] = { c->v[0], c->v[1] };
        kepler(1.0 - s->mu, p, v, h / 2.0);
        c->t += h / 2.0;
        c->rho[0] = p[0]; c->rho[1] = p[1]; c->v[0] = v[0]; c->v[1] = v[1];
        double b[2]; force_B(s, c, 1.0, b);
        c->v[0] += b[0] * h; c->v[1] += b[1] * h; c->evals++;
        kepler(1.0 - s->mu, p, c->v, h / 2.0);
        c->t += h / 2.0;
        c->rho[0] = p[0]; c->rho[1] = p[1];
        return;
    }
    if (cfg == C_SOI) {
        if (sep >= sc_soi(s)) {
            double p[2] = { c->rho[0], c->rho[1] }, v[2] = { c->v[0], c->v[1] };
            kepler(1.0 - s->mu, p, v, h / 2.0);
            c->t += h / 2.0;
            c->rho[0] = p[0]; c->rho[1] = p[1]; c->v[0] = v[0]; c->v[1] = v[1];
            double b[2]; force_B(s, c, 1.0, b);
            c->v[0] += b[0] * h; c->v[1] += b[1] * h; c->evals++;
            kepler(1.0 - s->mu, p, c->v, h / 2.0);
            c->t += h / 2.0;
            c->rho[0] = p[0]; c->rho[1] = p[1];
        } else {
            cand_sub_step(s, c, h, 0.0, 0.0, 0.0);
        }
        return;
    }
    // symba: one skeleton everywhere - windowed edge half-kicks of B, and a middle that is a
    // star-Kepler drift outside the changeover and recursive planet-centric sub-steps inside.
    // (Kicks commute and the ship does not move during them, so the two half-kicks of the far
    // branch merge into one evaluation when both windows are 1; counted separately here.)
    double b[2];
    force_B(s, c, window(sep, r0, rin), b);
    c->v[0] += b[0] * h / 2.0; c->v[1] += b[1] * h / 2.0; c->evals++;
    if (sep >= r0) {
        double p[2] = { c->rho[0], c->rho[1] }, v[2] = { c->v[0], c->v[1] };
        kepler(1.0 - s->mu, p, v, h);
        c->t += h;
        c->rho[0] = p[0]; c->rho[1] = p[1]; c->v[0] = v[0]; c->v[1] = v[1];
    } else {
        cand_middle(s, c, h, 1, r0, rin);
    }
    force_B(s, c, window(cand_sep(s, c), r0, rin), b);
    c->v[0] += b[0] * h / 2.0; c->v[1] += b[1] * h / 2.0; c->evals++;
}
static void cand_state_bary(Scene *s, Cand *c, double out[4]) {
    double sp[2], sv[2]; sc_star(s, c->t, sp, sv);
    out[0] = sp[0] + c->rho[0]; out[1] = sp[1] + c->rho[1];
    out[2] = sv[0] + c->v[0]; out[3] = sv[1] + c->v[1];
}

// ---------------------------------------------------------------- fit.rs::growth_exponent
static double growth_exponent(const double *err, int n) {
    int first = n / 10 > 1 ? n / 10 : 1;
    for (int i = 0; i < n; i++) if (!isfinite(err[i])) return NAN;
    if (n <= first) return NAN;
    int edge[17];
    for (int j = 0; j < 16; j++)
        edge[j] = (int)((double)first * pow((double)n / first, (double)j / 16.0) + 0.5);
    edge[16] = n;
    double px[16], py[16]; int used = 0, nz = 0;
    for (int j = 0; j < 16; j++) {
        int a = edge[j], b = edge[j + 1];
        if (b <= a) continue;
        used++;
        double top = 0.0;
        for (int i = a; i < b; i++) top = fmax(top, fabs(err[i]));
        if (top > 0.0) { px[nz] = log(sqrt((double)(a * (b - 1)))); py[nz] = log(top); nz++; }
    }
    if (used < 8) return NAN;
    if (nz == 0) return 0.0;
    if (nz < 3) return NAN;
    double mx = 0, my = 0;
    for (int i = 0; i < nz; i++) { mx += px[i]; my += py[i]; }
    mx /= nz; my /= nz;
    double num = 0, den = 0;
    for (int i = 0; i < nz; i++) { num += (px[i] - mx) * (py[i] - my); den += (px[i] - mx) * (px[i] - mx); }
    return num / den;
}

// ---------------------------------------------------------------- B12 cases
#define B12_PERIODS 200
#define B12_COARSE 8
#define B12_FINE 256
static const double B12_FLOOR = 1e-12, B12_CONVERGED = 1e-9;

typedef struct { double ship[4]; int crossings, converged; } B12Kept;
static void b12_ships(B12Kept *kept) {
    Handoff draws[47];
    handoffs(47, draws);
    for (int i = 0; i < 16; i++) {
        Handoff *d = &draws[HANDOFF_KEPT[i]];
        double rr = JUPITER.sep * (1.0 + d->side * sc_hill(&JUPITER) / JUPITER.sep * d->k);
        double v = pow(rr, -0.5);
        kept[i].ship[0] = rr * cos(d->alpha); kept[i].ship[1] = rr * sin(d->alpha);
        kept[i].ship[2] = -v * sin(d->alpha); kept[i].ship[3] = v * cos(d->alpha);
        kept[i].crossings = -1; kept[i].converged = 0;
    }
}
static double b12_dom_period(Scene *s, const double ship[4]) {
    double r = hypot(ship[0], ship[1]);
    return TAU * sqrt(r * r * r / (1.0 - s->mu));
}

// ---------------------------------------------------------------- B14 cases
#define B14_CIRC 128
#define B14_SEEDS 256
#define B14_PERIODS 50
#define B14_SPP 64
static const double B14_ESCAPE_HILL = 1.5, B14_NUDGE = 1e-6, B14_APSIDES_STABLE = 0.02;

static void b14_births(double draws[B14_SEEDS][3]) {
    Rng r1 = { HILL_SEED }, r2 = { ECCENTRIC_SEED };
    for (int i = 0; i < 128; i++) { draws[i][0] = 0.2 + 0.7 * rng_unit(&r1); draws[i][1] = TAU * rng_unit(&r1); draws[i][2] = 0.0; }
    for (int i = 128; i < 256; i++) { draws[i][0] = 0.2 + 0.7 * rng_unit(&r2); draws[i][1] = TAU * rng_unit(&r2); draws[i][2] = 0.3 * rng_unit(&r2); }
}
static void b14_birth(Scene *s, double a, double phase, double e0, int prograde, double ship[4]) {
    double sn = sin(phase), cs = cos(phase);
    double r = a * (1.0 - e0);
    double v = sqrt(s->mu * (1.0 + e0) / (a * (1.0 - e0))) * (prograde ? 1.0 : -1.0);
    sc_barycentric(s, 0.0, (double[4]){ r * cs, r * sn, -v * sn, v * cs }, ship);
}
static int apsides_series(Scene *s, const double *times, const double (*states)[4], int n, double *out) {
    double last = 0.0; int any = 0;
    for (int i = 0; i < n; i++) {
        double w[4]; sc_relative(s, times[i], states[i], w);
        double r2 = w[0] * w[0] + w[1] * w[1], v2 = w[2] * w[2] + w[3] * w[3], rv = w[0] * w[2] + w[1] * w[3];
        double k = v2 - s->mu / sqrt(r2);
        double ex = k * w[0] - rv * w[2], ey = k * w[1] - rv * w[3];
        if (!(hypot(ex, ey) > 1e-9 * s->mu)) return 0;
        double varpi = atan2(ey, ex);
        if (!isfinite(varpi)) return 0;
        if (!any) { out[i] = last = varpi; any = 1; continue; }
        double jump = fmod(varpi - last, TAU);
        if (jump > PI) jump -= TAU; else if (jump < -PI) jump += TAU;
        if (fabs(jump) > PI / 2.0) return 0;
        out[i] = last + jump; last = out[i];
    }
    return any;
}
static int apsidal_rate(Scene *s, const double *times, const double (*states)[4], int n, double *rate) {
    double *vp = malloc(sizeof(double) * n);
    if (!apsides_series(s, times, states, n, vp)) { free(vp); return 0; }
    double mu = 0, mv = 0;
    for (int i = 0; i < n; i++) { mu += times[i] / sc_period(s); mv += vp[i]; }
    mu /= n; mv /= n;
    double num = 0, den = 0;
    for (int i = 0; i < n; i++) { double u = times[i] / sc_period(s) - mu; num += u * (vp[i] - mv); den += u * u; }
    free(vp);
    if (!(den > 0.0)) return 0;
    *rate = num / den;
    return 1;
}
// One reference run: fills states up to the first escape (or the end); -1 = gave up, else 0/1 class.
static int b14_run(Scene *s, double rtol, const double ship[4], const double *times, int n,
                   double (*st)[4]) {
    Ref it; ref_init(&it, s, rtol, ship);
    for (int i = 0; i < n; i++) {
        if (!ref_advance(&it, times[i], st[i])) return -1;
        if (!(sc_planet_distance(s, times[i], st[i]) <= B14_ESCAPE_HILL * sc_hill(s))) return 1;
    }
    return 0;
}

// ---------------------------------------------------------------- B17 resonance cases
#define RES_SEP 100.0
static const double RES_MU[3] = { 3e-5, 3e-4, 3e-3 };
static const double RES_DET[3] = { -1.0 / 3.0, 0.0, 1.0 / 3.0 };
static const double RES_PHASES[2] = { 4.0 * PI / 180.0, 172.0 * PI / 180.0 };
#define RES_SYNODIC 200.0
typedef struct { Scene scene; int kind_j; double ratio, e0, m0, p1; int nsamp; char name[64]; } ResCase;
static double res_half_width(double mu) { return 2.5 * pow(mu, 2.0 / 3.0); }
static int res_cases(ResCase *out) {
    int n = 0;
    for (int ji = 0; ji < 2; ji++) {
        double exact = ji == 0 ? 2.0 : 1.5;
        for (int mi = 0; mi < 3; mi++) for (int di = 0; di < 3; di++) for (int ph = 0; ph < 2; ph++) {
            ResCase *c = &out[n];
            scene_init(&c->scene, RES_MU[mi], RES_SEP, 1e-3 * RES_SEP);
            c->kind_j = ji + 1;
            c->ratio = exact * (1.0 + RES_DET[di] * res_half_width(RES_MU[mi]));
            c->e0 = 0.02; c->m0 = RES_PHASES[ph];
            c->p1 = TAU / (c->ratio * sc_omega(&c->scene));
            double syn = 1.0 / (1.0 / c->p1 - 1.0 / sc_period(&c->scene));
            c->nsamp = (int)ceil(RES_SYNODIC * syn / (c->p1 / 8.0));
            snprintf(c->name, sizeof c->name, "%d:%d mu %.0e detune %+.2f phase %d", c->kind_j + 1, c->kind_j, RES_MU[mi], RES_DET[di], ph);
            n++;
        }
    }
    double ctl[5][3] = { {5.0, 3e-4, 0.05}, {2.55, 3e-4, 0.05}, {2.15, 3e-4, 0.05}, {5.0, 3e-3, 0.1}, {2.55, 3e-3, 0.1} };
    for (int i = 0; i < 5; i++) {
        ResCase *c = &out[n];
        scene_init(&c->scene, ctl[i][1], RES_SEP, 1e-3 * RES_SEP);
        c->kind_j = -1; c->ratio = ctl[i][0]; c->e0 = ctl[i][2]; c->m0 = RES_PHASES[0];
        c->p1 = TAU / (c->ratio * sc_omega(&c->scene));
        double syn = 1.0 / (1.0 / c->p1 - 1.0 / sc_period(&c->scene));
        c->nsamp = (int)ceil(RES_SYNODIC * syn / (c->p1 / 8.0));
        snprintf(c->name, sizeof c->name, "control %.2f mu %.0e", ctl[i][0], ctl[i][1]);
        n++;
    }
    return n;
}
static void res_start(ResCase *c, double ship[4]) {
    Scene *s = &c->scene;
    double n1 = c->ratio * sc_omega(s);
    double a = cbrt((1.0 - s->mu) / (n1 * n1));
    double e = c->e0, ea = c->m0;
    for (int i = 0; i < 50; i++) ea -= (ea - e * sin(ea) - c->m0) / (1.0 - e * cos(ea));
    double se = sin(ea), ce = cos(ea);
    double f = n1 * a / (1.0 - e * ce);
    double p[2], v[2]; sc_star(s, 0.0, p, v);
    ship[0] = p[0] + a * (ce - e);
    ship[1] = p[1] + a * sqrt(1.0 - e * e) * se;
    ship[2] = v[0] - f * se;
    ship[3] = v[1] + f * sqrt(1.0 - e * e) * ce;
}
static double res_wrap(double x) {
    double y = fmod(x, TAU);
    if (y > PI) return y - TAU;
    if (y < -PI) return y + TAU;
    return y;
}
static void res_elements(Scene *s, double t, const double st[4], double *a, double *e, double *varpi, double *lam) {
    double p[2], v[2]; sc_star(s, t, p, v);
    double x = st[0] - p[0], y = st[1] - p[1], vx = st[2] - v[0], vy = st[3] - v[1];
    double gm = 1.0 - s->mu;
    double r = sqrt(x * x + y * y), v2 = vx * vx + vy * vy, rv = x * vx + y * vy;
    double k = v2 - gm / r;
    double ex = (k * x - rv * vx) / gm, ey = (k * y - rv * vy) / gm;
    *e = hypot(ex, ey); *varpi = atan2(ey, ex);
    *a = 1.0 / (2.0 / r - v2 / gm);
    double ce = (1.0 - r / *a) / *e, se = rv / (*e * sqrt(gm * *a));
    *lam = *varpi + (atan2(se, ce) - *e * se);
}
typedef struct { double e_min, e_max, excursion; } Track;
static int res_track(ResCase *c, const double *times, const double (*states)[4], int n, Track *tr) {
    double j = c->kind_j >= 0 ? (double)c->kind_j : 0.0;
    double e_min = INFINITY, e_max = 0.0, lo = INFINITY, hi = -INFINITY, prev = 0.0, un = 0.0;
    for (int i = 0; i < n; i++) {
        double a, e, varpi, lam;
        res_elements(&c->scene, times[i], states[i], &a, &e, &varpi, &lam);
        if (!(a > 0.0 && e > 0.0 && e < 1.0 && isfinite(lam) && isfinite(varpi))) return 0;
        double phi = res_wrap((j + 1.0) * sc_phase(&c->scene, times[i]) - j * lam - varpi);
        un = i == 0 ? phi : un + res_wrap(phi - prev);
        prev = phi;
        e_min = fmin(e_min, e); e_max = fmax(e_max, e); lo = fmin(lo, un); hi = fmax(hi, un);
    }
    tr->e_min = e_min; tr->e_max = e_max; tr->excursion = hi - lo;
    return 1;
}
// One reference run for a resonance case; 0 if it gave up or left a bound orbit.
static int res_run(ResCase *c, double rtol, double nudge, const double *times,
                   double (*st)[4], Track *tr, uint64_t *evals) {
    double ship[4]; res_start(c, ship);
    if (nudge != 0.0) {
        double p[2], v[2]; sc_star(&c->scene, 0.0, p, v);
        double sc = 1.0 + nudge;
        ship[0] = p[0] + (ship[0] - p[0]) * sc; ship[1] = p[1] + (ship[1] - p[1]) * sc;
        ship[2] = v[0] + (ship[2] - v[0]) / sqrt(sc); ship[3] = v[1] + (ship[3] - v[1]) / sqrt(sc);
    }
    Ref it; ref_init(&it, &c->scene, rtol, ship);
    for (int i = 0; i < c->nsamp; i++) if (!ref_advance(&it, times[i], st[i])) return 0;
    if (evals) *evals = it.evals;
    return res_track(c, times, st, c->nsamp, tr);
}
static int res_close(Track *a, Track *b) {
    return fabs(a->e_max - b->e_max) <= 1e-3 * a->e_max
        && fabs(a->e_min - b->e_min) <= 1e-3 * a->e_max
        && fabs(a->excursion - b->excursion) <= 1e-2 * fmax(a->excursion, 1.0);
}

// ---------------------------------------------------------------- JSON output
static FILE *g_out;
static void jnum(double x) {
    if (isnan(x)) fprintf(g_out, "null");
    else if (isinf(x)) fprintf(g_out, x > 0 ? "1e999" : "-1e999");
    else fprintf(g_out, "%.17g", x);
}
static void jarr_d(const char *key, double *xs, int n) {
    fprintf(g_out, "\"%s\":[", key);
    for (int i = 0; i < n; i++) { jnum(xs[i]); fprintf(g_out, "%s", i < n - 1 ? "," : ""); }
    fprintf(g_out, "]");
}
static void jarr_i(const char *key, int *xs, int n) {
    fprintf(g_out, "\"%s\":[", key);
    for (int i = 0; i < n; i++) fprintf(g_out, "%s%d", i ? "," : "", xs[i]);
    fprintf(g_out, "]");
}

// ---------------------------------------------------------------- B12 truth
static void run_b12_truth(void) {
    Scene *s = &JUPITER;
    B12Kept kept[16]; b12_ships(kept);
    int nsamp = B12_PERIODS * B12_COARSE + 1;
    double exps[16], maxs[16], epo[16];
    double *series[3] = { malloc(sizeof(double) * nsamp), malloc(sizeof(double) * nsamp), malloc(sizeof(double) * nsamp) };
    for (int i = 0; i < 16; i++) {
        double *cj = malloc(sizeof(double) * nsamp), *cjf = malloc(sizeof(double) * nsamp);
        double c0 = sc_jacobi(s, 0.0, kept[i].ship);
        Ref it; ref_init(&it, s, 1e-12, kept[i].ship);
        int cross = 0, inside = -1, ok = 1;
        for (int j = 0; j <= B12_PERIODS * B12_FINE; j++) {
            double t = (double)j * sc_period(s) / (double)B12_FINE;
            double st[4];
            if (!ref_advance(&it, t, st)) { ok = 0; break; }
            int now = sc_planet_distance(s, t, st) < sc_soi(s);
            if (inside >= 0 && now != inside) cross++;
            inside = now;
            if (j % (B12_FINE / B12_COARSE) == 0) cj[j / (B12_FINE / B12_COARSE)] = sc_jacobi(s, t, st);
        }
        kept[i].crossings = ok ? cross : -1;
        Ref fine; ref_init(&fine, s, 1e-13, kept[i].ship);
        int okf = 1;
        for (int j = 0; j < nsamp; j++) {
            double t = (double)j * sc_period(s) / (double)B12_COARSE, st[4];
            if (!ref_advance(&fine, t, st)) { okf = 0; break; }
            cjf[j] = sc_jacobi(s, t, st);
        }
        kept[i].converged = ok && okf;
        if (kept[i].converged)
            for (int j = 0; j < nsamp; j++)
                if (fabs((cjf[j] - cj[j]) / c0) > B12_CONVERGED) { kept[i].converged = 0; break; }
        double *err = malloc(sizeof(double) * nsamp);
        for (int j = 0; j < nsamp; j++) err[j] = fabs((cj[j] - c0) / c0);
        exps[i] = growth_exponent(err, nsamp);
        maxs[i] = 0.0;
        for (int j = 0; j < nsamp; j++) maxs[i] = fmax(maxs[i], err[j]);
        int keep_err = 0;
        for (int q = 0; q < 3; q++) if (PIC_SHIPS[q] == i) { memcpy(series[q], err, sizeof(double) * nsamp); keep_err = 1; }
        if (!keep_err) free(err);
        epo[i] = (double)it.evals / (B12_PERIODS * sc_period(s) / b12_dom_period(s, kept[i].ship));
        free(cj); free(cjf);
        fprintf(stderr, "b12 truth ship %d: crossings %d converged %d\n", i, kept[i].crossings, kept[i].converged);
    }
    fprintf(g_out, "\"ships_truth\":{");
    {
        int cr[16], cv[16];
        for (int i = 0; i < 16; i++) { cr[i] = kept[i].crossings; cv[i] = kept[i].converged; }
        jarr_i("crossings", cr, 16); fputs(",", g_out);
        jarr_i("converged", cv, 16); fputs(",", g_out);
        jarr_d("err_exponent", exps, 16); fputs(",", g_out);
        jarr_d("max_err", maxs, 16); fputs(",", g_out);
        jarr_d("evals_per_orbit", epo, 16); fputs(",", g_out);
        fprintf(g_out, "\"err_series\":{");
        for (int q = 0; q < 3; q++) {
            fprintf(g_out, "%s\"%d\":[", q ? "," : "", PIC_SHIPS[q]);
            for (int j = 0; j < nsamp; j++) { jnum(series[q][j]); fprintf(g_out, "%s", j < nsamp - 1 ? "," : ""); }
            fprintf(g_out, "]");
        }
        fprintf(g_out, "}}\n");
    }
    for (int q = 0; q < 3; q++) free(series[q]);
    fflush(g_out);
}

// ---------------------------------------------------------------- B12 candidates
static void run_b12_cand(Cfg cfg) {
    Scene *s = &JUPITER;
    B12Kept kept[16]; b12_ships(kept);
    int nsamp = B12_PERIODS * B12_COARSE + 1;
    double exps[16], maxs[16], epo[16];
    double *series[3] = { malloc(sizeof(double) * nsamp), malloc(sizeof(double) * nsamp), malloc(sizeof(double) * nsamp) };
    double h = sc_period(s) / 128.0;
    for (int i = 0; i < 16; i++) {
        Cand c = { .t = 0.0, .evals = 0 };
        double sp[2], sv[2]; sc_star(s, 0.0, sp, sv);
        c.rho[0] = kept[i].ship[0] - sp[0]; c.rho[1] = kept[i].ship[1] - sp[1];
        c.v[0] = kept[i].ship[2] - sv[0]; c.v[1] = kept[i].ship[3] - sv[1];
        double c0 = sc_jacobi(s, 0.0, kept[i].ship);
        double *err = malloc(sizeof(double) * nsamp);
        err[0] = 0.0;
        for (int n = 1; n <= B12_PERIODS * 128; n++) {
            cand_step(s, &c, h, cfg);
            if (n % 16 == 0) {
                double st[4]; cand_state_bary(s, &c, st);
                double t = (double)(n / 16) * sc_period(s) / (double)B12_COARSE;
                err[n / 16] = fabs((sc_jacobi(s, t, st) - c0) / c0);
            }
        }
        exps[i] = growth_exponent(err, nsamp);
        maxs[i] = 0.0;
        for (int j = 0; j < nsamp; j++) maxs[i] = fmax(maxs[i], err[j]);
        int keep = 0;
        for (int q = 0; q < 3; q++) if (PIC_SHIPS[q] == i) { memcpy(series[q], err, sizeof(double) * nsamp); keep = 1; }
        if (!keep) free(err);
        epo[i] = (double)c.evals / (B12_PERIODS * sc_period(s) / b12_dom_period(s, kept[i].ship));
    }
    fprintf(g_out, "\"ships\":{");
    jarr_d("exponent", exps, 16); fputs(",", g_out);
    jarr_d("max_err", maxs, 16); fputs(",", g_out);
    jarr_d("evals_per_orbit", epo, 16); fputs(",", g_out);
    fprintf(g_out, "\"err_series\":{");
    for (int q = 0; q < 3; q++) {
        fprintf(g_out, "%s\"%d\":[", q ? "," : "", PIC_SHIPS[q]);
        for (int j = 0; j < nsamp; j++) { jnum(series[q][j]); fprintf(g_out, "%s", j < nsamp - 1 ? "," : ""); }
        fprintf(g_out, "]");
    }
    fprintf(g_out, "}}\n");
    for (int q = 0; q < 3; q++) free(series[q]);
    fflush(g_out);
}

// ---------------------------------------------------------------- B14 truth (classes: 0 bound, 1 escape, 2 chaotic, 3 unconverged)
static void b14_truth_one(Scene *s, const double *times, int n, double a_hill, double phase, double e0,
                          int prograde, int *cls, double *rate) {
    double a = a_hill * sc_hill(s);
    double ship[4], ship_n[4];
    b14_birth(s, a, phase, e0, prograde, ship);
    b14_birth(s, a * (1.0 + B14_NUDGE), phase, e0, prograde, ship_n);
    double (*st)[4] = malloc(sizeof(double[4]) * n);
    double (*sf)[4] = malloc(sizeof(double[4]) * n);
    double (*sn)[4] = malloc(sizeof(double[4]) * n);
    *cls = 3; *rate = 0.0;
    int c0 = b14_run(s, 1e-12, ship, times, n, st);
    if (c0 < 0) goto done;
    {
        int cf = b14_run(s, 1e-13, ship, times, n, sf);
        if (cf < 0 || (cf == 0) != (c0 == 0)) goto done;
        int cn = b14_run(s, 1e-12, ship_n, times, n, sn);
        if (cn < 0 || (cn == 0) != (c0 == 0)) { *cls = 2; goto done; }
        *cls = c0;
        if (c0 == 1) goto done;
        {
            double a_rate, f_rate, n_rate;
            if (!apsidal_rate(s, times, st, n, &a_rate) || a_rate == 0.0) goto done;
            if (!apsidal_rate(s, times, sf, n, &f_rate)) goto done;
            if (!apsidal_rate(s, times, sn, n, &n_rate)) goto done;
            if (fabs(f_rate - a_rate) <= B14_APSIDES_STABLE * fabs(a_rate)
                && fabs(n_rate - a_rate) <= B14_APSIDES_STABLE * fabs(a_rate)) *rate = a_rate;
        }
    }
done:
    free(st); free(sf); free(sn);
}
static void run_b14_truth(void) {
    Scene *s = &JUPITER;
    int n = B14_PERIODS * B14_SPP;
    double *times = malloc(sizeof(double) * n);
    for (int i = 0; i < n; i++) times[i] = (double)(i + 1) * sc_period(s) / (double)B14_SPP;
    double draws[256][3]; b14_births(draws);
    static int cls[256]; static double rates[256];
    for (int i = 0; i < 256; i++) {
        b14_truth_one(s, times, n, draws[i][0], draws[i][1], draws[i][2], i % 2 == 0, &cls[i], &rates[i]);
        fprintf(stderr, "b14 truth moon %d: class %d rate %.6g\r", i, cls[i], rates[i]);
    }
    fputc('\n', stderr);
    fprintf(g_out, "\"moons_truth\":{");
    jarr_i("class", cls, 256); fputs(",", g_out);
    { double r2[256]; for (int i = 0; i < 256; i++) r2[i] = rates[i] != 0.0 ? rates[i] : NAN; jarr_d("rate", r2, 256); }
    fprintf(g_out, "}\n");
    free(times);
    fflush(g_out);
}

// ---------------------------------------------------------------- B14 candidates
static void run_b14_cand(Cfg cfg) {
    Scene *s = &JUPITER;
    int n = B14_PERIODS * B14_SPP;
    double *times = malloc(sizeof(double) * n);
    for (int i = 0; i < n; i++) times[i] = (double)(i + 1) * sc_period(s) / (double)B14_SPP;
    double draws[256][3]; b14_births(draws);
    double h = sc_period(s) / 128.0;
    static int esc[256], have[256];
    static double rates[256], epo[256];
    double (*st)[4] = malloc(sizeof(double[4]) * n);
    for (int i = 0; i < 256; i++) {
        double a = draws[i][0] * sc_hill(s);
        double ship[4]; b14_birth(s, a, draws[i][1], draws[i][2], i % 2 == 0, ship);
        Cand c = { .t = 0.0, .evals = 0 };
        double sp[2], sv[2]; sc_star(s, 0.0, sp, sv);
        c.rho[0] = ship[0] - sp[0]; c.rho[1] = ship[1] - sp[1];
        c.v[0] = ship[2] - sv[0]; c.v[1] = ship[3] - sv[1];
        esc[i] = 0; have[i] = 0; rates[i] = 0.0;
        for (int k = 0; k < n; k++) {
            cand_step(s, &c, h, cfg);
            cand_step(s, &c, h, cfg);
            cand_state_bary(s, &c, st[k]);
            if (!(sc_planet_distance(s, times[k], st[k]) <= B14_ESCAPE_HILL * sc_hill(s))) { esc[i] = 1; break; }
        }
        if (!esc[i]) have[i] = apsidal_rate(s, times, st, n, &rates[i]);
        epo[i] = (double)c.evals / (B14_PERIODS * sc_period(s) / (TAU * sqrt(a * a * a / s->mu)));
        if (i % 32 == 0) fprintf(stderr, "b14 cand %s moon %d\r", "x", i);
    }
    fputc('\n', stderr);
    fprintf(g_out, "\"moons\":{");
    jarr_i("escaped", esc, 256); fputs(",", g_out);
    { double r2[256]; for (int i = 0; i < 256; i++) r2[i] = have[i] ? rates[i] : NAN; jarr_d("rate", r2, 256); } fputs(",", g_out);
    jarr_d("evals_per_orbit", epo, 256);
    fprintf(g_out, "}\n");
    free(times); free(st);
    fflush(g_out);
}

// ---------------------------------------------------------------- Resonance truth and candidates
static void run_res_truth(void) {
    ResCase cases[41]; int n = res_cases(cases);
    static double emin[41], emax[41], exc[41], epo[41];
    static int cv[41];
    for (int i = 0; i < n; i++) {
        ResCase *c = &cases[i];
        double *times = malloc(sizeof(double) * c->nsamp);
        for (int k = 0; k < c->nsamp; k++) times[k] = (double)(k + 1) * (c->p1 / 8.0);
        double (*st)[4] = malloc(sizeof(double[4]) * c->nsamp);
        Track base, other;
        uint64_t ev = 0;
        cv[i] = 0; emin[i] = emax[i] = exc[i] = NAN;
        if (res_run(c, 1e-12, 0.0, times, st, &base, &ev)) {
            emin[i] = base.e_min; emax[i] = base.e_max; exc[i] = base.excursion;
            int hf = res_run(c, 1e-13, 0.0, times, st, &other, NULL);
            int hn = res_run(c, 1e-12, 1e-9, times, st, &other, NULL);
            cv[i] = hf && hn && res_close(&base, &other);
        }
        double syn = 1.0 / (1.0 / c->p1 - 1.0 / sc_period(&c->scene));
        epo[i] = (double)ev / (RES_SYNODIC * syn / c->p1);
        free(times); free(st);
        fprintf(stderr, "res truth %d/%d %s cv %d\r", i + 1, n, cases[i].name, cv[i]);
    }
    fputc('\n', stderr);
    fprintf(g_out, "\"res_truth\":{");
    fprintf(g_out, "\"names\":[");
    for (int i = 0; i < n; i++) fprintf(g_out, "%s\"%s\"", i ? "," : "", cases[i].name);
    fprintf(g_out, "],\"kind_j\":[");
    for (int i = 0; i < n; i++) fprintf(g_out, "%s%d", i ? "," : "", cases[i].kind_j);
    fputs("],", g_out);
    jarr_d("e_min", emin, n); fputs(",", g_out);
    jarr_d("e_max", emax, n); fputs(",", g_out);
    jarr_d("excursion", exc, n); fputs(",", g_out);
    jarr_i("converged", cv, n); fputs(",", g_out);
    jarr_d("evals_per_orbit", epo, n);
    fprintf(g_out, "}\n");
    fflush(g_out);
}
static void run_res_cand(Cfg cfg) {
    ResCase cases[41]; int n = res_cases(cases);
    static double emin[41], emax[41], exc[41], epo[41];
    for (int i = 0; i < n; i++) {
        ResCase *c = &cases[i];
        double h = c->p1 / 128.0;
        double ship[4]; res_start(c, ship);
        Cand cd = { .t = 0.0, .evals = 0 };
        double sp[2], sv[2]; sc_star(&c->scene, 0.0, sp, sv);
        cd.rho[0] = ship[0] - sp[0]; cd.rho[1] = ship[1] - sp[1];
        cd.v[0] = ship[2] - sv[0]; cd.v[1] = ship[3] - sv[1];
        double *times = malloc(sizeof(double) * c->nsamp);
        double (*st)[4] = malloc(sizeof(double[4]) * c->nsamp);
        for (int k = 0; k < c->nsamp; k++) {
            for (int q = 0; q < 16; q++) cand_step(&c->scene, &cd, h, cfg);
            times[k] = (double)(k + 1) * (c->p1 / 8.0);
            cand_state_bary(&c->scene, &cd, st[k]);
        }
        Track tr;
        emin[i] = emax[i] = exc[i] = NAN;
        if (res_track(c, times, st, c->nsamp, &tr)) { emin[i] = tr.e_min; emax[i] = tr.e_max; exc[i] = tr.excursion; }
        double syn = 1.0 / (1.0 / c->p1 - 1.0 / sc_period(&c->scene));
        epo[i] = (double)cd.evals / (RES_SYNODIC * syn / c->p1);
        free(times); free(st);
        fprintf(stderr, "res cand %d/%d\r", i + 1, n);
    }
    fputc('\n', stderr);
    fprintf(g_out, "\"res\":{");
    jarr_d("e_min", emin, n); fputs(",", g_out);
    jarr_d("e_max", emax, n); fputs(",", g_out);
    jarr_d("excursion", exc, n); fputs(",", g_out);
    jarr_d("evals_per_orbit", epo, n);
    fprintf(g_out, "}\n");
    fflush(g_out);
}

// ---------------------------------------------------------------- one-moon probe
static void moonchk(double a_hill, double e0, int prograde, int periods) {
    Scene *s = &JUPITER;
    double a = a_hill * sc_hill(s);
    double ship[4]; b14_birth(s, a, 0.7, e0, prograde, ship);
    double cj0 = sc_jacobi(s, 0.0, ship);
    int n = periods * B14_SPP;
    double *times = malloc(sizeof(double) * n);
    for (int i = 0; i < n; i++) times[i] = (double)(i + 1) * sc_period(s) / (double)B14_SPP;
    double (*st)[4] = malloc(sizeof(double[4]) * n);
    // reference
    int esc = 0; double cjmax = 0;
    Ref it; ref_init(&it, s, 1e-12, ship);
    for (int i = 0; i < n; i++) {
        if (!ref_advance(&it, times[i], st[i])) { printf("ref gave up\n"); break; }
        cjmax = fmax(cjmax, fabs((sc_jacobi(s, times[i], st[i]) - cj0) / cj0));
        if (!(sc_planet_distance(s, times[i], st[i]) <= 1.5 * sc_hill(s))) { esc = 1; printf("ref escapes at %.2f periods\n", (double)(i + 1) / 64); break; }
    }
    double rate; int hr = esc ? 0 : apsidal_rate(s, times, st, n, &rate);
    printf("reference: escaped=%d max|dCj/Cj|=%.3e rate=%s\n", esc, cjmax, hr ? "yes" : "no");
    if (hr) printf("  rate %.6g rad/period\n", rate);
    const char *names[3] = { "symba", "wh", "soi" };
    for (int cfgi = 0; cfgi < 3; cfgi++) {
        Cfg cfg = (Cfg)cfgi;
        Cand c = { .t = 0.0, .evals = 0 };
        double sp[2], sv[2]; sc_star(s, 0.0, sp, sv);
        c.rho[0] = ship[0] - sp[0]; c.rho[1] = ship[1] - sp[1];
        c.v[0] = ship[2] - sv[0]; c.v[1] = ship[3] - sv[1];
        double h = sc_period(s) / 128.0;
        int myesc = 0, k = 0; double mycj = 0;
        for (k = 0; k < n; k++) {
            cand_step(s, &c, h, cfg);
            cand_step(s, &c, h, cfg);
            cand_state_bary(s, &c, st[k]);
            mycj = fmax(mycj, fabs((sc_jacobi(s, times[k], st[k]) - cj0) / cj0));
            if (!(sc_planet_distance(s, times[k], st[k]) <= 1.5 * sc_hill(s))) { myesc = 1; break; }
        }
        double myrate; int mhr = myesc ? 0 : apsidal_rate(s, times, st, n, &myrate);
        printf("%-7s: escaped=%d max|dCj/Cj|=%.3e rate=%s%s  evals/orbit=%.0f\n", names[cfgi], myesc, mycj,
               mhr ? "yes" : "no", (hr && mhr) ? (fabs(myrate / rate - 1) < 0.1 ? " (within 10%)" : " (OFF)") : "",
               (double)c.evals / ((double)(myesc ? k + 1 : n) * 2.0 / 128.0 * (sc_period(s) / (TAU * sqrt(a * a * a / s->mu)))));
    }
    free(times); free(st);
}

// ---------------------------------------------------------------- self-test
static void selftest(void) {
    Rng rng = { 42 };
    double worst = 0.0;
    int tested = 0;
    for (int i = 0; i < 50000; i++) {
        double gm = pow(10.0, -3.0 + 3.0 * rng_unit(&rng));
        double rad = pow(10.0, 5.0 + 3.5 * rng_unit(&rng));
        double th = TAU * rng_unit(&rng);
        double p[2] = { rad * cos(th), rad * sin(th) };
        double vmag = sqrt(gm / rad) * pow(10.0, -1.0 + 2.6 * rng_unit(&rng));
        double ang = TAU * rng_unit(&rng);
        double v[2] = { vmag * cos(ang), vmag * sin(ang) };
        double dt = rad / fmax(vmag, 1e-30) * pow(10.0, -3.0 + 4.0 * rng_unit(&rng)) * (rng_unit(&rng) < 0.5 ? 1.0 : -1.0);
        double p0[2] = { p[0], p[1] }, v0[2] = { v[0], v[1] };
        kepler(gm, p, v, dt); kepler(gm, p, v, -dt);
        double err = norm2(p[0] - p0[0], p[1] - p0[1]) / rad + norm2(v[0] - v0[0], v[1] - v0[1]) / fmax(vmag, 1e-30);
        if (err > worst) worst = err;
        tested++;
    }
    printf("kepler round-trip: %d states, worst relative error %.3e (needs < 1e-11)\n", tested, worst);
    scene_init(&JUPITER, 1e-3, 5.27e8, 4.84e4);
    Scene *s = &JUPITER;
    // far-field: symba == wh-fixed when the changeover never engages
    double rr = s->sep * 1.5, v = pow(rr, -0.5);
    double ship[4] = { rr, 0, 0, v };
    Cand a = { .t = 0 }, b = { .t = 0 };
    double sp[2], sv[2]; sc_star(s, 0.0, sp, sv);
    for (int k = 0; k < 2; k++) {
        Cand *c = k ? &b : &a;
        c->rho[0] = ship[0] - sp[0]; c->rho[1] = ship[1] - sp[1];
        c->v[0] = ship[2] - sv[0]; c->v[1] = ship[3] - sv[1];
    }
    double h = sc_period(s) / 128.0;
    for (int i = 0; i < 500; i++) { cand_step(s, &a, h, C_SYMBA); cand_step(s, &b, h, C_WH); }
    printf("far-field symba vs wh-fixed: %.3e (needs 0)\n",
           fabs(a.rho[0] - b.rho[0]) + fabs(a.rho[1] - b.rho[1]) + fabs(a.v[0] - b.v[0]) + fabs(a.v[1] - b.v[1]));
    // a moon at 0.5 Hill radii through symba for 5 planet periods: stays bound, C_J near constant
    double a_m = 0.5 * sc_hill(s);
    double mship[4]; b14_birth(s, a_m, 1.0, 0.0, 1, mship);
    Cand c = { .t = 0 };
    sc_star(s, 0.0, sp, sv);
    c.rho[0] = mship[0] - sp[0]; c.rho[1] = mship[1] - sp[1];
    c.v[0] = mship[2] - sv[0]; c.v[1] = mship[3] - sv[1];
    double cj0 = sc_jacobi(s, 0.0, mship), drift = 0.0;
    for (int i = 0; i < 5 * 128; i++) {
        cand_step(s, &c, h, C_SYMBA);
        if (i % 16 == 0) {
            double st[4]; cand_state_bary(s, &c, st);
            double t = (double)(i + 1) * (sc_period(s) / 128.0);
            drift = fmax(drift, fabs((sc_jacobi(s, t, st) - cj0) / cj0));
        }
    }
    printf("moon at 0.5 R_H, symba 5 periods: max |dC_J/C_J| %.3e, final sep %.3f R_H\n",
           drift, cand_sep(s, &c) / sc_hill(s));
    printf("selftest done\n");
}

// ---------------------------------------------------------------- main
int main(int argc, char **argv) {
    scene_init(&JUPITER, 1e-3, 5.27e8, 4.84e4);
    if (argc < 2) { fprintf(stderr, "usage: r10 <selftest|truth|symba|wh|soi>\n"); return 1; }
    if (!strcmp(argv[1], "selftest")) { selftest(); return 0; }
    if (!strcmp(argv[1], "diag")) {
        double r0mul = argc > 2 ? atof(argv[2]) : 1.3;
        CO_R0_HILL = r0mul;
        Scene *s = &JUPITER;
        B12Kept kept[16]; b12_ships(kept);
        int which = argc > 3 ? atoi(argv[3]) : 0;
        Cand c = { .t = 0.0, .evals = 0 };
        double sp[2], sv[2]; sc_star(s, 0.0, sp, sv);
        c.rho[0] = kept[which].ship[0] - sp[0]; c.rho[1] = kept[which].ship[1] - sp[1];
        c.v[0] = kept[which].ship[2] - sv[0]; c.v[1] = kept[which].ship[3] - sv[1];
        double c0 = sc_jacobi(s, 0.0, kept[which].ship);
        double h = sc_period(s) / 128.0;
        int zone = -1;
        for (int n = 1; n <= B12_PERIODS * 128; n++) {
            cand_step(s, &c, h, C_SYMBA);
            if (n % 16 == 0) {
                double st[4]; cand_state_bary(s, &c, st);
                double t = (double)(n / 16) * sc_period(s) / (double)B12_COARSE;
                double err = fabs((sc_jacobi(s, t, st) - c0) / c0);
                double sepR = cand_sep(s, &c) / sc_hill(s);
                int z = sepR >= r0mul ? 0 : (sepR <= r0mul / 3.0 ? 2 : 1);
                if (z != zone) { printf("ZONE %d->%d at t=%.2f err=%.3e\n", zone, z, t / sc_period(s), err); zone = z; }
                if (n % 128 == 0) printf("t=%6.1f err=%.3e sep=%.3f\n", t / sc_period(s), err, sepR);
            }
        }
        return 0;
    }
    if (!strcmp(argv[1], "moonchk")) {
        double a_hill = argc > 2 ? atof(argv[2]) : 0.5;
        double e0 = argc > 3 ? atof(argv[3]) : 0.0;
        int pro = argc > 4 ? atoi(argv[4]) : 1;
        int per = argc > 5 ? atoi(argv[5]) : 5;
        moonchk(a_hill, e0, pro, per);
        return 0;
    }
    const char *mode = argv[1];
    char path[256];
    snprintf(path, sizeof path, "raw-%s.json", mode);
    g_out = fopen(path, "w");
    if (!g_out) { perror("open"); return 1; }
    if (!strcmp(mode, "truth")) {
        run_b12_truth();
        run_b14_truth();
        run_res_truth();
    } else {
        Cfg cfg = !strcmp(mode, "symba") ? C_SYMBA : !strcmp(mode, "wh") ? C_WH : C_SOI;
        run_b12_cand(cfg);
        run_b14_cand(cfg);
        run_res_cand(cfg);
    }
    fclose(g_out);
    return 0;
}
