//! TEMPORARY repro (delete after use): C1 64-body world, trace pair (47,55).
use emergent_engine::{math::{r, Vec2}, propagator::Inertial, runtime::Body, Engine, WorkBudget};
struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 { self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15); let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9); z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB); z ^ (z >> 31) }
    fn range(&mut self, lo: i128, hi: i128) -> i128 { lo + (self.next() as u128 % (hi - lo + 1) as u128) as i128 }
}
fn world() -> Engine {
    let n = 64u64; let mut rng = Rng(2718281828u64 ^ n ^ 0xC1); let side = 8; let mut bodies = vec![];
    for i in 0..n as i128 {
        let p = [(i % side) * 8 + rng.range(-2, 2), (i / side) * 8 + rng.range(-2, 2)];
        let v = [rng.range(-512, 512), rng.range(-512, 512)];
        let mut b = Body::new(i as u64 + 1, "c1", Inertial::new(0, Vec2::new(p[0], p[1]), Vec2 { x: r(v[0]) / r(1024), y: r(v[1]) / r(1024) }).unwrap(), r(1), r(1));
        b.stop_on_contact = true; bodies.push(b);
    }
    Engine::new(2718281828, bodies, vec![]).unwrap()
}
fn main() {
    let watch: Vec<u64> = std::env::args().skip(1).map(|s| s.parse().unwrap()).collect();
    for budget in [1_000_000usize, 8] {
        let mut e = world(); e.incremental_sap = std::env::var("FULL").is_err();
        while !e.advance(128, WorkBudget::new(budget)).unwrap().complete {}
        println!("== budget {budget}");
        for ev in e.sorted_events() { if ev.subjects.iter().any(|s| watch.contains(s)) { println!("  event {} {:?} {}", ev.tick, ev.subjects, ev.detail); } }
        for id in &watch { let b = e.decode(*id).unwrap(); println!("  body {id}: {:?}", b.segments.iter().map(|s| (s.epoch, format!("({}, {})", s.origin.x, s.origin.y), format!("({}, {})", s.velocity.x, s.velocity.y))).collect::<Vec<_>>()); }
        let audit = e.independent_inertial_facts(128).unwrap().contacts;
        println!("  audit: {:?}", audit.iter().filter(|c| watch.contains(&c.1) || watch.contains(&c.2)).collect::<Vec<_>>());
    }
}
