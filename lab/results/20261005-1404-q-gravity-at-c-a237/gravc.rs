// Gravity at c: instantaneous vs naive-retarded vs "news", on the plane's own
// representation (drift = dominant-body Kepler tube; kicks = pairwise at cadence).
// Probe only (floats explore; behaviours decide). No deps. rustc -O gravc.rs.
use std::f64::consts::PI;

use std::time::Instant;

type V2 = (f64, f64);
#[inline] fn sub(a: V2, b: V2) -> V2 { (a.0 - b.0, a.1 - b.1) }
#[inline] fn add(a: V2, b: V2) -> V2 { (a.0 + b.0, a.1 + b.1) }
#[inline] fn sm(s: f64, a: V2) -> V2 { (s * a.0, s * a.1) }
#[inline] fn dot(a: V2, b: V2) -> f64 { a.0 * b.0 + a.1 * b.1 }
#[inline] fn norm(a: V2) -> f64 { (a.0 * a.0 + a.1 * a.1).sqrt() }
#[inline] fn rot(w: f64, a: V2) -> V2 { (w.cos() * a.0 - w.sin() * a.1, w.sin() * a.0 + w.cos() * a.1) }

// ---------- Kepler tube (compiled once per version) ----------
#[derive(Clone, Copy)]
struct Elements { a: f64, e: f64, w: f64, m0: f64, n: f64, hyp: bool, sgn: f64 }

fn wrap(m: f64) -> f64 { let mut x = m % (2.0 * PI); if x < 0.0 { x += 2.0 * PI; } if x > PI { x -= 2.0 * PI; } x }

fn elements(rel: V2, vrel: V2, mu: f64) -> Elements {
    // retrograde relative orbits (h < 0) are mirrored to prograde and mirrored back
    let hz = rel.0 * vrel.1 - rel.1 * vrel.0;
    let sgn = if hz < 0.0 { -1.0 } else { 1.0 };
    let rel = (rel.0, sgn * rel.1);
    let vrel = (vrel.0, sgn * vrel.1);
    let r = norm(rel); let v2 = dot(vrel, vrel); let rv = dot(rel, vrel);
    let a = 1.0 / (2.0 / r - v2 / mu);
    let k = (v2 - mu / r) / mu;
    let (ex, ey) = (k * rel.0 - rv / mu * vrel.0, k * rel.1 - rv / mu * vrel.1);
    let e = (ex * ex + ey * ey).sqrt();
    let w = if e < 1e-12 { 0.0 } else { ey.atan2(ex) };
    // true anomaly -> (eccentric | hyperbolic) anomaly: conditioned for all e, incl. e~0
    let nu0 = rel.1.atan2(rel.0) - w;
    let (sn, cn) = (nu0.sin(), nu0.cos());
    if a > 0.0 {
        let n = (mu / (a * a * a)).sqrt();
        let ea0 = ((1.0 - e * e).sqrt() * sn).atan2(e + cn);
        Elements { a, e, w, m0: wrap(ea0 - e * ea0.sin()), n, hyp: false, sgn }
    } else {
        let ah = -a;
        let n = (mu / (ah * ah * ah)).sqrt();
        let h0 = ((e * e - 1.0).sqrt() * sn / (1.0 + e * cn)).asinh();
        Elements { a, e, w, m0: e * h0.sinh() - h0, n, hyp: true, sgn }
    }
}

/// Position on the tube dt after the version epoch (relative to the dominant body).
fn tube_pos(el: &Elements, dt: f64) -> V2 {
    if el.hyp {
        let ah = -el.a;
        let m = el.m0 + el.n * dt;
        let mut hh = (2.0 * m.abs() / el.e + 1.85).ln();
        if m < 0.0 { hh = -hh; }
        for _ in 0..40 {
            let f = el.e * hh.sinh() - hh - m;
            let d = f / (el.e * hh.cosh() - 1.0); hh -= d;
            if d.abs() < 1e-14 { break; }
        }
        let p = rot(el.w, (ah * (el.e - hh.cosh()), ah * (el.e * el.e - 1.0).sqrt() * hh.sinh()));
        (p.0, el.sgn * p.1)
    } else {
        let m = wrap(el.m0 + el.n * dt);
        let mut ea = if el.e < 0.8 { m + el.e * m.sin() } else { PI };
        for _ in 0..24 {
            let f = ea - el.e * ea.sin() - m;
            let d = f / (1.0 - el.e * ea.cos()); ea -= d;
            if d.abs() < 1e-14 { break; }
        }
        let p = rot(el.w, (el.a * (ea.cos() - el.e), el.a * (1.0 - el.e * el.e).sqrt() * ea.sin()));
        (p.0, el.sgn * p.1)
    }
}

// ---------- bodies, versions, simulator ----------
#[derive(Clone)]
struct Body { m: f64, x: V2, v: V2, a: V2, dom: i32, mutual: bool }
#[derive(Clone, Copy)]
struct Ver { t: f64, x: V2, v: V2, a: V2, el: Elements }

#[derive(Clone, Copy, PartialEq)]
enum Cfg { Inst, Ret, News, NewsLin }

struct Sim {
    cfg: Cfg, c: f64, g: f64,
    b: Vec<Body>,
    hist: Vec<Vec<Ver>>,
    n_kepler: u64, n_bisect: u64,
}

impl Sim {
    fn new(cfg: Cfg, c: f64, mut b: Vec<Body>) -> Sim {
        // zero total momentum (star takes the balance)
        let n = b.len();
        let mut p = (0.0, 0.0); let mut mt = 0.0;
        for bi in &b { p = add(p, sm(bi.m, bi.v)); mt += bi.m; }
        b[0].v = add(b[0].v, sm(-1.0 / mt, p));
        let mut s = Sim { cfg, c, g: 1.0, b, hist: vec![Vec::new(); n], n_kepler: 0, n_bisect: 0 };
        let acc = s.accel_now();
        for i in 0..n { s.b[i].a = acc[i]; }
        s.record(0.0);
        s
    }
    fn record(&mut self, t: f64) {
        for i in 0..self.b.len() {
            let (rel, vrel, mu) = if self.b[i].dom >= 0 {
                let d = self.b[i].dom as usize;
                (sub(self.b[i].x, self.b[d].x), sub(self.b[i].v, self.b[d].v),
                 self.g * (self.b[i].m + self.b[d].m))
            } else { (self.b[i].x, self.b[i].v, self.g * self.b[i].m) };
            let el = elements(rel, vrel, mu);
            self.hist[i].push(Ver { t, x: self.b[i].x, v: self.b[i].v, a: self.b[i].a, el });
        }
    }
    /// instantaneous pairwise accelerations from the current state (no history needed)
    fn accel_now(&self) -> Vec<V2> {
        let n = self.b.len();
        let mut acc = vec![(0.0f64, 0.0f64); n];
        for bi in 0..n { for si in 0..n { if si == bi { continue; }
            let d = sub(self.b[si].x, self.b[bi].x); let r = norm(d);
            acc[bi] = add(acc[bi], sm(self.g * self.b[si].m / (r * r * r), d)); } }
        acc
    }
    fn accel(&mut self, t: f64) -> Vec<V2> {
        let n = self.b.len();
        let mut acc = vec![(0.0f64, 0.0f64); n];
        for bi in 0..n { for si in 0..n { if si == bi { continue; }
            let ab = self.pair_accel(bi, si, t); acc[bi] = add(acc[bi], ab); } }
        acc
    }
    fn accel_from(&mut self, bi: usize, si: usize, t: f64) -> V2 { self.pair_accel(bi, si, t) }
    fn pair_accel(&mut self, bi: usize, si: usize, t: f64) -> V2 {
        let gm = self.g * self.b[si].m;
        let xb = self.b[bi].x;
        let pos = match self.cfg {
            Cfg::Inst => self.b[si].x,
            _ => {
                let mut tr = t - norm(sub(self.b[si].x, xb)) / self.c;
                let mut ps = self.pos_known(bi, si, tr, tr);
                for _ in 0..3 {
                    tr = t - norm(sub(ps, xb)) / self.c;
                    ps = self.pos_known(bi, si, tr, tr);
                }
                match self.cfg {
                    Cfg::Ret => ps,
                    Cfg::News => self.pos_known(bi, si, tr, t),
                    _ => {
                        let v = self.ver_at(si, tr);
                        let dt = t - v.t;
                        add(v.x, add(sm(dt, v.v), sm(0.5 * dt * dt, v.a)))
                    }
                }
            }
        };
        let d = sub(pos, xb); let r = norm(d);
        if std::env::var("DBGF").is_ok() && bi == 0 && si == 1 && self.hist[1].len() < 60 {
            let di = sub(self.b[si].x, xb); let ri = norm(di);
            let fi = sm(gm / (ri * ri * ri), di);
            let f = sm(gm / (r * r * r), d);
            eprintln!("F t~step{} pos=({:.5},{:.5}) true=({:.5},{:.5}) |f_n|={:.5} |f_i|={:.5} dir_err={:.3e}",
                self.hist[1].len(), pos.0, pos.1, self.b[si].x.0, self.b[si].x.1,
                norm(f), norm(fi), norm(sub(f, fi)));
        }
        sm(gm / (r * r * r), d)
    }
    fn ver_at(&mut self, s: usize, t_ret: f64) -> Ver {
        let h = &self.hist[s];
        self.n_bisect += 1;
        let mut lo = 0usize; let mut hi = h.len();
        while lo + 1 < hi { let mid = (lo + hi) / 2; if h[mid].t <= t_ret { lo = mid } else { hi = mid } }
        h[lo]
    }
    /// consumer bi's view of body s at t_eval: the tube version its past light cone
    /// (at t_ret) last saw, evaluated at t_eval.
    fn pos_known(&mut self, bi: usize, s: usize, t_ret: f64, t_eval: f64) -> V2 {
        let v = self.ver_at(s, t_ret);
        let dt = t_eval - v.t;
        let dom = self.b[s].dom;
        if dom < 0 {
            return add(v.x, add(sm(dt, v.v), sm(0.5 * dt * dt, v.a)));
        }
        let d = dom as usize;
        if self.b[s].mutual {
            self.n_kepler += 1;
            let rel = tube_pos(&v.el, dt);
            let (ms, md) = (self.b[s].m, self.b[d].m); let mt = ms + md;
            let vd = self.ver_at(d, t_ret);
            let com0 = sm(1.0 / mt, add(sm(ms, v.x), sm(md, vd.x)));
            let vcom = sm(1.0 / mt, add(sm(ms, v.v), sm(md, vd.v)));
            return add(add(com0, sm(dt, vcom)), sm(md / mt, rel));
        }
        self.n_kepler += 1;
        add(self.pos_known(bi, d, t_ret, t_eval), tube_pos(&v.el, dt))
    }
    fn step(&mut self, t: f64, dt: f64) {
        let n = self.b.len();
        let acc = self.accel(t);
        for i in 0..n { self.b[i].v = add(self.b[i].v, sm(0.5 * dt, acc[i])); }
        for i in 0..n { self.b[i].x = add(self.b[i].x, sm(dt, self.b[i].v)); }
        let acc2 = self.accel(t + dt);
        for i in 0..n {
            self.b[i].a = acc2[i];
            self.b[i].v = add(self.b[i].v, sm(0.5 * dt, acc2[i]));
        }
        self.record(t + dt);
    }
    fn energy(&self) -> f64 {
        let mut e = 0.0; let n = self.b.len();
        for i in 0..n {
            e += 0.5 * self.b[i].m * dot(self.b[i].v, self.b[i].v);
            for j in (i + 1)..n { e -= self.g * self.b[i].m * self.b[j].m / norm(sub(self.b[j].x, self.b[i].x)); }
        }
        e
    }
}

fn osc_a(rel: V2, vrel: V2, mu: f64) -> f64 {
    let r = norm(rel); let v2 = dot(vrel, vrel);
    1.0 / (2.0 / r - v2 / mu)
}
fn osc_e(rel: V2, vrel: V2, mu: f64) -> f64 {
    let r = norm(rel); let v2 = dot(vrel, vrel); let rv = dot(rel, vrel);
    let k = (v2 - mu / r) / mu;
    let (ex, ey) = (k * rel.0 - rv / mu * vrel.0, k * rel.1 - rv / mu * vrel.1);
    (ex * ex + ey * ey).sqrt()
}

struct Out { s: String }
impl Out {
    fn new() -> Out { Out { s: String::new() } }
    fn k(&mut self, key: &str, v: String) { self.s.push_str(&format!("\"{}\":{},", key, v)); }
    fn kf(&mut self, key: &str, v: f64) { self.k(key, format!("{:.6e}", v)); }
    fn ki(&mut self, key: &str, v: i64) { self.k(key, format!("{}", v)); }
    fn arr(&mut self, key: &str, v: &[f64]) {
        self.s.push_str(&format!("\"{}\":[", key));
        for (i, x) in v.iter().enumerate() { if i > 0 { self.s.push(','); } self.s.push_str(&format!("{:.6e}", x)); }
        self.s.push_str("],");
    }
    fn str(mut self, path: &str) {
        if self.s.ends_with(',') { self.s.pop(); }
        self.s = format!("{{{}}}", self.s);
        std::fs::write(path, self.s).unwrap();
    }
}

struct Peri { prev_r: f64, prev_rr: f64, armed: bool, angs: Vec<f64>, smas: Vec<f64> }
impl Peri { fn new() -> Peri { Peri { prev_r: 0.0, prev_rr: 0.0, armed: false, angs: Vec::new(), smas: Vec::new() } } }
fn track_peri(p: &mut Peri, rel: V2, vrel: V2, mu: f64) {
    let r = norm(rel); let rr = r - p.prev_r;
    if p.armed && p.prev_rr < 0.0 && rr >= 0.0 {
        p.angs.push(rel.1.atan2(rel.0)); p.smas.push(osc_a(rel, vrel, mu));
    }
    p.prev_r = r; p.prev_rr = rr; p.armed = true;
}
fn prec_list(p: &Peri) -> Vec<f64> {
    let mut out = Vec::new();
    for w in p.angs.windows(2) {
        let mut d = w[1] - w[0];
        while d > PI { d -= 2.0 * PI; } while d < -PI { d += 2.0 * PI; }
        out.push(d);
    }
    out
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let scene = args[1].clone();
    let cfg = match args[2].as_str() { "inst" => Cfg::Inst, "ret" => Cfg::Ret, "news" => Cfg::News, "newslin" => Cfg::NewsLin, _ => panic!("cfg") };
    let c: f64 = args[3].parse().unwrap();
    let dt: f64 = args[4].parse().unwrap();
    let dur: f64 = args[5].parse().unwrap();
    let outpath = args[6].clone();
    let t0w = Instant::now();
    let mut o = Out::new();
    o.k("scene", format!("\"{}\"", scene));
    o.k("cfg", format!("\"{}\"", args[2]));
    o.kf("c", c); o.kf("dt", dt); o.kf("dur", dur);

    match scene.as_str() {
        // ============ binary (Laplace's argument) ============
        "binary" | "binary_e3" => {
            let e0: f64 = if scene == "binary_e3" { 0.3 } else { 0.0 };
            let r0: f64 = 1.0;
            let vrel0 = ((1.0 + e0) * 1.0 / r0).sqrt();
            let b = vec![
                Body { m: 0.5, x: (0.5 * r0, 0.0), v: (0.0, -0.5 * vrel0), a: (0.0, 0.0), dom: 1, mutual: true },
                Body { m: 0.5, x: (-0.5 * r0, 0.0), v: (0.0, 0.5 * vrel0), a: (0.0, 0.0), dom: 0, mutual: true },
            ];
            let mut sim = Sim::new(cfg, c, b);
            let e_start = sim.energy();
            let mut per = Peri::new();
            let mut ts = Vec::new(); let mut es = Vec::new(); let mut asamp = Vec::new();
            let nst = (dur / dt) as usize;
            let mut unbound_at = -1.0;
            for k in 0..nst {
                let t = k as f64 * dt;
                if std::env::var("DBGPK").is_ok() && k < 120 && k % 20 == 0 {
                    let tr0 = t - norm(sub(sim.b[1].x, sim.b[0].x)) / c;
                    let pk = sim.pos_known(0, 1, tr0, t);
                    let ver = sim.ver_at(1, tr0);
                    let (tp0, tpn) = (tube_pos(&ver.el, 0.0), tube_pos(&ver.el, t - ver.t));
                    eprintln!("   el: a={:.4} e={:.2e} m0={:.4} n={:.4} | ang(tube,0)={:.4} ang(tube,dt)={:.4}",
                        ver.el.a, ver.el.e, ver.el.m0, ver.el.n, rel_angle(tp0), rel_angle(tpn));
                    eprintln!("k={} t={:.3} tr0={:.4} ver_t={:.4} tube_dt={:.4} lag={:.4}",
                        k, t, tr0, ver.t, t - ver.t, (rel_angle(sub(sim.b[1].x, sim.b[0].x)) - rel_angle(sub(pk, sim.b[0].x))).abs());
                    eprintln!("k={} t={:.3} true1=({:.5},{:.5}) news1=({:.5},{:.5}) d={:.2e}",
                        k, t, sim.b[1].x.0, sim.b[1].x.1, pk.0, pk.1, norm(sub(pk, sim.b[1].x)));
                }
                let rel = sub(sim.b[1].x, sim.b[0].x); let vr = sub(sim.b[1].v, sim.b[0].v);
                track_peri(&mut per, rel, vr, 1.0);
                let a = osc_a(rel, vr, 1.0);
                if unbound_at < 0.0 && (a < 0.0 || a > 4.0) { unbound_at = t; }
                if k % (nst / 500).max(1) == 0 {
                    ts.push(t); es.push((sim.energy() - e_start) / e_start.abs()); asamp.push(a);
                }
                sim.step(t, dt);
            }
            let prec = prec_list(&per);
            o.ki("n_orbits", per.angs.len() as i64);
            o.kf("a_final", asamp[asamp.len() - 1]);
            o.kf("unbound_at", unbound_at);
            o.kf("max_dE_rel", es.iter().fold(0.0f64, |m, x| m.max(x.abs())));
            o.arr("per_orbit_dphi", &prec);
            o.kf("mean_prec_per_orbit", if prec.is_empty() { f64::NAN } else { prec.iter().sum::<f64>() / prec.len() as f64 });
            o.arr("t_samples", &ts); o.arr("dE_samples", &es); o.arr("a_samples", &asamp);
            o.ki("n_kepler", sim.n_kepler as i64);
        }
        // ============ star + planets + moons ============
        "system" | "sysmin" => {
            let mp: f64 = 3.0e-4;
            let r_h = (mp / 3.0).powf(1.0 / 3.0);
            let rm: f64 = 0.30 * r_h;
            let (pa, va) = ((1.0, 0.0), (0.0, 1.0));
            let vm_p: f64 = (mp / rm).sqrt();
            let mut b = vec![
                Body { m: 1.0, x: (0.0, 0.0), v: (0.0, 0.0), a: (0.0, 0.0), dom: -1, mutual: false },
                Body { m: mp, x: pa, v: va, a: (0.0, 0.0), dom: 0, mutual: false },
                Body { m: 1.0e-7, x: (1.0 + rm, 0.0), v: (0.0, 1.0 + vm_p), a: (0.0, 0.0), dom: 1, mutual: false },
            ];
            let minimal = scene == "sysmin";
            let (mb, rbp): (f64, f64) = (1.0e-4, 2.2 * 0.9);
            let vbp: f64 = ((1.0 / rbp) * (2.0 / rbp - 1.0 / 2.2)).sqrt();
            b.push(Body { m: mb, x: (rbp, 0.0), v: (0.0, vbp), a: (0.0, 0.0), dom: 0, mutual: false });
            let rcp: f64 = 4.5 * 0.95; let vcp = ((1.0 / rcp) * (2.0 / rcp - 1.0 / 4.5)).sqrt();
            let s2 = 0.5f64.sqrt();
            let mc: f64 = 0.0;
            b.push(Body { m: mc, x: (rcp * s2, rcp * s2), v: (-vcp * s2, vcp * s2), a: (0.0, 0.0), dom: 0, mutual: false });
            let mut sim = Sim::new(cfg, c, b);
            let e_start = sim.energy();
            let mut per_b = Peri::new();
            let mut ts = Vec::new(); let mut js = Vec::new(); let mut es = Vec::new(); let mut as_m = Vec::new();
            let nst = (dur / dt) as usize;
            let mut moon_escaped_at = -1.0;
            let mut j0 = 0.0f64;
            for k in 0..nst {
                let t = k as f64 * dt;
                let (xs, vs) = (sim.b[0].x, sim.b[0].v);
                let (xp, vp) = (sim.b[1].x, sim.b[1].v);
                let (xm, vm) = (sim.b[2].x, sim.b[2].v);
                let dx = sub(xp, xs); let d = norm(dx);
                let er = sm(1.0 / d, dx); let et = (-er.1, er.0);
                let n = norm(sub(vp, vs)) / d;
                let rrel = sub(xm, xs);
                let (xr, yr) = (dot(rrel, er), dot(rrel, et));
                let vrel = sub(vm, vs);
                let (vxr, vyr) = (dot(vrel, er) + n * yr, dot(vrel, et) - n * xr);
                let (r1, r2) = (norm(sub(xm, xs)), norm(sub(xm, xp)));
                let j = 2.0 * (1.0 / r1 + mp / r2) + n * n * (xr * xr + yr * yr) - (vxr * vxr + vyr * vyr);
                if k == 0 { j0 = j; }
                let am = osc_a(sub(xm, xp), sub(vm, vp), mp);
                if moon_escaped_at < 0.0 && (am < 0.0 || norm(sub(xm, xp)) > 5.0 * r_h) { moon_escaped_at = t; }
                track_peri(&mut per_b, sub(sim.b[3].x, sim.b[0].x), sub(sim.b[3].v, sim.b[0].v), 1.0);
                if k % (nst / 400).max(1) == 0 {
                    ts.push(t); js.push((j - j0) / j0.abs()); es.push((sim.energy() - e_start) / e_start.abs()); as_m.push(am / rm);
                }
                sim.step(t, dt);
            }
            let prec = prec_list(&per_b);
            o.arr("t_samples", &ts); o.arr("J_samples", &js); o.arr("dE_samples", &es); o.arr("moon_a_samples", &as_m);
            o.kf("moon_escaped_at", moon_escaped_at);
            o.kf("max_dE_rel", es.iter().fold(0.0f64, |m, x| m.max(x.abs())));
            o.kf("max_J_err", js.iter().fold(0.0f64, |m, x| m.max(x.abs())));
            o.arr("per_orbit_dphi", &prec);
            o.kf("mean_prec_per_orbit", if prec.is_empty() { f64::NAN } else { prec.iter().sum::<f64>() / prec.len() as f64 });
            o.ki("n_orbits_B", per_b.angs.len() as i64);
            o.ki("n_kepler", sim.n_kepler as i64);
            o.kf("ver_bytes", std::mem::size_of::<Ver>() as f64);
            o.kf("versions_needed", ((9.0 / c) / dt).ceil());
            o.ki("hist_len_star", sim.hist[0].len() as i64);
        }
        // ============ ship crossing a Hill sphere ============
        "flyby" => {
            let mp: f64 = 3.0e-4;
            let r_h = (mp / 3.0).powf(1.0 / 3.0);
            let nseed = 16i64;
            let mut vout_all = Vec::new();
            let mut dv_scatter = Vec::new();
            let mut jmax_all = Vec::new();
            let mut qmin_all = Vec::new();
            for seed in 0..nseed {
                let mut z = (seed as u64).wrapping_mul(0x9E3779B97F4A7C15).wrapping_add(1442695040888963407);
                let rnd = |z: &mut u64| -> f64 { *z = z.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407); ((*z >> 11) as f64) / (1u64 << 53) as f64 };
                let alpha = rnd(&mut z) * 2.0 * PI;          // approach direction in sky
                let vinf = (2.2 + 0.6 * rnd(&mut z)) * (mp / r_h).sqrt();
                let bimp = (0.35 + 0.75 * rnd(&mut z)) * r_h * if rnd(&mut z) < 0.5 { -1.0 } else { 1.0 };
                let u = (alpha.cos(), alpha.sin());
                let up = (-u.1, u.0);
                let b = vec![
                    Body { m: 1.0, x: (0.0, 0.0), v: (0.0, 0.0), a: (0.0, 0.0), dom: -1, mutual: false },
                    Body { m: mp, x: (1.0, 0.0), v: (0.0, 1.0), a: (0.0, 0.0), dom: 0, mutual: false },
                    Body { m: 1.0e-12, x: add(add((1.0, 0.0), sm(-1.5 * r_h, u)), sm(bimp, up)),
                           v: add((0.0, 1.0), sm(vinf, u)), a: (0.0, 0.0), dom: 0, mutual: false },
                ];
                let mut sim = Sim::new(cfg, c, b);
                let mut j0 = 0.0; let mut jmax_s = 0.0f64; let mut qmin = f64::INFINITY;
                let mut vout = (f64::NAN, f64::NAN);
                let nst = (dur / dt) as usize;
                let mut got_out = false;
                for k in 0..nst {
                    let t = k as f64 * dt;
                    let (xs, vs) = (sim.b[0].x, sim.b[0].v);
                    let (xp, vp) = (sim.b[1].x, sim.b[1].v);
                    let (xm, vm) = (sim.b[2].x, sim.b[2].v);
                    let dx = sub(xp, xs); let d = norm(dx);
                    let er = sm(1.0 / d, dx); let et = (-er.1, er.0);
                    let n = norm(sub(vp, vs)) / d;
                    let rrel = sub(xm, xs);
                    let (xr, yr) = (dot(rrel, er), dot(rrel, et));
                    let vrel = sub(vm, vs);
                    let (vxr, vyr) = (dot(vrel, er) + n * yr, dot(vrel, et) - n * xr);
                    let (r1, r2) = (norm(sub(xm, xs)), norm(sub(xm, xp)));
                    let j = 2.0 * (1.0 / r1 + mp / r2) + n * n * (xr * xr + yr * yr) - (vxr * vxr + vyr * vyr);
                    if k == 0 { j0 = j; }
                    jmax_s = jmax_s.max(((j - j0) / j0.abs()).abs());
                    qmin = qmin.min(r2);
                    if !got_out && t > 0.5 && r2 > 1.6 * r_h {
                        vout = sub(sim.b[2].v, sim.b[1].v); got_out = true;
                    }
                    sim.step(t, dt);
                }
                if !got_out { vout = sub(sim.b[2].v, sim.b[1].v); }
                vout_all.push(vout.0); vout_all.push(vout.1);
                dv_scatter.push(norm(vout) - vinf);
                jmax_all.push(jmax_s);
                qmin_all.push(qmin);
            }
            o.arr("vout_xy", &vout_all);
            o.arr("dv_scatter", &dv_scatter);
            o.arr("jmax", &jmax_all);
            o.arr("qmin_over_rh", &qmin_all.iter().map(|x| x / r_h).collect::<Vec<_>>());
        }
        // ============ a source that is struck ============
        "thrust" => {
            let mp: f64 = 3.0e-4;
            let dv = 0.06;
            let te = 8.0;
            struct RunOut { ts: Vec<f64>, aw: Vec<f64>, wtraj: Vec<V2>, a_at_te: V2 }
            let run = |impulse: bool| -> RunOut {
                let b = vec![
                    Body { m: 1.0, x: (0.0, 0.0), v: (0.0, 0.0), a: (0.0, 0.0), dom: -1, mutual: false },
                    Body { m: mp, x: (1.0, 0.0), v: (0.0, 1.0), a: (0.0, 0.0), dom: 0, mutual: false },
                    Body { m: 1.0e-9, x: (6.0 * 1.1f64.cos(), 6.0 * 1.1f64.sin()),
                           v: (-(1.0f64 / 6.0).sqrt() * 1.1f64.sin(), (1.0f64 / 6.0).sqrt() * 1.1f64.cos()),
                           a: (0.0, 0.0), dom: 0, mutual: false },
                ];
                let mut sim = Sim::new(cfg, c, b);
                let mut ts = Vec::new(); let mut aw = Vec::new(); let mut wtraj = Vec::new();
                let mut a_at_te = (f64::NAN, f64::NAN);
                let nst = (dur / dt) as usize;
                let mut applied = false;
                for k in 0..nst {
                    let t = k as f64 * dt;
                    if impulse && !applied && t >= te {
                        let u = sm(1.0 / norm(sim.b[1].x), sim.b[1].x);
                        let tang = (-u.1, u.0);
                        sim.b[1].v = add(sim.b[1].v, sm(dv, tang));
                        let acc = sim.accel(t);
                        for i in 0..sim.b.len() { sim.b[i].a = acc[i]; }
                        sim.record(t);
                        applied = true;
                        a_at_te = sim.b[1].x;
                    }
                    ts.push(t);
                    aw.push(norm(sim.accel_from(2, 1, t)));
                    wtraj.push(sim.b[2].x);
                    sim.step(t, dt);
                }
                RunOut { ts, aw, wtraj, a_at_te }
            };
            let kicked = run(true);
            let free = run(false);
            let res: Vec<f64> = kicked.ts.iter().enumerate().map(|(i, _)| kicked.aw[i] - free.aw[i]).collect();
            let jump = res.iter().rev().take(300).map(|x| x.abs()).fold(0.0f64, f64::max);
            let pre_noise = res.iter().zip(kicked.ts.iter()).filter(|(_, t)| **t < 7.9)
                .map(|(r, _)| r.abs()).fold(0.0f64, f64::max);
            let thr = (10.0 * pre_noise).max(0.001 * jump);
            let mut arrival = -1.0;
            for (i, r) in res.iter().enumerate() {
                if kicked.ts[i] > 7.95 && r.abs() > thr { arrival = kicked.ts[i]; break; }
            }
            o.kf("pre_noise", pre_noise);
            // exact light arrival: t = te + |x_w^free(t) - x_A(te)| / c
            let mut t_arr = te + norm(sub(free.wtraj[0], kicked.a_at_te)) / c;
            for _ in 0..30 {
                let idx = ((t_arr / dt) as usize).min(free.wtraj.len() - 1);
                let t_new = te + norm(sub(free.wtraj[idx], kicked.a_at_te)) / c;
                if (t_new - t_arr).abs() < dt * 1e-3 { t_arr = t_new; break; }
                t_arr = t_new;
            }
            o.arr("t_samples", &kicked.ts); o.arr("res_samples", &res);
            o.kf("arrival_t", arrival);
            o.kf("exact_light_arrival", t_arr);
            o.kf("jump", jump);
        }
        // ============ cost per kick ============
        "bench" => {
            let n = args[7].parse::<usize>().unwrap();
            let reps = args[8].parse::<usize>().unwrap();
            let mut b = vec![Body { m: 1.0, x: (0.0, 0.0), v: (0.0, 0.0), a: (0.0, 0.0), dom: -1, mutual: false }];
            let mut z = 42u64;
            let rnd = |z: &mut u64| -> f64 { *z = z.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407); ((*z >> 11) as f64) / (1u64 << 53) as f64 };
            for _ in 0..n {
                let r = 1.0 + 3.0 * rnd(&mut z); let ph = rnd(&mut z) * 2.0 * PI;
                let (x, v) = ((r * ph.cos(), r * ph.sin()), (-(1.0f64 / r).sqrt() * ph.sin(), (1.0f64 / r).sqrt() * ph.cos()));
                b.push(Body { m: 1e-6, x, v, a: (0.0, 0.0), dom: 0, mutual: false });
            }
            let mut sim = Sim::new(cfg, c, b);
            let nst = ((2.0 * PI / 8.0) / dt) as usize;
            let steps = nst.min(reps);
            let t0 = Instant::now();
            for k in 0..steps { sim.step(k as f64 * dt, dt); }
            let el = t0.elapsed().as_nanos() as f64;
            o.ki("n_bodies", n as i64);
            o.kf("ns_per_pair_eval", el / (steps as f64 * (n * n) as f64));
            o.kf("ns_per_step", el / steps as f64);
            o.ki("n_kepler", sim.n_kepler as i64);
        }
        _ => panic!("unknown scene"),
    }
    o.kf("wall_s", t0w.elapsed().as_secs_f64());
    o.str(&outpath);
}
fn rel_angle(v: V2) -> f64 { v.1.atan2(v.0) }
