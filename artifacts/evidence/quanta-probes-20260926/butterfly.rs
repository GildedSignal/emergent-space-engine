// How long does a one-quantum difference stay small? Two copies of the same gas, one body
// nudged by one position unit (1/Q light-chronon). Track the spread against collisions per body.
use emergent_lattice::{worlds, Law, Stepper};
use emergent_lattice_event::EventCore;
fn main() {
    let n = 4096u64;
    for &(qbits, law) in &[(10u32, Law::Newtonian), (16, Law::Newtonian), (20, Law::Newtonian), (10, Law::Relativistic), (14, Law::Relativistic)] {
        let q = 1i64 << qbits;
        let mut w0 = worlds::gas(n, 0.1, q, q / 4, 7);
        if law == Law::Relativistic { w0 = w0.with_law(law).unwrap(); }
        let mut w1 = w0.clone();
        w1.bodies[0].x[0] += 1;
        let (mut a, mut b) = (EventCore::new(w0, false).unwrap(), EventCore::new(w1, false).unwrap());
        let r = q as f64; // body radius in units
        let (mut t_any, mut t_r) = (None, None);
        let mut t = 0;
        while t < 20000 {
            t += 16;
            a.run_to(t);
            b.run_to(t);
            let (wa, wb) = (a.world(), b.world());
            let mut diff = 0;
            let mut maxd: i64 = 0;
            for (x, y) in wa.bodies.iter().zip(&wb.bodies) {
                let d = (x.x[0] - y.x[0]).abs().max((x.x[1] - y.x[1]).abs());
                if d != 0 || x.k != y.k { diff += 1; }
                maxd = maxd.max(d);
            }
            let cpb = 2.0 * a.log().contacts as f64 / n as f64;
            if t_any.is_none() && maxd > 1 { t_any = Some((t, cpb)); }
            if t_r.is_none() && maxd as f64 >= r { t_r = Some((t, cpb, diff)); }
            if t_r.is_some() && diff as u64 > n / 2 {
                println!("Q=2^{qbits} {law:?}: first growth past 1 unit at t={} ({:.2} coll/body); reaches one radius at t={} ({:.2} coll/body, {} bodies differ); half the gas differs at t={t} ({cpb:.2} coll/body)",
                    t_any.unwrap().0, t_any.unwrap().1, t_r.unwrap().0, t_r.unwrap().1, t_r.unwrap().2);
                break;
            }
        }
        if t >= 20000 { println!("Q=2^{qbits} {law:?}: t_any={t_any:?} t_r={t_r:?} (no half-gas spread by 20000)"); }
    }
}
