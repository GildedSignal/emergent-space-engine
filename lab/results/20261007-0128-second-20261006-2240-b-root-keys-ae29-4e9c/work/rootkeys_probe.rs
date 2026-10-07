//! A probe (not a shipped test): the author's P6 scene parameterized by β, counting how many
//! members' next-event keys silently sit at the unsheared doll tick because the centre's readout
//! refused (`horizon_of == plan.first().t` while the float oracle cannot see the centre either).
use emergent_space::orbit::Scalar;
use emergent_universe::num::{from_f64, s, to_f64};
use emergent_universe::scenario::STAR_RADIUS;
use emergent_universe::universe::Universe;
use emergent_universe::{Config, Kind, OrbitSpec};

const MASS_LOG2: i32 = -10;
const MEMBERS: usize = 200;

fn scene(beta: f64, specs: &[(u32, u32, i64)]) -> (Universe, usize, Vec<usize>) {
    let mut u = Universe::new(s(STAR_RADIUS), Config::default());
    let planet = u
        .add_body_state(Kind::Planet, 0, [s(500_000), s(0)], [Scalar::ZERO, from_f64(beta)], Scalar::ZERO)
        .unwrap();
    let doll = u.add_doll("fast", planet, MASS_LOG2, Scalar::raw(10, 10).unwrap()).unwrap();
    let ids: Vec<usize> = specs
        .iter()
        .map(|&(angle, phase, r)| {
            u.add_body(
                Kind::Ship,
                OrbitSpec { doll, periapsis: Scalar::raw(r as i128, 0).unwrap(), e_q48: 0, clockwise: false, angle, phase },
                Scalar::ZERO,
            )
            .unwrap()
        })
        .collect();
    u.start().unwrap();
    (u, planet, ids)
}

/// The float oracle: None exactly where the centre's committed readout refuses.
fn image(u: &Universe, planet: usize, i: usize) -> Option<f64> {
    let rec = u.rec(i);
    let t = rec.plan.first()?.t;
    let b = u.bodies().binding_at(i, t)?;
    let (x, _) = b.cartesian(t).ok()?;
    let to_root = 2f64.powi(-(u.dolls[b.doll as usize].shift as i32));
    let xr = [to_f64(x[0]) * to_root, to_f64(x[1]) * to_root];
    let pb = u.bodies().binding_at(planet, t)?;
    let (_, w) = pb.cartesian(t).ok()?;
    let w2 = to_f64(w[0]) * to_f64(w[0]) + to_f64(w[1]) * to_f64(w[1]);
    let g = 1.0 / (1.0 - w2).sqrt();
    Some(g * (to_f64(w[0]) * xr[0] + to_f64(w[1]) * xr[1]))
}

#[test]
fn probe_silent_fallback_by_beta() {
    let specs: Vec<(u32, u32, i64)> = (0..MEMBERS)
        .map(|k| {
            let f = k as f64 / MEMBERS as f64;
            let r = (1u64 << 18) as f64 * (1.0 + 63.0 * f);
            ((f * 4294967296.0) as u32, (f * 4294967296.0) as u32, r as i64)
        })
        .collect();
    for beta in [0.5f64, 0.9, 0.99] {
        let (u, planet, ids) = scene(beta, &specs);
        let mut readable = 0;
        let mut silent = 0;
        let mut worst = 0f64;
        for &i in &ids {
            let t = u.rec(i).plan.first().unwrap().t;
            let key = u.horizon_of(i).unwrap();
            match image(&u, planet, i) {
                Some(img) => {
                    readable += 1;
                    worst = worst.max(((key - t) as f64 - img).abs());
                }
                None => {
                    // The centre's readout refused: the oracle is blind here. Where does the key sit?
                    if key == t {
                        silent += 1; // the unsheared doll tick: the old, wrong convention
                    }
                }
            }
        }
        println!(
            "beta {beta}: members {MEMBERS}, readable {readable} (worst image miss {worst:.3}), oracle-blind {}, of which key silently unsheared {silent}",
            MEMBERS - readable
        );
        }
    }
