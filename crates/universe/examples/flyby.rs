// A flyby of a Jupiter-like planet (mass 2^-10 of the star's, radius 49,000 root units), the plane's close-pass path: ships
// that enter the planet's doll on a hyperbola of periapsis `r_p` planet radii and v_inf km/s (two-body about the planet), start
// 100 periapsis radii out, and are followed past periapsis. Reported per ship: whether it survived, the error of the sweep of
// its position angle between the start and the first sample outbound at the start's radius against the hyperbola's (radians),
// and the relative changes of its energy and angular momentum about the planet (the star's tide is the floor: it acts for days).
// `flyby [V_INF_KMS] [RP ...]`, e.g. `flyby 10 1.3 1.5 2 3.2 5 10 50`. READ=raw uses the tubes alone (no ramp).
use emergent_space::orbit::Scalar;
use emergent_universe::num::{from_f64, s, to_f64};
use emergent_universe::observe::{root_state, root_state_raw};
use emergent_universe::scenario::STAR_RADIUS;
use emergent_universe::universe::Universe;
use emergent_universe::{Config, Kind, OrbitSpec};

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let vinf_kms: f64 = args.first().map(|a| a.parse().unwrap()).unwrap_or(10.0);
    let rps: Vec<f64> = if args.len() > 1 { args[1..].iter().map(|a| a.parse().unwrap()).collect() } else { vec![1.3, 1.5, 2.0, 3.2, 5.0, 10.0, 50.0] };
    let raw = std::env::var("READ").is_ok_and(|v| v == "raw");
    let (mu_log2, sep) = (-10i32, 527_000_000i64);
    let vinf = vinf_kms / 299_792.458;
    let rad_doll = 49_000.0 * 2f64.powi(-mu_log2); // the planet's radius in its doll's units (GM = 1)
    let mut u = Universe::new(s(STAR_RADIUS), Config::default());
    let planet = u.add_body(Kind::Planet, OrbitSpec { doll: 0, periapsis: s(sep), e_q48: 0, clockwise: false, angle: 0, phase: 0 }, Scalar::ZERO).unwrap();
    let doll = u.add_doll("planet", planet, mu_log2, Scalar::raw(49_000, -mu_log2).unwrap()).unwrap();
    let mut ships = Vec::new();
    for &rp in &rps {
        let r_p = rp * rad_doll;
        let e = 1.0 + r_p * vinf * vinf;
        let l = (r_p * (1.0 + e)).sqrt(); // sqrt(GM p)
        let d0: f64 = std::env::var("D0").ok().and_then(|v| v.parse().ok()).unwrap_or(100.0) * r_p;
        let v0 = (vinf * vinf + 2.0 / d0).sqrt();
        let y0 = l / v0;
        let x0 = -(d0 * d0 - y0 * y0).sqrt();
        let id = match u.add_body_state(Kind::Ship, doll, [from_f64(x0), from_f64(y0)], [from_f64(v0), Scalar::ZERO], Scalar::ZERO) { Ok(i) => i, Err(e) => { println!("r_p {rp}: refused {e:?}"); continue } };
        ships.push((id, r_p, e, d0, [x0, y0], v0));
    }
    u.start().unwrap();
    let k = 2f64.powi(mu_log2); // doll units to root units: root = doll * 2^mu_log2
    println!("flyby of a planet of 2^{mu_log2}, v_inf {vinf_kms} km/s, tubes {}", if raw { "raw" } else { "ramped" });
    for (id, r_p, e, d0, p0, v0) in ships {
        let p = (r_p * (1.0 + e)).max(1.0);
        let f0 = ((p / d0 - 1.0) / e).acos();
        let transit = 2.0 * d0 / v0 / k.recip(); // ticks, roughly
        let n = 4000;
        let (mut alive_to, mut best): (f64, Option<(f64, [f64; 3])>) = (0.0, None);
        let mut min_r = f64::INFINITY;
        let jac0 = |pos: [f64; 2], vel: [f64; 2]| {
            let r = (pos[0] * pos[0] + pos[1] * pos[1]).sqrt();
            (0.5 * (vel[0] * vel[0] + vel[1] * vel[1]) - 1.0 / r, pos[0] * vel[1] - pos[1] * vel[0])
        };
        let (e0, l0) = jac0(p0, [v0, 0.0]);
        let mut passed = false;
        for j in 1..=n {
            let t = (j as f64 / n as f64 * 1.6 * transit) as i64;
            u.settle(t);
            if !u.rec(id).alive {
                break;
            }
            alive_to = t as f64;
            let ctx = u.ctx();
            let f = if raw { root_state_raw } else { root_state };
            let (xs, vs) = f(&ctx, id, t).unwrap();
            let (xp, vp) = f(&ctx, planet, t).unwrap();
            let rel = [(xs[0] - xp[0]) / k, (xs[1] - xp[1]) / k];
            let vrel = [vs[0] - vp[0], vs[1] - vp[1]];
            let r = (rel[0] * rel[0] + rel[1] * rel[1]).sqrt();
            min_r = min_r.min(r);
            let radial = rel[0] * vrel[0] + rel[1] * vrel[1];
            if radial > 0.0 {
                passed = true;
            }
            if passed && r >= d0 && best.is_none() {
                // the sweep of the position angle from the start, in the sense of the motion
                let cross = p0[0] * rel[1] - p0[1] * rel[0];
                let dot = p0[0] * rel[0] + p0[1] * rel[1];
                let mut ang = (cross * l0.signum()).atan2(dot);
                if ang < 0.0 {
                    ang += std::f64::consts::TAU;
                }
                let fs = ((p / r - 1.0) / e).clamp(-1.0, 1.0).acos();
                let (e1, l1) = jac0(rel, vrel);
                // the swept angle: the start is at true anomaly -f0, the sample at +fs
                best = Some((ang - (f0 + fs), [(e1 - e0) / e0.abs().max(1e-300), (l1 - l0) / l0, r / d0]));
            }
        }
        let _ = alive_to;
        let lost = !u.rec(id).alive;
        match best {
            Some((da, [de, dl, rr])) => println!("  r_p {:>5.1} R: survived, min r {:.2} R, sweep error {da:+.2e} rad, dE/E {de:+.2e}, dL/L {dl:+.2e} (sample at {rr:.4} of the start's radius)", r_p / rad_doll, min_r / rad_doll),
            None => println!("  r_p {:>5.1} R: {} (min r {:.2} R)", r_p / rad_doll, if lost { "LOST" } else { "did not come out in 1.6 transits" }, min_r / rad_doll),
        }
        let _ = to_f64;
    }
    println!("{} handoffs, {} lost", u.stats.handoffs, u.stats.lost);
}
