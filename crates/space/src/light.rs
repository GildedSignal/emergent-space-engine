//! Null capture in the same normalized units as turning passages. The radial
//! phase is r/b with an exponent; Schwarzschild time has no finite horizon value.
use crate::{
    Error, Result,
    orbit::{OrbitKey, OrbitState, Scalar},
    tables::{W, X},
};

#[derive(Clone, Debug)]
pub struct Capture {
    pub impact: Scalar,
    scale: Scalar,
    knots: Vec<(Scalar, [Scalar; 2])>,
}
impl Capture {
    /// Compile inward from outer to inner, both strictly outside the horizon.
    /// None means this input has a turning point and belongs to Passage instead.
    pub fn compile(impact: Scalar, outer: Scalar, inner: Scalar) -> Result<Option<Self>> {
        if OrbitKey::photon(impact)?.is_some() {
            return Ok(None);
        }
        if inner <= Scalar::integer(2) || outer <= inner {
            return Err(Error::Range);
        }
        let scale = if impact.is_positive() {
            impact
        } else {
            Scalar::ONE
        };
        let mut c = Self {
            impact,
            scale,
            knots: vec![(outer.div(scale)?, [Scalar::ZERO; 2])],
        };
        let end = inner.div(scale)?;
        let special = Scalar::integer(3).div(scale)?;
        while c.knots.last().unwrap().0 > end {
            let (hi, sum) = *c.knots.last().unwrap();
            let mut lo = hi
                .mul(Scalar::integer(15))?
                .div(Scalar::integer(16))?
                .max(end);
            if hi > special && lo < special {
                lo = special;
            }
            if hi == lo {
                return Err(Error::Range);
            }
            let a = c.integrate(lo, hi, 0)?;
            c.knots.push((lo, [sum[0].add(a[0])?, sum[1].add(a[1])?]));
        }
        Ok(Some(c))
    }
    fn node(&self, phase: Scalar) -> Result<[Scalar; 2]> {
        let r = phase.mul(self.scale)?;
        let lapse = Scalar::ONE.sub(Scalar::integer(2).div(r)?)?;
        let b_r = self.impact.div(r)?;
        let radial = Scalar::ONE.sub(lapse.mul(b_r.mul(b_r)?)?)?.sqrt()?;
        if !lapse.is_positive() || !radial.is_positive() {
            return Err(Error::Range);
        }
        Ok([
            b_r.div(phase)?.div(radial)?,
            lapse.mul(radial)?.reciprocal()?,
        ])
    }
    fn quad(&self, lo: Scalar, hi: Scalar) -> Result<[Scalar; 2]> {
        let h = hi.sub(lo)?;
        let mid = lo.add(hi)?.scale(-1)?;
        let mut sum = [Scalar::ZERO; 2];
        for j in 0..2 {
            let dx = h.mul(Scalar::raw(X[j], -62)?)?.scale(-1)?;
            let w = h.mul(Scalar::raw(W[j], -62)?)?.scale(-1)?;
            for x in [mid.sub(dx)?, mid.add(dx)?] {
                let n = self.node(x)?;
                for i in 0..2 {
                    sum[i] = sum[i].add(w.mul(n[i])?)?;
                }
            }
        }
        Ok(sum)
    }
    fn integrate(&self, lo: Scalar, hi: Scalar, depth: u8) -> Result<[Scalar; 2]> {
        let mid = lo.add(hi)?.scale(-1)?;
        if lo == mid || hi == mid {
            return self.quad(lo, hi);
        }
        let whole = self.quad(lo, hi)?;
        let a = self.quad(lo, mid)?;
        let b = self.quad(mid, hi)?;
        let split = [a[0].add(b[0])?, a[1].add(b[1])?];
        if (0..2).all(|i| {
            split[i]
                .sub(whole[i])
                .is_ok_and(|e| e.abs() <= split[i].abs().scale(-32).unwrap_or(Scalar::ZERO))
        }) {
            return Ok(split);
        }
        if depth == 56 {
            return Err(Error::Range);
        }
        let a = self.integrate(lo, mid, depth + 1)?;
        let b = self.integrate(mid, hi, depth + 1)?;
        Ok([a[0].add(b[0])?, a[1].add(b[1])?])
    }
    pub fn duration(&self) -> Result<Scalar> {
        self.knots.last().unwrap().1[1].mul(self.scale)
    }
    /// Pure readout at elapsed coordinate time from the incoming outer crossing.
    pub fn state(&self, elapsed: Scalar) -> Result<OrbitState> {
        let t = elapsed.div(self.scale)?;
        if t < Scalar::ZERO || elapsed > self.duration()? {
            return Err(Error::Range);
        }
        let i = self
            .knots
            .partition_point(|k| k.1[1] <= t)
            .saturating_sub(1);
        let (base, sum) = self.knots[i];
        let (x, sum) = if sum[1] == t || i + 1 == self.knots.len() {
            (base, sum)
        } else {
            let (mut lo, mut hi) = (self.knots[i + 1].0, base);
            let mut answer = None;
            for _ in 0..80 {
                let x = lo.add(hi)?.scale(-1)?;
                let a = self.integrate(x, base, 0)?;
                let here = [sum[0].add(a[0])?, sum[1].add(a[1])?];
                if here[1].sub(t)?.abs() <= t.scale(-30)? || x == lo || x == hi {
                    answer = Some((x, here));
                    break;
                }
                if here[1] > t {
                    lo = x;
                } else {
                    hi = x;
                }
            }
            answer.ok_or(Error::Range)?
        };
        let r = x.mul(self.scale)?;
        let lapse = Scalar::ONE.sub(Scalar::integer(2).div(r)?)?;
        let br = self.impact.div(r)?;
        let vr = lapse
            .mul(Scalar::ONE.sub(lapse.mul(br.mul(br)?)?)?.sqrt()?)?
            .negate();
        Ok(OrbitState {
            radius: r,
            radial_angle: 0,
            advance: sum[0],
            proper_time: Scalar::ZERO,
            radial_velocity: vr,
            transverse_velocity: lapse.mul(br)?,
            cycles: 0,
            outbound: false,
            psi: 0,
        })
    }
}

/// Lorentz transformation of a light direction into the frame moving at beta
/// along +x. The formula is exact SR; only integer arithmetic rounding remains.
pub fn aberrate(direction: [Scalar; 2], beta: Scalar) -> Result<[Scalar; 2]> {
    let root = Scalar::ONE.sub(beta.mul(beta)?)?.sqrt()?;
    if !root.is_positive() {
        return Err(Error::Range);
    }
    let den = Scalar::ONE.sub(beta.mul(direction[0])?)?;
    Ok([
        direction[0].sub(beta)?.div(den)?,
        direction[1].mul(root)?.div(den)?,
    ])
}
/// Bend in the lens's doll and transform back to the observer. b is signed;
/// direction trigonometry uses Q61 radians; the returned bend retains its exponent.
pub fn moving_deflection(direction: [Scalar; 2], beta: Scalar, impact: Scalar) -> Result<Scalar> {
    use crate::{num::ONE, num::cos, orbit::Passage, tables::PI};
    let incoming = aberrate(direction, beta)?;
    let p = Passage::photon(impact.abs(), impact.abs().scale(1)?)?.ok_or(Error::NoBoundOrbit)?;
    let bend = p.deflection()?;
    let (cs, mut sn, cm1) = if bend.abs() <= Scalar::power_of_two(-20) {
        // Retain a bend below a fixed angle word, including its cosine excess.
        let b2 = bend.mul(bend)?;
        let sn = bend.sub(bend.mul(b2)?.div(Scalar::integer(6))?)?;
        let cm1 = b2
            .scale(-1)?
            .negate()
            .add(b2.mul(b2)?.div(Scalar::integer(24))?)?;
        (Scalar::ONE.add(cm1)?, sn, cm1)
    } else {
        let angle = bend.fixed(61)?.rem_euclid(2 * PI);
        let cs = Scalar::raw(cos(if angle <= PI { angle } else { 2 * PI - angle }), -62)?;
        let sin_angle = (PI / 2 - angle).rem_euclid(2 * PI);
        let sn = Scalar::raw(
            cos(if sin_angle <= PI {
                sin_angle
            } else {
                2 * PI - sin_angle
            }),
            -62,
        )?;
        (cs, sn, cs.sub(Scalar::ONE)?)
    };
    if impact < Scalar::ZERO {
        sn = sn.negate();
    }
    let rotated = [
        incoming[0].mul(cs)?.sub(incoming[1].mul(sn)?)?,
        incoming[0].mul(sn)?.add(incoming[1].mul(cs)?)?,
    ];
    let out = aberrate(rotated, beta.negate())?;
    let dot = direction[0].mul(out[0])?.add(direction[1].mul(out[1])?)?;
    // Rationalize the difference of the two aberrated directions. Directly
    // subtracting O(1) components would erase a weak lens's tiny bend.
    let den0 = Scalar::ONE.add(beta.mul(incoming[0])?)?;
    let den1 = Scalar::ONE.add(beta.mul(rotated[0])?)?;
    let root = Scalar::ONE.sub(beta.mul(beta)?)?.sqrt()?;
    let cross = root
        .mul(sn.mul(den0)?.add(beta.mul(incoming[1])?.mul(cm1)?)?)?
        .div(den0.mul(den1)?)?;
    // atan2 from the integer primitive, preserving the sign and quadrant.
    let small = dot.abs().min(cross.abs());
    let large = dot.abs().max(cross.abs());
    let ratio = small.div(large)?;
    let a = if ratio <= Scalar::power_of_two(-20) {
        ratio.sub(ratio.mul(ratio)?.mul(ratio)?.div(Scalar::integer(3))?)?
    } else {
        Scalar::raw(crate::num::atan(ratio.fixed(62)?.clamp(0, ONE)), -62)?
    };
    let half = Scalar::raw(PI / 2, -61)?;
    let a = if cross.abs() > dot.abs() {
        half.sub(a)?
    } else {
        a
    };
    let a = if dot < Scalar::ZERO {
        Scalar::raw(PI, -61)?.sub(a)?
    } else {
        a
    };
    Ok(if cross < Scalar::ZERO { a.negate() } else { a })
}
