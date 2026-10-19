//! The view: physics, not visuals. A debug view of what arrives at the player's past light cone,
//! gathered across dolls. Observation is a pure function of the state: this module takes `&Universe`
//! and cannot write (the test `observation_never_changes_the_digest` holds it to that).
//!
//! For each emitter the emission event is where its worldline crosses the observer's past light
//! cone: the last tick `t_e` with `t_e + |x(t_e) − X| ≤ T` (c = 1; a root length unit is a tick of
//! light). Positions come from the tubes' readouts at the retarded time through the bodies' histories,
//! up the doll chain to the root frame. Each tube crosses the cone once, and Newton's method finds the
//! crossing starting from the previous frame's ([`ViewCache`], a memo owned by the caller: the crossing
//! is a function of the state alone, so a cold start, a warm one and a stale one find the same tick). The colour is `−p·u`: the photon's momentum carried between the emitter's and the
//! observer's four-velocities, `ν_obs/ν_em = [(1 − n·β_obs)/rate_obs] / [(1 − n·β_em)/rate_em]`
//! with each `rate = dτ/dt` derived from the doll clocks (the potential and speed at each level of
//! the chain), so gravitational redshift, Doppler shift and time dilation arrive as one number.
//! The direction in the observer's frame is the aberrated one. Light is straight in the root frame
//! (no lensing yet).
use crate::body::Kind;
use crate::num::{to_f64, Tick};
use crate::observe::{clock_rate, clocks_with, root_state, state_rate};
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

#[derive(Clone, Debug, PartialEq)]
pub struct Seen {
    pub id: usize,
    pub name: String,
    /// 0 star, 1 planet, 2 moon, 3 ship, 4 fleet member.
    pub kind: u8,
    /// Direction toward the emitter in the observer's frame (the heading axis is the page's).
    pub direction: [f64; 2],
    /// Light travel time in seconds, in the root frame.
    pub light_seconds: f64,
    /// Where the emitter was when the light left, relative to the observer, in the root frame (the page's map).
    pub offset: [f64; 2],
    /// The rate the star's frame sees the distance between them shrink (`c = 1`, positive: closing), the emitter's
    /// velocity at the emission against the observer's now.
    pub closing: f64,
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

/// An impact course: the player's tube dips below the surface of the body whose doll it is in, so unless something
/// changes the orbit (a burn rebinds it) the ship hits it. Derived from the tube when looked at, the same certificate the
/// engine plans its [`crate::body::What::Crash`] from; it is there from the moment the periapsis is under the surface (the
/// plan holds the item only once the step reaches it) and gone when the orbit no longer crosses one.
#[derive(Clone, Debug, PartialEq)]
pub struct Impact {
    /// What: the body whose surface (the name of its doll: "star", "Home").
    pub body: &'static str,
    /// When: the tick of the first contact (the root clock) and the game seconds from the presented tick to it.
    pub tick: Tick,
    pub seconds: f64,
    /// Where: the unit vector from the body's centre to the point of contact, in the doll's axes.
    pub at: [f64; 2],
    /// The speed against the body there (`c = 1`).
    pub speed: f64,
}

impl Impact {
    /// The page's words: "Home's surface in 3 min 12 s".
    pub fn sentence(&self) -> String {
        let body = if self.body == "star" { "the star".to_string() } else { self.body.to_string() };
        format!("{body}'s surface in {}", clock_text(self.seconds))
    }
}

#[derive(Clone, Debug, PartialEq)]
pub struct View {
    pub tick: Tick,
    pub coordinate_seconds: f64,
    pub proper_seconds: f64,
    /// The observer's clock rate against the root's (`dτ/dt`, the star's frame).
    pub rate: f64,
    pub beta: [f64; 2],
    /// The same two readings in the frame of the doll the observer is in: its clock against the doll's far time, and its
    /// velocity relative to the doll's centre (in the star's own doll they equal `rate` and `beta`).
    pub doll_rate: f64,
    pub doll_beta: [f64; 2],
    /// The throttle level held and whether a burn key is down (the engine's state, not the page's wish).
    pub level: u8,
    pub burning: bool,
    /// False for a wreck (crashed, left the system, or refused by the engine): its position and readings (β, rates, proper
    /// time) are frozen at its last state, and `loss` says why.
    pub alive: bool,
    pub loss: Option<String>,
    /// The keys the engine holds (bits 0-3: forward, reverse, left, right).
    pub keys: u8,
    /// Refusals the player's body has met (a nonzero count means the engine could not take a kick: the state is frozen).
    pub refusals: u64,
    pub position_light_seconds: [f64; 2],
    pub heading: [f64; 2],
    pub doll: &'static str,
    /// The impact the course holds, if it holds one (a live ship only).
    pub impact: Option<Impact>,
    pub seen: Vec<Seen>,
}

/// What the view remembers about an emitter between frames: where its worldline crossed the observer's
/// past light cone last time. Only a guess for Newton's method; it never decides the result.
#[derive(Clone, Copy, Debug)]
struct Crossing {
    observed: Tick,
    /// The root of `g` as a real number (the tick it floors to is the crossing): what the next guess extrapolates.
    root: f64,
    /// The `d t_e / d T` the next guess extrapolates with: the rate the last two frames measured, corrected by how
    /// it was changing (`2·inst − measured`: the instantaneous rate at this crossing against its average over the
    /// interval before), or the instantaneous rate on a first sight.
    slope: f64,
}

/// The view's per-emitter memo (by body id). Create one per observer and pass it to
/// [`gather_cached`] every frame; any cache, however stale or foreign, gives the same view.
#[derive(Clone, Debug, Default)]
pub struct ViewCache {
    slots: Vec<Option<Crossing>>,
    /// Readouts spent finding crossings, in the last gather (a measure, not a result).
    pub readouts: u64,
}

impl ViewCache {
    fn guess(&self, i: usize, t_now: Tick) -> Option<Tick> {
        let c = self.slots.get(i).copied().flatten().filter(|c| c.observed <= t_now)?;
        Some((c.root + (t_now - c.observed) as f64 * c.slope).floor() as Tick)
    }
    /// Remember the crossing `root` found at `t_now`, with `inst`, the arrival rate at the crossing itself:
    /// `(1 + n·β_obs)/(1 + n·β_em)`.
    fn put(&mut self, i: usize, t_now: Tick, root: f64, inst: f64) {
        if self.slots.len() <= i {
            self.slots.resize(i + 1, None);
        }
        let inst = inst.clamp(1e-3, 1e4);
        let slope = match self.slots[i] {
            // The arrival rate `dt_e/dT = (1 + n·β_obs)/(1 + n·β_em)` is anywhere in `(0, ∞)`: an emitter closing on the
            // observer at 0.9c is seen advancing ten ticks per tick of the observer's present, and at 0.9999c ten
            // thousand. The clamp only keeps a noisy measurement from sending the guess to the moon; it is no
            // physics (a clamp at 1.5 was the Newtonian one: lab run 20261003-2306-redteam-4570).
            Some(c) if t_now > c.observed => {
                let avg = ((root - c.root) / (t_now - c.observed) as f64).clamp(1e-3, 1e4);
                (2.0 * inst - avg).clamp(1e-3, 1e4)
            }
            _ => inst,
        };
        self.slots[i] = Some(Crossing { observed: t_now, root, slope });
    }
}

/// An emitter's state at one tick: position and velocity in the root frame and its clock rate.
struct At {
    x: [f64; 2],
    v: [f64; 2],
    rate: f64,
}

/// The crossing of an emitter's worldline with the past light cone of the event `(t_now, xo)`: the last
/// integer tick `t` with `t + |x(t) − xo| ≤ t_now`. `g(t) = t + |x(t) − xo| − t_now` rises by about one per
/// tick (an emitter is slower than light), so the root is unique, and Newton's method on it, started at
/// `guess`, ends in a bracket `g(t) ≤ 0 < g(t + 1)`: the answer does not depend on where it started. A tick
/// is certainly past the root when `g(t) > −(1 + n·β)`, so a good guess costs one readout: `g` is convex along
/// the worldline (the distance to a fixed point), so `g(t + 1) ≥ g(t) + g'(t)` with `g' = 1 + n·β` the inverse of
/// the arrival rate (`n` from the observer to the emitter). That rate is the relativistic one: an emitter
/// receding at 0.9c has a window of 1.9 ticks, one closing at 0.9c a window of 0.1, and the bound `1 − speed`
/// the Newtonian reading used was 0.1 for all of them (and empty at 0.9999c whichever way they moved). Returns
/// the tick, its state and the real root (for the next frame's guess). Before the first light (`t` down to 0)
/// the state at tick 0 is returned.
fn crossing(reads: &mut u64, eval: &mut dyn FnMut(Tick) -> Option<At>, t_now: Tick, xo: [f64; 2], guess: Tick) -> Option<(Tick, At, f64)> {
    let mut t = guess.clamp(0, t_now);
    let (mut lo, mut hi): (Option<(Tick, At, f64)>, Option<Tick>) = (None, None);
    for _ in 0..64 {
        *reads += 1;
        let at = eval(t)?;
        let d = [at.x[0] - xo[0], at.x[1] - xo[1]];
        let dist = dot(d, d).sqrt();
        // The light-travel difference is exact (small integers), where `t` and `t_now` alone would cancel
        // their last bits at a late tick.
        let g = (t - t_now) as f64 + dist;
        let rate = 1.0 + if dist > 0.0 { dot(d, at.v) / dist } else { 0.0 };
        let step = -g / rate;
        if g > 0.0 && t == 0 {
            return Some((0, at, 0.0));
        }
        if g <= 0.0 {
            if g > -(rate - 1e-4) || hi == Some(t + 1) {
                return Some((t, at, t as f64 + step));
            }
            lo = Some((t, at, t as f64 + step));
        } else {
            hi = Some(t);
            if lo.as_ref().is_some_and(|l| l.0 + 1 == t) {
                return lo;
            }
        }
        let mut next = (t as f64 + step).floor() as Tick;
        if let Some((l, ..)) = &lo {
            next = next.max(*l);
        }
        if let Some(h) = hi {
            next = next.min(h - 1);
        }
        if next == t {
            next = if g <= 0.0 { t + 1 } else { t - 1 };
        }
        t = next.clamp(0, t_now);
    }
    None
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

/// Gather everything that arrives at the player's present tick, every crossing found from scratch.
pub fn gather(u: &Universe, names: &[String]) -> Option<View> {
    gather_with(u, names, None)
}

/// [`gather`], each emitter's crossing started from the one `cache` holds from the last frame (and
/// updated): the same view, in about one readout per emitter instead of two or three.
pub fn gather_cached(u: &Universe, names: &[String], cache: &mut ViewCache) -> Option<View> {
    gather_with(u, names, Some(cache))
}

fn gather_with(u: &Universe, names: &[String], mut cache: Option<&mut ViewCache>) -> Option<View> {
    let ctx = u.ctx();
    if let Some(c) = cache.as_mut() {
        c.readouts = 0;
    }
    let p = u.player()?;
    let t_now = u.now;
    let rec = u.rec(p);
    // A lost player (a wreck) stays where it was lost, its readings frozen at its last state: the universe goes on.
    // A ship the engine could not carry on (refused kicks, possibly still "alive") is read at its last state when its tube or
    // partial step cannot be read at the presented tick (the motion law v2 refuses a read far past its last boundary).
    // A wreck is read where it was lost: at its impact when its last tube held one (the surface, not the tube's start).
    let mut t_read = if rec.alive {
        t_now
    } else {
        let doll = &u.dolls[rec.b.doll as usize];
        crate::step::next_impact(&rec.b, doll.surface, rec.b.event_time).ok().flatten().unwrap_or(rec.b.event_time)
    };
    let (xo, vo) = match root_state(&ctx, p, t_read) {
        Ok(x) => x,
        Err(_) => {
            t_read = rec.b.event_time;
            root_state(&ctx, p, t_read).or_else(|_| crate::observe::root_state_raw(&ctx, p, t_read)).ok()?
        }
    };
    // The keys held since the last flush: the turn and the burn owed, as a flush at this tick would write them.
    let owed = if rec.alive { crate::observe::held_thrust(&ctx, &rec, t_now).ok().flatten() } else { None };
    let dv = owed.map_or([0.0, 0.0], |o| o.1);
    let vo = [vo[0] + dv[0], vo[1] + dv[1]];
    let (rate_obs, doll_rate, doll_beta) = match clocks_with(&ctx, p, t_read, dv) {
        Ok(c) => (c.root, c.doll, c.doll_velocity),
        Err(_) => (1.0, 1.0, [0.0, 0.0]),
    };
    let heading = owed.map(|o| o.0).or(rec.thrust.map(|t| t.heading)).unwrap_or(0);
    let h = heading as f64 / 4294967296.0 * std::f64::consts::TAU;
    let tau = rec.b.orbit_state(t_read.max(rec.b.event_time)).ok().map(|s| {
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
            offset: [d[0] * TICK_SECONDS, d[1] * TICK_SECONDS],
            closing: dot(toward, vo) - dot(toward, vel),
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
    // Bodies: where each tube crosses the past light cone.
    let mut reads = 0u64;
    for i in 0..u.n_bodies() {
        if i == p || !u.bodies().alive(i) {
            continue;
        }
        let kind = u.info[i].kind;
        let guess = cache.as_deref().and_then(|c| c.guess(i, t_now)).unwrap_or(t_now);
        let Some((t_e, at, root)) = crossing(&mut reads, &mut |t| state_rate(&ctx, i, t).ok().map(|(x, v, rate)| At { x, v, rate }), t_now, xo, guess) else { continue };
        if let Some(c) = cache.as_deref_mut() {
            // The arrival rate at this crossing, from the emitter's velocity and the observer's (a guess's input only).
            let d = [at.x[0] - xo[0], at.x[1] - xo[1]];
            let dist = dot(d, d).sqrt();
            let inst = if dist > 0.0 { (1.0 + dot(d, vo) / dist) / (1.0 + dot(d, at.v) / dist) } else { 1.0 };
            c.put(i, t_now, root, inst);
        }
        let doll = &u.dolls[u.bodies().doll(i) as usize];
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
        match u.info[i].from {
            // A member that left its frame is the same ship to the eye (the same id, name and colour).
            Some((fi, m)) => push(1_000_000 + fi as usize * 1000 + m as usize, "fleet", 4, at.x, at.v, at.rate, 3500., 1e-6, radius, 0.0, t_e as f64),
            None => push(i, names.get(i).map(|s| s.as_str()).unwrap_or("?"), k, at.x, at.v, at.rate, temp, lum, radius, 0.0, t_e as f64),
        }
    }
    if let Some(c) = cache.as_deref_mut() {
        c.readouts = reads;
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
            // a member handed out is a body of the doll now, seen above
            if !f.is_member(m) {
                continue;
            }
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
            let rate = rate0 * (1.0 - 2.0 * u.dolls[f.doll as usize].mu_f64() / r_doll.max(3.0)).sqrt();
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
        doll_rate,
        doll_beta,
        level: rec.thrust.map_or(0, |t| t.level),
        burning: rec.alive && rec.thrust.is_some_and(|t| t.keys & 3 != 0),
        alive: rec.alive,
        loss: (!rec.alive).then(|| loss_cause(u, &rec)),
        keys: rec.thrust.map_or(0, |t| t.keys),
        refusals: rec.refusals,
        position_light_seconds: pos,
        heading: [h.cos(), h.sin()],
        doll: rec_doll,
        impact: if rec.alive { impact_course(u, &rec, t_now) } else { None },
        seen,
    })
}

/// The impact the player's tube holds from the presented tick: [`crate::step::next_impact`] on the surface of the body whose
/// doll the ship is in, with where and how fast the ship arrives. A tube that cannot be read says nothing (no warning is
/// better than a wrong one: the engine's own refusal is shown elsewhere).
fn impact_course(u: &Universe, rec: &crate::body::BodyRec, t_now: Tick) -> Option<Impact> {
    let doll = &u.dolls[rec.b.doll as usize];
    let course = crate::step::impact_course(&u.ctx(), u.player()?, rec, t_now.max(rec.b.event_time)).ok()??;
    let tick = crate::step::next_impact(&course, doll.surface, t_now.max(course.event_time)).ok().flatten()?;
    let (x, v) = course.cartesian(tick).ok()?;
    let (x, v) = ([to_f64(x[0]), to_f64(x[1])], [to_f64(v[0]), to_f64(v[1])]);
    let r = dot(x, x).sqrt().max(1e-300);
    Some(Impact { body: doll.name, tick, seconds: (tick - t_now).max(0) as f64 * TICK_SECONDS, at: [x[0] / r, x[1] / r], speed: dot(v, v).sqrt() })
}

/// Why the player was lost, in words: the impact (on the centre of the doll it was in: the first tick its last tube is
/// below the surface, found by bisection on the tube, with the speed there against the centre), the edge of the system,
/// or the engine's own refusal. Read only when the player is already lost.
fn loss_cause(u: &Universe, rec: &crate::body::BodyRec) -> String {
    let doll = &u.dolls[rec.b.doll as usize];
    let t0 = rec.b.event_time;
    let r_at = |t: Tick| -> Option<(f64, f64)> {
        let (x, v) = rec.b.cartesian(t).ok()?;
        let (x, v) = ([to_f64(x[0]), to_f64(x[1])], [to_f64(v[0]), to_f64(v[1])]);
        Some((dot(x, x).sqrt(), dot(v, v).sqrt()))
    };
    let fmt_speed = |b: f64| if b < 0.1 { format!("{:.2} km/s", b * 299_792.458) } else { format!("{:.4} c", b) };
    // The impact the last tube held (the first tick at or after the last state that is under the surface).
    if let Ok(Some(h)) = crate::step::next_impact(&rec.b, doll.surface, t0) {
        if let Some((_, v)) = r_at(h) {
            let body = if rec.b.doll == 0 { "the star" } else { doll.name };
            return format!("hit {body} at {} (relative to {body}), at world time {}", fmt_speed(v), clock_text(h as f64 * TICK_SECONDS));
        }
    }
    if rec.b.doll == 0 {
        if let Some((r, v)) = r_at(t0) {
            let edge = 2f64.powi(u.cfg.leave_log2);
            if r > edge * 0.5 {
                return format!("left the system: past the edge, {:.1} light-days from the star (2^{} ticks of light), at {}", edge * TICK_SECONDS / 86_400.0, u.cfg.leave_log2, fmt_speed(v));
            }
        }
    }
    let what = rec.fault.as_ref().map(|f| format!("{:?}: {:?}", f.0, f.1)).unwrap_or_else(|| "no fault recorded".into());
    format!("the engine lost it: {what} ({} refusals), in {} at {}", rec.refusals, if rec.b.doll == 0 { "the star's doll" } else { doll.name }, r_at(t0).map_or("an unreadable state".to_string(), |(_, v)| fmt_speed(v)))
}

/// A duration in game seconds as the page writes it.
pub fn clock_text(s: f64) -> String {
    if s < 60.0 {
        format!("{s:.3} s")
    } else if s < 3600.0 {
        format!("{} min {:02.0} s", (s / 60.0).floor(), s % 60.0)
    } else if s < 86_400.0 {
        format!("{} h {:02} min", (s / 3600.0).floor(), ((s % 3600.0) / 60.0).floor())
    } else {
        format!("{} d {} h", (s / 86_400.0).floor(), ((s % 86_400.0) / 3600.0).floor())
    }
}
