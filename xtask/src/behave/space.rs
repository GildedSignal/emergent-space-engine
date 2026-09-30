//! Boundary adapter only: quantize input, invoke the integer core, decode output.
//! Long runs look up the invariant-defined compiled generator.
use super::Law;
use emergent_space::{compile_variant, light_tail, scatter, Key, Memo, Outcome};
use std::cell::RefCell;

#[derive(Default)]
pub struct Space {
    memo: RefCell<Memo>,
    pub newton: bool,
}
fn bound_key(p: f64, e: f64) -> Option<Key> {
    if !p.is_finite() || !e.is_finite() || !(0.0..65536.0).contains(&p) || !(0.0..1.0).contains(&e)
    {
        return None;
    }
    Key::darwin(
        (p * 65536.0).round() as u32,
        (e * 1073741824.0).round() as u32,
    )
    .ok()
}
fn key(e: f64, l: f64) -> Option<Key> {
    if !e.is_finite() || !l.is_finite() || e <= 0.0 || l <= 0.0 {
        return None;
    }
    Key::new(
        (e * 281474976710656.0).round() as u64,
        (l * 4294967296.0).round() as u64,
    )
    .ok()
}
impl Law for Space {
    fn advance_per_cycle(&self, p: f64, e: f64) -> Option<(f64, f64, f64)> {
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
        let k = key(1.0, b)?;
        let (out, phi) = scatter(k, true).ok()?;
        if out != Outcome::Escaped {
            return None;
        }
        Some((phi.get() + 2 * light_tail(k).ok()?) as f64 / 1073741824.0 - std::f64::consts::PI)
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
        let Some(k) = bound_key(p, e) else {
            return vec![];
        };
        let Ok(c) = self.memo.borrow_mut().get(k) else {
            return vec![];
        };
        if c.repeat(cycles as u32).is_err() {
            return vec![];
        }
        let r = |s: emergent_space::State| 281474976710656.0 / s.u_q48() as f64;
        vec![
            (
                r(c.start),
                r(c.apo),
                k.energy.get() as f64 / 281474976710656.0,
                k.angular.get() as f64 / 4294967296.0
            );
            cycles
        ]
    }
}

#[cfg(test)]
mod tests {
    use super::*;
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
