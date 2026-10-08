fn main() {
    use std::mem::size_of;
    // Public path: BodyRec, Binding, Item are public via emergent_universe::body.
    println!("Scalar            {:>3} B", size_of::<emergent_space::orbit::Scalar>());
    println!("V2                {:>3} B", size_of::<emergent_universe::num::V2>());
    println!("Secondary         {:>3} B", size_of::<emergent_universe::force::Secondary>());
    println!("BodyInfo          {:>3} B", size_of::<emergent_universe::ctx::BodyInfo>());
    println!("Item              {:>3} B", size_of::<emergent_universe::body::Item>());
    println!("Kind              {:>3} B", size_of::<emergent_universe::body::Kind>());
    println!("BodyRec           {:>3} B", size_of::<emergent_universe::body::BodyRec>());
    println!("Binding           {:>3} B", size_of::<emergent_universe::bind::Binding>());
    println!("IntegerState      {:>3} B", size_of::<emergent_space::binding::IntegerState>());
    println!("Trajectory (enum) {:>2} B", size_of::<emergent_space::binding::Trajectory>());
    println!("Update            {:>3} B", size_of::<emergent_universe::step::Update>());
}
