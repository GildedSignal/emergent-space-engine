//! Sampled numerical state agreement, distinct from physical conservation.
use crate::coupled_source_response::{G, InitialCondition};
use crate::orbit_reference::Sample;
use crate::two_body_bank::Case;
use serde::{Deserialize, Serialize};

// Read only required fields; older retained reports lack optional work breakdowns.
// Do not fabricate missing counters or mutate the frozen report schema.
#[derive(Debug, Deserialize)]
pub struct ReferenceRun {
    pub version: String,
    pub case: Case,
    pub genesis: InitialCondition,
    pub period: f64,
    pub rungs: Vec<ReferenceRung>,
    pub total_charge: u64,
    pub complete_charge: bool,
}
#[derive(Debug, Deserialize)]
pub struct ReferenceRung {
    pub steps: usize,
    pub dt: f64,
    pub status: String,
    pub complete_charge: bool,
    pub samples: Vec<Sample>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Differences {
    pub position: f64,
    pub velocity: f64,
    pub energy: f64,
    pub angular_momentum: f64,
}
impl Differences {
    fn values(&self) -> [f64; 4] {
        [
            self.position,
            self.velocity,
            self.energy,
            self.angular_momentum,
        ]
    }
}
#[derive(Debug, Serialize)]
pub struct StateConvergence {
    pub version: &'static str,
    pub seed: u64,
    pub coarse_change: Differences,
    pub fine_change: Differences,
    pub compiler_difference: Differences,
    pub reference_pass: [bool; 4],
    pub agreement_pass: [bool; 4],
    pub all_pass: bool,
    pub sample_pair_comparisons: usize,
    pub reference_total_charge: u64,
    pub scope: &'static str,
}
/// Both sequences must represent the same 1025 uniform observation times.
pub fn differences(c: &Case, a: &[Sample], b: &[Sample]) -> Result<Differences, String> {
    if a.len() != 1025 || b.len() != a.len() {
        return Err("expected matching 1025-point observation grids".into());
    }
    let mu = G * c.total_mass;
    let scales = [
        c.a,
        (mu / c.a).sqrt(),
        mu / (2.0 * c.a),
        (mu * c.a * (1.0 - c.eccentricity.powi(2))).sqrt(),
    ];
    if !scales.iter().all(|s| s.is_finite() && *s > 0.0) {
        return Err("invalid physical normalization".into());
    }
    let mut maxima = [0.0_f64; 4];
    for (a, b) in a.iter().zip(b) {
        let invariants = |s: &Sample| -> Result<(f64, f64), String> {
            let r = s.x[0].hypot(s.x[1]);
            if !s.x.iter().chain(s.v.iter()).all(|x| x.is_finite()) || r <= 0.0 {
                return Err("invalid state sample".into());
            }
            Ok((
                0.5 * (s.v[0].powi(2) + s.v[1].powi(2)) - mu / r,
                s.x[0] * s.v[1] - s.x[1] * s.v[0],
            ))
        };
        let (ea, la) = invariants(a)?;
        let (eb, lb) = invariants(b)?;
        let deltas = [
            (a.x[0] - b.x[0]).hypot(a.x[1] - b.x[1]),
            (a.v[0] - b.v[0]).hypot(a.v[1] - b.v[1]),
            (ea - eb).abs(),
            (la - lb).abs(),
        ];
        for i in 0..4 {
            let d = deltas[i] / scales[i];
            if !d.is_finite() {
                return Err("nonfinite observable difference".into());
            }
            maxima[i] = maxima[i].max(d);
        }
    }
    Ok(Differences {
        position: maxima[0],
        velocity: maxima[1],
        energy: maxima[2],
        angular_momentum: maxima[3],
    })
}
fn screen(coarse: f64, fine: f64) -> bool {
    fine <= 0.005 && ((coarse <= 1e-10 && fine <= 1e-10) || fine <= 0.75 * coarse)
}
pub fn assess(reference: &ReferenceRun, candidate: &[Sample]) -> Result<StateConvergence, String> {
    if reference.version != "same-genesis-euler-refinement-v1"
        || reference.rungs.len() < 3
        || !reference.complete_charge
    {
        return Err("unsupported or incomplete reference".into());
    }
    let expected_period =
        std::f64::consts::TAU * (reference.case.a.powi(3) / (G * reference.case.total_mass)).sqrt();
    if !reference.genesis.genesis_t.is_finite()
        || reference.genesis.genesis_t >= 0.0
        || !expected_period.is_finite()
        || expected_period <= 0.0
        || !reference.period.is_finite()
        || (reference.period - expected_period).abs() > 1e-12 * expected_period
    {
        return Err("invalid observation horizon".into());
    }
    let r = &reference.rungs[reference.rungs.len() - 3..];
    for rung in r {
        if rung.status != "MEASURED"
            || !rung.complete_charge
            || rung.steps == 0
            || !rung.dt.is_finite()
            || rung.dt <= 0.0
        {
            return Err("unsuccessful reference rung".into());
        }
        let expected_dt = (reference.period - reference.genesis.genesis_t) / rung.steps as f64;
        if (rung.dt - expected_dt).abs() > 1e-12 * expected_dt {
            return Err("reference spacing does not match genesis and horizon".into());
        }
    }
    if r.windows(2)
        .any(|w| w[0].steps.checked_mul(2) != Some(w[1].steps))
    {
        return Err("reference steps must double".into());
    }
    let coarse = differences(&reference.case, &r[0].samples, &r[1].samples)?;
    let fine = differences(&reference.case, &r[1].samples, &r[2].samples)?;
    let compiler = differences(&reference.case, &r[2].samples, candidate)?;
    let cv = coarse.values();
    let fv = fine.values();
    let dv = compiler.values();
    let reference_pass = std::array::from_fn(|i| screen(cv[i], fv[i]));
    let agreement_pass: [bool; 4] = std::array::from_fn(|i| reference_pass[i] && dv[i] <= 0.02);
    Ok(StateConvergence {
        version: "orbital-state-convergence-v1",
        seed: reference.case.seed,
        coarse_change: coarse,
        fine_change: fine,
        compiler_difference: compiler,
        reference_pass,
        agreement_pass,
        all_pass: agreement_pass.iter().all(|p| *p),
        sample_pair_comparisons: 3 * 1025,
        reference_total_charge: reference.total_charge,
        scope: "Retrospective sampled agreement in position, velocity, Newtonian energy and signed angular momentum. Shared field algebra. No conservation, interval, canonical gravity or GR qualification. Original reference charge includes its original compiler run; audit pair comparisons counted separately.",
    })
}
#[cfg(test)]
mod tests {
    use super::*;
    fn circle() -> (Case, Vec<Sample>) {
        let c = Case::from_seed(0);
        let v = (G * c.total_mass / c.a).sqrt();
        let samples = (0..1025)
            .map(|i| {
                let t = std::f64::consts::TAU * i as f64 / 1024.0;
                Sample {
                    x: [c.a * t.cos(), c.a * t.sin()],
                    v: [-v * t.sin(), v * t.cos()],
                }
            })
            .collect();
        (c, samples)
    }
    #[test]
    fn reversed_velocity_is_not_hidden_by_equal_positions_or_energy() {
        let (c, a) = circle();
        let mut b = a.clone();
        for s in &mut b {
            s.v = [-s.v[0], -s.v[1]];
        }
        let d = differences(&c, &a, &b).unwrap();
        assert_eq!(d.position, 0.0);
        assert_eq!(d.energy, 0.0);
        assert!((d.velocity - 2.0).abs() < 1e-12);
        assert!((d.angular_momentum - 2.0).abs() < 1e-12);
    }
    #[test]
    fn isolated_velocity_error_and_invalid_samples_cannot_hide_in_extrema() {
        let (c, a) = circle();
        let mut b = a.clone();
        b[517].v[0] += 0.1;
        let d = differences(&c, &a, &b).unwrap();
        assert_eq!(d.position, 0.0);
        assert!(d.velocity > 0.02 && d.energy > 0.0);
        b[517].v[0] = f64::NAN;
        assert!(differences(&c, &a, &b).is_err());
        b[517].v[0] = f64::MAX;
        assert!(differences(&c, &a, &b).is_err());
        assert!(differences(&c, &a, &a[..1024]).is_err());
    }
    #[test]
    fn stale_or_incomplete_reference_metadata_is_refused() {
        let (case, samples) = circle();
        let period = std::f64::consts::TAU * (case.a.powi(3) / (G * case.total_mass)).sqrt();
        let genesis = case.initial_condition();
        let rungs = [8, 16, 32]
            .into_iter()
            .map(|steps| ReferenceRung {
                steps,
                dt: (period - genesis.genesis_t) / steps as f64,
                status: "MEASURED".into(),
                complete_charge: true,
                samples: samples.clone(),
            })
            .collect();
        let mut reference = ReferenceRun {
            version: "same-genesis-euler-refinement-v1".into(),
            case,
            genesis,
            period,
            rungs,
            total_charge: 0,
            complete_charge: true,
        };
        assert!(assess(&reference, &samples).unwrap().all_pass);
        reference.rungs[2].steps = 33;
        assert!(assess(&reference, &samples).is_err());
        reference.rungs[2].steps = 32;
        reference.rungs[2].complete_charge = false;
        assert!(assess(&reference, &samples).is_err());
        reference.rungs[2].complete_charge = true;
        reference.genesis.genesis_t = f64::NAN;
        assert!(assess(&reference, &samples).is_err());
    }

    #[test]
    fn screen_requires_both_resolution_and_contraction() {
        assert!(screen(0.008, 0.004));
        assert!(screen(0.0, 0.0));
        assert!(!screen(0.1, 0.05));
        assert!(!screen(0.004, 0.004));
        assert!(!screen(0.0, 0.004));
    }
}
