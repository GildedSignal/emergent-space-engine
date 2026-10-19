//! The centred burn's account: cuts and turns reconcile prepaid proper time,
//! including a decision at the midpoint itself. The view performs that same payment.
use emergent_universe::num::to_f64;
use emergent_universe::observe::held_thrust;
use emergent_universe::{fleet::Order, scenario::plane, thrust::word, Config};

#[test]
fn a_cut_refunds_the_prepaid_half_and_the_view_reads_that_same_decision() {
    for keys in [1, 2, 4, 8, 5, 9] {
        let mut p = plane(Config::default(), 5, Order::Sparse, 1, 8).unwrap();
        p.u.settle(2_000_000);
        p.u.input(p.u.now, word(keys, 8)).unwrap();
        let start = p.u.rec(p.player);
        let midpoint = start
            .plan
            .iter()
            .find(|it| matches!(it.what, emergent_universe::body::What::Kick(0)))
            .unwrap()
            .t;
        p.u.settle(midpoint);
        let before = p.u.rec(p.player);
        let th = before.thrust.unwrap();
        assert!(th.ahead.is_positive(), "keys {keys}: a kick pays ahead");
        assert_eq!(th.since, midpoint);
        let (heading, dv) = held_thrust(&p.u.ctx(), &before, midpoint).unwrap().unwrap();
        let (_, v) = before.b.cartesian(midpoint).unwrap();
        let want = [to_f64(v[0]) + dv[0], to_f64(v[1]) + dv[1]];
        p.u.input(midpoint, word(0, 8)).unwrap();
        let after = p.u.rec(p.player);
        let (_, got) = after.b.cartesian(midpoint).unwrap();
        for c in 0..2 {
            assert!(
                (to_f64(got[c]) - want[c]).abs() < 1e-15,
                "keys {keys}: view and decision differ"
            );
        }
        let th = after.thrust.unwrap();
        assert_eq!(th.heading, heading);
        assert!(th.ahead.is_zero());
        assert_eq!(th.cadence_step, 0);
        assert_eq!(th.kicks, 0);
        assert_eq!(after.refusals, 0);
    }
}

#[test]
fn a_held_burn_doubles_only_every_third_whole_step_kick_and_a_decision_restarts_it() {
    let mut p = plane(Config::default(), 5, Order::Sparse, 1, 8).unwrap();
    p.u.settle(2_000_000);
    p.u.input(p.u.now, word(1, 12)).unwrap();
    let first = p.u.rec(p.player).thrust.unwrap().cadence_step;
    for k in 0..9 {
        let rec = p.u.rec(p.player);
        let th = rec.thrust.unwrap();
        assert_eq!(th.kicks, k);
        assert_eq!(rec.step, first << (k / 3));
        let midpoint = rec
            .plan
            .iter()
            .find(|it| matches!(it.what, emergent_universe::body::What::Kick(0)))
            .unwrap()
            .t;
        p.u.settle(midpoint);
        // In Home's doll the next interval is planned at the boundary.
        let boundary =
            p.u.rec(p.player)
                .plan
                .iter()
                .find(|it| it.what == emergent_universe::body::What::Boundary)
                .unwrap()
                .t;
        p.u.settle(boundary);
    }
    p.u.input(p.u.now, word(2, 12)).unwrap();
    let th = p.u.rec(p.player).thrust.unwrap();
    assert_eq!(th.kicks, 0);
    assert!(th.ahead.is_zero());
    assert_eq!(p.u.rec(p.player).refusals, 0);
}

#[test]
fn the_dynamics_cap_does_not_bank_doublings_for_a_later_jump() {
    let mut p = plane(Config::default(), 5, Order::Sparse, 1, 8).unwrap();
    p.u.settle(2_000_000);
    p.u.input(p.u.now, word(1, 0)).unwrap();
    let end = p.u.now + (2000.0 / emergent_universe::view::TICK_SECONDS) as i64;
    let mut previous = p.u.rec(p.player).step;
    while p.u.now < end {
        let rec = p.u.rec(p.player);
        let boundary = rec.plan.iter().find(|it| it.what == emergent_universe::body::What::Boundary).unwrap().t;
        if boundary > end { break; }
        p.u.settle(boundary);
        let rec = p.u.rec(p.player);
        let th = rec.thrust.unwrap();
        let limit = if th.kicks % 3 == 0 { previous * 2 } else { previous };
        assert!(rec.step <= limit, "after kick {}: step {} exceeds permitted {}", th.kicks, rec.step, limit);
        previous = rec.step;
    }
    assert_eq!(p.u.rec(p.player).refusals, 0);
}

#[test]
fn refining_the_quantum_refines_the_early_geometric_ramp_too() {
    let mut steps = Vec::new();
    for finer in [0, 4] {
        let d = Config::default();
        let cfg = Config { step_log2: d.step_log2 + finer, thrust_quantum_log2: d.thrust_quantum_log2 + finer, ..d };
        let mut p = plane(cfg, 5, Order::Sparse, 1, 8).unwrap();
        p.u.settle(2_000_000);
        p.u.input(p.u.now, word(1, 4)).unwrap();
        p.u.settle(2_000_000 + (100.0 / emergent_universe::view::TICK_SECONDS) as i64);
        steps.push(p.u.rec(p.player).interval);
        assert_eq!(p.u.rec(p.player).refusals, 0);
    }
    assert!(steps[1] <= steps[0] / 8, "16x refinement regrew the shipped ramp: {steps:?}");
}

#[test]
fn a_shortened_root_interval_pays_only_its_own_gravity() {
    use emergent_universe::{body::What, force, num::{scale2, time_of}};
    let mut p = plane(Config::default(), 5, Order::Sparse, 1, 8).unwrap();
    p.u.input(0, word(1, 15)).unwrap();
    p.u.settle((200.0 / emergent_universe::view::TICK_SECONDS) as i64);
    assert_eq!(p.u.rec(p.player).b.doll, 0);
    // Opposite turn keys cancel; the held decision still caps the clock interval.
    p.u.input(p.u.now, word(12, 8)).unwrap();
    let rec = p.u.rec(p.player);
    let mid = rec.plan.iter().find(|i| i.what == What::Kick(0)).unwrap().t;
    p.u.settle(mid - 1);
    let rec = p.u.rec(p.player);
    let (x, v) = rec.b.cartesian(mid).unwrap();
    let ctx = p.u.ctx();
    let field = force::field(&ctx.secondaries(0, mid, p.player).unwrap(), x).unwrap();
    let dv = scale2(field.accel, time_of(rec.interval, rec.b.clock_exp).unwrap()).unwrap();
    let ext = rec.ext.unwrap();
    assert!(ext.time(ext.y(field.potential).unwrap(), ext.ds).unwrap() > time_of(rec.interval * 2, rec.b.clock_exp).unwrap(), "the control must actually shorten the clock");
    p.u.settle(mid);
    let (_, got) = p.u.rec(p.player).b.cartesian(mid).unwrap();
    for c in 0..2 {
        assert!((to_f64(got[c]) - to_f64(v[c]) - to_f64(dv[c])).abs() < 1e-15);
    }
    assert_eq!(p.u.rec(p.player).refusals, 0);
}
