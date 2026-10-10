//! H_live probe: the rate at which a program-born belt accumulates distinguishing
//! information per body, under the law's own event structure: exact Kepler drift
//! (tubes), impulses at conjunctions (strong ones integrated exactly), elastic
//! contacts. Measures the empirical entropy of quantized (dE/E, dL/L, dpom/2pi,
//! dlambda/2pi) offsets from the birth program, centered (the program absorbs the
//! shared secular drift). Exploratory floats; fixed seeds; single thread.
//!
//! Usage:
//!   hlive selftest
//!   hlive belt  <n> <mu_b> <rho_screen> <orbits> <seed> [width=0.01] [sigma_e=0.05]
//!   hlive lane  <n> <mu_f> <rho_screen> <orbits> <seed> [r_contact=0.001] [sigma_e=0.02]
//!   hlive kernel

use std::cmp::Reverse;
use std::collections::BinaryHeap;

const TAU: f64 = std::f64::consts::TAU;
const TICKS: f64 = 4294967296.0;

// ---------- rng (same generator as crates/encounters) ----------
pub struct Rng(pub u64);
impl Rng {
    fn next_u64(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }
    fn f64(&mut self) -> f64 {
        (self.next_u64() >> 11) as f64 / 9_007_199_254_740_992.0
    }
}

// ---------- body: one tube ----------
#[derive(Clone, Copy, Debug)]
struct Body {
    a: f64,
    e: f64,
    pom: f64,
    /// period in ticks (2^32 per time unit), integer by construction
    period: u64,
    /// periapsis time in ticks, in [0, period)
    tp: u64,
}

impl Body {
    fn with_period(period: u64, e: f64, pom: f64, lam0: f64) -> Self {
        let a = (TAU * TICKS / period as f64).powf(-2.0 / 3.0);
        let pom = pom.rem_euclid(TAU);
        let m0 = (lam0 - pom).rem_euclid(TAU);
        let tpf = (-(m0 / TAU) * period as f64).rem_euclid(period as f64);
        let tp = (tpf.round() as u64) % period;
        Body { a, e, pom, period, tp }
    }
    fn new(a0: f64, e: f64, pom: f64, lam0: f64) -> Self {
        let period = (TAU * a0.powf(1.5) * TICKS).round() as u64;
        Body::with_period(period, e, pom, lam0)
    }
    #[inline]
    fn nn(&self) -> f64 {
        TAU * TICKS / self.period as f64
    }
    #[inline]
    fn mean_anom(&self, t: f64) -> f64 {
        let x = (t * TICKS - self.tp as f64) / self.period as f64;
        TAU * (x - x.floor())
    }
    fn ecc(&self, m: f64) -> f64 {
        let e = self.e;
        if e < 1e-9 {
            return m;
        }
        let mut ea = m + e * m.cos();
        for _ in 0..10 {
            let f = ea - e * ea.sin() - m;
            let fp = 1.0 - e * ea.cos();
            let d = f / fp;
            ea -= d;
            if d.abs() < 1e-13 {
                break;
            }
        }
        ea
    }
    /// [x, y, vx, vy] at time t (time units).
    fn state(&self, t: f64) -> [f64; 4] {
        let m = self.mean_anom(t);
        let ea = self.ecc(m);
        let (a, e) = (self.a, self.e);
        let s = (1.0 - e * e).sqrt();
        let xp = a * (ea.cos() - e);
        let yp = a * s * ea.sin();
        let n = 1.0 / a.powf(1.5);
        let den = 1.0 - e * ea.cos();
        let vxp = -a * n * ea.sin() / den;
        let vyp = a * s * n * ea.cos() / den;
        let (cp, sp) = (self.pom.cos(), self.pom.sin());
        [xp * cp - yp * sp, xp * sp + yp * cp, vxp * cp - vyp * sp, vxp * sp + vyp * cp]
    }
    fn lambda(&self, t: f64) -> f64 {
        let m = self.mean_anom(t);
        let ea = self.ecc(m);
        let e = self.e;
        self.pom + ((1.0 - e * e).sqrt() * ea.sin()).atan2(ea.cos() - e)
    }
    fn from_state(t: f64, x: f64, y: f64, vx: f64, vy: f64) -> Body {
        let r = (x * x + y * y).sqrt();
        let v2 = vx * vx + vy * vy;
        let a = -1.0 / (v2 - 2.0 / r);
        let rv = x * vx + y * vy;
        let c = v2 - 1.0 / r;
        let (ex, ey) = (c * x - rv * vx, c * y - rv * vy);
        let e = (ex * ex + ey * ey).sqrt();
        let pom = if e < 1e-12 { 0.0 } else { ey.atan2(ex) };
        let period_f = TAU * a.powf(1.5) * TICKS;
        let period = period_f.round().max(1.0) as u64;
        // mean anomaly at t
        let m = if e < 1e-12 {
            ((x * vy - y * vx).atan2(x) - pom).rem_euclid(TAU)
        } else {
            let cos_e = ((1.0 - r / a) / e).clamp(-1.0, 1.0);
            let sin_e = (rv / (e * a.sqrt())).clamp(-1.0, 1.0);
            let ea = sin_e.atan2(cos_e);
            (ea - e * ea.sin()).rem_euclid(TAU)
        };
        let tpf = (t * TICKS - m / TAU * period as f64).rem_euclid(period as f64);
        Body { a, e, pom: pom.rem_euclid(TAU), period, tp: tpf.round() as u64 % period }
    }
}

fn wrap_pi(x: f64) -> f64 {
    let m = x.rem_euclid(TAU);
    if m > std::f64::consts::PI {
        m - TAU
    } else {
        m
    }
}

// ---------- pairs ----------
struct Pair {
    i: u32,
    j: u32,
    tnext: f64,
    ver: u64,
    active: bool,
    /// kick counters of (i, j) when this entry was scheduled
    ki: u64,
    kj: u64,
}

#[derive(Clone, Copy)]
struct Ev {
    t: f64,
    pair: u32,
    ver: u64,
}
impl PartialEq for Ev {
    fn eq(&self, o: &Self) -> bool {
        self.t == o.t
    }
}
impl Eq for Ev {}
impl PartialOrd for Ev {
    fn partial_cmp(&self, o: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(o))
    }
}
impl Ord for Ev {
    fn cmp(&self, o: &Self) -> std::cmp::Ordering {
        self.t.partial_cmp(&o.t).unwrap_or(std::cmp::Ordering::Equal)
    }
}

struct Sim {
    b: Vec<Body>,
    birth: Vec<Body>,
    m: Vec<f64>, // body masses (star = 1)
    pairs: Vec<Pair>,
    adj: Vec<Vec<u32>>,
    heap: BinaryHeap<Reverse<Ev>>,
    kicks: u64,
    contacts: u64,
    strong: u64,
    captures: u64,
    r_contact: f64,
    rho_screen: f64,
    kicks_per_body: Vec<u64>,
    // stats
    conj_tried: u64,
}

/// next conjunction of (i,j) strictly after t0: equal longitudes.
/// Returns (t, found-within-horizon).
use std::sync::atomic::{AtomicU64, Ordering};
static LAMC: AtomicU64 = AtomicU64::new(0);
static SCANC: AtomicU64 = AtomicU64::new(0);
static FALLC: AtomicU64 = AtomicU64::new(0);
static NEWTC: AtomicU64 = AtomicU64::new(0);
fn next_conj(bi: &Body, bj: &Body, t0: f64, horizon: f64) -> (f64, bool) {
    let dn = bi.nn() - bj.nn();
    let osc = 2.0 * (bi.e + bj.e);
    let lam = |t: f64| {
        LAMC.fetch_add(1, Ordering::Relaxed);
        bi.lambda(t) - bj.lambda(t)
    };
    let g0 = wrap_pi(lam(t0));
    // (a) epicyclic: if the oscillation alone can close the gap, scan soon.
    if g0.abs() <= osc + 1e-6 && osc > 1e-9 {
        SCANC.fetch_add(1, Ordering::Relaxed);
        let p = bi.period as f64 / TICKS;
        let n = 48;
        let mut t_prev = t0;
        let mut g_prev = wrap_pi(lam(t_prev));
        for k in 1..=n {
            let t = t0 + 1.5 * p * k as f64 / n as f64;
            let g = wrap_pi(lam(t));
            let crossed = (g_prev > 0.0) != (g > 0.0) && g_prev.abs() < 1.2 && g.abs() < 1.2;
            if crossed {
                let (mut lo, mut hi) = (t_prev, t);
                let glo = wrap_pi(lam(lo));
                for _ in 0..50 {
                    let mid = 0.5 * (lo + hi);
                    let gm = wrap_pi(lam(mid));
                    if (gm > 0.0) == (glo > 0.0) { lo = mid; } else { hi = mid; }
                }
                let t = 0.5 * (lo + hi);
                if t > t0 + 1e-9 {
                    return (t, true);
                }
            }
            t_prev = t;
            g_prev = g;
        }
        // no crossing in 1.5 periods: drift will close it; fall through
    }
    // (b) drift: Newton to the next multiple of 2pi in the drift direction; degenerate dn sleeps.
    if dn.abs() < 1e-14 {
        return (horizon + 1.0, false);
    }
    let vt = if dn > 0.0 {
        if g0 <= 0.0 { 0.0 } else { TAU }
    } else if g0 >= 0.0 { 0.0 } else { -TAU };
    let mut t = t0 + (vt - g0) / dn;
    if t <= t0 + 1e-9 {
        t = t0 + TAU / dn.abs();
    }
    NEWTC.fetch_add(1, Ordering::Relaxed);
    // bracketed scan around the linear synodic guess (robust to the wrap ambiguity)
    let psyn = TAU / dn.abs();
    let t_lin = t0 + (vt - g0) / dn;
    let u = |t: f64| wrap_pi(lam(t) - vt);
    if t_lin > t0 + 1e-9 && u(t_lin).abs() < 1e-9 {
        return (t_lin, t_lin <= horizon);
    }
    let w = 0.18 * psyn;
    let tl = (t_lin - w).max(t0 + 1e-9);
    let th = t_lin + w;
    let n = 32;
    let mut t_prev = tl;
    let mut u_prev = u(t_prev);
    for k in 1..=n {
        let tt = tl + (th - tl) * k as f64 / n as f64;
        let uu = u(tt);
        if (u_prev > 0.0) != (uu > 0.0) && u_prev.abs() < 1.5 && uu.abs() < 1.5 {
            let (mut lo, mut hi) = (t_prev, tt);
            let ulo = u(lo);
            for _ in 0..40 {
                let mid = 0.5 * (lo + hi);
                let um = u(mid);
                if (um > 0.0) == (ulo > 0.0) { lo = mid; } else { hi = mid; }
            }
            let t = 0.5 * (lo + hi);
            if t > t0 + 1e-9 {
                return (t, t <= horizon);
            }
        }
        t_prev = tt;
        u_prev = uu;
    }
    let t = t0 + psyn;
    (t, t <= horizon)
}

impl Sim {
    fn new(
        bodies: Vec<Body>,
        masses: Vec<f64>,
        rho_screen: f64,
        r_contact: f64,
    ) -> Self {
        let n = bodies.len();
        let birth = bodies.clone();
        let mut pairs = Vec::new();
        let mut adj: Vec<Vec<u32>> = vec![Vec::new(); n];
        let margin = rho_screen.max(1e-3);
        for i in 0..n {
            for j in (i + 1)..n {
                let (bi, bj) = (&bodies[i], &bodies[j]);
                let rmax_i = bi.a * (1.0 + bi.e);
                let rmin_i = bi.a * (1.0 - bi.e);
                let rmax_j = bj.a * (1.0 + bj.e);
                let rmin_j = bj.a * (1.0 - bj.e);
                if rmax_i + margin >= rmin_j && rmax_j + margin >= rmin_i {
                    let id = pairs.len() as u32;
                    pairs.push(Pair { i: i as u32, j: j as u32, tnext: 0.0, ver: 0, active: true, ki: 0, kj: 0 });
                    adj[i].push(id);
                    adj[j].push(id);
                }
            }
        }
        let mut sim = Sim {
            b: bodies,
            birth,
            m: masses,
            pairs,
            adj,
            heap: BinaryHeap::new(),
            kicks: 0,
            contacts: 0,
            strong: 0,
            captures: 0,
            r_contact,
            rho_screen,
            kicks_per_body: vec![0; n],
            conj_tried: 0,
        };
        let h = 1e30; // schedule everything; horizon applied in the loop
        eprintln!("init: {} pairs", sim.pairs.len());
        for id in 0..sim.pairs.len() {
            if id % 4000 == 0 { eprintln!("sched {} lam={} scan={} newt={} fall={}", id, LAMC.load(Ordering::Relaxed), SCANC.load(Ordering::Relaxed), NEWTC.load(Ordering::Relaxed), FALLC.load(Ordering::Relaxed)); }
            let (t, _) = next_conj(&sim.b[sim.pairs[id].i as usize], &sim.b[sim.pairs[id].j as usize], 0.0, h);
            sim.pairs[id].tnext = t;
            sim.heap.push(Reverse(Ev { t, pair: id as u32, ver: 0 }));
        }
        sim
    }

    fn reschedule(&mut self, body: usize, t0: f64, horizon: f64) {
        for &id in self.adj[body].clone().iter() {
            self.pairs[id as usize].ki = self.kicks_per_body[self.pairs[id as usize].i as usize];
            self.pairs[id as usize].kj = self.kicks_per_body[self.pairs[id as usize].j as usize];
            let (i, j) = (self.pairs[id as usize].i as usize, self.pairs[id as usize].j as usize);
            // overlap check with drift margin
            let (bi, bj) = (&self.b[i], &self.b[j]);
            let margin = self.rho_screen.max(1e-3);
            let ok = bi.a * (1.0 + bi.e) + margin >= bj.a * (1.0 - bj.e)
                && bj.a * (1.0 + bj.e) + margin >= bi.a * (1.0 - bi.e);
            self.pairs[id as usize].ver += 1;
            if !ok {
                self.pairs[id as usize].active = false;
                continue;
            }
            let (t, _) = next_conj(&self.b[i], &self.b[j], t0 + 1e-9, horizon);
            self.pairs[id as usize].tnext = t;
            self.heap.push(Reverse(Ev { t, pair: id, ver: self.pairs[id as usize].ver }));
        }
    }

    fn run(&mut self, horizon: f64) {
        let mut pops: u64 = 0;
        loop {
            pops += 1;
            if pops % 200000 == 0 {
                eprintln!("pops={} t={:.3} h={:.3} heap={} kicks={} conj={}", pops, 
                    self.heap.peek().map(|e| e.0.t).unwrap_or(-1.0), horizon, self.heap.len(), self.kicks, self.conj_tried);
            }
            let ev = match self.heap.pop() {
                Some(Reverse(e)) => e,
                None => break,
            };
            if ev.t > horizon {
                break;
            }
            let p = &self.pairs[ev.pair as usize];
            if !p.active || p.ver != ev.ver || p.tnext != ev.t {
                continue;
            }
            // lazy invalidation: too many kicks to either body since scheduling
            let (ii, jj) = (p.i as usize, p.j as usize);
            if self.kicks_per_body[ii] - p.ki >= 32 || self.kicks_per_body[jj] - p.kj >= 32 {
                self.reschedule_pair(ev.pair as usize, ev.t, horizon);
                continue;
            }
            self.conj_tried += 1;
            let (i, j) = (p.i as usize, p.j as usize);
            let t = ev.t;
            let si = self.b[i].state(t);
            let sj = self.b[j].state(t);
            // relative state of i about j
            let (rx, ry) = (si[0] - sj[0], si[1] - sj[1]);
            let (vx, vy) = (si[2] - sj[2], si[3] - sj[3]);
            let vv = vx * vx + vy * vy;
            if vv < 1e-20 {
                self.reschedule_pair(ev.pair as usize, t, horizon);
                continue;
            }
            let rv = rx * vx + ry * vy;
            let tau = -rv / vv;
            let (bx, by) = (rx + vx * tau, ry + vy * tau);
            let d = (bx * bx + by * by).sqrt();
            let mu_p = self.m[i] + self.m[j];
            if d > self.rho_screen || mu_p <= 0.0 {
                self.reschedule_pair(ev.pair as usize, t, horizon);
                continue;
            }
            // relative velocity after the encounter
            let mut nvx = vx;
            let mut nvy = vy;
            if d < 2.0 * self.r_contact {
                // elastic contact: flip the normal component (relative frame)
                let nrm = d.max(1e-300);
                let (nx, ny) = (bx / nrm, by / nrm);
                let vn = vx * nx + vy * ny;
                if vn < 0.0 {
                    nvx = vx - 2.0 * vn * nx;
                    nvy = vy - 2.0 * vn * ny;
                    self.contacts += 1;
                    self.kicks += 1;
                    self.kicks_per_body[i] += 1;
                    self.kicks_per_body[j] += 1;
                }
            } else {
                let deflect = 2.0 * (mu_p / (d * vv)).atan();
                if deflect > 0.3 {
                    // strong: the analytic hyperbola
                    self.strong += 1;
                    let (ex, ey, cap) = hyper_scatter(rx, ry, vx, vy, mu_p);
                    if cap {
                        self.captures += 1;
                        self.reschedule_pair(ev.pair as usize, t, horizon);
                        continue;
                    }
                    nvx = ex;
                    nvy = ey;
                    self.kicks += 1;
                    self.kicks_per_body[i] += 1;
                    self.kicks_per_body[j] += 1;
                } else if deflect > 1e-14 {
                    let s = if (bx * vy - by * vx) > 0.0 { 1.0 } else { -1.0 };
                    let (c, sn) = ((s * deflect).cos(), (s * deflect).sin());
                    nvx = vx * c - vy * sn;
                    nvy = vx * sn + vy * c;
                    self.kicks += 1;
                    self.kicks_per_body[i] += 1;
                    self.kicks_per_body[j] += 1;
                }
            }
            if (nvx - vx).abs() + (nvy - vy).abs() > 0.0 {
                let (dvx, dvy) = (nvx - vx, nvy - vy);
                let mi = self.m[i];
                let mj = self.m[j];
                let mp = mi + mj;
                // di = (mj/mp) dV, dj = -(mi/mp) dV
                let bi = Body::from_state(t, si[0], si[1], si[2] + mj / mp * dvx, si[3] + mj / mp * dvy);
                let bj = Body::from_state(t, sj[0], sj[1], sj[2] - mi / mp * dvx, sj[3] - mi / mp * dvy);
                self.b[i] = bi;
                self.b[j] = bj;
                let strong_kick = ((nvx - vx) * (nvx - vx) + (nvy - vy) * (nvy - vy)).sqrt() > 3e-3;
                if strong_kick {
                    self.reschedule(i, t, horizon);
                    self.reschedule(j, t, horizon);
                } else {
                    self.reschedule_pair(ev.pair as usize, t, horizon);
                }
            } else {
                self.reschedule_pair(ev.pair as usize, t, horizon);
            }
        }
    }

    fn reschedule_pair(&mut self, id: usize, t0: f64, horizon: f64) {
        let (i, j) = (self.pairs[id].i as usize, self.pairs[id].j as usize);
        let (tn, _) = next_conj(&self.b[i], &self.b[j], t0 + 1e-9, horizon);
        self.pairs[id].ki = self.kicks_per_body[i];
        self.pairs[id].kj = self.kicks_per_body[j];
        self.pairs[id].ver += 1;
        self.pairs[id].tnext = tn;
        self.heap.push(Reverse(Ev { t: tn, pair: id as u32, ver: self.pairs[id].ver }));
    }
}

/// exact two-body scattering of the isolated pair: the analytic hyperbola.
/// Outgoing speed = incoming speed (energy exact); direction rotated by
/// delta = 2*asin(1/e), e = sqrt(1 + 2 E L^2 / mu^2), toward the perturber.
/// The impulse kernel is this formula's weak limit (validated in `kernel`).
fn hyper_scatter(rx: f64, ry: f64, vx: f64, vy: f64, mu: f64) -> (f64, f64, bool) {
    let vv = vx * vx + vy * vy;
    let v = vv.sqrt();
    let en = 0.5 * vv; // specific energy of the relative orbit
    let ll = rx * vy - ry * vx; // specific angular momentum (signed)
    if en <= 0.0 {
        return (vx, vy, true); // capture: flag, no scatter
    }
    let e = (1.0 + 2.0 * en * ll * ll / (mu * mu)).sqrt();
    if e <= 1.0 {
        return (vx, vy, true);
    }
    let delta = 2.0 * (1.0 / e).asin();
    let tau = -(rx * vx + ry * vy) / vv;
    let (bx, by) = (rx + vx * tau, ry + vy * tau);
    let sgn = if (bx * vy - by * vx) > 0.0 { 1.0 } else { -1.0 };
    let (c, sn) = ((sgn * delta).cos(), (sgn * delta).sin());
    (vx * c - vy * sn, vx * sn + vy * c, false)
}

// ---------- measurement ----------
fn entropy_bits(vals: &[f64], q: f64) -> (f64, f64, f64) {
    let mut h = std::collections::HashMap::<i64, u64>::new();
    for &x in vals {
        *h.entry((x / q).round() as i64).or_default() += 1;
    }
    let n = vals.len() as f64;
    let mut hb = 0.0;
    for &c in h.values() {
        let p = c as f64 / n;
        hb -= p * p.log2();
    }
    let mean = vals.iter().sum::<f64>() / n;
    let var = vals.iter().map(|x| (x - mean) * (x - mean)).sum::<f64>() / n;
    (hb, h.get(&0).copied().unwrap_or(0) as f64 / n, var.sqrt())
}

fn measure(sim: &Sim, t: f64, tag: &str, scene: &str) {
    let n = sim.b.len();
    let mut oe = Vec::with_capacity(n);
    let mut ol = Vec::with_capacity(n);
    let mut op = Vec::with_capacity(n);
    let mut oph = Vec::with_capacity(n);
    let mut singletons = 0u64;
    let mut etot = 0.0;
    for k in 0..n {
        let (b, bb) = (&sim.b[k], &sim.birth[k]);
        etot += -0.5 / b.a;
        if b.a < 0.5 || b.a > 2.0 || b.e > 0.9 || b.a <= 0.0 {
            singletons += 1;
            continue;
        }
        oe.push(b.a / bb.a - 1.0); // dE/E (a_b/a - 1 is -dE/E to first order; sign irrelevant for entropy)
        let l = (b.a * (1.0 - b.e * b.e)).sqrt();
        let lb = (bb.a * (1.0 - bb.e * bb.e)).sqrt();
        ol.push(l / lb - 1.0);
        op.push(wrap_pi(b.pom - bb.pom) / TAU);
        oph.push(wrap_pi(b.lambda(t) - bb.lambda(t)) / TAU);
    }
    // center each column (the program absorbs the shared drift)
    let centered = |v: &mut Vec<f64>| {
        let mu = v.iter().sum::<f64>() / v.len() as f64;
        for x in v.iter_mut() {
            *x -= mu;
        }
        mu
    };
    let me = centered(&mut oe);
    let ml = centered(&mut ol);
    let mp = centered(&mut op);
    let mph = centered(&mut oph);
    for q in [1e-4f64, 1e-6, 1e-8] {
        let (he, _, se) = entropy_bits(&oe, q);
        let (hl, _, sl) = entropy_bits(&ol, q);
        let (hp, _, sp) = entropy_bits(&op, q);
        let (hh, _, sh) = entropy_bits(&oph, q);
        let tot = he + hl + hp + hh;
        println!(
            "{{\"scene\":\"{}\",\"tag\":\"{}\",\"t_orbits\":{:.2},\"q\":{:e},\"pop\":{},\"bits\":{:.3},\"H_E\":{:.3},\"H_L\":{:.3},\"H_pom\":{:.3},\"H_lam\":{:.3},\"sig_E\":{:.2e},\"sig_L\":{:.2e},\"sig_pom\":{:.2e},\"sig_lam\":{:.2e},\"drift_E\":{:.2e},\"drift_L\":{:.2e},\"drift_pom\":{:.2e},\"drift_lam\":{:.2e},\"singletons\":{},\"kicks\":{},\"contacts\":{},\"strong\":{},\"kicks_per_body\":{:.3},\"E_drift\":{:.2e}}}",
            scene, tag, t / TAU, q, n, tot, he, hl, hp, hh, se, sl, sp, sh, me, ml, mp, mph,
            singletons, sim.kicks, sim.contacts, sim.strong,
            sim.kicks as f64 / n as f64,
            etot,
        );
    }
}

// ---------- scenes ----------
fn belt_scene(n: usize, mu: f64, rho: f64, orbits: f64, seed: u64, width: f64, sigma_e: f64, r_contact: f64) {
    let mut rng = Rng(seed);
    let mut bodies = Vec::with_capacity(n);
    for _ in 0..n {
        let a = 1.0 + width * (2.0 * rng.f64() - 1.0);
        let u = rng.f64();
        let e = (sigma_e * (-2.0 * (1.0 - u).ln()).sqrt()).min(0.3);
        let pom = TAU * rng.f64();
        let lam = TAU * rng.f64();
        bodies.push(Body::new(a, e, pom, lam));
    }
    let masses = vec![mu / n as f64; n];
    let t_end = orbits * TAU;
    let mut sim = Sim::new(bodies, masses, rho, r_contact);
    let nck = 8;
    for k in 1..=nck {
        let t = t_end * k as f64 / nck as f64;
        sim.run(t);
        measure(&sim, t, &format!("ck{}", k), "belt");
    }
    println!("{{\"scene\":\"belt\",\"done\":true,\"conj_tried\":{},\"kicks\":{},\"contacts\":{},\"strong\":{},\"pairs\":{},\"n\":{},\"mu\":{:e},\"rho\":{:e},\"orbits\":{},\"wall_s\":{:.1}}}",
        sim.conj_tried, sim.kicks, sim.contacts, sim.strong, sim.pairs.len(), n, mu, rho, orbits, 0.0);
}

fn lane_scene(n: usize, mu: f64, rho: f64, orbits: f64, seed: u64, r_contact: f64, sigma_e: f64) {
    let mut rng = Rng(seed);
    let mut bodies = Vec::with_capacity(n);
    for _ in 0..n {
        let a = 1.0 + 5e-4 * (2.0 * rng.f64() - 1.0);
        let u = rng.f64();
        let e = (sigma_e * (-2.0 * (1.0 - u).ln()).sqrt()).min(0.1);
        let pom = TAU * rng.f64();
        let lam = TAU * rng.f64();
        bodies.push(Body::new(a, e, pom, lam));
    }
    let masses = vec![mu / n as f64; n];
    let t_end = orbits * TAU;
    let mut sim = Sim::new(bodies, masses, rho, r_contact);
    let nck = 6;
    for k in 1..=nck {
        let t = t_end * k as f64 / nck as f64;
        sim.run(t);
        measure(&sim, t, &format!("ck{}", k), "lane");
    }
    println!("{{\"scene\":\"lane\",\"done\":true,\"conj_tried\":{},\"kicks\":{},\"contacts\":{},\"strong\":{},\"pairs\":{},\"n\":{},\"mu\":{:e},\"r_contact\":{:e},\"orbits\":{}}}",
        sim.conj_tried, sim.kicks, sim.contacts, sim.strong, sim.pairs.len(), n, mu, r_contact, orbits);
}

/// impulse kernel vs the exact analytic hyperbola, over a grid of strengths.
fn kernel_scene() {
    for &m in &[1e-7f64, 1e-6, 1e-5] {
        for &vrel in &[0.03f64, 0.1, 0.3] {
            for &s in &[0.003f64, 0.03, 0.1, 0.3, 1.0, 3.0] {
                let mu = 2.0 * m;
                let d = mu / (s * vrel * vrel);
                let (ix, iy) = (d, 0.0);
                let (vx, vy) = (0.0, vrel);
                let vv = vrel * vrel;
                let deflect = 2.0 * (mu / (d * vv)).atan();
                let (ex, ey, cap) = hyper_scatter(ix, iy, vx, vy, mu);
                if cap {
                    println!("{{\"kernel\":true,\"m_each\":{:e},\"vrel\":{},\"strength\":{},\"cap\":true}}", m, vrel, s);
                    continue;
                }
                let v_exact = (ex * ex + ey * ey).sqrt();
                let v_imp = vrel; // impulse conserves speed exactly
                let delta_h = (-(vrel * ex)).atan2(vrel * ey).abs();
                let ang_err = ((ex * vy - ey * vx) / (v_exact * vrel)).acos();
                println!("{{\"kernel\":true,\"m_each\":{:e},\"vrel\":{},\"strength\":{},\"d\":{:.3e},\"deflect_imp\":{:.5},\"delta_hyp\":{:.5},\"rel_ang_err\":{:.2e},\"dv_rel\":{:.1e}}}",
                    m, vrel, s, d, deflect, delta_h, ang_err / deflect.max(1e-30), (v_exact - v_imp).abs() / vrel);
            }
        }
    }
}

fn selftest() {
    let mut rng = Rng(7);
    let mut worst = 0.0f64;
    for _ in 0..2000 {
        let a = 0.9 + 0.2 * rng.f64();
        let e = 0.3 * rng.f64();
        let pom = TAU * rng.f64();
        let lam = TAU * rng.f64();
        let b = Body::new(a, e, pom, lam);
        let t = 10.0 * rng.f64();
        let s = b.state(t);
        let b2 = Body::from_state(t, s[0], s[1], s[2], s[3]);
        let s2 = b2.state(t);
        let err = ((s2[0] - s[0]).powi(2) + (s2[1] - s[1]).powi(2)).sqrt()
            + 0.1 * ((s2[2] - s[2]).powi(2) + (s2[3] - s[3]).powi(2)).sqrt();
        worst = worst.max(err);
        // integer period discipline: same period after round trip (both rounded the same way usually)
        if !(b2.a > 0.0 && b2.e >= 0.0) { eprintln!("DBG a={} e={} a2={} e2={} s={:?}",a,e,b2.a,b2.e,s); }
    }
    println!("{{\"selftest\":\"kepler_roundtrip\",\"worst\":{:.2e}}}", worst);
    // hyperbola: speed conserved exactly; weak limit matches the impulse
    for &(m, v, d) in &[(1e-4f64, 0.1f64, 1e-2), (1e-3, 0.03, 1e-2), (3e-4, 0.2, 1e-2), (1e-3, 0.1, 1e-3)] {
        let mu = 2.0 * m;
        let (ex, ey, cap) = hyper_scatter(d, 0.0, 0.0, v, mu);
        let vv = v * v;
        let delta_h = (-(v * ex)).atan2(v * ey).abs(); // angle between (0,v) and (ex,ey)
        let delta_i = 2.0 * (mu / (d * vv)).atan();
        let dv = ((ex * ex + ey * ey).sqrt() - v).abs();
        println!("{{\"selftest\":\"hyperbola\",\"mu\":{:e},\"v\":{},\"d\":{},\"cap\":{},\"dv_rel\":{:.2e},\"delta_hyp\":{:.5},\"delta_imp\":{:.5},\"rel_err\":{:.2e}}}",
            mu, v, d, cap, dv / v, delta_h, delta_i, (delta_h - delta_i).abs() / delta_h);
    }
    // conjunction finder: two orbits with known synodic
    let bi = Body::new(1.0, 0.0, 0.0, 0.0);
    let bj = Body::new(1.01, 0.0, 0.0, 0.5);
    let (t, _) = next_conj(&bi, &bj, 0.0, 1e9);
    let li = bi.lambda(t);
    let lj = bj.lambda(t);
    println!("{{\"selftest\":\"conjunction\",\"t\":{:.6},\"wrap\":{:.2e}}}", t, wrap_pi(li - lj));
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    match args[1].as_str() {
        "selftest" => selftest(),
        "kernel" => kernel_scene(),
        "belt" => {
            let n: usize = args[2].parse().unwrap();
            let mu: f64 = args[3].parse().unwrap();
            let rho: f64 = args[4].parse().unwrap();
            let orbits: f64 = args[5].parse().unwrap();
            let seed: u64 = args[6].parse().unwrap();
            let width: f64 = args.get(7).map(|s| s.parse().unwrap()).unwrap_or(0.01);
            let sigma_e: f64 = args.get(8).map(|s| s.parse().unwrap()).unwrap_or(0.05);
            belt_scene(n, mu, rho, orbits, seed, width, sigma_e, 1e-4);
        }
        "lane" => {
            let n: usize = args[2].parse().unwrap();
            let mu: f64 = args[3].parse().unwrap();
            let rho: f64 = args[4].parse().unwrap();
            let orbits: f64 = args[5].parse().unwrap();
            let seed: u64 = args[6].parse().unwrap();
            let r_contact: f64 = args.get(7).map(|s| s.parse().unwrap()).unwrap_or(1e-3);
            let sigma_e: f64 = args.get(8).map(|s| s.parse().unwrap()).unwrap_or(0.02);
            lane_scene(n, mu, rho, orbits, seed, r_contact, sigma_e);
        }
        _ => eprintln!("unknown scene"),
    }
}
