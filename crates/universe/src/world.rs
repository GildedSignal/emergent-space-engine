//! The tree of dolls: the star is the root; a planet is a tube in the star's doll and the centre of
//! its own doll; the moon is a tube in the planet's doll.
//!
//! **Units.** A doll's mass is a mantissa with the doll's exponent ([`Mass`]: `M_D = μ·2^e · M_root`,
//! `μ` in `[1, 2)`; a power of two is the case `μ = 1`: "physics loves e while we love 2"). The doll's
//! *units* are the exponent's: lengths in `2^e` root units and times in `2^e` root time units (`G = c =
//! 1`), root units times `2^s` with `s = −e`, so a change of doll is an exact shift of exponents and
//! every state the doll stores is an integer at an exponent. The mantissa enters only where the
//! doll's mass does: the compiled tubes (`crates/space` compiles about a mass of exactly 1, so a tube
//! is held in units of `M_D` and read back in the doll's: [`Unit`]), the pulls of the centre's
//! secondaries and of the parent, and the lapse of the doll's clock. **One tick is the same physical
//! time in every doll**: the clock exponent of `D` is `s`, so the integer tick is the doll's time too
//! and a queue of ticks needs no conversion. The doll's far time is the root coordinate time; what a
//! clock *reads* (the centre's own redshift and speed) is derived from tubes when looked at.
use crate::num::Res;
use emergent_space::{
    events::{Doll as SpaceDoll, LogMass},
    orbit::Scalar,
    Tube,
};

/// A mass as the law holds it: a mantissa in `[1, 2)` and the doll's exponent, `value = mantissa · 2^octave`,
/// in units of the root's mass (or of a host's: the caller says which). Never a bare power of two.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Mass {
    pub mantissa: Scalar,
    pub octave: i32,
}
impl Mass {
    /// `2^k`: mantissa one.
    pub fn pow2(k: i32) -> Self {
        Self { mantissa: Scalar::ONE, octave: k }
    }
    /// Any positive scalar, normalised: the mantissa is its significand in `[1, 2)`, the octave its exponent.
    pub fn of(x: Scalar) -> Res<Self> {
        if !x.is_positive() {
            return Err(crate::num::Error::Refused("a mass must be positive"));
        }
        let octave = x.exponent() as i32;
        Ok(Self { mantissa: x.scale(-octave)?, octave })
    }
    /// The ratio `num/den` of two positive integers (rounded toward zero at 62 bits: a game's choice of mass,
    /// made once). `Mass::ratio(1, 999)` is a planet of a thousandth of the total with a star of 999.
    pub fn ratio(num: u64, den: u64) -> Res<Self> {
        if num == 0 || den == 0 {
            return Err(crate::num::Error::Refused("a mass must be positive"));
        }
        Self::of(Scalar::raw(num as i128, 0)?.div(Scalar::raw(den as i128, 0)?)?)
    }
    /// `mantissa · 2^octave` as a scalar.
    pub fn value(self) -> Res<Scalar> {
        Ok(self.mantissa.scale(self.octave)?)
    }
    /// `log2` in Q24, the form the events layer's doll record holds (`crates/space`'s `LogMass`):
    /// the octave, and the mantissa's logarithm by 24 squarings (an integer algorithm, no float).
    pub fn log2_q24(self) -> Res<i32> {
        let two = Scalar::integer(2);
        let (mut x, mut frac) = (self.mantissa, 0i32);
        for bit in (0..24).rev() {
            x = x.mul(x)?;
            if x >= two {
                x = x.scale(-1)?;
                frac |= 1 << bit;
            }
        }
        Ok((self.octave << 24) + frac)
    }
}
impl From<i32> for Mass {
    /// The old calls: a mass given as an octave.
    fn from(k: i32) -> Self {
        Self::pow2(k)
    }
}

/// A doll's mass in the doll's own units: `M_D = μ` doll length units (`μ` in `[1, 2)`), and `1/μ`. A tube
/// is compiled about a mass of one, in units of `M_D`, so the doll's units and the tube's differ by `μ`
/// (lengths and times; velocities are `c`). `unity` is the power-of-two case, where nothing is converted.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Unit {
    pub mu: Scalar,
    pub inverse: Scalar,
    pub unity: bool,
}
impl Unit {
    pub const ONE: Unit = Unit { mu: Scalar::ONE, inverse: Scalar::ONE, unity: true };
    pub fn of(mu: Scalar) -> Res<Self> {
        if mu == Scalar::ONE {
            return Ok(Self::ONE);
        }
        Ok(Self { mu, inverse: mu.reciprocal()?, unity: false })
    }
    /// A length or time in the tube's units (`M_D`) as the doll's.
    pub fn to_doll(&self, x: Scalar) -> Res<Scalar> {
        if self.unity { Ok(x) } else { Ok(x.mul(self.mu)?) }
    }
    /// A length or time in the doll's units as the tube's (`M_D`).
    pub fn to_tube(&self, x: Scalar) -> Res<Scalar> {
        if self.unity { Ok(x) } else { Ok(x.mul(self.inverse)?) }
    }
}

#[derive(Clone, Debug)]
pub struct DollRec {
    pub name: &'static str,
    pub parent: Option<u16>,
    /// The doll's exponent: `M_D = μ · 2^mass_log2` of the root's mass, `μ` in `[1, 2)` (zero for the root).
    pub mass_log2: i32,
    /// The mantissa `μ` and its inverse ([`Unit`]): the centre's mass in the doll's units.
    pub unit: Unit,
    /// `−mass_log2`: root units × `2^shift` = doll units; also the doll's clock exponent.
    pub shift: i16,
    /// The body that is the doll's centre (a tube in the parent doll).
    pub centre: Option<usize>,
    /// Radius of the centre's own surface, in this doll's units (impact below it).
    pub surface: Scalar,
    /// The sphere of influence, in this doll's units: the doll's edge.
    pub edge: Scalar,
    /// The events layer's doll record (mass in log form, parent, the centre's tube at genesis).
    pub record: SpaceDoll,
}

impl DollRec {
    pub fn root(name: &'static str, surface: Scalar) -> Self {
        Self {
            name,
            parent: None,
            mass_log2: 0,
            unit: Unit::ONE,
            shift: 0,
            centre: None,
            surface,
            edge: Scalar::power_of_two(i16::MAX / 2),
            record: SpaceDoll::root(LogMass(0)),
        }
    }
    pub fn child(name: &'static str, parent: u16, mass: Mass, centre: usize, centre_tube: Tube, surface: Scalar, edge: Scalar) -> Res<Self> {
        Ok(Self {
            name,
            parent: Some(parent),
            mass_log2: mass.octave,
            unit: Unit::of(mass.mantissa)?,
            shift: (-mass.octave) as i16,
            centre: Some(centre),
            surface,
            edge,
            record: SpaceDoll::child(LogMass(mass.log2_q24()?), parent, centre_tube),
        })
    }
    /// The centre's mass in the doll's units, as a float (for observation: the lapse of the doll's clock).
    pub fn mu_f64(&self) -> f64 {
        crate::num::to_f64(self.unit.mu)
    }
    pub fn clock_exp(&self) -> i16 {
        self.shift
    }
}

/// `2^k` as a scalar.
pub fn pow2(k: i32) -> Scalar {
    Scalar::power_of_two(k as i16)
}
