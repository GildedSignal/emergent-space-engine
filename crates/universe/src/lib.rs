//! The plane: one star system, whole (docs/plane.md). See the module docs for each foundation.
pub mod bind;
pub mod body;
pub mod calendar;
pub mod ctx;
pub mod dash;
pub mod encounter;
pub mod ext;
pub mod fleet;
pub mod force;
pub mod lorentz;
pub mod num;
pub mod observe;
pub mod prof;
pub mod radial;
pub mod scenario;
pub mod step;
pub mod thrust;
pub mod universe;
pub mod view;
pub mod world;

pub use body::Kind;
pub use ctx::Config;
pub use universe::{Budget, OrbitSpec, Universe};
pub use world::{Mass, Unit};
