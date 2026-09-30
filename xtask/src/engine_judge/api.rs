//! Public-contract adversarial probes: empty scenes and completeness of future-state digests.
use super::scene::{frame, world, Q, R};
use emergent_engine::{AnchorPolicy, Battle, Frame};
use emergent_lattice::{chronon::Chronon, Body, Response};

pub fn api() -> (bool, String) {
    let w = world(vec![Body::new(1, [0, 0], [0, 0], 1, 1, Response::Pass)], Q);
    let mut a = Battle::new(Chronon::new(w.clone(), false).unwrap(), frame(), 1);
    let mut b = Battle::new(
        Chronon::new(w, false).unwrap(),
        Frame::new(Q, R, 1 << 40).unwrap(),
        1,
    );
    a.run_to(0).unwrap();
    b.run_to(0).unwrap();
    let aliased = a.outcome() == b.outcome();
    let epochs = (a.next_epoch_tick(), b.next_epoch_tick());
    a.run_to(256).unwrap();
    b.run_to(256).unwrap();
    let futures_diverge = a.outcome() != b.outcome();
    // catch_unwind keeps a planted/public engine panic machine-readable as a FAIL.
    let hook = std::panic::take_hook();
    std::panic::set_hook(Box::new(|_| {}));
    let empty = std::panic::catch_unwind(|| {
        let s = Chronon::new(world(vec![], Q), false).unwrap();
        let mut b = Battle::new(s, frame(), 8)
            .with_anchoring(AnchorPolicy::default())
            .unwrap();
        b.run_to(0).unwrap();
    })
    .is_ok();
    std::panic::set_hook(hook);
    (!aliased && empty,format!("future_digest_alias={aliased} futures_diverge={futures_diverge} next_epochs={epochs:?} empty_anchor_threads8={empty} required=distinct,no_panic"))
}
