/* Premise red-team 20260930-2250, v2: Binet-band staircase vs exact GR (float64).
 *
 * Banded model = r1's frozen configuration: u'' + (1 - 6 u_k) u = 1/L^2 - 3 u_k^2
 * (light: RHS = -3 u_k^2), u and u' continuous across bands, bands r_k = 2^(k/m),
 * u_k = geometric centre of the band in u.  Oracle = exact Schwarzschild Binet
 * u'' + u = 1/L^2 + 3 u^2 (light: u'' + u = 3 u^2).  M = 1, equatorial plane.
 * RK4 in phi, fixed step 2e-4 rad (halved-step convergence checked).
 *
 * v2 fixes vs v1 (v1's init was wrong: (1+e)/p with L^2=p is not a GR turning
 * point for small e; light capture bisection used u_max below b_crit):
 *  - timelike seeds are turning-point pairs (u_p, u_a); L follows from both
 *    turning points, so both models start at the true periapsis with w=0.
 *  - light is launched from r0=2000 with identical (u, w) for both models.
 */
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

static int m_bands;
static double uk_of(double u) {
  if (u <= 0.0) return 0.0;
  double k = floor(m_bands * log2(1.0 / u));
  return pow(2.0, -(k + 0.5) / m_bands);
}
static double acc(int mode, double u, double invL2) {
  double uk = (mode & 1) ? uk_of(u) : 0.0;
  switch (mode) {
    case 0: return invL2 + 3.0 * u * u - u;
    case 1: return invL2 - 3.0 * uk * uk - (1.0 - 6.0 * uk) * u;
    case 2: return 3.0 * u * u - u;
    default: return -3.0 * uk * uk - (1.0 - 6.0 * uk) * u;
  }
}
static void rk4(int mode, double invL2, double *u, double *w, double h,
                long *xcross) {
  double k1u = *w,              k1w = acc(mode, *u, invL2);
  double k2u = *w + 0.5*h*k1w,  k2w = acc(mode, *u + 0.5*h*k1u, invL2);
  double k3u = *w + 0.5*h*k2w,  k3w = acc(mode, *u + 0.5*h*k2u, invL2);
  double k4u = *w + h*k3w,      k4w = acc(mode, *u + h*k3u, invL2);
  double un = *u + h / 6.0 * (k1u + 2*k2u + 2*k3u + k4u);
  *w += h / 6.0 * (k1w + 2*k2w + 2*k3w + k4w);
  if (xcross && uk_of(un) != uk_of(*u)) (*xcross)++;
  *u = un;
}

/* Timelike from periapsis (u_p max, w=0). Returns 1 bound, 0 captured, -1 other.
 * dphi[0..2] = periapsis-to-periapsis advances. umax drift over 4 cycles. */
static int run_timelike(int mode, double up, double ua, double h,
                        double *dphi, double *umax0, double *umax3, int ncyc) {
  double invL2 = 0.5 * (up + ua) - (up * up + up * ua + ua * ua);
  double u = up, w = 0.0, phi = 0.0, prev_w = w, prev_phi = 0.0, next_goal = -1.0;
  int n_peri = 0, done = 0;
  *umax0 = up; *umax3 = up;
  for (long i = 0; i < 80000000L; i++) {
    rk4(mode, invL2, &u, &w, h, NULL);
    phi += h;
    if (u >= 0.5) return 0;
    if (u <= 0.0) return -1;
    if (prev_w > 0.0 && w <= 0.0) {
      double phi_p = prev_phi + (prev_w / (prev_w - w)) * h;
      if (n_peri >= 1 && n_peri - 1 < ncyc) dphi[n_peri - 1] = phi_p - next_goal;
      if (n_peri == ncyc) { *umax3 = u; done = 1; }
      next_goal = phi_p; n_peri++;
      if (n_peri > ncyc + 1) break;
    }
    prev_w = w; prev_phi = phi;
  }
  return done ? 1 : -1;
}

/* Light from r0, incoming, impact parameter b. Returns sweep phi until
 * u < u_end (scattered), or -1 captured, -2 stuck. xcross counts band changes. */
static double run_light(int mode, double b, double r0, double u_end, double h,
                        long *xcross) {
  double phi0 = asin(b / r0);
  double u = sin(phi0) / b, w = cos(phi0) / b, phi = 0.0;
  for (long i = 0; i < 90000000L; i++) {
    rk4(mode, 0.0, &u, &w, h, xcross);
    phi += h;
    if (u >= 0.5) return -1.0;
    if (u < u_end) return phi;
    if (phi > 80.0 * M_PI) return -2.0;
  }
  return -2.0;
}

int main(int argc, char **argv) {
  double h = (argc > 1) ? atof(argv[1]) : 2e-4;
  double r0 = 2000.0, u_end = 1.0 / r0;
  clock_t t0 = clock();
  int ms[] = {8, 16, 32};

  printf("== timelike (turning-point seeds): relative precession error ==\n");
  printf("%5s %6s %4s | %-12s %-12s %-12s | %s\n", "e", "r_p", "m",
         "err_dphi", "exact_dphi", "drift_uperi", "verdict/in-box");
  double es[] = {0.1, 0.3, 0.5, 0.7, 0.9, 0.95};
  double rps[] = {4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 8.0, 10.0, 20.0, 100.0};
  for (int ie = 0; ie < 6; ie++)
    for (int ir = 0; ir < 10; ir++) {
      double e = es[ie], rp = rps[ir];
      double up = 1.0 / rp, ua = up * (1.0 - e) / (1.0 + e);
      double dex[8] = {0}, dba[8] = {0}, a1, a2, b1, b2;
      int rex = run_timelike(0, up, ua, h, dex, &a1, &b1, 4);
      int rba = run_timelike(1, up, ua, h, dba, &a2, &b2, 4);
      const char *se = rex == 1 ? "bound" : (rex == 0 ? "captured" : "other");
      const char *sb = rba == 1 ? "bound" : (rba == 0 ? "captured" : "other");
      int mismatch = (rex == 1) != (rba == 1);
      /* r1 box in (p, e) with p = 2/(up+ua) ... in-box test */
      double p_semilatus = 2.0 / (up + ua);
      int inbox = (e <= 0.7) && (p_semilatus >= 10.0) && (p_semilatus >= 6.5 + 2.0 * e);
      if (rex != 1 || rba != 1) {
        printf("%5.2f %6.2f %4d | %-12s %-12s %-12s | exact=%s band=%s%s\n",
               e, rp, 16, "-", "-", "-", se, sb,
               mismatch ? "  <-- MISCLASSIFIED" : "");
        continue;
      }
      double drift = fabs(a2 - b2) / b2;
      for (int im = 0; im < 3; im++) {
        m_bands = ms[im];
        double d1[8] = {0}, d2[8] = {0};
        run_timelike(0, up, ua, h, d1, &a1, &b1, 4);
        run_timelike(1, up, ua, h, d2, &a2, &b2, 4);
        double er = fabs(d2[3] - d1[3]) / d1[3];
        printf("%5.2f %6.2f %4d | %-12.3e %-12.6f %-12.3e | %s%s\n",
               e, rp, ms[im], er, d1[3], drift, inbox ? "IN-BOX" : "out-of-box",
               er > 0.01 ? "  ** >1% **" : "");
      }
    }

  printf("\n== separatrix scan (m=16): plunge boundary = smallest bound r_p ==\n");
  m_bands = 16;
  int mism = 0, tot = 0;
  for (int ie = 0; ie < 3; ie++) {
    double e = (double)ie * 0.45 + 0.05;   /* 0.05, 0.50, 0.95 */
    double sep_e = -1, sep_b = -1;         /* smallest r_p still bound */
    for (int ir = 200; ir >= 40; ir--) {   /* r_p from 10.0 down to 2.0, step 0.05 */
      double rp = 0.05 * ir;
      double up = 1.0 / rp, ua = up * (1.0 - e) / (1.0 + e);
      double d1[8], d2[8], a, b;
      int rex = run_timelike(0, up, ua, h, d1, &a, &b, 2);
      int rba = run_timelike(1, up, ua, h, d2, &a, &b, 2);
      tot++;
      if ((rex == 1) != (rba == 1)) mism++;
      if (rex == 1 && sep_e < 0) sep_e = rp;
      if (rba == 1 && sep_b < 0) sep_b = rp;
    }
    printf("e=%.2f: exact plunge boundary r_p in (%.2f, %.2f), banded in (%.2f, %.2f)\n",
           e, sep_e, sep_e - 0.05, sep_b, sep_b - 0.05);
  }
  printf("separatrix scan: %d/%d grid points disagree on bound<->captured\n", mism, tot);

  /* hover probe: e=0.1, r_p=6.0 (m=16): phi needed per radial cycle */
  {
    double up = 1.0 / 6.0, ua = up * 0.9 / 1.1;
    double invL2 = 0.5 * (up + ua) - (up * up + up * ua + ua * ua);
    double u = up, w = 0.0, phi = 0.0, prev_w = w;
    int nperi = 0; double firstperi = -1;
    for (long i = 0; i < 40000000L && phi < 4000.0; i++) {
      rk4(1, invL2, &u, &w, h, NULL); phi += h;
      if (u >= 0.5) { printf("hover probe: captured at phi=%.1f\n", phi); nperi = -99; break; }
      if (prev_w > 0 && w <= 0) { nperi++; if (nperi == 1) firstperi = phi;
        if (nperi >= 4) break; }
      prev_w = w;
    }
    if (nperi > 0) printf("hover probe (e=0.1, r_p=6, m=16): periapses seen=%d, dphi_cycle=%.1f rad (exact 68.9), umax=%.4f\n",
                          nperi, firstperi, u);
    else if (nperi == 0) printf("hover probe (e=0.1, r_p=6, m=16): NO periapsis within phi=4000; u drifts to %.4f (r=%.2f)\n", u, 1.0/u);
  }

  printf("\n== light from r0=%.0f: deflection = sweep - (pi - 2 phi0) ==\n", r0);
  double bs[] = {5.205, 5.22, 5.30, 5.45, 5.60, 5.80, 6.00, 6.50, 7.00, 8.00,
                 10.0, 20.0, 100.0};
  for (int ib = 0; ib < 13; ib++) {
    double b = bs[ib];
    double pe = run_light(2, b, r0, u_end, h, NULL);
    if (pe < 0) { printf("b=%6.3f: exact did not scatter (%.3f)?\n", b, pe); continue; }
    double phi0 = asin(b / r0), de = pe - (M_PI - 2 * phi0);
    for (int im = 0; im < 3; im++) {
      m_bands = ms[im];
      long xc = 0;
      double pb = run_light(3, b, r0, u_end, h, &xc);
      if (pb < 0)
        printf("b=%6.3f m=%2d defl_exact=%9.5f  banded: %s (xcross=%ld)\n", b,
               ms[im], de, pb == -1 ? "CAPTURED" : "stuck", xc);
      else {
        double db = pb - (M_PI - 2 * phi0);
        printf("b=%6.3f m=%2d defl_exact=%9.5f defl_band=%9.5f  err=%9.3e  loops=%5.2f  xcross=%ld%s\n",
               b, ms[im], de, db, fabs(db - de) / de, pe / M_PI, xc,
               fabs(db - de) / de > 0.01 ? "  ** >1% **" : "");
      }
    }
  }

  printf("\n== photon-capture critical b (bisection on far launch, m=16) ==\n");
  m_bands = 16;
  double lo = 3.0, hi = 8.0;   /* lo = captured side, hi = scattered side */
  for (int i = 0; i < 40; i++) {
    double mid = 0.5 * (lo + hi);
    if (run_light(3, mid, r0, u_end, h, NULL) < 0) lo = mid; else hi = mid;
  }
  printf("banded b_crit = %.5f   exact = %.5f   rel diff = %.3e\n",
         lo, 3 * sqrt(3.0), fabs(lo - 3 * sqrt(3.0)) / (3 * sqrt(3.0)));

  /* halved-step convergence */
  double d1[8] = {0}, d2[8] = {0}, a, b2;
  double up = 1.0 / 6.5, ua = up * 0.05 / 1.95;
  run_timelike(0, up, ua, h / 2, d1, &a, &b2, 4);
  run_timelike(1, up, ua, h / 2, d2, &a, &b2, 4);
  printf("\nhalved-step (e=0.95, r_p=6.5): exact dphi=%.9f banded dphi=%.9f\n",
         d1[3], d2[3]);
  double pe = run_light(2, 5.60, r0, u_end, h / 2, NULL);
  double pb = run_light(3, 5.60, r0, u_end, h / 2, NULL);
  double phi0 = asin(5.60 / r0);
  printf("halved-step (b=5.6): defl_exact=%.9f defl_band=%.9f\n",
         pe - (M_PI - 2 * phi0), pb - (M_PI - 2 * phi0));
  printf("\nwall time: %.2f s\n", (double)(clock() - t0) / CLOCKS_PER_SEC);
  return 0;
}
