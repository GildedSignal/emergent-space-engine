//! `behave`: the behaviour judge. It asks any gravity law around one static mass (G = c = M = 1,
//! the equatorial plane) for behaviours, over many seeds, and compares them with the float64 GR
//! oracle (docs/PRINCIPLES.md: behaviours over many seeds, error type over error size).
//! It knows no engine type and imports no physics crate: a law is anything that implements [`Law`].
//! G1-G6 mirror lab/rungs/r1-rings.md; B7, B9 and B10 are the law's clock, cost and scaling gates (docs/law.md).
//! B11-B14 judge the events layer: binaries (1PN oracle), handoffs (Jacobi constant), assists
//! (heliocentric energy and angular momentum) and Hill stability, the last three against the
//! float64 circular restricted three-body problem (`restricted`).
//!
//! ```text
//! cargo run --release -p xtask -- behave [--law echo|planted-precession|planted-walk|planted-nocapture|
//!     planted-clock|planted-steps|planted-quadratic|planted-newton|planted-kick|planted-notide|planted-drift]
//!     [--gates G1,B7,...]
//! ```
//! One line per gate, `G<n>` or `B<n> PASS|FAIL <numbers>`, between two `machine_state` lines.
//! `--gates` picks gates (default: all thirteen). Every phase is killed and reported as a failure
//! if it runs past 60 s. Exit 0 iff every gate that ran passes.
pub mod assist;
pub mod binary;
pub mod clocks;
pub mod cost;
pub mod fit;
pub mod handoff;
pub mod hill;
pub mod laws;
pub mod oracle;
pub mod restricted;
pub mod scale;
pub mod select;
pub mod sample;

use crate::measure::{machine_state, Watch};
use restricted::Restricted;
use crate::Result;
use std::time::{Duration, Instant};

/// What the judge asks of a gravity law. Units G = c = M = 1; angles in radians.
pub trait Law {
    /// One radial cycle of the bound orbit with semi-latus rectum p and eccentricity e:
    /// (periapsis advance, the angle beyond 2π; radial period in coordinate time; in proper time).
    fn advance_per_cycle(&self, p: f64, e: f64) -> Option<(f64, f64, f64)>;
    /// Light's deflection (total angle minus π) at impact parameter b, from and to infinity.
    fn deflection(&self, b: f64) -> Option<f64>;
    /// Is a body that arrives from infinity with energy E and angular momentum L (per unit mass) captured?
    fn captured(&self, energy: f64, angular: f64) -> bool;
    /// Is light with impact parameter b captured?
    fn photon_captured(&self, b: f64) -> bool;
    /// `cycles` radial cycles of the bound orbit (p, e) from periapsis: after each cycle, that
    /// cycle's (r_min, r_max, energy, angular momentum).
    fn long_run(&self, p: f64, e: f64, cycles: usize) -> Vec<(f64, f64, f64, f64)>;
    /// B7: dτ/dt of a static observer at r (units of M), derived and not stepped. None: not
    /// implemented, which fails the gate.
    fn static_clock_rate(&self, _r: f64) -> Option<f64> {
        None
    }
    /// B7: dτ/dt of a circular orbit at r > 3 (units of M). None: not implemented, which fails.
    fn circular_clock_rate(&self, _r: f64) -> Option<f64> {
        None
    }
    /// B9: band crossings the law spends on one radial cycle of the bound orbit (p, e). None: not
    /// implemented, which fails.
    fn crossings_per_cycle(&self, _p: f64, _e: f64) -> Option<f64> {
        None
    }
    /// B10: CPU seconds the law spends on a frozen scene: `n_bodies` bodies in one doll, orbits
    /// drawn from the seeds, no events beyond the orbits, advanced `game_seconds` (units of M). The
    /// cost includes building the scene. None: not implemented, which fails.
    fn scene_cost(&self, _n_bodies: usize, _game_seconds: f64) -> Option<f64> {
        None
    }
    /// B11: one radial cycle of a binary of total mass 1 and symmetric mass ratio nu, given its 1PN
    /// reduced energy and angular momentum (harmonic gauge, as `eih_invariants` returns them):
    /// (periapsis advance beyond 2π, radial period). None: not implemented, which fails.
    fn binary_cycle(&self, _energy: f64, _angular: f64, _nu: f64) -> Option<(f64, f64)> {
        None
    }
    /// B12-B14: a massless ship in the circular restricted three-body problem `scene`. From its
    /// barycentric inertial state (x, y, vx, vy) at t = 0, its states at each of `times` (ascending,
    /// all at least 0). None: not implemented, which fails.
    fn restricted(&self, _scene: &Restricted, _ship: [f64; 4], _times: &[f64]) -> Option<Vec<[f64; 4]>> {
        None
    }
}

const BOUND_SEEDS: usize = 256;
const LIGHT_SEEDS: usize = 64;
const LONG_SEEDS: usize = 32;
const LONG_CYCLES: usize = 10_000;
const ADVANCE_TOL: f64 = 1e-2;
const PERIOD_TOL: f64 = 1e-3;
const DEFLECTION_TOL: f64 = 1e-2;
const GROWTH_MAX: f64 = 0.2;
const SHAPE_TOL: f64 = 1e-2;
const CAPTURE_CASES: [f64; 6] = [0.5, 0.9, 0.97, 1.03, 1.1, 1.5];
const PHOTON_CASES: [f64; 4] = [0.9, 0.97, 1.03, 1.1];
/// A phase that runs past this is killed and reported as a failure.
const LIMIT: Duration = Duration::from_secs(60);

pub struct Gate {
    pub id: &'static str,
    pub pass: bool,
    pub detail: String,
    /// Wall time of the phase that computed it.
    pub secs: f64,
}

/// One bound orbit: the law's answer (None: it cannot answer) and the oracle's.
struct Orbit {
    law: Option<(f64, f64, f64)>,
    oracle: (f64, f64, f64),
}

fn rel(a: f64, b: f64) -> f64 {
    ((a - b) / b).abs()
}
/// The largest value; NaN if any is NaN (a failure must show).
fn worst(xs: impl Iterator<Item = f64>) -> f64 {
    xs.fold(0.0, |m, x| if m.is_nan() || x.is_nan() { f64::NAN } else { m.max(x) })
}
/// A gate that passes when at least 99% of the errors are within `tol` (NaN and unanswered fail).
fn within(id: &'static str, what: &str, errs: &[f64], tol: f64) -> Gate {
    let ok = errs.iter().filter(|&&e| e <= tol).count();
    let detail = format!("{what}: {ok}/{} within {tol:.0e}, worst {:.2e}", errs.len(), worst(errs.iter().copied()));
    Gate { id, pass: ok * 100 >= 99 * errs.len(), detail, secs: 0.0 }
}

fn bound_table(law: &dyn Law) -> Vec<Orbit> {
    sample::bound_orbits(BOUND_SEEDS)
        .into_iter()
        .map(|(p, e)| {
            let (t, tau) = oracle::radial_periods(p, e);
            Orbit { law: law.advance_per_cycle(p, e), oracle: (oracle::periapsis_advance(p, e), t, tau) }
        })
        .collect()
}

/// G1 precession: the advance per cycle, within 1% of the oracle for at least 99% of the seeds.
fn g1(rows: &[Orbit]) -> Gate {
    let errs: Vec<f64> = rows.iter().map(|r| r.law.map_or(f64::INFINITY, |l| rel(l.0, r.oracle.0))).collect();
    within("G1", "advance per cycle", &errs, ADVANCE_TOL)
}
/// G2 periods: the radial period in coordinate and in proper time, within 0.1% for at least 99%.
fn g2(rows: &[Orbit]) -> Gate {
    let errs: Vec<f64> = rows.iter().map(|r| r.law.map_or(f64::INFINITY, |l| rel(l.1, r.oracle.1).max(rel(l.2, r.oracle.2)))).collect();
    within("G2", "radial periods", &errs, PERIOD_TOL)
}
/// G3 deflection: light's deflection over 64 impact parameters, within 1% for at least 99%.
fn g3(law: &dyn Law) -> Gate {
    let errs: Vec<f64> = sample::light_impacts(LIGHT_SEEDS).into_iter().map(|b| law.deflection(b).map_or(f64::INFINITY, |d| rel(d, oracle::deflection(b)))).collect();
    within("G3", "deflection", &errs, DEFLECTION_TOL)
}
/// G4 capture: E = 1 bodies at L/4 in {0.5 .. 1.5}, light at b/b_c in {0.9 .. 1.1}: captured iff below 1.
fn g4(law: &dyn Law) -> Gate {
    let mut wrong = Vec::new();
    for x in CAPTURE_CASES {
        if law.captured(1.0, x * oracle::capture_angular(1.0)) != (x < 1.0) {
            wrong.push(format!("L/4={x}"));
        }
    }
    for x in PHOTON_CASES {
        if law.photon_captured(x * oracle::photon_critical_b()) != (x < 1.0) {
            wrong.push(format!("b/bc={x}"));
        }
    }
    let n = CAPTURE_CASES.len() + PHOTON_CASES.len();
    Gate { id: "G4", pass: wrong.is_empty(), detail: format!("capture: {} of {n} misclassified {wrong:?}", wrong.len()), secs: 0.0 }
}
/// G5 long-run type: over 10^4 cycles the growth exponents of the energy and angular momentum
/// errors are at most 0.2, and r_min and r_max stay within 1% of their first values.
fn g5(law: &dyn Law) -> Gate {
    let (mut ok, mut short) = (0, 0);
    let (mut grow_e, mut grow_l, mut shape) = (Vec::new(), Vec::new(), Vec::new());
    for (p, e) in sample::bound_orbits(LONG_SEEDS) {
        let run = law.long_run(p, e, LONG_CYCLES);
        if run.len() != LONG_CYCLES {
            short += 1;
            continue;
        }
        let first = run[0];
        let drift = |pick: fn(&(f64, f64, f64, f64)) -> f64| -> Vec<f64> { run.iter().map(|c| rel(pick(c), pick(&first))).collect() };
        let (ge, gl) = (fit::growth_exponent(&drift(|c| c.2)), fit::growth_exponent(&drift(|c| c.3)));
        let sh = worst(drift(|c| c.0).into_iter().chain(drift(|c| c.1)));
        ok += (ge <= GROWTH_MAX && gl <= GROWTH_MAX && sh <= SHAPE_TOL) as usize;
        grow_e.push(ge);
        grow_l.push(gl);
        shape.push(sh);
    }
    let detail = format!(
        "long run: {ok}/{LONG_SEEDS} seeds over {LONG_CYCLES} cycles ({short} short), worst growth E {:.3} L {:.3} (limit {GROWTH_MAX}), worst shape drift {:.2e} (limit {SHAPE_TOL:.0e})",
        worst(grow_e.into_iter()),
        worst(grow_l.into_iter()),
        worst(shape.into_iter())
    );
    Gate { id: "G5", pass: ok * 100 >= 99 * LONG_SEEDS, detail, secs: 0.0 }
}
/// G6 prograde: every seed's advance is positive.
fn g6(rows: &[Orbit]) -> Gate {
    let ok = rows.iter().filter(|r| r.law.is_some_and(|l| l.0 > 0.0)).count();
    Gate { id: "G6", pass: ok == rows.len(), detail: format!("prograde: {ok}/{} advances positive", rows.len()), secs: 0.0 }
}

/// Runs the gates of the single-mass core (`select::CORE`) on `law`, arming `watch` on each phase and
/// calling `emit` as each gate lands. The CLI runs all thirteen through `judge_only`.
#[allow(dead_code)] // the core entry point: the CLI goes through `judge_only`
pub fn judge(law: &dyn Law, watch: Option<&Watch>, emit: impl FnMut(&Gate)) -> Vec<Gate> {
    judge_only(law, watch, Some(&select::CORE), emit)
}

/// `judge` restricted to the gates named in `only` (None: all); a phase none of whose gates is wanted is skipped.
pub fn judge_only(law: &dyn Law, watch: Option<&Watch>, only: Option<&[&str]>, mut emit: impl FnMut(&Gate)) -> Vec<Gate> {
    let want = |id: &str| only.map_or(true, |o| o.contains(&id));
    let mut out = Vec::new();
    let mut phase = |label: &str, work: &mut dyn FnMut() -> Vec<Gate>| {
        let label = label.split(' ').filter(|id| want(id)).collect::<Vec<_>>().join(" ");
        if label.is_empty() {
            return;
        }
        if let Some(w) = watch {
            w.arm(&label);
        }
        let t = Instant::now();
        let mut gates = work();
        gates.retain(|g| want(g.id));
        let secs = t.elapsed().as_secs_f64();
        if let Some(w) = watch {
            w.disarm();
        }
        for g in &mut gates {
            g.secs = secs;
            emit(g);
        }
        out.extend(gates);
    };
    let mut rows = Vec::new();
    phase("G1 G2 G6", &mut || {
        rows = bound_table(law);
        vec![g1(&rows), g2(&rows)]
    });
    phase("G3", &mut || vec![g3(law)]);
    phase("G4", &mut || vec![g4(law)]);
    phase("G5", &mut || vec![g5(law)]);
    phase("G6", &mut || vec![g6(&rows)]);
    phase("B7", &mut || vec![clocks::b7(law)]);
    phase("B9", &mut || vec![cost::b9(law)]);
    phase("B10", &mut || vec![scale::b10(law)]);
    phase("B11", &mut || vec![binary::b11(law)]);
    phase("B12", &mut || vec![handoff::b12(law)]);
    phase("B13", &mut || vec![assist::b13(law)]);
    phase("B14", &mut || vec![hill::b14(law)]);
    out
}

const USAGE: &str = "usage: behave [--law echo|planted-precession|planted-walk|planted-nocapture|planted-clock|planted-steps|planted-quadratic|planted-newton|planted-kick|planted-notide|planted-drift] [--gates G1,G2,G3,G4,G5,G6,B7,B9,B10,B11,B12,B13,B14]";

pub fn run(args: Vec<String>) -> Result<u8> {
    let cli = select::parse(&args).map_err(|e| format!("{e}; {USAGE}"))?;
    let name = cli.law.as_str();
    let law = laws::by_name(name).ok_or_else(|| format!("unknown law {name:?}; {USAGE}"))?;
    println!("machine_state {}", machine_state("start"));
    let watch = Watch::spawn(LIMIT, |label, secs| {
        for id in label.split(' ') {
            println!("{id} FAIL timeout: {secs:.1} s over the {} s limit", LIMIT.as_secs());
        }
        println!("machine_state {}", machine_state("end"));
        std::process::exit(1);
    });
    let gates = judge_only(&*law, Some(&watch), cli.gates.as_deref(), |g| println!("{} {} {} [{:.2} s]", g.id, if g.pass { "PASS" } else { "FAIL" }, g.detail, g.secs));
    println!("machine_state {}", machine_state("end"));
    let failed: Vec<&str> = gates.iter().filter(|g| !g.pass).map(|g| g.id).collect();
    let picked = cli.gates.as_ref().map_or(String::new(), |g| format!(" ({})", g.join(" ")));
    println!("behave {name}{picked}: {}", if failed.is_empty() { "PASS".to_string() } else { format!("FAIL {}", failed.join(" ")) });
    Ok(if failed.is_empty() { 0 } else { 1 })
}

#[cfg(test)]
mod tests {
    use super::laws::{Echo, Fault, Planted};
    use super::*;

    fn failing(law: &dyn Law) -> Vec<&'static str> {
        judge(law, None, |_| {}).iter().filter(|g| !g.pass).map(|g| g.id).collect()
    }

    /// The oracle with a hook on each answer, to plant flaws that are not in the CLI.
    struct Hooked {
        advance: fn((f64, f64, f64)) -> (f64, f64, f64),
        deflection: fn(f64) -> f64,
    }
    impl Law for Hooked {
        fn advance_per_cycle(&self, p: f64, e: f64) -> Option<(f64, f64, f64)> {
            Echo.advance_per_cycle(p, e).map(self.advance)
        }
        fn deflection(&self, b: f64) -> Option<f64> {
            Echo.deflection(b).map(self.deflection)
        }
        fn captured(&self, energy: f64, angular: f64) -> bool {
            Echo.captured(energy, angular)
        }
        fn photon_captured(&self, b: f64) -> bool {
            Echo.photon_captured(b)
        }
        fn long_run(&self, p: f64, e: f64, cycles: usize) -> Vec<(f64, f64, f64, f64)> {
            Echo.long_run(p, e, cycles)
        }
        fn static_clock_rate(&self, r: f64) -> Option<f64> {
            Echo.static_clock_rate(r)
        }
        fn circular_clock_rate(&self, r: f64) -> Option<f64> {
            Echo.circular_clock_rate(r)
        }
        fn crossings_per_cycle(&self, p: f64, e: f64) -> Option<f64> {
            Echo.crossings_per_cycle(p, e)
        }
        fn scene_cost(&self, n: usize, game_seconds: f64) -> Option<f64> {
            Echo.scene_cost(n, game_seconds)
        }
    }

    #[test]
    fn echo_passes_every_gate() {
        let gates = judge(&Echo, None, |_| {});
        assert_eq!(gates.iter().map(|g| g.id).collect::<Vec<_>>(), ["G1", "G2", "G3", "G4", "G5", "G6", "B7", "B9", "B10"]);
        for g in &gates {
            assert!(g.pass, "{} {}", g.id, g.detail);
        }
    }

    #[test]
    fn each_planted_law_fails_exactly_its_gate() {
        assert_eq!(failing(&Planted(Fault::Precession)), ["G1"]);
        assert_eq!(failing(&Planted(Fault::NoCapture)), ["G4"]);
        assert_eq!(failing(&Planted(Fault::Walk)), ["G5"]);
        assert_eq!(failing(&Planted(Fault::Clock)), ["B7"]);
        assert_eq!(failing(&Planted(Fault::Steps)), ["B9"]);
        assert_eq!(failing(&Planted(Fault::Quadratic)), ["B10"]);
    }

    #[test]
    fn a_law_that_implements_none_of_the_new_gates_fails_exactly_them() {
        // The trait defaults are "not implemented": B7, B9 and B10 fail, the six older gates do not.
        struct Old;
        impl Law for Old {
            fn advance_per_cycle(&self, p: f64, e: f64) -> Option<(f64, f64, f64)> {
                Echo.advance_per_cycle(p, e)
            }
            fn deflection(&self, b: f64) -> Option<f64> {
                Echo.deflection(b)
            }
            fn captured(&self, energy: f64, angular: f64) -> bool {
                Echo.captured(energy, angular)
            }
            fn photon_captured(&self, b: f64) -> bool {
                Echo.photon_captured(b)
            }
            fn long_run(&self, p: f64, e: f64, cycles: usize) -> Vec<(f64, f64, f64, f64)> {
                Echo.long_run(p, e, cycles)
            }
        }
        assert_eq!(failing(&Old), ["B7", "B9", "B10"]);
    }

    #[test]
    fn gates_can_be_picked_and_only_they_run() {
        let ids = |only: &[&str]| judge_only(&Echo, None, Some(only), |_| {}).iter().map(|g| g.id).collect::<Vec<_>>();
        assert_eq!(ids(&["B7"]), ["B7"]);
        assert_eq!(ids(&["B10", "G3", "B9"]), ["G3", "B9", "B10"]);
        assert_eq!(ids(&["G6"]), ["G6"]);
        assert_eq!(ids(&["G1", "G2"]), ["G1", "G2"]);
        assert_eq!(judge_only(&Planted(Fault::Clock), None, Some(&["B9"]), |_| {}).iter().filter(|g| !g.pass).count(), 0);
    }

    #[test]
    fn the_other_gates_can_fail_too() {
        // G2: the coordinate period 0.5% long. G3: deflection 2% short.
        assert_eq!(failing(&Hooked { advance: |(a, t, s)| (a, t * 1.005, s), deflection: |d| d }), ["G2"]);
        assert_eq!(failing(&Hooked { advance: |a| a, deflection: |d| d * 0.98 }), ["G3"]);
        // G6 alone: two retrograde orbits in 256 leave G1 above its 99% bar.
        let mut rows = bound_table(&Echo);
        rows[0].law = rows[0].law.map(|(a, t, s)| (-a, t, s));
        rows[100].law = None;
        assert!(g1(&rows).pass && !g6(&rows).pass);
    }

    #[test]
    fn the_cli_refuses_unknown_laws_and_arguments() {
        assert!(run(vec!["--law".into(), "newton".into()]).is_err());
        assert!(run(vec!["--verbose".into()]).is_err());
        assert!(run(vec!["--gates".into(), "B8".into()]).is_err());
    }
}

/// The events layer's gates, B11-B14, judged together (the old tests above are for the core).
#[cfg(test)]
mod events_tests {
    use super::laws::{Echo, Fault, Planted, Silent};
    use super::*;

    const EVENTS: [&str; 4] = ["B11", "B12", "B13", "B14"];

    fn failing(law: &dyn Law) -> Vec<&'static str> {
        let gates = judge_only(law, None, Some(&EVENTS), |_| {});
        assert_eq!(gates.iter().map(|g| g.id).collect::<Vec<_>>(), EVENTS);
        gates.iter().filter(|g| !g.pass).map(|g| g.id).collect()
    }

    #[test]
    fn echo_passes_the_four_events_gates_with_the_evidence_on_each_line() {
        let gates = judge_only(&Echo, None, Some(&EVENTS), |_| {});
        assert_eq!(gates.iter().map(|g| (g.id, g.pass)).collect::<Vec<_>>(), EVENTS.map(|id| (id, true)));
        let detail = |id: &str| gates.iter().find(|g| g.id == id).unwrap().detail.clone();
        assert!(detail("B11").contains("precession 1024/1024"));
        assert!(detail("B12").contains("16 frozen ships") && detail("B12").contains("worst err "), "{}", detail("B12"));
        assert!(detail("B13").contains("64/64 judged") && detail("B13").contains("0 of 64 excluded"), "{}", detail("B13"));
        assert!(detail("B14").contains("escape") && !detail("B14").contains("(0 escape") && !detail("B14").contains(", 0 stay"), "{}", detail("B14"));
    }

    // The failing sets are what the planted laws deterministically do; each contains the gate it is for.
    #[test]
    fn planted_newton_fails_b11_and_answers_the_rest_as_echo_does() {
        assert_eq!(judge_only(&Planted(Fault::Newton), None, Some(&["B11"]), |_| {}).iter().filter(|g| !g.pass).count(), 1);
        // B12-B14 read only `restricted`, which Newton leaves to echo: the same answers, so the same verdicts.
        let ship = [1.1 * restricted::JUPITER.sep, 0.0, 0.0, (1.1 * restricted::JUPITER.sep).powf(-0.5)];
        let times = [1e12, 2e13];
        assert_eq!(Planted(Fault::Newton).restricted(&restricted::JUPITER, ship, &times), Echo.restricted(&restricted::JUPITER, ship, &times));
    }

    #[test]
    fn planted_kick_fails_b12_b13_and_b14() {
        assert_eq!(failing(&Planted(Fault::Kick)), ["B12", "B13", "B14"]);
    }

    #[test]
    fn planted_notide_fails_b12_b13_and_b14() {
        assert_eq!(failing(&Planted(Fault::NoTide)), ["B12", "B13", "B14"]);
    }

    #[test]
    fn planted_drift_fails_b12_alone() {
        assert_eq!(failing(&Planted(Fault::Drift)), ["B12"]);
    }

    #[test]
    fn a_law_that_implements_none_of_the_events_gates_fails_exactly_them() {
        // The trait defaults are "not implemented": B11-B14 fail (the core gates are `Old`'s test above).
        assert_eq!(failing(&Silent), EVENTS);
    }

    #[test]
    fn the_default_run_is_all_thirteen_gates_and_a_law_without_the_new_methods_fails_b7_b9_b10_and_b11_to_b14_in_it() {
        // `--gates` omitted is `only = None`: every gate, in the judge's order.
        let gates = judge_only(&Silent, None, None, |_| {});
        assert_eq!(gates.iter().map(|g| g.id).collect::<Vec<_>>(), select::ALL);
        assert_eq!(gates.iter().filter(|g| !g.pass).map(|g| g.id).collect::<Vec<_>>(), ["B7", "B9", "B10", "B11", "B12", "B13", "B14"]);
    }

    #[test]
    fn the_events_gates_run_only_when_named_and_in_the_judges_order() {
        let ids = |only: &[&str]| judge_only(&Echo, None, Some(only), |_| {}).iter().map(|g| g.id).collect::<Vec<_>>();
        assert_eq!(ids(&["B13", "B11"]), ["B11", "B13"]);
    }
}
