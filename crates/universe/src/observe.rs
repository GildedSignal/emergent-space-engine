//! Observation: pure functions of the state. Nothing here writes. Floats are allowed (the view is
//! not an outcome), and every read goes through the bodies' histories at the asked tick.
use crate::body::BodyRec;
use crate::ctx::Ctx;
use crate::num::{to_f64, Res, Tick};
use crate::{step, thrust};

/// A body's position and velocity in the root frame (root length units, c = 1, so one root length
/// unit is one tick of light travel) at root tick `t`: its own state in its doll, scaled to root
/// units, plus the doll centre's state, recursively up the tree. Dolls share axes (no rotation).
pub fn root_state(ctx: &Ctx, i: usize, t: Tick) -> Res<([f64; 2], [f64; 2])> {
    let b = ctx.bodies.binding_at(i, t).ok_or(crate::num::Error::Refused("history pruned"))?;
    let (p, v) = b.cartesian(t)?;
    let k = 2f64.powi(-(ctx.dolls[b.doll as usize].shift as i32));
    let mut pos = [to_f64(p[0]) * k, to_f64(p[1]) * k];
    let mut vel = [to_f64(v[0]), to_f64(v[1])];
    if let Some(c) = ctx.dolls[b.doll as usize].centre {
        let (cp, cv) = root_state(ctx, c, t)?;
        pos = [pos[0] + cp[0], pos[1] + cp[1]];
        vel = [vel[0] + cv[0], vel[1] + cv[1]];
    }
    Ok((pos, vel))
}

/// The chain of (doll, state in that doll) from the body up to the root, for the clock rate.
pub fn chain(ctx: &Ctx, i: usize, t: Tick) -> Res<Vec<(u16, [f64; 2], [f64; 2])>> {
    let b = ctx.bodies.binding_at(i, t).ok_or(crate::num::Error::Refused("history pruned"))?;
    let (p, v) = b.cartesian(t)?;
    let mut out = vec![(b.doll, [to_f64(p[0]), to_f64(p[1])], [to_f64(v[0]), to_f64(v[1])])];
    if let Some(c) = ctx.dolls[b.doll as usize].centre {
        out.extend(chain(ctx, c, t)?);
    }
    Ok(out)
}

/// The rate of a body's clock against the root's, `dτ/dt`, derived from the doll clocks: the
/// product, up the chain, of each tube's own rate in its doll, `√(f − v_r²/f − v_t²)` with
/// `f = 1 − 2/r` (the Schwarzschild lapse in the doll's units), corrected for the velocity
/// composition between a doll and its centre (`1 + v_centre·v_rel`). Nothing is stored or evolved.
pub fn clock_rate(ctx: &Ctx, i: usize, t: Tick) -> Res<f64> {
    let ch = chain(ctx, i, t)?;
    let mut rate = 1.0;
    for (k, (_, p, v)) in ch.iter().enumerate() {
        let r = (p[0] * p[0] + p[1] * p[1]).sqrt();
        let f = 1.0 - 2.0 / r;
        let vr = (p[0] * v[0] + p[1] * v[1]) / r;
        let vt = (p[0] * v[1] - p[1] * v[0]) / r;
        rate *= (f - vr * vr / f - vt * vt).max(1e-300).sqrt();
        if let Some((_, _, vc)) = ch.get(k + 1) {
            // the doll's centre moves at `vc` in the parent: composing velocities (1 + vc·v).
            rate /= 1.0 + vc[0] * v[0] + vc[1] * v[1];
        }
    }
    Ok(rate)
}

/// A body's position and velocity in the root frame and the rate of its clock against the root's, all
/// at root tick `t`, in one walk up the doll chain: [`root_state`] and [`clock_rate`] share every readout
/// (the view reads both for each emitter, at the emitter's retarded time).
pub fn state_rate(ctx: &Ctx, i: usize, t: Tick) -> Res<([f64; 2], [f64; 2], f64)> {
    let (mut pos, mut vel, mut rate) = ([0.0f64; 2], [0.0f64; 2], 1.0f64);
    let (mut cur, mut below) = (i, None::<[f64; 2]>);
    loop {
        let b = ctx.bodies.binding_at(cur, t).ok_or(crate::num::Error::Refused("history pruned"))?;
        let (p, v) = b.cartesian(t)?;
        let (p, v) = ([to_f64(p[0]), to_f64(p[1])], [to_f64(v[0]), to_f64(v[1])]);
        let doll = &ctx.dolls[b.doll as usize];
        let k = 2f64.powi(-(doll.shift as i32));
        pos = [pos[0] + p[0] * k, pos[1] + p[1] * k];
        vel = [vel[0] + v[0], vel[1] + v[1]];
        // This level's own rate (see `clock_rate`), then the velocity composition with the level below.
        let r = (p[0] * p[0] + p[1] * p[1]).sqrt();
        let f = 1.0 - 2.0 / r;
        let vr = (p[0] * v[0] + p[1] * v[1]) / r;
        let vt = (p[0] * v[1] - p[1] * v[0]) / r;
        rate *= (f - vr * vr / f - vt * vt).max(1e-300).sqrt();
        if let Some(vb) = below {
            rate /= 1.0 + v[0] * vb[0] + v[1] * vb[1];
        }
        below = Some(v);
        match doll.centre {
            Some(c) => cur = c,
            None => break,
        }
    }
    Ok((pos, vel, rate))
}

/// What the player's held thrust has made of its state since the last flush, at tick `t`: the heading
/// (turns, Q32) and the change of velocity (the burn owed), the same a flush at `t` would write. A pure
/// read, so the view shows the keys within the frame instead of at the next kick.
pub fn held_thrust(ctx: &Ctx, rec: &BodyRec, t: Tick) -> Res<Option<(u32, [f64; 2])>> {
    let Some(th) = rec.thrust else { return Ok(None) };
    if th.keys == 0 || t <= th.since || t < rec.b.event_time {
        return Ok(None);
    }
    let dtau = step::proper_since(&rec.b, ctx.dolls[rec.b.doll as usize].shift, th.since, t)?;
    let (x, v) = rec.b.cartesian(t)?;
    let (heading, v2) = thrust::owed(ctx.cfg, th, dtau, x, v)?;
    Ok(Some((heading, [to_f64(v2[0]) - to_f64(v[0]), to_f64(v2[1]) - to_f64(v[1])])))
}
