/* redteam-93a4: does "gravity is news" compound for kicked sources?
 * Scene D: fixed dominant M; sources S,J (mass mSJ) on near-circular orbits
 * kicked by each other; reader T (massless) further out. Truth = instantaneous
 * Newtonian. Candidate = every non-dominant body read as "the tube the past
 * light cone last saw": retarded state propagated along the pure-M drift.
 * Laws: 0 naive (retarded position), 1 tube (design), 2 tube + 1/2 a tau^2.
 * Scene G (-g): mutual binary, no dominant mass, straight-line tube.
 * Build: gcc -O2 -o news news.c -lm
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define G 1.0
#define C 1.0

typedef struct { double x, y, vx, vy, ax, ay; } St;

static double GM;        /* dominant mass (0 in scene G) */
static double m_src[2];  /* S, J masses */
static int    nsrc;      /* 1 or 2 */

/* ring buffer of one source's history in one law */
typedef struct { St *b; int cap, head; long nsteps; double dt; St init; } Ring;

static St circle_at(St s, double t) { /* analytic pure-M circle through s */
    if (GM <= 0.0) { St o = { s.x + s.vx*t, s.y + s.vy*t, s.vx, s.vy, 0, 0 }; return o; }
    double r2 = s.x*s.x + s.y*s.y, r = sqrt(r2), om = sqrt(GM/(r2*r));
    double th = om*t, c = cos(th), sn = sin(th);
    St o = { s.x*c + (s.vx/om)*sn, s.y*c + (s.vy/om)*sn,
             -s.x*om*sn + s.vx*c, -s.y*om*sn + s.vy*c, 0, 0 };
    return o;
}
/* quadratic interp at time t (3 nearest grid points) */
static St ring_at(Ring *R, double t) {
    long n = R->nsteps;
    double sf = t / R->dt - 1.0; /* push n holds the state at t = n*dt */
    if (sf <= 0.0 || n < 2) return circle_at(R->init, t);
    if (sf > (double)n) sf = (double)n;
    long i = (long)floor(sf) - 1; if (i < 0) i = 0; if (i > n - 2) i = n - 2;
    double u = sf - (double)(i + 1);
    /* slots: modular indices for i, i+1, i+2 */
    long s0 = ((i % R->cap) + R->cap) % R->cap, s1 = (s0 + 1) % R->cap, s2 = (s0 + 2) % R->cap;
    St *p0 = &R->b[s0], *p1 = &R->b[s1], *p2 = &R->b[s2];
    double a0[6], a1[6], a2[6];
    memcpy(a0, p0, sizeof a0); memcpy(a1, p1, sizeof a1); memcpy(a2, p2, sizeof a2);
    St o; double *w = (double *)&o;
    for (int k = 0; k < 6; k++)
        w[k] = 0.5*u*(u-1)*a0[k] + (1-u*u)*a1[k] + 0.5*u*(u+1)*a2[k];
    return o;
}
static void ring_init(Ring *R, St s, int cap, double dt) {
    R->b = malloc(sizeof(St)*cap); R->cap = cap; R->head = -1; R->nsteps = -1;
    R->dt = dt; R->init = s;
}
static void ring_push(Ring *R, St s) {
    R->head = (R->head + 1) % R->cap; R->nsteps++; R->b[R->head] = s;
}
static St tube_fwd(St s, double tau) {
    if (GM <= 0.0) { /* scene G: free-float drift */
        St o = { s.x + s.vx*tau, s.y + s.vy*tau, s.vx, s.vy, 0, 0 }; return o;
    }
    double r2 = s.x*s.x + s.y*s.y, r = sqrt(r2), om = sqrt(GM/(r2*r));
    double th = om*tau, c = cos(th), sn = sin(th);
    St o = { s.x*c + (s.vx/om)*sn, s.y*c + (s.vy/om)*sn,
             -s.x*om*sn + s.vx*c, -s.y*om*sn + s.vy*c, 0, 0 };
    return o;
}
/* source state as the reader's light cone sees it, extended to now */
static St seen(Ring *R, double xr, double yr, double t, int law) {
    double tr = t - 1.0; /* first guess: current distance */
    double dx = ring_at(R, t).x - xr, dy = ring_at(R, t).y - yr;
    tr = t - sqrt(dx*dx + dy*dy) / C;
    St s;
    for (int it = 0; it < 16; it++) {
        s = ring_at(R, tr);
        dx = s.x - xr; dy = s.y - yr;
        tr = t - sqrt(dx*dx + dy*dy) / C;
    }
    s = ring_at(R, tr);
    double tau = t - tr;
    St o = tube_fwd(s, tau);
    if (law == 0) o = s;                       /* naive retarded position */
    if (law == 2) { /* carlip: add only the KICK acceleration (drift is already in the tube) */
        double r2 = s.x*s.x + s.y*s.y, r = sqrt(r2), fd = -GM/(r2*r);
        o.x += 0.5*(s.ax - fd*s.x)*tau*tau; o.y += 0.5*(s.ay - fd*s.y)*tau*tau; }
    return o;
}
static void pull(St src, double m, double xr, double yr, double *ax, double *ay) {
    double dx = src.x - xr, dy = src.y - yr, d2 = dx*dx + dy*dy, d = sqrt(d2);
    double f = G * m / (d2 * d);
    *ax += f * dx; *ay += f * dy;
}

int main(int argc, char **argv) {
    /* argv: kappa R mSJ law nPT noSJ scene(D|G) chk1 chk2 chk3 */
    double kappa = atof(argv[1]), R = atof(argv[2]), mSJ = atof(argv[3]);
    int law = atoi(argv[4]), nPT = atoi(argv[5]), noSJ = atoi(argv[6]);
    char scene = argv[7][0];
    double ch[3] = { atof(argv[8]), atof(argv[9]), atof(argv[10]) };

    St S[2], T;          /* S[0]=S, S[1]=J; T reader */
    double rS, PS, rT, PT, dt, tau_max, scaleS = 1.0;
    if (scene == 'G') {
        GM = 0.0; nsrc = 2; m_src[0] = m_src[1] = 0.5;
        double a = 1.0 / (4.0 * kappa * kappa); /* circular: v = omega*(a/2) = kappa */
        double om = sqrt(G * 1.0 / (a*a*a));
        rS = a; PS = 2*M_PI/om; rT = R*a; scaleS = a;
        S[0].x = a/2;  S[0].y = 0; S[0].vx = 0; S[0].vy =  kappa;
        S[1].x = -a/2; S[1].y = 0; S[1].vx = 0; S[1].vy = -kappa;
        double vT = sqrt(1.0/rT);
        T.x = rT; T.y = 0; T.vx = 0; T.vy = vT;
        PT = 2*M_PI*rT/vT;
        tau_max = 1.2*(rT + a);
        dt = PS/5000.0;
        (void)rS;
    } else {
        GM = 1.0; nsrc = 2; m_src[0] = m_src[1] = mSJ;
        rS = 1.0/(kappa*kappa); PS = 2*M_PI/kappa/kappa/kappa; scaleS = rS;
        double rJ = 2.17*rS, vJ = kappa/sqrt(2.17);
        rT = R*rS; double vT = 1.0/sqrt(rT);
        S[0].x = rS; S[0].y = 0; S[0].vx = 0; S[0].vy = kappa;
        S[1].x = rJ; S[1].y = 0; S[1].vx = 0; S[1].vy = vJ;
        T.x = rT; T.y = 0; T.vx = 0; T.vy = vT;
        PT = 2*M_PI*rT/vT;
        tau_max = 1.2*(rT + rJ);
        dt = PS/5000.0;
    }
    long nsteps = (long)(ch[2] * PT / dt);
    int cap = (int)(tau_max/dt) + 16;
    if (noSJ) nsrc = 2; /* histories still kept; interaction flags below */

    /* two laws side by side: [0] truth, [1] candidate */
    St Sl[2][2], Tl[2];
    Ring ring[2];
    for (int L = 0; L < 2; L++) {
        Sl[L][0] = S[0]; Sl[L][1] = S[1]; Tl[L] = T;
        for (int k = 0; k < 2; k++) ring_init(&ring[k], S[k], cap, dt);
    }
    /* accelerations */
    St Sn[2][2], Tn[2];
    for (int L = 0; L < 2; L++) {
        for (int k = 0; k < 2; k++) { Sl[L][k].ax = Sl[L][k].ay = 0; }
        Tl[L].ax = Tl[L].ay = 0;
        for (int k = 0; k < 2; k++) {
            double r2 = Sl[L][k].x*Sl[L][k].x + Sl[L][k].y*Sl[L][k].y;
            double f = -GM/(r2*sqrt(r2));
            Sl[L][k].ax = f*Sl[L][k].x; Sl[L][k].ay = f*Sl[L][k].y;
        }
        {
            double r2 = Tl[L].x*Tl[L].x + Tl[L].y*Tl[L].y;
            double f = -GM/(r2*sqrt(r2));
            Tl[L].ax += f*Tl[L].x; Tl[L].ay += f*Tl[L].y;
        }
        if (!noSJ) {
            for (int k = 0; k < 2; k++) {
                int j = 1-k;
                if (L == 0) pull(Sl[0][j], m_src[j], Sl[0][k].x, Sl[0][k].y, &Sl[0][k].ax, &Sl[0][k].ay);
                else { St v = seen(&ring[j], Sl[1][k].x, Sl[1][k].y, 0.0, law);
                       pull(v, m_src[j], Sl[1][k].x, Sl[1][k].y, &Sl[1][k].ax, &Sl[1][k].ay); }
            }
        }
        for (int k = 0; k < 2; k++) {
            if (L == 0) pull(Sl[0][k], m_src[k], Tl[0].x, Tl[0].y, &Tl[0].ax, &Tl[0].ay);
            else { St v = seen(&ring[k], Tl[1].x, Tl[1].y, 0.0, law);
                   pull(v, m_src[k], Tl[1].x, Tl[1].y, &Tl[1].ax, &Tl[1].ay); }
        }
    }

    double E0[2];
    double energy(int L) {
        double r2 = Tl[L].x*Tl[L].x + Tl[L].y*Tl[L].y;
        double E = 0.5*(Tl[L].vx*Tl[L].vx + Tl[L].vy*Tl[L].vy) - GM/sqrt(r2);
        for (int k = 0; k < 2; k++) {
            double dx = Tl[L].x - Sl[L][k].x, dy = Tl[L].y - Sl[L][k].y;
            E -= G*m_src[k]/sqrt(dx*dx + dy*dy);
        }
        return E;
    }
    E0[0] = energy(0); E0[1] = energy(1);
    double maxdE = 0; long nextchk = 0; int ci = 0;
    long chk_step[3] = { (long)(ch[0]*PT/dt), (long)(ch[1]*PT/dt), (long)(ch[2]*PT/dt) };

    printf("# scene=%c kappa=%g R=%g mSJ=%g law=%d noSJ=%d dt=%.4g PT=%.4g steps=%ld cap=%d\n",
           scene, kappa, R, mSJ, law, noSJ, dt, PT, nsteps, cap);

    for (long n = 1; n <= nsteps; n++) {
        double t = n * dt;
        /* push candidate-law history at time t BEFORE using (states are at t after full step below); we push at end */
        for (int L = 0; L < 2; L++) {
            /* velocity Verlet */
            for (int k = 0; k < 2; k++) {
                Sl[L][k].x += Sl[L][k].vx*dt + 0.5*Sl[L][k].ax*dt*dt;
                Sl[L][k].y += Sl[L][k].vy*dt + 0.5*Sl[L][k].ay*dt*dt;
            }
            Tl[L].x += Tl[L].vx*dt + 0.5*Tl[L].ax*dt*dt;
            Tl[L].y += Tl[L].vy*dt + 0.5*Tl[L].ay*dt*dt;
            /* new accelerations at t */
            for (int k = 0; k < 2; k++) {
                double r2 = Sl[L][k].x*Sl[L][k].x + Sl[L][k].y*Sl[L][k].y;
                double f = -GM/(r2*sqrt(r2));
                Sn[L][k].ax = f*Sl[L][k].x; Sn[L][k].ay = f*Sl[L][k].y;
                Sn[L][k].vx = Sl[L][k].vx; Sn[L][k].vy = Sl[L][k].vy;
            }
            if (!noSJ) for (int k = 0; k < 2; k++) {
                int j = 1-k;
                if (L == 0) pull(Sl[0][j], m_src[j], Sl[0][k].x, Sl[0][k].y, &Sn[0][k].ax, &Sn[0][k].ay);
                else { St v = seen(&ring[j], Sl[1][k].x, Sl[1][k].y, t, law);
                       pull(v, m_src[j], Sl[1][k].x, Sl[1][k].y, &Sn[1][k].ax, &Sn[1][k].ay); }
            }
            Tn[L].ax = Tn[L].ay = 0;
            {
                double r2 = Tl[L].x*Tl[L].x + Tl[L].y*Tl[L].y;
                double f = -GM/(r2*sqrt(r2));
                Tn[L].ax += f*Tl[L].x; Tn[L].ay += f*Tl[L].y;
            }
            for (int k = 0; k < 2; k++) {
                if (L == 0) pull(Sl[0][k], m_src[k], Tl[0].x, Tl[0].y, &Tn[0].ax, &Tn[0].ay);
                else { St v = seen(&ring[k], Tl[1].x, Tl[1].y, t, law);
                       pull(v, m_src[k], Tl[1].x, Tl[1].y, &Tn[1].ax, &Tn[1].ay); }
            }
            for (int k = 0; k < 2; k++) {
                Sl[L][k].vx += 0.5*(Sl[L][k].ax + Sn[L][k].ax)*dt;
                Sl[L][k].vy += 0.5*(Sl[L][k].ay + Sn[L][k].ay)*dt;
                Sl[L][k].ax = Sn[L][k].ax; Sl[L][k].ay = Sn[L][k].ay;
            }
            Tl[L].vx += 0.5*(Tl[L].ax + Tn[L].ax)*dt;
            Tl[L].vy += 0.5*(Tl[L].ay + Tn[L].ay)*dt;
            Tl[L].ax = Tn[L].ax; Tl[L].ay = Tn[L].ay;
        }
        ring_push(&ring[0], Sl[1][0]); ring_push(&ring[1], Sl[1][1]);
        /* store accelerations for the carlip variant */
        ring[0].b[ring[0].head].ax = Sl[1][0].ax; ring[0].b[ring[0].head].ay = Sl[1][0].ay;
        ring[1].b[ring[1].head].ax = Sl[1][1].ax; ring[1].b[ring[1].head].ay = Sl[1][1].ay;

        if (n >= chk_step[ci] || n == nsteps) {
            double dE = (energy(1) - energy(0)) / fabs(E0[0]);
            double dSelf = (energy(0) - E0[0]) / fabs(E0[0]);
            if (fabs(dE) > maxdE) maxdE = fabs(dE);
            double dxS = Sl[1][0].x - Sl[0][0].x, dyS = Sl[1][0].y - Sl[0][0].y;
            double dxT = Tl[1].x - Tl[0].x, dyT = Tl[1].y - Tl[0].y;
            printf("rT=%8.4f vT=%7.4f E=%10.3e  t/P_T=%6.2f  maxdE=%9.2e  dE=%9.2e  dEtruth(self)=%9.2e  dS/rS=%9.2e  dT/rT=%9.2e\n",
                   sqrt(Tl[0].x*Tl[0].x+Tl[0].y*Tl[0].y), sqrt(Tl[0].vx*Tl[0].vx+Tl[0].vy*Tl[0].vy), energy(0), t/PT, maxdE, dE, dSelf,
                   sqrt(dxS*dxS+dyS*dyS)/scaleS,
                   sqrt(dxT*dxT+dyT*dyT)/rT);
            fflush(stdout);
            if (ci < 2) ci++;
        }
    }
    return 0;
}
