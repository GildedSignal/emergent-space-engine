// The falsifier for run 20261014-1511-scout-f0a2.
//
// Question: what is the quantum gate's affordable form at 10^9? The gate must not cost any
// per-pair work per refresh (candidates/kick = 0.0175-0.087 N measured), so we measure:
//   (1) Kepler-true per-pair strongest-conjunction charge (the propagated gate, 0b81's lever),
//   (2) the propagation-free contact screen (per-body one bit, satellite-ops style),
//   (3) the deflection charge vs RK4 (control), costs in ns/pair (control),
//   (4) the composed 10^9 stream: routing + exact-tier events, with the horizon dial.
//
// Float replica: star mu=1, a0=1, one orbit = 2pi. SI anchor: a = 1.5 AU, solar star.
// The key's quantum (shipped crates/space/src/lib.rs): E is dimensionless in Q48 on scale 1,
// so one quantum of specific energy q = c^2 * 2^-48. Deletable iff v*dv < q; with
// dv = 2*mu_max/(b*v_rel) the vk cancels: deletable iff 2*mu_max*c_rep < q*a_SI where
// c_rep = 1/(b_rep * vrel_rep) is the replica-unit charge coefficient.
//
// Build: gcc -O2 -lm. Output: JSON lines on stdout. Each experiment well under 60 s.

#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static uint64_t rng_s = 0x9E3779B97F4A7C15ull;
static uint64_t rng64(void) {
    rng_s ^= rng_s << 13; rng_s ^= rng_s >> 7; rng_s ^= rng_s << 17;
    return rng_s;
}
static double rng_f(void) { return (rng64() >> 11) * (1.0 / 9007199254740992.0); }

// ---- belt geometry (replica units) ----
#define SIGMA_E 0.05
#define HORIZON_ORBITS 1000.0
#define TAU 6.283185307179586

typedef struct { double a, e, pom, lam0; } Orb; // lam0 = mean longitude at t=0

typedef struct { double x, y, vx, vy; } State;

static State kepler(const Orb *o, double t) {
    double n = pow(o->a, -1.5);
    double M = o->lam0 - o->pom + n * t;
    M = fmod(M, TAU); if (M < 0) M += TAU;
    double E = M + o->e * sin(M);
    for (int i = 0; i < 6; i++) {
        double f = E - o->e * sin(E) - M;
        E -= f / (1.0 - o->e * cos(E));
    }
    double cE = cos(E), sE = sin(E);
    double r = o->a * (1.0 - o->e * cE);
    double Edot = n / (1.0 - o->e * cE);
    double xo = o->a * (cE - o->e), yo = o->a * sqrt(1.0 - o->e * o->e) * sE;
    double vxo = -o->a * sE * Edot, vyo = o->a * sqrt(1.0 - o->e * o->e) * cE * Edot;
    double cp = cos(o->pom), sp = sin(o->pom);
    State s;
    s.x = xo * cp - yo * sp; s.y = xo * sp + yo * cp;
    s.vx = vxo * cp - vyo * sp; s.vy = vxo * sp + vyo * cp;
    (void)r;
    return s;
}

// One pair scan: conjunctions by mean-longitude beats, refined on |dr| (golden section).
// Returns: c_max = max over conjunctions of 1/(b*vrel) [replica units], min_vrel, nconj,
// and per-level event counts (conjunctions whose charge exceeds level c*).
typedef struct { double c_max, min_vrel; int nconj; int ev[5]; } Scan;

static Scan scan_pair(const Orb *o1, const Orb *o2, const double *cstar, int nlev) {
    Scan s = { 0, 1e9, 0, {0} };
    double n1 = pow(o1->a, -1.5), n2 = pow(o2->a, -1.5);
    double dn = n1 - n2;
    if (fabs(dn) < 1e-14) return s;
    double dL0 = o1->lam0 - o2->lam0;
    double S = TAU / fabs(dn);
    double H = HORIZON_ORBITS * TAU;
    double w = fmin(S / 8.0, 2.5 * (o1->e / n1 + o2->e / n2) + 1e-9);
    // conjunctions at t_k = (TAU*k - dL0)/dn; step k in the direction of growing t
    long k = (long)floor(dL0 / TAU) - 2;
    for (int iter = 0; iter < 8192; iter++, k += (dn > 0 ? 1 : -1)) {
        double t = (TAU * (double)k - dL0) / dn;
        if (t < 0) continue;
        if (t > H) break;
        if (s.nconj >= 256) break;
        s.nconj++;
        // golden-section on |dr| over [t-w, t+w]
        double lo = t - w, hi = t + w;
        double phi = (sqrt(5.0) - 1.0) / 2.0;
        double x1 = hi - phi * (hi - lo), x2 = lo + phi * (hi - lo);
        State A = kepler(o1, x1), B = kepler(o2, x1);
        double f1 = hypot(A.x - B.x, A.y - B.y);
        A = kepler(o1, x2); B = kepler(o2, x2);
        double f2 = hypot(A.x - B.x, A.y - B.y);
        for (int i = 0; i < 24; i++) {
            if (f1 < f2) { hi = x2; x2 = x1; f2 = f1; x1 = hi - phi * (hi - lo);
                A = kepler(o1, x1); B = kepler(o2, x1); f1 = hypot(A.x - B.x, A.y - B.y);
            } else { lo = x1; x1 = x2; f1 = f2; x2 = lo + phi * (hi - lo);
                A = kepler(o1, x2); B = kepler(o2, x2); f2 = hypot(A.x - B.x, A.y - B.y);
            }
        }
        double tm = 0.5 * (lo + hi);
        A = kepler(o1, tm); B = kepler(o2, tm);
        double b = hypot(A.x - B.x, A.y - B.y);
        double vr = hypot(A.vx - B.vx, A.vy - B.vy);
        if (vr < s.min_vrel) s.min_vrel = vr;
        double c = 1.0 / (b * vr);
        if (c > s.c_max) s.c_max = c;
        for (int L = 0; L < nlev; L++) if (c > cstar[L]) s.ev[L]++;
    }
    return s;
}

// ---- SI anchors ----
#define AU 1.495978707e11
#define A_SI (1.5 * AU)
#define C_LIGHT 2.99792458e8
#define Q_ENERGY (C_LIGHT * C_LIGHT * 3.5527136788e-15) // c^2 * 2^-48
#define RHO_ROCK 2700.0
#define G_SI 6.674e-11
#define P_ORB_SI (TAU * sqrt(A_SI * A_SI * A_SI / 1.32712440018e20)) // ~5.80e7 s at 1.5 AU

static double mu_of_D(double D) { return G_SI * RHO_ROCK * (M_PI / 6.0) * D * D * D; }
static double D_dohnanyi(double dmin, double dmax) {
    double u = rng_f();
    double a = pow(dmin, -2.5), b = pow(dmax, -2.5);
    return pow(a + u * (b - a), -0.4);
}

// RK4 two-body scattering control: dv vs 2*mu/(b*v).
static double rk4_dv(double mu, double b, double v) {
    double far = 60.0 * b;
    double x = -sqrt(far * far - b * b), y = b;
    double vx = v, vy = 0.0;
    double dt = 2.0 * far / v / 4000.0;
    for (int i = 0; i < 4000; i++) {
        for (int sub = 0; sub < 1; sub++) {
            double r = hypot(x, y), r3 = r * r * r;
            double ax = -mu * x / r3, ay = -mu * y / r3;
            // one RK4 step of the relative problem
            double k1x = vx, k1y = vy, l1x = ax, l1y = ay;
            double x2 = x + 0.5 * dt * k1x, y2 = y + 0.5 * dt * k1y;
            r = hypot(x2, y2); r3 = r * r * r;
            double k2x = vx + 0.5 * dt * l1x, k2y = vy + 0.5 * dt * l1y;
            double l2x = -mu * x2 / r3, l2y = -mu * y2 / r3;
            double x3 = x + 0.5 * dt * k2x, y3 = y + 0.5 * dt * k2y;
            r = hypot(x3, y3); r3 = r * r * r;
            double k3x = vx + 0.5 * dt * l2x, k3y = vy + 0.5 * dt * l2y;
            double l3x = -mu * x3 / r3, l3y = -mu * y3 / r3;
            double x4 = x + dt * k3x, y4 = y + dt * k3y;
            r = hypot(x4, y4); r3 = r * r * r;
            double k4x = vx + dt * l3x, k4y = vy + dt * l3y;
            double l4x = -mu * x4 / r3, l4y = -mu * y4 / r3;
            x += dt / 6.0 * (k1x + 2 * k2x + 2 * k3x + k4x);
            y += dt / 6.0 * (k1y + 2 * k2y + 2 * k3y + k4y);
            vx += dt / 6.0 * (l1x + 2 * l2x + 2 * l3x + l4x);
            vy += dt / 6.0 * (l1y + 2 * l2y + 2 * l3y + l4y);
        }
    }
    return hypot(vx - v, vy);
}

static double now_sec(void) {
    struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + 1e-9 * ts.tv_nsec;
}

int main(int argc, char **argv) {
    uint64_t seed = argc > 1 ? strtoull(argv[1], 0, 10) : 20261014;
    rng_s = seed * 0x2545F4914F6CDD1Dull + 11;

    // controls: deflection charge vs RK4
    printf("{\"exp\":\"charge-control\",\"rows\":[");
    int first = 1;
    double mus[2] = { mu_of_D(1.0e4), mu_of_D(4.7e5) };
    for (int m = 0; m < 2; m++)
        for (int bv = 0; bv < 4; bv++) {
            double b_rep = 3e-3 * pow(10.0, bv - 1.0);   // 3e-4 .. 3e-3 of a
            double v_rep = 0.05 + 0.45 * (bv % 2);
            double b_SI = b_rep * A_SI, v_SI = v_rep * 24300.0; // vk at 1.5 AU
            double approx = 2.0 * mus[m] / (b_SI * v_SI);
            double exact = rk4_dv(mus[m], b_SI, v_SI);
            printf("%s{\"mu_kgms\":%.3e,\"b_m\":%.3e,\"v_rel_ms\":%.0f,\"ratio_exact_over_formula\":%.6f}",
                   first ? "" : ",", mus[m], b_SI, v_SI, exact / approx);
            first = 0;
        }
    printf("]}\n");

    // thresholds for event counting: D = 470 km, 100 km, 10 km, 1.3 km, 300 m
    double Dlev[5] = { 4.7e5, 1.0e5, 1.0e4, 1.3e3, 3.0e2 };
    double cstar[5], K = Q_ENERGY * A_SI / 2.0; // deletable iff mu*c < K
    for (int i = 0; i < 5; i++) cstar[i] = K / mu_of_D(Dlev[i]);

    double da_grid[7] = { 0.001, 0.003, 0.005, 0.01, 0.02, 0.05, 0.1 };
    int npairs = 2048, nmass = 64;
    double dmin = 70.0, dmax = 4.7e5;

    // the one-bit threshold D*: equal sizes, charge at contact with floor vk*P/H
    double floor_rep = 1.0 / HORIZON_ORBITS; // v_rel/vk >= P/H for any conjunction in H
    double Dstar = 0, lo = 1.0, hi = 1.0e5;
    for (int i = 0; i < 80; i++) {
        double mid = 0.5 * (lo + hi);
        // screen deletable iff 2*mu/(b_c * floor_rep) < Q_ENERGY with b_c = D (equal sizes),
        // all in SI: 2*mu_of_D(mid)/(mid*24300.0*floor_rep)... vk cancels:
        double charge = 2.0 * mu_of_D(mid) / (mid * 24300.0 * floor_rep) * 24300.0;
        if (charge < Q_ENERGY) lo = mid; else hi = mid;
        Dstar = 0.5 * (lo + hi);
    }

    double tot_w1_gate = 0, tot_w1_scr = 0, tot_w1_scr2 = 0, tot_w1_pairs = 0;
    double tot_ev_rate[5] = { 0, 0, 0, 0, 0 };
    double bench_ns = 0, scan_secs = 0, min_vrel_all = 1e9, nconj_sum = 0; int bench_pairs = 0;
    double surv_sum = 0, cmax_all = 0; long surv_n = 0, gate10k_fail = 0;
    for (int g = 0; g < 7; g++) {
        double da = da_grid[g];
        double t0 = now_sec();
        scan_secs = 0;
        long gate_del = 0, scr_del = 0, scr2_del = 0, nm = 0;
        long ev[5] = { 0, 0, 0, 0, 0 };
        double minv = 1e9;
        double w1 = 1.0; // weight per da-bin (uniform over the grid)
        for (int p = 0; p < npairs; p++) {
            Orb o1, o2;
            o1.a = 1.0; o2.a = 1.0 + da;
            o1.e = SIGMA_E * sqrt(-2.0 * log(1.0 - rng_f())); if (o1.e > 0.5) o1.e = 0.5;
            o2.e = SIGMA_E * sqrt(-2.0 * log(1.0 - rng_f())); if (o2.e > 0.5) o2.e = 0.5;
            o1.pom = TAU * rng_f(); o2.pom = TAU * rng_f();
            o1.lam0 = TAU * rng_f(); o2.lam0 = TAU * rng_f();
            double ts0 = now_sec();
            Scan s = scan_pair(&o1, &o2, cstar, 5);
            scan_secs += now_sec() - ts0;
            if (s.min_vrel < minv) minv = s.min_vrel;
            if (s.min_vrel < min_vrel_all) min_vrel_all = s.min_vrel;
            // analytic survivor expectation at the shipped-key anchor: the gate fails for
            // this pair only if a partner exceeds Dcrit = (6 K /(pi G rho c_max))^(1/3)
            double Dcrit = cbrt(6.0 * (K / fmax(s.c_max, 1e-12)) / (M_PI * G_SI * RHO_ROCK));
            double tail = (pow(Dcrit, -2.5) - pow(dmax, -2.5)) / (pow(dmin, -2.5) - pow(dmax, -2.5));
            if (Dcrit <= dmin) tail = 1.0;
            if (Dcrit >= dmax) tail = 0.0;
            surv_sum += 2.0 * tail; surv_n++;
            if (s.c_max > cmax_all) cmax_all = s.c_max;
            if (s.c_max > cstar[2]) gate10k_fail++;
            for (int L = 0; L < 5; L++) ev[L] += s.ev[L];
            for (int m = 0; m < nmass; m++) {
                double Di = D_dohnanyi(dmin, dmax), Dj = D_dohnanyi(dmin, dmax);
                double mu_max = fmax(mu_of_D(Di), mu_of_D(Dj));
                double bc = 0.5 * (Di + Dj);
                int gd = mu_max * s.c_max < K;                        // nconj = 0: deleted
                int sd = 2.0 * mu_max / (bc * floor_rep) < Q_ENERGY;  // one-bit screen
                int s2d = 2.0 * mu_max / (bc * fmax(s.min_vrel, 1e-6)) < Q_ENERGY;
                gate_del += gd; scr_del += sd; scr2_del += s2d; nm++;
            }
        }
        double dt = now_sec() - t0; (void)dt;
        if (da == 0.05) bench_ns = scan_secs / npairs * 1e9; (void)bench_pairs;
        tot_w1_gate += w1 * gate_del; tot_w1_scr += w1 * scr_del;
        tot_w1_scr2 += w1 * scr2_del; tot_w1_pairs += w1 * nm;
        for (int L = 0; L < 5; L++) tot_ev_rate[L] += w1 * ev[L];
        printf("{\"exp\":\"scan\",\"da\":%g,\"pairs\":%d,\"mass_draws\":%ld,\"gate_deletable\":%.5f,"
               "\"screen_deletable\":%.5f,\"screen_pairfloor_deletable\":%.5f,\"min_vrel\":%.3e,"
               "\"mean_nconj\":%.1f,\"events_per_pair_per_horizon\":[",
               da, npairs, nm, (double)gate_del / nm, (double)scr_del / nm,
               (double)scr2_del / nm, minv, nconj_sum / npairs);
        for (int L = 0; L < 5; L++)
            printf("%s%.3e", L ? "," : "", (double)ev[L] / npairs);
        printf("]}\n");
        nconj_sum = 0;
    }

    double gate = tot_w1_gate / tot_w1_pairs, scr = tot_w1_scr / tot_w1_pairs,
           scr2 = tot_w1_scr2 / tot_w1_pairs;
    double evper[5]; for (int i = 0; i < 5; i++) evper[i] = tot_ev_rate[i] / 7.0 / npairs;

    // controls: mono-size belts
    double mono_scr(double D) {
        // screen deletable fraction for all-D belt: mu_max = mu(D), bc = D
        return (2.0 * mu_of_D(D) / (D * 24300.0 * floor_rep) * 24300.0 < Q_ENERGY) ? 1.0 : 0.0;
    }

    // composition at 1e9 (one frame: rtf 1, averaged cadence 0.28/orbit, a in [1,1.5] AU)
    double N = 1e9;
    double nAbove = pow(Dstar / dmin, -2.5); if (nAbove > 1) nAbove = 1;
    double n_large = N * (pow(dmax, -2.5) - pow(Dstar, -2.5)) / (pow(dmax, -2.5) - pow(dmin, -2.5));
    double Pbar = P_ORB_SI * 1.06; // mean of a^1.5 over [1,1.5] AU = ((1.5^2.5-1)/0.5)/... approx
    double kicks_s = N * 0.28 / Pbar;
    double routing_evals_s = kicks_s * n_large;           // no-slack bound
    double routing_evals_s_slack = routing_evals_s * 0.05;// cited slack sensitivity
    double large_kicks_s = n_large * 0.28 / Pbar;
    double wake_evals_s = large_kicks_s * 0.0865 * N;
    double ev_s[5];
    for (int i = 0; i < 5; i++) {
        double nl = N * (pow(dmax, -2.5) - pow(Dlev[i], -2.5)) / (pow(dmax, -2.5) - pow(dmin, -2.5));
        ev_s[i] = nl * N * evper[i] / (HORIZON_ORBITS * Pbar);
    }

    printf("{\"exp\":\"summary\",\"q_energy_m2s2\":%.3f,\"K\":%.4e,\"Dstar_m\":%.1f,"
           "\"floor_vrel_over_vk\":%.2e,\"min_vrel_all\":%.3e,"
           "\"gate_deletable\":%.5f,\"screen_deletable\":%.5f,\"screen_pairfloor_deletable\":%.5f,"
           "\"screen_over_gate\":%.4f,\"all_50m_screen\":%f,\"all_470km_screen\":%f,"
           "\"bench_ns_per_pair\":%.0f,\"n_above_Dstar\":%.3e,\"n_large\":%.3e,"
           "\"kicks_s\":%.3e,\"routing_evals_s\":%.3e,\"routing_evals_s_slack05\":%.3e,"
           "\"wake_evals_s\":%.3e,\"exact_events_s\":[",
           Q_ENERGY, K, Dstar, floor_rep, min_vrel_all, gate, scr, scr2, scr / gate,
           mono_scr(50.0), mono_scr(4.7e5), bench_ns, nAbove, n_large, kicks_s,
           routing_evals_s, routing_evals_s_slack, wake_evals_s);
    for (int i = 0; i < 5; i++) printf("%s%.3e", i ? "," : "", ev_s[i]);
    printf("]}\n");
    {
        // the composed one-frame ledger, both cadences, three eval prices
        double evals[2] = { routing_evals_s, routing_evals_s * 457.0 }; // averaged, shipped k=128
        double evals_slack[2] = { routing_evals_s_slack, routing_evals_s_slack * 457.0 };
        printf("{\"exp\":\"ledger\",\"survivor_fraction_analytic\":%.3e,\"cmax_all\":%.3e,"
               "\"all10km_gate_deletable\":%.5f,\"routing_cores\":[",
               surv_sum / fmax((double)surv_n, 1.0), cmax_all,
               1.0 - (double)gate10k_fail / fmax((double)surv_n, 1.0));
        for (int c = 0; c < 2; c++)
            printf("%s[%.3f,%.3f,%.3f]", c ? "," : "", evals[c] * 1e-8, evals[c] * 5e-8, evals[c] * 2e-7);
        printf("],\"routing_cores_slack05\":[");
        for (int c = 0; c < 2; c++)
            printf("%s[%.4f,%.4f,%.4f]", c ? "," : "", evals_slack[c] * 1e-8, evals_slack[c] * 5e-8, evals_slack[c] * 2e-7);
        double evcore = 0; for (int i = 0; i < 5; i++) evcore += ev_s[i] * 4e-6;
        printf("],\"exact_tier_cores\":%.3e,\"gate_ms_per_pair\":%.4f,\"cut_vs_published_wall_8p2e3\":%.1f,\"dcrit_cmax_m\":%.1f}\n",
               evcore, bench_ns / 1e6, 8.2e3 / fmax(evals[0] * 5e-8, 1e-9),
               cbrt(6.0 * (K / fmax(cmax_all, 1e-12)) / (M_PI * G_SI * RHO_ROCK)));
    }

    // the horizon dial: D*(H) and the routing term at H in {100, 1000, 10000}
    printf("{\"exp\":\"horizon-dial\",\"rows\":[");
    for (int h = 0; h < 3; h++) {
        double hor = 100.0 * pow(10.0, h);
        double fl = 1.0 / hor;
        double l = 1.0, hh2 = 1.0e5;
        for (int i = 0; i < 80; i++) {
            double mid = 0.5 * (l + hh2);
            double charge = 2.0 * mu_of_D(mid) / (mid * fl);
            if (charge < Q_ENERGY) l = mid; else hh2 = mid;
        }
        double d = 0.5 * (l + hh2);
        double nl = N * (pow(dmax, -2.5) - pow(d, -2.5)) / (pow(dmax, -2.5) - pow(dmin, -2.5));
        double rt = (N * 0.28 / Pbar) * nl; // no-slack routing evals/s (refresh rate fixed by
        // the cadence law, not by the certificate horizon; D* moves with the floor only)
        printf("%s{\"horizon_orbits\":%.0f,\"Dstar_m\":%.1f,\"n_large\":%.3e,\"routing_evals_s\":%.3e}",
               h ? "," : "", hor, d, nl, rt);
    }
    printf("]}\n");
    return 0;
}
