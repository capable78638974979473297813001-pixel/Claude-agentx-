package main

import "fmt"

func main() {
	ptrs := []*int{}
	for i := 0; i < 3; i++ {
		ptrs = append(ptrs, &i)
	}
	fmt.Println(*ptrs[0], *ptrs[1], *ptrs[2])
}
