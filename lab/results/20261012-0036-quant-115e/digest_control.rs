//! Lab 20261012-0036 control: the plane's digest after the same settle, on pristine sources.
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::Config;

fn main() {
    let mut p = plane(Config::default(), 1, Order::Sparse, 1, 8).unwrap();
    p.u.settle(30_000_000_000);
    let s = p.u.stats;
    println!(
        "items {} (kicks {}, opens {}, boundaries {}, lost {}, refused {}) digest {}",
        s.kicks + s.opens + s.boundaries, s.kicks, s.opens, s.boundaries, s.lost, s.refused,
        p.u.digest()
    );
}
