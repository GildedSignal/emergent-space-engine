use emergent_shipmem::belt::{eccentricity, Belt, BeltError, Columns};
use emergent_shipmem::codec::{Buf, Enc};
use emergent_shipmem::program::Program;
use std::thread;

fn belt() -> Belt {
    Belt::new(Belt::LAB_KEYS, Columns::Independent).unwrap()
}

#[test]
fn regeneration_is_bit_identical_across_orders_and_threads() {
    let n = 1 << 16;
    let b = belt();
    let expected: Vec<_> = (0..n).map(|i| b.eval(i)).collect();
    for i in 0..n {
        let (p, _, _, _, _) = b.draws(i);
        assert!((2048 << 16..2560 << 16).contains(&p));
    }
    let p = b.population(n, &mut Enc::new(true));
    for threads in [1, 2, 7] {
        thread::scope(|scope| {
            for lane in 0..threads {
                let (expected, p) = (&expected, &p);
                scope.spawn(move || {
                    for i in (0..n).rev().filter(|i| i % threads == lane) {
                        let mut s = [0; 8];
                        p.eval(i, &mut s);
                        assert_eq!(s, expected[i as usize]);
                    }
                });
            }
        });
    }
}

#[test]
fn exact_round_trip_with_scars_splits_stream_and_reabsorption() {
    let n = 8192;
    let b = belt();
    let mut enc = Enc::new(true);
    let mut expected: Vec<_> = (0..n).map(|i| b.eval(i)).collect();
    let mut p = Program::with_prog(&expected, 5, b.programs(), &mut enc);
    assert_eq!(p.scars(), 0);
    for i in (0..n).step_by(31) {
        let s = &mut expected[i as usize];
        s[0] = s[0].wrapping_add(17);
        s[2] = s[2].wrapping_sub(3);
        s[3] = s[3].wrapping_add(9);
        s[4] = s[4].wrapping_add(7);
        p.update(i, *s);
    }
    for i in (0..n).rev() {
        let mut s = [0; 8];
        p.eval(i, &mut s);
        assert_eq!(s, expected[i as usize]);
    }
    p.seal(&mut enc);
    let split = 3907;
    let (left, right) = p.split(split, &mut enc);
    let (mut buf, mut rbuf) = (Buf::default(), Buf::default());
    for (store, offset) in [(&p, 0), (&left, 0), (&right, split)] {
        let bounds = store.bounds(0, store.n - 1);
        store.for_each(&mut buf, &mut rbuf, |start, buf| {
            for j in 0..buf.n {
                let i = start + j as u64;
                let mut s = [0; 8];
                store.eval(i, &mut s);
                for c in 0..5 {
                    assert_eq!(buf.col[c][j], expected[(offset + i) as usize][c]);
                    assert_eq!(s[c], buf.col[c][j]);
                    assert!((bounds[c].0..=bounds[c].1).contains(&(s[c] as i128)));
                }
            }
        });
        assert_eq!(store.count_arc(0, u64::MAX), None);
    }
    for i in (0..n).step_by(31) {
        p.update(i, b.eval(i));
    }
    p.seal(&mut enc);
    assert_eq!(p.scars(), 0);
    assert_eq!(p.bytes(), b.population(n, &mut enc).bytes());
}

#[test]
fn distinct_states_at_both_belt_sizes() {
    // Unique (time, angle, kind) implies unique full states; keep only this exact
    // projection while sorting, so the 2^23 rung does not materialize 512 MiB.
    for keys in [Belt::LAB_KEYS, [1, 3, 5, 7, 9]] {
        let b = Belt::new(keys, Columns::Independent).unwrap();
        for n in [1 << 20, 1 << 23] {
            let mut signatures: Vec<u128> = (0..n)
                .map(|i| {
                    let (_, _, kind, angle, time) = b.draws(i);
                    time as u128 | ((angle as u128) << 44) | ((kind as u128) << 76)
                })
                .collect();
            signatures.sort_unstable();
            assert!(
                signatures.windows(2).all(|w| w[0] != w[1]),
                "n={n} keys={keys:?}"
            );
        }
    }
}

#[test]
fn dyadic_tail_covers_the_discrete_rayleigh_endpoints() {
    let max = eccentricity(u64::MAX);
    let reference =
        (0.07f64 * (-2.0 * (0.5f64 / 2f64.powi(64)).ln()).sqrt() * 2f64.powi(30)) as u32;
    assert_eq!(max, reference);
    assert!(max > (0.6 * 2f64.powi(30)) as u32);
    let threshold = u64::MAX - ((1e-4 * 2f64.powi(64)) as u64);
    assert!(eccentricity(threshold) > (0.300 * 2f64.powi(30)) as u32);
    let mut previous = 0;
    for z in 12..64 {
        let u = u64::MAX - (1u64 << (63 - z));
        let e = eccentricity(u);
        assert!(e >= previous);
        previous = e;
    }
    assert!(max >= previous);
}

#[test]
fn refuses_correlations_and_nonbijective_keys() {
    assert_eq!(
        Belt::new(Belt::LAB_KEYS, Columns::Correlated),
        Err(BeltError::CorrelatedColumns)
    );
    assert_eq!(
        Belt::new([2, 3, 5, 7, 9], Columns::Independent),
        Err(BeltError::InvalidKeys)
    );
    assert_eq!(
        Belt::new([1, 1, 5, 7, 9], Columns::Independent),
        Err(BeltError::InvalidKeys)
    );
}
