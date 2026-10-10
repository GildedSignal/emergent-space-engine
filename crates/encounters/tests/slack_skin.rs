mod support;
use emergent_encounters::kepler::Body;
use emergent_encounters::method::{pair_events, Stats};
use emergent_encounters::skin::{displacement_bound, SkinStats, SlackSkin};
use std::collections::BTreeMap;
use std::f64::consts::TAU;
use support::{EPS, RHO};

macro_rules! gate {
    ($test:ident,$scene:literal) => {
        #[test]
        fn $test() {
            for eps in EPS {
                let mut pairs=BTreeMap::new();
                let mut stats=SkinStats::default();
                let (truth,missed,false_)=support::run($scene,eps,|i,j,bi,bj,t0,t1,out| {
                    pairs.entry((i,j)).or_insert_with(||SlackSkin::contact_scale(RHO,1.1))
                        .events(bi,bj,t0,t1,&mut stats,out);
                });
                println!("slack-truth scene={} eps={eps:e} truth={truth} missed={missed} false={false_} setups={} reused={} evals={}",$scene,stats.setups,stats.reused,stats.setup_evals+stats.query.evals);
                assert_eq!((missed,false_),(0,0));
                assert!(stats.reused>0);
            }
        }
    };
}
gate!(belt, "belt");
gate!(ring, "ring");
gate!(fleet, "fleet");
gate!(equal_period, "equal");
gate!(hot, "hot");

#[test]
fn displacement_bound_covers_correlated_and_reversing_kicks() {
    for seed in 0..8 {
        let a = Body::new(0.5 + seed as f64 * 0.25, 0.01 + seed as f64 * 0.1, 0.7, 1.3);
        let mut b = a;
        for k in 0..64 {
            let t0 = k as f64 * TAU;
            b = support::kick(b, t0, if k % 7 == 0 { -1e-4 } else { 1e-4 }, k);
            let t1 = t0 + 100.0 * TAU;
            let bound = displacement_bound(&a, &b, t0, t1);
            for q in 0..64 {
                let t = t0 + (t1 - t0) * q as f64 / 63.0;
                let (x, y) = (a.state(t), b.state(t));
                assert!((x[0] - y[0]).hypot(x[1] - y[1]) <= bound, "{seed} {k} {q}");
            }
        }
    }
}

#[test]
fn phase_only_and_long_horizon_exhaust_slack() {
    let a = Body::new(1.0, 0.02, 0.0, 0.0);
    let b = Body::new(1.01, 0.01, 1.0, 0.4);
    let mut skin = SlackSkin::new(RHO, 1e-4, 1.1);
    let mut st = SkinStats::default();
    skin.events(&a, &b, 0.0, TAU, &mut st, &mut vec![]);
    skin.events(&a, &b, 0.0, 1e6 * TAU, &mut st, &mut vec![]);
    assert_eq!(st.setups, 1, "unchanged tubes do not age");
    let phase = Body::with_period(a.period, a.e, a.pom, 0.01);
    assert_eq!(a.binet(), phase.binet());
    skin.events(&phase, &b, 0.0, TAU, &mut st, &mut vec![]);
    assert_eq!(st.setups, 2, "Binet identity does not certify phase identity");
    let tiny = support::kick(phase, TAU, 1e-8, 0);
    skin.events(&tiny, &b, TAU, 2.0 * TAU, &mut st, &mut vec![]);
    assert_eq!(st.setups, 3, "the zero-slack fallback resets before a small change");
    // A freshly rebuilt anchor is identical to tiny at every horizon. Change the period again
    // so the long query actually has phase drift to exhaust (the short query still reuses).
    let drift = support::kick(tiny, 2.0 * TAU, 1e-8, 0);
    skin.events(&drift, &b, 2.0 * TAU, 3.0 * TAU, &mut st, &mut vec![]);
    assert_eq!(st.setups, 3);
    skin.events(&drift, &b, 2.0 * TAU, 1e6 * TAU, &mut st, &mut vec![]);
    assert_eq!(st.setups, 4, "period drift cannot be reused past its horizon");
}

#[test]
fn empty_certificate_revalidates_before_new_contact() {
    let a = Body::new(1.0, 0.0, 0.0, 0.0);
    let far = Body::new(1.1, 0.0, 0.0, 0.0);
    let near = Body::new(1.0001, 0.0, 0.0, 0.001);
    let mut skin = SlackSkin::contact_scale(RHO, 1.1);
    let mut st = SkinStats::default();
    let mut out = vec![];
    skin.events(&a, &far, 0.0, TAU, &mut st, &mut out);
    assert!(out.is_empty());
    skin.events(&a, &near, 0.0, 30.0 * TAU, &mut st, &mut out);
    assert_eq!(st.setups, 2);
    let mut expected = vec![];
    pair_events(
        &a,
        &near,
        RHO,
        1.1,
        0.0,
        30.0 * TAU,
        &mut Stats::default(),
        &mut expected,
    );
    assert_eq!(out, expected);
}

#[test]
fn setup_cost_is_measured_on_the_crates_kick_workload() {
    use emergent_encounters::belt::{make_belt, Spec};
    let bodies = make_belt(&Spec {
        name: "setup-cost".into(),
        n: 1000,
        sigma_e: 0.01,
        rho: 1e-4,
        a_lo: 1.0,
        a_hi: 1.5,
        keys: 0,
        seed: 20261050,
        orbits: 16.0,
    });
    for eps in EPS {
        let (mut setups, mut base, mut se, mut be, mut checks) = (0, 0, 0, 0, 0);
        let mut digest = (0u64, 0u64);
        let (mut initial_setups, mut initial_skin_evals, mut initial_base_evals) = (0, 0, 0);
        for q in 0..16 {
            let i = (q * 97 + 13) % bodies.len();
            let mut b = bodies[i];
            let mut caches: BTreeMap<usize, SlackSkin> = BTreeMap::new();
            let mut st = SkinStats::default();
            let mut bs = Stats::default();
            // Populate each pair once; initial setup is reported separately from maintenance.
            for (j, bj) in bodies.iter().enumerate().filter(|(j, _)| *j != i) {
                if !emergent_encounters::pairs::is_candidate(&b, bj, 1e-4) {
                    continue;
                }
                let mut cache = SlackSkin::contact_scale(1e-4, 1.1);
                cache.events(&b, bj, 0.0, TAU, &mut st, &mut vec![]);
                let mut cold = Stats::default();
                pair_events(&b, bj, 1e-4, 1.1, 0.0, TAU, &mut cold, &mut vec![]);
                initial_base_evals += cold.evals;
                caches.insert(j, cache);
            }
            let initial = (st.setups, st.setup_evals + st.query.evals);
            initial_setups += initial.0;
            initial_skin_evals += initial.1;
            for seg in 1..=16 {
                let t0 = seg as f64 * TAU;
                b = support::kick(b, t0, eps, 0);
                for (j, bj) in bodies.iter().enumerate().filter(|(j, _)| *j != i) {
                    if !emergent_encounters::pairs::is_candidate(&b, bj, 1e-4) {
                        continue;
                    }
                    let mut direct = vec![];
                    pair_events(&b, bj, 1e-4, 1.1, t0, t0 + TAU, &mut bs, &mut direct);
                    let mut cached = vec![];
                    caches
                        .entry(j)
                        .or_insert_with(|| SlackSkin::contact_scale(1e-4, 1.1))
                        .events(&b, bj, t0, t0 + TAU, &mut st, &mut cached);
                    digest.0 += direct.len() as u64;
                    digest.1 += cached.len() as u64;
                    for x in &direct {
                        assert!(cached.iter().any(|y| (x.0 - y.0).abs() < 1e-6));
                    }
                    for x in &cached {
                        assert!(direct.iter().any(|y| (x.0 - y.0).abs() < 1e-6));
                    }
                }
            }
            setups += st.setups - initial.0;
            base += bs.pairs;
            se += st.setup_evals + st.query.evals - initial.1;
            be += bs.evals;
            checks += st.query.checks_total();
        }
        let reduction = if setups == 0 {
            f64::INFINITY
        } else {
            base as f64 / setups as f64
        };
        println!("skin-cost eps={eps:e} kicks=256 always_setups={base} skin_setups={setups} setups_per_kick={:.4}->{:.4} reduction={:.3} always_evals={be} skin_evals={se} cold_setups={initial_setups} cold_base_evals={initial_base_evals} cold_skin_evals={initial_skin_evals} checks={checks} events={digest:?}",base as f64/256.0,setups as f64/256.0,reduction);
        assert!(setups <= base);
    }
}

fn dense_kicked_truth(name: &str, hi: f64, eps: f64) {
    use emergent_encounters::belt::{make_belt, Spec};
    {
        let mut bodies = make_belt(&Spec {
            name: name.into(),
            n: 64,
            sigma_e: 0.025,
            rho: RHO,
            a_lo: 1.0,
            a_hi: hi,
            keys: 0,
            seed: 20261008,
            orbits: 4.0,
        });
        let mut caches = BTreeMap::new();
        let mut st = SkinStats::default();
        let (mut n, mut missed, mut false_, mut base_missed) = (0, 0, 0, 0);
        for seg in 0..4 {
            let t0 = seg as f64 * TAU;
            let t1 = t0 + TAU;
            for (i, b) in bodies.iter_mut().enumerate() {
                *b = support::kick(*b, t0, if i % 3 == 0 { -eps } else { eps }, (i + seg) % 4);
            }
            for i in 0..bodies.len() {
                for j in i + 1..bodies.len() {
                    let tr = support::truth(&bodies[i], &bodies[j], t0, t1);
                    let mut direct = vec![];
                    pair_events(
                        &bodies[i],
                        &bodies[j],
                        RHO,
                        1.1,
                        t0,
                        t1,
                        &mut Stats::default(),
                        &mut direct,
                    );
                    let mut got = vec![];
                    caches
                        .entry((i, j))
                        .or_insert_with(|| SlackSkin::contact_scale(RHO, 1.1))
                        .events(&bodies[i], &bodies[j], t0, t1, &mut st, &mut got);
                    for x in &tr {
                        n += 1;
                        missed += (!got.iter().any(|y| (x.0 - y.0).abs() < 1e-6)) as u64;
                        base_missed += (!direct.iter().any(|y| (x.0 - y.0).abs() < 1e-6)) as u64;
                    }
                    // The baseline comparison checks every extra candidate report, including
                    // shallow terraces; the independent oracle checks completeness separately.
                    for x in &got {
                        false_ += (!direct.iter().any(|y| (x.0 - y.0).abs() < 1e-6)) as u64;
                    }
                }
            }
        }
        println!("dense-kicked scene={name} eps={eps:e} truth={n} baseline_missed={base_missed} skin_missed={missed} extras_vs_baseline={false_}");
        assert!(n > 0, "a completeness probe must exercise encounters");
        assert_eq!((missed, false_, base_missed), (0, 0, 0));
    }
}

macro_rules! dense_gate {
    ($test:ident, $scene:literal, $hi:expr, $eps:expr) => {
        #[test]
        fn $test() {
            dense_kicked_truth($scene, $hi, $eps);
        }
    };
}
dense_gate!(dense_belt_e8, "belt", 1.5, 1e-8);
dense_gate!(dense_belt_e7, "belt", 1.5, 1e-7);
dense_gate!(dense_belt_e6, "belt", 1.5, 1e-6);
dense_gate!(dense_belt_e5, "belt", 1.5, 1e-5);
dense_gate!(dense_belt_e4, "belt", 1.5, 1e-4);
dense_gate!(dense_ring_e8, "ring", 1.0025, 1e-8);
dense_gate!(dense_ring_e7, "ring", 1.0025, 1e-7);
dense_gate!(dense_ring_e6, "ring", 1.0025, 1e-6);
dense_gate!(dense_ring_e5, "ring", 1.0025, 1e-5);
dense_gate!(dense_ring_e4, "ring", 1.0025, 1e-4);

#[test]
fn literal_skin_negative_control_misses_a_phase_kick() {
    use emergent_encounters::method::run_section_on;
    use emergent_encounters::pairs::sections;
    let a = Body::new(1.0, 0.02, 0.0, 0.0);
    let old = Body::new(1.0, 0.021, 0.0, 0.4);
    let current = Body::new(1.0, 0.021, 0.0, 0.001);
    let truth = support::truth(&a, &current, 0.0, 4.0 * TAU);
    assert!(!truth.is_empty());
    let mut literal = vec![];
    for sec in sections(&a, &old, RHO, 1.1, &mut 0) {
        run_section_on(
            &a,
            &old,
            &a,
            &current,
            &sec,
            RHO,
            0.0,
            4.0 * TAU,
            &mut Stats::default(),
            &mut literal,
        );
    }
    assert!(truth.iter().any(|x| !literal.iter().any(|y| (x.0 - y.0).abs() < 1e-6)));
    let mut skin = SlackSkin::contact_scale(RHO, 1.1);
    let mut st = SkinStats::default();
    skin.events(&a, &old, 0.0, 4.0 * TAU, &mut st, &mut vec![]);
    let mut got = vec![];
    skin.events(&a, &current, 0.0, 4.0 * TAU, &mut st, &mut got);
    assert_eq!(st.setups, 2);
    assert!(truth.iter().all(|x| got.iter().any(|y| (x.0 - y.0).abs() < 1e-6)));
}
