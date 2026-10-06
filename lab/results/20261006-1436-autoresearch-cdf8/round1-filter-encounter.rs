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
pub static SKIPPED: std::sync::atomic::AtomicUsize = std::sync::atomic::AtomicUsize::new(0);
pub static BANDED: std::sync::atomic::AtomicUsize = std::sync::atomic::AtomicUsize::new(0);
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

/// The finder reads the canonical tubes, never the ramp ([`crate::observe::credit`]): it is an outcome (its log is in the
/// digest), the player's kick at tick `M` reads a body whose own kick at `M` comes later in the order of ids, and the ramp
/// is a reader's completion of the state between kicks, which at a kick's own tick differs between the bodies that have
/// fired it and those that have not (by the kick's half, in a body's first window). The tubes are continuous at a kick;
/// the finder's neighbourhood (`2^ENCOUNTER_LOG2` of the radii) is orders of magnitude above what the ramp adds.
impl Encounters for PlayerNeighbourhood {
    fn find(&self, ctx: &Ctx, body: usize, t: Tick, interval: Tick) -> Vec<Encounter> {
        let mut out = Vec::new();
        let Some(me) = ctx.bodies.binding_at(body, t) else { return out };
        let Ok((x, v)) = me.cartesian(t) else { return out };
        let h = match time_of(interval, me.clock_exp) {
            Ok(h) => h,
            Err(_) => return out,
        };
        // The player's own norms, bounded both ways (sqrt truncates down, so `hi` re-inflates it).
        let norm = |a: V2| -> emergent_space::Result<Scalar> { a[0].mul(a[0])?.add(a[1].mul(a[1])?)?.sqrt() };
        let infl = |s: Scalar| -> emergent_space::Result<Scalar> { s.add(s.scale(-30)?) };
        let filter = match (norm(x), norm(v)) {
            (Ok(xl), Ok(vl)) => match (infl(xl), infl(vl)) {
                (Ok(xh), Ok(vh)) => Some((xl, xh, vh)),
                _ => None,
            },
            _ => None,
        };
        for j in 0..ctx.bodies.len() {
            // A member handed out of a frame is there for the ticks after its hand-out.
            if j == body || !ctx.bodies.alive(j) || t <= ctx.info[j].born {
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
            // Exact band pre-filter: skip a body whose whole radius band stays farther than the
            // neighbourhood over the interval even at its fastest (bands above).
            if let Some((x_lo, x_hi, v_me)) = filter {
                if let Some((r_lo, r_hi, v_hi)) = bands(&other) {
                    BANDED.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                    let skip = (|| -> Option<bool> {
                        let near = reach.scale(ENCOUNTER_LOG2).ok()?;
                        let drift = v_hi.add(v_me).ok()?.mul(h).ok()?;
                        let margin = near.add(drift).ok()?.add(near.scale(-30).ok()?).ok()?;
                        Some(r_lo.sub(x_hi).ok()?.gt(&margin) || x_lo.sub(r_hi).ok()?.gt(&margin))
                    })();
                    if skip == Some(true) {
                        // Self-check (development): a skipped pair must be one the exact
                        // predicate rejects; say so loudly when it is not.
                        let check = (|| -> Res<Option<bool>> {
                            let (xj, vj) = other.cartesian(t)?;
                            let d = sub2(xj, x)?;
                            let w = [vj[0].sub(v[0])?.mul(h)?, vj[1].sub(v[1])?.mul(h)?];
                            let q_exp = reach.exponent() as i32 - 20;
                            let (di, wi) = (integers(d, q_exp)?, integers(w, q_exp)?);
                            let near = reach.scale(ENCOUNTER_LOG2)?.fixed(-q_exp)?;
                            Ok(Some(hit(di, wi, near)))
                        })();
                        if check == Ok(Some(true)) {
                            eprintln!(
                                "UNSAFE SKIP: j={j} r_lo={} r_hi={} x_hi={} margin={} actual_hit=true",
                                r_lo.significand() as f64 * 2f64.powi(r_lo.exponent() as i32 - 62),
                                r_hi.significand() as f64 * 2f64.powi(r_hi.exponent() as i32 - 62),
                                x_hi.significand() as f64 * 2f64.powi(x_hi.exponent() as i32 - 62),
                                (|| -> Option<f64> {
                                    let near = reach.scale(ENCOUNTER_LOG2).ok()?;
                                    let drift = v_hi.add(v_me).ok()?.mul(h).ok()?;
                                    Some((near.add(drift).ok()?).significand() as f64 * 2f64.powi((near.add(drift).ok()?).exponent() as i32 - 62))
                                })().unwrap_or(f64::NAN)
                            );
                        }
                        SKIPPED.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        continue;
                    }
                }
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

pub fn bands(b: &crate::bind::Binding) -> Option<(Scalar, Scalar, Scalar)> {
    let r = bands_in(b);
    if std::env::var("ENC_DEBUG").is_ok() && r.is_none() {
        eprintln!("bands: none (key.k={}, peri_exp={}, units=({},{}) residual={:?})", b.entry.trajectory.key().k, b.entry.trajectory.key().periapsis.exponent(), b.units.0, b.units.1, b.residual.position);
    }
    r
}

fn bands_in(b: &crate::bind::Binding) -> Option<(Scalar, Scalar, Scalar)> {
/// rejection (the fit's residual and sub-quantum turn are read from the binding; sqrt and division
/// truncate toward zero). `None` disables the pre-filter for that binding.
    use emergent_space::binding::Trajectory;
    let key = b.entry.trajectory.key();
    let ks = Scalar::raw(key.k as i128, -48).ok()?;
    let unit = &b.entry.unit;
    let to_doll = |s: Scalar| -> Option<Scalar> {
        if unit.unity {
            Some(s)
        } else {
            unit.to_doll(s).ok()
        }
    };
    let r_hi_tube = match &b.entry.trajectory {
        Trajectory::Cycle(_) => key.periapsis.div(ks.scale(1).ok()?.sub(Scalar::ONE).ok()?).ok()?,
        Trajectory::Passage(p) => p.outer_radius,
    };
    let v_hi = if key.null { Scalar::ONE } else { Scalar::ONE.div(key.periapsis.mul(ks).ok()?).ok()?.sqrt().ok()? };
    let pad = |s: Scalar| -> Option<Scalar> { Some(s.add(s.scale(-30).ok()?).ok()?) };
    let res = |r: [i128; 2], exp: i16| -> Scalar {
        Scalar::raw(r[0].unsigned_abs().max(r[1].unsigned_abs()) as i128, exp as i32).unwrap_or(Scalar::ZERO)
    };
    let (res_r, res_v) = (res(b.residual.position, b.units.0), res(b.residual.velocity, b.units.1));
    let (q_r, q_v) = (Scalar::raw(2, b.units.0 as i32).ok()?, Scalar::raw(2, b.units.1 as i32).ok()?);
    let (r_lo, r_hi) = (to_doll(key.periapsis)?, pad(to_doll(r_hi_tube)?)?);
        let slack_r = res_r.add(r_hi.scale(-27).ok()?).ok()?.add(q_r).ok()?;
        let slack_v = res_v.add(v_hi.scale(-27).ok()?).ok()?.add(q_v).ok()?.add(pad(v_hi)?).ok()?;
    let v_hi = v_hi.add(slack_v).ok()?;
    Some((
        r_lo.sub(slack_r).ok()?,
        r_hi.add(slack_r).ok()?,
        v_hi,
    ))
}

