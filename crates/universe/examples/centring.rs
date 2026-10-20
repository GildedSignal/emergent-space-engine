//! The root doll's centring (20 October, the integrator's question): what would a barycentric (Jacobi) centring of a root-doll
//! body buy in kicks per orbit, and what would it cost? Not built in the law: measured here, in two parts.
//!
//! 1. **The census** (the law's own numbers): the ladder's belt (`scenario::ladder_ship`, the same births) and far bodies (5.5 to
//!    40 AU, e = 0.05) built in the plane's root doll; for each body the step the law gives it (`ext::constants`, heliocentric:
//!    its own period, the frame's fall toward every secondary, the passage of the secondaries it can meet) against the step the
//!    same rule gives it when the body is centred on the barycentre of the star and every secondary its orbit encloses (`Q_j <
//!    q`): the frame's fall toward an enclosed secondary is gone (its pull and the centre's motion cancel to a quadrupole,
//!    `ε_j = μ_j·(a_j/q)²` at half its period), the others keep the law's terms. Kicks per own period and per body per
//!    game-second, by population. Two Jacobi variants bracket the rule: the quadrupole under the law's floor of 4 steps a
//!    forcing period, and the quadrupole by its strength alone (`2^k_s·√(ε/ε_s)` a period, no floor).
//! 2. **The replica** (f64, outside the law): the law's map (`D(Δs/2)·Kc(Δs)·D(Δs/2)` in extended phase space, the time transform
//!    `f'(U_P + c)` with the law's `c` and `b`, the energy register) flown on the belt in both centrings with the planets on their
//!    two-body Kepler ellipses from the engine's tick-0 states, against a heliocentric reference at 2^9 steps a Cinder period
//!    (and a second at 2^10: their gap is the reference's own error). Reports |Δa|/a and |Δe| about the star (median and worst)
//!    and the growth exponent of the worst over the last four octaves (0 an offset, 0.5 a walk, 1 a drift), as
//!    `examples/cadence.rs` does for the law itself. The heliocentric arms check the replica against the law (with the law's
//!    steps: an offset; at 16 a period: Cinder's 88 days alias and e walks).
//!
//! cargo run --release -p emergent-universe --example centring -- <census bodies> <replica bodies> <years>
use emergent_space::orbit::Scalar;
use emergent_universe::ext::{PASSAGE_OCTAVES, SMOOTH_EPS_LOG2};
use emergent_universe::num::{s, to_f64};
use emergent_universe::scenario::{ladder_ship, PLANETS, STAR_RADIUS};
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{Config, Kind, OrbitSpec, Universe};
use std::f64::consts::PI;
use std::time::Instant;

const YEAR: f64 = 365.25 * 86_400.0;
const AU: f64 = 101_300_000.0; // root units (Home's axis)

type V = [f64; 2];
fn add(a: V, b: V) -> V {
    [a[0] + b[0], a[1] + b[1]]
}
fn sub(a: V, b: V) -> V {
    [a[0] - b[0], a[1] - b[1]]
}
fn mul(a: V, k: f64) -> V {
    [a[0] * k, a[1] * k]
}
fn dot(a: V, b: V) -> f64 {
    a[0] * b[0] + a[1] * b[1]
}
fn norm(a: V) -> f64 {
    dot(a, a).sqrt()
}

/// The Kepler flow for time `dt` about `mu` (bound orbits): Danby's f and g in the eccentric anomaly's increment.
fn kepler(x: V, v: V, mu: f64, dt: f64) -> (V, V) {
    let r0 = norm(x);
    let a = 1.0 / (2.0 / r0 - dot(v, v) / mu);
    assert!(a > 0.0, "a bound orbit");
    let n = (mu / (a * a * a)).sqrt();
    let (c0, s0) = (1.0 - r0 / a, dot(x, v) / (n * a * a));
    let m = n * dt;
    let mut de = m;
    for _ in 0..50 {
        let (sn, cs) = de.sin_cos();
        let f = de - c0 * sn + s0 * (1.0 - cs) - m;
        let fp = 1.0 - c0 * cs + s0 * sn;
        let step = f / fp;
        de -= step;
        if step.abs() < 1e-15 * (1.0 + de.abs()) {
            break;
        }
    }
    let (sn, cs) = de.sin_cos();
    let r = a * (1.0 - c0 * cs + s0 * sn);
    let f = 1.0 - a / r0 * (1.0 - cs);
    let g = dt - (de - sn) / n;
    let fd = -a * a * n * sn / (r * r0);
    let gd = 1.0 - a / r * (1.0 - cs);
    (add(mul(x, f), mul(v, g)), add(mul(x, fd), mul(v, gd)))
}

/// Osculating (a, e) about the star (G = M = 1, root units).
fn elements(x: V, v: V) -> (f64, f64) {
    let r = norm(x);
    let v2 = dot(v, v);
    let a = 1.0 / (2.0 / r - v2);
    let rv = dot(x, v);
    let e = sub(mul(x, v2 - 1.0 / r), mul(v, rv));
    (a, norm(e))
}

/// A planet on its two-body ellipse (the law's tube: the Kepler problem of the star and the planet, `1 + μ`).
#[derive(Clone, Copy)]
struct Planet {
    mu: f64,
    x0: V,
    v0: V,
    period: f64,
    axis: f64,
    peri: f64,
    apo: f64,
}
impl Planet {
    fn at(&self, t: f64) -> (V, V) {
        kepler(self.x0, self.v0, 1.0 + self.mu, t.rem_euclid(self.period))
    }
}

/// The centre of a body and its derivatives, from the planets it encloses: `R = Σ μ_j r_j / M`, `M = 1 + Σ μ_j`.
struct Centre {
    m: f64,
    set: Vec<usize>,
}
impl Centre {
    /// (R, Ṙ, R̈, R⃛) at `t`.
    fn at(&self, ps: &[Planet], states: &[(V, V)]) -> (V, V, V, V) {
        let (mut r, mut rd, mut rdd, mut rddd) = ([0.0; 2], [0.0; 2], [0.0; 2], [0.0; 2]);
        for &j in &self.set {
            let (p, (x, v)) = (&ps[j], states[j]);
            let k = p.mu / self.m;
            let rr = norm(x);
            let g = 1.0 + p.mu;
            r = add(r, mul(x, k));
            rd = add(rd, mul(v, k));
            rdd = add(rdd, mul(x, -k * g / (rr * rr * rr)));
            // d/dt(−g·x/r³) = −g·(v/r³ − 3·x·(x·v)/r⁵)
            rddd = add(rddd, mul(sub(mul(v, 1.0 / (rr * rr * rr)), mul(x, 3.0 * dot(x, v) / rr.powi(5))), -k * g));
        }
        (r, rd, rdd, rddd)
    }
}

/// The field a body reads at its kick, in its own centring: (U_P, ∇U_P, ∂_tU_P). `x` is the body's state about its centre.
fn field(ps: &[Planet], states: &[(V, V)], c: &Centre, x: V, cen: (V, V, V, V)) -> (f64, V, f64) {
    let (rc, rcd, rcdd, rcddd) = cen;
    let xa = add(x, rc); // heliocentric
    // The heliocentric perturbation (the law's): Σ μ_j/|x − r_j| − a_o·x.
    let (mut u, mut g, mut du, mut fall, mut fall_rate) = (0.0, [0.0; 2], 0.0, [0.0; 2], [0.0; 2]);
    for (p, &(xj, vj)) in ps.iter().zip(states) {
        let d = sub(xj, xa);
        let r = norm(d);
        let pull = mul(d, p.mu / (r * r * r));
        u += p.mu / r;
        g = add(g, pull);
        du -= dot(vj, pull);
        let rj = norm(xj);
        let k = p.mu / (rj * rj * rj);
        fall = add(fall, mul(xj, k));
        let along = 3.0 * dot(xj, vj) / (rj * rj);
        fall_rate = add(fall_rate, mul(sub(vj, mul(xj, along)), k));
    }
    let (u_h, g_h, du_h) = (u - dot(fall, xa), sub(g, fall), du - dot(fall_rate, xa));
    if c.set.is_empty() {
        return (u_h, g_h, du_h);
    }
    // Centred on R: U_P^J = Φ(x + R) − x·R̈ − M/|x|, Φ = 1/|x_h| + U_P^h (Hamiltonian of a translation by a given R(t)).
    let (ra, r) = (norm(xa), norm(x));
    let phi = 1.0 / ra + u_h;
    let grad_phi = add(mul(xa, -1.0 / (ra * ra * ra)), g_h);
    let u_j = phi - dot(x, rcdd) - c.m / r;
    let g_j = add(sub(grad_phi, rcdd), mul(x, c.m / (r * r * r)));
    let du_j = du_h + dot(grad_phi, rcd) - dot(x, rcddd);
    (u_j, g_j, du_j)
}

fn fp(y: f64, b: f64) -> f64 {
    1.0 / (y * y) + 1.0 / (b * y)
}

/// One body flown by the law's map in its centring at fictitious step `ds`; the heliocentric states at `samples`, and the kicks.
/// A sample between two boundaries (the middles of the drifts, where the map's state is synchronised) is a partial step of the
/// same map from the boundary before it (`D(τ/2)·Kc·D(τ/2)`): second order everywhere, as a reader of the law's state is.
fn fly(ps: &[Planet], c: &Centre, x0: V, v0: V, ds: f64, cc: f64, b: f64, samples: &[f64]) -> (Vec<(V, V)>, u64) {
    let states = |t: f64| -> Vec<(V, V)> { ps.iter().map(|p| p.at(t)).collect() };
    let y_of = |u: f64| (u + cc).max(cc / 8.0);
    let hd = |x: V, v: V| dot(v, v) / 2.0 - c.m / norm(x);
    let kick = |x: V, v: V, t: f64, sigma: f64| -> (V, f64) {
        let st = states(t);
        let cen = c.at(ps, &st);
        let (u, g, du) = field(ps, &st, c, x, cen);
        let w = sigma * fp(y_of(u), b);
        (add(v, mul(g, w)), w * du)
    };
    let st0 = states(0.0);
    let cen0 = c.at(ps, &st0);
    // The boundary: its state about the centre, its time, and the y of the drift through it.
    let (mut xb, mut vb, mut tb) = (sub(x0, cen0.0), sub(v0, cen0.1), 0.0);
    let (u0, _, _) = field(ps, &st0, c, xb, cen0);
    let mut pt = u0 - hd(xb, vb); // K = 0
    let mut yb = y_of(hd(xb, vb) + pt);
    let (mut out, mut next, mut kicks) = (Vec::with_capacity(samples.len()), 0usize, 0u64);
    loop {
        let half = 0.5 * ds * fp(yb, b);
        // The kick, then the next boundary.
        let (xk, vk) = kepler(xb, vb, c.m, half);
        let (vk, dpt) = kick(xk, vk, tb + half, ds);
        pt += dpt;
        kicks += 1;
        let y1 = y_of(hd(xk, vk) + pt);
        let half1 = 0.5 * ds * fp(y1, b);
        let t1 = tb + half + half1;
        while next < samples.len() && samples[next] < t1 {
            let tau = samples[next] - tb;
            let (x1, v1) = kepler(xb, vb, c.m, tau / 2.0);
            let (v1, _) = kick(x1, v1, tb + tau / 2.0, tau / fp(yb, b));
            let (xs, vs) = kepler(x1, v1, c.m, tau / 2.0);
            let cen = c.at(ps, &states(samples[next]));
            out.push((add(xs, cen.0), add(vs, cen.1)));
            next += 1;
        }
        if next == samples.len() {
            return (out, kicks);
        }
        let (x2, v2) = kepler(xk, vk, c.m, half1);
        (xb, vb, tb, yb) = (x2, v2, t1, y1);
    }
}

fn pct(v: &mut [f64], p: f64) -> f64 {
    v.sort_by(f64::total_cmp);
    v[((v.len() - 1) as f64 * p).round() as usize]
}

/// Growth exponent of the running maximum of `err` against `t`, least squares over the samples of the last four octaves.
fn exponent(t: &[f64], err: &[f64]) -> f64 {
    let mut m = 0.0f64;
    let run: Vec<f64> = err
        .iter()
        .map(|&e| {
            m = m.max(e);
            m
        })
        .collect();
    let last = *t.last().unwrap();
    let pts: Vec<(f64, f64)> = t.iter().zip(&run).filter(|(&ti, &e)| ti >= last / 16.0 && e > 0.0).map(|(&ti, &e)| (ti.ln(), e.ln())).collect();
    let k = pts.len() as f64;
    let (sx, sy) = (pts.iter().map(|p| p.0).sum::<f64>(), pts.iter().map(|p| p.1).sum::<f64>());
    let (sxx, sxy) = (pts.iter().map(|p| p.0 * p.0).sum::<f64>(), pts.iter().map(|p| p.0 * p.1).sum::<f64>());
    (k * sxy - sx * sy) / (k * sxx - sx * sx)
}

/// A body of the census: its tube's (q, Q, a, P), the law's Δs, and the time transform's constants.
struct Body {
    q: f64,
    big_q: f64,
    period: f64,
    ds: f64,
    c: f64,
    b: f64,
    x0: V,
    v0: V,
}

fn census_body(u: &Universe, i: usize) -> Body {
    let r = u.rec(i);
    let emergent_space::binding::Trajectory::Cycle(cy) = &r.b.entry.trajectory else { panic!("a bound tube") };
    let key = cy.key();
    let k = to_f64(key.shape().unwrap());
    let q = to_f64(r.b.to_doll(key.periapsis).unwrap());
    let ext = r.ext.expect("a ship of the root doll is on the clock");
    let ctx = u.ctx();
    let (x, v) = ctx.state_of(i, 0).unwrap();
    Body {
        q,
        big_q: q / (2.0 * k - 1.0),
        period: to_f64(r.b.to_doll(cy.period().unwrap()).unwrap()),
        ds: to_f64(ext.ds),
        c: to_f64(ext.c),
        b: to_f64(ext.b),
        x0: [to_f64(x[0]), to_f64(x[1])],
        v0: [to_f64(v[0]), to_f64(v[1])],
    }
}

/// The step (physical, far from every secondary) the law's rule gives `b`, in f64, with every secondary its orbit encloses at the
/// centre (`jacobi`; their fall replaced by their quadrupole at half their period, `floor`: under the law's floor of 4 a period).
fn rule_step(cfg: &Config, ps: &[Planet], b: &Body, jacobi: bool, floor: bool) -> f64 {
    let (k_s, k_f, k_p) = (cfg.step_log2 + cfg.smooth_octaves, cfg.step_log2 + cfg.forcing_octaves, cfg.step_log2 + PASSAGE_OCTAVES);
    let reach = 12f64.sqrt();
    let mut t = b.period * 2f64.powi(-k_s);
    for p in ps {
        let hill = p.axis * (p.mu / 3.0).cbrt();
        if (b.q - p.apo).max(p.peri - b.big_q) < reach * hill {
            t = t.min(p.period * 2f64.powi(-k_p));
        }
        let enclosed = jacobi && p.apo < b.q;
        let (eps, period) = if enclosed { (p.mu * (p.axis / b.q).powi(2), p.period / 2.0) } else { (p.mu * (b.big_q / p.axis).powi(2), p.period) };
        let mut n = 2f64.powi(k_s - SMOOTH_EPS_LOG2 / 2) * eps.sqrt();
        if !enclosed || floor {
            n = n.max(2f64.powi(k_f));
        }
        t = t.min(period / n);
    }
    t
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let n_census: usize = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(4_000);
    let n_fly: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(8);
    let years: f64 = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(20.0);
    let cfg = Config::default();
    let t0 = Instant::now();
    let mut u = Universe::new(s(STAR_RADIUS), cfg);
    u.threads = 1;
    let mut planets = Vec::new();
    for p in &PLANETS {
        let b = u
            .add_body(Kind::Planet, OrbitSpec { doll: 0, periapsis: s(p.periapsis), e_q48: p.e_q48, clockwise: false, angle: p.angle, phase: p.phase }, Scalar::ZERO)
            .unwrap();
        u.add_doll(p.name, b, p.mass_log2, Scalar::raw(p.radius as i128, -p.mass_log2).unwrap()).unwrap();
        planets.push((b, 2f64.powi(p.mass_log2)));
    }
    let belt: Vec<usize> = (0..n_census as u64).map(|k| ladder_ship(1, 300 + k, 1_000_000, 0).unwrap()).map(|(sp, r)| u.add_body(Kind::Ship, sp, r).unwrap()).collect();
    // Far bodies, beyond the Giant: periapsis 5.5 to 40 AU, e = 0.05.
    let far_au = [5.5, 7.0, 10.0, 15.0, 20.0, 30.0, 40.0];
    let far: Vec<usize> = far_au
        .iter()
        .enumerate()
        .map(|(k, &q)| {
            let spec = OrbitSpec { doll: 0, periapsis: s((q * AU) as i64), e_q48: (1u64 << 48) / 20, clockwise: false, angle: (k as u32).wrapping_mul(0x9E37_79B9), phase: (k as u32).wrapping_mul(0x7F4A_7C15) };
            u.add_body(Kind::Ship, spec, Scalar::raw(34, -10).unwrap()).unwrap()
        })
        .collect();
    u.start().unwrap();
    let ctx = u.ctx();
    let ps: Vec<Planet> = planets
        .iter()
        .map(|&(j, mu)| {
            let (x, v) = ctx.state_of(j, 0).unwrap();
            let (x0, v0) = ([to_f64(x[0]), to_f64(x[1])], [to_f64(v[0]), to_f64(v[1])]);
            let r = norm(x0);
            let a = 1.0 / (2.0 / r - dot(v0, v0) / (1.0 + mu));
            let e = norm(sub(mul(x0, dot(v0, v0) / (1.0 + mu) - 1.0 / r), mul(v0, dot(x0, v0) / (1.0 + mu))));
            Planet { mu, x0, v0, period: 2.0 * PI * (a * a * a / (1.0 + mu)).sqrt(), axis: a, peri: a * (1.0 - e), apo: a * (1.0 + e) }
        })
        .collect();
    drop(ctx);
    let build = t0.elapsed().as_secs_f64();
    let state = std::process::Command::new("sh").arg("artifacts/runs/frame/state.sh").output().map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string()).unwrap_or_default();
    println!("{state}");
    println!(
        "centring: the plane's root doll (Cinder {:.1} d, Home {:.1} d, the Giant {:.2} yr), {n_census} belt bodies of the ladder and {} far bodies; build {build:.1} s",
        ps[0].period * TICK_SECONDS / 86_400.0,
        ps[1].period * TICK_SECONDS / 86_400.0,
        ps[2].period * TICK_SECONDS / YEAR,
        far.len()
    );

    // 1. The census.
    let bodies: Vec<Body> = belt.iter().map(|&i| census_body(&u, i)).collect();
    let fars: Vec<Body> = far.iter().map(|&i| census_body(&u, i)).collect();
    let pow2 = |x: f64| 2f64.powi(x.log2().floor() as i32);
    // kicks per own period and per game-second for each rule (Δs = T/f'(c), rounded down to a power of two, as the law does).
    let rate = |b: &Body, t_phys: f64| -> (f64, f64) {
        let f = fp(b.c, b.b);
        let step = pow2(t_phys / f) * f;
        (b.period / step, 1.0 / (step * TICK_SECONDS))
    };
    let rules: [(&str, Box<dyn Fn(&Body) -> f64>); 5] = [
        ("the clock of 7 October (2^7 a Cinder period)", Box::new(|_b: &Body| ps[0].period * 2f64.powi(-cfg.step_log2))),
        ("the law now (heliocentric, each body's own clock)", Box::new(|b: &Body| b.ds * fp(b.c, b.b))),
        ("the same rule, heliocentric, in f64 (the check)", Box::new(|b: &Body| rule_step(&cfg, &ps, b, false, true))),
        ("Jacobi-centred, the quadrupole at the floor of 4", Box::new(|b: &Body| rule_step(&cfg, &ps, b, true, true))),
        ("Jacobi-centred, the quadrupole by its strength", Box::new(|b: &Body| rule_step(&cfg, &ps, b, true, false))),
    ];
    println!("\n1. THE CENSUS: steps per own period (min / median / max) and kicks per body per game-second (mean), by rule");
    for (name, rule) in &rules {
        let (mut spp, mut kgs): (Vec<f64>, Vec<f64>) = bodies.iter().map(|b| rate(b, rule(b))).unzip();
        let mean = kgs.iter().sum::<f64>() / kgs.len() as f64;
        print!(
            "  {name:<52} belt: {:>6.0} / {:>6.0} / {:>6.0} a period, {:.3e} kicks/body/game-s;",
            pct(&mut spp, 0.0),
            pct(&mut spp, 0.5),
            pct(&mut spp, 1.0),
            mean
        );
        let _ = pct(&mut kgs, 0.5);
        let far_spp: Vec<String> = fars.iter().map(|b| format!("{:.0}", rate(b, rule(b)).0)).collect();
        println!(" far ({}) AU: {} a period", far_au.iter().map(|q| format!("{q}")).collect::<Vec<_>>().join(", "), far_spp.join(", "));
    }
    // What a moving centre costs a reader: the enclosed planets' states at the read's tick, against the body's own tube read.
    {
        let ctx = u.ctx();
        let reads = 20_000i64;
        let tick = |k: i64| (k * 7_919_000_003) % 2_000_000_000_000;
        let t2 = Instant::now();
        let mut sink = 0.0;
        for k in 0..reads {
            sink += to_f64(ctx.state_of(belt[(k as usize) % belt.len().min(64)], tick(k)).unwrap().0[0]);
        }
        let own = t2.elapsed().as_secs_f64() / reads as f64;
        let t3 = Instant::now();
        for k in 0..reads {
            for &(j, _) in &planets[..2] {
                sink += to_f64(ctx.state_of(j, tick(k)).unwrap().0[0]);
            }
        }
        let two = t3.elapsed().as_secs_f64() / reads as f64;
        println!(
            "  a reader's cost: a belt body's own tube read {:.2} us; Cinder's and Home's states at the read's tick (the belt's centre) {:.2} us more ({sink:.0e})",
            own * 1e6,
            two * 1e6
        );
    }
    let check = bodies.iter().filter(|b| (pow2(rule_step(&cfg, &ps, b, false, true) / fp(b.c, b.b)) / b.ds - 1.0).abs() > 1e-9).count();
    println!("  (the f64 rule differs from the law's Δs on {check} of {} belt bodies)", bodies.len());

    // 2. The replica.
    let horizon = years * YEAR / TICK_SECONDS;
    let samples: Vec<f64> = (0..=32).map(|i| horizon * 2f64.powf((i as f64 - 32.0) / 4.0)).collect();
    let tyears: Vec<f64> = samples.iter().map(|&t| t * TICK_SECONDS / YEAR).collect();
    let fly_set: Vec<&Body> = bodies.iter().step_by((bodies.len() / n_fly).max(1)).take(n_fly).collect();
    let helio = Centre { m: 1.0, set: vec![] };
    let centre_of = |b: &Body| {
        let set: Vec<usize> = (0..ps.len()).filter(|&j| ps[j].apo < b.q).collect();
        Centre { m: 1.0 + set.iter().map(|&j| ps[j].mu).sum::<f64>(), set }
    };
    let ds_of = |b: &Body, t_phys: f64| pow2(t_phys / fp(b.c, b.b));
    let t1 = Instant::now();
    let reference: Vec<Vec<(V, V)>> = fly_set.iter().map(|b| fly(&ps, &helio, b.x0, b.v0, ds_of(b, ps[0].period / 512.0), b.c, b.b, &samples).0).collect();
    println!(
        "\n2. THE REPLICA (f64, the law's map, outside the law): {} belt bodies over {years} years; reference: heliocentric at 2^10 steps a Cinder period (2^9: {:.1} s)",
        fly_set.len(),
        t1.elapsed().as_secs_f64()
    );
    let report = |name: &str, jac: bool, t_of: &dyn Fn(&Body) -> f64, against: &Vec<Vec<(V, V)>>| -> Vec<Vec<(V, V)>> {
        let t2 = Instant::now();
        let runs: Vec<(Vec<(V, V)>, u64, f64)> = fly_set
            .iter()
            .map(|b| {
                let c = if jac { centre_of(b) } else { Centre { m: 1.0, set: vec![] } };
                let ds = ds_of(b, t_of(b));
                let (st, k) = fly(&ps, &c, b.x0, b.v0, ds, b.c, b.b, &samples);
                (st, k, b.period / (ds * fp(b.c, b.b)))
            })
            .collect();
        let (mut da, mut de) = (vec![Vec::new(); samples.len()], vec![Vec::new(); samples.len()]);
        for (r, (law, _, _)) in against.iter().zip(&runs) {
            for (k, (a, b)) in r.iter().zip(law).enumerate() {
                let ((ar, er), (al, el)) = (elements(a.0, a.1), elements(b.0, b.1));
                da[k].push(((al - ar) / ar).abs());
                de[k].push((el - er).abs());
            }
        }
        let worst = |m: &Vec<Vec<f64>>| -> Vec<f64> { m.iter().map(|v| v.iter().cloned().fold(0.0, f64::max)).collect() };
        let median = |m: &Vec<Vec<f64>>| -> Vec<f64> { m.iter().map(|v| pct(&mut v.clone(), 0.5)).collect() };
        let (wa, we, ma, me) = (worst(&da), worst(&de), median(&da), median(&de));
        let mut spp: Vec<f64> = runs.iter().map(|r| r.2).collect();
        let kicks: u64 = runs.iter().map(|r| r.1).sum();
        println!(
            "  {name:<54} {:>5.0} / {:>5.0} kicks a period (median / max), {:.3e} kicks/body/game-s, {:.1} s",
            pct(&mut spp, 0.5),
            pct(&mut spp, 1.0),
            kicks as f64 / fly_set.len() as f64 / (horizon * TICK_SECONDS),
            t2.elapsed().as_secs_f64()
        );
        for k in [16usize, 24, 28, 32] {
            println!("      t {:>7.2} yr: |da|/a median {:.2e} worst {:.2e}; |de| median {:.2e} worst {:.2e}", tyears[k], ma[k], wa[k], me[k], we[k]);
        }
        println!(
            "      growth exponent of the worst: da {:.2}, de {:.2}; of the median: da {:.2}, de {:.2}",
            exponent(&tyears, &wa),
            exponent(&tyears, &we),
            exponent(&tyears, &ma),
            exponent(&tyears, &me)
        );
        runs.into_iter().map(|r| r.0).collect()
    };
    let reference = report("the reference at 2^10 against 2^9 (its own error)", false, &|_b: &Body| ps[0].period / 1024.0, &reference);
    report("heliocentric, the law's steps (the check: an offset)", false, &|b: &Body| b.ds * fp(b.c, b.b), &reference);
    for k in [4, 5] {
        report(&format!("heliocentric, 2^{k} a period (the check: e walks)"), false, &|b: &Body| b.period * 2f64.powi(-k), &reference);
    }
    for k in [3, 4, 5] {
        report(&format!("Jacobi-centred, 2^{k} a period"), true, &|b: &Body| b.period * 2f64.powi(-k), &reference);
    }
    report("Jacobi-centred, the rule (quadrupole at the floor)", true, &|b: &Body| rule_step(&cfg, &ps, b, true, true), &reference);
}
