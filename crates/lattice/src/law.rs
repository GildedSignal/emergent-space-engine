//! `es-lattice-elastic-v0`: the law every execution mode implements bit for bit.
//!
//! State lives on integer lattices: positions in 1/Q units, velocities in 1/Q units per
//! chronon, time in chronons. A chronon t is the bin (t-1, t]. Per chronon, in this order:
//!
//! 1. **Detect** with positions at t-1 and the velocities valid during the bin: a pair hits
//!    when it is approaching and comes within reach (sum of radii) somewhere in the bin
//!    ([`hit`]). A pair whose contact was consumed at both bodies' current revisions does
//!    not hit again until one of them revises.
//! 2. **Advance** every position by its velocity (exact: x + k).
//! 3. **Walls**: a bouncer at or beyond a wall (container inset by its radius) while moving
//!    outward is in the wall set.
//! 4. **Respond** ([`resolve`]): bouncer pairs in canonical id order, sequential impulses
//!    (each pair starts from the velocities earlier pairs left), momentum rounded to the
//!    lcm(m_a, m_b)/Q lattice, choosing the floor/ceil candidate that minimises
//!    |owed + e| where owed is the pair's energy carry, never rounding a nonzero exchange
//!    to zero; the pair's rounding error joins the lower id's carry. Stop bodies in any
//!    pair stop. Wall bodies flip each outward component that is still outward, and the
//!    wall momentum ledger records it. A body revises (rev + 1) iff its velocity changed.
//!    Every hit pair is then consumed at the new revisions.
//!
//! Locality: the response is local to connected components of the batch. The pair
//! errors telescope, so the whole-batch remainder the H0159 engine assigns is identically
//! zero, and resolving components separately gives the same bits as resolving the whole
//! batch (tested). That is the licence for regions, cores and the GPU.
//!
//! Speed limit c = 1: |k|² ≤ Q² for every body at genesis and at every intervention.
//! Elastic exchanges can push a rare body past it (the Maxwell tail), so neighbourhood
//! bounds must come from the tracked current max |k_c|, never from c alone: a pair can
//! only hit in bin t if each component of its separation at t-1 is at most
//! reach + |w_c| ≤ reach + 2·max|k_c|.
//!
//! Exactness ranges ([`World::validate`]): Q ≤ 2^20, |x_c| ≤ 2^39, |k_c| ≤ 2^22 (4c at the
//! largest Q), radius in [1, 2^30], mass in [1, 2^16]. Inside them every predicate and
//! response below is exact in i128 for any pair, near or far (worst products: cross²,
//! dd·ww and dw² ≤ 2^126). Implementations with narrower words (the GPU's 64-bit
//! integers) must check their own tighter preconditions and hand anything outside them
//! back to an exact path; they may never round.
use serde::{Deserialize, Serialize};

pub type Tick = i64;

pub const MAX_Q: i64 = 1 << 20;
pub const MAX_COORD: i64 = 1 << 39;
pub const MAX_RADIUS: i64 = 1 << 30;
pub const MAX_MASS: i64 = 1 << 16;
/// Evolved velocities may exceed c (see [`World::check_speed_limit`]) but stay exact below this.
pub const MAX_SPEED: i64 = 1 << 22;

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub enum Response {
    /// Contacts are recorded; velocity never changes; walls are ignored.
    Pass,
    /// Elastic impulses with other bouncers; reflects off walls.
    Bounce,
    /// Stops (k = 0) at its first contact with anything; walls are ignored.
    Stop,
}

/// Which bounce a world obeys. Positions, predicates, walls and cells are shared.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum Law {
    /// `es-lattice-elastic-v0`: Newtonian impulses; evolved speeds may exceed c.
    #[default]
    Newtonian,
    /// `es-lattice-relativistic-v0` ([`crate::relativity`]): 4-momentum exact up to a bounded
    /// carry, and |k|² < Q² for every body at every tick.
    Relativistic,
    /// `es-lattice-relativistic-v1` ([`crate::relativity`]): v0's reflection with the energy
    /// quantum matched to the velocity quantum (scale 2Q, floors after the products), so the
    /// ledgers see kinetic energy at every speed and reduce exactly to the Newtonian ones.
    RelativisticV1,
}

impl Law {
    /// Every relativistic version keeps |k|² < Q² for every body at every tick.
    pub fn subluminal(self) -> bool {
        matches!(self, Law::Relativistic | Law::RelativisticV1)
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Body {
    pub id: u64,
    /// Position at the world's tick, in 1/Q units.
    pub x: [i64; 2],
    /// Velocity in 1/Q units per chronon.
    pub k: [i64; 2],
    pub mass: i64,
    /// Radius in 1/Q units.
    pub radius: i64,
    pub response: Response,
    /// Energy carry: m·|k|² units (2Q² × kinetic energy) under the Newtonian law; fixed-point
    /// 4-momentum units under the relativistic law.
    pub residual: i64,
    pub rev: u32,
    /// Momentum carry (relativistic law, fixed-point 4-momentum units); zero under Newtonian.
    #[serde(default)]
    pub carry: [i64; 2],
}

impl Body {
    pub fn new(id: u64, x: [i64; 2], k: [i64; 2], mass: i64, radius: i64, response: Response) -> Body {
        Body { id, x, k, mass, radius, response, residual: 0, rev: 0, carry: [0, 0] }
    }

    pub fn energy(&self) -> i128 {
        energy(self.mass as i128, [self.k[0] as i128, self.k[1] as i128])
    }
}

/// Axis-aligned box in 1/Q units; a body's centre is confined to [min + r, max - r].
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Container {
    pub min: [i64; 2],
    pub max: [i64; 2],
}

impl Container {
    pub fn inset(&self, radius: i64) -> ([i64; 2], [i64; 2]) {
        ([self.min[0] + radius, self.min[1] + radius], [self.max[0] - radius, self.max[1] - radius])
    }
}

/// The contact of pair (a, b), ids a < b, consumed at these revisions.
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub struct Consumed {
    pub a: u64,
    pub b: u64,
    pub rev_a: u32,
    pub rev_b: u32,
}

/// Complete canonical state at `tick`. Everything the future depends on is here.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct World {
    pub q: i64,
    pub tick: Tick,
    pub container: Option<Container>,
    /// Strictly increasing ids.
    pub bodies: Vec<Body>,
    /// Live consumed contacts (see [`World::canonical`]).
    pub consumed: Vec<Consumed>,
    /// Momentum given to the walls: mass·(1/Q units per chronon) under the Newtonian law,
    /// fixed-point 4-momentum units under the relativistic law.
    pub wall_momentum: [i64; 2],
    #[serde(default)]
    pub law: Law,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LawError(pub String);

impl std::fmt::Display for LawError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&self.0)
    }
}
impl std::error::Error for LawError {}

fn err<T>(s: String) -> Result<T, LawError> {
    Err(LawError(s))
}

impl World {
    /// A genesis world: exactness ranges and the speed limit c = 1.
    pub fn new(q: i64, container: Option<Container>, bodies: Vec<Body>) -> Result<Self, LawError> {
        let w = World { q, tick: 0, container, bodies, consumed: vec![], wall_momentum: [0, 0], law: Law::Newtonian };
        w.validate()?;
        w.check_speed_limit()?;
        Ok(w)
    }

    /// The same genesis under another law (the relativistic law needs |k| < c strictly).
    pub fn with_law(mut self, law: Law) -> Result<Self, LawError> {
        self.law = law;
        self.validate()?;
        self.check_speed_limit()?;
        Ok(self)
    }

    /// c = 1 (|k|² ≤ Q²): checked at genesis and interventions, not on evolved states.
    /// Open law question (25 September 2026): elastic exchanges with unequal masses can
    /// push a light body past c; a relativistic response would forbid it.
    pub fn check_speed_limit(&self) -> Result<(), LawError> {
        let q2 = self.q as i128 * self.q as i128;
        for b in &self.bodies {
            let kk = b.k[0] as i128 * b.k[0] as i128 + b.k[1] as i128 * b.k[1] as i128;
            let over = if self.law.subluminal() { kk >= q2 } else { kk > q2 };
            if over {
                return err(format!("body {} at or beyond light: |k|² = {kk}, Q² = {q2}", b.id));
            }
        }
        Ok(())
    }

    /// Exactness ranges (any state, evolved or genesis).
    pub fn validate(&self) -> Result<(), LawError> {
        if self.q < 1 || self.q > MAX_Q {
            return err(format!("quantum {} outside [1, 2^20]", self.q));
        }
        for (i, b) in self.bodies.iter().enumerate() {
            if i > 0 && self.bodies[i - 1].id >= b.id {
                return err(format!("ids not strictly increasing at body {}", b.id));
            }
            if b.x.iter().any(|c| c.abs() > MAX_COORD) {
                return err(format!("body {} position outside 2^39", b.id));
            }
            if b.radius < 1 || b.radius > MAX_RADIUS {
                return err(format!("body {} radius {} outside [1, 2^30]", b.id, b.radius));
            }
            if b.mass < 1 || b.mass > MAX_MASS {
                return err(format!("body {} mass {} outside [1, 2^16]", b.id, b.mass));
            }
            if b.k.iter().any(|c| c.abs() > MAX_SPEED) {
                return err(format!("body {} velocity outside 2^22", b.id));
            }
            let kk = b.k[0] as i128 * b.k[0] as i128 + b.k[1] as i128 * b.k[1] as i128;
            if self.law.subluminal() && kk >= self.q as i128 * self.q as i128 {
                return err(format!("body {} at or beyond light under the relativistic law", b.id));
            }
        }
        if let Some(c) = &self.container {
            if c.min[0] >= c.max[0] || c.min[1] >= c.max[1] {
                return err("empty container".into());
            }
        }
        Ok(())
    }

    pub fn index_of(&self, id: u64) -> Option<usize> {
        self.bodies.binary_search_by_key(&id, |b| b.id).ok()
    }

    /// Drop consumed entries that can no longer matter: a revision changed, or the pair is
    /// not approaching (with constant relative velocity it never will again). Sorted.
    pub fn canonical(mut self) -> Self {
        let keep: Vec<Consumed> = self
            .consumed
            .iter()
            .copied()
            .filter(|c| {
                let (Some(i), Some(j)) = (self.index_of(c.a), self.index_of(c.b)) else { return false };
                let (a, b) = (&self.bodies[i], &self.bodies[j]);
                a.rev == c.rev_a && b.rev == c.rev_b && dot(sub(b.x, a.x), sub(b.k, a.k)) < 0
            })
            .collect();
        self.consumed = keep;
        self.consumed.sort_unstable();
        self.consumed.dedup();
        self
    }

    pub fn max_radius(&self) -> i64 {
        self.bodies.iter().map(|b| b.radius).max().unwrap_or(1)
    }

    /// Σ m·|k|² (2Q² × kinetic energy).
    pub fn energy(&self) -> i128 {
        self.bodies.iter().map(Body::energy).sum()
    }

    pub fn residual(&self) -> i128 {
        self.bodies.iter().map(|b| b.residual as i128).sum()
    }

    /// Σ m·k (mass × 1/Q units per chronon).
    pub fn momentum(&self) -> [i128; 2] {
        self.bodies.iter().fold([0, 0], |p, b| {
            [p[0] + b.mass as i128 * b.k[0] as i128, p[1] + b.mass as i128 * b.k[1] as i128]
        })
    }

    /// Stable byte encoding of the canonical state (for digests).
    pub fn canonical_bytes(&self) -> Vec<u8> {
        let w = self.clone().canonical();
        let mut out = Vec::with_capacity(64 + w.bodies.len() * 64);
        let mut put = |v: i128| out.extend_from_slice(&v.to_le_bytes());
        put(w.q as i128);
        put(w.tick as i128);
        put(w.law as i128);
        match &w.container {
            Some(c) => {
                put(1);
                for v in [c.min[0], c.min[1], c.max[0], c.max[1]] {
                    put(v as i128);
                }
            }
            None => put(0),
        }
        put(w.bodies.len() as i128);
        for b in &w.bodies {
            for v in [b.id as i128, b.x[0] as i128, b.x[1] as i128, b.k[0] as i128, b.k[1] as i128, b.mass as i128, b.radius as i128] {
                put(v);
            }
            put(b.response as i128);
            put(b.residual as i128);
            put(b.rev as i128);
            put(b.carry[0] as i128);
            put(b.carry[1] as i128);
        }
        put(w.consumed.len() as i128);
        for c in &w.consumed {
            for v in [c.a as i128, c.b as i128, c.rev_a as i128, c.rev_b as i128] {
                put(v);
            }
        }
        put(w.wall_momentum[0] as i128);
        put(w.wall_momentum[1] as i128);
        out
    }

    pub fn digest(&self) -> String {
        blake3::hash(&self.canonical_bytes()).to_hex().to_string()
    }
}

pub fn sub(a: [i64; 2], b: [i64; 2]) -> [i128; 2] {
    [a[0] as i128 - b[0] as i128, a[1] as i128 - b[1] as i128]
}

pub fn dot(a: [i128; 2], b: [i128; 2]) -> i128 {
    a[0] * b[0] + a[1] * b[1]
}

pub fn energy(m: i128, k: [i128; 2]) -> i128 {
    m * (k[0] * k[0] + k[1] * k[1])
}

/// Bin predicate. `d` is b − a at the bin start, `w` = k_b − k_a, `reach` = r_a + r_b:
/// the pair is approaching and min over s in [0, 1] of |d + w·s| ≤ reach.
///
/// Exact for every `i128` input: its products are formed in `i128` when they fit, else in 512 bits ([`Wide`]). Until
/// 13 October 2026 they were formed in `i128` only and wrapped past |d|·|w| ≈ 2^63 (16-52% of the pairs a burn tests in
/// the plane's player scan), answering garbage there; the answer is unchanged wherever nothing wrapped.
pub fn hit(d: [i128; 2], w: [i128; 2], reach: i128) -> bool {
    hit_narrow(d, w, reach).unwrap_or_else(|| hit_in(d.map(Wide::of), w.map(Wide::of), Wide::of(reach)))
}

/// [`hit`] in `i128`, or None if a product or sum would leave it.
fn hit_narrow(d: [i128; 2], w: [i128; 2], reach: i128) -> Option<bool> {
    let dot = |a: [i128; 2], b: [i128; 2]| a[0].checked_mul(b[0])?.checked_add(a[1].checked_mul(b[1])?);
    let (dd, dw, ww, rr) = (dot(d, d)?, dot(d, w)?, dot(w, w)?, reach.checked_mul(reach)?);
    Some(if dd <= rr {
        dw < 0
    } else if ww == 0 || dw >= 0 {
        false
    } else if -dw >= ww {
        let e = [d[0].checked_add(w[0])?, d[1].checked_add(w[1])?];
        dot(e, e)? <= rr
    } else {
        let cross = d[0].checked_mul(w[1])?.checked_sub(d[1].checked_mul(w[0])?)?;
        cross.checked_mul(cross)? <= rr.checked_mul(ww)?
    })
}

/// [`hit`]'s branches over any exact integers.
fn hit_in<T: Copy + Ord + std::ops::Add<Output = T> + std::ops::Sub<Output = T> + std::ops::Mul<Output = T> + From<i8>>(d: [T; 2], w: [T; 2], reach: T) -> bool {
    let dot = |a: [T; 2], b: [T; 2]| a[0] * b[0] + a[1] * b[1];
    let (dd, dw, ww, rr, zero) = (dot(d, d), dot(d, w), dot(w, w), reach * reach, T::from(0));
    if dd <= rr {
        dw < zero
    } else if ww == zero || dw >= zero {
        false
    } else if zero - dw >= ww {
        let e = [d[0] + w[0], d[1] + w[1]];
        dot(e, e) <= rr
    } else {
        let cross = d[0] * w[1] - d[1] * w[0];
        cross * cross <= rr * ww
    }
}

/// A signed 512-bit integer (a sign and little-endian 64-bit limbs): wide enough for any product of four `i128`s, which is
/// all [`hit`] forms. Zero is never negative, so equality is limb equality.
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub struct Wide {
    neg: bool,
    mag: [u64; 8],
}

impl Wide {
    pub fn of(x: i128) -> Self {
        let m = x.unsigned_abs();
        Wide { neg: x < 0, mag: [m as u64, (m >> 64) as u64, 0, 0, 0, 0, 0, 0] }
    }

    fn signed(neg: bool, mag: [u64; 8]) -> Self {
        Wide { neg: neg && mag != [0; 8], mag }
    }

    fn cmp_mag(a: &[u64; 8], b: &[u64; 8]) -> std::cmp::Ordering {
        a.iter().rev().cmp(b.iter().rev())
    }

    /// |a| − |b| for |a| ≥ |b|, or |a| + |b|.
    fn mag_sub(a: &[u64; 8], b: &[u64; 8]) -> [u64; 8] {
        let (mut r, mut borrow) = ([0u64; 8], false);
        for i in 0..8 {
            let (x, o1) = a[i].overflowing_sub(b[i]);
            let (x, o2) = x.overflowing_sub(borrow as u64);
            (r[i], borrow) = (x, o1 || o2);
        }
        r
    }

    fn mag_add(a: &[u64; 8], b: &[u64; 8]) -> [u64; 8] {
        let (mut r, mut carry) = ([0u64; 8], 0u128);
        for i in 0..8 {
            let t = a[i] as u128 + b[i] as u128 + carry;
            (r[i], carry) = (t as u64, t >> 64);
        }
        debug_assert!(carry == 0, "Wide overflow");
        r
    }
}

impl From<i8> for Wide {
    fn from(x: i8) -> Self {
        Wide::of(x as i128)
    }
}

impl std::ops::Add for Wide {
    type Output = Wide;
    fn add(self, o: Wide) -> Wide {
        if self.neg == o.neg {
            return Wide::signed(self.neg, Wide::mag_add(&self.mag, &o.mag));
        }
        match Wide::cmp_mag(&self.mag, &o.mag) {
            std::cmp::Ordering::Less => Wide::signed(o.neg, Wide::mag_sub(&o.mag, &self.mag)),
            _ => Wide::signed(self.neg, Wide::mag_sub(&self.mag, &o.mag)),
        }
    }
}

impl std::ops::Sub for Wide {
    type Output = Wide;
    fn sub(self, o: Wide) -> Wide {
        self + Wide::signed(!o.neg, o.mag)
    }
}

impl std::ops::Mul for Wide {
    type Output = Wide;
    fn mul(self, o: Wide) -> Wide {
        let mut r = [0u64; 8];
        for i in 0..8 {
            if self.mag[i] == 0 {
                continue;
            }
            let mut carry = 0u128;
            for j in 0..8 - i {
                let t = self.mag[i] as u128 * o.mag[j] as u128 + r[i + j] as u128 + carry;
                (r[i + j], carry) = (t as u64, t >> 64);
            }
            debug_assert!(carry == 0 && (8 - i..8).all(|j| o.mag[j] == 0), "Wide overflow");
        }
        Wide::signed(self.neg != o.neg, r)
    }
}

impl Ord for Wide {
    fn cmp(&self, o: &Wide) -> std::cmp::Ordering {
        match (self.neg, o.neg) {
            (false, true) => std::cmp::Ordering::Greater,
            (true, false) => std::cmp::Ordering::Less,
            (false, false) => Wide::cmp_mag(&self.mag, &o.mag),
            (true, true) => Wide::cmp_mag(&o.mag, &self.mag),
        }
    }
}

impl PartialOrd for Wide {
    fn partial_cmp(&self, o: &Wide) -> Option<std::cmp::Ordering> {
        Some(self.cmp(o))
    }
}

/// Smallest u ≥ 0 with `hit(d + w·u, w, reach)`: the pair's next hit is in chronon
/// t0 + u + 1 when `d` is the separation at t0 and neither body revises before. None if
/// the linear motion never hits. Exact; O(log) integer steps.
pub fn first_hit(d: [i128; 2], w: [i128; 2], reach: i128) -> Option<i64> {
    let dw = dot(d, w);
    let ww = dot(w, w);
    if ww == 0 || dw >= 0 {
        return None;
    }
    let rr = reach * reach;
    let dd = dot(d, d);
    // Closest approach beyond reach: never.
    if dd * ww - dw * dw > rr * ww {
        return None;
    }
    if dd <= rr {
        return Some(0);
    }
    // P(u): within reach somewhere in [0, u + 1]. Monotone; true at u = ceil(τ*) - 1 where
    // τ* = -dw/ww is the closest approach, and every u with P(u) and u < τ* hits.
    let p = |u: i128| -> bool {
        if (u + 1) * ww >= -dw {
            return true;
        }
        let e = [d[0] + w[0] * (u + 1), d[1] + w[1] * (u + 1)];
        dot(e, e) <= rr
    };
    let mut hi = (-dw + ww - 1) / ww - 1; // ceil(τ*) - 1 ≥ 0 because dw < 0
    let mut lo = 0i128;
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if p(mid) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    debug_assert!(hit([d[0] + w[0] * lo, d[1] + w[1] * lo], w, reach));
    i64::try_from(lo).ok()
}

/// Smallest s ≥ 1 such that, `s` chronons after the state (x, k), the bouncer is at or
/// beyond a wall while moving outward (it joins that chronon's wall set). `lo`/`hi` are
/// the container inset by the radius. None if it never reaches a wall.
pub fn first_wall(x: [i64; 2], k: [i64; 2], lo: [i64; 2], hi: [i64; 2]) -> Option<i64> {
    let mut best: Option<i64> = None;
    for c in 0..2 {
        let s = if k[c] < 0 {
            let gap = x[c] as i128 - lo[c] as i128;
            Some(((gap + (-k[c] as i128) - 1).div_euclid(-k[c] as i128)).max(1))
        } else if k[c] > 0 {
            let gap = hi[c] as i128 - x[c] as i128;
            Some(((gap + k[c] as i128 - 1).div_euclid(k[c] as i128)).max(1))
        } else {
            None
        };
        if let Some(s) = s.and_then(|s| i64::try_from(s).ok()) {
            best = Some(best.map_or(s, |b| b.min(s)));
        }
    }
    best
}

/// Wall-set membership at the chronon's end position.
pub fn at_wall(x: [i64; 2], k: [i64; 2], lo: [i64; 2], hi: [i64; 2]) -> bool {
    (0..2).any(|c| (k[c] < 0 && x[c] <= lo[c]) || (k[c] > 0 && x[c] >= hi[c]))
}

fn gcd(a: i128, b: i128) -> i128 {
    if b == 0 { a.abs() } else { gcd(b, a % b) }
}

/// Respond under the world's law: every mode calls this, never a law's function directly.
pub fn respond(
    law: Law,
    q: i64,
    bodies: &mut [Body],
    pairs: &[(usize, usize)],
    walls: &[bool],
    container: Option<&Container>,
    wall_momentum: &mut [i64; 2],
) {
    match law {
        Law::Newtonian => resolve(bodies, pairs, walls, container, wall_momentum),
        Law::Relativistic | Law::RelativisticV1 => crate::relativity::resolve_law(law, q, bodies, pairs, walls, container, wall_momentum),
    }
}

/// Newtonian response to one chronon's batch (or any union of its connected components).
///
/// `bodies`: the batch's bodies sorted by id, already advanced to the chronon's end, with
/// `k` the velocity during the bin. `pairs`: hit pairs as (i, j) indices into `bodies`,
/// i < j, sorted. `walls[i]`: body i is in the wall set. Revisions and residuals are
/// updated in place; the caller consumes every pair at the new revisions and logs events.
pub fn resolve(
    bodies: &mut [Body],
    pairs: &[(usize, usize)],
    walls: &[bool],
    container: Option<&Container>,
    wall_momentum: &mut [i64; 2],
) {
    debug_assert_eq!(walls.len(), bodies.len());
    let before: Vec<[i64; 2]> = bodies.iter().map(|b| b.k).collect();
    let mut k: Vec<[i128; 2]> = before.iter().map(|k| [k[0] as i128, k[1] as i128]).collect();
    let mut work: Vec<i128> = bodies.iter().map(|b| b.residual as i128).collect();
    let mut changed_work = vec![false; bodies.len()];
    let (mut pair_errors, initial) = (0i128, bodies.iter().map(Body::energy).sum::<i128>());
    for &(a, b) in pairs {
        if bodies[a].response != Response::Bounce || bodies[b].response != Response::Bounce {
            continue;
        }
        changed_work[a] = true;
        changed_work[b] = true;
        let (ka, kb) = (k[a], k[b]);
        let d = sub(bodies[b].x, bodies[a].x);
        let w = [kb[0] - ka[0], kb[1] - ka[1]];
        let dotp = dot(d, w);
        let dd = dot(d, d);
        if dotp >= 0 || dd == 0 {
            continue;
        }
        let (ma, mb) = (bodies[a].mass as i128, bodies[b].mass as i128);
        let lcm = ma / gcd(ma, mb) * mb;
        // Momentum to a in lattice steps lcm/Q: d·2·ma·mb·dot / ((ma+mb)·dd·lcm).
        let den = (ma + mb) * dd * lcm;
        let num = [d[0] * 2 * ma * mb * dotp, d[1] * 2 * ma * mb * dotp];
        let exact_nonzero = num[0] != 0 || num[1] != 0;
        let fl = |v: i128| v.div_euclid(den);
        let ce = |v: i128| -(-v).div_euclid(den);
        let mut cands: Vec<[i128; 2]> = Vec::with_capacity(4);
        for x in [fl(num[0]), ce(num[0])] {
            for y in [fl(num[1]), ce(num[1])] {
                let c = [x, y];
                if !cands.contains(&c) && !(c == [0, 0] && exact_nonzero) {
                    cands.push(c);
                }
            }
        }
        let owed = work[a] + work[b];
        let mut best: Option<(i128, [i128; 2], [i128; 2], i128)> = None;
        for c in cands {
            let da = [c[0] * (lcm / ma), c[1] * (lcm / ma)];
            let db = [-c[0] * (lcm / mb), -c[1] * (lcm / mb)];
            let e = energy(ma, [ka[0] + da[0], ka[1] + da[1]]) + energy(mb, [kb[0] + db[0], kb[1] + db[1]])
                - energy(ma, ka)
                - energy(mb, kb);
            let score = (owed + e).abs();
            if best.as_ref().is_none_or(|(s, ..)| score < *s) {
                best = Some((score, da, db, e));
            }
        }
        let (_, da, db, e) = best.expect("at least one candidate");
        work[a] += e;
        pair_errors += e;
        k[a] = [ka[0] + da[0], ka[1] + da[1]];
        k[b] = [kb[0] + db[0], kb[1] + db[1]];
    }
    debug_assert_eq!(
        k.iter().zip(bodies.iter()).map(|(k, b)| energy(b.mass as i128, *k)).sum::<i128>() - initial,
        pair_errors,
        "sequential pair errors telescope to the batch error"
    );
    for &(a, b) in pairs {
        for i in [a, b] {
            if bodies[i].response == Response::Stop {
                k[i] = [0, 0];
            }
        }
    }
    if let Some(c) = container {
        for (i, body) in bodies.iter().enumerate() {
            if !walls[i] {
                continue;
            }
            let (lo, hi) = c.inset(body.radius);
            for ax in 0..2 {
                if (body.x[ax] <= lo[ax] && k[i][ax] < 0) || (body.x[ax] >= hi[ax] && k[i][ax] > 0) {
                    wall_momentum[ax] += (body.mass as i128 * 2 * k[i][ax]) as i64;
                    k[i][ax] = -k[i][ax];
                }
            }
        }
    }
    for (i, body) in bodies.iter_mut().enumerate() {
        if changed_work[i] {
            body.residual = i64::try_from(work[i]).expect("carry fits i64");
        }
        let nk = [k[i][0] as i64, k[i][1] as i64];
        if nk != before[i] {
            body.k = nk;
            body.rev += 1;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::worlds::Rng;

    /// The wide path answers as the `i128` one wherever that one fits, over every magnitude up to its edge.
    #[test]
    fn hit_wide_agrees_with_narrow_where_it_fits() {
        let mut rng = Rng(13);
        let mut cases = [0u32; 2];
        for i in 0..400_000 {
            let bits = (i % 63) as u32 + 1;
            let mut r = |b: u32| ((rng.next() as i128) << 64 | rng.next() as i128) >> (127 - b);
            let (d, w, reach) = ([r(bits), r(bits)], [r(bits), r(bits)], r(bits).abs());
            if let Some(narrow) = hit_narrow(d, w, reach) {
                assert_eq!(hit_in(d.map(Wide::of), w.map(Wide::of), Wide::of(reach)), narrow, "d {d:?} w {w:?} reach {reach}");
                cases[narrow as usize] += 1;
            }
        }
        assert!(cases[0] > 10_000 && cases[1] > 10_000, "both answers exercised: {cases:?}");
    }

    /// The predicate is homogeneous: scaling d, w and the reach by 2^s never changes it, so a small case scaled far past
    /// i128's products (where the old predicate wrapped) must answer as the small case.
    #[test]
    fn hit_is_exact_past_the_i128_products() {
        let mut rng = Rng(17);
        let (mut wide, mut yes) = (0u32, 0u32);
        for _ in 0..200_000 {
            let d = [rng.range(-300, 300) as i128, rng.range(-300, 300) as i128];
            let w = [rng.range(-40, 40) as i128, rng.range(-40, 40) as i128];
            let reach = rng.range(1, 40) as i128;
            let small = hit(d, w, reach);
            let s = rng.range(40, 117) as u32;
            let (ds, ws, rs) = (d.map(|x| x << s), w.map(|x| x << s), reach << s);
            wide += hit_narrow(ds, ws, rs).is_none() as u32;
            assert_eq!(hit(ds, ws, rs), small, "d {d:?} w {w:?} reach {reach} scaled by 2^{s}");
            yes += small as u32;
        }
        assert!(wide > 150_000 && yes > 1_000, "the wide path and hits exercised: {wide} wide, {yes} hits");
    }
}
