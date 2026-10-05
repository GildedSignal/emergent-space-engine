//! The oracle of B19 (docs/law.md, "Rotating holes"): equatorial Kerr geodesics in float64, G = c = M = 1,
//! spin a = χ in [0, 1), Boyer-Lindquist coordinates. Nothing here is a law, and no engine crate is imported.
//!
//! Written from the textbook: Bardeen, Press and Teukolsky 1972 (BPT: the ISCO, the photon orbit, the
//! marginally bound orbit, circular orbits, the ZAMO) and Chandrasekhar, *The Mathematical Theory of Black
//! Holes* (the equatorial radial potential). With Σ = r² and Δ = r² − 2r + a², a unit-mass geodesic of
//! energy E = −p_t and angular momentum L = p_φ (L > 0: it circles with the spin) obeys
//!
//! ```text
//! x = L − aE,  P(r) = E(r² + a²) − aL,   r⁴ (dr/dτ)² = R(r) = r·C(r),
//! C(r) = (E² − 1) r³ + 2r² − (a² + x² + 2axE) r + 2x²,
//! r² dφ/dτ = x + aP/Δ,   r² dt/dτ = a·x + (r² + a²)P/Δ.
//! ```
//!
//! Light is the same with E = 1, L = b and no "−1" nor "2r²" terms. A state is future-directed iff dt/dτ > 0, which has the sign of
//! E − ωL (u^t = A(E − ωL)/(r²Δ), A = (r² + a²)² − a²Δ, ω = 2ar/A), not of P. The oracle tests P ≥ 0, which agrees with it on every
//! state with R ≥ 0: the band where P > 0 but E − ωL < 0 has R < 0 throughout (GLM red-team, lab run 20261005-1540, 800,000 states;
//! `future_directed_is_p_nonnegative_on_allowed_states` below). Future-directed geodesics with E < 0 exist inside the ergosphere and plunge.
//!
//! - Bound orbits are labelled by Darwin's (p, e) and a sense (+1: with the spin, −1: against it), r = p/(1 + e cos ψ).
//!   Their (E, L) come in closed form (Glampedakis and Kennefick 2002, re-derived here: a quadratic in x²),
//!   polished by Newton on the two turning-point equations. In u = 1/r the potential is
//!   g(u) = 2x²(u − u_a)(u_p − u)(u_c − u), so du/√g = dψ/(√2·|x|·√(u_c − u)): smooth and even in ψ, and the
//!   trapezoid rule converges geometrically (doubled until two sums agree to 1e-15). The orbit is stable (it
//!   has a periapsis outside the horizon) iff u_c > u_p; u_c = u_p is the separatrix, whose e = 0 limit is the ISCO.
//! - Light's deflection: Δφ = 2∫ F du/√Q with the turning point factored out exactly and u = u0(1 − t²).
//! - χ = 0 is Schwarzschild: the same code runs at a = 0, and `echo` answers χ = 0 with the existing
//!   Schwarzschild oracle (`oracle.rs`), which this one reproduces to 1e-10 (tests).
//!
//! The oracle's own error is measured against mpmath (`kerr_mpmath.py`, `kerr_mp.json`): see `agreement`.
use std::f64::consts::PI;

/// Equatorial radius of the ergosphere (static observers exist only outside it): r = 2M, whatever the spin.
pub const ERGOSPHERE: f64 = 2.0;

/// What becomes of a body that starts at its outer turning point (E < 1) or arrives from infinity (E >= 1).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Fate {
    /// E < 1: a periapsis outside the horizon: it cycles for ever.
    Bound,
    /// E < 1: no periapsis outside the horizon: it falls in.
    Plunge,
    /// E >= 1: a turning point outside the horizon: it leaves again.
    Scattered,
    /// E >= 1: no turning point outside the horizon: it is absorbed.
    Captured,
}

/// One bound cycle: the periapsis advance beyond 2π in the direction of motion, the radial period in
/// coordinate time and in proper time, and the oracle's own convergence (relative change of the last doubling).
#[derive(Clone, Copy, Debug)]
pub struct Cycle {
    pub advance: f64,
    pub period: f64,
    pub proper_period: f64,
    pub converged: f64,
}

/// A rotating hole of spin a = χ (M = 1).
#[derive(Clone, Copy, Debug)]
pub struct Kerr {
    pub a: f64,
}

/// Real roots of c[0] r³ + c[1] r² + c[2] r + c[3], descending, polished by Newton (degenerate leading terms allowed).
pub fn real_roots(c: [f64; 4]) -> Vec<f64> {
    let eval = |r: f64| ((c[0] * r + c[1]) * r + c[2]) * r + c[3];
    let slope = |r: f64| (3.0 * c[0] * r + 2.0 * c[1]) * r + c[2];
    let mut roots: Vec<f64> = if c[0] == 0.0 {
        if c[1] == 0.0 {
            if c[2] == 0.0 {
                Vec::new()
            } else {
                vec![-c[3] / c[2]]
            }
        } else {
            let disc = c[2] * c[2] - 4.0 * c[1] * c[3];
            if disc < 0.0 {
                Vec::new()
            } else {
                // The stable form: no cancellation between −c2 and the root.
                let sign = if c[2] < 0.0 { -1.0 } else { 1.0 };
                let q = -0.5 * (c[2] + sign * disc.sqrt());
                let mut r = vec![q / c[1]];
                if q != 0.0 {
                    r.push(c[3] / q);
                }
                r
            }
        }
    } else {
        let (a, b, d) = (c[1] / c[0], c[2] / c[0], c[3] / c[0]);
        let p = b - a * a / 3.0;
        let q = 2.0 * a * a * a / 27.0 - a * b / 3.0 + d;
        let disc = (q / 2.0) * (q / 2.0) + (p / 3.0).powi(3);
        let shift = -a / 3.0;
        if disc < 0.0 {
            let m = 2.0 * (-p / 3.0).sqrt();
            let theta = ((3.0 * q) / (p * m)).clamp(-1.0, 1.0).acos() / 3.0;
            (0..3).map(|k| shift + m * (theta - 2.0 * PI * k as f64 / 3.0).cos()).collect()
        } else {
            let s = disc.sqrt();
            vec![shift + (-q / 2.0 + s).cbrt() + (-q / 2.0 - s).cbrt()]
        }
    };
    for r in roots.iter_mut() {
        for _ in 0..4 {
            let d = slope(*r);
            if d == 0.0 || !d.is_finite() {
                break;
            }
            let step = eval(*r) / d;
            if !step.is_finite() || step.abs() > 1e-3 * (1.0 + r.abs()) {
                break;
            }
            *r -= step;
        }
    }
    roots.sort_by(|x, y| y.total_cmp(x));
    roots
}

/// Gauss–Legendre nodes and weights on [−1, 1] (Newton on the Legendre recurrence).
fn gauss_legendre(n: usize) -> Vec<(f64, f64)> {
    (1..=n)
        .map(|i| {
            let mut x = (PI * (i as f64 - 0.25) / (n as f64 + 0.5)).cos();
            let mut dp = 1.0;
            for _ in 0..100 {
                let (mut p0, mut p1) = (1.0, x);
                for k in 2..=n {
                    let p2 = ((2 * k - 1) as f64 * x * p1 - (k - 1) as f64 * p0) / k as f64;
                    (p0, p1) = (p1, p2);
                }
                dp = n as f64 * (x * p1 - p0) / (x * x - 1.0);
                let dx = p1 / dp;
                x -= dx;
                if dx.abs() < 1e-16 {
                    break;
                }
            }
            (x, 2.0 / ((1.0 - x * x) * dp * dp))
        })
        .collect()
}

impl Kerr {
    pub fn new(a: f64) -> Kerr {
        assert!((0.0..1.0).contains(&a), "spin {a} outside [0, 1)");
        Kerr { a }
    }
    /// The outer horizon r₊ = 1 + √(1 − a²).
    pub fn horizon(&self) -> f64 {
        1.0 + (1.0 - self.a * self.a).sqrt()
    }
    /// The ISCO radius (BPT 2.21); `s` = +1 with the spin, −1 against it.
    pub fn isco(&self, s: f64) -> f64 {
        let a = self.a;
        let z1 = 1.0 + (1.0 - a * a).cbrt() * ((1.0 + a).cbrt() + (1.0 - a).cbrt());
        let z2 = (3.0 * a * a + z1 * z1).sqrt();
        3.0 + z2 - s * ((3.0 - z1) * (3.0 + z1 + 2.0 * z2)).sqrt()
    }
    /// The circular photon orbit's radius (BPT 2.18).
    pub fn photon_orbit(&self, s: f64) -> f64 {
        2.0 * (1.0 + (2.0 / 3.0 * (-s * self.a).acos()).cos())
    }
    /// The marginally bound orbit (E = 1): its radius and angular momentum (BPT 2.20 and 2.22).
    pub fn marginally_bound(&self, s: f64) -> (f64, f64) {
        let a = self.a;
        let w = (1.0 - s * a).sqrt();
        (2.0 - s * a + 2.0 * w, s * 2.0 * (1.0 + w))
    }
    /// The critical impact parameter b = L/E of light of this sense: light with b between the retrograde (negative)
    /// and the prograde (positive) one is captured. From R = R' = 0 at the photon orbit: P = ±√Δ·(b − a).
    pub fn photon_b(&self, s: f64) -> f64 {
        let (a, r) = (self.a, self.photon_orbit(s));
        let d = (r * r - 2.0 * r + a * a).max(0.0).sqrt();
        if s > 0.0 {
            (r * r + a * a + a * d) / (a + d)
        } else {
            -(r * r + a * a - a * d) / (d - a)
        }
    }
    /// (E, L) of the circular orbit at r (BPT 2.12 and 2.13); None at or inside the photon orbit.
    pub fn circular(&self, r: f64, s: f64) -> Option<(f64, f64)> {
        let a = self.a;
        let sr = r.sqrt();
        let w = r.powf(1.5) - 3.0 * sr + 2.0 * s * a;
        if r <= self.photon_orbit(s) || w <= 0.0 {
            return None;
        }
        let d = r.powf(0.75) * w.sqrt();
        Some(((r.powf(1.5) - 2.0 * sr + s * a) / d, s * (r * r - 2.0 * s * a * sr + a * a) / d))
    }
    /// The ZAMO frame on the equator: (lapse α, angular velocity ω, g_φφ). α² = r²Δ/A, ω = 2ar/A, g_φφ = A/r².
    pub fn zamo(&self, r: f64) -> (f64, f64, f64) {
        let a = self.a;
        let delta = r * r - 2.0 * r + a * a;
        let big_a = (r * r + a * a).powi(2) - a * a * delta;
        ((r * r * delta / big_a).sqrt(), 2.0 * a * r / big_a, big_a / (r * r))
    }
    /// dτ/dt of a static observer, √(1 − 2/r) whatever the spin (g_tt on the equator); None at r <= 2: none can stay there.
    pub fn static_rate(&self, r: f64) -> Option<f64> {
        (r > ERGOSPHERE).then(|| (1.0 - 2.0 / r).sqrt())
    }
    /// dτ/dt of the ZAMO at r (the lapse); defined down to the horizon.
    pub fn zamo_rate(&self, r: f64) -> Option<f64> {
        (r > self.horizon()).then(|| self.zamo(r).0)
    }

    /// The coefficients of C(r) = R(r)/r, highest first.
    pub fn cubic(&self, e: f64, l: f64) -> [f64; 4] {
        let a = self.a;
        let x = l - a * e;
        [e * e - 1.0, 2.0, -(a * a + x * x + 2.0 * a * x * e), 2.0 * x * x]
    }
    /// The radial potential R(r) of a unit-mass geodesic.
    pub fn radial(&self, e: f64, l: f64, r: f64) -> f64 {
        let c = self.cubic(e, l);
        r * (((c[0] * r + c[1]) * r + c[2]) * r + c[3])
    }
    /// The sum of the absolute values of R's terms at r: the scale against which R(r)'s sign is believed.
    pub fn radial_scale(&self, e: f64, l: f64, r: f64) -> f64 {
        let c = self.cubic(e, l);
        r * (c[0].abs() * r * r * r + c[1].abs() * r * r + c[2].abs() * r + c[3].abs())
    }
    /// P(r) = E(r² + a²) − aL. dt/dτ has the sign of E − ωL, not of P, but where R ≥ 0 the two agree (module docs), so `allowed` reads
    /// "future-directed" as P ≥ 0.
    pub fn forward(&self, e: f64, l: f64, r: f64) -> f64 {
        e * (r * r + self.a * self.a) - self.a * l
    }
    /// Can a unit-mass body with (E, L) be at r: outside the horizon, R >= 0 and future-directed?
    pub fn allowed(&self, e: f64, l: f64, r: f64) -> bool {
        r > self.horizon() && self.radial(e, l, r) >= 0.0 && self.forward(e, l, r) >= 0.0
    }
    /// (dφ/dt, dτ/dt) of the tube through r with constants (E, L); None where there is none (not allowed).
    pub fn tube_rates(&self, e: f64, l: f64, r: f64) -> Option<(f64, f64)> {
        if !self.allowed(e, l, r) {
            return None;
        }
        let a = self.a;
        let (x, p, delta) = (l - a * e, self.forward(e, l, r), r * r - 2.0 * r + a * a);
        let t = a * x + (r * r + a * a) * p / delta;
        Some(((x + a * p / delta) / t, r * r / t))
    }
    /// (E, L) of a unit-mass body at r whose velocity in the ZAMO frame is (v_r, v_φ): E = αγ + ωL, L = √g_φφ·γ·v_φ.
    pub fn state_constants(&self, r: f64, v_r: f64, v_phi: f64) -> (f64, f64) {
        let (alpha, omega, gpp) = self.zamo(r);
        let gamma = 1.0 / (1.0 - v_r * v_r - v_phi * v_phi).sqrt();
        let l = gpp.sqrt() * gamma * v_phi;
        (alpha * gamma + omega * l, l)
    }
    /// The Penrose split of a unit-mass body at a radial turning point r with constants (E0, L0) into two photons
    /// moving along +φ̂ and −φ̂ in the ZAMO frame: ((E, L) forward, (E, L) backward). Local energies are
    /// (ε₀ ± p_φ̂)/2 with ε₀ = (E₀ − ωL₀)/α and p_φ̂ = L₀/√g_φφ; E = αε + ωL, L = ±ε√g_φφ.
    /// None if the state is not at a turning point of a unit-mass body (|ε₀² − p_φ̂² − 1| > 1e-9 ε₀²).
    pub fn split(&self, e0: f64, l0: f64, r: f64) -> Option<[(f64, f64); 2]> {
        if r <= self.horizon() {
            return None;
        }
        let (alpha, omega, gpp) = self.zamo(r);
        let sg = gpp.sqrt();
        let (eps0, pphi) = ((e0 - omega * l0) / alpha, l0 / sg);
        if (eps0 * eps0 - pphi * pphi - 1.0).abs() > 1e-9 * eps0 * eps0 || eps0 <= 0.0 {
            return None;
        }
        let (ef, eb) = (0.5 * (eps0 + pphi), 0.5 * (eps0 - pphi));
        let (lf, lb) = (ef * sg, -eb * sg);
        Some([(alpha * ef + omega * lf, lf), (alpha * eb + omega * lb, lb)])
    }

    /// (E, L) of the orbit with Darwin parameters (p, e) and sense s, in closed form and then polished; None if there is none
    /// (no real root, or E outside (0, 1), or the wrong sense of L).
    pub fn bound_constants(&self, p: f64, e: f64, s: f64) -> Option<(f64, f64)> {
        let a = self.a;
        if a == 0.0 {
            // Schwarzschild: E² = ((p − 2)² − 4e²)/(p(p − 3 − e²)), L² = p²/(p − 3 − e²).
            let d = p - 3.0 - e * e;
            let en2 = ((p - 2.0).powi(2) - 4.0 * e * e) / (p * d);
            return (d > 0.0 && en2 > 0.0 && en2 < 1.0).then(|| (en2.sqrt(), s * p / d.sqrt()));
        }
        let (up, ua) = ((1.0 + e) / p, (1.0 - e) / p);
        let (al0, al1) = (p - a * a, ((3.0 + e * e) - p) / p);
        let c0 = 1.0 - 2.0 * ua + a * a * ua * ua + al0 * ua * ua;
        let c1 = ua * ua + al1 * ua * ua - 2.0 * ua * ua * ua;
        let (f, n, c) = (al1 * al1 - 4.0 * a * a * c1, 2.0 * al0 * al1 - 4.0 * a * a * c0, al0 * al0);
        let disc = n * n - 4.0 * f * c;
        if disc < 0.0 || f == 0.0 {
            return None;
        }
        // The two roots of F y² + N y + C = 0, y = x² (the stable form). Each positive root gives one candidate, x = sign(A)·√y so
        // that E = A/(2ax) > 0, with A = α0 + α1·y; its sense is the sign of L = x + aE. Prograde is the smaller y, retrograde the larger.
        let q = -0.5 * (n + if n < 0.0 { -1.0 } else { 1.0 } * disc.sqrt());
        let mut best: Option<(f64, f64, f64)> = None;
        for y in [q / f, if q != 0.0 { c / q } else { f64::NAN }] {
            let big_a = al0 + al1 * y;
            if !(y > 0.0) || big_a == 0.0 {
                continue;
            }
            let x = big_a.signum() * y.sqrt();
            let en = big_a / (2.0 * a * x);
            if !(en > 0.0 && en < 1.0 && (x + a * en) * s > 0.0) {
                continue;
            }
            if best.map_or(true, |(by, _, _)| if s > 0.0 { y < by } else { y > by }) {
                best = Some((y, x, en));
            }
        }
        let (_, mut x, mut en) = best?;
        // Newton on g(u_p) = g(u_a) = 0 for (E, x): g(u) = (E² − 1) + 2u − (a² + x² + 2axE)u² + 2x²u³. A step is kept only if it
        // lowers the residual (the Jacobian is singular as e → 0, where the two equations coincide).
        let g = |u: f64, en: f64, x: f64| (en * en - 1.0) + 2.0 * u - (a * a + x * x + 2.0 * a * x * en) * u * u + 2.0 * x * x * u * u * u;
        let residual = |en: f64, x: f64| g(up, en, x).abs() + g(ua, en, x).abs();
        for _ in 0..4 {
            let (g1, g2) = (g(up, en, x), g(ua, en, x));
            let d = |u: f64| (2.0 * en - 2.0 * a * x * u * u, -(2.0 * x + 2.0 * a * en) * u * u + 4.0 * x * u * u * u);
            let ((a1, b1), (a2, b2)) = (d(up), d(ua));
            let det = a1 * b2 - a2 * b1;
            let (de, dx) = ((g1 * b2 - g2 * b1) / det, (a1 * g2 - a2 * g1) / det);
            if !(de.is_finite() && dx.is_finite()) || residual(en - de, x - dx) >= residual(en, x) {
                break;
            }
            en -= de;
            x -= dx;
        }
        let l = x + a * en;
        (en > 0.0 && en < 1.0 && l * s > 0.0).then_some((en, l))
    }
    /// u_c = 1/r₃, the third root of g in u, from Vieta: (a² + x² + 2axE)/(2x²) − 2/p. The orbit is stable iff u_c > u_p.
    fn third_root(&self, p: f64, en: f64, l: f64) -> f64 {
        let (a, x) = (self.a, l - self.a * en);
        (a * a + x * x + 2.0 * a * x * en) / (2.0 * x * x) - 2.0 / p
    }
    /// Does a stable bound orbit (a periapsis outside the horizon, and the apoapsis reached from outside) have Darwin (p, e) and sense s?
    pub fn stable(&self, p: f64, e: f64, s: f64) -> bool {
        match self.bound_constants(p, e, s) {
            Some((en, l)) => {
                p / (1.0 + e) > self.horizon() && self.third_root(p, en, l) > (1.0 + e) / p && self.forward(en, l, p / (1.0 + e)) > 0.0
            }
            None => false,
        }
    }
    /// The separatrix p_s(e, s): the largest p below which no stable bound orbit of eccentricity e has this sense.
    /// At e = 0 it is the ISCO radius. Found by scanning down from p = 400 and bisecting the first loss of stability.
    pub fn separatrix(&self, e: f64, s: f64) -> f64 {
        let mut hi = 400.0;
        let mut lo = hi / 1.02;
        while self.stable(lo, e, s) && lo > 1.0 + 1e-9 {
            hi = lo;
            lo /= 1.02;
        }
        for _ in 0..80 {
            let mid = 0.5 * (lo + hi);
            if self.stable(mid, e, s) {
                hi = mid;
            } else {
                lo = mid;
            }
        }
        hi
    }

    /// The bound-orbit window at the separatrix of eccentricity e: (E_s, L_s, W). At the separatrix's angular momentum L_s the
    /// potential has its barrier at energy E_s (above it: plunge) and its stable circular orbit at E_s − W (between them: bound).
    pub fn separatrix_window(&self, e: f64, s: f64) -> Option<(f64, f64, f64)> {
        let (es, ls) = self.bound_constants(self.separatrix(e, s), e, s)?;
        // L_circ(r) rises from the ISCO outwards: find the stable circular orbit of angular momentum L_s.
        let (mut lo, mut hi) = (self.isco(s), 1e5);
        for _ in 0..200 {
            let mid = 0.5 * (lo + hi);
            if self.circular(mid, s)?.1 * s < ls * s {
                lo = mid;
            } else {
                hi = mid;
            }
        }
        Some((es, ls, es - self.circular(0.5 * (lo + hi), s)?.0))
    }

    /// One radial cycle of the stable orbit (p, e, s): None if there is none. Trapezoid in Darwin's ψ, doubled to convergence.
    pub fn cycle(&self, p: f64, e: f64, s: f64) -> Option<Cycle> {
        let a = self.a;
        let (en, l) = self.bound_constants(p, e, s)?;
        if !self.stable(p, e, s) {
            return None;
        }
        let (x, uc) = (l - a * en, self.third_root(p, en, l));
        // (dφ, dt, dτ) per unit ψ.
        let f = |psi: f64| -> [f64; 3] {
            let u = (1.0 + e * psi.cos()) / p;
            let r = 1.0 / u;
            let delta = r * r - 2.0 * r + a * a;
            let pp = en * (r * r + a * a) - a * l;
            let w = 1.0 / (std::f64::consts::SQRT_2 * x.abs() * (uc - u).sqrt());
            [(x + a * pp / delta) * w, (a * x + (r * r + a * a) * pp / delta) * w, r * r * w]
        };
        // The cycle is twice ∫₀^π of the integrand (ψ and its mirror). The trapezoid on [0, π] with n intervals,
        // then 2n (the old nodes kept, the midpoints added), until two sums agree.
        let (f0, f1) = (f(0.0), f(PI));
        let ends: [f64; 3] = std::array::from_fn(|i| 0.5 * (f0[i] + f1[i]));
        let mut n = 32usize;
        let mut inner = [0.0f64; 3];
        for k in 1..n {
            let v = f(PI * k as f64 / n as f64);
            for i in 0..3 {
                inner[i] += v[i];
            }
        }
        let value = |inner: &[f64; 3], n: usize| -> [f64; 3] { std::array::from_fn(|i| 2.0 * PI / n as f64 * (ends[i] + inner[i])) };
        let mut cur = value(&inner, n);
        let mut converged = f64::INFINITY;
        while converged >= 2e-15 && n < 1 << 17 {
            for k in 0..n {
                let v = f(PI * (k as f64 + 0.5) / n as f64);
                for i in 0..3 {
                    inner[i] += v[i];
                }
            }
            n *= 2;
            let next = value(&inner, n);
            converged = (0..3).map(|i| ((next[i] - cur[i]) / next[i]).abs()).fold(0.0, f64::max);
            cur = next;
        }
        Some(Cycle { advance: cur[0].abs() - 2.0 * PI, period: cur[1], proper_period: cur[2], converged })
    }

    /// The fate of a unit-mass body with constants (E, L), started at its outer turning point (E < 1) or at infinity (E >= 1).
    pub fn fate(&self, e: f64, l: f64) -> Fate {
        let rh = self.horizon();
        let roots = real_roots(self.cubic(e, l));
        if e < 1.0 {
            let bound = roots.len() == 3 && roots[1] > rh && self.forward(e, l, roots[1]) >= 0.0 && self.forward(e, l, roots[0]) >= 0.0;
            if bound {
                Fate::Bound
            } else {
                Fate::Plunge
            }
        } else if roots.first().is_some_and(|&r| r > rh) {
            Fate::Scattered
        } else {
            Fate::Captured
        }
    }
    /// The fate of light with impact parameter b = L/E: from infinity, scattered or captured.
    pub fn photon_fate(&self, b: f64) -> Fate {
        let a = self.a;
        let roots = real_roots([1.0, 0.0, -(b * b - a * a), 2.0 * (b - a) * (b - a)]);
        if roots.first().is_some_and(|&r| r > self.horizon()) {
            Fate::Scattered
        } else {
            Fate::Captured
        }
    }
    /// Light's deflection (the angle swept, |Δφ|, minus π; positive: bent toward the hole) at signed impact parameter b
    /// (negative: counter-rotating) from and to infinity. None if the light is captured. Also the quadrature's convergence.
    pub fn deflection(&self, b: f64) -> Option<(f64, f64)> {
        let a = self.a;
        let roots = real_roots([1.0, 0.0, -(b * b - a * a), 2.0 * (b - a) * (b - a)]);
        let r0 = *roots.first().filter(|&&r| r > self.horizon())?;
        let u0 = 1.0 / r0;
        let (m, k) = (b * b - a * a, 2.0 * (b - a) * (b - a));
        // Q(u) = 1 − m u² + k u³ = (u0 − u)·q(u), q(u) = (m u0 − k u0²) + (m − k u0) u − k u².
        let integrand = |t: f64| -> f64 {
            let u = u0 * (1.0 - t * t);
            let q = (m * u0 - k * u0 * u0) + (m - k * u0) * u - k * u * u;
            let fphi = (b - a) + a * (1.0 + a * (a - b) * u * u) / (1.0 - 2.0 * u + a * a * u * u);
            fphi * 2.0 * u0.sqrt() / q.sqrt()
        };
        let nodes = gauss_legendre(32);
        let run = |pieces: usize| -> f64 {
            let mut total = 0.0;
            for j in 0..pieces {
                let (lo, hi) = (j as f64 / pieces as f64, (j + 1) as f64 / pieces as f64);
                for &(x, w) in &nodes {
                    total += w * 0.5 * (hi - lo) * integrand(0.5 * (lo + hi) + 0.5 * (hi - lo) * x);
                }
            }
            2.0 * total
        };
        let (mut pieces, mut v) = (8usize, run(8));
        let mut converged;
        loop {
            pieces *= 2;
            let w = run(pieces);
            converged = ((w - v) / w).abs();
            v = w;
            if converged < 1e-14 || pieces >= 1 << 12 {
                break;
            }
        }
        Some((v.abs() - PI, converged))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::behave::oracle;

    const SPINS: [f64; 3] = [0.5, 0.9, 0.998];
    fn close(a: f64, b: f64, tol: f64) -> bool {
        ((a - b) / b).abs() <= tol
    }

    #[test]
    fn the_isco_the_photon_orbit_and_the_marginally_bound_orbit_are_the_textbook_ones() {
        // Schwarzschild: 6, 3, 4 (with L = 4 at r = 4).
        let s = Kerr::new(0.0);
        assert!(close(s.isco(1.0), 6.0, 1e-14) && close(s.isco(-1.0), 6.0, 1e-14));
        assert!(close(s.photon_orbit(1.0), 3.0, 1e-14) && close(s.photon_orbit(-1.0), 3.0, 1e-14));
        assert!(close(s.photon_b(1.0), 3.0 * 3f64.sqrt(), 1e-14) && close(s.photon_b(-1.0), -3.0 * 3f64.sqrt(), 1e-14));
        assert_eq!(s.marginally_bound(1.0), (4.0, 4.0));
        // Published ISCO radii (BPT 1972, Table; the values every textbook prints): a = 0.5, 0.9, 0.998.
        for (a, pro, retro) in [(0.5, 4.233, 7.555), (0.9, 2.321, 8.717), (0.998, 1.237, 8.994)] {
            let k = Kerr::new(a);
            assert!((k.isco(1.0) - pro).abs() < 1e-3 && (k.isco(-1.0) - retro).abs() < 1e-3, "a = {a}: {} {}", k.isco(1.0), k.isco(-1.0));
        }
        // a → 1: prograde ISCO, photon orbit and marginally bound orbit all tend to the horizon (r = 1); retrograde to 9, 4, 5.828.
        let k = Kerr::new(1.0 - 1e-12);
        assert!((k.isco(1.0) - 1.0).abs() < 1e-3 && (k.photon_orbit(1.0) - 1.0).abs() < 1e-3 && (k.marginally_bound(1.0).0 - 1.0).abs() < 1e-3);
        assert!(close(k.isco(-1.0), 9.0, 1e-9) && close(k.photon_orbit(-1.0), 4.0, 1e-9) && close(k.marginally_bound(-1.0).0, 3.0 + 2.0 * 2f64.sqrt(), 1e-9));
        // The extremal critical impact parameters of light are 2 (prograde) and −7 (retrograde).
        assert!((k.photon_b(1.0) - 2.0).abs() < 1e-3 && close(k.photon_b(-1.0), -7.0, 1e-9));
    }

    #[test]
    fn circular_orbits_solve_the_radial_potential_and_the_isco_is_where_their_stability_ends() {
        for a in SPINS {
            let k = Kerr::new(a);
            for s in [1.0, -1.0] {
                let (risco, rph) = (k.isco(s), k.photon_orbit(s));
                for r in [rph * 1.02, 0.5 * (rph + risco), risco, 1.5 * risco, 3.0 * risco, 40.0 * risco] {
                    let (e, l) = k.circular(r, s).unwrap();
                    // R(r) = 0 = R'(r), and R''(r) < 0 (stable) iff r >= the ISCO.
                    let h = 1e-4 * r;
                    let scale = k.radial_scale(e, l, r);
                    assert!(k.radial(e, l, r).abs() < 1e-12 * scale, "a = {a} s = {s} r = {r}");
                    assert!(((k.radial(e, l, r + h) - k.radial(e, l, r - h)) / (2.0 * h)).abs() < 1e-7 * scale / r, "a = {a} s = {s} r = {r}");
                    let r2 = (k.radial(e, l, r + h) - 2.0 * k.radial(e, l, r) + k.radial(e, l, r - h)) / (h * h);
                    if (r - risco).abs() > 1e-6 * risco {
                        assert_eq!(r2 < 0.0, r > risco, "a = {a} s = {s} r = {r} R'' = {r2}");
                    }
                    assert_eq!(l.signum(), s);
                }
                assert!(k.circular(rph, s).is_none() && k.circular(0.5 * (rph + k.horizon()), s).is_none());
            }
        }
    }

    #[test]
    fn bound_constants_put_the_turning_points_where_the_label_says() {
        for a in SPINS {
            let k = Kerr::new(a);
            for s in [1.0, -1.0] {
                for e in [0.1, 0.3, 0.6] {
                    let p = 1.2 * k.separatrix(e, s);
                    let (en, l) = k.bound_constants(p, e, s).unwrap();
                    for r in [p / (1.0 + e), p / (1.0 - e)] {
                        assert!(k.radial(en, l, r).abs() < 1e-11 * k.radial_scale(en, l, r), "a = {a} s = {s} e = {e}");
                    }
                    // Its third root lies inside the periapsis, and the fate is bound.
                    assert_eq!(k.fate(en, l), Fate::Bound);
                    // The weak field's limit is Newton's: E ≈ 1 − (1 − e²)/(2p), L ≈ s√p.
                }
                let (en, l) = k.bound_constants(1e4, 0.2, s).unwrap();
                assert!(close(1.0 - en, 0.96 / 2e4, 2e-3) && close(l.abs(), 1e2, 3e-3), "{en} {l}");
            }
        }
    }

    #[test]
    fn the_separatrix_at_zero_eccentricity_is_the_isco_and_it_moves_out_with_e() {
        for a in [0.0, 0.5, 0.9, 0.998] {
            let k = Kerr::new(a);
            for s in [1.0, -1.0] {
                assert!(close(k.separatrix(0.0, s), k.isco(s), 1e-9), "a = {a} s = {s}: {} {}", k.separatrix(0.0, s), k.isco(s));
                let mut last = k.isco(s);
                for e in [0.1, 0.3, 0.5, 0.7] {
                    let ps = k.separatrix(e, s);
                    assert!(ps > last && ps / (1.0 + e) > k.horizon(), "a = {a} s = {s} e = {e}");
                    last = ps;
                }
            }
        }
        // Schwarzschild: p_s = 6 + 2e.
        let k = Kerr::new(0.0);
        for e in [0.2, 0.5, 0.7] {
            assert!(close(k.separatrix(e, 1.0), 6.0 + 2.0 * e, 1e-9));
        }
    }

    #[test]
    fn chi_zero_is_the_schwarzschild_oracle() {
        let k = Kerr::new(0.0);
        for (p, e) in crate::behave::sample::bound_orbits(32) {
            for s in [1.0, -1.0] {
                let c = k.cycle(p, e, s).unwrap();
                let (t, tau) = oracle::radial_periods(p, e);
                assert!(close(c.advance, oracle::periapsis_advance(p, e), 1e-9), "p = {p} e = {e}: {} {}", c.advance, oracle::periapsis_advance(p, e));
                assert!(close(c.period, t, 1e-11) && close(c.proper_period, tau, 1e-11), "p = {p} e = {e}");
                let (en, l) = oracle::bound_invariants(p, e);
                let (e2, l2) = k.bound_constants(p, e, s).unwrap();
                assert!(en == e2 && l * s == l2);
            }
        }
        for b in [6.0, 10.0, 30.0, 300.0, 1000.0] {
            for s in [1.0, -1.0] {
                let (d, _) = k.deflection(s * b).unwrap();
                assert!(close(d, oracle::deflection(b), 1e-9), "b = {b}: {d} {}", oracle::deflection(b));
            }
        }
        assert_eq!(k.fate(1.0, 3.99), Fate::Captured);
        assert_eq!(k.fate(1.0, 4.01), Fate::Scattered);
        assert_eq!(k.photon_fate(5.19), Fate::Captured);
        assert_eq!(k.photon_fate(5.2), Fate::Scattered);
        assert!(close(k.zamo_rate(10.0).unwrap(), oracle::static_clock_rate(10.0), 1e-15));
        assert!(close(k.static_rate(10.0).unwrap(), oracle::static_clock_rate(10.0), 1e-15));
    }

    #[test]
    fn a_small_spin_is_continuous_with_zero() {
        // The closed form's cancellation is worst here; the Newton polish must hold it.
        let (z, k) = (Kerr::new(0.0), Kerr::new(1e-5));
        for (p, e) in [(20.0, 0.3), (100.0, 0.6)] {
            let (a, b) = (z.cycle(p, e, 1.0).unwrap(), k.cycle(p, e, 1.0).unwrap());
            // First order in a: the Lense-Thirring term ~ a/p^1.5 of the advance, here far below 1e-3 of it.
            assert!(close(b.advance, a.advance, 1e-3) && close(b.period, a.period, 1e-5), "{} {}", a.advance, b.advance);
        }
    }

    #[test]
    fn prograde_orbits_precess_less_and_retrograde_more_than_schwarzschild() {
        // Weak field: advance 6π/p·(1 ∓ ...) — spin lowers it for prograde (frame dragging carries the orbit round)
        // and raises it for retrograde.
        for a in SPINS {
            let k = Kerr::new(a);
            for (p, e) in [(30.0, 0.2), (100.0, 0.5)] {
                let (sch, pro, retro) = (oracle::periapsis_advance(p, e), k.cycle(p, e, 1.0).unwrap().advance, k.cycle(p, e, -1.0).unwrap().advance);
                assert!(pro < sch && sch < retro, "a = {a} p = {p}: {pro} {sch} {retro}");
            }
        }
    }

    #[test]
    fn the_cycle_integrals_converge_and_the_clocks_agree_with_the_geometry() {
        let k = Kerr::new(0.9);
        let c = k.cycle(10.0, 0.3, 1.0).unwrap();
        assert!(c.converged < 1e-14);
        // A circular orbit's proper time per radial cycle is 2π/κ_τ: the limit e → 0 is smooth.
        let c0 = k.cycle(20.0, 1e-5, 1.0).unwrap();
        let c1 = k.cycle(20.0, 2e-5, 1.0).unwrap();
        assert!(close(c0.period, c1.period, 1e-8) && close(c0.advance, c1.advance, 1e-6), "{c0:?} {c1:?}");
        // The static clock is √(1 − 2/r) whatever the spin, and the ZAMO's lapse tends to it far out and to 0 at the horizon.
        assert!(close(k.static_rate(7.0).unwrap(), (1.0 - 2.0 / 7.0f64).sqrt(), 1e-15));
        assert!(k.static_rate(2.0).is_none() && k.static_rate(1.5).is_none());
        assert!(close(k.zamo_rate(1e6).unwrap(), 1.0, 1e-5) && k.zamo_rate(k.horizon() + 1e-9).unwrap() < 1e-3 && k.zamo_rate(k.horizon()).is_none());
        // A zero-angular-momentum tube (L = 0, moving radially at 0.1 in the ZAMO frame): dφ/dt is ω and dτ/dt is α/γ.
        let r = 3.0;
        let (alpha, omega, _) = k.zamo(r);
        let (e, l) = k.state_constants(r, 0.1, 0.0);
        let (rate, clock) = k.tube_rates(e, l, r).unwrap();
        assert!(l == 0.0 && close(rate, omega, 1e-12) && close(clock, alpha * (1.0f64 - 0.01).sqrt(), 1e-12));
    }

    #[test]
    fn photons_the_critical_impact_parameters_two_ways_and_the_weak_field() {
        for a in SPINS {
            let k = Kerr::new(a);
            let (bp, bm) = (k.photon_b(1.0), k.photon_b(-1.0));
            assert!(bp > 0.0 && bm < 0.0 && bp < 3.0 * 3f64.sqrt() && -bm > 3.0 * 3f64.sqrt());
            // The root analysis (a different method) classifies on the two sides of each.
            for (b, captured) in [(bp * 0.999, true), (bp * 1.001, false), (bm * 0.999, true), (bm * 1.001, false)] {
                assert_eq!(k.photon_fate(b) == Fate::Captured, captured, "a = {a} b = {b}");
                assert_eq!(k.deflection(b).is_none(), captured);
            }
            // b → ∞: 4/b, with the spin's −4a/b² (sign by sense) the next term.
            for s in [1.0, -1.0] {
                let b = 2000.0;
                let (d, _) = k.deflection(s * b).unwrap();
                assert!(close(d, 4.0 / b + 15.0 * PI / (4.0 * b * b) - s * 4.0 * a / (b * b), 1e-4), "a = {a} s = {s}: {d}");
            }
            // Counter-rotating light is bent more than co-rotating light at the same |b|.
            assert!(k.deflection(-10.0).unwrap().0 > k.deflection(10.0).unwrap().0);
        }
    }

    #[test]
    fn capture_and_plunge_are_classified_by_the_roots_of_the_potential() {
        for a in SPINS {
            let k = Kerr::new(a);
            for s in [1.0, -1.0] {
                // E = 1 from infinity: captured iff L is between the retrograde and the prograde marginally bound L.
                let lmb = k.marginally_bound(s).1;
                assert_eq!(k.fate(1.0, 0.97 * lmb), Fate::Captured, "a = {a} s = {s}");
                assert_eq!(k.fate(1.0, 1.03 * lmb), Fate::Scattered, "a = {a} s = {s}");
                // L below the ISCO's: every E < 1 plunges. At the separatrix, E above it plunges and below it is bound.
                let (el, ll) = k.circular(k.isco(s), s).unwrap();
                assert_eq!(k.fate(0.5 * (1.0 + el), 0.9 * ll), Fate::Plunge);
                for e in [0.2, 0.4, 0.6] {
                    let (es, ls, w) = k.separatrix_window(e, s).unwrap();
                    assert!(w > 0.0 && w < 0.5 * (1.0 - es), "a = {a} s = {s} e = {e}: window {w}");
                    assert_eq!(k.fate(es - 0.25 * w, ls), Fate::Bound, "a = {a} s = {s} e = {e}");
                    assert_eq!(k.fate(es + 0.25 * w, ls), Fate::Plunge, "a = {a} s = {s} e = {e}");
                    // The window is real: well below it nothing is bound at this L either.
                    assert_eq!(k.fate(es - 2.0 * w, ls), Fate::Plunge, "a = {a} s = {s} e = {e}");
                }
            }
        }
    }

    #[test]
    fn real_roots_are_the_roots() {
        // (r − 1)(r − 2)(r − 5) and a quadratic and a lone real root.
        let r = real_roots([1.0, -8.0, 17.0, -10.0]);
        assert!(r.len() == 3 && (r[0] - 5.0).abs() < 1e-12 && (r[1] - 2.0).abs() < 1e-12 && (r[2] - 1.0).abs() < 1e-12, "{r:?}");
        let q = real_roots([0.0, 2.0, -6.0, 4.0]);
        assert!(q.len() == 2 && (q[0] - 2.0).abs() < 1e-12 && (q[1] - 1.0).abs() < 1e-12, "{q:?}");
        let one = real_roots([1.0, 0.0, 1.0, -2.0]);
        assert!(one.len() == 1 && (one[0] - 1.0).abs() < 1e-12);
    }

    #[test]
    fn the_ergosphere_negative_energy_and_the_penrose_split() {
        for a in SPINS {
            let k = Kerr::new(a);
            let rh = k.horizon();
            // Inside the ergosphere a fast counter-rotating state has E < 0 and its tube is allowed; at the same (E, L) outside it is not.
            let r = 0.5 * (rh + ERGOSPHERE);
            let (e, l) = k.state_constants(r, 0.0, -0.9995);
            assert!(e < 0.0 && l < 0.0, "a = {a}: E = {e}");
            let (rate, _) = k.tube_rates(e, l, r).unwrap();
            assert!(rate > 0.0, "frame dragging: dφ/dt = {rate} must be positive although L < 0");
            assert!(k.tube_rates(e, l, 2.5).is_none() && k.tube_rates(e, l, 6.0).is_none());
            // Outside the ergosphere no state has E <= 0.
            for v in [-0.9999, -0.9, 0.0, 0.9] {
                assert!(k.state_constants(2.05, 0.0, v).0 > 0.0, "a = {a} v = {v}");
            }
            // The split at a turning point conserves E and L, and gains energy inside the ergosphere only.
            let (e0, l0) = k.state_constants(r, 0.0, 0.6);
            let [(ef, lf), (eb, lb)] = k.split(e0, l0, r).unwrap();
            assert!((ef + eb - e0).abs() < 1e-14 * e0.abs().max(1.0) && (lf + lb - l0).abs() < 1e-14 * l0.abs().max(1.0));
            assert!(eb < 0.0 && ef > e0, "a = {a}: E_back = {eb}, E_forward = {ef}, E_in = {e0}");
            let (e1, l1) = k.state_constants(3.0, 0.0, 0.6);
            let [(ef, _), (eb, _)] = k.split(e1, l1, 3.0).unwrap();
            assert!(eb > 0.0 && ef < e1);
            // A state that is not at a turning point is not a split.
            let (e2, l2) = k.state_constants(r, 0.3, 0.6);
            assert!(k.split(e2, l2, r).is_none());
        }
    }

    #[test]
    fn no_future_directed_orbit_is_bound_with_negative_energy() {
        // The finding behind B19's "negative-energy tubes": scan (E, L) with E < 0 for three real roots of the potential and a
        // periapsis outside the horizon (R >= 0 between turning points). Such pockets exist, but every one is past-directed
        // (P < 0 at an end): the time reverse (E, L → −E, −L) of an ordinary bound orbit. Future-directed negative-energy
        // geodesics do exist inside the ergosphere (the Penrose process's fragments); none is bound: they plunge.
        // (E < 0 with L > 0 has P < 0 everywhere.)
        for a in [0.5, 0.9, 0.998] {
            let k = Kerr::new(a);
            let mut bound_type = 0;
            for ie in 1..=150 {
                for il in 1..=600 {
                    let (e, l) = (-0.9 * ie as f64 / 150.0, -20.0 * il as f64 / 600.0);
                    let roots = real_roots(k.cubic(e, l));
                    if roots.len() == 3 && roots[1] > k.horizon() {
                        bound_type += 1;
                        assert_ne!(k.fate(e, l), Fate::Bound, "a = {a} E = {e} L = {l}");
                        assert!(k.forward(e, l, roots[0]) < 0.0 || k.forward(e, l, roots[1]) < 0.0);
                    }
                }
            }
            assert!(bound_type > 0 || a == 0.5, "a = {a}: the scan found nothing to refute");
        }
    }

    #[test]
    fn future_directed_is_p_nonnegative_on_allowed_states() {
        // dt/dτ has the sign of E − ωL; the oracle reads P ≥ 0. On states with R >= 0 outside the horizon they agree (any E, either L).
        let mut rng = crate::behave::sample::Rng(11);
        for a in [0.5, 0.9, 0.998] {
            let k = Kerr::new(a);
            let (mut allowed, mut negative) = (0, 0);
            for _ in 0..200_000 {
                let r = k.horizon() + (rng.log_uniform(1e-3, 30.0));
                let e = (rng.unit() - 0.3) * 8.0 * rng.unit();
                let l = (rng.unit() - 0.5) * 30.0 * rng.unit();
                let (_, omega, _) = k.zamo(r);
                let (p, ut) = (k.forward(e, l, r), e - omega * l);
                if k.radial(e, l, r) < 0.0 || p.abs() < 1e-9 || ut.abs() < 1e-9 {
                    continue;
                }
                allowed += 1;
                negative += (e < 0.0 && ut > 0.0) as usize;
                assert_eq!(p > 0.0, ut > 0.0, "a = {a} E = {e} L = {l} r = {r}: P = {p}, E - wL = {ut}");
            }
            assert!(allowed > 5_000 && negative > 0, "a = {a}: {allowed} allowed states, {negative} future-directed with E < 0");
        }
    }

    #[test]
    fn chi_values_of_b19_agree_with_mpmath() {
        let rows = agreement();
        assert!(rows.iter().all(|r| r.worst < 1e-11), "{}", rows.iter().map(|r| format!("{} {:.1e}", r.name, r.worst)).collect::<Vec<_>>().join("; "));
    }
}

/// One row of the oracle's agreement with mpmath: a family of quantities, and the worst relative difference.
pub struct Agreement {
    pub name: String,
    pub count: usize,
    pub worst: f64,
}

/// The oracle's quantities against `kerr_mp.json` (made by `kerr_mpmath.py` at 40 digits). One row per spin and family.
pub fn agreement() -> Vec<Agreement> {
    let table: serde_json::Value = serde_json::from_str(include_str!("kerr_mp.json")).expect("kerr_mp.json parses");
    let mut rows: Vec<Agreement> = Vec::new();
    for case in table["cases"].as_array().expect("cases") {
        let chi: f64 = case["chi"].as_str().unwrap().parse().unwrap();
        let kind = case["kind"].as_str().unwrap();
        let args: Vec<f64> = case["args"].as_array().unwrap().iter().map(|v| v.as_f64().unwrap()).collect();
        let truth: f64 = case["value"].as_str().unwrap().parse().unwrap();
        let k = Kerr::new(chi);
        let got = match kind {
            "horizon" => k.horizon(),
            "isco" => k.isco(args[0]),
            "photon_orbit" => k.photon_orbit(args[0]),
            "photon_b" => k.photon_b(args[0]),
            "mb_radius" => k.marginally_bound(args[0]).0,
            "mb_angular" => k.marginally_bound(args[0]).1,
            "circular_energy" => k.circular(args[0], args[1]).map_or(f64::NAN, |c| c.0),
            "circular_angular" => k.circular(args[0], args[1]).map_or(f64::NAN, |c| c.1),
            "separatrix" => k.separatrix(args[0], args[1]),
            "bound_energy" => k.bound_constants(args[0], args[1], args[2]).map_or(f64::NAN, |c| c.0),
            "bound_angular" => k.bound_constants(args[0], args[1], args[2]).map_or(f64::NAN, |c| c.1),
            "advance" => k.cycle(args[0], args[1], args[2]).map_or(f64::NAN, |c| c.advance),
            "period" => k.cycle(args[0], args[1], args[2]).map_or(f64::NAN, |c| c.period),
            "proper_period" => k.cycle(args[0], args[1], args[2]).map_or(f64::NAN, |c| c.proper_period),
            "deflection" => k.deflection(args[0]).map_or(f64::NAN, |d| d.0),
            "zamo_lapse" => k.zamo(args[0]).0,
            "zamo_omega" => k.zamo(args[0]).1,
            "tube_phi_rate" => k.tube_rates(args[0], args[1], args[2]).map_or(f64::NAN, |t| t.0),
            "tube_clock_rate" => k.tube_rates(args[0], args[1], args[2]).map_or(f64::NAN, |t| t.1),
            "split_forward_energy" => k.split(args[0], args[1], args[2]).map_or(f64::NAN, |s| s[0].0),
            "split_backward_energy" => k.split(args[0], args[1], args[2]).map_or(f64::NAN, |s| s[1].0),
            other => panic!("unknown kind {other}"),
        };
        let err = if got.is_nan() { f64::NAN } else { ((got - truth) / truth).abs() };
        let name = format!("chi={chi} {kind}");
        match rows.iter_mut().find(|r| r.name == name) {
            Some(r) => {
                r.count += 1;
                r.worst = if r.worst.is_nan() || err.is_nan() { f64::NAN } else { r.worst.max(err) };
            }
            None => rows.push(Agreement { name, count: 1, worst: err }),
        }
    }
    rows
}

/// Prints the oracle's agreement with mpmath, one row per spin and family, then the worst; the exit code is 0 iff the worst is below 1e-11.
/// `cargo run --release -p xtask -- kerr-oracle`
pub fn print_agreement() -> u8 {
    let rows = agreement();
    println!("B19's oracle (xtask/src/behave/kerr.rs, float64) against mpmath at 40 digits (kerr_mpmath.py): relative difference");
    for chi in ["0.5", "0.9", "0.998"] {
        let mine: Vec<&Agreement> = rows.iter().filter(|r| r.name.starts_with(&format!("chi={chi} "))).collect();
        let (n, w) = (mine.iter().map(|r| r.count).sum::<usize>(), mine.iter().map(|r| r.worst).fold(0.0f64, f64::max));
        println!("chi = {chi}: {n} values, worst {w:.2e}");
        for r in mine {
            println!("    {:<28} {:>3} values  worst {:.2e}", r.name.trim_start_matches(&format!("chi={chi} ")), r.count, r.worst);
        }
    }
    let worst = rows.iter().map(|r| r.worst).fold(0.0f64, |m, x| if m.is_nan() || x.is_nan() { f64::NAN } else { m.max(x) });
    println!("worst over all {} values: {worst:.2e} (limit 1e-11): {}", rows.iter().map(|r| r.count).sum::<usize>(), if worst < 1e-11 { "ORACLE AGREES" } else { "ORACLE DISAGREES" });
    (worst < 1e-11) as u8 ^ 1
}
