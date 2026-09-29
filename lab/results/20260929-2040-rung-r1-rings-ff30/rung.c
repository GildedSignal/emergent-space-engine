/* rung r1: orbits in rings around one mass.  Configurations: binet-m8/m16/m32,
 * river-m16/m32, square (negative), tilt (negative).  Oracle functions are ports
 * of xtask/src/gr_oracle.rs and gr_oracle_extended.rs (periapsis_elliptic,
 * bound_period_quad, deflection_quadrature), each cross-checked against an
 * independent RK4 integration below (oracle_check.txt).
 *
 * Author rules the rung leaves open (documented in dossier.md):
 *  - Binet time rule: per band, dt = GL16 of E/(L u^2 (1-2u)) over the band's
 *    phi-interval along the band's exact solution (light: 1/b instead of E/L).
 *  - Deflection: d_in and d_out are local static-frame unit directions at the two
 *    r=1e4 crossings; delta_R = acos(d_in.d_out) compared to the exact same-radius
 *    value (equivalently oracle delta_inf minus the exact outgoing tails).
 *  - ISCO windows: "100 orbits" = 100 complete peri->peri cycles inside (2, 4 r0);
 *    "plunge within 50 orbits" = absorbed with accumulated sweep <= 100 pi.
 *  - square grid: quadtree, refine iff side > |centre|/16 (floor 2^-10); flow
 *    vector frozen at cell centre; H and tangential p conserved at edges, total
 *    reflection when the quadratic has no root.
 *  - tilt: same rings as river-m16; straight lines within a ring; at each ring
 *    crossing rotate v toward -rhat by dps = ds*sin(alpha)/(rc^2 v^2) (matter),
 *    ds*sin(alpha)/rc^2 (light, v=1); |v| kept (Newtonian-strength kicks).
 *  - Capture launches: r=100 inward (photon capture too); absorbed means r<=2.
 *
 * Band indexing: u bands are [2^(-(j+1)/m), 2^(-j/m)); LARGER u (deeper) is
 * SMALLER j.  Rings are r in [2^(j/m), 2^((j+1)/m)); larger r is larger j.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define PI 3.14159265358979323846

/* ================= oracle ports ================= */

static double ellip_k(double m) {
    double a = 1.0, g = sqrt(1.0 - m);
    for (int i = 0; i < 40; i++) {
        double a1 = (a + g) / 2.0, g1 = sqrt(a * g);
        if (fabs(a1 - g1) <= 1e-17 * a1) { a = a1; break; }
        a = a1; g = g1;
    }
    return PI / (2.0 * a);
}
static double ellip_k_minus_half_pi(double m) {
    if (m >= 0.25) return ellip_k(m) - PI / 2.0;
    double c = 1.0, mn = 1.0, sum = 0.0;
    for (int n = 1; n < 200; n++) {
        c *= (2.0 * n - 1.0) / (2.0 * n);
        mn *= m;
        double term = c * c * mn;
        sum += term;
        if (term < 1e-19 * sum) break;
    }
    return PI / 2.0 * sum;
}
/* periapsis-to-periapsis angle minus 2pi */
static double periapsis_elliptic(double p, double e) {
    double d = p - 6.0 + 2.0 * e;
    double s = sqrt(p / d);
    double s_minus_1 = (6.0 - 2.0 * e) / d / (s + 1.0);
    return 4.0 * (s * ellip_k_minus_half_pi(4.0 * e / d) + PI / 2.0 * s_minus_1);
}

static void gauss_legendre(int n, double *x, double *w) {
    for (int i = 1; i <= n; i++) {
        double xi = cos(PI * (i - 0.25) / (n + 0.5));
        double dp = 0;
        for (int it = 0; it < 100; it++) {
            double p0 = 1.0, p1 = xi;
            for (int k = 2; k <= n; k++) {
                double p2 = ((2.0 * k - 1.0) * xi * p1 - (k - 1.0) * p0) / k;
                p0 = p1; p1 = p2;
            }
            dp = (double)n * (xi * p1 - p0) / (xi * xi - 1.0);
            double dx = p1 / dp;
            xi -= dx;
            if (fabs(dx) < 1e-16) break;
        }
        x[i - 1] = xi; w[i - 1] = 2.0 / ((1.0 - xi * xi) * dp * dp);
    }
}

static double gln64_x[32], gln64_w[32], gl16_x[16], gl16_w[16];

static double light_u0(double b) {
    double u0 = 1.0 / b;
    for (int i = 0; i < 100; i++) {
        double h = 2.0 * u0 * u0 * u0 - u0 * u0 + 1.0 / (b * b);
        double dh = 6.0 * u0 * u0 - 2.0 * u0;
        double step = h / dh;
        u0 -= step;
        if (fabs(step) <= 1e-17 * u0) break;
    }
    return u0;
}
/* total deflection from infinity: 2(I - pi/2) with the root-factored integrand */
static double deflection_quadrature(double b) {
    double u0 = light_u0(b);
    double total = 0.0;
    for (int j = 0; j < 64; j++) {
        double a = (double)j / 64.0, c = (double)(j + 1) / 64.0;
        for (int k = 0; k < 32; k++) {
            double s = (a + c) / 2.0 + (c - a) / 2.0 * gln64_x[k];
            double u = u0 * (1.0 - s * s);
            double qf = u0 + u, r = 2.0 * (u * u + u * u0 + u0 * u0);
            double q = qf - r;
            total += gln64_w[k] * (c - a) / 2.0 * 4.0 * sqrt(u0) * r /
                     (sqrt(q * qf) * (sqrt(qf) + sqrt(q)));
        }
    }
    return total;
}
/* I_R = integral_0^{u_R} du/sqrt(1/b^2 - u^2 + 2u^3) */
static double light_half_sweep_to(double b, double u_R) {
    double u0 = light_u0(b);
    double sR = sqrt(1.0 - u_R / u0);
    double total = 0.0;
    for (int j = 0; j < 16; j++) {
        double a = sR + (1.0 - sR) * j / 16.0, c = sR + (1.0 - sR) * (j + 1) / 16.0;
        for (int k = 0; k < 32; k++) {
            double s = (a + c) / 2.0 + (c - a) / 2.0 * gln64_x[k];
            double u = u0 * (1.0 - s * s);
            double qf = u0 + u, r = 2.0 * (u * u + u * u0 + u0 * u0);
            double q = qf - r;
            total += gln64_w[k] * (c - a) / 2.0 * 2.0 * sqrt(u0) / sqrt(q);
        }
    }
    return total;
}

static void bound_constants(double p, double e, double *E, double *L) {
    *E = sqrt(((p - 2.0) * (p - 2.0) - 4.0 * e * e) / (p * (p - 3.0 - e * e)));
    *L = p / sqrt(p - 3.0 - e * e);
}

static double integrate_gl32(double lo, double hi, int pieces, double (*f)(double, void *), void *ctx) {
    double sum = 0.0;
    for (int j = 0; j < pieces; j++) {
        double a = lo + (hi - lo) * j / (double)pieces;
        double c = lo + (hi - lo) * (j + 1) / (double)pieces;
        for (int k = 0; k < 32; k++)
            sum += (c - a) * 0.5 * gln64_w[k] * f((a + c) * 0.5 + (c - a) * 0.5 * gln64_x[k], ctx);
    }
    return sum;
}

typedef struct { double p, e, E, L; } PerCtx;
static double per_t_chi(double chi, void *c) {
    PerCtx *q = c;
    double r = q->p / (1.0 + q->e * cos(chi));
    double dphi = sqrt(q->p / (q->p - 6.0 - 2.0 * q->e * cos(chi)));
    return dphi * r * r / q->L * q->E / (1.0 - 2.0 / r);
}
static double per_tau_chi(double chi, void *c) {
    PerCtx *q = c;
    double r = q->p / (1.0 + q->e * cos(chi));
    return sqrt(q->p / (q->p - 6.0 - 2.0 * q->e * cos(chi))) * r * r / q->L;
}
static double refine_gl(double (*f)(double, void *), void *ctx) {
    int pieces = 16;
    double v = integrate_gl32(0.0, 2.0 * PI, pieces, f, ctx);
    while (pieces < 1 << 14) {
        pieces *= 2;
        double w = integrate_gl32(0.0, 2.0 * PI, pieces, f, ctx);
        int done = fabs(w - v) <= 1e-14 * fabs(w);
        v = w;
        if (done) break;
    }
    return v;
}
static double bound_period_quad(double p, double e, double *tau_out) {
    PerCtx q = { p, e, 0, 0 };
    bound_constants(p, e, &q.E, &q.L);
    double t = refine_gl(per_t_chi, &q);
    double tau = refine_gl(per_tau_chi, &q);
    if (tau_out) *tau_out = tau;
    return t;
}

/* -------- independent RK4 cross-checks -------- */
static double periapsis_ode(double p, double e, double steps_per_rad) {
    double inv_l2 = (p - 3.0 - e * e) / (p * p);
    double h = 1.0 / steps_per_rad;
    double u = (1.0 + e) / p, v = 0.0, phi = 0.0;
    int seen_positive = 0;
    for (long i = 0; i < (long)(20.0 * PI * steps_per_rad); i++) {
        double k1u = v, k1v = inv_l2 + 3.0 * u * u - u;
        double u2 = u + h / 2.0 * k1u, u3 = u + h / 2.0 * (v + h / 2.0 * k1v);
        double k2u = v + h / 2.0 * k1v, k2v = inv_l2 + 3.0 * u2 * u2 - u2;
        double k3u = v + h / 2.0 * k2v, k3v = inv_l2 + 3.0 * u3 * u3 - u3;
        double u4 = u + h * k3u;
        double k4u = v + h * k3v, k4v = inv_l2 + 3.0 * u4 * u4 - u4;
        double u1 = u + h / 6.0 * (k1u + 2.0 * k2u + 2.0 * k3u + k4u);
        double v1 = v + h / 6.0 * (k1v + 2.0 * k2v + 2.0 * k3v + k4v);
        if (v1 > 0.0) seen_positive = 1;
        if (seen_positive && v > 0.0 && v1 <= 0.0) {
            double lo = 0.0, hi = h;
            for (int k = 0; k < 80; k++) {
                double mid = (lo + hi) / 2.0;
                double a2 = inv_l2 + 3.0 * (u + mid / 2 * k1u) * (u + mid / 2 * k1u) - (u + mid / 2 * k1u);
                double b2 = inv_l2 + 3.0 * (u + mid / 2 * k2u) * (u + mid / 2 * k2u) - (u + mid / 2 * k2u);
                double vv = v + mid / 6.0 * (k1v + 2.0 * b2 + 2.0 * b2 + k4v);
                (void)a2;
                if (vv > 0.0) lo = mid; else hi = mid;
            }
            return phi + (lo + hi) / 2.0 - 2.0 * PI;
        }
        u = u1; v = v1; phi += h;
    }
    return NAN;
}
/* midpoint-free bisection helper replaced by fine re-integration approach:
   we simply integrate with a much finer step and interpolate linearly; error is
   far below the comparison band. */
static double deflection_ode(double b, double steps_per_rad) {
    double h = 1.0 / steps_per_rad;
    double u = 0.0, v = 1.0 / b, phi = 0.0;
    for (long i = 0; i < (long)(4.0 * PI * steps_per_rad); i++) {
        double k1u = v, k1v = 3.0 * u * u - u;
        double u2 = u + h / 2.0 * k1u;
        double k2u = v + h / 2.0 * k1v, k2v = 3.0 * u2 * u2 - u2;
        double u3 = u + h / 2.0 * k2u;
        double k3u = v + h / 2.0 * k2v, k3v = 3.0 * u3 * u3 - u3;
        double u4 = u + h * k3u;
        double k4u = v + h * k3v, k4v = 3.0 * u4 * u4 - u4;
        double u1 = u + h / 6.0 * (k1u + 2.0 * k2u + 2.0 * k3u + k4u);
        double v1 = v + h / 6.0 * (k1v + 2.0 * k2v + 2.0 * k3v + k4v);
        if (phi > 1.0 && u1 <= 0.0) {
            double frac = u / (u - u1);
            return phi + frac * h - PI;
        }
        u = u1; v = v1; phi += h;
    }
    return NAN;
}
/* my independent period check: RK4 on Binet in phi carrying t */
static void period_ode(double p, double e, double *adv, double *T) {
    double E, L; bound_constants(p, e, &E, &L);
    double inv_l2 = (p - 3.0 - e * e) / (p * p);
    double h = 1.0 / 20000.0;
    double u = (1.0 + e) / p, v = 0.0, phi = 0.0, t = 0.0;
    int seen_positive = 0;
    for (long i = 0; i < (long)(20.0 * PI * 20000.0); i++) {
        double dtf = E / (L * u * u * (1.0 - 2.0 * u));
        double k1u = v, k1v = inv_l2 + 3.0 * u * u - u, k1t = dtf;
        double u2 = u + h / 2.0 * k1u;
        double k2u = v + h / 2.0 * k1v, k2v = inv_l2 + 3.0 * u2 * u2 - u2;
        double k2t = E / (L * u2 * u2 * (1.0 - 2.0 * u2));
        double u3 = u + h / 2.0 * k2u;
        double k3u = v + h / 2.0 * k2v, k3v = inv_l2 + 3.0 * u3 * u3 - u3;
        double k3t = E / (L * u3 * u3 * (1.0 - 2.0 * u3));
        double u4 = u + h * k3u;
        double k4u = v + h * k3v, k4v = inv_l2 + 3.0 * u4 * u4 - u4;
        double k4t = E / (L * u4 * u4 * (1.0 - 2.0 * u4));
        double u1 = u + h / 6.0 * (k1u + 2.0 * k2u + 2.0 * k3u + k4u);
        double v1 = v + h / 6.0 * (k1v + 2.0 * k2v + 2.0 * k3v + k4v);
        double t1 = t + h / 6.0 * (k1t + 2.0 * k2t + 2.0 * k3t + k4t);
        if (v1 > 0.0) seen_positive = 1;
        if (seen_positive && v > 0.0 && v1 <= 0.0) {
            double frac = v / (v - v1);
            *adv = phi + frac * h - 2.0 * PI;
            *T = t + frac * h;
            return;
        }
        u = u1; v = v1; phi += h; t = t1;
    }
    *adv = NAN; *T = NAN;
}

/* ================= engines ================= */

enum { EV_EDGE = 0, EV_PERI = 1, EV_APO = 2, EV_ABSORB = 3, EV_ESCAPE = 4, EV_ERR = 5 };
enum { K_BINET = 0, K_RIVER = 1, K_SQUARE = 2, K_TILT = 3 };

typedef struct {
    int kind, m, nullf;
    double E, H, L, b;
    double phi, t;
    /* binet */
    double u, v; int j;
    /* river */
    double r, pr; int sgn;
    /* square / tilt */
    double x, y, px, py, vx, vy;
    double ring_entry_x, ring_entry_y;
    double Rend, u_end;
    long last_id;
    double turn_r;
    long guard;
} Eng;

static double clampd(double x, double lo, double hi) { return x < lo ? lo : (x > hi ? hi : x); }

/* ---------- Binet: u bands [2^(-(j+1)/m), 2^(-j/m)); deeper = smaller j ---------- */

static void binet_set_band(Eng *s) {
    double m = (double)s->m;
    int j = (int)floor(m * log2(1.0 / s->u));
    while (s->u > exp2(-(double)j / m)) j--;
    while (s->u < exp2(-(double)(j + 1) / m)) j++;
    s->j = j;
}

static void binet_time(Eng *s, double c0, double w, double v, double w2, double om, double d) {
    if (s->nullf) return;
    double f = s->E / s->L, acc = 0.0;
    for (int k = 0; k < 16; k++) {
        double xi = d * 0.5 * (gl16_x[k] + 1.0);
        double uu = w2 > 0.0 ? c0 + w * cos(om * xi) + (v / om) * sin(om * xi)
                             : c0 + w * cosh(om * xi) + (v / om) * sinh(om * xi);
        acc += gl16_w[k] * f / (uu * uu * (1.0 - 2.0 * uu));
    }
    s->t += acc * d * 0.5;
}

static int binet_step(Eng *s) {
    if (++s->guard > 200000000L) return EV_ERR;
    int j = s->j;
    double m = (double)s->m;
    double uk = exp2(-(j + 0.5) / m);
    double Uhi = exp2(-(double)j / m);        /* larger-u edge (deeper side) */
    double Ulo = exp2(-(double)(j + 1) / m);  /* smaller-u edge (shallower side) */
    double w2 = 1.0 - 6.0 * uk;
    double F = s->nullf ? 0.0 : 1.0 / (s->L * s->L);
    if (fabs(w2) < 1e-13) return EV_ERR;
    double c0 = (F - 3.0 * uk * uk) / w2;
    double w = s->u - c0, v = s->v;
    double bestd = INFINITY; int bestev = EV_ERR; double bu = 0, bv = 0; int bestj = j;
    if (w2 > 0.0) {
        double om = sqrt(w2);
        double A = hypot(w, v / om);
        if (!(A > 0.0)) return EV_ERR;
        double th = atan2(-v / om, w);
        double n = ceil(th / PI - 1e-14);
        double tht = n * PI;
        while (tht <= th) { tht += PI; n += 1.0; }
        bestd = (tht - th) / om;
        bestev = (fmod(n, 2.0) == 0.0) ? EV_PERI : EV_APO;
        bu = (bestev == EV_PERI) ? c0 + A : c0 - A; bv = 0.0; bestj = j;
        double edges[2] = { Uhi, Ulo };
        int dj[2] = { -1, +1 };
        for (int ei = 0; ei < 2; ei++) {
            double cg = (edges[ei] - c0) / A;
            if (fabs(cg) < 1.0) {
                double base = acos(cg);
                double cand[2] = { base, -base };
                for (int ci = 0; ci < 2; ci++) {
                    double cnd = cand[ci];
                    double k = ceil((th - cnd) / (2.0 * PI) - 1e-14);
                    double the = cnd + k * 2.0 * PI;
                    while (the <= th) the += 2.0 * PI;
                    double d = (the - th) / om;
                    if (d < bestd) {
                        bestd = d; bestev = EV_EDGE; bu = edges[ei];
                        bv = -A * om * sin(the);
                        bestj = j + dj[ei];
                    }
                }
            }
        }
    } else {
        double om = sqrt(-w2);
        double A = (w + v / om) / 2.0, B = (w - v / om) / 2.0;
        if (A > 0.0 && B > 0.0 && B / A > 1.0) {
            double d = log(B / A) / (2.0 * om);
            if (d > 0.0 && d < bestd) {
                bestd = d; bestev = (v > 0.0) ? EV_PERI : EV_APO;
                double z = exp(om * d);
                bu = c0 + A * z + B / z; bv = 0.0; bestj = j;
            }
        }
        double edges[2] = { Uhi, Ulo };
        int dj[2] = { -1, +1 };
        for (int ei = 0; ei < 2; ei++) {
            double g = edges[ei] - c0;
            if (fabs(A) > 0.0) {
                double disc = g * g - 4.0 * A * B;
                if (disc >= 0.0) {
                    double zs[2] = { (g + sqrt(disc)) / (2.0 * A), (g - sqrt(disc)) / (2.0 * A) };
                    for (int zi = 0; zi < 2; zi++) {
                        if (zs[zi] > 1.0 + 1e-15) {
                            double d = log(zs[zi]) / om;
                            if (d > 0.0 && d < bestd) {
                                bestd = d; bestev = EV_EDGE; bu = edges[ei];
                                bv = om * (A * zs[zi] - B / zs[zi]);
                                bestj = j + dj[ei];
                            }
                        }
                    }
                }
            } else if (fabs(g) > 0.0 && B / g > 1.0) {
                double d = log(B / g) / om;
                if (d > 0.0 && d < bestd) {
                    bestd = d; bestev = EV_EDGE; bu = edges[ei];
                    bv = -om * g;
                    bestj = j + dj[ei];
                }
            }
        }
    }
    if (bestev == EV_ERR || !(bestd > 0.0) || !isfinite(bestd)) return EV_ERR;
    binet_time(s, c0, w, v, w2, (w2 > 0.0) ? sqrt(w2) : sqrt(-w2), bestd);
    s->phi += bestd;
    s->u = bu; s->v = bv; s->j = bestj;
    if (bestev == EV_PERI || bestev == EV_APO) s->turn_r = 1.0 / bu;
    if (bestev == EV_EDGE) {
        s->last_id = bestj;
        if (s->u >= 0.5) return EV_ABSORB;
        if (s->nullf && s->v < 0.0 && s->u <= s->u_end) return EV_ESCAPE;
    }
    return bestev;
}

static void binet_init_matter(Eng *s, int m, double p, double e) {
    memset(s, 0, sizeof *s);
    s->kind = K_BINET; s->m = m;
    bound_constants(p, e, &s->E, &s->L);
    s->u = (1.0 + e) / p; s->v = 0.0;
    binet_set_band(s);
    s->turn_r = 1.0 / s->u;
}
static void binet_init_null(Eng *s, int m, double b, double u0, double uend) {
    memset(s, 0, sizeof *s);
    s->kind = K_BINET; s->m = m; s->nullf = 1; s->b = b;
    s->u = u0; s->u_end = uend;
    s->v = sqrt(fmax(1.0 / (b * b) - u0 * u0 + 2.0 * u0 * u0 * u0, 0.0));
    binet_set_band(s);
}

/* ---------- River: rings r in [2^(j/m), 2^((j+1)/m)) ---------- */

static void river_consts(Eng *s, int j, double *beta, double *sb, double *a2, double *bq) {
    double rc = exp2((j + 0.5) / (double)s->m);
    *beta = -sqrt(2.0 / rc);
    *sb = 1.0 - (*beta) * (*beta);
    *a2 = s->nullf ? s->H * s->H : s->H * s->H - *sb;
    *bq = sqrt(*sb) * fabs(s->L);
}
static double river_Phi(double sb, double a, double bq, double r) {
    return acos(clampd(bq / (a * r), -1.0, 1.0)) / sqrt(sb);
}
static double river_T(double a2, double bq2, double r) {
    double v = a2 * r * r - bq2;
    return v <= 0.0 ? 0.0 : sqrt(v) / a2;
}

static void river_set_ring(Eng *s) {
    int m = s->m;
    int j = (int)floor(m * log2(s->r));
    while (s->r >= exp2((double)(j + 1) / m)) j++;
    while (s->r <= exp2((double)j / m)) j--;
    s->j = j;
}

static int river_step(Eng *s) {
    if (++s->guard > 200000000L) return EV_ERR;
    double beta, sb, a2, bq;
    river_consts(s, s->j, &beta, &sb, &a2, &bq);
    if (!(a2 > 0.0)) return EV_ERR;
    double a = sqrt(a2), bq2 = bq * bq;
    double rt = bq / a;
    double Rtarget = (s->sgn > 0) ? exp2((double)(s->j + 1) / s->m) : exp2((double)s->j / s->m);
    int turning = 0;
    double r2 = Rtarget;
    if (s->sgn < 0) { if (rt < s->r && rt >= Rtarget) { r2 = rt; turning = 1; } }
    double P1 = river_Phi(sb, a, bq, s->r), P2 = river_Phi(sb, a, bq, r2);
    double T1 = river_T(a2, bq2, s->r), T2 = river_T(a2, bq2, r2);
    double dphi = (double)s->sgn * (s->L > 0 ? 1.0 : -1.0) * (P2 - P1);
    double dt = (double)s->sgn * (s->H / sb) * (T2 - T1) - (beta / sb) * (r2 - s->r);
    s->phi += dphi; s->t += dt;
    s->r = r2;
    if (turning) {
        s->pr = -s->H * beta / sb;
        int was = s->sgn;
        s->sgn = -s->sgn;
        s->turn_r = r2;
        return (was < 0) ? EV_PERI : EV_APO;
    }
    if (Rtarget <= 2.0) return EV_ABSORB;
    if (s->sgn > 0 && Rtarget >= s->Rend) return EV_ESCAPE;
    int jn = s->sgn > 0 ? s->j + 1 : s->j - 1;
    double nbeta, nsb, na2, nbq;
    river_consts(s, jn, &nbeta, &nsb, &na2, &nbq);
    double Dn = na2 - nbq * nbq / (Rtarget * Rtarget);
    if (Dn >= 0.0 && na2 > 0.0) {
        s->j = jn;
        s->pr = (-s->H * nbeta + (double)s->sgn * sqrt(Dn)) / nsb;
        s->last_id = jn;
        return EV_EDGE;
    }
    s->sgn = -s->sgn;
    s->pr = (-s->H * beta + (double)s->sgn * sqrt(fmax(a2 - bq2 / (Rtarget * Rtarget), 0.0))) / sb;
    s->turn_r = Rtarget;
    return (s->sgn > 0) ? EV_PERI : EV_APO;
}
static void river_init_matter(Eng *s, int m, double p, double e) {
    memset(s, 0, sizeof *s);
    s->kind = K_RIVER; s->m = m;
    bound_constants(p, e, &s->E, &s->L);
    s->H = s->E;
    s->Rend = 1e9;
    s->r = p / (1.0 - e);
    river_set_ring(s);
    /* if the geometric ring's frozen flow forbids r (no real p_r), walk to the
       next deeper ring that admits it; the first descent leg then carries that
       ring's flow (a one-time smear before the first periapsis) */
    while (s->j > -100000) {
        double bb, ssb, aa2, bbq;
        river_consts(s, s->j, &bb, &ssb, &aa2, &bbq);
        if (aa2 > 0.0 && aa2 - bbq * bbq / (s->r * s->r) >= 0.0) break;
        s->j--;
    }
    s->sgn = -1;
    double beta, sb, a2, bq;
    river_consts(s, s->j, &beta, &sb, &a2, &bq);
    double D = a2 - bq * bq / (s->r * s->r);
    s->pr = (-s->H * beta - sqrt(fmax(D, 0.0))) / sb;
}
static void river_init_null(Eng *s, int m, double b, double r0, double Rend) {
    memset(s, 0, sizeof *s);
    s->kind = K_RIVER; s->m = m; s->nullf = 1; s->b = b; s->L = b;
    s->Rend = Rend;
    double beta = -sqrt(2.0 / r0), sb = 1.0 - beta * beta;
    double D = 1.0 - sb * b * b / (r0 * r0);
    double pr = (-beta - sqrt(fmax(D, 0.0))) / sb;
    double pmod = hypot(pr, b / r0);
    s->r = r0; s->sgn = -1;
    river_set_ring(s);
    double beta2, sb2, a2, bq;
    river_consts(s, s->j, &beta2, &sb2, &a2, &bq);
    s->H = pmod + beta2 * pr;
}
static void river_init_matter_rL(Eng *s, int m, double E, double L, double r0, double Rend) {
    memset(s, 0, sizeof *s);
    s->kind = K_RIVER; s->m = m;
    s->E = E; s->L = L; s->Rend = Rend;
    double beta = -sqrt(2.0 / r0), sb = 1.0 - beta * beta;
    double D = E * E - sb * (1.0 + L * L / (r0 * r0));
    double pr = (-beta * E - sqrt(fmax(D, 0.0))) / sb;
    double pmod = sqrt(1.0 + pr * pr + (L / r0) * (L / r0));
    s->r = r0; s->sgn = -1;
    river_set_ring(s);
    double beta2, sb2, a2, bq;
    river_consts(s, s->j, &beta2, &sb2, &a2, &bq);
    s->H = pmod + beta2 * pr;
}

/* ---------- Square ---------- */

static void square_flow(double x, double y, double *bx, double *by, int *lvl, long *ci, long *cj) {
    double x0 = -8192.0, y0 = -8192.0, s = 16384.0;
    int lv = 0;
    while (1) {
        double cx = x0 + s / 2.0, cy = y0 + s / 2.0, rc = hypot(cx, cy);
        if (!(s > rc / 16.0 && s > 1.0 / 1024.0)) break;
        s *= 0.5; lv++;
        long i = (long)floor((x - x0) / s), j = (long)floor((y - y0) / s);
        if (i < 0) i = 0; if (i > 1) i = 1;
        if (j < 0) j = 0; if (j > 1) j = 1;
        x0 += (double)i * s; y0 += (double)j * s;
    }
    double cx = x0 + s / 2.0, cy = y0 + s / 2.0, rc = hypot(cx, cy);
    double mag = sqrt(2.0 / rc);
    if (bx) *bx = -mag * cx / rc;
    if (by) *by = -mag * cy / rc;
    if (lvl) *lvl = lv;
    if (ci) *ci = (long)floor(x0 / s);
    if (cj) *cj = (long)floor(y0 / s);
}

/* static-frame (vr, vphi) at (x,y) -> cell-rain momentum, sets H */
static void square_p_from_static(Eng *s, double x, double y, double vr, double vphi, int nullf) {
    double bx, by;
    square_flow(x, y, &bx, &by, NULL, NULL, NULL);
    double rn = hypot(x, y), rx = x / rn, ry = y / rn;
    double svx = vr * rx - vphi * ry, svy = vr * ry + vphi * rx;
    double w = hypot(bx, by);
    double ux = w > 0 ? bx / w : 0.0, uy = w > 0 ? by / w : 0.0;
    double vpar = svx * ux + svy * uy;
    double perpx = svx - vpar * ux, perpy = svy - vpar * uy;
    double vp = (vpar - w) / (1.0 - w * vpar);
    double perpsc = sqrt(1.0 - w * w) / (1.0 - w * vpar);
    double vx = vp * ux + perpx * perpsc, vy = vp * uy + perpy * perpsc;
    double sp2 = vx * vx + vy * vy;
    if (nullf) {
        double inv = 1.0 / sqrt(sp2);
        s->px = vx * inv; s->py = vy * inv;
    } else {
        double gam = 1.0 / sqrt(fmax(1.0 - sp2, 1e-15));
        s->px = gam * vx; s->py = gam * vy;
    }
    s->H = (nullf ? hypot(s->px, s->py) : sqrt(1.0 + s->px * s->px + s->py * s->py)) + bx * s->px + by * s->py;
}

static int square_step(Eng *s) {
    if (++s->guard > 50000000L) return EV_ERR;
    double bx, by;
    int lvl; long ci, cj;
    square_flow(s->x, s->y, &bx, &by, &lvl, &ci, &cj);
    double s0 = exp2(14.0 - lvl);
    double x0 = (double)ci * s0, y0 = (double)cj * s0;
    double gam = s->nullf ? hypot(s->px, s->py) : sqrt(1.0 + s->px * s->px + s->py * s->py);
    double Vx = s->px / gam + bx, Vy = s->py / gam + by;
    double A = Vx * Vx + Vy * Vy;
    if (!(A > 0.0)) return EV_ERR;
    double B = 2.0 * (s->x * Vx + s->y * Vy);
    double tx = Vx > 0 ? (x0 + s0 - s->x) / Vx : (Vx < 0 ? (x0 - s->x) / Vx : INFINITY);
    double ty = Vy > 0 ? (y0 + s0 - s->y) / Vy : (Vy < 0 ? (y0 - s->y) / Vy : INFINITY);
    double te = fmin(tx, ty);
    if (!(te > 0.0) || !isfinite(te)) return EV_ERR;
    /* internal peri turning (r^2 is a upward parabola along the segment) */
    if (B < 0.0) {
        double tt = -B / (2.0 * A);
        if (tt > 0.0 && tt < te) {
            double r2 = (s->x * s->x + s->y * s->y) - B * B / (4.0 * A);
            double dphi = atan2(s->x * (s->y + Vy * tt) - s->y * (s->x + Vx * tt),
                                s->x * (s->x + Vx * tt) + s->y * (s->y + Vy * tt));
            s->phi += dphi; s->t += tt;
            s->x += Vx * tt; s->y += Vy * tt;
            s->turn_r = sqrt(fmax(r2, 0.0));
            return EV_PERI;
        }
    }
    /* capture r=2 on the segment */
    {
        double C = s->x * s->x + s->y * s->y - 4.0;
        double disc = B * B - 4.0 * A * C;
        if (disc >= 0.0) {
            double tq = (-B - sqrt(disc)) / (2.0 * A);
            if (tq > 0.0 && tq < te) return EV_ABSORB;
        }
    }
    /* escape r=Rend (outbound only) */
    if (B > 0.0) {
        double C = s->x * s->x + s->y * s->y - s->Rend * s->Rend;
        double disc = B * B - 4.0 * A * C;
        if (disc >= 0.0) {
            double tq = (-B + sqrt(disc)) / (2.0 * A);
            if (tq > 0.0 && tq < te) return EV_ESCAPE;
        }
    }
    double nx = s->x + Vx * te, ny = s->y + Vy * te;
    double dphi = atan2(s->x * ny - s->y * nx, s->x * nx + s->y * ny);
    s->phi += dphi; s->t += te;
    s->x = nx; s->y = ny;
    /* refract across the edge: conserve H and tangential p */
    int axis_x = (tx <= ty);
    double nbx, nby;
    double eps = 1e-6 * s0;
    double qx = s->x + (axis_x ? (Vx > 0 ? eps : -eps) : 0.0);
    double qy = s->y + (!axis_x ? (Vy > 0 ? eps : -eps) : 0.0);
    square_flow(qx, qy, &nbx, &nby, NULL, NULL, NULL);
    double pn_old = axis_x ? s->px : s->py;
    double ptan = axis_x ? s->py : s->px;
    double bn_par = axis_x ? nbx : nby;
    double bn_perp = axis_x ? nby : nbx;
    double Aq = 1.0 - bn_par * bn_par;
    double rhs = s->H - bn_perp * ptan;
    double Bq = 2.0 * bn_par * rhs;
    double Cq = (s->nullf ? ptan * ptan : 1.0 + ptan * ptan) - rhs * rhs;
    double newp = 0; int ok = 0;
    if (fabs(Aq) > 1e-14) {
        double dd = Bq * Bq - 4.0 * Aq * Cq;
        if (dd >= 0.0) {
            double r1 = (-Bq + sqrt(dd)) / (2.0 * Aq), r2 = (-Bq - sqrt(dd)) / (2.0 * Aq);
            newp = (fabs(r1 - pn_old) <= fabs(r2 - pn_old)) ? r1 : r2;
            ok = 1;
        }
    } else if (fabs(Bq) > 1e-14) {
        newp = -Cq / Bq; ok = 1;
    }
    double vxr_old = s->x * Vx + s->y * Vy;
    if (!ok) newp = -pn_old; /* total reflection */
    if (axis_x) s->px = newp; else s->py = newp;
    double gam2 = s->nullf ? hypot(s->px, s->py) : sqrt(1.0 + s->px * s->px + s->py * s->py);
    double nVx = s->px / gam2 + nbx, nVy = s->py / gam2 + nby;
    double vxr_new = s->x * nVx + s->y * nVy;
    int nlvl; long nci, ncj;
    square_flow(s->x + nVx * 1e-9, s->y + nVy * 1e-9, NULL, NULL, &nlvl, &nci, &ncj);
    s->last_id = (long)nlvl * 0x9E37797F + nci * 852049751L + ncj * 347470113L;
    if (vxr_old < 0.0 && vxr_new > 0.0) { s->turn_r = hypot(s->x, s->y); return EV_PERI; }
    if (vxr_old > 0.0 && vxr_new < 0.0) { s->turn_r = hypot(s->x, s->y); return EV_APO; }
    return EV_EDGE;
}

/* ---------- Tilt ---------- */

static int tilt_step(Eng *s) {
    if (++s->guard > 50000000L) return EV_ERR;
    int m = 16;
    int j = s->j;
    double vx = s->vx, vy = s->vy, V = hypot(vx, vy);
    if (!(V > 0.0)) return EV_ERR;
    double A = V * V, B = 2.0 * (s->x * vx + s->y * vy);
    double curr2 = s->x * s->x + s->y * s->y;
    double te = INFINITY; int dirn = 0;
    double edges[2] = { exp2((double)j / m), exp2((double)(j + 1) / m) };
    for (int ei = 0; ei < 2; ei++) {
        double C = curr2 - edges[ei] * edges[ei];
        double disc = B * B - 4.0 * A * C;
        if (disc >= 0.0) {
            double tq = (-B + sqrt(disc)) / (2.0 * A);
            if (tq > 1e-13 && tq < te) { te = tq; dirn = (ei == 0) ? -1 : +1; }
        }
    }
    if (!isfinite(te)) return EV_ERR;
    if (B < 0.0) {
        double tt = -B / (2.0 * A);
        if (tt > 0.0 && tt < te) {
            double r2 = curr2 - B * B / (4.0 * A);
            double dphi = atan2(s->x * (s->y + vy * tt) - s->y * (s->x + vx * tt),
                                s->x * (s->x + vx * tt) + s->y * (s->y + vy * tt));
            s->phi += dphi; s->t += tt / V;
            s->x += vx * tt; s->y += vy * tt;
            s->turn_r = sqrt(fmax(r2, 0.0));
            return EV_PERI;
        }
    }
    {
        double C = curr2 - 4.0;
        double disc = B * B - 4.0 * A * C;
        if (disc >= 0.0) {
            double tq = (-B - sqrt(disc)) / (2.0 * A);
            if (tq > 0.0 && tq < te) return EV_ABSORB;
        }
    }
    if (s->Rend > 0.0 && B > 0.0) {
        double C = curr2 - s->Rend * s->Rend;
        double disc = B * B - 4.0 * A * C;
        if (disc >= 0.0) {
            double tq = (-B + sqrt(disc)) / (2.0 * A);
            if (tq > 0.0 && tq < te) return EV_ESCAPE;
        }
    }
    double nx = s->x + vx * te, ny = s->y + vy * te;
    double dphi = atan2(s->x * ny - s->y * nx, s->x * nx + s->y * ny);
    s->phi += dphi; s->t += te;
    s->x = nx; s->y = ny;
    double dsring = hypot(s->x - s->ring_entry_x, s->y - s->ring_entry_y);
    s->ring_entry_x = s->x; s->ring_entry_y = s->y;
    double rc = exp2((j + 0.5) / (double)m);
    double rn = hypot(s->x, s->y);
    double sinalpha = fabs(s->x * vy - s->y * vx) / (rn * V);
    double dps = s->nullf ? dsring * sinalpha / (rc * rc)
                          : dsring * sinalpha / (rc * rc * V * V);
    if (dps > 0.5) dps = 0.5;
    double dmagx = -s->x / rn, dmagy = -s->y / rn;
    double crossz = vx * dmagy - vy * dmagx;
    double dotz = vx * dmagx + vy * dmagy;
    double sg = (atan2(crossz, dotz) >= 0.0) ? 1.0 : -1.0;
    double cd = cos(dps), sd = sin(dps) * sg;
    double nvx = vx * cd - vy * sd, nvy = vx * sd + vy * cd;
    double nvn = hypot(nvx, nvy);
    s->vx = nvx / nvn * V; s->vy = nvy / nvn * V;
    double srbefore = (s->x - vx * te) * vx + (s->y - vy * te) * vy;
    double srafter = s->x * s->vx + s->y * s->vy;
    s->j = j + dirn;
    s->last_id = s->j;
    if (srbefore < 0.0 && srafter >= 0.0) { s->turn_r = rn; return EV_PERI; }
    if (srbefore > 0.0 && srafter <= 0.0) { s->turn_r = rn; return EV_APO; }
    return EV_EDGE;
}

static void tilt_set_ring(Eng *s) {
    s->j = (int)floor(16.0 * log2(hypot(s->x, s->y)));
    while (hypot(s->x, s->y) >= exp2((double)(s->j + 1) / 16.0)) s->j++;
    while (hypot(s->x, s->y) <= exp2((double)s->j / 16.0)) s->j--;
}

/* ================= drivers ================= */

static int eng_step(Eng *s) {
    switch (s->kind) {
        case K_BINET: return binet_step(s);
        case K_RIVER: return river_step(s);
        case K_SQUARE: return square_step(s);
        default: return tilt_step(s);
    }
}
static double eng_r(Eng *s) {
    if (s->kind == K_BINET) return 1.0 / s->u;
    if (s->kind == K_RIVER) return s->r;
    return hypot(s->x, s->y);
}
static void eng_trace_pt(Eng *s, FILE *f) {
    if (s->kind == K_BINET) fprintf(f, "%.17g %.17g\n", cos(s->phi) / s->u, sin(s->phi) / s->u);
    else if (s->kind == K_RIVER) fprintf(f, "%.17g %.17g\n", s->r * cos(s->phi), s->r * sin(s->phi));
    else fprintf(f, "%.17g %.17g\n", s->x, s->y);
}

#define SEQCAP 8192

typedef struct {
    int ok, shape_ok, repeat_ok;
    double adv, T, cross;
} BoundOut;

static void sim_bound(Eng *e, int ncycles, BoundOut *bo, FILE *trace) {
    long seq1[SEQCAP], seq2[SEQCAP];
    int n1 = 0, n2 = 0, use2 = 0;
    double dphi1 = 0, dt1 = 0, rperi1 = 0, rapo1 = 0;
    int have_apo1 = 0;
    int nperi = (e->kind == K_BINET) ? 1 : 0;
    int cyc = 0;
    double phi_prev = 0, t_prev = 0;
    if (nperi == 1) { rperi1 = e->turn_r; phi_prev = 0; t_prev = 0; }
    bo->ok = 0; bo->shape_ok = 1; bo->repeat_ok = 1;
    bo->adv = NAN; bo->T = NAN; bo->cross = NAN;
    while (cyc < ncycles) {
        if (e->guard > 40000000L) return;
        int ev = eng_step(e);
        if (ev == EV_ERR || ev == EV_ABSORB || ev == EV_ESCAPE) return;
        if (trace) eng_trace_pt(e, trace);
        if (ev == EV_EDGE) {
            if (use2 == 1) { if (n2 < SEQCAP) seq2[n2++] = e->last_id; }
            else if (use2 == 0 && nperi >= 1) { if (n1 < SEQCAP) seq1[n1++] = e->last_id; }
        }
        if (ev == EV_APO && nperi >= 1) {
            if (!have_apo1) { rapo1 = e->turn_r; have_apo1 = 1; }
            else if (fabs(e->turn_r / rapo1 - 1.0) > 0.01) bo->shape_ok = 0;
        }
        if (ev == EV_PERI) {
            nperi++;
            if (nperi == 1) { rperi1 = e->turn_r; phi_prev = e->phi; t_prev = e->t; continue; }
            cyc = nperi - 1;
            double dphi = e->phi - phi_prev, dt = e->t - t_prev;
            phi_prev = e->phi; t_prev = e->t;
            if (cyc == 1) {
                dphi1 = dphi; dt1 = dt;
                bo->adv = dphi - 2.0 * PI; bo->T = dt;
            } else {
                if (fabs(dphi - dphi1) > 1e-12 * fabs(dphi1) || fabs(dt - dt1) > 1e-12 * fabs(dt1)) bo->repeat_ok = 0;
            }
            if (fabs(e->turn_r / rperi1 - 1.0) > 0.01) bo->shape_ok = 0;
            if (ncycles > 1) {
                if (use2 == 0 && cyc == 1) use2 = 1;
                else if (use2 == 1 && cyc == 2) {
                    if (n2 != n1) bo->repeat_ok = 0;
                    else for (int i = 0; i < n2; i++) if (seq1[i] != seq2[i]) { bo->repeat_ok = 0; break; }
                    use2 = 2;
                }
            }
            if (ncycles == 1 && cyc >= 1) break;
        }
    }
    bo->ok = 1;
    bo->cross = (ncycles > 1) ? n2 : n1;
}

static int sim_light(Eng *e, double b, double *delta_R, double *sweep) {
    double uR = 1.0e-4, R = 1.0e4;
    double alpha = asin(clampd(b * uR * sqrt(1.0 - 2.0 * uR), -1.0, 1.0));
    double dinx = -cos(alpha), diny = sin(alpha);
    long maxev = 20000000L;
    while (e->guard < maxev) {
        int ev = eng_step(e);
        if (ev == EV_ERR || ev == EV_ABSORB) return 0;
        if (ev == EV_ESCAPE) {
            double dox, doy;
            if (e->kind == K_BINET) {
                double n = sqrt(e->u * e->u + e->v * e->v);
                double a = -e->v / n, c = e->u / n;
                double cp = cos(e->phi), sp = sin(e->phi);
                dox = a * cp - c * sp; doy = a * sp + c * cp;
            } else if (e->kind == K_RIVER) {
                double rc = exp2((e->j + 0.5) / (double)e->m);
                double br = -sqrt(2.0 / rc);
                double pmod = e->H - br * e->pr;
                double vrr = e->pr / pmod, vpp = (e->L / R) / pmod;
                double w = -sqrt(2.0 / R);
                double vsr = (vrr + w) / (1.0 + w * vrr);
                double vsp = vpp * sqrt(1.0 - w * w) / (1.0 + w * vrr);
                double cp = cos(e->phi), sp = sin(e->phi);
                dox = vsr * cp - vsp * sp; doy = vsr * sp + vsp * cp;
            } else if (e->kind == K_SQUARE) {
                double pm = hypot(e->px, e->py);
                double vrr = (e->px * e->x + e->py * e->y) / (R * pm);
                double vpp = (e->px * (-e->y) + e->py * e->x) / (R * pm);
                double w = -sqrt(2.0 / R);
                double vsr = (vrr + w) / (1.0 + w * vrr);
                double vsp = vpp * sqrt(1.0 - w * w) / (1.0 + w * vrr);
                double cp = cos(e->phi), sp = sin(e->phi);
                dox = vsr * cp - vsp * sp; doy = vsr * sp + vsp * cp;
            } else {
                dox = e->vx / hypot(e->vx, e->vy); doy = e->vy / hypot(e->vx, e->vy);
            }
            *delta_R = acos(clampd(dinx * dox + diny * doy, -1.0, 1.0));
            *sweep = e->phi;
            return 1;
        }
    }
    return 0;
}

static void trace_light(Eng *e, FILE *f) {
    long maxev = 20000000L;
    eng_trace_pt(e, f);
    while (e->guard < maxev) {
        int ev = eng_step(e);
        if (ev == EV_ERR) break;
        eng_trace_pt(e, f);
        if (ev == EV_ABSORB || ev == EV_ESCAPE) break;
    }
}

static int sim_absorb(Eng *e) {
    long maxev = 20000000L;
    while (e->guard < maxev) {
        int ev = eng_step(e);
        if (ev == EV_ABSORB) return 1;
        if (ev == EV_ESCAPE) return 0;
        if (ev == EV_ERR) return -1;
    }
    return -1;
}

static int sim_isco_A(Eng *e, double r0, int ncycles) {
    int nperi = (e->kind == K_BINET) ? 1 : 0;
    long maxev = 200000000L;
    while (nperi - (e->kind == K_BINET ? 1 : 0) < ncycles) {
        if (e->guard > maxev) return 0;
        int ev = eng_step(e);
        if (ev == EV_ERR || ev == EV_ABSORB || ev == EV_ESCAPE) return 0;
        if (eng_r(e) > 4.0 * r0) return 0;
        if (ev == EV_PERI) nperi++;
    }
    return 1;
}
static int sim_isco_B(Eng *e) {
    long maxev = 200000000L;
    while (e->phi <= 100.0 * PI) {
        if (e->guard > maxev) return 0;
        int ev = eng_step(e);
        if (ev == EV_ABSORB) return 1;
        if (ev == EV_ERR || ev == EV_ESCAPE) return 0;
    }
    return 0;
}

/* ================= constructors ================= */

static void eng_init_bound(Eng *e, int kind, int m, double p, double ecc) {
    switch (kind) {
        case K_BINET: binet_init_matter(e, m, p, ecc); break;
        case K_RIVER: river_init_matter(e, m, p, ecc); break;
        case K_SQUARE: {
            memset(e, 0, sizeof *e); e->kind = K_SQUARE; e->Rend = 1e9;
            double E, L; bound_constants(p, ecc, &E, &L);
            e->E = E; e->L = L;
            double ra = p / (1.0 - ecc);
            e->x = ra; e->y = 0.0;
            double vphi = L * sqrt(1.0 - 2.0 / ra) / (ra * E);
            square_p_from_static(e, e->x, e->y, 0.0, vphi, 0);
            break; }
        default: {
            memset(e, 0, sizeof *e); e->kind = K_TILT; e->Rend = 1e9; e->m = 16;
            double E, L; bound_constants(p, ecc, &E, &L);
            double ra = p / (1.0 - ecc);
            double vphi = L * sqrt(1.0 - 2.0 / ra) / (ra * E);
            e->vx = 0.0; e->vy = vphi;
            e->x = ra; e->y = 0.0;
            tilt_set_ring(e);
            e->ring_entry_x = e->x; e->ring_entry_y = e->y;
            break; }
    }
}

static void eng_init_light(Eng *e, int kind, int m, double b) {
    double R = 1e4;
    double uR = 1e-4;
    double alpha = asin(clampd(b * uR * sqrt(1.0 - 2.0 * uR), -1.0, 1.0));
    switch (kind) {
        case K_BINET: binet_init_null(e, m, b, uR, uR); break;
        case K_RIVER: river_init_null(e, m, b, R, R); break;
        case K_SQUARE: {
            memset(e, 0, sizeof *e); e->kind = K_SQUARE; e->nullf = 1; e->Rend = R;
            double beta = -sqrt(2.0 / R), sb = 1.0 - beta * beta;
            double D = 1.0 - sb * b * b / (R * R);
            double pr = (-beta - sqrt(fmax(D, 0.0))) / sb;
            e->x = R; e->y = 0.0;
            double bx, by; square_flow(e->x, e->y, &bx, &by, NULL, NULL, NULL);
            e->px = pr; e->py = b / R;
            e->H = hypot(e->px, e->py) + bx * e->px + by * e->py;
            break; }
        default: {
            memset(e, 0, sizeof *e); e->kind = K_TILT; e->nullf = 1; e->Rend = R; e->m = 16;
            e->vx = -cos(alpha); e->vy = sin(alpha);
            e->x = R; e->y = 0.0;
            tilt_set_ring(e);
            e->ring_entry_x = e->x; e->ring_entry_y = e->y;
            break; }
    }
}

static void eng_init_capture_matter(Eng *e, int kind, int m, double L) {
    double r0 = 100.0, E = 1.0;
    switch (kind) {
        case K_BINET: {
            memset(e, 0, sizeof *e); e->kind = K_BINET; e->m = m;
            e->E = E; e->L = L; e->u_end = 1.0 / r0;
            e->u = 1.0 / r0;
            double D = E * E - (1.0 - 2.0 * e->u) * (1.0 + L * L * e->u * e->u);
            e->v = sqrt(fmax(D, 0.0)) / L;
            binet_set_band(e);
            break; }
        case K_RIVER: river_init_matter_rL(e, m, E, L, r0, r0); break;
        case K_SQUARE: {
            memset(e, 0, sizeof *e); e->kind = K_SQUARE; e->Rend = r0;
            e->E = E; e->L = L;
            double gam = 1.0 / sqrt(1.0 - 2.0 / r0);
            double vphi = L * sqrt(1.0 - 2.0 / r0) / (r0 * E);
            double v2 = 1.0 - 1.0 / (gam * gam);
            double vr = -sqrt(fmax(v2 - vphi * vphi, 0.0));
            e->x = r0; e->y = 0.0;
            square_p_from_static(e, e->x, e->y, vr, vphi, 0);
            break; }
        default: {
            memset(e, 0, sizeof *e); e->kind = K_TILT; e->Rend = r0; e->m = 16;
            e->E = E; e->L = L;
            double gam = 1.0 / sqrt(1.0 - 2.0 / r0);
            double vphi = L * sqrt(1.0 - 2.0 / r0) / (r0 * E);
            double v2 = 1.0 - 1.0 / (gam * gam);
            double vr = -sqrt(fmax(v2 - vphi * vphi, 0.0));
            double sp = hypot(vr, vphi);
            e->vx = vr / sp; e->vy = vphi / sp;
            e->x = r0; e->y = 0.0;
            tilt_set_ring(e);
            e->ring_entry_x = e->x; e->ring_entry_y = e->y;
            break; }
    }
}

static void eng_init_capture_photon(Eng *e, int kind, int m, double b) {
    double r0 = 100.0;
    double u0 = 1.0 / r0;
    double alpha = asin(clampd(b * u0 * sqrt(1.0 - 2.0 * u0), -1.0, 1.0));
    switch (kind) {
        case K_BINET: binet_init_null(e, m, b, u0, u0); break;
        case K_RIVER: river_init_null(e, m, b, r0, r0); break;
        case K_SQUARE: {
            memset(e, 0, sizeof *e); e->kind = K_SQUARE; e->nullf = 1; e->Rend = r0;
            double beta = -sqrt(2.0 / r0), sb = 1.0 - beta * beta;
            double D = 1.0 - sb * b * b / (r0 * r0);
            double pr = (-beta - sqrt(fmax(D, 0.0))) / sb;
            e->x = r0; e->y = 0.0;
            double bx, by; square_flow(e->x, e->y, &bx, &by, NULL, NULL, NULL);
            e->px = pr; e->py = b / r0;
            e->H = hypot(e->px, e->py) + bx * e->px + by * e->py;
            break; }
        default: {
            memset(e, 0, sizeof *e); e->kind = K_TILT; e->nullf = 1; e->Rend = r0; e->m = 16;
            e->vx = -cos(alpha); e->vy = sin(alpha);
            e->x = r0; e->y = 0.0;
            tilt_set_ring(e);
            e->ring_entry_x = e->x; e->ring_entry_y = e->y;
            break; }
    }
}

static void eng_init_isco(Eng *e, int kind, int m, double r0, double L) {
    double E = sqrt((1.0 - 2.0 / r0) * (1.0 + L * L / (r0 * r0)));
    switch (kind) {
        case K_BINET: {
            memset(e, 0, sizeof *e); e->kind = K_BINET; e->m = m;
            e->E = E; e->L = L;
            e->u = 1.0 / r0; e->v = 0.0;
            binet_set_band(e);
            e->turn_r = r0;
            break; }
        case K_RIVER: {
            memset(e, 0, sizeof *e); e->kind = K_RIVER; e->m = m;
            e->E = E; e->L = L; e->H = E; e->Rend = 1e9;
            e->r = r0; e->sgn = -1;
            river_set_ring(e);
            while (e->j > -100000) {
                double bb, ssb, aa2, bbq;
                river_consts(e, e->j, &bb, &ssb, &aa2, &bbq);
                if (aa2 > 0.0 && aa2 - bbq * bbq / (r0 * r0) >= 0.0) break;
                e->j--;
            }
            double beta, sb, a2, bq;
            river_consts(e, e->j, &beta, &sb, &a2, &bq);
            double D = a2 - bq * bq / (r0 * r0);
            e->pr = (-e->H * beta - sqrt(fmax(D, 0.0))) / sb;
            break; }
        case K_SQUARE: {
            memset(e, 0, sizeof *e); e->kind = K_SQUARE; e->Rend = 1e9;
            e->E = E; e->L = L;
            double vphi = L * sqrt(1.0 - 2.0 / r0) / (r0 * E);
            e->x = r0; e->y = 0.0;
            square_p_from_static(e, e->x, e->y, 0.0, vphi, 0);
            break; }
        default: {
            memset(e, 0, sizeof *e); e->kind = K_TILT; e->Rend = 1e9; e->m = 16;
            e->E = E; e->L = L;
            double vphi = L * sqrt(1.0 - 2.0 / r0) / (r0 * E);
            e->vx = 0.0; e->vy = vphi;
            e->x = r0; e->y = 0.0;
            tilt_set_ring(e);
            e->ring_entry_x = e->x; e->ring_entry_y = e->y;
            break; }
    }
}

/* exact GR reference traces (RK4 on the exact equations) */
static void exact_orbit_trace(double p, double e, int ncycles, FILE *f) {
    double inv_l2 = (p - 3.0 - e * e) / (p * p);
    double u = (1.0 + e) / p, v = 0.0, phi = 0.0;
    double dphitot = ncycles * (2.0 * PI + periapsis_elliptic(p, e));
    double h = dphitot / 6000.0;
    for (long i = 0; i <= 6000; i++) {
        if (i % 10 == 0) fprintf(f, "%.17g %.17g\n", cos(phi) / u, sin(phi) / u);
        double k1u = v, k1v = inv_l2 + 3.0 * u * u - u;
        double u2 = u + h / 2 * k1u;
        double k2u = v + h / 2 * k1v, k2v = inv_l2 + 3.0 * u2 * u2 - u2;
        double u3 = u + h / 2 * k2u;
        double k3u = v + h / 2 * k2v, k3v = inv_l2 + 3.0 * u3 * u3 - u3;
        double u4 = u + h * k3u;
        double k4u = v + h * k3v, k4v = inv_l2 + 3.0 * u4 * u4 - u4;
        u += h / 6 * (k1u + 2 * k2u + 2 * k3u + k4u);
        v += h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v);
        phi += h;
    }
}
static void exact_light_trace(double b, FILE *f) {
    double u = 1e-4, v = sqrt(1.0 / (b * b) - 1e-8 + 2e-12), phi = 0.0;
    double h = 1e-4;
    for (long n = 0; n < 4000000; n++) {
        if (n % 150 == 0) fprintf(f, "%.17g %.17g\n", cos(phi) / u, sin(phi) / u);
        double k1u = v, k1v = 3.0 * u * u - u;
        double u2 = u + h / 2 * k1u;
        double k2u = v + h / 2 * k1v, k2v = 3.0 * u2 * u2 - u2;
        double u3 = u + h / 2 * k2u;
        double k3u = v + h / 2 * k2v, k3v = 3.0 * u3 * u3 - u3;
        double u4 = u + h * k3u;
        double k4u = v + h * k3v, k4v = 3.0 * u4 * u4 - u4;
        u += h / 6 * (k1u + 2 * k2u + 2 * k3u + k4u);
        v += h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v);
        phi += h;
        if (v < 0.0 && u <= 1e-4) { fprintf(f, "%.17g %.17g\n", cos(phi) / u, sin(phi) / u); break; }
        if (u > 0.5) { fprintf(f, "%.17g %.17g\n", cos(phi) / u, sin(phi) / u); break; }
    }
}

/* ================= main ================= */

int main(void) {
    gauss_legendre(32, gln64_x, gln64_w);
    gauss_legendre(16, gl16_x, gl16_w);

    {
        FILE *f = fopen("oracle_check.txt", "w");
        double maxrel_p = 0, maxrel_d = 0, maxrel_T = 0;
        double pcs[5][2] = { {20,0.2},{30,0.5},{100,0.2},{1000,0.5},{10000,0.2} };
        for (int i = 0; i < 5; i++) {
            double p = pcs[i][0], e = pcs[i][1];
            double a1 = periapsis_elliptic(p, e), a2 = periapsis_ode(p, e, 40000.0);
            double tau, T1 = bound_period_quad(p, e, &tau);
            double a3, T2; period_ode(p, e, &a3, &T2);
            double r1 = fabs(a1 - a2) / fabs(a1), r2 = fabs(T1 - T2) / fabs(T1);
            double r3 = fabs(a1 - a3) / fabs(a1);
            if (r1 > maxrel_p) maxrel_p = r1;
            if (r2 > maxrel_T) maxrel_T = r2;
            if (r3 > maxrel_p) maxrel_p = r3;
            fprintf(f, "period p=%g e=%g ellip=%.15g ode=%.15g rel=%.3g odeT=%.15g relA=%.3g | Tquad=%.15g Tode=%.15g rel=%.3g tau=%.15g\n",
                    p, e, a1, a2, r1, a3, r3, T1, T2, r2, tau);
        }
        double bs[5] = { 10.0, 30.0, 100.0, 300.0, 1000.0 };
        for (int i = 0; i < 5; i++) {
            double d1 = deflection_quadrature(bs[i]), d2 = deflection_ode(bs[i], 40000.0);
            double r = fabs(d1 - d2) / fabs(d1);
            if (r > maxrel_d) maxrel_d = r;
            fprintf(f, "defl b=%g quad=%.15g ode=%.15g rel=%.3g\n", bs[i], d1, d2, r);
        }
        fprintf(f, "series check p=1000 e=0.5: ellip=%.15g series=%.15g\n",
                periapsis_elliptic(1000, 0.5),
                6 * PI / 1000.0 * (1.0 + (18.0 + 0.25) / (4.0 * 1000.0)));
        fprintf(f, "series check b=1000: quad=%.15g series=%.15g\n",
                deflection_quadrature(1000.0), 4.0 / 1000.0 + 15 * PI / (4.0 * 1000.0 * 1000.0));
        fprintf(f, "max rel: periapsis %.3g deflection %.3g period %.3g\n", maxrel_p, maxrel_d, maxrel_T);
        fclose(f);
        printf("oracle check: max rel (periapsis %.2g, deflection %.2g, period %.2g)\n", maxrel_p, maxrel_d, maxrel_T);
    }

    double bp[256], be[256], gb[64];
    int nb = 0, ng = 0;
    {
        FILE *f = fopen("seeds.txt", "r");
        char line[256];
        while (fgets(line, sizeof line, f)) {
            if (line[0] == 'B') { sscanf(line + 2, "%lf %lf", &bp[nb], &be[nb]); nb++; }
            else if (line[0] == 'G') { sscanf(line + 2, "%lf", &gb[ng]); ng++; }
        }
        fclose(f);
    }
    printf("seeds: %d bound %d light\n", nb, ng);

    {
        FILE *f = fopen("oracle_light.txt", "w");
        double uR = 1e-4;
        for (int i = 0; i < ng; i++) {
            double b = gb[i];
            double dinf = deflection_quadrature(b);
            double I = (dinf + PI) / 2.0;
            double IR = light_half_sweep_to(b, uR);
            double alpha = asin(clampd(b * uR * sqrt(1.0 - 2.0 * uR), -1.0, 1.0));
            double sweep_ex = 2.0 * (I - IR);
            double dR_ex = sweep_ex - PI + 2.0 * alpha;
            fprintf(f, "G %d %.17g %.17g %.17g %.17g\n", i, b, dinf, dR_ex, sweep_ex);
        }
        fclose(f);
    }

    const char *cfgs[7] = { "binet-m8", "binet-m16", "binet-m32", "river-m16", "river-m32", "square", "tilt" };
    int kinds[7] = { K_BINET, K_BINET, K_BINET, K_RIVER, K_RIVER, K_SQUARE, K_TILT };
    int ms[7] = { 8, 16, 32, 16, 32, 0, 16 };

    for (int c = 0; c < 7; c++) {
        char fn[256];
        snprintf(fn, sizeof fn, "raw_%s.txt", cfgs[c]);
        FILE *out = fopen(fn, "w");
        printf("config %s ...\n", cfgs[c]); fflush(stdout);
        for (int i = 0; i < nb; i++) {
            Eng e; BoundOut bo;
            eng_init_bound(&e, kinds[c], ms[c], bp[i], be[i]);
            sim_bound(&e, 1, &bo, NULL);
            fprintf(out, "P %d %d %.17g %.17g %.17g\n", i, bo.ok, bo.adv, bo.T, bo.cross);
        }
        for (int i = 0; i < ng; i++) {
            Eng e; double dR = NAN, sw = NAN;
            eng_init_light(&e, kinds[c], ms[c], gb[i]);
            int ok = sim_light(&e, gb[i], &dR, &sw);
            fprintf(out, "D %d %d %.17g %.17g\n", i, ok, dR, sw);
        }
        double Ls[6] = { 2.0, 3.6, 3.88, 4.12, 4.4, 6.0 };
        for (int i = 0; i < 6; i++) {
            Eng e; eng_init_capture_matter(&e, kinds[c], ms[c], Ls[i]);
            int a = sim_absorb(&e);
            fprintf(out, "C %d %d\n", i, a);
        }
        double s3 = sqrt(3.0);
        double bs4[4] = { 0.9 * 3 * s3, 0.97 * 3 * s3, 1.03 * 3 * s3, 1.1 * 3 * s3 };
        for (int i = 0; i < 4; i++) {
            Eng e; eng_init_capture_photon(&e, kinds[c], ms[c], bs4[i]);
            int a = sim_absorb(&e);
            fprintf(out, "C %d %d\n", 6 + i, a);
        }
        {
            double Lc7 = sqrt(49.0 / 4.0), Lc55 = sqrt(30.25 / 2.5);
            Eng e; eng_init_isco(&e, kinds[c], ms[c], 7.0, 1.01 * Lc7);
            int A = sim_isco_A(&e, 7.0, 100);
            Eng e2; eng_init_isco(&e2, kinds[c], ms[c], 5.5, 0.99 * Lc55);
            int B = sim_isco_B(&e2);
            fprintf(out, "I %d %d\n", A, B);
        }
        for (int i = 0; i < 32; i++) {
            Eng e; BoundOut bo;
            eng_init_bound(&e, kinds[c], ms[c], bp[i], be[i]);
            sim_bound(&e, 10000, &bo, NULL);
            fprintf(out, "L %d %d %d\n", i, bo.ok && bo.shape_ok, bo.ok && bo.repeat_ok);
            fflush(out);
        }
        fclose(out);
    }

    double tb[5] = { 10.0, 31.622776601683793, 100.0, 316.22776601683793, 1000.0 };
    for (int c = 0; c < 7; c++) {
        char fn[256];
        snprintf(fn, sizeof fn, "trace_%s.txt", cfgs[c]);
        FILE *f = fopen(fn, "w");
        fprintf(f, "# orbit p=20 e=0.5 5 cycles\n");
        Eng e; BoundOut bo;
        eng_init_bound(&e, kinds[c], ms[c], 20.0, 0.5);
        sim_bound(&e, 6, &bo, f);
        for (int i = 0; i < 5; i++) {
            fprintf(f, "# light b=%g\n", tb[i]);
            Eng el;
            eng_init_light(&el, kinds[c], ms[c], tb[i]);
            trace_light(&el, f);
        }
        fclose(f);
    }
    {
        FILE *f = fopen("trace_exact.txt", "w");
        fprintf(f, "# orbit p=20 e=0.5 5 cycles\n");
        exact_orbit_trace(20.0, 0.5, 5, f);
        for (int i = 0; i < 5; i++) {
            fprintf(f, "# light b=%g\n", tb[i]);
            exact_light_trace(tb[i], f);
        }
        fclose(f);
    }
    printf("done\n");
    return 0;
}
