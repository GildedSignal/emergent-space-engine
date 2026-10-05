//! The kick sources and SyMBA's smooth changeover (Duncan, Levison and Lee, 1998).
//!
//! A body's drift is the compiled geodesic of the doll it sits in (zero work). Everything else
//! is a kick: the parent's tide (the full differential pull, never its linear truncation), and
//! the pull of every secondary in the doll (a planet in the star's doll; the moon in a planet's).
//! A secondary's pull `V` is split across **levels** by weights that are smooth functions of the
//! separation only, so the split stays symplectic (a state-selected switch at the sphere of
//! influence is not: events3 measured Jacobi growth 0.83):
//!
//! ```text
//!   B_l(r) = S((r − R_l/2)/(R_l/2)),   S(y) = y²(3 − 2y) on [0,1]   (0 inside R_l/2, 1 outside R_l)
//!   W_0 = B_0,   W_1 = (1 − B_0)·B_1,   …,   W_L = Π(1 − B_i)   (they sum to 1)
//! ```
//!
//! with the shells `R_l = 2^(1−l)·R_edge` (`R_edge` the secondary's sphere of influence).
//! Level `l` kicks `W_l·V` at a step `H/4^l`: far pairs are kicked once per step, a pair inside
//! the shells is kicked on finer steps, recursively, only while it is inside.
//!
//! **The doll's origin falls** (docs/law.md). A doll is centred on its dominant body, which is pulled
//! by every secondary in the doll: the frame is accelerated, so every member's kick carries the
//! origin's acceleration with the opposite sign, `−Σ_j gm_j·x_j/|x_j|³`, one uniform vector per kick
//! epoch (the indirect term of a heliocentric split). It depends on the secondaries' positions alone,
//! never on the member's, so it is a level-0 kick like the parent's tide (the parent's tide already is
//! the origin's fall toward the *parent*: the differential pull). Without it a member far from a
//! secondary feels the secondary's whole pull with nothing to balance it.
use crate::num::{add2, dot2, norm2, scale2, sub2, Res, V2};
use emergent_space::{events::kicks::parent_tide, orbit::Scalar};

/// The deepest level of the changeover, and the step ratio between levels.
pub const LEVELS: u8 = 3;
pub const RATIO: i64 = 4;

/// `S(y) = y²(3 − 2y)` for `y` clipped to `[0, 1]`.
fn smooth(y: Scalar) -> Res<Scalar> {
    if y <= Scalar::ZERO {
        return Ok(Scalar::ZERO);
    }
    if y >= Scalar::ONE {
        return Ok(Scalar::ONE);
    }
    Ok(y.mul(y)?.mul(Scalar::integer(3).sub(y.scale(1)?)?)?)
}

/// `B_l(r)` for the shell radius `big_r`: zero inside `big_r/2`, one outside `big_r`.
fn boundary(r: Scalar, big_r: Scalar) -> Res<Scalar> {
    let half = big_r.scale(-1)?;
    smooth(r.sub(half)?.div(half)?)
}

/// The shell radius `R_l` of level `l` (`l < LEVELS`).
pub fn shell(edge: Scalar, l: u8) -> Res<Scalar> {
    Ok(edge.scale(1 - l as i32)?)
}

/// `W_l(r)`: the share of the pair's interaction kicked at level `l`:
/// `W_l = B_l·Π_{i<l}(1 − B_i)`, and the deepest level takes the rest, `Π_{i<L}(1 − B_i)`.
pub fn weight(l: u8, r: Scalar, edge: Scalar) -> Res<Scalar> {
    let mut w = Scalar::ONE;
    for i in 0..l.min(LEVELS) {
        w = w.mul(Scalar::ONE.sub(boundary(r, shell(edge, i)?)?)?)?;
        if w.is_zero() {
            return Ok(w);
        }
    }
    if l < LEVELS {
        w = w.mul(boundary(r, shell(edge, l)?)?)?;
    }
    Ok(w)
}

/// A secondary at the kick's time: its strength, position in the doll's units, velocity, and its
/// sphere of influence (the changeover's scale).
#[derive(Clone, Copy, Debug)]
pub struct Secondary {
    pub gm: Scalar,
    pub pos: V2,
    pub vel: V2,
    pub edge: Scalar,
}

/// `gm·(xj − x)/|xj − x|³` and the distance.
pub fn pull(gm: Scalar, xj: V2, x: V2) -> Res<(V2, Scalar)> {
    let d = sub2(xj, x)?;
    let r = norm2(d)?;
    if r.is_zero() {
        return Err(crate::num::Error::Refused("a body on top of its secondary"));
    }
    let k = gm.div(r.mul(r)?.mul(r)?)?;
    Ok((scale2(d, k)?, r))
}

/// The origin's acceleration toward the secondaries, `Σ_j gm_j·x_j/|x_j|³`: what a member's kick subtracts.
pub fn origin_fall(secondaries: &[Secondary]) -> Res<V2> {
    let mut a = [Scalar::ZERO; 2];
    for s in secondaries {
        let r = norm2(s.pos)?;
        if r.is_zero() {
            return Err(crate::num::Error::Refused("a secondary on top of its doll's centre"));
        }
        a = add2(a, scale2(s.pos, s.gm.div(r.mul(r)?.mul(r)?)?)?)?;
    }
    Ok(a)
}

/// The acceleration a body at `x` feels at the kick of `level`: the changeover share of every
/// secondary's pull and, at level 0, the origin's fall toward the secondaries and the parent's tide.
/// `secondaries` are the doll's other sources (the body itself excluded).
/// `tide` is `(parent mass, centre of the doll in the parent's frame)` in this doll's units.
pub fn acceleration(level: u8, x: V2, secondaries: &[Secondary], tide: Option<(Scalar, V2)>) -> Res<V2> {
    let mut a = [Scalar::ZERO; 2];
    for s in secondaries {
        let (p, r) = pull(s.gm, s.pos, x)?;
        let w = weight(level, r, s.edge)?;
        if !w.is_zero() {
            a = add2(a, scale2(p, w)?)?;
        }
    }
    if level == 0 {
        a = sub2(a, origin_fall(secondaries)?)?;
        if let Some((mass, centre)) = tide {
            a = add2(a, parent_tide(mass, centre, x)?)?;
        }
    }
    Ok(a)
}

/// Whether level `l + 1` must be engaged on an interval of length `h` (doll time units) starting
/// at separation `r` with relative speed `speed`: the pair can reach the support of `W_{l+1}`
/// (`r < R_l`) within the interval, with 25% of margin on the distance travelled. A
/// conservative certificate (every pair that could be weighted is engaged), so the weights
/// outside it are zero and the split is exact.
pub fn engaged(l: u8, r: Scalar, speed: Scalar, h: Scalar, edge: Scalar) -> Res<bool> {
    let reach = speed.mul(h)?.mul(Scalar::raw(5, -2)?)?;
    Ok(r.sub(reach)? < shell(edge, l)?)
}

/// Relative speed |v − vj| of body and secondary.
pub fn relative_speed(v: V2, vj: V2) -> Res<Scalar> {
    norm2(sub2(v, vj)?)
}

/// The dot product of position and acceleration is not needed here; kept for the Jacobi tests.
pub fn work(v: V2, a: V2) -> Res<Scalar> {
    dot2(v, a)
}
