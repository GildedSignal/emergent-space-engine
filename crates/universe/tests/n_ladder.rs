//! The N ladder: the population (integers and a seed; the plane's own bodies untouched at N = 0), the radial index the player's scan
//! reads through (`crate::radial`: a certificate, so it must drop only pairs that cannot be a hit), and the frame's bookkeeping that
//! stopped walking every body (queue membership, the ships' ticks, prune). Every test finishes within 60 s.
use emergent_lattice::law::hit;
use emergent_space::orbit::Scalar;
use emergent_universe::ctx::Ctx;
use emergent_universe::encounter::{Encounter, Encounters, ENCOUNTER_LOG2};
use emergent_universe::fleet::Order;
use emergent_universe::num::{s, sub2, time_of, to_f64, Res, Tick};
use emergent_universe::radial::{range_of, Window};
use emergent_universe::scenario::{ladder_locals, ladder_ship, plane, plane_extra, rayleigh_q48, restricted, AU};
use emergent_universe::thrust::word;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{Budget, Config, Kind, OrbitSpec};

/// The finder as it was before any filter: every body read at every scan.
struct Brute;
impl Encounters for Brute {
    fn find(&self, ctx: &Ctx, body: usize, t: Tick, interval: Tick) -> Vec<Encounter> {
        let mut out = Vec::new();
        let Some(me) = ctx.bodies.binding_at(body, t) else { return out };
        let Ok((x, v)) = me.cartesian(t) else { return out };
        let Ok(h) = time_of(interval, me.clock_exp) else { return out };
        for j in 0..ctx.bodies.len() {
            if j == body || !ctx.bodies.alive(j) || t <= ctx.info[j].born {
                continue;
            }
            let Some(other) = ctx.bodies.binding_at(j, t) else { continue };
            if other.doll != me.doll {
                continue;
            }
            let reach = ctx.info[body].radius.add(ctx.info[j].radius).unwrap_or(Scalar::ZERO);
            if reach.is_zero() {
                continue;
            }
            let found = (|| -> Res<Option<bool>> {
                let (xj, vj) = other.cartesian(t)?;
                let d = sub2(xj, x)?;
                let w = [vj[0].sub(v[0])?.mul(h)?, vj[1].sub(v[1])?.mul(h)?];
                let q_exp = reach.exponent() as i32 - 20;
                let integers = |a: [Scalar; 2]| -> Res<[i128; 2]> { Ok([a[0].fixed(-q_exp)?, a[1].fixed(-q_exp)?]) };
                let (di, wi) = (integers(d)?, integers(w)?);
                let near = reach.scale(ENCOUNTER_LOG2)?.fixed(-q_exp)?;
                if !hit(di, wi, near) {
                    return Ok(None);
                }
                Ok(Some(hit(di, wi, reach.fixed(-q_exp)?)))
            })();
            if let Ok(Some(contact)) = found {
                out.push(Encounter { a: body, b: j, t, contact });
            }
        }
        out
    }
}

#[test]
fn the_rayleigh_draw_is_integer_and_the_right_distribution() {
    // Against the float quantile (within a few quanta of 2^-48), over a grid of the survival probability, and monotone.
    let mut prev = 0;
    for k in 0..=4096u64 {
        let u = ((k * 0xFFFF_FFFF) / 4096) as u32;
        let e = rayleigh_q48(u, 70);
        assert!(e >= prev, "monotone in u");
        prev = e;
        let survival = (((1u64 << 32) - u as u64) as f64) / 4294967296.0;
        let want = 0.07 * (-2.0 * survival.ln()).sqrt() * (1u64 << 48) as f64;
        assert!((e as f64 - want).abs() <= 1e-6 * want + 4096.0, "u {u}: {e} against {want}");
    }
    assert_eq!(rayleigh_q48(0, 70), 0, "the survival probability one is the circle");
}

#[test]
fn a_ladder_ship_is_a_function_of_the_seed_and_its_index() {
    let n = 5000u64;
    let a: Vec<_> = (0..n).map(|k| ladder_ship(1, k, n, 2).unwrap().0).collect();
    let b: Vec<_> = (0..n).map(|k| ladder_ship(1, k, n, 2).unwrap().0).collect();
    let c: Vec<_> = (0..n).map(|k| ladder_ship(2, k, n, 2).unwrap().0).collect();
    let key = |o: &OrbitSpec| (o.doll, to_f64(o.periapsis).to_bits(), o.e_q48, o.angle, o.phase, o.clockwise);
    assert!(a.iter().zip(&b).all(|(x, y)| key(x) == key(y)), "the same seed makes the same ships");
    assert!(a.iter().zip(&c).filter(|(x, y)| key(x) != key(y)).count() > 4900, "another seed makes other ships");
    let mut distinct: Vec<_> = a.iter().map(key).collect();
    distinct.sort();
    distinct.dedup();
    assert_eq!(distinct.len(), n as usize, "every ship is on its own orbit");
    // The belt is above 1.2 AU with its Rayleigh e; the locals are in Home's doll, clear of the surface.
    let locals = ladder_locals(n) as usize;
    assert_eq!(locals, 300);
    for (k, o) in a.iter().enumerate() {
        if k >= locals {
            assert_eq!(o.doll, 0);
            let p = to_f64(o.periapsis) / AU as f64;
            assert!(p > 1.2 && p < 3.0, "belt periapsis {p} AU");
            assert!(o.e_q48 <= (2u64 << 48) / 5);
        } else {
            assert_eq!(o.doll, 2);
            assert!(to_f64(o.periapsis) / 2f64.powi(18) > 4313.0, "a local clears Home's surface");
        }
    }
    let belt_e: f64 = a[locals..].iter().map(|o| o.e_q48 as f64 / (1u64 << 48) as f64).sum::<f64>() / (n as usize - locals) as f64;
    assert!((belt_e - 0.07 * (std::f64::consts::PI / 2.0).sqrt()).abs() < 0.005, "the mean of a Rayleigh of scale 0.07: {belt_e}");
}

#[test]
fn the_plane_with_no_extra_ships_is_the_plane() {
    let cut = 200_000_000i64;
    let mut a = plane(Config::default(), 1, Order::Sparse, 1, 16).unwrap();
    let mut b = plane_extra(Config::default(), 1, Order::Sparse, 1, 16, 0).unwrap();
    assert_eq!(a.u.n_bodies(), b.u.n_bodies());
    a.u.settle(cut);
    b.u.settle(cut);
    assert_eq!(a.u.digest(), b.u.digest());
    // And with extra ships the plane's own bodies are the same bodies (ids before the extras are untouched).
    let c = plane_extra(Config::default(), 1, Order::Sparse, 1, 16, 50).unwrap();
    let d = plane_extra(Config::default(), 1, Order::Sparse, 1, 16, 0).unwrap();
    assert_eq!(c.u.n_bodies(), d.u.n_bodies() + 50);
    assert_eq!(c.ships.len(), d.ships.len() + 50);
    assert_eq!(c.u.rec(c.player).kind, Kind::Player);
}

/// Every readout of every binding a reader can still ask for lies in the radial range `range_of` says, and under its speed bound.
#[test]
fn the_radial_range_holds_every_readout() {
    let mut p = plane_extra(Config::default(), 1, Order::Sparse, 1, 48, 400).unwrap();
    p.u.schedule((1.0 * 3000.0 / TICK_SECONDS) as i64, word(1, 10)).unwrap();
    for _ in 0..600 {
        p.u.frame_to(1.0 / 60.0, 3000.0, Budget::unlimited(), i64::MAX);
    }
    let (mut checked, mut kicked) = (0usize, 0usize);
    // `shrink` plants a fault: the range narrowed by that fraction at both ends. At zero nothing may fall outside; at 5% something must
    // (the control: this check can fail).
    let mut violations = |shrink: f64| -> usize {
        let mut bad = 0;
        for i in 0..p.u.n_bodies() {
            let rec = p.u.rec(i);
            if rec.kind != Kind::Ship {
                continue;
            }
            let bindings = p.u.bodies().bindings_of(i);
            for (k, b) in bindings.iter().enumerate() {
                let Some((lo, hi, vmax)) = range_of(b) else { continue };
                let (lo, hi) = (lo * (1.0 + shrink), hi * (1.0 - shrink));
                let end = bindings.get(k + 1).map_or(b.event_time + (1i64 << 38), |n| n.event_time);
                for f in 0..24 {
                    let t = b.event_time + (end - b.event_time) * f / 24;
                    let Ok((x, v)) = b.cartesian(t) else { continue };
                    let (r, sp) = (to_f64(x[0]).hypot(to_f64(x[1])), to_f64(v[0]).hypot(to_f64(v[1])));
                    bad += (r < lo || r > hi || sp > vmax) as usize;
                    checked += 1;
                }
            }
            kicked += (bindings.len() > 1) as usize;
        }
        bad
    };
    assert_eq!(violations(0.0), 0, "a readout outside the range the index registered");
    let planted = violations(0.05);
    println!("{checked} readouts, {kicked} ship-passes with a history; a range narrowed by 5% is wrong at {planted} of them");
    assert!(planted > 100, "the check must fail on a narrowed range");
}

/// A scene in the star's doll where the filter has something to drop and the neighbours are close: the planet kicks everything,
/// the player and every ship are fat (so the scan's neighbourhood is wide), ships on orbits near the player's radius and far from it.
fn scene(extra_finder: Option<Box<dyn Encounters>>) -> emergent_universe::Universe {
    let mut w = restricted(-10, 5 * AU, 47_400, &[], 1).unwrap();
    let fat = s(20_000);
    let spec = |peri_au: f64, e: f64, k: u32| OrbitSpec {
        doll: 0,
        periapsis: s((peri_au * AU as f64) as i64),
        e_q48: (e * (1u64 << 48) as f64) as u64,
        clockwise: k % 7 == 6,
        angle: k.wrapping_mul(0x9E37_79B1),
        phase: k.wrapping_mul(0x85EB_CA77).rotate_left(11),
    };
    let me = w.u.add_body(Kind::Player, spec(1.0, 0.0, 0), fat).unwrap();
    w.u.info[me].radius = fat;
    for k in 1..=36u32 {
        let near = k <= 18;
        let peri = if near { 0.94 + 0.005 * k as f64 } else { 2.0 + 0.04 * k as f64 };
        let e = [0.0, 0.02, 0.05, 0.1][(k % 4) as usize];
        let id = w.u.add_body(Kind::Ship, spec(peri * (1.0 - 0.0), e, k), fat).unwrap();
        w.u.info[id].radius = fat;
    }
    if let Some(f) = extra_finder {
        w.u.set_encounters(f);
    }
    w.u.start().unwrap();
    w.u
}

#[test]
fn the_radial_index_finds_what_the_brute_force_finds() {
    let cut = 6_000_000_000_000i64;
    let mut a = scene(Some(Box::new(Brute)));
    let mut b = scene(None);
    // The filter must have something to drop: the player's window against the registered bodies.
    {
        let ctx = b.ctx();
        let w = Window { r: 1.0 * AU as f64, v: 1e-4, reach_p: 20_000.0, near_log2: ENCOUNTER_LOG2, h: 2.0e9 };
        let ids = ctx.radial.candidates(0, &w).expect("a window the index answers");
        println!("window of the player: {} of {} bodies", ids.len(), b.n_bodies());
        assert!(ids.len() < b.n_bodies() && ids.len() > 5, "the filter drops the far ships and keeps the near ones");
    }
    a.settle(cut);
    b.settle(cut);
    println!("encounters {} (contacts {}), kicks {}", a.stats.encounters, a.contacts, a.stats.kicks);
    assert!(a.stats.encounters > 50, "the scene must have encounters to find");
    assert_eq!(b.digest(), a.digest());
    assert_eq!((b.stats.encounters, b.contacts), (a.stats.encounters, a.contacts));
    assert_eq!(b.enc_log, a.enc_log);
}

#[test]
fn the_radial_index_is_the_brute_force_through_the_belt() {
    // The player burns forward at L8 from tick 0 at rtf 3000 (the nose is prograde there): it leaves Home's doll for the star's, and
    // spirals out into the belt's band, where the radial window covers most of the belt and then some of it. The encounters (and the
    // digest that holds their chain) must be the brute force's wherever the index answers and wherever it gives way.
    let seconds = 6.0;
    let cut = (seconds * 3000.0 / TICK_SECONDS) as i64;
    let go = |brute: bool| {
        let mut p = plane_extra(Config::default(), 1, Order::Sparse, 1, 16, 400).unwrap();
        if brute {
            p.u.set_encounters(Box::new(Brute));
        }
        p.u.schedule(0, word(1, 8)).unwrap();
        let mut r_max = 0f64;
        for _ in 0..4000 {
            if p.u.now >= cut {
                break;
            }
            p.u.frame_to(1.0 / 60.0, 3000.0, Budget::unlimited(), cut);
            let r = p.u.rec(p.player);
            if let Ok((x, _)) = r.b.cartesian(r.b.event_time) {
                if r.b.doll == 0 {
                    r_max = r_max.max(to_f64(x[0]).hypot(to_f64(x[1])));
                }
            }
        }
        p.u.settle(cut);
        (p.u.digest(), p.u.stats.encounters, p.u.contacts, p.u.enc_log.clone(), p.u.rec(p.player).b.doll, r_max / AU as f64)
    };
    let (a, b) = (go(true), go(false));
    println!("encounters {} (contacts {}), the player ends in doll {}, out to {:.3} AU", a.1, a.2, a.4, a.5);
    assert_eq!(a.4, 0, "the player must have crossed into the star's doll");
    assert!(a.5 > 1.22, "and spiralled into the belt's band ({:.3} AU)", a.5);
    assert_eq!(a, b);
}
