//! Each body's own clock (14 October; `crate::ext::constants`): a ship of the root doll is stepped by the longest step that resolves
//! what forces it: its own orbit (16 steps a period), the frame's fall toward every secondary (at least 4 per its period, more
//! where the fall is strong against the host's pull) and the passage of every secondary its orbit can meet (`2^(step_log2+1)` per that secondary's period); its first step
//! is a stub of a phase from its id, so bodies born at one tick never kick at one tick. Every test finishes within 60 s.
use emergent_universe::body::What;
use emergent_universe::ext::fprime;
use emergent_universe::num::to_f64;
use emergent_universe::scenario::{ladder_ship, restricted_with};
use emergent_universe::{Config, Kind, OrbitSpec, Universe};
use emergent_space::orbit::Scalar;
use emergent_universe::num::s;

/// The ladder's belt about the plane's three planets (`scenario::PLANETS`), its first `n` bodies.
fn belt(cfg: Config, n: u64) -> (Universe, Vec<usize>) {
    let mut u = Universe::new(s(emergent_universe::scenario::STAR_RADIUS), cfg);
    u.threads = 1;
    for p in &emergent_universe::scenario::PLANETS {
        let b = u
            .add_body(Kind::Planet, OrbitSpec { doll: 0, periapsis: s(p.periapsis), e_q48: p.e_q48, clockwise: false, angle: p.angle, phase: p.phase }, Scalar::ZERO)
            .unwrap();
        u.add_doll(p.name, b, p.mass_log2, Scalar::raw(p.radius as i128, -p.mass_log2).unwrap()).unwrap();
    }
    let ids = (0..n)
        .map(|k| {
            let (spec, radius) = ladder_ship(1, 300 + k, 1_000_000, 0).unwrap();
            u.add_body(Kind::Ship, spec, radius).unwrap()
        })
        .collect();
    u.start().unwrap();
    (u, ids)
}

/// The steps a ship's own period gets far from every secondary: `P / (Δs·f'(c))`.
fn steps_per_period(u: &Universe, i: usize) -> f64 {
    let r = u.rec(i);
    let emergent_space::binding::Trajectory::Cycle(c) = &r.b.entry.trajectory else { panic!("a bound ship") };
    to_f64(r.b.to_doll(c.period().unwrap()).unwrap()) / step_of(u, i)
}

/// The first kick of each ship, in ticks.
fn first_kicks(u: &Universe, ids: &[usize]) -> Vec<i64> {
    ids.iter().map(|&i| u.rec(i).plan.iter().find(|p| matches!(p.what, What::Kick(_))).expect("a planned kick").t).collect()
}

/// The physical step a ship's clock gives far from every secondary: `Δs·f'(c)`, root time units.
fn step_of(u: &Universe, i: usize) -> f64 {
    let ext = u.rec(i).ext.expect("a ship of the root doll is on the clock");
    to_f64(ext.ds) * to_f64(fprime(ext.c, ext.b).unwrap())
}

/// A belt between Home's orbit and the Giant's (2-3 AU) is stepped by the longest step that resolves its own orbit (2^k_s a
/// period), the frame's fall toward Cinder (2^k_f per Cinder's 88 days) and, for the few that can come within 2√3 Hill radii of
/// the Giant, the Giant's passage (2^(step_log2 + 1) a Giant period): within a factor two of that (`Δs` is a power of two). The clock of
/// 7 October (the reference) gave every one of them 2^7 to 2^8 steps per Cinder's 88 days, 16 to 64 times more.
#[test]
fn a_ship_is_stepped_by_what_forces_it() {
    let cfg = Config::default();
    let (u, ids) = belt(cfg, 2_000);
    let period = |i: usize| {
        let r = u.rec(i);
        let emergent_space::binding::Trajectory::Cycle(c) = &r.b.entry.trajectory else { panic!("a bound tube") };
        to_f64(r.b.to_doll(c.period().unwrap()).unwrap())
    };
    let (p_cinder, p_giant) = (period(0), period(2)); // Cinder, Home, the Giant, then the ships
    let k_p = cfg.step_log2 + emergent_universe::ext::PASSAGE_OCTAVES;
    let (old, old_ids) = belt(Config { own_clock: false, ..cfg }, 2_000);
    let (mut smooth, mut near, mut fewer) = (0, 0, f64::INFINITY);
    for (&i, &o) in ids.iter().zip(&old_ids) {
        let (step, p) = (step_of(&u, i), period(i));
        // (the frame's fall toward Home and the Giant asks for less here: ε·(Q/a)² keeps them under 2^k_f per their period)
        let want = (p * 2f64.powi(-(cfg.step_log2 + cfg.smooth_octaves))).min(p_cinder * 2f64.powi(-(cfg.step_log2 + cfg.forcing_octaves)));
        let passage = p_giant * 2f64.powi(-k_p);
        if step > 0.5 * want * 0.999 && step <= want * 1.001 {
            smooth += 1;
            fewer = fewer.min(step / step_of(&old, o));
        } else {
            assert!(step > 0.5 * passage * 0.999 && step <= passage * 1.001, "ship {i}: a step of {step:.3e}, neither {want:.3e} nor the Giant's passage {passage:.3e}");
            near += 1;
        }
    }
    println!("{smooth} ships on what forces them far from the planets (at least {fewer:.1}x the reference's step), {near} at the Giant's passage cadence, of {}", ids.len());
    assert!(smooth > ids.len() * 9 / 10, "the belt is far from the planets: {smooth} of {}", ids.len());
    assert!(fewer >= 16.0 * 0.999, "the reference's step is at most 1/16 of the new: {fewer}");
}

/// No lockstep: ships born at one tick with one step kick at as many ticks as there are ships (the stub's phase is a function of the
/// id), spread over the first half step; the reference clock (phase zero) put them all within the few percent `f'(U_P + c)` moves.
#[test]
fn ships_born_together_never_kick_together() {
    let (u, ids) = belt(Config::default(), 4_000);
    let mut t = first_kicks(&u, &ids);
    t.sort();
    let distinct = t.windows(2).filter(|w| w[0] != w[1]).count() + 1;
    let (lo, hi) = (t[0], t[t.len() - 1]);
    // In 16 equal bins of the first kicks' span, no bin holds more than 3x its share.
    let mut bins = [0usize; 16];
    for &x in &t {
        bins[(((x - lo) as f64 / (hi - lo + 1) as f64) * 16.0) as usize] += 1;
    }
    let worst = *bins.iter().max().unwrap() as f64 / (t.len() as f64 / 16.0);
    println!("{} ships: first kicks at {distinct} distinct ticks, from {lo} to {hi}; the fullest of 16 bins holds {worst:.2}x its share", t.len());
    assert!(distinct as f64 >= 0.99 * t.len() as f64, "{distinct} distinct first kicks of {}", t.len());
    assert!(worst < 3.0, "the first kicks bunch: {bins:?}");
    let (old, ids) = belt(Config { own_clock: false, ..Config::default() }, 4_000);
    let t_old = first_kicks(&old, &ids);
    let (a, b) = (*t_old.iter().min().unwrap() as f64, *t_old.iter().max().unwrap() as f64);
    println!("the reference clock: every first kick between {a} and {b} ({:.1}% apart)", 100.0 * (b - a) / a);
    assert!((b - a) / a < 0.25, "the control: the reference clock's first kicks are one wave");
}

/// The restricted problem's ships near the planet (1.5 to 3 Hill radii: within 2√3 of it) take the planet's passage cadence, one
/// octave over the 2^step_log2 a planet period every ship of the root doll had before (B13 passes 64/64 there, 59-60/64 at 2^7).
#[test]
fn ships_that_can_meet_the_planet_keep_its_cadence() {
    let (mu_log2, sep) = (-10, 527_000_000i64);
    let hill = sep as f64 * (2f64.powi(mu_log2) / 3.0).cbrt();
    let ships: Vec<(i64, u32)> = (0..8).map(|i| ((sep as f64 + if i % 2 == 0 { 1.0 } else { -1.0 } * hill * (1.5 + 0.2 * i as f64)) as i64, (i as u32).wrapping_mul(0x9E37_79B9))).collect();
    let cfg = Config::default();
    let new = restricted_with(mu_log2, sep, 49_000, &ships, 1, cfg).unwrap();
    let old = restricted_with(mu_log2, sep, 49_000, &ships, 1, Config { own_clock: false, ..cfg }).unwrap();
    for (&a, &b) in new.ships.iter().zip(&old.ships) {
        assert_eq!(new.u.rec(a).ext.unwrap().ds, old.u.rec(b).ext.unwrap().ds.scale(-1).unwrap(), "ship {a}: an octave over the planet's cadence");
    }
    // And a ship far inside it (at 0.4 of its orbit: 30 Hill radii away) is on its own period.
    let far = restricted_with(mu_log2, sep, 49_000, &[((sep as f64 * 0.4) as i64, 0)], 1, cfg).unwrap();
    let n = steps_per_period(&far.u, far.ships[0]);
    assert!((16.0 * 0.999..=32.0 * 1.001).contains(&n), "{n} steps a period");
}
