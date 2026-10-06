//! The plane itself as a law: `behave --law plane` answers the restricted problem with the shipped
//! plane (crates/universe), through its public API only, so the frozen gates B12-B14 and B17 judge
//! the engine the game flies, not the `space` crate's dense stepper. The scene is the judge's (a
//! star and a planet of mass ratio μ on a circle, in units of their total mass); the plane's root
//! unit is the star's mass, so every length and time crosses as `/(1 − μ)` and velocities (β,
//! c = 1) cross unchanged. Floats appear only at this boundary; everything inside is the plane's
//! integer law. The star's surface is the shipped plane's (STAR_RADIUS) at the plane's own scale,
//! scaled down with a scene shrunk below one AU (B17's miniature, sep = 100: the judge's star is a
//! point, and a surface that could swallow the whole system would decide an outcome nobody asked
//! for). The kick cadence is `Config::step_log2` (`--plane-step`): a power of two of ticks near
//! 2^step_log2 kicks per radial period of each tube. With `PLANE_TRACE` set, every answer leaves
//! one line on stderr: the event counts of the run that produced it, or where a ship the law lost
//! was lost (a law that kills a ship the judge keeps is a finding, not a gap in the adapter).
use super::restricted::Restricted;
use super::Law;
use emergent_space::orbit::Scalar;
use emergent_universe::num::{from_f64, to_f64};
use emergent_universe::observe;
use emergent_universe::scenario::{AU, STAR_RADIUS};
use emergent_universe::world::Mass;
use emergent_universe::{Config, Kind, OrbitSpec, Universe};

pub struct Plane {
    pub step_log2: i32,
}

impl Plane {
    /// From the CLI's `--plane-step`, the plane's own default when absent.
    pub fn new(step_log2: Option<i32>) -> Self {
        Self { step_log2: step_log2.unwrap_or(Config::default().step_log2) }
    }

    /// The star's surface in root units: the shipped plane's at its own scale, scaled down with a
    /// scene whose planet orbits within one AU of its star.
    fn star_surface(scene: &Restricted, to_root: f64) -> Scalar {
        from_f64(STAR_RADIUS as f64 * (scene.sep * to_root / AU as f64).min(1.0))
    }
}

/// The judge's scene as a universe: a star, a planet of mass ratio μ on a circle, and the ship at its exact start. The
/// planet's mass is `q = μ/(1 − μ)` of the star's, every length and time crosses as `/(1 − μ)` (see the module docs).
/// Returns the universe (started) and the ship's body id.
pub(crate) fn build_scene(scene: &Restricted, ship: [f64; 4], step_log2: i32) -> Option<(Universe, usize)> {
    let mu = scene.mu;
    let to_root = 1.0 / (1.0 - mu);
    let mass = Mass::of(from_f64(mu / (1.0 - mu))).ok()?;
    let cfg = Config { step_log2, ..Config::default() };
    let mut u = Universe::new(Plane::star_surface(scene, to_root), cfg);
    u.threads = 1;
    // The planet: a circular tube of the judge's separation about the star (the Kepler
    // problem of the pair's total mass, as the plane compiles it), at (sep, 0), ccw.
    let planet = u
        .add_body(
            Kind::Planet,
            OrbitSpec { doll: 0, periapsis: from_f64(scene.sep * to_root), e_q48: 0, clockwise: false, angle: 0, phase: 0 },
            Scalar::ZERO,
        )
        .ok()?;
    // The doll's surface is the planet's radius in the doll's units (root × 2^−octave).
    let surface = from_f64(scene.planet_radius * to_root).scale(-mass.octave).ok()?;
    u.add_doll("planet", planet, mass, surface).ok()?;
    // The ship: an exact heliocentric start (the star's own barycentric state at t = 0).
    let (sp, sv) = scene.star(0.0);
    let id = u
        .add_body_state(
            Kind::Ship,
            0,
            [from_f64((ship[0] - sp[0]) * to_root), from_f64((ship[1] - sp[1]) * to_root)],
            [from_f64(ship[2] - sv[0]), from_f64(ship[3] - sv[1])],
            Scalar::ZERO,
        )
        .ok()?;
    u.start().ok()?;
    Some((u, id))
}

// The single-mass questions the plane does not answer through this boundary: it says so, which
// fails those gates honestly (`space` answers them through the crates the plane shares).
impl Law for Plane {
    fn advance_per_cycle(&self, _: f64, _: f64) -> Option<(f64, f64, f64)> {
        None
    }
    fn deflection(&self, _: f64) -> Option<f64> {
        None
    }
    fn captured(&self, _: f64, _: f64) -> bool {
        false
    }
    fn photon_captured(&self, _: f64) -> bool {
        false
    }
    fn long_run(&self, _: f64, _: f64, _: usize) -> Vec<(f64, f64, f64, f64)> {
        Vec::new()
    }

    fn restricted(&self, scene: &Restricted, ship: [f64; 4], times: &[f64]) -> Option<Vec<[f64; 4]>> {
        if !(0.0..0.5).contains(&scene.mu)
            || !scene.sep.is_finite()
            || scene.sep <= 0.0
            || ship.iter().chain(times.iter()).any(|x| !x.is_finite())
            || times.iter().any(|&t| t < 0.0)
            || times.windows(2).any(|w| w[0] > w[1])
        {
            return None;
        }
        // Judge units (M_total = 1) → root units (M_star = 1): lengths and times × 1/(1 − μ).
        let mu = scene.mu;
        let to_root = 1.0 / (1.0 - mu);
        let trace = std::env::var_os("PLANE_TRACE").is_some();
        let build = || build_scene(scene, ship, self.step_log2);
        let (mut u, id) = build().or_else(|| {
            if trace {
                eprintln!("plane_trace step_log2={} refused: the scene would not build", self.step_log2);
            }
            None
        })?;
        let mut states = Vec::with_capacity(times.len());
        for &t in times {
            let tick = (t * to_root).round() as i64;
            u.settle(tick);
            // A ship the plane lost (a surface, the system's edge, a state no tube can hold) has
            // no answer; extrapolating its last tube would invent one.
            if !u.bodies().alive(id) {
                if trace {
                    eprintln!(
                        "plane_trace step_log2={} lost at sample {} of {} (kicks={} handoffs={} refused={} lost={})",
                        self.step_log2,
                        states.len() + 1,
                        times.len(),
                        u.stats.kicks,
                        u.stats.handoffs,
                        u.stats.refused,
                        u.stats.lost
                    );
                }
                return None;
            }
            let (pos, vel) = observe::root_state(&u.ctx(), id, tick).ok()?;
            // Heliocentric root units → barycentric judge units: × (1 − μ), plus the star's own.
            let (sp, sv) = scene.star(t);

            states.push([
                pos[0] / to_root + sp[0],
                pos[1] / to_root + sp[1],
                vel[0] + sv[0],
                vel[1] + sv[1],
            ]);
        }
        if trace {
            eprintln!(
                "plane_trace step_log2={} samples={} spans={:.4} planet-periods kicks={} handoffs={} boundaries={} opens={} refused={} lost={} events={}",
                self.step_log2,
                times.len(),
                times.last().copied().unwrap_or(0.0) / scene.period(),
                u.stats.kicks,
                u.stats.handoffs,
                u.stats.boundaries,
                u.stats.opens,
                u.stats.refused,
                u.stats.lost,
                u.stats.events(),
            );
        }
        let _ = to_f64; // observation only; never an outcome
        Some(states)
    }
}

#[cfg(test)]
mod tests {
    use super::super::restricted::{self, JUPITER, RTOL};
    use super::*;

    /// A ship at 4.1 sep, far outside the planet's sphere of influence, on a circular orbit.
    fn far_ship() -> [f64; 4] {
        let scene = JUPITER;
        let r = 4.1 * scene.sep;
        let v = (1.0 - scene.mu).sqrt() * r.powf(-0.5); // circular about the star's mass
        let (x, y) = (r * 0.6, r * 0.8);
        let (vx, vy) = (-v * 0.8, v * 0.6);
        let (p, w) = scene.star(0.0);
        [p[0] + x, p[1] + y, w[0] + vx, w[1] + vy]
    }

    fn times() -> Vec<f64> {
        (1..=40).map(|k| k as f64 * JUPITER.period() / 4.0).collect()
    }

    /// The worst of the law's states against the reference's, positions against `sep` and
    /// velocities against the planet's speed `sep·Ω`.
    fn worst(step: i32, truth: &[[f64; 4]]) -> f64 {
        let scene = JUPITER;
        let law = Plane { step_log2: step }.restricted(&scene, far_ship(), &times()).unwrap();
        let vscale = scene.sep * scene.omega();
        law.iter()
            .zip(truth)
            .flat_map(|(a, b)| (0..4).map(move |k| (a[k] - b[k]).abs() / if k < 2 { scene.sep } else { vscale }))
            .fold(0.0f64, f64::max)
    }

    /// The adapter is faithful at the boundary: the state it returns at t = 0 is the state it was
    /// given (the plane binds the exact integer state), through the whole unit and frame conversion.
    #[test]
    fn the_start_comes_back_through_the_conversion() {
        let ship = far_ship();
        let back = Plane { step_log2: 7 }.restricted(&JUPITER, ship, &[0.0]).unwrap();
        for (a, b) in back[0].iter().zip(ship) {
            assert!((a - b).abs() / b.abs().max(1e-30) < 1e-12, "{back:?} vs {ship:?}");
        }
    }

    /// A far ship keeps its orbit: against the judge's own reference (the planet present, float64
    /// at 1e-12), within the kicks' own error. A conversion bug errs at ~μ·sep per synodic period
    /// and grows linearly (past 1e-2·sep over this span); the cadence's own error is the 5e-4·sep
    /// measured here at 2^7, and the next test tells the two apart.
    #[test]
    fn a_far_ship_keeps_its_orbit_against_the_reference() {
        let truth = restricted::reference(&JUPITER, far_ship(), &times(), RTOL).unwrap();
        let w = worst(7, &truth);
        assert!(w < 3e-3, "worst {w:.3e}");
    }

    /// The far ship's error is the kick cadence's, not the conversion's: it falls like H² when the
    /// cadence doubles twice (a conversion bug would not move).
    #[test]
    fn a_far_ships_error_falls_like_the_cadence() {
        let truth = restricted::reference(&JUPITER, far_ship(), &times(), RTOL).unwrap();
        let (coarse, fine) = (worst(7, &truth), worst(9, &truth));
        assert!(coarse > 0.0 && fine < coarse / 8.0, "step 7: {coarse:.3e}, step 9: {fine:.3e}");
    }

    /// Not the B14 gate (its 768 reference runs cannot fit this machine's 60 s phase limit —
    /// `echo` itself times out): a probe of the same physics through the public pieces only —
    /// the gate's own first `N` circular births, one reference run each (no convergence nudge),
    /// the class from the gate's rule (beyond 1.5 R_H at any sample) and the gate's own
    /// `apsidal_rate`. `cargo test --release -p xtask moon_probe -- --ignored --nocapture`.
    #[test]
    #[ignore]
    fn moon_probe_b14_physics_not_the_gate() {
        use super::super::hill;
        let scene = JUPITER;
        let times = hill::times(&scene);
        let escape = |states: &[[f64; 4]]| times.iter().zip(states).any(|(&t, s)| scene.planet_distance(t, s) > 1.5 * scene.hill());
        for step in [7i32, 3] {
            let (mut agree, mut answered) = (0, 0);
            for (i, (a_hill, phase)) in super::super::sample::moons(12).into_iter().enumerate() {
                let ship = hill::birth(&scene, a_hill * scene.hill(), phase, 0.0, i % 2 == 0);
                let Some(truth_states) = restricted::reference(&scene, ship, &times, RTOL) else { continue };
                let truth = escape(&truth_states);
                answered += 1;
                match (Plane { step_log2: step }).restricted(&scene, ship, &times) {
                    None => println!("step {step} moon {i} a={a_hill:.3}R_H retro={}: LOST (reference {})", i % 2 == 1, if truth { "escape" } else { "bound" }),
                    Some(s) => {
                        let mine = escape(&s);
                        agree += (mine == truth) as usize;
                        let rate = |x: &[[f64; 4]]| hill::apsidal_rate(&scene, &times, x).map(|r| format!("{r:9.4}")).unwrap_or_else(|| "    none".into());
                        println!(
                            "step {step} moon {i} a={a_hill:.3}R_H retro={}: class {} (reference {}), apsidal rate law {} reference {}",
                            i % 2 == 1,
                            if mine { "escape" } else { "bound" },
                            if truth { "escape" } else { "bound" },
                            rate(&s),
                            rate(&truth_states)
                        );
                    }
                }
            }
            println!("step {step}: classes {agree}/{answered} agree");
        }
    }

    /// The tube's exact angular momentum (per unit rest mass), the geodesic's constant: `L = r·v_t/√(f − v_r²/f − v_t²)` with
    /// `f = 1 − 2M/r` (the star's `M` is 1 in the plane's root units), from the coordinate velocity.
    fn geodesic_angular_momentum(x: [Scalar; 2], v: [Scalar; 2]) -> Scalar {
        use emergent_universe::num::{cross2, dot2, norm2};
        let r = norm2(x).unwrap();
        let f = Scalar::ONE.sub(Scalar::integer(2).div(r).unwrap()).unwrap();
        let (vr, vt) = (dot2(x, v).unwrap().div(r).unwrap(), cross2(x, v).unwrap().div(r).unwrap());
        let den = f.sub(vr.mul(vr).unwrap().div(f).unwrap()).unwrap().sub(vt.mul(vt).unwrap()).unwrap();
        r.mul(vt).unwrap().div(den.sqrt().unwrap()).unwrap()
    }

    /// What one ship's run said about `J = p_t + Ω·L` (in quanta of the register, `2^pt_exp`).
    #[derive(Default, Debug)]
    struct JRun {
        kicks: usize,
        /// The largest change of `J` between consecutive kicks (the drift between them included).
        per_kick: f64,
        /// The largest change of `J` across a kick alone, and the largest of it over that kick's work `|Δp_t|`.
        across_kick: f64,
        across_kick_over_work: f64,
        /// The largest change of `J` along a drift (between a kick's output and the next kick's input).
        along_drift: f64,
        /// The mean of the last quarter of the series minus the first quarter's, and the largest `|J − J0|`.
        trend: f64,
        reach: f64,
        alive: bool,
    }

    /// Fly B12's ship `ship` for `periods` planet periods at `step`, event by event; `J` after every kick. `geodesic`: `L` of the
    /// tube's geodesic instead of `x × v`.
    fn j_run(ship: [f64; 4], step: i32, periods: f64, geodesic: bool) -> JRun {
        use emergent_universe::bind::scalars;
        use emergent_universe::num::{cross2, dot2};
        use emergent_universe::Budget;
        let scene = JUPITER;
        let t_end = (periods * scene.period() / (1.0 - scene.mu)) as i64;
        let (mut u, id) = build_scene(&scene, ship, step).unwrap();
        let planet = 0;
        let l_of = |x: [Scalar; 2], v: [Scalar; 2]| if geodesic { geodesic_angular_momentum(x, v) } else { cross2(x, v).unwrap() };
        let (mut run, mut series, mut last_kicks) = (JRun::default(), Vec::new(), 0u64);
        let (mut j0, mut prev_after) = (None::<Scalar>, None::<Scalar>);
        loop {
            let before = u.rec(id);
            if u.advance(t_end, Budget::events(1)).events == 0 || !u.bodies().alive(id) {
                break;
            }
            if u.stats.kicks == last_kicks {
                continue;
            }
            last_kicks = u.stats.kicks;
            let rec = u.rec(id);
            let Some(next_kick) = rec.plan.iter().find(|p| matches!(p.what, emergent_universe::body::What::Kick(_))) else { continue };
            let t = next_kick.t - rec.interval;
            let (pre, post) = (before.ext.expect("a ship of the root doll is stepped by the clock"), rec.ext.unwrap());
            let quantum = 2f64.powi(post.pt_exp as i32);
            let (x, v) = scalars(&rec.b.readout(t).unwrap()).unwrap();
            let (xb, vb) = scalars(&before.b.readout(t).unwrap()).unwrap();
            let (xp, vp) = scalars(&u.bodies().binding_at(planet, t).unwrap().readout(t).unwrap()).unwrap();
            let omega = cross2(xp, vp).unwrap().div(dot2(xp, xp).unwrap()).unwrap();
            let j_after = post.pt_value().unwrap().add(omega.mul(l_of(x, v)).unwrap()).unwrap();
            let j_before = pre.pt_value().unwrap().add(omega.mul(l_of(xb, vb)).unwrap()).unwrap();
            let across = to_f64(j_after.sub(j_before).unwrap()) / quantum;
            let work = (to_f64(post.pt_value().unwrap().sub(pre.pt_value().unwrap()).unwrap()) / quantum).abs();
            run.across_kick = run.across_kick.max(across.abs());
            run.across_kick_over_work = run.across_kick_over_work.max(across.abs() / work.max(1.0));
            if let Some(p) = prev_after {
                run.along_drift = run.along_drift.max((to_f64(j_before.sub(p).unwrap()) / quantum).abs());
                run.per_kick = run.per_kick.max((to_f64(j_after.sub(p).unwrap()) / quantum).abs());
            }
            prev_after = Some(j_after);
            let j0 = *j0.get_or_insert(j_after);
            series.push(to_f64(j_after.sub(j0).unwrap()) / quantum);
        }
        let q = series.len() / 4;
        let mean = |s: &[f64]| s.iter().sum::<f64>() / s.len().max(1) as f64;
        run.trend = if q > 0 { (mean(&series[series.len() - q..]) - mean(&series[..q])).abs() } else { f64::NAN };
        run.reach = series.iter().fold(0.0f64, |m, x| m.max(x.abs()));
        run.kicks = series.len();
        run.alive = u.bodies().alive(id);
        run
    }

    /// **P3 of the motion law v2** (the Opus memo, §4; frozen before the first run, kept with its failure): the energy register
    /// and the angular momentum move together. On B12's frozen ships, over 200 planet periods at 2^-6, the planet on a circle,
    /// `J = p_t + Ω·L` (`p_t` the integer register, `L = x × v` of the exact integer state after the kick, Ω the planet's own
    /// angular rate read from its exact state) is computed in the plane's integer arithmetic after every kick. Kills v2 if `|ΔJ|`
    /// between consecutive kicks exceeds 2 quanta of the register (`2^pt_exp`) on any ship, or if `J` trends (the last quarter's mean
    /// differs from the first's by more than 2 quanta).
    ///
    /// **It fails, by six orders of magnitude, and the cause is not the register** (first run, 6 October, M1 Air; the numbers below
    /// are the run's, 16 ships, 402,043 kicks, 18 s). Split in two, the change of `J` per kick is: *across the kick* at most 286
    /// quanta, and at most 1.1e-9 of the kick's own work `|Δp_t|` (about 10^11 quanta): the register and the velocity are one flow
    /// up to the law's post-Newtonian gap (`v² ≈ 2e-9`, the kick adds `Δv` to a coordinate velocity where the Hamiltonian adds
    /// `Δp` to a canonical momentum); and *along the drift* up to 5.4e6 quanta, because the drift is the compiled **geodesic** of the
    /// star, on which the Newtonian `x × v` is not constant (`r²φ̇ = (L/E)(1 − 2M/r)` varies by 1e-9 of itself). With `L` of the
    /// geodesic (the second run) the drift's part falls to 3.6e3-1.4e5 quanta (the key's Q48 fit noise, 1e-11 of `ΩL`), and the
    /// kick's part rises to 5.8e5-2e8 (`p_t` is Kepler's, `L` is not). So a probe that counts integer quanta cannot pass on a
    /// geodesic drift with a Kepler register: the memo's `H_D` ("Kepler in the weak field") and the plane's tubes are different
    /// Hamiltonians at order `v²`. Not patched (the stop rule): the finding is the integrator's.
    #[test]
    #[ignore = "probe P3 fails as frozen (6 October): J moves by up to 5.4e6 quanta per kick, 1.1e-9 of the kick's work across a kick and the rest along the geodesic drift; see the doc comment"]
    fn p3_the_energy_register_and_the_angular_momentum_move_together() {
        use super::super::handoff;
        let scene = JUPITER;
        let wall = std::time::Instant::now();
        let (mut worst_step, mut worst_trend, mut kicks, mut judged) = (0.0f64, 0.0f64, 0usize, 0);
        for (n, k) in handoff::kept().iter().filter(|k| k.closest >= scene.planet_radius).enumerate() {
            let r = j_run(k.ship, 6, 200.0, false);
            let g = j_run(k.ship, 6, 200.0, true);
            println!(
                "ship {n}: {} kicks, alive {}; L = x × v: per kick {:.3e} quanta (across the kick {:.1}, over its work {:.1e}; along the drift {:.3e}), trend {:.2e}, reach {:.2e}; L of the geodesic: per kick {:.3e} (across the kick {:.3e}, along the drift {:.3e})",
                r.kicks, r.alive, r.per_kick, r.across_kick, r.across_kick_over_work, r.along_drift, r.trend, r.reach, g.per_kick, g.across_kick, g.along_drift
            );
            (worst_step, worst_trend, kicks, judged) = (worst_step.max(r.per_kick), worst_trend.max(r.trend), kicks + r.kicks, judged + 1);
        }
        println!("{judged} ships, {kicks} kicks, {:.1} s: worst |ΔJ| per kick {worst_step:.3e} quanta, worst trend {worst_trend:.3e} quanta", wall.elapsed().as_secs_f64());
        assert!(judged >= 14);
        assert!(worst_step <= 2.0, "|ΔJ| per kick reaches {worst_step:.3e} quanta (limit 2)");
        assert!(worst_trend <= 2.0, "J trends by {worst_trend:.3e} quanta (limit 2)");
    }

    /// What does hold (measured after P3's failure, so stated as a measurement and not as a frozen gate): across a kick alone, `J`
    /// moves by at most the post-Newtonian gap, `5e-8` of the kick's own work `|Δp_t|` (measured: 1.8e-8 at worst, 7 quanta of
    /// 4e8; 16 ships over 200 periods: 286 quanta of 10^11 at worst), on four of B12's ships over 40 planet periods. The register is the work of the kick.
    #[test]
    fn across_a_kick_the_register_and_the_angular_momentum_agree_to_the_post_newtonian_gap() {
        use super::super::handoff;
        let scene = JUPITER;
        for (n, k) in handoff::kept().iter().filter(|k| k.closest >= scene.planet_radius).take(4).enumerate() {
            let r = j_run(k.ship, 6, 40.0, false);
            println!("ship {n}: {} kicks, across a kick {:.1} quanta, over its work {:.2e}", r.kicks, r.across_kick, r.across_kick_over_work);
            assert!(r.kicks > 1000 && r.across_kick_over_work <= 5e-8, "ship {n}: {r:?}");
        }
    }

    /// Diagnostic, not a gate: B13's flybys one by one (`cargo test --release -p xtask b13_by_draw -- --ignored --nocapture`, with
    /// `B13_STEP` the kick cadence): the draws that miss 1%, with what the law did on them.
    #[test]
    #[ignore]
    fn b13_by_draw() {
        use super::super::assist::{self, Flyby};
        let step: i32 = std::env::var("B13_STEP").ok().and_then(|v| v.parse().ok()).unwrap_or(8);
        let scene = JUPITER;
        let (mut taken, mut ok) = (0, 0);
        for (i, (q, v_inf, psi)) in super::super::sample::flybys(assist::DRAWS).into_iter().enumerate() {
            if taken == assist::SEEDS {
                break;
            }
            let s = assist::ship(&scene, q, v_inf, psi);
            let (flyby, closest) = assist::reference(&scene, s, RTOL);
            if closest < scene.planet_radius {
                continue;
            }
            taken += 1;
            let Flyby::Exit(t, de, dl) = flyby else { continue };
            let before = scene.heliocentric(0.0, &s);
            let (mut u, id) = build_scene(&scene, s, step).unwrap();
            let tick = (t / (1.0 - scene.mu)).round() as i64;
            u.settle(tick);
            let alive = u.bodies().alive(id);
            let (ee, el) = if alive {
                let (pos, vel) = observe::root_state(&u.ctx(), id, tick).unwrap();
                let (sp, sv) = scene.star(t);
                let st = [pos[0] * (1.0 - scene.mu) + sp[0], pos[1] * (1.0 - scene.mu) + sp[1], vel[0] + sv[0], vel[1] + sv[1]];
                let a = scene.heliocentric(t, &st);
                (((a.0 - before.0) - de).abs() / de.abs(), ((a.1 - before.1) - dl).abs() / dl.abs())
            } else {
                (f64::INFINITY, f64::INFINITY)
            };
            if ee <= 1e-2 && el <= 1e-2 {
                ok += 1;
            } else {
                println!("draw {i}: q {q:.2} R_p, v_inf {:.1} km/s: dE err {ee:.2e}, dL err {el:.2e}; alive {alive}, kicks {} refused {} lost {}, closest in the reference {:.2} R_p; fault {:?}", v_inf / 3.34e-6, u.stats.kicks, u.stats.refused, u.stats.lost, closest / scene.planet_radius, u.rec(id).fault);
            }
        }
        println!("step {step}: {ok}/{taken} within 1%");
    }

    /// Diagnostic: the first refused kicks of one B13 draw (`B13_DRAW`, `B13_STEP`), with the heliocentric state the kick refused.
    #[test]
    #[ignore]
    fn b13_refusals() {
        use super::super::assist::{self, Flyby};
        use emergent_universe::bind::scalars;
        use emergent_universe::num::{cross2, dot2, norm2};
        let step: i32 = std::env::var("B13_STEP").ok().and_then(|v| v.parse().ok()).unwrap_or(9);
        let draw: usize = std::env::var("B13_DRAW").ok().and_then(|v| v.parse().ok()).unwrap_or(5);
        let scene = JUPITER;
        let (q, v_inf, psi) = super::super::sample::flybys(assist::DRAWS)[draw];
        let s = assist::ship(&scene, q, v_inf, psi);
        let (Flyby::Exit(t, _, _), _) = assist::reference(&scene, s, RTOL) else { panic!("no exit") };
        let (mut u, id) = build_scene(&scene, s, step).unwrap();
        let tick = (t / (1.0 - scene.mu)).round() as i64;
        let mut shown = 0;
        let mut last = 0;
        loop {
            let a = u.advance(tick, emergent_universe::Budget::events(1));
            if a.events == 0 {
                break;
            }
            if u.stats.refused != last && shown < 6 {
                last = u.stats.refused;
                let rec = u.rec(id);
                let t_k = rec.b.event_time;
                let (x, v) = scalars(&rec.b.readout(rec.b.event_time).unwrap()).unwrap();
                let r = to_f64(norm2(x).unwrap());
                let (vr, vt) = (to_f64(dot2(x, v).unwrap()) / r, to_f64(cross2(x, v).unwrap()) / r);
                let e = 0.5 * (vr * vr + vt * vt) - 1.0 / r;
                let (xp, _) = scalars(&u.bodies().binding_at(0, t_k).unwrap().readout(t_k).unwrap()).unwrap();
                println!("refusal {last} after the binding at tick {t_k}: r {r:.4e}, vr {vr:.3e}, vt {vt:.3e}, E {e:.3e} (planet at {:.3e}), fault {:?}, E_circ {:.3e}", to_f64(norm2(xp).unwrap()), rec.fault, -0.5 / r);
                shown += 1;
            }
        }
    }

    /// Diagnostic, not a gate (the Opus memo's §1 setup, which the coordinator asked B12 to be read on): B12's frozen ships with the
    /// planet's radius shrunk by `B12_SHRINK` (default 1000), so that no ship is lost to a surface; the exponent of the Jacobi error
    /// and its worst value, per kick cadence `B12_STEP`. `cargo test --release -p xtask b12_small_planet -- --ignored --nocapture`.
    #[test]
    #[ignore]
    fn b12_small_planet() {
        use super::super::{fit, handoff};
        let step: i32 = std::env::var("B12_STEP").ok().and_then(|v| v.parse().ok()).unwrap_or(7);
        let shrink: f64 = std::env::var("B12_SHRINK").ok().and_then(|v| v.parse().ok()).unwrap_or(1000.0);
        let scene = Restricted { planet_radius: JUPITER.planet_radius / shrink, ..JUPITER };
        let times = handoff::coarse_times(&scene);
        let (mut exps, mut worst, mut lost) = (Vec::new(), 0.0f64, 0);
        let wall = std::time::Instant::now();
        let law = Plane { step_log2: step };
        for k in handoff::kept().iter().filter(|k| k.closest >= JUPITER.planet_radius) {
            let c0 = scene.jacobi(0.0, &k.ship);
            let Some(states) = law.restricted(&scene, k.ship, &times) else {
                lost += 1;
                continue;
            };
            let err: Vec<f64> = states.iter().zip(&times).map(|(st, &t)| ((scene.jacobi(t, st) - c0) / c0).abs()).collect();
            let top = err.iter().fold(0.0f64, |m, e| m.max(*e));
            worst = worst.max(top);
            if top > 1e-12 {
                exps.push(fit::growth_exponent(&err));
            }
        }
        exps.sort_by(f64::total_cmp);
        println!("step {step}, planet radius /{shrink}: {} judged, {lost} lost; median exponent {:.3} (all {:.2?}); worst error {worst:.2e}; {:.1} s", exps.len(), exps.get(exps.len() / 2).copied().unwrap_or(f64::NAN), exps, wall.elapsed().as_secs_f64());
    }
}
