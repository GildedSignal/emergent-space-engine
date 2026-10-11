/* Belt surprise-rate instrument: Wisdom-Holman (exact Kepler drift + heliocentric
 * mutual kicks with the indirect term, DKD split) for a 2D belt of N equal masses
 * around one star, with a Benettin shadow body set for the largest Lyapunov exponent.
 *
 * Faithful to docs/law.md's cheap path: compiled drift (exact two-body), kicks carry
 * everything else, fixed step shared by all bodies, doll's origin falls (indirect term).
 *
 * Usage: belt_lyap N mu_belt sigma_e steps_per_orbit orbits seed out_curve.dat [--selftest]
 * Prints one summary line: RESULT N mu sigma spon orbits seed lambda_raw L T dH_rel nren fallback
 * Curve file: lines "t_orbits L" at each renormalisation (t in mean-orbit units).
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

typedef struct { double *x, *y, *vx, *vy; int n; } State;

static State st_new(int n) {
    State s; s.n = n;
    s.x = malloc(sizeof(double)*n); s.y = malloc(sizeof(double)*n);
    s.vx = malloc(sizeof(double)*n); s.vy = malloc(sizeof(double)*n);
    return s;
}

/* xorshift64* deterministic rng */
static unsigned long long rng;
static double urand(void) {
    rng ^= rng >> 12; rng ^= rng << 25; rng ^= rng >> 27;
    return (double)((rng * 2685821657736338717ULL) >> 11) / 9007199254740992.0;
}

static long g_fallback = 0;

/* conjunction census (does not touch the dynamics): per-pair minimum sampled
 * separation over the run, counted once per pair. --conj enables it. */
static double *g_rmin2 = NULL;   /* pair-indexed min r^2, main state only */
static int g_conj = 0;
static long pair_id(int n, int i, int j) { return (long)i*n - (long)i*(i+1)/2 + (j - i - 1); }

/* Exact Kepler drift about the star (mu = GM* = 1) from t to t+dt, 2D.
 * Self-consistent pericentre frame built from the state itself. */
static void drift_body(double *x, double *y, double *vx, double *vy, double dt) {
    double r2 = (*x)*(*x) + (*y)*(*y), v2 = (*vx)*(*vx) + (*vy)*(*vy);
    double rv = (*x)*(*vx) + (*y)*(*vy);
    double ir = 1.0/sqrt(r2);
    double a = 1.0/(2.0*ir - v2);            /* mu=1 */
    double n = pow(a, -1.5);
    double ex = (v2 - ir)*(*x) - rv*(*vx);
    double ey = (v2 - ir)*(*y) - rv*(*vy);
    double e = sqrt(ex*ex + ey*ey);
    if (a <= 0 || e >= 0.999) { *x += *vx*dt; *y += *vy*dt; g_fallback++; return; }
    double px, py;                            /* pericentre direction */
    if (e < 1e-8) {
        /* circular limit: the anomaly is pure cancellation noise; an exact
         * rotation by n*dt is the right drift and preserves r, |v| bit-cheaply */
        double c = cos(n*dt), s = sin(n*dt);
        (void)px; (void)py;
        double xn = (*x)*c - (*y)*s, yn = (*x)*s + (*y)*c;
        double vxn = (*vx)*c - (*vy)*s, vyn = (*vx)*s + (*vy)*c;
        *x = xn; *y = yn; *vx = vxn; *vy = vyn;
        return;
    }
    px = ex/e; py = ey/e;
    double qx = -py, qy = px;
    double cosE = 1.0 - r2*ir/a, sinE = rv/sqrt(a);   /* sinE = rv/(n a^2) = rv*sqrt(a)/a^2 = rv/sqrt(a^3)... n a^2 = a^0.5 */
    double E0 = atan2(sinE, cosE);
    double M0 = E0 - e*sin(E0);
    double M1 = M0 + n*dt;
    M1 = fmod(M1, 2.0*M_PI); if (M1 < 0) M1 += 2.0*M_PI;
    double E = M1 + e*sin(M1);
    for (int k = 0; k < 60; k++) {
        double f = E - e*sin(E) - M1;
        double fp = 1.0 - e*cos(E);
        double dE = f/fp; E -= dE;
        if (fabs(dE) < 1e-15) break;
    }
    double cE = cos(E), sE = sin(E);
    double X = a*(cE - e), Y = a*sqrt(1-e*e)*sE;
    double den = 1.0 - e*cE;
    double VX = -a*n*sE/den, VY = a*n*sqrt(1-e*e)*cE/den;
    *x = px*X + qx*Y; *y = py*X + qy*Y;
    *vx = px*VX + qx*VY; *vy = py*VX + qy*VY;
}

static void drift_all(State *s, double dt) {
    for (int i = 0; i < s->n; i++)
        drift_body(&s->x[i], &s->y[i], &s->vx[i], &s->vy[i], dt);
}

/* heliocentric mutual kicks + indirect term (origin falls), masses m each */
static void kick_all(State *s, double m, double dt, int census) {
    int n = s->n;
    double *ax = malloc(sizeof(double)*n), *ay = malloc(sizeof(double)*n);
    /* indirect term: the belt's pull on the star (the doll's origin falls) */
    double axs = 0, ays = 0;
    for (int j = 0; j < n; j++) {
        double r2j = s->x[j]*s->x[j]+s->y[j]*s->y[j];
        double invj = 1.0/(r2j*sqrt(r2j));
        axs += m*s->x[j]*invj; ays += m*s->y[j]*invj;
    }
    #pragma omp parallel for schedule(static)
    for (int i = 0; i < n; i++) {
        double axi = -axs, ayi = -ays, xi = s->x[i], yi = s->y[i];
        for (int j = 0; j < n; j++) {
            if (j == i) continue;
            double dx = s->x[j]-xi, dy = s->y[j]-yi;
            double r2 = dx*dx+dy*dy, inv = 1.0/(r2*sqrt(r2));
            axi += m*dx*inv; ayi += m*dy*inv;
            if (census && j > i && r2 < g_rmin2[pair_id(n,i,j)]) g_rmin2[pair_id(n,i,j)] = r2;
        }
        ax[i] = axi; ay[i] = ayi;
    }
    for (int i = 0; i < n; i++) { s->vx[i] += ax[i]*dt; s->vy[i] += ay[i]*dt; }
    free(ax); free(ay);
}

static double energy(State *s, double m) {
    double H = 0;
    for (int i = 0; i < s->n; i++) {
        double r = sqrt(s->x[i]*s->x[i]+s->y[i]*s->y[i]);
        H += 0.5*m*(s->vx[i]*s->vx[i]+s->vy[i]*s->vy[i]) - m/r;   /* star mu=1 */
        for (int j = i+1; j < s->n; j++) {
            double dx = s->x[j]-s->x[i], dy = s->y[j]-s->y[i];
            H -= m*m/sqrt(dx*dx+dy*dy);
        }
    }
    return H;
}

int main(int argc, char **argv) {
    if (argc < 8) { fprintf(stderr, "args\n"); return 2; }
    int N = atoi(argv[1]);
    double mu = atof(argv[2]);          /* belt total mass / star */
    double sigma_e = atof(argv[3]);
    double spon = atof(argv[4]);        /* steps per orbit at a=1 */
    double orbits = atof(argv[5]);
    unsigned seed = (unsigned)atoi(argv[6]);
    const char *curve_path = argv[7];

    if (argc > 8 && !strcmp(argv[8], "--selftest")) {
        State t = st_new(1);
        t.x[0]=1; t.y[0]=0; t.vx[0]=0; t.vy[0]=1;
        for (int k=0;k<10000;k++) drift_body(&t.x[0],&t.y[0],&t.vx[0],&t.vy[0],2*M_PI/10000);
        double err = fabs(t.x[0]-1)+fabs(t.y[0])+fabs(t.vx[0])+fabs(t.vy[0]-1);
        printf("SELFTEST roundtrip err %.3e\n", err);
        if (err > 1e-9) return 4;
        /* elliptic e=0.3 roundtrip: one full period */
        double a=1.0,e=0.3,n=sqrt(1.0);
        double p=a*(1-e*e), r=p/(1+e), th=0.0;
        double x=r, y=0, vx=0, vy=sqrt(1.0/p)*(1+e);
        for (int k=0;k<100000;k++) drift_body(&x,&y,&vx,&vy,2*M_PI/(n*100000));
        double err2 = fabs(x-r)+fabs(y)+fabs(vx)+fabs(vy-sqrt(1.0/p)*(1+e));
        printf("SELFTEST e0.3 err %.3e\n", err2);
        if (err2 > 1e-8) return 5;
        return 0;
    }

    rng = 0x9E3779B97F4A7C15ULL ^ (seed*0xBF58476D1CE4E5B9ULL + 0x94D049BB133111EBULL);
    for (int k = 0; k < 20; k++) urand();
    double m = mu / N;

    State s = st_new(N), sh = st_new(N);
    for (int i = 0; i < N; i++) {
        double a = 0.95 + 0.10*urand();       /* uniform a in [0.95,1.05]: cold, 10%-wide belt */
        double e = sigma_e*sqrt(-2*log(1-urand()*0.99998));  /* Rayleigh */
        if (e > 0.6) e = 0.6;
        double om = 2*M_PI*urand(), f = 2*M_PI*urand();
        double p = a*(1-e*e);
        double r = p/(1+e*cos(f)), vt = sqrt(1.0/p)*(1+e*cos(f)), vr = sqrt(1.0/p)*e*sin(f);
        double c1 = cos(om), s1 = sin(om), cf = cos(f), sf = sin(f);
        double xr = r*cf, yr = r*sf;
        s.x[i] = c1*xr - s1*yr; s.y[i] = s1*xr + c1*yr;
        double vxc = vr*cf - vt*sf, vyc = vr*sf + vt*cf;
        s.vx[i] = c1*vxc - s1*vyc; s.vy[i] = s1*vxc + c1*vyc;
    }
    /* deterministic shadow offset: total norm exactly d0 across all 4N components */
    const double d0 = 1e-8;
    {
        double nrm = 0;
        for (int i = 0; i < N; i++) {
            double th = 2*M_PI*0.6180339887498949*i;
            sh.x[i]=s.x[i]+d0*cos(th); sh.y[i]=s.y[i]+d0*sin(th);
            sh.vx[i]=s.vx[i]+d0*cos(th+1.0); sh.vy[i]=s.vy[i]+d0*sin(th+1.0);
        }
        for (int i = 0; i < N; i++)
            nrm += sh.x[i]*sh.x[i]+sh.y[i]*sh.y[i]+sh.vx[i]*sh.vx[i]+sh.vy[i]*sh.vy[i];
        nrm = sqrt(nrm);
        /* subtract the base-state norm: offset vectors only (base is huge; compute offset norm directly) */
        double on = 0;
        for (int i = 0; i < N; i++) {
            double ox = d0*cos(2*M_PI*0.6180339887498949*i), oy = d0*sin(2*M_PI*0.6180339887498949*i);
            double ovx = d0*cos(2*M_PI*0.6180339887498949*i+1.0), ovy = d0*sin(2*M_PI*0.6180339887498949*i+1.0);
            on += ox*ox+oy*oy+ovx*ovx+ovy*ovy;
        }
        on = sqrt(on);
        double sc = d0/on;
        for (int i = 0; i < N; i++) {
            double th = 2*M_PI*0.6180339887498949*i;
            sh.x[i]=s.x[i]+d0*cos(th)*sc; sh.y[i]=s.y[i]+d0*sin(th)*sc;
            sh.vx[i]=s.vx[i]+d0*cos(th+1.0)*sc; sh.vy[i]=s.vy[i]+d0*sin(th+1.0)*sc;
        }
        (void)nrm;
    }
    if (argc > 8 && !strcmp(argv[8], "--conj")) {
        g_conj = 1;
        long np = (long)N*(N-1)/2;
        g_rmin2 = malloc(sizeof(double)*np);
        for (long p = 0; p < np; p++) g_rmin2[p] = 1e300;
    }
    double H0 = energy(&s, m);
    double dt = 2*M_PI/spon;
    double dmax = 100*d0;
    FILE *cur = fopen(curve_path, "w");
    double L = 0; int nren = 0;
    long total_steps = (long)(orbits*spon);
    double t_orb = 0;
    for (long k = 0; k < total_steps; k++) {
        drift_all(&s, dt/2); drift_all(&sh, dt/2);
        kick_all(&s, m, dt, g_conj);  kick_all(&sh, m, dt, 0);
        drift_all(&s, dt/2); drift_all(&sh, dt/2);
        t_orb += dt/(2*M_PI);
        double d2 = 0;
        for (int i = 0; i < N; i++) {
            double dx = sh.x[i]-s.x[i], dy = sh.y[i]-s.y[i];
            double dvx = sh.vx[i]-s.vx[i], dvy = sh.vy[i]-s.vy[i];
            d2 += dx*dx+dy*dy+dvx*dvx+dvy*dvy;
        }
        double d = sqrt(d2);
        if (d > dmax || d < d0*1e-3) {
            L += log(d/d0);
            fprintf(cur, "%.6f %.6f\n", t_orb, L);
            double sc = d0/d;
            for (int i = 0; i < N; i++) {
                sh.x[i] = s.x[i] + (sh.x[i]-s.x[i])*sc;
                sh.y[i] = s.y[i] + (sh.y[i]-s.y[i])*sc;
                sh.vx[i] = s.vx[i] + (sh.vx[i]-s.vx[i])*sc;
                sh.vy[i] = s.vy[i] + (sh.vy[i]-s.vy[i])*sc;
            }
            nren++;
        }
    }
    fclose(cur);
    double H1 = energy(&s, m);
    double dh = (fabs(H0) > 1e-300) ? fabs(H1-H0)/fabs(H0) : 0.0;
    printf("RESULT %d %.6g %.4g %.6g %.6g %u %.8g %.6g %.4g %.3e %d %ld\n",
           N, mu, sigma_e, spon, t_orb, seed,
           L/(t_orb>0?t_orb:1), L, t_orb, dh, nren, g_fallback);
    if (g_conj) {
        long np = (long)N*(N-1)/2;
        double minr = 1e300;
        long n_sqrt = 0, n_kill3 = 0, n_3rh = 0, n_10rh = 0;
        double m1 = mu/N, dtk = 2*M_PI/spon;
        double r_sqrt  = sqrt(m1*dtk);               /* dossier's d_kill      */
        double r_kill3 = pow(m1*dtk*dtk, 1.0/3.0);   /* deflection-per-step r */
        double rh      = pow(2.0*m1/3.0, 1.0/3.0);   /* mutual Hill radius    */
        for (long p = 0; p < np; p++) {
            if (g_rmin2[p] >= 1e300) continue;
            double r = sqrt(g_rmin2[p]);
            if (r < minr) minr = r;
            if (r < r_sqrt)  n_sqrt++;
            if (r < r_kill3) n_kill3++;
            if (r < 3*rh)    n_3rh++;
            if (r < 10*rh)   n_10rh++;
        }
        printf("CONJ %d %.6g %.6g %u %.6e %.6e %.6e %.6e %ld %ld %ld %ld\n",
               N, mu, spon, seed, minr, r_sqrt, r_kill3, rh,
               n_sqrt, n_kill3, n_3rh, n_10rh);
    }
    return 0;
}
