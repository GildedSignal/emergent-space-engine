//! `behave`: the behaviour judge. It asks any gravity law around one static mass (G = c = M = 1,
//! the equatorial plane) for behaviours, over many seeds, and compares them with the float64 GR
//! oracle (docs/PRINCIPLES.md: behaviours over many seeds, error type over error size).
//! It knows no engine type and imports no physics crate: a law is anything that implements [`Law`].
//! G1-G6 mirror lab/rungs/r1-rings.md; B7, B9 and B10 are the law's clock, cost and scaling gates (docs/law.md).
//! B11-B14 judge the events layer: binaries (1PN oracle), handoffs (Jacobi constant), assists
//! (heliocentric energy and angular momentum) and Hill stability (the class, and the apsides of
//! eccentric births), the last three against the float64 circular restricted three-body problem
//! (`restricted`). B9 is log-scaled to e = 0.99. B16-B18 come from the law's red-team (1 October):
//! moving lenses (a boosted Kerr-Schild geodesic oracle), resonance (r4 v3's cases as restricted
//! scenes) and memory (bytes per body on the shipmem ladder). B18b is the belt case of B18 (a belt born as a
//! program: `belt.rs`). B19 (5 October) judges rotating holes
//! against equatorial Kerr geodesics in float64 (`kerr`, cross-checked by `kerr_mpmath.py`).
//!
//! ```text
//! cargo run --release -p xtask -- behave [--law echo|planted-precession|planted-walk|planted-nocapture|
//!     planted-clock|planted-steps|planted-quadratic|planted-newton|planted-kick|planted-notide|planted-drift|planted-swollen|
//!     planted-linear|planted-apsides|planted-static|planted-flipped|planted-average|planted-bounded|planted-fat|iid-blocks|dyadic-belt|
//!     planted-belt-clipped|planted-belt-winsor|planted-belt-repeat|planted-belt-serial|planted-belt-thread|
//!     planted-belt-fat|planted-belt-ships|planted-belt-lattice|planted-belt-fatscars|planted-belt-crush|planted-belt-innerclip|planted-belt-aligned|
//!     planted-belt-table20|planted-nodrag|planted-isco|planted-penrose|planted-proonly|planted-rcapture]
//!     [--gates G1,B7,...]
//! ```
//! One line per gate, `G<n>` or `B<n> PASS|FAIL <numbers>`, between two `machine_state` lines.
//! `--gates` picks gates (default: all eighteen). Every phase is killed and reported as a failure
//! if it runs past 60 s. Exit 0 iff every gate that ran passes.
pub mod assist;
pub mod belt;
pub mod binary;
pub mod clocks;
pub mod cost;
pub mod fit;
pub mod handoff;
pub mod hill;
pub mod kerr;
pub mod laws;
pub mod lens;
pub mod memory;
pub mod plane;
pub mod oracle;
pub mod resonance;
pub mod restricted;
pub mod rotating;
pub mod scale;
pub mod select;
pub mod sample;
pub mod space;

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
    /// B16: the observed deflection of light passing a lens that moves: the signed angle, in the
    /// observer's frame, from the light's incoming direction to its outgoing one. None: not
    /// implemented, which fails the gate.
    fn moving_deflection(&self, _lens: &lens::MovingLens) -> Option<f64> {
        None
    }
    /// B18: bytes the law holds per live body on a scene of the shipmem population ladder: the tube,
    /// the catalogue's share, the event records and the remainders. None: not implemented, which fails.
    fn bytes_per_body(&self, _scene: &memory::MemoryScene) -> Option<f64> {
        None
    }
    /// B18 belt (B18b): a belt of `n` bodies born as a program (or stored as a draw)
    /// from `spec` and `seed`, behind `belt::Belt`. None: not implemented, which fails the gate.
    fn belt_birth(&self, _spec: &belt::BeltSpec, _n: u64, _seed: u64) -> Option<Box<dyn belt::Belt>> {
        None
    }
    /// B18 belt: the belt rebuilt from `Belt::store()` bytes alone. None: not implemented, or not a store of this law.
    fn belt_restore(&self, _store: &[u8]) -> Option<Box<dyn belt::Belt>> {
        None
    }
    /// B19: the law's answer to a question about equatorial geodesics around a hole of spin `chi` (a/M, spinning towards +φ;
    /// the judge asks 0, 0.5, 0.9 and 0.998): cycles, circular orbits, fates, light, clocks, tubes and the Penrose split
    /// (`rotating::KerrQuery`). None: not implemented, which fails the gate; `Some(KerrAnswer::Absent)` says there is no such
    /// orbit, observer or tube.
    fn kerr(&self, _chi: f64, _query: &rotating::KerrQuery) -> Option<rotating::KerrAnswer> {
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
/// calling `emit` as each gate lands. The CLI runs all eighteen through `judge_only`.
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
    phase("B16", &mut || vec![lens::b16(law)]);
    phase("B17", &mut || vec![resonance::b17(law)]);
    phase("B18", &mut || vec![memory::b18(law)]);
    phase("B18b", &mut || vec![belt::b18_belt(law)]);
    phase("B19", &mut || vec![rotating::b19(law)]);
    out
}

const USAGE: &str = "usage: behave [--law echo|space|plane|planted-precession|planted-walk|planted-nocapture|planted-clock|planted-steps|planted-quadratic|planted-newton|planted-kick|planted-notide|planted-drift|planted-swollen|planted-linear|planted-apsides|planted-static|planted-flipped|planted-average|planted-bounded|planted-fat|iid-blocks|dyadic-belt|planted-belt-clipped|planted-belt-winsor|planted-belt-repeat|planted-belt-serial|planted-belt-thread|planted-belt-fat|planted-belt-ships|planted-belt-lattice|planted-belt-fatscars|planted-belt-crush|planted-belt-innerclip|planted-belt-aligned|planted-belt-table20|planted-nodrag|planted-isco|planted-penrose|planted-proonly|planted-rcapture] [--gates G1,G2,...,B18,B18b,B19] [--plane-step N]";

pub fn run(args: Vec<String>) -> Result<u8> {
    let cli = select::parse(&args).map_err(|e| format!("{e}; {USAGE}"))?;
    let name = cli.law.as_str();
    let law = if name == "plane" {
        Box::new(plane::Plane::new(cli.plane_step))
    } else {
        laws::by_name(name).ok_or_else(|| format!("unknown law {name:?}; {USAGE}"))?
    };
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
    fn every_planted_law_the_usage_names_resolves() {
        let names = ["echo", "planted-precession", "planted-walk", "planted-nocapture", "planted-clock", "planted-steps", "planted-quadratic", "planted-newton", "planted-kick", "planted-notide", "planted-drift", "planted-swollen", "planted-linear", "planted-apsides", "planted-static", "planted-flipped", "planted-average", "planted-fat", "iid-blocks", "dyadic-belt", "planted-belt-clipped", "planted-belt-winsor", "planted-belt-repeat", "planted-belt-serial", "planted-belt-thread", "planted-belt-fat", "planted-belt-ships", "planted-belt-lattice", "planted-belt-fatscars", "planted-belt-crush", "planted-belt-innerclip", "planted-belt-aligned", "planted-belt-table20", "planted-nodrag", "planted-isco", "planted-penrose", "planted-proonly", "planted-rcapture"];
        for name in names {
            assert!(laws::by_name(name).is_some() && USAGE.contains(name), "{name}");
        }
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
    fn the_default_run_is_all_eighteen_gates_and_a_law_without_the_new_methods_fails_every_gate_after_g6_in_it() {
        // `--gates` omitted is `only = None`: every gate, in the judge's order.
        let gates = judge_only(&Silent, None, None, |_| {});
        assert_eq!(gates.iter().map(|g| g.id).collect::<Vec<_>>(), select::ALL);
        assert_eq!(gates.iter().filter(|g| !g.pass).map(|g| g.id).collect::<Vec<_>>(), ["B7", "B9", "B10", "B11", "B12", "B13", "B14", "B16", "B17", "B18", "B18b", "B19"]);
    }

    #[test]
    fn the_events_gates_run_only_when_named_and_in_the_judges_order() {
        let ids = |only: &[&str]| judge_only(&Echo, None, Some(only), |_| {}).iter().map(|g| g.id).collect::<Vec<_>>();
        assert_eq!(ids(&["B13", "B11"]), ["B11", "B13"]);
    }
}

/// The red-team's amendments (1 October): B9 log-scaled to e = 0.99, B14's apsides, and the new gates
/// B16 (moving lenses), B17 (resonance) and B18 (memory), judged together. Echo passes them and each
/// planted law fails exactly its gate.
///
/// B14 and B17 are the slow gates (they integrate the restricted three-body problem), so a planted law is
/// run through them only where it touches `restricted`; for the others a test shows its `restricted` is
/// echo's, so its B14 and B17 verdicts are echo's.
#[cfg(test)]
mod amendment_tests {
    use super::laws::{Echo, Fault, Planted, Silent};
    use super::*;

    const AMENDED: [&str; 5] = ["B9", "B14", "B16", "B17", "B18"];

    fn failing(law: &dyn Law, only: &[&str]) -> Vec<&'static str> {
        let gates = judge_only(law, None, Some(only), |_| {});
        assert_eq!(gates.iter().map(|g| g.id).collect::<Vec<_>>(), only);
        gates.iter().filter(|g| !g.pass).map(|g| g.id).collect()
    }
    /// A B14 moon and a B17 case's ship, with their times: one of each kind of scene `restricted` is asked about.
    fn scenes() -> Vec<(restricted::Restricted, [f64; 4], Vec<f64>)> {
        let case = &resonance::cases()[14];
        let moon = hill::moons().iter().find(|m| m.rate.is_some()).expect("a moon with an apsidal rate");
        vec![(restricted::JUPITER, moon.ship, hill::times(&restricted::JUPITER)), (case.scene, resonance::start(case), resonance::times(case))]
    }
    fn answers_as_echo_does_on_both_kinds_of_scene(fault: Fault) -> bool {
        scenes().iter().all(|(scene, ship, times)| Planted(fault).restricted(scene, *ship, times) == Echo.restricted(scene, *ship, times))
    }

    #[test]
    fn echo_passes_every_amended_gate_with_its_evidence_on_the_line() {
        let gates = judge_only(&Echo, None, Some(&AMENDED), |_| {});
        assert!(gates.iter().all(|g| g.pass), "{:?}", gates.iter().map(|g| (g.id, g.detail.clone())).collect::<Vec<_>>());
        let detail = |id: &str| gates.iter().find(|g| g.id == id).unwrap().detail.clone();
        assert!(detail("B9").contains("512/512 orbits") && detail("B9").contains("at e = 0.99"), "{}", detail("B9"));
        assert!(detail("B14").contains("apsides: ") && detail("B14").contains("e0 up to 0.3"), "{}", detail("B14"));
        assert!(detail("B16").contains("256/256") && detail("B16").contains("beta up to 0.90"), "{}", detail("B16"));
        assert!(detail("B17").contains("controls 5/5") && detail("B17").contains("regime 34/34"), "{}", detail("B17"));
        assert!(detail("B18").contains("12/12") && detail("B18").contains("at 1e9 bodies"), "{}", detail("B18"));
    }

    #[test]
    fn each_planted_law_of_the_amendments_fails_exactly_its_gate() {
        // The cheap gates, for the laws that plant their flaw in them.
        let cheap = ["B9", "B16", "B18"];
        assert_eq!(failing(&Planted(Fault::Linear), &cheap), ["B9"]);
        assert_eq!(failing(&Planted(Fault::Steps), &cheap), ["B9"]);
        assert_eq!(failing(&Planted(Fault::Static), &cheap), ["B16"]);
        assert_eq!(failing(&Planted(Fault::Flipped), &cheap), ["B16"]);
        assert_eq!(failing(&Planted(Fault::Fat), &cheap), ["B18"]);
        // Those that plant it in the restricted problem, in the slow ones.
        assert_eq!(failing(&Planted(Fault::Apsides), &["B14"]), ["B14"]);
        assert_eq!(failing(&Planted(Fault::Averaged), &["B17"]), ["B17"]);
    }

    #[test]
    fn a_planted_law_answers_the_restricted_problem_as_echo_does_unless_it_plants_its_flaw_there() {
        // So its B14 and B17 verdicts are echo's, which pass.
        for fault in [Fault::Linear, Fault::Steps, Fault::Static, Fault::Flipped, Fault::Fat, Fault::Newton, Fault::Walk, Fault::Clock, Fault::Quadratic, Fault::Precession, Fault::NoCapture] {
            assert!(answers_as_echo_does_on_both_kinds_of_scene(fault));
        }
        // planted-kick and -notide plant theirs inside the planet's sphere of influence, which B17's ships never enter
        // and a B14 moon at 0.2 to 0.9 Hill radii does.
        let (_, b17_ship, b17_times) = &scenes()[1];
        let case = &resonance::cases()[14];
        // (They integrate the reference without echo's conservation of the Jacobi constant, so their states differ from
        // echo's by 1e-4 over B17's run; what B17 reads of them is the same, and B17 passes them.)
        for fault in [Fault::Kick, Fault::NoTide] {
            assert_eq!(failing(&Planted(fault), &["B17"]), Vec::<&str>::new());
        }
        // The two that plant theirs in a kind of scene leave the other as it is: apsides acts on ships bound to the planet,
        // the average on B17's scenes only.
        let (jup, ship, times) = &scenes()[0];
        assert_eq!(Planted(Fault::Averaged).restricted(jup, *ship, times), Echo.restricted(jup, *ship, times));
        assert_eq!(Planted(Fault::Apsides).restricted(&case.scene, *b17_ship, b17_times), Echo.restricted(&case.scene, *b17_ship, b17_times));
        assert_ne!(Planted(Fault::Apsides).restricted(jup, *ship, times), Echo.restricted(jup, *ship, times));
        assert_ne!(Planted(Fault::Averaged).restricted(&case.scene, *b17_ship, b17_times), Echo.restricted(&case.scene, *b17_ship, b17_times));
    }

    #[test]
    fn a_law_that_implements_none_of_the_amended_methods_fails_them_all() {
        assert_eq!(failing(&Silent, &AMENDED), AMENDED);
    }
}

/// B18 belt (B18b, frozen 5 October): the control belts pass, each planted belt fails the criterion it plants, and a belt
/// that tampers with the interface (ignores a scar, forgets scars in its store, misdeclares its information) is caught.
/// The plants run on one belt of 2^18 (the statistics are valid from k = 27 up); the full frozen runs are `release` only.
#[cfg(test)]
mod belt_tests {
    use super::belt::{self, Belt, BeltSpec, Body, Flaw, Form, ProgramBelt, Run};
    use super::laws::{DyadicBelt, Echo, Fault, IidBlocks, Planted, Silent};
    use super::*;

    const SMALL: [Run; 1] = [Run { log2n: 18, seed: 31337, thorough: true }];

    fn verdict(law: &dyn Law) -> Gate {
        belt::judge(law, &SMALL)
    }
    /// The planted law must fail and its detail must name each of `names`.
    fn fails_naming(fault: Fault, names: &[&str]) {
        let g = verdict(&Planted(fault));
        assert!(!g.pass && g.id == "B18b", "{}", g.detail);
        for n in names {
            assert!(g.detail.contains(n), "{n:?} missing: {}", g.detail);
        }
    }

    #[test]
    fn the_reference_belt_and_the_stored_draw_pass_with_the_evidence_on_the_line() {
        let g = verdict(&Echo);
        assert!(g.pass && g.detail.contains("bytes at 1e9: 42 B") && g.detail.contains("scarred"), "{}", g.detail);
        let g = verdict(&IidBlocks);
        assert!(g.pass && g.detail.contains("a stored sample") && g.detail.contains("sample form"), "{}", g.detail);
        // A dyadic quantile table passes if it is dyadic in the octaves of the probability (the gold's, in its linear scale, clips).
        let g = verdict(&DyadicBelt);
        assert!(g.pass, "{}", g.detail);
    }

    #[test]
    fn a_law_with_no_belt_fails() {
        let g = verdict(&Silent);
        assert!(!g.pass && g.detail.contains("belt_birth is not implemented"), "{}", g.detail);
    }

    #[test]
    fn the_golds_clipped_table_fails_the_tail_count_the_range_and_the_shape_of_e_only() {
        // 2^12 midpoint quantiles: the top 1e-4 of e is one cell, below the reference's 1 - 1e-4 quantile. (At 2^18 the
        // count has only k = 27 to lose, z = -3.7: the range and the shape fire; the frozen 2^20 and 2^23 fire the count too.)
        // (Its bottom end is clipped too: the lowest cell of 2^12 is far above the bottom 1e-4.)
        fails_naming(Fault::BeltClipped, &["top 1e-4 of e reaches", "tail shape of top 1e-4 of e", "bottom 1e-4 of e reaches"]);
        let g = verdict(&Planted(Fault::BeltClipped));
        assert!(!g.detail.contains("of p"), "{}", g.detail);
    }

    #[test]
    fn a_winsorized_belt_keeps_the_count_and_loses_the_range() {
        fails_naming(Fault::BeltWinsor, &["top 1e-4 of e reaches", "top 1e-4 of p reaches", "tail shape of top 1e-4 of e", "tail shape of top 1e-4 of p"]);
        let g = verdict(&Planted(Fault::BeltWinsor));
        assert!(!g.detail.contains("count") && !g.detail.contains("chi2") && !g.detail.contains("serial"), "{}", g.detail);
    }

    #[test]
    fn repeated_states_are_caught_exactly_and_by_the_chi_square() {
        fails_naming(Fault::BeltRepeat, &["no two bodies share a state", "chi2"]);
    }

    #[test]
    fn serial_structure_is_caught_by_the_lag_correlation_and_nothing_else_fires() {
        fails_naming(Fault::BeltSerial, &["serial and cross correlation", "t_p lag 1"]);
        let g = verdict(&Planted(Fault::BeltSerial));
        assert!(g.detail.starts_with("belt: 1 of ") && !g.detail.contains("share a state"), "{}", g.detail);
    }

    #[test]
    fn a_rank_one_lattice_is_caught_by_the_two_dimensional_chi_square() {
        fails_naming(Fault::BeltLattice, &["chi2 z = -"]);
    }

    #[test]
    fn a_thread_order_dependence_is_caught_in_every_order() {
        fails_naming(Fault::BeltThread, &["bit-identically", "Ascending", "Interleaved", "Descending", "Scrambled", "Chunks"]);
    }

    #[test]
    fn an_over_budget_store_fails_at_birth_and_so_do_fat_scars_and_ships() {
        fails_naming(Fault::BeltFat, &["bytes at birth"]);
        fails_naming(Fault::BeltFatScars, &["scarred bodies cost 40.00 bytes each"]);
        fails_naming(Fault::BeltShips, &["sample bytes per body 64.00"]);
    }

    // The red-team's four holes (GLM run 20261005-1404, F1 to F4): each plant passed the first judge, and fails this one.

    #[test]
    fn f2_a_hollow_inner_edge_of_p_is_caught_at_the_bottom_end() {
        // p clipped from below at its 1e-4 quantile: the tests of the top end cannot see it, the mirrored ones do.
        fails_naming(Fault::BeltInnerClip, &["bottom 1e-4 of p reaches", "bottom 1e-4 of p: conditional log-score mean z = +"]);
        assert!(!verdict(&Planted(Fault::BeltInnerClip)).detail.contains("top 1e-4"));
    }

    #[test]
    fn f3_deep_dippers_aligned_in_one_corridor_are_caught_by_the_other_columns_of_the_tail() {
        // The top 1e-4 of e all in 1/32 of the omega circle: every column's own KS and the (p, t_p) chi-square are blind to it.
        fails_naming(Fault::BeltAligned, &["top 1e-4 of e: its bodies' other columns stay uniform", "(omega)"]);
        assert!(verdict(&Planted(Fault::BeltAligned)).detail.starts_with("belt: 1 of "));
    }

    #[test]
    fn f4_a_table_declared_as_information_is_over_the_cap() {
        // A one-level 2^20-cell quantile table (4 MB) in the store, declared as information: it passes every statistic (the
        // table resolves the tail to 2^-20) and fails only the cap on the declared information.
        fails_naming(Fault::BeltTable20, &["declared information 4194345 B is within 64 B"]);
        assert!(verdict(&Planted(Fault::BeltTable20)).detail.starts_with("belt: 1 of "));
    }

    /// A law whose belt is the reference program with this flaw (all else echo's).
    struct FlawLaw(Flaw);
    impl Law for FlawLaw {
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
        fn belt_birth(&self, spec: &BeltSpec, n: u64, seed: u64) -> Option<Box<dyn Belt>> {
            Some(Box::new(ProgramBelt::birth(spec, n, seed, self.0)))
        }
        fn belt_restore(&self, store: &[u8]) -> Option<Box<dyn Belt>> {
            ProgramBelt::restore(store).map(|b| Box::new(b) as Box<dyn Belt>)
        }
    }

    /// F1 on the frozen runs (release only). A 15% crush of the e-tail's spread keeps its count and its reach; the log-score mean
    /// of the tail sees it in the two 2^23 runs (the exponential mean's best z is 0.15 sqrt(X): 4.4 at X = 850) and pooled over
    /// all five (7). A 12% crush passes every run on its own and fails the pooled test alone.
    #[test]
    #[cfg_attr(debug_assertions, ignore = "release only")]
    fn f1_a_crush_of_the_e_tails_spread_is_caught_by_the_log_score_mean_alone_or_pooled() {
        let g = belt::b18_belt(&Planted(Fault::BeltCrush));
        assert!(!g.pass && g.detail.starts_with("belt: 1 of ") && g.detail.contains("top 1e-4 of e: conditional log-score mean z = -4."), "{}", g.detail);
        let g = belt::b18_belt(&FlawLaw(Flaw::Crush12));
        assert!(!g.pass && g.detail.starts_with("belt: 1 of ") && g.detail.contains("top 1e-4 of e: conditional log-score mean pooled over 5 runs: z = -"), "{}", g.detail);
    }

    /// A belt that wraps the reference and tampers with one part of the interface.
    #[derive(Clone, Copy, PartialEq)]
    enum Tamper {
        IgnoreScar,
        ForgetScarsInStore,
        HugeInfo,
        TinyInfo,
        FatButHonest,
        SlowGrowth,
    }
    struct Tweaked {
        inner: ProgramBelt,
        mode: Tamper,
        spec: BeltSpec,
        n: u64,
        seed: u64,
    }
    impl Belt for Tweaked {
        fn len(&self) -> u64 {
            self.inner.len()
        }
        fn body(&self, i: u64) -> Body {
            self.inner.body(i)
        }
        fn store(&self) -> Vec<u8> {
            match self.mode {
                Tamper::ForgetScarsInStore => ProgramBelt::birth(&self.spec, self.n, self.seed, Flaw::None).store(),
                Tamper::SlowGrowth => [self.inner.store(), vec![0; (self.n >> 13) as usize]].concat(),
                _ => self.inner.store(),
            }
        }
        fn bytes_used(&self) -> u64 {
            self.inner.bytes_used()
        }
        fn scar(&mut self, i: u64, b: Body) {
            if self.mode != Tamper::IgnoreScar {
                self.inner.scar(i, b);
            }
        }
        fn form(&self) -> Form {
            match self.mode {
                Tamper::HugeInfo => Form::Program { info_bytes: 1 << 20 },
                Tamper::TinyInfo => Form::Program { info_bytes: 4 },
                Tamper::FatButHonest => Form::Program { info_bytes: self.inner.store().len() as u64 },
                Tamper::SlowGrowth => Form::Program { info_bytes: belt::INFO_CAP },
                _ => self.inner.form(),
            }
        }
    }
    struct TweakLaw(Tamper);
    impl TweakLaw {
        fn wrap(&self, inner: ProgramBelt, spec: BeltSpec, n: u64, seed: u64) -> Box<dyn Belt> {
            Box::new(Tweaked { inner, mode: self.0, spec, n, seed })
        }
    }
    impl Law for TweakLaw {
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
        fn belt_birth(&self, spec: &BeltSpec, n: u64, seed: u64) -> Option<Box<dyn Belt>> {
            let flaw = if self.0 == Tamper::FatButHonest { Flaw::Fat } else { Flaw::None };
            Some(self.wrap(ProgramBelt::birth(spec, n, seed, flaw), *spec, n, seed))
        }
        fn belt_restore(&self, store: &[u8]) -> Option<Box<dyn Belt>> {
            let n = u64::from_le_bytes(store.get(3..11)?.try_into().unwrap());
            let store = if self.0 == Tamper::SlowGrowth { &store[..store.len() - (n >> 13) as usize] } else { store };
            let inner = ProgramBelt::restore(store)?;
            let seed = u64::from_le_bytes(store[11..19].try_into().unwrap());
            Some(self.wrap(inner, belt::SPEC, n, seed))
        }
    }

    #[test]
    fn a_belt_that_ignores_a_scar_or_forgets_it_in_its_store_is_caught_on_exactness() {
        let g = verdict(&TweakLaw(Tamper::IgnoreScar));
        assert!(!g.pass && g.detail.contains("every scarred ordinal returns its scar") && g.detail.contains("scarred bodies cost 0.00 bytes"), "{}", g.detail);
        let g = verdict(&TweakLaw(Tamper::ForgetScarsInStore));
        assert!(!g.pass && g.detail.contains("the churned belt restores exactly"), "{}", g.detail);
    }

    #[test]
    fn the_declared_information_is_bound_by_the_store_and_by_growth() {
        // Declaring less than it stores: the store is over 2 x info + 2. More than it stores: not a program's information.
        let g = verdict(&TweakLaw(Tamper::TinyInfo));
        assert!(!g.pass && g.detail.contains("bytes at birth 42 within 2 x info 4 + 2 = 10"), "{}", g.detail);
        let g = verdict(&TweakLaw(Tamper::HugeInfo));
        assert!(!g.pass && g.detail.contains("and not below the info"), "{}", g.detail);
        // A store with a byte per body that declares all of it as information passes the 2x rule and fails the cap (F4).
        let g = verdict(&TweakLaw(Tamper::FatButHonest));
        assert!(!g.pass && g.detail.contains("declared information 262186 B is within 64 B"), "{}", g.detail);
        // Under the cap, a store that still grows with n (a byte per 8192 bodies) fails on growth.
        let runs = [Run { log2n: 18, seed: 5, thorough: false }, Run { log2n: 19, seed: 6, thorough: false }];
        let g = belt::judge(&TweakLaw(Tamper::SlowGrowth), &runs);
        assert!(!g.pass && g.detail.starts_with("belt: 1 of ") && g.detail.contains("the store does not grow with n"), "{}", g.detail);
    }

    #[test]
    fn the_belt_gate_is_a_default_gate_named_like_the_others() {
        // B18b follows B18 in the default run (`the_default_run_is_all_eighteen_gates...` pins the whole list); `--gates b18b`
        // picks it, and it alone runs. A law without a belt (`space`, today) fails it.
        let at = select::ALL.iter().position(|g| *g == "B18").unwrap();
        assert_eq!(select::ALL[at + 1], "B18b");
        assert_eq!(select::parse(&["--gates".into(), "b18b".into()]).unwrap().gates, Some(vec!["B18b"]));
        let gates = judge_only(&Silent, None, Some(&["B18b"]), |_| {});
        assert_eq!(gates.iter().map(|g| (g.id, g.pass)).collect::<Vec<_>>(), [("B18b", false)]);
        assert!(judge_only(&Silent, None, Some(&["B18", "B18b", "B19"]), |_| {}).iter().any(|g| g.id == "B18b"));
    }

    /// The frozen runs, on the two controls (release only: the debug build is 20 times slower than the gate's 60 s allows).
    #[test]
    #[cfg_attr(debug_assertions, ignore = "release only")]
    fn both_controls_pass_the_frozen_runs_and_every_plant_fails_them() {
        for law in [&Echo as &dyn Law, &IidBlocks, &DyadicBelt] {
            let g = belt::b18_belt(law);
            assert!(g.pass && g.detail.contains("5 runs"), "{}", g.detail);
        }
        let g = belt::b18_belt(&Planted(Fault::BeltClipped));
        assert!(g.detail.contains("top 1e-4 of e: count 0 against the reference's 105 (z = -7"), "{}", g.detail);
        for fault in [Fault::BeltClipped, Fault::BeltWinsor, Fault::BeltRepeat, Fault::BeltSerial, Fault::BeltThread, Fault::BeltFat, Fault::BeltShips, Fault::BeltLattice, Fault::BeltFatScars, Fault::BeltCrush, Fault::BeltInnerClip, Fault::BeltAligned, Fault::BeltTable20] {
            assert!(!belt::b18_belt(&Planted(fault)).pass);
        }
    }
}
