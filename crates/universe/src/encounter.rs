//! Encounters sit behind one seam: [`Encounters`] answers "which pairs come close within this
//! interval". Today the answer is an exact check for the player's neighbourhood
//! ([`PlayerNeighbourhood`]); later the Binet cone of `crates/encounters` (orbits cross only inside a
//! 2+1 light cone, found with no work per orbit) implements the same trait, with no rewiring.
//!
//! The predicate is the lattice law's own bin predicate (`emergent_lattice::law::hit`): the pair's
//! linear relative motion over the interval comes within `reach`, exact in integers. A
//! *contact* is within the two bodies' radii; an *encounter* is within `2^ENCOUNTER_LOG2` of them
//! (the neighbourhood the player's own instruments would call close).
use crate::ctx::Ctx;
use crate::num::{sub2, time_of, Res, Tick, V2};
use emergent_lattice::law::hit;
use emergent_space::orbit::Scalar;

pub const ENCOUNTER_LOG2: i32 = 10;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Encounter {
    pub a: usize,
    pub b: usize,
    pub t: Tick,
    /// Within the two radii (a contact), not only within the neighbourhood.
    pub contact: bool,
}

pub trait Encounters: Send + Sync {
    /// The pairs `(body, other)` that come close during `[t, t + interval]`, given every body's tube.
    fn find(&self, ctx: &Ctx, body: usize, t: Tick, interval: Tick) -> Vec<Encounter>;
}

/// The exact check for the player's neighbourhood: every body in the player's doll, tested against
/// the player over the interval.
pub struct PlayerNeighbourhood;

fn integers(a: V2, q_exp: i32) -> Res<[i128; 2]> {
    Ok([a[0].fixed(-q_exp)?, a[1].fixed(-q_exp)?])
}

impl Encounters for PlayerNeighbourhood {
    fn find(&self, ctx: &Ctx, body: usize, t: Tick, interval: Tick) -> Vec<Encounter> {
        let mut out = Vec::new();
        let Some(me) = ctx.bodies.binding_at(body, t) else { return out };
        let Ok((x, v)) = me.cartesian(t) else { return out };
        let h = match time_of(interval, me.clock_exp) {
            Ok(h) => h,
            Err(_) => return out,
        };
        for j in 0..ctx.bodies.len() {
            if j == body || !ctx.bodies.alive(j) {
                continue;
            }
            let Some(other) = ctx.bodies.binding_at(j, t) else { continue };
            if other.doll != me.doll {
                continue;
            }
            let reach = ctx.info[body].radius.add(ctx.info[j].radius).unwrap_or(Scalar::ZERO);
            if reach.is_zero() {
                continue;
            }
            let found = (|| -> Res<Option<bool>> {
                let (xj, vj) = other.cartesian(t)?;
                let d = sub2(xj, x)?;
                let w = [vj[0].sub(v[0])?.mul(h)?, vj[1].sub(v[1])?.mul(h)?];
                // Integers in units of reach/2^20: the lattice predicate is exact on i128.
                let q_exp = reach.exponent() as i32 - 20;
                let (di, wi) = (integers(d, q_exp)?, integers(w, q_exp)?);
                let near = reach.scale(ENCOUNTER_LOG2)?.fixed(-q_exp)?;
                if !hit(di, wi, near) {
                    return Ok(None);
                }
                Ok(Some(hit(di, wi, reach.fixed(-q_exp)?)))
            })();
            if let Ok(Some(contact)) = found {
                out.push(Encounter { a: body, b: j, t, contact });
            }
        }
        out
    }
}
