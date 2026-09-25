//! Independent Newtonian evolution of the SAME observed relative state at t=0.
//! Diagnostic attribution only: does not replace retarded genesis or GEM physics.
use crate::coupled_source_response::G;
use crate::orbit_reference::Sample;
use crate::two_body_bank::Case;
use std::f64::consts::TAU;

fn derivative(y: [f64; 4], mu: f64) -> Result<[f64; 4], String> {
    let r = y[0].hypot(y[1]);
    if !y.iter().all(|x| x.is_finite()) || !r.is_finite() || r <= 0.0 {
        return Err("invalid Newtonian control state".into());
    }
    let k = -mu / (r * r * r);
    Ok([y[2], y[3], k * y[0], k * y[1]])
}
fn shifted(y: [f64; 4], k: [f64; 4], h: f64) -> [f64; 4] {
    std::array::from_fn(|i| y[i] + h * k[i])
}
pub fn evolve(case: &Case, initial: &Sample, steps: usize) -> Result<Vec<Sample>, String> {
    if steps == 0
        || steps % 1024 != 0
        || !case.a.is_finite()
        || case.a <= 0.0
        || !case.total_mass.is_finite()
        || case.total_mass <= 0.0
    {
        return Err("invalid Newtonian control grid or mass".into());
    }
    let mu = G * case.total_mass;
    let dt = TAU * (case.a.powi(3) / mu).sqrt() / steps as f64;
    if !dt.is_finite() || dt <= 0.0 {
        return Err("invalid Newtonian control period".into());
    }
    let mut y = [initial.x[0], initial.x[1], initial.v[0], initial.v[1]];
    let mut samples = Vec::with_capacity(1025);
    for i in 0..=steps {
        if i % (steps / 1024) == 0 {
            samples.push(Sample {
                x: [y[0], y[1]],
                v: [y[2], y[3]],
            });
        }
        if i == steps {
            break;
        }
        let k1 = derivative(y, mu)?;
        let k2 = derivative(shifted(y, k1, dt / 2.0), mu)?;
        let k3 = derivative(shifted(y, k2, dt / 2.0), mu)?;
        let k4 = derivative(shifted(y, k3, dt), mu)?;
        y = std::array::from_fn(|j| y[j] + dt * (k1[j] + 2.0 * k2[j] + 2.0 * k3[j] + k4[j]) / 6.0);
    }
    Ok(samples)
}
#[cfg(test)]
mod tests {
    use super::*;
    use crate::orbit_state_convergence::differences;
    use crate::two_body_bank::kepler_relative;
    #[test]
    fn rk4_control_refines_against_independent_analytic_eccentric_orbit() {
        for seed in [4, 8, 9, 10, 11] {
            let case = Case::from_seed(seed);
            let period = TAU * (case.a.powi(3) / (G * case.total_mass)).sqrt();
            let exact: Vec<_> = (0..1025)
                .map(|i| {
                    let (x, v) = kepler_relative(&case, period * i as f64 / 1024.0);
                    Sample { x, v }
                })
                .collect();
            let coarse = evolve(&case, &exact[0], 1024).unwrap();
            let fine = evolve(&case, &exact[0], 2048).unwrap();
            let c = differences(&case, &exact, &coarse).unwrap();
            let f = differences(&case, &exact, &fine).unwrap();
            assert!(f.position < c.position / 10.0 && f.velocity < c.velocity / 10.0);
            assert!(f.position < 1e-6 && f.velocity < 1e-6);
        }
    }
    #[test]
    fn control_uses_given_state_and_rejects_bad_input() {
        let c = Case::from_seed(8);
        let (x, v) = kepler_relative(&c, 0.0);
        let mut s = Sample { x, v };
        s.v[0] += 0.01;
        let out = evolve(&c, &s, 1024).unwrap();
        assert_eq!(out[0].v, s.v);
        s.x = [0.0, 0.0];
        assert!(evolve(&c, &s, 1024).is_err());
        assert!(evolve(&c, &s, 0).is_err());
    }
}
