//! The player's thrust: a decision that grows the rapidity linearly in proper time.
//!
//! `Δη = α·Δτ` along the heading, in the ship's local frame. The state is a coordinate
//! velocity in the doll (Schwarzschild coordinates), so the burn converts to the local
//! orthonormal frame (`v̂_r = v_r/f`, `v̂_t = v_t/√f`, `f = 1 − 2M/r`), composes the boost there
//! with the exact relativistic velocity addition, and converts back. Then the state is bound
//! again: the new `E` and `L` are the old ones changed by the work done, and nothing else.
use crate::body::Thrust;
use crate::ctx::Config;
use crate::num::{add2, dot2, norm2, scale2, Res, V2};
use emergent_space::orbit::Scalar;

/// Unit vector of a heading in turns (Q32): integer CORDIC (rotation mode), 24 iterations. The
/// constants are `atan(2^-i)` in turns·2^32 and the inverse gain in Q32.
pub fn direction(heading: u32) -> Res<V2> {
    const ATAN: [i64; 24] = [
        536870912, 316933406, 167458907, 85004756, 42667331, 21354465, 10679838, 5340245, 2670163, 1335087, 667544, 333772, 166886, 83443,
        41722, 20861, 10430, 5215, 2608, 1304, 652, 326, 163, 81,
    ];
    let mut z = heading as i64;
    let atan: [i128; 24] = ATAN.map(|a| a as i128);
    if z > 1 << 31 {
        z -= 1 << 32;
    }
    let mut sign = 1i128;
    let mut z = z as i128;
    if z > 1 << 30 {
        z -= 1 << 31;
        sign = -1;
    }
    if z < -(1 << 30) {
        z += 1 << 31;
        sign = -1;
    }
    let (mut x, mut y) = (2608131496i128, 0i128);
    for (i, a) in atan.iter().enumerate() {
        let d = if z >= 0 { 1 } else { -1 };
        (x, y, z) = (x - d * (y >> i), y + d * (x >> i), z - d * a);
    }
    Ok([Scalar::raw(sign * x, -32)?, Scalar::raw(sign * y, -32)?])
}

fn cosh_sinh(eta: Scalar) -> Res<(Scalar, Scalar)> {
    let e2 = eta.mul(eta)?;
    let one = Scalar::ONE;
    // cosh = 1 + η²/2 + η⁴/24 + η⁶/720;  sinh = η(1 + η²/6 + η⁴/120 + η⁶/5040)
    let c = one.add(e2.scale(-1)?)?.add(e2.mul(e2)?.div(Scalar::integer(24))?)?.add(e2.mul(e2)?.mul(e2)?.div(Scalar::integer(720))?)?;
    let sh = one
        .add(e2.div(Scalar::integer(6))?)?
        .add(e2.mul(e2)?.div(Scalar::integer(120))?)?
        .add(e2.mul(e2)?.mul(e2)?.div(Scalar::integer(5040))?)?;
    Ok((c, eta.mul(sh)?))
}

/// The coordinate velocity `v` at position `x` (doll units, `M = 1`) after a burn of rapidity
/// `eta` along the unit vector `n` (the ship's heading in the local frame).
pub fn burn(x: V2, v: V2, eta: Scalar, n: V2) -> Res<V2> {
    let r = norm2(x)?;
    let f = Scalar::ONE.sub(Scalar::integer(2).div(r)?)?;
    if !f.is_positive() {
        return Err(crate::num::Error::Refused("thrust inside the horizon"));
    }
    let rh = [x[0].div(r)?, x[1].div(r)?];
    let th = [rh[1].negate(), rh[0]];
    let sf = f.sqrt()?;
    // Local orthonormal velocity: radial v_r/f, tangential v_t/√f.
    let (vr, vt) = (dot2(v, rh)?, dot2(v, th)?);
    let w = add2(scale2(rh, vr.div(f)?)?, scale2(th, vt.div(sf)?)?)?;
    let ww = dot2(w, w)?;
    let gamma = Scalar::ONE.div(Scalar::ONE.sub(ww)?.sqrt()?)?;
    let u = scale2(w, gamma)?;
    let (ch, sh) = cosh_sinh(eta)?;
    let un = dot2(u, n)?;
    let along = add2(n, scale2(u, un.div(gamma.add(Scalar::ONE)?)?)?)?;
    let u2 = add2(scale2(u, ch)?, scale2(along, sh)?)?;
    let g2 = Scalar::ONE.add(dot2(u2, u2)?)?.sqrt()?;
    let w2 = scale2(u2, Scalar::ONE.div(g2)?)?;
    let (wr, wt) = (dot2(w2, rh)?, dot2(w2, th)?);
    add2(scale2(rh, wr.mul(f)?)?, scale2(th, wt.mul(sf)?)?)
}

/// The turn and the burn owed to a held thrust over the proper time `dtau` (root units) since its last
/// flush: the heading at the end and the velocity after the burn at the state `(x, v)` (doll units). Pure:
/// the kick that flushes the burn uses it, and so does the view, which reads the same state a flush at the
/// presented tick would write (docs/plane.md, foundation 5: observation is a pure function of the state).
/// The heading turns by `±turn·Δτ`, and the burn goes along the heading at the midpoint of the turn.
pub fn owed(cfg: &Config, th: Thrust, dtau: Scalar, x: V2, v: V2) -> Res<(u32, V2)> {
    let sign = (th.keys & 8 != 0) as i64 - (th.keys & 4 != 0) as i64;
    let dh = dtau.mul(Scalar::power_of_two(cfg.turn_log2 as i16))?.fixed(32)? as i64 * sign;
    let mid = th.heading.wrapping_add((dh / 2) as u32);
    let heading = th.heading.wrapping_add(dh as u32);
    let dir = (th.keys & 1 != 0) as i64 - (th.keys & 2 != 0) as i64;
    if dir == 0 {
        return Ok((heading, v));
    }
    let eta = dtau.mul(Scalar::power_of_two(cfg.thrust_log2 as i16))?;
    let eta = if dir > 0 { eta } else { eta.negate() };
    Ok((heading, burn(x, v, eta, direction(mid)?)?))
}
