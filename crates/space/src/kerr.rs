//! Equatorial Kerr, G=c=M=1. The existing Darwin phase, factored radial cubic
//! and four-point Gauss–Legendre rule carry over. All decisions use Scalar's
//! normalized integers. No floating point, timestepping, or oracle imports.
//!
//! With x=L-aE, H(u)=(E²-μ²)+2μ²u-[L²-a²(E²-μ²)]u²+2x²u³,
//! du/dσ=±sqrt(H), dσ=u²dλ. For turning roots ua<up<uc,
//! u=c+A cos ψ cancels the first two factors, leaving
//! dσ/dψ=1/sqrt(2x²(uc-u)). The three integrands are rational
//! functions of u times this root. Finite arcs use the same rule; neither
//! infinity nor the Boyer–Lindquist horizon has a finite arrival clock.
use crate::{
    num::{atan, cos, ratio_sqrt},
    orbit::{Orbit, OrbitKey, OrbitState, Passage},
    scaled::Scalar as S,
    tables::{EDGE, PI, W, X},
    Error, Result,
};
use std::{collections::HashMap, sync::Arc};
fn n(x: i64) -> S {
    S::integer(x)
}
fn sq(x: S) -> Result<S> {
    x.mul(x)
}
fn pi() -> S {
    S::raw(PI, -61).unwrap()
}
fn mid(a: S, b: S) -> Result<S> {
    a.add(b)?.scale(-1)
}
fn bisect(mut lo: S, mut hi: S, pred: impl Fn(S) -> Result<bool>) -> Result<S> {
    for _ in 0..128 {
        let m = mid(lo, hi)?;
        if m == lo || m == hi {
            break;
        }
        if pred(m)? {
            lo = m;
        } else {
            hi = m;
        }
    }
    mid(lo, hi)
}

/// One signed spin per doll, part of every shared generator's identity.
#[derive(Clone, Copy, Debug, Default, Eq, PartialEq, Hash)]
pub struct Spin(S);
impl Spin {
    pub const ZERO: Self = Self(S::ZERO);
    pub fn new(chi: S) -> Result<Self> {
        if chi.abs() >= S::ONE {
            return Err(Error::Range);
        }
        Ok(Self(chi))
    }
    pub fn value(self) -> S {
        self.0
    }
    pub fn horizon(self) -> Result<S> {
        S::ONE.add(S::ONE.sub(sq(self.0)?)?.sqrt()?)
    }
    /// ZAMO lapse, angular velocity and circumferential radius.
    pub fn frame(self, r: S) -> Result<[S; 3]> {
        if r <= self.horizon()? {
            return Err(Error::Range);
        }
        let r2 = sq(r)?;
        let a2 = sq(self.0)?;
        let delta = r2.sub(r.scale(1)?)?.add(a2)?;
        let big = sq(r2.add(a2)?)?.sub(a2.mul(delta)?)?;
        Ok([
            r2.mul(delta)?.div(big)?.sqrt()?,
            self.0.scale(1)?.mul(r)?.div(big)?,
            big.div(r2)?.sqrt()?,
        ])
    }
    pub fn static_clock(self, r: S) -> Result<Option<S>> {
        if r <= n(2) {
            return Ok(None);
        }
        Ok(Some(S::ONE.sub(n(2).div(r)?)?.sqrt()?))
    }
    pub fn zamo_clock(self, r: S) -> Result<Option<S>> {
        if r <= self.horizon()? {
            return Ok(None);
        }
        Ok(Some(self.frame(r)?[0]))
    }
    /// Circular constants and radial stability from R''; no ISCO lookup.
    pub fn circular(self, r: S, retrograde: bool) -> Result<Option<(Constants, bool)>> {
        if r <= self.horizon()? {
            return Ok(None);
        }
        let s = if retrograde { n(-1) } else { S::ONE };
        let root = r.sqrt()?;
        let a = self.0.mul(s)?;
        let w = r.mul(root)?.sub(root.mul(n(3))?)?.add(a.scale(1)?)?;
        if !w.is_positive() {
            return Ok(None);
        }
        let den = r.mul(root)?.mul(w)?.sqrt()?;
        let e = r.mul(root)?.sub(root.scale(1)?)?.add(a)?.div(den)?;
        let l = sq(r)?
            .sub(a.scale(1)?.mul(root)?)?
            .add(sq(a)?)?
            .mul(s)?
            .div(den)?;
        let stable = sq(r)?
            .sub(r.mul(n(6))?)?
            .add(a.mul(root)?.mul(n(8))?)?
            .sub(sq(a)?.mul(n(3))?)?
            >= S::ZERO;
        Ok(Some((Constants::massive(e, l), stable)))
    }
    /// Turning-point identities solve for x²; E is recovered without dividing
    /// by spin, so the small-spin limit does not amplify cancellation.
    pub fn bound_constants(self, p: S, e: S, retrograde: bool) -> Result<Constants> {
        if !p.is_positive() || e < S::ZERO || e >= S::ONE {
            return Err(Error::Range);
        }
        if e.is_zero() {
            return self
                .circular(p, retrograde)?
                .filter(|c| c.1)
                .map(|c| c.0)
                .ok_or(Error::NoBoundOrbit);
        }
        if self == Spin::ZERO {
            let den = S::ONE.sub(n(3).add(sq(e)?)?.div(p)?)?;
            if !den.is_positive() {
                return Err(Error::NoBoundOrbit);
            }
            let l = p.div(den)?.sqrt()?;
            let binding = S::ONE
                .sub(sq(e)?)?
                .div(p)?
                .mul(S::ONE.sub(n(4).div(p)?)?)?
                .div(den)?;
            let en = S::ONE.sub(binding)?.sqrt()?;
            return Ok(Constants::massive(
                en,
                if retrograde { l.negate() } else { l },
            ));
        }
        let a = self.0;
        let ua = S::ONE.sub(e)?.div(p)?;
        let a0 = p.sub(sq(a)?)?;
        let a1 = n(3).add(sq(e)?)?.sub(p)?.div(p)?;
        let c0 = S::ONE
            .sub(ua.scale(1)?)?
            .add(sq(a)?.mul(sq(ua)?)?)?
            .add(a0.mul(sq(ua)?)?)?;
        let c1 = sq(ua)?.mul(S::ONE.add(a1)?.sub(ua.scale(1)?)?)?;
        let f = sq(a1)?.sub(sq(a)?.mul(c1)?.mul(n(4))?)?;
        let b = a0.mul(a1)?.scale(1)?.sub(sq(a)?.mul(c0)?.mul(n(4))?)?;
        let c = sq(a0)?;
        // b²-4fc = 16a²(a²c0²-a0a1c0+a0²c1). Factoring before
        // evaluation preserves the spin splitting as a approaches zero.
        let disc = sq(a)?
            .mul(sq(c0)?)?
            .sub(a0.mul(a1)?.mul(c0)?)?
            .add(c.mul(c1)?)?;
        if disc < S::ZERO || f.is_zero() {
            return Err(Error::NoBoundOrbit);
        }
        let root = a.abs().mul(disc.sqrt()?)?.mul(n(4))?;
        let q = b
            .add(if b < S::ZERO { root.negate() } else { root })?
            .scale(-1)?
            .negate();
        if q.is_zero() {
            return Err(Error::NoBoundOrbit);
        }
        let ys = [q.div(f)?, c.div(q)?];
        let with_spin = (a >= S::ZERO) != retrograde;
        let y = if !ys[0].is_positive() {
            ys[1]
        } else if !ys[1].is_positive() {
            ys[0]
        } else if with_spin {
            ys[0].min(ys[1])
        } else {
            ys[0].max(ys[1])
        };
        if !y.is_positive() {
            return Err(Error::NoBoundOrbit);
        }
        let en2 = c0.add(c1.mul(y)?)?;
        if !en2.is_positive() || en2 >= S::ONE {
            return Err(Error::NoBoundOrbit);
        }
        let en = en2.sqrt()?;
        let x = if retrograde {
            y.sqrt()?.negate()
        } else {
            y.sqrt()?
        };
        Ok(Constants::massive(en, x.add(a.mul(en)?)?))
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq, Hash)]
pub struct Constants {
    pub energy: S,
    pub angular: S,
    pub null: bool,
}
impl Constants {
    pub fn massive(energy: S, angular: S) -> Self {
        Self {
            energy,
            angular,
            null: false,
        }
    }
    pub fn photon(impact: S) -> Self {
        Self {
            energy: S::ONE,
            angular: impact,
            null: true,
        }
    }
    fn coefficients(self, spin: Spin) -> Result<[S; 4]> {
        let a = spin.0;
        let z = sq(self.energy)?.sub(if self.null { S::ZERO } else { S::ONE })?;
        let x = self.angular.sub(a.mul(self.energy)?)?;
        Ok([
            z,
            if self.null { S::ZERO } else { n(2) },
            sq(self.angular)?.sub(sq(a)?.mul(z)?)?.negate(),
            sq(x)?.scale(1)?,
        ])
    }
    pub fn radial(self, spin: Spin, u: S) -> Result<S> {
        let c = self.coefficients(spin)?;
        c[3].mul(u)?.add(c[2])?.mul(u)?.add(c[1])?.mul(u)?.add(c[0])
    }
    /// Fφ, Ft (per Mino time), with future direction tested on Ft.
    fn rates(self, spin: Spin, u: S) -> Result<[S; 2]> {
        let a = spin.0;
        let x = self.angular.sub(a.mul(self.energy)?)?;
        let u2 = sq(u)?;
        let d = S::ONE.sub(u.scale(1)?)?.add(sq(a)?.mul(u2)?)?;
        if !u.is_positive() || !d.is_positive() {
            return Err(Error::Range);
        }
        let pp = self.energy.sub(a.mul(x)?.mul(u2)?)?.div(d)?;
        Ok([
            x.add(a.mul(pp)?)?,
            a.mul(x)?
                .add(S::ONE.add(sq(a)?.mul(u2)?)?.mul(pp)?.div(u2)?)?,
        ])
    }
    pub fn tube_rates(self, spin: Spin, r: S) -> Result<Option<[S; 2]>> {
        if r <= spin.horizon()? {
            return Ok(None);
        }
        let u = r.reciprocal()?;
        let h = self.radial(spin, u)?;
        // A boundary state supplied on its turning point may round just below
        // zero. The allowance is relative to the potential's evaluated terms.
        let c = self.coefficients(spin)?;
        let scale = c[3]
            .abs()
            .mul(u)?
            .add(c[2].abs())?
            .mul(u)?
            .add(c[1].abs())?
            .mul(u)?
            .add(c[0].abs())?;
        if h < scale.scale(-48)?.negate() {
            return Ok(None);
        }
        let [phi, t] = self.rates(spin, u)?;
        if !t.is_positive() {
            return Ok(None);
        }
        Ok(Some([
            phi.div(t)?,
            if self.null { S::ZERO } else { sq(r)?.div(t)? },
        ]))
    }
    /// Local two-photon split. Backward constants are exact residuals of the
    /// incident dyadic constants; conservation never depends on two roundings.
    pub fn split(self, spin: Spin, r: S) -> Result<Option<[Self; 2]>> {
        if self.null || r <= spin.horizon()? {
            return Ok(None);
        }
        let [alpha, omega, circum] = spin.frame(r)?;
        let eps = self.energy.sub(omega.mul(self.angular)?)?.div(alpha)?;
        let p = self.angular.div(circum)?;
        if !eps.is_positive() || sq(eps)?.sub(sq(p)?)?.sub(S::ONE)?.abs() > sq(eps)?.scale(-30)? {
            return Ok(None);
        }
        let ef = eps.add(p)?.scale(-1)?;
        let lf = ef.mul(circum)?;
        let en = alpha.mul(ef)?.add(omega.mul(lf)?)?;
        Ok(Some([
            Self {
                energy: en,
                angular: lf,
                null: true,
            },
            Self {
                energy: self.energy.sub(en)?,
                angular: self.angular.sub(lf)?,
                null: true,
            },
        ]))
    }
    /// Extrema partition the exterior cubic into monotone intervals; no grid
    /// scan can miss a narrow allowed band. Roots are bisected in dyadic u.
    fn roots(self, spin: Spin) -> Result<Vec<S>> {
        let c = self.coefficients(spin)?;
        let uh = spin.horizon()?.reciprocal()?;
        let mut cuts = vec![S::ZERO];
        if c[3].is_positive() {
            let disc = sq(c[2])?.sub(c[3].mul(c[1])?.mul(n(3))?)?;
            if disc >= S::ZERO {
                let d = disc.sqrt()?;
                for u in [
                    c[2].negate().sub(d)?.div(c[3].mul(n(3))?)?,
                    c[2].negate().add(d)?.div(c[3].mul(n(3))?)?,
                ] {
                    if u > S::ZERO && u < uh {
                        cuts.push(u);
                    }
                }
            }
        } else if !c[2].is_zero() {
            let u = c[1].negate().div(c[2].scale(1)?)?;
            if u > S::ZERO && u < uh {
                cuts.push(u);
            }
        }
        cuts.push(uh);
        let mut out = Vec::new();
        for w in cuts.windows(2) {
            let (a, b) = (self.radial(spin, w[0])?, self.radial(spin, w[1])?);
            if a.is_zero() && w[0].is_positive() {
                out.push(w[0]);
            }
            if (a > S::ZERO) != (b > S::ZERO) && !a.is_zero() && !b.is_zero() {
                out.push(bisect(w[0], w[1], |u| {
                    Ok((self.radial(spin, u)? > S::ZERO) == (a > S::ZERO))
                })?);
            }
        }
        Ok(out)
    }
    pub fn fate(self, spin: Spin) -> Result<Fate> {
        let roots = self.roots(spin)?;
        if self.null || self.energy >= S::ONE {
            return Ok(if roots.is_empty() {
                Fate::Captured
            } else {
                Fate::Scattered
            });
        }
        if roots.len() >= 2 {
            let [_, t1] = self.rates(spin, roots[0])?;
            let [_, t2] = self.rates(spin, roots[1])?;
            if t1.is_positive() && t2.is_positive() {
                return Ok(Fate::Bound);
            }
        }
        Ok(Fate::Plunge)
    }
}
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Fate {
    Bound,
    Plunge,
    Scattered,
    Captured,
}

type Sum = [S; 3];
fn plus(a: Sum, b: Sum) -> Result<Sum> {
    Ok([a[0].add(b[0])?, a[1].add(b[1])?, a[2].add(b[2])?])
}
fn times(a: Sum, w: S) -> Result<Sum> {
    Ok([a[0].mul(w)?, a[1].mul(w)?, a[2].mul(w)?])
}
fn quad(lo: S, hi: S, node: &impl Fn(S) -> Result<Sum>) -> Result<Sum> {
    let h = hi.sub(lo)?.scale(-1)?;
    let m = mid(lo, hi)?;
    let mut sum = [S::ZERO; 3];
    for j in 0..2 {
        let dx = h.mul(S::raw(X[j], -62)?)?;
        let w = h.mul(S::raw(W[j], -62)?)?;
        for x in [m.sub(dx)?, m.add(dx)?] {
            sum = plus(sum, times(node(x)?, w)?)?;
        }
    }
    Ok(sum)
}
fn integrate(lo: S, hi: S, node: &impl Fn(S) -> Result<Sum>, depth: u8) -> Result<Sum> {
    let m = mid(lo, hi)?;
    let whole = quad(lo, hi, node)?;
    let split = plus(quad(lo, m, node)?, quad(m, hi, node)?)?;
    if m == lo
        || m == hi
        || (0..3).all(|i| {
            split[i]
                .sub(whole[i])
                .is_ok_and(|e| e.abs() <= split[i].abs().max(S::ONE).scale(-32).unwrap())
        })
    {
        return Ok(split);
    }
    if depth >= 24 {
        return Err(Error::Range);
    }
    plus(
        integrate(lo, m, node, depth + 1)?,
        integrate(m, hi, node, depth + 1)?,
    )
}

#[derive(Clone, Debug)]
struct Darwin {
    spin: Spin,
    constants: Constants,
    ua: S,
    up: S,
    uc: S,
    knots: Vec<(i128, Sum)>,
}
impl Darwin {
    fn node(&self, psi: S, clocks: bool) -> Result<Sum> {
        let u = mid(self.ua, self.up)?.add(
            self.up
                .sub(self.ua)?
                .scale(-1)?
                .mul(S::raw(cos(psi.fixed(61)?), -62)?)?,
        )?;
        let x = self
            .constants
            .angular
            .sub(self.spin.0.mul(self.constants.energy)?)?;
        let w = sq(x)?
            .scale(1)?
            .mul(self.uc.sub(u)?)?
            .sqrt()?
            .reciprocal()?;
        if clocks {
            let [p, t] = self.constants.rates(self.spin, u)?;
            if !t.is_positive() {
                return Err(Error::NoBoundOrbit);
            }
            Ok([
                p.mul(w)?,
                t.mul(w)?,
                if self.constants.null {
                    S::ZERO
                } else {
                    w.div(sq(u)?)?
                },
            ])
        } else {
            // Fφ is regular at infinity; evaluate its u-form without Ft/u².
            let a = self.spin.0;
            let d = S::ONE.sub(u.scale(1)?)?.add(sq(a)?.mul(sq(u)?)?)?;
            Ok([
                x.add(a.mul(self.constants.energy.sub(a.mul(x)?.mul(sq(u)?)?)?.div(d)?)?)?
                    .mul(w)?,
                S::ZERO,
                S::ZERO,
            ])
        }
    }
    fn sum(&self, a: i128, b: i128, clocks: bool) -> Result<Sum> {
        integrate(
            S::raw(a, -61)?,
            S::raw(b, -61)?,
            &|p| self.node(p, clocks),
            0,
        )
    }
    fn cut(&self, u: S) -> Result<i128> {
        let num = self.up.sub(u)?;
        let den = u.sub(self.ua)?;
        let exp = num.exponent().max(den.exponent()) as i32;
        let a = num.fixed(62 - exp)?;
        let b = den.fixed(62 - exp)?;
        Ok(if a <= b {
            atan(ratio_sqrt(a, b))
        } else {
            PI - atan(ratio_sqrt(b, a))
        })
    }
    fn build(spin: Spin, constants: Constants, ua: S, up: S, end: i128) -> Result<Self> {
        let c = constants.coefficients(spin)?;
        if !c[3].is_positive() {
            return Err(Error::Range);
        }
        let uc = c[2].negate().div(c[3])?.sub(ua)?.sub(up)?;
        if uc <= up || up.reciprocal()? <= spin.horizon()? {
            return Err(Error::NoBoundOrbit);
        }
        let mut d = Self {
            spin,
            constants,
            ua,
            up,
            uc,
            knots: vec![(0, [S::ZERO; 3])],
        };
        // Same geometric band cuts as the native compiler, normalized to up.
        let mut cuts = vec![end];
        for band in 1..1024 {
            let ratio = S::raw(EDGE[band % 16], -62)?.scale(-(band as i32 / 16))?;
            let u = up.mul(ratio)?;
            if u <= ua || u <= S::ZERO {
                break;
            }
            let cut = d.cut(u)?;
            if cut >= end {
                break;
            }
            cuts.push(cut);
        }
        cuts.sort_unstable();
        cuts.dedup();
        for cut in cuts {
            let (lo, sum) = *d.knots.last().unwrap();
            d.knots.push((cut, plus(sum, d.sum(lo, cut, true)?)?));
        }
        Ok(d)
    }
    fn at_time(&self, t: S) -> Result<(i128, Sum)> {
        let i = self
            .knots
            .partition_point(|k| k.1[1] <= t)
            .saturating_sub(1);
        let (base, sum) = self.knots[i];
        if sum[1] == t || i + 1 == self.knots.len() {
            return Ok((base, sum));
        }
        let (mut lo, mut hi) = (base, self.knots[i + 1].0);
        for _ in 0..64 {
            let p = (lo + hi) / 2;
            let here = plus(sum, self.sum(base, p, true)?)?;
            if p == lo || p == hi || here[1].sub(t)?.abs() <= t.abs().max(S::ONE).scale(-32)? {
                return Ok((p, here));
            }
            if here[1] < t {
                lo = p;
            } else {
                hi = p;
            }
        }
        Err(Error::Range)
    }
    fn read(&self, psi: i128, sum: Sum, outbound: bool, cycles: u64) -> Result<OrbitState> {
        let u = mid(self.ua, self.up)?.add(
            self.up
                .sub(self.ua)?
                .scale(-1)?
                .mul(S::raw(cos(psi), -62)?)?,
        )?;
        let [p, t] = self.constants.rates(self.spin, u)?;
        let c = self.constants.coefficients(self.spin)?;
        let h = c[3]
            .mul(u.sub(self.ua)?)?
            .mul(self.up.sub(u)?)?
            .mul(self.uc.sub(u)?)?;
        let radial = h.max(S::ZERO).sqrt()?.div(t.mul(sq(u)?)?)?;
        let sense = if self.constants.angular < S::ZERO {
            -1
        } else {
            1
        };
        let angle = if outbound { psi } else { 2 * PI - psi };
        Ok(OrbitState {
            radius: u.reciprocal()?,
            radial_angle: (sense * angle).rem_euclid(2 * PI) as u64,
            advance: sum[0].sub(S::raw(sense * angle, -61)?)?,
            proper_time: sum[2],
            radial_velocity: if outbound { radial } else { radial.negate() },
            transverse_velocity: p.div(t.mul(u)?)?,
            cycles,
            outbound,
            psi: psi as u64,
        })
    }
}

/// Shared cycle. Zero spin uses the existing compiled Orbit without re-rounding.
#[derive(Clone, Debug)]
pub struct Cycle {
    spin: Spin,
    constants: Constants,
    kind: CycleKind,
}
#[derive(Clone, Debug)]
enum CycleKind {
    Schwarzschild(Orbit, bool),
    Kerr(Darwin),
}
impl Cycle {
    pub fn spin(&self) -> Spin {
        self.spin
    }
    pub fn constants(&self) -> Constants {
        self.constants
    }
    pub fn bound(spin: Spin, p: S, e_q48: u64, retrograde: bool) -> Result<Self> {
        let e = S::raw(e_q48 as i128, -48)?;
        if spin == Spin::ZERO {
            let o = Orbit::compile(OrbitKey::bound(p, e_q48)?)?;
            let c = spin.bound_constants(p, e, retrograde)?;
            return Ok(Self {
                spin,
                constants: c,
                kind: CycleKind::Schwarzschild(o, retrograde),
            });
        }
        let c = spin.bound_constants(p, e, retrograde)?;
        let up = S::ONE.add(e)?.div(p)?;
        let ua = S::ONE.sub(e)?.div(p)?;
        Ok(Self {
            spin,
            constants: c,
            kind: CycleKind::Kerr(Darwin::build(spin, c, ua, up, PI)?),
        })
    }
    pub fn from_constants(spin: Spin, c: Constants) -> Result<Self> {
        if c.null || c.fate(spin)? != Fate::Bound {
            return Err(Error::NoBoundOrbit);
        }
        let roots = c.roots(spin)?;
        let (ua, up) = (roots[0], roots[1]);
        if spin == Spin::ZERO {
            let key = OrbitKey::new(
                up.reciprocal()?,
                up.add(ua)?.div(up.scale(1)?)?.fixed(48)? as u64,
            )?;
            return Ok(Self {
                spin,
                constants: c,
                kind: CycleKind::Schwarzschild(Orbit::compile(key)?, c.angular < S::ZERO),
            });
        }
        Ok(Self {
            spin,
            constants: c,
            kind: CycleKind::Kerr(Darwin::build(spin, c, ua, up, PI)?),
        })
    }
    pub fn advance(&self) -> Result<S> {
        match &self.kind {
            CycleKind::Schwarzschild(o, _) => o.advance(),
            CycleKind::Kerr(d) => d.knots.last().unwrap().1[0]
                .abs()
                .scale(1)?
                .sub(pi().scale(1)?),
        }
    }
    pub fn period(&self) -> Result<S> {
        match &self.kind {
            CycleKind::Schwarzschild(o, _) => o.period(),
            CycleKind::Kerr(d) => d.knots.last().unwrap().1[1].scale(1),
        }
    }
    pub fn proper_period(&self) -> Result<S> {
        match &self.kind {
            CycleKind::Schwarzschild(o, _) => o.proper_period(),
            CycleKind::Kerr(d) => d.knots.last().unwrap().1[2].scale(1),
        }
    }
    pub fn state(&self, elapsed: S) -> Result<OrbitState> {
        if elapsed < S::ZERO {
            return Err(Error::Range);
        }
        match &self.kind {
            CycleKind::Schwarzschild(o, retro) => {
                let mut s = o.state(elapsed)?;
                if *retro {
                    s.radial_angle = (2 * PI - s.radial_angle as i128).rem_euclid(2 * PI) as u64;
                    s.advance = s.advance.negate();
                    s.transverse_velocity = s.transverse_velocity.negate();
                }
                Ok(s)
            }
            CycleKind::Kerr(d) => {
                let period = self.period()?;
                let cycles = u64::try_from(elapsed.div(period)?.fixed_floor(0)?)
                    .map_err(|_| Error::Range)?;
                let count = S::raw(cycles as i128, 0)?;
                let t = elapsed.sub(period.mul(count)?)?;
                let half = period.scale(-1)?;
                let outbound = t <= half;
                let (psi, mut sum) = d.at_time(if outbound { t } else { period.sub(t)? })?;
                let total = d.knots.last().unwrap().1;
                if !outbound {
                    for i in 0..3 {
                        sum[i] = total[i].scale(1)?.sub(sum[i])?;
                    }
                }
                let mut s = d.read(psi, sum, outbound, cycles)?;
                let sign = if self.constants.angular < S::ZERO {
                    n(-1)
                } else {
                    S::ONE
                };
                s.advance = s.advance.add(self.advance()?.mul(count)?.mul(sign)?)?;
                s.proper_time = s.proper_time.add(self.proper_period()?.mul(count)?)?;
                Ok(s)
            }
        }
    }
}

/// Signed impact parameter; captured rays return None. Angle at infinity is
/// integrated separately from clocks, which are undefined there.
pub fn deflection(spin: Spin, impact: S) -> Result<Option<S>> {
    if spin == Spin::ZERO {
        let b = impact.abs();
        return Passage::photon(b, b.scale(1)?)?
            .map(|p| p.deflection())
            .transpose();
    }
    let c = Constants::photon(impact);
    let roots = c.roots(spin)?;
    if roots.len() < 2 {
        return Ok(None);
    }
    let up = roots[0];
    // Remaining two roots of H/(u-up), from Vieta with a stable quadratic.
    let coeff = c.coefficients(spin)?;
    let sum = coeff[2].negate().div(coeff[3])?.sub(up)?;
    let prod = coeff[0].negate().div(coeff[3].mul(up)?)?;
    let disc = sq(sum)?.sub(prod.mul(n(4))?)?.sqrt()?;
    let ua = sum.sub(disc)?.scale(-1)?;
    let uc = sum.add(disc)?.scale(-1)?;
    let d = Darwin {
        spin,
        constants: c,
        ua,
        up,
        uc,
        knots: Vec::new(),
    };
    let end = d.cut(S::ZERO)?;
    let angle = d.sum(0, end, false)?[0].abs().scale(1)?.sub(pi())?;
    Ok(Some(angle))
}

/// Exact memo identity includes spin, sense and both invariants. No orientation
/// or epoch in the shared generator. Per-body Tube remains 16 bytes.
#[derive(Default)]
pub struct Memo {
    cycles: HashMap<(Spin, S, u64, bool), Arc<Cycle>>,
}
impl Memo {
    pub fn bound(&mut self, spin: Spin, p: S, e_q48: u64, retrograde: bool) -> Result<Arc<Cycle>> {
        let key = (spin, p, e_q48, retrograde);
        if let Some(c) = self.cycles.get(&key) {
            return Ok(c.clone());
        }
        let c = Arc::new(Cycle::bound(spin, p, e_q48, retrograde)?);
        self.cycles.insert(key, c.clone());
        Ok(c)
    }
    pub fn len(&self) -> usize {
        self.cycles.len()
    }
    pub fn is_empty(&self) -> bool {
        self.cycles.is_empty()
    }
}

/// A windowed radial arc. Endpoint turning roots are cancelled algebraically
/// in r=r_turn±span*z². A segment never invents a horizon arrival time.
#[derive(Clone, Debug)]
pub struct ArcSegment {
    spin: Spin,
    constants: Constants,
    origin: S,
    span: S,
    decreasing: bool,
    reverse: bool,
    root: Option<S>,
    knots: Vec<(S, Sum)>,
}
impl ArcSegment {
    pub fn spin(&self) -> Spin {
        self.spin
    }
    pub fn constants(&self) -> Constants {
        self.constants
    }
    /// Compile a future-directed segment from start to end. Both are finite
    /// exterior radii; turning endpoints may be supplied from `turning_radii`.
    pub fn compile(spin: Spin, constants: Constants, start: S, end: S) -> Result<Self> {
        if start == end || start.min(end) <= spin.horizon()? {
            return Err(Error::Range);
        }
        let roots = constants.roots(spin)?;
        let roots: Vec<_> = roots
            .into_iter()
            .map(|u| u.reciprocal())
            .collect::<Result<_>>()?;
        let close = |r: S, q: S| {
            r.sub(q)
                .is_ok_and(|d| d.abs() <= q.abs().scale(-44).unwrap())
        };
        let start_root = roots.iter().copied().find(|&r| close(start, r));
        let end_root = roots.iter().copied().find(|&r| close(end, r));
        // Regularize at a turning endpoint, otherwise start at the lower r.
        let (origin, other, reverse) = if let Some(r) = start_root {
            (r, end, false)
        } else if let Some(r) = end_root {
            (r, start, true)
        } else {
            (start.min(end), start.max(end), start > end)
        };
        if roots.iter().any(|&r| {
            r > start.min(end) && r < start.max(end) && !close(r, start) && !close(r, end)
        }) {
            return Err(Error::Topology);
        }
        let root = if start_root.is_some() || end_root.is_some() {
            Some(origin.reciprocal()?)
        } else {
            None
        };
        let mut s = Self {
            spin,
            constants,
            origin,
            span: other.sub(origin)?.abs(),
            decreasing: other < origin,
            reverse,
            root,
            knots: vec![(S::ZERO, [S::ZERO; 3])],
        };
        for i in 1..=16 {
            let z = n(i).div(n(16))?;
            let (lo, sum) = *s.knots.last().unwrap();
            s.knots.push((z, plus(sum, s.integral(lo, z)?)?));
        }
        Ok(s)
    }
    pub fn turning_radii(spin: Spin, constants: Constants) -> Result<Vec<S>> {
        constants
            .roots(spin)?
            .into_iter()
            .map(|u| u.reciprocal())
            .collect()
    }
    fn radius(&self, z: S) -> Result<S> {
        let d = self.span.mul(sq(z)?)?;
        if self.decreasing {
            self.origin.sub(d)
        } else {
            self.origin.add(d)
        }
    }
    fn radial(&self, u: S) -> Result<S> {
        if let Some(root) = self.root {
            let c = self.constants.coefficients(self.spin)?;
            // H(u)-H(root), with H(root)=0 by this generator's root definition.
            let b = c[1]
                .add(c[2].mul(u.add(root)?)?)?
                .add(c[3].mul(sq(u)?.add(u.mul(root)?)?.add(sq(root)?)?)?)?;
            u.sub(root)?.mul(b)
        } else {
            self.constants.radial(self.spin, u)
        }
    }
    fn node(&self, z: S) -> Result<Sum> {
        let r = self.radius(z)?;
        let u = r.reciprocal()?;
        let h = self.radial(u)?;
        if !h.is_positive() {
            return Err(Error::Range);
        }
        let jac = self.span.scale(1)?.mul(z)?.div(h.sqrt()?)?.mul(sq(u)?)?;
        let [phi, t] = self.constants.rates(self.spin, u)?;
        if !t.is_positive() {
            return Err(Error::Range);
        }
        Ok([
            phi.mul(jac)?,
            t.mul(jac)?,
            if self.constants.null {
                S::ZERO
            } else {
                jac.div(sq(u)?)?
            },
        ])
    }
    fn integral(&self, lo: S, hi: S) -> Result<Sum> {
        integrate(lo, hi, &|z| self.node(z), 0)
    }
    pub fn duration(&self) -> S {
        self.knots.last().unwrap().1[1]
    }
    pub fn proper_duration(&self) -> S {
        self.knots.last().unwrap().1[2]
    }
    pub fn angle(&self) -> S {
        self.knots.last().unwrap().1[0]
    }
    pub fn state(&self, elapsed: S) -> Result<OrbitState> {
        if elapsed < S::ZERO || elapsed > self.duration() {
            return Err(Error::Range);
        }
        let target = if self.reverse {
            self.duration().sub(elapsed)?
        } else {
            elapsed
        };
        let i = self
            .knots
            .partition_point(|k| k.1[1] <= target)
            .saturating_sub(1);
        let (base, sum) = self.knots[i];
        let (z, mut here) = if sum[1] == target || i + 1 == self.knots.len() {
            (base, sum)
        } else {
            let (mut lo, mut hi) = (base, self.knots[i + 1].0);
            let mut answer = None;
            for _ in 0..64 {
                let z = mid(lo, hi)?;
                let h = plus(sum, self.integral(base, z)?)?;
                if z == lo
                    || z == hi
                    || h[1].sub(target)?.abs() <= target.abs().max(S::ONE).scale(-32)?
                {
                    answer = Some((z, h));
                    break;
                }
                if h[1] < target {
                    lo = z;
                } else {
                    hi = z;
                }
            }
            answer.ok_or(Error::Range)?
        };
        if self.reverse {
            for i in 0..3 {
                here[i] = self.knots.last().unwrap().1[i].sub(here[i])?;
            }
        }
        let r = self.radius(z)?;
        let u = r.reciprocal()?;
        let [phi, t] = self.constants.rates(self.spin, u)?;
        let vr = self.radial(u)?.max(S::ZERO).sqrt()?.div(t.mul(sq(u)?)?)?;
        let outbound = self.decreasing == self.reverse;
        Ok(OrbitState {
            radius: r,
            radial_angle: 0,
            advance: here[0],
            proper_time: here[2],
            radial_velocity: if outbound { vr } else { vr.negate() },
            transverse_velocity: phi.div(t.mul(u)?)?,
            cycles: 0,
            outbound,
            psi: 0,
        })
    }
}

/// A turning passage consists of the incoming and outgoing halves of one
/// generator. No radial steps are taken between queries.
#[derive(Clone, Debug)]
pub struct TurningPassage {
    out: ArcSegment,
}
impl TurningPassage {
    pub fn compile(spin: Spin, c: Constants, outer: S) -> Result<Self> {
        if c.fate(spin)? != Fate::Scattered {
            return Err(Error::NoBoundOrbit);
        }
        let peri = c
            .roots(spin)?
            .first()
            .copied()
            .ok_or(Error::NoBoundOrbit)?
            .reciprocal()?;
        Ok(Self {
            out: ArcSegment::compile(spin, c, peri, outer)?,
        })
    }
    pub fn duration(&self) -> Result<S> {
        self.out.duration().scale(1)
    }
    pub fn state(&self, elapsed: S) -> Result<OrbitState> {
        let half = self.out.duration();
        if elapsed < S::ZERO || elapsed > self.duration()? {
            return Err(Error::Range);
        }
        if elapsed <= half {
            let mut s = self.out.state(half.sub(elapsed)?)?;
            s.advance = self.out.angle().sub(s.advance)?;
            s.proper_time = self.out.proper_duration().sub(s.proper_time)?;
            s.radial_velocity = s.radial_velocity.negate();
            s.outbound = false;
            Ok(s)
        } else {
            let mut s = self.out.state(elapsed.sub(half)?)?;
            s.advance = self.out.angle().add(s.advance)?;
            s.proper_time = self.out.proper_duration().add(s.proper_time)?;
            Ok(s)
        }
    }
}

/// The same 16-byte Tube handle indexes shared cycles, passages or plunges.
/// Kerr catalogue is additive: the events owner's Schwarzschild catalogue
/// and plane remain compatible until their motion contract supports spin.
#[derive(Clone, Debug)]
pub enum Generator {
    Cycle(Arc<Cycle>),
    Passage(TurningPassage),
    Arc(ArcSegment),
}
impl Generator {
    pub fn state(&self, time: S) -> Result<OrbitState> {
        match self {
            Self::Cycle(c) => c.state(time),
            Self::Passage(p) => p.state(time),
            Self::Arc(a) => a.state(time),
        }
    }
}
#[derive(Default)]
pub struct Catalogue {
    entries: Vec<Generator>,
}
impl Catalogue {
    pub fn insert(&mut self, g: Generator) -> Result<u32> {
        let id = u32::try_from(self.entries.len()).map_err(|_| Error::Range)?;
        self.entries.push(g);
        Ok(id)
    }
    pub fn state(&self, tube: crate::Tube, time: i64, clock_exponent: i16) -> Result<OrbitState> {
        let elapsed = S::raw(
            time as i128 - tube.periapsis_time.get() as i64 as i128,
            clock_exponent as i32,
        )?;
        let mut s = self
            .entries
            .get(tube.key as usize)
            .ok_or(Error::Range)?
            .state(elapsed)?;
        s.radial_angle = (s.radial_angle as i128 + ((tube.periapsis_angle as i128 * 2 * PI) >> 32))
            .rem_euclid(2 * PI) as u64;
        Ok(s)
    }
    pub fn len(&self) -> usize {
        self.entries.len()
    }
    pub fn is_empty(&self) -> bool {
        self.entries.is_empty()
    }
}
