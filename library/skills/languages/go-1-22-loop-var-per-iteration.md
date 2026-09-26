---
id: go-1-22-loop-var-per-iteration
area: languages
topic: go
task: capture-loop-variable
title: Go 1.22 gives each iteration its own loop variable
description: Use when &i inside a for loop prints the same number on Go 1.21 and a different number per element on Go 1.22.
triggers:
  - go loop variable capture
  - for i := 0 prints 3 3 3
  - go 1.22 loop var
  - address of loop index
aliases:
  - go
  - loop
  - closure
related:
  - go-nil-pointer-stored-in-interface
  - rust-temporary-dropped-while-borrowed
sources:
  - https://go.dev/doc/go1.22
commands:
  - python3 library/examples/go-1-22-loop-var-per-iteration/check.py
---

# Go 1.22 gives each iteration its own loop variable

The Go 1.22 release notes change `for` loop variables so each iteration has its own variable. The same `main.go` is compiled twice. The only difference is the `go` line in `go.mod`.

With `go 1.21`, `for i := 0; i < 3; i++` and `append(&i)` prints `3 3 3`. The value is 3, not 2, because `i` increments to 3 before the condition fails, and every pointer aliases that one variable. With `go 1.22` the same program prints `0 1 2`.

`go run .` in this check uses the `go` line in `go.mod`. A `go 1.21` line keeps the old capture on a 1.22 toolchain. Bump that line when you want the per-iteration variable, and re-test goroutines that closed over the index.

## Go 1.21 module

```text file=library/examples/go-1-22-loop-var-per-iteration/old/go.mod
module example.com/loopold

go 1.21
```

## Go 1.22 module

```text file=library/examples/go-1-22-loop-var-per-iteration/new/go.mod
module example.com/loopnew

go 1.22
```

## Loop

```go file=library/examples/go-1-22-loop-var-per-iteration/old/main.go
package main

import "fmt"

func main() {
	ptrs := []*int{}
	for i := 0; i < 3; i++ {
		ptrs = append(ptrs, &i)
	}
	fmt.Println(*ptrs[0], *ptrs[1], *ptrs[2])
}
```

## Verify

Run `python3 library/examples/go-1-22-loop-var-per-iteration/check.py`.

## Sources

- https://go.dev/doc/go1.22
