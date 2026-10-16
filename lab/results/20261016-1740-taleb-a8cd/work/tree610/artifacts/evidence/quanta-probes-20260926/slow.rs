// Does the relativistic law's energy ledger see slow kinetic energy? Same gas, speeds up to
// beta_max, both laws; Newtonian kinetic energy sum m|k|^2 at genesis vs end (plus the law's own
// energy residual for the Newtonian law), and the relativistic energy carry total.
use emergent_lattice::{worlds, Law, Stepper};
use emergent_lattice_event::EventCore;
fn main() {
    let q: i64 = 1 << 20;
    for beta in [0.001f64, 0.004, 0.02, 0.25] {
        let vmax = (beta * q as f64) as i64;
        for law in [Law::Newtonian, Law::Relativistic] {
            let mut w0 = worlds::gas(4096, 0.1, q, vmax, 9);
            if law == Law::Relativistic { w0 = w0.with_law(law).unwrap(); }
            // Relativistic kinetic energy sum m(γ−1), γ−1 = β²/(√(1−β²)(1+√(1−β²))) (no cancellation).
            let ke = |w: &emergent_lattice::World| w.bodies.iter().map(|b| { let b2 = ((b.k[0] as f64).powi(2) + (b.k[1] as f64).powi(2)) / (q as f64).powi(2); let r = (1.0 - b2).sqrt(); b.mass as f64 * b2 / (r * (1.0 + r)) }).sum::<f64>();
            // horizon: ~12 collisions per body (mean free path ~8 radii, radius = q units)
            let horizon = (12.0 * 8.0 * q as f64 / (0.5 * vmax as f64)) as i64;
            let mut s = EventCore::new(w0.clone(), false).unwrap();
            let t = std::time::Instant::now();
            s.run_to(horizon);
            let w1 = s.world();
            let (k0, k1) = (ke(&w0), ke(&w1));
            let ecarry: i128 = w1.bodies.iter().map(|b| b.residual as i128).sum();
            println!("beta_max {beta}, {law:?}: {} contacts/body, kinetic m(γ−1) drift {:+.3e} (relative), energy residual/carry sum {ecarry}, {:.1} s",
                2 * s.log().contacts / 4096, (k1 - k0) / k0, t.elapsed().as_secs_f64());
        }
    }
}
