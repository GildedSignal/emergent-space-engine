mod support;
use emergent_encounters::method::{pair_events, Stats};
use support::{EPS, RHO};

macro_rules! gate {
    ($test:ident,$scene:literal) => {
        #[test]
        fn $test() {
            for eps in EPS {
                let mut stats = Stats::default();
                let (truth, missed, false_) = support::run($scene, eps, |_, _, bi, bj, t0, t1, out| {
                    pair_events(bi, bj, RHO, 1.1, t0, t1, &mut stats, out);
                });
                println!(
                    "r8-truth scene={} eps={eps:e} truth={truth} missed={missed} false={false_}",
                    $scene
                );
                assert_eq!((missed, false_), (0, 0));
            }
        }
    };
}
gate!(belt, "belt");
gate!(ring, "ring");
gate!(fleet, "fleet");
gate!(equal_period, "equal");
gate!(hot, "hot");
