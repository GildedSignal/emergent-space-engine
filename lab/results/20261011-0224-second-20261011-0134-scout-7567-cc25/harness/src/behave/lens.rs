//! B16 moving lenses (docs/law.md; the law's red-team, 1 October). A lens that moves bends light
//! differently for an observer who does not move with it: a lens coming straight at the light
//! deflects it √((1+β)/(1−β)) times as much as a static memo says, and a lens crossing the beam γ
//! times as much. The law's prescription is composition: bend in the lens's frame, then aberrate
//! the light's direction into the observer's. This gate does not check the composition against
//! itself. Its oracle is independent of it: it integrates the null geodesic itself.
//!
//! - Seeds (`sample::moving_lenses`, 256): a lens of mass 1 moves along +x at β up to 0.9; the light
//!   travels, in the observer's frame, at angle θ from +x (head-on θ = π, transverse θ = π/2, and
//!   oblique); b is the signed impact parameter in the lens's frame (b > 0: the lens is on the
//!   light's left), |b| in [10, 1000]. The law returns the observed deflection: the signed angle,
//!   counter-clockwise, from the light's incoming to its outgoing direction in the observer's frame.
//! - The oracle: float64 null geodesics in the Kerr-Schild form of the Schwarzschild metric,
//!   g = η + (2M/r)·l⊗l with l = (1, x/r) null. That form is Lorentz-covariant (l is a null vector
//!   and r the distance in the lens's frame), so the boosted metric is exact: the observer's metric
//!   is the same formula with r and l read off the boosted coordinates. The geodesic is integrated in
//!   the observer's coordinates (t, x, y), where the lens moves and the metric depends on t, by
//!   Hamilton's equations for H = ½g^(μν)p_μp_ν, Dormand-Prince 5(4) with adaptive steps, from a
//!   distance R in the lens's frame to the same distance after the encounter. The deflection is
//!   the change of the direction dx^i/dt between the two ends.
//! - Converged: each seed is integrated twice (tolerances 1e-11 and 1e-12, R and 2R). The seed
//!   is judged iff the two agree to 1e-6 relative. More than 10% of the seeds not converged fails.
//! - PASS iff at least 99% of the judged seeds have the law's answer within 1% of the oracle's.
//!   A NaN and an unanswered seed fail it.
use super::{oracle, sample, Gate, Law};
use std::f64::consts::{PI, TAU};
use std::sync::OnceLock;

pub const SEEDS: usize = 256;
pub const TOL: f64 = 1e-2;
/// The oracle's two runs must agree to this, relative.
pub const CONVERGED: f64 = 1e-6;
pub const EXCLUDED_MAX: f64 = 0.1;
/// The distance, in the lens's frame, from which light is followed, in units of max(|b|, 10).
pub const START: f64 = 1e6;
const MAX_STEPS: usize = 2_000_000;

/// One encounter, in the observer's frame. Units G = c = M = 1 (the lens has mass 1).
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct MovingLens {
    /// The lens's speed, along +x; 0 < β ≤ 0.9.
    pub beta: f64,
    /// The direction the light travels in the observer's frame, radians counter-clockwise from +x:
    /// π is head-on (the lens comes straight at the light), π/2 transverse.
    pub theta: f64,
    /// The impact parameter in the lens's own frame, signed: b > 0 means the lens is on the light's left.
    pub b: f64,
}

/// Wraps an angle to (−π, π].
pub fn wrap(x: f64) -> f64 {
    let y = x % TAU;
    if y > PI {
        y - TAU
    } else if y <= -PI {
        y + TAU
    } else {
        y
    }
}

/// Aberration: the direction (angle from +x) in a frame that moves at speed `v` along +x, of light
/// that travels at `angle` in the frame it is seen from. tan θ' = sin θ / (γ(cos θ − v)).
pub fn aberrate(angle: f64, v: f64) -> f64 {
    let gamma = 1.0 / (1.0 - v * v).sqrt();
    angle.sin().atan2(gamma * (angle.cos() - v))
}

/// The law's prescription, as a function of its static bending: into the lens's frame (the lens
/// moves at `sign`·β), bend by `bend(|b|)` toward the lens (counter-clockwise for b > 0), and back.
/// `sign` is +1 for the right answer; −1 is the planted sign flip.
pub fn compose(lens: &MovingLens, bend: impl Fn(f64) -> f64, sign: f64) -> f64 {
    let v = sign * lens.beta;
    let in_lens = aberrate(lens.theta, v);
    let out_lens = in_lens + lens.b.signum() * bend(lens.b.abs());
    wrap(aberrate(out_lens, -v) - lens.theta)
}

/// What `echo` answers: the composition with the exact static deflection.
pub fn composed(lens: &MovingLens) -> f64 {
    compose(lens, oracle::deflection, 1.0)
}

/// The planted static memo: the lens's own deflection at its own impact parameter, with no aberration.
pub fn static_memo(lens: &MovingLens) -> f64 {
    lens.b.signum() * oracle::deflection(lens.b.abs())
}

// ----- The oracle: null geodesics in the boosted Kerr-Schild Schwarzschild metric -----

/// The state: t, x, y and the covariant momenta p_t, p_x, p_y, in the observer's frame.
type State = [f64; 6];

/// The lens moving along +x at speed β, passing the origin at t = 0, mass 1.
struct Boosted {
    beta: f64,
    gamma: f64,
}

/// Everything the equations need at one point: r' and n' = x'/r' in the lens's frame, l^μ in the
/// observer's.
struct Here {
    r: f64,
    n: [f64; 2],
    l: [f64; 3],
}

impl Boosted {
    fn new(beta: f64) -> Self {
        Boosted { beta, gamma: 1.0 / (1.0 - beta * beta).sqrt() }
    }

    fn here(&self, y: &State) -> Here {
        let (xp, yp) = (self.gamma * (y[1] - self.beta * y[0]), y[2]);
        let r = xp.hypot(yp);
        let n = [xp / r, yp / r];
        // l'^μ = (1, n') in the lens's frame; in the observer's frame (the lens moves at +β):
        let l = [self.gamma * (1.0 + self.beta * n[0]), self.gamma * (n[0] + self.beta), n[1]];
        Here { r, n, l }
    }

    /// dy/dλ by Hamilton's equations for H = ½η^(μν)p_μp_ν − (1/r')·F², F = l^μ p_μ.
    fn deriv(&self, y: &State) -> State {
        let h = self.here(y);
        let (pt, px, py) = (y[3], y[4], y[5]);
        let f = h.l[0] * pt + h.l[1] * px + h.l[2] * py;
        let (g, b) = (self.gamma, self.beta);
        // dx^μ/dλ = η^(μν)p_ν − (2/r')·F·l^μ
        let k = 2.0 * f / h.r;
        let dt = -pt - k * h.l[0];
        let dx = px - k * h.l[1];
        let dy = py - k * h.l[2];
        // ∂_μ x' (x' = γ(x − βt), y' = y) and ∂_μ r' = n'·∂_μ x', ∂_μ n'_i = (∂_μ x'_i − n'_i ∂_μ r')/r'.
        let dxp = [-g * b, g, 0.0];
        let dyp = [0.0, 0.0, 1.0];
        let mut dp = [0.0; 3];
        for mu in 0..3 {
            let dr = h.n[0] * dxp[mu] + h.n[1] * dyp[mu];
            let dn = [(dxp[mu] - h.n[0] * dr) / h.r, (dyp[mu] - h.n[1] * dr) / h.r];
            // ∂_μ F = p_t·γβ·∂_μ n'_x + p_x·γ·∂_μ n'_x + p_y·∂_μ n'_y
            let df = (pt * g * b + px * g) * dn[0] + py * dn[1];
            // dp_μ/dλ = −∂_μ H = ∂_μ(F²/r') = 2F ∂_μF / r' − F² ∂_μ r' / r'²
            dp[mu] = 2.0 * f * df / h.r - f * f * dr / (h.r * h.r);
        }
        [dt, dx, dy, dp[0], dp[1], dp[2]]
    }

    /// The Hamiltonian, which is 0 on a null geodesic.
    #[cfg(test)]
    fn hamiltonian(&self, y: &State) -> f64 {
        let h = self.here(y);
        let f = h.l[0] * y[3] + h.l[1] * y[4] + h.l[2] * y[5];
        0.5 * (-y[3] * y[3] + y[4] * y[4] + y[5] * y[5]) - f * f / h.r
    }

    /// The initial state of light that travels at angle θ in the observer's frame and has, in the
    /// lens's frame, impact parameter b, `start` before its closest approach. Its covariant momentum is built in the
    /// lens's frame from what the geodesic conserves there: the energy E = 1 and the angular
    /// momentum L = b·E (so the impact parameter is exactly b, whatever the distance it is started
    /// at), and the radial momentum solving H = 0 (the incoming root). It is then carried into the
    /// observer's frame, p_μ = ∂x'^ν/∂x^μ · p'_ν, with the event.
    fn start(&self, lens: &MovingLens, start: f64) -> Option<State> {
        // The light's direction in the lens's frame, from the Lorentz transform of its null vector
        // k = (1, cos θ, sin θ) (the formula the law composes with is not used here).
        let (g, beta) = (self.gamma, self.beta);
        let k = [1.0, lens.theta.cos(), lens.theta.sin()];
        let k_lens = [g * (k[0] - beta * k[1]), g * (k[1] - beta * k[0]), k[2]];
        let n = [k_lens[1] / k_lens[0], k_lens[2] / k_lens[0]];
        let right = [n[1], -n[0]];
        let x0 = [lens.b * right[0] - start * n[0], lens.b * right[1] - start * n[1]];
        let r = x0[0].hypot(x0[1]);
        let (nr, e) = ([x0[0] / r, x0[1] / r], 1.0);
        let ephi = [-nr[1], nr[0]];
        let pphi = lens.b * e / r;
        // H = 0: (1 − 2/r)·p_r² + (4E/r)·p_r + (p_φ² − E²(1 + 2/r)) = 0
        let (a, b, c) = (1.0 - 2.0 / r, 4.0 * e / r, pphi * pphi - e * e * (1.0 + 2.0 / r));
        let disc = b * b - 4.0 * a * c;
        if !(disc >= 0.0 && a > 0.0) {
            return None;
        }
        let pr = (-b - disc.sqrt()) / (2.0 * a);
        let p_lens = [-e, pr * nr[0] + pphi * ephi[0], pr * nr[1] + pphi * ephi[1]];
        Some([g * beta * x0[0], g * x0[0], x0[1], g * p_lens[0] - g * beta * p_lens[1], -g * beta * p_lens[0] + g * p_lens[1], p_lens[2]])
    }

    /// The direction angle dx^i/dt in the observer's frame at state y.
    fn direction(&self, y: &State) -> f64 {
        let d = self.deriv(y);
        d[2].atan2(d[1])
    }

    /// Integrates from `start` before the lens to the same distance after it. Returns the observed
    /// direction at the end and the number of steps. None: the integration gave up.
    fn run(&self, lens: &MovingLens, start: f64, rtol: f64) -> Option<(f64, usize)> {
        let mut y = self.start(lens, start)?;
        let mut h = 1e-3 * start;
        let mut steps = 0;
        // Dormand-Prince 5(4)
        const A: [[f64; 6]; 7] = [
            [0.0; 6],
            [0.2, 0.0, 0.0, 0.0, 0.0, 0.0],
            [3.0 / 40.0, 9.0 / 40.0, 0.0, 0.0, 0.0, 0.0],
            [44.0 / 45.0, -56.0 / 15.0, 32.0 / 9.0, 0.0, 0.0, 0.0],
            [19372.0 / 6561.0, -25360.0 / 2187.0, 64448.0 / 6561.0, -212.0 / 729.0, 0.0, 0.0],
            [9017.0 / 3168.0, -355.0 / 33.0, 46732.0 / 5247.0, 49.0 / 176.0, -5103.0 / 18656.0, 0.0],
            [35.0 / 384.0, 0.0, 500.0 / 1113.0, 125.0 / 192.0, -2187.0 / 6784.0, 11.0 / 84.0],
        ];
        const E: [f64; 7] = [71.0 / 57600.0, 0.0, -71.0 / 16695.0, 71.0 / 1920.0, -17253.0 / 339200.0, 22.0 / 525.0, -1.0 / 40.0];
        loop {
            steps += 1;
            if steps > MAX_STEPS || !(h > 0.0) || !h.is_finite() {
                return None;
            }
            let here = self.here(&y);
            // A step never jumps a sizeable part of the way to the lens.
            h = h.min(0.2 * here.r);
            let mut k: [State; 7] = [[0.0; 6]; 7];
            k[0] = self.deriv(&y);
            for s in 1..7 {
                let mut z = y;
                for (j, kj) in k.iter().enumerate().take(s) {
                    for i in 0..6 {
                        z[i] += h * A[s][j] * kj[i];
                    }
                }
                k[s] = self.deriv(&z);
            }
            // the fifth-order state is stage 7's argument
            let mut y5 = y;
            for (j, kj) in k.iter().enumerate().take(6) {
                for i in 0..6 {
                    y5[i] += h * A[6][j] * kj[i];
                }
            }
            let mut err = 0.0f64;
            for i in 0..6 {
                let e: f64 = (0..7).map(|j| E[j] * k[j][i]).sum::<f64>() * h;
                // positions against the distance from the lens, momenta against 1
                let scale = if i < 3 { here.r } else { 1.0 };
                err = err.max(e.abs() / (rtol * scale));
            }
            if !err.is_finite() {
                return None;
            }
            let fac = if err > 0.0 { (0.9 * err.powf(-0.2)).clamp(0.2, 5.0) } else { 5.0 };
            if err <= 1.0 {
                y = y5;
                let there = self.here(&y);
                // the distance from the lens is growing again, and we are as far as we began
                let dr = {
                    let d = self.deriv(&y);
                    let (g, b) = (self.gamma, self.beta);
                    there.n[0] * g * (d[1] - b * d[0]) + there.n[1] * d[2]
                };
                if there.r >= start && dr > 0.0 {
                    return Some((self.direction(&y), steps));
                }
            }
            h *= fac;
        }
    }
}

/// The oracle's observed deflection for one encounter: the change of the direction in the observer's
/// frame, from the incoming asymptote's angle θ. Runs at tolerance `rtol` from `start` times max(|b|, 10).
pub fn geodesic_deflection(lens: &MovingLens, start: f64, rtol: f64) -> Option<f64> {
    let boosted = Boosted::new(lens.beta);
    let (out, _) = boosted.run(lens, start * lens.b.abs().max(10.0), rtol)?;
    Some(wrap(out - lens.theta))
}

/// The oracle's answer for each seed, with whether its two runs agree: computed once per process on up
/// to four threads.
pub fn truths() -> &'static Vec<(Option<f64>, f64)> {
    static TRUTHS: OnceLock<Vec<(Option<f64>, f64)>> = OnceLock::new();
    TRUTHS.get_or_init(|| {
        let seeds = sample::moving_lenses(SEEDS);
        let next = std::sync::atomic::AtomicUsize::new(0);
        let threads = std::thread::available_parallelism().map_or(1, |n| n.get()).min(4);
        let mut done: Vec<(usize, (Option<f64>, f64))> = std::thread::scope(|scope| {
            let workers: Vec<_> = (0..threads)
                .map(|_| {
                    scope.spawn(|| {
                        let mut mine = Vec::new();
                        loop {
                            let i = next.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                            if i >= SEEDS {
                                return mine;
                            }
                            let (beta, theta, b) = seeds[i];
                            let lens = MovingLens { beta, theta, b };
                            let (a, c) = (geodesic_deflection(&lens, START, 1e-11), geodesic_deflection(&lens, 2.0 * START, 1e-12));
                            mine.push((
                                i,
                                match (a, c) {
                                    (Some(a), Some(c)) => {
                                        let rel = (a - c).abs() / c.abs();
                                        ((rel <= CONVERGED).then_some(c), rel)
                                    }
                                    _ => (None, f64::INFINITY),
                                },
                            ));
                        }
                    })
                })
                .collect();
            workers.into_iter().flat_map(|w| w.join().expect("a lens oracle panicked")).collect()
        });
        done.sort_by_key(|d| d.0);
        done.into_iter().map(|d| d.1).collect()
    })
}

pub fn b16(law: &dyn Law) -> Gate {
    let _quiet = super::scale::QUIET.read().unwrap_or_else(|e| e.into_inner());
    let seeds = sample::moving_lenses(SEEDS);
    let truths = truths();
    let unconverged = truths.iter().filter(|t| t.0.is_none()).count();
    let worst_disagree = truths.iter().map(|t| t.1).fold(0.0f64, |m, x| if m.is_nan() || x.is_nan() { f64::NAN } else { m.max(x) });
    let (mut judged, mut ok, mut worst) = (0, 0, 0.0f64);
    let mut by_kind = [(0, 0); sample::LENS_KINDS.len()];
    for (i, (&(beta, theta, b), truth)) in seeds.iter().zip(truths).enumerate() {
        let Some(truth) = truth.0 else { continue };
        judged += 1;
        let err = law.moving_deflection(&MovingLens { beta, theta, b }).map_or(f64::INFINITY, |d| (d - truth).abs() / truth.abs());
        let good = err <= TOL;
        ok += good as usize;
        worst = if worst.is_nan() || err.is_nan() { f64::NAN } else { worst.max(err) };
        let k = sample::lens_kind(i);
        by_kind[k].0 += good as usize;
        by_kind[k].1 += 1;
    }
    let pass = judged > 0 && ok * 100 >= 99 * judged && unconverged as f64 <= EXCLUDED_MAX * SEEDS as f64;
    let detail = format!(
        "moving lenses: {ok}/{judged} judged seeds within {TOL:.0e} of the boosted Kerr-Schild geodesic ({}), worst {worst:.2e}, beta up to {:.2}; oracle converged on {} of {SEEDS} (its two runs agree to {worst_disagree:.1e}, needs {CONVERGED:.0e})",
        sample::LENS_KINDS.iter().zip(&by_kind).map(|(name, (ok, n))| format!("{name} {ok}/{n}")).collect::<Vec<_>>().join(", "),
        seeds.iter().map(|s| s.0).fold(0.0, f64::max),
        SEEDS - unconverged
    );
    Gate { id: "B16", pass, detail, secs: 0.0 }
}

#[cfg(test)]
mod tests {
    use super::super::laws::{Echo, Fault, Planted, Silent};
    use super::*;

    fn lens(beta: f64, theta: f64, b: f64) -> MovingLens {
        MovingLens { beta, theta, b }
    }
    fn oracle_of(l: &MovingLens) -> f64 {
        geodesic_deflection(l, START, 1e-11).unwrap()
    }
    /// A law that answers only the lens, by echo's composition times a factor chosen by the closure.
    struct Skewed(Box<dyn Fn(usize, &MovingLens) -> Option<f64>>, std::cell::Cell<usize>);
    impl Law for Skewed {
        fn advance_per_cycle(&self, p: f64, e: f64) -> Option<(f64, f64, f64)> {
            Echo.advance_per_cycle(p, e)
        }
        fn deflection(&self, b: f64) -> Option<f64> {
            Echo.deflection(b)
        }
        fn captured(&self, energy: f64, angular: f64) -> bool {
            Echo.captured(energy, angular)
        }
        fn photon_captured(&self, b: f64) -> bool {
            Echo.photon_captured(b)
        }
        fn long_run(&self, p: f64, e: f64, cycles: usize) -> Vec<(f64, f64, f64, f64)> {
            Echo.long_run(p, e, cycles)
        }
        fn moving_deflection(&self, l: &MovingLens) -> Option<f64> {
            let i = self.1.get();
            self.1.set(i + 1);
            (self.0)(i, l)
        }
    }
    fn skewed(f: impl Fn(usize, &MovingLens) -> Option<f64> + 'static) -> Skewed {
        Skewed(Box::new(f), std::cell::Cell::new(0))
    }

    #[test]
    fn the_seeds_are_four_kinds_up_to_beta_09_with_lens_frame_impact_parameters_of_both_signs() {
        let s = sample::moving_lenses(SEEDS);
        assert_eq!(s.len(), 256);
        assert_eq!(s[..16], sample::moving_lenses(16)[..]);
        for (i, &(beta, theta, b)) in s.iter().enumerate() {
            assert!((0.05..=0.9).contains(&beta) && (10.0..=1000.0).contains(&b.abs()) && (0.0..=PI).contains(&theta), "seed {i}: {beta} {theta} {b}");
            match i % 4 {
                0 => assert_eq!(theta, PI),
                1 => assert_eq!(theta, PI / 2.0),
                _ => assert!((0.05 * PI..=0.95 * PI).contains(&theta)),
            }
        }
        // One of each kind at the extreme β; both signs of b; the oblique ones come from both sides of the transverse.
        assert!(s[..4].iter().all(|x| x.0 == 0.9) && s[4..].iter().any(|x| x.0 > 0.85));
        let positive = s.iter().filter(|x| x.2 > 0.0).count();
        assert!((100..156).contains(&positive), "{positive} of 256 with b > 0");
        let oblique: Vec<f64> = s.iter().enumerate().filter(|(i, _)| i % 4 >= 2).map(|(_, x)| x.1).collect();
        assert!(oblique.iter().filter(|&&t| t < PI / 2.0).count() > 30 && oblique.iter().filter(|&&t| t > PI / 2.0).count() > 30);
    }

    #[test]
    fn aberration_is_the_special_relativistic_one_and_its_inverse_is_the_opposite_velocity() {
        for theta in [0.1, 1.0, 2.0, 3.0, -2.5] {
            assert!((aberrate(theta, 0.0) - theta).abs() < 1e-15);
            for v in [0.3, 0.9, -0.6] {
                assert!(wrap(aberrate(aberrate(theta, v), -v) - theta).abs() < 1e-12, "{theta} {v}");
            }
        }
        // Light along +x stays along +x and light along −x stays along −x, whatever the frame's speed; light across
        // (θ = π/2) tilts back toward −x as the frame speeds along +x: cos θ' = −v.
        assert_eq!(aberrate(0.0, 0.9), 0.0);
        assert!((aberrate(PI, 0.9).abs() - PI).abs() < 1e-12);
        assert!((aberrate(PI / 2.0, 0.6).cos() + 0.6).abs() < 1e-12);
    }

    #[test]
    fn composition_in_the_weak_field_is_the_doppler_and_gamma_factors_of_the_red_team() {
        // Head-on (the lens comes straight at the light): √((1+β)/(1−β)) times the static 4/b; tail-chase the inverse;
        // transverse γ (second order in β, so a static memo is nearly right at small β and wrong at 0.9).
        let (b, beta) = (1000.0, 0.5);
        let stat = oracle::deflection(b);
        let head = composed(&lens(beta, PI, b));
        assert!((head / stat - ((1.0 + beta) / (1.0 - beta)).sqrt()).abs() < 1e-3, "{}", head / stat);
        let tail = composed(&lens(beta, 0.0, b));
        assert!((tail / stat - ((1.0 - beta) / (1.0 + beta)).sqrt()).abs() < 1e-3, "{}", tail / stat);
        let across = composed(&lens(beta, PI / 2.0, b));
        let gamma = 1.0 / (1.0 - beta * beta).sqrt();
        assert!((across / stat - gamma).abs() < 2e-3, "{} against {gamma}", across / stat);
        // The other side of the lens bends the other way, and a static lens (β = 0) is the static deflection from any direction.
        assert!((composed(&lens(beta, PI, -b)) + head).abs() < 1e-15);
        assert!((composed(&lens(0.0, 1.0, b)) - stat).abs() < 1e-15);
    }

    #[test]
    fn the_oracle_is_the_static_deflection_at_rest_and_not_the_composition_it_judges() {
        // At β = 0 the geodesic integrator is G3's oracle (a quadrature), from any direction, either side.
        for (theta, b) in [(1.0, 100.0), (PI, 10.0), (0.3, -30.0), (2.2, 1000.0)] {
            let got = oracle_of(&lens(0.0, theta, b));
            assert!((got - b.signum() * oracle::deflection(b.abs())).abs() < 1e-6 * got.abs(), "theta {theta} b {b}: {got}");
        }
        // Moving, it agrees with the composition to the 1e-6 of its convergence, including strong-field (b = 10) and β = 0.9.
        for (beta, theta, b) in [(0.9, PI, 100.0), (0.9, PI / 2.0, 100.0), (0.5, 1.0, 30.0), (0.9, 0.0, 10.0), (0.7, 2.5, -10.0), (0.9, 0.3, -1000.0)] {
            let l = lens(beta, theta, b);
            let (got, want) = (oracle_of(&l), composed(&l));
            assert!((got - want).abs() < 1e-6 * want.abs(), "{l:?}: oracle {got}, composition {want}");
        }
    }

    #[test]
    fn the_integration_conserves_the_hamiltonian_and_what_the_lens_frame_conserves() {
        // H = 0 (null), and in the lens's frame the energy E' = −p'_t and the angular momentum L' = b·E' are constants of the geodesic.
        let l = lens(0.9, PI / 2.0, 100.0);
        let bo = Boosted::new(l.beta);
        let mut y = bo.start(&l, 1e4).unwrap();
        let (g, b) = (bo.gamma, bo.beta);
        let inv = |y: &State| (bo.hamiltonian(y), -g * (y[3] + b * y[4]), g * (y[1] - b * y[0]) * y[5] - y[2] * g * (y[4] + b * y[3]));
        let first = inv(&y);
        assert!(first.0.abs() < 1e-12 && (first.2 / first.1 - l.b).abs() < 1e-9, "{first:?}: the start has the impact parameter b exactly");
        for _ in 0..30000 {
            let h = 1.0;
            let (k1, ) = (bo.deriv(&y), );
            let mut z = y;
            for i in 0..6 {
                z[i] += 0.5 * h * k1[i];
            }
            let k2 = bo.deriv(&z);
            let mut z = y;
            for i in 0..6 {
                z[i] += 0.5 * h * k2[i];
            }
            let k3 = bo.deriv(&z);
            let mut z = y;
            for i in 0..6 {
                z[i] += h * k3[i];
            }
            let k4 = bo.deriv(&z);
            for i in 0..6 {
                y[i] += h / 6.0 * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]);
            }
        }
        let last = inv(&y);
        assert!(last.0.abs() < 1e-10 && (last.1 / first.1 - 1.0).abs() < 1e-12 && (last.2 / first.2 - 1.0).abs() < 1e-9, "{first:?} -> {last:?}");
    }

    #[test]
    fn echo_passes_to_the_oracles_convergence_and_the_planted_static_and_flipped_laws_fail() {
        let g = b16(&Echo);
        let worst: f64 = g.detail.split("worst ").nth(1).unwrap().split(',').next().unwrap().parse().unwrap();
        assert!(g.pass && worst < 1e-5 && g.detail.contains("256/256") && g.detail.contains("head-on 64/64"), "{}", g.detail);
        // The static memo: right for nobody who is moving. 7 of 256 transverse seeds are slow enough (γ − 1 < 1%).
        let g = b16(&Planted(Fault::Static));
        assert!(!g.pass && g.detail.contains("head-on 0/64") && g.detail.contains("12/256"), "{}", g.detail);
        // The sign-flipped aberration: right for the transverse seeds whose mirror image is the same encounter.
        let g = b16(&Planted(Fault::Flipped));
        assert!(!g.pass && g.detail.contains("head-on 0/64"), "{}", g.detail);
        // At the head-on extreme the memo is off by √19 = 4.36 (to first order in the bending: 0.04 rad here).
        let l = lens(0.9, PI, 100.0);
        assert!((static_memo(&l) / oracle_of(&l) * 19f64.sqrt() - 1.0).abs() < 1e-2);
    }

    #[test]
    fn the_gate_is_99_percent_of_the_seeds_within_one_percent_and_a_nan_or_a_silence_fails() {
        let off_by = |factor: f64, seeds: &'static [usize]| skewed(move |i, l| Some(composed(l) * if seeds.contains(&i) { factor } else { 1.0 }));
        // 0.9% too big everywhere: within 1%, passes. 1.5% too big everywhere: fails.
        assert!(b16(&skewed(|_, l| Some(composed(l) * 1.009))).pass);
        assert!(!b16(&skewed(|_, l| Some(composed(l) * 1.015))).pass);
        // 2 of 256 (0.8%) twice as big: passes (99%). 3 of 256 (1.2%): fails.
        assert!(b16(&off_by(2.0, &[3, 100])).pass);
        let g = b16(&off_by(2.0, &[3, 100, 200]));
        assert!(!g.pass && g.detail.contains("253/256"), "{}", g.detail);
        // Not implemented, NaN, and silence on one seed in a hundred each.
        assert!(!b16(&Silent).pass);
        assert!(!b16(&skewed(|_, _| Some(f64::NAN))).pass);
        assert!(!b16(&skewed(|i, l| if i % 4 == 0 { None } else { Some(composed(l)) })).pass);
    }
}
