//! B12 candidate: conditional error growth over 200 planet periods, not a
//! power fit to a level. See docs/b12-statistic.md for the finite claim,
//! detector assumptions, resolution, and the still-required red-team.
#[cfg(test)]
use super::restricted::{Integrator, Model, RTOL, RTOL_FINE};
use super::restricted::{Restricted, JUPITER};
#[cfg(test)]
use super::sample;
use super::{b12_stat, Gate, Law};
use std::sync::OnceLock;

pub const PERIODS: usize = 200;
pub const COARSE: usize = 8;
#[cfg(test)]
pub const FINE: usize = 256;
pub const KEEP: usize = 16;
pub const CROSSINGS_MIN: usize = 20;
pub const ERR_MAX: f64 = 1e-4;
pub const FLOOR: f64 = 1e-12;
#[cfg(test)]
pub const CONVERGED: f64 = 1e-9;
pub const EXCLUDED_MAX: f64 = 0.1;
/// One resolvable relative invariant quantum leaking per planet period.
pub const DETECTABLE_LEAK: f64 = FLOOR * PERIODS as f64;
/// Standard-normal five-sigma reference score. This is NOT a confidence level
/// for correlated returns; the candidate's exchangeability premise needs review.
pub const ARROW_MAX: f64 = 5.0;

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

pub fn b12(law: &dyn Law) -> Gate {
    let _quiet = super::scale::QUIET
        .read()
        .unwrap_or_else(|e| e.into_inner());
    let times = coarse_times(&JUPITER);
    let mut stats = Vec::new();
    let mut injected_stats = Vec::new();
    let mut injection_bad = 0;
    let (mut unresolved, mut bad, mut stable_fate_fail) = (0, 0, 0);
    for k in kept() {
        // Growth needs an uninterrupted history, and is logically separate
        // from destruction at a surface. A split reference fate gets the
        // point-mass scene; no predicted surviving fate is imposed on it.
        let scene = Restricted {
            planet_radius: if k.fate_safe {
                JUPITER.planet_radius
            } else {
                0.0
            },
            ..JUPITER
        };
        let states = law.restricted(&scene, k.ship, &times).unwrap_or_default();
        let st = b12_stat::arrow(&scene, k.ship, &times, &states);
        stable_fate_fail += (st.bad && k.fate_safe) as usize;
        bad += st.bad as usize;
        unresolved += (!st.bad && st.above_floor && st.n < 3) as usize;
        // Sensitivity belongs to this law's histories, not only to echo's.
        // Failure to see the declared leak means UNSUPPORTED, not no growth.
        if !st.bad {
            match b12_stat::inject_leak(&scene, k.ship, &times, &states, DETECTABLE_LEAK) {
                Some(injected) => {
                    injected_stats.push(b12_stat::arrow(&scene, k.ship, &times, &injected))
                }
                None => injection_bad += 1,
            }
        }
        stats.push(st);
    }
    let worst = stats.iter().map(|s| s.worst).fold(0.0f64, f64::max);
    let arrow = b12_stat::pooled_score(&stats);
    let injected_arrow = b12_stat::pooled_score(&injected_stats);
    let sensitivity =
        injection_bad == 0 && injected_stats.len() == KEEP && injected_arrow > ARROW_MAX;
    let complete = kept().len() == KEEP
        && kept().iter().all(|k| k.converged)
        && bad == 0
        && unresolved as f64 <= EXCLUDED_MAX * KEEP as f64;
    let pass = complete && arrow <= ARROW_MAX && worst <= ERR_MAX && sensitivity;
    let safe = kept().iter().filter(|k| k.fate_safe).count();
    let nominal_min = kept().iter().map(|k| k.crossings).min().unwrap_or(0);
    let nominal_max = kept().iter().map(|k| k.crossings).max().unwrap_or(0);
    let closest = kept()
        .iter()
        .map(|k| k.closest / JUPITER.planet_radius)
        .fold(f64::INFINITY, f64::min);
    let pairs = stats.iter().map(|s| s.n).sum::<usize>();
    let ties = stats.iter().map(|s| s.ties).sum::<usize>();
    let residual = stats.iter().map(|s| s.diff_med).fold(0.0f64, f64::max);
    let leak_fit = stats.iter().map(|s| s.leak.abs()).fold(0.0f64, f64::max);
    let gap = stats
        .iter()
        .map(|s| s.gap_mean)
        .filter(|s| s.is_finite())
        .fold(0.0f64, f64::max);
    let detail = format!("handoffs: {KEEP} recorded ships, nominal R_SOI crossings {nominal_min}..{nominal_max}, replica median >= {CROSSINGS_MIN}, closest primary reference {closest:.2} R_p; horizon {PERIODS} P, detectable linear leak {DETECTABLE_LEAK:.1e}/horizon; {safe} perturbation-stable surviving fates, {} split fates use uninterrupted point-mass histories; {bad} missing/junk, {stable_fate_fail} stable-fate failures, {unresolved} unresolved above-floor histories; conditional arrow {arrow:.3} (limit {ARROW_MAX}, NOT a correlated-return confidence level); worst err {worst:.2e} (limit {ERR_MAX:.0e}); pairs {pairs} ({ties} exact ties), maximum pair-gap mean {gap:.1} P, maximum ship median residual {residual:.2e}, maximum fitted leak {leak_fit:.2e}/horizon; injected leak arrow {injected_arrow:.3}, sensitivity {} ({injection_bad} undelivered injections); candidate, NOT FROZEN", KEEP-safe, if sensitivity { "RESOLVED" } else { "UNSUPPORTED" });
    Gate {
        id: "B12",
        pass,
        detail,
        secs: 0.0,
    }
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
    for j in 0..=PERIODS * FINE {
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
    let times = coarse_times(scene);
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
    use super::super::laws::{Echo, Events, Fault, Planted, Silent};
    use super::*;
    fn events(
        f: impl Fn(&Restricted, [f64; 4], &[f64]) -> Option<Vec<[f64; 4]>> + 'static,
    ) -> Events {
        Events {
            binary: Box::new(Some),
            restricted: Box::new(f),
        }
    }
    fn scaled(eps: f64) -> Events {
        events(move |scene, ship, times| {
            Some(
                Echo.restricted(scene, ship, times)?
                    .into_iter()
                    .map(|s| [s[0], s[1], s[2] * (1.0 + eps), s[3] * (1.0 + eps)])
                    .collect(),
            )
        })
    }
    fn leak(total: f64, bounded: bool) -> Events {
        events(move |scene, ship, times| {
            let law: &dyn Law = if bounded {
                &Planted(Fault::Bounded)
            } else {
                &Echo
            };
            let states = law.restricted(scene, ship, times)?;
            let c0 = scene.jacobi(0.0, &ship).abs();
            let shifts = times
                .iter()
                .map(|t| c0 * total * t / (PERIODS as f64 * scene.period()))
                .collect::<Vec<_>>();
            Some(super::super::laws::lay(scene, states, &shifts))
        })
    }
    #[test]
    fn b12_controls_both_sides() {
        for (name, law, want) in [
            ("echo", &Echo as &dyn Law, true),
            ("scaled", &scaled(1e-11), true),
            ("planted-bounded", &Planted(Fault::Bounded), true),
            ("planted-compound", &Planted(Fault::Compound), false),
            ("planted-drift", &Planted(Fault::Drift), false),
            ("planted-kick", &Planted(Fault::Kick), false),
            ("leak", &leak(DETECTABLE_LEAK, false), false),
            ("leak+bounded", &leak(DETECTABLE_LEAK, true), false),
        ] {
            let g = b12(law);
            println!(
                "{name}: {} {}",
                if g.pass { "PASS" } else { "FAIL" },
                g.detail
            );
            assert_eq!(g.pass, want, "{name}: {}", g.detail);
        }
    }
    #[test]
    fn b12_a_small_bounded_offset_must_not_hide_the_claimed_leak() {
        // A state-only velocity scaling 1000 times inside the absolute cap:
        // it may be quiet, but a PASS still requires resolving the stated leak.
        let g = b12(&scaled(ERR_MAX / 1000.0));
        assert!(
            !g.pass && g.detail.contains("sensitivity UNSUPPORTED"),
            "{}",
            g.detail
        );
        assert!(g.detail.contains("0 missing/junk"), "{}", g.detail);
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
    fn b12_fate_is_required_only_for_unanimous_surviving_replicas() {
        assert_eq!(kept().iter().filter(|k| k.fate_safe).count(), 1);
        let law = events(|scene, ship, times| {
            if scene.planet_radius > 0.0 {
                None
            } else {
                Echo.restricted(scene, ship, times)
            }
        });
        let g = b12(&law);
        assert!(
            !g.pass && g.detail.contains("1 stable-fate failures"),
            "{}",
            g.detail
        );
        let safe = kept().iter().find(|k| k.fate_safe).unwrap().ship;
        let law = events(move |scene, ship, times| {
            if ship != safe && scene.planet_radius > 0.0 {
                None
            } else {
                Echo.restricted(scene, ship, times)
            }
        });
        assert!(b12(&law).pass);
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
