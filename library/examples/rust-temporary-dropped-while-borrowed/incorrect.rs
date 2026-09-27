fn main() {
    let value = Some("hi".to_string());
    let borrowed = value.unwrap().as_str();
    println!("{borrowed}");
}
