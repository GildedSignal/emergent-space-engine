//! Dump the plane's real kick stream through the shipped engine's public API.
//!
//! Two universes:
//!  - `massive`: scenario::plane's massive bodies only (3 planets + moon, the same literals),
//!    built through the same public calls; ships are massless test bodies and are never kick
//!    sources, so the massive bodies' kick streams are the plane's own gravity-news stream.
//!    Advanced far (default 4e13 ticks) to gather statistics.
//!  - `full`: the whole shipped plane (scenario::plane, members N), advanced short; confirms the
//!    massive streams are identical and gives the player's registers for the Q anchor.
//!
//! Output (stdout): header lines `# ...`, per-body `B,...`, per-kick `K,...`.
use emergent_space::events::{Doll as SpaceDoll, LogMass};
use emergent_space::orbit::Scalar;
use emergent_universe::body::Kind;
use emergent_universe::observe;
use emergent_universe::scenario::{plane, PlanetSpec, PLANETS, STAR_RADIUS};
use emergent_universe::world::Mass;
use emergent_universe::{Config, Universe};

fn raw(mant: i128, exp: i32) -> Scalar {
    Scalar::raw(mant, exp).unwrap()
}

/// A copy of scenario::plane's massive-body construction (same literals, same public calls),
/// without the ships, the fleet and the player: they are massless and never kick sources.
fn massive_only(cfg: Config) -> (Universe, Vec<usize>, usize) {
    let mut u = Universe::new(raw(STAR_RADIUS as i128, 0), cfg);
    let mut planets = Vec::new();
    let mut dolls = Vec::new();
    for p in &PLANETS {
        let b = u
            .add_body(
                Kind::Planet,
                emergent_universe::OrbitSpec {
                    doll: 0,
                    periapsis: raw(p.periapsis as i128, 0),
                    e_q48: p.e_q48,
                    clockwise: false,
                    angle: p.angle,
                    phase: p.phase,
                },
                Scalar::ZERO,
            )
            .unwrap();
        let surface = raw(p.radius as i128, -p.mass_log2);
        let d = u.add_doll(p.name, b, Mass::pow2(p.mass_log2), surface).unwrap();
        planets.push(b);
        dolls.push(d);
    }
    let (home, home_doll) = (planets[1], dolls[1]);
    let m = u
        .add_body(
            Kind::Moon,
            emergent_universe::OrbitSpec {
                doll: home_doll,
                periapsis: raw(260_000, 18),
                e_q48: (1u64 << 48) / 20,
                clockwise: false,
                angle: 0x1000_0000,
                phase: 0x7000_0000,
            },
            raw(1_176, 18),
        )
        .unwrap();
    let sep = u.rec(m).b.entry.trajectory.key().periapsis;
    let proto = SpaceDoll::child(LogMass((-24) << 24), home_doll, u.rec(m).b.tube);
    let soi = proto.edge_radius(&u.dolls[home_doll as usize].record.clone(), sep).unwrap();
    u.make_source(m, Mass::pow2(-6), soi).unwrap();
    u.start().unwrap();
    (u, planets, m)
}

fn dump(u: &Universe, names: &[String], mass_of: &[f64]) {
    let ctx = u.ctx();
    let store = u.bodies();
    println!("# now={} bodies={} kicks={} events={}", u.now, store.len(), u.stats.kicks, u.stats.events());
    for i in 0..store.len() {
        let r = store.rec(i);
        println!(
            "B,{i},{:?},{},{},{},{},{},{},{}",
            r.kind,
            names.get(i).map(|s| s.as_str()).unwrap_or("?"),
            mass_of[i],
            r.b.doll,
            r.step,
            r.b.units.1,
            r.carry[0],
            r.alive,
        );
        // Walk the binding chain back: every kick binding this body ever got.
        let mut b = r.b.clone();
        loop {
            let k = b.kick;
            if k.len > 0 {
                let (p, _) = observe::root_state(&ctx, i, b.event_time).unwrap_or(([f64::NAN; 2], [f64::NAN; 2]));
                println!(
                    "K,{i},{},{},{},{},{},{},{},{:.6e},{:.6e}",
                    b.event_time, k.len, k.level, k.dv[0], k.dv[1], b.units.1, b.doll, p[0], p[1]
                );
            }
            match store.binding_at(i, b.event_time - 1) {
                Some(prev) => b = prev,
                None => break,
            }
        }
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mode = args.get(1).map(|s| s.as_str()).unwrap_or("massive");
    let target: i64 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(40_000_000_000_000);
    let cfg = Config::default();
    match mode {
        "massive" => {
            let (mut u, planets, moon) = massive_only(cfg);
            u.advance(target, emergent_universe::Budget::unlimited());
            let mut names = Vec::new();
            for p in &PLANETS {
                names.push(p.name.to_string());
            }
            names.push("Moon".to_string());
            let mut mass_of = vec![0.0; 4];
            for (k, p) in PLANETS.iter().enumerate() {
                mass_of[k] = 2f64.powi(p.mass_log2);
            }
            mass_of[3] = 2f64.powi(-24); // the moon: Home's 2^-6, Home is 2^-18 of the star
            println!("# mode=massive target={target} planets={:?} moon={}", planets, moon);
            dump(&u, &names, &mass_of);
        }
        "full" => {
            let members: u64 = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(32);
            let seed = 20261008u64;
            let p = plane(cfg, seed, emergent_universe::fleet::Order::Sparse, 1, members)
                .unwrap_or_else(|e| panic!("plane: {e:?}"));
            let mut u = p.u;
            u.advance(target, emergent_universe::Budget::unlimited());
            let mut mass_of = vec![0.0; u.n_bodies()];
            mass_of[0] = 1.0;
            for (k, pl) in PLANETS.iter().enumerate() {
                mass_of[p.planets[k]] = 2f64.powi(pl.mass_log2);
            }
            mass_of[p.moon] = 2f64.powi(-24);
            println!("# mode=full target={target} members={members} player={}", p.player);
            dump(&u, &p.names, &mass_of);
        }
        _ => panic!("modes: massive | full"),
    }
}
