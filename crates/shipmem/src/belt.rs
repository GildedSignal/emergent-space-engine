//! Independent birth belt: banded Darwin p, Rayleigh e (sigma 0.07), uniform angles.
//! This is a description of individuals, not preservation of an existing iid sample.
//! Correlated/sculpted belts are unsupported: they require a joint description.
//! Tables are frozen integer data; no floating arithmetic decides regeneration.
use crate::codec::Enc;
use crate::codec::MAXC;
use crate::program::{Prog, Program};
use crate::shelf::Ship;
use emergent_space::Key;

#[path = "belt_quantiles.rs"]
mod quantiles;

/// Bijective counter finalizer for odd keys. Projection to a column is not injective.
#[inline]
pub fn mix(i: u64, key: u64) -> u64 {
    let mut z = i.wrapping_add(0x9E37_79B9_7F4A_7C15).wrapping_mul(key);
    z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
    z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
    z ^ (z >> 31)
}

/// Quantile of a uniform u64 draw. The last central cell is replaced by dyadic
/// survival bands and exact endpoints, so the upper 10^-4 is resolved, not capped.
#[inline]
pub fn eccentricity(u: u64) -> u32 {
    let central = (u >> 52) as usize;
    if central < 4095 {
        return quantiles::E[central];
    }
    let survival = !u;
    if survival < 64 {
        return quantiles::E[4095 + 46 * 64 + survival as usize];
    }
    let z = survival.leading_zeros();
    let fraction = ((survival >> (57 - z)) & 63) as usize;
    quantiles::E[4095 + (z as usize - 12) * 64 + fraction]
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Columns {
    Independent,
    Correlated,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum BeltError {
    CorrelatedColumns,
    InvalidKeys,
}

/// The lab's smooth belt: p in [2048,2560), e Rayleigh sigma 0.07, kind in [0,64),
/// omega in [0,2^32), t_p in [0,2^44). Only independent input columns are supported.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Belt {
    keys: [u64; 5],
}

impl Belt {
    pub const P_LO: u32 = 2048 << 16;
    pub const P_BITS: u32 = 25;
    pub const T_BITS: u32 = 44;
    pub const LAB_KEYS: [u64; 5] = [
        0x0123_4567_89ab_cdef,
        0x243f_6a88_85a3_08d3,
        0x1319_8a2e_0370_7345,
        0xa409_3822_299f_31d1,
        0x082e_fa98_ec4e_6c89,
    ];

    pub fn new(keys: [u64; 5], columns: Columns) -> Result<Self, BeltError> {
        if columns != Columns::Independent {
            return Err(BeltError::CorrelatedColumns);
        }
        if keys.iter().any(|k| k & 1 == 0) || (0..5).any(|i| keys[..i].contains(&keys[i])) {
            return Err(BeltError::InvalidKeys);
        }
        Ok(Self { keys })
    }

    /// Physical draws, before the law's exact boundary conversion.
    #[inline]
    pub fn draws(self, i: u64) -> (u32, u32, u64, u32, u64) {
        let u = |f: usize| mix(i, self.keys[f]);
        (
            Self::P_LO + (u(0) >> (64 - Self::P_BITS)) as u32,
            eccentricity(u(1)),
            u(2) >> 58,
            (u(3) >> 32) as u32,
            u(4) >> 20,
        )
    }

    #[inline]
    pub fn eval(self, i: u64) -> Ship {
        let (p, e, kind, w, t) = self.draws(i);
        let key = Key::darwin(p, e).expect("belt's full quantile range is bound");
        [
            t,
            kind,
            key.energy.get(),
            key.angular.get(),
            w as u64,
            0,
            0,
            0,
        ]
    }

    pub fn programs(self) -> [Prog; MAXC] {
        std::array::from_fn(|column| {
            if column < 5 {
                Prog::Belt(BeltColumn {
                    belt: self,
                    column: column as u8,
                    offset: 0,
                })
            } else {
                Prog::Const(0)
            }
        })
    }

    /// Birth is constant work and stores no generated members.
    pub fn population(self, n: u64, enc: &mut Enc) -> Program {
        assert!(n <= u32::MAX as u64, "population hot ordinals are u32");
        Program::seal_from(n, 5, self.programs(), &[], enc)
    }

    /// Shared table payload, charged once even though the executable embeds it.
    pub const fn table_bytes() -> usize {
        std::mem::size_of_val(&quantiles::E)
    }
}

/// A column view of the same population program; splitting only shifts its ordinal.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct BeltColumn {
    pub(crate) belt: Belt,
    pub(crate) column: u8,
    pub(crate) offset: u64,
}

impl BeltColumn {
    #[inline]
    pub fn at(self, i: u64) -> u64 {
        let i = self.offset.wrapping_add(i);
        match self.column {
            0 => mix(i, self.belt.keys[4]) >> 20,
            1 => mix(i, self.belt.keys[2]) >> 58,
            4 => mix(i, self.belt.keys[3]) >> 32,
            c => self.belt.eval(i)[c as usize],
        }
    }
    pub(crate) fn shifted(mut self, s: u64) -> Self {
        self.offset = self.offset.wrapping_add(s);
        self
    }
    pub(crate) fn bounds(self) -> (i128, i128) {
        match self.column {
            0 => (0, (1 << 44) - 1),
            1 => (0, 63),
            2 => (1, 16i128 << 48),
            3 => (1 << 30, 4096i128 << 32),
            4 => (0, u32::MAX as i128),
            _ => unreachable!(),
        }
    }
}

/// Recognize a full belt once, so E and L share one Darwin conversion.
pub(crate) fn base(prog: &[Prog; MAXC], cols: usize, i: u64) -> Option<Ship> {
    let Prog::Belt(first) = prog[0] else {
        return None;
    };
    if cols != 5 || first.column != 0 {
        return None;
    }
    if (1..5).any(|c| {
        prog[c]
            != Prog::Belt(BeltColumn {
                column: c as u8,
                ..first
            })
    }) {
        return None;
    }
    Some(first.belt.eval(first.offset.wrapping_add(i)))
}
