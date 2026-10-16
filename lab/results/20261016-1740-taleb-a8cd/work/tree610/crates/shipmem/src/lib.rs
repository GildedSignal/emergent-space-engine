//! Research crate (artifacts/runs/opus-shipmem): ships in memory, grouped by description
//! without averaging, lossless, laid out so that an event decodes only what it touches.
//! Every ship is real: a group writes once what its members share, and each member keeps
//! exactly what differs, at the width its information needs.
pub mod bits;
pub mod codec;
pub mod pop;
pub mod program;
pub mod shelf;
