---
id: go-nil-pointer-stored-in-interface
area: languages
topic: go
task: detect-typed-nil-interface
title: A nil pointer stored in an interface is not a nil interface
description: Use when a function returns a nil *T as an error or interface and the caller sees i == nil as false.
triggers:
  - typed nil interface
  - nil pointer not nil interface
  - i == nil is false
  - reflect IsNil pointer
aliases:
  - go
  - nil
  - interface
related:
  - go-1-22-loop-var-per-iteration
  - go-http-shutdown-blocks-on-handler
sources:
  - https://go.dev/doc/faq#nil_error
commands:
  - python3 library/examples/go-nil-pointer-stored-in-interface/check.py
---

# A nil pointer stored in an interface is not a nil interface

An interface value is a type pointer plus a data pointer. `var p *int` is a nil pointer. `var i interface{} = p` stores type `*int` and a nil data pointer. `i == nil` is false because the type is set. The FAQ entry "Why is my nil error value not equal to nil?" describes the same pair of words.

The incorrect program prints `typed-nil`. `reflect.Value.IsNil` is valid for Ptr, Map, Slice, Interface, Func, and Chan, and it reports the data pointer. The correct helper prints `nil` for this `*int`.

Return a bare `nil` error, not a nil pointer of a concrete error type assigned to an `error` variable. `var err *MyError; return err` is the usual way to smuggle a typed nil past `if err != nil`.

## Incorrect

```go file=library/examples/go-nil-pointer-stored-in-interface/incorrect.go
package main

import "fmt"

func pointerNil() any {
	var value *int
	return value
}

func main() {
	if pointerNil() == nil {
		fmt.Println("nil")
	} else {
		fmt.Println("typed-nil")
	}
}
```

## Correct

```go file=library/examples/go-nil-pointer-stored-in-interface/correct.go
package main

import (
	"fmt"
	"reflect"
)

func pointerNil() any {
	var value *int
	return value
}

func isNil(value any) bool {
	if value == nil {
		return true
	}
	reflected := reflect.ValueOf(value)
	switch reflected.Kind() {
	case reflect.Ptr, reflect.Map, reflect.Slice, reflect.Interface, reflect.Func, reflect.Chan:
		return reflected.IsNil()
	default:
		return false
	}
}

func main() {
	if isNil(pointerNil()) {
		fmt.Println("nil")
	} else {
		fmt.Println("typed-nil")
	}
}
```

## Verify

Run `python3 library/examples/go-nil-pointer-stored-in-interface/check.py`.

## Sources

- https://go.dev/doc/faq#nil_error
