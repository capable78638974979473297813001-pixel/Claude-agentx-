fn main() {
    let value = Some("hi".to_string());
    let binding = value.unwrap();
    let borrowed = binding.as_str();
    println!("{borrowed}");
}
