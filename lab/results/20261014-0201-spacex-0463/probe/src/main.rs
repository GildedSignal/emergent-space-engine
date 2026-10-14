//! The quiet belt's arrival stream on shipped code (lab run 20261014-0201-spacex-0463).
//!
//! Two arms, both the plane's own populations, no fleet, no player, no driver:
//! - `belt0`: N ships on heliocentric orbits 0.5-8 AU (the haulers' range) in the root doll,
//!   where ships are clock-stepped (motion law v2);
//! - `beltD`: N ships on low orbits about Home (the Orbiters' range), where ships are
//!   block-stepped on the shared power-of-two lattice (`step::aligned`).
//! Each arm is settled through ~3 steps of its fastest class with an unlimited budget; the
//! census (env `ES_CENSUS`, observation only) records every resolved item's tick. The digest
//! at the cut is printed for the probe-off control.
use emergent_space::orbit::Scalar;
use emergent_universe::body::BodyStore;
use emergent_universe::num::{from_f64, Tick};
use emergent_universe::scenario::{AU, PLANETS, STAR_RADIUS};
use emergent_universe::{Config, Kind, OrbitSpec, Universe};

fn lcg(seed: &mut u64) -> f64 {
    *seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
    (*seed >> 11) as f64 / (1u64 << 53) as f64
}

fn rss_hwm_kb() -> u64 {
    std::fs::read_to_string("/proc/self/status")
        .unwrap()
        .lines()
        .find(|l| l.starts_with("VmHWM"))
        .unwrap()
        .split_whitespace()
        .nth(1)
        .unwrap()
        .parse()
        .unwrap()
}

/// The plane's star and its three planets (each with its doll), no moon, no fleet, no player.
fn system() -> Universe {
    let mut u = Universe::new(from_f64(STAR_RADIUS as f64), Config::default());
    u.threads = 1;
    let mut dolls = Vec::new();
    for p in &PLANETS {
        let b = u
            .add_body(
                Kind::Planet,
                OrbitSpec {
                    doll: 0,
                    periapsis: from_f64(p.periapsis as f64),
                    e_q48: p.e_q48,
                    clockwise: false,
                    angle: p.angle,
                    phase: p.phase,
                },
                Scalar::ZERO,
            )
            .unwrap();
        let surface = Scalar::raw(p.radius as i128, -p.mass_log2).unwrap();
        dolls.push(u.add_doll(p.name, b, p.mass_log2, surface).unwrap());
    }
    assert_eq!(dolls.len(), 3);
    u
}

/// `belt0`: hauler-class tubes about the star. GM_sun = 1 (root unit, tick), so P = 2*pi*a^1.5.
fn belt0(n: usize, seed: u64) -> Universe {
    let mut u = system();
    let mut rng = seed ^ 0x5DEECE66D;
    for _ in 0..n {
        let a = (0.5 + 7.5 * lcg(&mut rng)) * AU as f64;
        let e = 0.05 * lcg(&mut rng);
        u.add_body(
            Kind::Ship,
            OrbitSpec {
                doll: 0,
                periapsis: from_f64(a * (1.0 - e)),
                e_q48: (e * (1u64 << 48) as f64) as u64,
                clockwise: lcg(&mut rng) < 0.15,
                angle: (lcg(&mut rng) * 4294967296.0) as u32,
                phase: (lcg(&mut rng) * 4294967296.0) as u32,
            },
            Scalar::raw(34, -10).unwrap(),
        )
        .unwrap();
    }
    u.start().unwrap();
    u
}

/// `beltD`: Orbiter-class tubes about Home (doll 1), block-stepped.
/// Home: GM = 2^-18 (root units), P = 2*pi*sqrt(r^3 / GM) with r in root units.
fn beltd(n: usize, seed: u64) -> (Universe, u16) {
    let mut u = system();
    let mut rng = seed ^ 0x9E3779B97F4A7C15;
    let home_doll = 1u16;
    for _ in 0..n {
        let alt = 1.2 + 2.8 * lcg(&mut rng);
        let e = 0.02 * lcg(&mut rng);
        u.add_body(
            Kind::Ship,
            OrbitSpec {
                doll: home_doll,
                periapsis: Scalar::raw((4_313.0 * alt * 1024.0) as i128, -10 + 18).unwrap(),
                e_q48: (e * (1u64 << 48) as f64) as u64,
                clockwise: lcg(&mut rng) < 0.2,
                angle: (lcg(&mut rng) * 4294967296.0) as u32,
                phase: (lcg(&mut rng) * 4294967296.0) as u32,
            },
            Scalar::raw(34, -10 + 18).unwrap(),
        )
        .unwrap();
    }
    u.start().unwrap();
    (u, home_doll)
}

fn json_arm(tag: &str, u: &Universe, horizon: Tick, wall_ms: f64) -> String {
    let census = emergent_universe::universe::take_census();
    let (ns, calls) = emergent_universe::prof::take();
    let mut prof = String::new();
    for (i, name) in emergent_universe::prof::NAMES.iter().enumerate() {
        if calls[i] > 0 {
            prof.push_str(&format!("{{\"n\":\"{}\",\"ns\":{},\"c\":{}}},", name.trim(), ns[i], calls[i]));
        }
    }
    let mut items = String::new();
    for (t, i, k) in &census {
        items.push_str(&format!("[{},{},{}],", t, i, k));
    }
    let next: Vec<String> = (0..u.n_bodies()).filter_map(|i| u.bodies().next_time(i)).map(|t| t.to_string()).collect();
    format!(
        "{{\"arm\":\"{}\",\"digest\":\"{}\",\"horizon\":{},\"resolved\":{},\"census\":[{}],\"prof\":[{}],\"next\":[{}],\"wall_ms\":{:.1},\"rss_kb\":{}}}\n",
        tag,
        u.digest(),
        horizon,
        census.len(),
        items.trim_end_matches(','),
        prof.trim_end_matches(','),
        next.join(","),
        wall_ms,
        rss_hwm_kb()
    )
}

fn main() {
    let n: usize = std::env::args().nth(1).and_then(|a| a.parse().ok()).unwrap_or(10_000);
    let seed: u64 = std::env::args().nth(2).and_then(|a| a.parse().ok()).unwrap_or(3);
    let arms: Vec<String> = std::env::args().nth(3).unwrap_or_else(|| "belt0,beltD".into()).split(',').map(String::from).collect();
    let mut out = String::new();
    for arm in arms {
        let t0 = std::time::Instant::now();
        if arm == "belt0" {
            // P(0.5 AU) = 2*pi*(0.5*101.3e6)^1.5 = 2.26e12 ticks; step ~ P/128; settle 3 steps.
            let a_min = 0.5 * AU as f64;
            let p_min = 2.0 * std::f64::consts::PI * a_min.powf(1.5);
            let t = (3.0 * p_min / 128.0) as Tick;
            let mut u = belt0(n, seed);
            let t_c = t0.elapsed().as_millis() as f64;
            u.settle(t);
            out.push_str(&json_arm(&format!("belt0-n{}-s{}", n, seed), &u, t, t_c + t0.elapsed().as_millis() as f64 - t_c));
        } else if arm == "beltD" {
            // r_min = 4313*1.2 root units, GM = 2^-18: P = 2*pi*sqrt(r_min^3 * 2^18) = 1.20e9; 3 steps of P/128.
            let r_min = 4_313.0 * 1.2;
            let p_min = 2.0 * std::f64::consts::PI * (r_min * r_min * r_min * (1u64 << 18) as f64).sqrt();
            let t = (3.0 * p_min / 128.0) as Tick;
            let (mut u, _) = beltd(n, seed);
            let t_c = t0.elapsed().as_millis() as f64;
            u.settle(t);
            out.push_str(&json_arm(&format!("beltD-n{}-s{}", n, seed), &u, t, t_c + t0.elapsed().as_millis() as f64 - t_c));
        } else {
            panic!("unknown arm {}", arm);
        }
    }
    print!("{}", out);
}
