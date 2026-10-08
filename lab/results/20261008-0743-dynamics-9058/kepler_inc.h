static void stumpff(double z, double *C, double *S) {
    if (z > 1e-8) { double sz = sqrt(z); *C = (1 - cos(sz)) / z; *S = (sz - sin(sz)) / (z * sz); }
    else if (z < -1e-8) { double sz = sqrt(-z); *S = (sinh(sz) - sz) / pow(-z, 1.5); *C = (cosh(sz) - 1) / (-z); }
    else { *C = 0.5 - z / 24.0 + z * z / 720.0; *S = 1.0 / 6.0 - z / 120.0 + z * z / 5040.0; }
}

static void kepler(St *s, double dt) {
    if (dt == 0) return;
    double r0 = hypot(s->x, s->y), v2 = s->vx * s->vx + s->vy * s->vy;
    double rdv = s->x * s->vx + s->y * s->vy, alpha = 2.0 / r0 - v2 / GMS;
    double X = sqrt(GMS) * fabs(alpha) * dt;
    if (X == 0) X = 1e-12;
    for (int it = 0; it < 100; it++) {
        double z = alpha * X * X, C, S; stumpff(z, &C, &S);
        double F = (1 - alpha * r0) * X * X * X * S + rdv / sqrt(GMS) * X * X * C + r0 * X - sqrt(GMS) * dt;
        double dF = (1 - alpha * r0) * X * X * C + rdv / sqrt(GMS) * X * (1 - z * S) + r0;
        double dX = F / dF; X -= dX;
        if (fabs(dX) < 1e-14 * (1 + fabs(X))) break;
    }
    double z = alpha * X * X, C, S; stumpff(z, &C, &S);
    double f = 1 - X * X / r0 * C, g = dt - X * X * X / sqrt(GMS) * S;
    double xn = f * s->x + g * s->vx, yn = f * s->y + g * s->vy;
    double rn = hypot(xn, yn);
    double fd = sqrt(GMS) / (rn * r0) * X * (z * S - 1);
    double gd = 1 - X * X / rn * C;
    double vxn = fd * s->x + gd * s->vx, vyn = fd * s->y + gd * s->vy;
    s->x = xn; s->y = yn; s->vx = vxn; s->vy = vyn;
}

