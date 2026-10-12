//! Finite inward arcs, including zero angular momentum and a start at rest.
//! The phase y = sqrt(r0/r - 1) cancels a radial turning point at the start.
//! Clocks and angle are compiled once; a read never advances another read.
use crate::{binding::IntegerState, orbit::Scalar, tables::{W, X}, Error, Result};

/// A horizon has no finite Schwarzschild arrival time. Its advanced time and
/// proper time are finite; no large finite number stands in for infinity.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum End {
    Surface(Scalar),
    Horizon,
}
impl End {
    pub fn radius(self) -> Scalar {
        match self { Self::Surface(r) => r, Self::Horizon => Scalar::integer(2) }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Arrival {
    pub end: End,
    pub angle: Scalar,
    pub proper_time: Scalar,
    /// Difference in v = t + r + 2 ln(r/2 - 1), from the binding event.
    pub advanced_time: Scalar,
    pub coordinate_time: Option<Scalar>,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Sample {
    pub radius: Scalar,
    pub angle: Scalar,
    pub proper_time: Scalar,
    pub advanced_time: Scalar,
    pub coordinate_time: Option<Scalar>,
    /// dr/dtau (or dr/dlambda for a photon with E=1).
    pub radial_momentum: Scalar,
    pub terminal: bool,
}

type Sum = [Scalar; 4]; // phi, tau/affine, advanced, Schwarzschild
#[derive(Clone, Copy, Debug)]
struct Knot { y: Scalar, sum: Sum }

#[derive(Clone, Debug)]
pub struct Plunge {
    r0: Scalar,
    w2: Scalar,
    l2: Scalar,
    energy: Scalar,
    angular: Scalar,
    null: bool,
    end: End,
    knots: Vec<Knot>,
}

impl Plunge {
    /// The state uses Schwarzschild coordinate velocities, in G=c=M=1.
    /// Only the incoming branch (or a genuine inward fall from rest) is accepted.
    /// A turning barrier anywhere before the endpoint is a refusal, not capture.
    pub fn from_state(state: IntegerState, end: End) -> Result<Self> {
        let (r0, w2, l2, energy, angular) = crate::inverse::plunge(state, end.radius())?;
        Self::build(r0, w2, l2, energy, angular, false, end)
    }

    /// Capture is decided by the existing exact dyadic b² <= 27 predicate.
    /// A critical ray asymptotes to r=3 and has no finite horizon arrival;
    /// compilation refuses unresolved infinite dwell instead of inventing one.
    pub fn photon(impact: Scalar, outer: Scalar, end: End) -> Result<Option<Self>> {
        if crate::orbit::OrbitKey::photon(impact.abs())?.is_some() { return Ok(None); }
        let u = outer.reciprocal()?;
        let l2 = impact.mul(impact)?;
        let w2 = Scalar::ONE.sub(Scalar::ONE.sub(u.scale(1)?)?.mul(l2.mul(u)?.mul(u)?)?)?;
        Self::build(outer, w2, l2, Scalar::ONE, impact, true, end).map(Some)
    }

    fn build(r0: Scalar, w2: Scalar, l2: Scalar, energy: Scalar, angular: Scalar, null: bool, end: End) -> Result<Self> {
        let inner = end.radius();
        if inner < Scalar::integer(2) || (matches!(end, End::Surface(_)) && inner <= Scalar::integer(2))
            || r0 <= inner || w2 < Scalar::ZERO || !energy.is_positive() {
            return Err(Error::Range);
        }
        let mut out = Self { r0, w2, l2, energy, angular, null, end,
            knots: vec![Knot { y: Scalar::ZERO, sum: [Scalar::ZERO; 4] }] };
        let last = r0.div(inner)?.sub(Scalar::ONE)?.sqrt()?;
        // Geometric panels retain relative radial information over many octaves.
        let mut lo = Scalar::ZERO;
        while lo < last {
            let hi = if lo < Scalar::ONE { lo.add(Scalar::power_of_two(-3))? }
                else { lo.mul(Scalar::integer(9))?.scale(-3)? }.min(last);
            if hi <= lo { return Err(Error::Range); }
            out.compile_panel(lo, hi, 0)?;
            lo = hi;
        }
        Ok(out)
    }

    pub fn initial_radius(&self) -> Scalar { self.r0 }
    /// Local gravity/crossing time, in the same period convention as a cycle.
    /// An endpoint cannot shrink this scale as an impact approaches.
    pub fn motion_period(&self) -> Result<Scalar> {
        let lapse = Scalar::ONE.sub(Scalar::integer(2).div(self.r0)?)?;
        let speed = self.w2.add(lapse.mul(self.l2)?.div(self.r0.mul(self.r0)?)?)?.sqrt()?.div(self.energy)?;
        let time = if speed.is_zero() { self.r0.sqrt()? } else { self.r0.sqrt()?.min(speed.reciprocal()?) };
        self.r0.mul(time)?.mul(Scalar::raw(2 * crate::tables::PI, -61)?)
    }
    /// Canonical coefficients for consumers' digests. Compiled tables are derived.
    pub fn coefficients(&self) -> [Scalar; 5] { [self.r0, self.w2, self.l2, self.energy, self.angular] }
    pub fn panel_count(&self) -> usize { self.knots.len() - 1 }
    pub fn retained_bytes(&self) -> usize {
        std::mem::size_of::<Self>() + self.knots.capacity() * std::mem::size_of::<Knot>()
    }
    /// A bound on Schwarzschild coordinate speed across the arc, from the
    /// largest local speed (at the smallest lapse). Retains weak-field scale.
    pub fn speed_bound(&self) -> Result<Scalar> {
        let r = self.end.radius();
        let (_, w, _) = self.radial(self.knots.last().unwrap().y)?;
        let lapse = Scalar::ONE.sub(Scalar::integer(2).div(r)?)?;
        w.mul(w)?.add(lapse.mul(self.l2)?.div(r.mul(r)?)?)?.sqrt()?.div(self.energy)
    }
    pub fn arrival(&self) -> Arrival {
        let s = self.knots.last().unwrap().sum;
        Arrival { end: self.end, angle: s[0], proper_time: if self.null { Scalar::ZERO } else { s[1] },
            advanced_time: s[2], coordinate_time: if matches!(self.end, End::Horizon) { None } else { Some(s[3]) } }
    }

    fn radial(&self, y: Scalar) -> Result<(Scalar, Scalar, Scalar)> {
        let y2 = y.mul(y)?;
        let z = Scalar::ONE.add(y2)?;
        let u0 = self.r0.reciprocal()?;
        let u = z.mul(u0)?;
        // R(u) - R(u0), factored before rounding; no E²-1 cancellation.
        let h = Scalar::integer(if self.null { 0 } else { 2 })
            .sub(self.l2.mul(u.add(u0)?)?)?
            .add(self.l2.scale(1)?.mul(u.mul(u)?.add(u.mul(u0)?)?.add(u0.mul(u0)?)?)?)?;
        let radial = self.w2.add(y2.mul(u0)?.mul(h)?)?;
        // Topology was decided before narrowing the coefficients. A negative
        // rounded radicand is an arithmetic refusal, not a second classifier.
        if radial < Scalar::ZERO { return Err(Error::Range); }
        Ok((z, radial.sqrt()?, h))
    }

    fn node(&self, y: Scalar) -> Result<Sum> {
        let (z, w, h) = self.radial(y)?;
        let r = self.r0.div(z)?;
        // |dr/dy|/sqrt(R), cancelling y exactly at a rest anchor.
        let affine = if self.w2.is_zero() {
            self.r0.mul(self.r0.sqrt()?)?.scale(1)?.div(z.mul(z)?)?.div(h.sqrt()?)?
        } else {
            self.r0.scale(1)?.mul(y)?.div(z.mul(z)?)?.div(w)?
        };
        let invr2 = r.mul(r)?.reciprocal()?;
        let angle = affine.mul(self.angular)?.mul(invr2)?;
        // (E-w)/f = (m²+L²/r²)/(E+w), finite all the way through f=0.
        let mass = if self.null { Scalar::ZERO } else { Scalar::ONE };
        let advanced = affine.mul(mass.add(self.l2.mul(invr2)?)?)?.div(self.energy.add(w)?)?;
        let coordinate = if matches!(self.end, End::Horizon) { Scalar::ZERO } else {
            affine.mul(self.energy)?.div(Scalar::ONE.sub(Scalar::integer(2).div(r)?)?)?
        };
        Ok([angle, affine, advanced, coordinate])
    }

    fn quad(&self, lo: Scalar, hi: Scalar) -> Result<Sum> {
        let half = hi.sub(lo)?.scale(-1)?;
        let mid = lo.add(half)?;
        let mut sum = [Scalar::ZERO; 4];
        for j in 0..2 {
            let dx = half.mul(Scalar::raw(X[j], -62)?)?;
            let weight = half.mul(Scalar::raw(W[j], -62)?)?;
            for y in [mid.sub(dx)?, mid.add(dx)?] {
                let value = self.node(y)?;
                for i in 0..4 { sum[i] = sum[i].add(weight.mul(value[i])?)?; }
            }
        }
        Ok(sum)
    }

    fn compile_panel(&mut self, lo: Scalar, hi: Scalar, depth: u8) -> Result<()> {
        if self.knots.len() > 8190 { return Err(Error::Range); }
        let mid = lo.add(hi.sub(lo)?.scale(-1)?)?;
        if mid == lo || mid == hi { return Err(Error::Range); }
        let whole = self.quad(lo, hi)?;
        let a = self.quad(lo, mid)?;
        let b = self.quad(mid, hi)?;
        let split = add(a, b)?;
        if (0..4).all(|i| split[i].sub(whole[i]).is_ok_and(|e|
            e.abs() <= split[i].abs().scale(-32).unwrap_or(Scalar::ZERO))) {
            // Retain the actual accepted half panels: readout uses the same rule.
            let sum = add(self.knots.last().unwrap().sum, a)?;
            self.knots.push(Knot { y: mid, sum });
            self.knots.push(Knot { y: hi, sum: add(sum, b)? });
            return Ok(());
        }
        if depth == 40 { return Err(Error::Range); }
        self.compile_panel(lo, mid, depth + 1)?;
        self.compile_panel(mid, hi, depth + 1)
    }

    /// Read by proper time (affine time for light). At the exact compiled endpoint
    /// the radius is exactly the requested surface/horizon, never a rounded root.
    pub fn at_affine(&self, elapsed: Scalar) -> Result<Sample> { self.at_clock(elapsed, 1) }
    /// Finite surfaces also support the plane's existing Schwarzschild clock.
    pub fn at_coordinate(&self, elapsed: Scalar) -> Result<Sample> {
        if matches!(self.end, End::Horizon) { return Err(Error::Range); }
        self.at_clock(elapsed, 3)
    }
    pub fn affine_duration(&self) -> Scalar { self.knots.last().unwrap().sum[1] }

    pub fn orbit_state(&self, elapsed: Scalar) -> Result<crate::orbit::OrbitState> {
        let s = self.at_coordinate(elapsed)?;
        let lapse = Scalar::ONE.sub(Scalar::integer(2).div(s.radius)?)?;
        Ok(crate::orbit::OrbitState { radius: s.radius, radial_angle: 0, advance: s.angle,
            proper_time: s.proper_time, radial_velocity: s.radial_momentum.mul(lapse)?.div(self.energy)?,
            transverse_velocity: self.angular.mul(lapse)?.div(self.energy)?.div(s.radius)?,
            cycles: 0, outbound: false, psi: 0 })
    }

    fn at_clock(&self, elapsed: Scalar, clock: usize) -> Result<Sample> {
        let last = self.knots.last().unwrap();
        if elapsed < Scalar::ZERO || elapsed > last.sum[clock] { return Err(Error::Range); }
        if elapsed == last.sum[clock] { return self.sample(last.y, last.sum, true); }
        let i = self.knots.partition_point(|k| k.sum[clock] <= elapsed).saturating_sub(1);
        let base = self.knots[i];
        if elapsed == base.sum[clock] { return self.sample(base.y, base.sum, false); }
        let (mut lo, mut hi) = (base.y, self.knots[i+1].y);
        for _ in 0..96 {
            let y = lo.add(hi.sub(lo)?.scale(-1)?)?;
            let sum = add(base.sum, self.quad(base.y, y)?)?;
            if sum[clock].sub(elapsed)?.abs() <= elapsed.abs().scale(-40)? || y == lo || y == hi {
                return self.sample(y, sum, false);
            }
            if sum[clock] < elapsed { lo = y; } else { hi = y; }
        }
        Err(Error::Range)
    }
    fn sample(&self, y: Scalar, sum: Sum, terminal: bool) -> Result<Sample> {
        let (z, w, _) = self.radial(y)?;
        Ok(Sample { radius: if terminal { self.end.radius() } else { self.r0.div(z)? },
            angle: sum[0], proper_time: if self.null { Scalar::ZERO } else { sum[1] }, advanced_time: sum[2],
            coordinate_time: if matches!(self.end, End::Horizon) { None } else { Some(sum[3]) },
            radial_momentum: w.negate(), terminal })
    }
}

fn add(a: Sum, b: Sum) -> Result<Sum> {
    Ok([a[0].add(b[0])?, a[1].add(b[1])?, a[2].add(b[2])?, a[3].add(b[3])?])
}
