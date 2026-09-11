fn main() {
    let report = emergent_law_lab::qualify();
    println!("{}", serde_json::to_string_pretty(&report).expect("finite qualification report"));
}
