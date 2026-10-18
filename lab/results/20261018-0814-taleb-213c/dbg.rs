use emergent_space::orbit::Scalar;
use emergent_universe::scenario::{AU, STAR_RADIUS};
use emergent_universe::{Budget, Config, Kind, Mass, OrbitSpec, Universe};
fn s(v: i64) -> Scalar { Scalar::integer(v) }
fn f(x: f64) -> Scalar { Scalar::raw((x * 2f64.powi(40)) as i128, -40).unwrap() }
fn main() {
    let sep = 5 * AU;
    let mut u = Universe::new(s(STAR_RADIUS), Config::default());
    u.threads = 1;
    let mu = Mass::pow2(-10);
    let planet = u.add_body(Kind::Planet, OrbitSpec { doll: 0, periapsis: s(sep), e_q48: 0, clockwise: false, angle: 0, phase: 0 }, Scalar::ZERO).unwrap();
    u.add_doll("planet", planet, mu, Scalar::raw(47_400, -mu.octave).unwrap()).unwrap();
    let i = u.add_body_state(Kind::Ship, 0, [f(0.0), f(sep as f64)], [f(-(1.0 / sep as f64).sqrt()), f(0.0)], Scalar::ZERO).unwrap();
    u.start().unwrap();
    let rec = u.rec(i);
    println!("plan {:?}", rec.plan);
    let a = u.advance(1 << 41, Budget::events(1000));
    println!("adv events={} now={} horizon={} overflow={}", a.events, u.now, a.horizon, a.overflow);
    let rec = u.rec(i);
    println!("after: ship_ev={} interval={} plan={:?}", rec.events, rec.interval, rec.plan);
}
