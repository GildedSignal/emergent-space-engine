//! The contact root on the shipped v1 Householder operator, in exact arithmetic.
//!
//! Shipped rule (relativity.rs): a contact with separation `d` reflects both 4-momenta in
//! the Minkowski hyperplane orthogonal to N = (d·p, E·d) (p, E the pair's total spatial
//! momentum and energy): p' = p − 2 (p·N)/(N·N) N. Everything below keeps that operator
//! and only replaces `d` (the bin-END separation, whose receding gate skips crossed-in-bin
//! pairs) by the contact ROOT normal.
//! Root (from the bin-start integers d0, w, R = reach):
//!   ww = w·w, dw = d0·w, dd = d0·d0,  D = dw² − ww·(dd − R²)
//!   P_num = d0·ww − w·dw          (w·P_num = 0 EXACTLY in integers)
//!   n = (P_num − √D·w)/ww         (|n| = R exactly, w·n = −√D exactly)
//!
//! Scale invariance: N(λd) = λN(d), so p' depends only on the DIRECTION of d. Take the
//! integer-and-√D direction n' = P_num − √D·w =: A − √D·B (A, B integer 2-vectors):
//!   N' = (n'·p, E·n') = U − √D·V  with U = (A·p, E·A), V = (B·p, E·B)  INTEGER.
//! The whole reflection closes in Z[√D] (BigInt):
//!   T' = N'·N' = α − √D·β,  α = U·U + D·V·V,  β = 2·U·V
//!   s  = pa·N' = σ0 − √D·σ1
//!   pa' = [α·pa − 2σ0·U − 2D·σ1·V] + √D·[2σ0·V + 2σ1·U − β·pa]
//!   pb' = [α·pb + 2σ0·U + 2D·σ1·V] + √D·[−β·pb − 2σ0·V − 2σ1·U]
//! Velocity targets Q·p'_c/E' live in Q(√D); their floor/ceil — all the lattice
//! machinery needs — is EXACT via integer square roots. So the root fix is not an
//! approximation: the shipped candidate/selection convention applied at the root is
//! bit-exact. The cheap fleet variant (ONE isqrt, quantized direction) is measured
//! against it.
use num_bigint::BigInt;
use num_traits::Zero;
use std::cmp::Ordering;

fn b(v: i128) -> BigInt {
    BigInt::from(v)
}

/// Minkowski dot x·y = x0y0 − x1y1 − x2y2.
fn dotm(x: &[BigInt; 3], y: &[BigInt; 3]) -> BigInt {
    &x[0] * &y[0] - &x[1] * &y[1] - &x[2] * &y[2]
}

/// floor(sqrt(n)) for n ≥ 0 (Newton; exact).
pub fn isqrt_big(n: &BigInt) -> BigInt {
    assert!(!(*n < BigInt::ZERO));
    if n.is_zero() {
        return BigInt::ZERO;
    }
    let mut x = BigInt::from(1u8) << ((n.bits() + 1) / 2);
    loop {
        let y = (&x + n / &x) >> 1u8;
        if y >= x {
            break;
        }
        x = y;
    }
    x
}

/// Compare m·√D with the integer g, exactly (D ≥ 0).
fn cmp_sqrt(d: &BigInt, m: &BigInt, g: &BigInt) -> Ordering {
    use num_bigint::Sign::{Minus, NoSign, Plus};
    let (sm, sg) = (m.sign(), g.sign());
    if sm == NoSign {
        return match sg {
            Plus => Ordering::Less,
/// Compare m·√D with the integer g, exactly (D ≥ 0). D = 0 or m = 0 collapse to 0 vs g.
fn cmp_sqrt(d: &BigInt, m: &BigInt, g: &BigInt) -> Ordering {
    use num_bigint::Sign::{Minus, NoSign, Plus};
    if d.is_zero() || m.is_zero() {
        return BigInt::ZERO.cmp(g);
    }
    let (sm, sg) = (m.sign(), g.sign());
    if sm != sg {
        return if sm == Plus { Ordering::Greater } else { Ordering::Less };
    }
    let (lhs, rhs) = (m * m * d, g * g);
    if sm == Plus { lhs.cmp(&rhs) } else { rhs.cmp(&lhs) }
}

/// floor((m0 + m1·√D)/Δ) for Δ > 0, exactly.
fn floor_sqrt_frac(m0: &BigInt, m1: &BigInt, d: &BigInt, delta: &BigInt) -> BigInt {
    assert!(*delta > BigInt::ZERO);
    // Estimate at 2^128 scale, then correct by exact comparisons (a few steps at most).
    let scale = BigInt::from(1u8) << 128u8;
    let s = isqrt_big(&(d * &scale * &scale));
    let num = m0 * &scale + m1 * &s;
    let den = delta * &scale;
    let mut c = num / den; // truncates toward zero: near the true floor
    let in_range = |c: &BigInt| -> bool {
        let g0 = c * delta - m0; // need m1√D ≥ g0
        let g1 = (c + 1u8) * delta - m0; // need m1√D < g1
        cmp_sqrt(d, m1, &g0) != Ordering::Less && cmp_sqrt(d, m1, &g1) == Ordering::Less
    };
    while !in_range(&c) {
        c -= 1u8;
    }
    while in_range(&c) {
        c += 1u8;
    }
    c -= 1u8; // the loop above leaves the first out-of-range value
    c
}

/// An exact Q(√D) velocity target: component c is (m0[c] + m1[c]·√D)/Δ, Δ > 0.
#[derive(Clone)]
pub struct ExactTarget {
    pub m0: [BigInt; 2],
    pub m1: [BigInt; 2],
    pub delta: BigInt,
    pub disc: BigInt,
}
impl ExactTarget {
    pub fn floor(&self, c: usize) -> i64 {
        let f = floor_sqrt_frac(&self.m0[c], &self.m1[c], &self.disc, &self.delta);
        i64::try_from(f).expect("velocity floor fits i64")
    }
    /// Exactly an integer lattice point: with an irrational √D only m1 = 0 can be, but a
    /// perfect-square D (tangent contacts: D = 0, and rational geometry) makes the target
    /// rational — integer iff Δ divides the rational numerator.
    pub fn is_integer(&self, c: usize) -> bool {
        let s = isqrt_big(&self.disc);
        let num = if &s * &s == self.disc { &self.m0[c] + &self.m1[c] * &s } else { self.m0[c].clone() };
        if &s * &s == self.disc {
            (&num % &self.delta).is_zero()
        } else {
            self.m1[c].is_zero() && (&self.m0[c] % &self.delta).is_zero()
        }
    }
}

/// The integer root data of one pair, from the bin-start state.
pub struct Root {
    pub d0: [i128; 2],
    pub w: [i128; 2],
    pub r: i128,
    pub ww: i128,
    pub dw: i128,
    pub dd: i128,
    pub disc: i128,
    pub pnum: [i128; 2],
}

impl Root {
    pub fn new(d0: [i128; 2], w: [i128; 2], r: i128) -> Root {
        let dot2 = |u: [i128; 2], v: [i128; 2]| u[0] * v[0] + u[1] * v[1];
        let ww = dot2(w, w);
        let dw = dot2(d0, w);
        let dd = dot2(d0, d0);
        let disc = dw * dw - ww * (dd - r * r);
        let pnum = [d0[0] * ww - w[0] * dw, d0[1] * ww - w[1] * dw];
        Root { d0, w, r, ww, dw, dd, disc, pnum }
    }

    /// The τ-window firing test, in pure integer arithmetic: the ENTERING root
    /// τ− = (−dw − √D)/ww lies in [0, 1]. Outside-start approaching pairs have
    /// τ− ≥ 0 automatically (D < dw² then), so the test is the clause below.
    /// Consumed (past) and future roots fail it; misses never reach it.
    pub fn fires(&self) -> bool {
        let approaching = self.dw < 0;
        let outside = self.dd > self.r * self.r;
        if !(approaching && outside && self.disc >= 0) {
            return false;
        }
        // τ− ≤ 1  ⇔  √D ≥ −dw − ww  ⇔ automatic when −dw ≤ ww, else D ≥ (−dw−ww)².
        -self.dw <= self.ww || self.disc >= (-self.dw - self.ww).pow(2)
    }

    /// τ− in f64 (classification oracle only).
    pub fn tau_minus_f64(&self) -> f64 {
        (-self.dw as f64 - (self.disc.max(0) as f64).sqrt()) / self.ww as f64
    }

    /// Algebra identities, exact: w·P_num = 0 and |P_num|² = ww·(ww·R² − D).
    pub fn identities_hold(&self) -> bool {
        if self.w[0] * self.pnum[0] + self.w[1] * self.pnum[1] != 0 {
            return false;
        }
        let p2 = b(self.pnum[0]) * b(self.pnum[0]) + b(self.pnum[1]) * b(self.pnum[1]);
        let want = b(self.ww) * (b(self.ww) * b(self.r * self.r) - b(self.disc));
        p2 == want
    }

    /// The exact v1 reflection at the root, in Z[√D]. None ⇔ the shipped operator
    /// exchanges nothing (pa·N' = 0) or the geometry degenerates (N'·N' = 0).
    pub fn exact_targets(&self, pa: [i128; 3], pb: [i128; 3], q: i64) -> Option<(ExactTarget, ExactTarget)> {
        let db = |p: [i128; 3]| [b(p[0]), b(p[1]), b(p[2])];
        let (pab, pbb) = (db(pa), db(pb));
        let e = &pab[0] + &pbb[0];
        let px = &pab[1] + &pbb[1];
        let py = &pab[2] + &pbb[2];
        let (a0, a1) = (b(self.pnum[0]), b(self.pnum[1]));
        let (w0, w1) = (b(self.w[0]), b(self.w[1]));
        let d = b(self.disc);
        // U = (A·p, E·A), V = (B·p, E·B) with A = P_num, B = w.
        let u = [&a0 * &px + &a1 * &py, &e * &a0, &e * &a1];
        let v = [&w0 * &px + &w1 * &py, &e * &w0, &e * &w1];
        // No exchange ⇔ s = σ0 − σ1·√D is EXACTLY zero (squared test with sign).
        let sq_zero = &s0 * &s0 == &s1 * &s1 * &d && (s0.sign() == s1.sign() || s0.is_zero());
        if sq_zero || (beta.is_zero() && alpha.is_zero()) {
            return None; // no exchange (shipped convention) or degenerate N'·N' = 0
        }
        let beta = uv * 2u8;
        if beta.is_zero() && alpha.is_zero() {
            return None; // N'·N' = 0: degenerate
        }
        let s0 = dotm(&pab, &u);
        let s1 = dotm(&pab, &v);
        if s0.is_zero() && s1.is_zero() {
            return None; // pa·N' = 0: no exchange (shipped convention)
        }
        // pa' = g + √D·h, pb' = g' + √D·h' (component-wise 3-vectors).
        let mut ga = [BigInt::ZERO; 3];
        let mut ha = [BigInt::ZERO; 3];
        let mut gb = [BigInt::ZERO; 3];
        let mut hb = [BigInt::ZERO; 3];
        for i in 0..3 {
            ga[i] = &alpha * &pab[i] - &s0 * 2u8 * &u[i] - &d * &s1 * 2u8 * &v[i];
            ha[i] = &s0 * 2u8 * &v[i] + &s1 * 2u8 * &u[i] - &beta * &pab[i];
            gb[i] = &alpha * &pbb[i] + &s0 * 2u8 * &u[i] + &d * &s1 * 2u8 * &v[i];
            hb[i] = -(&beta * &pbb[i]) - &s0 * 2u8 * &v[i] - &s1 * 2u8 * &u[i];
        }
        let qb = b(q as i128);
        let one = |g: [BigInt; 3], h: [BigInt; 3]| -> Option<ExactTarget> {
            let delta = &g[0] * &g[0] - &d * &h[0] * &h[0];
            if delta.is_zero() {
                return None;
            }
            let (m0x, m1x) = (&qb * (&g[1] * &g[0] - &d * &h[1] * &h[0]), &qb * (&h[1] * &g[0] - &g[1] * &h[0]));
            let (m0y, m1y) = (&qb * (&g[2] * &g[0] - &d * &h[2] * &h[0]), &qb * (&h[2] * &g[0] - &g[2] * &h[0]));
            let (sgn, delta) = if delta < BigInt::ZERO { (-1i128, -delta) } else { (1i128, delta) };
            let flip = |m: BigInt| if sgn < 0 { -m } else { m };
            Some(ExactTarget { m0: [flip(m0x), flip(m0y)], m1: [flip(m1x), flip(m1y)], delta, disc: d.clone() })
        };
        Some((one(ga, ha)?, one(gb, hb)?))
    }

    /// Float oracle: the same reflection with the float root normal (independent path:
    /// direct n = P_num/ww − (√D/ww)·w, no Z[√D] expansion). Returns the targets and the
    /// smallest margin of any component to its floor/ceil boundary (lattice units).
    pub fn float_targets(&self, pa: [i128; 3], pb: [i128; 3], q: i64) -> (([f64; 2], [f64; 2]), f64) {
        let f = |v: i128| v as f64;
        let sqd = (self.disc.max(0) as f64).sqrt();
        let nx = (f(self.pnum[0]) - sqd * f(self.w[0])) / f(self.ww);
        let ny = (f(self.pnum[1]) - sqd * f(self.w[1])) / f(self.ww);
        let nn = (nx * nx + ny * ny).sqrt();
        let (n0, n1) = (nx / nn, ny / nn);
        let e = f(pa[0] + pb[0]);
        let (px, py) = (f(pa[1] + pb[1]), f(pa[2] + pb[2]));
        let nvec = [n0 * px + n1 * py, e * n0, e * n1];
        let mdot = |x: [f64; 3], y: [f64; 3]| x[0] * y[0] - x[1] * y[1] - x[2] * y[2];
        let t = mdot(nvec, nvec);
        // pa' = pa − 2(pa·N)/T·N ; pb' = pb + 2(pa·N)/T·N  (the shipped composition).
        // The shipped composition: ONE s = pa·N drives both reflections.
        let c = 2.0 * mdot([f(pa[0]), f(pa[1]), f(pa[2])], nvec) / t;
        let sub = |p: [i128; 3], sgn: f64| -> [f64; 3] {
            [f(p[0]) - sgn * c * nvec[0], f(p[1]) - sgn * c * nvec[1], f(p[2]) - sgn * c * nvec[2]]
        };
        let pa2 = sub(pa, 1.0);
        let pb2 = sub(pb, -1.0);
        let qf = q as f64;
        let ta = [qf * pa2[1] / pa2[0], qf * pa2[2] / pa2[0]];
        let tb = [qf * pb2[1] / pb2[0], qf * pb2[2] / pb2[0]];
        let margin = |v: f64| (v - v.floor()).min(v.ceil() - v);
        let m = margin(ta[0]).min(margin(ta[1])).min(margin(tb[0])).min(margin(tb[1]));
        ((ta, tb), m)
    }

    /// The cheap fleet variant: ONE isqrt of D·4^j, direction (P_num<<j) − isqrt·w,
    /// 2-adically reduced. An integer vector along n to ~2^-j·|w|/R rad.
    pub fn quantized_dir(&self, j: u32) -> [i128; 2] {
        assert!(self.disc >= 0, "quantized_dir on a miss");
        let r: i128 = if self.disc <= i64::MAX as i128 && 2 * j < 63 {
            ((self.disc as u64 as u128) << (2 * j)).isqrt() as i128
        } else {
            i128::try_from(isqrt_big(&(b(self.disc) << (2 * j)))).expect("isqrt fits i128")
        };
        let m = [
            (self.pnum[0] << j) - r.checked_mul(self.w[0]).expect("r·w fits"),
            (self.pnum[1] << j) - r.checked_mul(self.w[1]).expect("r·w fits"),
        ];
        let v2 = |v: i128| if v == 0 { j as u32 } else { v.unsigned_abs().trailing_zeros().min(j) };
        let s = v2(m[0]).min(v2(m[1]));
        [m[0] >> s, m[1] >> s]
    }
}

/// Candidates in the shipped order (floor-floor, floor-ceil, ceil-floor, ceil-ceil),
/// deduped and filtered strictly inside the light cone — exact-Q(√D) version.
pub fn exact_candidates(t: &ExactTarget, q: i64) -> Vec<[i64; 2]> {
    let (flx, fly) = (t.floor(0), t.floor(1));
    let (cex, cey) = (
        flx + if t.is_integer(0) { 0 } else { 1 },
        fly + if t.is_integer(1) { 0 } else { 1 },
    );
    let q2 = q as i128 * q as i128;
    let mut out: Vec<[i64; 2]> = Vec::with_capacity(4);
    for x in [flx, cex] {
        for y in [fly, cey] {
            let c = [x, y];
            if !out.contains(&c) && (x as i128 * x as i128 + y as i128 * y as i128) < q2 {
                out.push(c);
            }
        }
    }
    out
}

/// Candidates from float targets (the f64 oracle's floor/ceil).
pub fn float_candidates(t: [f64; 2], q: i64) -> Vec<[i64; 2]> {
    let fl = |v: f64| v.floor() as i64;
    let ce = |v: f64| -((-v).floor() as i64);
    let q2 = q as i128 * q as i128;
    let mut out: Vec<[i64; 2]> = Vec::with_capacity(4);
    for x in [fl(t[0]), ce(t[0])] {
        for y in [fl(t[1]), ce(t[1])] {
            let c = [x, y];
            if !out.contains(&c) && (x as i128 * x as i128 + y as i128 * y as i128) < q2 {
                out.push(c);
            }
        }
    }
    out
}
