//! Scaled Darwin cycles/passages. See `ENVELOPE.md` for the derivation and error type.
pub use crate::scaled::Scalar;
use crate::{
    Error, Result,
    num::{ONE, cos},
    tables::{EDGE, PI, W, X},
};
use std::{cell::RefCell, collections::{HashMap, VecDeque}, sync::{Arc, Mutex}};

const HALF: u64 = 1 << 47;
const UNIT: u64 = 1 << 48;
const WEAK_EXPONENT: i16 = -18;
const CAP: i128 = PI / 4;
/// Coarsening measured on the frozen bound seeds and the added weak-field sweep.
/// One fewer shape bit passes G1/G2 but is not sufficient for the full weak envelope.
pub const MEMO_SHAPE_BITS: u32 = 12;
pub const MEMO_SCALE_BITS: u32 = 12;

fn f(n: i128) -> Result<Scalar> {
    Scalar::raw(n, -62)
}
fn product(a: i128, b: i128) -> i128 {
    (a * b) >> 62
}
fn square_root(a: i128) -> Result<Scalar> {
    f(a)?.sqrt()
}

/// Exact dimensionless orbit input, with an independent dimensional scale.
#[derive(Clone, Copy, Debug, Eq, PartialEq, Hash)]
pub struct OrbitKey {
    pub periapsis: Scalar,
    /// Mantissa of 1/(1+e): `k * 2^(k_exponent-48)`. Exponent zero retains Q48.
    pub k: u64,
    pub k_exponent: i16,
    /// Zero rest mass uses the same radial shape, with a null clock numerator.
    pub null: bool,
    /// The clock's gap `d = k − q(3k²+η²)` (`q` = 1/periapsis, η = 1−k) as a number with its own exponent, where the Q48 `k`
    /// cannot carry it: `E² = tn/d`, so for `E ≫ 1` the gap is `≈ q/E²`, a few quanta of `k` at `E ~ 10³` and none beyond.
    /// `None` is the gap `k` implies, the same bits as before. Only a weak-field hyperbolic key carries one
    /// ([`OrbitKey::needs_gap`]); it moves the proper clock and nothing else (positions and velocities read `k` alone).
    pub gap: Option<Scalar>,
}
impl OrbitKey {
    /// Null scattering input in M units. None means capture, with an exact predicate.
    pub fn photon(impact: Scalar) -> Result<Option<Self>> {
        crate::inverse::photon(impact)
    }
    /// Reduced binding energy E-1 and angular momentum L/M, both normalized dyadics.
    pub fn from_invariants(binding_energy: Scalar, angular: Scalar) -> Result<Self> {
        crate::inverse::invariants(binding_energy, angular)
    }
    pub fn new(periapsis: Scalar, k: u64) -> Result<Self> {
        if !periapsis.is_positive() || k == 0 || k > UNIT {
            return Err(Error::Range);
        }
        Ok(Self {
            periapsis,
            k,
            k_exponent: 0,
            null: false,
            gap: None,
        })
    }
    /// Preserve the Q48 domain bit for bit; below its relative-precision floor,
    /// move the binary point instead of rejecting the orbit. The 48-bit mantissa
    /// is normalized to [1/2,1), independently of the periapsis and clock gap.
    pub fn scaled(periapsis: Scalar, k: Scalar) -> Result<Self> {
        if !k.is_positive() || k > Scalar::ONE {
            return Err(Error::Range);
        }
        if k >= Scalar::power_of_two(-28) {
            return Self::new(periapsis, k.fixed(48)? as u64);
        }
        let exponent = k.exponent().checked_add(1).ok_or(Error::Range)?;
        let mantissa = k.scale(-(exponent as i32))?.fixed(48)? as u64;
        Ok(Self { k_exponent: exponent, ..Self::new(periapsis, mantissa)? })
    }
    pub fn shape(self) -> Result<Scalar> {
        Scalar::raw(self.k as i128, self.k_exponent as i32 - 48)
    }
    /// Whether this weak-field hyperbolic key's proper clock needs the exact gap. The weak branch's clock is first order in
    /// `q`: its numerator `√d = √k·√(1 − 2q·term)` is expanded with `term = (3k²+η²)/(2k)`, whose error is `s²/8` with
    /// `s = 2q·term`. That is below the branch's own truncation (`q² ≤ 2^-36`) while `s < 2^-16`, and
    /// above it from there on: the exact clock takes over at the point where the first-order one stops being as good as the
    /// rest of the branch. It is a pure integer predicate of the key; the two clocks agree to the branch's truncation at the
    /// switch, so a key on either side of it chatters by less than the branch resolves (no hysteresis is needed). Bound keys
    /// (`s ≤ 3q < 2^-16`) and every flyby slower than about 4×10⁻³ c never switch: their bits are unchanged.
    pub fn needs_gap(self) -> Result<bool> {
        if self.null || self.periodic() {
            return Ok(false);
        }
        let q = self.compactness()?;
        if q > Scalar::power_of_two(WEAK_EXPONENT) {
            return Ok(false);
        }
        let k = self.shape()?;
        let eta = Scalar::ONE.sub(k)?;
        let s = q.mul(k.mul(k)?.mul(Scalar::integer(3))?.add(eta.mul(eta)?)?)?.div(k)?;
        Ok(s >= Scalar::power_of_two(-16))
    }
    /// The same key with its exact gap (see [`OrbitKey::gap`]); only a weak-field hyperbolic key takes one.
    pub fn with_gap(self, gap: Scalar) -> Result<Self> {
        if self.null || self.periodic() || !gap.is_positive() || self.compactness()? > Scalar::power_of_two(WEAK_EXPONENT) {
            return Err(Error::Topology);
        }
        Ok(Self { gap: Some(gap), ..self })
    }
    /// p in M units, e in Q48. Unlike the legacy conversion, p has no absolute cap.
    pub fn bound(p: Scalar, eccentricity_q48: u64) -> Result<Self> {
        if eccentricity_q48 >= UNIT {
            return Err(Error::NoBoundOrbit);
        }
        let k = ((1u128 << 96) / (UNIT + eccentricity_q48) as u128) as u64;
        Self::new(p.mul(Scalar::raw(k as i128, -48)?)?, k)
    }
    pub fn periodic(self) -> bool {
        !self.null && self.k_exponent == 0 && self.k > HALF
    }
    pub fn memo_key(self) -> Result<Self> {
        self.quantized(MEMO_SHAPE_BITS, MEMO_SCALE_BITS)
    }
    pub fn compactness(self) -> Result<Scalar> {
        self.periapsis.reciprocal()
    }
    /// Coarsen dimensionless inputs before compiling. Never silently applied to an exact key.
    pub fn quantized(self, shape_bits: u32, scale_bits: u32) -> Result<Self> {
        if !(2..=48).contains(&shape_bits) {
            return Err(Error::Range);
        }
        // Null shape and scale are linked by b; the bound-orbit quantizer
        // cannot round them independently without changing the null metric.
        if self.null {
            return Ok(self);
        }
        Self::new(self.periapsis, self.k)?;
        if self.k_exponent != 0 {
            let mut key = Self::scaled(self.periapsis.quantize(scale_bits)?, self.shape()?.quantize(shape_bits)?)?;
            key.gap = self.gap.map(|g| g.quantize(shape_bits)).transpose()?;
            return Ok(key);
        }
        // The clock is singular at e=1. Quantize distance from that boundary,
        // not k itself: a relative quantum preserves information at every eccentricity.
        let k = if self.periodic() {
            let gap = Scalar::raw((2 * self.k - UNIT) as i128, -48)?
                .quantize(shape_bits)?
                .fixed(48)? as u64;
            (UNIT + gap) / 2
        } else {
            self.shape()?
                .quantize(shape_bits)?
                .fixed(48)? as u64
        };
        if (k > HALF) != self.periodic() || k == 0 {
            return Err(Error::Topology);
        }
        Self::new(self.periapsis.quantize(scale_bits)?, k)
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq, Hash)]
pub struct ShapeKey {
    pub k: u64,
    pub k_exponent: i16,
    /// Zero selects the Taylor coefficients at q=0. The binding retains its actual q.
    pub compactness: Scalar,
    pub null: bool,
}
impl ShapeKey {
    pub fn for_orbit(key: OrbitKey) -> Result<Self> {
        let q = key.compactness()?;
        Ok(Self {
            k: key.k,
            k_exponent: key.k_exponent,
            compactness: if !key.null && q <= Scalar::power_of_two(WEAK_EXPONENT) {
                Scalar::ZERO
            } else {
                q
            },
            null: key.null,
        })
    }
}

#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
struct Integral([Scalar; 5]);

/// Relative grid in the bound gap 2k-1; order is 1 (linear) or 3 (cubic).
#[derive(Clone, Copy, Debug, Eq, PartialEq, Hash)]
pub struct ShapeGrid { pub bits: u8, pub order: u8 }
pub const READOUT_GRID: Option<ShapeGrid> = Some(ShapeGrid { bits: 10, order: 1 });
impl Integral {
    fn add(self, rhs: Self) -> Result<Self> {
        let mut out = self;
        for i in 0..5 {
            out.0[i] = out.0[i].add(rhs.0[i])?;
        }
        Ok(out)
    }
    fn subtract(self, rhs: Self) -> Result<Self> {
        let mut out = self;
        for i in 0..5 {
            out.0[i] = out.0[i].sub(rhs.0[i])?;
        }
        Ok(out)
    }
}

/// A panel endpoint. Times are normalized by R^(3/2), never absolute Q20 values.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Knot {
    pub psi: u64,
}

// A memoized prefix is not part of the shape's identity. Readers on any thread
// fill the same immutable panel sequence, with the original left-to-right sums.
#[derive(Debug)]
struct Prefix(Mutex<Vec<Integral>>);
impl Clone for Prefix {
    fn clone(&self) -> Self { Self(Mutex::new(self.0.lock().unwrap().clone())) }
}
impl PartialEq for Prefix { fn eq(&self, _: &Self) -> bool { true } }
impl Eq for Prefix {}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct OrbitShape {
    key: ShapeKey,
    knots: Vec<Knot>,
    sums: Prefix,
    lazy: bool,
    crossings: Vec<usize>,
    k: i128,
    q: i128,
    t_numerator: Scalar,
    tau_numerator: Scalar,
    weak_tau_term: Scalar,
    floor: i128,
    fast: bool,
    word_root: bool,
    clock_shift: u32,
    clock_factor: [Scalar; 2],
}
impl OrbitShape {
    fn retained_bytes(&self) -> usize {
        std::mem::size_of::<Self>() + 2 * std::mem::size_of::<usize>()
            + self.knots.capacity() * std::mem::size_of::<Knot>()
            // Charge the largest possible prefix capacity before it grows, so
            // reads cannot exceed the cache's byte limit. Actual allocation is lazy.
            + self.knots.len().next_power_of_two().max(4) * std::mem::size_of::<Integral>()
            + self.crossings.capacity() * std::mem::size_of::<usize>()
    }
    /// Panels actually integrated so far (diagnostics only).
    pub fn integrated_panels(&self) -> usize { self.sums.0.lock().unwrap().len() - 1 }
    fn integral(&self, index: usize) -> Result<Integral> {
        if index >= self.knots.len() { return Err(Error::Range); }
        let mut sums = self.sums.0.lock().unwrap();
        while sums.len() <= index {
            let i = sums.len();
            let panel = self.quad(self.knots[i-1].psi as i128, self.knots[i].psi as i128)?;
            let next = sums[i-1].add(panel)?;
            sums.push(next);
        }
        Ok(sums[index])
    }
    fn total(&self) -> Result<Integral> { self.integral(self.knots.len() - 1) }
    pub fn key(&self) -> ShapeKey {
        self.key
    }
    pub fn knots(&self) -> &[Knot] {
        &self.knots
    }
    pub fn crossings(&self) -> &[usize] {
        &self.crossings
    }
    fn new(key: ShapeKey) -> Result<Self> {
        if (key.k == 0 && !key.null) || key.k > UNIT || key.k_exponent > 0 {
            return Err(Error::Range);
        }
        if key.compactness < Scalar::ZERO || key.compactness >= Scalar::power_of_two(-1) {
            return Err(Error::NoBoundOrbit);
        }
        let scalar_k = Scalar::raw(key.k as i128, key.k_exponent as i32 - 48)?;
        let k = scalar_k.fixed(62)?;
        let q = key.compactness.fixed(62)?;
        let eta = ONE - k;
        let d = k - product(q, product(3 * k, k) + product(eta, eta));
        // A turning orbit must be outside its separatrix; refusal is dynamical, not a size cap.
        if q < 0 || ONE - product(q, 6 * k + 2 * eta) <= 0 || (!key.null && d <= 0 && key.k_exponent == 0) {
            return Err(Error::NoBoundOrbit);
        }
        let tn = if key.null {
            ONE - 2 * q
        } else {
            product(product(k, ONE - 2 * q), ONE + product(2 * q, ONE - 2 * k))
        };
        if tn <= 0 && key.k_exponent == 0 {
            return Err(Error::NoBoundOrbit);
        }
        let floor = (2 * k - ONE).max(1);
        // Q62 resolves O(1) angular factors, but must not round away sqrt(k).
        // Tiny shapes keep both clock numerators and their ratio in scaled form.
        let t_numerator = if key.k_exponent != 0 {
            scalar_k.mul(Scalar::ONE.sub(key.compactness.scale(1)?)?)?
                .mul(Scalar::ONE.add(key.compactness.scale(1)?.mul(Scalar::ONE.sub(scalar_k.scale(1)?)?)?)?)?.sqrt()?
        } else { square_root(tn)? };
        let tau_numerator = if key.null {
            Scalar::ZERO
        } else if key.k_exponent != 0 {
            let eta = Scalar::ONE.sub(scalar_k)?;
            let d = scalar_k.sub(key.compactness.mul(scalar_k.mul(scalar_k)?.mul(Scalar::integer(3))?.add(eta.mul(eta)?)?)?)?;
            if !d.is_positive() { return Err(Error::NoBoundOrbit); }
            d.sqrt()?
        } else {
            square_root(d)?
        };
        let delta = ONE - product(q, 6 * k + 2 * eta);
        let gmax = if delta >= 1 << 30 {
            ((1u128 << 104) / crate::num::isqrt((delta as u128) << 62)) as u64
        } else {
            0
        };
        let floor2 = f(floor)?.mul(f(floor)?)?;
        Ok(Self {
            key,
            knots: vec![Knot { psi: 0 }],
            sums: Prefix(Mutex::new(vec![Integral::default()])),
            lazy: false,
            crossings: vec![],
            k,
            q,
            t_numerator,
            tau_numerator,
            weak_tau_term: if key.null {
                Scalar::ZERO
            } else if key.k_exponent != 0 {
                let eta = Scalar::ONE.sub(scalar_k)?;
                scalar_k.mul(scalar_k)?.mul(Scalar::integer(3))?.add(eta.mul(eta)?)?.div(scalar_k.scale(1)?)?
            } else {
                f(product(3 * k, k) + product(eta, eta))?.div(f(2 * k)?)?
            },
            floor,
            fast: !key.compactness.is_zero() && delta >= (1 << 30),
            word_root: !key.compactness.is_zero() && delta >= ONE / 4,
            clock_shift: 55.max(65 - gmax.leading_zeros()),
            clock_factor: [t_numerator.div(floor2)?, tau_numerator.div(floor2)?],
        })
    }
    pub(crate) fn x(&self, psi: i128) -> i128 {
        self.k + product(ONE - self.k, cos(psi))
    }
    fn node(&self, psi: i128) -> Result<Integral> {
        let cs = cos(psi);
        let x = self.k + product(ONE - self.k, cs);
        if x <= 0 {
            return Err(Error::Range);
        }
        let a = 6 * self.k + 2 * product(ONE - self.k, cs);
        let root = square_root(ONE - product(self.q, a))?;
        if !root.is_positive() {
            return Err(Error::Range);
        }
        let g = root.reciprocal()?;
        let excess = f(a)?.div(root.mul(root.add(Scalar::ONE)?)?)?;
        let x = f(x)?;
        let inv_x2 = x.mul(x)?.reciprocal()?;
        let tau = self.tau_numerator.mul(g)?.mul(inv_x2)?;
        let t = self
            .t_numerator
            .mul(g)?
            .mul(inv_x2)?
            .div(f(ONE - product(2 * self.q, self.x(psi)))?)?;
        let (dt, dtau) = if !self.key.null && self.key.compactness.is_zero() {
            (
                self.t_numerator.mul(Scalar::integer(3))?.div(x)?,
                tau.mul(f(a / 2)?.sub(self.weak_tau_term)?)?,
            )
        } else {
            (Scalar::ZERO, Scalar::ZERO)
        };
        Ok(Integral([excess, t, tau, dt, dtau]))
    }
    fn primitive(&self, psi: i128) -> Result<Integral> {
        let i = self.knots.partition_point(|k| k.psi as i128 <= psi).saturating_sub(1);
        self.integral(i)?.add(self.quad(self.knots[i].psi as i128, psi)?)
    }
    fn quad(&self, lo: i128, hi: i128) -> Result<Integral> {
        let h = hi - lo;
        if h == 0 {
            return Ok(Integral::default());
        }
        if !self.key.null && self.q == 0 && self.k >= ONE / 2 {
            return self.weak_quad(lo, hi);
        }
        if self.fast {
            return self.fast_quad(lo, hi);
        }
        let mid = lo + h / 2;
        let mut sum = Integral::default();
        for j in 0..2 {
            let dx = (X[j] * h) >> 63;
            let weight = Scalar::raw((W[j] * h) >> 63, -61)?;
            for psi in [mid - dx, mid + dx] {
                let node = self.node(psi)?;
                for i in 0..5 {
                    sum.0[i] = sum.0[i].add(weight.mul(node.0[i])?)?;
                }
            }
        }
        Ok(sum)
    }
    fn weak_quad(&self, lo: i128, hi: i128) -> Result<Integral> {
        let h = hi - lo;
        let mid = lo + h / 2;
        let mut sum = [0i128; 4];
        let term = self.weak_tau_term.fixed(62)?;
        for j in 0..2 {
            let dx = (X[j] * h) >> 63;
            let w = (W[j] * h) >> 63;
            for psi in [mid - dx, mid + dx] {
                let ac = product(ONE - self.k, cos(psi));
                let x = self.k + ac;
                let excess = 3 * self.k + ac;
                let ratio = crate::num::div_word((self.floor as u128) << 62, x as u64) as i128;
                let rtau = product(ratio, ratio);
                sum[0] += w * excess;
                sum[1] += w * rtau;
                sum[2] += w * product(rtau, 3 * x);
                sum[3] += w * product(rtau, excess - term);
            }
        }
        let base = Scalar::raw(sum[1], -123)?.mul(self.clock_factor[0])?;
        Ok(Integral([
            Scalar::raw(sum[0], -123)?,
            base,
            base,
            Scalar::raw(sum[2], -123)?.mul(self.clock_factor[0])?,
            Scalar::raw(sum[3], -123)?.mul(self.clock_factor[0])?,
        ]))
    }
    // Fixed point inside the normalized panel; the virtual point is moved only at
    // its boundary. Ratios floor/x <=1 bound every clock product independently of R.
    fn fast_quad(&self, lo: i128, hi: i128) -> Result<Integral> {
        let h = hi - lo;
        let mid = lo + h / 2;
        let mut sum = [0u128; 3];
        for j in 0..2 {
            let dx = (X[j] * h) >> 63;
            let w = ((W[j] * h) >> 63) as u64;
            for psi in [mid - dx, mid + dx] {
                let ac = product(ONE - self.k, cos(psi));
                let x = self.k + ac;
                // A node at x <= 0 lies at or beyond infinity (an unbound passage's asymptote):
                // refuse it as out of range rather than divide by zero (the certified bank's R5-05954).
                if x <= 0 {
                    return Err(Error::Range);
                }
                let a = 6 * self.k + 2 * ac;
                let denominator = ONE - product(self.q, a);
                // When sqrt(d)>=1/2 its Q31 floor has relative error <2^-30.
                // A single native u64 isqrt replaces the 126-bit square root.
                let root = if self.word_root {
                    ((denominator as u64).isqrt() as u128) << 31
                } else {
                    crate::num::isqrt((denominator as u128) << 62)
                };
                let horizon = ONE - product(2 * self.q, x);
                if root == 0 || horizon <= 0 {
                    return Err(Error::Range);
                }
                let g = ((1u128 << 104) / root) as u64;
                let g1 = (a as u128 * g as u128 / (ONE as u128 + root)) as u64;
                let ratio = ((self.floor << 62) / x) as u64;
                let rtau = ((ratio as u128 * ratio as u128) >> 62) as u64;
                let rt = (((rtau as u128) << 62) / horizon as u128) as u64;
                sum[0] += w as u128 * g1 as u128;
                let weighted = (w as u128 * g as u128) >> self.clock_shift;
                sum[1] += weighted * rt as u128;
                sum[2] += weighted * rtau as u128;
            }
        }
        Ok(Integral([
            Scalar::raw(sum[0] as i128, -103)?,
            Scalar::raw(sum[1] as i128, self.clock_shift as i32 - 165)?
                .mul(self.clock_factor[0])?,
            Scalar::raw(sum[2] as i128, self.clock_shift as i32 - 165)?
                .mul(self.clock_factor[1])?,
            Scalar::ZERO,
            Scalar::ZERO,
        ]))
    }
    fn append(&mut self, end: i128) -> Result<()> {
        let start = self.knots.last().unwrap().psi as i128;
        let eta = ONE - self.k;
        let delta = ONE - product(self.q, 6 * self.k + 2 * eta);
        let qa = product(self.q, eta);
        // The same global dyadic refinement as darwin16, now dimensionless.
        let mut cut = if qa > 0 && delta < 64 * qa {
            square_root(delta)?
                .div(square_root(qa)?)?
                .scale(-2)?
                .fixed(61)?
                .max(1)
        } else {
            PI
        };
        while cut <= start {
            cut *= 2;
        }
        let mut lo = start;
        while lo < end {
            let hi = end.min(cut);
            let n = (hi - lo + CAP - 1) / CAP;
            for i in 0..n {
                let a = lo + (hi - lo) * i / n;
                let b = lo + (hi - lo) * (i + 1) / n;
                debug_assert_eq!(self.knots.last().unwrap().psi as i128, a);
                self.knots.push(Knot { psi: b as u64 });
                if !self.lazy { self.total()?; }
            }
            lo = hi;
            cut *= 2;
        }
        Ok(())
    }
    pub(crate) fn cut(&self, x: i128) -> i128 {
        // acos((x-k)/(1-k)) via half-angle. All ratios are O(1), at every scale.
        let up = ONE;
        let ua = 2 * self.k - ONE;
        if 2 * x >= ua + up {
            crate::num::atan(crate::num::ratio_sqrt(up - x, x - ua))
        } else {
            PI - crate::num::atan(crate::num::ratio_sqrt(x - ua, up - x))
        }
    }
    fn bound(key: ShapeKey) -> Result<Self> {
        if key.k_exponent != 0 || key.k <= HALF {
            return Err(Error::NotPeriodic);
        }
        let mut s = Self::new(key)?;
        s.lazy = true;
        let xa = 2 * s.k - ONE;
        let mut band = 1usize;
        loop {
            let edge = EDGE[band % 16] >> (band / 16);
            if edge <= xa {
                break;
            }
            s.append(s.cut(edge))?;
            s.crossings.push(s.knots.len() - 1);
            band += 1;
        }
        s.append(PI)?;
        Ok(s)
    }
}

impl ShapeGrid {
    fn validate(self) -> Result<()> {
        if !(2..=47).contains(&self.bits) || ![1, 3].contains(&self.order) { return Err(Error::Range); }
        Ok(())
    }
    fn anchor(self, k: u64) -> ShapeKey {
        let gap = 2 * k - UNIT;
        let exponent = 63 - gap.leading_zeros();
        let step = 1u64 << exponent.saturating_sub(self.bits as u32).max(1);
        let anchor = (gap / step * step).max(2);
        ShapeKey { k: (UNIT + anchor) / 2, k_exponent: 0,
            compactness: Scalar::ZERO, null: false }
    }
    fn sample(self, k: u64, psi: i128) -> Result<Integral> {
        if psi == 0 { return Ok(Integral::default()); }
        let gap = 2 * k - UNIT;
        let exponent = 63 - gap.leading_zeros();
        // The Q48 domain has no finer input below a gap of two quanta.
        let step = 1u64 << exponent.saturating_sub(self.bits as u32).max(1);
        let count = self.order as usize + 1;
        let base = if self.order == 1 { gap / step * step }
            else { (gap / step).saturating_sub(1) * step };
        let base = base.max(2).min(UNIT - self.order as u64 * step);
        let mut values = [Integral::default(); 4];
        for (j, value) in values.iter_mut().enumerate().take(count) {
            let node_gap = base + j as u64 * step;
            let key = ShapeKey { k: (UNIT + node_gap) / 2, k_exponent: 0,
                compactness: Scalar::ZERO, null: false };
            let shape = SHAPE_CACHE.with(|cache| -> Result<Arc<OrbitShape>> {
                let mut cache = cache.borrow_mut();
                if let Some(shape) = cache.shapes.get(&key).cloned() {
                    cache.hits += 1;
                    return Ok(shape);
                }
                cache.misses += 1;
                let shape = Arc::new(OrbitShape::bound(key)?);
                cache.insert(shape.clone());
                Ok(shape)
            })?;
            *value = shape.primitive(psi)?;
        }
        // Newton forward polynomial, normalized dyadic x. Arithmetic and rounding
        // are fixed; cache contents and query history cannot select an answer.
        let x = Scalar::raw(gap as i128 - base as i128, -(step.trailing_zeros() as i32))?;
        let mut result = values[0];
        let mut weight = Scalar::ONE;
        for degree in 1..count {
            for j in 0..count-degree { values[j] = values[j+1].subtract(values[j])?; }
            weight = weight.mul(x.sub(Scalar::integer(degree as i64 - 1))?)?.div(Scalar::integer(degree as i64))?;
            for i in 0..5 { result.0[i] = result.0[i].add(weight.mul(values[0].0[i])?)?; }
        }
        Ok(result)
    }
}

/// Exact weak-bound table cache. These limits bound retained table bytes and metadata,
/// independently of the number of bodies and historical bindings. FIFO affects cost only.
const SHAPE_CACHE_BYTES: usize = 8 * 1024 * 1024;
const SHAPE_CACHE_ENTRIES: usize = 4096;
#[derive(Default)]
struct ShapeCache {
    shapes: HashMap<ShapeKey, Arc<OrbitShape>>,
    order: VecDeque<ShapeKey>,
    bytes: usize,
    hits: u64,
    misses: u64,
    evictions: u64,
}
impl ShapeCache {
    fn insert(&mut self, shape: Arc<OrbitShape>) {
        if self.shapes.contains_key(&shape.key) { return; }
        let bytes = shape.retained_bytes();
        if bytes > SHAPE_CACHE_BYTES { return; }
        while self.bytes + bytes > SHAPE_CACHE_BYTES || self.shapes.len() >= SHAPE_CACHE_ENTRIES {
            let key = self.order.pop_front().unwrap();
            self.bytes -= self.shapes.remove(&key).unwrap().retained_bytes();
            self.evictions += 1;
        }
        self.bytes += bytes;
        self.order.push_back(shape.key);
        self.shapes.insert(shape.key, shape);
    }
}
thread_local! { static SHAPE_CACHE: RefCell<ShapeCache> = RefCell::new(ShapeCache::default()); }
/// This thread's (tables, retained table bytes, hits, cold rebuilds, evictions).
/// Hash-map/deque capacity and transient read leases are additional; no per-body cache index.
pub fn shape_cache_stats() -> (usize, usize, u64, u64, u64) {
    SHAPE_CACHE.with(|c| { let c = c.borrow(); (c.shapes.len(), c.bytes, c.hits, c.misses, c.evictions) })
}

/// A shared shape plus a binding's scale. The catalogue pays this storage once per key.
#[derive(Clone, Debug)]
pub struct Orbit {
    key: OrbitKey,
    shape: Option<Arc<OrbitShape>>,
    grid: Option<ShapeGrid>,
    time_scale: Scalar,
    q: Scalar,
    speed_scale: Scalar,
    /// The exact proper clock of a key that carries a gap: `[√(d/k), q·term]`. The weak shape's `tau` integrals are
    /// `√k·∫(1/x²)(1 + q(a/2 − term))`, first order in `q`; with `E ≫ 1`, `q·term → 1/2` and that is not small. The exact numerator
    /// `√d` is `√k·√(d/k)`, and the first-order expansion of the rest (`g = 1/√(1−qa)`, uniformly `O(q)`) stays:
    /// `τ = √(d/k)·(i₂ + q·i₄ + q·term·i₂)`.
    clock: Option<[Scalar; 2]>,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct OrbitState {
    pub radius: Scalar,
    /// Azimuth = radial_angle + advance. Keeping the excess separate avoids cancellation.
    pub radial_angle: u64,
    pub advance: Scalar,
    pub proper_time: Scalar,
    pub radial_velocity: Scalar,
    pub transverse_velocity: Scalar,
    pub cycles: u64,
    pub outbound: bool,
    pub psi: u64,
}

impl Orbit {
    pub fn key(&self) -> OrbitKey {
        self.key
    }
    /// Lease the selected node table; the body retains its exact key separately.
    pub fn shape(&self) -> Arc<OrbitShape> {
        if let Some(shape) = &self.shape {
            return shape.clone();
        }
        // Only make_evictable can remove a table, after validating this recipe.
        let key = self.recipe();
        SHAPE_CACHE.with(|cache| {
            let mut cache = cache.borrow_mut();
            if let Some(shape) = cache.shapes.get(&key).cloned() {
                cache.hits += 1;
                return shape;
            }
            cache.misses += 1;
            let shape = Arc::new(OrbitShape::bound(key).expect("previously compiled exact bound shape"));
            cache.insert(shape.clone());
            shape
        })
    }
    /// Eviction preserves the exact key and the selected readout recipe.
    /// Shared nodes are retained once; strong cycles and passages remain pinned.
    pub fn make_evictable(&mut self) {
        let Some(shape) = &self.shape else { return };
        if !self.key.periodic() || shape.key.null || !shape.key.compactness.is_zero()
            || self.recipe() != shape.key
            || shape.retained_bytes() > SHAPE_CACHE_BYTES {
            return;
        }
        SHAPE_CACHE.with(|cache| cache.borrow_mut().insert(shape.clone()));
        self.shape = None;
    }
    /// Owned table storage only. Cached tables are charged once by shape_cache_stats.
    pub fn retained_shape_bytes(&self) -> usize {
        self.shape.as_ref().map_or(0, |s| s.retained_bytes())
    }
    fn recipe(&self) -> ShapeKey {
        self.grid.map_or(ShapeKey { k: self.key.k, k_exponent: self.key.k_exponent,
            compactness: Scalar::ZERO, null: false }, |grid| grid.anchor(self.key.k))
    }
    /// The body's key is exact. A node supplies brackets; integrals interpolate at that key.
    pub fn compile_interpolated(key: OrbitKey, grid: ShapeGrid) -> Result<Self> {
        grid.validate()?;
        if !key.periodic() || key.compactness()? > Scalar::power_of_two(WEAK_EXPONENT) {
            return Self::compile(key);
        }
        let recipe = grid.anchor(key.k);
        let shape = SHAPE_CACHE.with(|cache| -> Result<Arc<OrbitShape>> {
            let mut cache = cache.borrow_mut();
            if let Some(shape) = cache.shapes.get(&recipe).cloned() {
                cache.hits += 1;
                return Ok(shape);
            }
            cache.misses += 1;
            let shape = Arc::new(OrbitShape::bound(recipe)?);
            cache.insert(shape.clone());
            Ok(shape)
        })?;
        Self::from_shape_inner(key, shape, Some(grid))
    }
    fn integral(&self, shape: &OrbitShape, index: usize) -> Result<Integral> {
        if let Some(grid) = self.grid {
            grid.sample(self.key.k, shape.knots.get(index).ok_or(Error::Range)?.psi as i128)
        } else { shape.integral(index) }
    }
    fn total(&self) -> Result<Integral> {
        let shape = self.shape();
        self.integral(&shape, shape.knots.len() - 1)
    }
    fn geometry_k(&self, shape: &OrbitShape) -> i128 {
        if self.grid.is_some() { (self.key.k as i128) << 14 } else { shape.k }
    }
    fn geometry_x(&self, shape: &OrbitShape, psi: i128) -> i128 {
        let k = self.geometry_k(shape);
        k + product(ONE - k, cos(psi))
    }
    pub fn compile(key: OrbitKey) -> Result<Self> {
        if key.null {
            return Err(Error::NotPeriodic);
        }
        // A symbolic circle has no radial instability to integrate. The same
        // azimuth/clock readout applies on either side of the ISCO, down to r>3M.
        if key.k_exponent == 0 && key.k == UNIT && key.compactness()? >= Scalar::ONE.div(Scalar::integer(6))? {
            let q = key.compactness()?;
            if q >= Scalar::ONE.div(Scalar::integer(3))? {
                return Err(Error::NoBoundOrbit);
            }
            let mut shape = OrbitShape::bound(ShapeKey {
                k: UNIT,
                k_exponent: 0,
                compactness: Scalar::ZERO,
                null: false,
            })?;
            shape.key = ShapeKey::for_orbit(key)?;
            let rate = Scalar::ONE.sub(q.mul(Scalar::integer(3))?)?.sqrt()?;
            shape.total()?;
            *shape.sums.0.get_mut().unwrap().last_mut().unwrap() = Integral([
                Scalar::ZERO,
                Scalar::raw(PI, -61)?,
                Scalar::raw(PI, -61)?.mul(rate)?,
                Scalar::ZERO,
                Scalar::ZERO,
            ]);
            return Self::from_shape(key, Arc::new(shape));
        }
        Self::from_shape(key, Arc::new(OrbitShape::bound(ShapeKey::for_orbit(key)?)?))
    }
    /// Planted Newtonian force for the independent behaviour judge's negative control.
    pub fn newtonian(key: OrbitKey) -> Result<Self> {
        if key.null || !key.periodic() {
            return Err(Error::NotPeriodic);
        }
        let shape = Arc::new(OrbitShape::bound(ShapeKey {
            k: key.k,
            k_exponent: key.k_exponent,
            compactness: Scalar::ZERO,
            null: false,
        })?);
        let time_scale = key.periapsis.mul(key.periapsis.sqrt()?)?;
        let k = key.shape()?;
        Ok(Self {
            key,
            shape: Some(shape.clone()),
            grid: None,
            time_scale,
            q: Scalar::ZERO,
            speed_scale: key.compactness()?.div(k)?.sqrt()?,
            clock: None,
        })
    }
    fn from_shape(key: OrbitKey, shape: Arc<OrbitShape>) -> Result<Self> {
        if shape.key != ShapeKey::for_orbit(key)? {
            return Err(Error::Topology);
        }
        Self::from_shape_inner(key, shape, None)
    }
    fn from_shape_inner(key: OrbitKey, shape: Arc<OrbitShape>, grid: Option<ShapeGrid>) -> Result<Self> {
        let q = key.compactness()?;
        // Strong shapes were already validated at their actual q. For a bound
        // Taylor shape, k>1/2 and q<=2^-18 imply 1-qA>0, D>1/2-3q>0
        // and both clock factors positive. Do not rebuild and discard a shape
        // to prove those same predicates. Weak passages still need the check.
        if key.gap.is_some() && (shape.key.compactness != Scalar::ZERO || key.null || key.periodic()) {
            // A carried gap belongs to the weak branch's clock, and to nothing else.
            return Err(Error::Topology);
        }
        if shape.key.compactness != q && !key.periodic() && key.gap.is_none() {
            let _ = OrbitShape::new(ShapeKey {
                k: key.k,
                k_exponent: key.k_exponent,
                compactness: q,
                null: key.null,
            })?;
        }
        let k = key.shape()?;
        let tn = k
            .mul(Scalar::ONE.sub(q.scale(1)?)?)?
            .mul(Scalar::ONE.add(q.scale(1)?.mul(Scalar::ONE.sub(k.scale(1)?)?)?)?)?;
        // sqrt(q/D)/E = sqrt(q/[E² D]); the common D cancels.
        let speed_scale = if key.null {
            Scalar::ONE.sub(q.scale(1)?)?.sqrt()?.reciprocal()?
        } else {
            q.div(tn)?.sqrt()?
        };
        let mut orbit = Self {
            key,
            shape: Some(shape.clone()),
            grid,
            time_scale: if key.null {
                key.periapsis
            } else {
                key.periapsis.mul(key.periapsis.sqrt()?)?
            },
            q,
            speed_scale,
            clock: None,
        };
        if let Some(gap) = key.gap {
            // The gap is E's (E² = tn/d): it must be positive for E to be finite.
            if !gap.is_positive() {
                return Err(Error::NoBoundOrbit);
            }
            orbit.clock = Some([gap.div(k)?.sqrt()?, q.mul(shape.weak_tau_term)?]);
        }
        // Preserve eager validation for strong cycles and finite passages.
        if !shape.lazy { orbit.cycle_increments()?; }
        Ok(orbit)
    }
    fn time(&self, i: Integral) -> Result<Scalar> {
        i.0[1].add(self.q.mul(i.0[3])?)
    }
    fn tau(&self, i: Integral) -> Result<Scalar> {
        let first = i.0[2].add(self.q.mul(i.0[4])?)?;
        match self.clock {
            None => Ok(first),
            Some([ratio, q_term]) => ratio.mul(first.add(q_term.mul(i.0[2])?)?),
        }
    }
    fn cycle_increments(&self) -> Result<[Scalar; 3]> {
        let half = self.total()?;
        Ok([
            self.q.mul(half.0[0])?.scale(1)?,
            self.time(half)?.mul(self.time_scale)?.scale(1)?,
            self.tau(half)?.mul(self.time_scale)?.scale(1)?,
        ])
    }
    pub fn period(&self) -> Result<Scalar> { Ok(self.cycle_increments()?[1]) }
    pub fn proper_period(&self) -> Result<Scalar> { Ok(self.cycle_increments()?[2]) }
    pub fn advance(&self) -> Result<Scalar> { Ok(self.cycle_increments()?[0]) }
    pub fn crossing_time(&self, index: usize) -> Result<Scalar> {
        self.time(self.integral(&self.shape(), index)?)?
            .mul(self.time_scale)
    }
    /// A specified radial cycle and time within that cycle; no total elapsed clock needed.
    pub fn at_phase(&self, cycles: u64, normalized_time: Scalar) -> Result<OrbitState> {
        if normalized_time < Scalar::ZERO {
            return Err(Error::Range);
        }
        if self.key.k_exponent == 0 && self.key.k == UNIT && self.q >= Scalar::ONE.div(Scalar::integer(6))? {
            if normalized_time > Scalar::raw(2 * PI, -61)? {
                return Err(Error::Range);
            }
            let phi = normalized_time.fixed(61)?.rem_euclid(2 * PI) as u64;
            return Ok(OrbitState {
                radius: self.key.periapsis,
                radial_angle: phi,
                advance: Scalar::ZERO,
                proper_time: normalized_time
                    .mul(self.time_scale)?
                    .mul(Scalar::ONE.sub(self.q.mul(Scalar::integer(3))?)?.sqrt()?)?
                    .add(self.proper_period()?.mul(Scalar::raw(cycles as i128, 0)?)?)?,
                radial_velocity: Scalar::ZERO,
                transverse_velocity: self.q.sqrt()?,
                cycles,
                outbound: true,
                psi: phi,
            });
        }
        if self.prefix_covers(normalized_time)? {
            let (psi, sum) = self.outbound_at(normalized_time)?;
            return self.read(cycles, psi, true, sum);
        }
        let half = self.time(self.total()?)?;
        let full = half.scale(1)?;
        if normalized_time > full {
            return Err(Error::Range);
        }
        let outbound = normalized_time <= half;
        let target = if outbound {
            normalized_time
        } else {
            full.sub(normalized_time)?
        };
        let (psi, sum) = self.outbound_at(target)?;
        self.read(cycles, psi, outbound, sum)
    }
    pub fn state(&self, elapsed: Scalar) -> Result<OrbitState> {
        if elapsed < Scalar::ZERO {
            return Err(Error::Range);
        }
        let normalized = elapsed.div(self.time_scale)?;
        let symbolic_circle = self.key.k == UNIT && self.q >= Scalar::ONE.div(Scalar::integer(6))?;
        if !symbolic_circle && self.prefix_covers(normalized)? {
            let (psi, sum) = self.outbound_at(normalized)?;
            return self.read(0, psi, true, sum);
        }
        let period = self.time(self.total()?)?.scale(1)?;
        let cycles = u64::try_from(normalized.div(period)?.fixed(0)?).map_err(|_| Error::Range)?;
        let rem = normalized.sub(period.mul(Scalar::raw(cycles as i128, 0)?)?)?;
        self.at_phase(cycles, rem)
    }
    /// Time on either side of a periapsis. Reflection is exact in the integer law.
    pub fn signed_state(&self, elapsed: Scalar) -> Result<OrbitState> {
        let mut state = self.state(elapsed.abs())?;
        if elapsed < Scalar::ZERO {
            state.reflect();
        }
        Ok(state)
    }
    pub(crate) fn at_radius(&self, radius: Scalar) -> Result<(Scalar, OrbitState)> {
        if self.key.k_exponent == 0 && self.key.k == UNIT && self.q >= Scalar::ONE.div(Scalar::integer(6))? {
            if radius != self.key.periapsis {
                return Err(Error::Range);
            }
            return Ok((Scalar::ZERO, self.at_phase(0, Scalar::ZERO)?));
        }
        let x = self.key.periapsis.div(radius)?.fixed(62)?;
        let shape = self.shape();
        let low = self.geometry_x(&shape, shape.knots.last().unwrap().psi as i128);
        if x < low - 64 || x > ONE + 64 {
            return Err(Error::Range);
        }
        let psi = if self.key.k_exponent == 0 && self.key.k == UNIT {
            0
        } else {
            let k = self.geometry_k(&shape);
            let x = x.clamp(low, ONE);
            let ua = 2 * k - ONE;
            if 2 * x >= ua + ONE {
                crate::num::atan(crate::num::ratio_sqrt(ONE - x, x - ua))
            } else { PI - crate::num::atan(crate::num::ratio_sqrt(x - ua, ONE - x)) }
        };
        let i = shape
            .knots
            .partition_point(|k| k.psi as i128 <= psi)
            .saturating_sub(1);
        let base = &shape.knots[i];
        let sum = if let Some(grid) = self.grid { grid.sample(self.key.k, psi)? }
            else { shape.integral(i)?.add(shape.quad(base.psi as i128, psi)?)? };
        Ok((
            self.time(sum)?.mul(self.time_scale)?,
            self.read(0, psi, true, sum)?,
        ))
    }
    /// Direct table read, including velocity; no quadrature or root solve.
    pub fn crossing_state(&self, index: usize, cycles: u64, outbound: bool) -> Result<OrbitState> {
        let shape = self.shape();
        let k = shape.knots.get(index).ok_or(Error::Range)?;
        self.read(cycles, k.psi as i128, outbound, self.integral(&shape, index)?)
    }
    // Stop as soon as the requested time lies in the known outbound prefix.
    // A period is needed only after the reader actually reaches the half-cycle.
    fn prefix_covers(&self, target: Scalar) -> Result<bool> {
        let s = self.shape();
        let first = if self.grid.is_some() { s.knots.len() - 1 } else { s.integrated_panels() };
        for i in first..s.knots.len() {
            if self.time(self.integral(&s, i)?)? >= target { return Ok(true); }
        }
        Ok(false)
    }
    fn outbound_at(&self, target: Scalar) -> Result<(i128, Integral)> {
        let s = self.shape();
        let mut lo_i = 0;
        let mut hi_i = if self.grid.is_some() { s.knots.len() } else { s.integrated_panels() + 1 };
        while lo_i < hi_i {
            let mid = (lo_i + hi_i) / 2;
            if self.time(self.integral(&s, mid)?)? <= target {
                lo_i = mid + 1;
            } else {
                hi_i = mid;
            }
        }
        let index = lo_i.saturating_sub(1);
        let base = &s.knots[index];
        let base_sum = self.integral(&s, index)?;
        if self.time(base_sum)? == target || index + 1 == s.knots.len() {
            return Ok((base.psi as i128, base_sum));
        }
        let a = base.psi as i128;
        let b = s.knots[index + 1].psi as i128;
        let (mut lo, mut hi) = (a, b);
        let ta = self.time(base_sum)?;
        let tb = self.time(self.integral(&s, index + 1)?)?;
        let fraction = target.sub(ta)?.div(tb.sub(ta)?)?.fixed(61)?;
        let mut psi = a + (((b - a) * fraction) >> 61);
        // The panel clocks retain 48 weighted bits on the fast path. Do not
        // solve for phase below that clock's arithmetic information floor.
        let quantum = target
            .abs()
            .scale(if s.word_root { -36 } else { -40 })?
            .add(if s.fast {
                s.clock_factor[0].scale(s.clock_shift as i32 - 98)?
            } else {
                Scalar::ZERO
            })?;
        for iteration in 0..72 {
            let sum = if let Some(grid) = self.grid { grid.sample(self.key.k, psi)? }
                else { base_sum.add(s.quad(a, psi)?)? };
            let t = self.time(sum)?;
            if t.sub(target)?.abs() <= quantum || hi - lo <= 1 {
                return Ok((psi, sum));
            }
            if t < target {
                lo = psi;
            } else {
                hi = psi;
            }
            if iteration >= 8 {
                psi = lo + (hi - lo) / 2;
                continue;
            }
            let rate = self.time(s.node(psi)?)?;
            let step = target.sub(t)?.div(rate)?.fixed(61)?;
            let next = psi + step;
            // Accept the quantum nearest the root if Newton cannot change psi.
            if step == 0 {
                return Ok((psi, sum));
            }
            psi = if next > lo && next < hi {
                next
            } else {
                lo + (hi - lo) / 2
            };
        }
        Err(Error::Range)
    }
    fn read(&self, cycles: u64, psi: i128, outbound: bool, sum: Integral) -> Result<OrbitState> {
        let s = self.shape();
        let x = f(self.geometry_x(&s, psi))?;
        let q = self.q;
        let qx = q.mul(x)?;
        let lapse = Scalar::ONE.sub(qx.scale(1)?)?;
        let k = f(self.geometry_k(&s))?;
        let eta = Scalar::ONE.sub(k)?;
        let speed = self.speed_scale.mul(lapse)?;
        let native_k = self.geometry_k(&s);
        let a = 6 * native_k + 2 * product(ONE - native_k, cos(psi));
        let g = if s.key.compactness.is_zero() {
            Scalar::ONE.add(q.mul(f(a / 2)?)?)?
        } else {
            square_root(ONE - product(s.q, a))?.reciprocal()?
        };
        let sin = f(cos((psi - PI / 2).abs()))?;
        let mut radial = speed.mul(eta)?.mul(sin)?.div(g)?;
        if !outbound {
            radial = radial.negate();
        }
        let here = if outbound {
            sum
        } else {
            let total = self.total()?;
            total.add(total)?.subtract(sum)?
        };
        let n = Scalar::raw(cycles as i128, 0)?;
        let increments = if cycles == 0 { [Scalar::ZERO; 3] } else { self.cycle_increments()? };
        Ok(OrbitState {
            radius: self.key.periapsis.div(x)?,
            radial_angle: if outbound {
                psi as u64
            } else {
                (2 * PI - psi) as u64
            },
            advance: self.q.mul(here.0[0])?.add(increments[0].mul(n)?)?,
            proper_time: self
                .tau(here)?
                .mul(self.time_scale)?
                .add(increments[2].mul(n)?)?,
            radial_velocity: radial,
            transverse_velocity: speed.mul(x)?,
            cycles,
            outbound,
            psi: psi as u64,
        })
    }
}
impl OrbitState {
    pub(crate) fn reflect(&mut self) {
        self.radial_angle = (2 * PI - self.radial_angle as i128).rem_euclid(2 * PI) as u64;
        self.advance = self.advance.negate();
        self.proper_time = self.proper_time.negate();
        self.radial_velocity = self.radial_velocity.negate();
        self.outbound = !self.outbound;
    }
}

#[derive(Default)]
pub struct ShapeMemo {
    shapes: HashMap<ShapeKey, Arc<OrbitShape>>,
    pub hits: u64,
}
impl ShapeMemo {
    pub fn get(&mut self, key: OrbitKey) -> Result<Orbit> {
        let shape_key = ShapeKey::for_orbit(key)?;
        let shape = if let Some(s) = self.shapes.get(&shape_key) {
            self.hits += 1;
            s.clone()
        } else {
            let s = Arc::new(OrbitShape::bound(shape_key)?);
            self.shapes.insert(shape_key, s.clone());
            s
        };
        Orbit::from_shape(key, shape)
    }
    pub fn len(&self) -> usize {
        self.shapes.len()
    }
    pub fn is_empty(&self) -> bool {
        self.shapes.is_empty()
    }
}

/// Quantized bound memo input in 44 bits (stored in one u64): two implicit leading
/// bits, 11+11 fraction bits, a six-bit apoapsis-ratio exponent, a signed i16 radius
/// exponent. The shape identity drops radius altogether on the weak branch.
#[derive(Clone, Copy, Debug, Eq, PartialEq, Hash)]
pub struct MemoCode(u64);
impl MemoCode {
    pub fn encode(key: OrbitKey) -> Result<Self> {
        let key = key.memo_key()?;
        if !key.periodic() {
            return Err(Error::NotPeriodic);
        }
        let gap = Scalar::raw((2 * key.k - UNIT) as i128, -48)?;
        let fraction = |x: Scalar| ((x.significand() as u64) >> 51) & 2047;
        let bits = fraction(gap)
            | ((-gap.exponent() as u64) << 11)
            | (fraction(key.periapsis) << 17)
            | ((key.periapsis.exponent() as u16 as u64) << 28);
        Ok(Self(bits))
    }
    pub fn bits(self) -> u64 {
        self.0
    }
    pub fn decode(self) -> Result<OrbitKey> {
        let gap = Scalar::raw(
            (2048 + (self.0 & 2047)) as i128,
            -11 - ((self.0 >> 11) & 63) as i32,
        )?;
        let radius = Scalar::raw(
            (2048 + ((self.0 >> 17) & 2047)) as i128,
            ((self.0 >> 28) as u16 as i16) as i32 - 11,
        )?;
        OrbitKey::new(radius, (UNIT + gap.fixed(48)? as u64) / 2)
    }
    fn shape_bits(self) -> Result<u64> {
        if self.decode()?.compactness()? <= Scalar::power_of_two(WEAK_EXPONENT) {
            Ok((1 << 44) | (self.0 & ((1 << 17) - 1)))
        } else {
            Ok(self.0)
        }
    }
}

/// Actual eight-byte memo keys for the measured population path. Exact inputs
/// remain available through ShapeMemo; this boundary explicitly coarsens them.
#[derive(Default)]
pub struct QuantizedMemo {
    shapes: HashMap<u64, Arc<OrbitShape>>,
    pub hits: u64,
}
impl QuantizedMemo {
    pub fn with_capacity(n: usize) -> Self {
        Self {
            shapes: HashMap::with_capacity(n),
            hits: 0,
        }
    }
    pub fn get(&mut self, input: OrbitKey) -> Result<Orbit> {
        let code = MemoCode::encode(input)?;
        let key = code.decode()?;
        let bits = code.shape_bits()?;
        let shape = if let Some(s) = self.shapes.get(&bits) {
            self.hits += 1;
            s.clone()
        } else {
            let s = Arc::new(OrbitShape::bound(ShapeKey::for_orbit(key)?)?);
            self.shapes.insert(bits, s.clone());
            s
        };
        Orbit::from_shape(key, shape)
    }
    pub fn len(&self) -> usize {
        self.shapes.len()
    }
    pub fn is_empty(&self) -> bool {
        self.shapes.is_empty()
    }
}

/// An unbound geodesic over a finite radial window. Infinity has a deflection,
/// but no finite arrival time. No maximum passage radius is assumed by the compiler.
#[derive(Debug)]
struct PassageTail {
    edges: Vec<Scalar>,
    sums: Prefix,
}

#[derive(Clone, Debug)]
pub struct Passage {
    orbit: Orbit,
    pub outer_radius: Scalar,
    tail: Option<Arc<PassageTail>>,
}
impl Passage {
    /// Same shape and exponent-backed phase as massive passages; null proper time is zero.
    pub fn photon(impact: Scalar, outer_radius: Scalar) -> Result<Option<Self>> {
        OrbitKey::photon(impact)?
            .map(|key| Self::compile(key, outer_radius))
            .transpose()
    }
    pub fn compile(key: OrbitKey, outer_radius: Scalar) -> Result<Self> {
        if key.periodic() || outer_radius <= key.periapsis {
            return Err(Error::Topology);
        }
        let mut shape = OrbitShape::new(ShapeKey::for_orbit(key)?)?;
        shape.lazy = true;
        let endpoint = key.periapsis.div(outer_radius)?;
        // psi is a good phase near the turn, but cancels at infinity. Continue
        // in x=R/r with its own exponent once that cancellation matters.
        let join = Scalar::power_of_two(-10);
        let x = endpoint.max(join).fixed(62)?;
        if x <= 0 {
            return Err(Error::Range);
        } // requested endpoint is below the phase quantum
        shape.floor = x;
        let floor2 = f(x)?.mul(f(x)?)?;
        shape.clock_factor = [
            shape.t_numerator.div(floor2)?,
            shape.tau_numerator.div(floor2)?,
        ];
        let mut band = 1usize;
        loop {
            let edge = EDGE[band % 16] >> (band / 16);
            if edge <= x {
                break;
            }
            shape.append(shape.cut(edge))?;
            shape.crossings.push(shape.knots.len() - 1);
            band += 1;
        }
        shape.append(shape.cut(x))?;
        let mut edges = vec![];
        if endpoint < join {
            edges.push(join);
            let mut x = join;
            // Keep every original endpoint; only the cumulative integrals are deferred.
            while x > endpoint {
                let next = x.mul(Scalar::integer(15))?.div(Scalar::integer(16))?.max(endpoint);
                if next == x { return Err(Error::Range); }
                edges.push(next);
                x = next;
            }
        }
        Ok(Self {
            orbit: Orbit::from_shape(key, Arc::new(shape))?,
            outer_radius,
            tail: if edges.is_empty() { None } else {
                Some(Arc::new(PassageTail { edges, sums: Prefix(Mutex::new(vec![])) }))
            },
        })
    }
    pub fn key(&self) -> OrbitKey { self.orbit.key }
    /// Integrated panels, excluding endpoints that have never been read.
    pub fn integrated_panels(&self) -> usize {
        self.orbit.shape().integrated_panels() + self.tail.as_ref().map_or(0,
            |t| t.sums.0.lock().unwrap().len().saturating_sub(1))
    }
    fn tail_integral(&self, index: usize) -> Result<Integral> {
        let tail = self.tail.as_ref().ok_or(Error::Range)?;
        if index >= tail.edges.len() { return Err(Error::Range); }
        let mut sums = tail.sums.0.lock().unwrap();
        if sums.is_empty() { sums.push(self.orbit.shape().total()?); }
        while sums.len() <= index {
            let i = sums.len();
            let next = sums[i-1].add(self.tail_quad(tail.edges[i], tail.edges[i-1])?)?;
            sums.push(next);
        }
        Ok(sums[index])
    }
    pub fn at_radius(&self, radius: Scalar) -> Result<(Scalar, OrbitState)> {
        let x = self.key().periapsis.div(radius)?;
        let Some(tail) = &self.tail else { return self.orbit.at_radius(radius) };
        if x >= tail.edges[0] { return self.orbit.at_radius(radius); }
        if radius > self.outer_radius { return Err(Error::Range); }
        let i = tail.edges.partition_point(|&edge| edge >= x).saturating_sub(1);
        let base = tail.edges[i];
        let sum = self.tail_integral(i)?.add(self.tail_quad(x, base)?)?;
        Ok((self.orbit.time(sum)?.mul(self.orbit.time_scale)?, self.tail_read(x, sum)?))
    }
    /// Coordinate time between the incoming and outgoing outer-radius crossings.
    pub fn duration(&self) -> Result<Scalar> {
        if let Some(tail) = &self.tail {
            self.orbit.time(self.tail_integral(tail.edges.len()-1)?)?.mul(self.orbit.time_scale)?.scale(1)
        } else { self.orbit.period() }
    }
    /// Signed time since periapsis. Incoming times/angles/proper times are negative.
    pub fn state(&self, elapsed: Scalar) -> Result<OrbitState> {
        let t = elapsed.abs().div(self.orbit.time_scale)?;
        let mut state = if self.orbit.prefix_covers(t)? {
            let (psi, sum) = self.orbit.outbound_at(t)?;
            self.orbit.read(0, psi, true, sum)?
        } else {
            let tail = self.tail.as_ref().ok_or(Error::Range)?;
            let first = tail.sums.0.lock().unwrap().len().saturating_sub(1);
            for i in first..tail.edges.len() {
                if self.orbit.time(self.tail_integral(i)?)? >= t { break; }
            }
            let known = tail.sums.0.lock().unwrap().len();
            if self.orbit.time(self.tail_integral(known-1)?)? < t { return Err(Error::Range); }
            let (mut lo_i, mut hi_i) = (0, known);
            while lo_i < hi_i {
                let mid = (lo_i+hi_i)/2;
                if self.orbit.time(self.tail_integral(mid)?)? <= t { lo_i=mid+1; }
                else { hi_i=mid; }
            }
            let i = lo_i.saturating_sub(1);
            let (base, sum) = (tail.edges[i], self.tail_integral(i)?);
            if i + 1 == tail.edges.len() { self.tail_read(base, sum)? }
            else {
                let (mut lo, mut hi) = (tail.edges[i+1], base);
                let quantum = t.scale(-40)?;
                let mut answer = None;
                for _ in 0..80 {
                    let x = lo.add(hi)?.scale(-1)?;
                    let here = sum.add(self.tail_quad(x, base)?)?;
                    let time = self.orbit.time(here)?;
                    if time.sub(t)?.abs() <= quantum || x == lo || x == hi {
                        answer = Some(self.tail_read(x, here)?);
                        break;
                    }
                    if time > t { lo = x; } else { hi = x; }
                }
                answer.ok_or(Error::Range)?
            }
        };
        if elapsed < Scalar::ZERO { state.reflect(); }
        Ok(state)
    }
    fn tail_node(&self, x: Scalar) -> Result<Integral> {
        let s = self.orbit.shape();
        let k = f(s.k)?;
        let ua = k.scale(1)?.sub(Scalar::ONE)?;
        let slope = Scalar::ONE.sub(x)?.mul(x.sub(ua)?)?.sqrt()?;
        let a = k.scale(2)?.add(x.scale(1)?)?;
        let root = Scalar::ONE.sub(s.key.compactness.mul(a)?)?.sqrt()?;
        let g = root.reciprocal()?;
        let excess = a.div(root.mul(root.add(Scalar::ONE)?)?)?.div(slope)?;
        let inv = x.mul(x)?.reciprocal()?.div(slope)?;
        let t = s
            .t_numerator
            .mul(g)?
            .mul(inv)?
            .div(Scalar::ONE.sub(self.orbit.q.mul(x)?.scale(1)?)?)?;
        let tau = s.tau_numerator.mul(g)?.mul(inv)?;
        // Keep the same first-order weak integrands and the same shared shape.
        if !s.key.null && s.key.compactness.is_zero() {
            let dt = s.t_numerator.mul(Scalar::integer(3))?.div(x)?.div(slope)?;
            let dtau = tau.mul(a.scale(-1)?.sub(s.weak_tau_term)?)?;
            Ok(Integral([excess, t, tau, dt, dtau]))
        } else {
            Ok(Integral([excess, t, tau, Scalar::ZERO, Scalar::ZERO]))
        }
    }
    fn tail_quad(&self, lo: Scalar, hi: Scalar) -> Result<Integral> {
        let h = hi.sub(lo)?;
        if h.is_zero() {
            return Ok(Integral::default());
        }
        let mid = lo.add(hi)?.scale(-1)?;
        let mut sum = Integral::default();
        for j in 0..2 {
            let dx = h.mul(f(X[j])?)?.scale(-1)?;
            let w = h.mul(f(W[j])?)?.scale(-1)?;
            for x in [mid.sub(dx)?, mid.add(dx)?] {
                let node = self.tail_node(x)?;
                for i in 0..5 {
                    sum.0[i] = sum.0[i].add(w.mul(node.0[i])?)?;
                }
            }
        }
        Ok(sum)
    }
    fn tail_read(&self, x: Scalar, sum: Integral) -> Result<OrbitState> {
        let s = self.orbit.shape();
        let psi = s.cut(x.fixed(62)?);
        let k = f(s.k)?;
        let a = k.scale(2)?.add(x.scale(1)?)?;
        let g = if s.key.compactness.is_zero() {
            Scalar::ONE.add(self.orbit.q.mul(a.scale(-1)?)?)?
        } else {
            Scalar::ONE
                .sub(self.orbit.q.mul(a)?)?
                .sqrt()?
                .reciprocal()?
        };
        let speed = self
            .orbit
            .speed_scale
            .mul(Scalar::ONE.sub(self.orbit.q.mul(x)?.scale(1)?)?)?;
        let radial = speed
            .mul(
                Scalar::ONE
                    .sub(x)?
                    .mul(x.sub(k.scale(1)?.sub(Scalar::ONE)?)?)?
                    .sqrt()?,
            )?
            .div(g)?;
        Ok(OrbitState {
            radius: self.key().periapsis.div(x)?,
            radial_angle: psi as u64,
            advance: self.orbit.q.mul(sum.0[0])?,
            proper_time: self.orbit.tau(sum)?.mul(self.orbit.time_scale)?,
            radial_velocity: radial,
            transverse_velocity: speed.mul(x)?,
            cycles: 0,
            outbound: true,
            psi: psi as u64,
        })
    }
    /// The asymptotic total bend, evaluated without any clock integrand at infinity.
    pub fn deflection(&self) -> Result<Scalar> {
        let s = self.orbit.shape();
        if s.key.null && self.orbit.q <= Scalar::power_of_two(WEAK_EXPONENT) {
            // In q=M/R: 4q + (15π/4 - 4)q². Rationalized weak-field
            // expansion avoids subtracting two half-turns below the phase quantum.
            let q = self.orbit.q;
            let second = Scalar::raw(PI, -61)?
                .mul(Scalar::integer(15))?
                .scale(-2)?
                .sub(Scalar::integer(4))?;
            return q.mul(Scalar::integer(4))?.add(q.mul(q)?.mul(second)?);
        }
        let end = s.cut(0);
        let mut lo = 0;
        let mut sum = Scalar::ZERO;
        // Angle-only refinement uses the finite-window panel grid, extended to infinity.
        let mut edges: Vec<i128> = s.knots.iter().skip(1).map(|k| k.psi as i128).collect();
        let start = *edges.last().unwrap_or(&0);
        let n = (end - start + CAP - 1) / CAP;
        edges.extend((1..=n).map(|i| start + (end - start) * i / n));
        for hi in edges {
            let h = hi - lo;
            let mid = lo + h / 2;
            for j in 0..2 {
                let dx = (X[j] * h) >> 63;
                let weight = Scalar::raw((W[j] * h) >> 63, -61)?;
                for psi in [mid - dx, mid + dx] {
                    let a = 6 * s.k + 2 * product(ONE - s.k, cos(psi));
                    let root = square_root(ONE - product(s.q, a))?;
                    let excess = f(a)?.div(root.mul(root.add(Scalar::ONE)?)?)?;
                    sum = sum.add(weight.mul(excess)?)?;
                }
            }
            lo = hi;
        }
        Scalar::raw(2 * end - PI, -61)?.add(self.orbit.q.mul(sum)?.scale(1)?)
    }
}

#[cfg(test)]
#[path = "quadrature_tests.rs"]
mod quadrature_tests;

/// Clear this thread's memo; only reconstruction cost changes.
pub fn clear_shape_cache() { SHAPE_CACHE.with(|c| *c.borrow_mut() = ShapeCache::default()); }
