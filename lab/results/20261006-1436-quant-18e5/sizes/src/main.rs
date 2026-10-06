//! Cache-line audit of the plane's hot records (lab run 20261006-1436-quant).
//! The M1's line is 128 B; this x86's is 64 B. Both are printed against.
use emergent_space::orbit::Scalar;
use emergent_universe::body::{BodyRec, Item, Segment, Thrust};
use emergent_universe::view::Seen;
use emergent_universe::world::DollRec;

fn main() {
    let rows: Vec<(&str, usize)> = vec![
        ("Item (one plan item: Tick + What)", std::mem::size_of::<Item>()),
        ("BodyRec (one body, tube + plan)", std::mem::size_of::<BodyRec>()),
        ("Thrust (decision state)", std::mem::size_of::<Thrust>()),
        ("Segment (retired binding)", std::mem::size_of::<Segment>()),
        ("DollRec (one doll/frame)", std::mem::size_of::<DollRec>()),
        ("Seen (one emitter on the wire)", std::mem::size_of::<Seen>()),
        ("Scalar (one orbit scalar)", std::mem::size_of::<Scalar>()),
        ("Calendar heap element (Scalar, u32)", std::mem::size_of::<(Scalar, u32)>()),
    ];
    println!("{:<44} {:>6} {:>10} {:>12}", "type", "bytes", "x64 lines", "M1 128B lines");
    for (name, b) in rows {
        println!("{:<44} {:>6} {:>10.2} {:>12.2}", name, b, b as f64 / 64.0, b as f64 / 128.0);
    }
}
