//! The view: physics, not visuals. A debug view of what arrives at the player's past light cone,
//! gathered across dolls. Observation is a pure function of the state: this module takes `&Universe`
//! and cannot write (the test `observation_never_changes_the_digest` holds it to that).
//!
//! For each emitter the emission event is where its worldline crosses the observer's past light
//! cone: `t_e + |x(t_e) − X| = T` (c = 1; a root length unit is a tick of light). Positions come from
//! the tubes' readouts at the retarded time through the bodies' histories, up the doll chain to the
//! root frame. The colour is `−p·u`: the photon's momentum carried between the emitter's and the
//! observer's four-velocities, `ν_obs/ν_em = [(1 − n·β_obs)/rate_obs] / [(1 − n·β_em)/rate_em]`
//! with each `rate = dτ/dt` derived from the doll clocks (the potential and speed at each level of
//! the chain), so gravitational redshift, Doppler shift and time dilation arrive as one number.
//! The direction in the observer's frame is the aberrated one. Light is straight in the root frame
//! (no lensing yet).
use crate::body::Kind;
use crate::num::{to_f64, Tick};
use crate::observe::{clock_rate, root_state};
use crate::universe::Universe;
use emergent_space::orbit::Scalar;

/// Seconds in one tick (`G·M_sun/c³`, the star's `M/c`).
pub const TICK_SECONDS: f64 = 4.925_490_947e-6;

fn dot(a: [f64; 2], b: [f64; 2]) -> f64 {
    a[0] * b[0] + a[1] * b[1]
}

/// `n` points toward the emitter; Lorentz-transform the null momentum into the observer's frame:
/// the aberrated direction and the Doppler factor `γ(1 + β·n)`.
pub fn aberration(n: [f64; 2], beta: [f64; 2]) -> ([f64; 2], f64) {
    let bb = dot(beta, beta);
    let g = 1. / (1. - bb).sqrt();
    let bn = dot(beta, n);
    let d = g * (1. + bn);
    let w = if bb == 0. { 1. } else { g + (g - 1.) * bn / bb };
    (std::array::from_fn(|i| (n[i] + w * beta[i]) / d), d)
}

/// Rest-frame blackbody sampled at three wavelengths, as a colour (a palette, not a spectrum).
pub fn blackbody(temperature: f64) -> [f64; 3] {
    let t = temperature.clamp(100., 1e7);
    let samples = [700e-9_f64, 546e-9, 435e-9].map(|w| 1. / (w.powi(5) * (0.01438776877 / (w * t)).exp_m1()));
    let max = samples.into_iter().fold(0., f64::max);
    samples.map(|s| (s / max).powf(1. / 2.2))
}

#[derive(Clone, Debug)]
pub struct Seen {
    pub id: usize,
    pub name: String,
    /// 0 star, 1 planet, 2 moon, 3 ship, 4 fleet member.
    pub kind: u8,
    /// Direction toward the emitter in the observer's frame (the heading axis is the page's).
    pub direction: [f64; 2],
    /// Light travel time in seconds, in the root frame.
    pub light_seconds: f64,
    pub color: [f64; 3],
    pub luminosity: f64,
    /// `ν_obs/ν_em` from `−p·u`: Doppler, aberration and gravitational redshift together.
    pub shift: f64,
    /// How long ago the light left, in seconds of root time.
    pub age: f64,
    /// How stale the retarded state is (battle members only), in ticks.
    pub lag: f64,
    pub angular_radius: f64,
}

#[derive(Clone, Debug)]
pub struct View {
    pub tick: Tick,
    pub coordinate_seconds: f64,
    pub proper_seconds: f64,
    /// The observer's clock rate against the root's (`dτ/dt`).
    pub rate: f64,
    pub beta: [f64; 2],
    pub position_light_seconds: [f64; 2],
    pub heading: [f64; 2],
    pub doll: &'static str,
    pub seen: Vec<Seen>,
}

fn rest(kind: Kind, id: usize, doll_name: &str) -> (f64, f64) {
    // (temperature, luminosity): painted for now; the emergent version is starlight scattered.
    match kind {
        Kind::Planet => (if doll_name == "Cinder" { 700. } else if doll_name == "Giant" { 130. } else { 280. }, 1e-4),
        Kind::Moon => (220., 2e-5),
        Kind::Ship => (3000. + (id as f64 * 97.0) % 1500., 1e-6),
        Kind::Player => (3000., 0.),
    }
}

/// Gather everything that arrives at the player's present tick.
pub fn gather(u: &Universe, names: &[String]) -> Option<View> {
    let ctx = u.ctx();
    let p = u.player()?;
    let t_now = u.now;
    let (xo, vo) = root_state(&ctx, p, t_now).ok()?;
    let rate_obs = clock_rate(&ctx, p, t_now).ok()?;
    let rec = u.rec(p);
    let heading = rec.thrust.map(|t| t.heading).unwrap_or(0);
    let h = heading as f64 / 4294967296.0 * std::f64::consts::TAU;
    let tau = rec.b.orbit_state(t_now).ok().map(|s| {
        let doll = &u.dolls[rec.b.doll as usize];
        let along = s.proper_time.sub(rec.b.orbit_state(rec.b.event_time).ok()?.proper_time).ok()?;
        Some(to_f64(rec.proper) + to_f64(along) * 2f64.powi(-(doll.shift as i32)))
    });
    let proper = tau.flatten().unwrap_or(0.0) * TICK_SECONDS;
    let mut seen = Vec::new();
    let mut push = |id: usize, name: &str, kind: u8, pos: [f64; 2], vel: [f64; 2], rate: f64, temp: f64, lum: f64, radius_root: f64, lag: f64, t_e: f64| {
        let d = [pos[0] - xo[0], pos[1] - xo[1]];
        let dist = dot(d, d).sqrt().max(1e-9);
        let toward = [d[0] / dist, d[1] / dist];
        // n_prop: from emitter to observer is −toward.
        let n_prop = [-toward[0], -toward[1]];
        let shift = ((1. - dot(n_prop, vo)) / rate_obs) / ((1. - dot(n_prop, vel)) / rate);
        let (dir, _) = aberration(toward, vo);
        seen.push(Seen {
            id,
            name: name.to_string(),
            kind,
            direction: dir,
            light_seconds: dist * TICK_SECONDS,
            color: blackbody(temp * shift),
            luminosity: lum * shift.powi(4),
            shift,
            age: (t_now as f64 - t_e) * TICK_SECONDS,
            lag,
            angular_radius: (radius_root / dist).atan(),
        });
    };
    // The star.
    {
        let rate = (1.0f64 - 2.0 / crate::scenario::STAR_RADIUS as f64).sqrt();
        push(usize::MAX, "star", 0, [0.0, 0.0], [0.0, 0.0], rate, 5772., 1.0, crate::scenario::STAR_RADIUS as f64, 0.0, t_now as f64 - 0.0);
    }
    // Bodies: the retarded fixed point t = T − |x(t) − X|.
    for i in 0..u.n_bodies() {
        if i == p || !u.bodies().alive(i) {
            continue;
        }
        let kind = u.info[i].kind;
        let mut t = t_now as f64;
        let mut got = None;
        for _ in 0..6 {
            let Ok((x, v)) = root_state(&ctx, i, (t as Tick).max(0)) else { break };
            let d = [x[0] - xo[0], x[1] - xo[1]];
            let next = (t_now as f64 - dot(d, d).sqrt()).max(0.0);
            got = Some((x, v));
            if (next - t).abs() < 1.0 {
                t = next;
                break;
            }
            t = next;
        }
        let Some((x, v)) = got else { continue };
        let Ok(rate) = clock_rate(&ctx, i, (t as Tick).max(0)) else { continue };
        let doll = &u.dolls[u.rec(i).b.doll as usize];
        let host_name = match kind {
            Kind::Planet => u.dolls.iter().find(|d| d.centre == Some(i)).map(|d| d.name).unwrap_or("planet"),
            _ => doll.name,
        };
        let (temp, lum) = rest(kind, i, host_name);
        let radius = to_f64(u.info[i].radius) * 2f64.powi(-(doll.shift as i32));
        let radius = if kind == Kind::Planet { u.dolls.iter().find(|d| d.centre == Some(i)).map(|d| to_f64(d.surface) * 2f64.powi(-(d.shift as i32))).unwrap_or(radius) } else { radius };
        let k = match kind {
            Kind::Planet => 1,
            Kind::Moon => 2,
            _ => 3,
        };
        push(i, names.get(i).map(|s| s.as_str()).unwrap_or("?"), k, x, v, rate, temp, lum, radius, 0.0, t);
    }
    // Fleets: the battle's committed tick follows the retarded time of its light, so its members
    // are read where the stepper is, extrapolated along their own velocity to the retarded tick.
    let mut motions = Vec::new();
    for (fi, f) in u.fleets.iter().enumerate() {
        let tc = f.tick();
        let (Some((o, ov)), Ok((cp, cv))) = (f.origin(tc), root_state(&ctx, f.centre, tc.max(u.bodies().event_time(f.centre)).min(t_now))) else { continue };
        let k = 2f64.powi(-20);
        let q = crate::fleet::Q as f64;
        let origin = [cp[0] + o[0] * k, cp[1] + o[1] * k];
        let rate0 = clock_rate(&ctx, f.centre, tc.max(0).min(t_now)).unwrap_or(1.0);
        motions.clear();
        f.motions(&mut motions);
        let shift = u.dolls[f.doll as usize].shift as i32;
        for (m, mo) in motions.iter().enumerate() {
            let x = [origin[0] + mo.x[0] as f64 * k, origin[1] + mo.x[1] as f64 * k];
            let v = [cv[0] + ov[0] / q + mo.k[0] as f64 / q, cv[1] + ov[1] / q + mo.k[1] as f64 / q];
            let d = [x[0] - xo[0], x[1] - xo[1]];
            let dist = dot(d, d).sqrt();
            let want = t_now as f64 - dist;
            let dt = want - tc as f64;
            let xe = [x[0] + v[0] * dt, x[1] + v[1] * dt];
            // The planet's own clock, times the planet's potential at the member's radius.
            let rel = [origin[0] - cp[0] + mo.x[0] as f64 * k, origin[1] - cp[1] + mo.x[1] as f64 * k];
            let r_doll = dot(rel, rel).sqrt() * 2f64.powi(shift);
            let rate = rate0 * (1.0 - 2.0 / r_doll.max(3.0)).sqrt();
            let rad = f.radii.get(m).copied().unwrap_or(0) as f64 * k;
            push(1_000_000 + fi * 1000 + m, "fleet", 4, xe, v, rate, 3500., 1e-6, rad, dt.abs(), want);
        }
    }
    let rec_doll = u.dolls[rec.b.doll as usize].name;
    let pos = [xo[0] * TICK_SECONDS, xo[1] * TICK_SECONDS];
    let _ = Scalar::ZERO;
    Some(View {
        tick: t_now,
        coordinate_seconds: t_now as f64 * TICK_SECONDS,
        proper_seconds: proper,
        rate: rate_obs,
        beta: vo,
        position_light_seconds: pos,
        heading: [h.cos(), h.sin()],
        doll: rec_doll,
        seen,
    })
}
