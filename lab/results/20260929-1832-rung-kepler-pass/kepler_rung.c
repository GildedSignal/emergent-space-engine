/* Rung canary: Newtonian Kepler orbit, fixed step, 10^4 orbits, float64.
 * Case (frozen by the rung): 2D, one test body, GM = 1, a = 1, e = 0.5,
 * start at periopsi x = (0.5, 0), v = (0, sqrt(3)), E0 = -0.5,
 * h = T/200 with T = 2*pi, 2,000,000 steps.
 * Configs: leapfrog (kick-drift-kick velocity Verlet), euler (forward Euler).
 * Outputs metrics.json plus data files for the picture.
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

static const long   NSTEPS   = 2000000L;
static const double ORBITS   = 10000.0;
static const double TWO_PI   = 6.283185307179586476925286766559;
static const double E0       = -0.5;          /* oracle value, exact */
static const int    NWIN     = 20;
static const double FLOOR_DE = 1e-16;
static const long   TRAJ_STEPS = 8000L;       /* first 40 orbits, for the picture */
static const int    NENER     = 700;          /* log-spaced energy samples */

typedef struct { double x, y, vx, vy; } State;

static inline void accel(const State *s, double *ax, double *ay) {
    double r2 = s->x * s->x + s->y * s->y;
    double r  = sqrt(r2);
    double k  = -1.0 / (r2 * r);              /* GM = 1 */
    *ax = k * s->x;
    *ay = k * s->y;
}

static inline double energy(const State *s) {
    double r = sqrt(s->x * s->x + s->y * s->y);
    return 0.5 * (s->vx * s->vx + s->vy * s->vy) - 1.0 / r;
}

static void run(const char *name, int leapfrog, int first) {
    char fname[256];
    double h = TWO_PI / 200.0;
    State s = { 0.5, 0.0, 0.0, sqrt(3.0) };
    double t_end = (double)NSTEPS * h;

    snprintf(fname, sizeof fname, "ener_%s.txt", name);
    FILE *fe = fopen(fname, "w");
    snprintf(fname, sizeof fname, "traj_%s.txt", name);
    FILE *ft = fopen(fname, "w");

    /* windows: log-spaced edges from 0.1*t_end to t_end */
    double edges[NWIN + 1];
    for (int i = 0; i <= NWIN; i++)
        edges[i] = 0.1 * t_end * pow(10.0, (double)i / NWIN);
    double mwin[NWIN];
    for (int i = 0; i < NWIN; i++) mwin[i] = 0.0;

    /* log-spaced energy sample steps, from step 200 to NSTEPS */
    long sample[NENER];
    for (int k = 0; k < NENER; k++) {
        double lo = log(200.0), hi = log((double)NSTEPS);
        sample[k] = (long)round(exp(lo + (hi - lo) * k / (NENER - 1.0)));
        if (sample[k] < 1) sample[k] = 1;
        if (k > 0 && sample[k] <= sample[k - 1]) sample[k] = sample[k - 1] + 1;
    }

    double *traj = malloc(sizeof(double) * 2 * TRAJ_STEPS);
    long first_unbound = -1;
    double max_abs_dE = 0.0, final_abs_dE = 0.0;
    int w = -1, sk = 0;

    for (long j = 1; j <= NSTEPS; j++) {
        if (leapfrog) {                        /* kick-drift-kick */
            double ax, ay;
            accel(&s, &ax, &ay);
            s.vx += 0.5 * h * ax;  s.vy += 0.5 * h * ay;
            s.x  += h * s.vx;      s.y  += h * s.vy;
            accel(&s, &ax, &ay);
            s.vx += 0.5 * h * ax;  s.vy += 0.5 * h * ay;
        } else {                               /* forward Euler, old state only */
            double ax, ay;
            accel(&s, &ax, &ay);
            double vx = s.vx + h * ax, vy = s.vy + h * ay;
            s.x += h * s.vx;       s.y  += h * s.vy;
            s.vx = vx;             s.vy  = vy;
        }

        double E  = energy(&s);
        double dE = E - E0;
        double aD = fabs(dE);
        if (aD > max_abs_dE) max_abs_dE = aD;
        final_abs_dE = aD;
        if (first_unbound < 0 && E >= 0.0) first_unbound = j;

        double t = (double)j * h;
        if (t >= edges[0]) {                   /* window maxima */
            while (w < NWIN - 1 && t >= edges[w + 1]) w++;
            if (aD > mwin[w]) mwin[w] = aD;
        }
        if (j <= TRAJ_STEPS) { traj[2 * (j - 1)] = s.x; traj[2 * (j - 1) + 1] = s.y; }
        while (sk < NENER && sample[sk] == j) {
            fprintf(fe, "%.17g %.17g\n", t, aD < FLOOR_DE ? FLOOR_DE : aD);
            sk++;
        }
    }
    fclose(fe);

    /* exponent: least-squares slope of ln m vs ln(t_mid), t_mid geometric */
    double sx = 0, sy = 0, sxx = 0, sxy = 0;
    snprintf(fname, sizeof fname, "win_%s.txt", name);
    FILE *fw = fopen(fname, "w");
    for (int i = 0; i < NWIN; i++) {
        double tm = sqrt(edges[i] * edges[i + 1]);
        double mm = mwin[i] < FLOOR_DE ? FLOOR_DE : mwin[i];
        fprintf(fw, "%.17g %.17g\n", tm, mm);
        double x = log(tm), y = log(mm);
        sx += x; sy += y; sxx += x * x; sxy += x * y;
    }
    fclose(fw);
    double slope = (NWIN * sxy - sx * sy) / (NWIN * sxx - sx * sx);
    double bound_fraction = (first_unbound < 0) ? 1.0
                          : (double)(first_unbound - 1) / (double)NSTEPS;
    double steps_per_orbit = (double)NSTEPS / ORBITS;

    for (long j = 0; j < TRAJ_STEPS; j++)
        fprintf(ft, "%.17g %.17g\n", traj[2 * j], traj[2 * j + 1]);
    fclose(ft);
    free(traj);

    printf("%-9s energy_growth_exponent=%.6g bound_fraction=%.6g "
           "steps_per_orbit=%.6g max|dE|=%.6g final|dE|=%.6g first_unbound_step=%ld\n",
           name, slope, bound_fraction, steps_per_orbit, max_abs_dE, final_abs_dE,
           first_unbound);

    FILE *fm = fopen("metrics.json", first ? "w" : "a");
    fprintf(fm, "%s\"%s\": {\"energy_growth_exponent\": %.17g, "
                "\"bound_fraction\": %.17g, \"steps_per_orbit\": %.17g}%s\n",
           first ? "{\n" : "", name, slope, bound_fraction, steps_per_orbit,
           first ? "," : "\n}");
    fclose(fm);

    FILE *fs = fopen("summary.txt", first ? "w" : "a");
    fprintf(fs, "%s: first_unbound_step=%ld (orbit %.4f) max|dE|=%.6g final|dE|=%.6g slope=%.6g\n",
            name, first_unbound, first_unbound < 0 ? -1.0 : first_unbound / 200.0,
            max_abs_dE, final_abs_dE, slope);
    fclose(fs);
}

int main(void) {
    run("leapfrog", 1, 1);
    run("euler",    0, 0);
    return 0;
}
