//! Small-excursion oscillator centred on the stable radius selected by L.
//! The dimensionless selection is amplitude/centre <= 1/32; no eccentricity
//! supplied by the caller is retained. Unresolved energy-floor cells use the
//! circular/epicyclic limit. This changes the law, not just its evaluator.
use super::*;
const ONE64: u128 = 1 << 64;
pub const TAU_Q30: u64 = 6_746_518_852;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct LocalOscillator {
    pub center: Words,
    pub amplitude: Words,
    pub omega: Words,
}
fn potential(key: Key, u: i128) -> Result<u128> {
    let u2 = (u as u128 * u as u128) >> 32;
    let l = key.angular.get() as u128;
    let lu2 = l
        .checked_mul(l)
        .and_then(|x| x.checked_mul(u2))
        .ok_or(Error::Range)?
        >> 64;
    (ONE64 - ((u as u128) << 17))
        .checked_mul(ONE64 + lu2)
        .map(|v| v >> 64)
        .ok_or(Error::Range)
}
pub(super) fn compile_local(key: Key) -> Result<Option<Cycle>> {
    let inv = key.inverse_l2();
    if 12 * inv >= Q48 || key.energy.get() >= Q48 as u64 {
        return Ok(None);
    }
    let root = sqrt(((Q48 - 12 * inv) * Q48) as u128) as i128;
    let center = (Q48 - root) / 6;
    let energy = key.energy.get() as u128;
    let e2 = (energy * energy) >> 32;
    let minimum = potential(key, center)?;
    // E is a floored Q48 input: its original value is in [E,E+1 quantum).
    // L was floored too, which lowers the stable circular energy. Eight Q64
    // units additionally enclose arithmetic in potential and the centre root.
    let floor_width = (2 * energy >> 32) + 8;
    if e2 + floor_width < minimum {
        return Err(Error::NoBoundOrbit);
    }
    let max_u = center + center / 32;
    if potential(key, max_u)? < e2 {
        return Ok(None);
    }
    let mut lo = center;
    let mut hi = max_u;
    if e2 <= minimum {
        hi = center;
    }
    while hi - lo > 1 {
        let mid = (lo + hi) / 2;
        if potential(key, mid)? < e2 {
            lo = mid;
        } else {
            hi = mid;
        }
    }
    let amplitude = (lo + hi) / 2 - center;
    let w2 = Q48 - 6 * center;
    let omega = sqrt((w2 * Q48) as u128) as i128;
    let phi = u64c(rnd(TAU_Q30 as i128 * Q48, omega))?;
    let radial = sqrt((center * center - amplitude * amplitude) as u128) as i128;
    let lapse =
        sqrt(((Q48 - 2 * center) * (Q48 - 2 * center) - 4 * amplitude * amplitude) as u128) as i128;
    let l = key.angular.get() as i128;
    let tau_mean = rnd(
        rnd(1i128 << 68, (l * (radial * radial / Q48)) >> 32) * center,
        radial,
    );
    let first = rnd(1i128 << 68, (l * radial) >> 32);
    let last = rnd(1i128 << 68, (l * lapse) >> 32);
    let t_mean = rnd(
        (tau_mean + 2 * first + 4 * last) * key.energy.get() as i128,
        Q48,
    );
    let increments = Increments {
        phi: Words::new(phi),
        t: Words::new(u64c(rnd(t_mean * phi as i128, 1 << 30))?),
        tau: Words::new(u64c(rnd(tau_mean * phi as i128, 1 << 30))?),
    };
    let start = State::from_q48(center + amplitude, 0)?;
    let apo = State::from_q48(center - amplitude, 0)?;
    let band = band_index(start)?;
    Ok(Some(Cycle {
        key,
        start,
        end: start,
        start_band: band,
        end_band: band,
        apo,
        increments,
        crossings: vec![],
        steps: 0,
        local: Some(LocalOscillator {
            center: Words::new(center as u64),
            amplitude: Words::new(amplitude as u64),
            omega: Words::new(omega as u64),
        }),
    }))
}
