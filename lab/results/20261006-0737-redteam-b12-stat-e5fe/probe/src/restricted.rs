//! The circular restricted three-body problem of B12-B14 (docs/law.md): a star of mass 1 − μ and a
//! planet of mass μ on a circle of separation `sep` about their barycentre, and a massless ship.
//! Units G = c = M_star + M_planet = 1. This is the judge's own reference, float64: a
//! Dormand-Prince 5(4) integrator whose every step is clipped to the requested time, so states
//! come out exactly at the times asked. `echo` answers with the same integrator holding the Jacobi
//! constant (see [`Integrator::conserving`]); the judge itself never does.
//!
//! The ship is integrated relative to the planet, with the axes still inertial (they neither
//! rotate nor accelerate): the equations are the same as in barycentric coordinates, but the
//! rounding of each step is then relative to the ship's distance from the planet (4.84e4 at the
//! surface) and not to 5e8, and the error control scales to that distance too. The star's tide
//! is written in the cancellation-free form (Encke's f(q)). Inputs and outputs are barycentric.
//! Inside the planet's radius its pull is that of a uniform sphere, so a ship that hits the planet
//! passes through it and the integration goes on, where a point mass would end it (in B12's chaos
//! a ship can hit: one did, at r = 6 after 65 periods); outside, the pull is exactly the point
//! mass's, and so is the Jacobi constant the judge reads.
//! The planet's phase Ω·t is computed in double-double, because in float64 it is off by 1e-13 rad
//! after 200 periods, and a law that knew the planet's place exactly would then be blamed for it.
use std::f64::consts::TAU;

/// The scene: a star of mass 1 − `mu` at (−sep·mu, 0) and a planet of mass `mu` at (sep·(1 − mu), 0)
/// at t = 0, counter-clockwise on a circle at the angular speed Ω = sep^(−3/2).
#[derive(Clone, Copy, Debug)]
pub struct Restricted {
    pub mu: f64,
    pub sep: f64,
    pub planet_radius: f64,
}
/// The one scene the gates use: mu = 1e-3, 5.27e8 M (5.2 AU of the Sun), planet radius 4.84e4 M.
pub const JUPITER: Restricted = Restricted { mu: 1e-3, sep: 5.27e8, planet_radius: 4.84e4 };

/// The relative tolerance of the reference, and of the finer rerun that tests it (docs/law.md).
pub const RTOL: f64 = 1e-12;
pub const RTOL_FINE: f64 = 1e-13;
/// A run that needs more accepted steps than this is given up: it has no answer.
const MAX_STEPS: u64 = 40_000_000;

/// (a + b, its rounding error), exactly.
fn two_sum(a: f64, b: f64) -> (f64, f64) {
    let s = a + b;
    let v = s - a;
    (s, (a - (s - v)) + (b - v))
}
/// (a·b, its rounding error), exactly.
fn two_prod(a: f64, b: f64) -> (f64, f64) {
    let p = a * b;
    (p, a.mul_add(b, -p))
}
/// A double-double product of (a0 + a1)·(b0 + b1).
fn dd_mul(a: (f64, f64), b: (f64, f64)) -> (f64, f64) {
    let (p, e) = two_prod(a.0, b.0);
    let (s, r) = two_sum(p, e + (a.0 * b.1 + a.1 * b.0));
    two_sum(s, r)
}
/// Ω = sep^(−3/2) as a double-double: the phase Ω·t of a planet 10^16 time units in is then good
/// to 1e-16 rad, where the same product in float64 is good to 1e-13.
fn omega_dd(sep: f64) -> (f64, f64) {
    let root = sep.sqrt();
    // sep^(3/2) = sep·root, with root corrected by one Newton step: root + (sep − root²)/(2·root).
    let (sq, sqe) = two_prod(root, root);
    let root = two_sum(root, ((sep - sq) - sqe) / (2.0 * root));
    let cube = dd_mul((sep, 0.0), root);
    // The reciprocal: q = 1/cube.0, then q·(2 − cube·q) refined once.
    let q = 1.0 / cube.0;
    let back = dd_mul(cube, (q, 0.0));
    let (hi, lo) = two_sum(1.0, -back.0);
    two_sum(q, q * (hi + lo - back.1))
}
/// Ω·t reduced to [−π, π] (rad), from Ω as a double-double.
fn phase_of(omega: (f64, f64), t: f64) -> f64 {
    let (hi, lo) = dd_mul(omega, (t, 0.0));
    let n = (hi / TAU).round();
    // The reduction hi − n·2π, with 2π to double-double.
    let (nh, nl) = two_prod(n, TAU);
    let (d, e) = two_sum(hi, -nh);
    d + (e - nl - n * 2.449_293_598_294_706_4e-16 + lo)
}

impl Restricted {
    /// Angular speed of the planet.
    pub fn omega(&self) -> f64 {
        self.sep.powf(-1.5)
    }
    /// The planet's phase Ω·t reduced to [−π, π], accurate to 1e-15 rad at any time (float64 alone
    /// would be off by 1e-13 rad after 200 periods, which moves the planet by 5e-5).
    pub fn phase(&self, t: f64) -> f64 {
        phase_of(omega_dd(self.sep), t)
    }
    /// Period of the planet.
    pub fn period(&self) -> f64 {
        TAU * self.sep.powf(1.5)
    }
    /// Hill radius sep·(mu/3)^(1/3).
    pub fn hill(&self) -> f64 {
        self.sep * (self.mu / 3.0).cbrt()
    }
    /// Radius of the sphere of influence sep·mu^(2/5).
    pub fn soi(&self) -> f64 {
        self.sep * self.mu.powf(0.4)
    }
    /// The planet's position and velocity at time t.
    pub fn planet(&self, t: f64) -> ([f64; 2], [f64; 2]) {
        let (s, c) = self.phase(t).sin_cos();
        let (r, v) = (self.sep * (1.0 - self.mu), self.sep * (1.0 - self.mu) * self.omega());
        ([r * c, r * s], [-v * s, v * c])
    }
    /// The star's position and velocity at time t.
    pub fn star(&self, t: f64) -> ([f64; 2], [f64; 2]) {
        let (s, c) = self.phase(t).sin_cos();
        let (r, v) = (self.sep * self.mu, self.sep * self.mu * self.omega());
        ([-r * c, -r * s], [v * s, -v * c])
    }
    /// The ship's distance from the planet at time t, from its barycentric state.
    pub fn planet_distance(&self, t: f64, ship: &[f64; 4]) -> f64 {
        let (p, _) = self.planet(t);
        (ship[0] - p[0]).hypot(ship[1] - p[1])
    }
    /// The Jacobi constant 2(1−μ)/r₁ + 2μ/r₂ + 2Ω(x·v_y − y·v_x) − v² of a barycentric inertial state at time t.
    pub fn jacobi(&self, t: f64, ship: &[f64; 4]) -> f64 {
        let ((s, _), r2) = (self.star(t), self.planet_distance(t, ship));
        let r1 = (ship[0] - s[0]).hypot(ship[1] - s[1]);
        2.0 * (1.0 - self.mu) / r1 + 2.0 * self.mu / r2 + 2.0 * self.omega() * (ship[0] * ship[3] - ship[1] * ship[2]) - (ship[2] * ship[2] + ship[3] * ship[3])
    }
    /// Heliocentric energy v²/2 − (1 − μ)/r and angular momentum x·v_y − y·v_x of a barycentric
    /// state at time t, with position and velocity taken relative to the star's own.
    pub fn heliocentric(&self, t: f64, ship: &[f64; 4]) -> (f64, f64) {
        let (p, v) = self.star(t);
        let (x, y, vx, vy) = (ship[0] - p[0], ship[1] - p[1], ship[2] - v[0], ship[3] - v[1]);
        (0.5 * (vx * vx + vy * vy) - (1.0 - self.mu) / x.hypot(y), x * vy - y * vx)
    }
    /// A barycentric state from a state relative to the planet (inertial axes) at time t.
    pub fn barycentric(&self, t: f64, rel: &[f64; 4]) -> [f64; 4] {
        let (p, v) = self.planet(t);
        [rel[0] + p[0], rel[1] + p[1], rel[2] + v[0], rel[3] + v[1]]
    }
    /// A state relative to the planet (inertial axes) from a barycentric state at time t.
    pub fn relative(&self, t: f64, ship: &[f64; 4]) -> [f64; 4] {
        let (p, v) = self.planet(t);
        [ship[0] - p[0], ship[1] - p[1], ship[2] - v[0], ship[3] - v[1]]
    }
}

/// Which equations of motion the integrator solves: the full problem, or a planted flaw.
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum Model {
    /// The reference.
    Full,
    /// `planted-notide`: inside R_SOI the ship feels only the planet, the star's tide is dropped.
    NoTide,
    /// `planted-kick`: the ship's planetocentric velocity is multiplied by this factor each time
    /// it enters the R_SOI sphere.
    Kick(f64),
}

/// The integrator. Its state is the ship relative to the planet.
pub struct Integrator<'a> {
    scene: &'a Restricted,
    model: Model,
    omega: f64,
    omega_dd: (f64, f64),
    /// The planet's radius.
    radius: f64,
    soi: f64,
    rtol: f64,
    t: f64,
    rel: [f64; 4],
    /// The step the controller wants next.
    h: f64,
    /// The derivative at (t, rel) when it is known (first-same-as-last).
    k1: Option<[f64; 4]>,
    steps: u64,
    /// The Jacobi constant to hold after every step, when the integrator is asked to conserve it.
    jacobi: Option<f64>,
    /// Whether to track the closest approach to the planet's centre (see [`Integrator::tracking`]).
    track: bool,
    /// The smallest distance from the planet's centre seen so far, when tracking.
    closest: f64,
}

/// √(a² + b²): the lengths here are nowhere near overflow, and this is much faster than `hypot`.
fn norm(a: f64, b: f64) -> f64 {
    (a * a + b * b).sqrt()
}

impl<'a> Integrator<'a> {
    /// An integrator at t = 0 for the barycentric `ship` state.
    pub fn new(scene: &'a Restricted, model: Model, rtol: f64, ship: [f64; 4]) -> Self {
        let rel = scene.relative(0.0, &ship);
        let h = 1e-3 * norm(rel[0], rel[1]) / norm(rel[2], rel[3]).max(f64::MIN_POSITIVE);
        Integrator { scene, model, omega: scene.omega(), omega_dd: omega_dd(scene.sep), radius: scene.planet_radius, soi: scene.soi(), rtol, t: 0.0, rel, h, k1: None, steps: 0, jacobi: None, track: false, closest: norm(rel[0], rel[1]) }
    }

    /// This integrator, but keeping the closest approach to the planet's centre (the oracle's domain:
    /// B12 and B13 exclude a seed whose reference passes inside the planet). Every accepted step is
    /// sampled at its end, and a step in which the radial velocity turns from inward to outward (a
    /// periapsis) is bisected to that turning point, where the distance is stationary, so the result
    /// is the minimum itself to the last bits and not a sampled bound. Opt-in: a bisection costs
    /// 64 more Dormand-Prince steps per periapsis, which B14 and B17 do not need.
    pub fn tracking(mut self) -> Self {
        self.track = true;
        self
    }

    /// The smallest distance from the planet's centre since t = 0 (the start included), when
    /// [`Integrator::tracking`] is on; otherwise the start's distance.
    pub fn closest(&self) -> f64 {
        self.closest
    }

    /// This integrator, but holding the Jacobi constant of the initial state: after every step the
    /// state is moved, by a relative 1e-12 or so, to where the constant is exact again (projection
    /// onto the invariant). The true motion conserves it, so this removes the integrator's own
    /// drift, which float64 cannot keep from growing, and nothing else.
    pub fn conserving(mut self) -> Self {
        let (a, b) = self.jacobi_parts((0.0, 1.0), &self.rel);
        self.jacobi = Some(a + b - self.rel[2] * self.rel[2] - self.rel[3] * self.rel[3]);
        self
    }

    /// The time the integrator has reached.
    pub fn time(&self) -> f64 {
        self.t
    }
    /// The ship's barycentric state now.
    pub fn state(&self) -> [f64; 4] {
        self.scene.barycentric(self.t, &self.rel)
    }

    /// d/dt of the state relative to the planet: the planet's pull and the star's tide.
    fn deriv(&self, t: f64, w: &[f64; 4]) -> [f64; 4] {
        let Restricted { mu, sep, .. } = *self.scene;
        let r2 = w[0] * w[0] + w[1] * w[1];
        let pull = if r2 < self.radius * self.radius { mu / (self.radius * self.radius * self.radius) } else { mu / (r2 * r2.sqrt()) };
        let (mut ax, mut ay) = (-pull * w[0], -pull * w[1]);
        if !(self.model == Model::NoTide && r2 < self.soi * self.soi) {
            let (s, c) = phase_of(self.omega_dd, t).sin_cos();
            let (dx, dy) = (sep * c, sep * s);
            // With D the planet's position from the star: tide = (D + w)/|D + w|³ − D/|D|³ = (w − f·D)/(sep³·u^(3/2)).
            let q = (w[0] * (2.0 * dx + w[0]) + w[1] * (2.0 * dy + w[1])) / (sep * sep);
            let u = 1.0 + q;
            let u32 = u * u.sqrt();
            let f = q * (3.0 + q * (3.0 + q)) / (1.0 + u32);
            let k = (1.0 - mu) / (sep * sep * sep * u32);
            ax -= k * (w[0] - f * dx);
            ay -= k * (w[1] - f * dy);
        }
        [w[2], w[3], ax, ay]
    }

    /// The planet's position and velocity from the sine and cosine of its phase.
    fn planet_of(&self, s: f64, c: f64) -> ([f64; 2], [f64; 2]) {
        let (r, v) = (self.scene.sep * (1.0 - self.scene.mu), self.scene.sep * (1.0 - self.scene.mu) * self.omega);
        ([r * c, r * s], [-v * s, v * c])
    }

    /// The Jacobi constant of the relative state w, with the planet's phase given by its sine and
    /// cosine (s, c), as a + b·λ − λ²·|w_v|², where λ scales the relative velocity w_v: (a, b).
    fn jacobi_parts(&self, (s, c): (f64, f64), w: &[f64; 4]) -> (f64, f64) {
        let Restricted { mu, sep, .. } = *self.scene;
        let cross = |p: [f64; 2], q: [f64; 2]| p[0] * q[1] - p[1] * q[0];
        let (p, vp) = self.planet_of(s, c);
        let xb = [p[0] + w[0], p[1] + w[1]];
        let (r1, r2) = (norm(sep * c + w[0], sep * s + w[1]), norm(w[0], w[1]));
        let a = 2.0 * (1.0 - mu) / r1 + 2.0 * mu / r2 + 2.0 * self.omega * cross(xb, vp) - (vp[0] * vp[0] + vp[1] * vp[1]);
        (a, 2.0 * self.omega * cross(xb, [w[2], w[3]]) - 2.0 * (vp[0] * w[2] + vp[1] * w[3]))
    }

    /// Moves the relative state, by the smallest step in units of its own distance and speed, so
    /// that the Jacobi constant is `c0` again (Newton on the constant's gradient, two rounds). A
    /// step's drift is far below 1e-6 of the state; a larger one, or a state at rest in the
    /// rotating frame (no gradient), is left alone.
    fn hold_jacobi(&self, t: f64, w: &mut [f64; 4], c0: f64) {
        let Restricted { mu, sep, .. } = *self.scene;
        let (s, c) = phase_of(self.omega_dd, t).sin_cos();
        let (p, vp) = self.planet_of(s, c);
        let (lp, lv) = (norm(w[0], w[1]), norm(w[2], w[3]));
        if lp < self.radius {
            return; // inside the planet the pull is not the point mass's, and neither is the constant
        }
        let scale = [lp, lp, lv, lv];
        let mut y = *w;
        for _ in 0..2 {
            let (a, b) = self.jacobi_parts((s, c), &y);
            let g = a + b - (y[2] * y[2] + y[3] * y[3]) - c0;
            let (xb, vb) = ([p[0] + y[0], p[1] + y[1]], [vp[0] + y[2], vp[1] + y[3]]);
            let (d, r2) = ([sep * c + y[0], sep * s + y[1]], norm(y[0], y[1]));
            let r1 = norm(d[0], d[1]);
            let (k1, k2) = (2.0 * (1.0 - mu) / (r1 * r1 * r1), 2.0 * mu / (r2 * r2 * r2));
            let grad = [
                -k1 * d[0] - k2 * y[0] + 2.0 * self.omega * vb[1],
                -k1 * d[1] - k2 * y[1] - 2.0 * self.omega * vb[0],
                -2.0 * self.omega * xb[1] - 2.0 * vb[0],
                2.0 * self.omega * xb[0] - 2.0 * vb[1],
            ];
            let norm2: f64 = (0..4).map(|i| (scale[i] * grad[i]).powi(2)).sum();
            if !(norm2 > 0.0) {
                return;
            }
            for i in 0..4 {
                y[i] -= g * scale[i] * scale[i] * grad[i] / norm2;
            }
        }
        if (0..4).all(|i| (y[i] - w[i]).abs() < 1e-6 * scale[i]) {
            *w = y;
        }
    }

    /// One Dormand-Prince step of size h from (t, y) with k1 = f(t, y): the fifth-order state, the
    /// error estimate, and f at the new state.
    fn rk(&self, t: f64, y: &[f64; 4], k1: &[f64; 4], h: f64) -> ([f64; 4], [f64; 4], [f64; 4]) {
        let lin = |terms: &[(f64, &[f64; 4])]| {
            let mut out = *y;
            for i in 0..4 {
                out[i] += h * terms.iter().map(|(a, k)| a * k[i]).sum::<f64>();
            }
            out
        };
        let k2 = self.deriv(t + h / 5.0, &lin(&[(1.0 / 5.0, k1)]));
        let k3 = self.deriv(t + 3.0 * h / 10.0, &lin(&[(3.0 / 40.0, k1), (9.0 / 40.0, &k2)]));
        let k4 = self.deriv(t + 4.0 * h / 5.0, &lin(&[(44.0 / 45.0, k1), (-56.0 / 15.0, &k2), (32.0 / 9.0, &k3)]));
        let k5 = self.deriv(t + 8.0 * h / 9.0, &lin(&[(19372.0 / 6561.0, k1), (-25360.0 / 2187.0, &k2), (64448.0 / 6561.0, &k3), (-212.0 / 729.0, &k4)]));
        let k6 = self.deriv(t + h, &lin(&[(9017.0 / 3168.0, k1), (-355.0 / 33.0, &k2), (46732.0 / 5247.0, &k3), (49.0 / 176.0, &k4), (-5103.0 / 18656.0, &k5)]));
        let y5 = lin(&[(35.0 / 384.0, k1), (500.0 / 1113.0, &k3), (125.0 / 192.0, &k4), (-2187.0 / 6784.0, &k5), (11.0 / 84.0, &k6)]);
        let k7 = self.deriv(t + h, &y5);
        let mut err = [0.0; 4];
        for i in 0..4 {
            err[i] = h * (71.0 / 57600.0 * k1[i] - 71.0 / 16695.0 * k3[i] + 71.0 / 1920.0 * k4[i] - 17253.0 / 339200.0 * k5[i] + 22.0 / 525.0 * k6[i] - 1.0 / 40.0 * k7[i]);
        }
        (y5, err, k7)
    }

    /// The error estimate in units of the tolerance: positions against the distance from the
    /// planet, velocities against the speed relative to it (each times rtol). At most 1 is accepted.
    fn scaled_error(&self, y: &[f64; 4], y5: &[f64; 4], err: &[f64; 4]) -> f64 {
        let sp = self.rtol * norm(y[0], y[1]).max(norm(y5[0], y5[1]));
        let sv = self.rtol * norm(y[2], y[3]).max(norm(y5[2], y5[3]));
        (err[0].abs().max(err[1].abs()) / sp).max(err[2].abs().max(err[3].abs()) / sv)
    }

    /// One accepted step no later than `limit`. None: the step size collapsed or the run is too long.
    fn step(&mut self, limit: f64) -> Option<()> {
        let k1 = self.k1.unwrap_or_else(|| self.deriv(self.t, &self.rel));
        loop {
            if self.steps > MAX_STEPS || !(self.h > 1e-15 * self.t.abs().max(1.0)) {
                return None;
            }
            let left = limit - self.t;
            let clipped = self.h >= left;
            let hs = if clipped { left } else { self.h };
            let (y5, err, k7) = self.rk(self.t, &self.rel, &k1, hs);
            let e = self.scaled_error(&self.rel, &y5, &err);
            let fac = if e > 0.0 { (0.9 * e.powf(-0.2)).clamp(0.2, 5.0) } else { 5.0 };
            if e <= 1.0 {
                self.steps += 1;
                let (t0, y0) = (self.t, self.rel);
                self.t = if clipped { limit } else { t0 + hs };
                self.rel = y5;
                self.k1 = Some(k7);
                if let Some(c0) = self.jacobi {
                    let mut w = self.rel;
                    self.hold_jacobi(self.t, &mut w, c0);
                    (self.rel, self.k1) = (w, None);
                }
                // A step clipped short of the natural size keeps the natural size for the next one.
                self.h = if clipped && fac > 1.0 { self.h.max(hs * fac) } else { hs * fac };
                if self.track {
                    self.closest = self.closest.min(norm(y5[0], y5[1]));
                    let radial = |w: &[f64; 4]| w[0] * w[2] + w[1] * w[3];
                    if radial(&y0) < 0.0 && radial(&y5) >= 0.0 {
                        let (_, w) = self.crossing(t0, &y0, &k1, hs, |w| radial(w) >= 0.0);
                        self.closest = self.closest.min(norm(w[0], w[1]));
                    }
                }
                if let Model::Kick(factor) = self.model {
                    if norm(y0[0], y0[1]) >= self.soi && norm(y5[0], y5[1]) < self.soi {
                        let (h, mut w) = self.crossing(t0, &y0, &k1, hs, |w| norm(w[0], w[1]) < self.soi);
                        w[2] *= factor;
                        w[3] *= factor;
                        (self.t, self.rel, self.k1) = (t0 + h, w, None);
                    }
                }
                return Some(());
            }
            self.h = hs * fac;
        }
    }

    /// Where inside the step of size `hs` from (t0, y0) the predicate `beyond` first turns true (it
    /// is false at y0 and true at the end): the step size and the state there, by bisection on the
    /// step size, which lands on the far side.
    fn crossing(&self, t0: f64, y0: &[f64; 4], k1: &[f64; 4], hs: f64, beyond: impl Fn(&[f64; 4]) -> bool) -> (f64, [f64; 4]) {
        let (mut lo, mut hi) = (0.0, hs);
        for _ in 0..64 {
            let mid = 0.5 * (lo + hi);
            if beyond(&self.rk(t0, y0, k1, mid).0) {
                hi = mid;
            } else {
                lo = mid;
            }
        }
        (hi, self.rk(t0, y0, k1, hi).0)
    }

    /// Advances to time `to` (not before the current time) and returns the barycentric state
    /// there. None: the integration gave up.
    pub fn advance(&mut self, to: f64) -> Option<[f64; 4]> {
        while self.t < to {
            self.step(to)?;
        }
        Some(self.state())
    }

    /// Advances to the first time, before `limit`, at which the distance from the planet crosses
    /// `radius` going out (`outward`) or coming in. Returns that time, to the last bit of the
    /// step size; the integrator stands there, just past the sphere. None: no crossing before
    /// `limit`, or the integration gave up. Meant for the full model.
    pub fn until_crossing(&mut self, radius: f64, outward: bool, limit: f64) -> Option<f64> {
        let beyond = |w: &[f64; 4]| (norm(w[0], w[1]) >= radius) == outward;
        if beyond(&self.rel) {
            return Some(self.t);
        }
        while self.t < limit {
            let (t0, y0) = (self.t, self.rel);
            let k1 = self.k1.unwrap_or_else(|| self.deriv(t0, &y0));
            self.step(limit)?;
            if beyond(&self.rel) {
                let (h, w) = self.crossing(t0, &y0, &k1, self.t - t0, beyond);
                (self.t, self.rel, self.k1) = (t0 + h, w, None);
                return Some(self.t);
            }
        }
        None
    }
}

/// The barycentric states of the `ship` at each of `times` (ascending, all ≥ 0) in `model`, to
/// relative tolerance `rtol`. None: the integration gave up.
pub fn integrate(scene: &Restricted, model: Model, rtol: f64, ship: [f64; 4], times: &[f64]) -> Option<Vec<[f64; 4]>> {
    let mut it = Integrator::new(scene, model, rtol, ship);
    times.iter().map(|&t| it.advance(t)).collect()
}

/// The reference: the full problem to relative tolerance `rtol`.
pub fn reference(scene: &Restricted, ship: [f64; 4], times: &[f64], rtol: f64) -> Option<Vec<[f64; 4]>> {
    integrate(scene, Model::Full, rtol, ship, times)
}

/// The same states from an integrator that holds the Jacobi constant of the initial state exactly
/// (see [`Integrator::conserving`]).
pub fn conserving_reference(scene: &Restricted, ship: [f64; 4], times: &[f64], rtol: f64) -> Option<Vec<[f64; 4]>> {
    let mut it = Integrator::new(scene, Model::Full, rtol, ship).conserving();
    times.iter().map(|&t| it.advance(t)).collect()
}

