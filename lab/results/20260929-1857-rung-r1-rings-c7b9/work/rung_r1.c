// Rung r1: orbits in rings around one mass. Schwarzschild, G=c=M=1, equatorial plane, float64.
// Configs: binet-m8 | binet-m16 | binet-m32 | river-m16 | river-m32 | square | tiltonly
// Oracle ported from xtask/src/gr_oracle.rs and xtask/src/gr_oracle_extended.rs.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>

static const double PI = 3.14159265358979323846;

// ---------------------------------------------------------------- Gauss-Legendre (ported)
typedef struct { double x, w; } glnode;
static glnode GL32[32], GL16[16], GL12[12];
static void gauss_legendre_into(int n, glnode *out)
{
    for (int i = 1; i <= n; i++) {
        double x = cos(PI * ((double)i - 0.25) / ((double)n + 0.5)), dp = 0;
        for (int it = 0; it < 100; it++) {
            double p0 = 1, p1 = x;
            for (int k = 2; k <= n; k++) { double p2 = ((2*k-1)*x*p1 - (k-1)*p0)/k; p0 = p1; p1 = p2; }
            dp = (double)n * (x*p1 - p0) / (x*x - 1);
            double dx = p1 / dp; x -= dx;
            if (fabs(dx) < 1e-16) break;
        }
        out[i-1].x = x; out[i-1].w = 2.0 / ((1 - x*x) * dp * dp);
    }
}

// ---------------------------------------------------------------- oracle (ported)
static double ellip_k(double m)
{
    double a = 1.0, g = sqrt(1.0 - m);
    for (int i = 0; i < 40; i++) {
        double a1 = (a + g) / 2, g1 = sqrt(a * g);
        if (fabs(a1 - g1) <= 1e-17 * a1) { a = a1; break; }
        a = a1; g = g1;
    }
    return PI / (2 * a);
}
static double ellip_k_minus_half_pi(double m)
{
    if (m >= 0.25) return ellip_k(m) - PI / 2;
    double c = 1, mn = 1, sum = 0;
    for (int n = 1; n < 200; n++) {
        c *= (2.0*n - 1) / (2.0*n); mn *= m;
        double term = c * c * mn; sum += term;
        if (term < 1e-19 * sum) break;
    }
    return PI / 2 * sum;
}
static double periapsis_elliptic(double p, double e) // advance per radial cycle, exact
{
    double d = p - 6.0 + 2.0 * e;
    double s = sqrt(p / d);
    double sm1 = (6.0 - 2.0 * e) / d / (s + 1.0);
    return 4.0 * (s * ellip_k_minus_half_pi(4.0 * e / d) + PI / 2 * sm1);
}
static double null_turning_radius(double b)
{
    double r = b - 1.0;
    for (int i = 0; i < 40; i++) {
        double f = r * r / (1.0 - 2.0 / r) - b * b;
        double df = 2.0 * r * r * (r - 3.0) / ((r - 2.0) * (r - 2.0));
        double step = f / df; r -= step;
        if (fabs(step) < 2e-15 * r) break;
    }
    return r;
}
static double deflection_quadrature(double b)
{
    double u0 = 1.0 / b;
    for (int i = 0; i < 100; i++) {
        double h = 2.0*u0*u0*u0 - u0*u0 + 1.0/(b*b), dh = 6.0*u0*u0 - 2.0*u0;
        double step = h / dh; u0 -= step;
        if (fabs(step) <= 1e-17 * u0) break;
    }
    int pieces = 64; double total = 0;
    for (int j = 0; j < pieces; j++) {
        double a = (double)j / pieces, c = (double)(j + 1) / pieces;
        for (int i = 0; i < 32; i++) {
            double s = (a + c) / 2 + (c - a) / 2 * GL32[i].x;
            double u = u0 * (1.0 - s * s);
            double qf = u0 + u, r = 2.0 * (u*u + u*u0 + u0*u0);
            double q = qf - r;
            total += GL32[i].w * (c - a) / 2 * 4.0 * sqrt(u0) * r / (sqrt(q * qf) * (sqrt(qf) + sqrt(q)));
        }
    }
    return total;
}
static double light_tail(double b) // 2 * int_0^{1e-4} du/sqrt(1/b^2-u^2+2u^3): both legs beyond r=1e4
{
    double hi = 1e-4, sum = 0; int pieces = 4;
    for (int j = 0; j < pieces; j++) {
        double lo = hi * j / pieces, up = hi * (j + 1) / pieces;
        for (int i = 0; i < 32; i++) {
            double u = (lo + up) / 2 + (up - lo) / 2 * GL32[i].x;
            sum += (up - lo) * 0.5 * GL32[i].w / sqrt(1.0/(b*b) - u*u + 2.0*u*u*u);
        }
    }
    return 2 * sum;
}
static void bound_constants(double p, double e, double *E, double *L)
{
    *E = sqrt(((p - 2.0)*(p - 2.0) - 4.0*e*e) / (p * (p - 3.0 - e*e)));
    *L = p / sqrt(p - 3.0 - e*e);
}
typedef struct { double p, e, E, L; } bpq_ctx;
static double bpq_f(double chi, void *v)
{
    bpq_ctx *c = (bpq_ctx*)v;
    double r = c->p / (1.0 + c->e * cos(chi));
    double dphi = sqrt(c->p / (c->p - 6.0 - 2.0 * c->e * cos(chi)));
    return dphi * r * r / c->L * c->E / (1.0 - 2.0 / r);
}
static double integrate_gl(double lo, double hi, int pieces, double (*f)(double, void*), void *ctx)
{
    double sum = 0;
    for (int j = 0; j < pieces; j++) {
        double a = lo + (hi - lo) * j / pieces, b = lo + (hi - lo) * (j + 1) / pieces;
        for (int i = 0; i < 32; i++)
            sum += (b - a) * 0.5 * GL32[i].w * f((a + b) * 0.5 + (b - a) * 0.5 * GL32[i].x, ctx);
    }
    return sum;
}
static double bound_period_quad_t(double p, double e)
{
    bpq_ctx c = { p, e, 0, 0 }; bound_constants(p, e, &c.E, &c.L);
    int pieces = 16; double v = integrate_gl(0, 2*PI, pieces, bpq_f, &c);
    while (pieces < 1 << 14) {
        pieces *= 2;
        double w = integrate_gl(0, 2*PI, pieces, bpq_f, &c);
        int done = fabs(w - v) <= 1e-14 * fabs(w);
        v = w; if (done) break;
    }
    return v;
}
static int exact_captured_massive(double L) // E=1, from r=100: captured iff no turning in (0.01,0.5)
{
    double L2 = L * L;
    #define FMASS(u) (2.0*(u) - L2*(u)*(u) + 2.0*L2*(u)*(u)*(u))
    double lo = 0.01, hi = 0.5;
    double minf = fmin(FMASS(lo), FMASS(hi));
    double disc = 1.0 - 12.0 / L2;
    if (disc > 0) {
        double um = (1 - sqrt(disc)) / 6, up = (1 + sqrt(disc)) / 6;
        if (um > lo && um < hi && FMASS(um) < minf) minf = FMASS(um);
        if (up > lo && up < hi && FMASS(up) < minf) minf = FMASS(up);
    }
    return minf > 0 ? 1 : 0;
}
static int exact_captured_photon(double b)
{
    #define GPH(u) (1.0/(b*b) - (u)*(u) + 2.0*(u)*(u)*(u))
    double ming = fmin(GPH(1e-4), fmin(GPH(0.5), GPH(1.0/3.0)));
    return ming > 0 ? 1 : 0;
}

// ---------------------------------------------------------------- event codes
#define EV_OUT 0
#define EV_IN 1
#define EV_TURN 2
#define EV_CAP 3
#define EV_EXIT 4
#define EV_STALL (-1)

// ---------------------------------------------------------------- Binet ring engine
typedef struct {
    int m, light;
    double E, L;         // light: E=1, L=b
    double u, w, phi, t;
    int k;
    double exit_u; int exit_active; long long crossings;
} Binet;
static double band_uc(int k, int m) { return exp2(-((double)k + 0.5) / m); }
static double band_uhi(int k, int m) { return exp2(-(double)k / m); }
static double band_ulo(int k, int m) { return exp2(-(double)(k + 1) / m); }
static int band_of(double u, int m)
{
    int k = (int)floor(m * log2(1.0 / u));
    for (int it = 0; it < 4; it++) {
        if (u > band_uhi(k, m)) k++;
        else if (u <= band_ulo(k, m)) k--;
        else break;
    }
    return k;
}
static int binet_step(Binet *b, double *dphi, double *dt)
{
    double uc = band_uc(b->k, b->m);
    double ulo = band_ulo(b->k, b->m), uhi = band_uhi(b->k, b->m);
    double C = b->light ? -3.0*uc*uc : 1.0/(b->L*b->L) - 3.0*uc*uc;
    double w2 = 1.0 - 6.0*uc;
    double targ[4]; int ttyp[4]; int nt = 0;
    targ[nt] = ulo; ttyp[nt++] = EV_OUT;
    targ[nt] = uhi; ttyp[nt++] = EV_IN;
    if (0.5 > ulo && 0.5 < uhi) { targ[nt] = 0.5; ttyp[nt++] = EV_CAP; }
    if (b->exit_active && b->w < 0.0 && b->exit_u > ulo && b->exit_u < uhi) {
        targ[nt] = b->exit_u; ttyp[nt++] = EV_EXIT;
    }
    double best = 1e300, u_ev = b->u, w_ev = b->w; int ev = EV_STALL;
    *dphi = 0; *dt = 0;
    if (w2 > 0) {
        double om = sqrt(w2), up = C / w2;
        double A = b->u - up, B = b->w / om;
        double R = sqrt(A*A + B*B);
        if (R < 1e-13 * (fabs(up) + 1e-300)) { b->w += 1e-11 * (1 + fabs(b->w)); return EV_STALL; }
        double al = atan2(B, A);
        double th0 = fmod(-al, 2*PI); if (th0 < 0) th0 += 2*PI;
        for (int i = 0; i < nt; i++) {
            double cc = (targ[i] - up) / R;
            if (cc < -1 || cc > 1) continue;
            double thv = acos(cc);
            double cand[2] = { thv, 2*PI - thv };
            for (int q = 0; q < 2; q++) {
                double th = cand[q];
                if (th <= th0 + 1e-13) th += 2*PI;
                double d = (th - th0) / om;
                if (d > 0 && d < best) {
                    double w_at = -R * om * sin(th);
                    if (ttyp[i] == EV_EXIT && w_at >= 0) continue;
                    best = d; ev = ttyp[i]; u_ev = targ[i]; w_ev = w_at;
                }
            }
        }
        double ct[2] = { 0.0, PI };
        for (int q = 0; q < 2; q++) {
            double th = ct[q];
            if (th <= th0 + 1e-13) th += 2*PI;
            double d = (th - th0) / om;
            if (d > 0 && d < best) { best = d; ev = EV_TURN; u_ev = up + R * cos(th); w_ev = 0.0; }
        }
        if (ev != EV_STALL && !b->light && ev != EV_CAP) {
            double s = 0;
            for (int i = 0; i < 12; i++) {
                double dl = best / 2 * (GL12[i].x + 1);
                double uu = up + A * cos(om*dl) + B * sin(om*dl);
                s += GL12[i].w * b->E / (b->L * uu * uu * (1.0 - 2.0*uu));
            }
            *dt = best / 2 * s;
        }
    } else {
        double kap = sqrt(-w2), up = C / w2;
        double A = b->u - up, B = b->w / kap;
        double tg = -b->w / (kap * A);
        if (fabs(A) > 1e-300 && fabs(tg) < 1) {
            double d = atanh(tg) / kap;
            if (d > 1e-14 && d < best) {
                double tt = tanh(kap * d);
                double u_t = up + (A + B*tt) / sqrt(1 - tt*tt);
                if (u_t > ulo && u_t <= uhi) { best = d; ev = EV_TURN; u_ev = u_t; w_ev = 0; }
            }
        }
        for (int i = 0; i < nt; i++) {
            double V = targ[i];
            double al2 = (A + B) / 2, be = -(V - up), ga = (A - B) / 2;
            if (fabs(al2) < 1e-300) continue;
            double disc = be*be - 4*al2*ga;
            if (disc < 0) continue;
            double sq = sqrt(disc);
            double qq = -(be + (be >= 0 ? sq : -sq)) / 2;
            double zz[2] = { qq / al2, (fabs(qq) > 1e-300) ? ga / qq : 1e300 };
            for (int q = 0; q < 2; q++) {
                if (zz[q] > 1 + 1e-12) {
                    double d = log(zz[q]) / kap;
                    if (d > 0 && d < best) {
                        double w_at = kap * A * sinh(kap*d) + b->w * cosh(kap*d);
                        if (ttyp[i] == EV_EXIT && w_at >= 0) continue;
                        best = d; ev = ttyp[i]; u_ev = V; w_ev = w_at;
                    }
                }
            }
        }
        if (ev != EV_STALL && !b->light && ev != EV_CAP) {
            double s = 0;
            for (int i = 0; i < 12; i++) {
                double dl = best / 2 * (GL12[i].x + 1);
                double uu = up + A * cosh(kap*dl) + B * sinh(kap*dl);
                s += GL12[i].w * b->E / (b->L * uu * uu * (1.0 - 2.0*uu));
            }
            *dt = best / 2 * s;
        }
    }
    if (ev == EV_STALL) { b->w += 1e-11 * (1 + fabs(b->w)); return EV_STALL; }
    b->phi += best; b->t += *dt; b->u = u_ev; b->w = w_ev; *dphi = best;
    if (ev == EV_OUT) { b->k--; b->crossings++; }
    else if (ev == EV_IN) { b->k++; b->crossings++; }
    return ev;
}

// ---------------------------------------------------------------- River ring engine
typedef struct {
    int m; double H, L, mu;
    int k, sigma;
    double r, phi, t;
    double exit_r; int exit_active; long long crossings;
} River;
static double ring_rlo(int k, int m) { return exp2((double)k / m); }
static double ring_rhi(int k, int m) { return exp2((double)(k + 1) / m); }
static int ring_of(double r, int m)
{
    int k = (int)floor(m * log2(r));
    for (int it = 0; it < 4; it++) {
        if (r >= ring_rhi(k, m)) k++;
        else if (r < ring_rlo(k, m)) k--;
        else break;
    }
    return k;
}
typedef struct { double H, L, mu, ob, beta, sigma; } rivctx;
static double riv_dphi(double r, void *v)
{
    rivctx *c = (rivctx*)v;
    double S = sqrt(c->H*c->H - c->ob * (c->mu + c->L*c->L/(r*r)));
    return c->L / (r*r*S);
}
static double riv_dt(double r, void *v)
{
    rivctx *c = (rivctx*)v;
    double S = sqrt(c->H*c->H - c->ob * (c->mu + c->L*c->L/(r*r)));
    double g = (c->H - c->sigma * c->beta * S);
    return g * g / (c->ob * c->ob * S);
}
static double riv_int(double lo, double hi, bool sing_at_lo, double (*f)(double, void*), rivctx *c)
{
    if (!sing_at_lo) {
        double s = 0;
        for (int i = 0; i < 16; i++) {
            double r = (lo + hi)/2 + (hi - lo)/2 * GL16[i].x;
            s += GL16[i].w * f(r, c);
        }
        return (hi - lo) / 2 * s;
    }
    double a = lo, b = hi, s = 0;   // r = a + (b-a) s^2 kills the 1/sqrt turning singularity
    for (int i = 0; i < 16; i++) {
        double ss = (GL16[i].x + 1) / 2;
        double r = a + (b - a) * ss * ss;
        s += GL16[i].w * f(r, c) * 2 * (b - a) * ss;
    }
    return s / 2;
}
static int river_step(River *s, double *dphi, double *dt)
{
    double rc = exp2(((double)s->k + 0.5) / s->m);
    double beta = -sqrt(2.0 / rc), ob = 1.0 - beta*beta;
    double rlo = ring_rlo(s->k, s->m), rhi = ring_rhi(s->k, s->m);
    *dphi = 0; *dt = 0;
    if (ob <= 0) return EV_CAP;                       // should not happen: we stop at r=2
    double H2 = s->H*s->H;
    double S2cur = H2 - ob * (s->mu + s->L*s->L/(s->r*s->r));
    if (S2cur < -1e-12 * fmax(1.0, H2)) {             // no real p_r in this ring: reflect at the edge
        s->sigma = -s->sigma;
        if (s->sigma > 0) s->k++; else s->k--;        // step back into the ring we came from
        return EV_TURN;
    }
    double denom = H2 - ob * s->mu;
    double r_tp = (denom > 0) ? fabs(s->L) * sqrt(ob) / sqrt(denom) : -1.0;
    int ev; double endr;
    if (s->sigma > 0) {
        if (s->exit_active && s->exit_r > s->r && s->exit_r < rhi) { endr = s->exit_r; ev = EV_EXIT; }
        else if (r_tp > 0 && r_tp < rhi && r_tp > s->r) { endr = r_tp; ev = EV_TURN; }
        else { endr = rhi; ev = EV_OUT; }
    } else {
        if (s->k == s->m) return EV_CAP;              // crossing r=2.0 inward: absorbed
        if (r_tp > 0 && r_tp > rlo && r_tp < s->r) { endr = r_tp; ev = EV_TURN; }
        else { endr = rlo; ev = EV_IN; }
    }
    rivctx c = { s->H, s->L, s->mu, ob, beta, (double)s->sigma };
    double lo, hi; bool sing;
    if (ev == EV_TURN) { lo = endr; hi = s->r; sing = true; }  // S->0 at the turning end
    else { lo = fmin(s->r, endr); hi = fmax(s->r, endr); sing = false; }
    *dphi = riv_int(lo, hi, sing, riv_dphi, &c);
    *dt   = riv_int(lo, hi, sing, riv_dt, &c);
    s->phi += *dphi; s->t += *dt; s->r = endr;
    if (ev == EV_OUT) { s->k++; s->crossings++; }
    else if (ev == EV_IN) { s->k--; s->crossings++; }
    else if (ev == EV_TURN) s->sigma = -s->sigma;
    return ev;
}

// ---------------------------------------------------------------- Square cell engine (negative)
typedef struct {
    double x, y, px, py, t, H;
    int light;
    long long crossings;
    double phi;
} Square;
static double sq_mu(Square *s) { return s->light ? 0.0 : 1.0; }
static void sq_cell_beta(double x, double y, double *bx, double *by)
{
    double r = sqrt(x*x + y*y);
    int n = (int)round(log2(r / 16.0));
    double side = exp2((double)n);
    double i = floor(x / side), j = floor(y / side);
    double cx = (i + 0.5) * side, cy = (j + 0.5) * side;
    double rc = sqrt(cx*cx + cy*cy);
    double bmag = -sqrt(2.0 / rc);
    *bx = bmag * cx / rc; *by = bmag * cy / rc;
}
static void sq_recalc_h(Square *s)
{
    double bx, by; sq_cell_beta(s->x, s->y, &bx, &by);
    s->H = sqrt(sq_mu(s) + s->px*s->px + s->py*s->py) + bx * s->px + by * s->py;
}
static bool sq_solve_perp(double H, double mu, double ppar, double bpar, double bperp, double pperp_old, double *pperp)
{
    double Q = H - bpar * ppar;
    double A = 1 - bperp*bperp, B = -2*Q*bperp, Cc = Q*Q - mu - ppar*ppar;
    double disc = B*B - 4*A*Cc;
    if (disc < 0) return false;
    double sq = sqrt(disc);
    double r1 = (-B + sq) / (2*A), r2 = (-B - sq) / (2*A);
    *pperp = (fabs(r1 - pperp_old) <= fabs(r2 - pperp_old)) ? r1 : r2;
    return true;
}
static int square_step(Square *s, double *dphi, double *dt, int *peri, double *r_peri)
{
    double bx, by; sq_cell_beta(s->x, s->y, &bx, &by);
    double gam = sqrt(sq_mu(s) + s->px*s->px + s->py*s->py);
    double vx = s->px / gam + bx, vy = s->py / gam + by;
    double vv = vx*vx + vy*vy;
    if (vv < 1e-300) return EV_STALL;
    double r = sqrt(s->x*s->x + s->y*s->y);
    int n = (int)round(log2(r / 16.0));
    double side = exp2((double)n);
    double i = floor(s->x / side), j = floor(s->y / side);
    double tx = 1e300, ty = 1e300;
    if (vx > 1e-300) tx = ((i + 1)*side - s->x) / vx; else if (vx < -1e-300) tx = (i*side - s->x) / vx;
    if (vy > 1e-300) ty = ((j + 1)*side - s->y) / vy; else if (vy < -1e-300) ty = (j*side - s->y) / vy;
    double texit = fmin(tx, ty); int facex = (tx <= ty);
    double topt = -(s->x*vx + s->y*vy) / vv;
    *peri = 0;
    double tcap = fmax(0.0, fmin(texit, topt));
    double xc = s->x + vx*tcap, yc = s->y + vy*tcap;
    if (xc*xc + yc*yc <= 4.0) return EV_CAP;
    if (topt > 1e-300 && topt < texit) { *peri = -1; *r_peri = sqrt((s->x+vx*topt)*(s->x+vx*topt) + (s->y+vy*topt)*(s->y+vy*topt)); }
    double xn = s->x + vx*texit, yn = s->y + vy*texit;
    if (facex) xn = (vx > 0 ? (i + 1)*side : i*side); else yn = (vy > 0 ? (j + 1)*side : j*side);
    double p0 = atan2(s->y, s->x), p1 = atan2(yn, xn);
    double dp = p1 - p0; while (dp > PI) dp -= 2*PI; while (dp < -PI) dp += 2*PI;
    s->phi += dp; *dphi = dp; *dt = texit; s->t += texit;
    double eps = 1e-9 * fmax(1.0, fabs(xn));
    s->x = xn + (facex ? (vx > 0 ? eps : -eps) : 0);
    s->y = yn + (facex ? 0 : (vy > 0 ? eps : -eps));
    double bxn, byn; sq_cell_beta(s->x, s->y, &bxn, &byn);
    if (bxn != bx || byn != by) {
        double ppar, pperp_old, bpar, bperp, pp;
        if (facex) { ppar = s->py; pperp_old = s->px; bpar = byn; bperp = bxn; }
        else       { ppar = s->px; pperp_old = s->py; bpar = bxn; bperp = byn; }
        if (sq_solve_perp(s->H, sq_mu(s), ppar, bpar, bperp, pperp_old, &pp)) {
            if (facex) s->px = pp; else s->py = pp;
        } else {
            if (facex) s->px = -s->px; else s->py = -s->py;   // total reflection
        }
    }
    s->crossings++;
    return EV_OUT;
}
// packed cell id for sequence recording
static long long sq_cell_id(double x, double y)
{
    double r = sqrt(x*x + y*y);
    int n = (int)round(log2(r / 16.0));
    double side = exp2((double)n);
    long long i = (long long)floor(x / side), j = (long long)floor(y / side);
    return ((long long)(n + 100) << 44) ^ ((i + (1LL << 20)) << 22) ^ (j + (1LL << 20));
}

// ---------------------------------------------------------------- Tilt-only engine (negative)
typedef struct {
    double x, y, vx, vy, speed, t, phi;
    int m;
    long long crossings;
    double exit_r; int exit_active;
} Tilt;
static int tilt_step(Tilt *s, double *dphi, double *dt, int *peri, double *r_peri)
{
    double r = sqrt(s->x*s->x + s->y*s->y);
    int k = ring_of(r, s->m);
    double rlo = ring_rlo(k, s->m), rhi = ring_rhi(k, s->m);
    double v2 = s->vx*s->vx + s->vy*s->vy;
    double b = 2*(s->x*s->vx + s->y*s->vy);
    double best = 1e300; bool is_exit = false;
    double cand_R[3] = { rlo, rhi, s->exit_active ? s->exit_r : -1 };
    for (int d = 0; d < 3; d++) {
        double R = cand_R[d];
        if (R <= 0) continue;
        double c = r*r - R*R;
        double disc = b*b - 4*v2*c;
        if (disc < 0) continue;
        double sq = sqrt(disc);
        double t1 = (-b + sq) / (2*v2), t2 = (-b - sq) / (2*v2);
        if (t1 > 1e-13 && t1 < best) { best = t1; is_exit = (d == 2); }
        if (t2 > 1e-13 && t2 < best) { best = t2; is_exit = (d == 2); }
    }
    if (best >= 1e299) return EV_STALL;
    double topt = -(s->x*s->vx + s->y*s->vy) / v2;
    *peri = 0;
    double tcap = fmax(0.0, fmin(best, topt));
    double xc = s->x + s->vx*tcap, yc = s->y + s->vy*tcap;
    if (xc*xc + yc*yc <= 4.0) return EV_CAP;
    if (topt > 1e-300 && topt < best) { *peri = -1; *r_peri = sqrt(xc*xc + yc*yc); }
    double xn = s->x + s->vx*best, yn = s->y + s->vy*best;
    double p0 = atan2(s->y, s->x), p1 = atan2(yn, xn);
    double dp = p1 - p0; while (dp > PI) dp -= 2*PI; while (dp < -PI) dp += 2*PI;
    s->phi += dp; *dphi = dp; *dt = best; s->t += best;
    s->x = xn; s->y = yn;
    if (is_exit) return EV_EXIT;
    s->crossings++;
    double rr = sqrt(xn*xn + yn*yn);
    double rhx = -xn / rr, rhy = -yn / rr;
    double vhx = s->vx / s->speed, vhy = s->vy / s->speed;
    double cosps = rhx*vhx + rhy*vhy;
    double sinps = sqrt(fmax(0, 1 - cosps*cosps));
    double alpha = (best / (rr*rr)) * sinps / s->speed;
    double ux = rhx - cosps*vhx, uy = rhy - cosps*vhy;
    double un = sqrt(ux*ux + uy*uy);
    if (un > 1e-300) {
        ux /= un; uy /= un;
        s->vx = s->speed * (vhx*cos(alpha) + ux*sin(alpha));
        s->vy = s->speed * (vhy*cos(alpha) + uy*sin(alpha));
    }
    return EV_OUT;
}

// ---------------------------------------------------------------- bound-orbit walker (all engines)
#define MAXSEQ 8192
typedef struct { double dphi, dt, r_peri, r_apo; long long cross; } CycM;
// Fills cyc[0..ncycles-1]; records cycle-1/2 crossing sequences into seq1/seq2 (if non-NULL).
// Returns ncycles, or -1 (capture/stall), -2 (phi budget exceeded).
static int walk_bound(int engine, int m, double E, double L, double u0, int ncycles,
                      CycM *cyc, int *seq1, int *n1, int *seq2, int *n2,
                      double *tx, double *ty, int *tn, int trace_max)
{
    int cur_seq[MAXSEQ]; int ncur = 0;
    double phi_cap = 3000.0;        // pre-first-cycle budget: catches escapes/stalls early
    #define TRACE(xx, yy) do { if (tx && tn && *tn < trace_max) { tx[*tn] = (xx); ty[*tn] = (yy); (*tn)++; } } while (0)
    int nc = 0;                     // cycles completed
    if (engine == 0) {
        Binet st = { m, 0, E, L, u0, 0.0, 0.0, 0.0, band_of(u0, m), -1.0, 0, 0 };
        int atperi = 1; double lp = 0, lt = 0, rapo = -1; long long lc = 0;
        while (nc < ncycles) {
            double dph, dtt;
            int ev = binet_step(&st, &dph, &dtt);
            if (ev == EV_STALL) continue;
            if (ev == EV_CAP) return -1;
            if (st.u < 1e-5 || st.phi > phi_cap) return -2;   // escaped / over budget
            TRACE(cos(st.phi)/st.u, sin(st.phi)/st.u);
            if (ev == EV_OUT || ev == EV_IN) { if (ncur < MAXSEQ) cur_seq[ncur++] = st.k; }
            if (ev == EV_TURN) {
                if (atperi) { rapo = 1.0/st.u; atperi = 0; }
                else {
                    if (nc >= 1) {
                        cyc[nc-1].dphi = st.phi - lp; cyc[nc-1].dt = st.t - lt;
                        cyc[nc-1].r_peri = 1.0/st.u; cyc[nc-1].r_apo = rapo;
                        cyc[nc-1].cross = st.crossings - lc;
                    }
                    if (nc == 0 && seq1) { *n1 = ncur; memcpy(seq1, cur_seq, ncur*sizeof(int)); }
                    if (nc == 1 && seq2) { *n2 = ncur; memcpy(seq2, cur_seq, ncur*sizeof(int)); }
                    lp = st.phi; lt = st.t; lc = st.crossings; ncur = 0; atperi = 1;
                    nc++;
                    if (nc == 1) phi_cap = st.phi * (ncycles + 3.0) * 1.5 + 100;
                    else if (st.phi > phi_cap) return -2;
                }
            }
        }
        return nc;
    }
    if (engine == 1) {
        double r_p = 1.0/u0;
        int k0 = ring_of(r_p, m);
        double rtp_best = -1;
        for (int kk = k0 - 3; kk <= k0 + 3; kk++) {
            if (kk < m) continue;
            double rcen = exp2(((double)kk + 0.5)/m);
            double beta = -sqrt(2.0/rcen), ob = 1 - beta*beta;
            double den = E*E - ob;
            if (den <= 0) continue;
            double rtp = fabs(L)*sqrt(ob)/sqrt(den);
            if (rtp >= ring_rlo(kk, m) && rtp <= ring_rhi(kk, m))
                if (rtp_best < 0 || fabs(rtp - r_p) < fabs(rtp_best - r_p)) rtp_best = rtp;
        }
        double r_start = r_p;
        {
            double rcen = exp2(((double)k0 + 0.5)/m);
            double beta = -sqrt(2.0/rcen), ob = 1 - beta*beta;
            if (E*E - ob*(1.0 + L*L/(r_p*r_p)) < 0) {
                if (rtp_best > 0) r_start = rtp_best; else return -1;
            }
        }
        River st = { m, E, L, 1.0, ring_of(r_start, m), 1, r_start, 0, 0, -1.0, 0, 0 };
        int nturns = 0; double lp = 0, lt = 0, rapo = -1; long long lc = 0;
        while (nc < ncycles) {
            double dph, dtt;
            int ev = river_step(&st, &dph, &dtt);
            if (ev == EV_CAP || ev == EV_STALL) return -1;
            if (st.r > 2e5 || st.phi > phi_cap) return -2;    // escaped / over budget
            TRACE(st.r*cos(st.phi), st.r*sin(st.phi));
            if (ev == EV_OUT || ev == EV_IN) { if (ncur < MAXSEQ) cur_seq[ncur++] = st.k; }
            if (ev == EV_TURN) {
                if (nturns % 2 == 0) rapo = st.r;
                else {
                    if (nc >= 1) {
                        cyc[nc-1].dphi = st.phi - lp; cyc[nc-1].dt = st.t - lt;
                        cyc[nc-1].r_peri = st.r; cyc[nc-1].r_apo = rapo;
                        cyc[nc-1].cross = st.crossings - lc;
                    }
                    if (nc == 0 && seq1) { *n1 = ncur; memcpy(seq1, cur_seq, ncur*sizeof(int)); }
                    if (nc == 1 && seq2) { *n2 = ncur; memcpy(seq2, cur_seq, ncur*sizeof(int)); }
                    lp = st.phi; lt = st.t; lc = st.crossings; ncur = 0;
                    nc++;
                    if (nc == 1) phi_cap = st.phi * (ncycles + 3.0) * 1.5 + 100;
                    else if (st.phi > phi_cap) return -2;
                }
                nturns++;
            }
        }
        return nc;
    }
    if (engine == 2) {
        double r_p = 1.0/u0;
        Square st = { r_p, 0, 0, L/r_p, 0, 0, 1, 0, 0 }; sq_recalc_h(&st);
        double lp = 0, lt = 0, rapo = 1e-1; long long lc = 0;
        while (nc < ncycles) {
            double dph, dtt; int pa; double rp;
            int ev = square_step(&st, &dph, &dtt, &pa, &rp);
            if (ev == EV_CAP) return -1;
            if (ev == EV_STALL) return -1;
            if (st.x*st.x + st.y*st.y > 4e10 || st.phi > phi_cap) return -2;  // escaped / over budget
            TRACE(st.x, st.y);
            if (ncur < MAXSEQ) cur_seq[ncur++] = (int)sq_cell_id(st.x, st.y);
            if (pa == -1) {
                if (nc >= 1) {
                    cyc[nc-1].dphi = st.phi - lp; cyc[nc-1].dt = st.t - lt;
                    cyc[nc-1].r_peri = rp; cyc[nc-1].r_apo = rapo;
                    cyc[nc-1].cross = st.crossings - lc;
                }
                if (nc == 0 && seq1) { *n1 = ncur; memcpy(seq1, cur_seq, ncur*sizeof(int)); }
                if (nc == 1 && seq2) { *n2 = ncur; memcpy(seq2, cur_seq, ncur*sizeof(int)); }
                lp = st.phi; lt = st.t; lc = st.crossings; ncur = 0;
                nc++;
                if (nc == 1) phi_cap = st.phi * (ncycles + 3.0) * 1.5 + 100;
                else if (st.phi > phi_cap) return -2;
                rapo = rp;
            } else {
                double rnow = sqrt(st.x*st.x + st.y*st.y);
                if (rnow > rapo) rapo = rnow;
            }
        }
        return nc;
    }
    if (engine == 3) {
        double r_p = 1.0/u0;
        double beta0 = -sqrt(2.0/r_p), pf = L/r_p, gam = sqrt(1.0 + pf*pf);
        double speed = sqrt((pf/gam)*(pf/gam) + beta0*beta0);
        Tilt st = { r_p, 0, 0, speed, speed, 0, 0, 16, 0, -1.0, 0 };
        double lp = 0, lt = 0, rapo = 1e-1; long long lc = 0;
        while (nc < ncycles) {
            double dph, dtt; int pa; double rp;
            int ev = tilt_step(&st, &dph, &dtt, &pa, &rp);
            if (ev == EV_CAP) return -1;
            if (ev == EV_STALL) return -1;
            if (st.x*st.x + st.y*st.y > 4e10 || st.phi > phi_cap) return -2;  // escaped / over budget
            TRACE(st.x, st.y);
            if (ncur < MAXSEQ) cur_seq[ncur++] = ring_of(sqrt(st.x*st.x + st.y*st.y), 16);
            if (pa == -1) {
                if (nc >= 1) {
                    cyc[nc-1].dphi = st.phi - lp; cyc[nc-1].dt = st.t - lt;
                    cyc[nc-1].r_peri = rp; cyc[nc-1].r_apo = rapo;
                    cyc[nc-1].cross = st.crossings - lc;
                }
                if (nc == 0 && seq1) { *n1 = ncur; memcpy(seq1, cur_seq, ncur*sizeof(int)); }
                if (nc == 1 && seq2) { *n2 = ncur; memcpy(seq2, cur_seq, ncur*sizeof(int)); }
                lp = st.phi; lt = st.t; lc = st.crossings; ncur = 0;
                nc++;
                if (nc == 1) phi_cap = st.phi * (ncycles + 3.0) * 1.5 + 100;
                else if (st.phi > phi_cap) return -2;
                rapo = rp;
            } else {
                double rnow = sqrt(st.x*st.x + st.y*st.y);
                if (rnow > rapo) rapo = rnow;
            }
        }
        return nc;
    }
    return -1;
}

// ---------------------------------------------------------------- light / capture / isco
// deflection (>0) or -1 capture, -2 stall
static double run_light(int engine, int m, double b,
                        double *tx, double *ty, int *tn, int trace_max)
{
    const double u_start = 1e-4, r0 = 1e4;
    if (engine == 0) {
        Binet st = { m, 1, 1.0, b, u_start, sqrt(1.0/(b*b) - u_start*u_start + 2.0*u_start*u_start*u_start),
                     0, 0, band_of(u_start, m), u_start, 1, 0 };
        while (st.phi < 1e5) {
            double dph, dtt;
            int ev = binet_step(&st, &dph, &dtt);
            if (ev == EV_STALL) continue;
            TRACE(cos(st.phi)/st.u, sin(st.phi)/st.u);
            if (ev == EV_CAP) return -1;
            if (ev == EV_EXIT) return st.phi - PI + light_tail(b);
        }
        return -2;
    }
    if (engine == 1) {
        River st = { m, 1.0, b, 0.0, ring_of(r0, m), -1, r0, 0, 0, r0, 1, 0 };
        while (st.phi < 1e5) {
            double dph, dtt;
            int ev = river_step(&st, &dph, &dtt);
            if (ev == EV_CAP) return -1;
            if (ev == EV_STALL) return -2;
            TRACE(st.r*cos(st.phi), st.r*sin(st.phi));
            if (ev == EV_EXIT) return st.phi - PI + light_tail(b);
        }
        return -2;
    }
    if (engine == 2) {
        double xs = -sqrt(r0*r0 - b*b), ys = -b;
        Square st = { xs, ys, 0, 0, 0, 1, 1, 0, 0 };
        // bisection on angle th: p = P(th)*(cos,sin), P from H=1 with cell beta; target L = x*py - y*px = b
        double lo = -0.05, hi = 0.05;
        for (int it = 0; it < 80; it++) {
            double mid = (lo + hi)/2;
            double cth = cos(mid), sth = sin(mid);
            double bx, by; sq_cell_beta(st.x, st.y, &bx, &by);
            double bu = bx*cth + by*sth;
            double A = 1 - bu*bu, B = 2*bu, Cc = -1;
            double P = (-B + sqrt(B*B - 4*A*Cc)) / (2*A);
            st.px = P*cth; st.py = P*sth;
            double Lnow = xs*st.py - ys*st.px;
            if (Lnow > b) lo = mid; else hi = mid;
        }
        st.phi = atan2(ys, xs);
        double phi0 = st.phi;
        double lx = st.x, ly = st.y, lphi = st.phi;
        while (st.phi - phi0 < 1e5) {
            double dph, dtt; int pa; double rp;
            lx = st.x; ly = st.y; lphi = st.phi;
            int ev = square_step(&st, &dph, &dtt, &pa, &rp);
            if (ev == EV_CAP) return -1;
            if (ev == EV_STALL) return -2;
            TRACE(st.x, st.y);
            double rnow = sqrt(st.x*st.x + st.y*st.y);
            if (rnow >= r0 && st.phi - phi0 > 1.0) {
                // interpolate the exact r=r0 exit along the last straight segment
                double bx, by; sq_cell_beta(lx, ly, &bx, &by);
                double gam = sqrt(st.px*st.px + st.py*st.py);
                double vx = st.px/gam + bx, vy = st.py/gam + by;
                double vv = vx*vx + vy*vy, bb = 2*(lx*vx + ly*vy), cc = lx*lx + ly*ly - r0*r0;
                double disc = bb*bb - 4*vv*cc;
                double t = 0;
                if (disc >= 0) { double sq = sqrt(disc); double t2 = (-bb + sq)/(2*vv); t = (t2 > 0) ? t2 : (-bb - sq)/(2*vv); }
                double xe = lx + vx*t, ye = ly + vy*t;
                double pe = atan2(ye, xe);
                double dpe = pe - atan2(ly, lx); while (dpe > PI) dpe -= 2*PI; while (dpe < -PI) dpe += 2*PI;
                return lphi + dpe - phi0 - PI + light_tail(b);
            }
        }
        return -2;
    }
    if (engine == 3) {
        double xs = -sqrt(r0*r0 - b*b), ys = -b;
        Tilt st = { xs, ys, 1.0, 0.0, 1.0, 0, atan2(ys, xs), 16, 0, r0, 1 };
        double phi0 = st.phi;
        while (st.phi - phi0 < 1e5) {
            double dph, dtt; int pa; double rp;
            int ev = tilt_step(&st, &dph, &dtt, &pa, &rp);
            if (ev == EV_CAP) return -1;
            if (ev == EV_STALL) return -2;
            TRACE(st.x, st.y);
            if (ev == EV_EXIT) return st.phi - phi0 - PI + light_tail(b);
        }
        return -2;
    }
    return -2;
}
static int run_capture(int engine, int m, int light, double LorB)
{
    if (light) { double d = run_light(engine, m, LorB, NULL, NULL, NULL, 0); return d < 0 ? 1 : 0; }
    if (engine == 0) {
        double u0 = 0.01, L = LorB;
        Binet st = { m, 0, 1.0, L, u0,
                     sqrt(fmax(0, (2*u0 - L*L*u0*u0 + 2*L*L*u0*u0*u0)/(L*L))),
                     0, 0, band_of(u0, m), u0, 1, 0 };
        while (st.phi < 1e4) {
            double dph, dtt;
            int ev = binet_step(&st, &dph, &dtt);
            if (ev == EV_STALL) continue;
            if (ev == EV_CAP) return 1;
            if (ev == EV_EXIT) return 0;
        }
        return -1;
    }
    if (engine == 1) {
        River st = { m, 1.0, LorB, 1.0, ring_of(100.0, m), -1, 100.0, 0, 0, 100.0, 1, 0 };
        while (st.phi < 1e4) {
            double dph, dtt;
            int ev = river_step(&st, &dph, &dtt);
            if (ev == EV_CAP) return 1;
            if (ev == EV_STALL) return -1;
            if (ev == EV_EXIT) return 0;
        }
        return -1;
    }
    if (engine == 2) {
        Square st = { 100.0, 0, 0, 0, 0, 1, 0, 0 };
        // p_y = L/100 exactly (so L is exact); solve H=1 for p_x with the cell's beta;
        // two roots: pick the one with inward velocity v_x < 0 (the infalling branch).
        double bx, by; sq_cell_beta(st.x, st.y, &bx, &by);
        st.py = LorB / 100.0;
        {
            double Q = 1.0 - by * st.py;              // H - by*py
            double A = 1 - bx*bx, B = -2*Q*bx, Cc = Q*Q - 1.0 - st.py*st.py;
            double disc = B*B - 4*A*Cc;
            if (disc < 0) return -1;
            double sq = sqrt(disc);
            double r1 = (-B + sq) / (2*A), r2 = (-B - sq) / (2*A);
            st.px = r1;
            double gam = sqrt(1.0 + st.px*st.px + st.py*st.py);
            if (st.px/gam + bx >= 0) st.px = r2;      // v_x must be negative (inward)
        }
        st.phi = 0;
        while (st.phi < 1e4) {
            double dph, dtt; int pa; double rp;
            int ev = square_step(&st, &dph, &dtt, &pa, &rp);
            if (ev == EV_CAP) return 1;
            if (ev == EV_STALL) return -1;
            double rnow = sqrt(st.x*st.x + st.y*st.y);
            if (rnow >= 100.0 && st.phi > 1.0) return 0;
        }
        return -1;
    }
    if (engine == 3) {
        double beta0 = -sqrt(2.0/100.0);
        double pf = LorB/100.0, gam = sqrt(1.0 + pf*pf);
        double speed = sqrt((pf/gam)*(pf/gam) + beta0*beta0);
        Tilt st = { 100.0, 0, -speed, 0, speed, 0, 0, 16, 0, 100.0, 1 };
        while (st.phi < 1e4) {
            double dph, dtt; int pa; double rp;
            int ev = tilt_step(&st, &dph, &dtt, &pa, &rp);
            if (ev == EV_CAP) return 1;
            if (ev == EV_STALL) return -1;
            if (ev == EV_EXIT) return 0;
        }
        return -1;
    }
    return -1;
}
static int run_isco_bound(int engine, int m)
{
    double r0 = 7.0, L = 1.01 * (7.0 / 2.0);
    double E = sqrt((1.0 - 2.0/r0) * (1.0 + L*L/(r0*r0)));
    CycM cyc[104];
    int n = walk_bound(engine, m, E, L, 1.0/r0, 101, cyc, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0);
    return n >= 101 ? 1 : 0;
}
static int run_isco_plunge(int engine, int m)
{
    double r0 = 5.5, L = 0.99 * (5.5 / sqrt(2.5));
    double E = sqrt((1.0 - 2.0/r0) * (1.0 + L*L/(r0*r0)));
    if (engine == 0) {
        Binet st = { m, 0, E, L, 1.0/r0, 0.0, 0.0, 0.0, band_of(1.0/r0, m), -1.0, 0, 0 };
        while (st.phi < 50*40*PI) {
            double dph, dtt;
            int ev = binet_step(&st, &dph, &dtt);
            if (ev == EV_STALL) continue;
            if (ev == EV_CAP) return 1;
            if (ev == EV_TURN) return 0;
        }
        return 0;
    }
    if (engine == 1) {
        River st = { m, E, L, 1.0, ring_of(r0, m), -1, r0, 0, 0, -1.0, 0, 0 };
        while (st.phi < 50*40*PI) {
            double dph, dtt;
            int ev = river_step(&st, &dph, &dtt);
            if (ev == EV_CAP) return 1;
            if (ev == EV_TURN) return 0;
        }
        return 0;
    }
    if (engine == 2) {
        Square st = { r0, 0, 0, L/r0, 0, 1, 0, 0 }; sq_recalc_h(&st);
        while (st.phi < 50*40*PI) {
            double dph, dtt; int pa; double rp;
            int ev = square_step(&st, &dph, &dtt, &pa, &rp);
            if (ev == EV_CAP) return 1;
            if (ev == EV_STALL) return 0;
        }
        return 0;
    }
    if (engine == 3) {
        double beta0 = -sqrt(2.0/r0);
        double pf = L/r0, gam = sqrt(1.0 + pf*pf);
        double speed = sqrt((pf/gam)*(pf/gam) + beta0*beta0);
        Tilt st = { r0, 0, 0, speed, speed, 0, 0, 16, 0, -1.0, 0 };
        while (st.phi < 50*40*PI) {
            double dph, dtt; int pa; double rp;
            int ev = tilt_step(&st, &dph, &dtt, &pa, &rp);
            if (ev == EV_CAP) return 1;
            if (ev == EV_STALL) return 0;
        }
        return 0;
    }
    return 0;
}

// ---------------------------------------------------------------- selftest
static int selftest(void)
{
    struct { double p, e; } bc[3] = { {20,0.5}, {100,0.2}, {1000,0.5} };
    printf("periapsis advance (exact vs series 6pi/p(1+(18+e^2)/4p)):\n");
    for (int i = 0; i < 3; i++) {
        double ex = periapsis_elliptic(bc[i].p, bc[i].e);
        double se = 6*PI/bc[i].p * (1 + (18 + bc[i].e*bc[i].e)/(4*bc[i].p));
        printf("  p=%-7g e=%-4g exact=%.12g series=%.12g rel=%.2e\n", bc[i].p, bc[i].e, ex, se, fabs(ex-se)/ex);
    }
    printf("deflection (quad vs series 4/b+15pi/4b^2):\n");
    double bs[3] = { 10, 100, 1000 };
    for (int i = 0; i < 3; i++) {
        double ex = deflection_quadrature(bs[i]);
        double se = 4/bs[i] + 15*PI/4/(bs[i]*bs[i]);
        printf("  b=%-6g quad=%.12g series=%.12g rel=%.2e\n", bs[i], ex, se, fabs(ex-se)/ex);
    }
    printf("bound period (quad vs series 2pi a^1.5(1+3/a)):\n");
    for (int i = 0; i < 3; i++) {
        double ex = bound_period_quad_t(bc[i].p, bc[i].e);
        double a = bc[i].p/(1 - bc[i].e*bc[i].e);
        double se = 2*PI*pow(a, 1.5) * (1 + 3/a);
        printf("  p=%-7g e=%-4g quad=%.12g series=%.12g rel=%.2e\n", bc[i].p, bc[i].e, ex, se, fabs(ex-se)/ex);
    }
    printf("null turning: b=10 -> %.9f, b=100 -> %.9f\n", null_turning_radius(10), null_turning_radius(100));
    printf("light tail b=10: %.9g b=1000: %.9g\n", light_tail(10), light_tail(1000));
    printf("capture oracle massive L/4: ");
    double ls[6] = { 0.5, 0.9, 0.97, 1.03, 1.1, 1.5 };
    for (int i = 0; i < 6; i++) printf("%d", exact_captured_massive(4.0*ls[i]));
    printf(" (111000)  photon b/3sqrt3: ");
    double ps[4] = { 0.9, 0.97, 1.03, 1.1 };
    for (int i = 0; i < 4; i++) printf("%d", exact_captured_photon(3.0*sqrt(3.0)*ps[i]));
    printf(" (1100)\n");
    return 0;
}

// ---------------------------------------------------------------- seeds
static double sb_p[256], sb_e[256], sb_light[64];
static int load_seeds(const char *path)
{
    FILE *f = fopen(path, "r");
    if (!f) return -1;
    char buf[1 << 20];
    int len = fread(buf, 1, sizeof(buf) - 1, f); buf[len] = 0; fclose(f);
    char *pos = strstr(buf, "\"bound\"");
    if (!pos) return -1;
    pos = strchr(pos, '[');          // start of [[p,e],...]
    double nums[600]; int nn = 0;
    char *q = pos + 1;
    char *lightpos = strstr(buf, "\"light\"");
    while (*q && nn < 600) {
        if (q >= lightpos) break;
        if ((*q >= '0' && *q <= '9') || *q == '.' || *q == '-' || *q == '+' || *q == 'e' || *q == 'E') {
            char *end; double v = strtod(q, &end);
            if (end == q) q++;
            else { nums[nn++] = v; q = end; }
        } else q++;
    }
    if (nn < 512) { fprintf(stderr, "bound seed parse fail (%d)\n", nn); return -1; }
    for (int i = 0; i < 256; i++) { sb_p[i] = nums[2*i]; sb_e[i] = nums[2*i+1]; }
    q = strchr(lightpos, '[') + 1;
    int ln = 0;
    while (*q && ln < 64) {
        if ((*q >= '0' && *q <= '9') || *q == '.' || *q == '-' || *q == '+' || *q == 'e' || *q == 'E') {
            char *end; double v = strtod(q, &end);
            if (end == q) q++;
            else { sb_light[ln++] = v; q = end; }
        } else q++;
    }
    if (ln != 64) { fprintf(stderr, "light seed parse fail (%d)\n", ln); return -1; }
    return 0;
}
static int dblcmp(const void *a, const void *b)
{
    double x = *(const double*)a, y = *(const double*)b;
    return x < y ? -1 : x > y ? 1 : 0;
}

// ---------------------------------------------------------------- main
int main(int argc, char **argv)
{
    gauss_legendre_into(32, GL32);
    gauss_legendre_into(16, GL16);
    gauss_legendre_into(12, GL12);
    if (argc < 2) { fprintf(stderr, "usage: %s selftest|<config>\n", argv[0]); return 1; }
    if (!strcmp(argv[1], "selftest")) return selftest();

    const char *cfg = argv[1];
    int engine, m;
    if      (!strcmp(cfg, "binet-m8"))  { engine = 0; m = 8; }
    else if (!strcmp(cfg, "binet-m16")) { engine = 0; m = 16; }
    else if (!strcmp(cfg, "binet-m32")) { engine = 0; m = 32; }
    else if (!strcmp(cfg, "river-m16")) { engine = 1; m = 16; }
    else if (!strcmp(cfg, "river-m32")) { engine = 1; m = 32; }
    else if (!strcmp(cfg, "square"))    { engine = 2; m = 16; }
    else if (!strcmp(cfg, "tiltonly"))  { engine = 3; m = 16; }
    else { fprintf(stderr, "unknown config\n"); return 1; }
    if (load_seeds("seeds.json")) return 1;

    // bound seeds: precession / prograde / period / crossings (cycle 1)
    int prec_pass = 0, prog_pass = 0, per_pass = 0;
    double worst_prec = 0, worst_per = 0;
    double cross_counts[256];
    for (int i = 0; i < 256; i++) {
        double E, L; bound_constants(sb_p[i], sb_e[i], &E, &L);
        CycM cyc[4];
        double u0 = (1.0 + sb_e[i]) / sb_p[i];
        int n = walk_bound(engine, m, E, L, u0, 2, cyc, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0);
        double adv_GR = periapsis_elliptic(sb_p[i], sb_e[i]);
        double T_GR = bound_period_quad_t(sb_p[i], sb_e[i]);
        if (n >= 2 && cyc[0].dphi > 0) {
            double adv = cyc[0].dphi - 2*PI;
            if (fabs(adv - adv_GR) <= 0.01 * adv_GR) prec_pass++;
            else worst_prec = fmax(worst_prec, fabs(adv - adv_GR)/adv_GR);
            if (adv > 0) prog_pass++;
            if (fabs(cyc[0].dt - T_GR) <= 0.001 * T_GR) per_pass++;
            else worst_per = fmax(worst_per, fabs(cyc[0].dt - T_GR)/T_GR);
            cross_counts[i] = (double)cyc[0].cross;
        } else {
            cross_counts[i] = -1;
            if (!(n >= 2)) { worst_prec = fmax(worst_prec, 1e9); worst_per = fmax(worst_per, 1e9); }
        }
    }
    qsort(cross_counts, 256, sizeof(double), dblcmp);
    double median_cross = cross_counts[128] > 0 ? cross_counts[128] : cross_counts[130];

    // light
    int defl_pass = 0; double worst_defl = 0;
    for (int i = 0; i < 64; i++) {
        double b = sb_light[i];
        double d = run_light(engine, m, b, NULL, NULL, NULL, 0);
        double dor = deflection_quadrature(b);
        if (d > 0 && fabs(d - dor) <= 0.01 * dor) defl_pass++;
        else worst_defl = fmax(worst_defl, d > 0 ? fabs(d - dor)/dor : 1e9);
    }

    // capture
    int misclass = 0;
    double capL[6] = { 0.5, 0.9, 0.97, 1.03, 1.1, 1.5 };
    for (int i = 0; i < 6; i++) {
        int out = run_capture(engine, m, 0, 4.0*capL[i]);
        if (out != exact_captured_massive(4.0*capL[i])) misclass++;
    }
    double capB[4] = { 0.9, 0.97, 1.03, 1.1 };
    for (int i = 0; i < 4; i++) {
        double b = 3.0*sqrt(3.0)*capB[i];
        int out = run_capture(engine, m, 1, b);
        if (out != exact_captured_photon(b)) misclass++;
    }

    int isco = run_isco_bound(engine, m) && run_isco_plunge(engine, m);

    // long runs: first 32 seeds, 1e4 cycles
    int shape_pass = 0, repeat_pass = 0;
    for (int i = 0; i < 32; i++) {
        double E, L; bound_constants(sb_p[i], sb_e[i], &E, &L);
        double u0 = (1.0 + sb_e[i]) / sb_p[i];
        CycM *cyc = malloc(10000 * sizeof(CycM));
        int seq1[MAXSEQ], n1 = 0, seq2[MAXSEQ], n2 = 0;
        int n = walk_bound(engine, m, E, L, u0, 10000, cyc, seq1, &n1, seq2, &n2, NULL, NULL, NULL, 0);
        if (n == 10000) {
            bool shape = true, rep = true;
            if (n1 != n2) rep = false;
            else for (int q = 0; q < n1; q++) if (seq1[q] != seq2[q]) { rep = false; break; }
            for (int c = 1; c < 10000 && rep; c++)
                if (!(fabs(cyc[c].dphi - cyc[0].dphi) <= 1e-12*fabs(cyc[0].dphi) &&
                      fabs(cyc[c].dt - cyc[0].dt) <= 1e-12*fabs(cyc[0].dt))) rep = false;
            for (int c = 0; c < 10000; c++)
                if (!(fabs(cyc[c].r_peri - cyc[0].r_peri) <= 0.01*cyc[0].r_peri &&
                      fabs(cyc[c].r_apo - cyc[0].r_apo) <= 0.01*cyc[0].r_apo)) { shape = false; break; }
            if (shape) shape_pass++;
            if (rep) repeat_pass++;
        }
        free(cyc);
    }

    // picture traces
    {
        char fn[256]; snprintf(fn, sizeof fn, "trace-%s.json", cfg);
        FILE *f = fopen(fn, "w");
        double E, L; bound_constants(20.0, 0.5, &E, &L);
        static double tx[400000], ty[400000]; int tn = 0;
        static CycM tcyc[8];
        walk_bound(engine, m, E, L, 1.5/20.0, 5, tcyc, NULL, NULL, NULL, NULL, tx, ty, &tn, 400000);
        fprintf(f, "{\"orbit\":[");
        for (int i = 0; i < tn; i++) fprintf(f, "%s[%.5f,%.5f]", i ? "," : "", tx[i], ty[i]);
        fprintf(f, "],\"light\":[");
        double lb[5] = { 10, 30, 100, 300, 1000 };
        for (int i = 0; i < 5; i++) {
            static double lx[400000], ly[400000]; int ln = 0;
            run_light(engine, m, lb[i], lx, ly, &ln, 400000);
            fprintf(f, "%s{\"b\":%g,\"pts\":[", i ? "," : "", lb[i]);
            for (int q = 0; q < ln; q++) fprintf(f, "%s[%.5f,%.5f]", q ? "," : "", lx[q], ly[q]);
            fprintf(f, "]}");
        }
        fprintf(f, "]}\n");
        fclose(f);
    }

    char out[256]; snprintf(out, sizeof out, "metrics-%s.json", cfg);
    FILE *o = fopen(out, "w");
    fprintf(o, "{\n");
    fprintf(o, " \"precession_pass_fraction\": %.6f,\n", prec_pass / 256.0);
    fprintf(o, " \"prograde_fraction\": %.6f,\n", prog_pass / 256.0);
    fprintf(o, " \"period_pass_fraction\": %.6f,\n", per_pass / 256.0);
    fprintf(o, " \"deflection_pass_fraction\": %.6f,\n", defl_pass / 64.0);
    fprintf(o, " \"capture_misclassified\": %d,\n", misclass);
    fprintf(o, " \"isco_correct\": %d,\n", isco);
    fprintf(o, " \"shape_kept_fraction\": %.6f,\n", shape_pass / 32.0);
    fprintf(o, " \"cycle_repeat_fraction\": %.6f,\n", repeat_pass / 32.0);
    fprintf(o, " \"crossings_per_cycle\": %.3f,\n", median_cross);
    fprintf(o, " \"_worst_prec_rel\": %.3e,\n", worst_prec);
    fprintf(o, " \"_worst_period_rel\": %.3e,\n", worst_per);
    fprintf(o, " \"_worst_defl_rel\": %.3e\n", worst_defl);
    fprintf(o, "}\n");
    fclose(o);
    printf("%s: prec %d/256 prog %d/256 per %d/256 defl %d/64 cap %d isco %d shape %d/32 repeat %d/32 cross %.1f\n",
           cfg, prec_pass, prog_pass, per_pass, defl_pass, misclass, isco, shape_pass, repeat_pass, median_cross);
    return 0;
}
