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
