// Float replica of the plane's motion law (docs/law.md "Perturbed motion",
// crates/universe/src/step.rs): exact two-body drift around the dominant mass
// + tidal kicks at a fixed step. Question: how few kicks per moon orbit keep
// the behaviours (Jacobi bounded, apsidal precession, bound/escape class)
// when a symplectic corrector (WHFast, Rein&Tamayo 2015 / REBOUND coeff.) or
// a 4th-order split (Yoshida) is used, vs the plain DKD leapfrog.
//
// Model: star mu*=1 fixed at origin. Planet 1 forced circular: a=1, n=1.
// Optional planet 2 (close-pass scene): Kepler orbit (a2,e2,varpi2,M20).
// Moon: planetocentric state (r,v), mu_p. Kicks: tide = perturber pull on
// moon minus perturber pull on planet, evaluated at the kick epoch.
//
// Schemes (per step of size h, shared by all moons):
//   dkd   : D(h/2) K(h) D(h/2)                        [plane today, 1 kick]
//   dkd3  : dkd + 3rd-order corrector at outputs      [8 kicks/output]
//   dkd5  : dkd + 5th-order corrector at outputs      [16 kicks/output]
//   y4    : Yoshida-4 triple jump (3 kicks/step)
//   euler : K(h) D(h)  (non-symmetric, negative control)
//
// Outputs every 1 planet orbit: corrector applied, observed, un-applied.
// No deps. Prints JSON lines: scheme,K,scene,moon,metric...

use std::f64::consts::PI;
use std::io::Write;

#[derive(Clone, Copy, Debug)]
struct V3(pub [f64; 3]);
impl V3 {
    fn new(x: f64, y: f64, z: f64) -> Self { V3([x, y, z]) }
    fn add(self, o: V3) -> V3 { V3([self.0[0]+o.0[0], self.0[1]+o.0[1], self.0[2]+o.0[2]]) }
    fn sub(self, o: V3) -> V3 { V3([self.0[0]-o.0[0], self.0[1]-o.0[1], self.0[2]-o.0[2]]) }
    fn scale(self, s: f64) -> V3 { V3([self.0[0]*s, self.0[1]*s, self.0[2]*s]) }
    fn dot(self, o: V3) -> f64 { self.0[0]*o.0[0] + self.0[1]*o.0[1] + self.0[2]*o.0[2] }
    fn cross(self, o: V3) -> V3 {
        V3([self.0[1]*o.0[2]-self.0[2]*o.0[1], self.0[2]*o.0[0]-self.0[0]*o.0[2], self.0[0]*o.0[1]-self.0[1]*o.0[0]])
    }
    fn norm(self) -> f64 { self.dot(self).sqrt() }
}

#[derive(Clone, Copy)]
struct Scene {
    name: &'static str,
    mu_p: f64,
    // planet 2 (0 => none)
    mu2: f64, a2: f64, e2: f64, varpi2: f64, m20: f64,
    t_end: f64, // total time (50 planet orbits = 100*pi)
}

fn planet1(t: f64) -> V3 { V3::new(t.cos(), t.sin(), 0.0) }

/// Planet 2 heliocentric position (Kepler, mu*=1). M2 = m20 + n2 t.
fn planet2(t: f64, sc: &Scene) -> V3 {
    if sc.mu2 == 0.0 { return V3::new(0.0, 0.0, 0.0); }
    let n2 = (1.0f64 / sc.a2).powi(3).sqrt(); // mu*=1
    let mut m = sc.m20 + n2 * t;
    m = m.rem_euclid(2.0 * PI);
    let e = sc.e2;
    // Newton on E - e sinE = M
    let mut ea = m + e * m.sin();
    for _ in 0..60 {
        let f = ea - e * ea.sin() - m;
        let fp = 1.0 - e * ea.cos();
        let d = f / fp;
        ea -= d;
        if d.abs() < 1e-15 { break; }
    }
    let x = sc.a2 * (ea.cos() - e);
    let y = sc.a2 * (1.0 - e * e).sqrt() * ea.sin();
    let (c, s) = (sc.varpi2.cos(), sc.varpi2.sin());
    V3::new(c * x - s * y, s * x + c * y, 0.0)
}

/// Tidal acceleration on the moon, planetocentric, at epoch t.
fn tide(r: V3, t: f64, sc: &Scene) -> V3 {
    let rp1 = planet1(t);
    // star tide: pull on moon (heliocentric rp1 + r) minus pull on planet1
    let rm = rp1.add(r);
    let d3 = rm.norm().powi(3);
    let a_m = rm.scale(-1.0 / d3); // mu* = 1
    let p3 = rp1.norm().powi(3);
    let a_p = rp1.scale(-1.0 / p3);
    let mut a = a_m.sub(a_p);
    if sc.mu2 > 0.0 {
        let rp2 = planet2(t, sc);
        let rm2 = rp2.add(r);
        let a_m2 = rm2.scale(-sc.mu2 / rm2.norm().powi(3));
        let d13 = rp2.sub(rp1).norm().powi(3);
        let a_p2 = rp2.sub(rp1).scale(-sc.mu2 / d13);
        a = a.add(a_m2.sub(a_p2));
    }
    a
}

/// Exact Kepler drift (elliptic DE-form). Fails (returns false) if unbound.
fn drift(r: &mut V3, v: &mut V3, mu: f64, dt: f64) -> bool {
    let r0 = r.norm();
    let v2 = v.dot(*v);
    let energy = 0.5 * v2 - mu / r0;
    if energy >= 0.0 { return false; }
    let a = -mu / (2.0 * energy);
    let n = (mu / (a * a * a)).sqrt();
    let ece0 = 1.0 - r0 / a;
    let ese0 = r.dot(*v) / (mu * a).sqrt();
    // solve: de - ece0*sin(de) + ese0*(1 - cos(de)) = n*dt
    let mut de = n * dt;
    for _ in 0..80 {
        let f = de - ece0 * de.sin() + ese0 * (1.0 - de.cos()) - n * dt;
        let fp = 1.0 - ece0 * de.cos() + ese0 * de.sin();
        let d = f / fp;
        de -= d;
        if d.abs() < 1e-15 { break; }
    }
    let (sde, cde) = (de.sin(), de.cos());
    let f = 1.0 - (a / r0) * (1.0 - cde);
    let g = dt - (a * a * a / mu).sqrt() * (de - sde);
    let rn_v = r.scale(f).add(v.scale(g));
    let rn = rn_v.norm();
    let fd = -(mu * a).sqrt() / (r0 * rn) * sde;
    let gd = 1.0 - (a / rn) * (1.0 - cde);
    *v = r.scale(fd).add(v.scale(gd));
    *r = rn_v;
    true
}

/// Osculating planetocentric elements.
fn elems(r: V3, v: V3, mu: f64) -> (f64, f64) { // (a, e)
    let r0 = r.norm();
    let v2 = v.dot(v);
    let en = 0.5 * v2 - mu / r0;
    let a = -mu / (2.0 * en);
    let h = r.cross(v);
    let ev = v.cross(h).scale(1.0 / mu).sub(r.scale(1.0 / r0));
    (a, ev.norm())
}

/// Jacobi constant (no planet 2): rotating frame, n=1.
/// C = n^2 |R_h,xy|^2 + 2 mu*/|R_h| + 2 mu_p/|r| - |v_rot|^2,
/// v_rot = R(-nt) (v - n x r).
fn jacobi(r: V3, v: V3, t: f64, sc: &Scene) -> f64 {
    let rp = planet1(t);
    let rh = rp.add(r);
    let u = v.sub(V3::new(-r.0[1], r.0[0], 0.0)); // v - n x r
    let (c, s) = (t.cos(), t.sin());
    let rot = |w: V3| V3::new(c * w.0[0] + s * w.0[1], -s * w.0[0] + c * w.0[1], w.0[2]);
    let rr = rot(rh);
    let vr = rot(u);
    let _ = sc;
    (rr.0[0] * rr.0[0] + rr.0[1] * rr.0[1]) + 2.0 / rh.norm() + 2.0 * sc.mu_p / r.norm()
        - vr.dot(vr)
}
const A1: f64 = 0.41833001326703777398908601289259374469640768464934;
const A2: f64 = 0.83666002653407554797817202578518748939281536929867;
const A3: f64 = 1.2549900398011133219672580386777812340892230539480;
const A4: f64 = 1.6733200530681510959563440515703749787856307385973;
const A5: f64 = 2.0916500663351888699454300644629687234820384232467;
const B31: f64 = -0.024900596027799867499350357910273437184309981229127;
const B51: f64 = -0.0083001986759332891664501193034244790614366604097090;
const B52: f64 = 0.041500993379666445832250596517122395307183302048545;

#[derive(Clone)]
struct Moon {
    r: V3, v: V3,
    t: f64,
    h: f64,        // step size (time), constant
    kicks: u64,
    escaped: bool,
    esc_epoch: Option<f64>,
}

struct Ctx {
    sc: Scene,
}

impl Ctx {
    /// One elementary kernel Z(a,b) = D(a) K(-b) D(-2a) K(b) D(a). Returns kicks used.
    fn z(&self, m: &mut Moon, a: f64, b: f64) -> u32 {
        // dt scaling: a,b are already h-scaled
        let mut k = 0;
        drift(&mut m.r, &mut m.v, self.sc.mu_p, a); m.t += a;
        let acc = tide(m.r, m.t, &self.sc);
        m.v = m.v.add(acc.scale(-b)); m.t += 0.0; k += 1;
        drift(&mut m.r, &mut m.v, self.sc.mu_p, -2.0 * a); m.t -= 2.0 * a;
        let acc = tide(m.r, m.t, &self.sc);
        m.v = m.v.add(acc.scale(b)); k += 1;
        drift(&mut m.r, &mut m.v, self.sc.mu_p, a); m.t += a;
        k
    }

    /// Apply (inv=+1) or un-apply (inv=-1) corrector of given order.
    fn corrector(&self, m: &mut Moon, order: u32, inv: f64) -> u32 {
        let h = m.h;
        let mut k = 0;
        if order == 3 {
            k += self.z(m, A1 * h, -inv * B31 * h);
            k += self.z(m, -A1 * h, inv * B31 * h);
        } else if order == 5 {
            k += self.z(m, -A2 * h, -inv * B51 * h);
            k += self.z(m, -A1 * h, -inv * B52 * h);
            k += self.z(m, A1 * h, inv * B52 * h);
            k += self.z(m, A2 * h, inv * B51 * h);
        } else { unreachable!() }
        k
    }

    fn kick(&self, m: &mut Moon, w: f64) {
        let acc = tide(m.r, m.t, &self.sc);
        m.v = m.v.add(acc.scale(w));
        m.kicks += 1;
    }

    fn drift_ok(&self, m: &mut Moon, dt: f64) -> bool {
        let ok = drift(&mut m.r, &mut m.v, self.sc.mu_p, dt);
        if ok { m.t += dt; }
        ok
    }

    /// One macro step of a scheme. h = m.h. Returns false if drift failed (escape).
    fn step(&self, m: &mut Moon, scheme: &str) -> bool {
        let h = m.h;
        match scheme {
            "dkd" | "dkd3" | "dkd5" => {
                if !self.drift_ok(m, h / 2.0) { return false; }
                self.kick(m, h);
                if !self.drift_ok(m, h / 2.0) { return false; }
                true
            }
            "y4" => {
                let cbrt2 = 2.0f64.cbrt();
                let w1 = 1.0 / (2.0 - cbrt2);
                let w0 = -cbrt2 * w1;
                // D(w1/2) K(w1) D((w0+w1)/2) K(w0) D((w0+w1)/2) K(w1) D(w1/2)
                if !self.drift_ok(m, w1 * h / 2.0) { return false; }
                self.kick(m, w1 * h);
                if !self.drift_ok(m, (w0 + w1) * h / 2.0) { return false; }
                self.kick(m, w0 * h);
                if !self.drift_ok(m, (w0 + w1) * h / 2.0) { return false; }
                self.kick(m, w1 * h);
                if !self.drift_ok(m, w1 * h / 2.0) { return false; }
                true
            }
            "euler" => {
                self.kick(m, h);
                if !self.drift_ok(m, h) { return false; }
                true
            }
            _ => unreachable!(),
        }
    }
}

/// Apsidal angle (argument of periapsis) of the planetocentric orbit.
fn apsidal(r: V3, v: V3, mu: f64) -> f64 {
    let h = r.cross(v);
    let ev = v.cross(h).scale(1.0 / mu).sub(r.scale(1.0 / r.norm()));
    let nvec = V3::new(-h.0[1], h.0[0], 0.0); // node ~ z x h
    let nh = nvec.norm();
    if nh < 1e-6 * h.norm().max(1e-300) {
        // coplanar: measure from +x, sense from h_z
        let s = if h.0[2] >= 0.0 { 1.0 } else { -1.0 };
        return ev.0[1].atan2(ev.0[0]) * s + if s < 0.0 { 2.0 * PI } else { 0.0 };
    }
    let mut arg = (ev.0[0] * nvec.0[0] + ev.0[1] * nvec.0[1]) / (ev.norm() * nh);
    if arg > 1.0 { arg = 1.0; }
    if arg < -1.0 { arg = -1.0; }
    let mut w = arg.acos();
    // sign from (n x e) . h
    if nvec.cross(ev).dot(h) < 0.0 { w = 2.0 * PI - w; }
    w
}

struct RunResult {
    r_fin: V3,
    j_max: f64,          // max |dJ/J0| over outputs
    j_slope: f64,        // log-log slope of |dJ| envelope vs orbit count
    prec: f64,           // apsidal advance per moon orbit (rad), from LSQ fit
    bound: bool,         // never escaped
    kicks: u64,
    escaped_at: Option<f64>,
    final_a: f64, final_e: f64,
    valid: bool,         // reference-track sanity
}

fn run(scheme: &str, order: u32, kpo: u64, sc: &Scene, r0: V3, v0: V3, collect_trace: bool) -> RunResult {
    let ctx = Ctx { sc: *sc };
    let (a0, _e0) = elems(r0, v0, sc.mu_p);
    let p0 = 2.0 * PI * (a0 * a0 * a0 / sc.mu_p).sqrt();
    let h = p0 / kpo as f64;
    let mut m = Moon { r: r0, v: v0, t: 0.0, h, kicks: 0, escaped: false, esc_epoch: None };
    let j0 = if sc.mu2 == 0.0 { jacobi(r0, v0, 0.0, sc) } else { 0.0 };
    let mut j_max = 0.0f64;
    let mut j_hist: Vec<(f64, f64)> = Vec::new();
    let mut w_hist: Vec<(f64, f64, f64)> = Vec::new(); // (t, apsidal angle unwrapped, e_osc)
    let mut w_prev: Option<f64> = None;
    let mut outs: Vec<String> = Vec::new();
    let n_out = (sc.t_end / (2.0 * PI)).round() as i64;
    let mut last_out = 0i64;
    // initial output (t=0)
    let mut observe = |m: &Moon, j0: f64, w_prev: &mut Option<f64>, w_hist: &mut Vec<(f64, f64, f64)>, j_hist: &mut Vec<(f64,f64)>, j_max: &mut f64| -> f64 {
        if sc.mu2 == 0.0 {
            let j = jacobi(m.r, m.v, m.t, sc);
            let dj = ((j - j0) / j0).abs();
            if dj > *j_max { *j_max = dj; }
            j_hist.push((m.t, dj));
        }
        let w = apsidal(m.r, m.v, sc.mu_p);
        let (_, e_osc) = elems(m.r, m.v, sc.mu_p);
        if let Some(p) = *w_prev {
            let mut dw = w - p;
            while dw > PI { dw -= 2.0 * PI; }
            while dw < -PI { dw += 2.0 * PI; }
            w_hist.push((m.t, p + dw, e_osc));
            *w_prev = Some(p + dw);
        } else { *w_prev = Some(w); }
        w
    };
    let _ = observe(&m, j0, &mut w_prev, &mut w_hist, &mut j_hist, &mut j_max);
    // integrate
    let mut next_out = 2.0 * PI;
    loop {
        if m.t >= sc.t_end - 1e-9 || m.escaped { break; }
        // step until next output
        while m.t < next_out - 1e-12 && !m.escaped {
            // step size fixed; allow last partial? keep exact grid: outputs at multiples of 2pi
            let remain = next_out - m.t;
            let mut hh = m.h;
            if remain < m.h - 1e-12 { hh = remain; }
            let saved_h = m.h;
            m.h = hh;
            let ok = ctx.step(&mut m, scheme);
            m.h = saved_h;
            if !ok {
                m.escaped = true;
                m.esc_epoch = Some(m.t);
                break;
            }
            let (a, e) = elems(m.r, m.v, sc.mu_p);
            if m.r.norm() > 2.0 * (sc.mu_p / 3.0f64).powf(1.0 / 3.0) {
                m.escaped = true;
                m.esc_epoch = Some(m.t);
                break;
            }
        }
        if m.escaped { break; }
        // output epoch: apply corrector, observe, un-apply
        if scheme == "dkd3" || scheme == "dkd5" {
            let order = if scheme == "dkd3" { 3 } else { 5 };
            let mut mc = m.clone();
            let k1 = ctx.corrector(&mut mc, order, 1.0);
            let _ = observe(&mc, j0, &mut w_prev, &mut w_hist, &mut j_hist, &mut j_max);
            // un-apply on a copy to keep mapping state; kicks counted for both
            let mut mu_ = mc.clone();
            let _ = ctx.corrector(&mut mu_, order, -1.0);
            m.kicks += (k1 as u64) * 2;
        } else {
            let _ = observe(&m, j0, &mut w_prev, &mut w_hist, &mut j_hist, &mut j_max);
        }
        if collect_trace { outs.push(format!("{:.4},{:e}", m.t, j_max)); }
        last_out += 1;
        next_out += 2.0 * PI;
        if next_out > sc.t_end + 1e-9 { break; }
    }
    // final: corrector for schemes, and final elements
    let (fa, fe) = elems(m.r, m.v, sc.mu_p);
    // Jacobi envelope slope: fit log(dj) vs log(orbit) using points above floor
    let mut j_slope = 0.0f64;
    if sc.mu2 == 0.0 && j_hist.len() > 5 {
        let mut pts: Vec<(f64, f64)> = j_hist.iter().filter(|(_, d)| *d > 1e-14).cloned().collect();
        pts.retain(|(t, _)| *t > 0.0);
        if pts.len() > 5 {
            let n = pts.len() as f64;
            let sx: f64 = pts.iter().map(|(t, _)| t.ln()).sum();
            let sy: f64 = pts.iter().map(|(_, d)| d.ln()).sum();
            let sxx: f64 = pts.iter().map(|(t, _)| t.ln() * t.ln()).sum();
            let sxy: f64 = pts.iter().map(|(t, d)| t.ln() * d.ln()).sum();
            j_slope = (n * sxy - sx * sy) / (n * sxx - sx * sx);
        }
    }
    // apsidal rate: LSQ slope of w vs moon-orbit count, reported per moon orbit
    let mut prec = f64::NAN;
    // robust fit: mask e_osc < 0.01 (apse undefined), then drop >3-sigma outliers twice
    let mut pts: Vec<(f64, f64)> = w_hist.iter().filter(|(_, _, e)| *e > 0.01).map(|(t, w, _)| (*t / p0, *w)).collect();
    for _ in 0..2 {
        if pts.len() < 6 { break; }
        let n = pts.len() as f64;
        let sx: f64 = pts.iter().map(|p| p.0).sum();
        let sy: f64 = pts.iter().map(|p| p.1).sum();
        let sxx: f64 = pts.iter().map(|p| p.0 * p.0).sum();
        let sxy: f64 = pts.iter().map(|p| p.0 * p.1).sum();
        let sl = (n * sxy - sx * sy) / (n * sxx - sx * sx);
        let ic = (sy - sl * sx) / n;
        let res: Vec<f64> = pts.iter().map(|p| p.1 - (sl * p.0 + ic)).collect();
        let sig = res.iter().map(|r| r * r).sum::<f64>() / n;
        let sig = sig.sqrt();
        pts = pts.iter().zip(res.iter()).filter(|(_, r)| r.abs() < 3.0 * sig).map(|(p, _)| *p).collect();
    }
    if pts.len() > 5 {
        let n = pts.len() as f64;
        let sx: f64 = pts.iter().map(|p| p.0).sum();
        let sy: f64 = pts.iter().map(|p| p.1).sum();
        let sxx: f64 = pts.iter().map(|p| p.0 * p.0).sum();
        let sxy: f64 = pts.iter().map(|p| p.0 * p.1).sum();
        prec = (n * sxy - sx * sy) / (n * sxx - sx * sx);
    }
    RunResult {
        r_fin: m.r, j_max, j_slope, prec, bound: !m.escaped, kicks: m.kicks,
        escaped_at: m.esc_epoch, final_a: fa, final_e: fe, valid: true,
    }
}

fn circ_birth(f: f64, sc: &Scene, e0: f64, retro: bool, phase: f64) -> (V3, V3) {
    let rh = (sc.mu_p / 3.0f64).powf(1.0 / 3.0);
    let a = f * rh;
    // periapsis at phase, coplanar
    let (c, s) = (phase.cos(), phase.sin());
    let r = V3::new(a * (1.0 - e0) * c, a * (1.0 - e0) * s, 0.0);
    let vc = (sc.mu_p / a).sqrt();
    // periapsis velocity direction for the given sense
    let dir = if retro { V3::new(s, -c, 0.0) } else { V3::new(-s, c, 0.0) };
    // vis-viva speed at r = a(1-e)
    let v = (sc.mu_p * (2.0 / (a * (1.0 - e0)) - 1.0 / a)).sqrt();
    (r, dir.scale(v))
}

fn main() {
    let sc_s1 = Scene { name: "s1", mu_p: 1e-3, mu2: 0.0, a2: 0.0, e2: 0.0, varpi2: 0.0, m20: 0.0, t_end: 100.0 * PI };
    // close-pass scene: pick m20 deterministically for min sep closest to 0.065 AU
    let mut best = (0.0f64, 1e9f64);
    let mut mm = 0.0f64;
    while mm < 2.0 * PI {
        let sc_t = Scene { name: "t", mu_p: 1e-3, mu2: 3e-4, a2: 1.0, e2: 0.26, varpi2: 2.4, m20: mm, t_end: 100.0 * PI };
        // min sep over 30 orbits
        let mut smin = 1e9f64;
        let mut t = 0.0;
        while t < 60.0 * PI {
            let d = planet2(t, &sc_t).sub(planet1(t)).norm();
            if d < smin { smin = d; }
            t += 0.05;
        }
        if (smin - 0.152).abs() < best.1 { best = (mm, (smin - 0.152).abs()); }
        mm += 0.005;
    }
    let sc_s3 = Scene { name: "s3", mu_p: 1e-3, mu2: 3e-4, a2: 1.0, e2: 0.26, varpi2: 2.4, m20: best.0, t_end: 60.0 * PI };

    // scenes: (label, scene, births)
    let mut jobs: Vec<(&str, Scene, Vec<(String, f64, f64, bool, f64)>)> = Vec::new();
    // tuning: circular prograde f sweep + two e0=0.1
    let mut s1: Vec<(String, f64, f64, bool, f64)> = Vec::new();
    // prograde stable only to ~0.49 r_H (CR3BP); retrograde to ~0.9 r_H
    for f in [0.2f64, 0.35, 0.45] {
        s1.push((format!("pro{}", f), f, 0.05, false, 0.7));
    }
    for f in [0.5f64, 0.7, 0.85] {
        s1.push((format!("ret{}", f), f, 0.05, true, 0.7));
    }
    s1.push((String::from("e10-0.4"), 0.4, 0.1, false, 0.7));
    jobs.push(("s1", sc_s1, s1));
    // held out
    let s2 = vec![
        (String::from("ho-e30-0.4"), 0.4f64, 0.3f64, false, 0.7),
        (String::from("ho-retro-0.6"), 0.6, 0.05, true, 0.7),
        (String::from("ho-e15-0.85"), 0.85, 0.15, false, 0.7),
    ];
    jobs.push(("s2", sc_s1, s2));
    let s3 = vec![(String::from("pass-0.4"), 0.4f64, 0.05f64, false, 0.7)];
    jobs.push(("s3", sc_s3, s3));

    let schemes: Vec<(&str, u32)> = vec![("dkd", 0), ("dkd3", 3), ("dkd5", 5), ("y4", 0), ("euler", 0)];
    let kpos: Vec<u64> = vec![2, 4, 8, 16, 32, 64];

    let out = std::fs::File::create("results.jsonl").unwrap();
    let mut w = std::io::BufWriter::new(out);
    for (scn, sc, births) in &jobs {
        for (scheme, order) in &schemes {
            for kpo in &kpos {
                for (label, f, e0, retro, phase) in births {
                    // reference: dkd at 512 (no corrector)
                    let (r0, v0) = circ_birth(*f, sc, *e0, *retro, *phase);
                    let res = run(scheme, *order, *kpo, sc, r0, v0, false);
                    writeln!(w, "{{\"scene\":\"{}\",\"scheme\":\"{}\",\"kpo\":{},\"moon\":\"{}\",\"rf\":[{:.9e},{:.9e},{:.9e}],\"j_max\":{:e},\"j_slope\":{:.4},\"prec\":{:.6e},\"bound\":{},\"kicks\":{},\"final_a\":{:.6},\"final_e\":{:.6}}}",
                        scn, scheme, kpo, label, res.r_fin.0[0], res.r_fin.0[1], res.r_fin.0[2], res.j_max, res.j_slope, res.prec, res.bound, res.kicks, res.final_a, res.final_e).unwrap();
                }
            }
        }
    }
    // references at 512 for every moon (and one at 2048 for convergence)
    for (scn, sc, births) in &jobs {
        for (label, f, e0, retro, phase) in births {
            let (r0, v0) = circ_birth(*f, sc, *e0, *retro, *phase);
            let r512 = run("dkd", 0, 512, sc, r0, v0, false);
            let r2048 = run("dkd", 0, 2048, sc, r0, v0, false);
            writeln!(w, "{{\"scene\":\"{}\",\"scheme\":\"ref512\",\"kpo\":512,\"moon\":\"{}\",\"rf\":[{:.9e},{:.9e},{:.9e}],\"j_max\":{:e},\"j_slope\":{:.4},\"prec\":{:.6e},\"bound\":{},\"kicks\":{},\"final_a\":{:.6},\"final_e\":{:.6}}}",
                scn, label, r512.r_fin.0[0], r512.r_fin.0[1], r512.r_fin.0[2], r512.j_max, r512.j_slope, r512.prec, r512.bound, r512.kicks, r512.final_a, r512.final_e).unwrap();
            writeln!(w, "{{\"scene\":\"{}\",\"scheme\":\"ref2048\",\"kpo\":2048,\"moon\":\"{}\",\"rf\":[{:.9e},{:.9e},{:.9e}],\"j_max\":{:e},\"j_slope\":{:.4},\"prec\":{:.6e},\"bound\":{},\"kicks\":{},\"final_a\":{:.6},\"final_e\":{:.6}}}",
                scn, label, r2048.r_fin.0[0], r2048.r_fin.0[1], r2048.r_fin.0[2], r2048.j_max, r2048.j_slope, r2048.prec, r2048.bound, r2048.kicks, r2048.final_a, r2048.final_e).unwrap();
        }
    }
    eprintln!("m20 chosen: {:.4} (target min sep 0.152)", best.0);
}
