---
id: rust-temporary-dropped-while-borrowed
area: languages
topic: rust
task: bind-temporary-before-borrow
title: value.unwrap().as_str() drops the temporary and rustc reports E0716
description: Use when rustc says temporary value dropped while borrowed on a chain that borrows from unwrap or a function return.
triggers:
  - E0716
  - temporary value dropped while borrowed
  - unwrap as_str
  - rustc let binding suggestion
aliases:
  - rust
  - borrow
  - temporary
related:
  - java-21-switch-null-throws
  - go-1-22-loop-var-per-iteration
sources:
  - https://doc.rust-lang.org/error_codes/E0716.html
commands:
  - python3 library/examples/rust-temporary-dropped-while-borrowed/check.py
---

# value.unwrap().as_str() drops the temporary and rustc reports E0716

`value.unwrap()` returns a `String` temporary. `.as_str()` borrows it. The temporary is dropped at the end of the statement, so the borrow in `borrowed` outlives it. rustc 1.83 reports error `E0716` with the text `temporary value dropped while borrowed`, and the note suggests a `let` binding. The error index page for E0716 is the reference.

Bind the owned string first:

`let owned = value.unwrap();`
`let borrowed = owned.as_str();`

The `let` extends the owner's lifetime to the end of the block, which covers the borrow. Cloning to escape the error works and hides the lifetime; prefer the binding rustc suggests unless you actually need a new allocation.

## Incorrect

```rust file=library/examples/rust-temporary-dropped-while-borrowed/incorrect.rs
fn main() {
    let value = Some("hi".to_string());
    let borrowed = value.unwrap().as_str();
    println!("{borrowed}");
}
```

## Correct

```rust file=library/examples/rust-temporary-dropped-while-borrowed/correct.rs
fn main() {
    let value = Some("hi".to_string());
    let binding = value.unwrap();
    let borrowed = binding.as_str();
    println!("{borrowed}");
}
```

## Verify

Run `python3 library/examples/rust-temporary-dropped-while-borrowed/check.py`.

## Sources

- https://doc.rust-lang.org/error_codes/E0716.html
