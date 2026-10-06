// Probe A: the changeover near a secondary as a composition of integer shears (JANUS's arithmetic core).
// CR3BP on an integer lattice: star exact, planet imposed-circular, ship kicked by SyMBA-weighted
// shares across 3 levels (mirrors crates/universe/src/force.rs). Metrics: Jacobi growth exponent
// (exact-rational observer), out-and-back bit identity, ns/op, min conjunction distance.
// Configs: A1 floor-shear, A2 nearest-shear, A3 carried-shear, A4 trunc-chain (Scalar-like),
//          A5 rescale-round (negative control), A6 float64 reference.
#[allow(dead_code)]
use std::time::Instant;

const GM_S: i64 = 1 << 38;
const R_P: i64 = 1 << 20;
const V_P: i64 = 512; // omega = 2^-11 exactly
const GM_P: i64 = 1 << 24; // mass ratio 2^-14 (gentler conjunctions)
const EDGE: i64 = 1 << 15; // ~SOI for mass 2^-14 (R/32)
const LEVELS: u8 = 3;
const H0: i64 = 64;
const VE: u32 = 10; // 1 v-quantum = 2^-VE q/u
const ACC: u32 = 20; // carry in 2^-ACC v-quanta
const STEPS: i64 = 10_053; // ~50 planet orbits
const V_CAP: i64 = 1200; // engagement-certificate speed cap (asserted)

fn fdiv(a: i128, b: i128) -> i128 { let q = a / b; if a % b < 0 { q - 1 } else { q } }
fn frem(a: i128, b: i128) -> i128 { let r = a % b; if r < 0 { r + b } else { r } }
fn rdiv(a: i128, b: i128) -> i128 { let f = fdiv(a, b); let r = frem(a, b); if 2 * r >= b { f + 1 } else { f } }
fn ceildiv(a: i128, b: i128) -> i128 { -fdiv(-a, b) }

fn planet(t: i64) -> (i64, i64) {
    let th = (t as f64) * (V_P as f64) / (R_P as f64);
    ((R_P as f64 * th.cos()).round() as i64, (R_P as f64 * th.sin()).round() as i64)
}

fn isqrt128(a: i128) -> i128 {
    if a <= 0 { return 0; }
    let mut x = (a as f64).sqrt() as i128 + 2;
    loop { let y = (x + a / x) >> 1; if y >= x { break; } x = y; }
    while x * x > a { x -= 1; }
    while (x + 1) * (x + 1) <= a { x += 1; }
    x
}

fn shell(l: u8) -> i64 { if l == 0 { EDGE * 2 } else { EDGE >> (l - 1) } }

fn weight(l: u8, r2: i128) -> i128 {
    let s = shell(l);
    let r = isqrt128(r2);
    if 2 * r <= s as i128 { return 0; }
    if r >= s as i128 { return 1i128 << 32; }
    let n = 2 * r - s as i128;
    fdiv(n * n * (3 * s as i128 - 2 * n) * (1i128 << 32), (s as i128).pow(3))
}
fn weight_top(r2: i128) -> i128 {
    let mut w = 1i128 << 32;
    for i in 0..LEVELS { let b = weight(i, r2); w = fdiv(w * ((1i128 << 32) - b), 1i128 << 32); }
    w
}

fn engaged(l: u8, r2: i128, h: i64) -> bool {
    let reach = (5 * V_CAP * h) / 4;
    isqrt128(r2) - (reach as i128) < shell(l) as i128
}

#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
struct St { x: [i64; 2], xrem: [i128; 2], v: [i128; 2], acc: [i128; 2] }

#[derive(Clone, Copy, PartialEq)]
enum Cfg { FloorShear, NearestShear, CarriedShear, TruncChain, RescaleRound, Float64 }
impl Cfg {
    fn name(self) -> &'static str {
        match self { Cfg::FloorShear => "A1 floor-shear", Cfg::NearestShear => "A2 nearest-shear",
            Cfg::CarriedShear => "A3 carried-shear", Cfg::TruncChain => "A4 trunc-chain",
            Cfg::RescaleRound => "A5 rescale-rc", Cfg::Float64 => "A6 float64" }
    }
}

// A truncating 63-bit-significand software float (crates/space/src/scaled.rs semantics).
#[derive(Clone, Copy)]
struct F { sig: i64, e: i16 } // value = sig * 2^(e-62)
impl F {
    fn zero(self) -> bool { self.sig == 0 }
    fn from_i(v: i64) -> F { F::raw(v as i128, 0) }
    fn raw(n: i128, bp: i32) -> F {
        if n == 0 { return F { sig: 0, e: 0 }; }
        let bits = 128 - n.unsigned_abs().leading_zeros() as i32;
        let shift = bits - 63;
        let mag = if shift >= 0 { (n.unsigned_abs() >> shift) as i64 } else { (n.unsigned_abs() << -shift) as i64 };
        F { sig: if n < 0 { -mag } else { mag }, e: (bp + shift + 62) as i16 }
    }
    fn from_f64(v: f64) -> F {
        if v == 0.0 { return F { sig: 0, e: 0 }; }
        let mut e2 = v.abs().log2().floor() as i32;
        let mut m = ((v / 2f64.powi(e2)) * (1i64 << 62) as f64) as i128;
        while m.unsigned_abs() >= (1u128 << 62) { e2 += 1; m = ((v / 2f64.powi(e2)) * (1i64 << 62) as f64) as i128; }
        while m != 0 && m.unsigned_abs() < (1u128 << 61) { e2 -= 1; m = ((v / 2f64.powi(e2)) * (1i64 << 62) as f64) as i128; }
        F { sig: m as i64, e: e2 as i16 }
    }
    fn to_f64(self) -> f64 { (self.sig as f64) * 2f64.powi(self.e as i32 - 62) }
    fn mk(mut sig: i128, mut e: i32) -> F {
        // normalize (sig, e) with value = sig * 2^(e-62); truncate toward zero to 63 bits
        if sig == 0 { return F { sig: 0, e: 0 }; }
        let neg = sig < 0;
        let mut a = sig.unsigned_abs();
        let mut bits = 128 - a.leading_zeros() as i32;
        if bits > 63 {
            let sh = bits - 63;
            a >>= sh; e += sh; bits = 63;
        }
        while bits < 63 { a <<= 1; e -= 1; bits += 1; }
        // (the loop runs <= 127 times; values here are never denormal by much)
        F { sig: if neg { -(a as i64) } else { a as i64 }, e: e as i16 }
    }
    fn mul(self, o: F) -> F {
        if self.zero() || o.zero() { return F { sig: 0, e: 0 }; }
        F::mk((self.sig as i128) * (o.sig as i128), self.e as i32 + o.e as i32 - 62)
    }
    fn div(self, o: F) -> F {
        if self.zero() { return F { sig: 0, e: 0 }; }
        let n = (self.sig as i128) << 62;
        let d = o.sig as i128;
        let q = if (n >= 0) == (d >= 0) { n / d } else { -((-n) / d) };
        F::mk(q, self.e as i32 - o.e as i32)
    }
    fn add(self, o: F) -> F {
        if self.zero() { return o; } if o.zero() { return self; }
        let (hi, lo) = if self.e >= o.e { (self, o) } else { (o, self) };
        let d = (hi.e - lo.e) as i32;
        if d > 100 { return hi; }
        let n = (lo.sig as i128) / (1i128 << d); // truncate toward zero (scaled.rs rule)
        F::mk((hi.sig as i128) + n, hi.e as i32)
    }
    fn sub(self, o: F) -> F { self.add(F { sig: -o.sig, e: o.e }) }
    fn sqrt(self) -> F { if self.zero() { return self; } F::from_f64(self.to_f64().sqrt()) }
}
fn trunc(p: i128) -> i64 {
    let bits = 128 - p.unsigned_abs().leading_zeros() as i32;
    if bits <= 63 { return p as i64; }
    let shift = bits - 63;
    let mag = (p.unsigned_abs() >> shift) as i64;
    if p < 0 { -mag } else { mag }
}

struct Terms { ns: [i128; 2], ds: [i128; 2], np: [i128; 2], dp: [i128; 2] }
fn terms(st: &St, t: i64, l: u8, h: i64, star: bool) -> Terms {
    let (px, py) = planet(t);
    let dxp = (px - st.x[0]) as i128; let dyp = (py - st.x[1]) as i128;
    let d2 = dxp * dxp + dyp * dyp;
    let d3 = d2 * isqrt128(d2);
    let w = if l < LEVELS { weight(l, d2) } else { weight_top(d2) };
    let rx = -st.x[0] as i128; let ry = -st.x[1] as i128;
    let r2 = rx * rx + ry * ry;
    let r3 = r2 * isqrt128(r2);
    let ns = if star {
        [GM_S as i128 * rx * (h as i128) * (1i128 << VE), GM_S as i128 * ry * (h as i128) * (1i128 << VE)]
    } else { [0, 0] };
    Terms { ns, ds: [r3, r3],
        np: [GM_P as i128 * dxp * w * (h as i128), GM_P as i128 * dyp * w * (h as i128)], dp: [d3 << 32, d3 << 32] }
}

struct Sim {
    cfg: Cfg,
    st: St,
    fx: [f64; 2], fv: [f64; 2],
    ops: u64, engaged_ops: u64,
    bits: Vec<u8>,
    min_d: i64, max_rel_v: f64,
}

impl Sim {
    fn new(cfg: Cfg, st: St) -> Self {
        Sim { cfg, st, fx: [st.x[0] as f64, st.x[1] as f64],
            fv: [st.v[0] as f64 / (1 << VE) as f64, st.v[1] as f64 / (1 << VE) as f64],
            ops: 0, engaged_ops: 0, bits: Vec::new(), min_d: i64::MAX, max_rel_v: 0.0 }
    }

    fn planet_rel(&self, t: i64) -> (f64, f64, f64) {
        let (px, py) = planet(t);
        let (dx, dy) = if self.cfg == Cfg::Float64 {
            (px as f64 - self.fx[0], py as f64 - self.fx[1])
        } else {
            ((px - self.st.x[0]) as f64, (py - self.st.x[1]) as f64)
        };
        (dx, dy, (dx * dx + dy * dy).sqrt())
    }

    fn kick(&mut self, t: i64, l: u8, h: i64, star: bool) {
        let (_, _, d) = self.planet_rel(t);
        if (d as i64) < self.min_d { self.min_d = d as i64; }
        match self.cfg {
            Cfg::Float64 => {
                let (px, py) = planet(t);
                let dx = px as f64 - self.fx[0]; let dy = py as f64 - self.fx[1];
                let r3 = (self.fx[0] * self.fx[0] + self.fx[1] * self.fx[1]).sqrt().powi(3);
                let w = if l < LEVELS { w_f64(l, d) } else { w_top_f64(d) };
                let st = if star {
                    [-GM_S as f64 * self.fx[0] / r3, -GM_S as f64 * self.fx[1] / r3]
                } else { [0.0, 0.0] };
                self.fv[0] += (st[0] + GM_P as f64 * dx * w / d.powi(3)) * h as f64;
                self.fv[1] += (st[1] + GM_P as f64 * dy * w / d.powi(3)) * h as f64;
            }
            Cfg::TruncChain => {
                // the plane's rounding structure: floating inner chain, ONE quantize with carry at the end
                let (px, py) = planet(t);
                let dx = (px - self.st.x[0]) as f64; let dy = (py - self.st.x[1]) as f64;
                let d = (dx * dx + dy * dy).sqrt();
                let r = ((self.st.x[0] as f64).powi(2) + (self.st.x[1] as f64).powi(2)).sqrt();
                let w = if l < LEVELS { w_f64(l, d) } else { w_top_f64(d) };
                for c in 0..2 {
                    let mut dv = GM_P as f64 * (if c == 0 { dx } else { dy }) * w / d.powi(3);
                    if star {
                        dv += -GM_S as f64 * (self.st.x[c] as f64) / r.powi(3);
                    }
                    dv *= h as f64;
                    let n2 = (dv * (1i128 << (VE + ACC)) as f64).round() as i128;
                    let m = 1i128 << ACC;
                    self.st.acc[c] += n2;
                    let q = fdiv(self.st.acc[c], m);
                    self.st.acc[c] = frem(self.st.acc[c], m);
                    self.st.v[c] += q;
                }
            }
            Cfg::CarriedShear => {
                // exact rational inner chain; ONE floor onto the carry grid; FIXED modulus 2^ACC.
                // (a carry whose modulus follows the source distance is provably non-injective: killed.)
                let tm = terms(&self.st, t, l, h, star);
                for c in 0..2 {
                    self.st.v[c] += rdiv(tm.ns[c], tm.ds[c]); // star: unbiased shear (0 if !star)
                    let n2 = fdiv(tm.np[c] * (1i128 << ACC), tm.dp[c]);
                    let m = 1i128 << ACC;
                    self.st.acc[c] += n2;
                    let q = fdiv(self.st.acc[c], m);
                    self.st.acc[c] = frem(self.st.acc[c], m);
                    self.st.v[c] += q;
                }
            }
            Cfg::FloorShear => {
                let tm = terms(&self.st, t, l, h, star);
                for c in 0..2 { self.st.v[c] += fdiv(tm.ns[c], tm.ds[c]) + fdiv(tm.np[c], tm.dp[c]); }
            }
            Cfg::NearestShear | Cfg::RescaleRound => {
                let tm = terms(&self.st, t, l, h, star);
                for c in 0..2 { self.st.v[c] += rdiv(tm.ns[c], tm.ds[c]) + rdiv(tm.np[c], tm.dp[c]); }
            }
        }
        if l > 0 { self.engaged_ops += 1; }
        self.ops += 1;
        if self.cfg == Cfg::RescaleRound {
            for c in 0..2 {
                let a = self.st.v[c].unsigned_abs();
                if a > (1u128 << 15) {
                    let bl = 128 - a.leading_zeros() as i32;
                    let sh = (bl - 15) as u32;
                    let mag = a >> sh;
                    let rem = a & ((1u128 << sh) - 1);
                    let r = if rem >= (1u128 << (sh - 1)) { mag + 1 } else { mag };
                    self.st.v[c] = if self.st.v[c] < 0 { -(r as i128) } else { r as i128 } << sh;
                }
            }
        }
    }
    fn unkick(&mut self, t: i64, l: u8, h: i64, star: bool) {
        match self.cfg {
            Cfg::FloorShear => {
                let tm = terms(&self.st, t, l, h, star);
                for c in 0..2 { self.st.v[c] -= fdiv(tm.ns[c], tm.ds[c]) + fdiv(tm.np[c], tm.dp[c]); }
            }
            Cfg::NearestShear | Cfg::RescaleRound => {
                let tm = terms(&self.st, t, l, h, star);
                for c in 0..2 { self.st.v[c] -= rdiv(tm.ns[c], tm.ds[c]) + rdiv(tm.np[c], tm.dp[c]); }
            }
            Cfg::CarriedShear => {
                let tm = terms(&self.st, t, l, h, star);
                for c in 0..2 {
                    let n2 = fdiv(tm.np[c] * (1i128 << ACC), tm.dp[c]);
                    let m = 1i128 << ACC;
                    let sacc = self.st.acc[c];
                    let q = ceildiv(n2 - sacc, m);
                    self.st.acc[c] = sacc + q * m - n2;
                    self.st.v[c] -= q + rdiv(tm.ns[c], tm.ds[c]);
                }
            }
            Cfg::TruncChain => {
                let (px, py) = planet(t);
                let dx = (px - self.st.x[0]) as f64; let dy = (py - self.st.x[1]) as f64;
                let d = (dx * dx + dy * dy).sqrt();
                let r = ((self.st.x[0] as f64).powi(2) + (self.st.x[1] as f64).powi(2)).sqrt();
                let w = if l < LEVELS { w_f64(l, d) } else { w_top_f64(d) };
                for c in 0..2 {
                    let mut dv = GM_P as f64 * (if c == 0 { dx } else { dy }) * w / d.powi(3);
                    if star {
                        dv += -GM_S as f64 * (self.st.x[c] as f64) / r.powi(3);
                    }
                    dv *= h as f64;
                    let n2 = (dv * (1i128 << (VE + ACC)) as f64).round() as i128;
                    let m = 1i128 << ACC;
                    let sacc = self.st.acc[c];
                    let q = ceildiv(n2 - sacc, m);
                    self.st.acc[c] = sacc + q * m - n2;
                    self.st.v[c] -= q;
                }
            }
            Cfg::Float64 => {}
        }
    }

    fn drift(&mut self, h: i64) {
        for c in 0..2 {
            let tt = self.st.xrem[c] + self.st.v[c] * h as i128;
            self.st.x[c] += fdiv(tt, 1i128 << VE) as i64;
            self.st.xrem[c] = frem(tt, 1i128 << VE);
        }
        self.ops += 1;
    }
    fn undrift(&mut self, h: i64) {
        for c in 0..2 {
            // xrem is a carry: k is the unique integer with k*2^VE + xrem' - v*h in [0, 2^VE)
            let q = 1i128 << VE;
            let k = ceildiv(self.st.v[c] * h as i128 - self.st.xrem[c], q);
            let xr = k * q + self.st.xrem[c] - self.st.v[c] * h as i128;
            self.st.x[c] -= k as i64;
            self.st.xrem[c] = xr;
        }
    }

    fn fwd(&mut self, l: u8, t: i64) {
        let h = H0 >> (2 * l as i64);
        let (px, py) = planet(t);
        let engage = l < LEVELS && {
            if self.cfg == Cfg::Float64 {
                let dx = px as f64 - self.fx[0]; let dy = py as f64 - self.fx[1];
                (dx * dx + dy * dy).sqrt() - (((5 * V_CAP * h) / 4) as f64) < shell(l) as f64
            } else {
                let dxp = (px - self.st.x[0]) as i128; let dyp = (py - self.st.x[1]) as i128;
                engaged(l, dxp * dxp + dyp * dyp, h)
            }
        };
        self.kick(t, l, h, !engage); // the star (the drift's stand-in) rides the leaf step only
        if engage {
            let hs = H0 >> (2 * (l + 1) as i64);
            for i in 0..4 { self.fwd(l + 1, t + i * hs); }
            self.bits.push(1);
        } else {
            if self.cfg == Cfg::Float64 {
                self.fx[0] += self.fv[0] * h as f64; self.fx[1] += self.fv[1] * h as f64; self.ops += 1;
            } else { self.drift(h); }
            self.bits.push(0);
        }
    }

    fn bwd(&mut self, l: u8, t: i64) {
        let h = H0 >> (2 * l as i64);
        let bit = self.bits.pop().unwrap();
        if bit == 1 {
            let hs = H0 >> (2 * (l + 1) as i64);
            for i in (0..4).rev() { self.bwd(l + 1, t + i * hs); }
        } else {
            self.undrift(h);
        }
        self.unkick(t, l, h, bit == 0);
    }
}

fn s_f64(y: f64) -> f64 { if y <= 0.0 { 0.0 } else if y >= 1.0 { 1.0 } else { y * y * (3.0 - 2.0 * y) } }
fn w_f64(l: u8, r: f64) -> f64 { let s = shell(l) as f64; s_f64((r - s / 2.0) / (s / 2.0)) }
fn w_top_f64(r: f64) -> f64 { let mut w = 1.0; for i in 0..LEVELS { w *= 1.0 - w_f64(i, r); } w }
fn w_f(l: u8, d: F) -> F { let s = F::from_i(shell(l)); let half = s.mul(F::raw(1i128, -1));
    let y = d.sub(half).div(half); y.mul(y).mul(F::from_i(3).sub(y)) }
fn w_top_f(d: F) -> F { let mut w = F::from_i(1); for i in 0..LEVELS { w = w.mul(F::from_i(1).sub(w_f(i, d))); } w }

fn jacobi(st: &St, t: i64) -> f64 {
    let (px, py) = planet(t);
    let x = st.x[0] as i128; let y = st.x[1] as i128;
    let vx = st.v[0]; let vy = st.v[1];
    let dx = px as i128 - x; let dy = py as i128 - y;
    let r = isqrt128(x * x + y * y).max(1);
    let d = isqrt128(dx * dx + dy * dy).max(1);
    let dd = 4 * (1i128 << (2 * VE)) * r * d;
    let n = 8 * (GM_S as i128) * d * (1i128 << (2 * VE))
        + 8 * (GM_P as i128) * r * (1i128 << (2 * VE))
        - 4 * (vx * vx + vy * vy) * r * d
        - 4 * (y * vx - x * vy) * r * d
        - (x * x + y * y) * r * d;
    n as f64 / dd as f64
}
fn jacobi_f64(fx: [f64; 2], fv: [f64; 2], t: i64) -> f64 {
    let (px, py) = planet(t);
    let (x, y) = (fx[0], fx[1]);
    let d = ((px as f64 - x).powi(2) + (py as f64 - y).powi(2)).sqrt();
    let r = (x * x + y * y).sqrt().max(1.0);
    let w = V_P as f64 / R_P as f64;
    2.0 * GM_S as f64 / r + 2.0 * GM_P as f64 / d
        - (fv[0] + w * y).powi(2) - (fv[1] - w * x).powi(2)
}

fn init(seed: usize) -> St {
    let seeds: [(f64, f64); 16] = [
        (0.94, 0.0), (0.94, std::f64::consts::PI), (0.90, std::f64::consts::FRAC_PI_2),
        (0.97, 3.0 * std::f64::consts::FRAC_PI_2), (0.97, 0.0), (0.99, std::f64::consts::FRAC_PI_2),
        (0.96, std::f64::consts::PI), (0.92, 3.0 * std::f64::consts::FRAC_PI_2),
        (0.95, 0.4), (0.93, 2.1), (0.98, 5.0), (0.91, 1.2), (0.96, 4.0), (0.94, 3.5),
        (0.98, 2.7), (0.92, 0.8),
    ];
    let (rf, ph) = seeds[seed];
    let r0 = (rf * R_P as f64).round() as i64;
    let v0 = 1.02 * (GM_S as f64 / r0 as f64).sqrt();
    St {
        x: [(r0 as f64 * ph.cos()).round() as i64, (r0 as f64 * ph.sin()).round() as i64],
        xrem: [0, 0],
        v: [(-v0 * ph.sin() * (1 << VE) as f64).round() as i128,
            (v0 * ph.cos() * (1 << VE) as f64).round() as i128],
        acc: [0, 0],
    }
}

struct RunResult { exps: Vec<f64>, fins: Vec<f64>, ident: bool, min_d: i64, ns_per_op: f64, engaged_frac: f64 }

fn run(cfg: Cfg, steps: i64) -> RunResult {
    let mut exps = Vec::new(); let mut fins = Vec::new(); let mut min_d = i64::MAX;
    let mut ns_acc = 0u128; let mut ops_acc = 0u64;
    for s in 0..16 {
        let mut sim = Sim::new(cfg, init(s));
        let j0 = if cfg == Cfg::Float64 { jacobi_f64(sim.fx, sim.fv, 0) } else { jacobi(&sim.st, 0) };
        let mut mx = 0.0f64;
        let mut errs: Vec<(f64, f64)> = Vec::new();
        let t0 = Instant::now();
        for k in 1..=steps {
            sim.fwd(0, (k - 1) * H0);
            let jk = if cfg == Cfg::Float64 { jacobi_f64(sim.fx, sim.fv, k * H0) } else { jacobi(&sim.st, k * H0) };
            mx = mx.max((jk / j0 - 1.0).abs());
            errs.push((k as f64, mx));
        }
        ns_acc += t0.elapsed().as_nanos();
        ops_acc += sim.ops;
        min_d = min_d.min(sim.min_d);
        exps.push(fit(&errs)); fins.push(mx);
    }
    // bit identity: 400 steps out and back
    let ident = if cfg == Cfg::Float64 { false } else {
        let st0 = init(0);
        let mut sim = Sim::new(cfg, st0);
        for k in 0..400 { sim.fwd(0, k * H0); }
        for k in (0..400).rev() { sim.bwd(0, k * H0); }
        sim.st == init(0) && sim.bits.is_empty()
    };
    RunResult { exps, fins, ident, min_d, ns_per_op: ns_acc as f64 / ops_acc as f64, engaged_frac: 0.0 }
}

fn fit(errs: &[(f64, f64)]) -> f64 {
    let pts: Vec<(f64, f64)> = errs.iter().filter(|(k, _)| *k >= 100.0)
        .map(|(k, e)| (k.ln(), e.max(1e-300).ln())).collect();
    if pts.len() < 2 { return f64::NAN; }
    let n = pts.len() as f64;
    let sx: f64 = pts.iter().map(|p| p.0).sum();
    let sy: f64 = pts.iter().map(|p| p.1).sum();
    let sxx: f64 = pts.iter().map(|p| p.0 * p.0).sum();
    let sxy: f64 = pts.iter().map(|p| p.0 * p.1).sum();
    (n * sxy - sx * sy) / (n * sxx - sx * sx)
}

fn onestep_test(cfg: Cfg) -> usize {
    let mut fails = 0usize;
    for sd in 0..16usize {
        let mut sim = Sim::new(cfg, init(sd));
        let mut prev = init(sd);
        for k in 0..2000 {
            prev = sim.st;
            let nbits = sim.bits.len();
            sim.fwd(0, k * H0);
            // invert this single step from its post-state
            let mut back = Sim::new(cfg, sim.st);
            back.bits = sim.bits.clone();
            back.bwd(0, k * H0);
            if back.st != prev || back.bits.len() != nbits {
                fails += 1;
                break;
            }
        }
    }
    fails
}

fn dbg_traj(cfg: Cfg) {
    let mut sim = Sim::new(cfg, init(0));
    for k in 0..30 {
        sim.fwd(0, k * H0);
        let j = jacobi(&sim.st, (k + 1) * H0);
        println!("  [traj] {} k={} x=({},{}) v=({},{}) J={:.6e}", cfg.name(), k, sim.st.x[0], sim.st.x[1], sim.st.v[0], sim.st.v[1], j);
    }
}

fn main() {
    if std::env::var("TRAJ").is_ok() { dbg_traj(Cfg::Float64); dbg_traj(Cfg::TruncChain); return; }
    for cfg in [Cfg::FloorShear, Cfg::NearestShear, Cfg::CarriedShear, Cfg::TruncChain, Cfg::RescaleRound] {
        println!("onestep {} fails {}/16 seeds", cfg.name(), onestep_test(cfg));
    }
    println!("cpus={} GM_S={} R_P={} GM_P={} EDGE={} H0={} VE={} ACC={}",
        std::thread::available_parallelism().map(|n| n.get()).unwrap_or(0), GM_S, R_P, GM_P, EDGE, H0, VE, ACC);
    for cfg in [Cfg::FloorShear, Cfg::NearestShear, Cfg::CarriedShear, Cfg::TruncChain, Cfg::RescaleRound, Cfg::Float64] {
        let r = run(cfg, STEPS);
        let mut e = r.exps.clone(); e.sort_by(|a, b| a.partial_cmp(b).unwrap());
        let mut f = r.fins.clone(); f.sort_by(|a, b| a.partial_cmp(b).unwrap());
        println!("{:>17} exp_med={:6.3} exps=[{}] fin_med={:9.2e} ident={} min_d={} ns/op={:.0}",
            cfg.name(), e[16 / 2],
            e.iter().map(|x| format!("{:.2}", x)).collect::<Vec<_>>().join(","),
            f[16 / 2], r.ident, r.min_d, r.ns_per_op);
    }
}
