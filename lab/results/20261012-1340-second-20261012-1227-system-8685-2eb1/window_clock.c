// window_clock.c — run 20261012-1340-second (second author on 20261012-1227-system-8685)
//
// Float replica of the plane's Wisdom-Holman drift-kick-drift split for one test
// particle + one planet on a fixed circular orbit about a static star (mu=1).
// Variants differ ONLY in when the kick happens:
//   uN        uniform, one kick every P_body/N          (u64 = the plane's rule)
//   wW        kicks only while |wrapPi(lambda_b - lambda_p)| < W, at local step P/64
//   wWsegK    as wW, plus one kick per accumulated K micro-steps outside windows
//             (force sampled at the LAST step's midpoint, weight = full gap;
//              accumulated gap DISCARDED at window entry — the original seg8 rule)
//       segKm  same, but force sampled at the segment MIDPOINT (stashed state)
//       segKn  same, but the pending gap is kicked at window entry (no drop)
//       segKmn both
//   wWpK      ORBIT-ANCHORED rebuild (the checker's named experiment): outside
//             windows the step goes exactly to the next mean-longitude grid
//             multiple of 2*pi/K and carries one kick kw=h evaluated at the step
//             midpoint; inside windows fine P/64 kicks as wW; steps are capped at
//             window boundaries so no forcing is dropped or double-counted.
//   (truth = u2048 / u4096, same scheme, fine uniform)
//
// u/w/segK-plain reproduce run 20261012-1227 bit-identically (verified).
//
// Usage: window_clock <config> <variant> <nseeds>
//   config: encounter | resonant | belt
// CSV rows on stdout (see main).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

static double MU_P, A_P, N_P;   // planet mass ratio, orbital radius, mean motion

static unsigned long long rng_state;
static double urand(void) {     // splitmix64 -> [0,1)
    rng_state += 0x9E3779B97F4A7C15ULL;
    unsigned long long z = rng_state;
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    z = z ^ (z >> 31);
    return (double)(z >> 11) / 9007199254740992.0;
}

static double wrapPi(double a) {
    while (a >  M_PI) a -= 2.0 * M_PI;
    while (a < -M_PI) a += 2.0 * M_PI;
    return a;
}

typedef struct { double x, y, vx, vy; } State;

typedef struct { double a, e, varpi, M, n; int bad; } Elem;

static Elem elements(const State *s) {
    Elem el; el.bad = 0;
    double r = hypot(s->x, s->y);
    double v2 = s->vx * s->vx + s->vy * s->vy;
    double E = 0.5 * v2 - 1.0 / r;
    if (E >= -1e-13) { el.bad = 1; el.a = 1; el.e = 2; el.varpi = 0; el.M = 0; el.n = 0; return el; }
    double a = -0.5 / E;
    double rv = s->x * s->vx + s->y * s->vy;
    double c = v2 - 1.0 / r;
    double ex = c * s->x - rv * s->vx;
    double ey = c * s->y - rv * s->vy;
    double e = hypot(ex, ey);
    el.a = a; el.e = e; el.n = pow(a, -1.5);
    if (e < 1e-11) {
        el.varpi = atan2(s->y, s->x);
        el.M = 0.0; // circular: varpi already set to the position angle
    } else {
        el.varpi = atan2(ey, ex);
        double cosnu = (ex * s->x + ey * s->y) / (e * r);
        double sinnu = (ex * s->y - ey * s->x) / (e * r);
        if (cosnu > 1) cosnu = 1; if (cosnu < -1) cosnu = -1;
        double Ea = atan2(sqrt(1.0 - e * e) * sinnu, e + cosnu);
        el.M = Ea - e * sin(Ea);
    }
    return el;
}

static double solveE(double M, double e) {
    M = fmod(M, 2.0 * M_PI); if (M < 0) M += 2.0 * M_PI;
    double E = M + e * sin(M);
    for (int i = 0; i < 60; i++) {
        double f = E - e * sin(E) - M;
        double d = f / (1.0 - e * cos(E));
        if (d > 0.6) d = 0.6; if (d < -0.6) d = -0.6;
        E -= d;
        if (fabs(d) < 1e-14) break;
    }
    return E;
}

// exact Kepler drift of s by h (mu = 1); returns 0 ok, 1 unbound
static int drift(State *s, double h) {
    Elem el = elements(s);
    if (el.bad) return 1;
    double E = solveE(el.M + el.n * h, el.e);
    double ca = cos(el.varpi), sa = sin(el.varpi);
    double cE = cos(E), sE = sin(E);
    double sq = sqrt(1.0 - el.e * el.e);
    double px = el.a * (cE - el.e), py = el.a * sq * sE;
    double dEdt = el.n / (1.0 - el.e * cE);
    double pvx = -el.a * sE * dEdt, pvy = el.a * sq * cE * dEdt;
    s->x  = ca * px - sa * py;  s->y  = sa * px + ca * py;
    s->vx = ca * pvx - sa * pvy; s->vy = sa * pvx + ca * pvy;
    return 0;
}

// planet position at time t
static void planet(double t, double *px, double *py) {
    double th = N_P * t;
    *px = A_P * cos(th); *py = A_P * sin(th);
}

// perturbing acceleration at state s, time t (one eval = one kick cost unit)
static void accel(const State *s, double t, double *ax, double *ay) {
    double px, py; planet(t, &px, &py);
    double dx = s->x - px, dy = s->y - py;
    double d2 = dx * dx + dy * dy;
    double d = sqrt(d2);
    double f = -MU_P / (d2 * d);
    *ax = f * dx; *ay = f * dy;
}

static double jacobi(const State *s, double t) {
    double px, py; planet(t, &px, &py);
    double r = hypot(s->x, s->y);
    double d = hypot(s->x - px, s->y - py);
    double vr_x = s->vx + N_P * s->y, vr_y = s->vy - N_P * s->x;
    return 2.0 * (1.0 / r + MU_P / d) - (vr_x * vr_x + vr_y * vr_y);
}

typedef struct {
    long long kicks, solves, windows;
    double varpi_rate, e_rate, jacobi_max, a_end, e_end;
    int ejected_at_sample; // -1 none
    int nfit;
} Result;

// forward time for the synodic angle to reach boundary tb, moving at rate nsyn
static double dtb(double th, double tb, double nsyn) {
    double d;
    if (nsyn > 0) { d = tb - th; while (d <= 0) d += 2.0 * M_PI; }
    else          { d = th - tb; while (d <= 0) d += 2.0 * M_PI; }
    return d / fabs(nsyn);
}

// variant: 'u' N | 'w' W | 's' W with par2 seg-steps, fmid/fnd ablation flags | 'p' W with par2 grid/orbit
static Result simulate(double a0, double e0, double varpi0, double M0,
                       char kind, double par, double par2, int fmid, int fnd, double T) {
    Result R; memset(&R, 0, sizeof R); R.ejected_at_sample = -1;
    State s;
    {   // initial state from elements
        double E = solveE(M0, e0);
        double n = pow(a0, -1.5), sq = sqrt(1.0 - e0 * e0);
        double ca = cos(varpi0), sa = sin(varpi0);
        double px = a0 * (cos(E) - e0), py = a0 * sq * sin(E);
        double dEdt = n / (1.0 - e0 * cos(E));
        double pvx = -a0 * sin(E) * dEdt, pvy = a0 * sq * cos(E) * dEdt;
        s.x = ca * px - sa * py; s.y = sa * px + ca * py;
        s.vx = ca * pvx - sa * pvy; s.vy = sa * pvx + ca * pvy;
    }
    double C0 = jacobi(&s, 0.0);
    R.jacobi_max = 0.0;
    double P_p = 2.0 * M_PI / N_P;
    int nsamp = (int)(T / P_p) + 1;
    double *sv_t = malloc(nsamp * sizeof(double)), *sv_v = malloc(nsamp * sizeof(double));
    double *sv_e = malloc(nsamp * sizeof(double)), *sv_C = malloc(nsamp * sizeof(double));
    double varpi_prev = varpi0, varpi_acc = varpi0;
    double t = 0.0; int ejected = 0; double gap = 0.0;
    int next_s = 1;
    int jseg = 0; double smt = -1.0; State sms; memset(&sms, 0, sizeof sms);
    while (t < T) {
        if (ejected) break;
        Elem el = elements(&s);
        if (el.bad || el.e > 0.95 || el.a > 10.0) { ejected = 1; break; }
        double h = (2.0 * M_PI / el.n) / 64.0;          // micro step: P_current/64
        if (kind == 'u') h = (2.0 * M_PI / el.n) / par; // uniform variant step
        if (kind == 'p') {
            // orbit-anchored rebuild: outside windows step exactly to the next
            // mean-longitude grid multiple of 2*pi/par2; inside windows fine
            // P/64 steps; both capped at window boundaries (+1e-6 overshoot so
            // the boundary is crossed, never re-approached).
            double lam = el.varpi + el.M;
            double th = wrapPi(lam - N_P * t);
            double nsyn = el.n - N_P;
            double micro = (2.0 * M_PI / el.n) / 64.0;
            int inwin = (fabs(th) <= par);
            if (!inwin && fabs(nsyn) > 1e-12) {
                double te = dtb(th, -par, nsyn);
                double te2 = dtb(th, par, nsyn);
                if (te2 < te) te = te2;
                if (te < micro * 0.5) inwin = 1;   // about to enter: go fine now
            }
            if (inwin) {
                if (fabs(nsyn) > 1e-12 && par < M_PI - 1e-9) {
                    double tx = dtb(th, -par, nsyn);
                    double tx2 = dtb(th, par, nsyn);
                    if (tx2 < tx) tx = tx2;
                    if (tx < h) h = tx + 1e-6;
                }
            } else {
                double g = 2.0 * M_PI / par2;
                double fl = fmod(lam, g); if (fl < 0) fl += g;
                double d = g - fl; if (d < g * 1e-6) d = g;   // on-point float noise: full segment
                h = d / el.n;
                if (fabs(nsyn) > 1e-12 && par < M_PI - 1e-9) {
                    double te = dtb(th, -par, nsyn);
                    double te2 = dtb(th, par, nsyn);
                    if (te2 < te) te = te2;
                    if (te < h) h = te + 1e-6;
                }
            }
        }
        if (t + h > T) h = T - t;
        if (h < 1e-9) h = 1e-9;                     // never stall the clock
        // proximity refinement (the plane's shells): inside 3 Hill radii resolve the
        // encounter timescale by 8, for every variant alike
        { double px, py; planet(t, &px, &py);
          double dx = s.x - px, dy = s.y - py, d = hypot(dx, dy);
          double shell = 3.0 * A_P * cbrt(MU_P / 3.0);
          if (d < shell) { double pvx = -N_P * py, pvy = N_P * px;
            double rvx = s.vx - pvx, rvy = s.vy - pvy;
            double vrel = hypot(rvx, rvy) + 1e-9;
            double hh = d / (8.0 * vrel);
            if (hh < h) h = hh; } }
        // sample boundaries: sample strictly on planet-period grid before stepping past
        while (next_s < nsamp && (double)next_s * P_p <= t + 1e-9) {
            Elem e2 = elements(&s);
            double v = e2.varpi, d = wrapPi(v - varpi_prev); varpi_prev = v; varpi_acc += d;
            sv_t[next_s] = t; sv_v[next_s] = varpi_acc; sv_e[next_s] = e2.e; sv_C[next_s] = jacobi(&s, t);
            double dC = fabs(sv_C[next_s] - C0); if (dC > R.jacobi_max) R.jacobi_max = dC;
            if (e2.bad || e2.e > 0.95) { ejected = 1; }
            next_s++;
            if (ejected) break;
        }
        if (ejected) break;
        // --- one DKD step ---
        double half = 0.5 * h;
        if (drift(&s, half)) { ejected = 1; break; }
        R.solves++;
        int do_kick; double kw = h;
        if (kind == 'u') do_kick = 1;
        else if (kind == 'p') do_kick = 1;           // every step; midpoint-sampled
        else {
            double lam = atan2(s.y, s.x);
            double th = wrapPi(lam - N_P * (t + half));
            int in_win = fabs(th) < par;
            if (in_win) {
                if (kind == 's' && fnd && gap > 0.0) {
                    // no-drop ablation: deliver the pending segment at entry
                    double ax, ay; accel(&s, t + half, &ax, &ay);
                    s.vx += gap * ax; s.vy += gap * ay;
                    R.kicks++;
                }
                do_kick = 1; gap = 0.0; jseg = 0; smt = -1.0;
            } else {
                do_kick = 0;
                if (kind == 's') {
                    jseg++;
                    if (fmid && jseg == (int)(par2 / 2)) { sms = s; smt = t + half; }
                    gap += h;
                    if (gap >= par2 * h) { do_kick = 1; kw = gap; gap = 0.0; jseg = 0; }
                }
            }
        }
        if (do_kick) {
            double ax, ay;
            if (kind == 's' && fmid && kw > h && smt >= 0.0) {
                accel(&sms, smt, &ax, &ay);           // segment midpoint sampling
            } else {
                accel(&s, t + half, &ax, &ay);
            }
            s.vx += kw * ax; s.vy += kw * ay;
            R.kicks++;
            if (kind == 's' && fmid) smt = -1.0;
        }
        if (drift(&s, half)) { ejected = 1; break; }
        R.solves++;
        t += h;
    }
    // window count: recompute cheaply is not needed; derive from kicks for w variants later
    Elem elf = elements(&s);
    R.a_end = elf.a; R.e_end = elf.e;
    // fits over valid samples (>= 60% of T)
    int n_ok = next_s - 1;
    R.nfit = 0;
    if (n_ok > 0.6 * nsamp) {
        // least-squares slopes
        double st = 0, sv = 0, stt = 0, stv = 0, se = 0, ste = 0, n = 0;
        for (int i = 0; i < n_ok; i++) {
            n += 1; st += sv_t[i]; sv += sv_v[i]; stt += sv_t[i]*sv_t[i]; stv += sv_t[i]*sv_v[i];
            se += sv_e[i]; ste += sv_t[i]*sv_e[i];
        }
        double den = n * stt - st * st;
        if (fabs(den) > 0) {
            R.varpi_rate = (n * stv - st * sv) / den;
            R.e_rate = (n * ste - st * se) / den;
            R.nfit = (int)n;
        }
    }
    if (ejected && R.ejected_at_sample < 0) R.ejected_at_sample = next_s - 1;
    else if (!ejected) R.ejected_at_sample = -1;
    else R.ejected_at_sample = n_ok;
    free(sv_t); free(sv_v); free(sv_e); free(sv_C);
    return R;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s config variant nseeds [seed0]\n", argv[0]); return 2; }
    const char *config = argv[1], *vname = argv[2];
    int nseeds = atoi(argv[3]);
    int seed0 = (argc > 4) ? atoi(argv[4]) : 0;
    double a0, e0;
    if (!strcmp(config, "encounter")) { a0 = 1.25; e0 = 0.05; MU_P = 1e-4; A_P = 1.0; }
    else if (!strcmp(config, "resonant")) { a0 = 1.5874; e0 = 0.05; MU_P = 1e-4; A_P = 1.0; }
    else if (!strcmp(config, "belt"))     { a0 = 1.0;  e0 = 0.05; MU_P = 1e-3; A_P = 5.2; }
    else { fprintf(stderr, "bad config\n"); return 2; }
    N_P = pow(A_P, -1.5);
    double T = 1000.0 * 2.0 * M_PI / N_P;
    if (!strcmp(config, "belt")) T = 500.0 * 2.0 * M_PI / N_P; // 5930 body orbits; keeps runtime sane
    char kind; double par, par2 = 8.0; int fmid = 0, fnd = 0;
    if (vname[0] == 'u') { kind = 'u'; par = atof(vname + 1); }
    else if (vname[0] == 'w') {
        const char *sp = strstr(vname, "seg");
        const char *pp = strchr(vname, 'p');
        if (sp) {
            kind = 's'; par = atof(vname + 1);
            const char *q = sp + 3; par2 = 0;
            while (*q >= '0' && *q <= '9') { par2 = par2 * 10 + (*q - '0'); q++; }
            if (par2 < 1) par2 = 8;
            for (; *q; q++) { if (*q == 'm') fmid = 1; if (*q == 'n') fnd = 1; }
        } else if (pp) { kind = 'p'; par = atof(vname + 1); par2 = atof(pp + 1); }
        else    { kind = 'w'; par = atof(vname + 1); }
    } else { fprintf(stderr, "bad variant\n"); return 2; }
    printf("config,variant,seed,kicks,solves,varpi_rate,e_rate,jacobi_max,a_end,e_end,ejected_at_sample,nfit\n");
    for (int seed = seed0; seed < seed0 + nseeds; seed++) {
        rng_state = 0x20261012ULL + 1000ULL * (unsigned)(config[0]*7+config[1]*3+config[2]) + seed;
        (void)urand();
        double varpi0 = urand() * 2 * M_PI;
        double M0 = urand() * 2 * M_PI;
        Result R = simulate(a0, e0, varpi0, M0, kind, par, par2, fmid, fnd, T);
        printf("%s,%s,%d,%lld,%lld,%.6e,%.6e,%.3e,%.6f,%.6f,%d,%d\n",
               config, vname, seed, R.kicks, R.solves, R.varpi_rate, R.e_rate,
               R.jacobi_max, R.a_end, R.e_end, R.ejected_at_sample, R.nfit);
    }
    return 0;
}
