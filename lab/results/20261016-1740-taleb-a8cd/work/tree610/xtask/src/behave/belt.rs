//! B18 belt (docs/law.md, row "B18 belt", 5 October; Julien: "ok for the belt"). FROZEN on 5 October as gate B18b, after the
//! GLM red-team of the row (run 20261005-1404: four holes, F1 to F4, all repaired below): a default gate of `behave`, after B18.
//!
//! The thing judged is a belt program: a smooth population (banded p, Rayleigh e, uniform angles) of 2^20 or 2^23
//! bodies, born as a program (the lab's gold components-98bc: body i is a pure function of its ordinal). The judge
//! knows no belt code. It speaks to a belt through the narrow interface below, built by `Law::belt_birth` and
//! `Law::belt_restore`; a law that has not implemented them fails (the trait default is None).
//!
//! ## The interface ([`Belt`], on the integers of [`SPEC`])
//! - `body(i)`: regenerate ordinal i: the draw (p, e, omega, t_p), each on the grid of the spec.
//! - `store()` and `restore`: the whole store as bytes, and the belt rebuilt from those bytes alone.
//! - `bytes_used()`: what it holds that is specific to the population (parameters, scars). The judge charges the larger of
//!   this and `store().len()`. A table derived from the spec is a working constant, not counted, and not stored.
//! - `scar(i, body)`: history rewrites one body: afterwards `body(i)` is that body and nothing else changed.
//! - `form()`: [`Form::Program`] (with the bytes of its parameters, its information: at most [`INFO_CAP`]) or [`Form::Sample`]
//!   (a stored iid draw, judged under B18's iid floor rule, which this case leaves unchanged).
//!
//! ## The row's four criteria, and the statistics that decide them (all thresholds frozen here)
//! "Within its sampling noise" is a number: a z-score against the null of an iid draw of the same distribution,
//! or a two-sample statistic against the judge's own iid reference (xoshiro256**, a different family from the
//! in-judge belt's SplitMix counter stream) drawn at the same n.
//! 1. *Determinism and exact round trip.* A 64-bit hash per ordinal from one ascending pass is the truth. Every other
//!    pass must reproduce it: ascending again, descending, scrambled (i to i*K + c mod n), and 4 to 8 threads (chunks,
//!    interleaved, reversed). Two births from the same (spec, n, seed) store the same bytes. `restore(store())`
//!    regenerates every ordinal and stores the same bytes again. Exact: one mismatch fails.
//! 2. *Exact individuals.*
//!    - No two bodies share a state (the sorted hashes have no repeat; exact).
//!    - 2-D chi-square in (p, t_p) on 128 x 128 cells, dof 16383: the distance from dof, in units of sqrt(2 dof), is
//!      at most [`Z_CHI`], on either side (a lattice is too regular, a repeat too clumped).
//!    - Serial correlation of the probability-integral scores of each column at 18 lags (1 to 8, then 2^4 to 2^16) and
//!      of the 18 cross pairs (lag 0, lag 1): r times sqrt(count) is at most [`Z_SERIAL`] in absolute value (under iid
//!      r is N(0, 1/count)).
//!    - Per-column two-sample KS against the iid reference: D at most [`KS_C`] * sqrt(2/n), the asymptotic critical
//!      value at alpha = 1e-5.
//!    - The reference runs through the same tests: if it fails them, the judge is broken, and says so.
//! 3. *Tails survive*, at both ends of e and of p (the top and the bottom 1e-4; the bottom ends are the top ones mirrored:
//!    depth is the distance from the end). k = ceil(1e-4 n); thr = the reference's k-th deepest.
//!    - Count: X is the number of belt values at least as deep as thr. With the reference's own count K = k, X - K has
//!      variance 2K (the belt's binomial noise plus the noise of the reference's threshold), so |X - K| / sqrt(2K) is
//!      at most [`Z_TAIL`]. (Simulated: sd 0.95 to 0.97 over 120 iid pairs at k = 27 and 105.)
//!    - Range, two exact order-statistic tests, each wrong with probability 2^-20 under iid: the belt's deepest value
//!      reaches the reference's 20th deepest (the tail is not clipped), and the belt's 20th deepest does not pass the
//!      reference's deepest (nor stretched). Every value lies inside the law's support.
//!    - Shape: two-sample KS between the belt's X tail values and the reference's k, at the KS_C level.
//!    - Spread (red-team F1): conditional on thr, the belt's tail is exactly the law's tail, so -ln w is exponential with
//!      mean 1 (w the law's conditional survival score); the sum of (-ln w - 1) over the tail over sqrt(X) is a z, at most
//!      [`Z_TAIL`], and the same z pooled over the runs (sum over total X). A mean, not a sup: it sees a crush of the tail's
//!      spread that keeps its count and its reach. Its best possible z for a crush of c is c sqrt(X): 15% gives 4.4 at
//!      X = 850 (a 2^23 run) and 6.7 pooled over the five runs, so a crush of about 13% and over is the gate's floor.
//!    - Company (F3): the tail bodies' other three columns stay uniform: one-sample KS of each, D at most KS_C / sqrt(X).
//!    The reference's own tails run through the spread and company tests as the judge's control. (The angles have no tail:
//!    the ends of a circle are not special. A hollow in an arc of omega or t_p is the 2-D chi-square's and the company
//!    test's business, not a tail's.)
//! 4. *Bytes.*
//!    - Program form, at birth: the declared information is at most [`INFO_CAP`] bytes (red-team F4: a program's information
//!      is its parameters; a table derived from them is not information, so the belt derives it at birth and its store does
//!      not carry it); charge at most 2 x info + 2 bytes (`memory::limit_bytes`); the declaration is bound (charge at least
//!      info, and neither grows with n: 2^23 against 2^20, at most 16 bytes more). `bytes_used` counts what is specific to
//!      the population (parameters, scars); a table derived from the spec is a working constant, not counted.
//!    - Sample form, at birth: B18's rule, bytes per body in [0.5, 2] x the draw entropy + 2 bytes.
//!    - After 12 epochs of churn at 1e-2 (replacement kicks of 50 bits, relative to the program): Program, the bytes
//!      added per scarred body are in [0.5, 2] x the scar's information floor + 2 bytes (the floor is log2 C(n, m) / m
//!      for which ordinals, plus 50 for the kick; the lower bound is B18's "a lossless store cannot be there"); Sample,
//!      total per body within the same rule as at birth. The churned belt still returns every scar and every other
//!      ordinal exactly, and round-trips.
//!    - Reported, not gated: bytes at 1e9, and what 12 epochs of churn cost there.
//!
//! The row says "its tables and parameters"; this judge reads it as its parameters (the cap above), because a table
//! derived from the spec carries no information. The integrator rewords the row at the freeze.
//!
//! ## Controls and plants (the gate must pass the first three and fail every other)
//! [`ProgramBelt`] with [`Flaw::None`] is the exact in-judge reference belt (a SplitMix64 counter stream through an
//! integer-reproducible Rayleigh quantile; it passes), [`Flaw::Dyadic`] a two-level dyadic quantile table (2^12 cells in each
//! octave of the probability, at both ends; it passes), and [`SampleBelt`] an iid draw stored as packed blocks (passes under
//! the iid rule). The plants: [`Flaw::Table12`] (e through the gold's 2^12-entry midpoint quantile table: both ends of e fall
//! in one cell), [`Flaw::Winsor`] (both columns clipped at their 1 - 1e-4 quantile: the count survives, the range does not),
//! [`Flaw::Repeat`] (the states repeat every n/4), [`Flaw::Serial`] (a seventh of the odd bodies copy their neighbour's t_p),
//! [`Flaw::Thread`] (a shared call counter), [`Flaw::Fat`] (one more byte per body in the store), [`Flaw::Lattice`] (the lab's
//! rank-1 lattice: perfect marginals, structure in the plane), [`Flaw::FatScars`] (the program right, the scars 40 bytes
//! each), a [`SampleBelt`] kept as 64-byte ships; and the red-team's four holes (GLM run 20261005-1404, F1 to F4):
//! [`Flaw::Crush`] (the e-tail's spread crushed 15%), [`Flaw::InnerClip`] (a hollow inner edge of p), [`Flaw::Aligned`] (the
//! deep dippers in one 1/32 of the omega circle) and [`Flaw::Table20`] (a 4 MB table in the store, declared as information).

use super::memory::limit_bytes;
use super::{Gate, Law};
use std::cmp::Reverse;
use std::collections::{BTreeMap, BinaryHeap};
use std::sync::atomic::{AtomicU64, Ordering};
use std::time::Instant;

// ---------------------------------------------------------------------------------------------------------------
// The belt the row names, on integers.

/// The frozen belt: p uniform over a band, e Rayleigh, the angle and the periapsis time uniform. Integers all:
/// p on the law's 2^16 scale (`Key::darwin`), e on its 2^30 grid.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct BeltSpec {
    /// p = p_lo + (uniform over 2^p_bits).
    pub p_lo: u64,
    pub p_bits: u32,
    /// Rayleigh sigma of e, in thousandths (70 is 0.070).
    pub sigma_milli: u64,
    /// e is on the grid 2^e_bits; no body has e above e_cap (P(e > 0.6) is 1e-16 under the law).
    pub e_bits: u32,
    pub e_cap: u64,
    /// omega is uniform over 2^w_bits; t_p over 2^t_bits time quanta.
    pub w_bits: u32,
    pub t_bits: u32,
}
impl BeltSpec {
    pub fn sigma(&self) -> f64 {
        self.sigma_milli as f64 / 1000.0
    }
}
/// Darwin p in [2048, 2560) at 2^16; e Rayleigh sigma 0.07 on the 2^30 grid, capped at 0.6; omega 32 bits; t_p over
/// 2^44 quanta: the gold's belt (lab components-98bc), without its kind.
pub const SPEC: BeltSpec = BeltSpec { p_lo: 2048 << 16, p_bits: 27, sigma_milli: 70, e_bits: 30, e_cap: 644_245_094, w_bits: 32, t_bits: 44 };

/// One body of the belt: its draw.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Body {
    pub p: u64,
    pub e: u64,
    pub w: u64,
    pub t: u64,
}
impl Body {
    /// A 64-bit hash of the state (the judge's witness that two regenerations are the same body).
    pub fn hash(&self) -> u64 {
        mix64(self.p ^ mix64(self.e ^ mix64(self.w ^ mix64(self.t))))
    }
}

/// What a belt says it is.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Form {
    /// Bodies are a function of their ordinal. `info_bytes` is the program's information: its tables and parameters.
    Program { info_bytes: u64 },
    /// An iid draw stored as it is (judged under B18's iid floor rule).
    Sample,
}

/// What the judge asks of a belt. See the module doc. `body` is called from many threads at once (`Sync`), in any order.
pub trait Belt: Sync {
    /// The number of bodies (ordinals 0..len).
    fn len(&self) -> u64;
    /// Ordinal `i`, exactly: the same body on every call, thread, order, machine and restore.
    fn body(&self, i: u64) -> Body;
    /// The whole store, as bytes: `Law::belt_restore` rebuilds the belt from these alone.
    fn store(&self) -> Vec<u8>;
    /// The bytes the belt holds (the judge charges the larger of this and `store().len()`).
    fn bytes_used(&self) -> u64;
    /// History rewrites ordinal `i`: afterwards `body(i)` is `b` and no other ordinal changes. The judge calls it in
    /// ascending ordinal order within an epoch, and may rewrite the same ordinal again in a later epoch.
    fn scar(&mut self, i: u64, b: Body);
    /// A program (with the bytes of its tables and parameters) or a stored draw.
    fn form(&self) -> Form;
}

// ---------------------------------------------------------------------------------------------------------------
// Arithmetic the judge and its reference share.

const GAMMA: u64 = 0x9E37_79B9_7F4A_7C15;
/// The SplitMix64 finalizer.
#[inline]
fn mix64(mut z: u64) -> u64 {
    z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
    z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
    z ^ (z >> 31)
}
/// The k-th output of the SplitMix64 stream of `seed`: a counter-based generator, no state.
#[inline]
fn at(seed: u64, k: u64) -> u64 {
    mix64(seed.wrapping_add(k.wrapping_add(1).wrapping_mul(GAMMA)))
}

/// xoshiro256** (Blackman and Vigna): the judge's iid reference, a family apart from the reference belt's SplitMix.
struct Xoshiro([u64; 4]);
impl Xoshiro {
    fn new(seed: u64) -> Self {
        Xoshiro([at(seed, 0), at(seed, 1), at(seed, 2), at(seed, 3)])
    }
    #[inline]
    fn next(&mut self) -> u64 {
        let s = &mut self.0;
        let r = s[1].wrapping_mul(5).rotate_left(7).wrapping_mul(9);
        let t = s[1] << 17;
        s[2] ^= s[0];
        s[3] ^= s[1];
        s[1] ^= s[2];
        s[0] ^= s[3];
        s[2] ^= t;
        s[3] = s[3].rotate_left(45);
        r
    }
}

/// ln x for a positive normal x from +, -, *, / only (IEEE-exact, so the same bits on every machine): the exponent,
/// then 2 atanh((m-1)/(m+1)) for the mantissa in [sqrt(1/2), sqrt(2)).
fn ln_det(x: f64) -> f64 {
    let bits = x.to_bits();
    let mut k = ((bits >> 52) & 0x7FF) as i64 - 1023;
    let mut m = f64::from_bits((bits & 0x000F_FFFF_FFFF_FFFF) | 0x3FF0_0000_0000_0000);
    if m > std::f64::consts::SQRT_2 {
        m *= 0.5;
        k += 1;
    }
    let z = (m - 1.0) / (m + 1.0);
    let z2 = z * z;
    let (mut sum, mut term, mut j) = (0.0, z, 1.0);
    for _ in 0..14 {
        sum += term / j;
        term *= z2;
        j += 2.0;
    }
    k as f64 * std::f64::consts::LN_2 + 2.0 * sum
}

/// e on the 2^e_bits grid for the uniform word `u`: sigma * sqrt(-2 ln v), v = (top 52 bits + 1/2) / 2^52, floored and
/// capped. Reproducible bit for bit (sqrt is IEEE-exact; `ln_det` above).
fn rayleigh_grid(u: u64, spec: &BeltSpec) -> u64 {
    let v = ((u >> 12) as f64 + 0.5) / 4_503_599_627_370_496.0;
    let e = spec.sigma() * (-2.0 * ln_det(v)).sqrt();
    ((e * (1u64 << spec.e_bits) as f64) as u64).min(spec.e_cap)
}
/// e on the grid for a given ln v (v uniform; e = sigma sqrt(-2 ln v)), capped.
fn e_grid_from_ln(ln_v: f64, spec: &BeltSpec) -> u64 {
    ((spec.sigma() * (-2.0 * ln_v).sqrt() * (1u64 << spec.e_bits) as f64) as u64).min(spec.e_cap)
}
/// The e (on the grid) that a fraction `q` of the law lies above.
pub fn e_quantile_grid(q: f64, spec: &BeltSpec) -> u64 {
    ((spec.sigma() * (-2.0 * q.ln()).sqrt() * (1u64 << spec.e_bits) as f64) as u64).min(spec.e_cap)
}

/// An iid body from the judge's generator: one word per column.
fn iid_body(rng: &mut Xoshiro, spec: &BeltSpec) -> Body {
    Body { p: spec.p_lo + (rng.next() >> (64 - spec.p_bits)), e: rayleigh_grid(rng.next(), spec), w: rng.next() >> (64 - spec.w_bits), t: rng.next() >> (64 - spec.t_bits) }
}

/// The entropy of one iid body of the spec, in bits: the draw entropy that B18's iid floor rule charges. p, omega and
/// t_p are uniform; e is Rayleigh on a grid fine against sigma, where H = h(e) + e_bits and
/// h = 1 + ln(sigma / sqrt 2) + gamma / 2 nats.
pub fn iid_floor_bits(spec: &BeltSpec) -> f64 {
    let h_nats = 1.0 + (spec.sigma() / std::f64::consts::SQRT_2).ln() + 0.577_215_664_901_532_9 / 2.0;
    spec.p_bits as f64 + spec.w_bits as f64 + spec.t_bits as f64 + spec.e_bits as f64 + h_nats / std::f64::consts::LN_2
}

// ---------------------------------------------------------------------------------------------------------------
// The in-judge reference belt, and its plants.

/// The flaws planted into the reference belt (`Flaw::None` is the reference itself).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Flaw {
    None,
    /// e through a 2^12-entry midpoint quantile table (the gold's), so the top 1e-4 sits in one cell.
    Table12,
    /// p and e clipped at their 1 - 1e-4 quantile.
    Winsor,
    /// body i is body i mod (n/4).
    Repeat,
    /// one odd body in seven copies its neighbour's t_p.
    Serial,
    /// the draw depends on a call counter shared by every thread.
    Thread,
    /// the store carries one more byte per body.
    Fat,
    /// body i is i times a constant per column (the lab's rank-1 lattice: perfect marginals, stripes in the plane).
    Lattice,
    /// the scars are stored as fixed 40-byte records.
    FatScars,
    /// A CONTROL, not a plant: e through a two-level dyadic quantile table, 2^12 cells in each octave of the probability
    /// at BOTH ends (indexed by the side, the leading zeros of the draw's distance from that end, then its next 12 bits).
    /// It resolves both tails of e to 2^-53 and passes. (Dyadic at the top end only clips the bottom 1e-4 of e.)
    Dyadic,
    /// every e above the 1 - 1e-4 quantile is pulled 15% toward that quantile (the tail's spread crushed; count and
    /// reach survive).
    Crush,
    /// the same crush at 12%: each run passes on its own and only the pooled tail test sees it.
    Crush12,
    /// p clipped from below at its 1e-4 quantile (a hollow inner edge).
    InnerClip,
    /// the e-tail bodies (the top 1e-4) all take their omega from one 1/32 of the circle.
    Aligned,
    /// e through a one-level 2^20-cell midpoint quantile table that the store carries (4 MB) and declares as information.
    Table20,
}
impl Flaw {
    fn code(self) -> u8 {
        self as u8
    }
    fn from_code(c: u8) -> Option<Flaw> {
        [Flaw::None, Flaw::Table12, Flaw::Winsor, Flaw::Repeat, Flaw::Serial, Flaw::Thread, Flaw::Fat, Flaw::Lattice, Flaw::FatScars, Flaw::Dyadic, Flaw::Crush, Flaw::Crush12, Flaw::InnerClip, Flaw::Aligned, Flaw::Table20].get(c as usize).copied()
    }
}

fn put_varint(out: &mut Vec<u8>, mut v: u64) {
    while v >= 0x80 {
        out.push((v as u8) | 0x80);
        v >>= 7;
    }
    out.push(v as u8);
}
fn get_varint(b: &[u8], at: &mut usize) -> Option<u64> {
    let (mut v, mut shift) = (0u64, 0u32);
    loop {
        let byte = *b.get(*at)?;
        *at += 1;
        v |= ((byte & 0x7F) as u64).checked_shl(shift)?;
        if byte & 0x80 == 0 {
            return Some(v);
        }
        shift += 7;
        if shift > 63 {
            return None;
        }
    }
}
fn zigzag(d: u64) -> u64 {
    let d = d as i64;
    ((d << 1) ^ (d >> 63)) as u64
}
fn unzigzag(z: u64) -> u64 {
    ((z >> 1) as i64 ^ -((z & 1) as i64)) as u64
}

/// The reference belt: body i is a pure function of (seed, i): the four outputs 4i..4i+3 of the SplitMix64 stream of
/// the seed, through the spec. The store is its parameters (41 bytes) and its scars.
pub struct ProgramBelt {
    flaw: Flaw,
    spec: BeltSpec,
    n: u64,
    seed: u64,
    /// The quantile table of Table12, Dyadic or Table20 (derived at birth; only Table20's store carries it).
    table: Vec<u64>,
    /// The e that 1e-4 of the law lies above, and p's 1e-4 quantiles (offsets): the cuts of the tail plants.
    cut_e: u64,
    cut_p_lo: u64,
    cut_p_hi: u64,
    scars: BTreeMap<u64, Body>,
    calls: AtomicU64,
}

const HEADER_BYTES: usize = 41;

impl ProgramBelt {
    pub fn birth(spec: &BeltSpec, n: u64, seed: u64, flaw: Flaw) -> ProgramBelt {
        let table = match flaw {
            Flaw::Table12 => (0..4096).map(|j| e_quantile_grid(1.0 - (j as f64 + 0.5) / 4096.0, spec)).collect(),
            Flaw::Table20 => (0..1u64 << 20).map(|j| e_quantile_grid(1.0 - (j as f64 + 0.5) / (1u64 << 20) as f64, spec)).collect(),
            Flaw::Dyadic => (0..2 * 53 * 4096)
                .map(|c| {
                    let (side, lz, j) = (c / (53 * 4096), (c / 4096) % 53, c % 4096);
                    let dist = if lz == 52 { 2f64.powi(-53) } else { 2f64.powi(-(lz as i32 + 1)) * (1.0 + (j as f64 + 0.5) / 4096.0) };
                    e_grid_from_ln(if side == 0 { dist.ln() } else { (-dist).ln_1p() }, spec)
                })
                .collect(),
            _ => Vec::new(),
        };
        let cut_e = e_quantile_grid(1e-4, spec);
        let cut_p_lo = (1e-4 * (1u64 << spec.p_bits) as f64) as u64;
        let cut_p_hi = ((1.0 - 1e-4) * (1u64 << spec.p_bits) as f64) as u64;
        ProgramBelt { flaw, spec: *spec, n, seed, table, cut_e, cut_p_lo, cut_p_hi, scars: BTreeMap::new(), calls: AtomicU64::new(0) }
    }
    /// The program's body for ordinal `i`, with the flaw but without scars.
    fn program(&self, i: u64) -> Body {
        let s = &self.spec;
        let i = if self.flaw == Flaw::Repeat { i % (self.n / 4).max(1) } else { i };
        let i = if self.flaw == Flaw::Thread { self.calls.fetch_add(1, Ordering::Relaxed) } else { i };
        let k = i.wrapping_mul(4);
        let (wp, we, ww, wt) = if self.flaw == Flaw::Lattice {
            let g = |c: u64| at(self.seed, c) | 1;
            (i.wrapping_mul(g(0)), i.wrapping_mul(g(1)), i.wrapping_mul(g(2)), i.wrapping_mul(g(3)))
        } else {
            (at(self.seed, k), at(self.seed, k + 1), at(self.seed, k + 2), at(self.seed, k + 3))
        };
        let mut b = Body { p: s.p_lo + (wp >> (64 - s.p_bits)), e: rayleigh_grid(we, s), w: ww >> (64 - s.w_bits), t: wt >> (64 - s.t_bits) };
        match self.flaw {
            Flaw::Table12 => b.e = self.table[(we >> 52) as usize],
            Flaw::Table20 => b.e = self.table[(we >> 44) as usize],
            Flaw::Dyadic => {
                let u = we >> 12;
                let (side, t) = if u < 1 << 51 { (0usize, u) } else { (1, (1u64 << 52) - 1 - u) };
                let lz = t.leading_zeros() as usize - 12;
                let j = if lz >= 51 { 0 } else { ((t << (13 + lz)) >> 52) as usize };
                b.e = self.table[(side * 53 + lz) * 4096 + j];
            }
            Flaw::Winsor => {
                b.e = b.e.min(self.cut_e);
                b.p = b.p.min(s.p_lo + self.cut_p_hi);
            }
            Flaw::Crush if b.e > self.cut_e => b.e = self.cut_e + (b.e - self.cut_e) * 85 / 100,
            Flaw::Crush12 if b.e > self.cut_e => b.e = self.cut_e + (b.e - self.cut_e) * 88 / 100,
            Flaw::InnerClip => b.p = b.p.max(s.p_lo + self.cut_p_lo),
            Flaw::Aligned if b.e > self.cut_e => b.w >>= 5,
            Flaw::Serial if i % 2 == 1 && at(self.seed ^ 0x5E21A1, i) >> 61 == 0 => {
                b.t = at(self.seed, (i - 1).wrapping_mul(4) + 3) >> (64 - s.t_bits);
            }
            _ => {}
        }
        b
    }
    /// The program without the call counter: what scars are measured against (the same for every other flaw).
    fn base(&self, i: u64) -> Body {
        if self.flaw == Flaw::Thread {
            ProgramBelt::birth(&self.spec, self.n, self.seed, Flaw::None).program(i)
        } else {
            self.program(i)
        }
    }
    /// The program's information as it declares it: its parameters, and (Table20) the table its store carries.
    fn info_bytes(&self) -> u64 {
        HEADER_BYTES as u64 + if self.flaw == Flaw::Table20 { 4 << 20 } else { 0 }
    }
    pub fn restore(bytes: &[u8]) -> Option<ProgramBelt> {
        if bytes.len() < HEADER_BYTES || bytes[0] != b'B' || bytes[1] != 1 {
            return None;
        }
        let flaw = Flaw::from_code(bytes[2])?;
        let u64_at = |o: usize| u64::from_le_bytes(bytes[o..o + 8].try_into().unwrap());
        let spec = BeltSpec { p_lo: u64_at(19), p_bits: bytes[27] as u32, sigma_milli: u16::from_le_bytes([bytes[28], bytes[29]]) as u64, e_bits: bytes[30] as u32, e_cap: u64_at(31), w_bits: bytes[39] as u32, t_bits: bytes[40] as u32 };
        let mut belt = ProgramBelt::birth(&spec, u64_at(3), u64_at(11), flaw);
        let mut at = HEADER_BYTES;
        let count = get_varint(bytes, &mut at)?;
        let mut prev = 0u64;
        for j in 0..count {
            let (i, mut d) = if flaw == Flaw::FatScars {
                let rec = bytes.get(at..at + 40)?;
                at += 40;
                let word = |k: usize| u64::from_le_bytes(rec[8 * k..8 * k + 8].try_into().unwrap());
                (word(0), [word(1), word(2), word(3), word(4)])
            } else {
                let gap = get_varint(bytes, &mut at)?;
                let mut d = [0u64; 4];
                (if j == 0 { gap } else { prev + 1 + gap }, {
                    for x in &mut d {
                        *x = unzigzag(get_varint(bytes, &mut at)?);
                    }
                    d
                })
            };
            let base = belt.base(i);
            let _ = &mut d;
            belt.scars.insert(i, Body { p: base.p.wrapping_add(d[0]), e: base.e.wrapping_add(d[1]), w: base.w.wrapping_add(d[2]), t: base.t.wrapping_add(d[3]) });
            prev = i;
        }
        if flaw == Flaw::Fat {
            at += belt.n as usize;
        }
        if flaw == Flaw::Table20 {
            at += 4 << 20;
        }
        (at == bytes.len()).then_some(belt)
    }
}
impl Belt for ProgramBelt {
    fn len(&self) -> u64 {
        self.n
    }
    fn body(&self, i: u64) -> Body {
        if !self.scars.is_empty() {
            if let Some(b) = self.scars.get(&i) {
                return *b;
            }
        }
        self.program(i)
    }
    fn store(&self) -> Vec<u8> {
        let mut out = vec![b'B', 1, self.flaw.code()];
        out.extend(self.n.to_le_bytes());
        out.extend(self.seed.to_le_bytes());
        out.extend(self.spec.p_lo.to_le_bytes());
        out.push(self.spec.p_bits as u8);
        out.extend((self.spec.sigma_milli as u16).to_le_bytes());
        out.push(self.spec.e_bits as u8);
        out.extend(self.spec.e_cap.to_le_bytes());
        out.push(self.spec.w_bits as u8);
        out.push(self.spec.t_bits as u8);
        debug_assert_eq!(out.len(), HEADER_BYTES);
        put_varint(&mut out, self.scars.len() as u64);
        let mut prev = 0u64;
        for (j, (&i, b)) in self.scars.iter().enumerate() {
            let base = self.base(i);
            let d = [b.p.wrapping_sub(base.p), b.e.wrapping_sub(base.e), b.w.wrapping_sub(base.w), b.t.wrapping_sub(base.t)];
            if self.flaw == Flaw::FatScars {
                out.extend(i.to_le_bytes());
                d.iter().for_each(|x| out.extend(x.to_le_bytes()));
            } else {
                put_varint(&mut out, if j == 0 { i } else { i - prev - 1 });
                d.iter().for_each(|&x| put_varint(&mut out, zigzag(x)));
            }
            prev = i;
        }
        if self.flaw == Flaw::Fat {
            out.extend((0..self.n).map(|i| mix64(i) as u8));
        }
        if self.flaw == Flaw::Table20 {
            out.extend(self.table.iter().flat_map(|&e| (e as u32).to_le_bytes()));
        }
        out
    }
    fn bytes_used(&self) -> u64 {
        self.store().len() as u64
    }
    fn scar(&mut self, i: u64, b: Body) {
        self.scars.insert(i, b);
    }
    fn form(&self) -> Form {
        Form::Program { info_bytes: self.info_bytes() }
    }
}

/// A belt stored as a draw: iid bodies from the belt's own generator, packed 133 bits to the body in blocks (or, kept
/// as 64-byte ships, `fat`). Scars replace bodies in an exception list. It is the control for B18's iid rule.
pub struct SampleBelt {
    spec: BeltSpec,
    n: u64,
    fat: bool,
    words: Vec<u64>,
    ships: Vec<[u64; 8]>,
    scars: BTreeMap<u64, Body>,
}
const SAMPLE_HEADER: usize = 20;
impl SampleBelt {
    fn bits_per(spec: &BeltSpec) -> usize {
        (spec.p_bits + spec.e_bits + spec.w_bits + spec.t_bits) as usize
    }
    pub fn birth(spec: &BeltSpec, n: u64, seed: u64, fat: bool) -> SampleBelt {
        let mut rng = Xoshiro::new(seed ^ 0xB0D1E5_5A3F1E);
        let mut belt = SampleBelt { spec: *spec, n, fat, words: Vec::new(), ships: Vec::new(), scars: BTreeMap::new() };
        if fat {
            belt.ships = (0..n).map(|_| {
                let b = iid_body(&mut rng, spec);
                [b.p, b.e, b.w, b.t, 0, 0, 0, 0]
            }).collect();
        } else {
            belt.words = vec![0; (n as usize * Self::bits_per(spec)).div_ceil(64) + 1];
            for i in 0..n as usize {
                let b = iid_body(&mut rng, spec);
                belt.put(i, &b);
            }
        }
        belt
    }
    fn put(&mut self, i: usize, b: &Body) {
        let s = self.spec;
        let mut pos = i * Self::bits_per(&s);
        for (v, w) in [(b.p - s.p_lo, s.p_bits), (b.e, s.e_bits), (b.w, s.w_bits), (b.t, s.t_bits)] {
            for bit in 0..w as usize {
                self.words[(pos + bit) / 64] |= ((v >> bit) & 1) << ((pos + bit) % 64);
            }
            pos += w as usize;
        }
    }
    fn get(&self, pos: usize, width: u32) -> u64 {
        let (word, off) = (pos / 64, pos % 64);
        let lo = self.words[word] >> off;
        let hi = if off + width as usize > 64 { self.words[word + 1] << (64 - off) } else { 0 };
        (lo | hi) & ((1u64 << width) - 1)
    }
    pub fn restore(bytes: &[u8]) -> Option<SampleBelt> {
        if bytes.len() < SAMPLE_HEADER || bytes[0] != b'S' || bytes[1] != 1 {
            return None;
        }
        let fat = bytes[2] == 1;
        let n = u64::from_le_bytes(bytes[3..11].try_into().ok()?);
        let mut belt = SampleBelt { spec: SPEC, n, fat, words: Vec::new(), ships: Vec::new(), scars: BTreeMap::new() };
        let mut at = SAMPLE_HEADER;
        if fat {
            let end = at.checked_add(n as usize * 64)?;
            let body = bytes.get(at..end)?;
            belt.ships = body.chunks_exact(64).map(|c| std::array::from_fn(|k| u64::from_le_bytes(c[8 * k..8 * k + 8].try_into().unwrap()))).collect();
            at = end;
        } else {
            let nwords = (n as usize * Self::bits_per(&SPEC)).div_ceil(64) + 1;
            let end = at.checked_add(nwords * 8)?;
            let body = bytes.get(at..end)?;
            belt.words = body.chunks_exact(8).map(|c| u64::from_le_bytes(c.try_into().unwrap())).collect();
            at = end;
        }
        let count = get_varint(bytes, &mut at)?;
        let mut prev = 0u64;
        for j in 0..count {
            let gap = get_varint(bytes, &mut at)?;
            let i = if j == 0 { gap } else { prev + 1 + gap };
            let mut f = [0u64; 4];
            for x in &mut f {
                *x = get_varint(bytes, &mut at)?;
            }
            belt.scars.insert(i, Body { p: f[0], e: f[1], w: f[2], t: f[3] });
            prev = i;
        }
        (at == bytes.len()).then_some(belt)
    }
}
impl Belt for SampleBelt {
    fn len(&self) -> u64 {
        self.n
    }
    fn body(&self, i: u64) -> Body {
        if let Some(b) = self.scars.get(&i) {
            return *b;
        }
        if self.fat {
            let s = &self.ships[i as usize];
            return Body { p: s[0], e: s[1], w: s[2], t: s[3] };
        }
        let sp = &self.spec;
        let pos = i as usize * Self::bits_per(sp);
        Body { p: sp.p_lo + self.get(pos, sp.p_bits), e: self.get(pos + sp.p_bits as usize, sp.e_bits), w: self.get(pos + (sp.p_bits + sp.e_bits) as usize, sp.w_bits), t: self.get(pos + (sp.p_bits + sp.e_bits + sp.w_bits) as usize, sp.t_bits) }
    }
    fn store(&self) -> Vec<u8> {
        let mut out = vec![b'S', 1, self.fat as u8];
        out.extend(self.n.to_le_bytes());
        out.resize(SAMPLE_HEADER, 0);
        if self.fat {
            for s in &self.ships {
                for w in s {
                    out.extend(w.to_le_bytes());
                }
            }
        } else {
            for w in &self.words {
                out.extend(w.to_le_bytes());
            }
        }
        put_varint(&mut out, self.scars.len() as u64);
        let mut prev = 0u64;
        for (j, (&i, b)) in self.scars.iter().enumerate() {
            put_varint(&mut out, if j == 0 { i } else { i - prev - 1 });
            for v in [b.p, b.e, b.w, b.t] {
                put_varint(&mut out, v);
            }
            prev = i;
        }
        out
    }
    fn bytes_used(&self) -> u64 {
        self.store().len() as u64
    }
    fn scar(&mut self, i: u64, b: Body) {
        self.scars.insert(i, b);
    }
    fn form(&self) -> Form {
        Form::Sample
    }
}

// ---------------------------------------------------------------------------------------------------------------
// The judge.

/// One run of the gate: a belt of 2^log2n bodies from this seed. `thorough` runs every ordering of the determinism
/// pass (the biggest runs run two).
#[derive(Clone, Copy, Debug)]
pub struct Run {
    pub log2n: u32,
    pub seed: u64,
    pub thorough: bool,
}
/// The frozen runs: three belts of 2^20 and two of 2^23 (the row's sizes), each from its own seed. (The second 2^23 adds
/// tail bodies to the pooled test: the best z for a 15% crush of the e-tail's spread is 0.15 sqrt(X), X the tail bodies.)
pub const RUNS: [Run; 5] = [
    Run { log2n: 20, seed: 20261008, thorough: true },
    Run { log2n: 20, seed: 20261009, thorough: true },
    Run { log2n: 20, seed: 20261010, thorough: true },
    Run { log2n: 23, seed: 20261011, thorough: false },
    Run { log2n: 23, seed: 20261012, thorough: false },
];
/// The population `bytes at 1e9` is reported for.
const BILLION: u64 = 1_000_000_000;

/// Every threshold is a two-sided z or a KS critical value with a false-alarm rate per test of at most 1e-5, 6e-6 or 7e-6
/// (and the gate runs about 400 of them on an iid-quality belt: a family-wise false-failure rate of about 5e-4).
pub const Z_CHI: f64 = 4.5;
pub const Z_SERIAL: f64 = 5.0;
/// The asymptotic two-sample KS critical constant at alpha = 1e-5: sqrt(-ln(alpha / 2) / 2).
pub const KS_C: f64 = 2.470;
pub const Z_TAIL: f64 = 4.5;
/// The reach and overshoot tests compare against this order statistic of the reference (wrong with probability 2^-20).
const REACH_J: usize = 20;
/// A program's information is its parameters (the spec's words, n and the seed: 41 bytes in the reference's format); the
/// cap leaves room for another encoding of them. Tables derived from the spec are not information, so a belt derives them
/// at birth and its store does not carry them (red-team F4, 5 October: a 4 MB table passed when the allowance was self-declared).
pub const INFO_CAP: u64 = 64;
const TAIL_FRACTION: f64 = 1e-4;
const BINS: usize = 1 << 16;
const SIDE: usize = 128;
const LAGS: [usize; 18] = [1, 2, 3, 4, 5, 6, 7, 8, 16, 32, 64, 128, 256, 512, 1024, 4096, 16384, 65536];
const RING: usize = 1 << 17;
const EPOCHS: u32 = 12;
const CHURN: f64 = 1e-2;
/// The kick: bits of the replacement kick on (p, e, omega, t_p): 9 + 11 + 15 + 15 = 50 bits.
const KICK_BITS: [u32; 4] = [9, 11, 15, 15];
const CHURN_SEED: u64 = 0xC4_0123_5EED;
const PAIRS: [(usize, usize); 6] = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)];

/// The probability-integral scores of a body: uniform on (0, 1) under the law.
#[inline]
fn scores(b: &Body, s: &BeltSpec) -> [f64; 4] {
    let off = (b.p.wrapping_sub(s.p_lo)).min((1u64 << s.p_bits) - 1);
    let x = (b.e.min(s.e_cap) as f64 + 0.5) / (1u64 << s.e_bits) as f64;
    let sg = s.sigma();
    [
        (off as f64 + 0.5) / (1u64 << s.p_bits) as f64,
        -(-(x * x) / (2.0 * sg * sg)).exp_m1(),
        (b.w.min((1u64 << s.w_bits) - 1) as f64 + 0.5) / (1u64 << s.w_bits) as f64,
        (b.t.min((1u64 << s.t_bits) - 1) as f64 + 0.5) / (1u64 << s.t_bits) as f64,
    ]
}
fn in_support(b: &Body, s: &BeltSpec) -> bool {
    b.p.wrapping_sub(s.p_lo) >> s.p_bits == 0 && b.e <= s.e_cap && b.w >> s.w_bits == 0 && b.t >> s.t_bits == 0
}

/// Everything one pass over a population accumulates.
struct Acc {
    n: u64,
    bad: u64,
    hist: [Vec<u32>; 4],
    cells: Vec<u32>,
    ring: [Vec<f32>; 4],
    lag: [[f64; 18]; 4],
    cross0: [f64; 6],
    cross1: [f64; 12],
    prev: [f64; 4],
}
impl Acc {
    fn new() -> Acc {
        Acc { n: 0, bad: 0, hist: std::array::from_fn(|_| vec![0; BINS]), cells: vec![0; SIDE * SIDE], ring: std::array::from_fn(|_| vec![0.0; RING]), lag: [[0.0; 18]; 4], cross0: [0.0; 6], cross1: [0.0; 12], prev: [0.0; 4] }
    }
    #[inline]
    fn push(&mut self, b: &Body, s: &BeltSpec) -> [f64; 4] {
        let i = self.n as usize;
        if !in_support(b, s) {
            self.bad += 1;
        }
        let u = scores(b, s);
        let mut x = [0.0f64; 4];
        for c in 0..4 {
            x[c] = u[c] - 0.5;
            self.hist[c][((u[c] * BINS as f64) as usize).min(BINS - 1)] += 1;
            let ring = &mut self.ring[c];
            for (j, &l) in LAGS.iter().enumerate() {
                if i >= l {
                    self.lag[c][j] += x[c] * ring[(i - l) & (RING - 1)] as f64;
                }
            }
            ring[i & (RING - 1)] = x[c] as f32;
        }
        for (k, &(a, b2)) in PAIRS.iter().enumerate() {
            self.cross0[k] += x[a] * x[b2];
        }
        if i >= 1 {
            let mut k = 0;
            for (a, xa) in x.iter().enumerate() {
                for (b2, pb) in self.prev.iter().enumerate() {
                    if a != b2 {
                        self.cross1[k] += xa * pb;
                        k += 1;
                    }
                }
            }
        }
        self.prev = x;
        let cell = (((u[0] * SIDE as f64) as usize).min(SIDE - 1)) * SIDE + ((u[3] * SIDE as f64) as usize).min(SIDE - 1);
        self.cells[cell] += 1;
        self.n += 1;
        u
    }
}
// Scores are stored as f32 in the ring: the products are summed in f64 and the rounding (6e-8) is far below the 1/sqrt(n) noise.

/// The four ends the tail tests watch: the top and the bottom 1e-4 of p and of e. The bottom ends are the mirror of the
/// top ones (depth = distance from that end), so one set of tests serves all four.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Side {
    PTop,
    ETop,
    PBottom,
    EBottom,
}
const SIDES: [Side; 4] = [Side::PTop, Side::ETop, Side::PBottom, Side::EBottom];
impl Side {
    fn name(self) -> &'static str {
        match self {
            Side::PTop => "top 1e-4 of p",
            Side::ETop => "top 1e-4 of e",
            Side::PBottom => "bottom 1e-4 of p",
            Side::EBottom => "bottom 1e-4 of e",
        }
    }
    /// The column the end belongs to: the one score the tail conditions on.
    fn col(self) -> usize {
        match self {
            Side::PTop | Side::PBottom => 0,
            _ => 1,
        }
    }
    /// How deep a body lies in this end: larger is deeper. Out-of-support bodies are as deep as they are far out, or 0.
    #[inline]
    fn depth(self, b: &Body, s: &BeltSpec) -> u64 {
        let off = b.p.wrapping_sub(s.p_lo);
        match self {
            Side::PTop => off,
            Side::PBottom => ((1u64 << s.p_bits) - 1).saturating_sub(off),
            Side::ETop => b.e,
            Side::EBottom => s.e_cap.saturating_sub(b.e),
        }
    }
    /// The score of a tail body at `depth`, uniform on (0, 1) under the law given that it lies at least as deep as `thr`.
    fn conditional(self, depth: u64, thr: u64, s: &BeltSpec) -> f64 {
        let two_sigma2 = 2.0 * s.sigma() * s.sigma();
        let g = (1u64 << s.e_bits) as f64;
        match self {
            Side::PTop | Side::PBottom => (((1u64 << s.p_bits) - depth) as f64 - 0.5) / ((1u64 << s.p_bits) - thr) as f64,
            Side::ETop => {
                let (x, xt) = ((depth as f64 + 0.5) / g, thr as f64 / g);
                (-(x * x - xt * xt) / two_sigma2).exp()
            }
            Side::EBottom => {
                let (x, xt) = (((s.e_cap - depth) as f64 + 0.5) / g, ((s.e_cap - thr) as f64 + 1.0) / g);
                (-(x * x) / two_sigma2).exp_m1() / (-(xt * xt) / two_sigma2).exp_m1()
            }
        }
    }
}
/// A tail body: its depth and its four scores (as u32 fractions).
type Entry = (u64, [u32; 4]);
fn quant(u: &[f64; 4]) -> [u32; 4] {
    u.map(|x| (x * 4_294_967_296.0) as u32)
}

/// The k deepest bodies of a side in the reference.
struct RefTail {
    heap: BinaryHeap<Reverse<Entry>>,
    k: usize,
}
impl RefTail {
    fn new(k: usize) -> Self {
        RefTail { heap: BinaryHeap::with_capacity(k + 1), k }
    }
    #[inline]
    fn push(&mut self, e: Entry) {
        if self.heap.len() < self.k {
            self.heap.push(Reverse(e));
        } else if e.0 > self.heap.peek().unwrap().0 .0 {
            self.heap.pop();
            self.heap.push(Reverse(e));
        }
    }
    /// The k deepest, deepest first.
    fn into_sorted(self) -> Vec<Entry> {
        let mut v: Vec<Entry> = self.heap.into_iter().map(|r| r.0).collect();
        v.sort_unstable_by(|a, b| b.cmp(a));
        v
    }
}
/// The belt's bodies at least as deep as the reference's threshold, and its 20 deepest.
struct BeltTail {
    thr: u64,
    count: u64,
    values: Vec<Entry>,
    cap: usize,
    top: BinaryHeap<Reverse<u64>>,
}
impl BeltTail {
    fn new(thr: u64, cap: usize) -> Self {
        BeltTail { thr, count: 0, values: Vec::new(), cap, top: BinaryHeap::with_capacity(REACH_J + 1) }
    }
    #[inline]
    fn push(&mut self, depth: u64, sc: &[u32; 4]) {
        if depth >= self.thr {
            self.count += 1;
            if self.values.len() < self.cap {
                self.values.push((depth, *sc));
            }
        }
        if self.top.len() < REACH_J {
            self.top.push(Reverse(depth));
        } else if depth > self.top.peek().unwrap().0 {
            self.top.pop();
            self.top.push(Reverse(depth));
        }
    }
}
/// The sum over `bodies` of (-ln w - 1), w the conditional score: under the law -ln w is exponential with mean 1 and
/// variance 1, so the sum divided by sqrt(X) is a z. A mean, not a sup, so a crush of the tail's spread that keeps its
/// count and its reach still moves it; and the exponential's mean is its sufficient statistic, the best test of a scale.
fn conditional_log_sum(side: Side, thr: u64, bodies: &[Entry], spec: &BeltSpec) -> f64 {
    bodies.iter().map(|b| -side.conditional(b.0, thr, spec).ln() - 1.0).sum()
}
fn log_z(sum: f64, x: usize) -> f64 {
    if x == 0 {
        f64::INFINITY
    } else {
        sum / (x as f64).sqrt()
    }
}

/// The worst one-sample KS distance from the uniform, over the three columns the side does not condition on, as a
/// fraction of its critical value KS_C / sqrt(X), with the name of the column.
fn other_columns_ks(side: Side, bodies: &[Entry]) -> (f64, &'static str) {
    let mut worst = (0.0f64, "");
    if bodies.is_empty() {
        return (f64::INFINITY, "none");
    }
    let x = bodies.len() as f64;
    for c in (0..4).filter(|&c| c != side.col()) {
        let mut v: Vec<u32> = bodies.iter().map(|b| b.1[c]).collect();
        v.sort_unstable();
        let d = v.iter().enumerate().fold(0.0f64, |d, (i, &u)| {
            let u = u as f64 / 4_294_967_296.0;
            d.max(((i + 1) as f64 / x - u).abs()).max((u - i as f64 / x).abs())
        });
        let ratio = d / (KS_C / x.sqrt());
        if ratio > worst.0 {
            worst = (ratio, ["p", "e", "omega", "t_p"][c]);
        }
    }
    worst
}

/// The 2-D chi-square statistic against the uniform.
fn chi2(cells: &[u32], n: u64) -> f64 {
    let e = n as f64 / cells.len() as f64;
    cells.iter().map(|&c| (c as f64 - e) * (c as f64 - e) / e).sum()
}
/// The two-sample KS distance between two histograms of the same bins.
fn ks_hist(a: &[u32], b: &[u32], n: u64) -> f64 {
    let (mut ca, mut cb, mut d) = (0i64, 0i64, 0i64);
    for (x, y) in a.iter().zip(b) {
        ca += *x as i64;
        cb += *y as i64;
        d = d.max((ca - cb).abs());
    }
    d as f64 / n as f64
}
/// The two-sample KS distance between two sorted samples (ties handled).
fn ks_sorted(a: &[u64], b: &[u64]) -> f64 {
    let (mut d, mut i, mut j) = (0.0f64, 0usize, 0usize);
    while i < a.len() && j < b.len() {
        let x = a[i].min(b[j]);
        while i < a.len() && a[i] == x {
            i += 1;
        }
        while j < b.len() && b[j] == x {
            j += 1;
        }
        d = d.max((i as f64 / a.len() as f64 - j as f64 / b.len() as f64).abs());
    }
    d
}
/// ln of n! (Stirling with the 1/(12n) and 1/(360 n^3) terms; exact enough for n >= 10).
fn ln_factorial(n: f64) -> f64 {
    if n < 10.0 {
        return (2..=n as u64).map(|k| (k as f64).ln()).sum();
    }
    n * n.ln() - n + 0.5 * (2.0 * std::f64::consts::PI * n).ln() + 1.0 / (12.0 * n) - 1.0 / (360.0 * n * n * n)
}
/// The information in "which m of the n ordinals", per scarred body, in bits: log2 C(n, m) / m.
pub fn ordinal_bits(n: u64, m: u64) -> f64 {
    if m == 0 {
        return 0.0;
    }
    (ln_factorial(n as f64) - ln_factorial(m as f64) - ln_factorial((n - m) as f64)) / m as f64 / std::f64::consts::LN_2
}

/// One finding of a run.
struct Finding {
    pass: bool,
    text: String,
}
fn ok(findings: &mut Vec<Finding>, pass: bool, text: String) {
    findings.push(Finding { pass, text });
}

/// The worst numbers of a run, for the passing line.
#[derive(Default, Clone)]
struct Worst {
    chi: f64,
    serial: f64,
    ks: f64,
    tail_count: f64,
    tail_ks: f64,
    tail_mean: f64,
    tail_other: f64,
}
impl Worst {
    fn max(&mut self, o: &Worst) {
        self.chi = self.chi.max(o.chi);
        self.serial = self.serial.max(o.serial);
        self.ks = self.ks.max(o.ks);
        self.tail_count = self.tail_count.max(o.tail_count);
        self.tail_ks = self.tail_ks.max(o.tail_ks);
        self.tail_mean = self.tail_mean.max(o.tail_mean);
        self.tail_other = self.tail_other.max(o.tail_other);
    }
}

/// Which ordinals, in which order and on how many threads, a determinism pass visits.
#[derive(Clone, Copy, Debug)]
enum Order {
    Ascending,
    Descending,
    Scrambled,
    /// `threads` workers on contiguous chunks, each walking `down` or up.
    Chunks { threads: usize, down: bool },
    /// worker t takes ordinals t, t + threads, ...
    Interleaved { threads: usize },
}
/// Visits every ordinal of `belt` in the order and compares its hash with `truth`: how many differ.
fn pass_mismatches(belt: &dyn Belt, truth: &[u64], order: Order) -> u64 {
    let n = belt.len();
    let bad = |i: u64| (belt.body(i).hash() != truth[i as usize]) as u64;
    match order {
        Order::Ascending => (0..n).map(bad).sum(),
        Order::Descending => (0..n).rev().map(bad).sum(),
        Order::Scrambled => {
            let (k, c) = (0x9E37_79B9_7F4A_7C15u64 | 1, 0x1234_5678_9ABC_DEF1u64);
            (0..n).map(|j| bad(j.wrapping_mul(k).wrapping_add(c) & (n - 1))).sum()
        }
        Order::Chunks { threads, down } => std::thread::scope(|sc| {
            let chunk = n.div_ceil(threads as u64);
            let hs: Vec<_> = (0..threads as u64)
                .map(|t| {
                    let (lo, hi) = (t * chunk, ((t + 1) * chunk).min(n));
                    sc.spawn(move || if down { (lo..hi).rev().map(bad).sum::<u64>() } else { (lo..hi).map(bad).sum::<u64>() })
                })
                .collect();
            hs.into_iter().map(|h| h.join().unwrap()).sum()
        }),
        Order::Interleaved { threads } => std::thread::scope(|sc| {
            let hs: Vec<_> = (0..threads as u64).map(|t| sc.spawn(move || (t..n).step_by(threads).map(bad).sum::<u64>())).collect();
            hs.into_iter().map(|h| h.join().unwrap()).sum()
        }),
    }
}

/// The word of epoch `epoch`'s kick on ordinal `i`, or None if `i` is not kicked that epoch (probability [`CHURN`]).
fn kick_word(epoch: u32, i: u64) -> Option<u64> {
    let sel = mix64(mix64(CHURN_SEED.wrapping_add((epoch as u64).wrapping_mul(GAMMA))) ^ i);
    (sel < (CHURN * 18_446_744_073_709_551_616.0) as u64).then(|| mix64(sel ^ 0xD317A))
}
/// The replacement kick (relative to the program's body): 9, 11, 15 and 15 uniform bits on (p, e, omega, t_p), the
/// angle and the time wrapping, e not below zero (it never is: e below 2^-20 has probability 1e-10).
fn apply_kick(r: u64, base: &Body, spec: &BeltSpec) -> Body {
    let field = |shift: u32, bits: u32| ((r >> shift) & ((1u64 << bits) - 1)) as i64 - (1i64 << (bits - 1));
    let (dp, de, dw, dt) = (field(55, KICK_BITS[0]), field(44, KICK_BITS[1]), field(29, KICK_BITS[2]), field(14, KICK_BITS[3]));
    Body {
        p: (base.p as i64 + dp) as u64,
        e: (base.e as i64 + de).max(0) as u64,
        w: base.w.wrapping_add(dw as u64) & ((1u64 << spec.w_bits) - 1),
        t: base.t.wrapping_add(dt as u64) & ((1u64 << spec.t_bits) - 1),
    }
}

fn charge(b: &dyn Belt) -> u64 {
    b.bytes_used().max(b.store().len() as u64)
}

/// What a run measured for the report.
struct RunOut {
    n: u64,
    form: Form,
    birth_charge: u64,
    info: u64,
    ns_body: f64,
    scars: Option<(u64, f64, f64)>, // (distinct scarred, bytes per scarred body, floor bits)
    sample_total: Option<f64>,
    /// Per side: the sum of (-ln w - 1) over the tail and the number of its bodies, for pooling across runs.
    tail_mean: [(f64, usize); 4],
}

fn run_one(law: &dyn Law, r: &Run, findings: &mut Vec<Finding>, worst: &mut Worst) -> Option<RunOut> {
    let spec = SPEC;
    let n = 1u64 << r.log2n;
    let label = format!("2^{} seed {}", r.log2n, r.seed);
    let fail = |findings: &mut Vec<Finding>, what: &str| ok(findings, false, format!("{label}: {what}"));
    let Some(mut belt) = law.belt_birth(&spec, n, r.seed) else {
        fail(findings, "belt_birth is not implemented");
        return None;
    };
    let Some(pristine) = law.belt_birth(&spec, n, r.seed) else {
        fail(findings, "a second birth from the same (spec, n, seed) is not implemented");
        return None;
    };
    let form = belt.form();
    if belt.len() != n {
        fail(findings, &format!("len {} is not {n}", belt.len()));
        return None;
    }
    // ---- The iid reference of the same distribution and size.
    let k = (n as f64 * TAIL_FRACTION).ceil() as usize;
    let mut rng = Xoshiro::new(r.seed ^ 0x1D0F_AB1E);
    let mut ref_acc = Acc::new();
    let mut ref_tail: Vec<RefTail> = SIDES.iter().map(|_| RefTail::new(k)).collect();
    for _ in 0..n {
        let b = iid_body(&mut rng, &spec);
        let sc = quant(&ref_acc.push(&b, &spec));
        for (t, side) in ref_tail.iter_mut().zip(SIDES) {
            t.push((side.depth(&b, &spec), sc));
        }
    }
    let ref_top: Vec<Vec<Entry>> = ref_tail.into_iter().map(|t| t.into_sorted()).collect();
    // ---- The belt, one ascending pass: the truth hashes and every statistic.
    let mut acc = Acc::new();
    let mut tails: Vec<BeltTail> = ref_top.iter().map(|t| BeltTail::new(t[k - 1].0, 8 * k)).collect();
    let mut truth = Vec::with_capacity(n as usize);
    for i in 0..n {
        let b = belt.body(i);
        truth.push(b.hash());
        let sc = quant(&acc.push(&b, &spec));
        for (t, side) in tails.iter_mut().zip(SIDES) {
            t.push(side.depth(&b, &spec), &sc);
        }
    }
    // ---- (1) Determinism: every ordering reproduces the first pass, two births agree, the store round-trips.
    let mut w = Worst::default();
    let mut orders = vec![Order::Ascending, Order::Interleaved { threads: 7 }];
    if r.thorough {
        orders.extend([Order::Descending, Order::Scrambled, Order::Chunks { threads: 4, down: false }, Order::Chunks { threads: 8, down: true }]);
    }
    let mut bad_orders = Vec::new();
    let mut regen_ns = 0.0;
    for (j, o) in orders.into_iter().enumerate() {
        let t1 = Instant::now();
        let m = pass_mismatches(&*belt, &truth, o);
        if j == 0 {
            regen_ns = t1.elapsed().as_nanos() as f64 / n as f64;
        }
        if m > 0 {
            bad_orders.push(format!("{o:?} {m}"));
        }
    }
    ok(findings, bad_orders.is_empty(), format!("{label}: ordinals regenerate bit-identically in every order and thread count{}", if bad_orders.is_empty() { String::new() } else { format!(" (NOT: {})", bad_orders.join("; ")) }));
    let store0 = belt.store();
    let birth_charge = charge(&*belt);
    let twin = pristine.store();
    ok(findings, twin == store0, format!("{label}: two births from the same (spec, n, seed) store the same bytes"));
    let round = law.belt_restore(&store0);
    let round_ok = round.as_ref().is_some_and(|b| b.len() == n && b.store() == store0 && pass_mismatches(&**b, &truth, Order::Ascending) == 0);
    ok(findings, round_ok, format!("{label}: restore(store()) regenerates every ordinal and stores the same bytes"));
    drop(round);
    // ---- (2) Exact individuals.
    let mut sorted = truth;
    sorted.sort_unstable();
    let dups = sorted.windows(2).filter(|p| p[0] == p[1]).count();
    drop(sorted);
    ok(findings, dups == 0, format!("{label}: no two bodies share a state ({dups} repeats)"));
    ok(findings, acc.bad == 0, format!("{label}: every body inside the law's support ({} outside)", acc.bad));
    let dof = (SIDE * SIDE - 1) as f64;
    let zchi = |a: &Acc| (chi2(&a.cells, a.n) - dof) / (2.0 * dof).sqrt();
    let (z_belt, z_ref) = (zchi(&acc), zchi(&ref_acc));
    w.chi = z_belt.abs();
    ok(findings, z_belt.abs() <= Z_CHI, format!("{label}: (p, t_p) 2-D chi2 z = {z_belt:+.2} (iid reference {z_ref:+.2}; limit {Z_CHI})"));
    // Serial correlation: sum x_i x_{i-L} / (n - L) * 12 sqrt(n - L), since var x = 1/12 under the law.
    let mut ser = (0.0f64, String::new());
    for c in 0..4 {
        for (j, &l) in LAGS.iter().enumerate() {
            let z = acc.lag[c][j] * 12.0 / ((n - l as u64) as f64).sqrt();
            if z.abs() > ser.0 {
                ser = (z.abs(), format!("{} lag {l} z = {z:+.2}", ["p", "e", "omega", "t_p"][c]));
            }
        }
    }
    for (k2, &(a, b)) in PAIRS.iter().enumerate() {
        let z = acc.cross0[k2] * 12.0 / (n as f64).sqrt();
        if z.abs() > ser.0 {
            ser = (z.abs(), format!("{} x {} z = {z:+.2}", ["p", "e", "omega", "t_p"][a], ["p", "e", "omega", "t_p"][b]));
        }
    }
    let mut kx = 0;
    for a in 0..4 {
        for b in 0..4 {
            if a != b {
                let z = acc.cross1[kx] * 12.0 / ((n - 1) as f64).sqrt();
                if z.abs() > ser.0 {
                    ser = (z.abs(), format!("{} x previous {} z = {z:+.2}", ["p", "e", "omega", "t_p"][a], ["p", "e", "omega", "t_p"][b]));
                }
                kx += 1;
            }
        }
    }
    w.serial = ser.0;
    ok(findings, ser.0 <= Z_SERIAL, format!("{label}: serial and cross correlation, worst |z| = {:.2} ({}; limit {Z_SERIAL})", ser.0, ser.1));
    let crit = KS_C * (2.0 / n as f64).sqrt();
    let ks: Vec<f64> = (0..4).map(|c| ks_hist(&acc.hist[c], &ref_acc.hist[c], n)).collect();
    w.ks = ks.iter().fold(0.0f64, |m, d| m.max(d / crit));
    ok(findings, ks.iter().all(|&d| d <= crit), format!("{label}: per-column KS D = p {:.4} e {:.4} omega {:.4} t_p {:.4} (critical {crit:.4})", ks[0], ks[1], ks[2], ks[3]));
    // The reference through the same tests: the judge's own control.
    let ref_ser = (0..4).flat_map(|c| LAGS.iter().enumerate().map(move |(j, &l)| (c, j, l))).map(|(c, j, l)| (ref_acc.lag[c][j] * 12.0 / ((n - l as u64) as f64).sqrt()).abs()).fold(0.0f64, f64::max);
    let ref_ks = (0..4).map(|c| ks_hist(&ref_acc.hist[c], &acc.hist[c], n)).fold(0.0f64, f64::max);
    // ... and the reference's own tails through the conditional tests (its k - 1 deepest, given its k-th as the threshold).
    let (mut ref_mean, mut ref_other) = (0.0f64, 0.0f64);
    for (si, side) in SIDES.iter().enumerate() {
        let (thr, above) = (ref_top[si][k - 1].0, &ref_top[si][..k - 1]);
        ref_mean = ref_mean.max(log_z(conditional_log_sum(*side, thr, above, &spec), above.len()).abs());
        ref_other = ref_other.max(other_columns_ks(*side, above).0);
    }
    ok(
        findings,
        z_ref.abs() <= Z_CHI && ref_ser <= Z_SERIAL && ref_ks <= crit && ref_mean <= Z_TAIL && ref_other <= 1.0,
        format!("{label}: the judge's iid reference passes its own tests (chi2 z {z_ref:+.2}, serial {ref_ser:.2}, KS {ref_ks:.4}, tail mean {ref_mean:.2}, tail other-columns {ref_other:.2} of critical)"),
    );
    // ---- (3) Tails: the top and the bottom 1e-4 of p and of e.
    let mut tail_mean = [(0.0, 0usize); 4];
    for (si, side) in SIDES.iter().enumerate() {
        let (top, name) = (&ref_top[si], side.name());
        let (thr, big_k) = (top[k - 1].0, k as f64);
        let t = &mut tails[si];
        let x = t.count as f64;
        let z = (x - big_k) / (2.0 * big_k).sqrt();
        let mut belt_top: Vec<u64> = t.top.drain().map(|r| r.0).collect();
        belt_top.sort_unstable_by(|a, b| b.cmp(a));
        let (belt_max, belt_20th) = (belt_top[0], *belt_top.last().unwrap());
        let reach = belt_max >= top[REACH_J - 1].0;
        let over = belt_20th <= top[0].0;
        ok(findings, z.abs() <= Z_TAIL, format!("{label}: {name}: count {x} against the reference's {k} (z = {z:+.2}, limit {Z_TAIL})"));
        ok(findings, reach, format!("{label}: {name} reaches the reference's 20th deepest: belt deepest {belt_max}, reference {}", top[REACH_J - 1].0));
        ok(findings, over, format!("{label}: {name} does not overshoot the reference's deepest: belt 20th {belt_20th}, reference deepest {}", top[0].0));
        w.tail_count = w.tail_count.max(z.abs());
        let bodies = std::mem::take(&mut t.values);
        let mut mine: Vec<u64> = bodies.iter().map(|b| b.0).collect();
        mine.sort_unstable();
        let theirs: Vec<u64> = top.iter().rev().map(|b| b.0).collect();
        let (xx, d) = (mine.len(), if mine.is_empty() { f64::INFINITY } else { ks_sorted(&mine, &theirs) });
        let dcrit = KS_C * ((xx + k) as f64 / (xx.max(1) * k) as f64).sqrt();
        w.tail_ks = w.tail_ks.max(d / dcrit);
        ok(findings, xx >= 8 && d <= dcrit, format!("{label}: tail shape of {name}: KS D = {d:.3} against {dcrit:.3} ({xx} values; thr {thr})"));
        // The conditional tests: the tail against the law itself (no reference noise), by its mean and by its neighbours.
        let sum = conditional_log_sum(*side, thr, &bodies, &spec);
        let zm = log_z(sum, bodies.len());
        w.tail_mean = w.tail_mean.max(zm.abs());
        tail_mean[si] = (sum, bodies.len());
        ok(findings, zm.abs() <= Z_TAIL, format!("{label}: {name}: conditional log-score mean z = {zm:+.2} over {xx} bodies (limit {Z_TAIL})"));
        let (ratio, col) = other_columns_ks(*side, &bodies);
        w.tail_other = w.tail_other.max(ratio);
        ok(findings, ratio <= 1.0, format!("{label}: {name}: its bodies' other columns stay uniform: worst KS {ratio:.2} of critical ({col})"));
    }
    worst.max(&w);
    // ---- (4) Bytes at birth.
    let info = match form {
        Form::Program { info_bytes } => info_bytes,
        Form::Sample => 0,
    };
    let mut sample_total = None;
    match form {
        Form::Program { info_bytes } => {
            let limit = limit_bytes(info_bytes as f64);
            ok(findings, info_bytes <= INFO_CAP, format!("{label}: declared information {info_bytes} B is within {INFO_CAP} B (a program's information is its parameters; a table derived from them is not information)"));
            ok(findings, birth_charge as f64 <= limit && birth_charge >= info_bytes, format!("{label}: bytes at birth {birth_charge} within 2 x info {info_bytes} + 2 = {limit:.0} and not below the info"));
        }
        Form::Sample => {
            let floor = iid_floor_bits(&spec) / 8.0;
            let per = birth_charge as f64 / n as f64;
            sample_total = Some(per);
            ok(findings, per <= limit_bytes(floor) && per >= 0.5 * floor, format!("{label}: sample bytes per body {per:.2} in [{:.2}, {:.2}] (iid floor {floor:.2})", 0.5 * floor, limit_bytes(floor)));
        }
    }
    // ---- (4) The churn ladder: 12 epochs at 1e-2, replacement kicks relative to the program.
    let mut scarred: BTreeMap<u64, Body> = BTreeMap::new();
    for epoch in 1..=EPOCHS {
        for i in 0..n {
            if let Some(r) = kick_word(epoch, i) {
                let nb = apply_kick(r, &pristine.body(i), &spec);
                belt.scar(i, nb);
                scarred.insert(i, nb);
            }
        }
    }
    let m = scarred.len() as u64;
    let mut wrong = 0u64;
    let mut it = scarred.iter().peekable();
    for i in 0..n {
        let want = match it.peek() {
            Some((&j, _)) if j == i => *it.next().unwrap().1,
            _ => pristine.body(i),
        };
        wrong += (belt.body(i) != want) as u64;
    }
    ok(findings, wrong == 0, format!("{label}: after {EPOCHS} epochs every scarred ordinal returns its scar and every other its program ({wrong} wrong of {n})"));
    let after = belt.store();
    let after_charge = charge(&*belt);
    let round = law.belt_restore(&after);
    let round_ok = round.as_ref().is_some_and(|b| b.len() == n && b.store() == after && (0..n).all(|i| b.body(i) == belt.body(i)));
    ok(findings, round_ok, format!("{label}: the churned belt restores exactly"));
    let mut scars_out = None;
    let floor_bits = ordinal_bits(n, m) + KICK_BITS.iter().sum::<u32>() as f64;
    match form {
        Form::Program { .. } => {
            let per = after_charge.saturating_sub(birth_charge) as f64 / m as f64;
            let (lo, hi) = (0.5 * floor_bits / 8.0, limit_bytes(floor_bits / 8.0));
            scars_out = Some((m, per, floor_bits));
            ok(findings, per >= lo && per <= hi, format!("{label}: {m} scarred bodies cost {per:.2} bytes each, within [{lo:.2}, {hi:.2}] (floor {floor_bits:.1} bits = {:.2} B)", floor_bits / 8.0));
        }
        Form::Sample => {
            let floor = iid_floor_bits(&spec) / 8.0;
            let per = after_charge as f64 / n as f64;
            sample_total = Some(per);
            ok(findings, per <= limit_bytes(floor) && per >= 0.5 * floor, format!("{label}: sample bytes per body after churn {per:.2} in [{:.2}, {:.2}]", 0.5 * floor, limit_bytes(floor)));
        }
    }
    Some(RunOut { n, form, birth_charge, info, ns_body: regen_ns, scars: scars_out, sample_total, tail_mean })
}

/// B18 belt over `runs` (the CLI runs [`RUNS`]; tests run fewer). Stops after the first run with a failing finding.
pub fn judge(law: &dyn Law, runs: &[Run]) -> Gate {
    judge_findings(law, runs).0
}

/// [`judge`], and every finding it made, passing or failing, as (pass, text): the evidence behind the verdict.
pub fn judge_findings(law: &dyn Law, runs: &[Run]) -> (Gate, Vec<(bool, String)>) {
    let t0 = Instant::now();
    let (mut findings, mut worst, mut outs) = (Vec::new(), Worst::default(), Vec::new());
    for r in runs {
        let before = findings.len();
        let out = run_one(law, r, &mut findings, &mut worst);
        let bad = findings[before..].iter().any(|f| !f.pass);
        outs.extend(out);
        if bad {
            break;
        }
    }
    // Neither the program's information nor its bytes grow with n.
    if let (Some(small), Some(big)) = (outs.iter().filter(|o| matches!(o.form, Form::Program { .. })).min_by_key(|o| o.n), outs.iter().filter(|o| matches!(o.form, Form::Program { .. })).max_by_key(|o| o.n)) {
        if big.n > small.n {
            let grew = big.birth_charge.saturating_sub(small.birth_charge);
            ok(&mut findings, grew <= 16 && big.info <= small.info + 8, format!("the store does not grow with n: {} B at 2^{}, {} B at 2^{} (info {} and {})", small.birth_charge, small.n.trailing_zeros(), big.birth_charge, big.n.trailing_zeros(), small.info, big.info));
        }
    }
    // The conditional tail log-score means, pooled over the runs: a spread crush of 15% is 1.6 sigma in a run of 2^20 and 4.4 in 2^23
    // (the exponential mean's best possible 0.15 sqrt(X)); the pooled tails of the five runs give about 6.7.
    let mut pooled = 0.0f64;
    if outs.len() > 1 && findings.iter().all(|f| f.pass) {
        for (si, side) in SIDES.iter().enumerate() {
            let z = log_z(outs.iter().map(|o| o.tail_mean[si].0).sum(), outs.iter().map(|o| o.tail_mean[si].1).sum());
            pooled = pooled.max(z.abs());
            ok(&mut findings, z.abs() <= Z_TAIL, format!("{}: conditional log-score mean pooled over {} runs: z = {z:+.2} (limit {Z_TAIL})", side.name(), outs.len()));
        }
    }
    let failed: Vec<&Finding> = findings.iter().filter(|f| !f.pass).collect();
    let pass = failed.is_empty() && !outs.is_empty();
    let secs_run = t0.elapsed().as_secs_f64();
    let detail = if pass {
        let o = outs.last().unwrap();
        let report = match o.form {
            Form::Program { .. } => {
                let (m, per, floor) = o.scars.unwrap();
                let frac = m as f64 / o.n as f64;
                let at_billion = law.belt_birth(&SPEC, BILLION, runs.first().map_or(0, |r| r.seed)).map(|b| b.store().len());
                match at_billion {
                    Some(len) => format!("bytes at 1e9: {len} B ({:.1e} B/body); after {EPOCHS} epochs at 1e-2 {:.1}% are scarred, {per:.1} B each (floor {floor:.0} bits): {:.2} GB at 1e9 (reported)", len as f64 / 1e9, 100.0 * frac, frac * per * 1e9 / 1e9),
                    None => "bytes at 1e9: could not birth 1e9 (reported)".to_string(),
                }
            }
            Form::Sample => format!("sample form: {:.2} B per body, {:.1} GB at 1e9 (extrapolated, reported)", o.sample_total.unwrap_or(0.0), o.sample_total.unwrap_or(0.0)),
        };
        format!(
            "belt: {} runs, every criterion; worst: chi2 |z| {:.2} (limit {Z_CHI}), serial |z| {:.2} ({Z_SERIAL}), KS {:.2} of critical; four tail ends: count |z| {:.2} ({Z_TAIL}), shape KS {:.2} of critical, conditional mean |z| {:.2} (pooled {pooled:.2}), other columns {:.2} of critical; birth {} B for info {} B; {:.0} ns to regenerate and hash a body; {report}",
            outs.len(),
            worst.chi,
            worst.serial,
            worst.ks,
            worst.tail_count,
            worst.tail_ks,
            worst.tail_mean,
            worst.tail_other,
            outs.last().unwrap().birth_charge,
            outs.last().unwrap().info,
            outs.last().unwrap().ns_body
        )
        .replace(&format!("; birth {} B for info 0 B", outs.last().unwrap().birth_charge), &format!("; birth {} B (a stored sample)", outs.last().unwrap().birth_charge))
    } else if outs.is_empty() && failed.is_empty() {
        "belt: no run".to_string()
    } else {
        format!("belt: {} of {} findings fail: {}", failed.len(), findings.len(), failed.iter().map(|f| f.text.as_str()).collect::<Vec<_>>().join("; "))
    };
    (Gate { id: "B18b", pass, detail, secs: secs_run }, findings.into_iter().map(|f| (f.pass, f.text)).collect())
}

/// The CLI's gate: the frozen runs.
pub fn b18_belt(law: &dyn Law) -> Gate {
    judge(law, &RUNS)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ln_det_is_the_logarithm_to_a_few_ulps_across_the_range_the_belt_uses() {
        for k in 0..=2000 {
            let v = 2f64.powf(-53.0 * k as f64 / 2000.0) * (0.5 + k as f64 / 4001.0);
            if v < 1.0 && v > 0.0 {
                assert!((ln_det(v) - v.ln()).abs() <= 4e-16 * v.ln().abs().max(1.0), "{v}");
            }
        }
    }

    #[test]
    fn the_iid_floor_is_the_draw_entropy_of_the_belt() {
        // p 27 + omega 32 + t_p 44 + e: 30 - 2.477 (the Rayleigh sigma 0.07 on a 2^-30 grid) = 130.52 bits.
        assert!((iid_floor_bits(&SPEC) - 130.523).abs() < 0.01, "{}", iid_floor_bits(&SPEC));
    }

    #[test]
    fn the_ordinal_information_of_a_churn_is_log_binomial_per_scar() {
        // C(2^20, 0.1 n) per scar: H2(0.1)/0.1 = 4.69 bits; at 1% it is H2(0.01)/0.01 = 8.08.
        assert!((ordinal_bits(1 << 20, (1 << 20) / 10) - 4.69).abs() < 0.01);
        assert!((ordinal_bits(1 << 23, (1 << 23) / 100) - 8.08).abs() < 0.02);
    }

    #[test]
    fn varints_and_zigzag_round_trip() {
        for v in [0u64, 1, 127, 128, 300, u64::MAX / 3, u64::MAX] {
            let mut b = Vec::new();
            put_varint(&mut b, v);
            assert_eq!(get_varint(&b, &mut 0), Some(v));
        }
        for d in [0i64, 1, -1, 12345, -12345, i64::MIN, i64::MAX] {
            assert_eq!(unzigzag(zigzag(d as u64)), d as u64);
        }
    }

    #[test]
    fn the_reference_regenerates_and_round_trips_with_scars() {
        let mut belt = ProgramBelt::birth(&SPEC, 4096, 7, Flaw::None);
        let before: Vec<Body> = (0..4096).map(|i| belt.body(i)).collect();
        let b = Body { p: before[5].p + 3, e: before[5].e + 2, w: 0, t: before[5].t.wrapping_sub(9) & ((1 << 44) - 1) };
        belt.scar(5, b);
        belt.scar(4000, Body { p: SPEC.p_lo, e: 0, w: 1, t: 2 });
        let back = ProgramBelt::restore(&belt.store()).unwrap();
        assert_eq!(back.store(), belt.store());
        assert_eq!(back.body(5), b);
        assert_eq!((0..4096).filter(|&i| back.body(i) != belt.body(i)).count(), 0);
        assert_eq!((0..4096).filter(|&i| belt.body(i) != before[i as usize]).count(), 2);
        assert!(ProgramBelt::restore(&belt.store()[..40]).is_none());
        let mut s = SampleBelt::birth(&SPEC, 1000, 3, false);
        let s0: Vec<Body> = (0..1000).map(|i| s.body(i)).collect();
        s.scar(17, Body { p: SPEC.p_lo + 5, e: 6, w: 7, t: 8 });
        let sb = SampleBelt::restore(&s.store()).unwrap();
        assert_eq!(sb.store(), s.store());
        assert_eq!((0..1000).filter(|&i| sb.body(i) != s.body(i)).count(), 0);
        assert_eq!((0..1000).filter(|&i| s.body(i) != s0[i as usize]).count(), 1);
    }

    /// Calibration (not a gate): the tail-count z of one iid sample against another has mean 0 and standard deviation 1.
    /// Run with `cargo test --release -p xtask calibrate -- --ignored --nocapture`.
    #[test]
    #[ignore]
    fn calibrate_the_tail_count_z_under_iid() {
        for log2n in [18u32, 20] {
            let n = 1usize << log2n;
            let k = (n as f64 * TAIL_FRACTION).ceil() as usize;
            let mut zs = Vec::new();
            for rep in 0..120u64 {
                let draw = |seed: u64| {
                    let mut r = Xoshiro::new(seed);
                    (0..n).map(|_| iid_body(&mut r, &SPEC).e).collect::<Vec<u64>>()
                };
                let (a, b) = (draw(1000 + 2 * rep), draw(1001 + 2 * rep));
                let mut sa = a.clone();
                sa.sort_unstable_by(|x, y| y.cmp(x));
                let thr = sa[k - 1];
                let x = b.iter().filter(|&&v| v >= thr).count() as f64;
                zs.push((x - k as f64) / (2.0 * k as f64).sqrt());
            }
            let mean = zs.iter().sum::<f64>() / zs.len() as f64;
            let sd = (zs.iter().map(|z| (z - mean) * (z - mean)).sum::<f64>() / zs.len() as f64).sqrt();
            println!("n = 2^{log2n}, k = {k}: tail count z over {} pairs: mean {mean:+.3}, sd {sd:.3}, max |z| {:.2}", zs.len(), zs.iter().fold(0.0f64, |m, z| m.max(z.abs())));
            assert!((0.8..1.25).contains(&sd) && mean.abs() < 0.4, "sd {sd} mean {mean}");
        }
    }

    /// Not a gate: every finding of the controls, to read the margins (`--ignored --nocapture`).
    #[test]
    #[ignore]
    fn show_the_evidence_of_the_frozen_runs_on_the_controls() {
        for (name, law) in [("echo", &crate::behave::laws::Echo as &dyn Law), ("dyadic", &crate::behave::laws::DyadicBelt), ("iid-blocks", &crate::behave::laws::IidBlocks)] {
            let (g, findings) = judge_findings(law, &RUNS);
            println!("=== {name}: {} [{:.1} s]", if g.pass { "PASS" } else { "FAIL" }, g.secs);
            for (pass, text) in findings {
                println!("  {} {text}", if pass { "ok  " } else { "FAIL" });
            }
        }
    }

    /// Calibration (not a gate): the reference belt passes the gate from many seeds (the false-failure rate is near 0).
    #[test]
    #[ignore]
    fn calibrate_the_reference_passes_from_many_seeds() {
        struct Law0;
        impl Law for Law0 {
            fn advance_per_cycle(&self, _: f64, _: f64) -> Option<(f64, f64, f64)> {
                None
            }
            fn deflection(&self, _: f64) -> Option<f64> {
                None
            }
            fn captured(&self, _: f64, _: f64) -> bool {
                false
            }
            fn photon_captured(&self, _: f64) -> bool {
                false
            }
            fn long_run(&self, _: f64, _: f64, _: usize) -> Vec<(f64, f64, f64, f64)> {
                Vec::new()
            }
            fn belt_birth(&self, spec: &BeltSpec, n: u64, seed: u64) -> Option<Box<dyn Belt>> {
                Some(Box::new(ProgramBelt::birth(spec, n, seed, Flaw::None)))
            }
            fn belt_restore(&self, store: &[u8]) -> Option<Box<dyn Belt>> {
                ProgramBelt::restore(store).map(|b| Box::new(b) as Box<dyn Belt>)
            }
        }
        let mut fails = 0;
        for seed in 1..=60u64 {
            let g = judge(&Law0, &[Run { log2n: 20, seed: 777_000 + seed, thorough: false }]);
            if !g.pass {
                fails += 1;
                println!("seed {seed}: {}", g.detail);
            }
        }
        println!("{fails} of 60 seeds failed");
        assert_eq!(fails, 0);
    }

    /// Calibration (not a gate): the conditional log-score z of each tail end is standard normal for an iid belt (here the
    /// reference program against the judge's xoshiro thresholds, over many seeds at 2^20).
    #[test]
    #[ignore]
    fn calibrate_the_conditional_tail_z_under_iid() {
        let (n, k) = (1u64 << 20, 105usize);
        let mut zs: Vec<Vec<f64>> = vec![Vec::new(); 4];
        for seed in 0..80u64 {
            let mut rng = Xoshiro::new(900 + seed);
            let mut refs: Vec<RefTail> = SIDES.iter().map(|_| RefTail::new(k)).collect();
            for _ in 0..n {
                let b = iid_body(&mut rng, &SPEC);
                for (t, side) in refs.iter_mut().zip(SIDES) {
                    t.push((side.depth(&b, &SPEC), [0; 4]));
                }
            }
            let tops: Vec<Vec<Entry>> = refs.into_iter().map(|t| t.into_sorted()).collect();
            let belt = ProgramBelt::birth(&SPEC, n, 5000 + seed, Flaw::None);
            let mut bodies: Vec<Vec<Entry>> = vec![Vec::new(); 4];
            for i in 0..n {
                let b = belt.body(i);
                for (si, side) in SIDES.iter().enumerate() {
                    let d = side.depth(&b, &SPEC);
                    if d >= tops[si][k - 1].0 {
                        bodies[si].push((d, [0; 4]));
                    }
                }
            }
            for (si, side) in SIDES.iter().enumerate() {
                zs[si].push(log_z(conditional_log_sum(*side, tops[si][k - 1].0, &bodies[si], &SPEC), bodies[si].len()));
            }
        }
        for (si, side) in SIDES.iter().enumerate() {
            let m = zs[si].iter().sum::<f64>() / 80.0;
            let sd = (zs[si].iter().map(|z| (z - m) * (z - m)).sum::<f64>() / 80.0).sqrt();
            println!("{}: conditional log-score z over 80 seeds: mean {m:+.3}, sd {sd:.3}, max |z| {:.2}", side.name(), zs[si].iter().fold(0.0f64, |a, z| a.max(z.abs())));
        }
    }

    /// Not a gate: the crush plant's top-e conditional z in each frozen run on its own, and pooled (`--ignored --nocapture`).
    #[test]
    #[ignore]
    fn show_the_crush_in_each_run_and_pooled() {
        let law = crate::behave::laws::Planted(crate::behave::laws::Fault::BeltCrush);
        let (mut sum, mut x) = (0.0, 0usize);
        for r in RUNS {
            let (_, f) = judge_findings(&law, &[r]);
            let line = f.iter().find(|(_, t)| t.contains("top 1e-4 of e: conditional")).unwrap().1.clone();
            println!("{line}");
            let z: f64 = line.split("z = ").nth(1).unwrap().split(' ').next().unwrap().parse().unwrap();
            let xx: usize = line.split("over ").nth(1).unwrap().split(' ').next().unwrap().parse().unwrap();
            sum += z * (xx as f64).sqrt();
            x += xx;
        }
        println!("pooled z = {:+.2} over {x} bodies", sum / (x as f64).sqrt());
    }
}
