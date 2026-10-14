//! B12 v3: independent, per-ship Q40 Allan and alpha readings at 10,000 P.
//! The 13 October law row is archived with this job (the v2 checkout predates it).
#[cfg(test)]
use super::restricted::{Integrator, Model, RTOL, RTOL_FINE};
use super::restricted::{Restricted, JUPITER};
#[cfg(test)]
use super::sample;
use super::{b12_stat, Gate, Law};
use std::sync::OnceLock;

pub const PERIODS: usize = 10_000;
#[cfg(test)]
const CORPUS_PERIODS: usize = 200;
pub const COARSE: usize = 8;
#[cfg(test)]
pub const FINE: usize = 256;
pub const KEEP: usize = 16;
pub const CROSSINGS_MIN: usize = 20;
pub const FLOOR: f64 = 1e-12;
#[cfg(test)]
pub const CONVERGED: f64 = 1e-9;
/// The frozen slow control: 2e-10 across the entire horizon, not per period.
pub const DETECTABLE_LEAK: f64 = 2e-10;
/// Additional B12 controls, confined to this gate. The oscillation is deliberately
/// detuned from both the planet period and the sample cadence (100.001 P).
pub struct Control(pub bool);
pub fn control(detuned: bool) -> Control {
    Control(detuned)
}
impl Law for Control {
    fn advance_per_cycle(&self, p: f64, e: f64) -> Option<(f64, f64, f64)> {
        super::laws::Echo.advance_per_cycle(p, e)
    }
    fn deflection(&self, b: f64) -> Option<f64> {
        super::laws::Echo.deflection(b)
    }
    fn captured(&self, e: f64, l: f64) -> bool {
        super::laws::Echo.captured(e, l)
    }
    fn photon_captured(&self, b: f64) -> bool {
        super::laws::Echo.photon_captured(b)
    }
    fn long_run(&self, p: f64, e: f64, n: usize) -> Vec<(f64, f64, f64, f64)> {
        super::laws::Echo.long_run(p, e, n)
    }
    fn restricted(
        &self,
        scene: &Restricted,
        ship: [f64; 4],
        times: &[f64],
    ) -> Option<Vec<[f64; 4]>> {
        let states = super::laws::Echo.restricted(scene, ship, times)?;
        if !self.0 {
            return b12_stat::inject_leak(scene, ship, times, &states, 2e-10);
        }
        let c0 = scene.jacobi(0.0, &ship).abs();
        let shifts = times
            .iter()
            .map(|t| c0 * 1e-7 * (std::f64::consts::TAU * t / (100.001 * scene.period())).sin())
            .collect::<Vec<_>>();
        Some(super::laws::lay(scene, states, &shifts))
    }
}

#[cfg(test)]
pub fn ship(scene: &Restricted, side: f64, k: f64, alpha: f64) -> [f64; 4] {
    let r = scene.sep * (1.0 + side * scene.hill() / scene.sep * k);
    let v = r.powf(-0.5);
    [
        r * alpha.cos(),
        r * alpha.sin(),
        -v * alpha.sin(),
        v * alpha.cos(),
    ]
}
pub fn coarse_times(scene: &Restricted) -> Vec<f64> {
    (0..=PERIODS * COARSE)
        .map(|j| j as f64 * scene.period() / COARSE as f64)
        .collect()
}

#[derive(serde::Deserialize)]
struct Replica {
    crossings: usize,
    converged: bool,
    closest: f64,
}
#[derive(serde::Deserialize)]
struct Recorded {
    draw: usize,
    bits: [u64; 4],
    runs: Vec<Replica>,
}

pub struct Kept {
    pub ship: [f64; 4],
    pub crossings: usize,
    pub converged: bool,
    pub closest: f64,
    pub fate_safe: bool,
}

/// Exact IEEE input words and offline reference assessments: no trig, live
/// search, live convergence exclusion, or machine-dependent fate classification.
/// The corpus is a reviewable candidate, NOT a gate freeze.
pub fn kept() -> &'static Vec<Kept> {
    static KEPT: OnceLock<Vec<Kept>> = OnceLock::new();
    KEPT.get_or_init(|| {
        let rows: Vec<Recorded> =
            serde_json::from_str(include_str!("b12_corpus.json")).expect("B12 corpus");
        rows.into_iter()
            .map(|r| {
                let base = &r.runs[0];
                assert!(r.draw < 256 && r.runs.len() == 9);
                assert!(
                    base.crossings >= CROSSINGS_MIN
                        && base.converged
                        && base.closest >= JUPITER.planet_radius
                );
                let mut counts = r.runs.iter().map(|v| v.crossings).collect::<Vec<_>>();
                counts.sort_unstable();
                assert!(counts[4] >= CROSSINGS_MIN);
                Kept {
                    ship: r.bits.map(f64::from_bits),
                    crossings: base.crossings,
                    converged: base.converged,
                    closest: base.closest,
                    fate_safe: r.runs.iter().all(|v| v.closest >= JUPITER.planet_radius),
                }
            })
            .collect()
    })
}

/// Optional externally established window bounds, in sample intervals. No bound is
/// inferred from the candidate law's score. Missing bounds forbid qualification.
#[derive(serde::Deserialize)]
struct WindowBound {
    p_max_samples: u64,
    tau_c_samples: u64,
    #[serde(default)]
    reference_periods: u64,
    #[serde(default)]
    closest_planet_radius_q40: u64,
}
fn window_bounds() -> Option<Vec<WindowBound>> {
    let path = std::env::var_os("B12_WINDOW_FILE")?;
    serde_json::from_slice(&std::fs::read(path).ok()?).ok()
}
fn window_valid(b: &WindowBound) -> bool {
    let n = (PERIODS * COARSE) as u64;
    b.p_max_samples > 0
        && b.tau_c_samples > 0
        && b.p_max_samples <= n / 4
        && b.tau_c_samples <= n / 16
}

pub fn b12(law: &dyn Law) -> Gate {
    use super::b12_instruments::{self as instrument, Verdict};
    let _quiet = super::scale::QUIET
        .read()
        .unwrap_or_else(|e| e.into_inner());
    let times = coarse_times(&JUPITER);
    let bounds = window_bounds();
    let domain_verified = bounds
        .as_ref()
        .is_some_and(|v| v.len() == KEEP && v.iter().all(window_valid));
    let mut ships = Vec::new();
    let mut injected = Vec::new();
    let mut injection_bad = 0;
    for (ordinal, k) in kept().iter().enumerate() {
        // Preserve v2's explicit surface-fate split, not an invented continuation
        // of a law's destroyed body. This corpus is assessed at 200 P only.
        let scene = Restricted {
            planet_radius: if k.fate_safe {
                JUPITER.planet_radius
            } else {
                0.0
            },
            ..JUPITER
        };
        let states = law.restricted(&scene, k.ship, &times).unwrap_or_default();
        let series = integer_series(&scene, k.ship, &times, &states).unwrap_or_default();
        let reading = instrument::judge(ordinal, &series);
        if reading.n == times.len() {
            match b12_stat::inject_leak(&scene, k.ship, &times, &states, DETECTABLE_LEAK)
                .and_then(|v| integer_series(&scene, k.ship, &times, &v))
            {
                Some(v) => {
                    let inj = instrument::judge(ordinal, &v);
                    eprintln!("b12_injection {}", serde_json::to_string(&inj).unwrap());
                    injected.push(inj);
                }
                None => injection_bad += 1,
            }
        }
        eprintln!("b12_ship {}", serde_json::to_string(&reading).unwrap());
        ships.push(reading);
    }
    let missing = ships.iter().filter(|s| s.n != times.len()).count();
    let both_fail = ships
        .iter()
        .filter(|s| s.allan.verdict == Verdict::Fail && s.alpha.verdict == Verdict::Fail)
        .count();
    let disagreement = ships.iter().filter(|s| s.disagreement).count();
    let cap_fail = ships.iter().filter(|s| !s.envelope_pass).count();
    let readings_pass = ships.len() == KEEP && ships.iter().all(|s| s.verdict == Verdict::Pass);
    let sensitivity = injected.len() == KEEP
        && injection_bad == 0
        && injected
            .iter()
            .all(|s| s.allan.verdict == Verdict::Fail && s.alpha.verdict == Verdict::Fail);
    // The law row supplies no P_max/tau_c bounds, and the reused corpus is not
    // yet requalified at 10,000 P. Readings are reportable; PASS is not a freeze.
    let extended_corpus_verified = bounds.as_ref().is_some_and(|v| {
        v.len() == KEEP
            && v.iter().all(|b| {
                b.reference_periods >= PERIODS as u64
                    && b.closest_planet_radius_q40 >= super::b12_instruments::SCALE as u64
            })
    });
    let pass = readings_pass && domain_verified && extended_corpus_verified;
    let nominal_min = kept().iter().map(|k| k.crossings).min().unwrap_or(0);
    let nominal_closest = kept()
        .iter()
        .map(|k| k.closest / JUPITER.planet_radius)
        .fold(f64::INFINITY, f64::min);
    let nominal_converged = kept().iter().filter(|k| k.converged).count();
    let worst = ships.iter().map(|s| s.error_q40).max().unwrap_or(0);
    let stats = |which: bool| {
        let count = ships
            .iter()
            .filter(|s| (if which { &s.allan } else { &s.alpha }).verdict == Verdict::Fail)
            .count();
        let mut v = ships
            .iter()
            .filter_map(|s| (if which { &s.allan } else { &s.alpha }).value)
            .collect::<Vec<_>>();
        v.sort_by(f64::total_cmp);
        let median = if v.is_empty() {
            None
        } else if v.len() % 2 == 0 {
            Some((v[v.len() / 2 - 1] + v[v.len() / 2]) / 2.0)
        } else {
            Some(v[v.len() / 2])
        };
        serde_json::json!({"n":ships.len(),"fail":count,"numeric_n":v.len(),"zero_short_variance":ships.iter().filter(|s| (if which { &s.allan } else { &s.alpha }).denominator == "0").count(),"infinite_ratio":ships.iter().filter(|s| { let r=if which { &s.allan } else { &s.alpha }; r.denominator=="0" && r.numerator!="0" }).count(),"worst_finite":v.last(),"median_finite":median})
    };
    let detail = format!("handoffs v3: {KEEP} recorded ships; horizon {PERIODS} P; signed relative Jacobi Q40; worst err {:.2e} (integer cap 1/10000); {missing} missing/junk, {both_fail} both-fail, {disagreement} instrument disagreements, {cap_fail} envelope failures; Allan R1 {}; alpha top {}; window domain {} (T >= 4 P_max, T >= 16 tau_c); corpus provenance: assessed at 200 P (crossings min {nominal_min}, closest {nominal_closest:.2} Rp, converged {nominal_converged}/{KEEP}), extended-horizon surface domain UNVERIFIED; injected 2e-10/horizon: {} ({injection_bad} undelivered); readings {}; NOT QUALIFIED", worst as f64 / instrument::SCALE as f64, stats(true), stats(false), if domain_verified {"VERIFIED"} else {"UNVERIFIED"}, if sensitivity {"RESOLVED"} else {"UNSUPPORTED"}, if readings_pass {"PASS"} else if both_fail > 0 || cap_fail > 0 {"FAIL"} else {"UNRESOLVED"});
    Gate {
        id: "B12",
        pass,
        detail,
        secs: 0.0,
    }
}

fn integer_series(
    scene: &Restricted,
    ship: [f64; 4],
    times: &[f64],
    states: &[[f64; 4]],
) -> Option<Vec<i64>> {
    if states.len() != times.len() || states.iter().flatten().any(|v| !v.is_finite()) {
        return None;
    }
    let c0 = scene.jacobi(0.0, &ship);
    times
        .iter()
        .zip(states)
        .map(|(&t, s)| super::b12_instruments::integerize((scene.jacobi(t, s) - c0) / c0.abs()))
        .collect()
}

// Reference corpus producer, used only by the ignored, sharded reproduction test.
#[cfg(test)]
struct Assessed {
    crossings: usize,
    converged: bool,
    closest: f64,
}
#[cfg(test)]
fn watch(scene: &Restricted, ship: [f64; 4], rtol: f64) -> Option<(usize, Vec<f64>, f64)> {
    let mut it = Integrator::new(scene, Model::Full, rtol, ship).tracking();
    let (mut inside, mut crossings, mut jacobi) = (None, 0, Vec::new());
    for j in 0..=CORPUS_PERIODS * FINE {
        let t = j as f64 * scene.period() / FINE as f64;
        let state = it.advance(t)?;
        let now = scene.planet_distance(t, &state) < scene.soi();
        crossings += inside.is_some_and(|before| before != now) as usize;
        inside = Some(now);
        if j % (FINE / COARSE) == 0 {
            jacobi.push(scene.jacobi(t, &state));
        }
    }
    Some((crossings, jacobi, it.closest()))
}
#[cfg(test)]
fn assess(scene: &Restricted, ship: [f64; 4]) -> Option<Assessed> {
    let times = (0..=CORPUS_PERIODS * COARSE)
        .map(|j| j as f64 * scene.period() / COARSE as f64)
        .collect::<Vec<_>>();
    let (crossings, reference, closest) = watch(scene, ship, RTOL)?;
    let c0 = scene.jacobi(0.0, &ship);
    let mut fine = Integrator::new(scene, Model::Full, RTOL_FINE, ship).tracking();
    let finer = times
        .iter()
        .map(|&t| fine.advance(t))
        .collect::<Option<Vec<_>>>();
    let converged = finer.is_some_and(|f| {
        f.iter()
            .zip(&times)
            .zip(&reference)
            .all(|((s, &t), &c)| ((scene.jacobi(t, s) - c) / c0).abs() <= CONVERGED)
    });
    Some(Assessed {
        crossings,
        converged,
        closest: closest.min(fine.closest()),
    })
}

#[cfg(test)]
mod tests {
    use super::super::laws::{Events, Silent};
    use super::*;
    fn events(
        f: impl Fn(&Restricted, [f64; 4], &[f64]) -> Option<Vec<[f64; 4]>> + 'static,
    ) -> Events {
        Events {
            binary: Box::new(Some),
            restricted: Box::new(f),
        }
    }
    #[test]
    fn b12_window_bounds_are_required_and_equalities_are_valid() {
        assert!(window_valid(&WindowBound {
            reference_periods: 10_000,
            closest_planet_radius_q40: 1 << 40,
            p_max_samples: 20_000,
            tau_c_samples: 5_000
        }));
        assert!(!window_valid(&WindowBound {
            reference_periods: 10_000,
            closest_planet_radius_q40: 1 << 40,
            p_max_samples: 20_001,
            tau_c_samples: 5_000
        }));
        assert!(!window_valid(&WindowBound {
            reference_periods: 10_000,
            closest_planet_radius_q40: 1 << 40,
            p_max_samples: 20_000,
            tau_c_samples: 5_001
        }));
        assert!(!window_valid(&WindowBound {
            reference_periods: 10_000,
            closest_planet_radius_q40: 1 << 40,
            p_max_samples: 0,
            tau_c_samples: 0
        }));
    }
    #[test]
    fn b12_invalid_answers_fail_closed() {
        for law in [
            &Silent as &dyn Law,
            &events(|_, _, _| Some(vec![])),
            &events(|_, _, times| Some(vec![[f64::NAN; 4]; times.len()])),
            &events(|_, _, times| Some(vec![[f64::MAX; 4]; times.len()])),
        ] {
            assert!(!b12(law).pass);
        }
    }
    #[test]
    fn b12_corpus_is_exact_and_busy_and_classifies_fate_without_a_live_reference() {
        assert_eq!(kept().len(), KEEP);
        assert!(kept().iter().all(|k| k.converged
            && k.crossings >= CROSSINGS_MIN
            && k.ship.iter().all(|s| s.is_finite())));
        let mut words = kept()
            .iter()
            .map(|k| k.ship.map(f64::to_bits))
            .collect::<Vec<_>>();
        words.sort();
        words.dedup();
        assert_eq!(words.len(), KEEP);
        // The old platform-sensitive search is no longer on the gate path.
        assert!(kept().iter().any(|k| !k.fate_safe));
    }
    #[test]
    #[ignore = "candidate corpus producer; 32 candidates per invocation, no law consulted"]
    fn b12_reference_corpus_batch() {
        let first: usize = std::env::var("B12_FIRST")
            .unwrap_or("0".into())
            .parse()
            .unwrap();
        let draws = sample::handoffs(first + 32);
        let mut rows = Vec::new();
        for (idx, &(side, k, alpha)) in draws.iter().enumerate().skip(first) {
            let s = ship(&JUPITER, side, k, alpha);
            let primary = assess(&JUPITER, s).unwrap();
            if primary.crossings < CROSSINGS_MIN
                || !primary.converged
                || primary.closest < JUPITER.planet_radius
            {
                continue;
            }
            let mut variants = vec![s];
            for word in 0..4 {
                for offset in [1i64, -1] {
                    let mut v = s;
                    v[word] = f64::from_bits((s[word].to_bits() as i64 + offset) as u64);
                    variants.push(v);
                }
            }
            let mut runs = Vec::new();
            for v in variants {
                let a = assess(&JUPITER, v).unwrap();
                runs.push(serde_json::json!({"crossings":a.crossings, "converged":a.converged, "closest":a.closest}));
            }
            rows.push(serde_json::json!({"draw":idx,"bits":s.map(f64::to_bits),"runs":runs}));
        }
        let dir = "artifacts/runs/cx-b12-v2";
        std::fs::write(
            format!("{dir}/repro-corpus-{first}.json"),
            serde_json::to_vec_pretty(&rows).unwrap(),
        )
        .unwrap();
    }
}
