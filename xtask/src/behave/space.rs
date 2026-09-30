//! Boundary adapter only: quantize input, invoke the integer core, decode output.
//! Long runs read each cycle's turning points from positions derived from the compiled cycle.
use super::Law;
use emergent_space::events::clock_rate;
use emergent_space::{
    binding::Trajectory,
    orbit::{OrbitKey, QuantizedMemo, Scalar},
    tube::Catalogue,
};
use emergent_space::{compile_variant, scatter, Key, LegacyTube as Tube, Memo, Outcome, Words};
use std::cell::RefCell;

#[derive(Default)]
pub struct Space {
    memo: RefCell<Memo>,
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
    Scalar::raw((x * 2f64.powi(60 - exponent)).round() as i128, exponent - 60).ok()
}
fn decoded(x: Scalar) -> f64 {
    x.significand() as f64 * 2f64.powi(x.exponent() as i32 - 62)
}
fn native_key(p: f64, e: f64) -> Option<OrbitKey> {
    if !e.is_finite() || !(0.0..1.0).contains(&e) {
        return None;
    }
    OrbitKey::bound(scalar(p)?, (e * 2f64.powi(48)).round() as u64).ok()
}
fn bound_key(p: f64, e: f64) -> Option<Key> {
    if !p.is_finite() || !e.is_finite() || !(0.0..65536.0).contains(&p) || !(0.0..1.0).contains(&e) {
        return None;
    }
    Key::darwin((p * 65536.0).round() as u32, (e * 1073741824.0).round() as u32).ok()
}
fn key(e: f64, l: f64) -> Option<Key> {
    if !e.is_finite() || !l.is_finite() || e <= 0.0 || l <= 0.0 {
        return None;
    }
    Key::new((e * 281474976710656.0).round() as u64, (l * 4294967296.0).round() as u64).ok()
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
            energy: (energy * 281474976710656.0).round() as i64,
            angular: Words::new((angular * 4294967296.0).round() as u64),
            nu: (nu * 1073741824.0).round() as u32,
        };
        let c = self.memo.borrow_mut().get(binary.key().ok()?).ok()?;
        Some((
            c.increments.phi.get() as f64 / 1073741824.0 - std::f64::consts::TAU,
            binary.period(&c).ok()?.get() as f64 / 1048576.0,
        ))
    }
    fn restricted(&self, scene: &super::restricted::Restricted, ship: [f64; 4], times: &[f64]) -> Option<Vec<[f64; 4]>> {
        // Probe the required centre tube before building an event graph. The
        // public compiler envelope is checked before any evolution.
        // Unbound trajectory readout and authoritative state -> key/phase fitting
        // are not provided by scatter. Refuse rather than substitute the judge.
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
        let lapse = 1.0 - 3.0 / r;
        if lapse <= 0.0 {
            return None;
        }
        self.shapes.borrow_mut().get(self.bound_native_key(r, 0.0)?).ok()?;
        None // No authoritative three-body generator exists in this layer yet.
    }
    fn static_clock_rate(&self, r: f64) -> Option<f64> {
        rate(r, 2)
    }
    fn circular_clock_rate(&self, r: f64) -> Option<f64> {
        rate(r, 3)
    }
    fn crossings_per_cycle(&self, p: f64, e: f64) -> Option<f64> {
        Some(2.0 * self.shapes.borrow_mut().get(self.bound_native_key(p, e)?).ok()?.shape().crossings().len() as f64)
    }
    fn scene_cost(&self, n: usize, game_seconds: f64) -> Option<f64> {
        if !game_seconds.is_finite() || game_seconds < 0.0 || game_seconds * 1048576.0 > u64::MAX as f64 {
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
        if !self.newton {
            let c = self.shapes.borrow_mut().get(self.bound_native_key(p, e)?).ok()?;
            return Some((decoded(c.advance().ok()?), decoded(c.period().ok()?), decoded(c.proper_period().ok()?)));
        }
        let key = bound_key(p, e)?;
        let c = if self.newton {
            std::sync::Arc::new(compile_variant(key, true).ok()?)
        } else {
            self.memo.borrow_mut().get(key).ok()?
        };
        let d = c.increments;
        Some((
            d.phi.get() as f64 / 1073741824.0 - std::f64::consts::TAU,
            d.t.get() as f64 / 1048576.0,
            d.tau.get() as f64 / 1048576.0,
        ))
    }
    fn deflection(&self, b: f64) -> Option<f64> {
        let (out, half) = scatter(key(1.0, b)?, true).ok()?;
        if out != Outcome::Escaped {
            return None;
        }
        Some(2.0 * half.get() as f64 / 1073741824.0 - std::f64::consts::PI)
    }
    fn captured(&self, e: f64, l: f64) -> bool {
        key(e, l)
            .and_then(|k| scatter(k, false).ok())
            .is_some_and(|(o, _)| o == Outcome::Absorbed)
    }
    fn photon_captured(&self, b: f64) -> bool {
        key(1.0, b)
            .and_then(|k| scatter(k, true).ok())
            .is_some_and(|(o, _)| o == Outcome::Absorbed)
    }
    fn long_run(&self, p: f64, e: f64, cycles: usize) -> Vec<(f64, f64, f64, f64)> {
        if !self.newton {
            let Some(key) = self.bound_native_key(p, e) else {
                return vec![];
            };
            let Ok(c) = self.shapes.borrow_mut().get(key) else {
                return vec![];
            };
            let k = key.k as f64 / 2f64.powi(48);
            let rp = decoded(key.periapsis);
            let eq = 1.0 / k - 1.0;
            let pq = rp / k;
            let energy = (((pq - 2.0).powi(2) - 4.0 * eq * eq) / (pq * (pq - 3.0 - eq * eq))).sqrt();
            let angular = pq / (pq - 3.0 - eq * eq).sqrt();
            return (0..cycles as u64)
                .map_while(|n| {
                    let peri = c.crossing_state(0, n, true).ok()?;
                    let apo = c.crossing_state(c.shape().knots().len() - 1, n, true).ok()?;
                    Some((decoded(peri.radius), decoded(apo.radius), energy, angular))
                })
                .collect();
        }
        let Some(k) = bound_key(p, e) else {
            return vec![];
        };
        let Ok(c) = self.memo.borrow_mut().get(k) else {
            return vec![];
        };
        let tube = Tube::new(Words::default(), Words::default());
        let period = c.increments.t.get();
        let r = |u: i64| 4611686018427387904.0 / u as f64;
        let (energy, angular) = (k.energy.get() as f64 / 281474976710656.0, k.angular.get() as f64 / 4294967296.0);
        (0..cycles as u64)
            .map_while(|n| {
                let t = n.checked_mul(period)?;
                let peri = tube.position(&c, Words::new(t)).ok()?;
                let apo = tube.position(&c, Words::new(t.checked_add(period / 2)?)).ok()?;
                Some((r(peri.u), r(apo.u), energy, angular))
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
        let gates = super::super::judge_only(&law, None, Some(&["G1", "G2", "G3", "G4", "G5", "G6"]), |g| {
            println!("{} {} {}", g.id, if g.pass { "PASS" } else { "FAIL" }, g.detail)
        });
        assert_eq!(gates.len(), 6);
        assert!(gates.iter().all(|g| g.pass));
    }
    #[test]
    fn planted_newtonian_map_fails_precession_gate() {
        let law = Space {
            newton: true,
            ..Space::default()
        };
        let (advance, _, _) = law.advance_per_cycle(100.0, 0.3).expect("wrong law must answer a real orbit");
        assert!(advance.abs() < 1e-3, "the planted force must give Newtonian zero advance");
        let gates = super::super::judge(&law, None, |g| println!("{} {} {}", g.id, if g.pass { "PASS" } else { "FAIL" }, g.detail));
        let g = gates.iter().find(|g| g.id == "G1").unwrap();
        assert!(!g.pass, "the wrong force must be killed: {}", g.detail);
    }
}
