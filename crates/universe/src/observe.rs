//! Observation: pure functions of the state. Nothing here writes. Floats are allowed (the view is
//! not an outcome), and every read goes through the bodies' histories at the asked tick.
//!
//! **A body's state between kicks** (docs/law.md): the split's state exists at a body's step boundaries; between them
//! a reader completes the tube, so what it reads is second order in the step (the raw tube alone carries a pending half
//! kick and is first order). A body of the motion law v2 ([`crate::ext`]) is read through the **partial step** ([`partial`]):
//! the map run from the last boundary for just the time read; the others through a ramp ([`credit`]). [`root_state`],
//! [`chain`] and [`state_rate`] all read through [`ramped`]; [`root_state_raw`] is the tube alone, for the scheduler's
//! deadlines, which are never an outcome.
use crate::bind::{Binding, Kick};
use crate::body::{BodyRec, BodyStore};
use crate::force;
use crate::ctx::Ctx;
use crate::num::{add2, scale2, time_of, to_f64, Res, Tick, V2};
use crate::{step, thrust};
use emergent_space::orbit::Scalar;

/// What a reader at tick `t` adds to the tube of `b` (the binding that holds at `t`, body `i`): the velocity the
/// kicks around `t` have not yet delivered (or have delivered early), and the position it moves, in the doll's
/// units (`(Δx, Δv)`, with `c = 1`).
///
/// A kick at tick `M` stands for a force spread over its window `[M − len/2, M + len/2)`: at the window's start the
/// body has none of it, at its end all, and the tube holds all of it from `M` on, so the tube is wrong inside the
/// window by the part not yet delivered: first order in the step, the pending half kick. Taking the force linear
/// over the window (its mean `Δ/len`, its slope from the kick before it at the same level), with `s = (t − M −
/// len/2)/len` (zero at the window's end, where the map's state is exact):
///
/// ```text
///   Δv = Δ·s + δ·s(s + 1)/2             Δx = len·(Δ·s²/2 + δ·(s − 1/2)(s + 1)²/6)      (δ = Δ − Δ_before)
/// ```
///
/// the integrals of the force less what the tube has, so a reader sees a state second order in the step (error
/// `O(Δ²)` of the force's change, instead of the tube's own `O(Δ)`). The formula holds for `t` in `[M, M + len)`: past
/// the window's end it extrapolates the force one step on (the next kick has not fired in any history that ends at
/// `t`, and a reader never needs what is not yet resolved).
///
/// Only the past is read, so the result is a pure function of the history up to `t`, whatever the engine has
/// resolved beyond it. Every level of SyMBA's changeover has its own windows, nested: the latest kick of each
/// counts, found by walking back through the bindings until the whole step's level (0) is met, or the chain breaks (a
/// binding that is not a kick: a handoff, a burn's flush), or no earlier kick can reach `t`.
pub fn credit(bodies: &dyn BodyStore, i: usize, t: Tick, b: &Binding) -> Res<(V2, V2)> {
    let zero = [Scalar::ZERO; 2];
    if b.kick.len == 0 {
        return Ok((zero, zero));
    }
    // The latest and the one before it, per level: (the tick, the kick, the velocity exponent of its binding).
    let mut latest: [Option<(Tick, Kick, i32)>; 4] = [None; 4];
    let mut before: [Option<(Tick, Kick, i32)>; 4] = [None; 4];
    let mut held: Option<Binding> = None;
    loop {
        let cur = held.as_ref().unwrap_or(b);
        let k = cur.kick;
        if k.len == 0 {
            break;
        }
        let m = cur.event_time;
        let l = k.level as usize;
        let rec = (m, k, cur.units.1 as i32);
        if latest[l].is_none() {
            latest[l] = Some(rec);
        } else if before[l].is_none() {
            before[l] = Some(rec);
        }
        // The whole step's level is the coarsest: with its two latest kicks nothing earlier matters; and no kick before
        // `cur` reaches `t` once `t` is more than two of the whole step's windows past it.
        if before[0].is_some() || (t - m) > (k.len << (2 * k.level as u32 + 1)) {
            break;
        }
        match bodies.binding_at(i, m - 1) {
            Some(p) => held = Some(p),
            None => break,
        }
    }
    let (mut dx, mut dv) = (zero, zero);
    let half = Scalar::raw(1, -1)?;
    for l in 0..4 {
        let Some((m, k, ve)) = latest[l] else { continue };
        if t < m || t - m >= k.len {
            continue;
        }
        // The mean force's kick and its change from the kick before it (adjacent, the same level), in quanta.
        let delta = match before[l] {
            Some((mb, kb, _)) if m - mb == k.len && kb.len == k.len => [k.dv[0] as i128 - kb.dv[0] as i128, k.dv[1] as i128 - kb.dv[1] as i128],
            _ => [0, 0],
        };
        let s = Scalar::raw((t - m) as i128 - ((k.len as i128 + 1) >> 1), 0)?.div(Scalar::raw(k.len as i128, 0)?)?;
        let s1 = s.add(Scalar::ONE)?;
        let (s2, ss1) = (s.mul(s)?, s.mul(s1)?);
        let xs = s.sub(half)?.mul(s1.mul(s1)?)?;
        let len = Scalar::raw(k.len as i128, 0)?;
        for c in 0..2 {
            let (d, dd) = (Scalar::raw(k.dv[c] as i128, ve)?, Scalar::raw(delta[c], ve)?);
            let vc = d.mul(s)?.add(dd.mul(ss1)?.scale(-1)?)?;
            let xc = d.mul(s2)?.scale(-1)?.add(dd.mul(xs)?.div(Scalar::integer(6))?)?;
            dv[c] = dv[c].add(vc)?;
            // `Δx` is in velocity·ticks: a tick is `2^clock_exp` of the doll's time (and length) units.
            dx[c] = dx[c].add(len.mul(xc)?.scale(b.clock_exp as i32)?)?;
        }
    }
    Ok((dx, dv))
}

/// **The partial step** (the Opus motion memo, §2.7; the motion law v2): the state a reader sees at `t`, between the step's
/// boundaries, is the map run from the last boundary for the physical time read, `Φ_σ = D(σ/2)·Kc(σ)·D(σ/2)` with `σ` solving
/// `t(σ) = t_read`: a pure function of the body's history and of the sources' tubes, second order like the map.
///
/// With `τ = t − B` the time since the boundary `B` (a synchronised state: the tube read there, bit for bit), the step's kick has
/// the weight `w = τ·f'(U_P + c)/f'(H_D + p_t + c)`, and `H_D + p_t = U_P` on the constraint the map keeps (to its own second
/// order), so `w = τ`: the half drift to `B + τ/2`, the kick `τ·∇U_P` there (one evaluation of the sources, at that tick), the
/// half drift to `t`. The drifts are the tube; the kick is the velocity `Δv = τ·a` it adds and, `τ/2` later, the position
/// `Δx = Δv·τ/2` (the tube's own response to `Δv` over `τ/2` is a tide's order smaller). At `τ = 0` it is the boundary's state.
///
/// The tube is the binding that was current at `B` (the history one back for a reader before the binding's own kick, which the
/// partial step replaces), run on past its own end. A binding that is not a clock's (a creation, a handoff, a flush) keeps the
/// tube alone. Where the step cannot be read (history pruned, a tube that ends, a kick that never fired) the tube alone is read.
fn partial(ctx: &Ctx, i: usize, t: Tick, b: &Binding) -> Res<(V2, V2)> {
    let raw = || b.cartesian(t);
    let k = b.kick;
    if !k.clock {
        return raw();
    }
    let held;
    let (base, start) = if t >= k.boundary {
        (b, k.boundary)
    } else {
        // before this binding's own kick the step that it closes was running: from `event_time − lead` on the tube before it
        if k.lead <= 0 {
            return raw();
        }
        match ctx.bodies.binding_at(i, b.event_time - 1) {
            Some(prev) => {
                held = prev;
                (&held, b.event_time - k.lead)
            }
            None => return raw(),
        }
    };
    let tau = t - start;
    if tau <= 0 || tau > 2 * k.len.max(1) {
        return base.cartesian(t).or_else(|_| raw());
    }
    let step = || -> Res<(V2, V2)> {
        let mid = start + tau / 2;
        let (x_mid, _) = base.cartesian(mid)?;
        let field = force::field(&ctx.secondaries(base.doll, mid, i)?, x_mid)?;
        let tau_s = time_of(tau, base.clock_exp)?;
        let dv = scale2(field.accel, tau_s)?;
        let dx = scale2(dv, tau_s.scale(-1)?)?;
        let (p, v) = base.cartesian(t)?;
        Ok((add2(p, dx)?, add2(v, dv)?))
    };
    step().or_else(|_| raw())
}

/// Body `i`'s binding at `t` and its state there, completed between kicks ([`partial`], or the ramp [`credit`]), in the units of its doll.
pub fn ramped(ctx: &Ctx, i: usize, t: Tick) -> Res<(Binding, V2, V2)> {
    let b = ctx.bodies.binding_at(i, t).ok_or(crate::num::Error::Refused("history pruned"))?;
    let (p, v) = ramped_in(ctx, i, t, &b)?;
    Ok((b, p, v))
}

/// [`ramped`] for a binding already in hand (`b` is the one body `i` has at `t`).
pub fn ramped_in(ctx: &Ctx, i: usize, t: Tick, b: &Binding) -> Res<(V2, V2)> {
    if b.kick.clock {
        return partial(ctx, i, t, b);
    }
    let (p, v) = b.cartesian(t)?;
    let (dx, dv) = credit(ctx.bodies, i, t, b)?;
    Ok((add2(p, dx)?, add2(v, dv)?))
}

/// A body's position and velocity in the root frame (root length units, c = 1, so one root length
/// unit is one tick of light travel) at root tick `t`: its own state in its doll (completed by the ramp, [`credit`]),
/// scaled to root units, plus the doll centre's state, recursively up the tree. Dolls share axes (no rotation).
pub fn root_state(ctx: &Ctx, i: usize, t: Tick) -> Res<([f64; 2], [f64; 2])> {
    root_state_with(ctx, i, t, true)
}

/// [`root_state`] on the tubes alone: the state without the ramp (first order between kicks). For the scheduler's
/// deadlines and positions, which are never an outcome and are read after every event.
pub fn root_state_raw(ctx: &Ctx, i: usize, t: Tick) -> Res<([f64; 2], [f64; 2])> {
    root_state_with(ctx, i, t, false)
}

fn root_state_with(ctx: &Ctx, i: usize, t: Tick, ramp: bool) -> Res<([f64; 2], [f64; 2])> {
    let (b, p, v) = if ramp {
        ramped(ctx, i, t)?
    } else {
        let b = ctx.bodies.binding_at(i, t).ok_or(crate::num::Error::Refused("history pruned"))?;
        let (p, v) = b.cartesian(t)?;
        (b, p, v)
    };
    let k = 2f64.powi(-(ctx.dolls[b.doll as usize].shift as i32));
    let mut pos = [to_f64(p[0]) * k, to_f64(p[1]) * k];
    let mut vel = [to_f64(v[0]), to_f64(v[1])];
    if let Some(c) = ctx.dolls[b.doll as usize].centre {
        let (cp, cv) = root_state_with(ctx, c, t, ramp)?;
        pos = [pos[0] + cp[0], pos[1] + cp[1]];
        vel = [vel[0] + cv[0], vel[1] + cv[1]];
    }
    Ok((pos, vel))
}

/// The chain of (doll, state in that doll) from the body up to the root, for the clock rate.
pub fn chain(ctx: &Ctx, i: usize, t: Tick) -> Res<Vec<(u16, [f64; 2], [f64; 2])>> {
    let (b, p, v) = ramped(ctx, i, t)?;
    let mut out = vec![(b.doll, [to_f64(p[0]), to_f64(p[1])], [to_f64(v[0]), to_f64(v[1])])];
    if let Some(c) = ctx.dolls[b.doll as usize].centre {
        out.extend(chain(ctx, c, t)?);
    }
    Ok(out)
}

/// The rate of a body's clock against the root's, `dτ/dt`, derived from the doll clocks: the
/// product, up the chain, of each tube's own rate in its doll, `√(f − v_r²/f − v_t²)` with
/// `f = 1 − 2μ/r` (the Schwarzschild lapse in the doll's units, `μ` the centre's mass in them), corrected for the velocity
/// composition between a doll and its centre (`1 + v_centre·v_rel`). Nothing is stored or evolved.
pub fn clock_rate(ctx: &Ctx, i: usize, t: Tick) -> Res<f64> {
    Ok(rates_of(ctx, &chain(ctx, i, t)?).0)
}

/// `(the rate against the root's clock, the rate in the body's own doll)` along a chain: the second is the first
/// level's `√(f − v_r²/f − v_t²)` alone, the body's clock against its doll's far time.
fn rates_of(ctx: &Ctx, ch: &[(u16, [f64; 2], [f64; 2])]) -> (f64, f64) {
    let (mut rate, mut own) = (1.0, 1.0);
    for (k, (d, p, v)) in ch.iter().enumerate() {
        let r = (p[0] * p[0] + p[1] * p[1]).sqrt();
        let f = 1.0 - 2.0 * ctx.dolls[*d as usize].mu_f64() / r;
        let vr = (p[0] * v[0] + p[1] * v[1]) / r;
        let vt = (p[0] * v[1] - p[1] * v[0]) / r;
        rate *= (f - vr * vr / f - vt * vt).max(1e-300).sqrt();
        if k == 0 {
            own = rate;
        }
        if let Some((_, _, vc)) = ch.get(k + 1) {
            // the doll's centre moves at `vc` in the parent: composing velocities (1 + vc·v).
            rate /= 1.0 + vc[0] * v[0] + vc[1] * v[1];
        }
    }
    (rate, own)
}

/// The player's own readings, with the burn owed since the last flush (`dv`, in the doll's units: the view shows what a
/// flush at `t` would write): the clock's rate against the root's (`dτ/dt` in the star's frame), its rate in its own
/// doll (`dτ/dt` in the doll's frame), and its velocity relative to the doll's centre (`c = 1`; the star's doll's
/// centre is the star, at rest).
pub struct Clocks {
    pub root: f64,
    pub doll: f64,
    pub doll_velocity: [f64; 2],
}

pub fn clocks_with(ctx: &Ctx, i: usize, t: Tick, dv: [f64; 2]) -> Res<Clocks> {
    let mut ch = chain(ctx, i, t)?;
    ch[0].2 = [ch[0].2[0] + dv[0], ch[0].2[1] + dv[1]];
    let (root, doll) = rates_of(ctx, &ch);
    Ok(Clocks { root, doll, doll_velocity: ch[0].2 })
}

/// A body's position and velocity in the root frame and the rate of its clock against the root's, all
/// at root tick `t`, in one walk up the doll chain: [`root_state`] and [`clock_rate`] share every readout
/// (the view reads both for each emitter, at the emitter's retarded time).
pub fn state_rate(ctx: &Ctx, i: usize, t: Tick) -> Res<([f64; 2], [f64; 2], f64)> {
    let (mut pos, mut vel, mut rate) = ([0.0f64; 2], [0.0f64; 2], 1.0f64);
    let (mut cur, mut below) = (i, None::<[f64; 2]>);
    loop {
        let (b, p, v) = ramped(ctx, cur, t)?;
        let (p, v) = ([to_f64(p[0]), to_f64(p[1])], [to_f64(v[0]), to_f64(v[1])]);
        let doll = &ctx.dolls[b.doll as usize];
        let k = 2f64.powi(-(doll.shift as i32));
        pos = [pos[0] + p[0] * k, pos[1] + p[1] * k];
        vel = [vel[0] + v[0], vel[1] + v[1]];
        // This level's own rate (see `clock_rate`), then the velocity composition with the level below.
        let r = (p[0] * p[0] + p[1] * p[1]).sqrt();
        let f = 1.0 - 2.0 * doll.mu_f64() / r;
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
    let (heading, v2) = thrust::owed(ctx.cfg, th, dtau, x, v, ctx.dolls[rec.b.doll as usize].unit.mu)?;
    Ok(Some((heading, [to_f64(v2[0]) - to_f64(v[0]), to_f64(v2[1]) - to_f64(v[1])])))
}
