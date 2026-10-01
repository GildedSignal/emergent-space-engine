// How often does a member handed out of the frame still touch the members it left? (A handed-out body
// stays in the stepper until the frame dissolves: the engine has no way to remove one.) Counts contacts
// after the first hand-out. Measured (seeds 1 3 5 7 8 11, 24/48/200 members, to 6e7 ticks): none with a member
// still in the frame; a few (2-5 of 700-900 at 200 members) between two members that had both left.
use emergent_engine::{scenes, AnchorPolicy, Battle, Frame};
use emergent_lattice::Stepper;
use emergent_lattice_event::EventCore;
use emergent_universe::fleet::{mean_motion, Q};
fn main() {
    let seeds: Vec<u64> = std::env::args().skip(1).map(|s| s.parse().unwrap()).collect();
    for seed in if seeds.is_empty() { vec![1, 3, 5, 7, 8, 11] } else { seeds } {
        for members in [24u64, 48, 200] {
            let (w, _) = scenes::battle(members, Q, seed, 1 << 15, false);
            let r_lat = 4_740 * Q;
            let n = mean_motion(-18, r_lat).unwrap();
            let frame = Frame::on_orbit(Q, r_lat, n, 0, 0x4000_0000, 0).unwrap();
            let mut b = Battle::new(EventCore::new(w, true).unwrap(), frame, 1).with_anchoring(AnchorPolicy::default()).unwrap();
            let mut t = 0i64;
            while t < 60_000_000 && b.active().iter().any(|&a| a) {
                t += 1 << 18;
                b.run_to(t).unwrap();
            }
            let hand = b.handoffs();
            let mut first: std::collections::HashMap<usize, i64> = std::collections::HashMap::new();
            for h in hand {
                first.entry(h.index).or_insert(h.tick);
            }
            let (mut all, mut ghost_member, mut ghost_ghost) = (0, 0, 0);
            for e in b.stepper().log().events.iter() {
                all += 1;
                let (ia, ib) = ((e.a - 1) as usize, (e.b - 1) as usize);
                let ga = first.get(&ia).is_some_and(|&ht| e.tick > ht);
                let gb = first.get(&ib).is_some_and(|&ht| e.tick > ht);
                // the other is still in the frame at that tick (not yet handed out)
                let live_a = !first.get(&ia).is_some_and(|&ht| e.tick > ht);
                let live_b = !first.get(&ib).is_some_and(|&ht| e.tick > ht);
                if (ga && live_b) || (gb && live_a) { ghost_member += 1; }
                if ga && gb { ghost_ghost += 1; }
            }
            println!("seed {seed} members {members}: to tick {t}, {} handed out in {} anchors, contacts {all}, ghost-with-live-member {ghost_member}, ghost-ghost {ghost_ghost}, first hand-out tick {:?}", hand.len(), b.stats().anchors, first.values().min());
        }
    }
}
