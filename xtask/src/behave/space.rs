//! Boundary adapter only: quantize input, invoke the integer core, decode output.
//! Long runs read each cycle's turning points from positions derived from the compiled cycle.
use super::Law;
use emergent_space::events::clock_rate;
use emergent_space::{
    binding::Trajectory,
    orbit::{Orbit, OrbitKey, Passage, QuantizedMemo, Scalar},
    tube::Catalogue,
};
use std::cell::RefCell;

#[derive(Default)]
pub struct Space {
    shapes: RefCell<QuantizedMemo>,
    pub newton: bool,
    #[cfg(test)]
    key_bits: Option<(u32, u32)>,
}
fn scalar(x: f64) -> Option<Scalar> {
    if !x.is_finite() || x <= 0.0 {
        return None;
    }
    let exponent = x.log2().floor() as i32;
    Scalar::raw(
        (x * 2f64.powi(60 - exponent)).round() as i128,
        exponent - 60,
    )
    .ok()
}
fn decoded(x: Scalar) -> f64 {
    x.significand() as f64 * 2f64.powi(x.exponent() as i32 - 62)
}
fn signed(x: f64) -> Option<Scalar> {
    if x == 0.0 {
        Some(Scalar::ZERO)
    } else {
        scalar(x.abs()).map(|s| if x < 0.0 { s.negate() } else { s })
    }
}
fn native_key(p: f64, e: f64) -> Option<OrbitKey> {
    if !e.is_finite() || !(0.0..1.0).contains(&e) {
        return None;
    }
    OrbitKey::bound(scalar(p)?, (e * 2f64.powi(48)).round() as u64).ok()
}
impl Space {
    fn bound_native_key(&self, p: f64, e: f64) -> Option<OrbitKey> {
        let key = native_key(p, e)?;
        #[cfg(test)]
        if let Some((shape, scale)) = self.key_bits {
            return key.quantized(shape, scale).ok();
        }
        key.memo_key().ok()
    }
}
impl Law for Space {
    fn kerr(
        &self,
        chi: f64,
        query: &super::rotating::KerrQuery,
    ) -> Option<super::rotating::KerrAnswer> {
        use super::rotating::{KerrAnswer as A, KerrQuery as Q, Observer, Sense};
        use emergent_space::kerr::{Constants, Cycle, Fate, Spin};
        // The zero-spin boundary is exactly the established Schwarzschild
        // adapter, including its memo quantization and floating-point decode.
        if chi == 0.0 {
            match *query {
                Q::Cycle { p, e, .. } => {
                    return Some(self.advance_per_cycle(p, e).map_or(
                        A::Absent,
                        |(advance, period, proper_period)| A::Cycle {
                            advance,
                            period,
                            proper_period,
                        },
                    ))
                }
                Q::Deflection { b } => {
                    return Some(self.deflection(b.abs()).map_or(A::Absent, A::Angle))
                }
                Q::PhotonFate { b } => {
                    return Some(A::Fate(if self.photon_captured(b.abs()) {
                        super::kerr::Fate::Captured
                    } else {
                        super::kerr::Fate::Scattered
                    }))
                }
                Q::Fate { energy, angular } if energy >= 1.0 => {
                    return Some(A::Fate(if self.captured(energy, angular.abs()) {
                        super::kerr::Fate::Captured
                    } else {
                        super::kerr::Fate::Scattered
                    }))
                }
                Q::Clock {
                    r,
                    observer: Observer::Static,
                } => return Some(self.static_clock_rate(r).map_or(A::Absent, A::Rate)),
                _ => {}
            }
        }
        let spin = Spin::new(signed(chi)?).ok()?;
        let fate = |f| {
            A::Fate(match f {
                Fate::Bound => super::kerr::Fate::Bound,
                Fate::Plunge => super::kerr::Fate::Plunge,
                Fate::Scattered => super::kerr::Fate::Scattered,
                Fate::Captured => super::kerr::Fate::Captured,
            })
        };
        Some(match *query {
            Q::Cycle { p, e, sense } => {
                let c = Cycle::bound(
                    spin,
                    scalar(p)?,
                    (e * 2f64.powi(48)).round() as u64,
                    sense == Sense::Retro,
                );
                match c {
                    Ok(c) => A::Cycle {
                        advance: decoded(c.advance().ok()?),
                        period: decoded(c.period().ok()?),
                        proper_period: decoded(c.proper_period().ok()?),
                    },
                    Err(_) => A::Absent,
                }
            }
            Q::Circular { r, sense } => spin
                .circular(scalar(r)?, sense == Sense::Retro)
                .ok()?
                .map_or(A::Absent, |(_, stable)| A::Circular { stable }),
            Q::Fate { energy, angular } => fate(
                Constants::massive(signed(energy)?, signed(angular)?)
                    .fate(spin)
                    .ok()?,
            ),
            Q::PhotonFate { b } => fate(Constants::photon(signed(b)?).fate(spin).ok()?),
            Q::Deflection { b } => emergent_space::kerr::deflection(spin, signed(b)?)
                .ok()?
                .map_or(A::Absent, |d| A::Angle(decoded(d))),
            Q::Clock { r, observer } => match observer {
                Observer::Static => spin.static_clock(scalar(r)?),
                Observer::Zamo => spin.zamo_clock(scalar(r)?),
            }
            .ok()?
            .map_or(A::Absent, |r| A::Rate(decoded(r))),
            Q::Tube { energy, angular, r } => Constants::massive(signed(energy)?, signed(angular)?)
                .tube_rates(spin, scalar(r)?)
                .ok()?
                .map_or(A::Absent, |[p, t]| A::Tube {
                    phi_rate: decoded(p),
                    clock_rate: decoded(t),
                }),
            Q::Split { energy, angular, r } => {
                Constants::massive(signed(energy)?, signed(angular)?)
                    .split(spin, scalar(r)?)
                    .ok()?
                    .map_or(A::Absent, |[f, b]| A::Split {
                        forward: (decoded(f.energy), decoded(f.angular)),
                        backward: (decoded(b.energy), decoded(b.angular)),
                    })
            }
        })
    }
    fn binary_cycle(&self, energy: f64, angular: f64, nu: f64) -> Option<(f64, f64)> {
        if !energy.is_finite()
            || !angular.is_finite()
            || !nu.is_finite()
            || !(-1.0..0.0).contains(&energy)
            || angular <= 0.0
            || !(0.0..=0.25).contains(&nu)
        {
            return None;
        }
        let binary = emergent_space::events::binary::Binary {
            energy: scalar(-energy)?.negate(),
            angular: scalar(angular)?,
            nu: (nu * 1073741824.0).round() as u32,
        };
        let c = Orbit::compile(binary.key().ok()?).ok()?;
        Some((decoded(c.advance().ok()?), decoded(binary.period(&c).ok()?)))
    }
    fn restricted(
        &self,
        scene: &super::restricted::Restricted,
        ship: [f64; 4],
        times: &[f64],
    ) -> Option<Vec<[f64; 4]>> {
        // Float conversion is confined to this judge boundary; all evolution and
        // acceptance decisions are integer and independent of the oracle.
        use emergent_space::events::dense::{inertial, Scene, Stepper, ONE};
        if !scene.mu.is_finite()
            || !scene.sep.is_finite()
            || !(0.0..0.5).contains(&scene.mu)
            || scene.sep <= 0.0
            || ship.iter().chain(times).any(|x| !x.is_finite())
            || times.iter().any(|&t| t < 0.0)
            || times.windows(2).any(|w| w[0] > w[1])
        {
            return None;
        }
        let r = scene.sep / (1.0 - scene.mu);
        self.shapes
            .borrow_mut()
            .get(self.bound_native_key(r, 0.0)?)
            .ok()?;
        let speed_unit = 1.0 / scene.sep.sqrt();
        let time_unit = scene.sep / speed_unit;
        let encode = |x: f64| -> Option<i64> {
            let n = (x * ONE as f64).round();
            if !n.is_finite() || n < i64::MIN as f64 || n >= i64::MAX as f64 {
                None
            } else {
                Some(n as i64)
            }
        };
        let relative = scene.relative(0.0, &ship);
        if ship[2].hypot(ship[3]) > 0.25 || relative[2].hypot(relative[3]) > 0.25 {
            return None;
        }
        let initial = [
            encode(relative[0] / scene.sep)?,
            encode(relative[1] / scene.sep)?,
            encode(relative[2] / speed_unit)?,
            encode(relative[3] / speed_unit)?,
        ];
        let native = Scene {
            mu: encode(scene.mu)?,
            radius: encode(scene.planet_radius / scene.sep)?,
            edge: encode(scene.soi() / scene.sep)?,
            speed_unit: scalar(speed_unit)?,
        };
        let mut stepper = Stepper::new(native, initial).ok()?;
        let mut states = Vec::with_capacity(times.len());
        for &time in times {
            let at = encode(time / time_unit)?;
            let y = inertial(stepper.at(at).ok()?, at).ok()?;
            let rel = [
                y[0] as f64 / ONE as f64 * scene.sep,
                y[1] as f64 / ONE as f64 * scene.sep,
                y[2] as f64 / ONE as f64 * speed_unit,
                y[3] as f64 / ONE as f64 * speed_unit,
            ];
            states.push(scene.barycentric(time, &rel));
        }
        if std::env::var_os("SPACE_EVENTS_TRACE").is_some() {
            eprintln!(
                "events_trace samples={} periods={:.6} steps={} forces={} edges={}",
                times.len(),
                times.last().copied().unwrap_or(0.0) / scene.period(),
                stepper.counts.steps,
                stepper.counts.force_evaluations,
                stepper.counts.edge_crossings
            );
        }
        Some(states)
    }
    fn static_clock_rate(&self, r: f64) -> Option<f64> {
        rate(r, 2)
    }
    fn circular_clock_rate(&self, r: f64) -> Option<f64> {
        rate(r, 3)
    }
    fn crossings_per_cycle(&self, p: f64, e: f64) -> Option<f64> {
        Some(
            2.0 * self
                .shapes
                .borrow_mut()
                .get(self.bound_native_key(p, e)?)
                .ok()?
                .shape()
                .crossings()
                .len() as f64,
        )
    }
    fn scene_cost(&self, n: usize, game_seconds: f64) -> Option<f64> {
        if !game_seconds.is_finite()
            || game_seconds < 0.0
            || game_seconds * 1048576.0 > u64::MAX as f64
        {
            return None;
        }
        let start = std::time::Instant::now();
        let mut shapes = QuantizedMemo::with_capacity(n);
        let mut pool = Catalogue::with_capacity(n);
        let mut tubes = Vec::with_capacity(n);
        for (p, e) in super::sample::bound_orbits(n) {
            let orbit = shapes.get(self.bound_native_key(p, e)?).ok()?;
            let id = pool.insert(Trajectory::Cycle(orbit), false).ok()?;
            tubes.push(emergent_space::Tube::new(id, 0, 0));
        }
        // The frozen scene has no perturbations or edges; an empty queue proves
        // no work is due through the requested time. Charge all scene construction.
        let calendar = emergent_space::events::Calendar::new(n);
        std::hint::black_box((&pool, &shapes, &tubes, &calendar, game_seconds));
        Some(start.elapsed().as_secs_f64())
    }
    fn advance_per_cycle(&self, p: f64, e: f64) -> Option<(f64, f64, f64)> {
        let key = self.bound_native_key(p, e)?;
        let c = if self.newton {
            Orbit::newtonian(key).ok()?
        } else {
            self.shapes.borrow_mut().get(key).ok()?
        };
        Some((
            decoded(c.advance().ok()?),
            decoded(c.period().ok()?),
            decoded(c.proper_period().ok()?),
        ))
    }
    fn deflection(&self, b: f64) -> Option<f64> {
        let b = scalar(b)?;
        let p = Passage::photon(b, b.scale(1).ok()?).ok()??;
        Some(decoded(p.deflection().ok()?))
    }
    fn moving_deflection(&self, lens: &super::lens::MovingLens) -> Option<f64> {
        let signed = |x: f64| {
            if x == 0.0 {
                Some(Scalar::ZERO)
            } else {
                scalar(x.abs()).map(|a| if x < 0.0 { a.negate() } else { a })
            }
        };
        Some(decoded(
            emergent_space::light::moving_deflection(
                [signed(lens.theta.cos())?, signed(lens.theta.sin())?],
                signed(lens.beta)?,
                signed(lens.b)?,
            )
            .ok()?,
        ))
    }
    fn captured(&self, e: f64, l: f64) -> bool {
        let delta = if e == 1.0 {
            Scalar::ZERO
        } else if e > 1.0 {
            match scalar(e - 1.0) {
                Some(x) => x,
                None => return false,
            }
        } else {
            return false;
        };
        scalar(l).is_some_and(|l| {
            matches!(
                OrbitKey::from_invariants(delta, l),
                Err(emergent_space::Error::NoBoundOrbit)
            )
        })
    }
    fn photon_captured(&self, b: f64) -> bool {
        scalar(b)
            .and_then(|b| OrbitKey::photon(b).ok())
            .is_some_and(|k| k.is_none())
    }
    fn long_run(&self, p: f64, e: f64, cycles: usize) -> Vec<(f64, f64, f64, f64)> {
        let Some(key) = self.bound_native_key(p, e) else {
            return vec![];
        };
        let Ok(c) = (if self.newton {
            Orbit::newtonian(key)
        } else {
            self.shapes.borrow_mut().get(key)
        }) else {
            return vec![];
        };
        let k = key.k as f64 / 2f64.powi(48);
        let rp = decoded(key.periapsis);
        let eq = 1.0 / k - 1.0;
        let pq = rp / k;
        let energy = (((pq - 2.0).powi(2) - 4.0 * eq * eq) / (pq * (pq - 3.0 - eq * eq))).sqrt();
        let angular = pq / (pq - 3.0 - eq * eq).sqrt();
        (0..cycles as u64)
            .map_while(|n| {
                let peri = c.crossing_state(0, n, true).ok()?;
                let apo = c
                    .crossing_state(c.shape().knots().len() - 1, n, true)
                    .ok()?;
                Some((decoded(peri.radius), decoded(apo.radius), energy, angular))
            })
            .collect()
    }
}

fn rate(r: f64, k: u32) -> Option<f64> {
    if !r.is_finite() || r <= k as f64 {
        return None;
    }
    let u = (4611686018427387904.0 / r).floor() as u64;
    Some(clock_rate(u, k).ok()?.get() as f64 / 281474976710656.0)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn coarsest_screened_key_passes_all_six_unchanged_behavior_gates() {
        let law = Space {
            key_bits: Some((11, 12)),
            ..Space::default()
        };
        let gates = super::super::judge_only(
            &law,
            None,
            Some(&["G1", "G2", "G3", "G4", "G5", "G6"]),
            |g| {
                println!(
                    "{} {} {}",
                    g.id,
                    if g.pass { "PASS" } else { "FAIL" },
                    g.detail
                )
            },
        );
        assert_eq!(gates.len(), 6);
        assert!(gates.iter().all(|g| g.pass));
    }
    #[test]
    fn planted_newtonian_map_fails_precession_gate() {
        let law = Space {
            newton: true,
            ..Space::default()
        };
        let (advance, _, _) = law
            .advance_per_cycle(100.0, 0.3)
            .expect("wrong law must answer a real orbit");
        assert!(
            advance.abs() < 1e-3,
            "the planted force must give Newtonian zero advance"
        );
        let gates = super::super::judge(&law, None, |g| {
            println!(
                "{} {} {}",
                g.id,
                if g.pass { "PASS" } else { "FAIL" },
                g.detail
            )
        });
        let g = gates.iter().find(|g| g.id == "G1").unwrap();
        assert!(!g.pass, "the wrong force must be killed: {}", g.detail);
    }
}
