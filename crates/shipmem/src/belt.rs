//! Independent birth belt: banded Darwin p, Rayleigh e (sigma 0.07), uniform angles.
//! This is a description of individuals, not preservation of an existing iid sample.
//! Correlated/sculpted belts are unsupported: they require a joint description.
//! Tables are derived at birth in integers; no floating arithmetic decides regeneration.
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

/// Working constants for the legacy default birth parameters.
#[inline]
fn default_quantiles() -> &'static quantiles::Quantiles {
    static TABLE: std::sync::OnceLock<quantiles::Quantiles> = std::sync::OnceLock::new();
    TABLE.get_or_init(|| quantiles::Quantiles::new(70, 30, u32::MAX))
}

/// Quantile of a uniform draw, resolving both tails through dyadic probability bands.
#[inline]
pub fn eccentricity(u: u64) -> u32 {
    default_quantiles().at(u)
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
        default_quantiles();
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

    /// Derived table payload, charged once by the legacy population memory count.
    pub const fn table_bytes() -> usize {
        quantiles::Quantiles::bytes()
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

/// Integer birth parameters. The format accepts the current law's storage widths.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Spec {
    pub p_lo: u32,
    pub p_bits: u8,
    pub sigma_milli: u16,
    pub e_bits: u8,
    pub e_cap: u32,
    pub w_bits: u8,
    pub t_bits: u8,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Body {
    pub p: u64,
    pub e: u64,
    pub w: u64,
    pub t: u64,
}
#[derive(Clone, Copy)]
struct Scar {
    i: u32,
    delta: [u8; 8],
} // 12 bytes, without alignment padding
#[derive(Clone, Copy)]
struct Wide {
    i: u64,
    body: Body,
}

/// A birth program with sorted cold scars and the current monotone event batch.
/// Starting a new batch merges the previous one. Queries never mutate the store.
/// The quantile table is disposable and reconstructed from Spec on restore.
pub struct Population {
    spec: Spec,
    n: u64,
    seed: u64,
    keys: [u64; 4],
    table: quantiles::Quantiles,
    cold: Vec<Scar>,
    hot: Vec<Scar>,
    wide: Vec<Wide>,
}
impl Population {
    pub const INFO_BYTES: u64 = 34;
    pub fn birth(spec: Spec, n: u64, seed: u64) -> Option<Self> {
        if n > u32::MAX as u64
            || spec.p_bits == 0
            || spec.p_bits > 31
            || spec.e_bits > 30
            || spec.sigma_milli == 0
            || spec.sigma_milli > 1000
            || spec.w_bits == 0
            || spec.w_bits > 63
            || spec.t_bits == 0
            || spec.t_bits > 63
            || spec.p_lo as u64 + (1u64 << spec.p_bits) > u32::MAX as u64 + 1
        {
            return None;
        }
        // Column domains are distinct before the bijective finalizer. Force odd
        // multipliers and resolve the possible one-bit projection collision.
        let mut keys = [0; 4];
        for (c, column) in [0usize, 1, 3, 4].into_iter().enumerate() {
            let mut key = mix(seed ^ Belt::LAB_KEYS[column], 1) | 1;
            while keys[..c].contains(&key) {
                key = key.wrapping_add(2);
            }
            keys[c] = key;
        }
        Some(Self {
            spec,
            n,
            seed,
            keys,
            table: quantiles::Quantiles::new(spec.sigma_milli, spec.e_bits, spec.e_cap),
            cold: Vec::new(),
            hot: Vec::new(),
            wide: Vec::new(),
        })
    }
    pub fn len(&self) -> u64 {
        self.n
    }
    pub fn is_empty(&self) -> bool {
        self.n == 0
    }
    fn base(&self, i: u64) -> Body {
        // Retain wt/belt's independent odd-key ordinal finalizers; derive keys from one seed.
        let draw = |c| mix(i, self.keys[c]);
        Body {
            p: self.spec.p_lo as u64 + (draw(0) >> (64 - self.spec.p_bits)),
            e: self.table.at(draw(1)) as u64,
            w: draw(2) >> (64 - self.spec.w_bits),
            t: draw(3) >> (64 - self.spec.t_bits),
        }
    }
    pub fn body(&self, i: u64) -> Body {
        assert!(i < self.n);
        if let Ok(j) = self.wide.binary_search_by_key(&i, |s| s.i) {
            return self.wide[j].body;
        }
        let base = self.base(i);
        let record = self
            .hot
            .binary_search_by_key(&(i as u32), |s| s.i)
            .ok()
            .map(|j| self.hot[j])
            .or_else(|| {
                self.cold
                    .binary_search_by_key(&(i as u32), |s| s.i)
                    .ok()
                    .map(|j| self.cold[j])
            });
        let Some(s) = record else {
            return base;
        };
        let d: [u64; 4] = std::array::from_fn(|c| {
            i16::from_le_bytes([s.delta[2 * c], s.delta[2 * c + 1]]) as i64 as u64
        });
        Body {
            p: base.p.wrapping_add(d[0]),
            e: base.e.wrapping_add(d[1]),
            w: base.w.wrapping_add(d[2]) & ((1u64 << self.spec.w_bits) - 1),
            t: base.t.wrapping_add(d[3]) & ((1u64 << self.spec.t_bits) - 1),
        }
    }
    fn merged(&self) -> Vec<Scar> {
        let mut out = Vec::with_capacity(self.cold.len() + self.hot.len());
        let (mut a, mut b) = (0, 0);
        while a < self.cold.len() || b < self.hot.len() {
            let next =
                if b == self.hot.len() || (a < self.cold.len() && self.cold[a].i < self.hot[b].i) {
                    let s = self.cold[a];
                    a += 1;
                    s
                } else {
                    let s = self.hot[b];
                    b += 1;
                    if a < self.cold.len() && self.cold[a].i == s.i {
                        a += 1;
                    }
                    s
                };
            if next.delta != [0; 8]
                && self
                    .wide
                    .binary_search_by_key(&(next.i as u64), |s| s.i)
                    .is_err()
            {
                out.push(next);
            }
        }
        out
    }
    pub fn compact(&mut self) {
        self.cold = self.merged();
        self.cold.shrink_to_fit();
        self.hot = Vec::new();
        self.wide.shrink_to_fit();
    }
    pub fn scar(&mut self, i: u64, body: Body) {
        assert!(i < self.n);
        let base = self.base(i);
        let circular = |a: u64, b: u64, bits: u8| {
            let shift = 64 - bits;
            (a.wrapping_sub(b) << shift) as i64 >> shift
        };
        let d = [
            body.p.wrapping_sub(base.p) as i64,
            body.e.wrapping_sub(base.e) as i64,
            circular(body.w, base.w, self.spec.w_bits),
            circular(body.t, base.t, self.spec.t_bits),
        ];
        let exact_circle = body.w < 1u64 << self.spec.w_bits && body.t < 1u64 << self.spec.t_bits;
        if exact_circle && d.iter().all(|&d| i16::try_from(d).is_ok()) {
            if let Ok(j) = self.wide.binary_search_by_key(&i, |s| s.i) {
                self.wide.remove(j);
            }
            if self.hot.last().is_some_and(|s| i <= s.i as u64) {
                self.compact();
            }
            if self.hot.len() == self.hot.capacity() {
                self.hot.reserve_exact((self.hot.len() / 16).max(1));
            }
            let mut delta = [0; 8];
            for c in 0..4 {
                delta[2 * c..2 * c + 2].copy_from_slice(&(d[c] as i16).to_le_bytes());
            }
            self.hot.push(Scar { i: i as u32, delta });
        } else {
            match self.wide.binary_search_by_key(&i, |s| s.i) {
                Ok(j) => self.wide[j].body = body,
                Err(j) => {
                    self.wide.reserve_exact(1);
                    self.wide.insert(j, Wide { i, body });
                }
            }
        }
    }
    /// Count parameters in memory and the allocated scar buffers, not just their payload.
    /// Derived quantiles carry no population information and are excluded by the contract.
    pub fn bytes_used(&self) -> u64 {
        (std::mem::size_of::<Spec>()
            + 16
            + std::mem::size_of_val(&self.keys)
            + (self.cold.capacity() + self.hot.capacity()) * std::mem::size_of::<Scar>()
            + self.wide.capacity() * std::mem::size_of::<Wide>()) as u64
    }
    pub fn store(&self) -> Vec<u8> {
        let mut out = Vec::new();
        out.extend_from_slice(b"BLT1");
        out.extend_from_slice(&self.n.to_le_bytes());
        out.extend_from_slice(&self.seed.to_le_bytes());
        out.extend_from_slice(&self.spec.p_lo.to_le_bytes());
        out.push(self.spec.p_bits);
        out.extend_from_slice(&self.spec.sigma_milli.to_le_bytes());
        out.push(self.spec.e_bits);
        out.extend_from_slice(&self.spec.e_cap.to_le_bytes());
        out.extend([self.spec.w_bits, self.spec.t_bits]);
        let records = self.merged();
        out.extend_from_slice(&(records.len() as u32).to_le_bytes());
        for s in records {
            out.extend_from_slice(&s.i.to_le_bytes());
            out.extend_from_slice(&s.delta);
        }
        out.extend_from_slice(&(self.wide.len() as u32).to_le_bytes());
        for s in &self.wide {
            out.extend_from_slice(&(s.i as u32).to_le_bytes());
            for v in [s.body.p, s.body.e, s.body.w, s.body.t] {
                out.extend_from_slice(&v.to_le_bytes());
            }
        }
        out
    }
    pub fn restore(bytes: &[u8]) -> Option<Self> {
        struct Reader<'a> {
            b: &'a [u8],
            p: usize,
        }
        impl Reader<'_> {
            fn read<const N: usize>(&mut self) -> Option<[u8; N]> {
                let v = self
                    .b
                    .get(self.p..self.p.checked_add(N)?)?
                    .try_into()
                    .ok()?;
                self.p += N;
                Some(v)
            }
            fn byte(&mut self) -> Option<u8> {
                Some(self.read::<1>()?[0])
            }
            fn u32(&mut self) -> Option<u32> {
                Some(u32::from_le_bytes(self.read()?))
            }
            fn u64(&mut self) -> Option<u64> {
                Some(u64::from_le_bytes(self.read()?))
            }
        }
        let mut r = Reader { b: bytes, p: 0 };
        if r.read::<4>()? != *b"BLT1" {
            return None;
        }
        let (n, seed) = (r.u64()?, r.u64()?);
        let spec = Spec {
            p_lo: r.u32()?,
            p_bits: r.byte()?,
            sigma_milli: u16::from_le_bytes(r.read()?),
            e_bits: r.byte()?,
            e_cap: r.u32()?,
            w_bits: r.byte()?,
            t_bits: r.byte()?,
        };
        let count = r.u32()? as usize;
        if count > n as usize || count > bytes.len().saturating_sub(r.p) / 12 {
            return None;
        }
        let mut belt = Self::birth(spec, n, seed)?;
        belt.cold.reserve_exact(count);
        for _ in 0..count {
            let s = Scar {
                i: r.u32()?,
                delta: r.read()?,
            };
            if s.i as u64 >= n || s.delta == [0; 8] || belt.cold.last().is_some_and(|p| p.i >= s.i)
            {
                return None;
            }
            belt.cold.push(s);
        }
        let count = r.u32()? as usize;
        if count > n as usize || count > bytes.len().saturating_sub(r.p) / 36 {
            return None;
        }
        belt.wide.reserve_exact(count);
        for _ in 0..count {
            let i = r.u32()? as u64;
            let body = Body {
                p: r.u64()?,
                e: r.u64()?,
                w: r.u64()?,
                t: r.u64()?,
            };
            if i >= n
                || belt.wide.last().is_some_and(|p| p.i >= i)
                || belt.cold.binary_search_by_key(&(i as u32), |s| s.i).is_ok()
            {
                return None;
            }
            belt.wide.push(Wide { i, body });
        }
        (r.p == bytes.len()).then_some(belt)
    }
}
