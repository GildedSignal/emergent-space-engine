//! The tree of dolls: the star is the root; a planet is a tube in the star's doll and the centre of
//! its own doll; the moon is a tube in the planet's doll.
//!
//! **Units.** A doll's mass is a power of two of the root's (a game's choice: "physics loves e
//! while we love 2"), so a change of doll is an exact shift of exponents. A doll `D` of mass
//! `M_D = 2^-s · M_root` has lengths in units of `M_D` and times in units of `M_D/c`
//! (`G = c = 1`): root units times `2^s`. **One tick is the same physical time in every
//! doll**: the clock exponent of `D` is `s`, so the integer tick is the doll's time too and a
//! queue of ticks needs no conversion. The doll's far time is the root coordinate time; what a
//! clock *reads* (the centre's own redshift and speed) is derived from tubes when looked at.
use emergent_space::{
    events::{Doll as SpaceDoll, LogMass},
    orbit::Scalar,
    Tube,
};

#[derive(Clone, Debug)]
pub struct DollRec {
    pub name: &'static str,
    pub parent: Option<u16>,
    /// `log2(M_D / M_root)`, an integer octave (zero for the root).
    pub mass_log2: i32,
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
            shift: 0,
            centre: None,
            surface,
            edge: Scalar::power_of_two(i16::MAX / 2),
            record: SpaceDoll::root(LogMass(0)),
        }
    }
    pub fn child(name: &'static str, parent: u16, mass_log2: i32, centre: usize, centre_tube: Tube, surface: Scalar, edge: Scalar) -> Self {
        Self {
            name,
            parent: Some(parent),
            mass_log2,
            shift: (-mass_log2) as i16,
            centre: Some(centre),
            surface,
            edge,
            record: SpaceDoll::child(LogMass(mass_log2 << 24), parent, centre_tube),
        }
    }
    pub fn clock_exp(&self) -> i16 {
        self.shift
    }
}

/// `2^k` as a scalar.
pub fn pow2(k: i32) -> Scalar {
    Scalar::power_of_two(k as i16)
}
