//! Compile-time exact predicates in Q(sqrt(S)), S = X.X in the input's integer units.
//! Adapted from retired v0 `algebraic.rs`/`roots.rs`: decide multiplicity before
//! rounding; carry the small root gap through its square root before narrowing.
use crate::{
    Error, Result,
    binding::IntegerState,
    orbit::{OrbitKey, Scalar},
};
use num_bigint::BigInt;
use num_traits::{One, Signed, ToPrimitive, Zero};

fn gcd(mut a: BigInt, mut b: BigInt) -> BigInt {
    a = a.abs();
    b = b.abs();
    while !b.is_zero() {
        let r = &a % &b;
        a = b;
        b = r;
    }
    a
}

#[derive(Clone)]
struct A {
    a: BigInt,
    b: BigInt,
    d: BigInt,
    s: BigInt,
}
impl A {
    fn new(a: BigInt, b: BigInt, d: BigInt, s: &BigInt) -> Self {
        let root = s.sqrt();
        let (a, b) = if &root * &root == *s {
            (a + b * root, BigInt::zero())
        } else {
            (a, b)
        };
        let mut g = gcd(gcd(a.clone(), b.clone()), d.clone());
        if d.is_negative() {
            g = -g;
        }
        Self {
            a: a / &g,
            b: b / &g,
            d: d / g,
            s: s.clone(),
        }
    }
    fn n(&self, n: i64) -> Self {
        Self::new(n.into(), 0.into(), 1.into(), &self.s)
    }
    fn dyadic(n: BigInt, e: i32, s: &BigInt) -> Self {
        if e >= 0 {
            Self::new(n << e as usize, 0.into(), 1.into(), s)
        } else {
            Self::new(n, 0.into(), BigInt::one() << -e as usize, s)
        }
    }
    fn add(&self, o: &Self) -> Self {
        Self::new(
            &self.a * &o.d + &o.a * &self.d,
            &self.b * &o.d + &o.b * &self.d,
            &self.d * &o.d,
            &self.s,
        )
    }
    fn neg(&self) -> Self {
        Self {
            a: -&self.a,
            b: -&self.b,
            ..self.clone()
        }
    }
    fn sub(&self, o: &Self) -> Self {
        self.add(&o.neg())
    }
    fn mul(&self, o: &Self) -> Self {
        Self::new(
            &self.a * &o.a + &self.b * &o.b * &self.s,
            &self.a * &o.b + &self.b * &o.a,
            &self.d * &o.d,
            &self.s,
        )
    }
    fn div(&self, o: &Self) -> Self {
        assert!(!o.sign().eq(&0));
        Self::new(
            (&self.a * &o.a - &self.b * &o.b * &self.s) * &o.d,
            (&self.b * &o.a - &self.a * &o.b) * &o.d,
            &self.d * (&o.a * &o.a - &o.b * &o.b * &self.s),
            &self.s,
        )
    }
    fn square(&self) -> Self {
        self.mul(self)
    }
    fn sign(&self) -> i8 {
        let sign = |x: &BigInt| {
            if x.is_zero() {
                0
            } else if x.is_negative() {
                -1
            } else {
                1
            }
        };
        let a = sign(&self.a);
        let b = sign(&self.b);
        if a == 0 {
            b
        } else if b == 0 || a == b {
            a
        } else {
            a * sign(&(&self.a * &self.a - &self.b * &self.b * &self.s))
        }
    }
    fn fixed(&self) -> BigInt {
        // 256 fraction bits are compilation scratch, not retained runtime storage.
        let r = (&self.s << (2 * BITS)).sqrt();
        ((&self.a << BITS) + &self.b * r) / &self.d
    }
}
const BITS: usize = 256;
fn mul(a: &BigInt, b: &BigInt) -> BigInt {
    (a * b) >> BITS
}
fn div(a: &BigInt, b: &BigInt) -> BigInt {
    (a << BITS) / b
}
fn sqrt(a: &BigInt) -> Result<BigInt> {
    if a.is_negative() {
        Err(Error::Range)
    } else {
        Ok((a << BITS).sqrt())
    }
}
fn scalar(n: &BigInt) -> Result<Scalar> {
    if n.is_zero() {
        return Ok(Scalar::ZERO);
    }
    let shift = n.bits().saturating_sub(63) as usize;
    Scalar::raw(
        (n >> shift).to_i128().ok_or(Error::Range)?,
        shift as i32 - BITS as i32,
    )
}

struct Cubic {
    a: A,
    b: A,
    z: A,
    circular: bool,
}
pub(crate) fn circular(st: IntegerState) -> bool {
    let [x, y] = st.position.map(BigInt::from);
    let [vx, vy] = st.velocity.map(BigInt::from);
    if &x * &vx + &y * &vy != BigInt::zero() {
        return false;
    }
    let ss = &x * &x + &y * &y;
    let vv = &vx * &vx + &vy * &vy;
    let e = 2 * st.length_exponent as i32 + 4 * st.velocity_exponent as i32;
    let lhs = &vv * &vv * ss;
    if e >= 0 {
        (lhs << e as usize) == BigInt::one()
    } else {
        lhs == BigInt::one() << -e as usize
    }
}
impl Cubic {
    fn new(st: IntegerState) -> Result<Self> {
        let [x, y] = st.position.map(BigInt::from);
        let [vx, vy] = st.velocity.map(BigInt::from);
        let s = &x * &x + &y * &y;
        let dot = &x * &vx + &y * &vy;
        let cross = &x * &vy - &y * &vx;
        if s.is_zero() || cross.is_zero() {
            return Err(Error::NoBoundOrbit);
        }
        let pe = st.length_exponent as i32;
        let ve = st.velocity_exponent as i32;
        let seed = A::dyadic(1.into(), 0, &s);
        let r = A::new(0.into(), 1.into(), 1.into(), &s).mul(&A::dyadic(1.into(), pe, &s));
        let z = seed.n(2).div(&r);
        let lapse = seed.n(1).sub(&z);
        if lapse.sign() <= 0 {
            return Err(Error::NoBoundOrbit);
        }
        let ss = A::dyadic(s.clone(), 2 * pe, &s);
        let dot2 = A::dyadic(&dot * &dot, 2 * (pe + ve), &s);
        let cross2 = A::dyadic(&cross * &cross, 2 * (pe + ve), &s);
        let kinetic = dot2.div(&ss.mul(&lapse)).add(&cross2.div(&ss));
        let den = lapse.sub(&kinetic);
        if den.sign() <= 0 {
            return Err(Error::NoBoundOrbit);
        }
        let a = seed.n(4).mul(&den).div(&cross2);
        let b = seed.n(4).mul(&lapse.square().sub(&den)).div(&cross2);
        let vv = A::dyadic(&vx * &vx + &vy * &vy, 2 * ve, &s);
        let circular = dot.is_zero() && vv.square().mul(&ss).sub(&seed.n(1)).sign() == 0;
        Ok(Self { a, b, z, circular })
    }
}

pub(crate) fn fit(st: IntegerState) -> Result<OrbitKey> {
    let c = Cubic::new(st)?;
    if c.circular {
        return OrbitKey::new(
            scalar(&div(&(BigInt::from(2) << BITS), &c.z.fixed()))?,
            1 << 48,
        );
    }
    fit_cubic(c)
}

/// Binding energy E-1 retains its exponent; never round a weak E to unity.
pub(crate) fn invariants(
    delta: crate::scaled::Scalar,
    angular: crate::scaled::Scalar,
) -> Result<OrbitKey> {
    if !angular.is_positive() || delta <= crate::scaled::Scalar::integer(-1) {
        return Err(Error::Range);
    }
    let s = BigInt::one();
    let d = A::dyadic(delta.significand().into(), delta.exponent() as i32 - 62, &s);
    let l = A::dyadic(
        angular.significand().into(),
        angular.exponent() as i32 - 62,
        &s,
    );
    let a = d.n(4).div(&l.square());
    let b = a.mul(&d.mul(&d.n(2).add(&d)));
    if angular >= crate::scaled::Scalar::power_of_two(10) && delta < crate::scaled::Scalar::ZERO {
        // In x=L²/r the two bound roots are O(1), even when their
        // Schwarzschild u values have disjoint exponents from the third root.
        // Never materialize the tiny coefficient ε/L² in fixed scratch units.
        let one = BigInt::one() << BITS;
        let q = d.n(1).div(&l.square()).fixed();
        let c = d.mul(&d.n(2).add(&d)).mul(&l.square()).fixed();
        let vertex = div(&(&one * 2), &(&one + sqrt(&(&one - &q * 12))?));
        let poly = |x: &BigInt| mul(x, x) - x * 2 - &c - mul(&q, &mul(&mul(x, x), x)) * 2;
        if poly(&vertex) >= BigInt::zero() || c >= BigInt::zero() {
            return Err(Error::NoBoundOrbit);
        }
        let root = |mut lo: BigInt, mut hi: BigInt, increasing: bool| {
            while &hi - &lo > BigInt::one() {
                let mid = (&lo + &hi) >> 1;
                if (poly(&mid) > BigInt::zero()) == increasing {
                    hi = mid;
                } else {
                    lo = mid;
                }
            }
            (lo + hi) >> 1
        };
        let apo = root(BigInt::zero(), vertex.clone(), false);
        let peri = root(vertex, &one * 4, true);
        let shape: BigInt = div(&(&peri + apo), &(&peri * 2)) >> (BITS - 48);
        let radius = angular.mul(angular)?.div(scalar(&peri)?)?;
        return OrbitKey::new(radius, shape.to_u64().ok_or(Error::Range)?);
    }
    fit_cubic(Cubic {
        a,
        b,
        z: d.n(0),
        circular: false,
    })
}

/// Null turn R/b, solved with normalized compilation scratch. Capture is decided
/// on the exact dyadic b², before any root or shape rounding.
pub(crate) fn photon(impact: crate::scaled::Scalar) -> Result<Option<OrbitKey>> {
    use crate::scaled::Scalar;
    if impact < Scalar::ZERO {
        return Err(Error::Range);
    }
    let s = BigInt::one();
    let b = A::dyadic(
        impact.significand().into(),
        impact.exponent() as i32 - 62,
        &s,
    );
    if b.square().sub(&b.n(27)).sign() <= 0 {
        return Ok(None);
    }
    let one = BigInt::one() << BITS;
    let inverse = b.n(2).div(&b).fixed();
    let (mut lo, mut hi) = (sqrt(&(&one / 3))?, one.clone());
    while &hi - &lo > BigInt::one() {
        let y = (&lo + &hi) >> 1;
        let p = mul(&mul(&y, &y), &y) - &y + &inverse;
        if p > BigInt::zero() {
            hi = y;
        } else {
            lo = y;
        }
    }
    let radius = impact.mul(scalar(&hi)?)?;
    let q = radius.reciprocal()?;
    let lapse = Scalar::ONE.sub(q.scale(1)?)?;
    let root = lapse
        .mul(Scalar::ONE.add(q.mul(Scalar::integer(6))?)?)?
        .sqrt()?;
    let den = root.add(lapse)?;
    let k = q.scale(2)?.mul(lapse)?.div(den.mul(den)?)?;
    Ok(Some(OrbitKey {
        periapsis: radius,
        k: k.fixed(48)? as u64,
        null: true,
    }))
}

fn fit_cubic(c: Cubic) -> Result<OrbitKey> {
    let one = BigInt::one() << BITS;
    // Exact depressed-cubic discriminant, as in v0. No rounded residual decides
    // whether the two neighbouring roots exist.
    let pp = c.a.sub(&c.a.n(1).div(&c.a.n(3)));
    let rr = c.b.add(&c.a.div(&c.a.n(3))).sub(&c.a.n(2).div(&c.a.n(27)));
    let discriminant = rr
        .square()
        .div(&c.a.n(4))
        .add(&pp.square().mul(&pp).div(&c.a.n(27)));
    if discriminant.sign() >= 0 {
        return Err(Error::NoBoundOrbit);
    }
    // Select the exterior allowed interval with the exact v0 anchor predicate.
    let v = c.z.mul(&c.a.n(3)).sub(&c.a.n(1));
    if v.sign() > 0 && v.square().sub(&c.a.n(1).sub(&c.a.mul(&c.a.n(3)))).sign() >= 0 {
        return Err(Error::NoBoundOrbit);
    }
    let a = c.a.fixed();
    let b = c.b.fixed();
    if a <= BigInt::zero() || (b.is_zero() && c.b.sign() != 0) {
        return Err(Error::Range);
    }
    let derivative = sqrt(&(&one - &a * 3))?;
    let maximum = (&one - &derivative) / 3;
    let poly = |z: &BigInt| mul(&mul(z, z), z) - mul(z, z) + mul(&a, z) + &b;
    let (mut lo, mut hi) = if c.b.sign() < 0 {
        (BigInt::zero(), maximum)
    } else {
        let mut lo = -&one;
        while poly(&lo) > BigInt::zero() {
            lo *= 2;
        }
        (lo, BigInt::zero())
    };
    while &hi - &lo > BigInt::one() {
        let mid = (&lo + &hi) >> 1;
        if poly(&mid) > BigInt::zero() {
            hi = mid;
        } else {
            lo = mid;
        }
    }
    let small = if c.b.sign() == 0 {
        BigInt::zero()
    } else {
        (&lo + &hi) >> 1
    };
    let center2 = &one - &small;
    // Never narrow the squared gap: its exponent is twice the physical gap's.
    // b=0 is the symbolic E=1 root and needs no division by the zero root.
    let gap2 = if c.b.sign() == 0 {
        &one - &a * 4
    } else {
        mul(&center2, &center2) + div(&b, &small) * 4
    };
    if gap2 <= BigInt::zero() {
        return Err(Error::Range);
    }
    let gap = sqrt(&gap2)?;
    let peri = (&center2 - &gap) / 2;
    if peri <= BigInt::zero() {
        return Err(Error::Range);
    }
    let rp = scalar(&div(&(&one * 2), &peri))?;
    let k: BigInt = (&one + div(&small, &peri)) / 2;
    // E=1 is symbolic. Only its half-quantum neighbourhood rounds to the
    // even parabolic word; otherwise floor k so the fitted apoapsis still
    // contains the event. A sub-quantum adapter perturbation must not invent
    // hyperbolic asymptotic speed at an arbitrarily distant passage endpoint.
    let shift = BITS - 48;
    let half: BigInt = &one >> 1;
    let half_quantum = BigInt::one() << (shift - 1);
    let word = if (&k - half).abs() <= half_quantum {
        BigInt::one() << 47
    } else {
        &k >> shift
    };
    OrbitKey::new(rp, word.to_u64().ok_or(Error::Range)?)
}
