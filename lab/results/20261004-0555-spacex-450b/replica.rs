// Float replica of the plane's motion law (docs/law.md "Perturbed motion", crates/universe/src/step.rs)
// for the q-correctors question: fewer kicks per orbit at unchanged behaviours.
//
// Scene: CRTBP (star + planet on a circular barycentric orbit at rate N_ORB = sqrt(G M_tot / a^3)),
// moon as a test particle. Split: drift = exact Kepler about the planet (the doll's tube); kick =
// the star's tide (star gravity on the moon minus the uniform field = star gravity at the planet),
// evaluated at the kick time. The step is in the drift's own phase: dt = P(a)/N, like the plane's
// 1/64 of the radial period. DKD: drift h/2, one kick of weight h at the midpoint, drift h/2.
//
// Schemes: dkd (the plane's law; 1 kick per interval), y4 = Yoshida-4 triple jump of DKD (3 kicks),
// y6 = triple jump of y4 (9 kicks), y4q = y4 with weights rounded to 1/256 (integer path: dyadic).
// Cost metric = kick applications per orbit (each application is a rebind in the engine).
//
// Gates: apsidal precession within 10% of the reference (B14), Jacobi error <= 1e-4 relative with
// growth exponent <= 0.2 (B12/B5 style), mean e over the last 100 planet orbits within 10% (B14).
use std::f64::consts::PI;

#[derive(Clone, Copy)]
struct V2 { x: f64, y: f64 }
impl V2 {
    fn new(x: f64, y: f64) -> V2 { V2 { x, y } }
    fn add(self, o: V2) -> V2 { V2::new(self.x + o.x, self.y + o.y) }
    fn scale(self, s: f64) -> V2 { V2::new(self.x * s, self.y * s) }
    fn dot(self, o: V2) -> f64 { self.x * o.x + self.y * o.y }
    fn norm(self) -> f64 { self.dot(self).sqrt() }
}

const MUSTAR: f64 = 1.0;   // G M_star
const MUP: f64 = 1.0e-3;   // G M_planet
const MTOT: f64 = MUSTAR + MUP;
const AP: f64 = 1.0;       // star-planet separation
const N_ORB: f64 = 1.0004998750624609; // sqrt(MTOT / AP^3), exact circular rate
const TEND: f64 = 50.0 * 2.0 * PI / N_ORB; // 50 planet orbits

// planet-relative helpers: (cos, sin) of the phase angle
fn cs(t: f64) -> (f64, f64) { let a = N_ORB * t; (a.cos(), a.sin()) }
fn planet_pos(t: f64) -> V2 { let (c, s) = cs(t); V2::new((MUSTAR / MTOT) * AP * c, (MUSTAR / MTOT) * AP * s) }
fn planet_vel(t: f64) -> V2 { let (c, s) = cs(t); V2::new(-(MUSTAR / MTOT) * AP * N_ORB * s, (MUSTAR / MTOT) * AP * N_ORB * c) }

// the kick: star's tide at planet-relative r, at time ts
fn tide_accel(r: V2, ts: f64) -> V2 {
    let (c, s) = cs(ts);
    let d = V2::new(r.x + AP * c, r.y + AP * s); // moon - star
    let dcub = d.norm().powi(3);
    // a_rel = -GM* [ d/|d|^3 - unit(cos,sin)/AP^2 ]
    V2::new(-MUSTAR * (d.x / dcub - c / (AP * AP)), -MUSTAR * (d.y / dcub - s / (AP * AP)))
}

#[derive(Clone, Copy)]
struct State { r: V2, v: V2 } // planet-relative

fn inertial_advance(st: State, dt: f64) -> State { State { r: st.r.add(st.v.scale(dt)), v: st.v } }

// Kepler advance about the planet by dt (the exact drift). s = sign of angular momentum.
fn kepler_advance(st: State, dt: f64) -> State {
    let mu = MUP;
    let r = st.r.norm();
    let v2 = st.v.dot(st.v);
    let eps = v2 / 2.0 - mu / r;
    let a = -mu / (2.0 * eps);
    if !(a > 0.0 && a < 10.0) { return inertial_advance(st, dt); } // unbound: straight line
    let hz = st.r.x * st.v.y - st.r.y * st.v.x;
    let s = if hz >= 0.0 { 1.0 } else { -1.0 };
    let rv = st.r.dot(st.v);
    let ex = (v2 / mu - 1.0 / r) * st.r.x - (rv / mu) * st.v.x;
    let ey = (v2 / mu - 1.0 / r) * st.r.y - (rv / mu) * st.v.y;
    let e = (ex * ex + ey * ey).sqrt();
    let w = f64::atan2(ey, ex);
    let n = (mu / (a * a * a)).sqrt();
    // current eccentric anomaly
    let mut ecc = f64::atan2(rv / (e * (mu * a).sqrt()), (1.0 - r / a) / e);
    let manom0 = ecc - e * ecc.sin();
    // advance mean anomaly and solve Kepler's equation
    let manom = manom0 + n * dt;
    let mut ean = manom;
    for _ in 0..8 {
        let f = ean - e * ean.sin() - manom;
        let fp = 1.0 - e * ean.cos();
        ean -= f / fp;
    }
    let rn = a * (1.0 - e * ean.cos());
    let xp = a * (ean.cos() - e);
    let yp = s * a * (1.0 - e * e).sqrt() * ean.sin();
    let vxp = -(mu * a).sqrt() / rn * ean.sin();
    let vyp = s * (mu * a).sqrt() / rn * (1.0 - e * e).sqrt() * ean.cos();
    let (cw, sw) = (w.cos(), w.sin());
    State {
        r: V2::new(cw * xp - sw * yp, sw * xp + cw * yp),
        v: V2::new(cw * vxp - sw * vyp, sw * vxp + cw * vyp),
    }
}

// one DKD step of total dt at time t: drift h/2, kick of weight h at the midpoint, drift h/2.
fn dkd_step(mut st: State, t: f64, dt: f64) -> State {
    st = kepler_advance(st, dt / 2.0);
    let a = tide_accel(st.r, t + dt / 2.0);
    st.v = st.v.add(a.scale(dt));
    kepler_advance(st, dt / 2.0)
}

fn y4_step(st: State, t: f64, dt: f64) -> State {
    let w1 = 1.0 / (2.0 - 2.0f64.cbrt());
    let w2 = 1.0 - 2.0 * w1;
    let mut s = dkd_step(st, t, w1 * dt);
    s = dkd_step(s, t + w1 * dt, w2 * dt);
    dkd_step(s, t + (w1 + w2) * dt, w1 * dt)
}

// y4 with weights rounded to 1/256 (dyadic rationals: the integer path)
fn y4q_step(st: State, t: f64, dt: f64) -> State {
    let w1 = (256.0 / (2.0 - 2.0f64.cbrt())).round() / 256.0;
    let w2 = 1.0 - 2.0 * w1;
    let mut s = dkd_step(st, t, w1 * dt);
    s = dkd_step(s, t + w1 * dt, w2 * dt);
    dkd_step(s, t + (w1 + w2) * dt, w1 * dt)
}

fn y6_step(st: State, t: f64, dt: f64) -> State {
    let u1 = 1.0 / (2.0 - 2.0f64.powf(0.2));
    let u2 = 1.0 - 2.0 * u1;
    let mut s = y4_step(st, t, u1 * dt);
    s = y4_step(s, t + u1 * dt, u2 * dt);
    y4_step(s, t + (u1 + u2) * dt, u1 * dt)
}

#[derive(Clone, Copy, PartialEq)]
enum Scheme { Dkd, Y4, Y4q, Y6 }
fn step_fn(s: Scheme) -> fn(State, f64, f64) -> State {
    match s { Scheme::Dkd => dkd_step, Scheme::Y4 => y4_step, Scheme::Y4q => y4q_step, Scheme::Y6 => y6_step }
}
fn subkicks(s: Scheme) -> f64 { match s { Scheme::Dkd => 1.0, Scheme::Y4 | Scheme::Y4q => 3.0, Scheme::Y6 => 9.0 } }
fn sch_id(s: Scheme) -> &'static str { match s { Scheme::Dkd => "dkd", Scheme::Y4 => "y4", Scheme::Y4q => "y4q", Scheme::Y6 => "y6" } }

// Jacobi constant of the CRTBP at time t (rotating frame at N_ORB)
fn jacobi(st: State, t: f64) -> f64 {
    let (c, s) = cs(t);
    let ri = st.r.add(planet_pos(t));
    let vi = st.v.add(planet_vel(t));
    let xr = c * ri.x + s * ri.y;
    let yr = -s * ri.x + c * ri.y;
    let vxr = c * vi.x + s * vi.y + N_ORB * yr;
    let vyr = -s * vi.x + c * vi.y - N_ORB * xr;
    // star sits at (-(MUP/MTOT)*AP, 0) in the rotating frame
    let dsx = xr + (MUP / MTOT) * AP;
    let d_star = (dsx * dsx + yr * yr).sqrt();
    let d_p = st.r.norm();
    N_ORB * N_ORB * (xr * xr + yr * yr) + 2.0 * MUSTAR / d_star + 2.0 * MUP / d_p - (vxr * vxr + vyr * vyr)
}

fn elements(st: State) -> (f64, f64, f64) {
    let mu = MUP;
    let r = st.r.norm();
    let v2 = st.v.dot(st.v);
    let eps = v2 / 2.0 - mu / r;
    let a = -mu / (2.0 * eps);
    let rv = st.r.dot(st.v);
    let ex = (v2 / mu - 1.0 / r) * st.r.x - (rv / mu) * st.v.x;
    let ey = (v2 / mu - 1.0 / r) * st.r.y - (rv / mu) * st.v.y;
    let e = (ex * ex + ey * ey).sqrt();
    (a, e, f64::atan2(ey, ex))
}

struct Outcome { kicks_per_orbit: f64, prec_slope: f64, e_mean_late: f64, jac_max: f64, jac_exp: f64, e_max: f64, bound: bool }

fn run(scheme: Scheme, macro_per_orbit: f64, a_m: f64, e0: f64, retro: bool) -> Outcome {
    let f = step_fn(scheme);
    let r0 = a_m * (1.0 + e0);
    let v0 = (MUP / a_m * (1.0 - e0) / (1.0 + e0)).sqrt();
    let sgn = if retro { -1.0 } else { 1.0 };
    let mut st = State { r: V2::new(r0, 0.0), v: V2::new(0.0, sgn * v0) };
    let mut t = 0.0f64;
    let c0 = jacobi(st, t);
    let mut jac_max = 0.0f64;
    let mut max_to: Vec<(f64, f64)> = Vec::new();
    let mut prec: Vec<(f64, f64)> = Vec::new();
    let mut es: Vec<(f64, f64)> = Vec::new();
    let mut kicks = 0u64;
    let mut om_prev = elements(st).2;
    let mut unwrapped = 0.0f64;
    let mut next_sample = 0.0f64;
    let mut e_max = 0.0f64;
    let p_moon = 2.0 * PI * (a_m * a_m * a_m / MUP).sqrt();
    while t < TEND {
        let (a, _e, _w) = elements(st);
        let a_eff = if a > 0.0 && a < 10.0 { a } else { a_m };
        let period = 2.0 * PI * (a_eff * a_eff * a_eff / MUP).sqrt();
        let dt = period / macro_per_orbit;
        st = f(st, t, dt);
        t += dt;
        kicks += subkicks(scheme) as u64;
        if st.r.norm() > 5.0 { break; } // escaped
        if t >= next_sample {
            let cj = jacobi(st, t);
            let err = ((cj - c0) / c0).abs();
            if err > jac_max { jac_max = err; }
            max_to.push((t, jac_max));
            let (_a, e, w) = elements(st);
            if e > e_max { e_max = e; }
            let mut dw = w - om_prev;
            while dw > PI { dw -= 2.0 * PI; }
            while dw < -PI { dw += 2.0 * PI; }
            unwrapped += dw;
            om_prev = w;
            prec.push((t, unwrapped));
            es.push((t, e));
            next_sample += 0.25;
        }
    }
    let bound = t >= TEND;
    let t0 = TEND * 0.4;
    let (mut n, mut sx, mut sy, mut sxx, mut sxy) = (0.0, 0.0, 0.0, 0.0, 0.0);
    for (tt, w) in &prec { if *tt >= t0 { n += 1.0; sx += tt; sy += w; sxx += tt * tt; sxy += tt * w; } }
    let slope = (n * sxy - sx * sy) / (n * sxx - sx * sx).max(1e-30);
    let te = TEND - 100.0 * 2.0 * PI / N_ORB;
    let (mut m, mut se) = (0.0, 0.0);
    for (tt, e) in &es { if *tt >= te { m += 1.0; se += e; } }
    let e_mean = if m > 0.0 { se / m } else { -1.0 };
    let th = TEND * 0.5;
    let (mut n2, mut sx2, mut sy2, mut sxx2, mut sxy2) = (0.0, 0.0, 0.0, 0.0, 0.0);
    for (tt, err) in &max_to { if *tt >= th && *err > 0.0 { n2 += 1.0; let (lt, le) = (tt.ln(), err.ln()); sx2 += lt; sy2 += le; sxx2 += lt * lt; sxy2 += lt * le; } }
    let expn = if n2 > 2.0 { (n2 * sxy2 - sx2 * sy2) / (n2 * sxx2 - sx2 * sx2) } else { 0.0 };
    Outcome {
        kicks_per_orbit: kicks as f64 / (TEND / p_moon),
        prec_slope: slope, e_mean_late: e_mean, jac_max, jac_exp: expn, e_max, bound,
    }
}

fn main() {
    let mode = std::env::args().nth(1).unwrap_or_else(|| "sweep".to_string());
    let rhill = AP * (MUP / 3.0f64).cbrt();
    let cases: Vec<(&str, f64, f64, bool)> = vec![
        ("A_prec_0.30RH_e15", 0.30, 0.15, false),
        ("B_jac_0.30RH_e05", 0.30, 0.05, false),
        ("C_hold_e30", 0.30, 0.30, false),
        ("D_hold_e60", 0.30, 0.60, false),
        ("E_hold_retro", 0.30, 0.15, true),
        ("F_hold_retro_0.60RH", 0.60, 0.15, true),
        ("G_hold_0.45RH", 0.45, 0.15, false),
    ];
    let mut refs = std::collections::HashMap::new();
    for (name, fr, e0, retro) in &cases {
        let a_m = fr * rhill;
        let o1 = run(Scheme::Dkd, 4096.0, a_m, *e0, *retro);
        let o2 = run(Scheme::Y6, 456.0, a_m, *e0, *retro);
        refs.insert(name.to_string(), (o1.prec_slope, o2.prec_slope, o1.e_mean_late, o2.e_mean_late));
        if mode == "ref" {
            println!("REF {} a_m={:.5} e0={} prec_dkd4096={:.6e} prec_y6={:.6e} rel={:.3e} jac_dkd={:.2e} jac_y6={:.2e} e_dkd={:.5} e_y6={:.5} bound={}/{}",
                name, a_m, e0, o1.prec_slope, o2.prec_slope,
                ((o2.prec_slope - o1.prec_slope) / o1.prec_slope).abs(), o1.jac_max, o2.jac_max, o1.e_mean_late, o2.e_mean_late, o1.bound, o2.bound);
        }
    }
    if mode == "ref" { return; }
    println!("scheme macro kicksPerOrbit case prec_slope prec_rel e_mean e_rel jac_max jac_exp e_max bound");
    for (name, fr, e0, retro) in &cases {
        let a_m = fr * rhill;
        let (p1, p2, e1, e2) = refs[*name];
        let pref = 0.5 * (p1 + p2);
        let eref = 0.5 * (e1 + e2);
        let schemes: Vec<(Scheme, Vec<f64>)> = vec![
            (Scheme::Dkd, vec![2.0, 4.0, 8.0, 16.0, 32.0, 64.0]),
            (Scheme::Y4, vec![1.0, 2.0, 4.0, 8.0, 16.0]),
            (Scheme::Y4q, vec![1.0, 2.0, 4.0, 8.0]),
            (Scheme::Y6, vec![1.0, 2.0, 4.0]),
        ];
        for (sch, ms) in &schemes {
            for m in ms {
                let o = run(*sch, *m, a_m, *e0, *retro);
                let prel = ((o.prec_slope - pref) / pref).abs();
                let erel = ((o.e_mean_late - eref) / eref).abs();
                println!("{} {} {:.1} {} {:.6e} {:.4} {:.5} {:.4} {:.2e} {:.3} {:.4} {}",
                    sch_id(*sch), m, o.kicks_per_orbit, name, o.prec_slope, prel, o.e_mean_late, erel, o.jac_max, o.jac_exp, o.e_max, o.bound);
            }
        }
    }
}
