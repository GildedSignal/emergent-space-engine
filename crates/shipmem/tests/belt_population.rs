use emergent_shipmem::belt::{Body, Population, Spec};
const SPEC: Spec = Spec {
    p_lo: 2048 << 16,
    p_bits: 27,
    sigma_milli: 70,
    e_bits: 30,
    e_cap: 644_245_094,
    w_bits: 32,
    t_bits: 44,
};

#[test]
fn arbitrary_scar_history_is_exact_in_any_order_and_reabsorbs() {
    let mut b = Population::birth(SPEC, 10000, 17).unwrap();
    let before: Vec<_> = (0..b.len()).map(|i| b.body(i)).collect();
    let pristine = b.store();
    for i in [9999, 2, 3, 9999, 0, 1, 2] {
        b.scar(
            i,
            Body {
                p: u64::MAX - 1,
                e: 31,
                w: u64::MAX,
                t: 0,
            },
        );
        b.scar(
            i,
            Body {
                p: before[i as usize].p + 10,
                e: before[i as usize].e + 5,
                w: 0,
                t: before[i as usize].t,
            },
        );
    }
    b.scar(
        777,
        Body {
            p: 4,
            e: 5,
            w: 6,
            t: 7,
        },
    );
    let bytes = b.store();
    let round = Population::restore(&bytes).unwrap();
    assert_eq!(round.store(), bytes);
    for i in 0..b.len() {
        assert_eq!(b.body(i), round.body(i));
    }
    for i in [9999, 2, 3, 0, 1, 777] {
        b.scar(i, before[i as usize]);
    }
    b.compact();
    assert_eq!(b.store(), pristine);
    assert_eq!(
        b.bytes_used(),
        Population::birth(SPEC, 10000, 17).unwrap().bytes_used()
    );
}
#[test]
fn wrapped_angles_and_time_round_trip_as_small_deltas() {
    let mut b = Population::birth(SPEC, 100, 42).unwrap();
    for i in 0..100 {
        let mut body = b.body(i);
        body.w = body.w.wrapping_sub(16384) & ((1 << 32) - 1);
        body.t = body.t.wrapping_add(16383) & ((1 << 44) - 1);
        b.scar(i, body);
    }
    let round = Population::restore(&b.store()).unwrap();
    for i in 0..100 {
        assert_eq!(round.body(i), b.body(i));
    }
    assert!(b.bytes_used() < 1600);
}
#[test]
fn tables_and_store_follow_the_birth_parameters_not_population_size() {
    for spec in [
        SPEC,
        Spec {
            sigma_milli: 110,
            p_bits: 19,
            w_bits: 17,
            t_bits: 21,
            ..SPEC
        },
    ] {
        let a = Population::birth(spec, 10000, 8).unwrap();
        let b = Population::birth(spec, 1_000_000_000, 8).unwrap();
        assert_eq!(a.store().len(), 42);
        assert_eq!(a.store().len(), b.store().len());
        let round = Population::restore(&a.store()).unwrap();
        for i in 0..a.len() {
            assert_eq!(a.body(i), b.body(i));
            assert_eq!(a.body(i), round.body(i));
        }
    }
    assert_ne!(
        Population::birth(SPEC, 10, 8).unwrap().body(0).e,
        Population::birth(
            Spec {
                sigma_milli: 110,
                ..SPEC
            },
            10,
            8
        )
        .unwrap()
        .body(0)
        .e
    );
}
#[test]
fn malformed_stores_are_rejected_without_panicking_or_large_allocations() {
    let b = Population::birth(SPEC, 100, 42).unwrap().store();
    for end in 0..b.len() {
        assert!(Population::restore(&b[..end]).is_none());
    }
    let mut bad = b.clone();
    bad[24] = 255;
    assert!(Population::restore(&bad).is_none());
    let mut bad = b.clone();
    bad.extend([0]);
    assert!(Population::restore(&bad).is_none());
    let mut bad = b;
    bad[34..38].copy_from_slice(&u32::MAX.to_le_bytes());
    assert!(Population::restore(&bad).is_none());
}
