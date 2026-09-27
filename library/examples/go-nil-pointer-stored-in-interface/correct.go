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
