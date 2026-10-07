use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::{Budget, Config};

fn main() {
    let mut p = plane(Config::default(), 7, Order::Sparse, 1, 16).unwrap();
    p.u.advance(5_000_000, Budget::unlimited());
    for &i in &[p.moon, p.ships[14], p.ships[20], p.player] {
        let rec = p.u.rec(i);
        let t = rec.plan.first().map(|x| x.t).unwrap_or(-1);
        let key = p.u.horizon_of(i).unwrap_or(-1);
        println!("{:>10} (doll {}): next doll tick {t}, root key {key}, offset {}", p.names[i], rec.b.doll, key - t);
    }
    let f = p.u.fleets[0].tick();
    println!("fleet: battle tick {f}");
}
